"""PostgreSQL + pgvector + FTS access layer."""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)

_pool: ConnectionPool | None = None


def init_pool(dsn: str, min_size: int = 2, max_size: int = 10):
    """Initialize the connection pool."""
    global _pool
    if _pool is not None:
        _pool.close()
    _pool = ConnectionPool(
        dsn,
        min_size=min_size,
        max_size=max_size,
        open=True,
        kwargs={"row_factory": dict_row},
    )


def ensure_pool() -> None:
    """Ensure the connection pool is initialised, auto-creating from env if needed.

    Safe to call multiple times — no-op if pool already exists.
    """
    if _pool is not None:
        return
    from reading_app.config import Config
    cfg = Config()
    init_pool(cfg.postgres_dsn)
    logger.info("Auto-initialised DB pool from env vars")


def close_pool():
    """Close the connection pool."""
    global _pool
    if _pool:
        _pool.close()
        _pool = None


@contextmanager
def get_conn():
    """Get a connection from the pool."""
    if _pool is None:
        raise RuntimeError("Connection pool not initialized. Call init_pool() first.")
    with _pool.connection() as conn:
        yield conn


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

def find_source_by_url(url: str) -> dict | None:
    """Check if a source with the given URL already exists.

    Compares both raw and normalized URLs (strips www., trailing slash).
    Returns the existing source row or None.
    """
    if not url:
        return None
    normalized = url.strip().rstrip("/").replace("www.", "")
    with get_conn() as conn:
        row = conn.execute(
            """SELECT id, title, url, source_type, processing_status
               FROM sources
               WHERE url = %s
                  OR REPLACE(RTRIM(url, '/'), 'www.', '') = %s
               LIMIT 1""",
            (url, normalized),
        ).fetchone()
        return row


def insert_source(
    id: str,
    source_type: str,
    title: str,
    url: str | None = None,
    authors: list[str] | None = None,
    published_at: datetime | str | None = None,
    abstract: str | None = None,
    library_path: str | None = None,
    processing_status: str = "pending",
    metadata: dict | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO sources (id, source_type, title, url, authors, published_at,
               abstract, library_path, processing_status, metadata)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 title = EXCLUDED.title,
                 processing_status = EXCLUDED.processing_status,
                 metadata = EXCLUDED.metadata
               RETURNING *""",
            (id, source_type, title, url, json.dumps(authors) if authors else None,
             published_at, abstract, library_path, processing_status,
             json.dumps(metadata) if metadata else None),
        ).fetchone()
        conn.commit()
        return row


def update_source_authors(source_id: str, authors: list[str]) -> None:
    """Update the authors field for an existing source."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE sources SET authors = %s WHERE id = %s",
            (json.dumps(authors), source_id),
        )
        conn.commit()


def get_source(source_id: str) -> dict | None:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM sources WHERE id = %s", (source_id,)
        ).fetchone()


def list_sources(
    source_type: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    with get_conn() as conn:
        conditions = []
        params: list[Any] = []
        if source_type:
            conditions.append("source_type = %s")
            params.append(source_type)
        if status:
            conditions.append("processing_status = %s")
            params.append(status)
        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        params.extend([limit, offset])
        return conn.execute(
            f"SELECT * FROM sources {where} ORDER BY ingested_at DESC LIMIT %s OFFSET %s",
            params,
        ).fetchall()


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------

def insert_claim(
    id: str,
    source_id: str,
    claim_text: str,
    claim_type: str | None = None,
    section: str | None = None,
    confidence: float | None = None,
    evidence_snippet: str | None = None,
    evidence_location: str | None = None,
    evidence_type: str | None = None,
    embedding: list[float] | None = None,
    temporal_scope: str | None = None,
    provenance_type: str = "extracted",
    evidence_validation: str | None = None,
) -> dict:
    # Validate temporal_scope
    valid_scopes = {"current_state", "historical", "future_prediction"}
    if temporal_scope and temporal_scope not in valid_scopes:
        temporal_scope = None
    # Validate provenance_type
    valid_provenance = {"extracted", "generated", "synthesis"}
    if provenance_type not in valid_provenance:
        provenance_type = "extracted"
    with get_conn() as conn:
        emb_str = str(embedding) if embedding else None
        row = conn.execute(
            """INSERT INTO claims (id, source_id, claim_text, claim_type, section,
               confidence, evidence_snippet, evidence_location, evidence_type,
               embedding, temporal_scope, provenance_type, evidence_validation)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 claim_text = EXCLUDED.claim_text,
                 confidence = EXCLUDED.confidence,
                 embedding = EXCLUDED.embedding,
                 temporal_scope = EXCLUDED.temporal_scope,
                 provenance_type = EXCLUDED.provenance_type,
                 evidence_validation = EXCLUDED.evidence_validation
               RETURNING *""",
            (id, source_id, claim_text, claim_type, section,
             confidence, evidence_snippet, evidence_location, evidence_type,
             emb_str, temporal_scope, provenance_type, evidence_validation),
        ).fetchone()
        conn.commit()
        return row


def get_claims_for_source(source_id: str) -> list[dict]:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM claims WHERE source_id = %s ORDER BY section, confidence DESC",
            (source_id,),
        ).fetchall()


# ---------------------------------------------------------------------------
# Concepts
# ---------------------------------------------------------------------------

def insert_concept(
    id: str,
    canonical_name: str,
    concept_type: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
    external_ids: dict | None = None,
    embedding: list[float] | None = None,
) -> dict:
    with get_conn() as conn:
        emb_str = str(embedding) if embedding else None
        row = conn.execute(
            """INSERT INTO concepts (id, canonical_name, concept_type, description,
               aliases, external_ids, embedding)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 canonical_name = EXCLUDED.canonical_name,
                 description = EXCLUDED.description,
                 aliases = EXCLUDED.aliases
               RETURNING *""",
            (id, canonical_name, concept_type, description,
             json.dumps(aliases) if aliases else None,
             json.dumps(external_ids) if external_ids else None,
             emb_str),
        ).fetchone()
        conn.commit()
        return row


def get_or_create_concept(
    canonical_name: str,
    concept_type: str | None = None,
    description: str | None = None,
    aliases: list[str] | None = None,
) -> str:
    """Find existing concept by name+type, or create new one. Returns concept_id."""
    from ulid import ULID

    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM concepts WHERE lower(canonical_name) = lower(%s) AND COALESCE(concept_type, '') = COALESCE(%s, '')",
            (canonical_name, concept_type),
        ).fetchone()
        if existing:
            return existing["id"]
        concept_id = f"con_{ULID()}"
        conn.execute(
            "INSERT INTO concepts (id, canonical_name, concept_type, description, aliases) VALUES (%s, %s, %s, %s, %s)",
            (concept_id, canonical_name, concept_type, description,
             json.dumps(aliases) if aliases else None),
        )
        conn.commit()
        return concept_id


# ---------------------------------------------------------------------------
# Graph edges
# ---------------------------------------------------------------------------

def insert_source_edge(
    source_a: str,
    source_b: str,
    edge_type: str,
    explanation: str | None = None,
    evidence_a: str | None = None,
    evidence_b: str | None = None,
    confidence: float | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO source_edges (source_a, source_b, edge_type, explanation,
               evidence_a, evidence_b, confidence)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (source_a, source_b, edge_type) DO UPDATE SET
                 explanation = EXCLUDED.explanation,
                 confidence = EXCLUDED.confidence,
                 evidence_a = EXCLUDED.evidence_a,
                 evidence_b = EXCLUDED.evidence_b
               RETURNING *""",
            (source_a, source_b, edge_type, explanation, evidence_a, evidence_b, confidence),
        ).fetchone()
        conn.commit()
        return row


def insert_source_concept(
    source_id: str,
    concept_id: str,
    relationship: str,
    confidence: float | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO source_concepts (source_id, concept_id, relationship, confidence)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (source_id, concept_id, relationship) DO UPDATE SET
                 confidence = EXCLUDED.confidence
               RETURNING *""",
            (source_id, concept_id, relationship, confidence),
        ).fetchone()
        conn.commit()
        return row


