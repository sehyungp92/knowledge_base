"""Tests for challenge handler cascade functions.

Tests _check_beliefs_for_landscape_entity, _check_stale_implications,
_cascade_to_anticipations, and _cascade_to_dependent_bottlenecks.
These are warning generators that surface linked entities for human review.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from gateway.challenge_handler import (
    _check_beliefs_for_landscape_entity,
    _check_stale_implications,
    _cascade_to_anticipations,
    _cascade_to_dependent_bottlenecks,
    _parse_command,
    _budget_sections,
)

# Patch targets — functions imported locally inside each cascade function
_DB = "reading_app.db"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_log():
    log = MagicMock()
    log.bind.return_value = log
    return log


def _mock_conn_with_rows(rows):
    """Create a mock get_conn context manager returning given rows."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows
    mock_cursor.fetchone.return_value = rows[0] if rows else None

    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)

    return mock_conn


# ---------------------------------------------------------------------------
# Command parser tests
# ---------------------------------------------------------------------------

class TestParseCommand:
    def test_basic_parse(self):
        etype, eid, steelman = _parse_command("/challenge bottleneck bn_123")
        assert etype == "bottleneck"
        assert eid == "bn_123"
        assert steelman is False

    def test_steelman_mode(self):
        etype, eid, steelman = _parse_command("/challenge belief bel_1 steelman")
        assert etype == "belief"
        assert eid == "bel_1"
        assert steelman is True

    def test_missing_id(self):
        etype, eid, steelman = _parse_command("/challenge capability")
        assert etype == "capability"
        assert eid == ""
        assert steelman is False

    def test_empty_input(self):
        etype, eid, steelman = _parse_command("")
        assert steelman is False


# ---------------------------------------------------------------------------
# Budget sections tests
# ---------------------------------------------------------------------------

class TestBudgetSections:
    def test_all_fit(self):
        sections = [(10, "a", "short"), (5, "b", "text")]
        result = _budget_sections(sections, 1000)
        assert result["a"] == "short"
        assert result["b"] == "text"

    def test_empty_sections(self):
        assert _budget_sections([], 1000) == {}

    def test_empty_text_filtered(self):
        sections = [(10, "a", "content"), (5, "b", ""), (3, "c", "   ")]
        result = _budget_sections(sections, 1000)
        assert "a" in result
        assert "b" not in result
        assert "c" not in result

    def test_truncation_respects_priority(self):
        sections = [
            (10, "high", "A" * 500),
            (1, "low", "B" * 500),
        ]
        result = _budget_sections(sections, 200)
        assert len(result["high"]) > len(result["low"])


# ---------------------------------------------------------------------------
# _check_beliefs_for_landscape_entity
# ---------------------------------------------------------------------------

class TestCheckBeliefsForLandscapeEntity:
    @patch(f"{_DB}.get_beliefs_for_theme")
    def test_finds_linked_beliefs(self, mock_get_beliefs):
        mock_get_beliefs.return_value = [
            {"id": "bel_1", "claim": "LLMs can reason about math problems"},
            {"id": "bel_2", "claim": "Scaling improves reasoning"},
        ]
        entity = {"theme_id": "reasoning"}
        warnings = _check_beliefs_for_landscape_entity(
            "capability", "cap_1", entity, {"confidence": 0.9}, _make_log()
        )
        assert len(warnings) == 2
        assert "bel_1" in warnings[0]
        assert "bel_2" in warnings[1]
        assert "may need review" in warnings[0]

    @patch(f"{_DB}.get_beliefs_for_theme")
    def test_no_theme_returns_empty(self, mock_get_beliefs):
        entity = {}  # no theme_id
        warnings = _check_beliefs_for_landscape_entity(
            "capability", "cap_1", entity, {}, _make_log()
        )
        assert warnings == []
        mock_get_beliefs.assert_not_called()

    @patch(f"{_DB}.get_beliefs_for_theme")
    def test_no_linked_beliefs_returns_empty(self, mock_get_beliefs):
        mock_get_beliefs.return_value = []
        entity = {"theme_id": "reasoning"}
        warnings = _check_beliefs_for_landscape_entity(
            "capability", "cap_1", entity, {}, _make_log()
        )
        assert warnings == []

    @patch(f"{_DB}.get_beliefs_for_theme")
    def test_db_error_returns_empty(self, mock_get_beliefs):
        mock_get_beliefs.side_effect = Exception("connection lost")
        entity = {"theme_id": "reasoning"}
        warnings = _check_beliefs_for_landscape_entity(
            "capability", "cap_1", entity, {}, _make_log()
        )
        assert warnings == []


