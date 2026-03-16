-- Migration 007: Landscape History for temporal trajectory tracking
-- Tracks changes to landscape entity fields over time, enabling honest
-- "was X, shifted to Y because of Z" narratives in /landscape views.

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

CREATE INDEX IF NOT EXISTS idx_landscape_history_entity
    ON landscape_history(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_landscape_history_changed
    ON landscape_history(changed_at DESC);

-- Trigram indexes for entity deduplication
CREATE INDEX IF NOT EXISTS idx_capabilities_description_trgm
    ON capabilities USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_limitations_description_trgm
    ON limitations USING gin(description gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_bottlenecks_description_trgm
    ON bottlenecks USING gin(description gin_trgm_ops);
