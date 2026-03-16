"""Tests for ingest.belief_relevance_checker."""

import json
from unittest.mock import patch, MagicMock

from ingest.belief_relevance_checker import (
    _parse_relevance_hits,
    categorize_hits,
    check_belief_relevance,
    VALID_RELATIONSHIPS,
)


# --- Parsing ---

def test_parse_relevance_hits_json_block():
    text = '```json\n[{"belief_id": "b1", "relationship": "supports", "evidence": "test", "confidence": 0.8}]\n```'
    result = _parse_relevance_hits(text)
    assert len(result) == 1
    assert result[0]["relationship"] == "supports"


def test_parse_relevance_hits_raw_json():
    text = '[{"belief_id": "b1", "relationship": "contradicts", "evidence": "test", "confidence": 0.9}]'
    result = _parse_relevance_hits(text)
    assert len(result) == 1
    assert result[0]["belief_id"] == "b1"


def test_parse_relevance_hits_empty_array():
    text = "No matches found.\n```json\n[]\n```"
    result = _parse_relevance_hits(text)
    assert result == []


def test_parse_relevance_hits_invalid_text():
    result = _parse_relevance_hits("no json here at all")
    assert result == []


def test_parse_relevance_hits_with_preamble():
    text = 'After analysis:\n[{"belief_id": "b1", "relationship": "extends", "evidence": "x", "confidence": 0.7}]\nDone.'
    result = _parse_relevance_hits(text)
    assert len(result) == 1


# --- Categorization ---

def test_categorize_hits_mixed():
    hits = [
        {"belief_id": "b1", "relationship": "contradicts", "evidence": "a", "confidence": 0.8},
        {"belief_id": "b2", "relationship": "supports", "evidence": "b", "confidence": 0.7},
        {"belief_id": "b3", "relationship": "undermines", "evidence": "c", "confidence": 0.6},
        {"belief_id": "b4", "relationship": "extends", "evidence": "d", "confidence": 0.9},
    ]
    result = categorize_hits(hits)
    assert result["has_challenges"] is True
    assert result["has_support"] is True
    assert len(result["challenges"]) == 2  # contradicts + undermines
    assert len(result["support"]) == 2  # supports + extends


def test_categorize_hits_only_support():
    hits = [
        {"belief_id": "b1", "relationship": "supports", "evidence": "a", "confidence": 0.8},
    ]
    result = categorize_hits(hits)
    assert result["has_challenges"] is False
    assert result["has_support"] is True


def test_categorize_hits_only_challenges():
    hits = [
        {"belief_id": "b1", "relationship": "supersedes", "evidence": "a", "confidence": 0.8},
    ]
    result = categorize_hits(hits)
    assert result["has_challenges"] is True
    assert result["has_support"] is False


def test_categorize_hits_empty():
    result = categorize_hits([])
    assert result["has_challenges"] is False
    assert result["has_support"] is False


# --- Validation ---

def test_valid_relationships_complete():
    """All 5 relationship types should be defined."""
    assert VALID_RELATIONSHIPS == {"contradicts", "undermines", "supports", "extends", "supersedes"}


def test_check_belief_relevance_empty_claims():
    """Should return empty list when no claims provided."""
    result = check_belief_relevance([], [{"id": "b1", "claim": "test"}], "src_1")
    assert result == []


def test_check_belief_relevance_empty_beliefs():
    """Should return empty list when no beliefs provided."""
    result = check_belief_relevance([{"claim_text": "test"}], [], "src_1")
    assert result == []


def test_check_belief_relevance_filters_low_confidence():
    """Hits with confidence < 0.5 should be filtered out."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"belief_id": "b1", "relationship": "supports", "evidence": "x", "confidence": 0.3}]'
    )

    claims = [{"claim_text": "Test claim"}]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert result == []  # Filtered out due to low confidence


def test_check_belief_relevance_filters_invalid_belief_ids():
    """Hits referencing non-existent belief IDs should be filtered out."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"belief_id": "nonexistent", "relationship": "supports", "evidence": "x", "confidence": 0.9}]'
    )

    claims = [{"claim_text": "Test claim"}]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert result == []  # Filtered out due to invalid belief_id


def test_check_belief_relevance_filters_invalid_relationships():
    """Hits with invalid relationship types should be filtered out."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"belief_id": "b1", "relationship": "invalid_type", "evidence": "x", "confidence": 0.9}]'
    )

    claims = [{"claim_text": "Test claim"}]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert result == []


def test_check_belief_relevance_valid_hit():
    """Valid hits should pass through."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"belief_id": "b1", "relationship": "supports", "evidence": "test evidence", "reasoning": "because", "confidence": 0.8}]'
    )

    claims = [{"claim_text": "Test claim"}]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert len(result) == 1
    assert result[0]["belief_id"] == "b1"
    assert result[0]["relationship"] == "supports"


