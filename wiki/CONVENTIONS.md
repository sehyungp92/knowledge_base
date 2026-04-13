# Wiki Conventions

This document defines the conventions for the knowledge base wiki — page templates, frontmatter schema, link patterns, naming rules, and maintenance rules. It co-evolves with use; the lint pass may suggest updates.

---

## Frontmatter Schema

Every wiki page must have YAML frontmatter. Required and optional fields depend on page type.

### Common Fields (all page types)

```yaml
---
type: theme | entity | source | synthesis | belief | question
title: "Human-readable page title"
created: 2026-04-07
updated: 2026-04-07
tags: []
---
```

### Theme Pages

```yaml
---
type: theme
title: "LLM Reasoning"
theme_id: llm_reasoning
level: 1
parent_theme: foundation_models
child_themes: [chain_of_thought_methods, formal_verification]
created: 2026-04-07
updated: 2026-04-07
source_count: 23
sources_since_update: 0
update_count: 1
velocity: 0.72
staleness: 0.0
status: active
tags: [capability, bottleneck]
---
```

### Entity Pages

```yaml
---
type: entity
title: "Chain-of-Thought"
entity_type: method | theory | model | technique | metric | company | researcher | dataset | benchmark | entity | concept
theme_ids: [llm_reasoning, prompt_engineering]
created: 2026-04-07
updated: 2026-04-07
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.85
staleness: 0.0
status: active
tags: []
---
```

### Source Pages

```yaml
---
type: source
title: "Attention Is All You Need"
source_id: 01KJRZT83ABESRYVAH5FMDMW7W
source_type: paper | article | video | podcast | report
authors: ["Author Name"]
published_at: 2017-06-12
theme_ids: [transformer_architecture, attention_mechanisms]
created: 2026-04-07
updated: 2026-04-07
claim_count: 15
tags: []
---
```

### Synthesis Pages

```yaml
---
type: synthesis
title: "Autonomous Agents: State of the Art"
theme_ids: [autonomous_agents]
created: 2026-04-07
updated: 2026-04-07
source_count: 12
tags: []
---
```

### Belief Pages

```yaml
---
type: belief
title: "LLM Reasoning Will Plateau"
belief_id: "db-belief-id"
confidence: 0.65
theme_ids: [llm_reasoning]
created: 2026-04-07
updated: 2026-04-07
tags: []
---
```

### Question Pages

```yaml
---
type: question
title: "What is the state of robotics?"
theme_ids: [robotics]
created: 2026-04-07
updated: 2026-04-07
tags: []
---
```

---

## Staleness Metric

Wiki page staleness is computed as:

```
staleness = min(1.0, (sources_since_update × 0.15) + (days_since_update / 60))
```

- `sources_since_update`: sources touching this page's themes ingested since last update (incremented by `/save`, reset to 0 on page update)
- `days_since_update`: derived from the `updated` frontmatter field

**Threshold bands:**
| Range | Status | Action |
|-------|--------|--------|
| < 0.3 | Fresh | No action |
| 0.3–0.6 | Aging | Lint may flag |
| 0.6–0.8 | Stale | `gather_wiki_context` supplements with live DB |
| > 0.8 | Critical | `gather_wiki_context` falls back to DB assembly; heartbeat prioritises regeneration |

---

## Page Templates

### Theme Page Template

```markdown
---
(theme frontmatter)
---

# {Theme Name}

> One-paragraph summary of this theme's current state and trajectory.

**Parent:** [[themes/{parent-theme}|Parent Theme Name]]
**Sub-themes:** [[themes/{child-1}|Child 1]], [[themes/{child-2}|Child 2]]

## Current State

Narrative synthesis of where this theme stands — capabilities achieved, active limitations, key bottlenecks, and trajectory direction. Written as temporal narrative, not static inventory.

## Capabilities

- **{Capability name}** ({maturity: experimental|emerging|production|commodity}) — description. First reported by [[sources/{source-id}-{slug}|Source]].

## Limitations

- **{Limitation name}** ({severity: minor|moderate|major|fundamental}, {trajectory: improving|stable|worsening}) — description with evidence.

## Bottlenecks

- **{Bottleneck name}** ({status: active|partially_resolved|resolved}) — description. Resolution horizon: {timeframe}. Active approaches: {list}.

## Breakthroughs

- **{Breakthrough}** ({significance: incremental|notable|major|paradigm_shifting}) — what changed and why it matters. Source: [[sources/{id}-{slug}|Title]].

## Anticipations

- **{Prediction}** (confidence: {0-1}, status: {open|confirmed|invalidated}) — evidence for/against.

## Cross-Theme Implications

- [[themes/{other-theme}|Other Theme]]: {implication description}

## Contradictions

- **{Claim A}** vs **{Claim B}** — sources disagree on {topic}. Evidence: [[sources/...|Source A]] vs [[sources/...|Source B]].

## Research Opportunities

- {Idea from /reflect deep with rating ≥ 4}

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **{YYYY-MM-DD}** — [Source: {source_id}, published {date}] {What happened and its significance}.
```

