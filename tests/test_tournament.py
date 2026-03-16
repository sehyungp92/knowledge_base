"""Tests for agents.tournament."""

from unittest.mock import MagicMock
from agents.tournament import (
    TournamentPipeline, TournamentResult,
    DEPTH_CALL_LIMITS, DEPTH_STRATEGIES, DEPTH_COUNT,
)
from agents.generate import TournamentGoal


def test_depth_call_limits():
    assert DEPTH_CALL_LIMITS["quick"] < DEPTH_CALL_LIMITS["normal"]
    assert DEPTH_CALL_LIMITS["normal"] < DEPTH_CALL_LIMITS["deep"]
    assert DEPTH_CALL_LIMITS["deep"] < DEPTH_CALL_LIMITS["research"]


def test_depth_strategies():
    assert DEPTH_STRATEGIES["quick"] <= DEPTH_STRATEGIES["normal"]


def test_tournament_result():
    result = TournamentResult()
    assert result.ideas == []
    assert result.total_calls == 0
    assert result.steps_completed == 0
    assert result.call_limit_hit is False


def test_mmr_dedup():
    executor = MagicMock()
    pipeline = TournamentPipeline(executor)
    ideas = [
        {"idea_text": "Idea about RLHF safety", "overall_score": 0.9},
        {"idea_text": "Idea about RLHF safety improvements", "overall_score": 0.85},  # Similar
        {"idea_text": "Completely different NLP idea", "overall_score": 0.8},
    ]
    deduped = pipeline._mmr_dedup(ideas, lambda_param=0.5, k=2)
    assert len(deduped) == 2


def test_mmr_dedup_all_fit():
    executor = MagicMock()
    pipeline = TournamentPipeline(executor)
    ideas = [{"idea_text": "A", "overall_score": 0.9}]
    deduped = pipeline._mmr_dedup(ideas, k=5)
    assert len(deduped) == 1


def test_validate_grounding():
    executor = MagicMock()
    pipeline = TournamentPipeline(executor)
    ideas = [
        {"idea_text": "Grounded idea", "grounding": [{"source_id": "s1"}]},
        {"idea_text": "Ungrounded idea", "grounding": None},
    ]
    validated = pipeline._validate_grounding(ideas)
    assert len(validated) == 2  # Both kept, but ungrounded flagged


def test_build_reviews_overview():
    executor = MagicMock()
    pipeline = TournamentPipeline(executor)
    ideas = [
        {"overall_score": 0.8, "critique_strengths": "Novel approach",
         "critique_weaknesses": "Hard to test"},
    ]
    overview = pipeline._build_reviews_overview(ideas)
    assert "0.80" in overview
    assert "Novel" in overview


def test_tournament_goal():
    goal = TournamentGoal(
        description="Explore alignment techniques",
        focus_themes=["alignment", "safety"],
        preferences={"prefer_testable": True},
    )
    assert goal.description == "Explore alignment techniques"
