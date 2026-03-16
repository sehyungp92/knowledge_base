-- Taxonomy evolution proposals: meso-level structural changes proposed by
-- periodic health checks and approved by human review.

CREATE TABLE IF NOT EXISTS taxonomy_evolution_proposals (
    id          SERIAL PRIMARY KEY,
    change_type TEXT NOT NULL,              -- 'split_l2', 'merge_l2', 'new_l2', 'new_l1', 'rename', 'reparent'
    target_theme_id TEXT,                   -- theme being changed (NULL for new themes)
    proposed_changes JSONB NOT NULL,        -- {new_ids, new_names, new_descriptions, new_parent, merge_into, ...}
    rationale   TEXT NOT NULL,              -- LLM-generated explanation
    evidence    JSONB,                      -- {source_count, proposal_ids, sample_titles}
    status      TEXT NOT NULL DEFAULT 'pending',  -- pending, approved, rejected, superseded
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_taxonomy_evolution_status
    ON taxonomy_evolution_proposals (status);
