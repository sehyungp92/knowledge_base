"""Direct Python handler for /ask jobs.

Performs hybrid retrieval (vector + keyword) over the claims table,
then delegates synthesis to executor.run_raw(). Falls back to
formatted raw results if the LLM call fails.
"""

from __future__ import annotations

import re
import time
from typing import Callable

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_ask_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /ask directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("ask_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    question = _parse_command(text)
    if not question:
        return "Usage: `/ask <your question>`\n\nExample: `/ask what are the main bottlenecks in robotics?`"

    log = log.bind(question=question[:80])

    # Check for report follow-up context
    report_answer = _try_report_followup(question, config, executor, log, on_progress)
    if report_answer is not None:
        elapsed = time.monotonic() - t0
        log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="report_followup")
        return report_answer

    # Check for structured queries before doing hybrid retrieval
    structured = _try_structured_query(question, log)
    if structured is not None:
        elapsed = time.monotonic() - t0
        log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="structured")
        return structured

    # Classify complexity to decide whether to use lenses
    is_complex = _is_complex_question(question)
    log = log.bind(complex=is_complex)

    if is_complex:
        return _handle_complex_question(question, config, executor, log, on_progress, t0)

    if on_progress:
        on_progress(f"Searching knowledge base for: {question[:60]}...")

    # Retrieve relevant claims via hybrid search
    claims = _retrieve_claims(question, log)

    if not claims:
        return (
            f"**No relevant evidence found** for: *{question}*\n\n"
            "The knowledge base doesn't have sources that address this question yet. "
            "Try `/save <url>` to ingest relevant sources first."
        )

    # Graph expansion: follow edges from top sources to bring in connected evidence
    claims = _expand_via_graph(claims, log)

    if on_progress:
        on_progress(f"Found {len(claims)} relevant claims, synthesizing answer...")

    # Gather wiki context for richer synthesis (best-effort)
    wiki_block = ""
    graph_block = ""
    theme_ids_for_filing: list[str] = []
    try:
        from retrieval.wiki_retrieval import gather_wiki_context, format_wiki_context_block
        wctx = gather_wiki_context(
            query=question, max_pages=3,
            include_entities=True, include_sources=True,
        )
        if wctx.theme_narratives:
            wiki_block = format_wiki_context_block(
                wctx, header="Thematic Context", max_chars_per_theme=2000,
            )
            theme_ids_for_filing = list(wctx.theme_narratives.keys())
    except Exception:
        log.debug("ask_wiki_context_failed", exc_info=True)

    # Graph structural context (bridge concepts, implications, contradictions)
    try:
        from retrieval.graph_context import query_graph_context, format_graph_context_block
        gctx = query_graph_context(query=question, theme_ids=theme_ids_for_filing)
        graph_block = format_graph_context_block(gctx, max_chars=1500)
        if graph_block:
            log.info("ask_graph_context", **gctx.stats)
    except Exception:
        log.debug("ask_graph_context_failed", exc_info=True)

    # Load voice for narrative output
    voice = _load_voice(config)

    # Try LLM synthesis
    combined_context = wiki_block
    if graph_block:
        combined_context = (combined_context + "\n\n" + graph_block) if combined_context else graph_block
    answer = _synthesize_with_llm(question, claims, executor, log, voice=voice, wiki_context=combined_context)
    if answer:
        # File answer to wiki (best-effort, background)
        if len(answer) > 200:
            try:
                import threading

                def _wiki_file():
                    try:
                        from reading_app.db import ensure_pool
                        from retrieval.wiki_writer import create_question_page
                        ensure_pool()
                        page = create_question_page(question, answer, theme_ids_for_filing)
                        if page and on_progress:
                            on_progress("_Wiki updated: question page filed._")
                    except Exception:
                        logger.warning("ask_wiki_filing_failed", question=question[:80], exc_info=True)

                threading.Thread(target=_wiki_file).start()
            except Exception:
                logger.warning("ask_wiki_thread_spawn_failed", exc_info=True)

        elapsed = time.monotonic() - t0
        log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="llm")
        return answer

    # Fallback: format raw results
    log.info("ask_handler_llm_fallback")
    answer = _format_raw_results(question, claims)

    elapsed = time.monotonic() - t0
    log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="fallback")
    return answer


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> str | None:
    """Parse '/ask <question>'. Returns the question or None."""
    cleaned = text.strip()
    for prefix in ("/ask ", "/ask"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break
    return cleaned if cleaned else None


# ---------------------------------------------------------------------------
# Report follow-up detection
# ---------------------------------------------------------------------------

def _try_report_followup(question, config, executor, log, on_progress) -> str | None:
    """Check if a recent report exists and answer in its context if so."""
    try:
        from pathlib import Path
        from gateway.report_followup_handler import find_recent_report_state, handle_report_followup
        from reading_app.db import get_conn

        library_path = Path(config.library_path)
        report_state = find_recent_report_state(library_path)
        if report_state is None:
            return None

        log.info("report_followup_detected", topic=report_state.get("topic", ""))
        return handle_report_followup(
            question=question,
            report_state=report_state,
            get_conn_fn=get_conn,
            executor=executor,
            on_progress=on_progress,
        )
    except Exception:
        log.debug("report_followup_check_failed", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Complexity classification (heuristic, no LLM)
# ---------------------------------------------------------------------------

_COMPLEX_KEYWORDS = {
    "why", "how", "implications", "impact", "consequences", "relationship",
    "compare", "contrast", "difference", "connection", "between",
    "across", "landscape", "state of", "trajectory", "trend",
    "bottleneck", "limitation", "breakthrough",
}


def _is_complex_question(question: str) -> bool:
    """Heuristic complexity classifier: multi-clause or analytical keywords → complex."""
    q_lower = question.lower()

    # Multi-clause detection
    clause_markers = [" and ", " but ", " while ", " whereas ", " because ", " since "]
    clause_count = sum(1 for m in clause_markers if m in q_lower)
    if clause_count >= 1:
        return True

    # Analytical keyword detection
    keyword_hits = sum(1 for kw in _COMPLEX_KEYWORDS if kw in q_lower)
    if keyword_hits >= 2:
        return True

    # Long questions tend to be complex
    if len(question.split()) > 15:
        return True

    return False


def _handle_complex_question(question, config, executor, log, on_progress, t0) -> str:
    """Handle complex questions using analytical lenses with query decomposition."""
    from reading_app.db import get_conn
    from retrieval.lenses import (
        evidence_lens, panorama_lens,
        format_lens_results_for_prompt,
    )

    if on_progress:
        on_progress(f"Complex question detected. Decomposing and running analytical lenses...")

    # Get embedding for vector search
    embedding = None
    try:
        from reading_app.embeddings import embed_batch
        embedding = embed_batch([question])[0]
    except Exception:
        log.debug("embedding_failed_keyword_only")

    # Run decomposed Evidence + Panorama lenses in parallel (using threads)
    from concurrent.futures import ThreadPoolExecutor, as_completed

    lens_results = []

    def _run_evidence():
        # Use decomposition-enhanced retrieval for complex questions
        from retrieval.hybrid import decompose_and_retrieve
        from retrieval.lenses import LensResult
        try:
            claims = decompose_and_retrieve(
                question, get_conn, executor, embedding=embedding, k=15,
            )
        except Exception:
            log.debug("decompose_and_retrieve_failed_fallback", exc_info=True)
            return evidence_lens(question, get_conn, embedding=embedding, k=15)

        if not claims:
            return evidence_lens(question, get_conn, embedding=embedding, k=15)

        # Build LensResult from decomposed claims (same format as evidence_lens)
        evidence_items = []
        citations = set()
        for c in claims:
            sid = c.get("source_id", "")
            citations.add(sid)
            evidence_items.append({
                "claim_text": c.get("claim_text", c.get("claim", "")),
                "evidence_snippet": c.get("evidence_snippet", ""),
                "source_id": sid,
                "source_title": c.get("source_title", ""),
                "confidence": c.get("claim_confidence", c.get("confidence")),
                "rrf_score": c.get("rrf_score", 0),
            })

        summary_parts = [f"Found {len(claims)} relevant claims across {len(citations)} sources (decomposed query)."]
        for item in evidence_items[:5]:
            sid = item["source_id"]
            title = item["source_title"] or sid[:12]
            summary_parts.append(f"- [{sid[:12]}] {title}: {item['claim_text'][:120]}")

        avg_score = sum(c.get("rrf_score", 0) for c in claims) / len(claims) if claims else 0
        confidence = min(1.0, avg_score * 30)

        return LensResult(
            lens_id="evidence",
            query=question,
            summary="\n".join(summary_parts),
            confidence=confidence,
            citations=list(citations),
            evidence_items=evidence_items,
        )

    def _run_panorama():
        return panorama_lens(question, get_conn)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(_run_evidence), pool.submit(_run_panorama)]
        for future in as_completed(futures):
            try:
                lens_results.append(future.result())
            except Exception:
                log.debug("lens_call_failed", exc_info=True)

    if not lens_results or all(lr.confidence < 0.05 for lr in lens_results):
        log.info("ask_handler_lenses_empty_fallback")
        # Fallback to simple retrieval
        claims = _retrieve_claims(question, log)
        if not claims:
            return (
                f"**No relevant evidence found** for: *{question}*\n\n"
                "The knowledge base doesn't have sources that address this question yet."
            )
        claims = _expand_via_graph(claims, log)
        voice = _load_voice(config)
        answer = _synthesize_with_llm(question, claims, executor, log, voice=voice)
        if answer:
            elapsed = time.monotonic() - t0
            log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="lens_fallback")
            return answer
        return _format_raw_results(question, claims)

    if on_progress:
        total_evidence = sum(len(lr.evidence_items) for lr in lens_results)
        on_progress(f"Found {total_evidence} evidence items across {len(lens_results)} lenses, synthesizing...")

    # Build combined context from lenses
    lens_context = format_lens_results_for_prompt(lens_results)

    # Load voice
    voice = _load_voice(config)
    voice_section = f"\n## Voice & Personality\n{voice}\n" if voice else ""

    prompt = f"""You are a research assistant answering a complex question using multi-perspective evidence.
{voice_section}

## Question
{question}

## Multi-Lens Evidence
{lens_context}

## Instructions
1. Synthesize an answer that draws on ALL relevant lenses — direct evidence, landscape context, and connections.
2. Cite sources using [source_id] inline.
3. Address multiple dimensions of the question (implications, limitations, trajectory where relevant).
4. Note contradictions, uncertainty, or coverage gaps if present.
5. If certain lenses found nothing, note what's missing.

## Format
{{Multi-paragraph answer with [source_id] citations, organized by dimension}}

Sources:
- [source_id] "claim text" — {{relevant snippet}}
"""

    try:
        result = executor.run_raw(
            prompt,
            session_id="ask_lens_synthesis",
            timeout=120,
        )
        if result.text and len(result.text) > 20:
            # File answer to wiki (best-effort, background) — same pattern as simple path
            if len(result.text) > 200:
                try:
                    import threading

                    answer_text = result.text

                    def _wiki_file_complex():
                        try:
                            from reading_app.db import ensure_pool
                            from retrieval.wiki_writer import create_question_page, extract_theme_ids_from_text
                            ensure_pool()
                            theme_ids = extract_theme_ids_from_text(question)
                            page = create_question_page(question, answer_text, theme_ids)
                            if page and on_progress:
                                on_progress("_Wiki updated: question page filed._")
                        except Exception:
                            logger.debug(
                                "ask_complex_wiki_filing_failed", question=question[:80], exc_info=True,
                            )

                    threading.Thread(target=_wiki_file_complex).start()
                except Exception:
                    pass

            elapsed = time.monotonic() - t0
            log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="lens")
            return result.text
    except Exception as e:
        log.warning("ask_lens_synthesis_failed", error=str(e)[:200])

    # Fallback: format lens results directly
    elapsed = time.monotonic() - t0
    log.info("ask_handler_complete", elapsed_s=round(elapsed, 1), mode="lens_raw")
    return f"**Evidence for:** *{question}*\n\n{lens_context}"


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def _retrieve_claims(question: str, log) -> list[dict]:
    """Hybrid retrieval: vector + keyword search over claims."""
    from reading_app.db import get_conn
    from retrieval.hybrid import hybrid_retrieve

    # Try to get embedding for vector search
    embedding = None
    try:
        from reading_app.embeddings import embed_batch
        embedding = embed_batch([question])[0]
    except Exception:
        log.debug("embedding_failed_keyword_only")

    try:
        with get_conn() as conn:
            results = hybrid_retrieve(
                query=question,
                get_conn_fn=lambda: conn,
                embedding=embedding,
                k=15,
                temporal_decay=False,
            )
        log.info("ask_retrieval_done", count=len(results))
        return results
    except Exception as e:
        log.error("ask_retrieval_failed", error=str(e)[:200])
        return []


