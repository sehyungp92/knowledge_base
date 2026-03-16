from __future__ import annotations

from types import SimpleNamespace

from notify.discord import send_discord_message
from notify.monitor_preview import build_monitor_preview_text
from notify.telegram import send_telegram_message


class FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None, text: str = "ok"):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_send_telegram_message_chunks_without_parse_mode(monkeypatch):
    import reading_app.config
    import notify.telegram

    monkeypatch.setattr(
        reading_app.config,
        "Config",
        lambda: SimpleNamespace(
            telegram_bot_token="token",
            telegram_allowed_chat_id="chat",
        ),
    )

    calls = []

    def fake_post(url, json=None, timeout=None):
        calls.append((url, json))
        return FakeResponse(200)

    monkeypatch.setattr(notify.telegram.httpx, "post", fake_post)

    assert send_telegram_message("x" * 9000, parse_mode=None) is True
    assert len(calls) == 3
    assert all("parse_mode" not in payload for _, payload in calls)


def test_send_discord_message_chunks(monkeypatch):
    import notify.discord
    import reading_app.config

    monkeypatch.setattr(
        reading_app.config,
        "Config",
        lambda: SimpleNamespace(
            discord_bot_token="token",
            discord_allowed_user_id="user123",
        ),
    )

    calls = []

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append((url, json))
        if url.endswith("/users/@me/channels"):
            return FakeResponse(200, {"id": "dm123"})
        return FakeResponse(200, {"id": "msg123"})

    monkeypatch.setattr(notify.discord.httpx, "post", fake_post)

    assert send_discord_message("y" * 5000) is True
    assert calls[0][0].endswith("/users/@me/channels")
    assert len(calls[1:]) == 3


def test_send_discord_message_skips_without_config(monkeypatch):
    import reading_app.config

    monkeypatch.setattr(
        reading_app.config,
        "Config",
        lambda: SimpleNamespace(
            discord_bot_token="",
            discord_allowed_user_id="",
        ),
    )

    assert send_discord_message("hello") is False


def test_monitor_preview_text_ends_with_save_confirmed():
    text = build_monitor_preview_text(
        title="Video",
        channel="Tracked Channel",
        url="https://www.youtube.com/watch?v=test123",
        theme_names=["autonomous_agents"],
        summary_markdown="# Summary\n\nDetails",
        source_id="01KABCDE1234567890FGHIJKLM",
    )

    assert text.endswith("/save_confirmed 01KABCDE1234567890FGHIJKLM")
