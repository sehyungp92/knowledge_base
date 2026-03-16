-- Migration 012: Remap themes after taxonomy regeneration
-- Lightweight migration — only 2 ingested sources in DB at time of writing.
--
-- This migration is a TEMPLATE. After running generate_taxonomy.py and
-- updating db/seed_themes.py with the new taxonomy, run seed_themes.py
-- which is idempotent (ON CONFLICT DO NOTHING).
--
-- This migration handles cleanup of old theme data that no longer exists
-- in the new taxonomy.

-- Step 1: Remove source_themes referencing themes that no longer exist
-- (safe because we only have 2 ingested sources — re-ingest is trivial)
DELETE FROM source_themes
WHERE theme_id NOT IN (SELECT id FROM themes);

-- Step 2: Remove cross_theme_implications referencing dead themes
DELETE FROM cross_theme_implications
WHERE source_theme_id NOT IN (SELECT id FROM themes)
   OR target_theme_id NOT IN (SELECT id FROM themes);

-- Step 3: Remove theme_edges referencing dead themes
DELETE FROM theme_edges
WHERE parent_id NOT IN (SELECT id FROM themes)
   OR child_id NOT IN (SELECT id FROM themes);

-- Step 4: Remove orphaned theme_proposals referencing dead parent themes
UPDATE theme_proposals
SET parent_id = NULL
WHERE parent_id IS NOT NULL
  AND parent_id NOT IN (SELECT id FROM themes);

-- Step 5: Remove landscape entities (capabilities, limitations, bottlenecks,
-- anticipations) tied to themes that no longer exist.
-- With only 2 sources, re-ingesting is cheaper than remapping.
DELETE FROM capabilities WHERE theme_id NOT IN (SELECT id FROM themes);
DELETE FROM limitations WHERE theme_id NOT IN (SELECT id FROM themes);
DELETE FROM bottlenecks WHERE theme_id NOT IN (SELECT id FROM themes);
DELETE FROM anticipations WHERE theme_id NOT IN (SELECT id FROM themes);

-- Step 6: Remove beliefs tied to dead themes
UPDATE beliefs
SET domain_theme_id = NULL
WHERE domain_theme_id IS NOT NULL
  AND domain_theme_id NOT IN (SELECT id FROM themes);
