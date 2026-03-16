"""Tests for agents.generate."""

from agents.generate import GenerateAgent, TournamentGoal, STRATEGIES, _parse_ideas


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
