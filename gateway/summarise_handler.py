"""Direct Python handler for /summarise jobs."""

from __future__ import annotations

import re
import time

import structlog

from gateway.models import Event, Job
from gateway.preview_flow import create_summary_preview

logger = structlog.get_logger(__name__)

_URL_RE = re.compile(r"https?://\S+")


def handle_summarise_job(
    event: Event, job: Job, config, executor, *, on_progress=None
) -> str:
    """Fetch, classify themes, generate summary, and stage for later save."""
    text = event.payload.get("text", "")

    url_match = _URL_RE.search(text)
    if not url_match:
        raise ValueError(f"No URL found in summarise command: {text!r}")
    url = url_match.group(0)

    time_ranges = None
    if "youtube.com" in url or "youtu.be" in url:
        after_url = text[url_match.end():].strip()
        if after_url:
            from ingest.youtube import parse_youtube_input

            _, time_ranges = parse_youtube_input(f"{url} {after_url}")

    log = logger.bind(job_id=job.id, url=url)
    log.info("summarise_handler_start", time_ranges=time_ranges)
    t0 = time.monotonic()

    preview = create_summary_preview(
        config=config,
        executor=executor,
        url=url,
        time_ranges=time_ranges,
        csv_file="webapp",
        processing_status="preview",
        on_progress=on_progress,
    )

    elapsed = time.monotonic() - t0
    source_id = preview["source_id"]
    title = preview["title"]
    summary_text = preview["summary_text"]
    theme_ids = [theme.get("theme_id", "") for theme in preview["themes"]]

    log = log.bind(source_id=source_id, title=title[:80])
    log.info(
        "summarise_handler_complete",
        elapsed_s=round(elapsed, 1),
        themes=theme_ids,
        summary_chars=len(summary_text),
    )

    lines = [
        f"**{title}**",
        f"Themes: {', '.join(theme_ids)}" if theme_ids else "",
        "",
        summary_text,
        "",
        "---",
        f"To save this source and run full extraction: `/save_confirmed {source_id}`",
        f"Preview generated in {elapsed:.0f}s. Staging expires in 24h.",
    ]

    return "\n".join(line for line in lines if line is not None)
