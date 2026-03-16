-- Drop claim_edges table.
-- This table used regex heuristics on claim text to classify relationships,
-- never produced usable data (0 rows across 582 sources), and has been
-- replaced by source_edges (LLM-classified) and embedding similarity search.

DROP TABLE IF EXISTS claim_edges;

-- Clean up any lingering post_processing_status rows for the removed step
DELETE FROM post_processing_status WHERE step = 'claim_edges';
