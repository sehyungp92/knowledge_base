---
name: ask
description: Grounded QA over your library
---

# /ask Skill

You are executing the /ask skill to answer a question grounded in the user's library.

## Safety
- Only answer based on evidence in the library — never fabricate
- Cite source_id and evidence_snippet for every claim
- If insufficient evidence exists, say so explicitly

## Execution Contract

1. **Parse Question** — identify key concepts, entities, and intent

2. **Hybrid Retrieval** — search claims using vector + keyword fusion (RRF)

3. **Graph Context** — follow claim edges to find supporting/contradicting evidence

4. **Synthesize Answer** — combine evidence from multiple sources:
   - Lead with the direct answer
   - Support with evidence citations
   - Note contradictions or uncertainty

5. **Return Response** — format with inline citations:
   ```
   {Answer paragraph with [source_id] citations}

   Sources:
   - [source_id] "Title" — {relevant snippet}
   ```
