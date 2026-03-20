"""Direct Python handler for /reflect jobs.

Bypasses the Claude CLI subprocess and runs graph retrieval + LLM synthesis
(simple mode) or the full TournamentPipeline (deep mode) directly.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Callable

import structlog
import yaml

from gateway.models import Event, Job
from reading_app.text_utils import truncate, truncate_sentences

logger = structlog.get_logger(__name__)

_ID_RE = re.compile(r"[0-9A-Z]{26}")


def _load_voice(config) -> str:
    """Load soul.md voice preamble for narrative output."""
    try:
        from reading_app.memory import MemorySystem
        ms = MemorySystem(Path(config.memory_path))
        return ms.load_voice()
    except Exception:
        return ""

# ---------------------------------------------------------------------------
# Prompt for simple-mode LLM synthesis
# ---------------------------------------------------------------------------
_SIMPLE_SYNTHESIS_PROMPT = """\
You are a research reflection engine. Given a source and its connections in the
knowledge graph, generate novel insights, questions, and cross-domain links.
{voice_section}
## Source
Title: {title}
Summary (excerpt):
{summary_excerpt}

## Claims from this source
{claims_text}

## Graph connections (1-hop and 2-hop)
{connections_text}

## Similar claims from other sources (keyword retrieval)
{similar_text}

## Instructions
1. Identify the most interesting cross-source connections.
2. Surface tensions or contradictions between this source and connected sources.
3. Propose 3-5 novel questions or ideas that arise from these connections.
4. Note any gaps — themes this source touches that have thin coverage.

Be specific: cite source titles and claim texts. Do NOT produce generic summaries.
"""


def handle_reflect_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run reflection directly for a /reflect job.

    Returns:
        Response text with reflection or tournament results.

    Raises:
        ValueError: If source not found or extractions missing.
    """
    text = event.payload.get("text", "")

    # Check for topic mode first: /reflect topic "agent economics"
    topic_match = re.search(r'\btopic\b\s+(.+)', text, re.IGNORECASE)
    if topic_match:
        topic = topic_match.group(1).strip().strip('"\'')
        log = logger.bind(job_id=job.id, mode="topic", topic=topic)
        log.info("reflect_handler_start")
        t0 = time.monotonic()
        result_text = _run_topic_mode(topic, config, executor, log, on_progress)
        elapsed = time.monotonic() - t0
        log.info("reflect_handler_complete", elapsed_s=round(elapsed, 1))
        return result_text

    source_id, deep = _parse_command(text)

    library_path = Path(config.library_path)
    log = logger.bind(job_id=job.id, source_id=source_id, deep=deep)
    log.info("reflect_handler_start")
    t0 = time.monotonic()

    # Validate source directory
    source_dir = library_path / source_id
    extractions_path = source_dir / "extractions.json"
    if not source_dir.is_dir():
        raise ValueError(f"Source directory not found: {source_dir}")
    if not extractions_path.is_file():
        raise ValueError(f"No extractions.json for source {source_id}")

    # Load source data
    title = _load_title(source_dir)
    extractions = json.loads(extractions_path.read_text(encoding="utf-8"))
    summary = _load_summary(source_dir)

    if deep:
        if on_progress:
            on_progress(f"Starting deep tournament for **{title}**...")
        result_text = _run_deep_mode(source_id, title, config, executor, log, on_progress, job=job)
    else:
        if on_progress:
            on_progress(f"Reflecting on **{title}**...")
        result_text = _run_simple_mode(
            source_id, title, extractions, summary, config, executor, log, on_progress,
        )

    # Save result
    reflection_path = source_dir / "reflection.md"
    reflection_path.write_text(result_text, encoding="utf-8")

    elapsed = time.monotonic() - t0
    log.info("reflect_handler_complete", elapsed_s=round(elapsed, 1))

    return result_text


