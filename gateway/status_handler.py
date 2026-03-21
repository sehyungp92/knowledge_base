"""Direct Python handler for /status — job status or system overview."""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from typing import Callable

from gateway.models import Event, Job
from gateway.queue import DEFAULT_QUEUE_DB_PATH, Queue


def handle_status_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    queue: Queue | None = None,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Show job status or system overview."""
    text = event.payload.get("text", "")
    q = queue or Queue(DEFAULT_QUEUE_DB_PATH)
    job_id = _parse_job_id(text)

    if job_id is not None:
        return _job_detail(q, job_id)
    return _system_overview(q)


def _parse_job_id(text: str) -> int | None:
    """Extract numeric job_id from '/status [job_id]'."""
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group(1)) if match else None


def _job_detail(q: Queue, job_id: int) -> str:
    """Return status detail for a specific job."""
    j = q.get_job(job_id)
    if j is None:
        return f"Job `{job_id}` not found."

    elapsed = ""
    if j.created_at and j.updated_at:
        secs = j.updated_at - j.created_at
        elapsed = f" ({secs:.0f}s)" if secs > 0 else ""

    lines = [
        f"**Job {j.id}** — `{j.skill}`",
        f"- Status: **{j.status}**{elapsed}",
        f"- Provider: {j.provider_id or '?'}",
    ]

    if j.result:
        progress = j.result.get("progress")
        if progress:
            lines.append(f"- Progress: {progress}")
        error = j.result.get("error")
        if error:
            lines.append(f"- Error: {str(error)[:200]}")

    return "\n".join(lines)


def _system_overview(q: Queue) -> str:
    """Return a system overview with source counts and queue status."""
    from reading_app.db import ensure_pool, get_conn

    ensure_pool()

    with get_conn() as conn:
        # Source stats + knowledge model counts in a single query
        row = conn.execute(
            """SELECT
                (SELECT count(*) FROM sources) AS total_sources,
                (SELECT count(*) FROM sources WHERE ingested_at > now() - interval '7 days') AS recent_sources,
                (SELECT count(*) FROM themes WHERE level = (SELECT max(level) FROM themes)) AS themes,
                (SELECT count(*) FROM capabilities) AS capabilities,
                (SELECT count(*) FROM limitations) AS limitations,
                (SELECT count(*) FROM bottlenecks) AS bottlenecks,
                (SELECT count(*) FROM breakthroughs) AS breakthroughs,
                (SELECT count(*) FROM beliefs WHERE status = 'active') AS beliefs,
                (SELECT count(*) FROM anticipations WHERE status = 'open') AS anticipations,
                (SELECT count(*) FROM ideas) AS ideas,
                (SELECT count(*) FROM sources WHERE processing_status = 'incomplete') AS incomplete"""
        ).fetchone()
        total = row["total_sources"]
        recent = row["recent_sources"]
        km = {k: row[k] for k in (
            "themes", "capabilities", "limitations", "bottlenecks",
            "breakthroughs", "beliefs", "anticipations", "ideas", "incomplete",
        )}

    # Queue stats
    pending = q.count_pending_user_jobs()

    # Last heartbeat
    last_hb = "unknown"
    try:
        hb_time = q.get_last_heartbeat_time()
        if hb_time is not None:
            ts = datetime.fromtimestamp(hb_time, tz=timezone.utc)
            ago = int((datetime.now(timezone.utc) - ts).total_seconds())
            last_hb = f"{ago}s ago" if ago < 120 else f"{ago // 60}m ago"
    except Exception:
        pass

    lines = [
        "**System Overview**",
        f"- Sources: **{total}** total, **{recent}** in last 7 days",
        f"- Queue: **{pending}** pending/running jobs",
        f"- Last heartbeat: {last_hb}",
        "",
        "**Knowledge Model**",
        f"- Themes: **{km['themes']}** leaf themes",
        f"- Capabilities: **{km['capabilities']}** / Limitations: **{km['limitations']}**",
        f"- Bottlenecks: **{km['bottlenecks']}** / Breakthroughs: **{km['breakthroughs']}**",
        f"- Beliefs: **{km['beliefs']}** active / Anticipations: **{km['anticipations']}** open",
        f"- Ideas: **{km['ideas']}**",
    ]
    if km["incomplete"]:
        lines.append(f"- Incomplete sources: **{km['incomplete']}**")
    return "\n".join(lines)
