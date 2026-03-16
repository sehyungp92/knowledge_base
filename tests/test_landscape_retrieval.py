"""Tests for landscape-specific retrieval queries."""

from unittest.mock import patch, MagicMock


def test_get_theme_state_returns_dict():
    from retrieval.landscape import get_theme_state
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = {
            "id": "robotics", "name": "Robotics", "state_summary": "evolving",
            "velocity": 0.6,
        }
        mock_conn.execute.return_value.fetchall.return_value = []
        result = get_theme_state("robotics")
    assert result["theme"]["id"] == "robotics"
    assert "capabilities" in result
    assert "limitations" in result
    assert "bottlenecks" in result
    assert "breakthroughs" in result
    assert "anticipations" in result
    assert "cross_theme_implications" in result


def test_get_theme_state_returns_none_theme():
    from retrieval.landscape import get_theme_state
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchone.return_value = None
        result = get_theme_state("nonexistent")
    assert result["theme"] is None


def test_get_recent_breakthroughs():
    from retrieval.landscape import get_recent_breakthroughs
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "bt_001", "description": "test", "theme_name": "Robotics"}
        ]
        result = get_recent_breakthroughs(days=90)
    assert len(result) == 1


def test_get_recent_breakthroughs_with_theme_filter():
    from retrieval.landscape import get_recent_breakthroughs
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "bt_001", "description": "test", "theme_name": "Robotics"}
        ]
        result = get_recent_breakthroughs(days=30, theme_id="robotics")
    assert len(result) == 1
    # Verify theme_id was passed in the query params
    call_args = mock_conn.execute.call_args
    assert "robotics" in call_args[0][1]


def test_get_bottleneck_ranking():
    from retrieval.landscape import get_bottleneck_ranking
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "bn_001", "description": "test", "horizon_score": 4}
        ]
        result = get_bottleneck_ranking(theme_id="robotics")
    assert len(result) >= 1


def test_get_bottleneck_ranking_no_filter():
    from retrieval.landscape import get_bottleneck_ranking
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "bn_001", "description": "test", "horizon_score": 5, "theme_name": "Robotics"},
            {"id": "bn_002", "description": "test2", "horizon_score": 2, "theme_name": "Safety"},
        ]
        result = get_bottleneck_ranking()
    assert len(result) == 2
    # Verify no WHERE clause params were passed
    call_args = mock_conn.execute.call_args
    assert call_args[0][1] == ()


def test_compute_theme_velocity():
    from retrieval.landscape import compute_theme_velocity
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "robotics", "name": "Robotics", "velocity_window_days": 90,
             "recent_ingested": 5, "recent_published": 2, "total_with_pub_date": 10,
             "recent_breakthroughs": 1, "total_sources": 20}
        ]
        result = compute_theme_velocity()
    assert len(result) >= 1
    assert "velocity" in result[0]


def test_velocity_capped_at_one():
    from retrieval.landscape import compute_theme_velocity
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "hot_theme", "name": "Hot", "velocity_window_days": 90,
             "recent_ingested": 100, "recent_published": 80, "total_with_pub_date": 5,
             "recent_breakthroughs": 10, "total_sources": 5}
        ]
        result = compute_theme_velocity()
    assert result[0]["velocity"] <= 1.0


def test_velocity_ordering():
    from retrieval.landscape import compute_theme_velocity
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "robotics", "name": "Robotics", "velocity_window_days": 90,
             "recent_ingested": 10, "recent_published": 5, "total_with_pub_date": 30,
             "recent_breakthroughs": 2, "total_sources": 50},
            {"id": "safety", "name": "Safety", "velocity_window_days": 90,
             "recent_ingested": 0, "recent_published": 0, "total_with_pub_date": 0,
             "recent_breakthroughs": 0, "total_sources": 5},
        ]
        result = compute_theme_velocity()
    assert len(result) == 2
    assert result[0]["velocity"] > result[1]["velocity"]


def test_velocity_zero_total_sources():
    """Velocity should handle zero total sources without division error."""
    from retrieval.landscape import compute_theme_velocity
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "empty", "name": "Empty", "velocity_window_days": 90,
             "recent_ingested": 0, "recent_published": 0, "total_with_pub_date": 0,
             "recent_breakthroughs": 0, "total_sources": 0}
        ]
        result = compute_theme_velocity()
    assert result[0]["velocity"] == 0.0


def test_velocity_none_values():
    """Velocity should handle None values from the database gracefully."""
    from retrieval.landscape import compute_theme_velocity
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "sparse", "name": "Sparse", "velocity_window_days": 90,
             "recent_ingested": None, "recent_published": None, "total_with_pub_date": None,
             "recent_breakthroughs": None, "total_sources": None}
        ]
        result = compute_theme_velocity()
    assert result[0]["velocity"] == 0.0


def test_update_all_theme_velocities():
    from retrieval.landscape import update_all_theme_velocities
    with patch("retrieval.landscape.compute_theme_velocity") as mock_compute, \
         patch("retrieval.landscape.db") as mock_db:
        mock_compute.return_value = [
            {"id": "robotics", "velocity": 0.5},
            {"id": "safety", "velocity": 0.1},
        ]
        count = update_all_theme_velocities()
    assert count == 2
    assert mock_db.update_theme_velocity.call_count == 2


def test_update_all_theme_velocities_empty():
    from retrieval.landscape import update_all_theme_velocities
    with patch("retrieval.landscape.compute_theme_velocity") as mock_compute, \
         patch("retrieval.landscape.db"):
        mock_compute.return_value = []
        count = update_all_theme_velocities()
    assert count == 0


def test_get_anticipations_with_evidence():
    from retrieval.landscape import get_anticipations_with_evidence
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "ant_001", "prediction": "test prediction", "theme_id": "robotics",
             "theme_name": "Robotics", "confidence": 0.8,
             "status_evidence": [{"source_id": "s1"}], "evidence_count": 1}
        ]
        result = get_anticipations_with_evidence()
    assert len(result) == 1
    assert result[0]["evidence_count"] == 1


def test_get_limitation_validation_rates():
    from retrieval.landscape import get_limitation_validation_rates
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"signal_type": "implicit_hedging", "total": 15,
             "confirmed": 10, "rejected": 3, "rejection_rate": 0.23}
        ]
        result = get_limitation_validation_rates()
    assert len(result) == 1
    assert result[0]["signal_type"] == "implicit_hedging"


def test_get_over_optimistic_themes_uses_preaggregated_counts():
    from retrieval.landscape import get_over_optimistic_themes
    with patch("retrieval.landscape.db.get_conn") as mock_conn_ctx:
        mock_conn = MagicMock()
        mock_conn_ctx.return_value.__enter__ = lambda s: mock_conn
        mock_conn_ctx.return_value.__exit__ = MagicMock(return_value=False)
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "robotics", "name": "Robotics", "capability_count": 4, "limitation_count": 0}
        ]

        result = get_over_optimistic_themes()

    assert len(result) == 1
    query = mock_conn.execute.call_args[0][0]
    assert "capability_counts" in query
    assert "limitation_counts" in query
    assert "LEFT JOIN capabilities c ON t.id = c.theme_id" not in query


def test_module_importable():
    from retrieval import landscape
    assert hasattr(landscape, "get_theme_state")
    assert hasattr(landscape, "get_recent_breakthroughs")
    assert hasattr(landscape, "get_bottleneck_ranking")
    assert hasattr(landscape, "compute_theme_velocity")
    assert hasattr(landscape, "update_all_theme_velocities")
    assert hasattr(landscape, "get_anticipations_with_evidence")
    assert hasattr(landscape, "get_limitation_validation_rates")