# ---------------------------------------------------------------------------
# Command parsing
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str, bool]:
    """Extract source_id and deep flag from '/reflect <id> [deep]'."""
    m = _ID_RE.search(text)
    if not m:
        raise ValueError(f"No source ID (ULID) found in: {text!r}")
    source_id = m.group(0)
    deep = bool(re.search(r"\bdeep\b", text, re.IGNORECASE))
    return source_id, deep


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def _load_title(source_dir: Path) -> str:
    # Try meta.yaml first
    meta_path = source_dir / "meta.yaml"
    if meta_path.is_file():
        try:
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
            if meta and meta.get("title"):
                return meta["title"]
        except Exception:
            pass
    # Fall back to DB
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            row = conn.execute(
                "SELECT title FROM sources WHERE id = %s", (source_dir.name,)
            ).fetchone()
            if row and row.get("title"):
                return row["title"]
    except Exception:
        pass
    return source_dir.name


def _load_summary(source_dir: Path) -> str:
    summary_path = source_dir / "deep_summary.md"
    if summary_path.is_file():
        return summary_path.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------------------
# Simple mode: graph retrieval + LLM synthesis
# ---------------------------------------------------------------------------

def _run_simple_mode(
    source_id: str,
    title: str,
    extractions: dict,
    summary: str,
    config,
    executor,
    log,
    on_progress: Callable[[str], None] | None,
) -> str:
    from reading_app.db import get_conn, ensure_pool
    from retrieval.graph import GraphRetriever
    from retrieval.hybrid import hybrid_retrieve

    ensure_pool()

    # 1. Query graph
    if on_progress:
        on_progress("Querying knowledge graph...")

    gr = GraphRetriever(get_conn)
    one_hop = gr.one_hop(source_id)
    two_hop_concepts = gr.two_hop_via_concepts(source_id)
    two_hop_claims = gr.two_hop_via_claims(source_id)
    implications = gr.get_source_implications(source_id)

    total_connections = len(one_hop) + len(two_hop_concepts) + len(two_hop_claims) + len(implications)
    log.info("reflect_graph_done", connections=total_connections)
    if on_progress:
        on_progress(f"Found {total_connections} connections. Searching similar claims...")

    # 2. Hybrid keyword search using top claims
    claims = extractions.get("claims", [])
    claim_texts = [c.get("claim_text", "") for c in claims[:5] if c.get("claim_text")]
    query = " ".join(claim_texts)[:500]

    similar = []
    if query.strip():
        try:
            similar = hybrid_retrieve(query, get_conn, k=10)
            # Filter out claims from this source
            similar = [s for s in similar if s.get("source_id") != source_id]
        except Exception:
            log.warning("reflect_hybrid_search_failed", exc_info=True)

    # 3. Build context strings
    connections_parts = []
    if one_hop:
        connections_parts.append("### Direct connections (1-hop)")
        for r in one_hop[:15]:
            connections_parts.append(
                f"- [{r.get('edge_type', '?')}] **{r.get('title', '?')}** — {r.get('explanation', '')[:120]}"
            )
    if two_hop_concepts:
        connections_parts.append("\n### Shared-concept connections (2-hop)")
        for r in two_hop_concepts[:10]:
            concepts = r.get("shared_concepts", [])
            concept_str = ", ".join(concepts) if isinstance(concepts, list) else str(concepts)
            connections_parts.append(
                f"- **{r.get('title', '?')}** via [{concept_str}]"
            )
    if two_hop_claims:
        connections_parts.append("\n### Claim-linked connections (2-hop)")
        for r in two_hop_claims[:10]:
            connections_parts.append(
                f"- [{r.get('edge_type', '?')}] **{r.get('title', '?')}**: "
                f"\"{r.get('our_claim', '')[:80]}\" ↔ \"{r.get('their_claim', '')[:80]}\""
            )
    if implications:
        connections_parts.append("\n### Cross-theme implications")
        for r in implications[:10]:
            connections_parts.append(
                f"- {r.get('source_theme_name', '?')} → {r.get('target_theme_name', '?')}"
            )
    connections_text = "\n".join(connections_parts) if connections_parts else "(no graph connections found)"

    claims_text = "\n".join(
        f"- {truncate_sentences(c.get('claim_text', ''), 250)}" for c in claims[:20]
    ) or "(no claims)"

    similar_text = "\n".join(
        f"- [{s.get('source_title', '?')}] {truncate_sentences(s.get('claim_text', ''), 250)}"
        for s in similar[:10]
    ) or "(no similar claims found)"

    summary_excerpt = summary[:2000] if summary else "(no summary available)"

    # 4. LLM synthesis
    if on_progress:
        on_progress("Generating reflection...")

    voice = _load_voice(config)
    voice_section = f"\n## Voice & Personality\n{voice}" if voice else ""

    prompt = _SIMPLE_SYNTHESIS_PROMPT.format(
        title=title,
        summary_excerpt=summary_excerpt,
        claims_text=claims_text,
        connections_text=connections_text,
        similar_text=similar_text,
        voice_section=voice_section,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="reflect_simple",
            timeout=120,
        )
        text = result.text
    except Exception as e:
        log.error("reflect_simple_llm_failed", error=str(e)[:200])
        return f"Reflection synthesis failed: {str(e)[:200]}"

    # Guard against empty or binary output
    if not text or not text.strip():
        log.warning("reflect_simple_empty_output")
        return (
            f"# Reflection — {title}\n\n"
            f"LLM synthesis returned empty output.\n\n"
            f"**Data retrieved:**\n"
            f"- Graph connections: {total_connections}\n"
            f"- Similar claims from other sources: {len(similar)}\n"
            f"- Source claims used: {len(claim_texts)}\n\n"
            f"Try running `/reflect {source_id} deep` for tournament-based reflection."
        )

    # Prepend data summary for transparency
    header = (
        f"# Reflection — {title}\n"
        f"*Graph: {total_connections} connections, "
        f"{len(similar)} cross-source claims*\n\n"
    )
    return header + text


