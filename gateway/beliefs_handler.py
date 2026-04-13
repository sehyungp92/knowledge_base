"""Direct Python handler for /beliefs jobs.

Bypasses the Claude CLI subprocess. Handles belief CRUD operations natively
and delegates LLM reasoning (classification, review, synthesis) to executor.run_raw().
"""

from __future__ import annotations

import json
import re
import time

from ingest.json_parser import parse_json_from_llm
from datetime import datetime, timezone
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job
from reading_app.text_utils import truncate, truncate_sentences

logger = structlog.get_logger(__name__)

# Categories that count as "diverse" for belief suggestion diversity enforcement.
# Matches the category enum in _SUGGEST_PROMPT.
_DIVERSITY_CATEGORIES = {"limitation", "risk", "architectural", "methodological"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_beliefs_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /beliefs directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("beliefs_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    subcmd, args = _parse_subcommand(text)
    log = log.bind(subcommand=subcmd)

    if subcmd == "add":
        result = _handle_add(args, executor, on_progress, log)
    elif subcmd == "update":
        result = _handle_update(args, on_progress, log)
    elif subcmd == "review":
        result = _handle_review(executor, on_progress, log)
    elif subcmd == "synthesis":
        result = _handle_synthesis(args, executor, on_progress, log)
    elif subcmd == "suggest":
        result = _handle_suggest(args, executor, on_progress, log)
    else:
        # list (default) — args may be a topic filter or empty
        result = _handle_list(args, on_progress, log)

    elapsed = time.monotonic() - t0
    log.info("beliefs_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Subcommand parser
# ---------------------------------------------------------------------------

_SUBCOMMANDS = {"add", "update", "review", "synthesis", "suggest"}


def _parse_subcommand(text: str) -> tuple[str, str]:
    """Parse '/beliefs <subcommand> <args>' into (subcommand, remaining_args).

    Returns ('list', topic_or_empty) for bare /beliefs or /beliefs <topic>.
    """
    # Strip the /beliefs prefix
    cleaned = text.strip()
    for prefix in ("/beliefs ", "/beliefs"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    if not cleaned:
        return "list", ""

    first_word = cleaned.split(None, 1)[0].lower()
    if first_word in _SUBCOMMANDS:
        rest = cleaned.split(None, 1)[1] if len(cleaned.split(None, 1)) > 1 else ""
        return first_word, rest.strip()

    # Not a known subcommand — treat as topic filter for list
    return "list", cleaned


# ---------------------------------------------------------------------------
# /beliefs (list)
# ---------------------------------------------------------------------------

def _handle_list(topic_filter: str, on_progress, log) -> str:
    """List active beliefs, optionally filtered by topic/theme."""
    from reading_app.db import get_active_beliefs, get_beliefs_for_theme, get_conn

    if on_progress:
        on_progress("Loading beliefs...")

    if topic_filter:
        # Try to match theme by ID or name
        with get_conn() as conn:
            theme = conn.execute(
                """SELECT id, name FROM themes
                   WHERE id = %s OR name ILIKE %s
                   ORDER BY velocity DESC NULLS LAST LIMIT 1""",
                (topic_filter, f"%{topic_filter}%"),
            ).fetchone()

        if theme:
            beliefs = get_beliefs_for_theme(theme["id"])
            if not beliefs:
                return f"No active beliefs for theme **{theme['name']}**."
            return f"**Tracked Beliefs — {theme['name']}**\n\n" + _format_beliefs_list(beliefs)
        else:
            # Fall back to full list filtered client-side
            all_beliefs = get_active_beliefs()
            filtered = [
                b for b in all_beliefs
                if topic_filter.lower() in (b.get("claim") or "").lower()
                or topic_filter.lower() in (b.get("theme_name") or "").lower()
            ]
            if not filtered:
                return f"No active beliefs matching **{topic_filter}**."
            return f"**Tracked Beliefs matching \"{topic_filter}\"**\n\n" + _format_beliefs_list(filtered)
    else:
        beliefs = get_active_beliefs()
        if not beliefs:
            return "No active beliefs tracked yet. Use `/beliefs add <statement>` to add one."
        return "**Tracked Beliefs**\n\n" + _format_beliefs_list(beliefs)


def _format_beliefs_list(beliefs: list[dict]) -> str:
    """Format beliefs grouped by theme with confidence indicators."""
    grouped: dict[str, list[dict]] = {}
    for b in beliefs:
        theme_name = b.get("theme_name") or "Unlinked"
        grouped.setdefault(theme_name, []).append(b)

    lines = []
    for theme_name, theme_beliefs in grouped.items():
        lines.append(f"**{theme_name}**")
        for b in theme_beliefs:
            conf = b.get("confidence") or 0.0
            indicator = "●" if conf > 0.8 else "◐" if conf >= 0.4 else "○"

            ev_for = b.get("evidence_for")
            ev_against = b.get("evidence_against")
            n_for = len(ev_for) if isinstance(ev_for, list) else 0
            n_against = len(ev_against) if isinstance(ev_against, list) else 0

            stale = ""
            if b.get("last_updated"):
                lu = b["last_updated"]
                if isinstance(lu, str):
                    lu = datetime.fromisoformat(lu)
                if hasattr(lu, "tzinfo"):
                    now = datetime.now(timezone.utc) if lu.tzinfo else datetime.now()
                    age_days = (now - lu).days
                    if age_days > 30:
                        stale = " ⚠ needs review"

            lines.append(
                f"{indicator} {b['claim']} [conf: {conf:.2f}] — "
                f"{n_for}↑ {n_against}↓{stale}"
            )
            lines.append(f"  `{b['id']}` | type: {b.get('belief_type', '?')}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# /beliefs add <statement>
# ---------------------------------------------------------------------------

_CLASSIFY_PROMPT = """\
You are classifying a new belief for a personal knowledge engine about AI.

## Belief Statement
{statement}

## Available Themes
{themes_text}

## Instructions

Classify this belief and return ONLY a JSON block:

```json
{{
  "belief_type": "factual|predictive|methodological|meta",
  "domain_theme_id": "<theme_id or null if none fit>",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation of classification"
}}
```

- **factual**: Claims about what is currently true (e.g., "LLMs cannot reliably do multi-step planning")
- **predictive**: Claims about what will happen (e.g., "Scaling will hit diminishing returns by 2027")
- **methodological**: Claims about how things should be done (e.g., "RLHF is insufficient for alignment")
- **meta**: Claims about the field itself (e.g., "Most benchmarks don't measure real-world capability")

Set confidence based on how strongly the statement is phrased and how well-evidenced it seems.
If unsure about the theme, set domain_theme_id to null.
"""


def _handle_add(statement: str, executor, on_progress, log) -> str:
    """Add a new tracked belief."""
    from reading_app.db import (
        find_similar_belief, get_themes_by_level, insert_belief, get_conn,
    )
    from retrieval.hybrid import hybrid_retrieve

    if not statement:
        return "Usage: `/beliefs add <your belief statement>`"

    if on_progress:
        on_progress("Checking for similar beliefs...")

    # 1. Duplicate check
    similar = None
    try:
        similar = find_similar_belief(statement, threshold=0.7)
    except Exception as e:
        # pg_trgm extension may not be installed
        log.debug("find_similar_belief_failed", error=str(e)[:100])

    if similar:
        sim_score = similar.get("sim", 0)
        return (
            f"**Similar belief already exists** (similarity: {sim_score:.2f}):\n\n"
            f"> {similar['claim']}\n\n"
            f"ID: `{similar['id']}` | Confidence: {similar.get('confidence', '?')}\n\n"
            f"Consider using `/beliefs update {similar['id']} <new_confidence>` instead."
        )

    # 2. Get themes for classification
    if on_progress:
        on_progress("Classifying belief...")

    themes_l0 = get_themes_by_level(0)
    themes_l1 = get_themes_by_level(1)
    all_themes = themes_l0 + themes_l1

    themes_text = "\n".join(
        f"- `{t['id']}`: {t['name']}" + (f" — {t.get('description', '')[:80]}" if t.get("description") else "")
        for t in all_themes
    ) if all_themes else "(no themes in database)"

    # 3. LLM classification
    classify_prompt = _CLASSIFY_PROMPT.format(
        statement=statement,
        themes_text=themes_text,
    )

    try:
        result = executor.run_raw(
            classify_prompt,
            session_id="beliefs_classify",
            timeout=60,
        )
        classification = _parse_json(result.text)
    except Exception as e:
        log.warning("beliefs_classify_failed", error=str(e)[:200])
        classification = {}

    belief_type = classification.get("belief_type", "factual")
    if belief_type not in {"factual", "predictive", "methodological", "meta"}:
        belief_type = "factual"

    domain_theme_id = classification.get("domain_theme_id")
    # Validate theme_id exists
    if domain_theme_id:
        valid_ids = {t["id"] for t in all_themes}
        if domain_theme_id not in valid_ids:
            log.info("beliefs_invalid_theme", theme_id=domain_theme_id)
            domain_theme_id = None

    confidence = classification.get("confidence", 0.5)
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        confidence = 0.5

    reasoning = classification.get("reasoning", "")

    # 4. Evidence search
    if on_progress:
        on_progress("Searching for evidence...")

    evidence_for = []
    evidence_against = []
    try:
        results = hybrid_retrieve(statement, get_conn, k=10)
        for r in results:
            entry = {
                "claim_id": r.get("id"),
                "claim_text": (r.get("claim_text") or "")[:200],
                "source_id": r.get("source_id"),
                "score": round(r.get("rrf_score", 0), 4),
            }
            # Simple heuristic: all retrieved claims are potential support
            # A proper for/against split would need another LLM call
            evidence_for.append(entry)
    except Exception as e:
        log.warning("beliefs_evidence_search_failed", error=str(e)[:200])

    # 5. Persist
    if on_progress:
        on_progress("Saving belief...")

    now_iso = datetime.now(timezone.utc).isoformat()
    belief_id = f"belief_{ULID()}"
    history = [{
        "ts": now_iso,
        "old_conf": None,
        "new_conf": confidence,
        "trigger": "initial creation",
        "trigger_type": "manual",
    }]

    insert_belief(
        id=belief_id,
        claim=statement,
        confidence=confidence,
        status="active",
        belief_type=belief_type,
        domain_theme_id=domain_theme_id,
        landscape_links=[],
        evidence_for=evidence_for,
        evidence_against=evidence_against,
        derived_anticipations=[],
        history=history,
    )

    log.info("belief_inserted", belief_id=belief_id, belief_type=belief_type,
             theme=domain_theme_id, confidence=confidence)

    # --- Wiki page creation (best-effort) ---
    _wiki_updated = False
    try:
        from retrieval.wiki_writer import file_belief_to_wiki
        file_belief_to_wiki(
            belief_id, statement, confidence, belief_type,
            domain_theme_id, evidence_for, evidence_against,
        )
        _wiki_updated = True
    except Exception:
        log.warning("belief_wiki_create_failed", belief_id=belief_id, exc_info=True)

    # 6. Format response
    theme_name = domain_theme_id or "None"
    if domain_theme_id:
        for t in all_themes:
            if t["id"] == domain_theme_id:
                theme_name = t["name"]
                break

    response_lines = [
        f"**Belief tracked:** {statement}",
        f"Type: {belief_type} | Theme: {theme_name} | Confidence: {confidence:.2f}",
        f"Evidence: {len(evidence_for)} supporting, {len(evidence_against)} contradicting",
        f"ID: `{belief_id}`",
    ]
    if reasoning:
        response_lines.append(f"Reasoning: {reasoning}")

    if belief_type == "predictive" and confidence >= 0.6:
        response_lines.append(
            "\nThis is a predictive belief with high confidence. "
            "Consider creating anticipations to track it: "
            "`/beliefs synthesis` on its theme to explore implications."
        )

    if _wiki_updated:
        response_lines.append("\n_Wiki updated: beliefs page filed._")

    return "\n".join(response_lines)


# ---------------------------------------------------------------------------
# /beliefs update <id> <confidence> [trigger]
# ---------------------------------------------------------------------------

def _handle_update(args: str, on_progress, log) -> str:
    """Update belief confidence."""
    from reading_app.db import get_belief, update_belief_confidence

    parts = args.split(None, 2)
    if len(parts) < 2:
        return "Usage: `/beliefs update <belief_id> <new_confidence> [reason]`"

    belief_id = parts[0]
    try:
        new_conf = float(parts[1])
        if not 0 <= new_conf <= 1:
            return "Confidence must be between 0.0 and 1.0."
    except ValueError:
        return f"Invalid confidence value: `{parts[1]}`. Must be a number between 0.0 and 1.0."

    trigger = parts[2] if len(parts) > 2 else "manual update"

    if on_progress:
        on_progress("Updating belief...")

    current = get_belief(belief_id)
    if not current:
        return f"Belief not found: `{belief_id}`"

    old_conf = current.get("confidence", 0)
    updated = update_belief_confidence(belief_id, new_conf, trigger, trigger_type="manual")

    if not updated:
        return f"Failed to update belief `{belief_id}`."

    # --- Wiki page update (best-effort) ---
    _wiki_updated = False
    try:
        from retrieval.wiki_writer import file_belief_to_wiki
        file_belief_to_wiki(
            belief_id, current["claim"], new_conf,
            current.get("belief_type"), current.get("domain_theme_id"),
            is_update=True, trigger=trigger,
        )
        _wiki_updated = True
    except Exception:
        log.warning("belief_wiki_update_failed", belief_id=belief_id, exc_info=True)

    direction = "↑" if new_conf > old_conf else "↓" if new_conf < old_conf else "→"
    response = (
        f"**Belief updated** `{belief_id}`\n\n"
        f"> {current['claim']}\n\n"
        f"Confidence: {old_conf:.2f} {direction} {new_conf:.2f}\n"
        f"Trigger: {trigger}"
    )

    if new_conf < 0.3:
        response += "\n\n⚠ Low confidence — consider archiving with `/beliefs archive`."
    if new_conf > 0.8 and old_conf <= 0.8:
        response += "\n\n💡 High confidence reached — check for counter-evidence gaps."
    if _wiki_updated:
        response += "\n\n_Wiki updated: belief page updated._"

    return response


# ---------------------------------------------------------------------------
# /beliefs review
# ---------------------------------------------------------------------------

_REVIEW_PROMPT = """\
You are reviewing stale beliefs against recent evidence for a personal AI knowledge engine.

## Stale Beliefs
{beliefs_text}

## Recent Evidence (claims from sources ingested in the last 30 days)
{evidence_text}

## Instructions

For each stale belief, assess:
1. Does recent evidence **support**, **contradict**, or **extend** it?
2. Should confidence go up, down, or stay the same?
3. Is the belief still relevant?

Output a narrative review, then a JSON block:

```json
{{
  "reviews": [
    {{
      "belief_id": "...",
      "direction": "up|down|unchanged",
      "suggested_confidence": 0.0-1.0,
      "reasoning": "...",
      "key_evidence": "..."
    }}
  ]
}}
```
"""


def _handle_review(executor, on_progress, log) -> str:
    """Review stale beliefs against recent evidence."""
    from reading_app.db import get_stale_beliefs, get_conn

    if on_progress:
        on_progress("Finding stale beliefs...")

    stale = get_stale_beliefs()
    if not stale:
        return "All beliefs are up-to-date. No review needed."

    # Gather recent claims for context
    if on_progress:
        on_progress(f"Reviewing {len(stale)} stale beliefs...")

    beliefs_text = "\n".join(
        f"- **{b['id']}**: {b['claim']} (conf: {b.get('confidence', '?')}, "
        f"theme: {b.get('theme_name', 'unlinked')}, "
        f"last updated: {str(b.get('last_updated', '?'))[:10]})"
        for b in stale[:15]
    )

    # Get recent claims
    with get_conn() as conn:
        recent_claims = conn.execute(
            """SELECT c.claim_text, c.confidence, s.title, s.id AS source_id
               FROM claims c
               JOIN sources s ON c.source_id = s.id
               WHERE s.ingested_at >= NOW() - INTERVAL '30 days'
               ORDER BY c.confidence DESC
               LIMIT 30"""
        ).fetchall()

    evidence_text = "\n".join(
        f"- [{r.get('source_id', '?')}] {r['claim_text'][:150]} (conf: {r.get('confidence', '?')})"
        for r in recent_claims
    ) if recent_claims else "(no recent claims)"

    prompt = _REVIEW_PROMPT.format(
        beliefs_text=beliefs_text,
        evidence_text=evidence_text,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="beliefs_review",
            timeout=180,
        )
        response_text = result.text
    except Exception as e:
        log.error("beliefs_review_failed", error=str(e)[:200])
        return f"Belief review failed: {str(e)[:200]}"

    # Parse structured output for summary
    parsed = _parse_json(response_text)
    reviews = parsed.get("reviews", [])

    # Build summary
    summary_lines = [response_text]
    if reviews:
        summary_lines.append("\n---\n**Summary:**")
        for r in reviews:
            direction_icon = {"up": "↑", "down": "↓", "unchanged": "→"}.get(r.get("direction", ""), "?")
            summary_lines.append(
                f"- `{r.get('belief_id', '?')}` {direction_icon} → "
                f"suggested conf: {r.get('suggested_confidence', '?')}"
            )
        summary_lines.append(
            f"\nUse `/beliefs update <id> <confidence> <reason>` to apply updates."
        )

    return "\n".join(summary_lines)


# ---------------------------------------------------------------------------
# /beliefs synthesis <topic>
# ---------------------------------------------------------------------------

_SYNTHESIS_PROMPT = """\
You are synthesizing the user's tracked beliefs about a topic into a coherent narrative.

## Topic: {topic}

## Active Beliefs
{beliefs_text}

## Theme Context
{theme_context}

## Recent Breakthroughs
{breakthroughs_text}

## Instructions

Generate a synthesis with these sections:

1. **Current Position**: "Your current position on [topic] is..." (2-3 sentences)
2. **Key Beliefs**: For each belief — the claim, confidence, and key evidence
3. **Strongest Evidence**: What is the most solid ground?
4. **Open Questions**: What remains uncertain?
5. **Belief Tensions**: If any beliefs seem incompatible, flag them
6. **Landscape Changes**: Recent breakthroughs or shifts that may affect these beliefs
7. **Suggested Actions**: What to read, add, update, or review next

Write a substantive narrative, not a list. Ground everything in the specific beliefs provided.
"""


def _handle_synthesis(topic: str, executor, on_progress, log) -> str:
    """Synthesize beliefs for a topic into a narrative."""
    from retrieval.landscape import get_beliefs_for_synthesis

    if not topic:
        return "Usage: `/beliefs synthesis <topic>`"

    if on_progress:
        on_progress(f"Gathering beliefs for **{topic}**...")

    ctx = get_beliefs_for_synthesis(topic)
    beliefs = ctx.get("beliefs", [])

    if not beliefs:
        return (
            f"No active beliefs found for **{topic}**.\n\n"
            f"Use `/beliefs add <statement>` to start tracking beliefs about this topic."
        )

    beliefs_text = "\n".join(
        f"- **{b['claim']}** (conf: {b.get('confidence', '?')}, "
        f"type: {b.get('belief_type', '?')}, "
        f"evidence: {len(b.get('evidence_for') or [])}↑ {len(b.get('evidence_against') or [])}↓)"
        for b in beliefs
    )

    theme_ids = list(set(s.get("theme_id") for s in ctx.get("state_summaries", []) if s.get("theme_id")))
    if theme_ids:
        from retrieval.wiki_retrieval import gather_wiki_context, format_wiki_context_block
        wiki_ctx = gather_wiki_context(theme_ids=theme_ids[:5])
        theme_context = format_wiki_context_block(wiki_ctx, header="Theme Context", max_chars_per_theme=2000) or "(no theme context)"
    else:
        theme_context = "(no theme context)"

    breakthroughs_text = "\n".join(
        f"- {b.get('description', '?')} ({b.get('theme_name', '?')})"
        for b in ctx.get("recent_breakthroughs", [])
    ) or "(no recent breakthroughs)"

    prompt = _SYNTHESIS_PROMPT.format(
        topic=topic,
        beliefs_text=beliefs_text,
        theme_context=theme_context,
        breakthroughs_text=breakthroughs_text,
    )

    if on_progress:
        on_progress(f"Synthesizing {len(beliefs)} beliefs...")

    try:
        result = executor.run_raw(
            prompt,
            session_id="beliefs_synthesis",
            timeout=180,
        )
        return f"**Belief Synthesis: {topic}**\n\n{result.text}"
    except Exception as e:
        log.error("beliefs_synthesis_failed", error=str(e)[:200])
        return f"Belief synthesis failed: {str(e)[:200]}"


# ---------------------------------------------------------------------------
# /beliefs suggest
# ---------------------------------------------------------------------------

_SUGGEST_PROMPT = """\
You are identifying potential beliefs that emerge from claim convergence in a knowledge engine.

## Claim Clusters (3+ sources converging on similar topics)
{clusters_text}

## Existing Beliefs (avoid duplicates)
{existing_text}

## Instructions

Identify claim clusters where multiple sources converge on a pattern that could form a trackable belief.
Only propose beliefs that:
1. Are supported by claims from 3+ different sources
2. Are NOT already tracked (check existing beliefs above)
3. Are specific and falsifiable — not generic truisms. Each belief MUST have a clear falsification criterion.
4. Fall into one of: factual, predictive, methodological, or meta

**IMPORTANT — diversity requirement:** You MUST include at least one belief about:
- A **limitation, risk, or constraint** (e.g., "Current RLHF methods cannot align models on distribution-shifted inputs")
- An **architectural or methodological constraint** (e.g., "Transformer attention is fundamentally O(n²) and no proven sub-quadratic alternative maintains quality")

Do NOT only suggest capability-expansion claims. The most valuable beliefs to track are about what AI *cannot* do or where it is stuck.

Output a JSON block:
```json
{{
  "suggestions": [
    {{
      "claim": "The belief statement",
      "belief_type": "factual|predictive|methodological|meta",
      "category": "capability|limitation|risk|architectural|methodological",
      "confidence": 0.0-1.0,
      "falsifiable_by": "Describe the specific evidence that would disprove this belief",
      "supporting_claim_ids": ["claim_id_1", "claim_id_2", "claim_id_3"],
      "source_count": 3,
      "reasoning": "Why this pattern warrants tracking as a belief"
    }}
  ]
}}
```
"""


def _handle_suggest(topic_filter: str, executor, on_progress, log) -> str:
    """Suggest beliefs from claim convergence patterns."""
    from reading_app.db import get_conn, get_active_beliefs, find_similar_belief

    if executor is None:
        return (
            "**Belief suggestion requires an LLM executor.**\n\n"
            "Check your configuration — the executor was not initialised."
        )

    if on_progress:
        on_progress("Identifying claim convergence patterns...")

    # Find claim clusters: claims grouped by theme with 3+ sources
    with get_conn() as conn:
        # Get themes with sufficient claims from multiple sources
        if topic_filter:
            theme_filter_sql = "AND (t.id = %s OR t.name ILIKE %s)"
            params = (topic_filter, f"%{topic_filter}%")
        else:
            theme_filter_sql = ""
            params = ()

        clusters = conn.execute(
            f"""SELECT t.id AS theme_id, t.name AS theme_name,
                   COUNT(DISTINCT c.source_id) AS source_count,
                   COUNT(c.id) AS claim_count,
                   array_agg(DISTINCT c.source_id) AS source_ids
               FROM claims c
               JOIN source_themes st ON c.source_id = st.source_id
               JOIN themes t ON st.theme_id = t.id
               WHERE c.confidence >= 0.5
                 {theme_filter_sql}
               GROUP BY t.id, t.name
               HAVING COUNT(DISTINCT c.source_id) >= 3
               ORDER BY COUNT(DISTINCT c.source_id) DESC
               LIMIT 10""",
            params,
        ).fetchall()

        if not clusters:
            return (
                "**No claim convergence patterns found.**\n\n"
                "Need at least 3 sources with overlapping claims in a theme. "
                "Keep reading and ingesting sources."
            )

        # For each cluster, get representative claims
        cluster_claims = {}
        for cluster in clusters:
            claims = conn.execute(
                """SELECT c.id, c.claim_text, c.source_id, c.confidence,
                      s.title AS source_title
                   FROM claims c
                   JOIN source_themes st ON c.source_id = st.source_id
                   JOIN sources s ON c.source_id = s.id
                   WHERE st.theme_id = %s
                     AND c.confidence >= 0.5
                   ORDER BY c.confidence DESC
                   LIMIT 15""",
                (cluster["theme_id"],),
            ).fetchall()
            cluster_claims[cluster["theme_id"]] = claims

    # Get existing beliefs for dedup
    existing = get_active_beliefs()
    existing_text = "\n".join(
        f"- {truncate(b['claim'], 110)}" for b in existing
    ) or "(no existing beliefs)"

    # Build clusters text
    clusters_text_parts = []
    for cluster in clusters:
        tid = cluster["theme_id"]
        claims = cluster_claims.get(tid, [])
        clusters_text_parts.append(
            f"### {cluster['theme_name']} ({cluster['source_count']} sources, "
            f"{cluster['claim_count']} claims)"
        )
        for c in claims[:5]:
            clusters_text_parts.append(
                f"- [{truncate(c.get('source_title', '?'), 50)}] "
                f"{truncate_sentences(c['claim_text'], 250)} "
                f"(id: {c['id']})"
            )
        clusters_text_parts.append("")

    clusters_text = "\n".join(clusters_text_parts)

    if on_progress:
        on_progress(f"Analysing {len(clusters)} theme clusters for belief candidates...")

    prompt = _SUGGEST_PROMPT.format(
        clusters_text=clusters_text,
        existing_text=existing_text,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="beliefs_suggest",
            timeout=120,
        )
        llm_text = result.text
    except Exception as e:
        log.error("beliefs_suggest_failed", error=str(e)[:200])
        # Informative fallback: show cluster stats even without LLM
        return _format_cluster_fallback(clusters)

    parsed = _parse_json(llm_text)
    suggestions = parsed.get("suggestions", [])

    # Clamp confidence values for consistency with _handle_add
    for s in suggestions:
        conf = s.get("confidence", 0.5)
        if not isinstance(conf, (int, float)) or conf < 0 or conf > 1:
            s["confidence"] = 0.5

    if not suggestions:
        return _format_cluster_fallback(clusters)

    # Filter out near-duplicates of existing beliefs
    filtered = []
    for s in suggestions:
        try:
            similar = find_similar_belief(s["claim"], threshold=0.6)
            if similar:
                log.info("beliefs_suggest_duplicate", claim=s["claim"][:60])
                continue
        except Exception:
            pass
        filtered.append(s)

    # Enforce diversity: at least one limitation/risk/architectural/methodological belief
    has_diverse = any(
        (s.get("category") or "").lower() in _DIVERSITY_CATEGORIES
        or (s.get("belief_type") or "").lower() in _DIVERSITY_CATEGORIES
        for s in filtered
    )
    diversity_warning = ""
    if filtered and not has_diverse:
        diversity_warning = (
            "\n> **Note:** All suggestions are capability-focused. "
            "Consider manually adding a limitation or risk belief "
            "(`/beliefs add <claim>`) for balanced coverage.\n"
        )
        log.warning("beliefs_suggest_no_diversity", count=len(filtered))

    # Format response
    lines = [f"**Belief Candidates** ({len(filtered)} suggestions)\n"]
    if diversity_warning:
        lines.append(diversity_warning)

    # Show narrative
    json_start = llm_text.find("```json")
    if json_start > 0:
        lines.append(llm_text[:json_start].strip())
        lines.append("")

    for i, s in enumerate(filtered, 1):
        category = s.get("category", "")
        cat_badge = f" [{category}]" if category else ""
        lines.append(
            f"### {i}. [{s.get('belief_type', '?')}]{cat_badge} (conf: {s.get('confidence', '?')}, "
            f"{s.get('source_count', '?')} sources)"
        )
        lines.append(f"**{s['claim']}**")
        if s.get("falsifiable_by"):
            lines.append(f"Falsifiable by: _{s['falsifiable_by']}_")
        if s.get("reasoning"):
            lines.append(f"Reasoning: _{s['reasoning']}_")
        lines.append(
            f"\nTo track: `/beliefs add {s['claim']}`"
        )
        lines.append("")

    if not filtered:
        lines.append("All suggestions were too similar to existing beliefs.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON parsing (same pattern as implications_handler)
# ---------------------------------------------------------------------------

def _format_cluster_fallback(clusters: list[dict]) -> str:
    """Format cluster stats with top claims when LLM analysis is unavailable."""
    from reading_app.db import get_conn

    lines = [
        "**Belief Candidates — Cluster Analysis**\n",
        f"Found {len(clusters)} theme clusters with 3+ converging sources.\n",
    ]

    try:
        with get_conn() as conn:
            for c in clusters[:5]:
                lines.append(
                    f"### {c['theme_name']} ({c['source_count']} sources, "
                    f"{c['claim_count']} claims)"
                )
                source_ids = c.get("source_ids", [])
                if source_ids:
                    top_claims = conn.execute(
                        """SELECT claim_text, confidence FROM claims
                           WHERE source_id = ANY(%s) AND confidence >= 0.8
                           ORDER BY confidence DESC LIMIT 3""",
                        (source_ids,),
                    ).fetchall()
                    if top_claims:
                        lines.append("Potential beliefs worth tracking:")
                        for cl in top_claims:
                            lines.append(
                                f"  - {cl['claim_text'][:150]} "
                                f"(conf: {cl['confidence']:.2f})"
                            )
                lines.append("")
    except Exception:
        logger.debug("Failed to fetch claims for cluster fallback", exc_info=True)

    lines.append(
        "LLM analysis was unavailable. Use `/beliefs add <statement>` "
        "to track beliefs you identify from the claims above."
    )
    return "\n".join(lines)


def _parse_json(text: str) -> dict:
    """Extract JSON block from LLM output."""
    result = parse_json_from_llm(text, expect=dict)
    if result is None:
        logger.warning("beliefs_no_json_parsed")
        return {}
    return result
