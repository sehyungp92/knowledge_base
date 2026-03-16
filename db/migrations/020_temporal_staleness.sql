-- Migration 020: Temporal fact validity tracking
-- Adds staleness scoring to landscape entities so stale facts surface in reports.

ALTER TABLE capabilities
    ADD COLUMN IF NOT EXISTS last_corroborated_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS staleness_score REAL DEFAULT 0;

ALTER TABLE limitations
    ADD COLUMN IF NOT EXISTS last_corroborated_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS staleness_score REAL DEFAULT 0;

ALTER TABLE bottlenecks
    ADD COLUMN IF NOT EXISTS last_corroborated_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS staleness_score REAL DEFAULT 0;

-- Set initial corroboration date from last_updated for existing rows
UPDATE capabilities SET last_corroborated_at = last_updated WHERE last_corroborated_at IS NULL;
UPDATE limitations SET last_corroborated_at = last_updated WHERE last_corroborated_at IS NULL;
UPDATE bottlenecks SET last_corroborated_at = last_updated WHERE last_corroborated_at IS NULL;

-- Index for staleness queries
CREATE INDEX IF NOT EXISTS idx_capabilities_staleness ON capabilities(staleness_score DESC) WHERE staleness_score > 0.5;
CREATE INDEX IF NOT EXISTS idx_limitations_staleness ON limitations(staleness_score DESC) WHERE staleness_score > 0.5;
CREATE INDEX IF NOT EXISTS idx_bottlenecks_staleness ON bottlenecks(staleness_score DESC) WHERE staleness_score > 0.5;
