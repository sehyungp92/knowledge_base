-- Add would_confirm and would_invalidate columns to anticipations.
-- The LLM already generates these criteria during /anticipate generate
-- but they were discarded because the schema had no columns for them.

ALTER TABLE anticipations ADD COLUMN IF NOT EXISTS would_confirm TEXT;
ALTER TABLE anticipations ADD COLUMN IF NOT EXISTS would_invalidate TEXT;
