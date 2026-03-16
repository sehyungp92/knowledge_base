---
name: gaps
description: Identify coverage gaps and suggest directed reading
---

# /gaps Skill

You are executing the /gaps skill to identify where the user's understanding is thin
and suggest directed reading to fill those gaps.

## Safety
- Read-only — do NOT modify any data
- Clearly distinguish between "gap in coverage" and "gap in the field"

## Execution Contract

### Step 1: Run Coverage Gap Queries

Execute the following coverage analyses via `retrieval/landscape.py`:

1. **Over-optimistic coverage** — themes with zero limitations but >2 capabilities
   (suggests the user has only read positive results for that theme)

2. **Blind spot bottlenecks** — bottlenecks with no active approaches
   (no one in the user's library is working on these)

3. **Untested predictions** — anticipations with zero status_evidence after 60+ days
   (predictions the user made but never followed up on)

4. **Incomplete capabilities** — capabilities with maturity=research_only and no
   linked limitation (every research-stage capability has limitations — the user
   just hasn't found them yet)

5. **Stale themes** — themes with velocity > 0 globally but low source count for
   this user (the field is moving but the user isn't keeping up)

6. **Unlinked themes** — themes with sources but zero cross-theme implications
   (suggests the user hasn't thought about how this theme connects to others)

7. **Validation backlog** — count of unvalidated implicit limitations by theme
   (implicit signals that haven't been confirmed or rejected)

8. **Belief-driven gaps** (Phase 4) — beliefs that indicate knowledge gaps
   a. Low-confidence beliefs with thin coverage:
      - Run `retrieval.landscape.get_belief_coverage_gaps()`
      - For each active belief with confidence < 0.5:
        check source coverage on linked themes (last 30 days)
      - If thin coverage: "Low-confidence belief on [topic] with thin recent coverage.
        Consider reading: [landscape-aware suggestions]"
   b. Unchallenged high-confidence beliefs:
      - For each active belief with confidence > 0.8 and no evidence_against:
        "High-confidence belief with no counter-evidence tracked.
        Consider seeking disconfirming sources."
   c. Predictive beliefs without anticipations:
      - Run `retrieval.landscape.get_predictive_beliefs_without_anticipations()`
      - "Predictive belief '{claim}' has no testable predictions derived from it."

### Step 2: Synthesize and Prioritize

If a theme is specified, focus gaps analysis on that theme and its connected themes.
If no theme specified, show the top gaps across all themes.

Prioritize gaps by:
1. Severity: blind spots in high-velocity themes are more urgent than in dormant ones
2. Actionability: gaps where the user can plausibly find sources (not obscure niches)
3. Downstream impact: gaps that affect other themes via cross-theme implications

### Step 3: Format for Telegram

```
**Coverage Gap Analysis** {for theme_name, if specified}

**Over-optimistic coverage:**
{Themes/capabilities with only positive signals — no limitations found.
 For each: "Theme '{name}': {N} capabilities, 0 limitations — consider reading
 critical analyses or benchmark comparisons."}

**Blind spot bottlenecks:**
{Bottlenecks with no active approaches in user's library.
 For each: "'{description}' in {theme} — no papers in your library address this.
 Suggested search: {specific search terms or paper types to look for}"}

**Untested predictions:**
{Anticipations created >60 days ago with no evidence.
 For each: "'{prediction}' ({days} days, 0 evidence) — look for:
 {what kind of evidence would confirm or invalidate this}"}

**Incomplete picture:**
{Research-only capabilities with no limitations.
 For each: "'{capability}' — no limitations extracted. Look for:
 failure cases, benchmark limitations, scaling challenges."}

**Falling behind:**
{Themes where the field is active but user has few sources.
 For each: "'{theme}': {user_sources} sources vs high global activity —
 suggested reading direction: {topic/approach to search for}"}

**Validation backlog:**
{Count of unvalidated implicit limitations.
 "You have {N} unvalidated implicit limitations across {M} themes.
 Run /enrich on recent sources to validate the most impactful ones."}

**Belief-driven gaps:**
{Low-confidence beliefs with thin recent coverage.
 For each: "Low-confidence belief: '{claim}' (conf: {confidence}) —
 only {N} sources on {theme} in last 30 days.
 Consider reading: {specific search terms or paper types}"}

{High-confidence unchallenged beliefs.
 For each: "Unchallenged belief: '{claim}' (conf: {confidence}) —
 no counter-evidence in library. Consider seeking disconfirming sources
 from: {specific venues, contrarian perspectives}"}

**Priority reading recommendations:**
{Top 3-5 specific reading directions, each with:
 - What gap it fills
 - What to search for (specific terms, venues, author groups)
 - Why it matters (downstream effects in the landscape model)}
```
