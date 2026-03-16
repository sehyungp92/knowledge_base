"""Tests for reading_app.db.

These are unit tests that verify the function signatures and SQL construction.
Integration tests require a running PostgreSQL instance with pgvector.
"""

import json
from unittest.mock import patch, MagicMock

import pytest


def test_import():
    from reading_app import db
    assert hasattr(db, "insert_source")
    assert hasattr(db, "get_source")
    assert hasattr(db, "list_sources")
    assert hasattr(db, "insert_claim")
    assert hasattr(db, "get_claims_for_source")
    assert hasattr(db, "insert_concept")
    assert hasattr(db, "insert_source_edge")
    assert hasattr(db, "insert_source_concept")
    assert hasattr(db, "insert_idea")
    assert hasattr(db, "get_ideas_for_source")
    assert hasattr(db, "insert_theme")
    assert hasattr(db, "insert_theme_edge")
    assert hasattr(db, "insert_source_theme")
    assert hasattr(db, "insert_cross_theme_implication")


def test_insert_claim_edge_raises_not_implemented():
    """insert_claim_edge is a deprecation stub and should raise."""
    from reading_app.db import insert_claim_edge
    with pytest.raises(NotImplementedError, match="no longer supported"):
        insert_claim_edge("a", "b", "c")


def test_pool_not_initialized():
    from reading_app.db import get_conn
    import reading_app.db as db_mod
    original_pool = db_mod._pool
    db_mod._pool = None
    try:
        with pytest.raises(RuntimeError, match="not initialized"):
            with get_conn():
                pass
    finally:
        db_mod._pool = original_pool


def test_landscape_helpers_importable():
    """All landscape DB helpers should be importable."""
    from reading_app import db
    assert hasattr(db, "insert_capability")
    assert hasattr(db, "insert_limitation")
    assert hasattr(db, "insert_bottleneck")
    assert hasattr(db, "get_bottleneck")
    assert hasattr(db, "update_bottleneck")
    assert hasattr(db, "append_bottleneck_approach")
    assert hasattr(db, "insert_breakthrough")
    assert hasattr(db, "insert_anticipation")
    assert hasattr(db, "get_anticipation")
    assert hasattr(db, "get_open_anticipations_for_themes")
    assert hasattr(db, "append_anticipation_evidence")
    assert hasattr(db, "insert_challenge_log")
    assert hasattr(db, "insert_theme_proposal")
    assert hasattr(db, "get_pending_theme_proposals")
    assert hasattr(db, "update_theme_proposal_status")
    assert hasattr(db, "update_theme_velocity")
    assert hasattr(db, "update_theme_state_summary")


def test_belief_helpers_importable():
    """All belief DB helpers should be importable (Phase 4)."""
    from reading_app import db
    assert hasattr(db, "insert_belief")
    assert hasattr(db, "get_belief")
    assert hasattr(db, "get_active_beliefs")
    assert hasattr(db, "get_beliefs_for_theme")
    assert hasattr(db, "get_beliefs_by_type")
    assert hasattr(db, "list_beliefs")
    assert hasattr(db, "update_belief_confidence")
    assert hasattr(db, "update_belief_status")
    assert hasattr(db, "append_belief_evidence")
    assert hasattr(db, "append_belief_landscape_link")
    assert hasattr(db, "append_belief_derived_anticipation")
    assert hasattr(db, "find_similar_belief")
    assert hasattr(db, "get_stale_beliefs")
    assert hasattr(db, "get_low_confidence_beliefs")
    assert hasattr(db, "get_unchallenged_beliefs")
    assert hasattr(db, "get_belief_pairs_for_consistency")


def test_belief_valid_enums():
    """Belief status and type enums should be defined."""
    from reading_app.db import VALID_BELIEF_STATUS, VALID_BELIEF_TYPE
    assert VALID_BELIEF_STATUS == {"active", "resolved", "archived"}
    assert VALID_BELIEF_TYPE == {"factual", "predictive", "methodological", "meta"}
