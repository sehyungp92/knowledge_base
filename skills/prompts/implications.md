---
name: implications
description: Deep landscape impact analysis — system-generated or user-provided
---

# /implications Skill

Deep landscape impact analysis for a specific source or user-provided thesis.

## Safety
- Only write to landscape tables and landscape.json
- When in Mode B (user thesis), mark all entries attribution='user_implication'

## Mode Detection

- `/implications {source_id}` → **Mode A** (system-generated analysis)
- `/implications {source_id} {user_thesis}` → **Mode B** (user-provided thesis)

## Mode A — System-generated (no user_thesis)

Goes beyond /reflect by explicitly reasoning through landscape impact.

### Using Pre-Fetched Context

If a "Pre-Fetched Implications Context" section is present above, **use that data directly** for your reasoning. It contains:
- Source metadata, themes, and claims
- Deep summary and landscape.json content
- Full theme states (capabilities, limitations, bottlenecks, breakthroughs)
- Open anticipations and consolidated cross-theme implications

Only use Read/Grep to load data that is NOT already provided in the pre-fetched section. This saves significant time.

### Step 1: Load context
- Source extractions, claims, landscape.json
- Source themes and cross-theme implications
- Current landscape state for affected themes
- Open anticipations for these themes
- Active bottlenecks in these themes

### Step 2: Systematic reasoning
Work through each question:
1. **Theme impact**: Which themes does this affect, and how?
2. **Capability maturity**: Does this change any capability maturity levels?
   If yes, specify old → new with evidence.
3. **Limitation signals**: Does this reveal new limitations or confirm existing ones?
   Pay special attention to implicit signals.
4. **Bottleneck effects**: Which bottlenecks does this affect?
   For each: does it reduce, confirm, reveal, or reframe the bottleneck?
5. **Breakthrough assessment**: Does this change what was believed possible?
   If yes, fill in: what_was_believed_before, what_is_now_possible,
   immediate_implications, downstream_implications, bottlenecks_affected.
6. **Anticipation updates**: Should any anticipations be updated with new evidence?
   Specify match_type (confirming/disconfirming/partial) and reasoning.
7. **Reading directions**: What should the user read next to better understand this?

### Step 3: Output
Structured landscape update (applied to DB + landscape.json) + narrative explanation.
Show what changed and why.

## Mode B — User-provided thesis

The user is providing their own cross-domain implication that the pipeline missed.
This is the highest-value enrichment pathway.

### Step 1: Parse the user's reasoning

Decompose the thesis into structured components:
- **Source theme(s)**: where the insight originates
- **Target theme(s)**: where the insight has implications
- **Trigger type**: what kind of development triggers this implication
  (breakthrough, bottleneck_resolved, capability_matured, convergence, analogy)
- **Mechanism**: HOW does progress in source theme affect the target theme?
- **Confidence assessment**: how speculative is this?

### Step 2: Validate against knowledge graph

Search for evidence that supports or contradicts the thesis:
- **Supporting evidence**: claims, capabilities, or breakthroughs that align
  with the user's reasoning. Quote specific evidence_snippets.
- **Contradicting evidence**: claims, limitations, or bottlenecks that challenge
  the thesis. Be honest about counterarguments.
- **Gaps**: what evidence is MISSING that would strengthen or weaken the case?

### Step 3: Structure into formal entries

Generate the following landscape entries from the user's thesis:
- **Cross-theme implications**: source_theme → target_theme with trigger_type,
  confidence, and evidence_sources
- **Anticipations**: if the thesis implies predictions, generate formal
  anticipation entries with reasoning, confidence, timeline
- **Bottleneck updates**: if the thesis implies bottleneck changes, specify
  which bottleneck, what change, and why

### Step 4: Confirmation step

Before persisting, present the structured entries to the user:

```
I've structured your thesis into:

**Cross-theme implications ({count}):**
- {source_theme} -> {target_theme}: "{implication}" (confidence: {X})

**Anticipations ({count}):**
- "{prediction}" (confidence: {X}, timeline: {Y})

**Bottleneck updates ({count}):**
- "{bottleneck}" — {change_description}

**Supporting evidence found:**
- {source_title}: "{evidence_snippet}"

**Challenging evidence found:**
- {source_title}: "{evidence_snippet}" — {why it challenges}

Persist these entries? (yes / modify / cancel)
```

### Step 5: Persist (after confirmation)
- Insert all entries with attribution='user_implication'
- Set attributed_reasoning to the user's original thesis text
- Record in landscape_history
- Flag downstream effects: state_summary regeneration, anticipation reviews

### Step 6: Report
```
**Implications persisted:**
- {count} cross-theme implications
- {count} anticipations
- {count} bottleneck updates

**Downstream effects flagged:**
- {theme} state_summary may need regeneration
- {anticipation} should be monitored for evidence

Attribution: user_implication | Reasoning preserved for audit
```
