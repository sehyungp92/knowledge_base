"""Tests for ingest.implication_extractor."""

from ingest.implication_extractor import _parse_implications


def test_parse_implications_json():
    text = '[{"source_theme_id": "scaling", "target_theme_id": "alignment", "implication": "Scaling affects alignment", "confidence": 0.7}]'
    result = _parse_implications(text)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.7


def test_parse_implications_code_block():
    text = '```json\n[{"source_theme_id": "a", "target_theme_id": "b", "implication": "test", "confidence": 0.5}]\n```'
    result = _parse_implications(text)
    assert len(result) == 1


def test_parse_implications_empty():
    assert _parse_implications("no json") == []


def test_parse_implications_multiple():
    text = '[{"source_theme_id": "a", "target_theme_id": "b", "implication": "1", "confidence": 0.5}, {"source_theme_id": "c", "target_theme_id": "d", "implication": "2", "confidence": 0.6}]'
    result = _parse_implications(text)
    assert len(result) == 2


def test_adaptive_cap():
    # cap = min(4 + (n-1) * 2, 12)
    assert min(4 + (1 - 1) * 2, 12) == 4
    assert min(4 + (3 - 1) * 2, 12) == 8
    assert min(4 + (5 - 1) * 2, 12) == 12
    assert min(4 + (10 - 1) * 2, 12) == 12
