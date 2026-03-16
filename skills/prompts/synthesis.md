---
name: synthesis
description: Generate a consolidated topic synthesis report across multiple sources
---

# /synthesis Skill

You are executing the /synthesis skill to produce a structured report that
consolidates all sources on a given topic into a single integrated understanding.

This is **different from** other skills:
- `/ask` answers a specific question with citations (claim-level retrieval)
- `/landscape` shows theme-level trajectory (capabilities/limitations/bottlenecks movement over time)
- `/synthesis` produces a **topic-level consolidated understanding** — what is X, what makes it different, where sources disagree, and what questions remain

## Safety
- Read-only — do NOT modify any database tables or library files (except the synthesis cache)
- Only synthesize from evidence in the library — never fabricate sources
- Cite specific sources inline

## Execution Contract

### Step 1: Extract the search topic

The user's input may be a bare topic OR a natural language request. You must
extract a **short, searchable topic phrase** (1-4 words) that will work as a
retrieval query against the knowledge base.

Examples:
- `/synthesis openclaw` → topic = `"openclaw"`
- `/synthesis world models` → topic = `"world models"`
- `/synthesis create a report about the detrimental impact AI is having on SaaS`
  → topic = `"AI impact on SaaS"` (or `"SaaS disruption"`)
- `/synthesis what do we know about scaling laws and their limits?`
  → topic = `"scaling laws"`
- `/synthesis how does openclaw compare to langchain and crewai`
  → topic = `"openclaw"` (the primary subject)

Rules for extraction:
- Strip instructional phrasing ("create a report about", "what do we know about", "summarize")
- Keep it short — the topic feeds into database search queries
- If the user names a specific technology, project, or concept, use that as-is
- If the user describes a theme or trend, distill it to the core noun phrase
- If ambiguous, prefer terms that match known theme names or source titles in the system

### Step 2: Check cache

Check if `library/syntheses/{topic_slug}.md` exists and is recent (< 24h old).
If cached and fresh, return the cached report.
If stale or missing, proceed to generation.

### Step 3: Generate synthesis report from pre-fetched data

All relevant data has been pre-fetched and appended to this prompt in the
**"Pre-Fetched Synthesis Data"** section. This includes:
- Sources found via multi-facet sub-query decomposition
- Deep summaries from `library/{source_id}/deep_summary.md`
- Concrete evidence snippets (verbatim claims with provenance)
- Landscape signals (capabilities, limitations, bottlenecks, anticipations)
- Consolidated cross-theme implications

**Do NOT call `generate_topic_synthesis()` or any other Python functions.**
Synthesize your report directly from the pre-fetched data below.

Produce a structured synthesis report in this exact format:

```
# Topic Synthesis: {topic}

Based on {count} sources ingested between {date_range}.

## What It Is
{2-3 paragraphs explaining what this topic/technology/concept is. Synthesize ACROSS sources — do NOT summarize each one sequentially. Cite specific sources inline as [Source N: "Title"]. Include concrete facts and numbers where available.}

## What Makes It Different
{Bullet points with **bold labels** identifying the key differentiators or novel contributions. Each must cite at least one source. Focus on what distinguishes this from related work or alternatives.}

## Core Capabilities
{Draw from both the capabilities table AND claims/evidence. Order by maturity. For each: description, maturity level, confidence, and supporting evidence. Prioritise capabilities backed by concrete data (benchmarks, numbers, demonstrations) over vague claims.}

## Key Limitations
{Draw from both the limitations table AND claims/evidence. Order by severity. For each: description, type, trajectory, and supporting evidence. IMPORTANT: Limitations are the most valuable signal. Include implicit limitations (hedging language, controlled conditions, conspicuous absences, scale/cost barriers) alongside explicit ones. If sources are suspiciously optimistic about an area, flag it.}

## Where Sources Disagree
{Explicit contradictions, tensions, or different framings between sources. For each: what source A says vs. what source B says, and your assessment of which has stronger evidence. If no disagreements exist, say so and explain why the convergence is (or isn't) meaningful.}

## Cross-Theme Implications

### Obvious Connections
{High-confidence implications (>= 0.7) that are direct/expected. Include observation count and confidence. Explain briefly why each matters.}

### Non-Obvious Connections
{Lower-confidence or surprising implications. These are the most valuable section — connections that aren't immediately apparent. Explain the reasoning chain for each.}

## Open Questions
{Specific, answerable questions that remain unresolved. Include:
- Gaps in coverage (what aspects haven't been examined?)
- Untested anticipations (predictions that need evidence)
- Areas where confidence is low and more sources would help
- Conspicuous absences (what would you expect to find but don't?)}
```

**CRITICAL RULES:**
- Synthesize ACROSS sources. Do NOT write sequential source summaries.
- Cite specific sources inline: [Source N: "Title"]
- Include concrete facts, numbers, statistics, and quotes wherever available.
- Separate obvious from non-obvious implications — explain the reasoning for non-obvious ones.
- If sources disagree, note the disagreement explicitly with your assessment.
- Limitations and open questions are MORE valuable than capabilities — invest depth there.
- Form your own concrete opinion based on the evidence. Do NOT defer to vague conclusions.
- Identify gaps — what questions remain unanswered? What's suspiciously absent?
- Keep the report focused and specific — no generic statements.

### Merge Mode (when sources are specified by ID/URL)

If the pre-fetched data section is titled **"Pre-Fetched Merge Data"**, you are in
merge mode. Follow the merge prompt instructions embedded in that data block
instead of the standard synthesis format above.

Key differences from topic mode:
- Output is a **standalone professional report** — no meta-references to sources
- Use light `[1]` inline citations, not `[Source N: "Title"]`
- End with a `## References` section: `[N] Title (date)`
- Structure follows the logical flow of content, not a fixed template
- Never say "according to", "one study found", "sources disagree", etc.

If the section is titled **"Cached Merge Report"**, return the cached report
directly to the user without modification.

### Step 4: Cache the result

Write the completed report to `library/syntheses/{topic_slug}.md` using the Write tool,
where `{topic_slug}` is the topic lowercased with spaces replaced by underscores
(e.g. "death of saas" → "death_of_saas").

### Step 5: Offer follow-up

After presenting the report, offer:
- "Run `/landscape {theme}` for temporal trajectory of a specific theme"
- "Run `/ask {question}` for a specific question with citations"
- "Run `/reflect {topic}` to generate novel ideas based on this synthesis"
