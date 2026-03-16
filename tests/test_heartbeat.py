"""Tests for adapters.heartbeat."""

import asyncio
from unittest.mock import patch
from datetime import datetime

from adapters.heartbeat import HeartbeatAdapter
from gateway.queue import Queue


def test_heartbeat_quiet_hours(memory_path):
    q = Queue(":memory:")
    hb = HeartbeatAdapter(q, memory_path, quiet_hours="23:00-07:00")
    with patch.object(hb, "_is_quiet_hour", return_value=True):
        assert hb.tick() is False


def test_heartbeat_empty_file(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    (mem / "heartbeat.md").write_text("# Heartbeat\n", encoding="utf-8")
    q = Queue(":memory:")
    hb = HeartbeatAdapter(q, mem)
    assert hb.tick() is False


def test_heartbeat_enqueues(memory_path):
    q = Queue(":memory:")
    hb = HeartbeatAdapter(q, memory_path)
    # memory_path fixture has real heartbeat content from conftest
    (memory_path / "heartbeat.md").write_text(
        "# Heartbeat\n\n- Check for unread sources\n",
        encoding="utf-8",
    )
    with patch.object(hb, "_is_quiet_hour", return_value=False):
        assert hb.tick() is True


def test_heartbeat_skips_when_user_busy(memory_path):
    from gateway.models import Event, Job
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="msg", payload={}, source="telegram"))
    q.insert_job(Job(event_id=eid, skill="save"))
    (memory_path / "heartbeat.md").write_text(
        "# Heartbeat\n\n- Check for unread sources\n",
        encoding="utf-8",
    )
    hb = HeartbeatAdapter(q, memory_path)
    with patch.object(hb, "_is_quiet_hour", return_value=False):
        assert hb.tick() is False


def test_is_ok_response():
    assert HeartbeatAdapter.is_ok_response("HEARTBEAT_OK") is True
    assert HeartbeatAdapter.is_ok_response("  heartbeat_ok\n") is True
    assert HeartbeatAdapter.is_ok_response("Here is a report") is False


def test_heartbeat_start_runs_startup_evaluation(memory_path):
    q = Queue(":memory:")
    hb = HeartbeatAdapter(q, memory_path)
    (memory_path / "heartbeat.md").write_text(
        "# Heartbeat\n\n- Check for unread sources\n",
        encoding="utf-8",
    )
    with patch.object(hb, "_is_quiet_hour", return_value=False):
        with patch.object(hb, "start_timer") as start_timer:
            asyncio.run(hb.start())

    assert start_timer.called
    job = q.claim_next_job()
    assert job is not None
    event = q.get_event(job.event_id)
    assert event.payload["trigger"] == "startup"