def insert_claim_edge(*args, **kwargs) -> dict:
    """Legacy compatibility shim for removed claim-edge writes.

    Claim-edge persistence was removed in migration 017. Keep a named entry
    point so older code fails with a clear explanation instead of an
    AttributeError during import-time capability checks.
    """
    raise NotImplementedError(
        "insert_claim_edge() is no longer supported because the claim_edges table "
        "was removed in migration 017. Use source-level graph edges or "
        "retrieval-time claim comparison instead."
    )


# ---------------------------------------------------------------------------
# Ideas
# ---------------------------------------------------------------------------

def insert_idea(
    id: str,
    idea_text: str,
    idea_type: str | None = None,
    grounding: dict | None = None,
    testability: str | None = None,
    novelty_score: float | None = None,
    feasibility_score: float | None = None,
    impact_score: float | None = None,
    overall_score: float | None = None,
    similar_existing_ideas: list | None = None,
    novelty_check_passed: bool | None = None,
    generation_context: dict | None = None,
    parent_idea_id: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO ideas (id, idea_text, idea_type, grounding, testability,
               novelty_score, feasibility_score, impact_score, overall_score,
               similar_existing_ideas, novelty_check_passed, generation_context, parent_idea_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 overall_score = EXCLUDED.overall_score,
                 novelty_check_passed = EXCLUDED.novelty_check_passed
               RETURNING *""",
            (id, idea_text, idea_type,
             json.dumps(grounding) if grounding else None,
             testability, novelty_score, feasibility_score, impact_score, overall_score,
             json.dumps(similar_existing_ideas) if similar_existing_ideas else None,
             novelty_check_passed,
             json.dumps(generation_context) if generation_context else None,
             parent_idea_id),
        ).fetchone()
        conn.commit()
        return row


def get_ideas_for_source(source_id: str) -> list[dict]:
    """Get ideas grounded in a specific source."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT * FROM ideas
               WHERE grounding::text LIKE %s
               ORDER BY overall_score DESC NULLS LAST""",
            (f"%{source_id}%",),
        ).fetchall()


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

def insert_theme(
    id: str,
    name: str,
    description: str | None = None,
    state_summary: str | None = None,
    velocity: float | None = None,
    level: int = 1,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO themes (id, name, description, state_summary, velocity, level)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING
               RETURNING *""",
            (id, name, description, state_summary, velocity, level),
        ).fetchone()
        conn.commit()
        return row


def get_themes_by_level(level: int) -> list[dict]:
    """Get all themes at a specific hierarchy level (0=meta, 1=subtheme, 2=subsubtheme)."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM themes WHERE level = %s ORDER BY id",
            (level,),
        ).fetchall()


def get_parent_theme(child_id: str) -> dict | None:
    """Get the level-1 parent of a theme via theme_edges (relationship='contains')."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT t.* FROM themes t
               JOIN theme_edges te ON te.parent_id = t.id
               WHERE te.child_id = %s AND te.relationship = 'contains'
               ORDER BY t.level DESC
               LIMIT 1""",
            (child_id,),
        ).fetchone()


def insert_theme_edge(
    parent_id: str,
    child_id: str,
    relationship: str = "contains",
    strength: float | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (parent_id, child_id) DO NOTHING
               RETURNING *""",
            (parent_id, child_id, relationship, strength),
        ).fetchone()
        conn.commit()
        return row


