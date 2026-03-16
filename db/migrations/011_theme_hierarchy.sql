-- Migration 011: 3-level theme hierarchy
-- Adds level column to themes and theme_proposals, adds theme_edge_proposals table.
-- Level 0 = meta/theme (organizational grouping, ~5-6 nodes)
-- Level 1 = subtheme (primary analytical unit, ~17-20 nodes, equivalent to old 27 flat themes)
-- Level 2 = subsubtheme (leaf classification target, ~35-45 nodes)
-- Additive only — all 27 existing rows get level=1 by DEFAULT 1.

ALTER TABLE themes ADD COLUMN IF NOT EXISTS level INTEGER NOT NULL DEFAULT 1;
CREATE INDEX IF NOT EXISTS idx_themes_level ON themes(level);
CREATE INDEX IF NOT EXISTS idx_theme_edges_child ON theme_edges(child_id, relationship);

ALTER TABLE theme_proposals ADD COLUMN IF NOT EXISTS level INTEGER NOT NULL DEFAULT 2;

-- Co-occurrence edge proposals table
CREATE TABLE IF NOT EXISTS theme_edge_proposals (
    id TEXT PRIMARY KEY,
    source_theme_id TEXT REFERENCES themes(id),
    target_theme_id TEXT REFERENCES themes(id),
    co_occurrence_count INTEGER DEFAULT 1,
    suggested_relationship TEXT DEFAULT 'related',
    suggested_strength REAL,
    status TEXT DEFAULT 'pending',
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_theme_edge_proposals_status ON theme_edge_proposals(status);
