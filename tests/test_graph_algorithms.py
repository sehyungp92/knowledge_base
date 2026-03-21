"""Tests for retrieval.graph_algorithms."""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock, patch, call

from retrieval.graph_algorithms import KnowledgeGraphAnalyzer


# ---------------------------------------------------------------------------
# 1. _build_source_graph
# ---------------------------------------------------------------------------

def test_build_graph_from_edges(mock_conn):
    """Mock source_edges rows, verify graph has correct nodes and edges."""
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"source_a": "s1", "source_b": "s2", "edge_type": "extends", "confidence": 0.9},
        {"source_a": "s2", "source_b": "s3", "edge_type": "supports", "confidence": 0.8},
    ]
    analyzer = KnowledgeGraphAnalyzer(get_conn)
    G = analyzer._build_source_graph()
    assert G is not None
    assert set(G.nodes()) == {"s1", "s2", "s3"}
    assert G.number_of_edges() == 2
    assert G.has_edge("s1", "s2")
    assert G.has_edge("s2", "s3")


# ---------------------------------------------------------------------------
# 2. compute_pagerank
# ---------------------------------------------------------------------------

def test_pagerank_returns_ranked_sources(mock_conn):
    """3-node cycle — verify 3 results with scores summing to ~1.0."""
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"source_a": "s1", "source_b": "s2", "edge_type": "extends", "confidence": 0.9},
        {"source_a": "s2", "source_b": "s3", "edge_type": "extends", "confidence": 0.9},
        {"source_a": "s3", "source_b": "s1", "edge_type": "extends", "confidence": 0.9},
    ]
    analyzer = KnowledgeGraphAnalyzer(get_conn)
    results = analyzer.compute_pagerank()

    assert len(results) == 3
    total_score = sum(r["score"] for r in results)
    assert abs(total_score - 1.0) < 0.01
    for r in results:
        assert r["metric_type"] == "pagerank"
        assert r["entity_type"] == "source"


# ---------------------------------------------------------------------------
# 3. compute_communities
# ---------------------------------------------------------------------------

def test_communities_returns_clusters(mock_conn):
    """Verify all results have metadata with community_id."""
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"source_a": "s1", "source_b": "s2", "edge_type": "extends", "confidence": 0.9},
        {"source_a": "s2", "source_b": "s3", "edge_type": "extends", "confidence": 0.9},
        {"source_a": "s3", "source_b": "s1", "edge_type": "extends", "confidence": 0.9},
    ]
    analyzer = KnowledgeGraphAnalyzer(get_conn)
    results = analyzer.compute_communities()

    assert len(results) == 3
    for r in results:
        assert r["metric_type"] == "community"
        assert "community_id" in r["metadata"]


# ---------------------------------------------------------------------------
# 4. compute_betweenness
# ---------------------------------------------------------------------------

def test_betweenness_returns_bridge_concepts(mock_conn):
    """Mock source_concepts so one concept bridges two groups; verify results have scores."""
    # Source s1 has concepts c1, c2; source s2 has concepts c2, c3.
    # c2 is the bridge node and should have betweenness > 0.
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"source_id": "s1", "concept_id": "c1"},
        {"source_id": "s1", "concept_id": "c2"},
        {"source_id": "s2", "concept_id": "c2"},
        {"source_id": "s2", "concept_id": "c3"},
    ]
    analyzer = KnowledgeGraphAnalyzer(get_conn)
    results = analyzer.compute_betweenness()

    # c2 bridges c1 and c3 — only c2 should have betweenness > 0
    assert len(results) >= 1
    ids = [r["entity_id"] for r in results]
    assert "c2" in ids
    for r in results:
        assert r["metric_type"] == "betweenness"
        assert r["entity_type"] == "concept"
        assert r["score"] > 0


# ---------------------------------------------------------------------------
# 5. materialize
# ---------------------------------------------------------------------------

def test_materialize_writes_to_db(mock_conn):
    """Stub compute methods, verify upsert calls reference graph_metrics."""
    get_conn, conn = mock_conn
    analyzer = KnowledgeGraphAnalyzer(get_conn)

    # Stub all four compute methods to return fixed results
    fake_results = [
        {
            "metric_type": "pagerank",
            "entity_type": "source",
            "entity_id": "s1",
            "score": 0.5,
            "metadata": {},
        }
    ]
    analyzer.compute_pagerank = MagicMock(return_value=fake_results)
    analyzer.compute_communities = MagicMock(return_value=[])
    analyzer.compute_betweenness = MagicMock(return_value=[])
    analyzer.compute_theme_influence = MagicMock(return_value=[])

    summary = analyzer.materialize()

    # The four compute methods were called
    analyzer.compute_pagerank.assert_called_once()
    analyzer.compute_communities.assert_called_once()
    analyzer.compute_betweenness.assert_called_once()
    analyzer.compute_theme_influence.assert_called_once()

    # At least one execute call contains "graph_metrics"
    insert_calls = [
        c for c in conn.execute.call_args_list if "graph_metrics" in str(c)
    ]
    assert len(insert_calls) >= 1

    assert summary["counts"]["pagerank"] == 1
    assert summary["errors"] == []


# ---------------------------------------------------------------------------
# 6. Empty graph
# ---------------------------------------------------------------------------

def test_empty_graph_returns_empty_results(mock_conn):
    """Empty fetchall → empty list from compute methods."""
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = []

    analyzer = KnowledgeGraphAnalyzer(get_conn)
    assert analyzer.compute_pagerank() == []
    assert analyzer.compute_communities() == []
    assert analyzer.compute_betweenness() == []


# ---------------------------------------------------------------------------
# Additional: materialize continues on failure
# ---------------------------------------------------------------------------

def test_materialize_continues_on_failure(mock_conn):
    """If one compute method raises, others still run."""
    get_conn, conn = mock_conn
    analyzer = KnowledgeGraphAnalyzer(get_conn)

    analyzer.compute_pagerank = MagicMock(side_effect=RuntimeError("boom"))
    analyzer.compute_communities = MagicMock(return_value=[])
    analyzer.compute_betweenness = MagicMock(return_value=[])
    analyzer.compute_theme_influence = MagicMock(return_value=[])

    summary = analyzer.materialize()

    assert "compute_pagerank" in summary["errors"]
    # Other methods still called
    analyzer.compute_communities.assert_called_once()
    analyzer.compute_betweenness.assert_called_once()
    analyzer.compute_theme_influence.assert_called_once()