def insert_source_theme(
    source_id: str,
    theme_id: str,
    relevance: float = 1.0,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO source_themes (source_id, theme_id, relevance)
               VALUES (%s, %s, %s)
               ON CONFLICT (source_id, theme_id) DO UPDATE SET
                 relevance = EXCLUDED.relevance
               RETURNING *""",
            (source_id, theme_id, relevance),
        ).fetchone()
        conn.commit()
        return row


def insert_cross_theme_implication(
    id: str,
    source_theme_id: str,
    target_theme_id: str,
    trigger_type: str,
    trigger_id: str,
    implication: str,
    confidence: float | None = None,
    evidence_sources: list | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO cross_theme_implications
               (id, source_theme_id, target_theme_id, trigger_type, trigger_id,
                implication, confidence, evidence_sources, attribution, attributed_reasoning)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 implication = EXCLUDED.implication,
                 confidence = EXCLUDED.confidence,
                 evidence_sources = COALESCE(
                   cross_theme_implications.evidence_sources::jsonb || EXCLUDED.evidence_sources::jsonb,
                   EXCLUDED.evidence_sources
                 )
               RETURNING *""",
            (id, source_theme_id, target_theme_id, trigger_type, trigger_id,
             implication, confidence,
             json.dumps(evidence_sources) if evidence_sources else None,
             attribution, attributed_reasoning),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Capabilities
# ---------------------------------------------------------------------------

def insert_capability(
    id: str,
    theme_id: str,
    description: str,
    maturity: str | None = None,
    confidence: float | None = None,
    evidence_sources: list | None = None,
    first_demonstrated_at: str | None = None,
    production_ready_at: str | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO capabilities
               (id, theme_id, description, maturity, confidence, evidence_sources,
                first_demonstrated_at, production_ready_at, attribution, attributed_reasoning)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 description = EXCLUDED.description,
                 maturity = COALESCE(EXCLUDED.maturity, capabilities.maturity),
                 evidence_sources = COALESCE(EXCLUDED.evidence_sources, capabilities.evidence_sources),
                 first_demonstrated_at = COALESCE(EXCLUDED.first_demonstrated_at, capabilities.first_demonstrated_at),
                 production_ready_at = COALESCE(EXCLUDED.production_ready_at, capabilities.production_ready_at),
                 confidence = EXCLUDED.confidence,
                 last_updated = NOW()
               RETURNING *""",
            (id, theme_id, description, maturity, confidence,
             json.dumps(evidence_sources) if evidence_sources else None,
             first_demonstrated_at, production_ready_at,
             attribution, attributed_reasoning),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------------

def insert_limitation(
    id: str,
    theme_id: str,
    description: str,
    limitation_type: str | None = None,
    signal_type: str | None = None,
    severity: str | None = None,
    trajectory: str | None = None,
    confidence: float | None = None,
    evidence_sources: list | None = None,
    underlying_reason: str | None = None,
    bottleneck_id: str | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO limitations
               (id, theme_id, description, limitation_type, signal_type, severity,
                trajectory, confidence, evidence_sources, underlying_reason,
                bottleneck_id, attribution, attributed_reasoning)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 description = EXCLUDED.description,
                 limitation_type = COALESCE(EXCLUDED.limitation_type, limitations.limitation_type),
                 signal_type = COALESCE(EXCLUDED.signal_type, limitations.signal_type),
                 severity = COALESCE(EXCLUDED.severity, limitations.severity),
                 trajectory = COALESCE(EXCLUDED.trajectory, limitations.trajectory),
                 underlying_reason = COALESCE(EXCLUDED.underlying_reason, limitations.underlying_reason),
                 bottleneck_id = COALESCE(EXCLUDED.bottleneck_id, limitations.bottleneck_id),
                 evidence_sources = COALESCE(EXCLUDED.evidence_sources, limitations.evidence_sources),
                 confidence = EXCLUDED.confidence,
                 last_updated = NOW()
               RETURNING *""",
            (id, theme_id, description, limitation_type, signal_type, severity,
             trajectory, confidence,
             json.dumps(evidence_sources) if evidence_sources else None,
             underlying_reason, bottleneck_id, attribution, attributed_reasoning),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Bottlenecks
# ---------------------------------------------------------------------------

def insert_bottleneck(
    id: str,
    theme_id: str,
    description: str,
    blocking_what: str | None = None,
    bottleneck_type: str | None = None,
    resolution_horizon: str | None = None,
    active_approaches: list | None = None,
    evidence_sources: list | None = None,
    confidence: float | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO bottlenecks
               (id, theme_id, description, blocking_what, bottleneck_type,
                resolution_horizon, active_approaches, evidence_sources,
                confidence, attribution, attributed_reasoning)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 description = EXCLUDED.description,
                 blocking_what = COALESCE(EXCLUDED.blocking_what, bottlenecks.blocking_what),
                 bottleneck_type = COALESCE(EXCLUDED.bottleneck_type, bottlenecks.bottleneck_type),
                 resolution_horizon = COALESCE(EXCLUDED.resolution_horizon, bottlenecks.resolution_horizon),
                 active_approaches = COALESCE(EXCLUDED.active_approaches, bottlenecks.active_approaches),
                 evidence_sources = COALESCE(EXCLUDED.evidence_sources, bottlenecks.evidence_sources),
                 confidence = EXCLUDED.confidence,
                 last_updated = NOW()
               RETURNING *""",
            (id, theme_id, description, blocking_what, bottleneck_type,
             resolution_horizon,
             json.dumps(active_approaches) if active_approaches else None,
             json.dumps(evidence_sources) if evidence_sources else None,
             confidence, attribution, attributed_reasoning),
        ).fetchone()
        conn.commit()
        return row


def get_bottleneck(bottleneck_id: str) -> dict | None:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM bottlenecks WHERE id = %s", (bottleneck_id,)
        ).fetchone()


def update_bottleneck(
    bottleneck_id: str,
    resolution_horizon: str | None = None,
    active_approaches: list | None = None,
    **kwargs,
) -> dict | None:
    sets, params = [], []
    if resolution_horizon is not None:
        sets.append("resolution_horizon = %s")
        params.append(resolution_horizon)
    if active_approaches is not None:
        sets.append("active_approaches = %s")
        params.append(json.dumps(active_approaches))
    for k, v in kwargs.items():
        sets.append(f"{k} = %s")
        params.append(v)
    if not sets:
        return get_bottleneck(bottleneck_id)
    sets.append("last_updated = NOW()")
    params.append(bottleneck_id)
    with get_conn() as conn:
        row = conn.execute(
            f"UPDATE bottlenecks SET {', '.join(sets)} WHERE id = %s RETURNING *",
            params,
        ).fetchone()
        conn.commit()
        return row


def append_bottleneck_approach(bottleneck_id: str, approach: dict) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE bottlenecks
               SET active_approaches = COALESCE(active_approaches, '[]'::jsonb) || %s::jsonb,
                   last_updated = NOW()
               WHERE id = %s
               RETURNING *""",
            (json.dumps(approach), bottleneck_id),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Breakthroughs
# ---------------------------------------------------------------------------

def insert_breakthrough(
    id: str,
    theme_id: str,
    description: str,
    significance: str | None = None,
    what_was_believed_before: str | None = None,
    what_is_now_possible: str | None = None,
    immediate_implications: list | None = None,
    downstream_implications: list | None = None,
    bottlenecks_affected: list | None = None,
    primary_source_id: str | None = None,
    corroborating_sources: list | None = None,
    confidence: float | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO breakthroughs
               (id, theme_id, description, significance, what_was_believed_before,
                what_is_now_possible, immediate_implications, downstream_implications,
                bottlenecks_affected, primary_source_id, corroborating_sources,
                confidence, attribution, attributed_reasoning)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 description = EXCLUDED.description,
                 significance = COALESCE(EXCLUDED.significance, breakthroughs.significance),
                 what_was_believed_before = COALESCE(EXCLUDED.what_was_believed_before, breakthroughs.what_was_believed_before),
                 what_is_now_possible = COALESCE(EXCLUDED.what_is_now_possible, breakthroughs.what_is_now_possible),
                 immediate_implications = COALESCE(EXCLUDED.immediate_implications, breakthroughs.immediate_implications),
                 downstream_implications = COALESCE(EXCLUDED.downstream_implications, breakthroughs.downstream_implications),
                 bottlenecks_affected = COALESCE(EXCLUDED.bottlenecks_affected, breakthroughs.bottlenecks_affected),
                 corroborating_sources = COALESCE(EXCLUDED.corroborating_sources, breakthroughs.corroborating_sources),
                 confidence = EXCLUDED.confidence
               RETURNING *""",
            (id, theme_id, description, significance, what_was_believed_before,
             what_is_now_possible,
             json.dumps(immediate_implications) if immediate_implications else None,
             json.dumps(downstream_implications) if downstream_implications else None,
             json.dumps(bottlenecks_affected) if bottlenecks_affected else None,
             primary_source_id,
             json.dumps(corroborating_sources) if corroborating_sources else None,
             confidence, attribution, attributed_reasoning),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Anticipations
# ---------------------------------------------------------------------------

def insert_anticipation(
    id: str,
    theme_id: str,
    prediction: str,
    based_on: list | None = None,
    reasoning: str | None = None,
    confidence: float | None = None,
    timeline: str | None = None,
    attribution: str = "automated_extraction",
    attributed_reasoning: str | None = None,
    would_confirm: str | None = None,
    would_invalidate: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO anticipations
               (id, theme_id, prediction, based_on, reasoning,
                confidence, timeline, attribution, attributed_reasoning,
                would_confirm, would_invalidate)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 prediction = EXCLUDED.prediction,
                 based_on = COALESCE(EXCLUDED.based_on, anticipations.based_on),
                 reasoning = COALESCE(EXCLUDED.reasoning, anticipations.reasoning),
                 timeline = COALESCE(EXCLUDED.timeline, anticipations.timeline),
                 would_confirm = COALESCE(EXCLUDED.would_confirm, anticipations.would_confirm),
                 would_invalidate = COALESCE(EXCLUDED.would_invalidate, anticipations.would_invalidate),
                 confidence = EXCLUDED.confidence
               RETURNING *""",
            (id, theme_id, prediction,
             json.dumps(based_on) if based_on else None,
             reasoning, confidence, timeline, attribution, attributed_reasoning,
             would_confirm, would_invalidate),
        ).fetchone()
        conn.commit()
        return row


def get_anticipation(anticipation_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM anticipations WHERE id = %s", (anticipation_id,)
        ).fetchone()
        if row and isinstance(row.get("status_evidence"), str):
            row["status_evidence"] = json.loads(row["status_evidence"])
        return row


def get_open_anticipations_for_themes(theme_ids: list[str]) -> list[dict]:
    with get_conn() as conn:
        return conn.execute(
            """SELECT a.*, t.name AS theme_name
               FROM anticipations a
               JOIN themes t ON a.theme_id = t.id
               WHERE a.status = 'open'
                 AND (a.theme_id = ANY(%s)
                      OR a.theme_id IN (
                          SELECT target_theme_id FROM cross_theme_implications
                          WHERE source_theme_id = ANY(%s)
                      ))
               ORDER BY a.confidence DESC""",
            (theme_ids, theme_ids),
        ).fetchall()


def append_anticipation_evidence(anticipation_id: str, evidence: dict) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE anticipations
               SET status_evidence = COALESCE(status_evidence, '[]'::jsonb) || %s::jsonb,
                   last_reviewed = NOW()
               WHERE id = %s
               RETURNING *""",
            (json.dumps([evidence]), anticipation_id),
        ).fetchone()
        conn.commit()
        if row and isinstance(row.get("status_evidence"), str):
            row["status_evidence"] = json.loads(row["status_evidence"])
        return row


def update_anticipation_status(anticipation_id: str, status: str) -> dict | None:
    """Update an anticipation's status (e.g. to 'expired')."""
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE anticipations SET status = %s, last_reviewed = NOW()
               WHERE id = %s RETURNING *""",
            (status, anticipation_id),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Challenge Log
# ---------------------------------------------------------------------------

def insert_challenge_log(
    id: str,
    entity_type: str,
    entity_id: str,
    system_position: str | None = None,
    system_evidence: list | None = None,
    user_argument: str | None = None,
    user_evidence: list | None = None,
    outcome: str | None = None,
    resolution_reasoning: str | None = None,
    changes_made: list | None = None,
    belief_id: str | None = None,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO challenge_log
               (id, entity_type, entity_id, system_position, system_evidence,
                user_argument, user_evidence, outcome, resolution_reasoning,
                changes_made, belief_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING *""",
            (id, entity_type, entity_id, system_position,
             json.dumps(system_evidence) if system_evidence else None,
             user_argument,
             json.dumps(user_evidence) if user_evidence else None,
             outcome, resolution_reasoning,
             json.dumps(changes_made) if changes_made else None,
             belief_id),
        ).fetchone()
        conn.commit()
        return row


# ---------------------------------------------------------------------------
# Theme Proposals
# ---------------------------------------------------------------------------

def insert_theme_proposal(
    id: str,
    proposed_theme_id: str,
    name: str,
    description: str,
    trigger_reason: str,
    parent_id: str | None = None,
    suggested_edges: list | None = None,
    source_id: str | None = None,
    level: int = 2,
) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO theme_proposals
               (id, proposed_theme_id, name, description, trigger_reason,
                parent_id, suggested_edges, source_id, level)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING *""",
            (id, proposed_theme_id, name, description, trigger_reason,
             parent_id,
             json.dumps(suggested_edges) if suggested_edges else "[]",
             source_id, level),
        ).fetchone()
        conn.commit()
        return row


def materialize_theme_proposal(proposal_id: str) -> dict:
    """Approve a theme proposal and insert it into the live taxonomy.

    Single transaction:
    1. Fetch pending proposal
    2. INSERT into themes
    3. INSERT 'contains' edge to parent (if parent_id set)
    4. INSERT suggested_edges
    5. UPDATE theme_proposals.status = 'approved'

    Returns the newly created theme row.
    Raises ValueError if proposal not found or not pending.
    """
    with get_conn() as conn:
        proposal = conn.execute(
            "SELECT * FROM theme_proposals WHERE id = %s AND status = 'pending'",
            (proposal_id,),
        ).fetchone()
        if not proposal:
            raise ValueError(f"No pending proposal with id={proposal_id}")

        theme_id = proposal["proposed_theme_id"]
        level = proposal.get("level", 2)

        # 1. Insert theme
        theme_row = conn.execute(
            """INSERT INTO themes (id, name, description, level)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING
               RETURNING *""",
            (theme_id, proposal["name"], proposal["description"], level),
        ).fetchone()

        # 2. Insert contains edge to parent
        parent_id = proposal.get("parent_id")
        if parent_id:
            conn.execute(
                """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
                   VALUES (%s, %s, 'contains', 1.0)
                   ON CONFLICT (parent_id, child_id) DO NOTHING""",
                (parent_id, theme_id),
            )

        # 3. Insert suggested edges
        suggested_edges = proposal.get("suggested_edges")
        if isinstance(suggested_edges, str):
            try:
                suggested_edges = json.loads(suggested_edges)
            except (json.JSONDecodeError, TypeError):
                suggested_edges = []
        if suggested_edges:
            for edge in suggested_edges:
                from_id = edge.get("from", theme_id)
                to_id = edge.get("to")
                rel = edge.get("relationship", "related")
                if to_id:
                    conn.execute(
                        """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
                           VALUES (%s, %s, %s, 0.6)
                           ON CONFLICT (parent_id, child_id) DO NOTHING""",
                        (from_id, to_id, rel),
                    )

        # 4. Mark proposal approved
        conn.execute(
            """UPDATE theme_proposals
               SET status = 'approved', reviewed_at = NOW()
               WHERE id = %s""",
            (proposal_id,),
        )

        conn.commit()

        logger.info(
            "Materialized theme proposal %s → theme %s (level %d)",
            proposal_id, theme_id, level,
        )
        return theme_row or {"id": theme_id, "name": proposal["name"],
                             "description": proposal["description"], "level": level}


def get_pending_theme_proposals() -> list[dict]:
    with get_conn() as conn:
        return conn.execute(
            """SELECT tp.*, s.title AS source_title, s.url AS source_url
               FROM theme_proposals tp
               LEFT JOIN sources s ON tp.source_id = s.id
               WHERE tp.status = 'pending'
               ORDER BY tp.created_at DESC"""
        ).fetchall()


def update_theme_proposal_status(proposal_id: str, status: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE theme_proposals
               SET status = %s, reviewed_at = NOW()
               WHERE id = %s
               RETURNING *""",
            (status, proposal_id),
        ).fetchone()
        conn.commit()
        return row


def insert_theme_edge_proposal(
    id: str,
    source_theme_id: str,
    target_theme_id: str,
    co_occurrence_count: int = 1,
    suggested_relationship: str = "related",
    suggested_strength: float | None = None,
) -> dict:
    """Insert or increment a co-occurrence-based edge proposal."""
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO theme_edge_proposals
               (id, source_theme_id, target_theme_id, co_occurrence_count,
                suggested_relationship, suggested_strength)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 co_occurrence_count = theme_edge_proposals.co_occurrence_count + 1
               RETURNING *""",
            (id, source_theme_id, target_theme_id, co_occurrence_count,
             suggested_relationship, suggested_strength),
        ).fetchone()
        conn.commit()
        return row


def get_pending_theme_edge_proposals() -> list[dict]:
    """Get all pending co-occurrence edge proposals."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT tep.*,
                      ts.name AS source_name,
                      tt.name AS target_name
               FROM theme_edge_proposals tep
               JOIN themes ts ON ts.id = tep.source_theme_id
               JOIN themes tt ON tt.id = tep.target_theme_id
               WHERE tep.status = 'pending'
               ORDER BY tep.co_occurrence_count DESC, tep.created_at DESC"""
        ).fetchall()


# ---------------------------------------------------------------------------
# Taxonomy Evolution Proposals
# ---------------------------------------------------------------------------

def insert_evolution_proposal(
    change_type: str,
    proposed_changes: dict,
    rationale: str,
    target_theme_id: str | None = None,
    evidence: dict | None = None,
) -> dict:
    """Insert a taxonomy evolution proposal."""
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO taxonomy_evolution_proposals
               (change_type, target_theme_id, proposed_changes, rationale, evidence)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING *""",
            (change_type, target_theme_id,
             json.dumps(proposed_changes), rationale,
             json.dumps(evidence) if evidence is not None else None),
        ).fetchone()
        conn.commit()
        return row


