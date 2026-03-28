-- Correction examples for extraction learning loop
-- Stores paired corrections from /enrich and /challenge for few-shot injection

CREATE TABLE IF NOT EXISTS correction_examples (
    id SERIAL PRIMARY KEY,
    extraction_type TEXT NOT NULL,    -- 'capability', 'limitation', 'bottleneck', 'claim', 'implication'
    correction_type TEXT NOT NULL,    -- 'missed', 'wrong', 'spurious', 'reclassified'
    original_value JSONB,            -- what system extracted (NULL for 'missed')
    corrected_value JSONB,           -- what user provided
    source_context TEXT,             -- snippet of source text for few-shot context
    source_id TEXT,
    theme_id TEXT,
    skill_origin TEXT,               -- 'enrich', 'challenge'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_corrections_type ON correction_examples (extraction_type, correction_type);
CREATE INDEX IF NOT EXISTS idx_corrections_created ON correction_examples (created_at DESC);
