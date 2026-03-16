-- Migration 013: Clean up legacy L1 themes
-- Merges 7 orphan L1 themes into structured taxonomy,
-- converts 6 to L2, promotes 2 to structured L1 with meta-domain edges.
--
-- All tables with theme_id FK: source_themes, capabilities, limitations,
-- bottlenecks, breakthroughs, anticipations, cross_theme_implications (x2),
-- theme_edges (x2), theme_proposals, beliefs, theme_edge_proposals (x2)

-- Helper: for each merge, we must update ALL referencing tables before DELETE.
-- Pattern: UPDATE or DELETE refs in every FK table, then DELETE theme.

-- ================================================================
-- PART 1: Merge legacy L1 into structured L1
-- ================================================================

-- 1a. ai_ethics → safety_and_alignment
UPDATE source_themes SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'safety_and_alignment');
DELETE FROM source_themes WHERE theme_id = 'ai_ethics';
UPDATE capabilities SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics';
UPDATE limitations SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics';
UPDATE bottlenecks SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics';
UPDATE breakthroughs SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics';
UPDATE anticipations SET theme_id = 'safety_and_alignment' WHERE theme_id = 'ai_ethics';
UPDATE cross_theme_implications SET source_theme_id = 'safety_and_alignment' WHERE source_theme_id = 'ai_ethics';
UPDATE cross_theme_implications SET target_theme_id = 'safety_and_alignment' WHERE target_theme_id = 'ai_ethics';
UPDATE beliefs SET domain_theme_id = 'safety_and_alignment' WHERE domain_theme_id = 'ai_ethics';
UPDATE theme_proposals SET parent_id = 'safety_and_alignment' WHERE parent_id = 'ai_ethics';
UPDATE theme_edge_proposals SET source_theme_id = 'safety_and_alignment' WHERE source_theme_id = 'ai_ethics';
UPDATE theme_edge_proposals SET target_theme_id = 'safety_and_alignment' WHERE target_theme_id = 'ai_ethics';
DELETE FROM theme_edges WHERE parent_id = 'ai_ethics' OR child_id = 'ai_ethics';
DELETE FROM themes WHERE id = 'ai_ethics';

-- 1b. economic_impact → ai_economics
UPDATE source_themes SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'ai_economics');
DELETE FROM source_themes WHERE theme_id = 'economic_impact';
UPDATE capabilities SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact';
UPDATE limitations SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact';
UPDATE bottlenecks SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact';
UPDATE breakthroughs SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact';
UPDATE anticipations SET theme_id = 'ai_economics' WHERE theme_id = 'economic_impact';
UPDATE cross_theme_implications SET source_theme_id = 'ai_economics' WHERE source_theme_id = 'economic_impact';
UPDATE cross_theme_implications SET target_theme_id = 'ai_economics' WHERE target_theme_id = 'economic_impact';
UPDATE beliefs SET domain_theme_id = 'ai_economics' WHERE domain_theme_id = 'economic_impact';
UPDATE theme_proposals SET parent_id = 'ai_economics' WHERE parent_id = 'economic_impact';
UPDATE theme_edge_proposals SET source_theme_id = 'ai_economics' WHERE source_theme_id = 'economic_impact';
UPDATE theme_edge_proposals SET target_theme_id = 'ai_economics' WHERE target_theme_id = 'economic_impact';
DELETE FROM theme_edges WHERE parent_id = 'economic_impact' OR child_id = 'economic_impact';
DELETE FROM themes WHERE id = 'economic_impact';

-- 1c. embodied_intelligence → robotics
UPDATE source_themes SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'robotics');
DELETE FROM source_themes WHERE theme_id = 'embodied_intelligence';
UPDATE capabilities SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence';
UPDATE limitations SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence';
UPDATE bottlenecks SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence';
UPDATE breakthroughs SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence';
UPDATE anticipations SET theme_id = 'robotics' WHERE theme_id = 'embodied_intelligence';
UPDATE cross_theme_implications SET source_theme_id = 'robotics' WHERE source_theme_id = 'embodied_intelligence';
UPDATE cross_theme_implications SET target_theme_id = 'robotics' WHERE target_theme_id = 'embodied_intelligence';
UPDATE beliefs SET domain_theme_id = 'robotics' WHERE domain_theme_id = 'embodied_intelligence';
UPDATE theme_proposals SET parent_id = 'robotics' WHERE parent_id = 'embodied_intelligence';
UPDATE theme_edge_proposals SET source_theme_id = 'robotics' WHERE source_theme_id = 'embodied_intelligence';
UPDATE theme_edge_proposals SET target_theme_id = 'robotics' WHERE target_theme_id = 'embodied_intelligence';
DELETE FROM theme_edges WHERE parent_id = 'embodied_intelligence' OR child_id = 'embodied_intelligence';
DELETE FROM themes WHERE id = 'embodied_intelligence';