# ---------------------------------------------------------------------------
# Graph expansion
# ---------------------------------------------------------------------------

def _expand_via_graph(claims: list[dict], log) -> list[dict]:
    """Expand retrieval results by following graph edges from top source hits.

    Takes the top source IDs from initial retrieval, finds their graph neighbours,
    and pulls in additional claims from connected sources that weren't in the
    initial results. This surfaces corroborating and contradicting evidence.
    """
    try:
        from reading_app.db import get_conn
        from retrieval.graph import GraphRetriever

        # Get unique source IDs from top claims
        seen_sources = set()
        top_sources = []
        for c in claims[:10]:
            sid = c.get("source_id")
            if sid and sid not in seen_sources:
                seen_sources.add(sid)
                top_sources.append(sid)

        if not top_sources:
            return claims

        with get_conn() as conn:
            retriever = GraphRetriever(lambda: conn)
            neighbour_ids: set[str] = set()

            # Get 1-hop neighbours for top 3 sources
            for sid in top_sources[:3]:
                neighbours = retriever.one_hop(sid)
                for n in neighbours:
                    nid = n.get("source_id") or n.get("id")
                    if nid and nid not in seen_sources:
                        neighbour_ids.add(nid)

            if not neighbour_ids:
                return claims

            # Pull claims from graph neighbours (up to 5 extra claims)
            placeholders = ",".join(["%s"] * len(neighbour_ids))
            extra_rows = conn.execute(
                f"""SELECT c.id, c.claim_text AS claim, c.evidence_snippet,
                       c.source_id, c.claim_type, c.confidence
                FROM claims c
                WHERE c.source_id IN ({placeholders})
                ORDER BY c.confidence DESC
                LIMIT 5""",
                tuple(neighbour_ids),
            ).fetchall()

            existing_ids = {c.get("id") for c in claims}
            graph_claims = []
            for r in extra_rows:
                if r["id"] not in existing_ids:
                    graph_claims.append({
                        **dict(r),
                        "text": r["claim"],
                        "retrieval_source": "graph_expansion",
                    })

            if graph_claims:
                log.info("graph_expansion", extra_claims=len(graph_claims), neighbour_sources=len(neighbour_ids))
                return claims + graph_claims

    except Exception as e:
        log.debug("graph_expansion_skipped", error=str(e)[:100])

    return claims


