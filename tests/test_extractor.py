"""Tests for ingest.extractor."""

from ingest.extractor import _parse_extractions, _validate_evidence


def test_parse_extractions_json():
    text = '{"claims": [{"claim_text": "test"}], "concepts": []}'
    result = _parse_extractions(text)
    assert len(result["claims"]) == 1
    assert result["claims"][0]["claim_text"] == "test"


def test_parse_extractions_code_block():
    text = '```json\n{"claims": [{"claim_text": "test"}], "concepts": []}\n```'
    result = _parse_extractions(text)
    assert len(result["claims"]) == 1


def test_parse_extractions_empty():
    result = _parse_extractions("")
    assert result["claims"] == []
    assert result["concepts"] == []


def test_parse_extractions_invalid():
    result = _parse_extractions("not json at all")
    assert result["claims"] == []


def test_parse_extractions_embedded():
    text = 'Here is the result:\n{"claims": [{"claim_text": "embedded"}], "concepts": []}\nDone.'
    result = _parse_extractions(text)
    assert len(result["claims"]) == 1


def test_validate_evidence_exact():
    assert _validate_evidence("exact match", "This is an exact match in text.")


def test_validate_evidence_missing():
    assert not _validate_evidence("completely different", "No overlap at all with source.")


def test_validate_evidence_fuzzy():
    # 80% of words should match in order
    snippet = "the model achieves state of the art performance on benchmark"
    source = "Our results show that the model achieves state of the art performance on the benchmark dataset."
    assert _validate_evidence(snippet, source)


def test_validate_evidence_short():
    assert _validate_evidence("test", "this is a test string")
    assert not _validate_evidence("xyz", "no match here")
