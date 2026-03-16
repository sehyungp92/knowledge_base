---
name: bottlenecks
description: View bottleneck analysis for a theme or all themes
---

# /bottlenecks Skill

Present the current bottleneck analysis with a leverage-based ranking.

## Safety
- Read-only — do NOT modify bottleneck data

## Execution Contract

### Step 1: Parse and Retrieve

Parse optional theme_id from user input.
Query bottlenecks via `retrieval/landscape.py`:
- `get_bottleneck_ranking(theme_id)` — ranked by impact x (1/resolution_horizon)
- Cross-theme implications involving affected bottlenecks
- challenge_log entries for bottleneck changes (last 90 days)
- landscape_history entries for resolution_horizon changes

### Step 2: Analyze

For each bottleneck, assess:
- **Leverage score**: impact x proximity to resolution (highest = most worth watching)
- **Approach convergence**: are multiple active_approaches converging on a solution,
  or are they divergent attempts? Convergence signals imminent resolution.
- **Approach divergence**: many approaches but no convergence suggests the problem
  is harder than expected or poorly understood.
- **Recent changes**: has the resolution_horizon shifted recently? Was it from
  breakthrough propagation or user enrichment?

Also identify:
- **Unaddressed bottlenecks**: those with zero active_approaches (no one in the
  user's library is working on these)
- **Cascade potential**: bottlenecks whose resolution would unblock the most
  downstream capabilities

### Step 3: Format for Telegram

```
**Bottleneck Analysis** {for theme_name, if specified}
Ranked by leverage: impact x proximity to resolution

{For each bottleneck, ordered by leverage score:}

**#{rank}. {description}** [{bottleneck_type}]
- Blocks: {blocking_what}
- Resolution horizon: {horizon} {if recently changed: "(was {old}, shifted {date})"}
- Active approaches: {count}
  {For each approach: "- {approach} ({who}, promise: {level})"}
- Approach assessment: {converging / diverging / unexplored}
- Downstream: {what would change if resolved — capabilities unlocked, other
  bottlenecks affected}
- Confidence: {confidence}

---

**Unaddressed bottlenecks** (no active approaches):
{List of bottlenecks with zero approaches — these are blind spots}

**Highest cascade potential:**
{Top 2-3 bottlenecks whose resolution would unblock the most other things,
 with explanation of the cascade chain}

**Recent horizon changes:**
{From challenge_log and landscape_history — bottlenecks whose horizons shifted
 recently, with reason for the shift}

Sources: {count} across {themes_count} themes
```
