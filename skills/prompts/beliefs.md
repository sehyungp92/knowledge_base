---
name: beliefs
description: View, update, and synthesize tracked beliefs
---

# /beliefs Skill

You are executing the /beliefs skill to manage the user's tracked beliefs about AI.

Beliefs are the third layer of the knowledge engine: where "what sources say" (knowledge graph)
and "what is true about AI" (landscape model) meet "what you think about what is true."
They are DB-backed with full history tracking, evidence linkage, and landscape integration.

## Safety
- Beliefs must be grounded in evidence from the library
- Never delete beliefs — only update confidence, resolve, or archive
- Never auto-update confidence without user confirmation
- Preserve attribution: distinguish user-created vs system-suggested beliefs

## Execution Contract

### Step 1: Parse Command

- `/beliefs` — list all active beliefs grouped by theme
- `/beliefs add <statement>` — add a new tracked belief
- `/beliefs update <id> <confidence>` — update confidence with trigger logging
- `/beliefs review` — review stale beliefs against recent evidence
- `/beliefs synthesis <topic>` — synthesize beliefs into coherent narrative
- `/beliefs <topic>` — filter to beliefs relevant to a topic/theme

### Step 2: Execute Mode

#### Mode: List (`/beliefs` or `/beliefs <topic>`)

1. Query `reading_app.db.get_active_beliefs()` (or `get_beliefs_for_theme()` if topic specified)
2. Group by theme (domain_theme_id)
3. Show confidence indicators: ● (>0.8), ◐ (0.4-0.8), ○ (<0.4)
4. Show evidence counts: {N} for / {M} against
5. Flag beliefs needing review (stale per velocity-aware staleness)

#### Mode: Add (`/beliefs add <statement>`)

1. Parse the statement as a belief claim
2. Check for similar existing beliefs via `reading_app.db.find_similar_belief()`
3. If similar belief exists, suggest updating that instead
4. Classify belief_type: factual, predictive, methodological, meta
5. Identify domain_theme_id from theme matching
6. Search the library for supporting and contradicting evidence
7. Suggest initial confidence based on evidence strength
8. Insert via `reading_app.db.insert_belief()` with:
   - Generated ID: `belief_{ULID()}`
   - Landscape links to relevant capabilities/limitations/bottlenecks
   - Evidence from library search
9. If belief_type is "predictive" and confidence >= 0.6:
   - Ask: "This belief implies testable predictions. Generate anticipations?"
   - If yes: create anticipations with belief_id in based_on JSONB
   - Link via `reading_app.db.append_belief_derived_anticipation()`

#### Mode: Update (`/beliefs update <id> <confidence>`)

1. Fetch current belief via `reading_app.db.get_belief()`
2. Validate new confidence (0.0-1.0)
3. Ask user for trigger reason (what prompted the update)
4. Update via `reading_app.db.update_belief_confidence()` with history entry
5. If confidence dropped below 0.3: suggest archiving
6. If confidence rose above 0.8: check for counter-evidence gaps

#### Mode: Review (`/beliefs review`)

1. Get stale beliefs via `reading_app.db.get_stale_beliefs()`
2. For each stale belief:
   a. Load recent sources for the belief's theme (last 30 days)
   b. Check if new evidence supports, contradicts, or extends the belief
   c. Present findings with suggested confidence direction
3. User confirms updates or dismisses

#### Mode: Synthesis (`/beliefs synthesis <topic>`)

1. Load synthesis context via `retrieval.landscape.get_beliefs_for_synthesis(topic)`
2. This provides: beliefs, themes, state summaries, recent breakthroughs
3. Generate a narrative synthesis:
   - "Your current position on [topic] is..."
   - "This rests on {N} tracked beliefs:"
   - For each belief: claim, confidence, key evidence
   - "The strongest evidence is..."
   - "Open questions remain about..."
   - "Recent landscape changes that may affect this: ..."
4. Detect internal tensions between beliefs:
   - If two beliefs in the set seem incompatible, flag as "belief tension"
   - Include: the two beliefs, the logical connection, what makes them tension-bearing
5. Identify coverage gaps:
   - "You have no tracked belief about [subtopic] despite {N} sources touching it"
6. Suggest next actions: review, add new beliefs, seek disconfirming sources

### Step 3: Return Response

```
{For list mode:}
**Tracked Beliefs** {for theme, if filtered}

**{Theme Name}** (velocity: {v})
● {belief_claim} [conf: {0.85}] — {N}↑ {M}↓
◐ {belief_claim} [conf: {0.55}] — {N}↑ {M}↓ ⚠ needs review
○ {belief_claim} [conf: {0.30}] — {N}↑ {M}↓

{For add mode:}
**Belief tracked:** {claim}
Type: {belief_type} | Theme: {theme_name} | Confidence: {initial}
Evidence: {N} supporting, {M} contradicting
Landscape links: {linked entities}
{If predictive: "Derived anticipation: {prediction}"}

{For synthesis mode:}
**Belief Synthesis: {topic}**

{3-5 paragraph narrative synthesizing the user's position}

**Belief Tensions:**
{Any detected tensions between beliefs}

**Coverage Gaps:**
{Topics with sources but no tracked beliefs}

**Suggested Actions:**
- /beliefs add ... for identified gaps
- /beliefs update ... for stale beliefs
```
