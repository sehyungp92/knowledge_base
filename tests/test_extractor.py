"""Tests for ingest.extractor."""

from ingest.extractor import _parse_extractions, _validate_evidence, validate_claims_evidence


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


def test_validate_evidence_relaxed_word_threshold():
    """Relaxed mode uses 0.55 threshold instead of 0.8."""
    # Only ~60% of words match in order — fails strict, passes relaxed
    snippet = "the model achieves breakthrough performance on difficult tasks"
    source = "Our the model results achieves on difficult tasks with some caveats."
    assert not _validate_evidence(snippet, source, relaxed=False)
    assert _validate_evidence(snippet, source, relaxed=True)


def test_validate_evidence_relaxed_trigram_fallback():
    """Relaxed mode falls back to trigram similarity for mangled PDF text."""
    # Simulates PDF extraction inserting spaces within words
    snippet = "the efficiency of the architecture improves performance"
    source = "the effi ciency of the archi tecture improves perfor mance significantly"
    assert not _validate_evidence(snippet, source, relaxed=False)
    assert _validate_evidence(snippet, source, relaxed=True)


def test_validate_claims_evidence_basic():
    """validate_claims_evidence keeps valid claims and drops invalid ones."""
    claims = [
        {"claim_text": "good claim", "evidence_snippet": "exact match"},
        {"claim_text": "bad claim", "evidence_snippet": "not in source at all xyz"},
        {"claim_text": "no evidence", "evidence_snippet": ""},
    ]
    source_text = "This text contains an exact match for testing."
    result = validate_claims_evidence(claims, source_text, "test_source")
    assert len(result) == 1
    assert result[0]["claim_text"] == "good claim"


def test_validate_claims_evidence_relaxed_retry():
    """When all claims fail strict validation, retries with relaxed matching."""
    claims = [
        {"claim_text": "claim1", "evidence_snippet": "the efficiency of the architecture improves performance"},
    ]
    # PDF-mangled source with split words — fails strict, passes relaxed trigram
    source_text = "the effi ciency of the archi tecture improves perfor mance significantly"
    result = validate_claims_evidence(claims, source_text, "test_source")
    assert len(result) == 1
    assert result[0].get("evidence_validation") == "relaxed"


def test_validate_claims_evidence_no_relaxed_when_some_pass():
    """Relaxed retry only fires when ALL claims fail, not when some pass."""
    claims = [
        {"claim_text": "good", "evidence_snippet": "exact match"},
        {"claim_text": "bad", "evidence_snippet": "completely unrelated xyz abc"},
    ]
    source_text = "This has an exact match in the text."
    result = validate_claims_evidence(claims, source_text, "test_source")
    assert len(result) == 1
    assert result[0]["claim_text"] == "good"
