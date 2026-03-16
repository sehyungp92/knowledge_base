"""Tests for local runtime helpers and scheduler ledger."""

from __future__ import annotations

import os

import reading_app.runtime as runtime
from reading_app.scheduler_ledger import SchedulerLedger


class _DummyConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_acquire_pid_lock_and_request_shutdown(tmp_path, monkeypatch):
    runtime_dir = tmp_path / "runtime"
    monkeypatch.setattr(runtime, "RUNTIME_DIR", runtime_dir)
    monkeypatch.setenv("RUNTIME_LOG_DIR", str(runtime_dir / "logs"))
    monkeypatch.setattr(runtime.os, "kill", lambda pid, sig: None)

    files = runtime.acquire_pid_lock("unit_runtime")

    assert runtime.read_live_pid(files.pid_file) == os.getpid()
    runtime.mark_process_ready(files)
    assert runtime.wait_for_process_ready("unit_runtime", timeout_s=0.1) is True
    runtime.clear_process_ready(files)
    assert files.ready_file.exists() is False
    assert runtime.request_shutdown("unit_runtime") is True
    assert files.shutdown_file.exists()


def test_wait_for_postgres_retries_until_success(monkeypatch):
    attempts = {"count": 0}

    def fake_connect(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("database unavailable")
        return _DummyConnection()

    monkeypatch.setattr(runtime.psycopg, "connect", fake_connect)

    ok, last_error = runtime.wait_for_postgres("postgresql://example", timeout_s=1, interval_s=0)

    assert ok is True
    assert last_error == ""
    assert attempts["count"] == 2


def test_wait_for_process_ready_allows_pid_to_appear_late(tmp_path, monkeypatch):
    runtime_dir = tmp_path / "runtime"
    monkeypatch.setattr(runtime, "RUNTIME_DIR", runtime_dir)
    monkeypatch.setenv("RUNTIME_LOG_DIR", str(runtime_dir / "logs"))

    files = runtime.get_process_files("late_ready")
    state = {"calls": 0}

    def fake_read_live_pid(_pid_file):
        state["calls"] += 1
        if state["calls"] < 2:
            return None
        return 1234

    def fake_sleep(_seconds):
        if state["calls"] >= 2:
            files.ready_file.write_text("ready", encoding="utf-8")

    monkeypatch.setattr(runtime, "read_live_pid", fake_read_live_pid)
    monkeypatch.setattr(runtime.time, "sleep", fake_sleep)

    assert runtime.wait_for_process_ready("late_ready", timeout_s=1.0) is True


def test_detached_popen_kwargs_windows(monkeypatch):
    monkeypatch.setattr(runtime.os, "name", "nt", raising=False)

    kwargs = runtime.detached_popen_kwargs()

    assert "creationflags" in kwargs
    assert kwargs["close_fds"] is True


def test_scheduler_ledger_state_transitions(tmp_path):
    ledger = SchedulerLedger(tmp_path / "runtime.db")

    assert ledger.should_enqueue("news_digest", "daily", "slot-1") is True

    ledger.mark_enqueued(
        "news_digest",
        "daily",
        "slot-1",
        scheduled_for="2026-03-09T10:00:00-04:00",
        metadata={"date": "2026-03-09"},
    )
    assert ledger.should_enqueue("news_digest", "daily", "slot-1") is False

    ledger.mark_pending(
        "news_digest",
        "daily",
        "slot-1",
        scheduled_for="2026-03-09T10:00:00-04:00",
        metadata={"date": "2026-03-09"},
    )
    assert ledger.should_enqueue("news_digest", "daily", "slot-1") is False

    ledger.mark_failed(
        "news_digest",
        "daily",
        "slot-1",
        scheduled_for="2026-03-09T10:00:00-04:00",
        metadata={"date": "2026-03-09"},
    )
    assert ledger.should_enqueue("news_digest", "daily", "slot-1") is True

    ledger.mark_skipped_empty(
        "news_digest",
        "daily",
        "slot-1",
        scheduled_for="2026-03-09T10:00:00-04:00",
        metadata={"date": "2026-03-09"},
    )
    assert ledger.should_enqueue("news_digest", "daily", "slot-1") is False