# ---------------------------------------------------------------------------
# _check_stale_implications
# ---------------------------------------------------------------------------

class TestCheckStaleImplications:
    @patch(f"{_DB}.get_conn")
    def test_finds_stale_implications(self, mock_get_conn):
        rows = [
            {
                "id": "impl_1",
                "implication": "Progress in reasoning affects tool-use capabilities",
                "confidence": 0.7,
                "source_theme": "Reasoning",
                "target_theme": "Tool Use",
                "created_at": "2025-01-01",
            },
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "reasoning"}
        warnings = _check_stale_implications(
            "capability", "cap_1", entity, _make_log()
        )
        assert len(warnings) == 1
        assert "impl_1" in warnings[0]
        assert "Reasoning" in warnings[0]
        assert "Tool Use" in warnings[0]
        assert "may be stale" in warnings[0]

    @patch(f"{_DB}.get_conn")
    def test_no_theme_returns_empty(self, mock_get_conn):
        entity = {}  # no theme_id
        warnings = _check_stale_implications(
            "capability", "cap_1", entity, _make_log()
        )
        assert warnings == []
        mock_get_conn.assert_not_called()

    @patch(f"{_DB}.get_conn")
    def test_no_implications_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value = _mock_conn_with_rows([])
        entity = {"theme_id": "reasoning"}
        warnings = _check_stale_implications(
            "capability", "cap_1", entity, _make_log()
        )
        assert warnings == []

    @patch(f"{_DB}.get_conn")
    def test_capped_at_five(self, mock_get_conn):
        rows = [
            {
                "id": f"impl_{i}",
                "implication": f"Implication {i}",
                "confidence": 0.5,
                "source_theme": "A",
                "target_theme": "B",
                "created_at": "2025-01-01",
            }
            for i in range(10)
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "reasoning"}
        warnings = _check_stale_implications(
            "capability", "cap_1", entity, _make_log()
        )
        assert len(warnings) <= 5

    @patch(f"{_DB}.get_conn")
    def test_db_error_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value.__enter__ = MagicMock(
            side_effect=Exception("connection lost")
        )
        entity = {"theme_id": "reasoning"}
        warnings = _check_stale_implications(
            "capability", "cap_1", entity, _make_log()
        )
        assert warnings == []


# ---------------------------------------------------------------------------
# _cascade_to_anticipations
# ---------------------------------------------------------------------------

