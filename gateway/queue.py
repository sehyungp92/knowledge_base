"""SQLite-backed job queue for the gateway."""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path

from gateway.models import Event, Job
from gateway.model_preferences import (
    DEFAULT_MODEL_PREFERENCE_KEY,
    normalize_model_tier,
)
from gateway.providers import get_default_provider_id, normalize_provider_id

DEFAULT_QUEUE_DB_PATH = Path(__file__).resolve().parents[1] / "var" / "queue.db"


class Queue:
    """SQLite-backed event and job queue."""

    def __init__(self, db_path: Path | str = DEFAULT_QUEUE_DB_PATH):
        self.db_path = str(db_path)
        parent = os.path.dirname(self.db_path)
        if parent and self.db_path != ":memory:":
            os.makedirs(parent, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._lock = threading.Lock()
        self.create_tables()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                payload TEXT NOT NULL DEFAULT '{}',
                source TEXT DEFAULT '',
                chat_id TEXT DEFAULT '',
                created_at REAL NOT NULL,
                status TEXT DEFAULT 'pending'
            );
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL REFERENCES events(id),
                skill TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                logs_path TEXT DEFAULT '',
                result TEXT DEFAULT '{}',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 2,
                provider_id TEXT NOT NULL DEFAULT 'claude'
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_key TEXT NOT NULL,
                backend_id TEXT NOT NULL DEFAULT 'claude',
                backend_session_id TEXT NOT NULL,
                chat_id TEXT DEFAULT '',
                skill TEXT DEFAULT '',
                last_active_at REAL NOT NULL,
                UNIQUE(session_key, backend_id)
            );
            CREATE TABLE IF NOT EXISTS chat_runtime_preferences (
                session_key TEXT PRIMARY KEY,
                provider_id TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS global_runtime_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS cost_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider_id TEXT NOT NULL,
                model TEXT DEFAULT '',
                cost_usd REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                skill TEXT DEFAULT '',
                job_id INTEGER,
                created_at REAL NOT NULL
            );
        """)
        self._conn.commit()
        self._migrate_jobs_table()
        self._migrate_sessions_table()
        self._migrate_chat_runtime_preferences()
        self._migrate_global_runtime_preferences()

    def _table_columns(self, table_name: str) -> dict[str, sqlite3.Row]:
        cur = self._conn.execute(f"PRAGMA table_info({table_name})")
        return {row["name"]: row for row in cur.fetchall()}

    def _migrate_jobs_table(self):
        """Add provider and retry columns to existing jobs tables if missing."""
        columns = self._table_columns("jobs")
        if "retry_count" not in columns:
            self._conn.execute("ALTER TABLE jobs ADD COLUMN retry_count INTEGER DEFAULT 0")
        if "max_retries" not in columns:
            self._conn.execute("ALTER TABLE jobs ADD COLUMN max_retries INTEGER DEFAULT 2")
        if "provider_id" not in columns:
            self._conn.execute("ALTER TABLE jobs ADD COLUMN provider_id TEXT NOT NULL DEFAULT 'claude'")
        self._conn.commit()

    def _migrate_sessions_table(self):
        """Upgrade legacy Claude-only sessions to provider-aware session rows."""
        columns = self._table_columns("sessions")
        if not columns:
            return

        needs_rebuild = (
            "backend_id" not in columns
            or "backend_session_id" not in columns
            or "claude_session_id" in columns
        )
        if not needs_rebuild:
            return

        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_key TEXT NOT NULL,
                backend_id TEXT NOT NULL DEFAULT 'claude',
                backend_session_id TEXT NOT NULL,
                chat_id TEXT DEFAULT '',
                skill TEXT DEFAULT '',
                last_active_at REAL NOT NULL,
                UNIQUE(session_key, backend_id)
            );
        """)

        if "claude_session_id" in columns:
            self._conn.execute("""
                INSERT INTO sessions_new (session_key, backend_id, backend_session_id, chat_id, skill, last_active_at)
                SELECT session_key, 'claude', claude_session_id, chat_id, skill, last_active_at
                FROM sessions
                WHERE claude_session_id IS NOT NULL AND claude_session_id != ''
            """)
        else:
            self._conn.execute("""
                INSERT INTO sessions_new (session_key, backend_id, backend_session_id, chat_id, skill, last_active_at)
                SELECT session_key, backend_id, backend_session_id, chat_id, skill, last_active_at
                FROM sessions
                WHERE backend_session_id IS NOT NULL AND backend_session_id != ''
            """)

        self._conn.executescript("""
            DROP TABLE sessions;
            ALTER TABLE sessions_new RENAME TO sessions;
        """)
        self._conn.commit()

    def _migrate_chat_runtime_preferences(self):
        """Ensure the provider preference table exists."""
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_runtime_preferences (
                session_key TEXT PRIMARY KEY,
                provider_id TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        self._conn.commit()

    def _migrate_global_runtime_preferences(self):
        """Ensure the global runtime preference table exists."""
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS global_runtime_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        self._conn.commit()

    def close(self):
        """Close the underlying database connection."""
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def insert_event(self, event: Event) -> int:
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO events (type, payload, source, chat_id, created_at, status) VALUES (?, ?, ?, ?, ?, ?)",
                (event.type, json.dumps(event.payload), event.source, event.chat_id, time.time(), event.status),
            )
            self._conn.commit()
            return cur.lastrowid

    def insert_job(self, job: Job) -> int:
        with self._lock:
            now = time.time()
            provider_id = normalize_provider_id(job.provider_id or get_default_provider_id())
            cur = self._conn.execute(
                "INSERT INTO jobs (event_id, skill, status, logs_path, result, created_at, updated_at, retry_count, max_retries, provider_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    job.event_id,
                    job.skill,
                    job.status,
                    job.logs_path,
                    json.dumps(job.result or {}),
                    now,
                    now,
                    job.retry_count,
                    job.max_retries,
                    provider_id,
                ),
            )
            self._conn.commit()
            return cur.lastrowid

    def claim_next_job(self) -> Job | None:
        """Atomically claim the next pending job (excludes post_process jobs)."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM jobs WHERE status = 'pending' AND skill != 'post_process' ORDER BY created_at ASC LIMIT 1"
            )
            row = cur.fetchone()
            if row is None:
                return None
            now = time.time()
            self._conn.execute(
                "UPDATE jobs SET status = 'running', updated_at = ? WHERE id = ? AND status = 'pending'",
                (now, row["id"]),
            )
            self._conn.commit()
            cur2 = self._conn.execute("SELECT * FROM jobs WHERE id = ? AND status = 'running'", (row["id"],))
            row2 = cur2.fetchone()
            if row2 is None:
                return None
            return self._row_to_job(row2)

    def claim_next_job_by_skill(self, skill: str) -> Job | None:
        """Atomically claim the next pending job matching a specific skill."""
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM jobs WHERE status = 'pending' AND skill = ? ORDER BY created_at ASC LIMIT 1",
                (skill,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            now = time.time()
            self._conn.execute(
                "UPDATE jobs SET status = 'running', updated_at = ? WHERE id = ? AND status = 'pending'",
                (now, row["id"]),
            )
            self._conn.commit()
            cur2 = self._conn.execute("SELECT * FROM jobs WHERE id = ? AND status = 'running'", (row["id"],))
            row2 = cur2.fetchone()
            if row2 is None:
                return None
            return self._row_to_job(row2)

    def update_job_status(self, job_id: int, status: str, result: dict | None = None):
        with self._lock:
            now = time.time()
            if result is not None:
                self._conn.execute(
                    "UPDATE jobs SET status = ?, result = ?, updated_at = ? WHERE id = ?",
                    (status, json.dumps(result), now, job_id),
                )
            else:
                self._conn.execute(
                    "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
                    (status, now, job_id),
                )
            self._conn.commit()

    def update_job_progress(
        self,
        job_id: int,
        progress: str,
        *,
        provider_id: str | None = None,
        skill: str | None = None,
        extra: dict | None = None,
        stages: list[dict] | None = None,
    ) -> None:
        """Persist the latest in-flight progress snippet for a running job.

        Args:
            stages: Optional list of RunStage dicts for structured stage tracking.
        """
        with self._lock:
            job = self.get_job(job_id)
            if job is None:
                return

            result = dict(job.result or {})
            result["progress"] = str(progress).strip()
            if provider_id:
                result["provider_id"] = normalize_provider_id(provider_id)
            if skill:
                result["skill"] = skill
            if extra:
                result.update(extra)
            if stages is not None:
                result["stages"] = stages

            now = time.time()
            self._conn.execute(
                "UPDATE jobs SET status = 'running', result = ?, updated_at = ? WHERE id = ?",
                (json.dumps(result), now, job_id),
            )
            self._conn.commit()

    def get_job(self, job_id: int) -> Job | None:
        cur = self._conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cur.fetchone()
        return self._row_to_job(row) if row else None

    def get_event(self, event_id: int) -> Event | None:
        cur = self._conn.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cur.fetchone()
        return self._row_to_event(row) if row else None

    def retry_or_dead_letter(self, job_id: int, error: str) -> str:
        """Retry a failed job or move to dead_letter.

        Returns the new status: 'pending' (retrying) or 'dead_letter'.
        """
        with self._lock:
            job = self.get_job(job_id)
            if job is None:
                return "dead_letter"

            now = time.time()
            if job.retry_count < job.max_retries:
                delay = 5 * (2 ** job.retry_count)
                self._conn.execute(
                    "UPDATE jobs SET status = 'pending', retry_count = retry_count + 1, "
                    "created_at = ?, updated_at = ?, result = ? WHERE id = ?",
                    (now + delay, now, json.dumps({"last_error": error}), job_id),
                )
                self._conn.commit()
                return "pending"

            self._conn.execute(
                "UPDATE jobs SET status = 'dead_letter', updated_at = ?, result = ? WHERE id = ?",
                (now, json.dumps({"error": error, "retries_exhausted": True}), job_id),
            )
            self._conn.commit()
            return "dead_letter"

    def retry_job(self, job_id: int) -> bool:
        """Manually re-queue a dead_letter job. Returns True if successful."""
        with self._lock:
            job = self.get_job(job_id)
            if job is None or job.status != "dead_letter":
                return False
            now = time.time()
            self._conn.execute(
                "UPDATE jobs SET status = 'pending', retry_count = 0, "
                "created_at = ?, updated_at = ? WHERE id = ?",
                (now, now, job_id),
            )
            self._conn.commit()
            return True

    def mark_running_interrupted(self):
        """Mark all currently running jobs as interrupted (used during forced shutdown)."""
        with self._lock:
            now = time.time()
            self._conn.execute(
                "UPDATE jobs SET status = 'interrupted', updated_at = ? WHERE status = 'running'",
                (now,),
            )
            self._conn.commit()

    def count_pending_user_jobs(self) -> int:
        """Count pending/running jobs from non-heartbeat sources."""
        cur = self._conn.execute("""
            SELECT COUNT(*) as cnt FROM jobs j
            JOIN events e ON j.event_id = e.id
            WHERE j.status IN ('pending', 'running')
            AND e.source != 'heartbeat'
        """)
        return cur.fetchone()["cnt"]

    def get_session(self, session_key: str, backend_id: str) -> str | None:
        """Get the persisted backend session/thread ID for a chat session."""
        cur = self._conn.execute(
            "SELECT backend_session_id FROM sessions WHERE session_key = ? AND backend_id = ?",
            (session_key, normalize_provider_id(backend_id)),
        )
        row = cur.fetchone()
        return row["backend_session_id"] if row else None

    def upsert_session(
        self,
        session_key: str,
        backend_session_id: str,
        *,
        backend_id: str = "claude",
        chat_id: str = "",
        skill: str = "",
    ):
        """Create or update a provider-specific session mapping."""
        with self._lock:
            now = time.time()
            normalized_backend = normalize_provider_id(backend_id)
            self._conn.execute(
                "INSERT INTO sessions (session_key, backend_id, backend_session_id, chat_id, skill, last_active_at) "
                "VALUES (?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(session_key, backend_id) DO UPDATE SET "
                "backend_session_id = excluded.backend_session_id, "
                "chat_id = excluded.chat_id, "
                "skill = excluded.skill, "
                "last_active_at = excluded.last_active_at",
                (session_key, normalized_backend, backend_session_id, chat_id, skill, now),
            )
            self._conn.commit()

    def get_chat_provider(self, session_key: str) -> str | None:
        """Return the sticky provider for a chat, if one was chosen."""
        cur = self._conn.execute(
            "SELECT provider_id FROM chat_runtime_preferences WHERE session_key = ?",
            (session_key,),
        )
        row = cur.fetchone()
        return normalize_provider_id(row["provider_id"]) if row else None

    def set_chat_provider(self, session_key: str, provider_id: str) -> str:
        """Persist a chat-scoped provider choice."""
        with self._lock:
            normalized = normalize_provider_id(provider_id)
            now = time.time()
            self._conn.execute(
                "INSERT INTO chat_runtime_preferences (session_key, provider_id, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(session_key) DO UPDATE SET provider_id = excluded.provider_id, updated_at = excluded.updated_at",
                (session_key, normalized, now),
            )
            self._conn.commit()
            return normalized

    def get_global_preference(self, key: str) -> str | None:
        """Return a global runtime preference value, if one was set."""
        cur = self._conn.execute(
            "SELECT value FROM global_runtime_preferences WHERE key = ?",
            (key,),
        )
        row = cur.fetchone()
        return str(row["value"]).strip() if row and row["value"] is not None else None

    def set_global_preference(self, key: str, value: str) -> str:
        """Persist a global runtime preference value."""
        with self._lock:
            normalized = str(value).strip()
            now = time.time()
            self._conn.execute(
                "INSERT INTO global_runtime_preferences (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
                (key, normalized, now),
            )
            self._conn.commit()
            return normalized

    def get_global_model(self) -> str | None:
        """Return the persisted global default model tier, if one was set."""
        stored = self.get_global_preference(DEFAULT_MODEL_PREFERENCE_KEY)
        if not stored:
            return None
        return normalize_model_tier(stored)

    def set_global_model(self, model_tier: str) -> str:
        """Persist the global default model tier."""
        normalized = normalize_model_tier(model_tier)
        self.set_global_preference(DEFAULT_MODEL_PREFERENCE_KEY, normalized)
        return normalized

    def cleanup_stale_sessions(self, max_age_hours: int = 24):
        """Remove sessions older than max_age_hours."""
        with self._lock:
            cutoff = time.time() - (max_age_hours * 3600)
            self._conn.execute("DELETE FROM sessions WHERE last_active_at < ?", (cutoff,))
            self._conn.commit()

    def _row_to_job(self, row: sqlite3.Row) -> Job:
        return Job(
            id=row["id"],
            event_id=row["event_id"],
            skill=row["skill"],
            status=row["status"],
            logs_path=row["logs_path"],
            result=json.loads(row["result"]) if row["result"] else None,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            retry_count=row["retry_count"] if "retry_count" in row.keys() else 0,
            max_retries=row["max_retries"] if "max_retries" in row.keys() else 2,
            provider_id=row["provider_id"] if "provider_id" in row.keys() else "claude",
        )

    def log_cost(
        self,
        *,
        provider_id: str,
        model: str = "",
        cost_usd: float | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        skill: str = "",
        job_id: int | None = None,
    ) -> None:
        """Record a cost entry for provider spend tracking."""
        if cost_usd is None and input_tokens is None and output_tokens is None:
            return
        with self._lock:
            self._conn.execute(
                "INSERT INTO cost_log (provider_id, model, cost_usd, input_tokens, output_tokens, skill, job_id, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    normalize_provider_id(provider_id),
                    model or "",
                    cost_usd,
                    input_tokens,
                    output_tokens,
                    skill or "",
                    job_id,
                    time.time(),
                ),
            )
            self._conn.commit()

    def get_cost_summary(self, *, days: int = 1) -> list[dict]:
        """Aggregate cost data by provider for the last N days."""
        cutoff = time.time() - (days * 86400)
        cur = self._conn.execute(
            """
            SELECT
                provider_id,
                COUNT(*) as call_count,
                COALESCE(SUM(cost_usd), 0) as total_cost_usd,
                COALESCE(SUM(input_tokens), 0) as total_input_tokens,
                COALESCE(SUM(output_tokens), 0) as total_output_tokens
            FROM cost_log
            WHERE created_at >= ?
            GROUP BY provider_id
            ORDER BY total_cost_usd DESC
            """,
            (cutoff,),
        )
        return [dict(row) for row in cur.fetchall()]

    def update_job_provider(self, job_id: int, provider_id: str) -> None:
        """Update the provider_id on a job."""
        with self._lock:
            self._conn.execute(
                "UPDATE jobs SET provider_id = ?, updated_at = ? WHERE id = ?",
                (provider_id, time.time(), job_id),
            )
            self._conn.commit()

    def update_job_skill(self, job_id: int, skill: str) -> None:
        """Update the skill on a job."""
        with self._lock:
            self._conn.execute(
                "UPDATE jobs SET skill = ?, updated_at = ? WHERE id = ?",
                (skill, time.time(), job_id),
            )
            self._conn.commit()

    def get_last_heartbeat_time(self) -> float | None:
        """Return the updated_at timestamp of the most recent heartbeat job, or None."""
        cur = self._conn.execute(
            "SELECT max(updated_at) AS t FROM jobs WHERE skill = 'heartbeat'"
        )
        row = cur.fetchone()
        if row and row["t"]:
            return row["t"]
        return None

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        return Event(
            id=row["id"],
            type=row["type"],
            payload=json.loads(row["payload"]) if row["payload"] else {},
            source=row["source"],
            chat_id=row["chat_id"],
            created_at=row["created_at"],
            status=row["status"],
        )