# ---------------------------------------------------------------------------
# Deep mode: full tournament pipeline
# ---------------------------------------------------------------------------

def _run_deep_mode(
    source_id: str,
    title: str,
    config,
    executor,
    log,
    on_progress: Callable[[str], None] | None,
    job: Job | None = None,
) -> str:
    from reading_app.db import get_conn, ensure_pool
    from agents.tournament import TournamentPipeline, TournamentResult
    from agents.generate import TournamentGoal
    from gateway.run_stages import StageTracker, REFLECT_DEEP_STAGES

    ensure_pool()

    # Initialize structured stage tracker
    tracker = StageTracker(REFLECT_DEEP_STAGES, on_progress=on_progress)
    if job:
        _emit_reflect_stages(job, tracker)

    # Get source themes
    theme_ids = []
    try:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT theme_id FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
            theme_ids = [r["theme_id"] for r in rows]
    except Exception:
        log.warning("reflect_theme_lookup_failed", exc_info=True)

    if on_progress and theme_ids:
        on_progress(f"Themes: {', '.join(theme_ids)}")

    # Build goal
    goal = TournamentGoal(
        description=f"Generate novel ideas from source: {title}",
        focus_themes=theme_ids or None,
    )

    # Run tournament
    pipeline = TournamentPipeline(
        executor=executor,
        get_conn_fn=get_conn,
        library_path=Path(config.library_path),
    )

    # Stage progress callback
    def _on_tournament_step(step: int, step_name: str):
        stage_map = {
            1: "retrieve", 2: "retrieve",
            3: "generate", 4: "generate",
            5: "novelty",
            6: "critique",
            7: "debate",
            8: "debate",
            9: "evolve",
            10: "rank", 11: "rank",
        }
        stage_key = stage_map.get(step)
        if not stage_key:
            return
        prev_key = stage_map.get(step - 1) if step > 1 else None
        if prev_key and prev_key != stage_key:
            tracker.complete(prev_key)
        tracker.start(stage_key, step_name)
        if job:
            _emit_reflect_stages(job, tracker)

    tracker.start("retrieve", "Running tournament pipeline...")
    if job:
        _emit_reflect_stages(job, tracker)

    result: TournamentResult = pipeline.run(
        source_id=source_id,
        depth="deep",
        goal=goal,
        timeout=840,
        on_step=_on_tournament_step,
    )

    # Complete all stages
    for stage_key in ("retrieve", "generate", "novelty", "critique", "debate", "evolve", "rank"):
        stage = tracker._stage_map.get(stage_key)
        if stage and stage.status in ("pending", "running"):
            if result.steps_completed >= 11:
                stage.complete()
            else:
                stage.skip()
    if job:
        _emit_reflect_stages(job, tracker)

    if on_progress:
        on_progress(
            f"Tournament complete: {result.ideas_generated} generated → "
            f"{result.ideas_after_novelty} novel → {len(result.ideas)} final"
        )

    # Format result
    return _format_tournament_result(result, title)


