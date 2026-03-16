"""Tests for agents.debate."""

from agents.debate import DebateAgent, _parse_debate_result, _parse_deep_debate


def test_parse_debate_result():
    text = '{"winner": "A", "reasoning": "Better grounded", "loser_weaknesses": "Too vague"}'
    result = _parse_debate_result(text)
    assert result["winner"] == "A"
    assert "grounded" in result["reasoning"]


def test_parse_debate_result_b_wins():
    text = 'After analysis:\n{"winner": "B", "reasoning": "More novel"}\n'
    result = _parse_debate_result(text)
    assert result["winner"] == "B"


def test_parse_debate_result_fallback():
    result = _parse_debate_result("unparseable")
    assert result["winner"] == "A"  # Default


def test_parse_deep_debate():
    text = '{"discussion": "Panel agreed", "rankings": [{"idea_index": 0, "rank": 1}], "eliminated_indices": [2]}'
    result = _parse_deep_debate(text)
    assert len(result["rankings"]) == 1
    assert 2 in result["eliminated_indices"]


def test_parse_deep_debate_fallback():
    result = _parse_deep_debate("not json")
    assert result["rankings"] == []
    assert result["eliminated_indices"] == []
