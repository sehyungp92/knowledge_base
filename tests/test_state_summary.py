"""Tests for retrieval.state_summary."""

import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from retrieval.state_summary import (
    should_regenerate,
    generate_theme_state_summary,
    _score_summary,
    _validate_summary_quality,
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


def test_should_regenerate_source_count_staleness():
    """Fresh summary should regenerate if >= 5 new sources arrived since last update."""
    now = datetime.now(timezone.utc)
    theme = {
        "id": "test_theme",
        "state_summary": "existing summary",
        "state_summary_updated_at": now,  # fresh (not age-stale)
        "velocity": 0.5,
    }
    # Mock db.get_conn to return 5 new sources
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.execute.return_value.fetchone.return_value = {"c": 5}

    with patch("retrieval.state_summary.db") as mock_db:
        mock_db.get_conn.return_value = mock_conn
        assert should_regenerate(theme, source_count=10) is True


def test_should_regenerate_few_new_sources_stays_fresh():
    """Fresh summary with < 5 new sources should NOT regenerate."""
    now = datetime.now(timezone.utc)
    theme = {
        "id": "test_theme",
        "state_summary": "existing summary",
        "state_summary_updated_at": now,
        "velocity": 0.5,
    }
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    mock_conn.execute.return_value.fetchone.return_value = {"c": 2}

    with patch("retrieval.state_summary.db") as mock_db:
        mock_db.get_conn.return_value = mock_conn
        assert should_regenerate(theme, source_count=10) is False


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
        mock_db.get_landscape_history_for_theme.return_value = []

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
        mock_db.get_landscape_history_for_theme.return_value = []

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
        mock_db.get_landscape_history_for_theme.return_value = []

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
        mock_db.get_landscape_history_for_theme.return_value = []

        generate_theme_state_summary("robotics", executor=mock_executor)
        # The two-phase architecture makes multiple run_raw calls
        # (analysis, synthesis, quality check). The old summary should
        # appear in at least one of the prompts (analysis and synthesis).
        all_prompts = [
            call[0][0] for call in mock_executor.run_raw.call_args_list
        ]
        assert any(
            "Old summary about perception." in p for p in all_prompts
        ), "Previous summary not found in any prompt sent to executor"


# --- _score_summary ---

def test_score_summary_parses_scores():
    """_score_summary returns avg score when LLM returns valid score lines."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="TEMPORAL_LANGUAGE: 4\nSPECIFICITY: 3\nNARRATIVE_FLOW: 5"
    )
    score = _score_summary("some summary", "Robotics", "robotics", mock_executor)
    assert score == 4.0


def test_score_summary_returns_none_on_incomplete_parse():
    """_score_summary returns None when LLM output can't be parsed."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="This is not a valid score output"
    )
    score = _score_summary("some summary", "Robotics", "robotics", mock_executor)
    assert score is None


def test_score_summary_returns_none_on_exception():
    """_score_summary returns None when executor raises."""
    mock_executor = MagicMock()
    mock_executor.run_raw.side_effect = RuntimeError("LLM down")
    score = _score_summary("some summary", "Robotics", "robotics", mock_executor)
    assert score is None


def test_score_summary_with_entity_names():
    """_score_summary passes ground truth entities to prompt."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="TEMPORAL_LANGUAGE: 3\nSPECIFICITY: 4\nNARRATIVE_FLOW: 3"
    )
    entities = ["dexterous manipulation", "sim-to-real gap"]
    score = _score_summary("summary", "Robotics", "robotics", mock_executor, entity_names=entities)
    assert score is not None
    # Verify ground truth was included in the prompt
    prompt_sent = mock_executor.run_raw.call_args[0][0]
    assert "Ground Truth Entities" in prompt_sent
    assert "dexterous manipulation" in prompt_sent


# --- _validate_summary_quality ---

def test_validate_returns_three_tuple():
    """_validate_summary_quality returns (passes, feedback, score)."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="TEMPORAL_LANGUAGE: 4\nSPECIFICITY: 4\nNARRATIVE_FLOW: 4"
    )
    passes, feedback, score = _validate_summary_quality(
        "good summary", "Robotics", "robotics", mock_executor
    )
    assert passes is True
    assert feedback == ""
    assert score == 4.0