def _format_tournament_result(result: TournamentResult, title: str) -> str:
    """Format TournamentResult into a readable response."""
    lines = [f"# Reflection (deep) — {title}\n"]

    lines.append(
        f"**Pipeline**: {result.ideas_generated} generated → "
        f"{result.ideas_after_novelty} novel → "
        f"{result.ideas_after_debate} debated → "
        f"{len(result.ideas)} final"
    )
    lines.append(f"**Steps completed**: {result.steps_completed}/11")
    lines.append(f"**Total LLM calls**: {result.total_calls}")
    if result.call_limit_hit:
        lines.append("*(call limit exceeded — results may be truncated)*")
    lines.append("")

    for i, idea in enumerate(result.ideas, 1):
        score = idea.get("overall_score", 0)
        idea_type = idea.get("idea_type", "?")
        lines.append(f"## Idea {i} [{idea_type}] (score: {score:.2f})\n")
        lines.append(idea.get("idea_text", "(no text)"))
        lines.append("")

        if idea.get("rationale"):
            lines.append(f"**Rationale**: {idea['rationale']}")
        if idea.get("testability"):
            lines.append(f"**Testability**: {idea['testability']}")
        if idea.get("grounding"):
            grounding = idea["grounding"]
            if isinstance(grounding, list):
                snippets = [g.get("snippet", "")[:80] for g in grounding[:3]]
                lines.append(f"**Grounding**: {'; '.join(snippets)}")
        lines.append("")

    if not result.ideas:
        lines.append("No novel ideas survived the tournament pipeline.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Topic mode: cross-source idea generation
# ---------------------------------------------------------------------------

_TOPIC_SYNTHESIS_PROMPT = """\
You are generating novel research ideas by synthesizing claims across multiple sources
on a specific topic.
{voice_section}
## Topic: {topic}

## Sources and Claims
{sources_text}

## Landscape Context
{landscape_text}

## Current Bottlenecks
{bottlenecks_text}

## Instructions

Generate 5-8 novel ideas that emerge from cross-source synthesis on this topic.
Use all 6 idea strategies:
1. **Synthesis**: Combine insights from 2+ sources into something neither says alone
2. **Transfer**: Apply a method/insight from one source's domain to another's
3. **Contradiction**: Find tensions between sources and propose resolutions
4. **Extension**: Push a finding to its logical extreme
5. **Bottleneck**: Identify what's blocking progress and propose unblocking strategies
6. **Implications**: Trace downstream effects across themes

For each idea:
- Reference specific claims from specific sources (by source title and claim text)
- Explain why this is novel (not already stated in any single source)
- Suggest how it could be tested or validated

Be specific and grounded. Every idea must cite evidence from at least 2 different sources.
"""


def _emit_reflect_stages(job: Job, tracker):
    """Emit structured stages to the job queue."""
    try:
        from gateway.queue import Queue, DEFAULT_QUEUE_DB_PATH
        q = Queue(db_path=DEFAULT_QUEUE_DB_PATH)
        q.update_job_progress(
            job.id,
            tracker.progress_text(),
            stages=tracker.to_list(),
        )
    except Exception:
        pass


def _run_topic_mode(
    topic: str,
    config,
    executor,
    log,
    on_progress: Callable[[str], None] | None,
) -> str:
    """Generate a structured report across all sources for a topic.

    Uses the report generator with analytical lenses for outline-first generation.
    Falls back to legacy single-pass synthesis on failure.
    """
    from reading_app.db import get_conn, ensure_pool

    ensure_pool()

    if on_progress:
        on_progress(f"Generating report for **{topic}**...")

    # Try new report generator flow
    try:
        from agents.report_generator import run_report

        state = run_report(
            topic=topic,
            get_conn_fn=get_conn,
            executor=executor,
            on_progress=on_progress,
            library_path=Path(config.library_path),
        )

        if state.final_markdown and len(state.final_markdown) > 100:
            return state.final_markdown
    except Exception:
        log.warning("report_generator_failed_fallback_to_legacy", exc_info=True)

    # Fallback: legacy single-pass synthesis
    result = _run_topic_mode_legacy(topic, config, executor, log, on_progress)

    # Persist synthesis claims even from the legacy path
    _persist_synthesis_claims(topic, result, get_conn, executor, log)

    return result


def _persist_synthesis_claims(
    topic: str,
    text: str,
    get_conn_fn,
    executor,
    log,
) -> None:
    """Extract key conclusions from legacy topic synthesis and persist as synthesis claims."""
    if not text or len(text) < 200:
        return

    try:
        from reading_app.db import insert_claim, ensure_pool
        from reading_app.embeddings import embed_batch
        from ulid import ULID

        ensure_pool()

        prompt = f"""Extract 3-5 key conclusions from this report. Each conclusion should be
a standalone claim that captures a non-obvious insight from the analysis.

Report:
{text[:6000]}

Return ONLY a JSON array of objects with "claim" and "evidence" fields.
Example: [{{"claim": "...", "evidence": "..."}}]"""

        result = executor.run_raw(prompt, session_id="legacy_conclusions", timeout=60)
        if not result.text:
            return

        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if not json_match:
            return

        conclusions = json.loads(json_match.group(0))
        if not isinstance(conclusions, list):
            return

        report_source_id = f"report_{topic.lower().replace(' ', '_')[:30]}"

        with get_conn_fn() as conn:
            existing = conn.execute(
                "SELECT id FROM sources WHERE id = %s", (report_source_id,)
            ).fetchone()
            if not existing:
                conn.execute(
                    """INSERT INTO sources (id, source_type, title, processing_status)
                       VALUES (%s, 'synthesis', %s, 'complete')
                       ON CONFLICT (id) DO NOTHING""",
                    (report_source_id, f"Report: {topic}"),
                )
                conn.commit()

        valid_conclusions = [
            c for c in conclusions[:5]
            if c.get("claim") and len(c.get("claim", "")) >= 10
        ]
        texts = [c["claim"] for c in valid_conclusions]
        embeddings = embed_batch(texts) if texts else []

        for i, conclusion in enumerate(valid_conclusions):
            claim_text = conclusion["claim"]
            emb = embeddings[i] if i < len(embeddings) and embeddings[i] else None
            insert_claim(
                id=f"syn_{ULID()}",
                source_id=report_source_id,
                claim_text=claim_text,
                claim_type="synthesis_conclusion",
                section=f"report:{topic}",
                confidence=0.6,
                evidence_snippet=conclusion.get("evidence", "")[:500],
                evidence_type="synthesis",
                embedding=emb,
                provenance_type="synthesis",
            )

        log.info("legacy_synthesis_claims_persisted", count=len(valid_conclusions), topic=topic)
    except Exception:
        log.warning("legacy_synthesis_claims_failed", exc_info=True)


def _run_topic_mode_legacy(
    topic: str,
    config,
    executor,
    log,
    on_progress: Callable[[str], None] | None,
) -> str:
    """Legacy single-pass topic synthesis (fallback)."""
    from reading_app.db import get_conn
    from retrieval.landscape import get_bottleneck_ranking
    from retrieval.hybrid import hybrid_retrieve

    if on_progress:
        on_progress(f"Searching sources for **{topic}**...")

    # Find relevant sources via theme match and hybrid search
    with get_conn() as conn:
        # Get theme matches
        themes = conn.execute(
            """SELECT t.id, t.name, t.state_summary
               FROM themes t
               WHERE t.name ILIKE %s OR t.id = %s
               ORDER BY t.velocity DESC NULLS LAST LIMIT 5""",
            (f"%{topic}%", topic),
        ).fetchall()

        theme_ids = [t["id"] for t in themes]

        # Get sources for matching themes
        sources = []
        if theme_ids:
            sources = conn.execute(
                """SELECT s.id, s.title, s.source_type,
                      array_agg(DISTINCT t.name) AS theme_names
                   FROM sources s
                   JOIN source_themes st ON s.id = st.source_id
                   JOIN themes t ON st.theme_id = t.id
                   WHERE st.theme_id = ANY(%s)
                   GROUP BY s.id, s.title, s.source_type, s.ingested_at
                   ORDER BY s.ingested_at DESC NULLS LAST
                   LIMIT 20""",
                (theme_ids,),
            ).fetchall()

        # Get claims for these sources
        source_ids = [s["id"] for s in sources]
        claims_by_source = {}

        if source_ids:
            all_claims = conn.execute(
                """SELECT c.id, c.claim_text, c.source_id, c.confidence,
                      c.evidence_snippet, s.title AS source_title
                   FROM claims c
                   JOIN sources s ON c.source_id = s.id
                   WHERE c.source_id = ANY(%s)
                     AND c.confidence >= 0.4
                   ORDER BY c.confidence DESC""",
                (source_ids,),
            ).fetchall()

            for c in all_claims:
                sid = c["source_id"]
                claims_by_source.setdefault(sid, []).append(c)

    # Also search via hybrid retrieval for claims matching the topic
    extra_claims = []
    try:
        extra_claims = hybrid_retrieve(topic, get_conn, k=15)
    except Exception as e:
        log.debug("topic_hybrid_search_failed", error=str(e)[:100])

    if not sources and not extra_claims:
        return (
            f"**No sources found for topic \"{topic}\"**\n\n"
            f"Try a broader topic, or check available themes with `/themes`."
        )

    # Build sources text
    sources_text_parts = []
    for s in sources[:15]:
        sid = s["id"]
        claims = claims_by_source.get(sid, [])[:8]
        themes_str = ", ".join(s.get("theme_names") or [])
        sources_text_parts.append(f"### {s['title']} ({themes_str})")
        for c in claims:
            sources_text_parts.append(
                f"- {truncate_sentences(c['claim_text'], 250)} (conf: {c.get('confidence', '?')})"
            )
        sources_text_parts.append("")

    # Add extra claims from hybrid search
    if extra_claims:
        sources_text_parts.append("### Additional claims (hybrid search)")
        seen = set()
        for c in extra_claims:
            if c.get("source_id") in {s["id"] for s in sources}:
                continue
            key = c.get("claim_text", "")[:80]
            if key in seen:
                continue
            seen.add(key)
            sources_text_parts.append(
                f"- [{c.get('source_title', c.get('source_id', '?'))}] "
                f"{truncate_sentences(c.get('claim_text', ''), 250)}"
            )

    sources_text = "\n".join(sources_text_parts) or "(no claims found)"

    # Landscape context
    landscape_parts = []
    for t in themes:
        if t.get("state_summary"):
            landscape_parts.append(
                f"**{t['name']}**: {truncate_sentences(t['state_summary'], 500)}"
            )
    landscape_text = "\n".join(landscape_parts) or "(no landscape context)"

    # Bottlenecks
    bottlenecks = []
    for tid in theme_ids:
        bottlenecks.extend(get_bottleneck_ranking(theme_id=tid)[:3])
    bottlenecks_text = "\n".join(
        f"- {b['description']} (horizon: {b.get('resolution_horizon', '?')}, "
        f"blocking: {truncate(b.get('blocking_what', '?'), 175)})"
        for b in bottlenecks[:8]
    ) or "(no bottlenecks)"

    # LLM synthesis
    if on_progress:
        on_progress(
            f"Generating cross-source ideas ({len(sources)} sources, "
            f"{sum(len(v) for v in claims_by_source.values())} claims)..."
        )

    voice = _load_voice(config)
    voice_section = f"\n## Voice & Personality\n{voice}" if voice else ""

    prompt = _TOPIC_SYNTHESIS_PROMPT.format(
        topic=topic,
        sources_text=sources_text,
        landscape_text=landscape_text,
        bottlenecks_text=bottlenecks_text,
        voice_section=voice_section,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="reflect_topic",
            timeout=180,
        )
        text = result.text
    except Exception as e:
        log.error("reflect_topic_llm_failed", error=str(e)[:200])
        return f"Topic reflection failed: {str(e)[:200]}"

    if not text or not text.strip():
        return f"Topic reflection for \"{topic}\" returned empty output."

    header = (
        f"# Cross-Source Reflection — {topic}\n"
        f"*{len(sources)} sources, "
        f"{sum(len(v) for v in claims_by_source.values())} claims, "
        f"{len(themes)} themes*\n\n"
    )
    return header + text
