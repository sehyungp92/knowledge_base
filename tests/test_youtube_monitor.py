"""Tests for the YouTube channel monitor adapter."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from adapters.youtube_monitor import YouTubeMonitorAdapter


@pytest.fixture
def tmp_paths(tmp_path):
    watchlist_path = tmp_path / "youtube_watchlist.yaml"
    state_path = tmp_path / "youtube_monitor_state.json"
    return watchlist_path, state_path


@pytest.fixture
def adapter(tmp_paths):
    watchlist_path, state_path = tmp_paths
    queue = MagicMock()
    queue.insert_event.return_value = 1
    config = MagicMock()
    return YouTubeMonitorAdapter(
        queue=queue,
        config=config,
        watchlist_path=watchlist_path,
        state_path=state_path,
        timezone="America/New_York",
    )


class TestTickNoWatchlist:
    def test_returns_zero_when_no_watchlist(self, adapter):
        """No watchlist file -> tick does nothing."""
        result = adapter.tick()
        assert result == 0

    def test_returns_zero_when_empty_watchlist(self, adapter, tmp_paths):
        """Empty channels list -> tick does nothing."""
        watchlist_path, _ = tmp_paths
        watchlist_path.write_text("channels: []\nsettings:\n  schedule: ['09:00', '21:00']\n")
        result = adapter.tick()
        assert result == 0


class TestQuietHours:
    def test_skips_during_quiet_hours(self, adapter, tmp_paths):
        """Tick returns 0 when in quiet hours."""
        watchlist_path, _ = tmp_paths
        watchlist_path.write_text(
            "channels:\n  - name: Test\n    channel_id: UC123\n    keywords: []\n"
            "settings:\n  schedule: ['09:00', '21:00']\n  quiet_hours: '00:00-23:59'\n"
        )
        # Force quiet hours to cover all hours
        adapter._quiet_start = 0
        adapter._quiet_end = 24
        # Override _is_quiet_hour to return True
        adapter._is_quiet_hour = lambda: True
        result = adapter.tick()
        assert result == 0


class TestKeywordFiltering:
    def test_matches_keyword_case_insensitive(self):
        assert YouTubeMonitorAdapter._matches_keywords("New AI Model Released", ["ai"])

    def test_no_match_when_keyword_absent(self):
        assert not YouTubeMonitorAdapter._matches_keywords("Cooking Tutorial", ["ai", "neural"])

    def test_empty_keywords_matches_all(self):
        assert YouTubeMonitorAdapter._matches_keywords("Anything at all", [])

    def test_partial_match(self):
        assert YouTubeMonitorAdapter._matches_keywords("Diffusion Models Explained", ["diffusion"])


class TestStatePersistence:
    def test_state_roundtrip(self, adapter, tmp_paths):
        _, state_path = tmp_paths
        state = {"UC123": {"last_video_id": "abc", "published": "2025-01-01"}}
        adapter._save_state(state)
        loaded = adapter._load_state()
        assert loaded == state

    def test_corrupt_state_resets(self, adapter, tmp_paths):
        _, state_path = tmp_paths
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("not json at all")
        loaded = adapter._load_state()
        assert loaded == {}


class TestStartupBacklog:
    @patch("adapters.youtube_monitor.feedparser")
    def test_startup_backlog_drains_without_duplicates(self, mock_feedparser, adapter, tmp_paths):
        watchlist_path, state_path = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: []\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 2\n"
            "  quiet_hours: '23:00-07:00'\n"
        )

        state_path.write_text(json.dumps({"UC123": {"last_video_id": "vid0"}}), encoding="utf-8")
        adapter._config.youtube_startup_backlog_cap = 2
        adapter._is_quiet_hour = lambda: False

        entries = []
        for video_id in ["vid3", "vid2", "vid1", "vid0"]:
            entry = MagicMock()
            entry.get = lambda key, default="", video_id=video_id: {
                "yt_videoid": video_id,
                "title": f"Video {video_id}",
                "published": f"2025-01-0{max(1, len(video_id))}",
            }.get(key, default)
            entries.append(entry)

        mock_feed = MagicMock()
        mock_feed.entries = entries
        mock_feedparser.parse.return_value = mock_feed

        first_result = adapter.tick(startup=True)
        assert first_result == 2

        state_after_first = adapter._load_state()
        assert state_after_first["UC123"]["last_video_id"] == "vid3"
        assert [item["video_id"] for item in state_after_first["UC123"]["startup_backlog"]] == ["vid3"]

        second_result = adapter.tick()
        assert second_result == 1

        state_after_second = adapter._load_state()
        assert "startup_backlog" not in state_after_second["UC123"]
        assert adapter.queue.insert_event.call_count == 3

        third_result = adapter.tick()
        assert third_result == 0
        assert adapter.queue.insert_event.call_count == 3

    @patch("adapters.youtube_monitor.feedparser")
    def test_saved_backlog_drains_even_if_feed_fetch_fails(self, mock_feedparser, adapter, tmp_paths):
        watchlist_path, state_path = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: []\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 2\n"
            "  quiet_hours: '23:00-07:00'\n"
        )
        state_path.write_text(
            json.dumps(
                {
                    "UC123": {
                        "last_video_id": "vid3",
                        "startup_backlog": [
                            {
                                "video_id": "vid2",
                                "title": "Video vid2",
                                "published": "2025-01-02",
                                "url": "https://www.youtube.com/watch?v=vid2",
                            }
                        ],
                    }
                }
            ),
            encoding="utf-8",
        )
        adapter._is_quiet_hour = lambda: False
        mock_feedparser.parse.side_effect = RuntimeError("feed unavailable")

        result = adapter.tick()

        assert result == 1
        assert adapter.queue.insert_event.call_count == 1
        state_after = adapter._load_state()
        assert "startup_backlog" not in state_after["UC123"]

    @patch("adapters.youtube_monitor.feedparser")
    def test_newer_videos_append_behind_saved_backlog(self, mock_feedparser, adapter, tmp_paths):
        watchlist_path, state_path = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: []\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 3\n"
            "  quiet_hours: '23:00-07:00'\n"
        )
        state_path.write_text(
            json.dumps(
                {
                    "UC123": {
                        "last_video_id": "vid3",
                        "startup_backlog": [
                            {
                                "video_id": "vid2",
                                "title": "Video vid2",
                                "published": "2025-01-02",
                                "url": "https://www.youtube.com/watch?v=vid2",
                            }
                        ],
                    }
                }
            ),
            encoding="utf-8",
        )
        adapter._is_quiet_hour = lambda: False

        entries = []
        for video_id in ["vid5", "vid4", "vid3", "vid2"]:
            entry = MagicMock()
            entry.get = lambda key, default="", video_id=video_id: {
                "yt_videoid": video_id,
                "title": f"Video {video_id}",
                "published": f"2025-01-{10 + len(video_id)}",
            }.get(key, default)
            entries.append(entry)

        mock_feed = MagicMock()
        mock_feed.entries = entries
        mock_feedparser.parse.return_value = mock_feed

        result = adapter.tick()

        assert result == 3
        payload_titles = [
            call.args[0].payload["title"]
            for call in adapter.queue.insert_event.call_args_list
        ]
        assert payload_titles == ["Video vid2", "Video vid4", "Video vid5"]
        state_after = adapter._load_state()
        assert state_after["UC123"]["last_video_id"] == "vid5"


class TestMaxVideosPerTick:
    @patch("adapters.youtube_monitor.feedparser")
    def test_respects_max_videos_cap(self, mock_feedparser, adapter, tmp_paths):
        """Only enqueue up to max_videos_per_tick videos."""
        watchlist_path, _ = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: Test\n"
            "    channel_id: UC123\n"
            "    keywords: []\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 2\n"
            "  quiet_hours: '23:00-07:00'\n"
        )

        # Mock feedparser to return 5 entries
        entries = []
        for i in range(5):
            entry = MagicMock()
            entry.get = lambda key, default="", i=i: {
                "yt_videoid": f"vid{i}",
                "title": f"Video {i}",
                "published": "2025-01-01",
            }.get(key, default)
            entries.append(entry)

        mock_feed = MagicMock()
        mock_feed.entries = entries
        mock_feedparser.parse.return_value = mock_feed

        # Ensure not quiet hours
        adapter._is_quiet_hour = lambda: False

        result = adapter.tick()
        assert result == 2
        assert adapter.queue.insert_event.call_count == 2


class TestRSSParsing:
    @patch("adapters.youtube_monitor.feedparser")
    def test_enqueues_matching_video(self, mock_feedparser, adapter, tmp_paths):
        """A single matching video gets enqueued."""
        watchlist_path, _ = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: ['AI']\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 3\n"
            "  quiet_hours: '23:00-07:00'\n"
        )

        entry = MagicMock()
        entry.get = lambda key, default="": {
            "yt_videoid": "vid1",
            "title": "New AI Breakthrough",
            "published": "2025-06-01",
        }.get(key, default)

        mock_feed = MagicMock()
        mock_feed.entries = [entry]
        mock_feedparser.parse.return_value = mock_feed

        adapter._is_quiet_hour = lambda: False

        result = adapter.tick()
        assert result == 1

        # Verify event payload
        call_args = adapter.queue.insert_event.call_args[0][0]
        assert call_args.type == "youtube_monitor"
        assert call_args.payload["url"] == "https://www.youtube.com/watch?v=vid1"
        assert call_args.payload["channel"] == "TestChannel"

    @patch("adapters.youtube_monitor.feedparser")
    def test_skips_non_matching_video(self, mock_feedparser, adapter, tmp_paths):
        """A video that doesn't match keywords is not enqueued."""
        watchlist_path, _ = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: ['quantum']\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 3\n"
            "  quiet_hours: '23:00-07:00'\n"
        )

        entry = MagicMock()
        entry.get = lambda key, default="": {
            "yt_videoid": "vid1",
            "title": "Cooking with Fire",
            "published": "2025-06-01",
        }.get(key, default)

        mock_feed = MagicMock()
        mock_feed.entries = [entry]
        mock_feedparser.parse.return_value = mock_feed

        adapter._is_quiet_hour = lambda: False

        result = adapter.tick()
        assert result == 0

    @patch("adapters.youtube_monitor.feedparser")
    def test_deduplicates_against_state(self, mock_feedparser, adapter, tmp_paths):
        """Videos already seen (in state) are not re-enqueued."""
        watchlist_path, state_path = tmp_paths
        watchlist_path.write_text(
            "channels:\n"
            "  - name: TestChannel\n"
            "    channel_id: UC123\n"
            "    keywords: []\n"
            "settings:\n"
            "  schedule: ['09:00', '21:00']\n"
            "  max_videos_per_tick: 3\n"
            "  quiet_hours: '23:00-07:00'\n"
        )

        # Pre-populate state with vid1 already seen
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps({
            "UC123": {"last_video_id": "vid1", "published": "2025-06-01"}
        }))

        entry1 = MagicMock()
        entry1.get = lambda key, default="": {
            "yt_videoid": "vid1",
            "title": "Already Seen",
            "published": "2025-06-01",
        }.get(key, default)

        mock_feed = MagicMock()
        mock_feed.entries = [entry1]  # Only the already-seen video
        mock_feedparser.parse.return_value = mock_feed

        adapter._is_quiet_hour = lambda: False

        result = adapter.tick()
        assert result == 0


