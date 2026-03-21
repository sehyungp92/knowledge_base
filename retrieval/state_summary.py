"""State summary generation for landscape themes.

Generates temporal trajectory narratives for themes based on their
capabilities, limitations, bottlenecks, breakthroughs, and history.
Called by heartbeat for periodic regeneration.
"""

from __future__ import annotations

import logging
import re
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

{analysis_section}---

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


ANALYSIS_PROMPT = """You are pre-digesting landscape data for the AI theme "{theme_name}" to guide a narrative synthesis.

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

## Delta Since Last Summary
{delta_text}

## Previous Summary
{previous_summary}

---

Produce a structured analysis with these sections (use plain text, not JSON):

KEY MOVEMENTS: 3-5 most significant trajectory shifts — not just listing entities, but describing what moved and why. Focus on changes since the last summary.

TENSIONS: Signals that conflict — e.g. a capability advancing while a related limitation worsens, or a breakthrough that doesn't resolve the expected bottleneck. If none, say so.

WHAT CHANGED: Explicit comparison to the previous summary — what's new, what shifted, what's no longer relevant. If this is the first summary, describe the current state instead.

COVERAGE ASSESSMENT: Where evidence is thin/stale (few sources, old dates) vs rich/fresh. Flag entities with no source dates or only pre-2025 dates.

NARRATIVE FOCUS: What should the summary emphasize? What's the most important story to tell about this theme right now?

Be specific — name concrete entities. Keep each section to 2-4 sentences.
"""

