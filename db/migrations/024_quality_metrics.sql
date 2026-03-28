-- Quality metrics persistence for learning loops
-- Tracks output quality signals across pipeline stages

CREATE TABLE IF NOT EXISTS quality_metrics (
    id SERIAL PRIMARY KEY,
    metric_type TEXT NOT NULL,        -- 'state_summary', 'source_extraction', 'tournament_strategy'
    entity_type TEXT NOT NULL,        -- 'theme', 'source', 'strategy'
    entity_id TEXT NOT NULL,
    dimensions JSONB DEFAULT '{}',    -- e.g. {"temporal_language": 4, "specificity": 3}
    aggregate_score REAL,
    cost_usd REAL,
    skill TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quality_metrics_type ON quality_metrics (metric_type, entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_quality_metrics_created ON quality_metrics (created_at DESC);