# ---------------------------------------------------------------------------
# LLM synthesis
# ---------------------------------------------------------------------------

def _load_voice(config) -> str:
    """Load soul.md voice preamble for narrative output."""
    try:
        from pathlib import Path
        from reading_app.memory import MemorySystem
        ms = MemorySystem(Path(config.memory_path))
        return ms.load_voice()
    except Exception:
        return ""


def _synthesize_with_llm(question: str, claims: list[dict], executor, log, *, voice: str = "", wiki_context: str = "") -> str | None:
    """Use executor.run_raw() to synthesize an answer from retrieved claims."""
    # Format claims for the prompt
    evidence_block = _format_evidence_for_prompt(claims)

    voice_section = f"\n## Voice & Personality\n{voice}\n" if voice else ""

    wiki_section = ""
    if wiki_context:
        wiki_section = f"""
## Thematic Context
The following wiki narratives provide broader context for the themes relevant to this question.
Use this to ground your answer in the landscape of what is known.

{wiki_context}
"""

    prompt = f"""You are a research assistant answering a question using the evidence provided below.
{voice_section}

## Question
{question}
{wiki_section}
## Retrieved Evidence
{evidence_block}

## Instructions
1. Answer the question directly, grounding every statement in the retrieved evidence and thematic context above.
2. Cite sources using [source_id] inline.
3. Note contradictions or uncertainty if present.
4. If the evidence is insufficient, say so.

## Format
{{Answer paragraph(s) with [source_id] citations}}

Sources:
- [source_id] "claim text" — {{relevant snippet}}
"""

    try:
        result = executor.run_raw(
            prompt,
            session_id="ask_synthesis",
            timeout=90,
        )
        if result.text and len(result.text) > 20:
            return result.text
        log.warning("ask_llm_empty_response")
        return None
    except Exception as e:
        log.warning("ask_llm_failed", error=str(e)[:200])
        return None


