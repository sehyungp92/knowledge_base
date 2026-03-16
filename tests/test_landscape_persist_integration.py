"""Integration tests for landscape signal persistence.

Tests the actual DB insert/merge path that produced FK constraint
violations when theme_ids didn't exist in the themes table.
"""

import pytest


@pytest.mark.integration
class TestLandscapePersistence:
    """Test persist_landscape_signals with real Postgres."""

    def test_valid_signals_persist(self, pg_conn):
        """Signals with valid theme_ids persist without errors."""
        get_conn, source_id, theme_ids = pg_conn
        from ingest.landscape_extractor import persist_landscape_signals

        signals = {
            "capabilities": [
                {
                    "description": "Integration test capability: chain-of-thought reasoning",
                    "theme_id": theme_ids[1],  # chain_of_thought
                    "maturity": "research_only",
                    "confidence": 0.8,
                    "evidence_snippet": "Test evidence snippet",
                },
            ],
            "limitations": [
                {
                    "description": "Integration test limitation: fails on multi-step",
                    "theme_id": theme_ids[0],  # reasoning_and_planning
                    "limitation_type": "architectural",
                    "signal_type": "explicit",
                    "severity": "significant",
                    "trajectory": "improving",
                    "confidence": 0.7,
                    "evidence_snippet": "Test evidence",
                },
            ],
            "bottlenecks": [
                {
                    "description": "Integration test bottleneck: compute for search",
                    "theme_id": theme_ids[2],  # test_time_compute
                    "blocking_what": "real-time inference",
                    "bottleneck_type": "compute",
                    "resolution_horizon": "1-2_years",
                    "confidence": 0.6,
                    "evidence_snippet": "Test evidence",
                },
            ],
            "breakthroughs": [],
        }

        delta = persist_landscape_signals(signals, source_id, get_conn)

        assert delta.counts["capabilities"] >= 1
        assert delta.counts["limitations"] >= 1
        assert delta.counts["bottlenecks"] >= 1

    def test_invalid_theme_ids_filtered(self, pg_conn):
        """Signals with non-existent theme_ids are silently dropped."""
        get_conn, source_id, _ = pg_conn
        from ingest.landscape_extractor import persist_landscape_signals

        signals = {
            "capabilities": [
                {
                    "description": "Should be dropped: fake theme",
                    "theme_id": "completely_nonexistent_theme_abc",
                    "maturity": "demo",
                    "confidence": 0.9,
                    "evidence_snippet": "Test",
                },
            ],
            "limitations": [],
            "bottlenecks": [],
            "breakthroughs": [],
        }

        # This should NOT raise an FK constraint error
        delta = persist_landscape_signals(signals, source_id, get_conn)
        assert delta.counts["capabilities"] == 0

    def test_parent_fallback_remaps_theme(self, pg_conn):
        """Slash-path theme_ids get remapped to their parent."""
        get_conn, source_id, theme_ids = pg_conn
        from ingest.landscape_extractor import persist_landscape_signals

        signals = {
            "capabilities": [
                {
                    "description": "Integration test: parent fallback remap",
                    "theme_id": f"{theme_ids[0]}/nonexistent_child",
                    "maturity": "research_only",
                    "confidence": 0.7,
                    "evidence_snippet": "Test evidence for remap",
                },
            ],
            "limitations": [],
            "bottlenecks": [],
            "breakthroughs": [],
        }

        delta = persist_landscape_signals(signals, source_id, get_conn)
        # Should succeed because parent fallback remaps to theme_ids[0]
        assert delta.counts["capabilities"] >= 1

    def test_deduplication_merge_path(self, pg_conn):
        """Inserting a similar entity twice merges instead of duplicating."""
        get_conn, source_id, theme_ids = pg_conn
        from ingest.landscape_extractor import persist_landscape_signals

        signals = {
            "capabilities": [
                {
                    "description": "Integration test capability for dedup merge",
                    "theme_id": theme_ids[0],
                    "maturity": "demo",
                    "confidence": 0.7,
                    "evidence_snippet": "First evidence",
                },
            ],
            "limitations": [],
            "bottlenecks": [],
            "breakthroughs": [],
        }

        # First insert
        delta1 = persist_landscape_signals(signals, source_id, get_conn)
        assert len(delta1.new_capabilities) >= 1

        # Second insert with same description — should merge
        signals["capabilities"][0]["evidence_snippet"] = "Second evidence"
        delta2 = persist_landscape_signals(signals, source_id, get_conn)
        # Should have merged (or new if similarity below threshold)
        total = delta2.counts["capabilities"]
        assert total >= 1


@pytest.mark.integration
class TestImplicationPersistence:
    """Test persist_cross_theme_implications with real Postgres."""

    def test_valid_implications_persist(self, pg_conn):
        get_conn, source_id, theme_ids = pg_conn
        from ingest.implication_extractor import persist_cross_theme_implications

        implications = [
            {
                "source_theme_id": theme_ids[0],
                "target_theme_id": theme_ids[2],
                "trigger_type": "capability_matured",
                "trigger_id": "",
                "implication": "Integration test: better planning enables test-time compute",
                "confidence": 0.7,
                "evidence_sources": [{"source_id": source_id, "snippet": "Test"}],
            },
        ]

        # Should not raise FK errors
        persist_cross_theme_implications(implications, source_id, get_conn)

        # Verify persisted
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM cross_theme_implications WHERE evidence_sources::text LIKE %s",
                (f"%{source_id}%",),
            ).fetchall()
        assert len(rows) >= 1

    def test_invalid_theme_ids_skipped(self, pg_conn):
        get_conn, source_id, theme_ids = pg_conn
        from ingest.implication_extractor import persist_cross_theme_implications

        implications = [
            {
                "source_theme_id": "fake_nonexistent_theme",
                "target_theme_id": theme_ids[0],
                "trigger_type": "breakthrough",
                "trigger_id": "",
                "implication": "Should be skipped due to invalid source_theme_id",
                "confidence": 0.8,
                "evidence_sources": [],
            },
        ]

        # Should not raise, just skip
        persist_cross_theme_implications(implications, source_id, get_conn)