### Entity Page Template

```markdown
---
(entity frontmatter)
---

# {Entity Name}

> One-paragraph summary of this entity and its significance.

**Type:** {entity_type}
**Themes:** [[themes/{theme-1}|Theme 1]], [[themes/{theme-2}|Theme 2]]

## Overview

What this entity is, why it matters, and its role in the landscape.

## Key Findings

Findings from sources that mention this entity, with evidence links.

## Relationships

- Related to [[entities/{other}|Other Entity]]: {relationship description}
- Mentioned in [[sources/{id}-{slug}|Source Title]]: {context}

## Challenged

{Any challenge resolutions — added by /challenge skill}
```

### Source Page Template

```markdown
---
(source frontmatter)
---

# {Source Title}

> One-paragraph summary of what this source contributes.

**Authors:** {authors}
**Published:** {date}
**Type:** {source_type}
**Library:** `library/{source_id}/`

## Key Claims

1. {Claim text} — {evidence snippet}
2. ...

## Landscape Contributions

- **Capabilities:** {any capabilities this source established or updated}
- **Limitations:** {any limitations identified}
- **Bottlenecks:** {any bottleneck evidence}

## Themes

- [[themes/{theme-id}|Theme Name]]: {how this source relates to the theme}

## Related Sources

- [[sources/{id}-{slug}|Title]]: {relationship type} — {evidence}
```

---

## Naming Conventions

| Page type | Path pattern | Example |
|-----------|-------------|---------|
| Theme | `wiki/themes/{theme_id}.md` | `wiki/themes/llm_reasoning.md` |
| Entity | `wiki/entities/{slug}.md` | `wiki/entities/chain-of-thought.md` |
| Source | `wiki/sources/{source-id}-{slug}.md` | `wiki/sources/01KJRZT83A-attention-is-all-you-need.md` |
| Synthesis | `wiki/syntheses/{slug}.md` | `wiki/syntheses/autonomous-agents.md` |
| Belief | `wiki/beliefs/{slug}.md` | `wiki/beliefs/llm-reasoning-will-plateau.md` |
| Question | `wiki/questions/{slug}.md` | `wiki/questions/state-of-robotics.md` |

Slugs: lowercase, hyphen-separated, derived from title. Theme IDs use underscore-separated format (matching DB convention). Source pages include the first 10 chars of the ULID for uniqueness.

---

## Link Conventions

Use Obsidian-style wikilinks for all intra-wiki references:

```markdown
[[themes/llm_reasoning|LLM Reasoning]]
[[entities/chain-of-thought|Chain-of-Thought]]
[[sources/01KJRZT83A-attention-is-all-you-need|Attention Is All You Need]]
```

This enables Obsidian's graph view and backlink tracking.

---

## Development Timeline Convention

Theme pages include an append-only **Development Timeline** section:

1. **Entries are ordered by source `published_at` date** (reverse chronological), NOT ingestion date
2. **New entries are inserted at the correct chronological position**, not always at the top
3. **Existing entries are never modified** — this section is append-only
4. **Each entry cites the source ID and publication date** for traceability
5. **The bootstrap entry** (page creation) goes at the bottom with its creation date

This preserves raw temporal signal that cannot be smoothed away by incremental rewrites.

---

## Two Temporal Dimensions

| Dimension | Question answered | Date used | Where it appears |
|-----------|------------------|-----------|-----------------|
| Real-world chronology | "When did this happen?" | `published_at` from source | Development Timeline, narrative ordering |
| System freshness | "Is this page current?" | `ingested_at` / frontmatter `updated` | Staleness metric, freshness checks |

---

## Update Rules

1. **Incremental, not regenerative** — when new information arrives, update affected sections; don't regenerate the entire page
2. **Frontmatter updates on every write:** `updated` = today, `update_count++`, `sources_since_update = 0`, recompute `staleness`
3. **Development Timeline is append-only** — insert new entries, never rewrite existing ones
4. **Narrative sections are rewritten incrementally** — the LLM sees the current page and integrates new information
5. **Use Haiku for routine updates**, Sonnet for substantive rewrites (splits, merges, bootstrap)
6. **Flag emergent connections** — if the LLM notices cross-theme implications during an update, flag them for DB write-back