def get_pending_evolution_proposals() -> list[dict]:
    """Get all pending taxonomy evolution proposals."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT tep.*,
                      t.name AS target_theme_name
               FROM taxonomy_evolution_proposals tep
               LEFT JOIN themes t ON t.id = tep.target_theme_id
               WHERE tep.status = 'pending'
               ORDER BY tep.created_at DESC"""
        ).fetchall()


def resolve_evolution_proposal(proposal_id: int, status: str) -> dict | None:
    """Approve or reject an evolution proposal."""
    if status not in ("approved", "rejected", "superseded"):
        raise ValueError(f"Invalid status: {status}")
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE taxonomy_evolution_proposals
               SET status = %s, resolved_at = NOW()
               WHERE id = %s AND status = 'pending'
               RETURNING *""",
            (status, proposal_id),
        ).fetchone()
        conn.commit()
        return row


def get_taxonomy_health_stats() -> dict:
    """Gather taxonomy health statistics for the health check analysis."""
    with get_conn() as conn:
        # Theme distribution: source count per theme
        theme_dist = conn.execute("""
            SELECT t.id, t.name, t.level,
                   COUNT(DISTINCT st.source_id) AS source_count,
                   AVG(st.relevance) AS avg_relevance
            FROM themes t
            LEFT JOIN source_themes st ON st.theme_id = t.id
            GROUP BY t.id, t.name, t.level
            ORDER BY t.level, source_count DESC
        """).fetchall()

        # Recent theme proposals (last 30 days)
        recent_proposals = conn.execute("""
            SELECT id, proposed_theme_id, name, description, parent_id,
                   level, status, trigger_reason, created_at
            FROM theme_proposals
            WHERE created_at > NOW() - INTERVAL '30 days'
            ORDER BY created_at DESC
        """).fetchall()

        # Source count and last health check
        total_sources = conn.execute(
            "SELECT count(*) AS cnt FROM sources"
        ).fetchone()["cnt"]

        last_check = conn.execute(
            "SELECT max(created_at) AS ts FROM taxonomy_evolution_proposals"
        ).fetchone()["ts"]

        sources_since_check = conn.execute(
            "SELECT count(*) AS cnt FROM sources WHERE ingested_at > %s",
            (last_check or "1970-01-01T00:00:00+00:00",),
        ).fetchone()["cnt"]

        # Theme hierarchy edges
        hierarchy = conn.execute("""
            SELECT parent_id, child_id FROM theme_edges
            WHERE relationship = 'contains'
        """).fetchall()

    return {
        "theme_distribution": [dict(r) for r in theme_dist],
        "recent_proposals": [dict(r) for r in recent_proposals],
        "total_sources": total_sources,
        "last_check": last_check,
        "sources_since_check": sources_since_check,
        "hierarchy_edges": [dict(r) for r in hierarchy],
    }


# ---------------------------------------------------------------------------
# Theme Velocity & State Summary
# ---------------------------------------------------------------------------

def insert_landscape_history(
    entity_type: str,
    entity_id: str,
    field: str,
    old_value: str | None,
    new_value: str | None,
    source_id: str | None = None,
    attribution: str | None = None,
    source_published_at=None,
    note: str | None = None,
) -> dict:
    """Record a landscape entity field change for temporal tracking.

    Args:
        source_published_at: Publication date of the source that triggered this
            change. If None and source_id is provided, looked up automatically.
        note: Optional contextual note (e.g., breakthrough that triggered change).
    """
    # Auto-lookup source_published_at if not provided
    if source_published_at is None and source_id:
        try:
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT published_at FROM sources WHERE id = %s",
                    (source_id,),
                ).fetchone()
                if row and row.get("published_at"):
                    source_published_at = row["published_at"]
        except Exception:
            pass

    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO landscape_history
               (entity_type, entity_id, field, old_value, new_value, source_id, attribution, source_published_at, note)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING *""",
            (entity_type, entity_id, field, old_value, new_value, source_id, attribution, source_published_at, note),
        ).fetchone()
        conn.commit()
        return row


