-- Migration 010: Add source_published_at to landscape_history
-- Distinguishes "when the field changed" from "when we learned about it"
-- by storing the publication date of the source that triggered the change.

ALTER TABLE landscape_history
    ADD COLUMN IF NOT EXISTS source_published_at TIMESTAMPTZ;

-- Backfill from sources table where possible
UPDATE landscape_history lh
SET source_published_at = s.published_at
FROM sources s
WHERE lh.source_id = s.id
  AND s.published_at IS NOT NULL
  AND lh.source_published_at IS NULL;
