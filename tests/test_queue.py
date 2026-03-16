"""Tests for gateway.queue."""

import sqlite3

from gateway.queue import Queue
from gateway.models import Event, Job


def test_create_tables():
    q = Queue(":memory:")
    q.create_tables()
    # Should not raise on second call (idempotent)
    q.create_tables()


def test_insert_and_get_event():
    q = Queue(":memory:")

    event = Event(type="human_message", payload={"text": "hello"}, source="telegram", chat_id="123")
    event_id = q.insert_event(event)
    assert event_id is not None

    retrieved = q.get_event(event_id)
    assert retrieved is not None
    assert retrieved.type == "human_message"


def test_insert_job_and_claim():
    q = Queue(":memory:")

    event = Event(type="human_message", payload={"text": "/save url"}, source="telegram", chat_id="123")
    event_id = q.insert_event(event)
    q.insert_job(Job(event_id=event_id, skill="save", provider_id="codex"))

    job = q.claim_next_job()
    assert job is not None
    assert job.skill == "save"
    assert job.provider_id == "codex"


def test_claim_empty_queue():
    q = Queue(":memory:")
    job = q.claim_next_job()
    assert job is None


def test_update_job_status():
    q = Queue(":memory:")

    event = Event(type="human_message", payload={"text": "test"}, source="telegram", chat_id="123")
    event_id = q.insert_event(event)
    q.insert_job(Job(event_id=event_id, skill="ask"))
    job = q.claim_next_job()

    q.update_job_status(job.id, "complete", result={"text": "Done"})
    updated = q.get_job(job.id)
    assert updated.status == "complete"


def test_update_job_progress():
    q = Queue(":memory:")

    event = Event(type="human_message", payload={"text": "test"}, source="webapp", chat_id="webapp")
    event_id = q.insert_event(event)
    q.insert_job(Job(event_id=event_id, skill="save", provider_id="claude"))
    job = q.claim_next_job()

    q.update_job_progress(job.id, "Reading source...", provider_id="claude", skill="save")
    updated = q.get_job(job.id)

    assert updated.status == "running"
    assert updated.result["progress"] == "Reading source..."
    assert updated.result["provider_id"] == "claude"
    assert updated.result["skill"] == "save"


def test_count_pending_user_jobs():
    q = Queue(":memory:")

    # Insert a user job
    event = Event(type="human_message", payload={"text": "test"}, source="telegram", chat_id="123")
    event_id = q.insert_event(event)
    q.insert_job(Job(event_id=event_id, skill="ask"))

    count = q.count_pending_user_jobs()
    assert count == 1


def test_count_pending_excludes_heartbeat():
    q = Queue(":memory:")

    # Insert a heartbeat job
    event = Event(type="heartbeat", payload={}, source="heartbeat", chat_id="")
    event_id = q.insert_event(event)
    q.insert_job(Job(event_id=event_id, skill="heartbeat"))

    count = q.count_pending_user_jobs()
    assert count == 0


def test_provider_specific_sessions_are_isolated():
    q = Queue(":memory:")

    q.upsert_session("chat_123", "claude-session", backend_id="claude")
    q.upsert_session("chat_123", "codex-thread", backend_id="codex")

    assert q.get_session("chat_123", "claude") == "claude-session"
    assert q.get_session("chat_123", "codex") == "codex-thread"
    assert q.get_session("chat_123", "zai") is None


def test_chat_provider_preference_round_trip():
    q = Queue(":memory:")

    assert q.get_chat_provider("chat_123") is None
    assert q.set_chat_provider("chat_123", "zai") == "zai"
    assert q.get_chat_provider("chat_123") == "zai"


def test_global_model_round_trip():
    q = Queue(":memory:")

    assert q.get_global_model() is None
    assert q.set_global_model("balanced") == "sonnet"
    assert q.get_global_model() == "sonnet"


def test_legacy_sessions_migrate_to_provider_aware_schema(tmp_path):
    db_path = tmp_path / "queue.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key TEXT NOT NULL,
            claude_session_id TEXT NOT NULL,
            chat_id TEXT DEFAULT '',
            skill TEXT DEFAULT '',
            last_active_at REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        INSERT INTO sessions (session_key, claude_session_id, chat_id, skill, last_active_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("chat_42", "legacy-session", "42", "ask", 1.0),
    )
    conn.commit()
    conn.close()

    q = Queue(db_path)

    assert q.get_session("chat_42", "claude") == "legacy-session"
    columns = {
        row["name"]
        for row in q._conn.execute("PRAGMA table_info(sessions)").fetchall()
    }
    assert "backend_id" in columns
    assert "backend_session_id" in columns
