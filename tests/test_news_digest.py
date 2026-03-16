"""Tests for the news digest system."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import pytest


class FrozenDateTime(datetime):
    frozen_now: datetime | None = None

    @classmethod
    def now(cls, tz=None):
        assert cls.frozen_now is not None
        if tz is not None:
            return cls.frozen_now.astimezone(tz)
        return cls.frozen_now


class TestSendDigestEmail:
    @patch("notify.email.send_email", return_value=True)
    @patch("reading_app.config.Config")
    def test_daily_email_sent(self, mock_config_cls, mock_send):
        mock_cfg = MagicMock()
        mock_cfg.monitor_email_to = "user@example.com"
        mock_cfg.agentmail_api_key = "key-123"
        mock_cfg.agentmail_inbox_id = "inbox@agentmail.to"
        mock_config_cls.return_value = mock_cfg

        from notify.email import send_digest_email

        result = send_digest_email(
            date="2026-03-03",
            digest_markdown="# Daily Digest\n\nContent here",
            digest_type="daily",
        )

        assert result is True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args
        # Check subject contains daily label
        subject = call_kwargs[1].get("subject", "")
        assert "[KB Digest] Daily" in subject

    @patch("reading_app.config.Config")
    def test_skips_when_no_email_configured(self, mock_config_cls):
        mock_cfg = MagicMock()
        mock_cfg.monitor_email_to = ""
        mock_config_cls.return_value = mock_cfg

        from notify.email import send_digest_email

        result = send_digest_email(date="2026-03-03", digest_markdown="content")
        assert result is False

    @patch("notify.email.send_email", return_value=True)
    @patch("reading_app.config.Config")
    def test_weekly_subject_line(self, mock_config_cls, mock_send):
        mock_cfg = MagicMock()
        mock_cfg.monitor_email_to = "user@example.com"
        mock_cfg.agentmail_api_key = "key-123"
        mock_cfg.agentmail_inbox_id = "inbox@agentmail.to"
        mock_config_cls.return_value = mock_cfg

        from notify.email import send_digest_email

        send_digest_email(
            date="2026-W09",
            digest_markdown="# Weekly Roundup",
            digest_type="weekly",
        )

        args = mock_send.call_args
        subject = args[1].get("subject", "")
        assert "Weekly Roundup" in subject


class TestSendTelegramDigest:
    @patch("reading_app.config.Config")
    def test_skips_when_no_token(self, mock_config_cls):
        mock_cfg = MagicMock()
        mock_cfg.telegram_bot_token = ""
        mock_cfg.telegram_allowed_chat_id = ""
        mock_config_cls.return_value = mock_cfg

        from notify.telegram import send_telegram_message

        result = send_telegram_message("Hello world")
        assert result is False

    @patch("notify.telegram.httpx.post")
    @patch("reading_app.config.Config")
    def test_sends_message(self, mock_config_cls, mock_post):
        mock_cfg = MagicMock()
        mock_cfg.telegram_bot_token = "bot123:ABC"
        mock_cfg.telegram_allowed_chat_id = "12345"
        mock_config_cls.return_value = mock_cfg
        mock_post.return_value = MagicMock(status_code=200)

        from notify.telegram import send_telegram_message

        result = send_telegram_message("Hello world")
        assert result is True
        mock_post.assert_called_once()

    @patch("notify.telegram.httpx.post")
    @patch("reading_app.config.Config")
    def test_truncates_long_messages(self, mock_config_cls, mock_post):
        mock_cfg = MagicMock()
        mock_cfg.telegram_bot_token = "bot123:ABC"
        mock_cfg.telegram_allowed_chat_id = "12345"
        mock_config_cls.return_value = mock_cfg
        mock_post.return_value = MagicMock(status_code=200)

        from notify.telegram import send_telegram_message

        result = send_telegram_message("x" * 5000)
        assert result is True
        call_args = mock_post.call_args
        sent_text = call_args[1].get("json", {}).get("text", "")
        assert len(sent_text) <= 4096


class TestSourceIdentification:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_identifies_ainews(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        text = (
            "Some prefix text\n"
            "---------- Forwarded message ---------\n"
            "From: AINews <swyx+ainews@substack.com>\n"
            "Date: Mon, 3 Mar 2026\n"
            "Subject: AI News #123\n"
            "To: user@gmail.com\n"
            "\n"
            "Body content here"
        )
        sources = [
            {"name": "AINews", "sender": "swyx+ainews@substack.com", "category": "ai_tech"},
            {"name": "Techmeme", "sender": "newsletter@techmeme.com", "category": "ai_tech"},
        ]
        result = adapter._identify_source(text, sources)
        assert result == "AINews"

    def test_returns_none_for_unknown_sender(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        text = (
            "---------- Forwarded message ---------\n"
            "From: Random Person <random@example.com>\n"
            "Date: Mon, 3 Mar 2026\n"
            "\n"
            "Body"
        )
        sources = [
            {"name": "AINews", "sender": "swyx+ainews@substack.com", "category": "ai_tech"},
        ]
        result = adapter._identify_source(text, sources)
        assert result is None

    def test_returns_none_without_forwarded_header(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        text = "Just a regular email body"
        sources = [
            {"name": "AINews", "sender": "swyx+ainews@substack.com", "category": "ai_tech"},
        ]
        result = adapter._identify_source(text, sources)
        assert result is None


class TestContentCleaning:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_strips_forwarded_header(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        msg.text = (
            "---------- Forwarded message ---------\n"
            "From: AINews <swyx+ainews@substack.com>\n"
            "Date: Mon, 3 Mar 2026\n"
            "Subject: AI News\n"
            "\n"
            "Actual newsletter body content"
        )
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "Forwarded message" not in result
        assert "Actual newsletter body content" in result

    def test_removes_invisible_unicode(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        msg.text = "Hello\u034f World\u200b Test\u00ad Content"
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "\u034f" not in result
        assert "\u200b" not in result
        assert "\u00ad" not in result
        assert "Hello World Test Content" in result

    def test_removes_tracking_urls(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        msg.text = "Check this https://example.substack.com/redirect/abc123 and https://example.com/page?utm_source=newsletter&utm_medium=email for more"
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "substack.com/redirect" not in result
        assert "utm_source" not in result

    def test_removes_footer_in_last_20_percent(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        body = "A" * 800 + "\n\nUnsubscribe from this list"
        msg.text = body
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "Unsubscribe" not in result

    def test_keeps_footer_text_in_first_80_percent(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        msg.text = "Unsubscribe from the old service\n\n" + "B" * 800
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "Unsubscribe" in result

    def test_collapses_whitespace(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        msg = MagicMock()
        msg.html = None
        msg.text = "Line one\n\n\n\n\nLine two    with   spaces"
        msg.extracted_text = None

        result = adapter._clean_newsletter_content(msg)
        assert "\n\n\n" not in result
        assert "  " not in result


class TestLinkExtraction:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_extracts_article_links(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        html = """
        <html><body>
        <a href="https://example.com/article1">Article 1</a>
        <a href="https://techcrunch.com/story">Story</a>
        <a href="https://twitter.com/user/status">Tweet</a>
        </body></html>
        """
        links = adapter._extract_links(html, max_links=5)
        assert "https://example.com/article1" in links
        assert "https://techcrunch.com/story" in links
        # twitter.com is in skip_domains
        assert not any("twitter.com" in l for l in links)

    def test_skips_unsubscribe_links(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        html = """
        <html><body>
        <a href="https://example.com/article">Good</a>
        <a href="https://example.com/unsubscribe">Unsub</a>
        </body></html>
        """
        links = adapter._extract_links(html, max_links=5)
        assert len(links) == 1
        assert "article" in links[0]

    def test_respects_max_links(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        html_links = "".join(
            f'<a href="https://example.com/article{i}">Art {i}</a>\n'
            for i in range(10)
        )
        html = f"<html><body>{html_links}</body></html>"
        links = adapter._extract_links(html, max_links=3)
        assert len(links) == 3

    def test_deduplicates_by_path(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        html = """
        <html><body>
        <a href="https://example.com/article?ref=1">Link A</a>
        <a href="https://example.com/article?ref=2">Link B</a>
        </body></html>
        """
        links = adapter._extract_links(html, max_links=5)
        assert len(links) == 1


class TestAdapterState:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_state_roundtrip(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        state = {
            "last_checked_at": 1709470800.0,
            "processed_message_ids": ["msg_1", "msg_2"],
            "last_weekly_generated": "2026-W09",
        }
        adapter._save_state(state)
        loaded = adapter._load_state()
        assert loaded == state

    def test_corrupt_state_resets(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        adapter._state_path.parent.mkdir(parents=True, exist_ok=True)
        adapter._state_path.write_text("not json at all")
        loaded = adapter._load_state()
        assert loaded == {}

    def test_missing_state_returns_empty(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        loaded = adapter._load_state()
        assert loaded == {}


class TestAdapterTickNoConfig:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_returns_zero_when_no_config(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        adapter._is_quiet_hour = lambda: False
        result = adapter.tick()
        assert result == 0

    def test_returns_zero_during_quiet_hours(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        adapter._is_quiet_hour = lambda: True
        result = adapter.tick()
        assert result == 0


class TestApplySettings:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        config = MagicMock()
        config.agentmail_api_key = "test-key"
        config.agentmail_inbox_id = "test@agentmail.to"

        return NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
        )

    def test_parses_schedule(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        adapter._apply_settings({
            "daily_schedule": "09:30",
            "weekly_schedule": "18:00",
            "quiet_hours": "22:00-07:00",
        })
        assert adapter._daily_schedule == (9, 30)
        assert adapter._weekly_schedule == (18, 0)
        assert adapter._quiet_start == 22
        assert adapter._quiet_end == 7


class TestDailyDigestHandler:
    _DIGEST_PATCHES = [
        patch("gateway.news_digest_handler.load_digest_voice", return_value=""),
        patch("gateway.news_digest_handler.gather_landscape_briefing", return_value=""),
        patch("gateway.news_digest_handler.scan_digest_for_signals", return_value={
            "anticipation_flags": [], "bottleneck_signals": [], "belief_tensions": [],
        }),
        patch("gateway.news_digest_handler.persist_signal_scan_results", return_value={}),
        patch("gateway.news_digest_handler.send_signal_alerts", return_value={}),
    ]

    def _apply_patches(self):
        mocks = [p.start() for p in self._DIGEST_PATCHES]
        return mocks

    def _stop_patches(self):
        for p in self._DIGEST_PATCHES:
            p.stop()

    def test_generates_digest(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "var" / "news_digests" / "daily").mkdir(parents=True)
        self._apply_patches()

        try:
            from gateway.models import Event, Job
            from gateway.news_digest_handler import handle_news_digest_job

            event = Event(
                type="news_digest",
                payload={
                    "date": "2026-03-03",
                    "newsletters": [
                        {
                            "source": "AINews",
                            "category": "ai_tech",
                            "subject": "AI News #200",
                            "clean_text": "Today OpenAI released GPT-5 with multimodal capabilities...",
                            "links_context": [],
                        },
                        {
                            "source": "Sifted",
                            "category": "startups",
                            "subject": "European startups weekly",
                            "clean_text": "Berlin-based Stripe competitor raises $50M...",
                            "links_context": [],
                        },
                    ],
                },
                source="news_digest",
                id=1,
            )
            job = Job(event_id=1, skill="news_digest", id=1)

            mock_executor = MagicMock()
            mock_result = MagicMock()
            mock_result.text = "# Daily Digest — 2026-03-03\n\n## AI & Technology\n\nContent here"
            mock_executor.run_raw.return_value = mock_result

            mock_config = MagicMock()
            mock_config.telegram_bot_token = ""
            mock_config.telegram_allowed_chat_id = ""

            with patch("gateway.news_digest_handler.send_digest_email", return_value=True):
                with patch("gateway.news_digest_handler.send_telegram_message", return_value=False):
                    result = handle_news_digest_job(event, job, mock_config, mock_executor)

            assert "2026-03-03" in result
            assert mock_executor.run_raw.called

            # Verify prompt contains both sections
            prompt_arg = mock_executor.run_raw.call_args[1].get("prompt") or mock_executor.run_raw.call_args[0][0]
            assert "AI & TECH" in prompt_arg or "AINews" in prompt_arg
            assert "STARTUP" in prompt_arg or "Sifted" in prompt_arg

            # Verify file saved
            digest_file = tmp_path / "var" / "news_digests" / "daily" / "2026-03-03.md"
            assert digest_file.exists()
        finally:
            self._stop_patches()

    def test_handles_single_category(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "var" / "news_digests" / "daily").mkdir(parents=True)
        self._apply_patches()

        try:
            from gateway.models import Event, Job
            from gateway.news_digest_handler import handle_news_digest_job

            event = Event(
                type="news_digest",
                payload={
                    "date": "2026-03-03",
                    "newsletters": [
                        {
                            "source": "AINews",
                            "category": "ai_tech",
                            "subject": "AI News",
                            "clean_text": "Content " * 50,
                            "links_context": [],
                        },
                    ],
                },
                source="news_digest",
                id=1,
            )
            job = Job(event_id=1, skill="news_digest", id=1)

            mock_executor = MagicMock()
            mock_result = MagicMock()
            mock_result.text = "# Digest\n\nContent"
            mock_executor.run_raw.return_value = mock_result
            mock_config = MagicMock()

            with patch("gateway.news_digest_handler.send_digest_email", return_value=True):
                with patch("gateway.news_digest_handler.send_telegram_message", return_value=False):
                    result = handle_news_digest_job(event, job, mock_config, mock_executor)

            assert "2026-03-03" in result
        finally:
            self._stop_patches()


class TestWeeklyRoundupHandler:
    _WEEKLY_PATCHES = [
        patch("gateway.news_weekly_handler.load_digest_voice", return_value=""),
        patch("gateway.news_weekly_handler.gather_weekly_landscape_context", return_value=""),
        patch("gateway.news_weekly_handler.scan_weekly_for_anticipation_suggestions", return_value=[]),
        patch("gateway.news_weekly_handler.send_anticipation_suggestions", return_value=0),
    ]

    def _apply_patches(self):
        mocks = [p.start() for p in self._WEEKLY_PATCHES]
        return mocks

    def _stop_patches(self):
        for p in self._WEEKLY_PATCHES:
            p.stop()

    def test_generates_weekly_roundup(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._apply_patches()

        try:
            # Create some daily digests
            daily_dir = tmp_path / "var" / "news_digests" / "daily"
            daily_dir.mkdir(parents=True)
            weekly_dir = tmp_path / "var" / "news_digests" / "weekly"
            weekly_dir.mkdir(parents=True)

            for day in ["2026-02-24", "2026-02-25", "2026-02-26"]:
                (daily_dir / f"{day}.md").write_text(
                    f"# Daily Digest -- {day}\n\n## AI & Technology\n\nContent for {day}",
                    encoding="utf-8",
                )

            from gateway.models import Event, Job
            from gateway.news_weekly_handler import handle_news_weekly_job

            event = Event(
                type="news_weekly",
                payload={"week_label": "2026-W09"},
                source="news_digest",
                id=2,
            )
            job = Job(event_id=2, skill="news_weekly", id=2)

            mock_executor = MagicMock()
            mock_result = MagicMock()
            mock_result.text = "# Weekly Roundup — 2026-W09\n\n## Executive Summary\n\nGreat week."
            mock_executor.run_raw.return_value = mock_result
            mock_config = MagicMock()

            with patch("gateway.news_weekly_handler.send_digest_email", return_value=True):
                with patch("gateway.news_weekly_handler.send_telegram_message", return_value=False):
                    result = handle_news_weekly_job(event, job, mock_config, mock_executor)

            assert "2026-W09" in result
            assert mock_executor.run_raw.called

            weekly_file = weekly_dir / "2026-W09.md"
            assert weekly_file.exists()
        finally:
            self._stop_patches()

    def test_handles_no_daily_digests(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._apply_patches()

        try:
            (tmp_path / "var" / "news_digests" / "daily").mkdir(parents=True)

            from gateway.models import Event, Job
            from gateway.news_weekly_handler import handle_news_weekly_job

            event = Event(
                type="news_weekly",
                payload={"week_label": "2026-W09"},
                source="news_digest",
                id=3,
            )
            job = Job(event_id=3, skill="news_weekly", id=3)
            mock_config = MagicMock()
            mock_executor = MagicMock()

            with patch("gateway.news_weekly_handler.send_digest_email", return_value=False):
                with patch("gateway.news_weekly_handler.send_telegram_message", return_value=False):
                    result = handle_news_weekly_job(event, job, mock_config, mock_executor)

            assert "No daily digests" in result
            assert not mock_executor.run_raw.called
        finally:
            self._stop_patches()


class TestReplayScheduling:
    def _make_adapter(self, tmp_path):
        from adapters.news_digest import NewsDigestAdapter

        config_path = tmp_path / "news_digest_config.yaml"
        config_path.write_text(
            "sources:\n"
            "  - name: AINews\n"
            "    sender: swyx+ainews@substack.com\n"
            "    category: ai_tech\n"
            "settings:\n"
            "  daily_schedule: '10:00'\n"
            "  weekly_schedule: '19:00'\n"
            "  quiet_hours: '23:00-06:00'\n",
            encoding="utf-8",
        )
        state_path = tmp_path / "news_digest_state.json"
        queue = MagicMock()
        queue.insert_event.side_effect = [1, 2, 3, 4, 5]
        config = SimpleNamespace(
            agentmail_api_key="test-key",
            agentmail_inbox_id="test@agentmail.to",
            runtime_db_path=tmp_path / "runtime.db",
            scheduler_replay_days=3,
        )

        adapter = NewsDigestAdapter(
            queue=queue,
            config=config,
            config_path=config_path,
            state_path=state_path,
            timezone="America/New_York",
        )
        adapter._is_quiet_hour = lambda: False
        return adapter

    def test_replays_daily_slots_once_and_marks_empty_slots(self, tmp_path):
        from reading_app.scheduler_ledger import SchedulerLedger

        adapter = self._make_adapter(tmp_path)
        timezone = ZoneInfo("America/New_York")
        FrozenDateTime.frozen_now = datetime(2026, 3, 12, 12, 0, tzinfo=timezone)
        adapter._iter_due_weekly_slots = lambda *_args, **_kwargs: []

        def collect_items(_sources, _settings, *, processed_entry_ids, slot_dt):
            date = slot_dt.strftime("%Y-%m-%d")
            if date == "2026-03-12":
                return [], set()
            return (
                [
                    {
                        "kind": "newsletter",
                        "source": "AINews",
                        "category": "ai_tech",
                        "subject": f"Digest for {date}",
                        "url": "",
                        "published_at": "",
                        "topic_tags": [],
                        "clean_text": "Important update",
                        "links_context": [],
                        "story_key": date,
                    }
                ],
                {f"msg-{date}"},
            )

        adapter._collect_items_for_slot = collect_items

        with patch("adapters.news_digest.datetime", FrozenDateTime):
            result = adapter.tick(startup=True)

        assert result == 2
        payload_dates = [
            call.args[0].payload["date"]
            for call in adapter.queue.insert_event.call_args_list
            if call.args[0].type == "news_digest"
        ]
        assert payload_dates == ["2026-03-10", "2026-03-11"]

        ledger = SchedulerLedger(tmp_path / "runtime.db")
        empty_slot = ledger.get_slot("news_digest", "daily", "2026-03-12T10:00:00-04:00")
        assert empty_slot is not None
        assert empty_slot["status"] == "skipped_empty"

        with patch("adapters.news_digest.datetime", FrozenDateTime):
            second_result = adapter.tick(startup=True)

        assert second_result == 0
        assert adapter.queue.insert_event.call_count == 2

    def test_replays_missed_weekly_slot_once(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        timezone = ZoneInfo("America/New_York")
        FrozenDateTime.frozen_now = datetime(2026, 3, 9, 12, 0, tzinfo=timezone)
        adapter._collect_items_for_slot = lambda *_args, **_kwargs: ([], set())

        with patch("adapters.news_digest.datetime", FrozenDateTime):
            result = adapter.tick(startup=True)

        assert result == 1
        weekly_events = [
            call.args[0]
            for call in adapter.queue.insert_event.call_args_list
            if call.args[0].type == "news_weekly"
        ]
        assert len(weekly_events) == 1
        assert weekly_events[0].payload["week_label"] == "2026-W10"

        with patch("adapters.news_digest.datetime", FrozenDateTime):
            second_result = adapter.tick(startup=True)

        assert second_result == 0

    def test_weekly_replay_still_finds_last_sunday_by_midweek(self, tmp_path):
        adapter = self._make_adapter(tmp_path)
        timezone = ZoneInfo("America/New_York")
        FrozenDateTime.frozen_now = datetime(2026, 3, 11, 12, 0, tzinfo=timezone)
        adapter._collect_items_for_slot = lambda *_args, **_kwargs: ([], set())

        with patch("adapters.news_digest.datetime", FrozenDateTime):
            result = adapter.tick(startup=True)

        assert result == 1
        weekly_events = [
            call.args[0]
            for call in adapter.queue.insert_event.call_args_list
            if call.args[0].type == "news_weekly"
        ]
        assert len(weekly_events) == 1
        assert weekly_events[0].payload["week_label"] == "2026-W10"
