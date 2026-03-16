---
name: enrich
description: Correct, supplement, or reinterpret source extractions
---

# /enrich Skill

You are the primary mechanism for human-in-the-loop landscape shaping. The user wants
to correct, supplement, or reinterpret what the system extracted from a source.

## Safety
- Only write to landscape tables and library/{source_id}/landscape.json
- Mark all entries attribution='user_enrichment'
- Do NOT modify claims, extractions.json, or clean.md

## Execution Contract

### Step 1: Load and Present Current State (Opening Move)

Load the source's extractions, landscape.json, and all landscape DB entries for this source.
Present a compact summary organized by enrichment type:

```
**{source_title}** — Current Extractions

**Capabilities:** {count} extracted
{brief list with maturity levels}

**Limitations:** {total_count} ({implicit_count} implicit, {unvalidated_count} unvalidated)
{brief list, starring items with lowest confidence or implicit signals}

**Bottlenecks linked:** {count}
{brief list with resolution horizons}

**Themes assigned:** {theme_list with relevance scores}

**Cross-theme implications:** {count}
```

Then highlight the most questionable items — lowest confidence entries, implicit signals
that may need validation, and any gaps you notice:

```
**Items needing attention:**
- {N} implicit limitations have not been validated
- Capability "{X}" has low confidence (0.4)
- No bottlenecks linked despite discussing scalability challenges
```

### Step 2: Offer Structured Input Modes

Present the user with clear options:

```
What would you like to do?
(1) Validate extracted limitations — confirm or reject implicit signals
(2) Add missed signals — capabilities, limitations, or bottlenecks not extracted
(3) Correct classifications — fix theme assignments, severity, maturity levels
(4) Add cross-domain implication — connections to other themes the pipeline missed
(5) Reclassify significance — e.g., "this is a breakthrough, not incremental"
(6) Free-form enrichment — tell me what you see that the system missed

Or just type your enrichment directly — I'll parse it.
```

### Step 3: Guided Validation Mode (if user chooses option 1 or source has unvalidated implicit limitations)

For each unvalidated implicit limitation, present inline for quick validation:

```
**Implicit limitation #{n}** (signal: {signal_type}, confidence: {confidence})
"{description}"
Evidence: "{evidence_snippet}"

Does this seem right? (confirm / reject / skip)
```

Process responses:
- confirm → set validated=TRUE, validated_at=NOW()
- reject → set validated=FALSE, validated_at=NOW()
- skip → leave unchanged

After validation batch: show summary of what was confirmed/rejected.

### Step 4: Parse and Structure Updates

For any user input (structured or free-form), parse into:
- **New capabilities**: description, theme_id, maturity, confidence, evidence_snippet
- **New limitations**: description, theme_id, limitation_type, signal_type='explicit', severity, trajectory
- **New bottlenecks**: description, theme_id, blocking_what, bottleneck_type, resolution_horizon
- **Reclassifications**: entity_id, field, old_value, new_value
- **Theme corrections**: add/remove source_themes entries
- **Cross-theme implications**: source_theme, target_theme, trigger_type, implication text
- **Significance upgrades**: e.g., capability → breakthrough with full breakthrough fields

For cross-theme implications: validate against the knowledge graph. Find supporting evidence
if it exists. Note when the connection is purely the user's interpretation.

### Step 5: Apply Updates

1. Update landscape.json in library/{source_id}/
2. Insert/update relevant landscape tables
3. For all entries: set attribution='user_enrichment', attributed_reasoning=<user's input text>
4. For reclassifications: record old values in landscape_history
5. If significance upgraded (e.g., to breakthrough): insert breakthrough record with
   what_was_believed_before, what_is_now_possible, bottlenecks_affected

### Step 6: Post-Change Summary with Downstream Effects

After applying changes, show what was updated AND flag downstream effects:

```
**Changes applied:**
- Validated 3 limitations (2 confirmed, 1 rejected)
- Added 1 capability: "{description}" (maturity: {level})
- Added 1 cross-theme implication: {source_theme} -> {target_theme}
- Corrected theme assignment: added {theme_name}

**Downstream effects flagged:**
- Theme '{theme_name}' state_summary may need regeneration
  (run /landscape {theme_name} to refresh)
- Anticipation "{prediction}" should be reviewed — new evidence from this enrichment
- Bottleneck "{description}" has a new linked limitation

**Attribution:** All changes recorded as user_enrichment
```
