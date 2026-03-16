---
name: anticipate
description: Generate or review predictions about what comes next
---

# /anticipate Skill

You are executing the /anticipate skill to generate or review predictions
about what's likely to happen next in AI.

## Safety
- Do NOT auto-change anticipation status — flag for human review
- Mark all generated anticipations clearly as speculative
- This is explicitly speculative — the value is in making the model of the future
  explicit and trackable

## Mode Selection

Parse the user's input to determine mode and theme:
- `/anticipate review {theme}` → **Review mode** (explicit)
- `/anticipate generate {theme}` → **Generate mode** (explicit)
- `/anticipate {theme}` → **Auto-select:**
  - If open anticipations exist for this theme with new status_evidence
    (evidence accumulated since last_reviewed), default to **Review mode**
  - If anticipations exist but none have new evidence, or last_reviewed > 30 days,
    default to **Review mode** with staleness flag
  - Otherwise, default to **Generate mode**
- `/anticipate` (no theme) → Show anticipations across all themes that need attention

## Review Mode

### Step 1: Load anticipations needing review
Query open anticipations for the theme (or all themes) that meet ANY of:
- Have new status_evidence since last_reviewed
- last_reviewed is NULL or > 30 days ago
- Have 3+ confirming or 2+ disconfirming evidence pieces

### Step 2: Present each anticipation for review
For each anticipation, ranked by evidence_count DESC:

```
**Anticipation #{n}:** "{prediction}"
Created: {date} | Confidence: {confidence} | Timeline: {timeline}

**Evidence accumulated:**
- Confirming ({count}):
  {For each: source, signal, reasoning, date}
- Disconfirming ({count}):
  {For each: source, signal, reasoning, date}
- Partial ({count}):
  {Brief summary}

**Suggested status change:** {based on evidence balance}
- If 3+ confirming, 0 disconfirming → suggest "partially_confirmed"
- If 5+ confirming from different sources → suggest "confirmed"
- If 2+ disconfirming → suggest "invalidated" or "needs revision"
- Otherwise → suggest keeping "open" with note

**Your call:** Keep open / Partially confirm / Confirm / Invalidate / Revise prediction
```

### Step 3: Apply user decisions
- Update anticipation status based on user's choice
- Record the review: set last_reviewed = NOW()
- Do NOT auto-change status without user confirmation

## Generate Mode

### Step 1: Gather landscape context
Load for the specified theme:
- Current bottlenecks and their resolution trajectories
- Recent breakthroughs (last 90 days) and their downstream implications
- Convergence of capabilities across connected themes
- Existing anticipations (to avoid duplicates)
- Cross-theme implications that suggest future developments
- landscape_history showing recent trajectory changes

### Step 2: Generate anticipations
Reason through what's likely to happen next based on:
1. Bottleneck trajectories — which are shifting? What happens when they resolve?
2. Breakthrough implications — what second-order effects are emerging?
3. Capability convergence — what becomes possible when capabilities from different
   themes combine?
4. Historical patterns — what typically follows this kind of advance?

For each anticipation (generate 3-5):
```
**Prediction:** {clear, specific, falsifiable statement}
**Reasoning:** {which bottlenecks, breakthroughs, trends support this}
**Confidence:** {0.0-1.0 with calibration note}
**Timeline:** {months / 1-2_years / 3-5_years / 5+_years}
**Would confirm:** {what evidence would support this}
**Would invalidate:** {what evidence would refute this}
**Based on:** {specific source IDs, bottleneck IDs, breakthrough IDs}
```

### Step 3: Persist new anticipations
- Insert into anticipations table
- Set attribution='automated_extraction' (or 'user_enrichment' if user modified)
- Set status='open'
- Confirm to user what was created

## Format for Telegram

```
**Anticipations: {theme_name}** ({mode}: {review/generate})

{mode-specific content as described above}

{If review mode: summary of decisions made}
{If generate mode: "Use /anticipate review {theme} to check these against future evidence."}
```
