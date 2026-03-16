-- Migration 014: Implication dedup support
-- Adds trigram index for similarity matching and last_updated column.

-- Ensure pg_trgm is available (already used by capabilities etc.)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_implications_description_trgm
    ON cross_theme_implications USING gin(implication gin_trgm_ops);

ALTER TABLE cross_theme_implications
    ADD COLUMN IF NOT EXISTS last_updated TIMESTAMP DEFAULT NOW();