# ---------------------------------------------------------------------------
# Fallback formatting
# ---------------------------------------------------------------------------

def _format_evidence_for_prompt(claims: list[dict]) -> str:
    """Format claims as numbered evidence items for the LLM prompt."""
    lines = []
    for i, c in enumerate(claims, 1):
        source_id = c.get("source_id", "?")
        claim_text = c.get("claim", c.get("text", "?"))
        evidence = c.get("evidence_snippet", "")
        score = c.get("rrf_score", 0)
        line = f"{i}. [{source_id}] {claim_text}"
        if evidence:
            line += f'\n   Evidence: "{evidence}"'
        lines.append(line)
    return "\n\n".join(lines)


def _format_raw_results(question: str, claims: list[dict]) -> str:
    """Format raw retrieval results as a readable answer (no LLM)."""
    lines = [f"**Evidence for:** *{question}*\n"]

    # Group by source
    by_source: dict[str, list[dict]] = {}
    for c in claims:
        sid = c.get("source_id", "unknown")
        by_source.setdefault(sid, []).append(c)

    lines.append(f"Found **{len(claims)} claims** across **{len(by_source)} sources**:\n")

    for source_id, source_claims in list(by_source.items())[:8]:
        # Get source title if available
        title = _get_source_title(source_id)
        header = f"**[{source_id[:12]}]** {title}" if title else f"**[{source_id[:12]}]**"
        lines.append(header)

        for c in source_claims[:3]:
            claim_text = c.get("claim", c.get("text", "?"))
            evidence = c.get("evidence_snippet", "")
            lines.append(f"- {claim_text}")
            if evidence:
                lines.append(f'  > "{_truncate(evidence, 150)}"')
        lines.append("")

    lines.append(
        "---\n"
        "*Results shown as raw retrieval (LLM synthesis unavailable). "
        "Evidence is ranked by relevance.*"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Structured query engine
# ---------------------------------------------------------------------------

# Patterns that trigger structured mode (natural language → DB query)
_STRUCTURED_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Bottlenecks queries
    (re.compile(r"\b(show|list|find|what are|get).{0,30}bottleneck", re.I), "bottlenecks"),
    (re.compile(r"\bbottleneck.{0,40}(horizon|timeline|year|month|in\s)", re.I), "bottlenecks"),
    (re.compile(r"\bhow many.{0,20}bottleneck", re.I), "bottlenecks"),
    # Anticipations/predictions queries
    (re.compile(r"\b(show|list|find|which|get).{0,30}(anticipation|prediction)", re.I), "anticipations"),
    (re.compile(r"\b(anticipation|prediction).{0,40}(evidence|month|recent|this year|in\s)", re.I), "anticipations"),
    (re.compile(r"\bopen (prediction|anticipation)", re.I), "anticipations"),
    (re.compile(r"\bhow many.{0,20}(anticipation|prediction)", re.I), "anticipations"),
    # Capabilities queries
    (re.compile(r"\b(show|list|find|get).{0,30}(capabilit)", re.I), "capabilities"),
    (re.compile(r"\bcapabilit.{0,40}(mature|emerging|experimental|theme|in\s)", re.I), "capabilities"),
    (re.compile(r"\bhow many.{0,20}capabilit", re.I), "capabilities"),
    # Limitations queries
    (re.compile(r"\b(show|list|find|get).{0,30}limitation", re.I), "limitations"),
    (re.compile(r"\blimitation.{0,40}(blocking|significant|architectural|compute|behavioral|evaluation|in\s)", re.I), "limitations"),
    (re.compile(r"\bhow many.{0,20}limitation", re.I), "limitations"),
    # Breakthroughs queries
    (re.compile(r"\b(show|list|find|get|recent).{0,30}breakthrough", re.I), "breakthroughs"),
    (re.compile(r"\bhow many.{0,20}breakthrough", re.I), "breakthroughs"),
    # Beliefs queries
    (re.compile(r"\b(show|list|find|get|what are).{0,30}belief", re.I), "beliefs"),
    (re.compile(r"\bhow many.{0,20}belief", re.I), "beliefs"),
    # Cross-theme implications
    (re.compile(r"\b(show|list|find|get).{0,30}(cross.?theme|implication)", re.I), "implications"),
    # Coverage/stats
    (re.compile(r"\b(coverage|gap|theme).{0,30}(thin|missing|no source|empty)", re.I), "coverage"),
    (re.compile(r"\b(stats|statistics|summary|overview) (of |for )?(the )?(knowledge base|library|db)", re.I), "stats"),
    (re.compile(r"\b(knowledge base|library|db) (stats|statistics|summary|overview)", re.I), "stats"),
]

