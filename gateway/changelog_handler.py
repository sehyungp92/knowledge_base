"""Direct Python handler for /changelog jobs.

Queries landscape_history for a theme or time period and formats
changes as a temporal narrative.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timedelta, timezone
from typing import Callable

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)

_ULID_RE = re.compile(r"[0-9A-Z]{26}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_changelog_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /changelog directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("changelog_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    theme_id, days = _parse_command(text)
    log = log.bind(theme_id=theme_id, days=days)

    if theme_id:
        result = _changelog_for_theme(theme_id, days, on_progress, log)
    else:
        result = _changelog_global(days, on_progress, log)

    elapsed = time.monotonic() - t0
    log.info("changelog_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str | None, int]:
    """Parse '/changelog [theme_id] [Nd]'.

    Returns (theme_id_or_None, days).
    """
    cleaned = text.strip()
    for prefix in ("/changelog ", "/changelog"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    # Extract days (e.g. "30d", "7d")
    days = 30
    days_match = re.search(r"(\d+)\s*d\b", cleaned, re.IGNORECASE)
    if days_match:
        days = int(days_match.group(1))
        cleaned = cleaned[:days_match.start()] + cleaned[days_match.end():]
        cleaned = cleaned.strip()

    # Extract theme_id (ULID or theme slug)
    theme_id = None
    ulid_match = _ULID_RE.search(cleaned)
    if ulid_match:
        theme_id = ulid_match.group(0)
    elif cleaned:
        # Treat remaining text as theme name/slug
        theme_id = cleaned.strip()

    return theme_id, days


# ---------------------------------------------------------------------------
# Theme-scoped changelog
# ---------------------------------------------------------------------------

def _changelog_for_theme(
    theme_id: str, days: int, on_progress, log
) -> str:
    from reading_app.db import get_conn, get_landscape_history_for_theme

    if on_progress:
        on_progress(f"Loading changelog for theme `{theme_id}` (last {days} days)...")

    # Resolve theme name
    theme_name = theme_id
    with get_conn() as conn:
        # Try exact ID first, then name match
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s", (theme_id,)
        ).fetchone()
        if not theme:
            theme = conn.execute(
                "SELECT id, name FROM themes WHERE name ILIKE %s LIMIT 1",
                (f"%{theme_id}%",),
            ).fetchone()
        if theme:
            theme_name = theme["name"]
            theme_id = theme["id"]
        else:
            return f"Theme not found: `{theme_id}`"

    # Get history, filtering by date in Python (DB query doesn't filter by date)
    history = get_landscape_history_for_theme(theme_id, limit=200)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_naive = cutoff.replace(tzinfo=None)
    history = [
        h for h in history
        if h.get("changed_at") and (
            h["changed_at"] >= cutoff if h["changed_at"].tzinfo else
            h["changed_at"] >= cutoff_naive
        )
    ]

    if not history:
        return (
            f"**Changelog: {theme_name}** (last {days} days)\n\n"
            f"No landscape changes recorded in this period."
        )

    return _format_changelog(theme_name, days, history)


# ---------------------------------------------------------------------------
# Global changelog
# ---------------------------------------------------------------------------

def _changelog_global(days: int, on_progress, log) -> str:
    from reading_app.db import get_conn

    if on_progress:
        on_progress(f"Loading global changelog (last {days} days)...")

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    with get_conn() as conn:
        history = conn.execute(
            """SELECT lh.*, t.name AS theme_name
               FROM landscape_history lh
               LEFT JOIN capabilities c ON lh.entity_type = 'capability'
                   AND lh.entity_id = c.id
               LEFT JOIN limitations l ON lh.entity_type = 'limitation'
                   AND lh.entity_id = l.id
               LEFT JOIN bottlenecks b ON lh.entity_type = 'bottleneck'
                   AND lh.entity_id = b.id
               LEFT JOIN anticipations a ON lh.entity_type = 'anticipation'
                   AND lh.entity_id = a.id
               LEFT JOIN themes t ON t.id = COALESCE(
                   c.theme_id, l.theme_id, b.theme_id, a.theme_id
               )
               WHERE lh.changed_at >= %s
               ORDER BY lh.changed_at DESC
               LIMIT 100""",
            (cutoff,),
        ).fetchall()

    if not history:
        return (
            f"**Global Changelog** (last {days} days)\n\n"
            f"No landscape changes recorded in this period."
        )

    return _format_changelog("All Themes", days, history)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _format_changelog(scope_name: str, days: int, history: list[dict]) -> str:
    """Format changelog entries into a temporal narrative."""
    lines = [f"**Changelog: {scope_name}** (last {days} days)\n"]

    # Group by date
    by_date: dict[str, list[dict]] = {}
    for h in history:
        date_key = str(h.get("changed_at", "?"))[:10]
        by_date.setdefault(date_key, []).append(h)

    # Summary counts
    entity_types = {}
    attributions = {}
    for h in history:
        et = h.get("entity_type", "?")
        entity_types[et] = entity_types.get(et, 0) + 1
        attr = h.get("attribution", "?")
        attributions[attr] = attributions.get(attr, 0) + 1

    lines.append(f"**{len(history)} changes** across {len(by_date)} days")
    type_summary = ", ".join(f"{v} {k}" for k, v in sorted(entity_types.items(), key=lambda x: -x[1]))
    lines.append(f"Entity types: {type_summary}")
    attr_summary = ", ".join(f"{v} by {k}" for k, v in sorted(attributions.items(), key=lambda x: -x[1]))
    lines.append(f"Attribution: {attr_summary}\n")

    # Per-date entries
    for date_key in sorted(by_date.keys(), reverse=True):
        entries = by_date[date_key]
        lines.append(f"### {date_key}")

        for h in entries:
            entity_type = h.get("entity_type", "?")
            entity_id = h.get("entity_id", "?")
            field = h.get("field", "?")
            old_val = _truncate(str(h.get("old_value", "")), 60)
            new_val = _truncate(str(h.get("new_value", "")), 60)
            attr = h.get("attribution", "?")
            theme = h.get("theme_name", "")
            theme_str = f" [{theme}]" if theme else ""

            line = (
                f"- **{entity_type}**{theme_str} `{entity_id[:12]}…` "
                f"— {field}: {old_val} → {new_val} "
                f"*(by {attr})*"
            )
            note = h.get("note", "")
            if note:
                line += f"\n  _{note}_"
            lines.append(line)

        lines.append("")

    lines.append(
        "---\n"
        "Filter: `/changelog <theme> [Nd]` — e.g. `/changelog autonomous_agents 7d`"
    )

    return "\n".join(lines)


def _truncate(s: str, n: int) -> str:
    return s[:n] + "…" if len(s) > n else s
