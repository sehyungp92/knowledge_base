"""Direct Python handler for /save_confirmed jobs."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import structlog

from gateway.models import Event, Job
from gateway.preview_flow import (
    STAGING_DIR,
    discard_staging_preview,
    staging_created_at,
    staging_ttl_label,
    staging_ttl_seconds,
)

logger = structlog.get_logger(__name__)

_ULID_RE = re.compile(r"[0-9A-Z]{26}")
_URL_RE = re.compile(r"https?://\S+")


def _find_staging_by_url(url: str) -> Path | None:
    """Search staging directory for a file matching the given URL."""
    if not STAGING_DIR.exists():
        return None

    best_match = None
    best_created_at = 0.0
    for staging_file in STAGING_DIR.glob("*.json"):
        try:
            data = json.loads(staging_file.read_text(encoding="utf-8"))
            if data.get("url") == url:
                created_at = staging_created_at(data, staging_path=staging_file)
                if best_match is None or created_at >= best_created_at:
                    best_match = staging_file
                    best_created_at = created_at
        except Exception:
            pass

    return best_match


def handle_save_confirmed_job(
    event: Event, job: Job, config, executor, *, on_progress=None
) -> str:
    """Load staging metadata and run the extraction pipeline."""
    text = event.payload.get("text", "")

    staging_path = None
    source_id = None

    ulid_match = _ULID_RE.search(text)
    if ulid_match:
        source_id = ulid_match.group(0)
        candidate = STAGING_DIR / f"{source_id}.json"
        if candidate.exists():
            staging_path = candidate

    if staging_path is None:
        url_match = _URL_RE.search(text)
        if url_match:
            staging_path = _find_staging_by_url(url_match.group(0))

    if staging_path is None:
        hint = source_id or text.strip()
        raise ValueError(
            f"No staging file found for {hint}. "
            "Use /summarise <url> first, or use /save <url> for direct ingestion."
        )

    staging = json.loads(staging_path.read_text(encoding="utf-8"))
    source_id = staging["source_id"]
    origin = staging.get("origin")

    log = logger.bind(job_id=job.id, source_id=source_id)
    log.info("save_confirmed_handler_start")
    t0 = time.monotonic()

    created_at = staging_created_at(staging, staging_path=staging_path)
    ttl = staging_ttl_seconds(origin)
    if time.time() - created_at > ttl:
        discard_staging_preview(staging_path, staging, config)
        raise ValueError(
            f"Staging for {source_id} expired (>{staging_ttl_label(origin)}). "
            "Please run /summarise again."
        )

    library_path = config.library_path
    url = staging["url"]
    title = staging["title"]
    source_type = staging["source_type"]
    authors = staging.get("authors")
    published_at = staging.get("published_at")
    metadata = staging.get("metadata", {})
    themes = staging.get("themes", [])
    theme_proposal = staging.get("theme_proposal")
    source_library_path = staging.get("library_path", "")

    log = log.bind(title=title[:80], url=url)

    clean_md_path = (
        Path(source_library_path) / "clean.md"
        if source_library_path
        else library_path / source_id / "clean.md"
    )
    if not clean_md_path.exists():
        discard_staging_preview(staging_path, staging, config)
        raise ValueError(
            f"clean.md not found at {clean_md_path}. "
            "The fetched content may have been deleted. Run /summarise again."
        )
    clean_text = clean_md_path.read_text(encoding="utf-8")

    from reading_app.db import ensure_pool, get_conn

    ensure_pool()
    with get_conn() as conn:
        conn.execute(
            "UPDATE sources SET processing_status = 'ingested' "
            "WHERE id = %s AND processing_status IN ('preview', 'monitor_preview')",
            (source_id,),
        )
        conn.commit()
    log.info("save_confirmed_source_promoted", status="ingested")

    if on_progress:
        on_progress("Running extraction pipeline...")

    from ingest.save_pipeline import run_save_pipeline

    show_name = metadata.get("channel") or metadata.get("podcast_name")
    pre_themes = list(themes)
    if theme_proposal:
        pre_themes.append({"_proposal": theme_proposal})

    result = run_save_pipeline(
        source_id=source_id,
        clean_text=clean_text,
        title=title,
        source_type=source_type,
        url=url,
        authors=authors,
        published_at=published_at,
        library_path=library_path,
        show_name=show_name,
        executor=executor,
        get_conn_fn=get_conn,
        skip_summary=True,
        pre_classified_themes=pre_themes,
    )
    theme_ids = [theme.get("theme_id", "") for theme in result.get("themes", [])]

    try:
        if source_type in ("video", "podcast") and not authors:
            summary_path = (
                Path(source_library_path) / "deep_summary.md"
                if source_library_path
                else library_path / source_id / "deep_summary.md"
            )
            if summary_path.exists():
                summary_text = summary_path.read_text(encoding="utf-8")
                if summary_text:
                    import yaml

                    from ingest.source_utils import parse_participants_from_summary, write_meta_yaml
                    from reading_app.db import update_source_authors

                    participants = parse_participants_from_summary(summary_text)
                    if participants:
                        update_source_authors(source_id, participants)
                        source_dir = Path(source_library_path) if source_library_path else library_path / source_id
                        meta_path = source_dir / "meta.yaml"
                        if meta_path.exists():
                            existing = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                            existing["authors"] = participants
                            write_meta_yaml(source_dir, existing)
                        log.info("save_confirmed_participants_extracted", participants=participants)
    except Exception:
        log.debug("save_confirmed_participant_extraction_failed", exc_info=True)

    try:
        with get_conn() as conn:
            conn.execute(
                "UPDATE sources SET processing_status = 'complete' WHERE id = %s",
                (source_id,),
            )
            conn.commit()
    except Exception:
        log.warning("save_confirmed_status_update_failed", exc_info=True)

    try:
        from ingest.post_processor import enqueue_post_processing

        enqueue_post_processing(source_id, theme_ids, get_conn)
    except Exception:
        log.debug("save_confirmed_post_processing_enqueue_failed", exc_info=True)

    auto_reflected = False
    if origin == "youtube_monitor":
        try:
            from gateway.digest_context import maybe_trigger_auto_reflect

            auto_reflected = maybe_trigger_auto_reflect(result)
            if auto_reflected:
                log.info("save_confirmed_auto_reflect_triggered")
        except Exception:
            log.debug("save_confirmed_auto_reflect_failed", exc_info=True)

    try:
        staging_path.unlink(missing_ok=True)
    except Exception:
        log.debug("staging_cleanup_failed", exc_info=True)

    elapsed = time.monotonic() - t0
    claims_count = len(result.get("claims", []))
    errors = result.get("errors", [])

    log.info(
        "save_confirmed_handler_complete",
        elapsed_s=round(elapsed, 1),
        claims=claims_count,
        themes=theme_ids,
        errors=len(errors),
        auto_reflected=auto_reflected,
    )

    lines = [f"Saved: **{title}**"]
    if theme_ids:
        lines.append(f"Themes: {', '.join(theme_ids)}")
    lines.append(f"Claims extracted: {claims_count}")

    summary_path = (
        Path(source_library_path) / "deep_summary.md"
        if source_library_path
        else library_path / source_id / "deep_summary.md"
    )
    if summary_path.exists():
        lines.append(f"Summary: {summary_path.stat().st_size} chars (reused from /summarise)")

    if errors:
        lines.append(f"Warnings: {len(errors)} non-critical errors")
    lines.append(f"Completed in {elapsed:.0f}s (summary + themes skipped)")

    return "\n".join(lines)
