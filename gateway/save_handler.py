"""Direct Python handler for /save jobs."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import structlog

from gateway.models import Event, Job
from gateway.preview_flow import staging_created_at, staging_ttl_seconds

logger = structlog.get_logger(__name__)

_URL_RE = re.compile(r"https?://\S+")


def handle_save_job(event: Event, job: Job, config, executor, *, on_progress=None) -> str:
    """Run the save pipeline directly for a /save job."""
    from gateway.run_stages import StageTracker, SAVE_STAGES

    text = event.payload.get("text", "")

    url_match = _URL_RE.search(text)
    if not url_match:
        raise ValueError(f"No URL found in save command: {text!r}")
    url = url_match.group(0)

    time_ranges = None
    if "youtube.com" in url or "youtu.be" in url:
        after_url = text[url_match.end():].strip()
        if after_url:
            from ingest.youtube import parse_youtube_input

            _, time_ranges = parse_youtube_input(f"{url} {after_url}")

    log = logger.bind(job_id=job.id, url=url)
    log.info("save_handler_start", time_ranges=time_ranges)
    t0 = time.monotonic()

    # Check for duplicate URL before doing any work
    from reading_app.db import ensure_pool, find_source_by_url

    ensure_pool()
    existing = find_source_by_url(url)
    if existing:
        log.info("save_handler_duplicate_url", existing_id=existing["id"])
        raise ValueError(
            f"This URL is already saved as **{existing['title']}** "
            f"(ID: `{existing['id']}`, status: {existing['processing_status']}). "
            f"No duplicate ingestion performed."
        )

    # Initialize structured stage tracker
    tracker = StageTracker(SAVE_STAGES, on_progress=on_progress)

    # Emit initial stages to job result
    _emit_stages(job, tracker, on_progress)

    from gateway.save_confirmed_handler import _find_staging_by_url, handle_save_confirmed_job

    staging_path = _find_staging_by_url(url)
    if staging_path is not None:
        try:
            staging = json.loads(staging_path.read_text(encoding="utf-8"))
            created_at = staging_created_at(staging, staging_path=staging_path)
            max_ttl = staging_ttl_seconds(staging.get("origin"))
            if time.time() - created_at <= max_ttl:
                if on_progress:
                    on_progress("Reusing the recent preview and completing the save...")
                log.info(
                    "save_handler_reusing_staging",
                    source_id=staging["source_id"],
                    origin=staging.get("origin", "summarise"),
                )
                event.payload["text"] = f"/save_confirmed {staging['source_id']}"
                return handle_save_confirmed_job(event, job, config, executor, on_progress=on_progress)
        except Exception:
            log.debug("save_handler_staging_check_failed", exc_info=True)

    library_path = config.library_path

    from scripts.bulk_ingest import SourceEntry, detect_source_type_from_url, fetch_source

    source_type = detect_source_type_from_url(url, "article")

    # Stage 1: Fetch
    tracker.start("fetch", "Fetching source content...")
    _emit_stages(job, tracker, on_progress)

    if source_type == "video" and time_ranges:
        from ingest.youtube import fetch as yt_fetch

        fetch_result = yt_fetch(url, library_path, time_ranges=time_ranges)
    else:
        entry = SourceEntry(
            title="",
            date="",
            url=url,
            source_type=source_type,
            csv_file="webapp",
            row_num=0,
        )
        fetch_result = fetch_source(entry, library_path)

    source_id = fetch_result["id"]
    clean_text = fetch_result.get("clean_text", "")
    title = fetch_result.get("title", "Untitled")
    published_at = fetch_result.get("published_at")
    metadata = fetch_result.get("metadata", {})

    tracker.complete("fetch", f"Fetched: {title}")

    log = log.bind(source_id=source_id, title=title[:80])

    if not clean_text or len(clean_text) < 100:
        raise ValueError(f"Fetched text too short ({len(clean_text)} chars) for {url}")

    from reading_app.db import get_conn, insert_source

    insert_source(
        id=source_id,
        source_type=fetch_result.get("source_type", source_type),
        title=title,
        url=url,
        authors=fetch_result.get("authors"),
        published_at=published_at,
        abstract=fetch_result.get("abstract"),
        library_path=fetch_result.get("library_path"),
        processing_status="ingested",
        metadata=metadata,
    )
    log.info("save_handler_source_inserted")

    # Stage 2-6: Run extraction pipeline (classify, extract_claims, summary, landscape, implications)
    from ingest.save_pipeline import run_save_pipeline

    def _pipeline_stage_callback(step_name: str, step_status: str):
        """Bridge save_pipeline step events to our stage tracker."""
        stage_map = {
            "themes": "classify",
            "claims": "extract_claims",
            "summary": "summary",
            "landscape": "landscape",
            "implications": "implications",
        }
        stage_key = stage_map.get(step_name)
        if not stage_key:
            return
        if step_status == "running":
            # Complete the previous stage first
            for prev_key in ("classify", "extract_claims", "summary", "landscape", "implications"):
                prev = tracker._stage_map.get(prev_key)
                if prev and prev.status == "running" and prev_key != stage_key:
                    prev.complete()
            tracker.start(stage_key)
            _emit_stages(job, tracker, on_progress)
        elif step_status == "completed":
            tracker.complete(stage_key)
            _emit_stages(job, tracker, on_progress)
        elif step_status == "failed":
            tracker.fail(stage_key)
            _emit_stages(job, tracker, on_progress)

    result = run_save_pipeline(
        source_id=source_id,
        clean_text=clean_text,
        title=title,
        source_type=fetch_result.get("source_type", source_type),
        url=url,
        authors=fetch_result.get("authors"),
        published_at=str(published_at) if published_at else None,
        library_path=library_path,
        category_hints=metadata.get("category_theme_hints"),
        show_name=metadata.get("channel") or metadata.get("podcast_name"),
        executor=executor,
        get_conn_fn=get_conn,
        on_step=_pipeline_stage_callback,
    )
    theme_ids = [theme.get("theme_id", "") for theme in result.get("themes", [])]

    # Complete any still-running extraction stages
    for stage_key in ("classify", "extract_claims", "summary", "landscape", "implications"):
        stage = tracker._stage_map.get(stage_key)
        if stage and stage.status in ("pending", "running"):
            stage.complete()

    try:
        source_type_val = fetch_result.get("source_type", source_type)
        if source_type_val in ("video", "podcast") and not fetch_result.get("authors"):
            summary_text = result.get("summary", "")
            if summary_text:
                import yaml

                from ingest.source_utils import parse_participants_from_summary, write_meta_yaml
                from reading_app.db import update_source_authors

                participants = parse_participants_from_summary(summary_text)
                if participants:
                    update_source_authors(source_id, participants)
                    source_dir = Path(fetch_result.get("library_path", ""))
                    meta_path = source_dir / "meta.yaml"
                    if meta_path.exists():
                        existing = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                        existing["authors"] = participants
                        write_meta_yaml(source_dir, existing)
                    log.info("save_handler_participants_extracted", participants=participants)
    except Exception:
        log.debug("save_handler_participant_extraction_failed", exc_info=True)

    try:
        with get_conn() as conn:
            conn.execute(
                "UPDATE sources SET processing_status = 'complete' WHERE id = %s",
                (source_id,),
            )
            conn.commit()
    except Exception:
        log.warning("save_handler_status_update_failed", exc_info=True)

    # Stage 7: Graph (post-processing enqueue)
    tracker.start("graph", "Enqueuing post-processing...")
    _emit_stages(job, tracker, on_progress)

    try:
        from ingest.post_processor import enqueue_post_processing

        enqueue_post_processing(source_id, theme_ids, get_conn)
        tracker.complete("graph", "Post-processing enqueued")
    except Exception:
        tracker.fail("graph", "Post-processing enqueue failed")
        log.debug("save_handler_post_processing_enqueue_failed", exc_info=True)

    _emit_stages(job, tracker, on_progress)

    elapsed = time.monotonic() - t0
    claims_count = len(result.get("claims", []))
    errors = result.get("errors", [])

    log.info(
        "save_handler_complete",
        elapsed_s=round(elapsed, 1),
        claims=claims_count,
        themes=theme_ids,
        errors=len(errors),
    )

    lines = [f"Saved: **{title}**"]
    if theme_ids:
        lines.append(f"Themes: {', '.join(theme_ids)}")
    lines.append(f"Claims extracted: {claims_count}")
    if result.get("summary"):
        lines.append(f"Summary: {len(result['summary'])} chars")

    # Surface anticipation matches prominently
    ant_matches = result.get("anticipation_matches", [])
    if ant_matches:
        lines.append(f"\n**Anticipation matches: {len(ant_matches)}**")
        for m in ant_matches[:5]:
            ant_id = m.get("anticipation_id", "?")
            match_type = m.get("match_type", "?")
            prediction = m.get("prediction", m.get("evidence_text", ""))[:100]
            lines.append(f"  - `{ant_id}` [{match_type}]: {prediction}")
        if len(ant_matches) > 5:
            lines.append(f"  ... and {len(ant_matches) - 5} more")

    if errors:
        lines.append(f"Warnings: {len(errors)} non-critical errors")
    lines.append(f"Completed in {elapsed:.0f}s")

    return "\n".join(lines)


_stage_queue = None

def _get_stage_queue():
    """Reuse a single Queue instance for stage emissions."""
    global _stage_queue
    if _stage_queue is None:
        from gateway.queue import Queue, DEFAULT_QUEUE_DB_PATH
        _stage_queue = Queue(db_path=DEFAULT_QUEUE_DB_PATH)
    return _stage_queue


def _emit_stages(job: Job, tracker, on_progress):
    """Emit structured stages to the job queue via the on_progress extra channel."""
    try:
        q = _get_stage_queue()
        q.update_job_progress(
            job.id,
            tracker.progress_text(),
            stages=tracker.to_list(),
        )
    except Exception:
        pass  # Best-effort stage tracking
