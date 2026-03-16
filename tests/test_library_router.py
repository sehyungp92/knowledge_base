"""Tests for library router artifact loading."""

from contextlib import contextmanager
from unittest.mock import MagicMock, patch


def test_get_source_summary_reads_from_source_subdirectory(tmp_path):
    source_id = "src_123"
    library_path = tmp_path / "library"
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True)
    (source_dir / "deep_summary.md").write_text("# Summary", encoding="utf-8")

    with patch("webapp.api.routers.library.db.get_source", return_value={"library_path": str(library_path)}):
        from webapp.api.routers.library import get_source_summary

        result = get_source_summary(source_id)

    assert result == {"markdown": "# Summary"}


def test_get_source_reflection_reads_from_source_subdirectory(tmp_path):
    source_id = "src_456"
    library_path = tmp_path / "library"
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True)
    (source_dir / "reflection.md").write_text("# Reflection", encoding="utf-8")

    with patch("webapp.api.routers.library.db.get_source", return_value={"library_path": str(library_path)}):
        from webapp.api.routers.library import get_source_reflection

        result = get_source_reflection(source_id)

    assert result == {"markdown": "# Reflection"}


def test_get_source_graph_context_returns_cluster_peers_and_implications():
    source_id = "src_789"

    conn = MagicMock()
    conn.execute.side_effect = [
        MagicMock(fetchone=MagicMock(return_value={"influence_score": 0.42, "community_id": "7"})),
        MagicMock(fetchone=MagicMock(return_value={"cnt": 4})),
        MagicMock(fetchall=MagicMock(return_value=[
            {"id": "peer_1", "title": "Peer Source", "influence_score": 0.12},
        ])),
    ]

    @contextmanager
    def get_conn():
        yield conn

    mock_graph = MagicMock()
    mock_graph.get_source_implications.return_value = [
        {
            "source_theme_name": "Autonomous Agents",
            "target_theme_name": "Inference Efficiency",
            "implication": "Agents pressure cost and latency constraints.",
            "confidence": 0.9,
        }
    ]

    with patch("webapp.api.routers.library.db.get_source", return_value={"id": source_id}), \
         patch("webapp.api.routers.library.db.get_conn", side_effect=get_conn), \
         patch("webapp.api.routers.library.GraphRetriever", return_value=mock_graph):
        from webapp.api.routers.library import get_source_graph_context

        result = get_source_graph_context(source_id)

    assert result["influence_score"] == 0.42
    assert result["community_id"] == 7
    assert result["community_size"] == 4
    assert result["cluster_peers"][0]["id"] == "peer_1"
    assert result["implications"][0]["target_theme_name"] == "Inference Efficiency"
