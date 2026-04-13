---
type: entity
title: Fine-tuning
entity_type: method
theme_ids:
- agent_evaluation
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- alignment_and_safety
- evaluation_and_benchmarks
- frontier_lab_competition
- hallucination_and_reliability
- startup_and_investment
- startup_formation_and_gtm
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0006385314710820228
staleness: 0.0
status: active
tags: []
---
# Fine-tuning

Fine-tuning is a post-training technique that modifies or supplements a pre-trained model's weights using curated task-specific examples, enabling specialization beyond what pretraining alone achieves. Once considered a primary pathway to production AI, its role has become more nuanced: it delivers measurable gains in narrow domains — robotics, medical consultation, customer service — but carries significant costs and risks that have caused enterprise practitioners to scale back its use in favor of prompting and retrieval-based approaches.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/startup_and_investment|Startup and Investment]], [[themes/startup_formation_and_gtm|Startup Formation and GTM]], [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

---

## Overview

Fine-tuning encompasses a family of post-training optimization techniques — including supervised fine-tuning (SFT), reinforcement learning from human feedback (RLHF), distillation, and action fine-tuning for robotics — that substantially amplify the capabilities of foundation models beyond pretraining. The core promise is specialization: adapting a general-purpose model to a domain's vocabulary, edge cases, and behavioral norms using far fewer examples than training from scratch.

In practice, the technique is more expensive and complex than prompt engineering or instruction tuning, and carries a well-documented failure mode — catastrophic forgetting — where gains in one specialized dimension come at the cost of degraded performance elsewhere. BrainTrust, which runs evaluation and observability infrastructure for enterprise AI teams, reports that fine-tuning usage has *declined* among its customer base, a signal that many practitioners are finding the cost-benefit calculus unfavorable as foundation models improve and prompting techniques mature.

---

## Key Findings

The enterprise retreat from fine-tuning is echoed in the founding philosophy of startups like Dust, whose internal strategy was explicitly "no GPUs before PMF" — a deliberate decision to avoid training proprietary models until product-market fit was established. This heuristic reflects a broader shift: the value of fine-tuning is most defensible in narrow, well-defined domains where behavioral consistency and domain knowledge depth matter more than general reasoning. Dust's founders, alumni of Stripe and OpenAI, bet instead on multi-model integration as the primary lever for enterprise AI value, a conviction that foundation models would commoditize fast enough to make proprietary weight modifications a liability rather than a moat. Getting the Most From AI With Multiple Custom Agents ft Dust

BrainTrust's $36M raise from Andreessen Horowitz was premised on building evaluation and observability tooling, not model training — again suggesting that the enterprise market is orienting around prompt development and measurement rather than weight modification. No Priors Ep. 85 | CEO of Braintrust Ankur Goyal

---

## Capabilities

Where fine-tuning does work, the gains can be dramatic. Specialization via fine-tuning on 2,000–5,000 demonstrations has enabled robot policies to achieve 79% average success on highly dexterous long-horizon tasks including origami folding and lunch-box packing — tasks that zero-shot foundation models cannot approach. Post-training optimization more broadly (combining fine-tuning, RL, and distillation) substantially amplifies capabilities beyond pretraining alone, and this remains the dominant pathway for agentic customer service benchmarks: fine-tuned systems have achieved strong scores on Tau2-retail, Tau2-airline, and Tau2-telecom, with telecom scores exceeding reported Claude baselines. Fine-tuning also appears to enable state-aware medical consultation agents that track dialogue phase and drive uncertainty-targeted questioning — though this remains largely at the demo and research stage rather than broad production deployment.

---

## Known Limitations

The limitations of fine-tuning are structurally important and not merely practical inconveniences:

**Catastrophic forgetting** is the most documented failure mode. Domain-specific supervised fine-tuning of foundation models for medical tasks measurably degrades performance on other consultation aspects — such as management plan appropriateness — even as it improves narrow knowledge depth. The same dynamic appears in robotics: VLAs face substantial challenges retaining abstract reasoning capabilities after action fine-tuning, creating a direct tension between dexterous skill acquisition and generalization. This is not a solvable engineering problem so much as a fundamental constraint of gradient-based weight modification.

**Skill versus generalization.** Fine-tuning on domain-specific data increases knowledge in a niche but does not teach models how to solve novel problems or carry out extended multi-step tasks. The capability being instilled is pattern matching to training distribution, not reasoning about out-of-distribution scenarios. This is a significant limitation for any use case where edge case handling matters more than average-case performance.

**Cross-embodiment transfer.** In robotics, zero-shot cross-embodiment transfer has not been achieved — new robot platforms still require fine-tuning data, which blocks rapid generalization to novel hardware and makes the technique a bottleneck for scaling robot deployments.

**Off-distribution fragility.** Off-the-shelf foundation models cannot handle the full variability of industry-specific edge cases, exceptions, and constantly changing rules — yet fine-tuning on a fixed dataset only partially addresses this, and the distribution shift problem returns as domains evolve. This dynamic pushes teams toward human-in-the-loop architectures even after fine-tuning.

---

## Relationships

Fine-tuning sits at the intersection of several active tensions in the field. It is a primary mechanism for [[themes/alignment_and_safety|alignment work]] (RLHF, Constitutional AI) but also a source of alignment risk when domain specialization degrades safety-relevant behaviors. It is central to [[themes/agent_systems|agentic systems]] benchmarks where specialized models outperform prompted generalists, yet the [[themes/hallucination_and_reliability|reliability]] costs of forgetting undermine enterprise adoption. The startup ecosystem — as tracked through YC Winter 2024 batch analysis, Conviction's investment thesis, and a16z's fund structure — has largely voted with its architecture choices against fine-tuning as a differentiation strategy, preferring prompting, retrieval, and multi-model orchestration instead. Whether this reflects a durable equilibrium or a temporary pause while fine-tuning tooling matures remains an open question.

## Limitations and Open Questions

## Sources