-- 1d. scaling_and_architecture → architectural_innovation
UPDATE source_themes SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'architectural_innovation');
DELETE FROM source_themes WHERE theme_id = 'scaling_and_architecture';
UPDATE capabilities SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture';
UPDATE limitations SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture';
UPDATE bottlenecks SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture';
UPDATE breakthroughs SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture';
UPDATE anticipations SET theme_id = 'architectural_innovation' WHERE theme_id = 'scaling_and_architecture';
UPDATE cross_theme_implications SET source_theme_id = 'architectural_innovation' WHERE source_theme_id = 'scaling_and_architecture';
UPDATE cross_theme_implications SET target_theme_id = 'architectural_innovation' WHERE target_theme_id = 'scaling_and_architecture';
UPDATE beliefs SET domain_theme_id = 'architectural_innovation' WHERE domain_theme_id = 'scaling_and_architecture';
UPDATE theme_proposals SET parent_id = 'architectural_innovation' WHERE parent_id = 'scaling_and_architecture';
UPDATE theme_edge_proposals SET source_theme_id = 'architectural_innovation' WHERE source_theme_id = 'scaling_and_architecture';
UPDATE theme_edge_proposals SET target_theme_id = 'architectural_innovation' WHERE target_theme_id = 'scaling_and_architecture';
DELETE FROM theme_edges WHERE parent_id = 'scaling_and_architecture' OR child_id = 'scaling_and_architecture';
DELETE FROM themes WHERE id = 'scaling_and_architecture';

-- 1e. training_paradigms → learning_dynamics
UPDATE source_themes SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'learning_dynamics');
DELETE FROM source_themes WHERE theme_id = 'training_paradigms';
UPDATE capabilities SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms';
UPDATE limitations SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms';
UPDATE bottlenecks SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms';
UPDATE breakthroughs SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms';
UPDATE anticipations SET theme_id = 'learning_dynamics' WHERE theme_id = 'training_paradigms';
UPDATE cross_theme_implications SET source_theme_id = 'learning_dynamics' WHERE source_theme_id = 'training_paradigms';
UPDATE cross_theme_implications SET target_theme_id = 'learning_dynamics' WHERE target_theme_id = 'training_paradigms';
UPDATE beliefs SET domain_theme_id = 'learning_dynamics' WHERE domain_theme_id = 'training_paradigms';
UPDATE theme_proposals SET parent_id = 'learning_dynamics' WHERE parent_id = 'training_paradigms';
UPDATE theme_edge_proposals SET source_theme_id = 'learning_dynamics' WHERE source_theme_id = 'training_paradigms';
UPDATE theme_edge_proposals SET target_theme_id = 'learning_dynamics' WHERE target_theme_id = 'training_paradigms';
DELETE FROM theme_edges WHERE parent_id = 'training_paradigms' OR child_id = 'training_paradigms';
DELETE FROM themes WHERE id = 'training_paradigms';