def get_landscape_history(
    entity_type: str,
    entity_id: str,
    limit: int = 10,
) -> list[dict]:
    """Get change history for a landscape entity."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT * FROM landscape_history
               WHERE entity_type = %s AND entity_id = %s
               ORDER BY changed_at DESC LIMIT %s""",
            (entity_type, entity_id, limit),
        ).fetchall()


def get_landscape_history_for_theme(
    theme_id: str,
    limit: int = 30,
) -> list[dict]:
    """Get change history across all landscape entities belonging to a theme.

    Joins landscape_history through capabilities, limitations, bottlenecks,
    and anticipations to scope results to a specific theme.
    """
    with get_conn() as conn:
        return conn.execute(
            """SELECT lh.* FROM landscape_history lh
               WHERE (lh.entity_type = 'capability' AND lh.entity_id IN (
                   SELECT id FROM capabilities WHERE theme_id = %s))
               OR (lh.entity_type = 'limitation' AND lh.entity_id IN (
                   SELECT id FROM limitations WHERE theme_id = %s))
               OR (lh.entity_type = 'bottleneck' AND lh.entity_id IN (
                   SELECT id FROM bottlenecks WHERE theme_id = %s))
               OR (lh.entity_type = 'anticipation' AND lh.entity_id IN (
                   SELECT id FROM anticipations WHERE theme_id = %s))
               ORDER BY lh.changed_at DESC LIMIT %s""",
            (theme_id, theme_id, theme_id, theme_id, limit),
        ).fetchall()


# ---------------------------------------------------------------------------
# Similarity search for deduplication
# ---------------------------------------------------------------------------

def find_similar_capability(theme_id: str, description: str, threshold: float = 0.7) -> dict | None:
    """Find an existing capability in the same theme with similar description."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(description, %s) AS sim
               FROM capabilities
               WHERE theme_id = %s AND similarity(description, %s) >= %s
               ORDER BY sim DESC LIMIT 1""",
            (description, theme_id, description, threshold),
        ).fetchone()


def find_similar_limitation(theme_id: str, description: str, threshold: float = 0.7) -> dict | None:
    """Find an existing limitation in the same theme with similar description."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(description, %s) AS sim
               FROM limitations
               WHERE theme_id = %s AND similarity(description, %s) >= %s
               ORDER BY sim DESC LIMIT 1""",
            (description, theme_id, description, threshold),
        ).fetchone()


def find_similar_bottleneck(theme_id: str, description: str, threshold: float = 0.7) -> dict | None:
    """Find an existing bottleneck in the same theme with similar description."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(description, %s) AS sim
               FROM bottlenecks
               WHERE theme_id = %s AND similarity(description, %s) >= %s
               ORDER BY sim DESC LIMIT 1""",
            (description, theme_id, description, threshold),
        ).fetchone()


def _recency_weighted_confidence(
    old_confidence: float | None,
    new_confidence: float,
    new_source_id: str | None = None,
    source_type_weight: float = 1.0,
) -> float:
    """Compute recency-weighted confidence merging.

    Instead of flat (old + new) / 2, weights newer evidence more heavily.
    Recent sources get 0.65 weight, old sources get 0.35 weight.
    When publication date comparison is unavailable, falls back to 0.55/0.45
    (slight recency bias since new evidence is being ingested now).

    Source authority is applied as a multiplier on the new evidence's influence:
    peer_reviewed=1.2, report=1.0, article=0.9, blog=0.7, video/podcast=0.6.
    """
    old_conf = old_confidence if old_confidence is not None else 0.5

    # Base recency weight: newer evidence gets more weight
    # When we're merging, the new evidence is always the more recent ingestion,
    # so we give it a slight advantage by default.
    new_weight = 0.55
    old_weight = 0.45

    # If we can determine temporal ordering via source publication dates,
    # use stronger weighting
    if new_source_id:
        try:
            # Check if new source has a publication date (proxy for temporal info)
            source = get_source(new_source_id)
            if source and source.get("published_at"):
                new_weight = 0.65
                old_weight = 0.35
        except Exception:
            pass

    # Apply source authority factor
    adjusted_new = new_confidence * source_type_weight

    result = old_conf * old_weight + adjusted_new * new_weight
    return max(0.0, min(1.0, result))


# Source type authority weights for confidence merging.
# Peer-reviewed sources get higher weight; informal sources get lower weight.
SOURCE_TYPE_WEIGHTS = {
    "paper": 1.2,
    "peer_reviewed": 1.2,
    "report": 1.0,
    "article": 0.9,
    "video": 0.9,
    "newsletter": 0.85,
    "blog": 0.7,
    "podcast": 0.6,
}


def _get_source_type_weight(source_id: str | None) -> float:
    """Look up the authority weight for a source based on its type."""
    if not source_id:
        return 1.0
    try:
        source = get_source(source_id)
        if source:
            return SOURCE_TYPE_WEIGHTS.get(source.get("source_type", ""), 1.0)
    except Exception:
        pass
    return 1.0


def merge_capability(
    existing_id: str,
    new_evidence: list,
    new_confidence: float,
    source_id: str | None = None,
) -> dict | None:
    """Merge new evidence into an existing capability with recency-weighted confidence."""
    source_weight = _get_source_type_weight(source_id)
    with get_conn() as conn:
        # Fetch current confidence for recency-weighted calculation
        current = conn.execute(
            "SELECT confidence FROM capabilities WHERE id = %s", (existing_id,)
        ).fetchone()
        old_conf = current["confidence"] if current else 0.5
        merged_conf = _recency_weighted_confidence(old_conf, new_confidence, source_id, source_weight)
        row = conn.execute(
            """UPDATE capabilities
               SET evidence_sources = COALESCE(evidence_sources, '[]'::jsonb) || %s::jsonb,
                   confidence = %s,
                   last_updated = NOW(),
                   last_corroborated_at = NOW(),
                   staleness_score = 0
               WHERE id = %s RETURNING *""",
            (json.dumps(new_evidence), merged_conf, existing_id),
        ).fetchone()
        conn.commit()
        return row


def merge_limitation(
    existing_id: str,
    new_evidence: list,
    new_confidence: float,
    source_id: str | None = None,
) -> dict | None:
    """Merge new evidence into an existing limitation with recency-weighted confidence."""
    source_weight = _get_source_type_weight(source_id)
    with get_conn() as conn:
        current = conn.execute(
            "SELECT confidence FROM limitations WHERE id = %s", (existing_id,)
        ).fetchone()
        old_conf = current["confidence"] if current else 0.5
        merged_conf = _recency_weighted_confidence(old_conf, new_confidence, source_id, source_weight)
        row = conn.execute(
            """UPDATE limitations
               SET evidence_sources = COALESCE(evidence_sources, '[]'::jsonb) || %s::jsonb,
                   confidence = %s,
                   last_updated = NOW(),
                   last_corroborated_at = NOW(),
                   staleness_score = 0
               WHERE id = %s RETURNING *""",
            (json.dumps(new_evidence), merged_conf, existing_id),
        ).fetchone()
        conn.commit()
        return row


