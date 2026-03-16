"""Tests for retrieval.state_summary."""

import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from retrieval.state_summary import (
    should_regenerate,
    generate_theme_state_summary,
    MIN_SOURCE_THRESHOLD,
    STALENESS_DAYS,
)


# --- should_regenerate ---

def test_should_regenerate_no_summary():
    theme = {"state_summary": None, "state_summary_updated_at": None, "velocity": 0.5}
    assert should_regenerate(theme, source_count=3) is True


def test_should_regenerate_too_few_sources():
    theme = {"state_summary": None, "state_summary_updated_at": None, "velocity": 0.5}
    assert should_regenerate(theme, source_count=2) is False


def test_should_regenerate_stale():
    old = datetime.now(timezone.utc) - timedelta(days=STALENESS_DAYS + 1)
    theme = {"state_summary": "old text", "state_summary_updated_at": old, "velocity": 0.5}
    assert should_regenerate(theme, source_count=5) is True


def test_should_regenerate_fresh():
    now = datetime.now(timezone.utc)
    theme = {"state_summary": "recent text", "state_summary_updated_at": now, "velocity": 0.5}
    assert should_regenerate(theme, source_count=5) is False


def test_should_regenerate_no_updated_at():
    theme = {"state_summary": "has text but no date", "state_summary_updated_at": None, "velocity": 0.3}
    assert should_regenerate(theme, source_count=5) is True


def test_should_regenerate_string_datetime():
    old = (datetime.now(timezone.utc) - timedelta(days=STALENESS_DAYS + 1)).isoformat()
    theme = {"state_summary": "old text", "state_summary_updated_at": old, "velocity": 0.5}
    assert should_regenerate(theme, source_count=5) is True


def test_should_regenerate_naive_datetime():
    """Naive datetime (no tzinfo) should still be handled."""
    old = datetime.now() - timedelta(days=STALENESS_DAYS + 1)
    theme = {"state_summary": "old text", "state_summary_updated_at": old, "velocity": 0.5}
    assert should_regenerate(theme, source_count=5) is True


def test_should_regenerate_exactly_at_threshold():
    """At exactly MIN_SOURCE_THRESHOLD, should proceed."""
    theme = {"state_summary": None, "state_summary_updated_at": None, "velocity": 0.1}
    assert should_regenerate(theme, source_count=MIN_SOURCE_THRESHOLD) is True


# --- generate_theme_state_summary ---

def test_generate_returns_summary():
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="Robotics shifted from perception bottleneck to sim-to-real. Momentum building in world model integration."
    )
    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": None},
            "capabilities": [{"description": "dexterous manipulation", "maturity": "demo"}],
            "limitations": [{"description": "sim-to-real gap", "severity": "blocking", "limitation_type": "engineering", "trajectory": "improving"}],
            "bottlenecks": [{"description": "sim-to-real transfer", "resolution_horizon": "1-2_years", "bottleneck_type": "engineering", "blocking_what": "deployment"}],
            "breakthroughs": [],
            "anticipations": [],
            "cross_theme_implications": [],
        }
        mock_db.get_landscape_history.return_value = []

        result = generate_theme_state_summary("robotics", executor=mock_executor)
        assert result is not None
        assert "Robotics" in result or "robotics" in result.lower()
        mock_db.update_theme_state_summary.assert_called_once_with("robotics", result)


def test_generate_returns_none_for_unknown_theme():
    with patch("retrieval.state_summary.get_theme_state") as mock_state:
        mock_state.return_value = {"theme": None}
        result = generate_theme_state_summary("nonexistent")
        assert result is None


def test_generate_returns_none_for_short_summary():
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(text="Too short")
    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": None},
            "capabilities": [], "limitations": [], "bottlenecks": [],
            "breakthroughs": [], "anticipations": [], "cross_theme_implications": [],
        }
        mock_db.get_landscape_history.return_value = []

        result = generate_theme_state_summary("robotics", executor=mock_executor)
        assert result is None
        mock_db.update_theme_state_summary.assert_not_called()


def test_generate_handles_executor_failure():
    mock_executor = MagicMock()
    mock_executor.run_raw.side_effect = RuntimeError("LLM down")
    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": None},
            "capabilities": [], "limitations": [], "bottlenecks": [],
            "breakthroughs": [], "anticipations": [], "cross_theme_implications": [],
        }
        mock_db.get_landscape_history.return_value = []

        result = generate_theme_state_summary("robotics", executor=mock_executor)
        assert result is None


def test_generate_includes_previous_summary_in_prompt():
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="Updated narrative about robotics progress with new breakthroughs in manipulation."
    )
    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": "Old summary about perception."},
            "capabilities": [{"description": "grasping", "maturity": "narrow_production"}],
            "limitations": [], "bottlenecks": [], "breakthroughs": [],
            "anticipations": [], "cross_theme_implications": [],
        }
        mock_db.get_landscape_history.return_value = []

        generate_theme_state_summary("robotics", executor=mock_executor)
        # Check that the prompt sent to executor includes the old summary
        prompt_sent = mock_executor.run_raw.call_args[0][0]
        assert "Old summary about perception." in prompt_sent
