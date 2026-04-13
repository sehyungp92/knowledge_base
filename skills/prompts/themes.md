---
name: themes
description: Review theme proposals, view taxonomy hierarchy, and manage edge proposals
---

# /themes Skill

## Safety
- Only write to themes, theme_edges, theme_proposals, theme_edge_proposals tables
- Validate proposed_theme_id is snake_case: ^[a-z][a-z0-9_]*$
- Check uniqueness before inserting
- Never insert level-0 meta nodes via approve — only level-1 and level-2
- Level-2 proposals with a valid parent_id are auto-approved at ingest time;
  level-1 proposals always require human review here

## Execution Contract

### List mode (default: /themes)
1. Query pending proposals from theme_proposals (status='pending'), ordered by level ASC then created_at DESC
2. For each proposal, show: level badge [L1] or [L2], name, id, description, parent, edges, trigger reason, source
3. Show approve/reject commands
4. If no pending proposals, show count summary: "No pending proposals. X subthemes, Y subsubthemes in taxonomy."

### Approve mode (/themes approve {id})
1. Fetch proposal WHERE status='pending'
2. Validate snake_case id and uniqueness against themes table
3. Call `reading_app.db.materialize_theme_proposal(proposal_id)` — this handles:
   - INSERT into themes with correct level
   - INSERT 'contains' edge to parent
   - INSERT suggested_edges
   - UPDATE proposal status to 'approved'
4. Call `ingest.theme_classifier.refresh_static_theme_block(get_conn)` to update classifier
5. Create wiki page for the new theme (best-effort, do not abort on failure):
   ```python
   from retrieval.wiki_migration import migrate_theme_new
   from retrieval.landscape import get_theme_state
   theme_data = get_theme_state(theme_id)
   theme_data["source_count"] = 0
   theme_data["theme_edges"] = {"parent_id": parent_id or "", "child_ids": []}
   migrate_theme_new(theme_id, theme_data, executor)
   ```
6. Confirm: "Theme **{name}** (`{id}`) added at level {level}."

### Reject mode (/themes reject {id})
1. Mark proposal rejected (reviewed_at = NOW())
2. Confirm: "Proposal `{id}` rejected."

### Hierarchy mode (/themes hierarchy)
1. Query all themes with level and source count:
   ```sql
   SELECT t.id, t.name, t.level,
          COUNT(DISTINCT st.source_id) AS source_count
   FROM themes t
   LEFT JOIN source_themes st ON st.theme_id = t.id
   GROUP BY t.id, t.name, t.level
   ORDER BY t.level, t.id
   ```
2. Query HIERARCHY_EDGES (relationship='contains') to build parent→child map
3. Render ASCII tree:
   ```
   Intelligence Foundations (meta_foundations)
   ├── Reasoning & Planning (reasoning_and_planning) [12 sources]
   │   ├── MCTS & Tree Search (mcts_and_tree_search) [3 sources]
   │   ├── Chain-of-Thought (chain_of_thought) [8 sources]
   │   └── ...
   └── ...
   ```
4. Show total counts: "X meta | Y subthemes | Z subsubthemes | N total sources classified"

### Edges mode (/themes edges)
1. Query pending theme_edge_proposals ordered by co_occurrence_count DESC
2. For each, show: source_name → target_name, count, suggested_relationship, strength
3. Show approve/reject commands: `/themes approve-edge {id}`, `/themes reject-edge {id}`

### Approve-edge mode (/themes approve-edge {id})
1. Fetch edge proposal WHERE status='pending'
2. Insert into theme_edges (parent_id=source_theme_id, child_id=target_theme_id, relationship, strength)
3. Mark proposal approved
4. Confirm: "Edge **{source_name}** → **{target_name}** (`{relationship}`) added."

### Reject-edge mode (/themes reject-edge {id})
1. Mark edge proposal rejected
2. Confirm: "Edge proposal `{id}` rejected."

### Evolve mode (/themes evolve)
Manually trigger a taxonomy health check to propose structural changes.

1. Call `scripts.taxonomy_health.run_health_check(dsn, library_path)` using:
   ```python
   from reading_app.config import Config
   from reading_app.db import init_pool, ensure_pool
   from scripts.taxonomy_health import run_health_check
   config = Config()
   ensure_pool()
   proposals = run_health_check(config.postgres_dsn, config.library_path)
   ```
2. If proposals were generated, display each with:
   - Change type badge: [split_l2], [merge_l2], [new_l2], [new_l1], [rename], [reparent]
   - Target theme (if applicable) with current source count
   - Proposed changes (new IDs, names, descriptions)
   - Rationale with evidence
3. Show available commands: `/themes review-evolution` to approve/reject
4. If no proposals: "Taxonomy is healthy — no structural issues detected."

### Review-evolution mode (/themes review-evolution)
Review and approve/reject pending taxonomy evolution proposals.

1. Query pending proposals via `reading_app.db.get_pending_evolution_proposals()`
2. For each proposal, display:
   - ID, change type, target theme
   - Proposed changes details
   - Rationale and evidence
3. For each proposal, user can:
   - **Approve**:
     1. Call `scripts.taxonomy_health.apply_evolution_proposal(dsn, id)` — DB changes
     2. Execute wiki migration (best-effort, do not abort on failure):
        ```python
        from retrieval.wiki_migration import execute_wiki_migration
        result = execute_wiki_migration(
            {"change_type": proposal["change_type"],
             "target_theme_id": proposal["target_theme_id"],
             "proposed_changes": proposal["proposed_changes"]},
            executor,
        )
        ```
     3. Report wiki changes: "{pages_created} pages created, {pages_deleted} deleted"
        If result has errors, log them but do not fail the approval.
   - **Reject**: Call `reading_app.db.resolve_evolution_proposal(id, 'rejected')`
4. Confirm: "Applied {n} proposals, rejected {m}. Taxonomy updated."
