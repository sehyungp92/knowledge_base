-- Post-processing status tracking table.
-- Tracks per-source, per-step progress for the 5 post-processing steps
-- that run after /save (source_edges, claim_edges, graph_metrics,
-- state_summaries, anticipations).

CREATE TABLE IF NOT EXISTS post_processing_status (
    source_id       TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    step            TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    result          JSONB DEFAULT '{}',
    error           TEXT,
    attempt_count   INTEGER DEFAULT 0,
    PRIMARY KEY (source_id, step)
);

CREATE INDEX IF NOT EXISTS idx_pp_pending
    ON post_processing_status(step, status)
    WHERE status = 'pending';

CREATE INDEX IF NOT EXISTS idx_pp_source
    ON post_processing_status(source_id);
