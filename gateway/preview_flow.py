"""Shared preview staging flow for /summarise and monitor-driven previews."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

STAGING_DIR = Path("var/summarise_staging")
STAGING_TTL_SECONDS = 24 * 60 * 60
MONITOR_STAGING_TTL_SECONDS = 7 * 24 * 60 * 60


def staging_ttl_seconds(origin: str | None) -> int:
    """Return the staging TTL for the given origin."""
    if origin == "youtube_monitor":
        return MONITOR_STAGING_TTL_SECONDS
    return STAGING_TTL_SECONDS


def staging_ttl_label(origin: str | None) -> str:
    """Return a human-readable TTL label for the given origin."""
    if origin == "youtube_monitor":
        return "7 days"
    return "24h"


def staging_created_at(staging: dict, *, staging_path: Path | None = None) -> float:
    """Return the staging creation timestamp, falling back to file metadata."""
    created_at = staging.get("created_at")
    if isinstance(created_at, (int, float)) and created_at > 0:
        return float(created_at)
    if staging_path is not None and staging_path.exists():
        return staging_path.stat().st_mtime
    return 0.0


def is_staging_expired(
    staging: dict,
    *,
    now: float | None = None,
    staging_path: Path | None = None,
) -> bool:
    """Return True when the staged preview is older than its allowed TTL."""
    if now is None:
        now = time.time()
    created_at = staging_created_at(staging, staging_path=staging_path)
    return now - created_at > staging_ttl_seconds(staging.get("origin"))


def _write_staging_file(staging_path: Path, staging: dict) -> None:
    """Write staging JSON atomically to reduce partial-file corruption."""
    staging_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = staging_path.with_suffix(f"{staging_path.suffix}.tmp")
    tmp_path.write_text(json.dumps(staging, indent=2, default=str), encoding="utf-8")
    tmp_path.replace(staging_path)


def remove_preview_source(source_id: str | None, config) -> None:
    """Remove a preview source row and its library directory."""
    if not source_id:
        return

    should_remove_library = False
    try:
        from reading_app.db import get_conn

        with get_conn() as conn:
            row = conn.execute(
                "SELECT processing_status FROM sources WHERE id = %s",
                (source_id,),
            ).fetchone()
            should_remove_library = row is None or row.get("processing_status") in (
                "preview",
                "monitor_preview",
            )
            conn.execute(
                "DELETE FROM sources WHERE id = %s AND processing_status IN ('preview', 'monitor_preview')",
                (source_id,),
            )
            conn.commit()
    except Exception:
        logger.debug("preview_source_db_cleanup_failed", source_id=source_id, exc_info=True)
        return

    if not should_remove_library:
        logger.debug(
            "preview_source_library_cleanup_skipped",
            source_id=source_id,
        )
        return

    try:
        lib_dir = config.library_path / source_id
        if lib_dir.exists():
            shutil.rmtree(lib_dir)
    except Exception:
        logger.debug("preview_source_library_cleanup_failed", source_id=source_id, exc_info=True)


def discard_staging_preview(staging_path: Path, staging: dict, config) -> None:
    """Remove a staging file and its associated preview source artifacts."""
    remove_preview_source(staging.get("source_id"), config)
    try:
        staging_path.unlink(missing_ok=True)
    except Exception:
        logger.debug("staging_file_cleanup_failed", path=str(staging_path), exc_info=True)


def cleanup_stale(config) -> None:
    """Remove expired staging files and their preview source rows."""
    now = time.time()

    if not STAGING_DIR.exists():
        return

    for staging_file in STAGING_DIR.glob("*.json"):
        try:
            staging = json.loads(staging_file.read_text(encoding="utf-8"))
            if not is_staging_expired(staging, now=now, staging_path=staging_file):
                continue

            discard_staging_preview(staging_file, staging, config)
            logger.debug("staging_file_expired", path=str(staging_file))
        except Exception:
            logger.debug("staging_cleanup_failed", path=str(staging_file), exc_info=True)


def find_active_staging_by_url(
    url: str,
    *,
    config=None,
    origin: str | None = None,
) -> tuple[Path, dict] | None:
    """Return an active staging file matching the URL, optionally filtered by origin."""
    if config is not None:
        cleanup_stale(config)

    if not STAGING_DIR.exists():
        return None

    now = time.time()
    best_match: tuple[Path, dict] | None = None
    best_created_at = 0.0
    for staging_file in STAGING_DIR.glob("*.json"):
        try:
            staging = json.loads(staging_file.read_text(encoding="utf-8"))
            if staging.get("url") != url:
                continue
            if origin is not None and staging.get("origin") != origin:
                continue
            if is_staging_expired(staging, now=now, staging_path=staging_file):
                if config is not None:
                    discard_staging_preview(staging_file, staging, config)
                continue
            created_at = staging_created_at(staging, staging_path=staging_file)
            if best_match is None or created_at >= best_created_at:
                best_match = (staging_file, staging)
                best_created_at = created_at
        except Exception:
            logger.debug("staging_lookup_failed", path=str(staging_file), exc_info=True)

    return best_match


def update_staging_metadata(staging_path: Path, **updates) -> dict:
    """Patch a staging file in place and return the updated payload."""
    staging = json.loads(staging_path.read_text(encoding="utf-8"))
    staging.update(updates)
    _write_staging_file(staging_path, staging)
    return staging


def create_summary_preview(
    *,
    config,
    executor,
    url: str,
    title_hint: str = "",
    source_type: str | None = None,
    time_ranges=None,
    csv_file: str = "webapp",
    processing_status: str = "preview",
    staging_origin: str | None = None,
    show_name_hint: str | None = None,
    on_progress=None,
) -> dict:
    """Fetch, classify, summarise, and stage a source for later confirmation."""
    cleanup_stale(config)

    library_path = config.library_path

    from scripts.bulk_ingest import SourceEntry, detect_source_type_from_url, fetch_source

    resolved_source_type = source_type or detect_source_type_from_url(url, "article")

    if on_progress:
        on_progress("Fetching source...")

    source_id = None
    staging_path = None

    try:
        if resolved_source_type == "video" and time_ranges:
            from ingest.youtube import fetch as yt_fetch

            fetch_result = yt_fetch(url, library_path, time_ranges=time_ranges)
        else:
            entry = SourceEntry(
                title=title_hint,
                date="",
                url=url,
                source_type=resolved_source_type,
                csv_file=csv_file,
                row_num=0,
            )
            fetch_result = fetch_source(entry, library_path)

        source_id = fetch_result["id"]
        clean_text = fetch_result.get("clean_text", "")
        title = fetch_result.get("title", title_hint or "Untitled") or title_hint or "Untitled"
        published_at = fetch_result.get("published_at")
        metadata = fetch_result.get("metadata", {})
        authors = fetch_result.get("authors")
        abstract = fetch_result.get("abstract")
        resolved_source_type = fetch_result.get("source_type", resolved_source_type)

        if not clean_text or len(clean_text) < 100:
            raise ValueError(f"Fetched text too short ({len(clean_text)} chars) for {url}")

        from reading_app.db import ensure_pool, get_conn, insert_source

        ensure_pool()

        insert_source(
            id=source_id,
            source_type=resolved_source_type,
            title=title,
            url=url,
            authors=authors,
            published_at=published_at,
            abstract=abstract,
            library_path=str(fetch_result.get("library_path", "")),
            processing_status=processing_status,
            metadata=metadata,
        )

        if on_progress:
            on_progress("Classifying themes...")

        from ingest.theme_classifier import classify_themes

        themes_raw = classify_themes(
            clean_text,
            source_id,
            category_hints=metadata.get("category_theme_hints"),
            executor=executor,
            get_conn_fn=get_conn,
        )

        themes_for_summary = []
        theme_proposal = None
        for theme in themes_raw:
            if "_proposal" in theme:
                theme_proposal = theme["_proposal"]
            elif "theme_id" in theme:
                themes_for_summary.append(theme)

        if on_progress:
            on_progress("Generating deep summary...")

        from ingest.deep_summarizer import generate_deep_summary

        show_name = metadata.get("channel") or metadata.get("podcast_name") or show_name_hint
        summary_text = generate_deep_summary(
            source_id=source_id,
            clean_text=clean_text,
            title=title,
            source_type=resolved_source_type,
            url=url,
            authors=authors,
            published_at=str(published_at) if published_at else None,
            executor=executor,
            library_path=library_path,
            themes=themes_for_summary or None,
            show_name=show_name,
        )

        created_at = time.time()
        staging_data = {
            "source_id": source_id,
            "url": url,
            "title": title,
            "source_type": resolved_source_type,
            "authors": authors,
            "published_at": str(published_at) if published_at else None,
            "metadata": metadata,
            "themes": themes_for_summary,
            "theme_proposal": theme_proposal,
            "library_path": str(fetch_result.get("library_path", "")),
            "created_at": created_at,
        }
        if staging_origin:
            staging_data["origin"] = staging_origin

        staging_path = STAGING_DIR / f"{source_id}.json"
        _write_staging_file(staging_path, staging_data)

        logger.info(
            "summary_preview_staged",
            source_id=source_id,
            origin=staging_origin or "summarise",
            processing_status=processing_status,
            themes=[theme.get("theme_id", "") for theme in themes_for_summary],
            summary_chars=len(summary_text),
        )

        return {
            "source_id": source_id,
            "url": url,
            "title": title,
            "source_type": resolved_source_type,
            "authors": authors,
            "published_at": str(published_at) if published_at else None,
            "metadata": metadata,
            "themes": themes_for_summary,
            "theme_proposal": theme_proposal,
            "library_path": str(fetch_result.get("library_path", "")),
            "summary_text": summary_text,
            "staging_path": staging_path,
            "created_at": created_at,
            "fetch_result": fetch_result,
        }
    except Exception:
        if staging_path is not None:
            try:
                staging_path.unlink(missing_ok=True)
            except Exception:
                logger.debug("preview_staging_cleanup_failed", path=str(staging_path), exc_info=True)
        remove_preview_source(source_id, config)
        raise
