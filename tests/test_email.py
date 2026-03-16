"""Tests for the email notification module (AgentMail)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from notify.email import send_email, send_summary_email


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
