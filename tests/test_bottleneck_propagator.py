"""Tests for bottleneck propagation from breakthrough detection."""

import sys
import pytest
from unittest.mock import patch, MagicMock

from ingest.bottleneck_propagator import (
    propagate_breakthrough_to_bottlenecks,
    persist_bottleneck_updates,
    _effect_to_promise,
    BottleneckUpdate,
)


def _mock_db(**overrides):
    """Create a mock reading_app.db module with default stubs."""
    mock = MagicMock()
    for name, value in overrides.items():
        setattr(mock, name, value)
    return mock


class _DBPatch:
    """Context manager to temporarily replace reading_app.db in sys.modules."""

    def __init__(self, mock_db):
        self.mock_db = mock_db
        self.saved = None

    def __enter__(self):
        self.saved = sys.modules.get("reading_app.db")
        sys.modules["reading_app.db"] = self.mock_db
        return self.mock_db

    def __exit__(self, *exc):
        if self.saved is None:
            sys.modules.pop("reading_app.db", None)
        else:
            sys.modules["reading_app.db"] = self.saved
        return False


class TestEffectToPromise:
    def test_resolves_is_high(self):
        assert _effect_to_promise("resolves") == "high"

    def test_reduces_is_medium(self):
        assert _effect_to_promise("reduces") == "medium"

    def test_reframes_is_medium(self):
        assert _effect_to_promise("reframes") == "medium"

    def test_unknown_is_low(self):
        assert _effect_to_promise("something_else") == "low"


class TestPropagateBreakthroughToBottlenecks:

    def test_no_affected_returns_empty(self):
        result = propagate_breakthrough_to_bottlenecks(
            {"description": "test", "bottlenecks_affected": []}, "src_1"
        )
        assert result == []

    def test_missing_affected_returns_empty(self):
        result = propagate_breakthrough_to_bottlenecks(
            {"description": "test"}, "src_1"
        )
        assert result == []

    def test_bottleneck_not_found_skips(self):
        mock_db = _mock_db(get_bottleneck=MagicMock(return_value=None))
        with _DBPatch(mock_db):
            result = propagate_breakthrough_to_bottlenecks(
                {"description": "test", "bottlenecks_affected": [{"bottleneck_id": "bn_1", "effect": "reduces"}]},
                "src_1",
            )
            assert result == []

    def test_resolves_shortens_horizon(self):
        mock_db = _mock_db(
            get_bottleneck=MagicMock(return_value={"id": "bn_1", "resolution_horizon": "5+_years", "description": "test bn"})
        )
        with _DBPatch(mock_db):
            result = propagate_breakthrough_to_bottlenecks(
                {"description": "major advance", "bottlenecks_affected": [{"bottleneck_id": "bn_1", "effect": "resolves"}]},
                "src_1",
            )
            assert len(result) == 1
            assert result[0].new_horizon == "1-2_years"
            assert result[0].add_approach["promise_level"] == "high"

    def test_reduces_shortens_horizon_conservatively(self):
        mock_db = _mock_db(
            get_bottleneck=MagicMock(return_value={"id": "bn_1", "resolution_horizon": "5+_years", "description": "test bn"})
        )
        with _DBPatch(mock_db):
            result = propagate_breakthrough_to_bottlenecks(
                {"description": "partial advance", "bottlenecks_affected": [{"bottleneck_id": "bn_1", "effect": "reduces"}]},
                "src_1",
            )
            assert len(result) == 1
            assert result[0].new_horizon == "3-5_years"

    def test_reframes_no_horizon_change(self):
        mock_db = _mock_db(
            get_bottleneck=MagicMock(return_value={"id": "bn_1", "resolution_horizon": "3-5_years", "description": "test bn"})
        )
        with _DBPatch(mock_db):
            result = propagate_breakthrough_to_bottlenecks(
                {"description": "new perspective", "bottlenecks_affected": [{"bottleneck_id": "bn_1", "effect": "reframes"}]},
                "src_1",
            )
            assert len(result) == 1
            assert result[0].new_horizon is None
            assert result[0].note is not None

    def test_resolves_already_short_no_change(self):
        mock_db = _mock_db(
            get_bottleneck=MagicMock(return_value={"id": "bn_1", "resolution_horizon": "months", "description": "test bn"})
        )
        with _DBPatch(mock_db):
            result = propagate_breakthrough_to_bottlenecks(
                {"description": "advance", "bottlenecks_affected": [{"bottleneck_id": "bn_1", "effect": "resolves"}]},
                "src_1",
            )
            assert len(result) == 1
            assert result[0].new_horizon is None  # months is already shortest practical


class TestPersistBottleneckUpdates:

    def test_empty_updates_returns_zero(self):
        assert persist_bottleneck_updates([], "src_1") == 0

    def test_persists_with_horizon_change(self):
        mock_db = _mock_db(
            append_bottleneck_approach=MagicMock(return_value={"id": "bn_1"}),
            update_bottleneck=MagicMock(return_value={"id": "bn_1"}),
            insert_challenge_log=MagicMock(return_value={"id": "cl_1"}),
            insert_landscape_history=MagicMock(return_value={"id": 1}),
        )
        with _DBPatch(mock_db):
            updates = [BottleneckUpdate(
                bottleneck_id="bn_1",
                add_approach={"approach": "test", "who": "src_1", "promise_level": "high", "source_ids": ["src_1"]},
                new_horizon="1-2_years",
                old_horizon="5+_years",
                propagation_source="src_1",
            )]
            count = persist_bottleneck_updates(updates, "src_1")
            assert count == 1
            mock_db.append_bottleneck_approach.assert_called_once()
            mock_db.update_bottleneck.assert_called_once()
            mock_db.insert_challenge_log.assert_called_once()
            mock_db.insert_landscape_history.assert_called_once()

    def test_persists_approach_only(self):
        mock_db = _mock_db(
            append_bottleneck_approach=MagicMock(return_value={"id": "bn_1"}),
        )
        with _DBPatch(mock_db):
            updates = [BottleneckUpdate(
                bottleneck_id="bn_1",
                add_approach={"approach": "test", "who": "src_1", "promise_level": "medium", "source_ids": ["src_1"]},
                propagation_source="src_1",
            )]
            count = persist_bottleneck_updates(updates, "src_1")
            assert count == 1
