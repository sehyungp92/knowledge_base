"""Tests for webapp graph router helpers."""

from contextlib import contextmanager
from unittest.mock import MagicMock, patch


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
