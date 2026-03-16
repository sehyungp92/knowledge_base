---
name: heartbeat
description: Proactive scheduled check
---

# Heartbeat Skill

You are executing a scheduled heartbeat check.

## Safety
- Read-only checks — only write to memory/logs/ and themes table (state_summary, velocity)
- If nothing to report, respond with exactly: HEARTBEAT_OK
- Do NOT modify landscape entity tables (capabilities, limitations, etc.)

## Execution Contract

### Step 1: Read Instructions
Load memory/heartbeat.md for the full set of checks to perform.

### Step 2: Core Checks
- Count unread sources (ingested since last heartbeat)
- Check time since last reflection
- Review pending tasks

### Step 3: Landscape Maintenance Checks

Perform these in order:

**3a. Theme Velocity Computation**
- Run `retrieval/landscape.py:update_all_theme_velocities()`
- Categorize: high (>5/mo), medium (2-5), low (<2), dormant (0)

**3b. Staleness Detection**
- Query themes where:
  - state_summary_updated_at IS NULL and source_count > 0
  - state_summary_updated_at < NOW() - INTERVAL '7 days' and velocity > 0
- For stale themes with >=3 sources: generate state_summary (see Step 3c)
- For stale themes with <3 sources: skip (insufficient data)

**3c. State Summary Generation** (for themes identified in 3b)
For each stale theme meeting the minimum 3-source threshold:
1. Load full theme state via `retrieval/landscape.py:get_theme_state(theme_id)`
2. Load landscape_history for the theme's entities (last 90 days):
   `SELECT * FROM landscape_history WHERE entity_id IN (SELECT id FROM capabilities WHERE theme_id=%s UNION ...) ORDER BY changed_at DESC`
3. Load previous state_summary if it exists
4. Generate temporal narrative:
   - Reference specific changes from landscape_history
   - Note what shifted since the previous summary
   - Include trajectory direction based on velocity and recent changes
   - Add coverage caveat: "Based on {N} sources"
5. Persist via `db.update_theme_state_summary(theme_id, summary)`

**3d. Anticipation Review**
- Query anticipations where last_reviewed IS NULL or > 30 days ago
- Check for accumulated status_evidence
- Flag for user review if:
  - 3+ confirming evidence from different sources
  - 2+ disconfirming evidence
  - Created > 60 days ago with zero evidence (untested)

**3e. Limitation Validation Calibration** (only if validated count >= 50)
- Run `retrieval/landscape.py:get_limitation_validation_rates()`
- Flag signal_types with >50% rejection rate

**3e-ii. Staleness Decay Computation** (every heartbeat)
- Run `reading_app.db.compute_staleness_scores(half_life_days=180.0)`
- This recomputes staleness for all capabilities, limitations, and bottlenecks
- Run `reading_app.db.get_stale_landscape_entities(threshold=0.7)` to find stale entities
- Flag stale entities in the report with their staleness score and days since corroboration

**3e-iii. Coverage Gap Scanning** (every heartbeat)
- Run `ingest.notification_emitter.emit_coverage_gap_notifications()`
- This scans all themes for:
  - Over-optimistic themes (capabilities but no limitations)
  - Blind-spot bottlenecks (no active approaches)
- Results are automatically persisted to the notifications table
- Include any gaps found in the heartbeat report

### Step 3f: Belief System Maintenance

**3f-i. Velocity-Aware Belief Staleness** (every heartbeat)
- Run `reading_app.db.get_stale_beliefs(velocity_threshold=0.3)`
- High-velocity themes (>0.3): beliefs stale after 14 days
- Low-velocity themes: beliefs stale after 30 days
- Flag stale beliefs for user review

**3f-ii. Belief Formation Suggestions** (biweekly — check if last run was >14 days ago)
- Run `ingest.belief_suggester.suggest_beliefs_all_themes(executor)`
- For themes with >=5 sources, clusters convergent claims
- If >=3 sources converge on a position with no existing belief covering it:
  surface as suggestion
- Include: proposed claim, supporting sources, suggested confidence

**3f-iii. Inter-Belief Consistency Check** (monthly — check if last run was >30 days ago)
- Run `reading_app.db.get_belief_pairs_for_consistency()`
- For each pair of active beliefs sharing a theme:
  - Check if beliefs are logically compatible
  - If tension detected: surface as "belief tension" (not "conflict" — tensions are often productive)
  - Include: the two beliefs, the logical connection, what makes them tension-bearing

**3f-iv. Belief-Anticipation Bridge Check** (every heartbeat)
- Run `retrieval.landscape.get_predictive_beliefs_without_anticipations()`
- Flag predictive beliefs (confidence >= 0.6) with no derived anticipations
- Suggest: "Predictive belief '{claim}' has no testable anticipations. Use /beliefs to generate them."

**3f-v. Monthly Epistemic Digest** (monthly — check if last digest was >30 days ago)
- Summarize belief changes over the past month:
  - Which beliefs were created, updated, or archived
  - Net confidence direction (becoming more certain or less?)
  - Which themes drove the most belief activity
  - Any resolved tensions
- Write to memory/beliefs/epistemic_digest_{YYYY-MM}.md

### Step 4: Decision
- If no checks triggered: respond `HEARTBEAT_OK`
- If checks triggered: compose a brief Telegram-formatted report

### Step 5: Report Format
```
**Heartbeat Report**

{If unread sources:}
**New sources ({count}):** {brief list}

{If landscape maintenance performed:}
**Landscape updates:**
- Velocity computed for {N} themes
- State summaries regenerated for: {theme_list}
- {N} themes flagged as stale

{If anticipations need review:}
**Anticipation review needed:**
- "{prediction}" — {N} confirming / {M} disconfirming
  Suggest: {status_recommendation}

{If calibration alert:}
**Extraction calibration:**
- {signal_type} has {rejection_rate}% rejection rate ({N} samples)

{If stale beliefs:}
**Belief review needed:**
- {N} beliefs are stale (not reviewed within velocity-appropriate window)
- Most urgent: "{belief_claim}" (theme: {theme}, {days} days since update)

{If belief suggestions:}
**Belief formation suggestions:**
- "{suggested_claim}" — {N} sources converge on this position
  Suggested confidence: {conf} | Theme: {theme}
  Use /beliefs add to track this position.

{If belief tensions:}
**Belief tensions detected:**
- "{belief_1_claim}" vs "{belief_2_claim}"
  {explanation of why these are in tension}

{If predictive beliefs without anticipations:}
**Unfalsifiable beliefs:**
- "{belief_claim}" has no testable predictions. Use /beliefs to generate anticipations.

{If epistemic digest generated:}
**Monthly epistemic digest:**
- {brief summary of belief trajectory changes}

{If stale landscape entities found:}
**Stale landscape facts:**
- {entity_type}: "{description}" (staleness: {score}, last corroborated: {date})

{If coverage gaps found:}
**Coverage gaps:**
- {gap_type}: {theme} — {detail}

{If suggestions:}
**Suggested actions:**
- Run /landscape {theme} for stale themes
- Run /anticipate review {theme} for flagged anticipations
- Run /beliefs review for stale beliefs
- Run /gaps for coverage analysis
```
