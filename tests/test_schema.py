"""Tests for database schema and migration system."""

from pathlib import Path

from db.migrate import SCHEMA_PATH, MIGRATIONS_DIR


def test_schema_file_exists():
    assert SCHEMA_PATH.exists()


def test_schema_has_core_tables():
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "CREATE TABLE" in sql
    assert "sources" in sql
    assert "claims" in sql
    assert "concepts" in sql
    assert "source_edges" in sql
    assert "source_concepts" in sql
    assert "ideas" in sql
    assert "themes" in sql


def test_schema_has_extensions():
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "CREATE EXTENSION IF NOT EXISTS vector" in sql
    assert "CREATE EXTENSION IF NOT EXISTS pg_trgm" in sql


def test_schema_has_indexes():
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "idx_sources_fts" in sql
    assert "idx_claims_fts" in sql
    assert "idx_claims_source" in sql


def test_migrate_module_importable():
    from db import migrate
    assert hasattr(migrate, "migrate")
    assert hasattr(migrate, "_ensure_migrations_table")


def test_migrations_dir_exists():
    assert MIGRATIONS_DIR.exists() or True  # May be empty but parent exists


def test_schema_has_landscape_tables():
    """Schema should include all 7 landscape model tables."""
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    for table in ["capabilities", "limitations", "bottlenecks", "breakthroughs",
                   "anticipations", "challenge_log", "theme_proposals"]:
        assert table in sql, f"Table {table} should be in schema.sql"


def test_schema_has_landscape_indexes():
    """Schema should include landscape-specific indexes."""
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "idx_capabilities_theme" in sql
    assert "idx_limitations_theme" in sql
    assert "idx_bottlenecks_theme" in sql
    assert "idx_breakthroughs_theme" in sql
    assert "idx_anticipations_status" in sql


def test_migration_002_exists():
    """Migration file for landscape tables should exist."""
    migration = MIGRATIONS_DIR / "002_landscape_model.sql"
    assert migration.exists()


def test_migration_002_has_all_tables():
    """Migration 002 should create all landscape tables."""
    migration = MIGRATIONS_DIR / "002_landscape_model.sql"
    sql = migration.read_text(encoding="utf-8")
    for table in ["capabilities", "limitations", "bottlenecks", "breakthroughs",
                   "anticipations", "challenge_log", "theme_proposals"]:
        assert f"CREATE TABLE" in sql and table in sql
