"""YouTube channel monitor adapter: wall-clock scheduled RSS feed checking."""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import feedparser
import yaml

from gateway.models import Event, Job
from gateway.queue import Queue

logger = logging.getLogger(__name__)

_DEFAULT_SCHEDULE = ["09:00", "21:00"]


def _coerce_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class YouTubeMonitorAdapter:
    """Polls YouTube RSS feeds at fixed wall-clock times and on startup."""

    name: str = "youtube_monitor"

    def __init__(
        self,
        queue: Queue,
        config,
        watchlist_path: Path,
        state_path: Path,
        timezone: str = "America/New_York",
    ):
        self.queue = queue
        self._config = config
        self._watchlist_path = Path(watchlist_path)
        self._state_path = Path(state_path)
        self.timezone = ZoneInfo(timezone)
        self._timer: threading.Timer | None = None
        self._running = False
        self._startup_replay_pending = True

        self._schedule: list[tuple[int, int]] = [(9, 0), (21, 0)]
        self._max_videos_per_tick = 3
        self._quiet_start = 23
        self._quiet_end = 7
        self._startup_backlog_cap = _coerce_int(
            getattr(config, "youtube_startup_backlog_cap", 10),
            10,
        )

    def _load_watchlist(self) -> dict:
        if not self._watchlist_path.exists():
            return {}
        try:
            return yaml.safe_load(self._watchlist_path.read_text(encoding="utf-8")) or {}
        except Exception:
            logger.error("Failed to parse watchlist", exc_info=True)
            return {}

    def _load_state(self) -> dict:
        if not self._state_path.exists():
            return {}
        try:
            return json.loads(self._state_path.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Corrupt state file, resetting", exc_info=True)
            return {}

    def _save_state(self, state: dict) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _is_quiet_hour(self) -> bool:
        now = datetime.now(self.timezone)
        hour = now.hour
        if self._quiet_start > self._quiet_end:
            return hour >= self._quiet_start or hour < self._quiet_end
        return self._quiet_start <= hour < self._quiet_end

    @staticmethod
    def _matches_keywords(title: str, keywords: list[str]) -> bool:
        if not keywords:
            return True
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in keywords)

    def _entry_state(self, entry) -> dict:
        video_id = entry.get("yt_videoid", "")
        return {
            "video_id": video_id,
            "title": entry.get("title", "Untitled"),
            "published": entry.get("published", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }

    def _normalize_backlog(self, raw_backlog) -> list[dict]:
        backlog: list[dict] = []
        for item in raw_backlog or []:
            if not isinstance(item, dict):
                continue
            video_id = str(item.get("video_id") or "").strip()
            if not video_id:
                continue
            backlog.append(
                {
                    "video_id": video_id,
                    "title": str(item.get("title") or "Untitled"),
                    "published": str(item.get("published") or ""),
                    "url": str(item.get("url") or f"https://www.youtube.com/watch?v={video_id}"),
                }
            )
        return backlog

    def _build_backlog(self, entries, keywords: list[str], last_seen_id: str | None) -> list[dict]:
        backlog: list[dict] = []
        for entry in entries:
            video_id = entry.get("yt_videoid", "")
            if not video_id:
                continue
            if video_id == last_seen_id:
                break
            if self._matches_keywords(entry.get("title", ""), keywords):
                backlog.append(self._entry_state(entry))
        backlog.reverse()
        return backlog

    def _merge_backlog(self, existing: list[dict], discovered: list[dict]) -> list[dict]:
        merged: list[dict] = []
        seen_ids: set[str] = set()
        for item in [*(existing or []), *(discovered or [])]:
            video_id = str(item.get("video_id") or "").strip()
            if not video_id or video_id in seen_ids:
                continue
            seen_ids.add(video_id)
            merged.append(item)
        return merged

    def _enqueue_video(self, item: dict, channel_name: str, channel_id: str) -> None:
        event = Event(
            type="youtube_monitor",
            payload={
                "text": item["url"],
                "url": item["url"],
                "title": item["title"],
                "channel": channel_name,
                "channel_id": channel_id,
                "published": item.get("published", ""),
            },
            source="youtube_monitor",
        )
        event_id = self.queue.insert_event(event)
        self.queue.insert_job(Job(event_id=event_id, skill="youtube_monitor"))
        logger.info("YouTube monitor enqueued: %s -- %s", channel_name, item["title"])

    def _drain_backlog(
        self,
        backlog: list[dict],
        *,
        remaining: int,
        channel_name: str,
        channel_id: str,
    ) -> tuple[int, list[dict]]:
        if remaining <= 0 or not backlog:
            return 0, backlog
        to_send = backlog[:remaining]
        for item in to_send:
            self._enqueue_video(item, channel_name, channel_id)
        return len(to_send), backlog[remaining:]

    def tick(self, *, startup: bool = False) -> int:
        """Execute one monitor tick. Returns number of videos enqueued."""
        if self._is_quiet_hour() and not startup:
            logger.debug("YouTube monitor skipped: quiet hours")
            return 0

        watchlist = self._load_watchlist()
        channels = watchlist.get("channels", [])
        if not channels:
            logger.debug("YouTube monitor skipped: no channels configured")
            return 0

        settings = watchlist.get("settings", {})
        quiet_spec = settings.get("quiet_hours", "23:00-07:00")
        parts = quiet_spec.replace("\u2013", "-").split("-")
        self._quiet_start = int(parts[0].strip().split(":")[0])
        self._quiet_end = int(parts[1].strip().split(":")[0])
        self._max_videos_per_tick = settings.get("max_videos_per_tick", 3)
        self._schedule = self._parse_schedule(settings.get("schedule", _DEFAULT_SCHEDULE))
        self._startup_backlog_cap = _coerce_int(
            getattr(self._config, "youtube_startup_backlog_cap", self._startup_backlog_cap),
            self._startup_backlog_cap,
        )

        if self._is_quiet_hour() and not startup:
            logger.debug("YouTube monitor skipped: quiet hours (after settings load)")
            return 0

        state = self._load_state()
        enqueued = 0
        cap = self._startup_backlog_cap if startup else self._max_videos_per_tick

        for channel in channels:
            if enqueued >= cap:
                break

            channel_id = channel.get("channel_id", "")
            channel_name = channel.get("name", channel_id)
            keywords = channel.get("keywords", [])

            if not channel_id:
                continue

            feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = None
            try:
                feed = feedparser.parse(feed_url)
            except Exception:
                logger.warning("RSS fetch failed for %s", channel_name, exc_info=True)

            ch_state = dict(state.get(channel_id, {}))
            existing_backlog = self._normalize_backlog(ch_state.get("startup_backlog"))
            last_seen_id = ch_state.get("last_video_id")

            newest = None
            newest_id = ""
            discovered_backlog: list[dict] = []
            if feed is not None and feed.entries:
                newest = feed.entries[0]
                newest_id = newest.get("yt_videoid", "")
                if startup or existing_backlog:
                    discovered_backlog = self._build_backlog(feed.entries, keywords, last_seen_id)

            combined_backlog = self._merge_backlog(existing_backlog, discovered_backlog)
            if combined_backlog:
                drained, remaining_backlog = self._drain_backlog(
                    combined_backlog,
                    remaining=cap - enqueued,
                    channel_name=channel_name,
                    channel_id=channel_id,
                )
                enqueued += drained
                if remaining_backlog:
                    ch_state["startup_backlog"] = remaining_backlog
                else:
                    ch_state.pop("startup_backlog", None)
                if newest_id:
                    ch_state["last_video_id"] = newest_id
                    ch_state["published"] = newest.get("published", "")
                ch_state["checked_at"] = datetime.now(self.timezone).isoformat()
                state[channel_id] = ch_state
                continue

            if feed is None or not feed.entries:
                ch_state["checked_at"] = datetime.now(self.timezone).isoformat()
                state[channel_id] = ch_state
                continue

            new_videos = []
            for entry in feed.entries:
                video_id = entry.get("yt_videoid", "")
                if not video_id:
                    continue
                if video_id == last_seen_id:
                    break
                if self._matches_keywords(entry.get("title", ""), keywords):
                    new_videos.append(entry)

            remaining = cap - enqueued
            for entry in new_videos[:remaining]:
                self._enqueue_video(self._entry_state(entry), channel_name, channel_id)
                enqueued += 1

            ch_state["last_video_id"] = newest_id
            ch_state["published"] = newest.get("published", "")
            ch_state["checked_at"] = datetime.now(self.timezone).isoformat()
            state[channel_id] = ch_state

        self._save_state(state)
        if enqueued:
            logger.info("YouTube monitor tick: %d videos enqueued", enqueued)
        return enqueued

    @staticmethod
    def _parse_schedule(spec: list[str]) -> list[tuple[int, int]]:
        result = []
        for s in spec:
            parts = s.strip().split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            result.append((hour, minute))
        return sorted(result)

    def _seconds_until_next_scheduled(self) -> int:
        now = datetime.now(self.timezone)

        for hour, minute in self._schedule:
            candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if candidate > now:
                return max(1, int((candidate - now).total_seconds()))

        first_hour, first_minute = self._schedule[0]
        tomorrow = (now + timedelta(days=1)).replace(
            hour=first_hour,
            minute=first_minute,
            second=0,
            microsecond=0,
        )
        return max(1, int((tomorrow - now).total_seconds()))

    async def start(self) -> None:
        self._running = True
        self._schedule_next(2)
        logger.info(
            "YouTube monitor started (schedule=%s, startup tick in 2s)",
            [f"{h:02d}:{m:02d}" for h, m in self._schedule],
        )

    async def stop(self) -> None:
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def send_message_sync(self, chat_id: str, text: str) -> None:
        """No-op: monitor adapter doesn't send messages."""

    def send_typing_sync(self, chat_id: str) -> None:
        """No-op: monitor adapter doesn't send typing indicators."""

    def _schedule_next(self, delay_seconds: int) -> None:
        if not self._running:
            return
        self._timer = threading.Timer(delay_seconds, self._on_timer)
        self._timer.daemon = True
        self._timer.start()

    def _on_timer(self) -> None:
        startup = self._startup_replay_pending
        self._startup_replay_pending = False
        try:
            self.tick(startup=startup)
        except Exception:
            logger.error("YouTube monitor tick failed", exc_info=True)
        finally:
            if self._running:
                delay = self._seconds_until_next_scheduled()
                next_time = datetime.now(self.timezone) + timedelta(seconds=delay)
                logger.info(
                    "Next YouTube monitor tick at %s (%ds)",
                    next_time.strftime("%H:%M"),
                    delay,
                )
                self._schedule_next(delay)
