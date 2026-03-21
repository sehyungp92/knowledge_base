"""Tests for retrieval.graph."""

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from retrieval.graph import GraphRetriever


def test_one_hop(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"connected_id": "src_002", "title": "Related Paper", "edge_type": "extends",
         "explanation": "Builds on method", "confidence": 0.8}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.one_hop("src_001")
    assert len(results) == 1
    assert results[0]["edge_type"] == "extends"


def test_one_hop_empty(mock_conn):
    get_conn, _ = mock_conn
    gr = GraphRetriever(get_conn)
    assert gr.one_hop("nonexistent") == []


def test_two_hop_via_concepts(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"id": "src_003", "title": "Shared Concept Paper",
         "shared_concepts": ["RLHF", "alignment"], "overlap_count": 2}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_concepts("src_001")
    assert len(results) == 1
    assert results[0]["overlap_count"] == 2


def test_two_hop_via_claims(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"id": "src_004", "title": "Claim-linked Paper", "edge_type": "supports",
         "our_claim": "RLHF works", "their_claim": "RLHF is effective"}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_claims("src_001")
    assert len(results) == 1


def test_explain_path(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"path": ["src_001", "src_002"], "depth": 1}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.explain_path("src_001", "src_002")
    assert len(results) == 1


def test_find_contradictions_empty(mock_conn):
    get_conn, _ = mock_conn
    gr = GraphRetriever(get_conn)
    results = gr.find_contradictions("alignment")
    assert results == []


def test_find_contradictions_with_topic(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"claim_a_id": "c1", "claim_a_text": "RLHF helps", "source_a_id": "s1",
         "claim_b_id": "c2", "claim_b_text": "RLHF hurts", "source_b_id": "s2",
         "explanation": "Contradictory", "confidence": 0.9}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.find_contradictions("RLHF")
    assert len(results) >= 1


def test_get_source_implications(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = [
        {"source_theme_name": "alignment", "target_theme_name": "safety",
         "implication": "New technique helps", "confidence": 0.7}
    ]
    gr = GraphRetriever(get_conn)
    results = gr.get_source_implications("src_001")
    assert len(results) == 1


def test_graph_retriever_init(mock_conn):
    get_conn, _ = mock_conn
    gr = GraphRetriever(get_conn)
    assert gr._get_conn is not None


def test_explain_path_empty(mock_conn):
    get_conn, _ = mock_conn
    gr = GraphRetriever(get_conn)
    results = gr.explain_path("src_001", "src_nonexistent")
    assert results == []


def test_two_hop_min_overlap(mock_conn):
    get_conn, conn = mock_conn
    conn.execute.return_value.fetchall.return_value = []
    gr = GraphRetriever(get_conn)
    results = gr.two_hop_via_concepts("src_001", min_overlap=5)
    assert results == []


# ---------------------------------------------------------------------------
# Tests merged from test_graph_router.py — webapp graph router helpers
# ---------------------------------------------------------------------------


def test_export_graph_includes_community_ids():
    """Source graph export should carry community ids alongside pagerank nodes."""
    conn = MagicMock()
    conn.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=[
            {
                "id": "src_1",
                "title": "Source One",
                "pagerank": 0.9,
                "community_metadata": {"community_id": "13"},
                "community_score": 13.0,
            }
        ])),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]

    @contextmanager
    def get_conn():
        yield conn

    with patch("webapp.api.routers.graph.db.get_conn", side_effect=get_conn):
        from webapp.api.routers.graph import export_graph

        result = export_graph(limit=10)

    assert result["nodes"][0]["community"] == 13


def test_export_graph_falls_back_to_community_score_when_metadata_missing():
    """Source graph export should derive community ids from score when metadata is absent."""
    conn = MagicMock()
    conn.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=[
            {
                "id": "src_2",
                "title": "Source Two",
                "pagerank": 0.7,
                "community_metadata": None,
                "community_score": 7.0,
            }
        ])),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]

    @contextmanager
    def get_conn():
        yield conn

    with patch("webapp.api.routers.graph.db.get_conn", side_effect=get_conn):
        from webapp.api.routers.graph import export_graph

        result = export_graph(limit=10)

    assert result["nodes"][0]["community"] == 7


def test_theme_context_returns_rank_and_relationships():
    """Theme context should expose influence rank plus parent/child and implication previews."""
    conn = MagicMock()
    conn.execute.side_effect = [
        MagicMock(fetchone=MagicMock(return_value={"id": "autonomous_agents", "name": "Autonomous Agents"})),
        MagicMock(fetchone=MagicMock(return_value={"score": 0.5, "rank": 2})),
        MagicMock(fetchall=MagicMock(return_value=[{"id": "meta_capabilities", "name": "AI Capabilities", "relationship": "contains"}])),
        MagicMock(fetchall=MagicMock(return_value=[{"id": "computer_use_agents", "name": "Computer Use Agents", "relationship": "contains"}])),
        MagicMock(fetchall=MagicMock(return_value=[{
            "id": "imp_1",
            "implication": "Agents reshape software delivery.",
            "confidence": 0.88,
            "source_theme_id": "autonomous_agents",
            "target_theme_id": "saas_disruption",
            "target_theme": "SaaS & Service-as-Software",
        }])),
        MagicMock(fetchall=MagicMock(return_value=[{
            "id": "imp_2",
            "implication": "Test-time compute unlocks longer agent loops.",
            "confidence": 0.9,
            "source_theme_id": "test_time_compute",
            "target_theme_id": "autonomous_agents",
            "source_theme": "Test-Time Compute",
        }])),
    ]

    @contextmanager
    def get_conn():
        yield conn

    with patch("webapp.api.routers.graph.db.get_conn", side_effect=get_conn):
        from webapp.api.routers.graph import theme_context

        result = theme_context("autonomous_agents")

    assert result["influence"]["rank"] == 2
    assert result["parents"][0]["id"] == "meta_capabilities"
    assert result["children"][0]["id"] == "computer_use_agents"
    assert result["outgoing_implications"][0]["target_theme"] == "SaaS & Service-as-Software"
    assert result["incoming_implications"][0]["source_theme"] == "Test-Time Compute"
