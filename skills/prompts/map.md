---
name: map
description: Show concept neighborhood in knowledge graph
---

# /map Skill

You are executing the /map skill to visualize the neighborhood of a concept or source in the knowledge graph.

## Safety
- Read-only — do not modify any data
- Only show verified edges with evidence

## Execution Contract

1. **Parse Input** — identify the concept or source_id

2. **Query Graph**:
   - 1-hop: direct edges (source_edges, claim_edges)
   - 2-hop via concepts: sources sharing >= 2 concepts
   - 2-hop via claims: sources with related claims

3. **Build Map**:
   - Center node: the queried concept/source
   - Connected nodes with edge types and confidence
   - Shared concepts as bridge labels

4. **Return Response** — ASCII graph representation for Telegram:
   ```
   [Source A] --extends--> [Source B]
        |                      |
        +--shares: "RLHF", "alignment"--+
        |
   [Source C] --contradicts--> [Source A]
   ```
