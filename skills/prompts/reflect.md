---
name: reflect
description: Generate connections and ideas from a source
---

# /reflect Skill

You are executing the /reflect skill to find connections and generate ideas from a source.

## Modes

Parse the command: `/reflect {source_id}` (simple mode) or `/reflect {source_id} deep` (tournament mode).

- **Simple mode** (default): 8-step graph traversal, produces 3-5 ideas quickly.
- **Deep mode**: Invokes the full 11-step tournament pipeline (novelty gate, critique, two-tier debate, evolution) with landscape context. Produces higher-quality, more rigorously vetted ideas but takes longer.

## Safety
- Only cite claims with evidence from the library
- Do not fabricate connections — all links must trace to actual claims
- Do not modify source files

## Execution Contract (Simple Mode)

1. **Load Source** — read library/{source_id}/extractions.json and deep_summary.md

2. **Query Graph** — find 1-hop and 2-hop connections via shared concepts and claim edges

3. **Hybrid Retrieval** — find semantically similar claims across the library

4. **Identify Connections** — for each related source:
   - What claims support, extend, or contradict each other?
   - What shared concepts bridge these sources?

5. **Generate Ideas** — propose 3-5 ideas based on the connections found:
   - Synthesis: combining insights from multiple sources
   - Transfer: applying a method from one domain to another
   - Contradiction resolution: reconciling conflicting claims
   - Extension: what would happen if a finding were pushed further?

6. **Save Reflection** — write to library/{source_id}/reflection.md

7. **Update Memory** — append ideas to today's log

8. **Return Response** — format connections and ideas for Telegram

## Execution Contract (Deep Mode)

When the user specifies "deep", run the full tournament pipeline:

1. **Load Source** — same as simple mode (extractions.json + deep_summary.md)

2. **Query Graph** — same as simple mode (1-hop + 2-hop connections)

3. **Build Tournament Goal** — construct a TournamentGoal from the connections found:
   ```python
   from agents.generate import TournamentGoal
   from agents.tournament import TournamentPipeline
   from agents.executor import ClaudeExecutor
   from reading_app.db import get_conn
   from pathlib import Path

   goal = TournamentGoal(
       description="Generate ideas building on {source_id} and its connections",
       focus_themes=source_themes,  # from source_themes table
   )
   ```

4. **Run Tournament** — execute the 11-step pipeline with time budgeting:
   ```python
   executor = ClaudeExecutor(Path("workspace"))
   pipeline = TournamentPipeline(executor, get_conn_fn=get_conn, library_path=Path("library"))
   # Pass timeout from the Runtime Budget section (default 540 if not specified)
   result = pipeline.run(source_id=source_id, depth="deep", goal=goal, timeout=540)
   ```
   The pipeline will gracefully skip non-critical steps (debate, evolution) if the deadline is exceeded, ensuring you always get results even if time runs short.

5. **Save Reflection** — write tournament results to library/{source_id}/reflection.md, including:
   - Number of ideas generated, survived novelty gate, survived debate
   - Top ideas with scores, rationale, grounding
   - Total calls used

6. **Update Memory** — append top ideas to today's log

7. **Return Response** — format as:
   ```
   🏆 Tournament complete: {result.ideas_generated} generated → {result.ideas_after_novelty} novel → {len(result.ideas)} final

   Top ideas:
   1. [score] idea_text (type: strategy)
      Grounding: source citations
   ...
   ```