QUALITY_CHECK_PROMPT = """Rate this state summary for the AI theme "{theme_name}" on three criteria.

## Summary
{summary}
{ground_truth_section}
---

Score each 1-5 (1=poor, 5=excellent):

TEMPORAL_LANGUAGE: Does it describe trajectories, shifts, and momentum — or does it read like a static inventory?
  Score 2: "The field has capabilities in X and limitations in Y." (static inventory)
  Score 4: "Since Q3 2025, X shifted from demo-stage to narrow production as Y limitation eased." (trajectory)

SPECIFICITY: Does it name concrete capabilities, bottlenecks, and breakthroughs — or use vague generalities?
  Score 2: "Several models show improved performance on benchmarks." (vague)
  Score 4: "GPT-4o scores 88.7% on MMLU while Gemini Ultra reaches 90.0%, though both plateau on ARC-AGI." (concrete)
{specificity_guidance}
NARRATIVE_FLOW: Does it tell a coherent story with cause-and-effect — or just list items in paragraph form?
  Score 2: "There are capabilities. There are also limitations. Bottlenecks exist." (list-as-paragraphs)
  Score 4: "The breakthrough in X alleviated bottleneck Y, but this exposed a new limitation Z that now gates further progress." (cause-and-effect)

Return ONLY three lines:
TEMPORAL_LANGUAGE: N
SPECIFICITY: N
NARRATIVE_FLOW: N
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

    # Source-count staleness: regenerate if many new sources since last summary
    try:
        with db.get_conn() as conn:
            new_sources = conn.execute(
                """SELECT COUNT(*) AS c FROM source_themes st
                   JOIN sources s ON s.id = st.source_id
                   WHERE st.theme_id = %s AND s.created_at > %s""",
                (theme.get("id"), updated_at),
            ).fetchone()["c"]
        if new_sources >= 5:
            return True
    except Exception:
        pass  # Fall through to age-based check

    age = datetime.now(timezone.utc) - updated_at
    return age > timedelta(days=STALENESS_DAYS)


def _compute_temporal_delta(theme_id: str, last_updated: datetime | None) -> str:
    """Compute what changed since the last state summary generation.

    Queries for new entities, status changes, new sources, and anticipation
    updates since the last summary was written.
    """
    if not last_updated:
        return "First summary generation — no prior baseline."

    if isinstance(last_updated, str):
        last_updated = datetime.fromisoformat(last_updated)
    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)

    parts = []
    try:
        with db.get_conn() as conn:
            # New capabilities since last summary
            new_caps = conn.execute(
                """SELECT COUNT(*) AS c FROM capabilities
                   WHERE theme_id = %s AND created_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if new_caps:
                parts.append(f"{new_caps} new capabilities added")

            # New limitations
            new_lims = conn.execute(
                """SELECT COUNT(*) AS c FROM limitations
                   WHERE theme_id = %s AND created_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if new_lims:
                parts.append(f"{new_lims} new limitations recorded")

            # New bottlenecks
            new_bns = conn.execute(
                """SELECT COUNT(*) AS c FROM bottlenecks
                   WHERE theme_id = %s AND created_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if new_bns:
                parts.append(f"{new_bns} new bottlenecks identified")

            # New breakthroughs
            new_bts = conn.execute(
                """SELECT COUNT(*) AS c FROM breakthroughs
                   WHERE theme_id = %s AND created_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if new_bts:
                parts.append(f"{new_bts} new breakthroughs detected")

            # Landscape history changes (field updates on existing entities)
            # Exclude anticipations — counted separately below
            field_changes = conn.execute(
                """SELECT entity_type, field, COUNT(*) AS c
                   FROM landscape_history
                   WHERE theme_id = %s AND changed_at > %s
                     AND entity_type != 'anticipation'
                   GROUP BY entity_type, field""",
                (theme_id, last_updated),
            ).fetchall()
            for fc in field_changes:
                parts.append(
                    f"{fc['c']} {fc['entity_type']}.{fc['field']} update(s)"
                )

            # New sources ingested for this theme
            new_sources = conn.execute(
                """SELECT COUNT(*) AS c FROM source_themes st
                   JOIN sources s ON s.id = st.source_id
                   WHERE st.theme_id = %s AND s.created_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if new_sources:
                parts.append(f"{new_sources} new sources ingested")

            # Anticipation status changes
            ant_changes = conn.execute(
                """SELECT COUNT(*) AS c FROM landscape_history
                   WHERE theme_id = %s AND entity_type = 'anticipation'
                     AND changed_at > %s""",
                (theme_id, last_updated),
            ).fetchone()["c"]
            if ant_changes:
                parts.append(f"{ant_changes} anticipation status change(s)")

    except Exception:
        logger.debug("Failed to compute temporal delta for %s", theme_id, exc_info=True)
        return "Delta computation unavailable."

    if not parts:
        return f"No recorded changes since last summary ({str(last_updated)[:10]})."

    return f"Since last summary ({str(last_updated)[:10]}): " + ", ".join(parts) + "."


def _score_summary(
    summary: str,
    theme_name: str,
    theme_id: str,
    executor,
    entity_names: list[str] | None = None,
) -> float | None:
    """Score a summary on quality dimensions. Returns average score (1-5) or None on parse failure."""
    ground_truth_section = ""
    specificity_guidance = ""
    if entity_names:
        ground_truth_section = (
            "\n## Ground Truth Entities\n"
            + ", ".join(entity_names[:30])
            + "\n"
        )
        specificity_guidance = (
            "  Score 4-5 only if the summary references entities from the ground truth list. "
            "Score 1-2 if it uses vague generalities or names entities not in the list.\n"
        )

    prompt = QUALITY_CHECK_PROMPT.format(
        theme_name=theme_name,
        summary=summary,
        ground_truth_section=ground_truth_section,
        specificity_guidance=specificity_guidance,
    )
    session_id = f"state_quality_check_{theme_id}"
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
            for key in ("TEMPORAL_LANGUAGE", "SPECIFICITY", "NARRATIVE_FLOW"):
                if line.strip().startswith(key):
                    m = re.search(r"(\d)", line.split(":", 1)[-1])
                    if m:
                        val = int(m.group(1))
                        if 1 <= val <= 5:
                            scores[key] = val

        if len(scores) < 3:
            logger.debug("Quality check parse incomplete for %s: %s", theme_id, scores)
            return None

        return sum(scores.values()) / len(scores)
    except Exception:
        logger.debug("Quality check failed for %s", theme_name, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


def _validate_summary_quality(
    summary: str,
    theme_name: str,
    theme_id: str,
    executor,
    entity_names: list[str] | None = None,
) -> tuple[bool, str, float | None]:
    """Check if summary meets trajectory narrative standards.

    Returns (passes, feedback, avg_score). A summary passes if average score >= 3.
    """
    avg = _score_summary(summary, theme_name, theme_id, executor, entity_names)
    if avg is None:
        return True, "", None  # Can't parse — accept

    if avg >= 3:
        return True, "", avg

    feedback = (
        f"Quality scores averaged {avg:.1f}/5. "
        "The summary reads too much like a static inventory. "
        "Rewrite with stronger temporal language (trajectories, shifts, momentum), "
        "more specific entity references, and cause-and-effect narrative flow."
    )
    return False, feedback, avg


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
            for i in state.get("cross_theme_implications", [])
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

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    theme_name = theme.get("name", theme_id)
    previous_summary = theme.get("state_summary") or "None — first generation."

    # Compute temporal delta (what changed since last summary)
    delta_text = _compute_temporal_delta(
        theme_id, theme.get("state_summary_updated_at")
    )

    # Phase 1: Structured analysis (Haiku — fast, cheap)
    analysis_prompt = ANALYSIS_PROMPT.format(
        theme_name=theme_name,
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
        delta_text=delta_text,
        previous_summary=previous_summary,
    )

    analysis_text = ""
    analysis_session = f"state_analysis_{theme_id}"
    try:
        analysis_result = executor.run_raw(
            analysis_prompt,
            session_id=analysis_session,
            model="haiku",
            timeout=30,
        )
        analysis_text = analysis_result.text.strip()
        logger.info("Phase 1 analysis for %s: %d chars", theme_id, len(analysis_text))
    except Exception:
        logger.warning("Phase 1 analysis failed for %s, proceeding without", theme_id, exc_info=True)
    finally:
        try:
            executor.cleanup_session(analysis_session)
        except Exception:
            pass

    # Phase 2: Narrative synthesis (Sonnet)
    analysis_section = ""
    if analysis_text:
        analysis_section = (
            f"## Pre-Analysis (editorial direction)\n{analysis_text}\n\n"
            "Use this pre-analysis to guide your narrative focus and emphasis.\n\n"
        )

    prompt = STATE_SUMMARY_PROMPT.format(
        theme_name=theme_name,
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
        previous_summary=previous_summary,
        analysis_section=analysis_section,
    )

    session_id = f"state_summary_{theme_id}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="sonnet",
            timeout=90,
        )
        summary = result.text.strip()
        if not summary or len(summary) < 50:
            logger.warning("State summary too short for %s: %d chars", theme_id, len(summary))
            return None

        # Extract entity names for quality gate ground truth
        entity_names = [
            entity.get("description", "")[:60]
            for key in ("capabilities", "limitations", "bottlenecks")
            for entity in state[key]
            if entity.get("description")
        ]

        # Quality gate: check if the summary meets narrative standards
        passes, feedback, original_score = _validate_summary_quality(
            summary, theme_name, theme_id, executor, entity_names=entity_names
        )
        if not passes:
            logger.info("Quality gate failed for %s (score: %s), retrying with feedback",
                        theme_id, original_score)
            retry_prompt = prompt + f"\n\nIMPORTANT CORRECTION: {feedback}"
            retry_session = f"state_summary_retry_{theme_id}"
            try:
                retry_result = executor.run_raw(
                    retry_prompt,
                    session_id=retry_session,
                    model="sonnet",
                    timeout=90,
                )
                retry_text = retry_result.text.strip()
                if retry_text and len(retry_text) >= 50:
                    # Re-score the retry to verify improvement
                    retry_score = _score_summary(
                        retry_text, theme_name, theme_id, executor,
                        entity_names=entity_names,
                    )
                    if retry_score is not None and (
                        retry_score >= 3
                        or (original_score is not None and retry_score > original_score)
                    ):
                        summary = retry_text
                        logger.info("Retry improved summary for %s (score: %.1f -> %.1f)",
                                    theme_id, original_score or 0, retry_score)
                    elif original_score is not None and retry_score is not None and retry_score <= original_score:
                        logger.info("Retry did not improve for %s (score: %.1f -> %.1f), keeping original",
                                    theme_id, original_score, retry_score)
                    else:
                        # Can't score retry — accept it if it's long enough
                        summary = retry_text
                        logger.info("Retry accepted without scoring for %s", theme_id)
            except Exception:
                logger.debug("Quality retry failed for %s, using original", theme_id, exc_info=True)
            finally:
                try:
                    executor.cleanup_session(retry_session)
                except Exception:
                    pass

        db.update_theme_state_summary(theme_id, summary)
        logger.info("Generated state summary for %s (%d chars)", theme_id, len(summary))
        return summary

    except Exception:
        logger.error("Failed to generate state summary for %s", theme_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass
