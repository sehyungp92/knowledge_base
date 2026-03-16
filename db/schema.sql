-- Knowledge Base Schema
-- PostgreSQL + pgvector + FTS

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- CORE KNOWLEDGE GRAPH
-- ============================================================

CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    url TEXT,
    title TEXT NOT NULL,
    authors JSONB,
    published_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT NOW(),
    abstract TEXT,
    library_path TEXT,
    processing_status TEXT DEFAULT 'pending',
    metadata JSONB,
    fts_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(abstract, ''))
    ) STORED
);

CREATE TABLE IF NOT EXISTS claims (
    id TEXT PRIMARY KEY,
    source_id TEXT REFERENCES sources(id),
    claim_text TEXT NOT NULL,
    claim_type TEXT,
    section TEXT,
    confidence REAL,
    evidence_snippet TEXT,
    evidence_location TEXT,
    evidence_type TEXT,
    temporal_scope TEXT,  -- current_state, historical, future_prediction
    provenance_type TEXT DEFAULT 'extracted',  -- extracted, generated, synthesis
    embedding VECTOR(768),
    fts_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', claim_text)
    ) STORED
);

CREATE TABLE IF NOT EXISTS concepts (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    concept_type TEXT,
    description TEXT,
    aliases JSONB,
    external_ids JSONB,
    embedding VECTOR(768)
);

CREATE TABLE IF NOT EXISTS source_edges (
    source_a TEXT REFERENCES sources(id),
    source_b TEXT REFERENCES sources(id),
    edge_type TEXT,
    explanation TEXT,
    evidence_a TEXT,
    evidence_b TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (source_a, source_b, edge_type)
);

CREATE TABLE IF NOT EXISTS source_concepts (
    source_id TEXT REFERENCES sources(id),
    concept_id TEXT REFERENCES concepts(id),
    relationship TEXT,
    confidence REAL,
    PRIMARY KEY (source_id, concept_id, relationship)
);

