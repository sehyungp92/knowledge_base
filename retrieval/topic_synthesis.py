"""Topic synthesis report generation.

Consolidates multiple sources on a topic into a structured report integrating
deep summaries, landscape signals, and cross-theme implications.

Inspired by gpt-researcher patterns:
- Sub-query decomposition for broader source recall
- Evidence snippet loading for concrete, quotable facts
- Opinion-forming synthesis prompt with contradiction surfacing
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

from reading_app import db
from reading_app.embeddings import embed_batch
from retrieval.hybrid import hybrid_retrieve
from retrieval.landscape import get_consolidated_implications

logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(__file__).resolve().parent.parent / "library"
SYNTHESES_DIR = LIBRARY_DIR / "syntheses"
MERGES_DIR = LIBRARY_DIR / "merges"

# ---------------------------------------------------------------------------
# Adaptive sub-query generation
# ---------------------------------------------------------------------------

# Topic-type detection keywords (checked against query + matched theme names)
_STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "and", "but", "if", "or", "because", "until", "while", "about",
    "what", "which", "who", "how", "all", "each", "some", "no", "not",
}

_TREND_SIGNALS = {"death", "end", "decline", "rise", "shift", "disruption", "replacement",
                  "future", "collapse", "boom", "emergence", "transformation"}
_CONCEPT_SIGNALS = {"tax", "paradox", "problem", "hypothesis", "theory", "principle",
                    "law", "effect", "dilemma", "tradeoff", "trade-off"}
_RESEARCH_SIGNALS = {"model", "models", "learning", "training", "architecture",
                     "benchmark", "scaling", "reasoning", "alignment", "safety"}

# Facet templates by topic type
_FACETS_PRODUCT = [
    "{topic}",
    "{topic} how it works architecture design",
    "{topic} limitations problems weaknesses risks",
    "{topic} implications consequences downstream effects",
    "{topic} compared to alternatives competitors vs",
]
_FACETS_TREND = [
    "{topic}",
    "evidence supporting {topic}",
    "evidence against {topic} counterarguments criticism",
    "what is driving {topic} causes reasons",
    "{topic} implications consequences what it means",
]
_FACETS_RESEARCH = [
    "{topic}",
    "{topic} key results breakthroughs state of the art",
    "{topic} open problems limitations bottlenecks",
    "{topic} connections implications for other areas",
    "{topic} recent advances progress 2025 2026",
]
_FACETS_CONCEPT = [
    "{topic}",
    "{topic} definition examples what it means",
    "arguments for {topic} evidence supporting",
    "arguments against {topic} criticism counterexamples",
    "{topic} implications practical consequences",
]
_FACETS_DEFAULT = [
    "{topic}",
    "{topic} key findings main ideas",
    "{topic} limitations problems open questions",
    "{topic} implications connections related topics",
]

# ---------------------------------------------------------------------------
# Synthesis prompt
# ---------------------------------------------------------------------------

SYNTHESIS_PROMPT = """You are generating a topic synthesis report that consolidates multiple sources into a single structured understanding.

Your role is that of an expert research analyst specialising in AI. You must determine your own concrete assessment based on the evidence — do NOT defer to generic or meaningless conclusions. When sources disagree, say so explicitly and explain why.

## Topic: {topic}

{analysis_section}## Sources ({source_count} total)

{sources_block}

## Deep Summaries (full per-source analysis)

{summaries_block}

## Key Evidence (verbatim claims with provenance)

{evidence_block}

## Landscape Signals (structured database records)

### Capabilities
{capabilities_block}

### Limitations
{limitations_block}

### Bottlenecks
{bottlenecks_block}

## Cross-Theme Implications (consolidated across sources)

{implications_block}

## Active Anticipations (testable predictions)

{anticipations_block}

---

## Instructions

Produce a structured synthesis report in this exact format. Every factual claim must cite its source(s).

# Topic Synthesis: {topic}

Based on {{count}} sources ingested between {{date_range}}.

## What It Is
{{2-3 paragraphs explaining what this topic/technology/concept is. Synthesize ACROSS sources — do NOT summarize each one sequentially. Cite specific sources inline as [Source N: "Title"]. Include concrete facts and numbers where available.}}

## What Makes It Different
{{Bullet points with **bold labels** identifying the key differentiators or novel contributions. Each must cite at least one source. Focus on what distinguishes this from related work or alternatives.}}

## Core Capabilities
{{Draw from both the capabilities table AND claims/evidence. Order by maturity. For each: description, maturity level, confidence, and supporting evidence. Prioritise capabilities backed by concrete data (benchmarks, numbers, demonstrations) over vague claims.}}

## Key Limitations
{{Draw from both the limitations table AND claims/evidence. Order by severity. For each: description, type, trajectory, and supporting evidence. IMPORTANT: Limitations are the most valuable signal. Include implicit limitations (hedging language, controlled conditions, conspicuous absences, scale/cost barriers) alongside explicit ones. If sources are suspiciously optimistic about an area, flag it.}}

