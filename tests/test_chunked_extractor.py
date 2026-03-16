"""Tests for ingest.chunked_extractor."""

from unittest.mock import MagicMock, patch
from dataclasses import dataclass

from ingest.chunked_extractor import (
    split_with_overlap,
    _deduplicate_claims,
    _deduplicate_concepts,
    _deduplicate_signals,
    _evidence_similar,
)


# --- split_with_overlap ---


def test_split_short_text():
    """Text shorter than chunk_size should return a single chunk."""
    text = "Short text."
    chunks = split_with_overlap(text, chunk_size=1000)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_produces_multiple_chunks():
    """Long text should be split into multiple chunks."""
    text = ". ".join(f"Sentence {i}" for i in range(500)) + "."
    chunks = split_with_overlap(text, chunk_size=2000, overlap=200)
    assert len(chunks) >= 2


def test_split_overlap_exists():
    """Consecutive chunks should share overlapping content."""
    sentences = [f"Word{i} " * 10 + "." for i in range(100)]
    text = " ".join(sentences)
    chunks = split_with_overlap(text, chunk_size=2000, overlap=500)
    assert len(chunks) >= 2
    # Check overlap: end of chunk 0 should appear in start of chunk 1
    tail_0 = chunks[0][-200:]
    # At least some of the tail should appear in the next chunk
    # (overlap might not be exact due to sentence boundary truncation)
    overlap_words = set(tail_0.split()) & set(chunks[1][:500].split())
    assert len(overlap_words) > 0, "No overlap detected between chunks"


def test_split_covers_all_text():
    """All content should appear in at least one chunk."""
    sentences = [f"UniqueMarker{i}." for i in range(50)]
    text = " ".join(sentences)
    chunks = split_with_overlap(text, chunk_size=500, overlap=50)
    combined = " ".join(chunks)
    for i in range(50):
        assert f"UniqueMarker{i}" in combined, f"UniqueMarker{i} missing from chunks"


def test_split_chunk_size_respected():
    """Each chunk should not exceed chunk_size."""
    text = "x" * 10000
    chunks = split_with_overlap(text, chunk_size=3000, overlap=200)
    for i, chunk in enumerate(chunks):
        assert len(chunk) <= 3000, f"Chunk {i} is {len(chunk)} chars, exceeds 3000"


# --- Evidence similarity ---


def test_evidence_similar_exact():
    assert _evidence_similar("hello world", "hello world")


def test_evidence_similar_whitespace():
    assert _evidence_similar("hello  world", "hello world")


def test_evidence_similar_case():
    assert _evidence_similar("Hello World", "hello world")


def test_evidence_dissimilar():
    assert not _evidence_similar("completely different text", "something else entirely")


def test_evidence_similar_empty():
    assert not _evidence_similar("", "some text")
    assert not _evidence_similar("some text", "")


# --- Claim deduplication ---


def test_deduplicate_claims_exact():
    claims = [
        {"claim_text": "A", "evidence_snippet": "evidence one", "confidence": 0.8},
        {"claim_text": "B", "evidence_snippet": "evidence one", "confidence": 0.6},
    ]
    result = _deduplicate_claims(claims)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.8  # kept higher confidence


def test_deduplicate_claims_distinct():
    claims = [
        {"claim_text": "A", "evidence_snippet": "completely unique evidence"},
        {"claim_text": "B", "evidence_snippet": "totally different evidence"},
    ]
    result = _deduplicate_claims(claims)
    assert len(result) == 2


def test_deduplicate_claims_keeps_higher_confidence():
    claims = [
        {"claim_text": "A", "evidence_snippet": "same evidence text", "confidence": 0.5},
        {"claim_text": "A v2", "evidence_snippet": "same evidence text", "confidence": 0.9},
    ]
    result = _deduplicate_claims(claims)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.9


# --- Concept deduplication ---


def test_deduplicate_concepts():
    concepts = [
        {"canonical_name": "Transformer", "aliases": ["attention model"]},
        {"canonical_name": "transformer", "aliases": ["self-attention"]},
    ]
    result = _deduplicate_concepts(concepts)
    assert len(result) == 1
    aliases = set(result[0]["aliases"])
    assert "attention model" in aliases
    assert "self-attention" in aliases


def test_deduplicate_concepts_distinct():
    concepts = [
        {"canonical_name": "Transformer", "aliases": []},
        {"canonical_name": "LSTM", "aliases": []},
    ]
    result = _deduplicate_concepts(concepts)
    assert len(result) == 2


# --- Signal deduplication ---


def test_deduplicate_signals():
    signals1 = {
        "capabilities": [
            {"description": "Cap A", "evidence_snippet": "The transformer model achieves state of the art results on all benchmarks tested", "confidence": 0.8},
        ],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [],
    }
    signals2 = {
        "capabilities": [
            {"description": "Cap A again", "evidence_snippet": "The transformer model achieves state of the art results on all benchmarks tested", "confidence": 0.6},
            {"description": "Cap B", "evidence_snippet": "The system can process over ten thousand tokens per second with minimal latency overhead", "confidence": 0.7},
        ],
        "limitations": [
            {"description": "Lim 1", "evidence_snippet": "Performance degrades significantly when input length exceeds the context window", "confidence": 0.5},
        ],
        "bottlenecks": [],
        "breakthroughs": [],
    }
    merged = _deduplicate_signals([signals1, signals2])
    assert len(merged["capabilities"]) == 2  # A (deduped) + B
    assert len(merged["limitations"]) == 1
    # Higher confidence kept for deduplicated entry
    cap_a = [c for c in merged["capabilities"] if "Cap A" in c["description"]]
    assert cap_a[0]["confidence"] == 0.8


# --- Integration-style tests with mocked executor ---


@dataclass
class MockResult:
    text: str


def test_chunked_extract_claims_mock():
    """Test that chunked_extract_claims splits, extracts, and merges."""
    # Build text that's >2x budget
    markers = [f"UniqueEvidence{i}." for i in range(200)]
    text = " ".join(markers)

    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MockResult(
        text='{"claims": [{"claim_text": "test", "claim_type": "finding", '
             '"evidence_snippet": "UniqueEvidence0.", "confidence": 0.8}], '
             '"concepts": [{"canonical_name": "Test", "concept_type": "method", '
             '"description": "test concept", "aliases": []}]}'
    )

    from ingest.chunked_extractor import chunked_extract_claims
    result = chunked_extract_claims(
        "test_source", text, "article", mock_executor,
        budget=500,
    )

    assert "claims" in result
    assert "concepts" in result
    # Executor was called multiple times (once per chunk)
    assert mock_executor.run_raw.call_count >= 2


def test_chunked_deep_summary_mock():
    """Test that chunked_deep_summary produces per-chunk + merge."""
    text = "Content. " * 20000  # ~180k chars

    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MockResult(
        text="# Test\n\n### Key Claims\n- Claim 1."
    )

    from ingest.chunked_extractor import chunked_deep_summary
    result = chunked_deep_summary(
        "test_source", text, "Test Title", "article",
        executor=mock_executor, budget=50000,
    )

    assert isinstance(result, str)
    assert len(result) > 0
    # Should have called run_raw for chunks + merge
    assert mock_executor.run_raw.call_count >= 3  # at least 2 chunks + 1 merge
