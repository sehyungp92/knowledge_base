"""Tests for retrieval.graph."""

from unittest.mock import MagicMock, patch
from retrieval.graph import GraphRetriever


def _mock_conn():
    """Create a mock connection context manager."""
    conn = MagicMock()
    conn.execute.return_value.fetchall.return_value = []
    from contextlib import contextmanager
    @contextmanager
    def get_conn():
        yield conn
    return get_conn, conn


def test_one_hop():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"connected_id": "src_002", "title": "Related Paper", "edge_type": "extends",
         "explanation": "Builds on method", "confidence": 0.8}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.one_hop("src_001")
    assert len(results) == 1
    assert results[0]["edge_type"] == "extends"


def test_one_hop_empty():
    get_conn, _ = _mock_conn()
    gr = GraphRetriever(get_conn)
    assert gr.one_hop("nonexistent") == []


def test_two_hop_via_concepts():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"id": "src_003", "title": "Shared Concept Paper",
         "shared_concepts": ["RLHF", "alignment"], "overlap_count": 2}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_concepts("src_001")
    assert len(results) == 1
    assert results[0]["overlap_count"] == 2


def test_two_hop_via_claims():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"id": "src_004", "title": "Claim-linked Paper", "edge_type": "supports",
         "our_claim": "RLHF works", "their_claim": "RLHF is effective"}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_claims("src_001")
    assert len(results) == 1


def test_explain_path():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"path": ["src_001", "src_002"], "depth": 1}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.explain_path("src_001", "src_002")
    assert len(results) == 1


def test_find_contradictions_empty():
    get_conn, _ = _mock_conn()
    gr = GraphRetriever(get_conn)
    results = gr.find_contradictions("alignment")
    assert results == []


def test_find_contradictions_with_topic():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"claim_a_id": "c1", "claim_a_text": "RLHF helps", "source_a_id": "s1",
         "claim_b_id": "c2", "claim_b_text": "RLHF hurts", "source_b_id": "s2",
         "explanation": "Contradictory", "confidence": 0.9}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.find_contradictions("RLHF")
    assert len(results) >= 1


def test_get_source_implications():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = [
        {"source_theme_name": "alignment", "target_theme_name": "safety",
         "implication": "New technique helps", "confidence": 0.7}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.get_source_implications("src_001")
    assert len(results) == 1


def test_graph_retriever_init():
    get_conn, _ = _mock_conn()
    gr = GraphRetriever(get_conn)
    assert gr._get_conn is not None


def test_explain_path_empty():
    get_conn, _ = _mock_conn()
    gr = GraphRetriever(get_conn)
    results = gr.explain_path("src_001", "src_nonexistent")
    assert results == []


def test_two_hop_min_overlap():
    get_conn, conn = _mock_conn()
    conn.execute.return_value.fetchall.return_value = []
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_concepts("src_001", min_overlap=5)
    assert results == []
