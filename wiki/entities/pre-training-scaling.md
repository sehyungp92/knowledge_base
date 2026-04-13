---
type: entity
title: Pre-training scaling
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- frontier_lab_competition
- model_commoditization_and_open_source
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- startup_and_investment
- synthetic_data_generation
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00017350130920106273
staleness: 0.0
status: active
tags: []
---
# Pre-training scaling

Pre-training scaling — the practice of increasing model parameter counts and training compute to improve capability — was the defining paradigm of the LLM era from GPT-3 through GPT-4. The central narrative of 2024–2025 is its maturation into a regime of diminishing returns: benchmarks are converging, competitors are reaching parity without proportionally larger clusters, and the research community is pivoting toward post-training methods — particularly reinforcement learning — as the next axis of capability growth.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business & Economics]], [[themes/ai_governance|AI Governance]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/ai_pricing_and_business_models|AI Pricing & Business Models]], [[themes/alignment_and_safety|Alignment & Safety]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/model_commoditization_and_open_source|Model Commoditization & Open Source]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/pretraining_data|Pretraining Data]], [[themes/startup_and_investment|Startup & Investment]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]

---

## Overview

Pre-training scaling operates on the empirical observation — formalized in scaling laws — that model capability improves predictably with compute, parameter count, and data volume. For several years this translated directly into benchmark leadership and perceived competitive advantage: whoever trained the largest model on the most tokens held the frontier. That relationship is now breaking down.

The evidence is not that scaling has stopped working entirely, but that the marginal return per dollar of compute has declined sharply enough to change the strategic calculus. Benchmarks have compressed: as of early 2025, multiple labs are near the top on standard evaluations. Grok 3 reached near the top of all major benchmarks upon release, yet commentators immediately noted that benchmark parity had become the baseline expectation rather than a differentiator — every serious competitor now achieves it. Crucially, benchmark convergence has *not* translated into consumer velocity convergence: OpenAI maintained 400 million weekly active users and ~$11–12 billion in projected annual revenue despite competitors matching them on evals, suggesting that pre-training-derived capability parity is now table stakes rather than a moat.

The most structurally important signal came from DeepSeek, which produced a frontier-quality open-source model with substantially lower compute than expected — arriving "out of left field" and efficiently reaching quality parity. This demonstrated that the pre-training scaling race can be shortcut via architectural and training efficiency improvements, decoupling "frontier quality" from "largest cluster."

---

## The Pivot to Post-Training

The successor paradigm is reinforcement learning applied after pre-training, and the evidence for its efficacy is domain-specific and revealing. RL is clearly powerful in areas with verifiable, objective answers — mathematics and coding — where reward signals are unambiguous. Progress in those domains has been outsized precisely because ground truth is cheaply available. But RL's effectiveness in domains without clean verification remains an open question. The limitation is structural: if the simulation environment is imperfect, models overfit to it, finding spurious reward paths rather than generalizing. This reward-hacking failure mode is the primary unsolved problem in post-training scaling.

This suggests a two-tier capability landscape emerging from the transition: domains with verifiable structure (math, code, formal reasoning) will see continued rapid progress via RL; domains requiring open-ended judgment, nuanced interpretation, or hard-to-specify quality criteria will remain more dependent on pre-training breadth and may plateau sooner.

---

## Strategic and Market Consequences

The flattening of pre-training returns has immediate implications for competitive dynamics. In the prior regime, scale was defensible — only a handful of organizations could afford it. In the emerging regime, efficiency is what matters, and efficiency advantages dissipate faster. DeepSeek's result implies that the frontier is more reachable than the capital requirements of GPT-4-era training suggested, which accelerates commoditization pressure.

The analogy to the search wars is instructive: Yahoo, AltaVista, and Excite all produced capable search products, but Google won on distribution and mindshare, not on marginal algorithmic superiority. The parallel now is that benchmark leadership no longer predicts market leadership. ChatGPT's 2022 launch succeeded not because it outscored competitors on evals but because it was a 100x better *product experience* that attacked the incumbent's mindshare orthogonally. The implication is that as pre-training scaling yields commodity-grade capability across labs, product decisions — memory, personalization, switching costs — become the primary battleground. Memory features in particular are identified as a mechanism that could dramatically increase user lock-in and free-to-paid conversion, effects that have nothing to do with pre-training scale.

---

## Open Questions

- **Where exactly is the ceiling?** Benchmark compression is visible, but whether pre-training scaling has fully saturated or merely slowed remains contested. The answer differs across capability domains.
- **Does RL actually replace pre-training scale, or does it compound it?** Current evidence suggests RL post-training requires a strong pre-trained base; whether it can compensate for a weaker base is unclear.
- **How far does DeepSeek's efficiency generalize?** One efficient model is a proof of concept; whether systematic efficiency gains erode the cost advantage of large-cluster training across model classes is an open empirical question.
- **Verification bottleneck for RL:** The hard limit on RL-driven post-training scaling is the availability of reliable reward signals. Progress in verifiable domains will continue; progress elsewhere depends on solving scalable oversight — a problem that remains unsolved.

---

## Relationships

Pre-training scaling sits upstream of nearly every other competitive and technical dynamic in the field. Its maturation feeds directly into [[themes/model_commoditization_and_open_source|model commoditization]] (as DeepSeek illustrates), reshapes [[themes/frontier_lab_competition|frontier lab competition]] away from compute races toward product and efficiency competition, and hands the baton to [[themes/post_training_methods|post-training methods]] as the new primary capability lever. The [[themes/pretraining_data|pretraining data]] bottleneck — data exhaustion — is a parallel constraint that reinforces the ceiling. [[themes/synthetic_data_generation|Synthetic data generation]] is one proposed response to that constraint, with its own unresolved questions about quality and diversity degradation at scale.

## Key Findings

## Limitations and Open Questions

## Sources
