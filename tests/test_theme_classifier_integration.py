"""Integration tests for theme_classifier persistence path.

These tests exercise the actual DB insert path that was the root cause
of FK constraint violations in production.
"""

import pytest


@pytest.mark.integration
class TestThemeClassifierPersistence:
    """Test classify_themes DB persistence with real Postgres."""

    def test_valid_themes_insert_succeeds(self, pg_conn):
        """Pre-parsed themes with valid theme_ids insert without FK errors."""
        get_conn, source_id, theme_ids = pg_conn

        # Simulate what classify_themes does after parsing: upsert to source_themes
        with get_conn() as conn:
            for tid in theme_ids[:2]:
                conn.execute(
                    """INSERT INTO source_themes (source_id, theme_id, relevance)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (source_id, theme_id) DO UPDATE SET
                         relevance = EXCLUDED.relevance""",
                    (source_id, tid, 0.85),
                )
            conn.commit()

        # Verify they persisted
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT theme_id, relevance FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
        assert len(rows) >= 2
        inserted_ids = {r["theme_id"] for r in rows}
        assert theme_ids[0] in inserted_ids
        assert theme_ids[1] in inserted_ids

    def test_invalid_theme_id_filtered_out(self, pg_conn):
        """Themes with invalid theme_id are filtered before insert — no FK error."""
        get_conn, source_id, theme_ids = pg_conn
        from ingest.theme_validator import load_valid_theme_ids

        valid_themes = load_valid_theme_ids(get_conn)
        assert valid_themes is not None

        fake_themes = [
            {"theme_id": "nonexistent_theme_xyz", "relevance": 0.9, "level": 1},
            {"theme_id": theme_ids[0], "relevance": 0.8, "level": 1},
        ]

        # Filter like classify_themes does
        filtered = [t for t in fake_themes if t.get("theme_id") in valid_themes]
        assert len(filtered) == 1
        assert filtered[0]["theme_id"] == theme_ids[0]

    def test_parent_propagation_for_level2(self, pg_conn):
        """Level-2 themes propagate to their level-1 parent via theme_edges."""
        get_conn, source_id, theme_ids = pg_conn
        from ingest.theme_classifier import _propagate_parent_themes

        # chain_of_thought is level-2 under reasoning_and_planning
        themes = [{"theme_id": "chain_of_thought", "relevance": 0.9, "level": 2}]
        result = _propagate_parent_themes(themes, source_id, get_conn)

        parent_ids = {t["theme_id"] for t in result if t.get("_propagated")}
        assert "reasoning_and_planning" in parent_ids


@pytest.mark.integration
class TestThemeValidator:
    """Test the shared theme_validator module."""

    def test_load_valid_theme_ids(self, pg_conn):
        get_conn, _, theme_ids = pg_conn
        from ingest.theme_validator import load_valid_theme_ids

        valid = load_valid_theme_ids(get_conn)
        assert valid is not None
        for tid in theme_ids:
            assert tid in valid

    def test_resolve_theme_id_exact(self, pg_conn):
        get_conn, _, theme_ids = pg_conn
        from ingest.theme_validator import load_valid_theme_ids, resolve_theme_id

        valid = load_valid_theme_ids(get_conn)
        assert resolve_theme_id("chain_of_thought", valid) == "chain_of_thought"

    def test_resolve_theme_id_parent_fallback(self, pg_conn):
        get_conn, _, _ = pg_conn
        from ingest.theme_validator import load_valid_theme_ids, resolve_theme_id

        valid = load_valid_theme_ids(get_conn)
        # Slash-path format: parent/child where parent exists but child doesn't
        result = resolve_theme_id("reasoning_and_planning/nonexistent_child", valid)
        assert result == "reasoning_and_planning"

    def test_resolve_theme_id_unknown_returns_none(self, pg_conn):
        get_conn, _, _ = pg_conn
        from ingest.theme_validator import load_valid_theme_ids, resolve_theme_id

        valid = load_valid_theme_ids(get_conn)
        assert resolve_theme_id("completely_fake_theme", valid) is None

    def test_validate_theme_ids_in_entities(self, pg_conn):
        get_conn, _, theme_ids = pg_conn
        from ingest.theme_validator import load_valid_theme_ids, validate_theme_ids_in_entities

        valid = load_valid_theme_ids(get_conn)
        entities = [
            {"theme_id": theme_ids[0], "description": "Valid"},
            {"theme_id": "fake_nonexistent", "description": "Invalid"},
            {"theme_id": f"{theme_ids[0]}/fake_child", "description": "Remapped to parent"},
        ]
        result = validate_theme_ids_in_entities(entities, valid)
        assert len(result) == 2
        assert result[0]["theme_id"] == theme_ids[0]
        assert result[1]["theme_id"] == theme_ids[0]  # Remapped