# Horizon extraction
_HORIZON_RE = re.compile(
    r"(<|within|less than|under|before|by|next)\s*(\d+)\s*(year|month|yr|mo)s?", re.I
)
# Theme extraction — captures mixed-case names like "Embodied AI", stops at common boundaries
_THEME_RE = re.compile(
    r"\b(for|in|about|on|related to|within)\s+"
    r"([A-Za-z][A-Za-z0-9 &\-/]{2,50}?)"
    r"(?:\s+theme|\s+area|\s+domain|\s*\??\s*$)",
    re.I,
)


def _try_structured_query(question: str, log) -> str | None:
    """Return a formatted structured answer if the question matches a known pattern, else None."""
    entity = None
    for pattern, etype in _STRUCTURED_PATTERNS:
        if pattern.search(question):
            entity = etype
            break
    if entity is None:
        return None

    log.info("structured_query_detected", entity=entity)
    try:
        return _run_structured_query(entity, question, log)
    except Exception as e:
        log.warning("structured_query_failed", error=str(e)[:200])
        return None  # fall through to normal retrieval


def _extract_horizon_months(question: str) -> int | None:
    """Extract a horizon constraint in months from the query text."""
    m = _HORIZON_RE.search(question)
    if not m:
        return None
    value = int(m.group(2))
    unit = m.group(3).lower()
    if unit.startswith("year") or unit == "yr":
        return value * 12
    return value  # months


def _extract_theme_hint(question: str) -> str | None:
    """Extract an optional theme keyword from the query text."""
    m = _THEME_RE.search(question)
    if m:
        return m.group(2).strip()
    return None


def _run_structured_query(entity: str, question: str, log) -> str:
    """Execute a structured DB query and format results as markdown."""
    from reading_app.db import get_conn

    q_lower = question.lower()

    with get_conn() as conn:
        if entity == "bottlenecks":
            return _query_bottlenecks(conn, question, q_lower, log)
        elif entity == "anticipations":
            return _query_anticipations(conn, question, q_lower, log)
        elif entity == "capabilities":
            return _query_capabilities(conn, question, q_lower, log)
        elif entity == "limitations":
            return _query_limitations(conn, question, q_lower, log)
        elif entity == "breakthroughs":
            return _query_breakthroughs(conn, question, q_lower, log)
        elif entity == "beliefs":
            return _query_beliefs(conn, question, q_lower, log)
        elif entity == "implications":
            return _query_implications(conn, question, q_lower, log)
        elif entity == "coverage":
            return _query_coverage(conn, log)
        elif entity == "stats":
            return _query_stats(conn, log)
    return ""


