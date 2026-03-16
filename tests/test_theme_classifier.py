"""Tests for ingest.theme_classifier."""

from ingest.theme_classifier import _parse_theme_output


def test_parse_json_array():
    text = '[{"theme_id": "alignment", "relevance": 0.8}]'
    result = _parse_theme_output(text)
    assert len(result) == 1
    assert result[0]["theme_id"] == "alignment"


def test_parse_json_block():
    text = '```json\n[{"theme_id": "safety", "relevance": 0.7}]\n```'
    result = _parse_theme_output(text)
    assert len(result) == 1


def test_parse_with_surrounding_text():
    text = 'Here are the themes:\n[{"theme_id": "reasoning", "relevance": 0.6}]\nDone.'
    result = _parse_theme_output(text)
    assert len(result) == 1


def test_parse_failure():
    result = _parse_theme_output("not json")
    assert result == []


def test_parse_multiple_themes():
    text = '[{"theme_id": "ml", "relevance": 0.9}, {"theme_id": "nlp", "relevance": 0.7}]'
    result = _parse_theme_output(text)
    assert len(result) == 2
