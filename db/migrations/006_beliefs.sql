-- Migration 006: Belief System (Phase 4)
--
-- DB-backed beliefs that integrate bidirectionally with the landscape model.
-- Beliefs track the user's positions on claims about AI, with confidence,
-- evidence tracking, history, and links to themes and anticipations.

CREATE TABLE IF NOT EXISTS beliefs (
    id               TEXT PRIMARY KEY,
    claim            TEXT NOT NULL,
    confidence       FLOAT NOT NULL DEFAULT 0.5,
    status           TEXT DEFAULT 'active',       -- active | resolved | archived
    belief_type      TEXT DEFAULT 'factual',      -- factual | predictive | methodological | meta
    domain_theme_id  TEXT,                         -- primary theme link (queryable FK)
    landscape_links  JSONB DEFAULT '[]',           -- [{type: 'capability'|'limitation'|'bottleneck'|'anticipation', id: ...}]
    evidence_for     JSONB DEFAULT '[]',           -- [{source_id, claim_id?, snippet, added_at}]
    evidence_against JSONB DEFAULT '[]',           -- [{source_id, claim_id?, snippet, added_at}]
    derived_anticipations JSONB DEFAULT '[]',      -- anticipation IDs this belief generated
    parent_belief_id TEXT,                         -- for decomposed sub-beliefs
    history          JSONB DEFAULT '[]',           -- [{ts, old_conf, new_conf, trigger, trigger_type}]
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    last_updated     TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (domain_theme_id) REFERENCES themes(id),
    FOREIGN KEY (parent_belief_id) REFERENCES beliefs(id)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_beliefs_domain ON beliefs(domain_theme_id);
CREATE INDEX IF NOT EXISTS idx_beliefs_status ON beliefs(status);
CREATE INDEX IF NOT EXISTS idx_beliefs_confidence ON beliefs(confidence);
CREATE INDEX IF NOT EXISTS idx_beliefs_type ON beliefs(belief_type);
CREATE INDEX IF NOT EXISTS idx_beliefs_parent ON beliefs(parent_belief_id);

-- Trigram index for deduplication / similarity search
CREATE INDEX IF NOT EXISTS idx_beliefs_claim_trgm
    ON beliefs USING gin(claim gin_trgm_ops);
