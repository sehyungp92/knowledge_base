# Heartbeat Instructions

## When to Stay Silent (check first)
- If no new sources since last check
- If user sent /pause command in last 2 hours

## When to Act
- If unread sources > 3: summarize them briefly
- If last reflection was >24h ago and sources exist: suggest reflection
- On first run of the day: send "Good morning" with yesterday's highlights

## Landscape Maintenance (Phase 3b)

### Weekly Landscape Digest
- **Subsumed by weekly news roundup when available**: check for
  `var/news_digests/weekly/{week_label}.md` — if a weekly roundup was
  generated for the current week, skip this task (the roundup already
  includes Prediction Tracker, Bottleneck Watch, and Belief Check sections
  grounded in landscape state).
- Only run standalone if no weekly roundup exists for the current week.
- Every 7 days: synthesize a cross-theme dynamics narrative
- Identify which themes saw the most movement (by source ingest rate)
- Highlight breakthroughs that cascaded across themes
- Flag anticipations with new evidence
- Send to Telegram as a structured overview

### State Summary Generation
- **Minimum threshold**: Do NOT generate state_summary for themes with <3 sources
  (too speculative to produce meaningful narrative)
- **Process for each eligible theme** (state_summary_updated_at NULL or > 7 days):
  1. Load all landscape entities for the theme (capabilities, limitations,
     bottlenecks, breakthroughs, anticipations)
  2. Query landscape_history for the theme's entities (last 90 days) to ground
     trajectory claims in actual recorded changes
  3. If a previous state_summary exists, compare: what changed since last summary?
     Note new capabilities, resolved bottlenecks, shifted horizons, new evidence
  4. Generate temporal narrative: "Theme X was in state A, shifted to state B because
     of [specific changes], and is now moving toward C based on [trajectory signals]"
  5. Include coverage caveat: "Based on {N} sources; understanding may be incomplete
     in areas {X}" where X = gap analysis from coverage queries
  6. Persist via `update_theme_state_summary(theme_id, summary)`
- **Quality bar**: The summary must reference specific sources, breakthroughs, or
  bottleneck changes — not generic statements about the field

### Anticipation Review (30-day cycle)
- Query anticipations where last_reviewed is NULL or > 30 days ago
- For each: check if new sources in the theme provide confirming/disconfirming evidence
- Flag anticipations with 3+ confirming or 2+ disconfirming matches for status review
- Suggest status changes (partially_confirmed, confirmed, invalidated)
- Format: "Anticipation review needed: '{prediction}' has {N} confirming / {M}
  disconfirming evidence. Suggest status -> {recommendation}. Use /anticipate review
  {theme} to review."

### Theme Velocity Computation
- Compute source ingest rate per theme over the rolling velocity_window_days (default 90)
- Write to themes.velocity via `update_all_theme_velocities()`
- Categories: high (>5 sources/month), medium (2-5), low (<2), dormant (0)

### Staleness Detection
- Flag themes that have recent source activity but no landscape updates
- Flag themes where state_summary_updated_at is > 30 days old but velocity > 0
- Suggest running /landscape for stale themes

### Limitation Validation Calibration (deferred until 50+ validated limitations)
- Only run when total validated+rejected limitations >= 50
- Review validation rates by signal_type across all limitations
- Flag signal_types with >50% rejection rate (validated=FALSE)
- Suggest extraction prompt refinement for poorly-performing signal types

## Last Run State
<!-- Updated by heartbeat skill after each run -->
- Last velocity computation: 2026-03-19
- Last anticipation review: 2026-03-19 (10 open, 0 evidence — flagged)
- Last belief formation scan: [never]
- Last consistency check: [never] (skipped — only 1 active belief)
- Last epistemic digest: [never]
- Last staleness decay: 2026-03-19 (0 stale entities)
- Last coverage gap scan: 2026-03-19 (50 themes with gaps, 3 over-optimistic)