-- 1f. governance_and_regulation → safety_and_alignment
UPDATE source_themes SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'safety_and_alignment');
DELETE FROM source_themes WHERE theme_id = 'governance_and_regulation';
UPDATE capabilities SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation';
UPDATE limitations SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation';
UPDATE bottlenecks SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation';
UPDATE breakthroughs SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation';
UPDATE anticipations SET theme_id = 'safety_and_alignment' WHERE theme_id = 'governance_and_regulation';
UPDATE cross_theme_implications SET source_theme_id = 'safety_and_alignment' WHERE source_theme_id = 'governance_and_regulation';
UPDATE cross_theme_implications SET target_theme_id = 'safety_and_alignment' WHERE target_theme_id = 'governance_and_regulation';
UPDATE beliefs SET domain_theme_id = 'safety_and_alignment' WHERE domain_theme_id = 'governance_and_regulation';
UPDATE theme_proposals SET parent_id = 'safety_and_alignment' WHERE parent_id = 'governance_and_regulation';
UPDATE theme_edge_proposals SET source_theme_id = 'safety_and_alignment' WHERE source_theme_id = 'governance_and_regulation';
UPDATE theme_edge_proposals SET target_theme_id = 'safety_and_alignment' WHERE target_theme_id = 'governance_and_regulation';
DELETE FROM theme_edges WHERE parent_id = 'governance_and_regulation' OR child_id = 'governance_and_regulation';
DELETE FROM themes WHERE id = 'governance_and_regulation';

-- 1g. genomics_and_proteins → scientific_discovery
UPDATE source_themes SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins' AND NOT EXISTS (SELECT 1 FROM source_themes x WHERE x.source_id = source_themes.source_id AND x.theme_id = 'scientific_discovery');
DELETE FROM source_themes WHERE theme_id = 'genomics_and_proteins';
UPDATE capabilities SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins';
UPDATE limitations SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins';
UPDATE bottlenecks SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins';
UPDATE breakthroughs SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins';
UPDATE anticipations SET theme_id = 'scientific_discovery' WHERE theme_id = 'genomics_and_proteins';
UPDATE cross_theme_implications SET source_theme_id = 'scientific_discovery' WHERE source_theme_id = 'genomics_and_proteins';
UPDATE cross_theme_implications SET target_theme_id = 'scientific_discovery' WHERE target_theme_id = 'genomics_and_proteins';
UPDATE beliefs SET domain_theme_id = 'scientific_discovery' WHERE domain_theme_id = 'genomics_and_proteins';
UPDATE theme_proposals SET parent_id = 'scientific_discovery' WHERE parent_id = 'genomics_and_proteins';
UPDATE theme_edge_proposals SET source_theme_id = 'scientific_discovery' WHERE source_theme_id = 'genomics_and_proteins';
UPDATE theme_edge_proposals SET target_theme_id = 'scientific_discovery' WHERE target_theme_id = 'genomics_and_proteins';
DELETE FROM theme_edges WHERE parent_id = 'genomics_and_proteins' OR child_id = 'genomics_and_proteins';
DELETE FROM themes WHERE id = 'genomics_and_proteins';

-- ================================================================
-- PART 2: Convert 6 legacy L1 to L2 under existing parents
-- ================================================================

UPDATE themes SET level = 2 WHERE id = 'drug_discovery';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('scientific_discovery', 'drug_discovery', 'contains', 1.0) ON CONFLICT DO NOTHING;

UPDATE themes SET level = 2 WHERE id = 'medical_ai';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('scientific_discovery', 'medical_ai', 'contains', 1.0) ON CONFLICT DO NOTHING;

UPDATE themes SET level = 2 WHERE id = 'self_driving';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('robotics', 'self_driving', 'contains', 1.0) ON CONFLICT DO NOTHING;

UPDATE themes SET level = 2 WHERE id = 'personal_assistants';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('autonomous_agents', 'personal_assistants', 'contains', 1.0) ON CONFLICT DO NOTHING;

UPDATE themes SET level = 2 WHERE id = 'neuroscience_intersection';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('architectural_innovation', 'neuroscience_intersection', 'contains', 1.0) ON CONFLICT DO NOTHING;

UPDATE themes SET level = 2 WHERE id = 'data';
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('learning_dynamics', 'data', 'contains', 1.0) ON CONFLICT DO NOTHING;

-- ================================================================
-- PART 3: Promote 2 legacy L1 to structured L1 (add meta-domain edge)
-- ================================================================

INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('meta_foundations', 'memory_and_context', 'contains', 1.0) ON CONFLICT DO NOTHING;
INSERT INTO theme_edges (parent_id, child_id, relationship, strength) VALUES ('meta_capabilities', 'creative_generation', 'contains', 1.0) ON CONFLICT DO NOTHING;
