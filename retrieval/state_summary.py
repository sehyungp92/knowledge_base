"""State summary generation for landscape themes.

Generates temporal trajectory narratives for themes based on their
capabilities, limitations, bottlenecks, breakthroughs, and history.
Called by heartbeat for periodic regeneration.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from reading_app import db
from retrieval.landscape import get_consolidated_implications, get_theme_state

logger = logging.getLogger(__name__)

# Minimum sources before generating a summary (avoid thin summaries)
MIN_SOURCE_THRESHOLD = 3

# Regenerate if summary is older than this
STALENESS_DAYS = 7

STATE_SUMMARY_PROMPT = """You are generating a temporal trajectory narrative for the AI theme "{theme_name}".

This should read as a STORY OF MOVEMENT — how this theme got to its current state and where it appears headed.
Do NOT write a static inventory. Frame everything with trajectory: "was X, shifted to Y because of Z, now moving toward W."

## Current Landscape Data

**Capabilities ({n_caps} total):**
{capabilities_text}

**Limitations ({n_lims} total):**
{limitations_text}

**Bottlenecks ({n_bns} total):**
{bottlenecks_text}

**Recent Breakthroughs:**
{breakthroughs_text}

**Active Anticipations:**
{anticipations_text}

**Cross-Theme Implications:**
{implications_text}

## Recent Changes (landscape_history)
{history_text}

## Previous Summary (if any)
{previous_summary}

---

Write a 3-5 paragraph narrative summary (200-400 words) that:
1. Opens with the theme's current trajectory in one sentence
2. Describes how key bottlenecks have shifted (or remained stuck)
3. Notes capability maturity changes and what drove them
4. Identifies where momentum is building or stalling
5. Closes with what to watch for next

Pay attention to source dates in brackets. A capability described in a 2023 source may have evolved since.
Distinguish between "what sources say" and "what is likely true now given the trajectory."
When history entries show source_published_at, use that to establish when changes happened in the field
(not just when we ingested them).

