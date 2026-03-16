"""Direct Python handler for /delete jobs.

Bypasses the Claude CLI subprocess and calls delete_source() directly.
"""

from __future__ import annotations

import re
import time

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)

_URL_RE = re.compile(r"https?://\S+")
_ID_RE = re.compile(r"[0-9A-Z]{26}")  # ULID pattern


def _extract_identifier(text: str) -> str:
    """Extract source ID or URL from /delete command text."""
    # Strip the /delete prefix
    cleaned = re.sub(r"^/delete\s+", "", text).strip()

    # Try ULID first
    m = _ID_RE.search(cleaned)
    if m:
        return m.group(0)

    # Try URL
    m = _URL_RE.search(cleaned)
    if m:
        return m.group(0)

    # Fall back to raw text (might be partial URL or ID)
    return cleaned


def _resolve_source(identifier: str) -> dict | None:
    """Look up a source by ID or URL."""
    from reading_app.db import get_conn

    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sources WHERE id = %s", (identifier,)
        ).fetchone()
        if row:
            return row

        row = conn.execute(
            "SELECT * FROM sources WHERE url = %s", (identifier,)
        ).fetchone()
        if row:
            return row

        row = conn.execute(
            "SELECT * FROM sources WHERE url LIKE %s LIMIT 1",
            (f"%{identifier}%",),
        ).fetchone()
        return row


def handle_delete_job(event: Event, job: Job, config, executor, *, on_progress=None) -> str:
    """Run delete_source() directly for a /delete job.

    Returns:
        Response text summarising what was deleted.

    Raises:
        ValueError: If no source found matching the identifier.
    """
    text = event.payload.get("text", "")
    identifier = _extract_identifier(text)

    log = logger.bind(job_id=job.id, identifier=identifier)
    log.info("delete_handler_start")
    t0 = time.monotonic()

    # Resolve source
    source = _resolve_source(identifier)
    if not source:
        raise ValueError(f"No source found matching: {identifier}")

    source_id = source["id"]
    title = source.get("title", "(untitled)")
    log = log.bind(source_id=source_id, title=title[:80])

    # Delete
    from reading_app.db import delete_source
    summary = delete_source(source_id, library_path=config.library_path)

    elapsed = time.monotonic() - t0
    log.info("delete_handler_complete", elapsed_s=round(elapsed, 1), summary=summary)

    # Build response
    lines = [f"Deleted: **{title}**"]
    lines.append(f"Source ID: `{source_id}`")

    affected = [f"{k}: {v}" for k, v in sorted(summary.items()) if v > 0]
    if affected:
        lines.append(f"Cleaned: {', '.join(affected)}")

    lines.append(f"Completed in {elapsed:.1f}s")

    return "\n".join(lines)