def merge_bottleneck(
    existing_id: str,
    new_evidence: list,
    new_confidence: float,
    source_id: str | None = None,
) -> dict | None:
    """Merge new evidence into an existing bottleneck with recency-weighted confidence."""
    source_weight = _get_source_type_weight(source_id)
    with get_conn() as conn:
        current = conn.execute(
            "SELECT confidence FROM bottlenecks WHERE id = %s", (existing_id,)
        ).fetchone()
        old_conf = current["confidence"] if current else 0.5
        merged_conf = _recency_weighted_confidence(old_conf, new_confidence, source_id, source_weight)
        row = conn.execute(
            """UPDATE bottlenecks
               SET evidence_sources = COALESCE(evidence_sources, '[]'::jsonb) || %s::jsonb,
                   confidence = %s,
                   last_updated = NOW(),
                   last_corroborated_at = NOW(),
                   staleness_score = 0
               WHERE id = %s RETURNING *""",
            (json.dumps(new_evidence), merged_conf, existing_id),
        ).fetchone()
        conn.commit()
        return row


def compute_staleness_scores(half_life_days: float = 180.0) -> int:
    """Recompute staleness_score for all landscape entities.

    staleness = 1 - exp(-ln(2) / half_life * days_since_corroboration)

    Called from the heartbeat skill handler. Returns total entities updated.
    """
    sql = """
        UPDATE {table}
        SET staleness_score = CASE
            WHEN last_corroborated_at IS NULL THEN 0.5
            ELSE LEAST(1.0, 1.0 - EXP(
                -LN(2) / %s * EXTRACT(EPOCH FROM (NOW() - last_corroborated_at)) / 86400.0
            ))
        END
        WHERE last_corroborated_at IS NOT NULL
           OR staleness_score != 0.5
    """
    total = 0
    with get_conn() as conn:
        for table in ("capabilities", "limitations", "bottlenecks"):
            cur = conn.execute(sql.format(table=table), (half_life_days,))
            total += cur.rowcount
        conn.commit()
    return total


def get_stale_landscape_entities(threshold: float = 0.7, limit: int = 20) -> list[dict]:
    """Return landscape entities with staleness_score above threshold."""
    results = []
    with get_conn() as conn:
        for table, entity_type in [
            ("capabilities", "capability"),
            ("limitations", "limitation"),
            ("bottlenecks", "bottleneck"),
        ]:
            rows = conn.execute(
                f"""SELECT id, description, theme_id, staleness_score, last_corroborated_at
                    FROM {table}
                    WHERE staleness_score > %s
                    ORDER BY staleness_score DESC
                    LIMIT %s""",
                (threshold, limit),
            ).fetchall()
            for r in rows:
                results.append({**dict(r), "entity_type": entity_type})
    return results


def find_similar_breakthrough(theme_id: str, description: str, threshold: float = 0.6) -> dict | None:
    """Find an existing breakthrough in the same theme with similar description.

    Uses a lower threshold (0.6) than other entities because breakthrough
    descriptions tend to vary more in phrasing while describing the same event.
    """
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(description, %s) AS sim
               FROM breakthroughs
               WHERE theme_id = %s AND similarity(description, %s) >= %s
               ORDER BY sim DESC LIMIT 1""",
            (description, theme_id, description, threshold),
        ).fetchone()


def merge_breakthrough(
    existing_id: str,
    new_source_id: str,
    new_confidence: float,
) -> dict | None:
    """Merge a corroborating source into an existing breakthrough.

    Appends to corroborating_sources and updates confidence via recency weighting.
    """
    with get_conn() as conn:
        current = conn.execute(
            "SELECT confidence, corroborating_sources FROM breakthroughs WHERE id = %s",
            (existing_id,),
        ).fetchone()
        if not current:
            return None

        old_conf = current["confidence"] if current["confidence"] is not None else 0.5
        source_weight = _get_source_type_weight(new_source_id)
        merged_conf = _recency_weighted_confidence(old_conf, new_confidence, new_source_id, source_weight)

        # Append to corroborating_sources
        new_entry = json.dumps([new_source_id])

        row = conn.execute(
            """UPDATE breakthroughs
               SET corroborating_sources = COALESCE(corroborating_sources, '[]'::jsonb) || %s::jsonb,
                   confidence = %s
               WHERE id = %s RETURNING *""",
            (new_entry, merged_conf, existing_id),
        ).fetchone()
        conn.commit()
        return row


def find_similar_implication(
    source_theme_id: str,
    target_theme_id: str,
    implication: str,
    threshold: float = 0.7,
) -> dict | None:
    """Find an existing cross-theme implication with similar text for the same theme pair."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(implication, %s) AS sim
               FROM cross_theme_implications
               WHERE source_theme_id = %s AND target_theme_id = %s
                 AND similarity(implication, %s) >= %s
               ORDER BY sim DESC LIMIT 1""",
            (implication, source_theme_id, target_theme_id, implication, threshold),
        ).fetchone()


def merge_implication(existing_id: str, new_evidence: list, new_confidence: float) -> dict | None:
    """Merge new evidence into an existing implication, averaging confidence."""
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE cross_theme_implications
               SET evidence_sources = COALESCE(evidence_sources, '[]'::jsonb) || %s::jsonb,
                   confidence = (COALESCE(confidence, 0.5) + %s) / 2.0,
                   last_updated = NOW()
               WHERE id = %s RETURNING *""",
            (json.dumps(new_evidence), new_confidence, existing_id),
        ).fetchone()
        conn.commit()
        return row


def update_theme_velocity(theme_id: str, velocity: float) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE themes SET velocity = %s WHERE id = %s RETURNING *""",
            (velocity, theme_id),
        ).fetchone()
        conn.commit()
        return row


def update_theme_state_summary(theme_id: str, summary: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE themes
               SET state_summary = %s, state_summary_updated_at = NOW()
               WHERE id = %s RETURNING *""",
            (summary, theme_id),
        ).fetchone()
        conn.commit()
        return row


def invalidate_theme_summaries(theme_ids: list[str]) -> int:
    """Mark theme state summaries as stale by resetting state_summary_updated_at.

    Called when breakthroughs are detected or bottleneck horizons shift,
    forcing regeneration on next heartbeat cycle instead of waiting for
    the 7-day staleness window.

    Returns count of themes invalidated.
    """
    if not theme_ids:
        return 0
    with get_conn() as conn:
        result = conn.execute(
            """UPDATE themes
               SET state_summary_updated_at = NULL
               WHERE id = ANY(%s) AND state_summary IS NOT NULL
               RETURNING id""",
            (theme_ids,),
        )
        rows = result.fetchall()
        conn.commit()
        return len(rows)


# ---------------------------------------------------------------------------
# Beliefs (Phase 4)
# ---------------------------------------------------------------------------

VALID_BELIEF_STATUS = {"active", "resolved", "archived"}
VALID_BELIEF_TYPE = {"factual", "predictive", "methodological", "meta"}


