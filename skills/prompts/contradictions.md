---
name: contradictions
description: Show conflicting claims on a topic
---

# /contradictions Skill

You are executing the /contradictions skill to find conflicting claims.

## Safety
- Read-only — do not modify any data
- Both sides of a contradiction must have evidence citations

## Execution Contract

1. **Parse Input** — identify topic, concept, or source to check

2. **Find Contradictions**:
   - Query claim_edges where edge_type = 'contradicts'
   - Use embedding similarity to find high-similarity claims with opposing content
   - Threshold: cosine similarity > 0.85 between claims

3. **Present Contradictions** — for each pair:
   - Claim A with source and evidence
   - Claim B with source and evidence
   - Possible explanations for the discrepancy

4. **Return Response** — formatted contradiction pairs for Telegram
