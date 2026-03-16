"""Heartbeat adapter: scheduled proactive checks."""

from __future__ import annotations

import logging
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from gateway.models import Event, Job
from gateway.queue import Queue

logger = logging.getLogger(__name__)


class HeartbeatAdapter:
    """Scheduled heartbeat adapter with quiet hours and queue-busy skip.

    Implements the Adapter protocol from adapters.base.
    Unlike messaging adapters, HeartbeatAdapter generates events on a timer
    rather than receiving them from external platforms.
    """

    name: str = "heartbeat"

    def __init__(
        self,
        queue: Queue,
        memory_path: Path,
        timezone: str = "America/New_York",
        quiet_hours: str = "23:00-07:00",
        interval: int = 1800,
    ):
        self.queue = queue
        self.memory_path = Path(memory_path)
        self._heartbeat_path = self.memory_path / "heartbeat.md"
        self.timezone = ZoneInfo(timezone)
        self.quiet_start, self.quiet_end = self._parse_quiet_hours(quiet_hours)
        self.interval = interval
        self._timer: threading.Timer | None = None
        self._running = False

    def _parse_quiet_hours(self, spec: str) -> tuple[int, int]:
        """Parse 'HH:MM-HH:MM' into (start_hour, end_hour)."""
        parts = spec.replace("\u2013", "-").split("-")
        start = int(parts[0].strip().split(":")[0])
        end = int(parts[1].strip().split(":")[0])
        return start, end

    def _is_quiet_hour(self) -> bool:
        """Check if current time is within quiet hours."""
        now = datetime.now(self.timezone)
        hour = now.hour
        if self.quiet_start > self.quiet_end:
            # Wraps midnight: e.g., 23:00 - 07:00
            return hour >= self.quiet_start or hour < self.quiet_end
        return self.quiet_start <= hour < self.quiet_end

    def _heartbeat_effectively_empty(self) -> bool:
        """Check if heartbeat.md has no actionable content."""
        if not self._heartbeat_path.exists():
            return True
        try:
            for line in self._heartbeat_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and stripped not in ("- [ ]", "-", "*"):
                    return False
            return True
        except Exception:
            return True

    def tick(self, *, trigger: str = "scheduled") -> bool:
        """Execute one heartbeat tick.

        Returns True if a heartbeat event was enqueued, False if skipped.
        """
        # Check quiet hours
        if self._is_quiet_hour():
            logger.debug("Heartbeat skipped: quiet hours")
            return False

        # Check if heartbeat.md is effectively empty
        if self._heartbeat_effectively_empty():
            logger.debug("Heartbeat skipped: heartbeat.md empty")
            return False

        # Check queue busy (user jobs pending)
        if self.queue.count_pending_user_jobs() > 0:
            logger.debug("Heartbeat skipped: user jobs pending")
            return False

        # Enqueue heartbeat event
        event = Event(
            type="heartbeat",
            payload={"trigger": trigger},
            source="heartbeat",
        )
        event_id = self.queue.insert_event(event)
        self.queue.insert_job(Job(event_id=event_id, skill="heartbeat"))
        logger.info("Heartbeat event %d enqueued", event_id)
        return True

    @staticmethod
    def is_ok_response(text: str) -> bool:
        """Check if response is the suppression signal."""
        return text.strip().upper() == "HEARTBEAT_OK"

    async def start(self) -> None:
        """Start the heartbeat timer (Adapter protocol)."""
        self.tick(trigger="startup")
        self.start_timer()

    async def stop(self) -> None:
        """Stop the heartbeat timer (Adapter protocol)."""
        self.stop_timer()

    def send_message_sync(self, chat_id: str, text: str) -> None:
        """No-op: heartbeat adapter doesn't send messages."""

    def send_typing_sync(self, chat_id: str) -> None:
        """No-op: heartbeat adapter doesn't send typing indicators."""

    def start_timer(self, interval: int | None = None):
        """Start the repeating heartbeat timer."""
        self._running = True
        self._schedule_next(interval or self.interval)

    def stop_timer(self):
        """Stop the heartbeat timer."""
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _schedule_next(self, interval: int):
        if not self._running:
            return
        self._timer = threading.Timer(interval, self._on_timer)
        self._timer.daemon = True
        self._timer.start()

    def _on_timer(self):
        try:
            self.tick()
        except Exception:
            logger.error("Heartbeat tick failed", exc_info=True)
        finally:
            if self._running:
                self._schedule_next(self.interval)
