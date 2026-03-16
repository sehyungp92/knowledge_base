-- Migration 015: Temporal Intelligence Improvements
-- Adds claim temporality, breakthrough dedup index, and source_type_weight support.

-- 1. Add temporal_scope to claims for distinguishing time references
ALTER TABLE claims ADD COLUMN IF NOT EXISTS temporal_scope TEXT;
-- Valid values: current_state, historical, future_prediction
-- NULL means unclassified (backward compatible)

-- 2. Add source_published_at to landscape_history if not already present
-- (should exist from migration 010, but ensure it)
ALTER TABLE landscape_history ADD COLUMN IF NOT EXISTS source_published_at TIMESTAMP;

-- 3. Add trgm index on breakthroughs.description for deduplication
CREATE INDEX IF NOT EXISTS idx_breakthroughs_description_trgm
    ON breakthroughs USING gin(description gin_trgm_ops);

-- 4. Add index on claims.temporal_scope for filtering
CREATE INDEX IF NOT EXISTS idx_claims_temporal_scope
    ON claims(temporal_scope) WHERE temporal_scope IS NOT NULL;
