---
name: landscape
description: View current state of AI for a theme or full overview
---

# /landscape Skill

You are executing the /landscape skill to present the current state of AI
for a given theme (or the full landscape if no theme specified).

## Safety
- Read-only — do NOT modify any landscape tables or files
- Only present information from the database, do not invent landscape state

## Execution Contract

### Step 1: Retrieve theme data

Load ALL of the following via `retrieval/landscape.py` and direct DB queries:
- Theme metadata: state_summary, velocity, state_summary_updated_at
- Capabilities (maturity-ordered) — note any with recent maturity changes
- Limitations (severity-ordered) — include signal_type, trajectory, validated status
- Bottlenecks (with resolution_horizon, active_approaches, bottleneck_type)
- Recent breakthroughs (last 90 days) — include bottlenecks_affected
- Active anticipations — include status_evidence counts
- Cross-theme implications involving this theme
- challenge_log entries for this theme's entities (last 90 days)
- landscape_history entries for key field changes (last 90 days)
- Recent source ingestion count and velocity

### Step 2: Synthesize current state as a temporal trajectory

The state_summary should read as a narrative of *how the theme got here* and
*where it appears to be going*, not a flat inventory.

Use landscape_history data to ground trajectory claims in actual recorded changes.
Frame every section with trajectory context:
"was X, shifted to Y because of Z, now moving toward W."

If state_summary exists and is recent (<7 days old), use it as the narrative backbone.
If state_summary is stale (>7 days) or absent, note this:
"(State summary last updated {date} — may not reflect recent changes)"
If state_summary is absent and <3 sources exist for the theme:
"(Limited coverage: only {N} sources — understanding may be incomplete)"

### Step 3: Format for Telegram

**If theme specified:**
```
**{theme_name}**: State of AI

**Trajectory:**
{2-3 sentence narrative: how this theme's state evolved over recent months,
 what shifted and why, where momentum is building or stalling.
 Ground in landscape_history changes where possible.}

**Current Capabilities:**
{maturity-ordered list. For each:
 - description (maturity_level)
 - If maturity changed recently (from landscape_history), show arrow: maturity_old -> maturity_new
 - Note source count backing each capability}

**Key Limitations:**
{severity-ordered list. For each:
 - description [type: architectural/data/compute/etc]
 - Trajectory indicator: improving/stable/worsening/unclear
 - If implicit signal: note signal_type (e.g., "implicit: hedging")
 - If validated=FALSE, note "(disputed)"
 - If from challenge_log, note the dispute}

**Active Bottlenecks:**
{For each:
 - description (type) — resolution horizon: {horizon}
 - Active approaches: {count} ({approach summaries})
 - If resolution_horizon recently changed (from landscape_history or challenge_log):
   "Horizon shifted: {old} -> {new} due to {reason}"
 - What it blocks: {blocking_what}}

**Recent Breakthroughs** (last 90 days):
{If any:
 - description (significance)
 - Implications: {immediate + downstream}
 - Bottlenecks affected: {which ones and how}
 If none: "No breakthroughs detected in last 90 days."}

**Anticipations:**
{For each open anticipation:
 - prediction (confidence: {X}, timeline: {Y})
 - Evidence: {confirming_count} confirming, {disconfirming_count} disconfirming
 - If status_evidence is non-empty, summarize recent matches
 - Flag any that are overdue for review (last_reviewed > 30 days)}

**Connected Themes:**
{Use `retrieval.landscape.get_consolidated_implications(theme_id)` for compact display.
 Group by (source_theme, target_theme) pair:
 - "{source_theme} -> {target_theme}: {top_implication}" ({N} observations, confidence: {X})
   If second perspective exists: "Also: {second_perspective}"
 - Note if any are user-contributed (attribution='user_implication')}

Last updated: {state_summary_updated_at or 'never'} | Velocity: {high/medium/low/dormant} | Sources: {count}
```

**If no theme specified — synthesized cross-theme dynamics overview:**

Do NOT just list themes with one-line states. Instead, synthesize a narrative:

```
**AI Landscape Overview**

**Biggest Movement (last 30 days):**
{1-2 paragraphs synthesizing which themes saw the most significant changes,
 what breakthroughs or bottleneck shifts drove them, and how these are
 cascading across themes. Name specific cross-theme implications.
 Example: "The biggest movement is in reasoning_and_planning, driven by
 [breakthrough]. This is cascading into autonomous_agents via [implication]
 and may affect the [bottleneck] in code_and_software."}

**Themes by Velocity:**
{velocity-ordered list with one-line trajectory per theme:
 - {theme_name}: {velocity_category} — {one-sentence trajectory summary}}

**Cross-Theme Breakthroughs** (last 30 days):
{Breakthroughs that affected multiple themes, with cascade descriptions}

**Anticipations Under Pressure:**
{Anticipations that received new confirming/disconfirming evidence recently.
 For each: prediction, evidence summary, suggested action.
 If none: "No anticipations have received new evidence recently."}

Coverage: {total_sources} sources across {themes_with_sources} themes | {themes_without_sources} themes have no sources yet
```
