"""Direct Python handler for youtube_monitor jobs."""

from __future__ import annotations

import time
from pathlib import Path

import structlog

from gateway.models import Event, Job
from gateway.preview_flow import (
    create_summary_preview,
    discard_staging_preview,
    find_active_staging_by_url,
    update_staging_metadata,
)
from notify.monitor_preview import send_monitor_preview_notifications

logger = structlog.get_logger(__name__)
_NOTIFICATION_CHANNELS = ("email", "telegram", "discord")


def _load_existing_preview(staging_path: Path, staging: dict, config) -> dict | None:
    """Reuse an active staged monitor preview when the summary is still on disk."""
    source_id = staging.get("source_id")
    if not source_id:
        return None

    source_library_path = staging.get("library_path", "")
    source_dir = Path(source_library_path) if source_library_path else config.library_path / source_id
    clean_md_path = source_dir / "clean.md"
    summary_path = source_dir / "deep_summary.md"
    if not clean_md_path.exists() or not summary_path.exists():
        return None

    summary_text = summary_path.read_text(encoding="utf-8").strip()
    if not summary_text:
        return None

    return {
        "source_id": source_id,
        "url": staging.get("url", ""),
        "title": staging.get("title", source_id),
        "source_type": staging.get("source_type", "video"),
        "authors": staging.get("authors"),
        "published_at": staging.get("published_at"),
        "metadata": staging.get("metadata", {}),
        "themes": staging.get("themes", []),
        "theme_proposal": staging.get("theme_proposal"),
        "library_path": str(source_dir),
        "summary_text": summary_text,
        "staging_path": staging_path,
        "created_at": staging.get("created_at", 0),
        "fetch_result": {},
        "notifications": staging.get("notifications", {}),
    }


def _pending_notification_channels(stored_notifications: dict) -> tuple[str, ...]:
    """Return only the channels that still need delivery for a staged preview."""
    if not stored_notifications:
        return _NOTIFICATION_CHANNELS
    return tuple(
        channel for channel in _NOTIFICATION_CHANNELS if not stored_notifications.get(channel)
    )


def handle_youtube_monitor_job(
    event: Event, job: Job, config, executor, *, on_progress=None
) -> str:
    """Stage a monitor-detected video and send preview notifications."""
    payload = event.payload
    url = payload.get("url") or payload.get("text", "")
    title = payload.get("title", "")
    channel = payload.get("channel", "")

    log = logger.bind(job_id=job.id, url=url, channel=channel)
    log.info("youtube_monitor_handler_start")
    t0 = time.monotonic()

    reused_preview = False
    preview = None
    existing = find_active_staging_by_url(url, config=config, origin="youtube_monitor")
    if existing is not None:
        staging_path, staging = existing
        preview = _load_existing_preview(staging_path, staging, config)
        if preview is not None:
            reused_preview = True
            log.info(
                "youtube_monitor_handler_reused_preview",
                source_id=preview["source_id"],
            )
        else:
            discard_staging_preview(staging_path, staging, config)
            log.warning(
                "youtube_monitor_handler_discarded_invalid_preview",
                source_id=staging.get("source_id"),
            )

    if preview is None:
        preview = create_summary_preview(
            config=config,
            executor=executor,
            url=url,
            title_hint=title,
            source_type="video",
            csv_file="youtube_monitor",
            processing_status="monitor_preview",
            staging_origin="youtube_monitor",
            show_name_hint=channel,
            on_progress=on_progress,
        )

    source_id = preview["source_id"]
    title = preview["title"]
    summary_text = preview["summary_text"]
    metadata = preview["metadata"]
    theme_ids = [theme.get("theme_id", "") for theme in preview["themes"]]
    channel_name = metadata.get("channel") or channel or "Unknown"
    stored_notifications = preview.get("notifications", {})
    channels_to_notify = _pending_notification_channels(stored_notifications) if reused_preview else _NOTIFICATION_CHANNELS

    notification_results = {
        notification_channel: bool(stored_notifications.get(notification_channel))
        for notification_channel in _NOTIFICATION_CHANNELS
    }

    if channels_to_notify:
        sent_notifications = send_monitor_preview_notifications(
            title=title,
            channel=channel_name,
            url=url,
            theme_names=theme_ids,
            summary_markdown=summary_text,
            source_id=source_id,
            channels=channels_to_notify,
        )
        notification_results.update(
            {
                channel_name: notification_results[channel_name] or sent_notifications[channel_name]
                for channel_name in _NOTIFICATION_CHANNELS
            }
        )
        try:
            update_staging_metadata(
                preview["staging_path"],
                notifications={
                    **notification_results,
                    "last_attempt_at": time.time(),
                },
            )
        except Exception:
            log.debug("youtube_monitor_notification_state_update_failed", exc_info=True)

    elapsed = time.monotonic() - t0
    log = log.bind(source_id=source_id, title=title[:80])
    log.info(
        "youtube_monitor_handler_complete",
        elapsed_s=round(elapsed, 1),
        themes=theme_ids,
        summary_chars=len(summary_text),
        email_sent=notification_results["email"],
        telegram_sent=notification_results["telegram"],
        discord_sent=notification_results["discord"],
        reused_preview=reused_preview,
    )

    return (
        f"Monitor preview ready: {title}\n"
        f"Themes: {', '.join(theme_ids)}\n"
        f"Stage with: /save_confirmed {source_id}\n"
        f"Summary: {len(summary_text)} chars\n"
        f"Email: {'sent' if notification_results['email'] else 'skipped'}\n"
        f"Telegram: {'sent' if notification_results['telegram'] else 'skipped'}\n"
        f"Discord: {'sent' if notification_results['discord'] else 'skipped'}\n"
        f"Completed in {elapsed:.0f}s"
    )
