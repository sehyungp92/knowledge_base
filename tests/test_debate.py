"""Tests for agents.debate."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from agents.debate import DebateAgent, _parse_debate_result, _parse_deep_debate


# ---------------------------------------------------------------------------
# Parsing tests
# ---------------------------------------------------------------------------

def test_parse_debate_result():
    text = '{"winner": "A", "reasoning": "Better grounded", "loser_weaknesses": "Too vague"}'
    result = _parse_debate_result(text)
    assert result["winner"] == "A"
    assert "grounded" in result["reasoning"]


def test_parse_debate_result_b_wins():
    text = 'After analysis:\n{"winner": "B", "reasoning": "More novel"}\n'
    result = _parse_debate_result(text)
    assert result["winner"] == "B"


def test_parse_debate_result_fallback_is_random():
    """Parse failure should produce random winner (no position bias)."""
    winners = {_parse_debate_result("unparseable")["winner"] for _ in range(50)}
    # With 50 tries, both A and B should appear (probability of all-same ≈ 2^-49)
    assert winners == {"A", "B"}


def test_parse_deep_debate():
    text = '{"discussion": "Panel agreed", "rankings": [{"idea_index": 0, "rank": 1}], "eliminated_indices": [2]}'
    result = _parse_deep_debate(text)
    assert len(result["rankings"]) == 1
    assert 2 in result["eliminated_indices"]


def test_parse_deep_debate_fallback():
    result = _parse_deep_debate("not json")
    assert result["rankings"] == []
    assert result["eliminated_indices"] == []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_idea(score=0.5, text="idea"):
    return {"idea_text": text, "overall_score": score}


def _make_agent(response_text: str) -> DebateAgent:
    """Create a DebateAgent with a mocked LLM returning given text."""
    agent = DebateAgent(MagicMock())
    agent._run = MagicMock(return_value=SimpleNamespace(text=response_text))
    return agent


# ---------------------------------------------------------------------------
# Pairwise debate scoring (exercises real DebateAgent.debate)
# ---------------------------------------------------------------------------

def test_pairwise_deltas_clamped():
    """Deltas outside ±0.1 should be clamped."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": 0.5, "loser_score_delta": -0.5}'
    )
    result = agent.debate(_make_idea(0.5, "A"), _make_idea(0.5, "B"))
    assert abs(result["winner"]["overall_score"] - 0.6) < 1e-9
    assert abs(result["loser"]["overall_score"] - 0.4) < 1e-9


def test_pairwise_score_bounded_at_one():
    """Score should not exceed 1.0 after winner delta."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": 0.1, "loser_score_delta": 0.0}'
    )
    result = agent.debate(_make_idea(0.98, "A"), _make_idea(0.5, "B"))
    assert result["winner"]["overall_score"] == 1.0


def test_pairwise_score_bounded_at_zero():
    """Score should not go below 0.0 after loser delta."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": 0.0, "loser_score_delta": -0.1}'
    )
    result = agent.debate(_make_idea(0.5, "A"), _make_idea(0.02, "B"))
    assert result["loser"]["overall_score"] == 0.0


def test_pairwise_pre_debate_score_preserved():
    """pre_debate_score should record the score before the first debate only."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": 0.05, "loser_score_delta": 0.0}'
    )
    idea_a = _make_idea(0.6, "A")
    agent.debate(idea_a, _make_idea(0.4, "B"))
    assert idea_a["tournament_metadata"]["pre_debate_score"] == 0.6

    # Second debate — pre_debate_score should NOT be overwritten
    agent.debate(idea_a, _make_idea(0.3, "C"))
    assert idea_a["tournament_metadata"]["pre_debate_score"] == 0.6


def test_pairwise_delta_accumulation():
    """Debate score deltas should accumulate across multiple debates."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": 0.05, "loser_score_delta": 0.0}'
    )
    idea_a = _make_idea(0.5, "A")
    agent.debate(idea_a, _make_idea(0.4, "B"))

    agent._run.return_value = SimpleNamespace(
        text='{"winner": "A", "reasoning": "ok", '
             '"winner_score_delta": 0.08, "loser_score_delta": 0.0}'
    )
    agent.debate(idea_a, _make_idea(0.3, "C"))
    assert abs(idea_a["tournament_metadata"]["debate_score_delta"] - 0.13) < 1e-9


def test_pairwise_invalid_deltas_zeroed():
    """Non-numeric deltas from LLM should result in no score change."""
    agent = _make_agent(
        '{"winner": "A", "reasoning": "ok", '
        '"winner_score_delta": "high", "loser_score_delta": "low"}'
    )
    result = agent.debate(_make_idea(0.5, "A"), _make_idea(0.5, "B"))
    assert result["winner"]["overall_score"] == 0.5
    assert result["loser"]["overall_score"] == 0.5


def test_pairwise_b_wins():
    """Idea B should win when LLM says B, with correct score adjustments."""
    agent = _make_agent(
        '{"winner": "B", "reasoning": "More novel", '
        '"winner_score_delta": 0.05, "loser_score_delta": -0.05}'
    )
    result = agent.debate(_make_idea(0.5, "A"), _make_idea(0.5, "B"))
    assert result["winner"]["idea_text"] == "B"
    assert result["loser"]["idea_text"] == "A"
    assert abs(result["winner"]["overall_score"] - 0.55) < 1e-9
    assert abs(result["loser"]["overall_score"] - 0.45) < 1e-9


# ---------------------------------------------------------------------------
# Deep debate scoring (exercises real DebateAgent.deep_debate)
# ---------------------------------------------------------------------------

def test_deep_debate_deltas_clamped():
    """Deep debate score deltas should be clamped to ±0.15."""
    response = json.dumps({
        "discussion": "Panel discussed",
        "rankings": [
            {"idea_index": 0, "rank": 1, "score_delta": 0.3, "justification": "strong"},
            {"idea_index": 1, "rank": 2, "score_delta": -0.3, "justification": "weak"},
            {"idea_index": 2, "rank": 3, "score_delta": -0.3, "justification": "worst"},
        ],
        "eliminated_indices": [2],
        "loser_weaknesses": "Weak grounding",
    })
    agent = _make_agent(response)
    ideas = [_make_idea(0.5, "A"), _make_idea(0.5, "B"), _make_idea(0.5, "C")]
    agent.deep_debate(ideas, rounds=1)
    assert abs(ideas[0]["overall_score"] - 0.65) < 1e-9   # +0.15 clamped
    assert abs(ideas[1]["overall_score"] - 0.35) < 1e-9   # -0.15 clamped


def test_deep_debate_loser_weaknesses_on_eliminated():
    """loser_weaknesses should annotate eliminated ideas, not survivors."""
    response = json.dumps({
        "discussion": "Panel discussed",
        "rankings": [
            {"idea_index": 0, "rank": 1, "score_delta": 0.0, "justification": "ok"},
            {"idea_index": 1, "rank": 2, "score_delta": 0.0, "justification": "ok"},
            {"idea_index": 2, "rank": 3, "score_delta": 0.0, "justification": "ok"},
        ],
        "eliminated_indices": [2],
        "loser_weaknesses": "Weak grounding",
    })
    agent = _make_agent(response)
    ideas = [_make_idea(0.5, "A"), _make_idea(0.5, "B"), _make_idea(0.5, "C")]
    remaining = agent.deep_debate(ideas, rounds=1)

    for idea in remaining:
        assert "debate_notes" not in idea
    assert "Weak grounding" in ideas[2].get("debate_notes", "")
