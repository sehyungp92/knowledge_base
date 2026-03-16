"""Database migration runner.

Applies schema.sql + numbered migrations from db/migrations/.
Tracks state in a _migrations table. Idempotent.

Usage: python -m db.migrate
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _ensure_migrations_table(conn):
    """Create _migrations tracking table if it doesn't exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            name TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()


def _get_applied(conn) -> set[str]:
    """Get set of already-applied migration names."""
    rows = conn.execute("SELECT name FROM _migrations").fetchall()
    return {r["name"] for r in rows}


def _apply_sql(conn, name: str, sql: str):
    """Apply a SQL migration and record it."""
    logger.info("Applying: %s", name)
    conn.execute(sql)
    conn.execute("INSERT INTO _migrations (name) VALUES (%s) ON CONFLICT DO NOTHING", (name,))
    conn.commit()


def migrate(dsn: str):
    """Run all pending migrations."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        _ensure_migrations_table(conn)
        applied = _get_applied(conn)

        # Apply base schema
        if "schema.sql" not in applied:
            sql = SCHEMA_PATH.read_text(encoding="utf-8")
            _apply_sql(conn, "schema.sql", sql)
        else:
            logger.info("schema.sql already applied")

        # Apply numbered migrations in order
        if MIGRATIONS_DIR.exists():
            migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
            for mf in migration_files:
                if mf.name not in applied:
                    sql = mf.read_text(encoding="utf-8")
                    _apply_sql(conn, mf.name, sql)
                else:
                    logger.info("%s already applied", mf.name)

    logger.info("Migration complete")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    from reading_app.config import Config
    config = Config()
    migrate(config.postgres_dsn)


if __name__ == "__main__":
    main()