## Where Sources Disagree
{{Explicit contradictions, tensions, or different framings between sources. For each: what source A says vs. what source B says, and your assessment of which has stronger evidence. If no disagreements exist, say so and explain why the convergence is (or isn't) meaningful.}}

## Cross-Theme Implications

### Obvious Connections
{{High-confidence implications (>= 0.7) that are direct/expected. Include observation count and confidence. Explain briefly why each matters.}}

### Non-Obvious Connections
{{Lower-confidence or surprising implications. These are the most valuable section — connections that aren't immediately apparent. Explain the reasoning chain for each.}}

## Open Questions
{{Specific, answerable questions that remain unresolved. Include:
- Gaps in coverage (what aspects haven't been examined?)
- Untested anticipations (predictions that need evidence)
- Areas where confidence is low and more sources would help
- Conspicuous absences (what would you expect to find but don't?)}}

---

VOICE AND ATTRIBUTION — these are absolute:
- State findings as direct facts, results, and open questions.
- NEVER reference sources meta-textually. Forbidden patterns: "according to", "one study found", "the authors argue", "Source A claims", "the paper shows", "research suggests".
- Where contradictions exist, present them as open tensions in the field — not as source disagreements. Example: "Whether X scales beyond Y remains unresolved — results at 7B parameters show Z [Source 1: "Title"], while larger-scale experiments suggest the opposite [Source 2: "Title"]."

CRITICAL RULES:
- Synthesize ACROSS sources. Do NOT write sequential source summaries.
- Cite specific sources inline: [Source N: "Title"]
- Include concrete facts, numbers, statistics, and quotes wherever available.
- Separate obvious from non-obvious implications — explain the reasoning for non-obvious ones.
- Limitations and open questions are MORE valuable than capabilities — invest depth there.
- Form your own concrete opinion based on the evidence. Do NOT defer to vague conclusions.
- Identify gaps — what questions remain unanswered? What's suspiciously absent?
- Keep the report focused and specific — no generic statements.
"""


SYNTHESIS_QUALITY_CHECK_PROMPT = """Rate this topic synthesis report on "{topic}" on three criteria.

## Report
{report}
{ground_truth_section}
---

Score each 1-5 (1=poor, 5=excellent):

SOURCE_INTEGRATION: Does it synthesize across sources into unified analysis — or read like sequential source summaries?
  Score 2: "Source A found X. Source B found Y. Source C argues Z." (sequential)
  Score 4: "X is well-established [1][2], though Y remains contested — 7B-scale results diverge from larger experiments [3]." (integrated)

SPECIFICITY: Does it name concrete capabilities, benchmarks, and results — or use vague generalities?
  Score 2: "Several models show improved performance on benchmarks." (vague)
  Score 4: "GPT-4o scores 88.7% on MMLU while Gemini Ultra reaches 90.0%, though both plateau on ARC-AGI." (concrete)
{specificity_guidance}
ANALYTICAL_DEPTH: Does it form original assessments, surface contradictions, and identify gaps — or just restate source claims?
  Score 2: "The technology has strengths and weaknesses. More research is needed." (surface)
  Score 4: "The 7B-scale results are promising but the absence of any evaluation beyond English is conspicuous — the claimed 'multilingual capability' rests on architecture similarity, not demonstrated performance." (original analysis)

Return ONLY three lines:
SOURCE_INTEGRATION: N
SPECIFICITY: N
ANALYTICAL_DEPTH: N
"""


def _score_synthesis(
    report: str,
    topic: str,
    executor,
    entity_names: list[str] | None = None,
) -> float | None:
    """Score a synthesis report on quality dimensions. Returns average score (1-5) or None on parse failure."""
    ground_truth_section = ""
    specificity_guidance = ""
    if entity_names:
        ground_truth_section = (
            "\n## Ground Truth Entities\n"
            + ", ".join(entity_names[:30])
            + "\n"
        )
        specificity_guidance = (
            "  Score 4-5 only if the report references entities from the ground truth list. "
            "Score 1-2 if it uses vague generalities or names entities not in the list.\n"
        )

    prompt = SYNTHESIS_QUALITY_CHECK_PROMPT.format(
        topic=topic,
        report=report,
        ground_truth_section=ground_truth_section,
        specificity_guidance=specificity_guidance,
    )
    session_id = f"synthesis_quality_{hashlib.md5(topic.encode()).hexdigest()[:8]}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="haiku",
            timeout=15,
        )
        text = result.text.strip()

        scores = {}
        for line in text.splitlines():
            for key in ("SOURCE_INTEGRATION", "SPECIFICITY", "ANALYTICAL_DEPTH"):
                if line.strip().startswith(key):
                    m = re.search(r"(\d)", line.split(":", 1)[-1])
                    if m:
                        val = int(m.group(1))
                        if 1 <= val <= 5:
                            scores[key] = val

        if len(scores) < 3:
            logger.debug("Synthesis quality check parse incomplete for %s: %s", topic, scores)
            return None

        return sum(scores.values()) / len(scores)
    except Exception:
        logger.debug("Synthesis quality check failed for %s", topic, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


def _validate_synthesis_quality(
    report: str,
    topic: str,
    executor,
    entity_names: list[str] | None = None,
) -> tuple[bool, str, float | None]:
    """Check if synthesis report meets quality standards.

    Returns (passes, feedback, avg_score). Passes if average score >= 3.
    """
    avg = _score_synthesis(report, topic, executor, entity_names)
    if avg is None:
        return True, "", None  # Can't parse — accept

    if avg >= 3:
        return True, "", avg

    feedback = (
        f"Quality scores averaged {avg:.1f}/5. "
        "Rewrite by integrating across sources rather than summarizing sequentially, "
        "using concrete facts, and forming original analytical assessments."
    )
    return False, feedback, avg


MERGE_PROMPT = """You are writing a standalone professional knowledge report that integrates information from {source_count} sources into a unified narrative.

## Topic: {topic}

## References

{references_block}

## Deep Summaries

{summaries_block}

## Key Evidence

{evidence_block}

## Landscape Signals

### Capabilities
{capabilities_block}

### Limitations
{limitations_block}

### Bottlenecks
{bottlenecks_block}

## Cross-Theme Implications

{implications_block}

---

## Instructions

Write a standalone professional report. The reader should be able to read this as an authoritative document without needing to consult any external material.

**Voice and attribution rules — these are absolute:**
- State findings as direct facts, results, and open questions.
- NEVER reference sources meta-textually. Forbidden patterns: "according to", "one study found", "the authors argue", "Source A claims", "the paper shows", "research suggests", "sources agree/disagree".
- Where multiple sources provide evidence for the same point, just state the point with inline citations: "Transformer architectures achieve state-of-the-art performance on X [1][2]."
- Where contradictions exist, present them as open tensions in the field — not as source disagreements. Example: "Whether X scales beyond Y remains unresolved — results at the 7B scale show Z [1], while larger-scale experiments indicate the opposite [2]."

**Citation format:**
- Use light inline `[1]` superscript-style citations for traceability.
- Multiple citations: `[1][3]` (no comma, no space between).
- End the report with a `## References` section listing `[N] Title (date)`.

**Structure:**
- Follow the natural logical structure of the content, NOT per-source sections.
- Use descriptive section headings that reflect the actual content.
- Open with a concise overview paragraph, then develop the main themes.
- Close with open questions and unresolved tensions.

**Content priorities:**
- Concrete facts, numbers, benchmarks, and results over generalities.
- Limitations, failure modes, and open problems are MORE valuable than capabilities.
- Non-obvious connections between the material in different sources.
- What remains unknown or untested.
"""


def _slugify(text: str) -> str:
    """Convert topic text to filesystem-safe slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "_", slug).strip("_")
    return slug[:80]


def _classify_topic_type(query: str) -> str:
    """Classify a topic into a type for facet selection.

    Uses keyword heuristics against the query text. No LLM call needed.
    Returns: 'product', 'trend', 'research', 'concept', or 'default'.
    """
    words = set(query.lower().split())

    if words & _TREND_SIGNALS:
        return "trend"
    if words & _CONCEPT_SIGNALS:
        return "concept"
    if words & _RESEARCH_SIGNALS:
        return "research"

    # Check if query matches a known theme name (suggests research area)
    try:
        with db.get_conn() as conn:
            match = conn.execute(
                "SELECT id FROM themes WHERE id ILIKE %s OR name ILIKE %s LIMIT 1",
                (f"%{query}%", f"%{query}%"),
            ).fetchone()
            if match:
                return "research"
    except Exception:
        pass

    # Short queries that match source titles are likely products/projects
    if len(words) <= 3:
        try:
            with db.get_conn() as conn:
                match = conn.execute(
                    "SELECT id FROM sources WHERE title ILIKE %s LIMIT 1",
                    (f"%{query}%",),
                ).fetchone()
                if match:
                    return "product"
        except Exception:
            pass

    # Short, proper-noun-like queries are likely products/projects
    if len(words) <= 2 and any(w[0].isupper() for w in query.split() if w):
        return "product"

    return "default"


def _generate_sub_queries(query: str) -> list[str]:
    """Generate topic-appropriate sub-queries via heuristic classification.

    Detects whether the topic is a product, trend, research area, or concept
    and selects facet templates accordingly. Zero-latency — no LLM call.
    """
    topic_type = _classify_topic_type(query)

    facets = {
        "product": _FACETS_PRODUCT,
        "trend": _FACETS_TREND,
        "research": _FACETS_RESEARCH,
        "concept": _FACETS_CONCEPT,
        "default": _FACETS_DEFAULT,
    }[topic_type]

    sub_queries = [f.format(topic=query) for f in facets]
    logger.info("Topic '%s' classified as %s — %d sub-queries", query, topic_type, len(sub_queries))
    return sub_queries


def _find_relevant_sources(query: str) -> list[dict]:
    """Find sources matching the query via adaptive multi-facet retrieval.

    Classifies the topic type (product, trend, research area, concept) and
    generates appropriate sub-queries for each. E.g. for "death of SaaS"
    it searches for evidence, counterarguments, drivers, and implications.
    """
    source_map: dict[str, dict] = {}

    # 1. Adaptive multi-facet hybrid retrieval on claims
    sub_queries = _generate_sub_queries(query)
    embeddings = embed_batch(sub_queries) if sub_queries else []
    for sq, embedding in zip(sub_queries, embeddings):
        try:
            claims = hybrid_retrieve(
                query=sq,
                get_conn_fn=db.get_conn,
                embedding=embedding,
                k=15,
            )
            for claim in claims:
                sid = claim.get("source_id")
                if sid and sid not in source_map:
                    source_map[sid] = {
                        "source_id": sid,
                        "title": claim.get("source_title", ""),
                        "published_at": claim.get("published_at"),
                    }
        except Exception:
            logger.debug("Hybrid retrieval failed for sub-query: %s", sq, exc_info=True)

    # 2. Theme-scoped source lookup
    try:
        with db.get_conn() as conn:
            themes = conn.execute(
                """SELECT id, name FROM themes
                   WHERE id ILIKE %s OR name ILIKE %s""",
                (f"%{query}%", f"%{query}%"),
            ).fetchall()

            for theme in themes:
                rows = conn.execute(
                    """SELECT s.id, s.title, s.published_at
                       FROM sources s
                       JOIN source_themes st ON s.id = st.source_id
                       WHERE st.theme_id = %s""",
                    (theme["id"],),
                ).fetchall()
                for r in rows:
                    if r["id"] not in source_map:
                        source_map[r["id"]] = {
                            "source_id": r["id"],
                            "title": r.get("title", ""),
                            "published_at": r.get("published_at"),
                        }
    except Exception:
        logger.warning("Theme-scoped source lookup failed", exc_info=True)

    # 3. Keyword-search source titles (full phrase + individual keywords)
    try:
        with db.get_conn() as conn:
            rows = conn.execute(
                """SELECT id, title, published_at FROM sources
                   WHERE title ILIKE %s""",
                (f"%{query}%",),
            ).fetchall()
            for r in rows:
                if r["id"] not in source_map:
                    source_map[r["id"]] = {
                        "source_id": r["id"],
                        "title": r.get("title", ""),
                        "published_at": r.get("published_at"),
                    }

            # Also try individual significant keywords in titles
            keywords = [w for w in query.split() if len(w) > 3 and w.lower() not in _STOP_WORDS]
            for kw in keywords:
                kw_rows = conn.execute(
                    """SELECT id, title, published_at FROM sources
                       WHERE title ILIKE %s""",
                    (f"%{kw}%",),
                ).fetchall()
                for r in kw_rows:
                    if r["id"] not in source_map:
                        source_map[r["id"]] = {
                            "source_id": r["id"],
                            "title": r.get("title", ""),
                            "published_at": r.get("published_at"),
                        }
    except Exception:
        logger.debug("Title search failed", exc_info=True)

    # 4. Fallback: per-keyword FTS if multi-word AND query returned nothing
    if not source_map:
        keywords = [w for w in query.split() if len(w) > 3 and w.lower() not in _STOP_WORDS]
        try:
            with db.get_conn() as conn:
                for kw in keywords:
                    rows = conn.execute(
                        """SELECT DISTINCT c.source_id AS id, s.title, s.published_at
                           FROM claims c JOIN sources s ON c.source_id = s.id
                           WHERE c.fts_vector @@ websearch_to_tsquery('english', %s)
                           LIMIT 10""",
                        (kw,),
                    ).fetchall()
                    for r in rows:
                        if r["id"] not in source_map:
                            source_map[r["id"]] = {
                                "source_id": r["id"],
                                "title": r.get("title", ""),
                                "published_at": r.get("published_at"),
                            }
        except Exception:
            logger.debug("Keyword FTS fallback failed", exc_info=True)

    # 5. Fallback: per-keyword theme search
    if not source_map:
        keywords = [w for w in query.split() if len(w) > 3 and w.lower() not in _STOP_WORDS]
        try:
            with db.get_conn() as conn:
                for kw in keywords:
                    themes = conn.execute(
                        "SELECT id FROM themes WHERE id ILIKE %s OR name ILIKE %s",
                        (f"%{kw}%", f"%{kw}%"),
                    ).fetchall()
                    for theme in themes:
                        rows = conn.execute(
                            """SELECT s.id, s.title, s.published_at
                               FROM sources s JOIN source_themes st ON s.id = st.source_id
                               WHERE st.theme_id = %s""",
                            (theme["id"],),
                        ).fetchall()
                        for r in rows:
                            if r["id"] not in source_map:
                                source_map[r["id"]] = {
                                    "source_id": r["id"],
                                    "title": r.get("title", ""),
                                    "published_at": r.get("published_at"),
                                }
        except Exception:
            logger.debug("Keyword theme fallback failed", exc_info=True)

    return list(source_map.values())


def _load_deep_summaries(sources: list[dict]) -> dict[str, str]:
    """Load deep_summary.md for each source from library directory."""
    summaries = {}
    for src in sources:
        sid = src["source_id"]
        path = LIBRARY_DIR / sid / "deep_summary.md"
        if path.exists():
            try:
                text = path.read_text(encoding="utf-8")
                if text.strip():
                    summaries[sid] = text
            except Exception:
                logger.debug("Failed to read deep summary for %s", sid)
    return summaries


def _load_evidence_snippets(source_ids: list[str], query: str, per_source: int = 8) -> dict[str, list[dict]]:
    """Load the strongest evidence snippets per source for concrete, quotable facts.

    Inspired by gpt-researcher's emphasis on "include all factual information
    such as numbers, stats, quotes." Retrieves claims with evidence snippets
    scoped to the matched sources, ordered by confidence.
    """
    evidence: dict[str, list[dict]] = {}
    if not source_ids:
        return evidence

    try:
        with db.get_conn() as conn:
            rows = conn.execute(
                """SELECT c.source_id, c.claim_text, c.evidence_snippet,
                          c.confidence, c.section
                   FROM claims c
                   WHERE c.source_id = ANY(%s)
                     AND c.evidence_snippet IS NOT NULL
                     AND c.evidence_snippet != ''
                   ORDER BY c.confidence DESC NULLS LAST""",
                (source_ids,),
            ).fetchall()

            for row in rows:
                sid = row["source_id"]
                if sid not in evidence:
                    evidence[sid] = []
                if len(evidence[sid]) < per_source:
                    evidence[sid].append({
                        "claim": row["claim_text"],
                        "snippet": row["evidence_snippet"],
                        "confidence": row["confidence"],
                        "section": row.get("section"),
                    })
    except Exception:
        logger.warning("Failed to load evidence snippets", exc_info=True)

    return evidence


def _get_themes_for_sources(source_ids: list[str]) -> list[str]:
    """Get all theme IDs associated with the given sources."""
    if not source_ids:
        return []
    try:
        with db.get_conn() as conn:
            rows = conn.execute(
                """SELECT DISTINCT theme_id FROM source_themes
                   WHERE source_id = ANY(%s)""",
                (source_ids,),
            ).fetchall()
            return [r["theme_id"] for r in rows]
    except Exception:
        return []


def _load_landscape_signals(theme_ids: list[str]) -> dict:
    """Load wiki-based landscape context and open anticipations for themes."""
    from retrieval.wiki_retrieval import gather_wiki_context
    wiki_ctx = gather_wiki_context(theme_ids=theme_ids, include_syntheses=True)

    anticipations = []
    if theme_ids:
        try:
            with db.get_conn() as conn:
                anticipations = conn.execute(
                    """SELECT a.prediction, a.confidence, a.timeline,
                              t.name AS theme_name
                       FROM anticipations a
                       JOIN themes t ON a.theme_id = t.id
                       WHERE a.theme_id = ANY(%s) AND a.status = 'open'
                       ORDER BY a.confidence DESC
                       LIMIT 20""",
                    (theme_ids,),
                ).fetchall()
                anticipations = [dict(a) for a in anticipations]
        except Exception:
            logger.debug("Failed to load anticipations for synthesis", exc_info=True)

    return {"wiki_context": wiki_ctx, "anticipations": anticipations}


def _load_consolidated_implications(theme_ids: list[str]) -> list[dict]:
    """Load consolidated implications for all matched themes."""
    seen_pairs = set()
    results = []
    for tid in theme_ids:
        for impl in get_consolidated_implications(tid):
            pair_key = (impl["source_theme_id"], impl["target_theme_id"])
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                results.append(impl)
    results.sort(key=lambda x: x.get("max_confidence", 0), reverse=True)
    return results


SYNTHESIS_ANALYSIS_PROMPT = """You are pre-digesting research context for a synthesis report on "{topic}".

You have {source_count} sources with deep summaries, {evidence_count} evidence snippets, and landscape signals across {theme_count} themes.

## Source Titles
{source_titles}

## Evidence Sample (top claims by confidence)
{evidence_sample}

## Landscape Signals
Capabilities: {n_caps} | Limitations: {n_lims} | Bottlenecks: {n_bns}
Implications: {n_impls}

## Anticipations
{anticipations_text}

---

Produce a structured analysis to guide the synthesis LLM:

KEY TENSIONS: Contradictions or conflicts across the sources — where do they disagree or frame things differently? Be specific about which sources.

MOST IMPORTANT CONNECTIONS: Non-obvious links between findings from different sources. What patterns emerge when you look across all sources together?

CONVERGENCE VS DIVERGENCE: Where do sources strongly agree? Where do they diverge? Is the convergence meaningful or just shared assumptions?

COVERAGE GAPS: What's missing from the evidence? What questions remain unanswered? What would you expect to see but don't?

RECOMMENDED EMPHASIS: What deserves the most depth in the synthesis? What's the single most important insight across all these sources?

Keep each section to 2-4 sentences. Be specific — reference concrete findings.
"""


def analyze_synthesis_context(ctx: dict, executor=None) -> str:
    """Pre-digest gathered synthesis context to guide the synthesis LLM.

    Runs a fast Haiku call to identify tensions, connections, gaps,
    and recommended emphasis before the expensive synthesis call.

    Args:
        ctx: Output of gather_synthesis_context().
        executor: ClaudeExecutor instance.

    Returns:
        Analysis text, or empty string on failure.
    """
    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    sources = ctx.get("indexed_sources") or ctx.get("sources", [])
    summaries = ctx.get("summaries", {})
    evidence = ctx.get("evidence", {})
    landscape = ctx.get("landscape", {})
    implications = ctx.get("implications", [])

    # Build evidence sample (top snippets across all sources)
    all_evidence = []
    for sid, snippets in evidence.items():
        for ev in snippets[:3]:
            all_evidence.append(ev)
    all_evidence.sort(key=lambda e: e.get("confidence", 0), reverse=True)
    evidence_sample = "\n".join(
        f"- {(ev.get('claim') or '')[:150]}" for ev in all_evidence[:10]
    ) or "No evidence snippets."

    source_titles = "\n".join(
        f"- {s.get('title', s.get('source_id', '?'))}" for s in sources
    )

    ants = landscape.get("anticipations", [])
    anticipations_text = "\n".join(
        f"- {a['prediction'][:150]} (confidence: {a.get('confidence', '?')})"
        for a in ants[:10]
    ) or "None active."

    n_themes = len(landscape["wiki_context"].theme_narratives) if landscape.get("wiki_context") else 0
    total_evidence = sum(len(v) for v in evidence.values())
    prompt = SYNTHESIS_ANALYSIS_PROMPT.format(
        topic=ctx["topic"],
        source_count=len(summaries),
        evidence_count=total_evidence,
        theme_count=len(ctx.get("theme_ids", [])),
        source_titles=source_titles,
        evidence_sample=evidence_sample,
        n_caps=f"{n_themes} theme narratives (wiki)" if n_themes else 0,
        n_lims=f"(in {n_themes} wiki narratives)" if n_themes else 0,
        n_bns=f"(in {n_themes} wiki narratives)" if n_themes else 0,
        n_impls=len(implications),
        anticipations_text=anticipations_text,
    )

    session_id = f"synthesis_analysis_{_slugify(ctx['topic'])}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="haiku",
            timeout=30,
        )
        analysis = result.text.strip()
        if analysis and len(analysis) > 50:
            logger.info("Pre-analysis for '%s': %d chars", ctx["topic"], len(analysis))
            return analysis
    except Exception:
        logger.warning("Pre-analysis failed for '%s'", ctx["topic"], exc_info=True)
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass

    return ""


def gather_synthesis_context(query: str) -> dict | None:
    """Gather all data needed for a synthesis report — no LLM calls.

    Returns a dict with keys: topic, sources, indexed_sources, summaries,
    evidence, landscape, implications, theme_ids.  Returns None if no
    sources or summaries are found.
    """
    sources = _find_relevant_sources(query)
    if not sources:
        logger.warning("No sources found for topic: %s", query)
        return None

    logger.info("Found %d sources for topic: %s", len(sources), query)

    summaries = _load_deep_summaries(sources)
    if not summaries:
        logger.warning("No deep summaries found for topic: %s", query)
        return None

    source_ids = [s["source_id"] for s in sources]
    evidence = _load_evidence_snippets(
        [sid for sid in source_ids if sid in summaries],
        query,
    )
    logger.info("Loaded evidence snippets for %d sources", len(evidence))

    theme_ids = _get_themes_for_sources(source_ids)
    landscape = _load_landscape_signals(theme_ids)
    implications = _load_consolidated_implications(theme_ids)
    indexed_sources = [s for s in sources if s["source_id"] in summaries]

    return {
        "topic": query,
        "sources": sources,
        "indexed_sources": indexed_sources,
        "summaries": summaries,
        "evidence": evidence,
        "landscape": landscape,
        "implications": implications,
        "theme_ids": theme_ids,
    }


def format_synthesis_context(ctx: dict, analysis: str = "") -> str:
    """Format a gathered synthesis context dict into prompt-injectable text.

    Args:
        ctx: Output of gather_synthesis_context().
        analysis: Optional pre-analysis text from analyze_synthesis_context().
    """
    query = ctx["topic"]
    sources = ctx["sources"]
    indexed_sources = ctx["indexed_sources"]
    summaries = ctx["summaries"]
    evidence = ctx["evidence"]
    landscape = ctx["landscape"]
    implications = ctx["implications"]

    sources_block = "\n".join(
        f"- Source {i+1}: \"{s.get('title', s['source_id'])}\" "
        f"(ID: {s['source_id']}, published: {str(s.get('published_at', '?'))[:10]})"
        for i, s in enumerate(indexed_sources)
    )

    max_chars_per_summary = 5000
    summaries_block = ""
    for i, (sid, text) in enumerate(summaries.items()):
        title = next((s.get("title", sid) for s in sources if s["source_id"] == sid), sid)
        truncated = text[:max_chars_per_summary]
        if len(text) > max_chars_per_summary:
            truncated += "\n[...truncated]"
        summaries_block += f"\n### Source {i+1}: \"{title}\"\n\n{truncated}\n"

    evidence_block = ""
    for i, src in enumerate(indexed_sources):
        sid = src["source_id"]
        snippets = evidence.get(sid, [])
        if snippets:
            evidence_block += f"\n**Source {i+1}** key evidence:\n"
            for ev in snippets:
                conf_str = f" (confidence: {ev['confidence']:.2f})" if ev.get("confidence") else ""
                evidence_block += f"- Claim: {ev['claim']}\n"
                if ev.get("snippet"):
                    evidence_block += f"  Verbatim: \"{ev['snippet'][:300]}\"{conf_str}\n"
    evidence_block = evidence_block or "No evidence snippets available."

    if landscape.get("wiki_context"):
        from retrieval.wiki_retrieval import format_wiki_context_block
        _wiki_block = format_wiki_context_block(
            landscape["wiki_context"], header="Landscape Signals", max_chars_per_theme=4000
        )
        capabilities_block = _wiki_block
        limitations_block = "(see Landscape Signals above)"
        bottlenecks_block = "(see Landscape Signals above)"
    else:
        capabilities_block = "None recorded."
        limitations_block = "None recorded."
        bottlenecks_block = "None recorded."

    implications_block = "\n".join(
        f"- {imp['source_theme']} -> {imp['target_theme']}: {imp['top_implication']} "
        f"({imp['observation_count']} obs, confidence: {imp.get('max_confidence', '?')})"
        + (f"\n  Second perspective: {imp['second_perspective']}" if imp.get("second_perspective") else "")
        for imp in implications
    ) or "None recorded."

    anticipations_block = "\n".join(
        f"- {a['prediction']} (confidence: {a.get('confidence', '?')}, timeline: {a.get('timeline', '?')})"
        for a in landscape.get("anticipations", [])
    ) or "None active."

    analysis_section = ""
    if analysis:
        analysis_section = (
            "## Pre-Analysis (editorial direction — use this to guide emphasis)\n\n"
            + analysis
            + "\n\n---\n\n"
        )

    formatted = SYNTHESIS_PROMPT.format(
        topic=query,
        analysis_section=analysis_section,
        source_count=len(summaries),
        sources_block=sources_block,
        summaries_block=summaries_block,
        evidence_block=evidence_block,
        capabilities_block=capabilities_block,
        limitations_block=limitations_block,
        bottlenecks_block=bottlenecks_block,
        implications_block=implications_block,
        anticipations_block=anticipations_block,
    )

    return formatted


def generate_topic_synthesis(query: str, executor=None) -> str | None:
    """Generate a topic synthesis report consolidating all sources on a topic.

    Thin wrapper: gathers context, then calls the executor for LLM synthesis.
    Kept for backward compatibility (e.g. heartbeat, ad-hoc scripts).

    Args:
        query: Topic to synthesize (e.g. "openclaw", "robotics").
        executor: ClaudeExecutor instance.

    Returns:
        Report markdown text, or None on failure.
    """
    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    ctx = gather_synthesis_context(query)
    if ctx is None:
        return None

    analysis = analyze_synthesis_context(ctx, executor)
    prompt = format_synthesis_context(ctx, analysis=analysis)

    session_id = f"synthesis_{_slugify(query)}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="sonnet",
            timeout=180,
        )
        report = result.text.strip()
        if not report or len(report) < 100:
            logger.warning("Synthesis report too short for %s: %d chars", query, len(report))
            return None

        # Extract entity names for quality gate ground truth
        landscape = ctx.get("landscape") or {}
        entity_names = [
            entity.get("description", "")[:60]
            for key in ("capabilities", "limitations", "bottlenecks")
            for entity in landscape.get(key, [])
            if entity.get("description")
        ]

        # Quality gate: check if the report meets synthesis standards
        passes, feedback, original_score = _validate_synthesis_quality(
            report, query, executor, entity_names=entity_names
        )
        if not passes:
            logger.info("Synthesis quality gate failed for %s (score: %s), retrying with feedback",
                        query, original_score)
            retry_prompt = prompt + f"\n\nIMPORTANT CORRECTION: {feedback}"
            retry_session = f"synthesis_retry_{_slugify(query)}"
            try:
                retry_result = executor.run_raw(
                    retry_prompt,
                    session_id=retry_session,
                    model="sonnet",
                    timeout=180,
                )
                retry_text = retry_result.text.strip()
                if retry_text and len(retry_text) >= 100:
                    # Re-score the retry to verify improvement
                    retry_score = _score_synthesis(
                        retry_text, query, executor,
                        entity_names=entity_names,
                    )
                    if retry_score is not None and (
                        retry_score >= 3
                        or (original_score is not None and retry_score > original_score)
                    ):
                        report = retry_text
                        logger.info("Retry improved synthesis for %s (score: %.1f -> %.1f)",
                                    query, original_score or 0, retry_score)
                    elif original_score is not None and retry_score is not None and retry_score <= original_score:
                        logger.info("Retry did not improve for %s (score: %.1f -> %.1f), keeping original",
                                    query, original_score, retry_score)
                    else:
                        # Can't score retry — accept it if it's long enough
                        report = retry_text
                        logger.info("Retry accepted without scoring for %s", query)
            except Exception:
                logger.debug("Quality retry failed for %s, using original", query, exc_info=True)
            finally:
                try:
                    executor.cleanup_session(retry_session)
                except Exception:
                    pass

        # Cache the report
        SYNTHESES_DIR.mkdir(parents=True, exist_ok=True)
        slug = _slugify(query)
        cache_path = SYNTHESES_DIR / f"{slug}.md"
        cache_path.write_text(report, encoding="utf-8")
        logger.info("Cached synthesis report: %s (%d chars)", cache_path, len(report))

        return report

    except Exception:
        logger.error("Failed to generate synthesis for %s", query, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Merge mode — explicit source IDs/URLs
# ---------------------------------------------------------------------------

_ULID_RE = re.compile(r"^[0-9A-Za-z]{26}$")


def resolve_source_refs(tokens: list[str]) -> list[str] | None:
    """Resolve a list of tokens to source IDs.

    Each token must be either a ULID (26 alphanumeric chars) or a URL
    (starts with ``http``).  URLs are looked up via ``sources.url``.

    Returns a list of resolved source_ids if **all** tokens resolve,
    otherwise ``None`` (caller should fall through to topic mode).
    """
    if not tokens:
        return None

    resolved: list[str] = []
    for tok in tokens:
        if _ULID_RE.match(tok):
            resolved.append(tok)
        elif tok.startswith("http"):
            try:
                with db.get_conn() as conn:
                    row = conn.execute(
                        "SELECT id FROM sources WHERE url = %s", (tok,)
                    ).fetchone()
                    if row:
                        resolved.append(row["id"])
                    else:
                        return None  # URL not found — fall through
            except Exception:
                logger.debug("URL lookup failed for %s", tok, exc_info=True)
                return None
        else:
            return None  # token is neither ULID nor URL

    return resolved if resolved else None


def _merge_cache_path(source_ids: list[str]) -> Path:
    """Deterministic cache path for a set of source IDs."""
    key = "|".join(sorted(source_ids))
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    return MERGES_DIR / f"{digest}.md"


def check_merge_cache(source_ids: list[str], max_age_hours: int = 24) -> str | None:
    """Return cached merge report if it exists and is fresh enough."""
    path = _merge_cache_path(source_ids)
    if not path.exists():
        return None
    age_hours = (datetime.now(timezone.utc).timestamp() - path.stat().st_mtime) / 3600
    if age_hours > max_age_hours:
        return None
    try:
        text = path.read_text(encoding="utf-8")
        return text if text.strip() else None
    except Exception:
        return None


def save_merge_cache(source_ids: list[str], report: str, topic: str, titles: list[str]) -> Path:
    """Write a merge report to disk with YAML front-matter."""
    MERGES_DIR.mkdir(parents=True, exist_ok=True)
    path = _merge_cache_path(source_ids)
    front_matter = yaml.dump(
        {
            "source_ids": sorted(source_ids),
            "titles": titles,
            "inferred_topic": topic,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        default_flow_style=False,
    )
    path.write_text(f"---\n{front_matter}---\n\n{report}", encoding="utf-8")
    logger.info("Cached merge report: %s (%d chars)", path, len(report))
    return path


def _load_source_meta(source_id: str) -> dict:
    """Load meta.yaml for a source, returning a dict with title/url/published_at."""
    meta_path = LIBRARY_DIR / source_id / "meta.yaml"
    if meta_path.exists():
        try:
            return yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except Exception:
            logger.debug("Failed to read meta.yaml for %s", source_id)
    return {}


def gather_merge_context(source_ids: list[str]) -> dict | None:
    """Gather all data for a merge report from explicit source IDs.

    Returns a dict with mode="merge" and all necessary context, or None if
    fewer than 2 sources have valid data.
    """
    # Validate sources exist and are complete
    valid_sources: list[dict] = []
    try:
        with db.get_conn() as conn:
            rows = conn.execute(
                """SELECT id, title, published_at, processing_status
                   FROM sources WHERE id = ANY(%s)""",
                (source_ids,),
            ).fetchall()
            by_id = {r["id"]: r for r in rows}
    except Exception:
        logger.error("Failed to validate source IDs", exc_info=True)
        return None

    for sid in source_ids:
        row = by_id.get(sid)
        if row and row.get("processing_status") == "complete":
            meta = _load_source_meta(sid)
            valid_sources.append({
                "source_id": sid,
                "title": meta.get("title") or row.get("title") or sid,
                "url": meta.get("url", ""),
                "published_at": row.get("published_at"),
            })

    if len(valid_sources) < 2:
        logger.warning("Merge requires >= 2 complete sources, got %d", len(valid_sources))
        return None

    sids = [s["source_id"] for s in valid_sources]
    summaries = _load_deep_summaries(valid_sources)
    if not summaries:
        logger.warning("No deep summaries for merge sources")
        return None

    evidence = _load_evidence_snippets(sids, "")
    theme_ids = _get_themes_for_sources(sids)
    landscape = _load_landscape_signals(theme_ids)
    implications = _load_consolidated_implications(theme_ids)

    # Infer topic from the most common theme name
    topic = _infer_topic(theme_ids)

    return {
        "mode": "merge",
        "topic": topic,
        "sources": valid_sources,
        "summaries": summaries,
        "evidence": evidence,
        "landscape": landscape,
        "implications": implications,
    }


def _infer_topic(theme_ids: list[str]) -> str:
    """Pick the most common theme name as the inferred topic."""
    if not theme_ids:
        return "merged sources"
    try:
        with db.get_conn() as conn:
            rows = conn.execute(
                "SELECT id, name FROM themes WHERE id = ANY(%s)", (theme_ids,)
            ).fetchall()
            if rows:
                # Use most frequent; tie-break alphabetically
                counts = Counter(r["name"] for r in rows)
                return counts.most_common(1)[0][0]
    except Exception:
        pass
    return theme_ids[0] if theme_ids else "merged sources"


def format_merge_context(ctx: dict) -> str:
    """Format gathered merge context into prompt-injectable text."""
    sources = ctx["sources"]
    summaries = ctx["summaries"]
    evidence = ctx["evidence"]
    landscape = ctx["landscape"]
    implications = ctx["implications"]
    topic = ctx["topic"]

    # Numbered reference list: [N] "Title" (date)
    references_block = "\n".join(
        f"[{i+1}] \"{s['title']}\" ({str(s.get('published_at', '?'))[:10]})"
        for i, s in enumerate(sources)
    )
    # Map source_id -> reference number for inline use
    sid_to_num = {s["source_id"]: i + 1 for i, s in enumerate(sources)}

    max_chars_per_summary = 5000
    summaries_block = ""
    for sid, text in summaries.items():
        num = sid_to_num.get(sid, "?")
        title = next((s["title"] for s in sources if s["source_id"] == sid), sid)
        truncated = text[:max_chars_per_summary]
        if len(text) > max_chars_per_summary:
            truncated += "\n[...truncated]"
        summaries_block += f"\n### [{num}] \"{title}\"\n\n{truncated}\n"

    evidence_block = ""
    for src in sources:
        sid = src["source_id"]
        num = sid_to_num[sid]
        snippets = evidence.get(sid, [])
        if snippets:
            evidence_block += f"\n**[{num}]** key evidence:\n"
            for ev in snippets:
                conf_str = f" (confidence: {ev['confidence']:.2f})" if ev.get("confidence") else ""
                evidence_block += f"- Claim: {ev['claim']}\n"
                if ev.get("snippet"):
                    evidence_block += f"  Verbatim: \"{ev['snippet'][:300]}\"{conf_str}\n"
    evidence_block = evidence_block or "No evidence snippets available."

    if landscape.get("wiki_context"):
        from retrieval.wiki_retrieval import format_wiki_context_block
        _wiki_block = format_wiki_context_block(
            landscape["wiki_context"], header="Landscape Signals", max_chars_per_theme=4000
        )
        capabilities_block = _wiki_block
        limitations_block = "(see Landscape Signals above)"
        bottlenecks_block = "(see Landscape Signals above)"
    else:
        capabilities_block = "None recorded."
        limitations_block = "None recorded."
        bottlenecks_block = "None recorded."

    implications_block = "\n".join(
        f"- {imp['source_theme']} -> {imp['target_theme']}: {imp['top_implication']} "
        f"({imp['observation_count']} obs, confidence: {imp.get('max_confidence', '?')})"
        + (f"\n  Second perspective: {imp['second_perspective']}" if imp.get("second_perspective") else "")
        for imp in implications
    ) or "None recorded."

    return MERGE_PROMPT.format(
        topic=topic,
        source_count=len(sources),
        references_block=references_block,
        summaries_block=summaries_block,
        evidence_block=evidence_block,
        capabilities_block=capabilities_block,
        limitations_block=limitations_block,
        bottlenecks_block=bottlenecks_block,
        implications_block=implications_block,
    )
