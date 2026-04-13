-- Concept-level semantic edges: explicit typed relationships between concepts.
-- Populated selectively during /save for high-confidence co-occurring concepts.

CREATE TABLE IF NOT EXISTS concept_edges (
    id              SERIAL PRIMARY KEY,
    concept_a_id    TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    concept_b_id    TEXT NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    edge_type       TEXT NOT NULL CHECK (edge_type IN (
        'alternative_to', 'builds_on', 'contrasts_with',
        'enables', 'specializes', 'component_of'
    )),
    confidence      REAL DEFAULT 0.7,
    evidence_source TEXT,  -- source_id that triggered this edge
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (concept_a_id, concept_b_id, edge_type)
);

CREATE INDEX IF NOT EXISTS idx_concept_edges_a ON concept_edges(concept_a_id);
CREATE INDEX IF NOT EXISTS idx_concept_edges_b ON concept_edges(concept_b_id);
CREATE INDEX IF NOT EXISTS idx_concept_edges_type ON concept_edges(edge_type);
