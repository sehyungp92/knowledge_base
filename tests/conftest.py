"""Shared test fixtures for the knowledge_base test suite."""

from __future__ import annotations

import os
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: tests requiring a real PostgreSQL connection"
    )


@pytest.fixture
def pg_conn():
    """Real PostgreSQL connection for integration tests.

    Creates test themes, test source, and cleans up after.
    Skips if DB is unavailable (CI environments without Postgres).

    Yields (get_conn_fn, source_id, theme_ids) tuple.
    """
    try:
        from reading_app.db import ensure_pool, get_conn
        ensure_pool()
        # Verify connection works
        with get_conn() as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        pytest.skip(f"PostgreSQL not available: {exc}")

    source_id = "src_integ_test_001"
    theme_ids = ["reasoning_and_planning", "chain_of_thought", "test_time_compute"]

    # Setup: ensure themes and source exist
    with get_conn() as conn:
        for tid in theme_ids:
            conn.execute(
                """INSERT INTO themes (id, name)
                   VALUES (%s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (tid, tid.replace("_", " ").title()),
            )
        # Insert parent edge: chain_of_thought -> reasoning_and_planning
        conn.execute(
            """INSERT INTO theme_edges (parent_id, child_id, relationship)
               VALUES (%s, %s, 'contains')
               ON CONFLICT DO NOTHING""",
            ("reasoning_and_planning", "chain_of_thought"),
        )
        conn.execute(
            """INSERT INTO theme_edges (parent_id, child_id, relationship)
               VALUES (%s, %s, 'contains')
               ON CONFLICT DO NOTHING""",
            ("reasoning_and_planning", "test_time_compute"),
        )
        conn.execute(
            """INSERT INTO sources (id, source_type, title, processing_status)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING""",
            (source_id, "article", "Integration Test Source", "processing"),
        )
        conn.commit()

    yield get_conn, source_id, theme_ids

    # Teardown: clean up test data
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM source_themes WHERE source_id = %s", (source_id,)
        )
        conn.execute(
            "DELETE FROM capabilities WHERE evidence_sources::text LIKE %s",
            (f"%{source_id}%",),
        )
        conn.execute(
            "DELETE FROM limitations WHERE evidence_sources::text LIKE %s",
            (f"%{source_id}%",),
        )
        conn.execute(
            "DELETE FROM bottlenecks WHERE evidence_sources::text LIKE %s",
            (f"%{source_id}%",),
        )
        conn.execute(
            "DELETE FROM breakthroughs WHERE primary_source_id = %s",
            (source_id,),
        )
        conn.execute(
            "DELETE FROM cross_theme_implications WHERE evidence_sources::text LIKE %s",
            (f"%{source_id}%",),
        )
        conn.execute(
            "DELETE FROM sources WHERE id = %s", (source_id,)
        )
        conn.commit()


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory for test artifacts."""
    return tmp_path


@pytest.fixture
def library_path(tmp_path):
    """Provide a temporary library directory."""
    lib = tmp_path / "library"
    lib.mkdir()
    return lib


@pytest.fixture
def memory_path(tmp_path):
    """Provide a temporary memory directory with standard structure."""
    mem = tmp_path / "memory"
    mem.mkdir()
    (mem / "logs").mkdir()
    (mem / "beliefs").mkdir()
    (mem / "memory.md").write_text("# Memory\n\n## Preferences\n\n## Objectives\n", encoding="utf-8")
    (mem / "soul.md").write_text("# Soul\n\nI am a research assistant.\n", encoding="utf-8")
    (mem / "agents.md").write_text("# Agent Rules\n\n- Always cite sources.\n", encoding="utf-8")
    (mem / "heartbeat.md").write_text("# Heartbeat Instructions\n", encoding="utf-8")
    return mem


@pytest.fixture
def sqlite_db(tmp_path):
    """Provide a temporary SQLite database connection."""
    db_path = tmp_path / "test_queue.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def mock_executor():
    """Provide a mock ClaudeExecutor."""
    executor = MagicMock()
    executor.run_raw.return_value = MagicMock(
        text="Test response",
        cost_usd=0.001,
        usage={"input_tokens": 100, "output_tokens": 50},
        success=True,
        return_code=0,
    )
    executor.run.return_value = executor.run_raw.return_value
    return executor


@pytest.fixture
def sample_source():
    """Provide sample source data for testing."""
    return {
        "id": "src_test_001",
        "source_type": "article",
        "url": "https://example.com/test-article",
        "title": "Test Article on AI Safety",
        "authors": ["Alice", "Bob"],
        "abstract": "This article discusses AI safety mechanisms.",
    }


@pytest.fixture
def sample_claims():
    """Provide sample claim data for testing."""
    return [
        {
            "id": "clm_001",
            "source_id": "src_test_001",
            "claim_text": "RLHF reduces harmful outputs by 70%",
            "claim_type": "finding",
            "section": "Results",
            "confidence": 0.85,
            "evidence_snippet": "Our experiments show RLHF reduces harmful outputs by 70%",
            "evidence_location": "Section 4.2",
            "evidence_type": "quote",
        },
        {
            "id": "clm_002",
            "source_id": "src_test_001",
            "claim_text": "Constitutional AI outperforms vanilla RLHF",
            "claim_type": "finding",
            "section": "Discussion",
            "confidence": 0.75,
            "evidence_snippet": "Constitutional AI consistently outperforms vanilla RLHF in our benchmarks",
            "evidence_location": "Section 5.1",
            "evidence_type": "quote",
        },
    ]
