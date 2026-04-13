---
type: entity
title: GPT-3.5
entity_type: entity
theme_ids:
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- frontier_lab_competition
- hallucination_and_reliability
- in_context_and_meta_learning
- post_training_methods
- robotics_and_embodied_ai
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0012312178217740689
staleness: 0.0
status: active
tags: []
---
# GPT-3.5

GPT-3.5 (specifically `gpt-3.5-turbo`) is OpenAI's mid-tier language model that occupies a critical position in the AI ecosystem as a cost-efficient workhorse — capable enough for a wide range of NLP tasks, yet clearly outclassed by GPT-4 in reasoning-intensive work. Its significance lies less in what it can do at the frontier and more in what it reveals about the economics and architectural decisions shaping how large language models are deployed in practice.

**Type:** entity
**Themes:** [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business & Economics]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/ai_pricing_and_business_models|AI Pricing & Business Models]], [[themes/alignment_and_safety|Alignment & Safety]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/in_context_and_meta_learning|In-Context & Meta-Learning]], [[themes/post_training_methods|Post-Training Methods]], [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]], [[themes/startup_and_investment|Startup & Investment]], [[themes/startup_formation_and_gtm|Startup Formation & GTM]], [[themes/tool_use_and_agent_protocols|Tool Use & Agent Protocols]], [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]

---

## Overview

GPT-3.5 is OpenAI's language model — most commonly referenced as `gpt-3.5-turbo` — used extensively as a cost-conscious alternative to GPT-4 in multi-model systems. In the context of VOYAGER, it handles standard NLP tasks such as skill description generation, query suggestion, and text embeddings via `text-embedding-ada-002`, while GPT-4 is reserved for the more demanding code generation core. This split-model architecture is a direct consequence of GPT-4's 15× price premium over GPT-3.5, which the VOYAGER authors cite explicitly as a meaningful cost barrier.

---

## Role in Multi-Model Systems

The VOYAGER agent provides one of the clearest documented examples of intentional model stratification: GPT-4 handles code generation (where it is dramatically superior), while GPT-3.5 handles everything else. This is not a workaround — it is deliberate system design driven by the economics of inference. The performance gap is stark: GPT-4 obtains **5.7× more unique items** than GPT-3.5 in code generation tasks, which the authors attribute to "a quantum leap in coding abilities." For any task that doesn't require that leap, GPT-3.5 is the rational choice.

This pattern resonates with the founding thesis of Dust, where Gabriel Hubert and Stanislas Polu (both Stripe and OpenAI alumni) built their product on the conviction that "one model will not rule them all" — that multi-model integration, with different models assigned to different task types, is the key to extracting real-world value from AI. GPT-3.5's continued relevance in 2023–2024 pipelines is partly a validation of this view: there is a large surface area of tasks where its price-performance ratio is superior.

---

## Capabilities and Performance Benchmarks

Within its intended scope, GPT-3.5 is capable for a broad range of NLP tasks — query generation, summarization, embedding, and lightweight reasoning. In health conversation contexts, frontier models at roughly the GPT-3.5 Turbo tier achieved **16% quality** as measured by physician-written rubrics, compared to ~60% for stronger frontier models — a near 4× gap that illustrates the ceiling on what GPT-3.5 class models can deliver in high-stakes domains. Models at this tier also showed notably worse safety-relevant behavior, with roughly 4× higher error rates on critical behaviors like emergency referrals compared to more capable successors.

---

## Known Limitations

The limitations of GPT-3.5 are well-documented and significant in the context of agentic systems:

**Coding and reasoning.** The 5.7× performance gap versus GPT-4 on code generation in VOYAGER is not a marginal difference — it reflects a qualitative ceiling on what GPT-3.5 can reliably produce in agentic loops that depend on executable, correct code.

**Abstract reasoning.** Frozen pretrained LLMs at the GPT-3.5 tier achieve only **6–20% accuracy on ARC** (Abstraction and Reasoning Corpus) without task-specific training, demonstrating that scale and general pretraining alone are insufficient for abstract visual reasoning. This is a direct challenge to the assumption that larger general-purpose models automatically generalize to structured reasoning tasks.

**Health and safety domains.** The 4× degradation in safety-critical health behaviors (e.g., emergency referral accuracy) versus more capable models raises a direct question about deployment responsibility: using GPT-3.5 class models in domains where errors have real consequences requires explicit mitigation, not just cost optimization.

**Visual perception.** Although this limitation applies to the GPT-4 API available at the time of VOYAGER's writing rather than GPT-3.5 specifically, it contextualizes the broader text-only constraint that shaped how both models were used in early multimodal agentic systems.

---

## Economic Significance

The 15× price differential between GPT-3.5 and GPT-4 is one of the most consequential facts in applied AI system design during 2023–2024. It created a strong incentive to architect systems that route tasks by complexity — using GPT-4 only where it provably adds value. This dynamic accelerated the development of orchestration layers (like Dust) and task-routing agents, and influenced how [[themes/vertical_ai_and_saas_disruption|vertical AI products]] were priced and architected. As GPT-4 prices have fallen over time, the routing calculus shifts — but the architectural pattern it established (heterogeneous model stacks) has persisted.

---

## Open Questions

- As GPT-4 and successor models become cheaper, at what point does the cognitive overhead of maintaining split-model architectures outweigh the cost savings?
- Is the 6–20% ARC accuracy ceiling for GPT-3.5 class models evidence of a fundamental architectural limitation, or a training data and fine-tuning gap?
- How much of GPT-3.5's continued use in production reflects genuine task-fitness versus organizational inertia and migration cost?

---

## Related Entities & Sources

- Voyager: An Open-Ended Embodied Agent with Large Language Models — primary source documenting GPT-3.5/GPT-4 split architecture and cost analysis
- Getting the Most From AI With Multiple Custom Agents ft Dust's Gabriel Hubert and Stanislas Polu — contextualizes multi-model philosophy that GPT-3.5's cost profile helped create
- Why Vertical LLM Agents Are The New $1 Billion SaaS Opportunities — frames the economic landscape in which GPT-3.5 vs. GPT-4 cost tradeoffs matter
- A Masterclass in Building AI Applications From Legora's CEO — additional context on applied LLM deployment decisions

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
