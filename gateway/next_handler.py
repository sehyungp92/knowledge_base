"""Direct Python handler for /next jobs.

Reading queue generator — combines gap analysis (blind spot bottlenecks,
unvalidated limitations, belief gaps) with bottleneck priority ranking
to generate "read these next" recommendations with search terms.
"""

from __future__ import annotations

import json
import time
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job
from reading_app.text_utils import truncate

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_next_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /next directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("next_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    count, focus_theme = _parse_command(text)
    log = log.bind(count=count, focus_theme=focus_theme)

    if on_progress:
        on_progress("Analysing coverage gaps and bottleneck priorities...")

    result = _generate_reading_queue(count, focus_theme, executor, on_progress, log)

    elapsed = time.monotonic() - t0
    log.info("next_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[int, str | None]:
    """Parse '/next [N] [theme]'.

    Returns (count, theme_or_None).
    """
    cleaned = text.strip()
    for prefix in ("/next ", "/next"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    count = 5
    focus_theme = None

    parts = cleaned.split()
    for part in parts:
        try:
            count = int(part)
            count = max(1, min(count, 15))
        except ValueError:
            focus_theme = part

    return count, focus_theme


# ---------------------------------------------------------------------------
# Queue generation
# ---------------------------------------------------------------------------

def _generate_reading_queue(
    count: int,
    focus_theme: str | None,
    executor,
    on_progress,
    log,
) -> str:
    """Gather signals from multiple gap sources and rank into a reading queue."""
    from retrieval.landscape import (
        get_blind_spot_bottlenecks,
        get_validation_backlog,
        get_belief_coverage_gaps,
        get_theme_source_counts,
        get_bottleneck_ranking,
        get_untested_anticipations,
    )

    # Gather all signals
    signals = []

    # 1. Blind spot bottlenecks (no active approaches)
    try:
        blind_spots = get_blind_spot_bottlenecks()
        for bn in blind_spots:
            if focus_theme and bn.get("theme_id") != focus_theme and \
               focus_theme.lower() not in (bn.get("theme_name") or "").lower():
                continue
            signals.append({
                "type": "blind_spot_bottleneck",
                "priority": _horizon_priority(bn.get("resolution_horizon", "")),
                "theme": bn.get("theme_name", "?"),
                "theme_id": bn.get("theme_id"),
                "description": bn.get("description", ""),
                "reason": f"Bottleneck with no active approaches (confidence: {bn.get('confidence', '?')})",
                "search_hint": _bottleneck_to_search(bn),
            })
    except Exception as e:
        log.warning("next_blind_spots_failed", error=str(e)[:200])

    # 2. Validation backlog (themes with most unvalidated implicit limitations)
    try:
        backlog = get_validation_backlog()
        for entry in backlog[:5]:
            if focus_theme and entry.get("theme_id") != focus_theme and \
               focus_theme.lower() not in (entry.get("theme_name") or "").lower():
                continue
            signals.append({
                "type": "validation_backlog",
                "priority": min(entry.get("unvalidated_count", 0) * 0.3, 5.0),
                "theme": entry.get("theme_name", "?"),
                "theme_id": entry.get("theme_id"),
                "description": f"{entry['unvalidated_count']} unvalidated implicit limitations",
                "reason": "Implicit limitations need evidence to confirm or reject",
                "search_hint": f"{entry.get('theme_name', '')} limitations benchmarks evaluation",
            })
    except Exception as e:
        log.warning("next_validation_backlog_failed", error=str(e)[:200])

    # 3. High-priority bottlenecks (ranked by impact)
    try:
        ranked = get_bottleneck_ranking()
        for bn in ranked[:8]:
            if focus_theme and bn.get("theme_id") != focus_theme and \
               focus_theme.lower() not in (bn.get("theme_name") or "").lower():
                continue
            # Only add if not already a blind spot
            if not any(s["description"] == bn.get("description") for s in signals):
                signals.append({
                    "type": "high_priority_bottleneck",
                    "priority": (bn.get("horizon_score") or 0) * (bn.get("confidence") or 0.5),
                    "theme": bn.get("theme_name", "?"),
                    "theme_id": bn.get("theme_id"),
                    "description": bn.get("description", ""),
                    "reason": f"High-leverage bottleneck (horizon: {bn.get('resolution_horizon', '?')})",
                    "search_hint": _bottleneck_to_search(bn),
                })
    except Exception as e:
        log.warning("next_bottleneck_ranking_failed", error=str(e)[:200])

    # 4. Belief coverage gaps
    try:
        belief_gaps = get_belief_coverage_gaps()
        for bg in belief_gaps.get("low_confidence_gaps", [])[:3]:
            theme_id = bg.get("domain_theme_id")
            if focus_theme and theme_id != focus_theme and \
               focus_theme.lower() not in (bg.get("theme_name") or "").lower():
                continue
            signals.append({
                "type": "belief_gap",
                "priority": (1.0 - (bg.get("confidence") or 0.5)) * 4,
                "theme": bg.get("theme_name", "?"),
                "theme_id": theme_id,
                "description": f"Low-confidence belief: {bg.get('claim', '')[:100]}",
                "reason": f"Belief at {bg.get('confidence', '?')} confidence needs evidence",
                "search_hint": _belief_to_search(bg),
            })
    except Exception as e:
        log.warning("next_belief_gaps_failed", error=str(e)[:200])

    # 5. Untested anticipations
    try:
        untested = get_untested_anticipations(min_age_days=30)
        for ant in untested[:5]:
            if focus_theme and ant.get("theme_id") != focus_theme and \
               focus_theme.lower() not in (ant.get("theme_name") or "").lower():
                continue
            signals.append({
                "type": "untested_anticipation",
                "priority": min((ant.get("age_days") or 30) / 30, 3.0),
                "theme": ant.get("theme_name", "?"),
                "theme_id": ant.get("theme_id"),
                "description": f"Untested prediction: {ant.get('prediction', '')[:100]}",
                "reason": f"Prediction from {ant.get('age_days', '?')} days ago with no evidence yet",
                "search_hint": _anticipation_to_search(ant),
            })
    except Exception as e:
        log.warning("next_untested_anticipations_failed", error=str(e)[:200])

    # 6. Low-coverage themes
    try:
        theme_counts = get_theme_source_counts()
        for tc in theme_counts:
            sc = tc.get("source_count") or 0
            vel = tc.get("velocity") or 0
            if sc < 2 and vel > 0:
                if focus_theme and tc.get("id") != focus_theme and \
                   focus_theme.lower() not in (tc.get("name") or "").lower():
                    continue
                signals.append({
                    "type": "low_coverage_theme",
                    "priority": vel * 3,
                    "theme": tc.get("name", "?"),
                    "theme_id": tc.get("id"),
                    "description": f"Only {sc} sources for active theme",
                    "reason": f"Theme has velocity={vel:.2f} but thin coverage ({sc} sources)",
                    "search_hint": f"{tc.get('name', '')} AI research 2025 2026",
                })
    except Exception as e:
        log.warning("next_theme_counts_failed", error=str(e)[:200])

    if not signals:
        return (
            "**No reading recommendations found.**\n\n"
            "Your knowledge base appears well-covered! Try:\n"
            "- `/gaps` for detailed coverage analysis\n"
            "- `/bottlenecks` to review current bottleneck landscape"
        )

    # Sort by priority (descending) and deduplicate
    signals.sort(key=lambda s: s.get("priority", 0), reverse=True)
    seen_descriptions = set()
    unique_signals = []
    for s in signals:
        desc_key = s["description"][:80]
        if desc_key not in seen_descriptions:
            seen_descriptions.add(desc_key)
            unique_signals.append(s)

    # Take top N
    top = unique_signals[:count]

    # Use LLM to generate search queries if executor available
    if executor:
        try:
            top = _refine_search_terms(top, executor, log)
        except Exception as e:
            log.debug("next_search_refine_failed", error=str(e)[:200])

    # Persist to reading_queue table
    _persist_queue(top, log)

    return _format_queue(top, count, focus_theme)


# ---------------------------------------------------------------------------
# Search term generation
# ---------------------------------------------------------------------------

def _refine_search_terms(signals: list[dict], executor, log) -> list[dict]:
    """Use LLM to generate better search queries for each recommendation."""
    descriptions = "\n".join(
        f"{i+1}. {s['theme']}: {truncate(s['description'], 175)}"
        for i, s in enumerate(signals)
    )

    prompt = (
        "Generate 1-2 search queries per item for Google Scholar/arXiv.\n\n"
        f"{descriptions}\n\n"
        'JSON array: [{"index": 1, "queries": ["query"]}]'
    )

    result = executor.run_raw(
        prompt,
        session_id="next_search",
        timeout=60,
    )

    # Parse
    import re
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", result.text, re.DOTALL)
    if json_match:
        try:
            items = json.loads(json_match.group(1))
            for item in items:
                idx = item.get("index", 0) - 1
                if 0 <= idx < len(signals):
                    queries = item.get("queries", [])
                    if queries:
                        signals[idx]["search_queries"] = queries
        except (json.JSONDecodeError, KeyError):
            pass

    return signals


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _persist_queue(signals: list[dict], log) -> None:
    """Persist reading queue items to the reading_queue table.

    Creates the table if it doesn't exist.
    """
    from reading_app.db import get_conn

    with get_conn() as conn:
        # Ensure table exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_queue (
                id TEXT PRIMARY KEY,
                signal_type TEXT NOT NULL,
                theme_id TEXT,
                theme_name TEXT,
                description TEXT,
                reason TEXT,
                search_hint TEXT,
                search_queries JSONB,
                priority REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW(),
                completed_at TIMESTAMP
            )
        """)
        conn.commit()

        # Archive old pending items
        conn.execute(
            "UPDATE reading_queue SET status = 'superseded' WHERE status = 'pending'"
        )

        # Insert new items
        for s in signals:
            queue_id = f"rq_{ULID()}"
            conn.execute(
                """INSERT INTO reading_queue
                   (id, signal_type, theme_id, theme_name, description, reason,
                    search_hint, search_queries, priority)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    queue_id,
                    s["type"],
                    s.get("theme_id"),
                    s.get("theme"),
                    s["description"],
                    s["reason"],
                    s.get("search_hint"),
                    json.dumps(s.get("search_queries")) if s.get("search_queries") else None,
                    s.get("priority", 0),
                ),
            )

        conn.commit()
        log.info("reading_queue_persisted", count=len(signals))


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _format_queue(signals: list[dict], count: int, focus_theme: str | None) -> str:
    """Format the reading queue as a response."""
    scope = f"for `{focus_theme}`" if focus_theme else "across all themes"
    lines = [f"**Read Next** — Top {len(signals)} recommendations {scope}\n"]

    type_icons = {
        "blind_spot_bottleneck": "🔲",
        "high_priority_bottleneck": "⚡",
        "validation_backlog": "❓",
        "belief_gap": "🎯",
        "untested_anticipation": "🔮",
        "low_coverage_theme": "📭",
    }

    for i, s in enumerate(signals, 1):
        icon = type_icons.get(s["type"], "📖")
        lines.append(f"### {i}. {icon} {s['theme']}")
        lines.append(f"**Why:** {s['reason']}")
        lines.append(f"**Gap:** {s['description']}")

        # Search suggestions
        queries = s.get("search_queries")
        if queries:
            lines.append("**Search:**")
            for q in queries[:2]:
                lines.append(f"  - `{q}`")
        elif s.get("search_hint"):
            lines.append(f"**Search:** `{s['search_hint']}`")

        lines.append("")

    # Summary
    type_counts = {}
    for s in signals:
        t = s["type"].replace("_", " ")
        type_counts[t] = type_counts.get(t, 0) + 1

    summary_parts = [f"{v} {k}" for k, v in type_counts.items()]
    lines.append(f"---\nSignal mix: {', '.join(summary_parts)}")
    lines.append("Queue saved. After reading, use `/save <url>` to ingest.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Search term helpers
# ---------------------------------------------------------------------------

def _horizon_priority(horizon: str) -> float:
    return {
        "months": 5.0,
        "1-2_years": 4.0,
        "3-5_years": 3.0,
        "5+_years": 2.0,
        "possibly_fundamental": 1.5,
    }.get(horizon, 2.0)


def _bottleneck_to_search(bn: dict) -> str:
    desc = bn.get("description", "")
    theme = bn.get("theme_name", "")
    blocking = bn.get("blocking_what", "")
    parts = [theme, desc[:60]]
    if blocking:
        parts.append(blocking[:40])
    return " ".join(p for p in parts if p)


def _belief_to_search(belief: dict) -> str:
    claim = belief.get("claim", "")
    theme = belief.get("theme_name", "")
    return f"{theme} {claim[:80]} evidence"


def _anticipation_to_search(ant: dict) -> str:
    prediction = ant.get("prediction", "")
    theme = ant.get("theme_name", "")
    return f"{theme} {prediction[:80]}"
