"""Shared dependencies for FastAPI routes."""

from __future__ import annotations

from reading_app.db import get_conn


def get_db_conn():
    """Dependency that yields a Postgres connection from the pool."""
    with get_conn() as conn:
        yield conn