def insert_belief(
    id: str,
    claim: str,
    confidence: float = 0.5,
    status: str = "active",
    belief_type: str = "factual",
    domain_theme_id: str | None = None,
    landscape_links: list | None = None,
    evidence_for: list | None = None,
    evidence_against: list | None = None,
    derived_anticipations: list | None = None,
    parent_belief_id: str | None = None,
    history: list | None = None,
) -> dict:
    """Insert or update a belief."""
    with get_conn() as conn:
        row = conn.execute(
            """INSERT INTO beliefs
               (id, claim, confidence, status, belief_type, domain_theme_id,
                landscape_links, evidence_for, evidence_against,
                derived_anticipations, parent_belief_id, history)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO UPDATE SET
                 claim = EXCLUDED.claim,
                 confidence = EXCLUDED.confidence,
                 status = EXCLUDED.status,
                 belief_type = EXCLUDED.belief_type,
                 domain_theme_id = EXCLUDED.domain_theme_id,
                 landscape_links = EXCLUDED.landscape_links,
                 evidence_for = EXCLUDED.evidence_for,
                 evidence_against = EXCLUDED.evidence_against,
                 derived_anticipations = EXCLUDED.derived_anticipations,
                 parent_belief_id = EXCLUDED.parent_belief_id,
                 history = EXCLUDED.history,
                 last_updated = NOW()
               RETURNING *""",
            (id, claim, confidence,
             status if status in VALID_BELIEF_STATUS else "active",
             belief_type if belief_type in VALID_BELIEF_TYPE else "factual",
             domain_theme_id,
             json.dumps(landscape_links) if landscape_links else "[]",
             json.dumps(evidence_for) if evidence_for else "[]",
             json.dumps(evidence_against) if evidence_against else "[]",
             json.dumps(derived_anticipations) if derived_anticipations else "[]",
             parent_belief_id,
             json.dumps(history) if history else "[]"),
        ).fetchone()
        conn.commit()
        return row


def get_belief(belief_id: str) -> dict | None:
    """Get a single belief by ID."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM beliefs WHERE id = %s", (belief_id,)
        ).fetchone()


def get_active_beliefs() -> list[dict]:
    """Get all active beliefs."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active'
               ORDER BY b.confidence DESC, b.last_updated DESC"""
        ).fetchall()


def get_beliefs_for_theme(theme_id: str) -> list[dict]:
    """Get all active beliefs for a specific theme."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT * FROM beliefs
               WHERE domain_theme_id = %s AND status = 'active'
               ORDER BY confidence DESC""",
            (theme_id,),
        ).fetchall()


def get_beliefs_by_type(belief_type: str) -> list[dict]:
    """Get active beliefs of a specific type."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.belief_type = %s AND b.status = 'active'
               ORDER BY b.confidence DESC""",
            (belief_type,),
        ).fetchall()


def list_beliefs(
    status: str | None = None,
    belief_type: str | None = None,
    domain_theme_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    """List beliefs with optional filters."""
    conditions: list[str] = []
    params: list[Any] = []
    if status:
        conditions.append("b.status = %s")
        params.append(status)
    if belief_type:
        conditions.append("b.belief_type = %s")
        params.append(belief_type)
    if domain_theme_id:
        conditions.append("b.domain_theme_id = %s")
        params.append(domain_theme_id)
    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.extend([limit, offset])
    with get_conn() as conn:
        return conn.execute(
            f"""SELECT b.*, t.name AS theme_name
                FROM beliefs b
                LEFT JOIN themes t ON b.domain_theme_id = t.id
                {where}
                ORDER BY b.last_updated DESC
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()


def update_belief_confidence(
    belief_id: str,
    new_confidence: float,
    trigger: str,
    trigger_type: str = "manual",
) -> dict | None:
    """Update belief confidence and append to history."""
    with get_conn() as conn:
        current = conn.execute(
            "SELECT confidence, history FROM beliefs WHERE id = %s",
            (belief_id,),
        ).fetchone()
        if not current:
            return None

        old_conf = current["confidence"]
        history = current["history"]
        if isinstance(history, str):
            history = json.loads(history)
        if not isinstance(history, list):
            history = []

        history.append({
            "ts": datetime.now().isoformat(),
            "old_conf": old_conf,
            "new_conf": new_confidence,
            "trigger": trigger,
            "trigger_type": trigger_type,
        })

        row = conn.execute(
            """UPDATE beliefs
               SET confidence = %s, history = %s, last_updated = NOW()
               WHERE id = %s RETURNING *""",
            (new_confidence, json.dumps(history), belief_id),
        ).fetchone()
        conn.commit()
        return row


def update_belief_status(belief_id: str, status: str) -> dict | None:
    """Update belief status (active, resolved, archived)."""
    if status not in VALID_BELIEF_STATUS:
        return None
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE beliefs
               SET status = %s, last_updated = NOW()
               WHERE id = %s RETURNING *""",
            (status, belief_id),
        ).fetchone()
        conn.commit()
        return row


def append_belief_evidence(
    belief_id: str,
    evidence: dict,
    evidence_type: str = "for",
) -> dict | None:
    """Append evidence to a belief's evidence_for or evidence_against."""
    field = "evidence_for" if evidence_type == "for" else "evidence_against"
    with get_conn() as conn:
        row = conn.execute(
            f"""UPDATE beliefs
                SET {field} = COALESCE({field}, '[]'::jsonb) || %s::jsonb,
                    last_updated = NOW()
                WHERE id = %s RETURNING *""",
            (json.dumps([evidence]), belief_id),
        ).fetchone()
        conn.commit()
        return row


def append_belief_landscape_link(belief_id: str, link: dict) -> dict | None:
    """Append a landscape link to a belief."""
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE beliefs
               SET landscape_links = COALESCE(landscape_links, '[]'::jsonb) || %s::jsonb,
                   last_updated = NOW()
               WHERE id = %s RETURNING *""",
            (json.dumps([link]), belief_id),
        ).fetchone()
        conn.commit()
        return row


def append_belief_derived_anticipation(belief_id: str, anticipation_id: str) -> dict | None:
    """Record that a belief generated a derived anticipation."""
    with get_conn() as conn:
        row = conn.execute(
            """UPDATE beliefs
               SET derived_anticipations = COALESCE(derived_anticipations, '[]'::jsonb) || %s::jsonb,
                   last_updated = NOW()
               WHERE id = %s RETURNING *""",
            (json.dumps([anticipation_id]), belief_id),
        ).fetchone()
        conn.commit()
        return row


def find_similar_belief(claim: str, threshold: float = 0.7) -> dict | None:
    """Find an existing belief with similar claim text."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT *, similarity(claim, %s) AS sim
               FROM beliefs
               WHERE similarity(claim, %s) >= %s AND status = 'active'
               ORDER BY sim DESC LIMIT 1""",
            (claim, claim, threshold),
        ).fetchone()


def get_stale_beliefs(velocity_threshold: float = 0.3) -> list[dict]:
    """Get active beliefs that need review based on theme velocity.

    High-velocity themes (> threshold) need more frequent review.
    Returns beliefs whose last_updated is older than the velocity-appropriate window.
    """
    with get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name, t.velocity
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active'
                 AND (
                   -- High-velocity themes: review every 14 days
                   (COALESCE(t.velocity, 0) > %s AND b.last_updated < NOW() - INTERVAL '14 days')
                   OR
                   -- Low-velocity themes: review every 30 days
                   (COALESCE(t.velocity, 0) <= %s AND b.last_updated < NOW() - INTERVAL '30 days')
                   OR
                   -- Unlinked beliefs: review every 30 days
                   (b.domain_theme_id IS NULL AND b.last_updated < NOW() - INTERVAL '30 days')
                 )
               ORDER BY t.velocity DESC NULLS LAST, b.last_updated ASC""",
            (velocity_threshold, velocity_threshold),
        ).fetchall()


def get_low_confidence_beliefs(threshold: float = 0.5) -> list[dict]:
    """Get active beliefs with confidence below threshold."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active' AND b.confidence < %s
               ORDER BY b.confidence ASC""",
            (threshold,),
        ).fetchall()


