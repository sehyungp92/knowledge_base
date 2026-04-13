---
type: entity
title: Gross margin
entity_type: metric
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- frontier_lab_competition
- multimodal_models
- startup_and_investment
- startup_formation_and_gtm
- unified_multimodal_models
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0013803159368289306
staleness: 0.0
status: active
tags: []
---
# Gross margin

> Gross margin — revenue minus cost of goods sold, expressed as a percentage of revenue — has become a central diagnostic for unit economics health in the AI software era. As LLM inference costs enter the P&L as a direct cost of service, gross margin has gained renewed analytical importance: it distinguishes companies building durable software businesses from those reselling compute at thin spreads, and it sits at the heart of debates about whether vertical AI can match or exceed the economics of legacy SaaS.

**Type:** metric
**Themes:** [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/multimodal_models|multimodal_models]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Gross margin is calculated as `(Revenue − COGS) / Revenue`. In traditional SaaS, COGS is dominated by hosting, support, and implementation; best-in-class SaaS companies routinely achieve 75–85%. LLM-native companies currently benchmark around 65%, reflecting the non-trivial cost of inference embedded in every user interaction. This gap is not merely a cosmetic accounting difference — it determines how much revenue a company can reinvest in sales, R&D, and customer success, and therefore how fast the business can compound.

The figure of ~65% for LLM-native companies represents a current snapshot, not a structural ceiling. Inference costs continue to fall as model efficiency improves and as frontier labs compete on price; if that trend persists, gross margins for AI-native companies could converge toward or exceed legacy SaaS baselines. Conversely, if competitive differentiation requires using the most capable (and most expensive) frontier models indefinitely, margin compression could become a persistent structural feature of the category.

## Key Findings

### Gross margin as a lens on vertical AI economics

The significance of gross margin in the AI context is sharpest when evaluated against the vertical AI thesis. Sources like Part I: The future of AI is vertical and Vertical AI shows potential to dwarf legacy SaaS argue that vertical AI companies can eventually generate higher revenue per customer than horizontal SaaS — by owning workflows end-to-end rather than just serving as a system of record. If that revenue expansion holds, a somewhat lower gross margin rate may still yield superior gross profit dollars per customer, making the economics compelling even at 65%.

Acquisition signals partially validate this. Thomson Reuters paid $650M for CaseText in 2023, and DocuSign acquired Lexion for $165M in 2024 — both legal AI companies with deeply embedded workflow ownership. These multiples suggest buyers are pricing in durable revenue streams and switching costs, not just discounting for below-SaaS margins.

### The startup cohort as a leading indicator

Data from the YC Winter 2024 batch offers a ground-level view of where early-stage gross margin pressure actually lands. The batch grew aggregate ARR from $6M to $20M — a 3× increase in three months — across roughly 300 companies, the vast majority of which (~70%) are AI-focused. That growth rate is impressive, but the distribution matters: many of these companies are early enough that gross margin is not yet the binding constraint, and over 80% entered the program with no revenue at all. At that stage, founders are typically optimizing for product-market fit and top-line growth rather than margin management. The gross margin reckoning arrives later, when companies scale API costs alongside customer counts.

The shift in batch composition is itself a gross margin signal. With 99% of Winter 2024 companies having a technical founder (up from 88% in prior cohorts) and a 5× increase in open-source developer tool companies, the ecosystem is skewing toward products where compute-intensive inference may be less central — improving the margin outlook for the cohort as a whole compared to, say, pure LLM wrapper businesses.

### Inference cost as the structural variable

The ~65% gross margin benchmark for LLM-native companies is driven primarily by inference cost embedded in COGS. This creates a direct dependency on frontier lab pricing decisions — a structural exposure that horizontal SaaS companies never had to manage. Companies building on models from OpenAI, Anthropic, or Google are, in effect, margin-sharing with their upstream suppliers. This is why Startup Ideas You Can Now Build With AI and related sources emphasize the importance of workflow depth: the more irreplaceable the AI's role in a customer workflow, the more pricing power the application layer has to absorb inference costs without sacrificing margin.

## Open Questions and Limitations

The 65% figure is an aggregate heuristic, not a well-documented empirical consensus — its provenance and sample composition are unclear, and it may obscure wide variance across verticals, model choices, and usage patterns. Companies using smaller, fine-tuned, or self-hosted models may achieve margins far above 65%; those using frontier multimodal models for compute-intensive tasks may fall well below it.

A deeper limitation is that gross margin alone cannot distinguish between companies whose costs are falling (because inference is getting cheaper) and those whose costs are rising (because they are using more capable models as competitive pressure intensifies). The trajectory of the margin matters as much as the level. There is also an open question about whether the vertical AI acquisition comparables (CaseText, Lexion) price in gross margin quality or primarily reflect strategic value — the former would anchor valuations to unit economics; the latter might sustain premium multiples even as margins compress.

Finally, as vertical AI companies expand from software into services and autonomous agents executing real-world tasks, the COGS structure may shift in ways that make gross margin a less stable signal than it has been in SaaS. Whether the metric retains its diagnostic power in an agentic world is an unresolved question.

## Limitations and Open Questions

## Relationships

## Sources