def _query_bottlenecks(conn, question: str, q_lower: str, log) -> str:
    theme_hint = _extract_theme_hint(question)
    params: list = []
    where = ""
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    # Wire up horizon filter: "bottlenecks within 2 years"
    horizon_months = _extract_horizon_months(question)
    if horizon_months is not None:
        # Map months to resolution_horizon enum values
        if horizon_months <= 6:
            where += " AND b.resolution_horizon = 'months'"
        elif horizon_months <= 24:
            where += " AND b.resolution_horizon IN ('months', '1-2_years')"
        elif horizon_months <= 60:
            where += " AND b.resolution_horizon IN ('months', '1-2_years', '3-5_years')"

    # Bottleneck type filter
    for btype in ("compute", "data", "algorithmic", "hardware", "theoretical", "regulatory", "integration"):
        if btype in q_lower:
            where += " AND b.bottleneck_type = %s"
            params.append(btype)
            break

    sql = f"""
        SELECT b.description, b.resolution_horizon, b.bottleneck_type,
               b.confidence, b.blocking_what, t.name AS theme_name
        FROM bottlenecks b
        LEFT JOIN themes t ON b.theme_id = t.id
        WHERE 1=1{where}
        ORDER BY b.confidence DESC NULLS LAST LIMIT 20
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_bottlenecks", count=len(rows))

    if not rows:
        return "**No bottlenecks found** matching those criteria."

    qualifiers = []
    if theme_hint:
        qualifiers.append(f"in {theme_hint}")
    if horizon_months:
        qualifiers.append(f"within {horizon_months} months")
    qualifier_str = f" ({', '.join(qualifiers)})" if qualifiers else ""

    lines = [f"**Bottlenecks{qualifier_str}** ({len(rows)} results)\n"]
    for r in rows:
        btype = r["bottleneck_type"] or "general"
        horizon = r["resolution_horizon"] or "unknown"
        theme = r["theme_name"] or "General"
        blocking = (r["blocking_what"] or "")[:80]
        desc = (r["description"] or "")[:200]
        line = f"- **[{theme}]** `{btype}` - {desc}\n  Horizon: {horizon}"
        if blocking:
            line += f" | Blocking: {blocking}"
        lines.append(line)
    return "\n".join(lines)


def _query_anticipations(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = ""

    if "open" in q_lower or "unanswered" in q_lower:
        where += " AND a.status = 'open'"
    elif "confirmed" in q_lower or "verified" in q_lower:
        where += " AND a.status = 'confirmed'"
    elif "disconfirmed" in q_lower or "falsified" in q_lower:
        where += " AND a.status = 'disconfirmed'"

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    if "high confidence" in q_lower or "most likely" in q_lower:
        order = " ORDER BY a.confidence DESC"
    else:
        order = " ORDER BY a.created_at DESC"

    sql = f"""
        SELECT a.prediction, a.confidence, a.timeline, a.status,
               a.created_at, t.name AS theme_name
        FROM anticipations a
        LEFT JOIN themes t ON a.theme_id = t.id
        WHERE 1=1{where}{order}
        LIMIT 15
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_anticipations", count=len(rows))

    if not rows:
        return "**No anticipations found** matching those criteria."

    qualifier = f" in {theme_hint}" if theme_hint else ""
    lines = [f"**Anticipations{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        theme = r["theme_name"] or "General"
        conf = f"{(r['confidence'] or 0)*100:.0f}%"
        status = r["status"] or "open"
        timeline = r["timeline"] or "?"
        pred = (r["prediction"] or "")[:180]
        lines.append(f"- **[{theme}]** _{status}_ | conf: {conf} | {timeline}\n  {pred}")
    return "\n".join(lines)


def _query_capabilities(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = ""

    if "mature" in q_lower or "production" in q_lower:
        where += " AND c.maturity = 'mature'"
    elif "emerging" in q_lower:
        where += " AND c.maturity = 'emerging'"
    elif "experimental" in q_lower or "research" in q_lower:
        where += " AND c.maturity IN ('experimental', 'research')"

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    sql = f"""
        SELECT c.description, c.maturity, c.confidence, t.name AS theme_name
        FROM capabilities c
        LEFT JOIN themes t ON c.theme_id = t.id
        WHERE 1=1{where}
        ORDER BY c.last_updated DESC NULLS LAST
        LIMIT 15
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_capabilities", count=len(rows))

    if not rows:
        return "**No capabilities found** matching those criteria."

    qualifier = f" in {theme_hint}" if theme_hint else ""
    lines = [f"**Capabilities{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        theme = r["theme_name"] or "General"
        maturity = r["maturity"] or "?"
        desc = (r["description"] or "")[:200]
        lines.append(f"- **[{theme}]** `{maturity}` - {desc}")
    return "\n".join(lines)


def _query_limitations(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = " AND l.severity != 'pruned'"

    # Type filter — includes behavioral/evaluation from quality recalibration
    _LIM_TYPES = ("architectural", "compute", "data", "engineering", "theoretical", "behavioral", "evaluation")
    for ltype in _LIM_TYPES:
        if ltype in q_lower:
            where += " AND l.limitation_type = %s"
            params.append(ltype)
            break

    if "blocking" in q_lower or "critical" in q_lower:
        where += " AND l.severity = 'blocking'"
    elif "significant" in q_lower or "major" in q_lower:
        where += " AND l.severity = 'significant'"

    # Signal strength filter
    if "grounded" in q_lower:
        where += " AND l.signal_strength = 'grounded'"
    elif "speculative" in q_lower:
        where += " AND l.signal_strength = 'speculative'"

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    sql = f"""
        SELECT l.description, l.limitation_type, l.severity, l.signal_strength,
               t.name AS theme_name
        FROM limitations l
        LEFT JOIN themes t ON l.theme_id = t.id
        WHERE 1=1{where}
        ORDER BY
            CASE l.severity WHEN 'blocking' THEN 1 WHEN 'significant' THEN 2 ELSE 3 END,
            CASE l.signal_strength WHEN 'grounded' THEN 1 WHEN 'moderate' THEN 2 ELSE 3 END
        LIMIT 15
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_limitations", count=len(rows))

    if not rows:
        return "**No limitations found** matching those criteria."

    qualifier = f" in {theme_hint}" if theme_hint else ""
    lines = [f"**Limitations{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        theme = r["theme_name"] or "General"
        ltype = r["limitation_type"] or "unknown"
        severity = r["severity"] or "?"
        signal = r["signal_strength"] or "moderate"
        desc = (r["description"] or "")[:200]
        lines.append(f"- **[{theme}]** `{ltype}` _{severity}_ ({signal}) - {desc}")
    return "\n".join(lines)


def _query_breakthroughs(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = ""

    if "recent" in q_lower or "this month" in q_lower or "latest" in q_lower:
        where += " AND b.detected_at >= NOW() - INTERVAL '90 days'"

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    # Semantic ordering instead of lexicographic sort on significance text
    sql = f"""
        SELECT b.description, b.what_is_now_possible, b.significance,
               t.name AS theme_name, b.detected_at
        FROM breakthroughs b
        LEFT JOIN themes t ON b.theme_id = t.id
        WHERE 1=1{where}
        ORDER BY
            CASE b.significance
                WHEN 'paradigm_shifting' THEN 1
                WHEN 'major' THEN 2
                WHEN 'notable' THEN 3
                WHEN 'incremental' THEN 4
                ELSE 5
            END,
            b.detected_at DESC NULLS LAST
        LIMIT 12
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_breakthroughs", count=len(rows))

    if not rows:
        return "**No breakthroughs found** matching those criteria."

    qualifier = f" in {theme_hint}" if theme_hint else ""
    lines = [f"**Breakthroughs{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        theme = r["theme_name"] or "General"
        sig = r["significance"] or "?"
        desc = (r["description"] or "")[:180]
        what_possible = (r["what_is_now_possible"] or "")[:120]
        entry = f"- **[{theme}]** _{sig}_ - {desc}"
        if what_possible:
            entry += f"\n  Now possible: {what_possible}"
        lines.append(entry)
    return "\n".join(lines)


def _query_beliefs(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = ""

    if "active" in q_lower:
        where += " AND b.status = 'active'"
    elif "resolved" in q_lower:
        where += " AND b.status = 'resolved'"

    if "predictive" in q_lower:
        where += " AND b.belief_type = 'predictive'"
    elif "methodological" in q_lower:
        where += " AND b.belief_type = 'methodological'"
    elif "factual" in q_lower:
        where += " AND b.belief_type = 'factual'"

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND LOWER(t.name) LIKE %s"
        params.append(f"%{theme_hint.lower()}%")

    sql = f"""
        SELECT b.claim, b.confidence, b.status, b.belief_type,
               t.name AS theme_name
        FROM beliefs b
        LEFT JOIN themes t ON b.domain_theme_id = t.id
        WHERE 1=1{where}
        ORDER BY b.confidence DESC, b.last_updated DESC
        LIMIT 15
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_beliefs", count=len(rows))

    if not rows:
        return "**No beliefs found** matching those criteria."

    qualifier = f" in {theme_hint}" if theme_hint else ""
    lines = [f"**Beliefs{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        theme = r["theme_name"] or "General"
        conf = f"{(r['confidence'] or 0)*100:.0f}%"
        status = r["status"] or "active"
        btype = r["belief_type"] or "factual"
        claim = (r["claim"] or "")[:200]
        lines.append(f"- **[{theme}]** `{btype}` _{status}_ (conf: {conf}) - {claim}")
    return "\n".join(lines)


def _query_implications(conn, question: str, q_lower: str, log) -> str:
    params: list = []
    where = ""

    theme_hint = _extract_theme_hint(question)
    if theme_hint:
        where += " AND (LOWER(st.name) LIKE %s OR LOWER(tt.name) LIKE %s)"
        params.extend([f"%{theme_hint.lower()}%", f"%{theme_hint.lower()}%"])

    sql = f"""
        SELECT c.implication, c.confidence, c.trigger_type,
               st.name AS source_theme, tt.name AS target_theme,
               c.attribution
        FROM cross_theme_implications c
        LEFT JOIN themes st ON c.source_theme_id = st.id
        LEFT JOIN themes tt ON c.target_theme_id = tt.id
        WHERE 1=1{where}
        ORDER BY c.confidence DESC NULLS LAST, c.created_at DESC
        LIMIT 15
    """
    rows = conn.execute(sql, params).fetchall() if params else conn.execute(sql).fetchall()
    log.info("structured_implications", count=len(rows))

    if not rows:
        return "**No cross-theme implications found** matching those criteria."

    qualifier = f" involving {theme_hint}" if theme_hint else ""
    lines = [f"**Cross-Theme Implications{qualifier}** ({len(rows)} results)\n"]
    for r in rows:
        src = r["source_theme"] or "?"
        tgt = r["target_theme"] or "?"
        conf = f"{(r['confidence'] or 0)*100:.0f}%"
        imp = (r["implication"] or "")[:200]
        attr = r["attribution"] or "automated"
        lines.append(f"- **{src}** → **{tgt}** (conf: {conf}, {attr})\n  {imp}")
    return "\n".join(lines)


def _query_coverage(conn, log) -> str:
    rows = conn.execute("""
        SELECT t.name, COUNT(DISTINCT s.id) AS source_count,
               COUNT(DISTINCT c.id) AS claim_count
        FROM themes t
        LEFT JOIN source_themes st ON st.theme_id = t.id
        LEFT JOIN sources s ON s.id = st.source_id
        LEFT JOIN claims c ON c.source_id = s.id
        GROUP BY t.id, t.name
        HAVING COUNT(DISTINCT s.id) < 3
        ORDER BY COUNT(DISTINCT s.id) ASC
        LIMIT 15
    """).fetchall()
    log.info("structured_coverage", thin_themes=len(rows))

    if not rows:
        return "All themes have adequate source coverage (≥3 sources each)."

    lines = ["**Thin coverage themes** (fewer than 3 sources)\n"]
    for r in rows:
        name = r["name"]
        sc = r["source_count"]
        cc = r["claim_count"]
        lines.append(f"- **{name}** — {sc} source{'s' if sc != 1 else ''}, {cc} claims")

    return "\n".join(lines)


def _query_stats(conn, log) -> str:
    # Single query for all table counts instead of N round-trips
    row = conn.execute("""
        SELECT
            (SELECT COUNT(*) FROM sources) AS sources,
            (SELECT COUNT(*) FROM claims) AS claims,
            (SELECT COUNT(*) FROM capabilities) AS capabilities,
            (SELECT COUNT(*) FROM limitations) AS limitations,
            (SELECT COUNT(*) FROM limitations WHERE severity != 'pruned') AS active_limitations,
            (SELECT COUNT(*) FROM bottlenecks) AS bottlenecks,
            (SELECT COUNT(*) FROM breakthroughs) AS breakthroughs,
            (SELECT COUNT(*) FROM anticipations) AS anticipations,
            (SELECT COUNT(*) FROM source_edges) AS source_edges,
            (SELECT COUNT(*) FROM themes) AS themes,
            (SELECT COUNT(*) FROM beliefs) AS beliefs,
            (SELECT COUNT(DISTINCT id) FROM (
                SELECT DISTINCT source_a AS id FROM source_edges
                UNION
                SELECT DISTINCT source_b AS id FROM source_edges
            ) x) AS connected_sources
    """).fetchone()

    sources = row["sources"]
    caps = row["capabilities"]
    active_lims = row["active_limitations"]
    connected = row["connected_sources"]

    lines = [
        "**Knowledge Base Overview**\n",
        f"- **Sources**: {sources:,} ({connected} connected via graph)",
        f"- **Claims**: {row['claims']:,}",
        f"- **Capabilities**: {caps:,}",
        f"- **Limitations**: {active_lims:,} active ({row['limitations']:,} total)",
        f"- **Bottlenecks**: {row['bottlenecks']:,}",
        f"- **Breakthroughs**: {row['breakthroughs']:,}",
        f"- **Anticipations**: {row['anticipations']:,}",
        f"- **Beliefs**: {row['beliefs']:,}",
        f"- **Source edges**: {row['source_edges']:,}",
        f"- **Themes**: {row['themes']:,}",
    ]
    if caps:
        lines.append(f"\nLimitation:capability ratio: {active_lims/caps:.2f}:1")
    if sources:
        lines.append(f"Graph coverage: {connected}/{sources} sources = {connected/sources*100:.1f}%")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_source_title(source_id: str) -> str | None:
    """Look up source title."""
    from reading_app.db import get_conn
    try:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT title FROM sources WHERE id = %s", (source_id,)
            ).fetchone()
            return row["title"] if row else None
    except Exception:
        return None


def _truncate(s: str, n: int) -> str:
    return s[:n] + "..." if len(s) > n else s