def get_unchallenged_beliefs(min_confidence: float = 0.8) -> list[dict]:
    """Get high-confidence beliefs with no evidence_against."""
    with get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active'
                 AND b.confidence >= %s
                 AND (b.evidence_against IS NULL
                      OR jsonb_array_length(b.evidence_against) = 0)
               ORDER BY b.confidence DESC""",
            (min_confidence,),
        ).fetchall()


def get_belief_pairs_for_consistency(theme_id: str | None = None) -> list[dict]:
    """Get pairs of active beliefs sharing a theme for consistency checking.

    Returns pairs as rows with b1_* and b2_* prefixed columns.
    """
    with get_conn() as conn:
        theme_filter = "AND b1.domain_theme_id = %s" if theme_id else ""
        params = (theme_id,) if theme_id else ()
        return conn.execute(
            f"""SELECT
                   b1.id AS b1_id, b1.claim AS b1_claim, b1.confidence AS b1_confidence,
                   b2.id AS b2_id, b2.claim AS b2_claim, b2.confidence AS b2_confidence,
                   t.name AS theme_name
               FROM beliefs b1
               JOIN beliefs b2 ON b1.domain_theme_id = b2.domain_theme_id
                   AND b1.id < b2.id
               LEFT JOIN themes t ON b1.domain_theme_id = t.id
               WHERE b1.status = 'active' AND b2.status = 'active'
               {theme_filter}
               ORDER BY t.name, b1.id""",
            params,
        ).fetchall()


# ---------------------------------------------------------------------------
# Source Deletion
# ---------------------------------------------------------------------------

def _jsonb_prune_source(
    conn,
    table: str,
    jsonb_column: str,
    source_id: str,
    *,
    delete_if_sole: bool = True,
) -> tuple[int, int]:
    """Remove source_id from a JSONB array column, optionally deleting sole-source rows.

    Returns (rows_deleted, rows_pruned).
    """
    deleted = 0
    pruned = 0

    if delete_if_sole:
        # Delete rows where this source_id is the ONLY entry in the array
        cur = conn.execute(
            f"""DELETE FROM {table}
                WHERE jsonb_typeof({jsonb_column}) = 'array'
                  AND jsonb_array_length({jsonb_column}) = 1
                  AND {jsonb_column}::text LIKE %s""",
            (f"%{source_id}%",),
        )
        deleted = cur.rowcount

    # Prune source_id from remaining rows that reference it
    cur = conn.execute(
        f"""UPDATE {table}
            SET {jsonb_column} = (
                SELECT COALESCE(jsonb_agg(elem), '[]'::jsonb)
                FROM jsonb_array_elements({jsonb_column}) AS elem
                WHERE NOT (elem::text LIKE %s)
            )
            WHERE jsonb_typeof({jsonb_column}) = 'array'
              AND {jsonb_column}::text LIKE %s""",
        (f"%{source_id}%", f"%{source_id}%"),
    )
    pruned = cur.rowcount
    return deleted, pruned


def delete_source(source_id: str, library_path: Path | None = None) -> dict:
    """Delete a source and all its dependent data from the database and filesystem.

    Performs all DB operations in a single transaction respecting FK constraints.
    Filesystem cleanup happens after the transaction commits.

    Args:
        source_id: The source ID (ULID) to delete.
        library_path: Base library directory (default: from Config).

    Returns:
        Dict with counts per table of rows affected.
    """
    from pathlib import Path as _Path
    import shutil

    summary: dict[str, int] = {}

    with get_conn() as conn:
        # -- Phase A: Direct FK children (hard references to source_id) --

        cur = conn.execute(
            "DELETE FROM claims WHERE source_id = %s", (source_id,)
        )
        summary["claims"] = cur.rowcount

        cur = conn.execute(
            """DELETE FROM source_edges
               WHERE source_a = %s OR source_b = %s""",
            (source_id, source_id),
        )
        summary["source_edges"] = cur.rowcount

        cur = conn.execute(
            "DELETE FROM source_concepts WHERE source_id = %s", (source_id,)
        )
        summary["source_concepts"] = cur.rowcount

        cur = conn.execute(
            "DELETE FROM source_themes WHERE source_id = %s", (source_id,)
        )
        summary["source_themes"] = cur.rowcount

        # breakthroughs with primary_source_id FK
        cur = conn.execute(
            "DELETE FROM breakthroughs WHERE primary_source_id = %s",
            (source_id,),
        )
        summary["breakthroughs"] = cur.rowcount

        # theme_proposals has ON DELETE SET NULL, but clean up explicitly
        cur = conn.execute(
            "DELETE FROM theme_proposals WHERE source_id = %s", (source_id,)
        )
        summary["theme_proposals"] = cur.rowcount

        # -- Phase B: JSONB evidence_sources cleanup --

        # Before deleting bottlenecks, null out limitations.bottleneck_id
        # for bottlenecks that will be deleted (sole-source)
        conn.execute(
            """UPDATE limitations SET bottleneck_id = NULL
               WHERE bottleneck_id IN (
                   SELECT id FROM bottlenecks
                   WHERE jsonb_typeof(evidence_sources) = 'array'
                     AND jsonb_array_length(evidence_sources) = 1
                     AND evidence_sources::text LIKE %s
               )""",
            (f"%{source_id}%",),
        )

        d, p = _jsonb_prune_source(conn, "capabilities", "evidence_sources", source_id)
        summary["capabilities_deleted"] = d
        summary["capabilities_pruned"] = p

        d, p = _jsonb_prune_source(conn, "limitations", "evidence_sources", source_id)
        summary["limitations_deleted"] = d
        summary["limitations_pruned"] = p

        d, p = _jsonb_prune_source(conn, "bottlenecks", "evidence_sources", source_id)
        summary["bottlenecks_deleted"] = d
        summary["bottlenecks_pruned"] = p

        d, p = _jsonb_prune_source(conn, "cross_theme_implications", "evidence_sources", source_id)
        summary["implications_deleted"] = d
        summary["implications_pruned"] = p

        d, p = _jsonb_prune_source(conn, "anticipations", "based_on", source_id)
        summary["anticipations_deleted"] = d
        summary["anticipations_pruned"] = p

        # Breakthroughs corroborating_sources cleanup (non-primary references)
        d, p = _jsonb_prune_source(
            conn, "breakthroughs", "corroborating_sources", source_id,
            delete_if_sole=False,
        )
        summary["breakthroughs_corroborate_pruned"] = p

        # Beliefs: prune source_id from evidence_for and evidence_against
        for field in ("evidence_for", "evidence_against"):
            conn.execute(
                f"""UPDATE beliefs
                    SET {field} = (
                        SELECT COALESCE(jsonb_agg(elem), '[]'::jsonb)
                        FROM jsonb_array_elements({field}) AS elem
                        WHERE NOT (elem::text LIKE %s)
                    )
                    WHERE jsonb_typeof({field}) = 'array'
                      AND {field}::text LIKE %s""",
                (f"%{source_id}%", f"%{source_id}%"),
            )

        # Ideas: prune from grounding JSONB
        conn.execute(
            """UPDATE ideas
               SET grounding = (
                   SELECT COALESCE(jsonb_agg(elem), '[]'::jsonb)
                   FROM jsonb_array_elements(
                       CASE WHEN jsonb_typeof(grounding) = 'array' THEN grounding
                            ELSE '[]'::jsonb END
                   ) AS elem
                   WHERE NOT (elem::text LIKE %s)
               )
               WHERE grounding::text LIKE %s""",
            (f"%{source_id}%", f"%{source_id}%"),
        )

        # -- Phase C: Text references (no FK, just cleanup) --

        cur = conn.execute(
            "DELETE FROM landscape_history WHERE source_id = %s", (source_id,)
        )
        summary["landscape_history"] = cur.rowcount

        cur = conn.execute(
            "DELETE FROM notifications WHERE source_id = %s", (source_id,)
        )
        summary["notifications"] = cur.rowcount

        # -- Phase D: Delete source record --

        cur = conn.execute(
            "DELETE FROM sources WHERE id = %s", (source_id,)
        )
        summary["sources"] = cur.rowcount

        conn.commit()

    # -- Phase E: Filesystem cleanup (outside transaction) --
    if library_path is None:
        from reading_app.config import Config
        library_path = Config().library_path

    source_dir = _Path(library_path) / source_id
    if source_dir.exists():
        try:
            shutil.rmtree(source_dir)
            summary["filesystem"] = 1
            logger.info("Removed library dir: %s", source_dir)
        except PermissionError:
            # Windows: retry after clearing read-only flags
            import stat
            def _on_rm_error(_func, _path, _exc_info):
                _Path(_path).chmod(stat.S_IWRITE)
                _func(_path)
            shutil.rmtree(source_dir, onexc=_on_rm_error)
            summary["filesystem"] = 1
            logger.info("Removed library dir (with permission fix): %s", source_dir)
    else:
        summary["filesystem"] = 0

    logger.info("Deleted source %s: %s", source_id, summary)
    return summary
