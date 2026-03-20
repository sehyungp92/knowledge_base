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

2. **Query Graph** (use progressive fallback — always render something useful):
   - **Level 1**: Direct edges (source_edges) — edge type, explanation, confidence
   - **Level 2**: 2-hop via shared concepts — sources sharing >= 2 concepts
   - **Level 3**: Thematic proximity — sources in the same themes
   - **Level 4**: Cross-theme implications — if the source's themes have implications linking to other themes

   If Level 1 (source_edges) returns no results, DO NOT report "no edges found" and stop.
   Instead, fall through to Level 2-4 and build the map from whatever is available.

3. **Build Map**:
   - Center node: the queried concept/source
   - Connected nodes with edge types and confidence
   - Shared concepts as bridge labels
   - Theme membership as context
   - If only thematic proximity is available, show the theme DAG neighborhood with velocity metrics

4. **Always show**:
   - Theme(s) the source belongs to, with velocity
   - Concept list for the source (even if no edges exist)
   - Cross-theme implications touching this source's themes

5. **Return Response** — ASCII graph representation for Telegram:
   ```
   [Source A] --extends--> [Source B]
        |                      |
        +--shares: "RLHF", "alignment"--+
        |
   [Source C] --contradicts--> [Source A]

   Theme: Agent Systems (velocity: 0.8)
   Concepts: RLHF, alignment, reward hacking
   ```

   If no direct edges exist, render the concept/theme neighborhood instead:
   ```
   Theme: [Agent Systems] (velocity: 0.8)
     Sources: [Source A], [Source B], [Source C]
     Shared concepts: "tool use", "planning", "memory"
     Cross-theme link → [Robotics]: "Agent architectures transfer to embodied systems"
   ```
