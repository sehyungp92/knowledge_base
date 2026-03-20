-- Add evidence_validation column to claims table.
-- Tracks whether a claim's evidence passed strict (0.80 word overlap)
-- or relaxed (0.55) validation during extraction.
-- NULL = strict (default, pre-existing claims).

ALTER TABLE claims ADD COLUMN IF NOT EXISTS evidence_validation TEXT;
