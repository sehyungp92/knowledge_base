"""Tests for all notification subsystems: email, emitter, and transports."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from ingest.notification_emitter import emit_notification
from notify.discord import send_discord_message
from notify.email import send_email, send_summary_email
from notify.monitor_preview import build_monitor_preview_text
from notify.telegram import send_telegram_message


# --- Email tests ---


class TestSendEmail:
    @patch.dict("sys.modules", {"agentmail": MagicMock()})
    def test_successful_send(self):
        """Email sends successfully via AgentMail API."""
        import sys

        mock_agentmail_cls = sys.modules["agentmail"].AgentMail
        mock_client = MagicMock()
        mock_agentmail_cls.return_value = mock_client

        result = send_email(
            inbox_id="monitor@agentmail.to",
            to="test@example.com",
            subject="Test Subject",
            body_text="Hello World",
            api_key="test-api-key",
        )

        assert result is True
        mock_agentmail_cls.assert_called_once_with(api_key="test-api-key")
        mock_client.inboxes.messages.send.assert_called_once_with(
            inbox_id="monitor@agentmail.to",
            to=["test@example.com"],
            subject="Test Subject",
            text="Hello World",
        )

    @patch.dict("sys.modules", {"agentmail": MagicMock()})
    def test_sends_html_when_provided(self):
        """HTML body is included when provided."""
        import sys

        mock_client = MagicMock()
        sys.modules["agentmail"].AgentMail.return_value = mock_client

        send_email(
            inbox_id="monitor@agentmail.to",
            to="test@example.com",
            subject="Test",
            body_text="Plain text",
            body_html="<p>Rich text</p>",
            api_key="test-api-key",
        )

        call_kwargs = mock_client.inboxes.messages.send.call_args
        assert call_kwargs.kwargs.get("html") == "<p>Rich text</p>"

    @patch.dict("sys.modules", {"agentmail": MagicMock()})
    def test_failure_returns_false(self):
        """API failure returns False instead of raising."""
        import sys

        sys.modules["agentmail"].AgentMail.side_effect = ConnectionError("Connection refused")

        result = send_email(
            inbox_id="monitor@agentmail.to",
            to="test@example.com",
            subject="Test Subject",
            body_text="Hello World",
            api_key="test-api-key",
        )

        assert result is False


class TestSendSummaryEmail:
    @patch("notify.email.send_email")
    @patch("reading_app.config.Config")
    def test_formats_subject_correctly(self, mock_config_cls, mock_send):
        """Summary email subject follows [KB Monitor] format."""
        mock_config = MagicMock()
        mock_config.monitor_email_to = "user@example.com"
        mock_config.agentmail_api_key = "test-key"
        mock_config.agentmail_inbox_id = "monitor@agentmail.to"
        mock_config_cls.return_value = mock_config
        mock_send.return_value = True

        result = send_summary_email(
            title="New AI Model",
            channel="Two Minute Papers",
            url="https://youtube.com/watch?v=abc",
            summary_markdown="## Summary\nGreat video.",
            source_id="01ABC123",
        )

        assert result is True
        call_args = mock_send.call_args
        assert call_args.kwargs["subject"] == "[KB Monitor] Preview: Two Minute Papers: New AI Model"
        assert call_args.kwargs["inbox_id"] == "monitor@agentmail.to"
        assert call_args.kwargs["api_key"] == "test-key"
        # Body should contain the save command
        assert "/save" in call_args.kwargs["body_text"]

    @patch("reading_app.config.Config")
    def test_skips_when_no_email_configured(self, mock_config_cls):
        """Returns False when MONITOR_EMAIL_TO is empty."""
        mock_config = MagicMock()
        mock_config.monitor_email_to = ""
        mock_config_cls.return_value = mock_config

        result = send_summary_email(
            title="Test",
            channel="Test",
            url="https://youtube.com/watch?v=abc",
            summary_markdown="Summary",
            source_id="01ABC123",
        )

        assert result is False

    @patch("reading_app.config.Config")
    def test_skips_when_no_api_key(self, mock_config_cls):
        """Returns False when AgentMail API key is missing."""
        mock_config = MagicMock()
        mock_config.monitor_email_to = "user@example.com"
        mock_config.agentmail_api_key = ""
        mock_config.agentmail_inbox_id = "monitor@agentmail.to"
        mock_config_cls.return_value = mock_config

        result = send_summary_email(
            title="Test",
            channel="Test",
            url="https://youtube.com/watch?v=abc",
            summary_markdown="Summary",
            source_id="01ABC123",
        )

        assert result is False

    @patch("reading_app.config.Config")
    def test_skips_when_no_inbox_id(self, mock_config_cls):
        """Returns False when AgentMail inbox ID is missing."""
        mock_config = MagicMock()
        mock_config.monitor_email_to = "user@example.com"
        mock_config.agentmail_api_key = "test-key"
        mock_config.agentmail_inbox_id = ""
        mock_config_cls.return_value = mock_config

        result = send_summary_email(
            title="Test",
            channel="Test",
            url="https://youtube.com/watch?v=abc",
            summary_markdown="Summary",
            source_id="01ABC123",
        )

        assert result is False


# --- Emitter tests ---


def test_emit_notification_inserts():
    with patch("ingest.notification_emitter.db") as mock_db:
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        mock_db.get_conn.return_value = conn

        emit_notification("test_type", "source", "s1", "Test notification")

        conn.execute.assert_called_once()
        call_args = conn.execute.call_args
        assert "INSERT INTO notifications" in call_args[0][0]
        assert call_args[0][1][0] == "test_type"
        assert call_args[0][1][2] == "s1"
        conn.commit.assert_called_once()


def test_emit_notification_with_detail():
    with patch("ingest.notification_emitter.db") as mock_db:
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        mock_db.get_conn.return_value = conn

        emit_notification(
            "anticipation_match", "anticipation", "a1",
            "Evidence found for prediction",
            detail={"match_confidence": 0.85},
            source_id="src_123",
        )

        call_args = conn.execute.call_args[0][1]
        assert call_args[0] == "anticipation_match"
        assert '"match_confidence": 0.85' in call_args[4]
        assert call_args[5] == "src_123"


def test_emit_notification_swallows_errors():
    with patch("ingest.notification_emitter.db") as mock_db:
        mock_db.get_conn.side_effect = RuntimeError("no pool")
        # Should not raise
        emit_notification("test", "source", "s1", "Test notification")


# --- Transport tests ---


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
