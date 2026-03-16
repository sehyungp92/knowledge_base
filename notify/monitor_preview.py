"""Cross-channel notifications for staged YouTube monitor previews."""

from __future__ import annotations

from notify.discord import send_discord_message
from notify.email import send_summary_email
from notify.telegram import send_telegram_message


def build_monitor_preview_text(
    *,
    title: str,
    channel: str,
    url: str,
    theme_names: list[str],
    summary_markdown: str,
    source_id: str,
) -> str:
    """Build a plain-text preview notification for chat channels."""
    lines = [
        "YouTube monitor preview ready",
        f"Channel: {channel}",
        f"Title: {title}",
        f"URL: {url}",
    ]
    if theme_names:
        lines.append(f"Themes: {', '.join(theme_names)}")

    lines.extend(
        [
            "",
            summary_markdown.strip(),
            "",
            "To continue ingestion, run:",
            f"/save_confirmed {source_id}",
        ]
    )
    return "\n".join(lines)


def send_monitor_preview_notifications(
    *,
    title: str,
    channel: str,
    url: str,
    theme_names: list[str],
    summary_markdown: str,
    source_id: str,
    channels: tuple[str, ...] | None = None,
) -> dict[str, bool]:
    """Send a staged monitor preview over email, Telegram, and Discord."""
    enabled_channels = set(channels or ("email", "telegram", "discord"))
    chat_text = build_monitor_preview_text(
        title=title,
        channel=channel,
        url=url,
        theme_names=theme_names,
        summary_markdown=summary_markdown,
        source_id=source_id,
    )

    results = {"email": False, "telegram": False, "discord": False}
    if "email" in enabled_channels:
        results["email"] = send_summary_email(
            title=title,
            channel=channel,
            url=url,
            summary_markdown=summary_markdown,
            source_id=source_id,
            theme_names=theme_names,
        )
    if "telegram" in enabled_channels:
        results["telegram"] = send_telegram_message(chat_text, parse_mode=None)
    if "discord" in enabled_channels:
        results["discord"] = send_discord_message(chat_text)
    return results