Write in present tense. Be specific — name concrete capabilities, bottlenecks, and breakthroughs.
Do NOT list items — synthesize them into a narrative.
"""


def should_regenerate(theme: dict, source_count: int) -> bool:
    """Check if a theme's state_summary should be regenerated.

    Args:
        theme: Theme dict with state_summary, state_summary_updated_at, velocity.
        source_count: Number of sources classified under this theme.

    Returns:
        True if the summary should be regenerated.
    """
    if source_count < MIN_SOURCE_THRESHOLD:
        return False

    summary = theme.get("state_summary")
    updated_at = theme.get("state_summary_updated_at")

    if not summary:
        return True

    if not updated_at:
        return True

    if isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at)

    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=timezone.utc)

    age = datetime.now(timezone.utc) - updated_at
    return age > timedelta(days=STALENESS_DAYS)


def generate_theme_state_summary(
    theme_id: str,
    executor=None,
) -> str | None:
    """Generate a temporal trajectory narrative for a theme.

    Gathers capabilities, limitations, bottlenecks, breakthroughs,
    anticipations, and history, then calls LLM to synthesize.

    Args:
        theme_id: Theme to generate summary for.
        executor: ClaudeExecutor instance.

    Returns:
        Generated summary text, or None on failure.
    """
    state = get_theme_state(theme_id)
    if not state.get("theme"):
        logger.warning("Theme %s not found", theme_id)
        return None

    theme = state["theme"]

    # Gather landscape history for trajectory context (scoped to this theme)
    try:
        recent_history = db.get_landscape_history_for_theme(theme_id, limit=20)
    except Exception:
        recent_history = []

    # Build source date lookup for enriching landscape data
    source_dates = {}
    try:
        all_source_ids = set()
        for entity_list in [state["capabilities"], state["limitations"], state["bottlenecks"]]:
            for entity in entity_list:
                ev = entity.get("evidence_sources")
                if isinstance(ev, list):
                    for e in ev:
                        if isinstance(e, dict) and e.get("source_id"):
                            all_source_ids.add(e["source_id"])
        if all_source_ids:
            with db.get_conn() as conn:
                rows = conn.execute(
                    "SELECT id, published_at, title FROM sources WHERE id = ANY(%s)",
                    (list(all_source_ids),),
                ).fetchall()
                for r in rows:
                    if r.get("published_at"):
                        source_dates[r["id"]] = {
                            "date": str(r["published_at"])[:10],
                            "title": r.get("title", ""),
                        }
    except Exception:
        logger.debug("Failed to build source date lookup for state summary", exc_info=True)

    def _source_date_tag(entity: dict) -> str:
        """Build a [YYYY-MM-DD] tag from the entity's evidence sources."""
        ev = entity.get("evidence_sources")
        if not isinstance(ev, list):
            return ""
        dates = []
        for e in ev:
            if isinstance(e, dict) and e.get("source_id"):
                info = source_dates.get(e["source_id"])
                if info:
                    dates.append(info["date"])
        if dates:
            # Use the most recent source date
            return f"[{max(dates)}] "
        return ""

    # Format data for prompt
    caps_text = "\n".join(
        f"- {_source_date_tag(c)}{c['description']} (maturity: {c.get('maturity', '?')})"
        for c in state["capabilities"]
    ) or "None recorded."

    lims_text = "\n".join(
        f"- {_source_date_tag(l)}{l['description']} (type: {l.get('limitation_type', '?')}, severity: {l.get('severity', '?')}, trajectory: {l.get('trajectory', '?')})"
        for l in state["limitations"]
    ) or "None recorded."

    bns_text = "\n".join(
        f"- {_source_date_tag(b)}{b['description']} (type: {b.get('bottleneck_type', '?')}, horizon: {b.get('resolution_horizon', '?')}, blocking: {b.get('blocking_what', '?')})"
        for b in state["bottlenecks"]
    ) or "None recorded."

    bts_text = "\n".join(
        f"- {b['description']} (significance: {b.get('significance', '?')})"
        for b in state["breakthroughs"]
    ) or "None in recent window (significance-scaled: 90d-730d)."

    ants_text = "\n".join(
        f"- {a['prediction']} (confidence: {a.get('confidence', '?')}, timeline: {a.get('timeline', '?')})"
        for a in state["anticipations"]
    ) or "None active."

    # Use consolidated implications for compact display
    try:
        consolidated = get_consolidated_implications(theme_id)
        impls_text = "\n".join(
            f"- {c['source_theme']} -> {c['target_theme']}: {c['top_implication']} "
            f"({c['observation_count']} obs, confidence: {c.get('max_confidence', '?')})"
            for c in consolidated
        ) or "None recorded."
    except Exception:
        impls_text = "\n".join(
            f"- {i['implication']} ({i.get('source_theme', '?')} -> {i.get('target_theme', '?')})"
            for i in state["cross_theme_implications"]
        ) or "None recorded."

    def _history_date_label(h: dict) -> str:
        """Build a date label preferring source_published_at over changed_at."""
        source_pub = h.get("source_published_at")
        changed = h.get("changed_at")
        if source_pub:
            return f"field:{str(source_pub)[:10]}, ingested:{str(changed)[:10]}"
        return f"ingested:{str(changed)[:10]}" if changed else "?"

    history_text = "\n".join(
        f"- [{_history_date_label(h)}] {h.get('entity_type', '?')}.{h.get('field', '?')}: {h.get('old_value', '?')} -> {h.get('new_value', '?')}"
        for h in recent_history
    ) or "No recent changes."

    prompt = STATE_SUMMARY_PROMPT.format(
        theme_name=theme.get("name", theme_id),
        n_caps=len(state["capabilities"]),
        capabilities_text=caps_text,
        n_lims=len(state["limitations"]),
        limitations_text=lims_text,
        n_bns=len(state["bottlenecks"]),
        bottlenecks_text=bns_text,
        breakthroughs_text=bts_text,
        anticipations_text=ants_text,
        implications_text=impls_text,
        history_text=history_text,
        previous_summary=theme.get("state_summary") or "None — first generation.",
    )

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    session_id = f"state_summary_{theme_id}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="sonnet",
            timeout=90,
        )
        executor.cleanup_session(session_id)
        summary = result.text.strip()
        if not summary or len(summary) < 50:
            logger.warning("State summary too short for %s: %d chars", theme_id, len(summary))
            return None

        db.update_theme_state_summary(theme_id, summary)
        logger.info("Generated state summary for %s (%d chars)", theme_id, len(summary))
        return summary

    except Exception:
        logger.error("Failed to generate state summary for %s", theme_id, exc_info=True)
        return None
