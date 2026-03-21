"""Integration tests for Phase 4 belief system components.

Tests the tournament belief weighting, landscape belief queries,
and cross-module interactions.
"""

import yaml
from unittest.mock import patch, MagicMock


# --- Tournament Belief Weighting ---

def test_tournament_belief_weighting_no_conn():
    """Belief weighting should be a no-op without a DB connection."""
    from agents.tournament import TournamentPipeline
    from agents.executor import ClaudeExecutor

    executor = MagicMock(spec=ClaudeExecutor)
    pipeline = TournamentPipeline(executor, get_conn_fn=None)

    ideas = [{"idea_text": "Test idea about scaling", "overall_score": 0.5}]
    result = pipeline._apply_belief_weighting(ideas)
    assert result[0]["overall_score"] == 0.5  # Unchanged


def test_tournament_belief_weighting_no_open_beliefs():
    """Belief weighting should be a no-op when no open-question beliefs exist."""
    from agents.tournament import TournamentPipeline
    from agents.executor import ClaudeExecutor

    executor = MagicMock(spec=ClaudeExecutor)
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    pipeline = TournamentPipeline(executor, get_conn_fn=lambda: mock_conn)

    ideas = [{"idea_text": "Test idea", "overall_score": 0.5}]

    with patch("reading_app.db.get_low_confidence_beliefs", return_value=[]):
        result = pipeline._apply_belief_weighting(ideas)
    assert result[0]["overall_score"] == 0.5


def test_tournament_belief_weighting_boost_applied():
    """Ideas matching open-question beliefs should get a score boost."""
    from agents.tournament import TournamentPipeline
    from agents.executor import ClaudeExecutor

    executor = MagicMock(spec=ClaudeExecutor)
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    pipeline = TournamentPipeline(executor, get_conn_fn=lambda: mock_conn)

    ideas = [
        {"idea_text": "New approach to scaling laws compute efficiency training", "overall_score": 0.5},
        {"idea_text": "Completely unrelated topic about cats", "overall_score": 0.5},
    ]

    open_beliefs = [
        {"claim": "Scaling laws for compute efficiency will continue through larger training runs", "confidence": 0.3},
    ]

    with patch("reading_app.db.get_low_confidence_beliefs", return_value=open_beliefs):
        result = pipeline._apply_belief_weighting(ideas)

    # First idea should be boosted (matches scaling/compute/training keywords)
    assert result[0].get("belief_boost_applied", False) is True
    assert result[0]["overall_score"] > 0.5
    # Second idea should not be boosted
    assert result[1].get("belief_boost_applied", False) is False
    assert result[1]["overall_score"] == 0.5


def test_tournament_belief_weighting_caps_at_1():
    """Belief boost should not push score above 1.0."""
    from agents.tournament import TournamentPipeline
    from agents.executor import ClaudeExecutor

    executor = MagicMock(spec=ClaudeExecutor)
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    pipeline = TournamentPipeline(executor, get_conn_fn=lambda: mock_conn)

    ideas = [
        {"idea_text": "Scaling laws compute training efficiency models future", "overall_score": 0.95},
    ]

    open_beliefs = [
        {"claim": "Scaling laws for compute efficiency will continue through training of future models", "confidence": 0.4},
    ]

    with patch("reading_app.db.get_low_confidence_beliefs", return_value=open_beliefs):
        result = pipeline._apply_belief_weighting(ideas)

    assert result[0]["overall_score"] <= 1.0


# --- Schema Migration ---

def test_migration_006_exists():
    """Migration file for beliefs table should exist."""
    from pathlib import Path
    migration = Path("db/migrations/006_beliefs.sql")
    assert migration.exists()
    content = migration.read_text()
    assert "CREATE TABLE" in content
    assert "beliefs" in content
    assert "belief_type" in content
    assert "domain_theme_id" in content
    assert "derived_anticipations" in content
    assert "parent_belief_id" in content


# --- Skills Registry ---

def test_challenge_skill_in_registry():
    """Challenge skill should be registered."""
    import yaml
    from pathlib import Path
    registry = yaml.safe_load(Path("skills/registry.yaml").read_text())
    assert "challenge" in registry["skills"]
    assert registry["skills"]["challenge"]["prompt"] == "prompts/challenge.md"


def test_challenge_prompt_exists():
    """Challenge skill prompt should exist."""
    from pathlib import Path
    assert Path("skills/prompts/challenge.md").exists()


# ===========================================================================
# NEW VERIFICATION TESTS
# ===========================================================================

# --- DB function signatures (Task 3) ---

def test_db_belief_functions_exist():
    """All 18 belief-related DB functions should be importable and callable."""
    from reading_app import db

    expected = [
        "insert_belief",
        "get_belief",
        "get_active_beliefs",
        "get_beliefs_for_theme",
        "get_beliefs_by_type",
        "list_beliefs",
        "update_belief_confidence",
        "update_belief_status",
        "append_belief_evidence",
        "append_belief_landscape_link",
        "append_belief_derived_anticipation",
        "find_similar_belief",
        "get_stale_beliefs",
        "get_low_confidence_beliefs",
        "get_unchallenged_beliefs",
        "get_belief_pairs_for_consistency",
        "insert_challenge_log",
    ]
    for name in expected:
        fn = getattr(db, name, None)
        assert fn is not None, f"db.{name} not found"
        assert callable(fn), f"db.{name} is not callable"


