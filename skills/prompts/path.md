---
name: path
description: Explain connection path between two sources
---

# /path Skill

You are executing the /path skill to explain how two sources are connected.

## Safety
- Read-only — do not modify any data
- All path explanations must trace through actual evidence

## Execution Contract

1. **Parse Input** — identify source_a and source_b IDs

2. **Find Paths** — use recursive CTE to find paths up to 3 hops:
   - Direct edges between sources
   - Paths via shared concepts
   - Paths via claim relationships

3. **Explain Path** — for each path found:
   - List each hop with edge type
   - Quote evidence snippets at each connection
   - Note confidence levels

4. **Return Response** — formatted path explanation for Telegram
