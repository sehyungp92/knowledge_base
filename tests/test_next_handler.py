"""Tests for the /next reading queue handler.

Tests the 6 gap signal sources, priority scoring, deduplication,
focus-theme filtering, command parsing, and graceful degradation.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from gateway.next_handler import (
    _parse_command,
    _generate_reading_queue,
    _horizon_priority,
    _bottleneck_to_search,
    _belief_to_search,
    _anticipation_to_search,
    _format_queue,
    handle_next_job,
)
from gateway.models import Event, Job


# Patch targets — these are imported locally inside _generate_reading_queue
_RL = "retrieval.landscape"
_PERSIST = "gateway.next_handler._persist_queue"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_log():
    log = MagicMock()
    log.bind.return_value = log
    return log


def _make_executor(narrative_response=None):
    """Create mock executor that returns search refinement JSON."""
    executor = MagicMock()
    if narrative_response is None:
        narrative_response = json.dumps([
            {
                "index": 1,
                "narrative": "This matters because...",
                "temporal_urgency": "accelerating",
                "queries": ["test query 1"],
            }
        ])
    executor.run_raw.return_value = MagicMock(
        text=f"```json\n{narrative_response}\n```"
    )
    return executor


@pytest.fixture
def mocks():
    """Patch all 6 retrieval functions + _persist_queue with empty defaults.

    Returns a dict keyed by short name — override .return_value or
    .side_effect in individual tests as needed.
    """
    with patch(f"{_RL}.get_blind_spot_bottlenecks", return_value=[]) as m_blind, \
         patch(f"{_RL}.get_validation_backlog", return_value=[]) as m_backlog, \
         patch(f"{_RL}.get_belief_coverage_gaps", return_value={"low_confidence_gaps": []}) as m_belief, \
         patch(f"{_RL}.get_bottleneck_ranking", return_value=[]) as m_ranking, \
         patch(f"{_RL}.get_theme_source_counts", return_value=[]) as m_counts, \
         patch(f"{_RL}.get_untested_anticipations", return_value=[]) as m_untested, \
         patch(_PERSIST) as m_persist:
        yield {
            "blind_spots": m_blind,
            "backlog": m_backlog,
            "belief_gaps": m_belief,
            "ranking": m_ranking,
            "counts": m_counts,
            "untested": m_untested,
            "persist": m_persist,
        }


# ---------------------------------------------------------------------------
# Command parser tests
# ---------------------------------------------------------------------------

class TestParseCommand:
    def test_default_count(self):
        count, theme = _parse_command("/next")
        assert count == 5
        assert theme is None

    def test_custom_count(self):
        count, theme = _parse_command("/next 3")
        assert count == 3
        assert theme is None

    def test_count_with_theme(self):
        count, theme = _parse_command("/next 7 robotics")
        assert count == 7
        assert theme == "robotics"

    def test_theme_without_count(self):
        count, theme = _parse_command("/next robotics")
        assert count == 5
        assert theme == "robotics"

    def test_count_clamped_high(self):
        count, _ = _parse_command("/next 100")
        assert count == 15

    def test_count_clamped_low(self):
        count, _ = _parse_command("/next 0")
        assert count == 1

    def test_empty_input(self):
        count, theme = _parse_command("")
        assert count == 5
        assert theme is None


# ---------------------------------------------------------------------------
# Priority scoring tests
# ---------------------------------------------------------------------------

class TestHorizonPriority:
    def test_months_highest(self):
        assert _horizon_priority("months") == 5.0

    def test_1_2_years(self):
        assert _horizon_priority("1-2_years") == 4.0

    def test_3_5_years(self):
        assert _horizon_priority("3-5_years") == 3.0

    def test_5_plus_years(self):
        assert _horizon_priority("5+_years") == 2.0

    def test_possibly_fundamental(self):
        assert _horizon_priority("possibly_fundamental") == 1.5

    def test_unknown_defaults(self):
        assert _horizon_priority("unknown") == 2.0
        assert _horizon_priority("") == 2.0


# ---------------------------------------------------------------------------
# Search hint helpers
# ---------------------------------------------------------------------------

class TestSearchHints:
    def test_bottleneck_to_search(self):
        bn = {
            "description": "Insufficient training data",
            "theme_name": "Robotics",
            "blocking_what": "real-world deployment",
        }
        result = _bottleneck_to_search(bn)
        assert "Robotics" in result
        assert "Insufficient" in result
        assert "real-world" in result

    def test_bottleneck_to_search_no_blocking(self):
        bn = {"description": "Test", "theme_name": "AI"}
        result = _bottleneck_to_search(bn)
        assert "AI" in result
        assert "Test" in result

    def test_belief_to_search(self):
        bg = {"claim": "LLMs cannot reason", "theme_name": "Reasoning"}
        result = _belief_to_search(bg)
        assert "Reasoning" in result
        assert "LLMs cannot reason" in result
        assert "evidence" in result

    def test_anticipation_to_search(self):
        ant = {"prediction": "GPT-5 will pass ARC", "theme_name": "Scaling"}
        result = _anticipation_to_search(ant)
        assert "Scaling" in result
        assert "GPT-5 will pass ARC" in result


# ---------------------------------------------------------------------------
# Signal collection and ranking (mocked retrieval functions)
# ---------------------------------------------------------------------------

class TestGenerateReadingQueue:
    """Test _generate_reading_queue with mocked retrieval functions."""

    def test_empty_db_returns_no_recommendations(self, mocks):
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "No reading recommendations" in result

    def test_blind_spot_signal(self, mocks):
        mocks["blind_spots"].return_value = [
            {
                "theme_id": "t1",
                "theme_name": "Robotics",
                "description": "No sim-to-real approaches",
                "confidence": 0.8,
                "resolution_horizon": "months",
            }
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Robotics" in result
        assert "No sim-to-real" in result

    def test_validation_backlog_signal(self, mocks):
        mocks["backlog"].return_value = [
            {
                "theme_id": "t1",
                "theme_name": "Safety",
                "unvalidated_count": 12,
            }
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Safety" in result
        assert "12 unvalidated" in result

    def test_belief_gap_signal(self, mocks):
        mocks["belief_gaps"].return_value = {
            "low_confidence_gaps": [
                {
                    "domain_theme_id": "t1",
                    "theme_name": "Scaling",
                    "claim": "Scaling laws hold for reasoning",
                    "confidence": 0.3,
                }
            ]
        }
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Scaling" in result
        assert "Low-confidence belief" in result

    def test_untested_anticipation_signal(self, mocks):
        mocks["untested"].return_value = [
            {
                "theme_id": "t1",
                "theme_name": "Alignment",
                "prediction": "RLHF will plateau by 2026",
                "age_days": 90,
            }
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Alignment" in result
        assert "RLHF will plateau" in result

    def test_low_coverage_theme_signal(self, mocks):
        mocks["counts"].return_value = [
            {"id": "t_new", "name": "Embodied AI", "source_count": 1, "velocity": 0.8}
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Embodied AI" in result
        assert "1 sources" in result

    def test_focus_theme_filters(self, mocks):
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "Robotics", "description": "A",
             "confidence": 0.8, "resolution_horizon": "months"},
            {"theme_id": "t2", "theme_name": "NLP", "description": "B",
             "confidence": 0.7, "resolution_horizon": "months"},
        ]
        result = _generate_reading_queue(5, "robotics", None, None, _make_log())
        assert "Robotics" in result
        assert "NLP" not in result


class TestDeduplication:
    """Signals with the same description[:80] should be deduplicated."""

    def test_duplicate_descriptions_collapsed(self, mocks):
        shared_desc = "Same bottleneck description"
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "X", "description": shared_desc,
             "confidence": 0.8, "resolution_horizon": "months"},
        ]
        mocks["ranking"].return_value = [
            {"theme_id": "t1", "theme_name": "X", "description": shared_desc,
             "confidence": 0.9, "horizon_score": 5},
        ]
        result = _generate_reading_queue(10, None, None, None, _make_log())
        assert result.count(f"**Gap:** {shared_desc}") == 1


class TestPriorityOrdering:
    """Signals should be sorted by priority descending."""

    def test_higher_priority_first(self, mocks):
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "High Priority",
             "description": "Urgent bottleneck", "confidence": 0.9,
             "resolution_horizon": "months"},
        ]
        mocks["backlog"].return_value = [
            {"theme_id": "t2", "theme_name": "Low Priority",
             "unvalidated_count": 2},
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert result.index("High Priority") < result.index("Low Priority")


class TestSignalDiversity:
    """No single signal type should monopolize all slots."""

    def test_diverse_types_when_available(self, mocks):
        """With 4 blind spots and 2 backlog items, requesting 5 should include both types."""
        mocks["blind_spots"].return_value = [
            {"theme_id": f"t{i}", "theme_name": f"Blind {i}",
             "description": f"Bottleneck {i}", "confidence": 0.9,
             "resolution_horizon": "months"}
            for i in range(4)
        ]
        mocks["backlog"].return_value = [
            {"theme_id": "t10", "theme_name": "Backlog Theme",
             "unvalidated_count": 15},
            {"theme_id": "t11", "theme_name": "Backlog Theme 2",
             "unvalidated_count": 10},
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Backlog Theme" in result
        assert "unvalidated" in result

    def test_cap_allows_backfill(self, mocks):
        """When only one signal type exists, it can still fill all slots."""
        mocks["blind_spots"].return_value = [
            {"theme_id": f"t{i}", "theme_name": f"Only Blind {i}",
             "description": f"Bottleneck {i}", "confidence": 0.8,
             "resolution_horizon": "1-2_years"}
            for i in range(10)
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Only Blind 0" in result
        assert "Only Blind 4" in result

    def test_three_types_all_represented(self, mocks):
        """With 3 signal types, all should appear in results."""
        mocks["blind_spots"].return_value = [
            {"theme_id": f"t{i}", "theme_name": f"Blind {i}",
             "description": f"Bottleneck {i}", "confidence": 0.9,
             "resolution_horizon": "months"}
            for i in range(5)
        ]
        mocks["backlog"].return_value = [
            {"theme_id": "t10", "theme_name": "Validation Theme",
             "unvalidated_count": 15},
        ]
        mocks["belief_gaps"].return_value = {
            "low_confidence_gaps": [
                {"domain_theme_id": "t20", "theme_name": "Belief Theme",
                 "claim": "Some uncertain claim", "confidence": 0.2},
            ]
        }
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Blind" in result
        assert "Validation Theme" in result
        assert "Belief Theme" in result


class TestGracefulDegradation:
    """Individual signal source failures should not crash the handler."""

    def test_partial_failure_still_returns(self, mocks):
        for key in ("backlog", "belief_gaps", "ranking", "counts", "untested"):
            mocks[key].side_effect = Exception("DB down")
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "Surviving",
             "description": "Still works", "confidence": 0.5,
             "resolution_horizon": "months"},
        ]
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "Surviving" in result

    def test_total_failure_returns_no_recs(self, mocks):
        for key in ("blind_spots", "backlog", "belief_gaps", "ranking", "counts", "untested"):
            mocks[key].side_effect = Exception("DB down")
        result = _generate_reading_queue(5, None, None, None, _make_log())
        assert "No reading recommendations" in result


class TestLLMRefinement:
    """Test search term refinement via executor."""

    def test_executor_adds_narrative(self, mocks):
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "Robotics",
             "description": "Bottleneck X", "confidence": 0.8,
             "resolution_horizon": "months"},
        ]
        result = _generate_reading_queue(5, None, _make_executor(), None, _make_log())
        assert "This matters because" in result

    def test_executor_failure_still_formats(self, mocks):
        mocks["blind_spots"].return_value = [
            {"theme_id": "t1", "theme_name": "Robotics",
             "description": "Bottleneck X", "confidence": 0.8,
             "resolution_horizon": "months"},
        ]
        executor = MagicMock()
        executor.run_raw.side_effect = Exception("LLM timeout")
        result = _generate_reading_queue(5, None, executor, None, _make_log())
        assert "Robotics" in result


# ---------------------------------------------------------------------------
# Format output tests
# ---------------------------------------------------------------------------

class TestFormatQueue:
    def test_format_includes_type_icons(self):
        signals = [
            {"type": "blind_spot_bottleneck", "theme": "Robotics",
             "description": "No approaches", "reason": "Missing",
             "priority": 5.0},
        ]
        result = _format_queue(signals, 5, None)
        assert "Robotics" in result
        assert "Read Next" in result

    def test_format_with_narrative(self):
        signals = [
            {"type": "belief_gap", "theme": "Safety",
             "description": "Low confidence", "reason": "Needs evidence",
             "priority": 3.0, "narrative": "Critical gap because...",
             "temporal_urgency": "accelerating"},
        ]
        result = _format_queue(signals, 5, None)
        assert "Critical gap because" in result
        assert "accelerating" in result

    def test_format_with_search_queries(self):
        signals = [
            {"type": "untested_anticipation", "theme": "Scaling",
             "description": "Untested prediction", "reason": "Old",
             "priority": 2.0, "search_queries": ["scaling laws 2026"]},
        ]
        result = _format_queue(signals, 5, None)
        assert "scaling laws 2026" in result

    def test_format_with_focus_theme(self):
        signals = [
            {"type": "low_coverage_theme", "theme": "Robotics",
             "description": "Thin coverage", "reason": "Velocity mismatch",
             "priority": 2.0},
        ]
        result = _format_queue(signals, 5, "robotics")
        assert "for `robotics`" in result

    def test_signal_mix_summary(self):
        signals = [
            {"type": "blind_spot_bottleneck", "theme": "A",
             "description": "X", "reason": "Y", "priority": 5.0},
            {"type": "belief_gap", "theme": "B",
             "description": "Z", "reason": "W", "priority": 3.0},
        ]
        result = _format_queue(signals, 5, None)
        assert "Signal mix:" in result


# ---------------------------------------------------------------------------
# Handle job entry point
# ---------------------------------------------------------------------------

class TestHandleNextJob:
    def test_no_executor_returns_error(self):
        event = Event(
            type="command",
            payload={"text": "/next"},
            source="test",
        )
        job = Job(event_id=1, skill="next")
        result = handle_next_job(event, job, MagicMock(), None)
        assert "Error" in result
