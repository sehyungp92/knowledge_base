-- Migration 008: Add composite index for landscape history theme-scoped queries
-- Supports get_landscape_history_for_theme() which joins through entity tables.

CREATE INDEX IF NOT EXISTS idx_landscape_history_entity_type_changed
    ON landscape_history(entity_type, changed_at DESC);