def test_check_belief_relevance_multiple_hits():
    """Multiple valid hits from different relationship types."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text=json.dumps([
            {"belief_id": "b1", "relationship": "supports", "evidence": "e1", "confidence": 0.8},
            {"belief_id": "b2", "relationship": "contradicts", "evidence": "e2", "confidence": 0.9},
            {"belief_id": "b1", "relationship": "extends", "evidence": "e3", "confidence": 0.7},
        ])
    )

    claims = [{"claim_text": "Test claim 1"}, {"claim_text": "Test claim 2"}]
    beliefs = [
        {"id": "b1", "claim": "Belief one", "confidence": 0.6},
        {"id": "b2", "claim": "Belief two", "confidence": 0.7},
    ]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert len(result) == 3


# --- Persistence ---

def test_persist_belief_updates_empty():
    """Empty hits should return zero counts."""
    from ingest.belief_relevance_checker import persist_belief_updates
    result = persist_belief_updates([], "src_1")
    assert result["total"] == 0


def test_persist_belief_updates_routes_correctly():
    """Supports/extends → evidence_for; contradicts/undermines/supersedes → evidence_against."""
    hits = [
        {"belief_id": "b1", "relationship": "supports", "evidence": "e1", "confidence": 0.8},
        {"belief_id": "b2", "relationship": "contradicts", "evidence": "e2", "confidence": 0.9},
        {"belief_id": "b3", "relationship": "extends", "evidence": "e3", "confidence": 0.7},
        {"belief_id": "b4", "relationship": "undermines", "evidence": "e4", "confidence": 0.6},
        {"belief_id": "b5", "relationship": "supersedes", "evidence": "e5", "confidence": 0.85},
    ]

    with patch("reading_app.db.append_belief_evidence") as mock_append:
        from ingest.belief_relevance_checker import persist_belief_updates
        result = persist_belief_updates(hits, "src_1")

    assert result["total"] == 5
    assert result["supports"] == 1
    assert result["contradicts"] == 1
    assert result["extends"] == 1
    assert result["undermines"] == 1
    assert result["supersedes"] == 1

    # Check evidence_type routing
    calls = mock_append.call_args_list
    # supports → "for"
    assert calls[0][1]["evidence_type"] == "for"
    # contradicts → "against"
    assert calls[1][1]["evidence_type"] == "against"
    # extends → "for"
    assert calls[2][1]["evidence_type"] == "for"
    # undermines → "against"
    assert calls[3][1]["evidence_type"] == "against"
    # supersedes → "against"
    assert calls[4][1]["evidence_type"] == "against"


# --- Edge cases ---

def test_check_belief_relevance_executor_exception():
    """When executor.run_raw raises an Exception, should return empty list."""
    mock_executor = MagicMock()
    mock_executor.run_raw.side_effect = Exception("LLM timeout")

    claims = [{"claim_text": "Test claim"}]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    result = check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)
    assert result == []


def test_check_belief_relevance_caps_claims_at_30():
    """When 50 claims are passed, only first 30 should be in the prompt sent to executor."""
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(text="[]")

    claims = [{"claim_text": f"Claim number {i}"} for i in range(50)]
    beliefs = [{"id": "b1", "claim": "Test belief", "confidence": 0.5}]

    check_belief_relevance(claims, beliefs, "src_1", executor=mock_executor)

    # Inspect the prompt passed to executor.run_raw
    prompt_arg = mock_executor.run_raw.call_args[0][0]
    # Claims 0-29 should be present; claims 30-49 should not
    assert "Claim number 29" in prompt_arg
    assert "Claim number 30" not in prompt_arg


def test_persist_belief_updates_handles_db_error():
    """When append_belief_evidence raises for one hit but succeeds for the next, total should be 1."""
    hits = [
        {"belief_id": "b1", "relationship": "supports", "evidence": "e1", "confidence": 0.8},
        {"belief_id": "b2", "relationship": "contradicts", "evidence": "e2", "confidence": 0.9},
    ]

    with patch("reading_app.db.append_belief_evidence") as mock_append:
        mock_append.side_effect = [Exception("DB connection lost"), None]
        from ingest.belief_relevance_checker import persist_belief_updates
        result = persist_belief_updates(hits, "src_1")

    assert result["total"] == 1
    assert result["supports"] == 0  # first hit failed
    assert result["contradicts"] == 1  # second hit succeeded