CREATE TABLE IF NOT EXISTS ideas (
    id TEXT PRIMARY KEY,
    idea_text TEXT NOT NULL,
    idea_type TEXT,
    grounding JSONB,
    testability TEXT,
    novelty_score REAL,
    feasibility_score REAL,
    impact_score REAL,
    overall_score REAL,
    similar_existing_ideas JSONB,
    novelty_check_passed BOOLEAN,
    generation_context JSONB,
    parent_idea_id TEXT REFERENCES ideas(id),
    user_rating INTEGER,
    user_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- THEMES (Phase 2+)
-- ============================================================

CREATE TABLE IF NOT EXISTS themes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    state_summary TEXT,
    state_summary_updated_at TIMESTAMP,
    velocity REAL,
    velocity_window_days INTEGER DEFAULT 90,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS theme_edges (
    parent_id TEXT REFERENCES themes(id),
    child_id TEXT REFERENCES themes(id),
    relationship TEXT,
    strength REAL,
    PRIMARY KEY (parent_id, child_id)
);

CREATE TABLE IF NOT EXISTS source_themes (
    source_id TEXT REFERENCES sources(id),
    theme_id TEXT REFERENCES themes(id),
    relevance REAL,
    PRIMARY KEY (source_id, theme_id)
);

CREATE TABLE IF NOT EXISTS cross_theme_implications (
    id TEXT PRIMARY KEY,
    source_theme_id TEXT REFERENCES themes(id),
    target_theme_id TEXT REFERENCES themes(id),
    trigger_type TEXT,
    trigger_id TEXT,
    implication TEXT NOT NULL,
    confidence REAL,
    evidence_sources JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT
);

-- ============================================================
-- LANDSCAPE MODEL
-- ============================================================

CREATE TABLE IF NOT EXISTS capabilities (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    description TEXT NOT NULL,
    maturity TEXT,  -- research_only, demo, narrow_production, broad_production, commoditized
    confidence REAL,
    evidence_sources JSONB,
    first_demonstrated_at TEXT,
    production_ready_at TEXT,
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT,
    last_updated TIMESTAMP DEFAULT NOW(),
    last_corroborated_at TIMESTAMPTZ,
    staleness_score REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bottlenecks (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    description TEXT NOT NULL,
    blocking_what TEXT,
    bottleneck_type TEXT,  -- compute, data, algorithmic, hardware, theoretical, regulatory, integration
    resolution_horizon TEXT,  -- months, 1-2_years, 3-5_years, 5+_years, unknown, possibly_fundamental
    active_approaches JSONB,
    evidence_sources JSONB,
    confidence REAL,
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT,
    last_updated TIMESTAMP DEFAULT NOW(),
    last_corroborated_at TIMESTAMPTZ,
    staleness_score REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS limitations (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    description TEXT NOT NULL,
    underlying_reason TEXT,
    limitation_type TEXT,  -- architectural, data, compute, theoretical, engineering, behavioral, evaluation, unknown
    signal_type TEXT,  -- explicit, implicit_performance_cliff, implicit_controlled_conditions,
                       -- implicit_conspicuous_absence, implicit_hedging, implicit_scale_cost
    severity TEXT,     -- blocking, significant, minor, workaround_exists
    trajectory TEXT,   -- improving, stable, worsening, unclear
    confidence REAL,
    evidence_sources JSONB,
    validated BOOLEAN,
    validated_at TIMESTAMP,
    bottleneck_id TEXT REFERENCES bottlenecks(id),
    signal_strength TEXT DEFAULT 'moderate',  -- grounded, moderate, speculative
    embedding VECTOR(768),
    grounding_claim_ids JSONB,
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT,
    last_updated TIMESTAMP DEFAULT NOW(),
    last_corroborated_at TIMESTAMPTZ,
    staleness_score REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS breakthroughs (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    description TEXT NOT NULL,
    what_was_believed_before TEXT,
    what_is_now_possible TEXT,
    significance TEXT,  -- incremental, notable, major, paradigm_shifting
    immediate_implications JSONB,
    downstream_implications JSONB,
    bottlenecks_affected JSONB,  -- [{bottleneck_id, effect: resolves|reduces|reframes}]
    primary_source_id TEXT REFERENCES sources(id),
    corroborating_sources JSONB,
    detected_at TIMESTAMP DEFAULT NOW(),
    confidence REAL,
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT
);

CREATE TABLE IF NOT EXISTS anticipations (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    prediction TEXT NOT NULL,
    based_on JSONB,
    reasoning TEXT,
    confidence REAL,
    timeline TEXT,  -- months, 1-2_years, 3-5_years, 5+_years
    status TEXT DEFAULT 'open',  -- open, partially_confirmed, confirmed, invalidated, expired
    status_evidence JSONB,
    would_confirm TEXT,
    would_invalidate TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_reviewed TIMESTAMP,
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT
);

CREATE TABLE IF NOT EXISTS challenge_log (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    system_position TEXT,
    system_evidence JSONB,
    user_argument TEXT,
    user_evidence JSONB,
    outcome TEXT,  -- system_updated, user_position_recorded, ambiguous_flagged, system_maintained
    resolution_reasoning TEXT,
    changes_made JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    belief_id TEXT
);

CREATE TABLE IF NOT EXISTS theme_proposals (
    id TEXT PRIMARY KEY,
    proposed_theme_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    parent_id TEXT REFERENCES themes(id) ON DELETE SET NULL,
    suggested_edges JSONB DEFAULT '[]',
    source_id TEXT REFERENCES sources(id) ON DELETE SET NULL,
    trigger_reason TEXT NOT NULL,  -- low_coverage, no_themes
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, approved, rejected
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- BELIEF SYSTEM (Phase 4)
-- ============================================================

CREATE TABLE IF NOT EXISTS beliefs (
    id               TEXT PRIMARY KEY,
    claim            TEXT NOT NULL,
    confidence       FLOAT NOT NULL DEFAULT 0.5,
    status           TEXT DEFAULT 'active',       -- active | resolved | archived
    belief_type      TEXT DEFAULT 'factual',      -- factual | predictive | methodological | meta
    domain_theme_id  TEXT,                         -- primary theme link (queryable FK)
    landscape_links  JSONB DEFAULT '[]',
    evidence_for     JSONB DEFAULT '[]',
    evidence_against JSONB DEFAULT '[]',
    derived_anticipations JSONB DEFAULT '[]',
    parent_belief_id TEXT,
    history          JSONB DEFAULT '[]',
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    last_updated     TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (domain_theme_id) REFERENCES themes(id),
    FOREIGN KEY (parent_belief_id) REFERENCES beliefs(id)
);

-- ============================================================
-- LANDSCAPE HISTORY (temporal trajectory tracking)
-- ============================================================

CREATE TABLE IF NOT EXISTS landscape_history (
    id SERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,  -- capability, limitation, bottleneck, anticipation
    entity_id TEXT NOT NULL,
    field TEXT NOT NULL,        -- maturity, resolution_horizon, status, trajectory, etc.
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    source_id TEXT,
    attribution TEXT
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_sources_fts ON sources USING gin(fts_vector);
CREATE INDEX IF NOT EXISTS idx_claims_fts ON claims USING gin(fts_vector);
-- Concept dedup: unique on case-insensitive name + type
CREATE UNIQUE INDEX IF NOT EXISTS idx_concepts_canonical_name_type
    ON concepts (lower(canonical_name), COALESCE(concept_type, ''));
-- Note: ivfflat index requires data to exist; create after initial data load
-- CREATE INDEX IF NOT EXISTS idx_claims_embedding ON claims USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_claims_source ON claims(source_id);
CREATE INDEX IF NOT EXISTS idx_claims_provenance ON claims(provenance_type);
CREATE INDEX IF NOT EXISTS idx_source_edges_a ON source_edges(source_a);
CREATE INDEX IF NOT EXISTS idx_source_edges_b ON source_edges(source_b);
CREATE INDEX IF NOT EXISTS idx_ideas_novelty ON ideas(novelty_check_passed, overall_score DESC);
CREATE INDEX IF NOT EXISTS idx_source_themes ON source_themes(theme_id);
CREATE INDEX IF NOT EXISTS idx_cross_theme ON cross_theme_implications(source_theme_id, target_theme_id);
CREATE INDEX IF NOT EXISTS idx_capabilities_theme ON capabilities(theme_id);
CREATE INDEX IF NOT EXISTS idx_capabilities_description_trgm
    ON capabilities USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_limitations_theme ON limitations(theme_id);
CREATE INDEX IF NOT EXISTS idx_limitations_description_trgm
    ON limitations USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_limitations_validation
    ON limitations(signal_type, validated) WHERE signal_type LIKE 'implicit_%';
CREATE INDEX IF NOT EXISTS idx_bottlenecks_theme ON bottlenecks(theme_id);
CREATE INDEX IF NOT EXISTS idx_bottlenecks_description_trgm
    ON bottlenecks USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_breakthroughs_theme ON breakthroughs(theme_id);
CREATE INDEX IF NOT EXISTS idx_breakthroughs_detected ON breakthroughs(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_breakthroughs_description_trgm
    ON breakthroughs USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_anticipations_status ON anticipations(status, theme_id);
CREATE INDEX IF NOT EXISTS idx_challenge_entity ON challenge_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_theme_proposals_status ON theme_proposals(status);
CREATE INDEX IF NOT EXISTS idx_landscape_history_entity ON landscape_history(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_landscape_history_changed ON landscape_history(changed_at DESC);
CREATE INDEX IF NOT EXISTS idx_beliefs_domain ON beliefs(domain_theme_id);
CREATE INDEX IF NOT EXISTS idx_beliefs_status ON beliefs(status);
CREATE INDEX IF NOT EXISTS idx_beliefs_confidence ON beliefs(confidence);
CREATE INDEX IF NOT EXISTS idx_beliefs_type ON beliefs(belief_type);
CREATE INDEX IF NOT EXISTS idx_beliefs_parent ON beliefs(parent_belief_id);
CREATE INDEX IF NOT EXISTS idx_beliefs_claim_trgm ON beliefs USING gin(claim gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_claims_temporal_scope
    ON claims(temporal_scope) WHERE temporal_scope IS NOT NULL;

-- ============================================================
-- PHASE 5: NOTIFICATIONS + GRAPH METRICS
-- ============================================================

CREATE TABLE IF NOT EXISTS notifications (
    id              SERIAL PRIMARY KEY,
    type            TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    title           TEXT NOT NULL,
    detail          JSONB DEFAULT '{}',
    source_id       TEXT,
    read            BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS graph_metrics (
    id              SERIAL PRIMARY KEY,
    metric_type     TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    score           FLOAT NOT NULL,
    metadata        JSONB DEFAULT '{}',
    computed_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_unread
    ON notifications (read, created_at DESC) WHERE read = FALSE;
CREATE UNIQUE INDEX IF NOT EXISTS idx_graph_metrics_lookup
    ON graph_metrics (metric_type, entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_graph_metrics_rank
    ON graph_metrics (metric_type, entity_type, score DESC);
CREATE INDEX IF NOT EXISTS idx_anticipations_prediction_trgm
    ON anticipations USING gin(prediction gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_sources_title_trgm
    ON sources USING gin(title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_ideas_text_trgm
    ON ideas USING gin(idea_text gin_trgm_ops);
