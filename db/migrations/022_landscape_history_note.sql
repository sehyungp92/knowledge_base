-- Add note column to landscape_history for contextual information
-- (e.g., breakthrough description that triggered a bottleneck change)
ALTER TABLE landscape_history ADD COLUMN IF NOT EXISTS note TEXT;
