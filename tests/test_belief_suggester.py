"""Tests for ingest.belief_suggester."""

import json
from unittest.mock import patch, MagicMock

from ingest.belief_suggester import (
    _text_similarity,
    _format_clusters,
    _parse_suggestions,
    _cluster_by_text,
    MIN_SOURCES_FOR_SUGGESTION,
    MIN_CONVERGENT_SOURCES,
    suggest_beliefs_for_theme,
)


# --- Text Similarity ---

def test_text_similarity_identical():
    assert _text_similarity("hello world", "hello world") == 1.0


def test_text_similarity_disjoint():
    assert _text_similarity("hello world", "foo bar") == 0.0


def test_text_similarity_partial():
    sim = _text_similarity("scaling laws hold for llms", "scaling laws apply to language models")
    assert 0.0 < sim < 1.0


def test_text_similarity_empty():
    assert _text_similarity("", "hello") == 0.0
    assert _text_similarity("hello", "") == 0.0
    assert _text_similarity("", "") == 0.0


# --- Cluster Formatting ---

def test_format_clusters_empty():
    result = _format_clusters([])
    assert result == ""


def test_format_clusters_single():
    clusters = [{
        "claims": [
            {"claim_text": "Claim A", "source_id": "src_1"},
            {"claim_text": "Claim B", "source_id": "src_2"},
        ],
        "source_count": 2,
    }]
    result = _format_clusters(clusters)
    assert "Cluster 1" in result
    assert "src_1" in result
    assert "Claim A" in result


# --- Suggestion Parsing ---

def test_parse_suggestions_json_block():
    text = '```json\n[{"claim": "Scaling laws hold", "suggested_confidence": 0.7, "belief_type": "predictive"}]\n```'
    result = _parse_suggestions(text)
    assert len(result) == 1
    assert result[0]["claim"] == "Scaling laws hold"


def test_parse_suggestions_raw_json():
    text = '[{"claim": "Test", "suggested_confidence": 0.5}]'
    result = _parse_suggestions(text)
    assert len(result) == 1


def test_parse_suggestions_empty():
    result = _parse_suggestions("no suggestions")
    assert result == []


def test_parse_suggestions_empty_array():
    result = _parse_suggestions("[]")
    assert result == []


# --- Text-Based Clustering ---

def test_cluster_by_text_insufficient_claims():
    """Fewer claims than MIN_CONVERGENT_SOURCES should return no clusters."""
    rows = [
        {"claim_text": "Scaling laws hold for LLMs", "source_id": "src_1", "id": "c1"},
        {"claim_text": "Scaling laws hold for language models", "source_id": "src_2", "id": "c2"},
    ]
    clusters = _cluster_by_text(rows)
    assert clusters == []  # Need 3+ distinct sources


def test_cluster_by_text_with_convergence():
    """Claims from 3+ distinct sources with similar text should form a cluster."""
    rows = [
        {"claim_text": "Scaling laws continue to hold for large language models", "source_id": "src_1", "id": "c1"},
        {"claim_text": "Scaling laws hold for language models at current scale", "source_id": "src_2", "id": "c2"},
        {"claim_text": "Scaling laws are holding for large language model training", "source_id": "src_3", "id": "c3"},
    ]
    clusters = _cluster_by_text(rows)
    # These claims share enough keywords to cluster
    assert len(clusters) >= 1
    assert clusters[0]["source_count"] >= 3


def test_cluster_by_text_same_source_not_counted():
    """Multiple claims from the same source shouldn't inflate source_count."""
    rows = [
        {"claim_text": "Scaling laws hold for large language models", "source_id": "src_1", "id": "c1"},
        {"claim_text": "Scaling laws hold for language model training", "source_id": "src_1", "id": "c2"},
        {"claim_text": "Scaling laws continue for large language models", "source_id": "src_1", "id": "c3"},
    ]
    clusters = _cluster_by_text(rows)
    # All from same source, so no cluster should form (need 3+ distinct sources)
    assert clusters == []


def test_cluster_by_text_disjoint_claims():
    """Claims on completely different topics should not cluster."""
    rows = [
        {"claim_text": "Scaling laws hold for large language models", "source_id": "src_1", "id": "c1"},
        {"claim_text": "Robotics requires physical world understanding", "source_id": "src_2", "id": "c2"},
        {"claim_text": "Drug discovery benefits from protein folding models", "source_id": "src_3", "id": "c3"},
    ]
    clusters = _cluster_by_text(rows)
    assert clusters == []  # Too different to cluster


# --- Constants ---

def test_min_sources_threshold():
    assert MIN_SOURCES_FOR_SUGGESTION == 5


def test_min_convergent_sources():
    assert MIN_CONVERGENT_SOURCES == 3


# --- Edge Cases for suggest_beliefs_for_theme ---

@patch("ingest.belief_suggester._get_theme_source_count", return_value=2)
def test_suggest_beliefs_for_theme_below_threshold(mock_count):
    result = suggest_beliefs_for_theme("t1", "Theme One")
    assert result == []


@patch("ingest.belief_suggester._get_convergent_clusters", return_value=[])
@patch("ingest.belief_suggester._get_theme_source_count", return_value=10)
def test_suggest_beliefs_for_theme_no_clusters(mock_count, mock_clusters):
    result = suggest_beliefs_for_theme("t1", "Theme One")
    assert result == []


@patch("reading_app.db.get_beliefs_for_theme", return_value=[])
@patch("ingest.belief_suggester._get_convergent_clusters", return_value=[{"claims": [], "source_count": 3}])
@patch("ingest.belief_suggester._get_theme_source_count", return_value=10)
def test_suggest_beliefs_validates_belief_type(mock_count, mock_clusters, mock_beliefs):
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"claim": "Test claim", "suggested_confidence": 0.7, "belief_type": "INVALID_TYPE"}]'
    )
    result = suggest_beliefs_for_theme("t1", "Theme One", executor=mock_executor)
    assert len(result) == 1
    assert result[0]["belief_type"] == "factual"


@patch("reading_app.db.get_beliefs_for_theme", return_value=[])
@patch("ingest.belief_suggester._get_convergent_clusters", return_value=[{"claims": [], "source_count": 3}])
@patch("ingest.belief_suggester._get_theme_source_count", return_value=10)
def test_suggest_beliefs_clamps_confidence(mock_count, mock_clusters, mock_beliefs):
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"claim": "Test claim", "suggested_confidence": 1.5, "belief_type": "factual"}]'
    )
    result = suggest_beliefs_for_theme("t1", "Theme One", executor=mock_executor)
    assert len(result) == 1
    assert result[0]["suggested_confidence"] <= 1.0


@patch("reading_app.db.get_beliefs_for_theme", return_value=[])
@patch("ingest.belief_suggester._get_convergent_clusters", return_value=[{"claims": [], "source_count": 3}])
@patch("ingest.belief_suggester._get_theme_source_count", return_value=10)
def test_suggest_beliefs_adds_theme_metadata(mock_count, mock_clusters, mock_beliefs):
    mock_executor = MagicMock()
    mock_executor.run_raw.return_value = MagicMock(
        text='[{"claim": "Valid claim", "suggested_confidence": 0.8, "belief_type": "factual"}]'
    )
    result = suggest_beliefs_for_theme("my_theme", "My Theme", executor=mock_executor)
    assert len(result) == 1
    assert result[0]["theme_id"] == "my_theme"
    assert result[0]["theme_name"] == "My Theme"