class TestCascadeToAnticipations:
    @patch(f"{_DB}.insert_landscape_history")
    @patch(f"{_DB}.get_conn")
    def test_finds_open_anticipations(self, mock_get_conn, mock_insert_history):
        rows = [
            {
                "id": "ant_1",
                "prediction": "GPT-5 will pass ARC-AGI",
                "confidence": 0.6,
                "timeline": "2026",
                "status": "open",
            },
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "scaling"}
        changes = {"confidence": 0.9}
        warnings = _cascade_to_anticipations(
            "capability", "cap_1", entity, changes, _make_log()
        )
        assert len(warnings) == 1
        assert "ant_1" in warnings[0]
        assert "GPT-5 will pass ARC" in warnings[0]
        assert "may need re-evaluation" in warnings[0]
        mock_insert_history.assert_called_once()

    @patch(f"{_DB}.get_conn")
    def test_no_theme_returns_empty(self, mock_get_conn):
        entity = {}
        warnings = _cascade_to_anticipations(
            "capability", "cap_1", entity, {}, _make_log()
        )
        assert warnings == []
        mock_get_conn.assert_not_called()

    @patch(f"{_DB}.get_conn")
    def test_no_open_anticipations_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value = _mock_conn_with_rows([])
        entity = {"theme_id": "scaling"}
        warnings = _cascade_to_anticipations(
            "capability", "cap_1", entity, {"confidence": 0.9}, _make_log()
        )
        assert warnings == []

    @patch(f"{_DB}.insert_landscape_history")
    @patch(f"{_DB}.get_conn")
    def test_capped_at_five(self, mock_get_conn, mock_insert_history):
        rows = [
            {
                "id": f"ant_{i}",
                "prediction": f"Prediction {i}",
                "confidence": 0.5,
                "timeline": "2026",
                "status": "open",
            }
            for i in range(10)
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "scaling"}
        warnings = _cascade_to_anticipations(
            "capability", "cap_1", entity, {"confidence": 0.9}, _make_log()
        )
        assert len(warnings) <= 5

    @patch(f"{_DB}.get_conn")
    def test_db_error_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value.__enter__ = MagicMock(
            side_effect=Exception("connection lost")
        )
        entity = {"theme_id": "scaling"}
        warnings = _cascade_to_anticipations(
            "capability", "cap_1", entity, {}, _make_log()
        )
        assert warnings == []


# ---------------------------------------------------------------------------
# _cascade_to_dependent_bottlenecks
# ---------------------------------------------------------------------------

class TestCascadeToDependentBottlenecks:
    @patch(f"{_DB}.insert_landscape_history")
    @patch(f"{_DB}.get_conn")
    def test_finds_dependent_bottlenecks(self, mock_get_conn, mock_insert_history):
        rows = [
            {
                "id": "bn_2",
                "description": "Compute cost limits training",
                "resolution_horizon": "1-2_years",
                "confidence": 0.7,
                "blocking_what": "large-scale deployment",
            },
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "scaling", "description": "Data bottleneck"}
        changes = {"resolution_horizon": "months"}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert len(warnings) == 1
        assert "bn_2" in warnings[0]
        assert "Compute cost" in warnings[0]
        assert "review for cascade" in warnings[0]
        mock_insert_history.assert_called_once()

    def test_no_relevant_changes_returns_empty(self):
        """Only cascades when resolution_horizon or confidence changed."""
        entity = {"theme_id": "scaling"}
        changes = {"description": "Updated text"}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert warnings == []

    @patch(f"{_DB}.get_conn")
    def test_no_theme_returns_empty(self, mock_get_conn):
        entity = {}  # no theme_id
        changes = {"confidence": 0.9}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert warnings == []
        mock_get_conn.assert_not_called()

    @patch(f"{_DB}.get_conn")
    def test_no_related_bottlenecks_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value = _mock_conn_with_rows([])
        entity = {"theme_id": "scaling"}
        changes = {"confidence": 0.8}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert warnings == []

    @patch(f"{_DB}.insert_landscape_history")
    @patch(f"{_DB}.get_conn")
    def test_capped_at_five(self, mock_get_conn, mock_insert_history):
        rows = [
            {
                "id": f"bn_{i}",
                "description": f"Bottleneck {i}",
                "resolution_horizon": "3-5_years",
                "confidence": 0.5,
                "blocking_what": "something",
            }
            for i in range(10)
        ]
        mock_get_conn.return_value = _mock_conn_with_rows(rows)
        entity = {"theme_id": "scaling"}
        changes = {"confidence": 0.9}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert len(warnings) <= 5

    @patch(f"{_DB}.get_conn")
    def test_db_error_returns_empty(self, mock_get_conn):
        mock_get_conn.return_value.__enter__ = MagicMock(
            side_effect=Exception("connection lost")
        )
        entity = {"theme_id": "scaling"}
        changes = {"resolution_horizon": "months"}
        warnings = _cascade_to_dependent_bottlenecks(
            "bn_1", entity, changes, _make_log()
        )
        assert warnings == []
