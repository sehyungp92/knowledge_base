"""Durable ledger for scheduled adapter runs and replay state."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from reading_app.runtime import get_runtime_db_path

TERMINAL_SLOT_STATUSES = {"pending", "enqueued", "complete", "skipped_empty"}


class SchedulerLedger:
    """SQLite-backed ledger for scheduled slots."""

    def __init__(self, db_path: Path | str | None = None):
        resolved_path = Path(db_path) if db_path is not None else get_runtime_db_path()
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(resolved_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scheduler_slots (
                adapter TEXT NOT NULL,
                job_type TEXT NOT NULL,
                slot_key TEXT NOT NULL,
                scheduled_for TEXT NOT NULL,
                status TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                PRIMARY KEY (adapter, job_type, slot_key)
            )
            """
        )
        self._conn.commit()

    def get_slot(self, adapter: str, job_type: str, slot_key: str) -> dict | None:
        row = self._conn.execute(
            """
            SELECT * FROM scheduler_slots
            WHERE adapter = ? AND job_type = ? AND slot_key = ?
            """,
            (adapter, job_type, slot_key),
        ).fetchone()
        if row is None:
            return None
        data = dict(row)
        try:
            data["metadata"] = json.loads(data.get("metadata") or "{}")
        except json.JSONDecodeError:
            data["metadata"] = {}
        return data

    def should_enqueue(self, adapter: str, job_type: str, slot_key: str) -> bool:
        slot = self.get_slot(adapter, job_type, slot_key)
        return slot is None or slot["status"] not in TERMINAL_SLOT_STATUSES

    def mark_status(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        status: str,
        metadata: dict | None = None,
    ) -> None:
        now = time.time()
        metadata_json = json.dumps(metadata or {})
        self._conn.execute(
            """
            INSERT INTO scheduler_slots
                (adapter, job_type, slot_key, scheduled_for, status, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(adapter, job_type, slot_key) DO UPDATE SET
                scheduled_for = excluded.scheduled_for,
                status = excluded.status,
                metadata = excluded.metadata,
                updated_at = excluded.updated_at
            """,
            (adapter, job_type, slot_key, scheduled_for, status, metadata_json, now, now),
        )
        self._conn.commit()

    def mark_pending(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        metadata: dict | None = None,
    ) -> None:
        self.mark_status(
            adapter,
            job_type,
            slot_key,
            scheduled_for=scheduled_for,
            status="pending",
            metadata=metadata,
        )

    def mark_enqueued(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        metadata: dict | None = None,
    ) -> None:
        self.mark_status(
            adapter,
            job_type,
            slot_key,
            scheduled_for=scheduled_for,
            status="enqueued",
            metadata=metadata,
        )

    def mark_complete(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        metadata: dict | None = None,
    ) -> None:
        self.mark_status(
            adapter,
            job_type,
            slot_key,
            scheduled_for=scheduled_for,
            status="complete",
            metadata=metadata,
        )

    def mark_failed(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        metadata: dict | None = None,
    ) -> None:
        self.mark_status(
            adapter,
            job_type,
            slot_key,
            scheduled_for=scheduled_for,
            status="failed",
            metadata=metadata,
        )

    def mark_skipped_empty(
        self,
        adapter: str,
        job_type: str,
        slot_key: str,
        *,
        scheduled_for: str,
        metadata: dict | None = None,
    ) -> None:
        self.mark_status(
            adapter,
            job_type,
            slot_key,
            scheduled_for=scheduled_for,
            status="skipped_empty",
            metadata=metadata,
        )
