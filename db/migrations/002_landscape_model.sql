-- Migration 002: AI Landscape Model tables
-- Adds capabilities, limitations, bottlenecks, breakthroughs, anticipations,
-- challenge_log, and theme_proposals tables.

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
    last_updated TIMESTAMP DEFAULT NOW()
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
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS limitations (
    id TEXT PRIMARY KEY,
    theme_id TEXT REFERENCES themes(id),
    description TEXT NOT NULL,
    underlying_reason TEXT,
    limitation_type TEXT,  -- architectural, data, compute, theoretical, engineering, unknown
    signal_type TEXT,  -- explicit, implicit_performance_cliff, implicit_controlled_conditions,
                       -- implicit_conspicuous_absence, implicit_hedging, implicit_scale_cost
    severity TEXT,     -- blocking, significant, minor, workaround_exists
    trajectory TEXT,   -- improving, stable, worsening, unclear
    confidence REAL,
    evidence_sources JSONB,
    validated BOOLEAN,
    validated_at TIMESTAMP,
    bottleneck_id TEXT REFERENCES bottlenecks(id),
    attribution TEXT DEFAULT 'automated_extraction',
    attributed_reasoning TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
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
    status TEXT DEFAULT 'open',  -- open, partially_confirmed, confirmed, invalidated
    status_evidence JSONB,
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
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_capabilities_theme ON capabilities(theme_id);
CREATE INDEX IF NOT EXISTS idx_limitations_theme ON limitations(theme_id);
CREATE INDEX IF NOT EXISTS idx_limitations_validation
    ON limitations(signal_type, validated) WHERE signal_type LIKE 'implicit_%';
CREATE INDEX IF NOT EXISTS idx_bottlenecks_theme ON bottlenecks(theme_id);
CREATE INDEX IF NOT EXISTS idx_breakthroughs_theme ON breakthroughs(theme_id);
CREATE INDEX IF NOT EXISTS idx_breakthroughs_detected ON breakthroughs(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_anticipations_status ON anticipations(status, theme_id);
CREATE INDEX IF NOT EXISTS idx_challenge_entity ON challenge_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_theme_proposals_status ON theme_proposals(status);
