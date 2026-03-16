-- Migration 009: Phase 5 tables — notifications, graph_metrics, anticipation search index

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

CREATE INDEX IF NOT EXISTS idx_notifications_unread
    ON notifications (read, created_at DESC) WHERE read = FALSE;

CREATE TABLE IF NOT EXISTS graph_metrics (
    id              SERIAL PRIMARY KEY,
    metric_type     TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    score           FLOAT NOT NULL,
    metadata        JSONB DEFAULT '{}',
    computed_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_graph_metrics_lookup
    ON graph_metrics (metric_type, entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_graph_metrics_rank
    ON graph_metrics (metric_type, entity_type, score DESC);

-- New trigram index for anticipation search (Improvement 2)
CREATE INDEX IF NOT EXISTS idx_anticipations_prediction_trgm
    ON anticipations USING gin(prediction gin_trgm_ops);

-- Source title trigram index for unified search
CREATE INDEX IF NOT EXISTS idx_sources_title_trgm
    ON sources USING gin(title gin_trgm_ops);

-- Ideas text trigram index for unified search
CREATE INDEX IF NOT EXISTS idx_ideas_text_trgm
    ON ideas USING gin(idea_text gin_trgm_ops);
