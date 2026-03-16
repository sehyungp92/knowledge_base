"""Tests for Priority 3 synthesis UX and performance route changes."""

from unittest.mock import MagicMock, patch


def _mock_conn(fetchone_values=None, fetchall_values=None):
    conn = MagicMock()
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    execute_result = MagicMock()
    execute_result.fetchone.side_effect = fetchone_values or []
    execute_result.fetchall.side_effect = fetchall_values or []
    conn.execute.return_value = execute_result
    return conn


def test_briefing_uses_cache_for_default_requests():
    from webapp.api.routers import landscape as landscape_router

    landscape_router._briefing_cache["payload"] = None
    landscape_router._briefing_cache["generated_at"] = None
    landscape_router._briefing_cache["expires_at"] = 0.0

    payload = {
        "recent_sources": [],
        "breakthroughs": [],
        "attention_signals": {
            "stale_beliefs": [],
            "anticipations_with_evidence": [],
            "over_optimistic_themes": [],
            "blind_spot_bottlenecks": [],
        },
        "highest_movement": [],
        "reading_recommendations": [],
    }

    with patch("webapp.api.routers.landscape._build_briefing_payload", return_value=payload) as build_payload:
        first = landscape_router.briefing(None, False)
        second = landscape_router.briefing(None, False)

    assert build_payload.call_count == 1
    assert first["meta"]["cached"] is False
    assert second["meta"]["cached"] is True


def test_theme_synthesis_returns_compact_overview():
    with patch("webapp.api.routers.landscape._theme_exists", return_value={"id": "robotics", "name": "Robotics"}), \
         patch("webapp.api.routers.landscape._fetch_theme_counts", return_value={"sources": 8}), \
         patch("webapp.api.routers.landscape._fetch_theme_previews", return_value={"authoritative_sources": []}), \
         patch("webapp.api.routers.landscape._build_theme_overview", return_value={"top_takeaways": [], "key_tensions": [], "strongest_evidence": []}):
        from webapp.api.routers.landscape import theme_synthesis

        result = theme_synthesis("robotics")

    assert result["theme"]["id"] == "robotics"
    assert "counts" in result
    assert "overview" in result
    assert "previews" in result
    assert "beliefs" not in result


def test_theme_synthesis_section_paginates_capabilities():
    conn = _mock_conn(
        fetchone_values=[{"cnt": 3}],
        fetchall_values=[[{"id": "cap_1", "description": "Generalises across tasks", "evidence_sources": ["src_1"]}]],
    )

    with patch("webapp.api.routers.landscape._theme_exists", return_value={"id": "agents"}), \
         patch("webapp.api.routers.landscape.db.get_conn", return_value=conn), \
         patch(
             "webapp.api.routers.landscape._attach_resolved_sources",
             return_value=[{"id": "cap_1", "description": "Generalises across tasks", "resolved_sources": [{"id": "src_1", "title": "Source 1"}]}],
         ):
        from webapp.api.routers.landscape import theme_synthesis_section

        result = theme_synthesis_section("agents", "capabilities", limit=1, offset=0)

    assert result["section"] == "capabilities"
    assert result["total"] == 3
    assert result["has_more"] is True
    assert result["items"][0]["resolved_sources"][0]["title"] == "Source 1"


def test_get_source_returns_compact_overview():
    conn = _mock_conn(
        fetchone_values=[{
            "claim_count": 12,
            "related_count": 4,
            "capability_count": 2,
            "limitation_count": 1,
            "bottleneck_count": 1,
            "breakthrough_count": 0,
        }],
        fetchall_values=[
            [{"id": "theme_1", "name": "Agents"}],
            [{"id": "concept_1", "canonical_name": "Tool use", "concept_type": "capability"}],
        ],
    )

    with patch("webapp.api.routers.library.db.get_source", return_value={"id": "src_1", "title": "Example", "library_path": "library"}), \
         patch("webapp.api.routers.library.db.get_conn", return_value=conn), \
         patch("webapp.api.routers.library._artifact_flags", return_value={"has_summary": True, "has_reflection": False}):
        from webapp.api.routers.library import get_source

        result = get_source("src_1")

    assert result["counts"]["claims"] == 12
    assert result["counts"]["landscape_signals"]["capabilities"] == 2
    assert result["artifacts"]["has_summary"] is True
    assert result["themes"][0]["name"] == "Agents"


def test_get_source_claims_paginates():
    conn = _mock_conn(
        fetchone_values=[{"cnt": 5}],
        fetchall_values=[[{"id": "claim_1", "claim_text": "A key claim"}]],
    )

    with patch("webapp.api.routers.library._get_source_or_404", return_value={"id": "src_1"}), \
         patch("webapp.api.routers.library.db.get_conn", return_value=conn):
        from webapp.api.routers.library import get_source_claims

        result = get_source_claims("src_1", limit=1, offset=0)

    assert result["total"] == 5
    assert result["has_more"] is True
    assert result["items"][0]["claim_text"] == "A key claim"
