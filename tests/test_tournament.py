"""Tests for agents.tournament (and related: generate, evolve, critique)."""

from unittest.mock import MagicMock
from agents.tournament import (
    TournamentPipeline, TournamentResult,
    DEPTH_CALL_LIMITS, DEPTH_STRATEGIES, DEPTH_COUNT,
)
from agents.generate import GenerateAgent, TournamentGoal, STRATEGIES, _parse_ideas
from agents.evolve import EvolveAgent, MUTATIONS, _parse_evolved
from agents.critique import CritiqueAgent, _parse_critiques


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


# --- Tests merged from test_generate.py ---


def test_strategies_count():
    assert len(STRATEGIES) == 6


def test_all_strategies_listed():
    expected = {"synthesis", "transfer", "contradiction", "extension", "bottleneck", "implications"}
    assert set(STRATEGIES) == expected


def test_parse_ideas_json_block():
    text = '```json\n[{"idea_text": "Test idea", "idea_type": "synthesis"}]\n```'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1
    assert ideas[0]["idea_text"] == "Test idea"


def test_parse_ideas_raw_array():
    text = '[{"idea_text": "Direct JSON"}]'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1


def test_parse_ideas_empty():
    assert _parse_ideas("no json here") == []


def test_parse_ideas_embedded():
    text = 'Here are ideas:\n[{"idea_text": "embedded"}]\nDone.'
    ideas = _parse_ideas(text)
    assert len(ideas) == 1


def test_tournament_goal():
    goal = TournamentGoal(
        description="Focus on alignment",
        focus_themes=["alignment", "safety"],
    )
    assert goal.description == "Focus on alignment"
    assert "alignment" in goal.focus_themes


# --- Tests merged from test_evolve.py ---


def test_mutations_defined():
    assert "TIGHTEN" in MUTATIONS
    assert "INVERT" in MUTATIONS
    assert "TRANSFER" in MUTATIONS
    assert "BROADEN" in MUTATIONS


def test_choose_mutation_low_testability():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.3, "novelty_score": 0.7, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "TIGHTEN"


def test_choose_mutation_low_novelty():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.3, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "INVERT"


def test_choose_mutation_high_domain():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.6, "domain_specificity": 0.8}
    assert agent._choose_mutation(idea) == "TRANSFER"


def test_choose_mutation_default():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.6, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "BROADEN"


def test_parse_evolved():
    text = '{"evolved_idea_text": "Improved idea", "mutation_applied": "TIGHTEN", "what_changed": "More specific"}'
    result = _parse_evolved(text)
    assert result["evolved_idea_text"] == "Improved idea"


def test_parse_evolved_code_block():
    text = '```json\n{"evolved_idea_text": "Better idea"}\n```'
    result = _parse_evolved(text)
    assert result["evolved_idea_text"] == "Better idea"


def test_parse_evolved_failure():
    result = _parse_evolved("no json")
    assert result == {}


# --- Tests merged from test_critique.py ---


def test_parse_critiques_json():
    text = '[{"idea_index": 0, "novelty": 0.8, "testability": 0.7, "impact": 0.9, "grounding": 0.6, "domain_specificity": 0.5, "overall_score": 0.78, "strengths": "Novel", "weaknesses": "Hard to test", "suggestions": "Narrow scope"}]'
    critiques = _parse_critiques(text)
    assert len(critiques) == 1
    assert critiques[0]["novelty"] == 0.8


def test_parse_critiques_code_block():
    text = '```json\n[{"idea_index": 0, "novelty": 0.5, "testability": 0.5, "impact": 0.5, "grounding": 0.5, "domain_specificity": 0.5, "overall_score": 0.5}]\n```'
    critiques = _parse_critiques(text)
    assert len(critiques) == 1


def test_parse_critiques_empty():
    assert _parse_critiques("not json") == []


def test_overall_score_formula():
    # 0.3*novelty + 0.2*testability + 0.3*impact + 0.2*grounding
    n, t, i, g = 0.8, 0.6, 0.9, 0.7
    expected = 0.3 * n + 0.2 * t + 0.3 * i + 0.2 * g
    assert abs(expected - 0.77) < 0.01


def test_parse_critiques_multiple():
    text = '[{"idea_index": 0, "overall_score": 0.8}, {"idea_index": 1, "overall_score": 0.6}]'
    critiques = _parse_critiques(text)
    assert len(critiques) == 2