# --- Migration/schema consistency (Task 2) ---

def test_migration_006_matches_schema():
    """Migration 006 and schema.sql should contain the same belief columns."""
    import re as _re
    from pathlib import Path

    def _normalise(text: str) -> str:
        """Collapse runs of whitespace to single space for comparison."""
        return _re.sub(r"\s+", " ", text)

    migration = _normalise(Path("db/migrations/006_beliefs.sql").read_text())
    schema = _normalise(Path("db/schema.sql").read_text())

    required_fragments = [
        "claim TEXT NOT NULL",
        "confidence FLOAT NOT NULL DEFAULT 0.5",
        "belief_type TEXT DEFAULT",
        "domain_theme_id TEXT",
        "landscape_links JSONB",
        "evidence_for JSONB",
        "evidence_against JSONB",
        "derived_anticipations JSONB",
        "parent_belief_id TEXT",
        "history JSONB",
    ]

    for frag in required_fragments:
        assert frag in migration, f"Migration missing: {frag}"
        assert frag in schema, f"Schema missing: {frag}"


# --- Retrieval return structures (Task 6) ---

def test_get_belief_coverage_gaps_return_structure():
    """get_belief_coverage_gaps should return dict with expected keys."""
    from retrieval.landscape import get_belief_coverage_gaps

    with patch("reading_app.db.get_low_confidence_beliefs", return_value=[]), \
         patch("reading_app.db.get_unchallenged_beliefs", return_value=[]), \
         patch("reading_app.db.get_conn"):
        result = get_belief_coverage_gaps()

    assert isinstance(result, dict)
    assert "low_confidence_gaps" in result
    assert "unchallenged_beliefs" in result
    assert isinstance(result["low_confidence_gaps"], list)
    assert isinstance(result["unchallenged_beliefs"], list)


# --- Tournament weighting (Task 7) ---

def test_tournament_belief_weighting_stop_words_filtered():
    """Stop-word-only beliefs should not trigger a boost."""
    from agents.tournament import TournamentPipeline
    from agents.executor import ClaudeExecutor

    executor = MagicMock(spec=ClaudeExecutor)
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    pipeline = TournamentPipeline(executor, get_conn_fn=lambda: mock_conn)

    ideas = [{"idea_text": "the is for and to", "overall_score": 0.5}]
    open_beliefs = [
        {"claim": "the is for and to with at as but", "confidence": 0.3},
    ]

    with patch("reading_app.db.get_low_confidence_beliefs", return_value=open_beliefs):
        result = pipeline._apply_belief_weighting(ideas)

    assert result[0].get("belief_boost_applied", False) is False
    assert result[0]["overall_score"] == 0.5


# --- Challenge log and prompts (Task 8) ---

def test_challenge_log_table_in_schema():
    """schema.sql should contain challenge_log table with required columns."""
    from pathlib import Path

    schema = Path("db/schema.sql").read_text()
    assert "challenge_log" in schema
    assert "entity_type" in schema
    assert "system_position" in schema
    assert "user_argument" in schema
    assert "outcome" in schema
    assert "belief_id" in schema


def test_beliefs_prompt_has_frontmatter():
    """beliefs.md should have valid YAML frontmatter with name and description."""
    from pathlib import Path

    content = Path("skills/prompts/beliefs.md").read_text(encoding="utf-8")
    assert content.startswith("---"), "beliefs.md must start with YAML frontmatter"
    # Extract frontmatter between first and second '---'
    parts = content.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])
    assert frontmatter["name"] == "beliefs"
    assert "description" in frontmatter


def test_beliefs_prompt_has_5_modes():
    """beliefs.md should document all 5 modes."""
    from pathlib import Path

    content = Path("skills/prompts/beliefs.md").read_text(encoding="utf-8")
    for mode in ["Mode: List", "Mode: Add", "Mode: Update", "Mode: Review", "Mode: Synthesis"]:
        assert mode in content, f"beliefs.md missing '{mode}'"


def test_challenge_prompt_has_belief_mode():
    """challenge.md should support belief self-challenge with steelman."""
    from pathlib import Path

    content = Path("skills/prompts/challenge.md").read_text(encoding="utf-8")
    assert "Belief Self-Challenge" in content
    assert "steelman" in content.lower()


def test_beliefs_skill_in_registry():
    """beliefs skill should be registered with correct prompt."""
    from pathlib import Path

    registry = yaml.safe_load(Path("skills/registry.yaml").read_text())
    assert "beliefs" in registry["skills"]
    assert registry["skills"]["beliefs"]["prompt"] == "prompts/beliefs.md"