class TestScheduleParsing:
    def test_parse_schedule(self):
        result = YouTubeMonitorAdapter._parse_schedule(["09:00", "21:00"])
        assert result == [(9, 0), (21, 0)]

    def test_parse_schedule_unsorted_input(self):
        result = YouTubeMonitorAdapter._parse_schedule(["21:00", "09:00"])
        assert result == [(9, 0), (21, 0)]

    def test_parse_schedule_with_minutes(self):
        result = YouTubeMonitorAdapter._parse_schedule(["09:30", "21:15"])
        assert result == [(9, 30), (21, 15)]


class TestSecondsUntilNextScheduled:
    def test_next_tick_is_later_today(self, adapter):
        """When a scheduled time is still ahead today, targets that time."""
        adapter._schedule = [(23, 59)]
        with patch("adapters.youtube_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 3, 10, 0, 0, tzinfo=adapter.timezone)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            seconds = adapter._seconds_until_next_scheduled()
            # 10:00 -> 23:59 = 13h59m = 50340s
            assert seconds == 50340

    def test_all_times_passed_wraps_to_tomorrow(self, adapter):
        """When all scheduled times passed, targets the first one tomorrow."""
        adapter._schedule = [(9, 0)]
        with patch("adapters.youtube_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 3, 22, 0, 0, tzinfo=adapter.timezone)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            seconds = adapter._seconds_until_next_scheduled()
            # 22:00 today -> 09:00 tomorrow = 11h = 39600s
            assert seconds == 39600

    def test_picks_earliest_future_time(self, adapter):
        """With two times, picks the nearest one that's still in the future."""
        adapter._schedule = [(9, 0), (21, 0)]
        with patch("adapters.youtube_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 3, 12, 0, 0, tzinfo=adapter.timezone)
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            seconds = adapter._seconds_until_next_scheduled()
            # 12:00 -> 21:00 = 9h = 32400s
            assert seconds == 32400