def test_validate_fails_on_low_scores():
    """_validate_summary_quality fails and returns feedback for low scores."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text="TEMPORAL_LANGUAGE: 2\nSPECIFICITY: 2\nNARRATIVE_FLOW: 2"
    )
    passes, feedback, score = _validate_summary_quality(
        "bad summary", "Robotics", "robotics", mock_executor
    )
    assert passes is False
    assert "2.0" in feedback
    assert score == 2.0


def test_validate_accepts_on_parse_failure():
    """_validate_summary_quality accepts when scoring fails."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(text="unparseable")
    passes, feedback, score = _validate_summary_quality(
        "summary", "Robotics", "robotics", mock_executor
    )
    assert passes is True
    assert score is None


# --- Quality gate re-scoring ---

def test_quality_gate_rescores_retry_and_picks_better():
    """When quality gate fails, retry is re-scored and accepted only if better."""
    mock_executor = MagicMock()

    # Call sequence: analysis (haiku), synthesis (sonnet), quality check (haiku),
    # retry synthesis (sonnet), re-score (haiku)
    call_count = {"n": 0}
    def side_effect(*args, **kwargs):
        call_count["n"] += 1
        n = call_count["n"]
        if n == 1:
            # Phase 1 analysis
            return MagicMock(text="KEY MOVEMENTS: shift detected")
        elif n == 2:
            # Phase 2 synthesis — produces summary
            return MagicMock(text="Original summary that is long enough to pass length check but not quality gate.")
        elif n == 3:
            # Quality check — fails (avg 2.0)
            return MagicMock(text="TEMPORAL_LANGUAGE: 2\nSPECIFICITY: 2\nNARRATIVE_FLOW: 2")
        elif n == 4:
            # Retry synthesis
            return MagicMock(text="Improved summary with trajectory language about shifting bottlenecks and momentum.")
        elif n == 5:
            # Re-score retry — passes (avg 4.0)
            return MagicMock(text="TEMPORAL_LANGUAGE: 4\nSPECIFICITY: 4\nNARRATIVE_FLOW: 4")
        return MagicMock(text="fallback")

    mock_executor.run_raw.side_effect = side_effect

    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db, \
         patch("retrieval.state_summary.get_consolidated_implications") as mock_impl:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": None},
            "capabilities": [{"description": "manipulation", "maturity": "demo"}],
            "limitations": [{"description": "sim gap", "severity": "high", "limitation_type": "eng", "trajectory": "stable"}],
            "bottlenecks": [],
            "breakthroughs": [],
            "anticipations": [],
            "cross_theme_implications": [],
        }
        mock_db.get_landscape_history_for_theme.return_value = []
        mock_impl.return_value = []

        result = generate_theme_state_summary("robotics", executor=mock_executor)
        assert result is not None
        # Should use the retry (improved) summary
        assert "Improved summary" in result
        mock_db.update_theme_state_summary.assert_called_once()


def test_quality_gate_keeps_original_when_retry_worse():
    """When retry scores worse than original, keep original."""
    mock_executor = MagicMock()

    call_count = {"n": 0}
    def side_effect(*args, **kwargs):
        call_count["n"] += 1
        n = call_count["n"]
        if n == 1:
            return MagicMock(text="KEY MOVEMENTS: analysis")
        elif n == 2:
            return MagicMock(text="Original summary with decent content that should be kept over worse retry.")
        elif n == 3:
            # Quality check — fails (avg 2.7)
            return MagicMock(text="TEMPORAL_LANGUAGE: 2\nSPECIFICITY: 3\nNARRATIVE_FLOW: 3")
        elif n == 4:
            return MagicMock(text="Worse retry summary that somehow degraded in quality compared to original.")
        elif n == 5:
            # Re-score retry — also fails, lower (avg 2.0)
            return MagicMock(text="TEMPORAL_LANGUAGE: 2\nSPECIFICITY: 2\nNARRATIVE_FLOW: 2")
        return MagicMock(text="fallback")

    mock_executor.run_raw.side_effect = side_effect

    with patch("retrieval.state_summary.get_theme_state") as mock_state, \
         patch("retrieval.state_summary.db") as mock_db, \
         patch("retrieval.state_summary.get_consolidated_implications") as mock_impl:
        mock_state.return_value = {
            "theme": {"id": "robotics", "name": "Robotics", "state_summary": None},
            "capabilities": [], "limitations": [], "bottlenecks": [],
            "breakthroughs": [], "anticipations": [], "cross_theme_implications": [],
        }
        mock_db.get_landscape_history_for_theme.return_value = []
        mock_impl.return_value = []

        result = generate_theme_state_summary("robotics", executor=mock_executor)
        assert result is not None
        # Should keep the original
        assert "Original summary" in result
