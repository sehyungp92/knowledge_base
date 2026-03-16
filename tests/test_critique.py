"""Tests for agents.critique."""

from agents.critique import CritiqueAgent, _parse_critiques


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
