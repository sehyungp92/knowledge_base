---
type: entity
title: Agentic Workflow
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- audio_and_speech_models
- context_engineering
- knowledge_and_memory
- multimodal_models
- retrieval_augmented_generation
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0009230692324630141
staleness: 0.0
status: active
tags: []
---
# Agentic Workflow

Agentic workflow is a paradigm in AI system design where model outputs iteratively feed back into context construction, enabling multi-step reasoning, tool use, and planning through cycles of generation and retrieval or action execution. It represents a significant departure from single-pass inference — instead of producing a final answer in one shot, the model operates as an autonomous loop, deciding what to retrieve, what to call, and what to generate next at each step. This architecture underpins a broad class of modern AI products, from coding assistants to enterprise automation, and is widely viewed as the primary mechanism through which language models are being converted from text predictors into operational agents.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business & Economics]], [[themes/context_engineering|Context Engineering]], [[themes/knowledge_and_memory|Knowledge & Memory]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/tool_use_and_agent_protocols|Tool Use & Agent Protocols]], [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]], [[themes/multimodal_models|Multimodal Models]], [[themes/audio_and_speech_models|Audio & Speech Models]]

---

## Overview

At its core, an agentic workflow couples a generator (a language or multimodal model) with a retriever or action layer that it can invoke — the basic anatomy of RAG extended into a feedback loop. The model produces a draft, assesses what information is missing or what action is needed, retrieves or executes accordingly, and integrates the result before continuing. The loop terminates when the model judges the task complete, a stopping criterion is met, or an error is raised.

This architecture is not just a design choice — it is increasingly the unit of value delivery in AI-native products. The practical engineering challenges are largely about context: what goes into the window at each step, how long it stays there, and how to keep it accurate and relevant without burning cost.

---

## Context Engineering as the Core Bottleneck

The quality of an agentic workflow is almost entirely determined by context quality at each cycle. This makes context engineering — not model capability per se — the primary lever for practitioners.

**Prompt caching** is one of the most impactful optimisations. When a system prompt is reused across millions of API calls (a common pattern in agentic deployments), processing it from scratch each time is wasteful. Prompt cache, introduced in November 2023 by Gim et al. and since incorporated into major commercial APIs, stores overlapping token segments so they are processed only once. For a 1,000-token system prompt across 1 million daily API calls, this eliminates approximately 1 billion redundant input tokens per day — a substantial reduction in both latency and cost (from Building A Generative AI Platform). Google's Gemini API offers context caching at a 75% discount on cached input tokens, though it charges for storage at $1.00 per million tokens per hour, illustrating the emerging trade-off between compute savings and memory cost.

**Exact caching for retrieval** extends the same logic to the embedding layer: if an incoming query matches one already seen, the cached vector search result is returned directly, avoiding redundant retrieval cycles. This matters in agentic loops where sub-questions often recur across different task traces.

The evidence consistently supports the value of retrieved context: having relevant information in the window at generation time produces more detailed responses and measurably reduces hallucinations. But this benefit is contingent on retrieval quality — irrelevant or stale context degrades outputs, and the loop can compound errors if early retrievals mislead later steps.

---

## Reasoning Models and the Architecture Shift

Standard LLMs predict the next token based on distributional patterns in training data. Reasoning-focused models like o1 take a structurally different approach — running extended internal computation before generating a final response (from Part II: Multimodal capabilities unlock new opportunities in Vertical AI). In the context of agentic workflows, this distinction matters: a reasoning model can potentially compress multiple agent turns into a single extended generation, collapsing the loop at the cost of more compute per call. Whether this is a convergence point or an alternative architecture remains an open question.

---

## Multimodal Extensions

Agentic workflows are increasingly multimodal. Speech-native models — which process audio directly rather than transcribing to text first — eliminate a major latency bottleneck. The cascading architecture (speech-to-text → LLM → text-to-speech) introduces not only additional round-trip latency but also loses non-textual signal: emotion, sentiment, prosody. Speech-native models achieve latency under 500 milliseconds, making real-time conversational agents practical in a way the cascading approach never fully achieved.

Vision-language models extend the same pattern to visual inputs. Google's Gemini 1.5 Pro supports image and video understanding with context retention up to one million input tokens — enabling agentic loops over long documents, video streams, and mixed-media corpora that would have been impractical to address with text-only architectures.

At the research frontier, agentic workflows are also being applied to low-level compute optimisation: LLM agents that automatically fuse discrete CUDA operations into optimised kernels represent an early instance of agentic systems operating on the infrastructure layer beneath themselves. This capability remains research-only in maturity.

---

## Security and Operational Risk

Agentic workflows introduce attack surfaces that single-pass inference does not. **Prompt injection** — where adversarial content in retrieved documents or tool outputs manipulates the model into performing undesired actions — is the primary threat. Because the model's context is dynamically assembled from external sources across multiple turns, the window of exposure is larger and harder to audit than in a static prompt.

The Samsung incident illustrates the data exfiltration risk: employees submitted proprietary internal information to ChatGPT, inadvertently leaking it to the model provider, which led Samsung to ban external LLM use in May 2023. In an agentic context where the model autonomously retrieves and synthesises information, the risk is amplified — the model may pull sensitive data into context without explicit user intent, and that data may propagate across tool calls or be logged in ways the user does not control.

---

## Business and Market Implications

Agentic workflows are the mechanism through which AI is attacking systems of record (SoR). Incumbent SoR vendors (ERP, CRM, vertical platforms) have historically been protected by two deep moats: high upfront implementation costs and custody of customer data. Agentic AI erodes both — it can automate integration work that previously required expensive consultants, and it can operate across data sources rather than being locked to a single vendor's schema. The result is that incumbents face pressure not just from feature competition but from the potential obsolescence of the workflow layer they've owned.

This dynamic is particularly acute in vertical AI: conversational voice agents, vision-enabled inspection systems, and document-processing pipelines are all instances of agentic workflows displacing human-in-the-loop processes that SoR vendors had assumed would remain manual indefinitely.

---

## Open Questions and Limitations

The deepest unresolved tension is between **loop depth and error propagation**. Each cycle introduces the possibility of a retrieval failure, a hallucinated intermediate output, or an action with irreversible side effects. Existing evaluations of agentic systems rarely stress-test failure recovery at depth — most benchmarks measure success on short chains. Robustness at 20+ steps in real-world, noisy environments remains poorly characterised.

**Cost and latency at scale** are still live concerns. Prompt caching helps significantly, but multi-turn agentic loops accumulate tokens across cycles. For high-frequency applications, the economics can invert: the per-query cost of an agentic workflow may exceed the value it generates unless the task is genuinely complex enough to warrant it. The right granularity — when to run a loop versus a single call versus a reasoning model — is not yet well understood at a practical engineering level.

Finally, **evaluation** is an open problem. Static benchmarks measure point-in-time capability; agentic workflows must be evaluated on trajectory quality, recovery behaviour, and the reliability of stopping conditions — dimensions that current standardised evals do not adequately capture.

---

## Related Entities

- Retrieval-Augmented Generation — the retrieval component that anchors most agentic loops
- Prompt Injection — the primary security vulnerability introduced by dynamic context assembly
- Context Window — the operational constraint that governs what an agent can attend to at each step
- Reasoning Models — an architectural alternative that may compress multi-step reasoning into single extended generations
- Systems of Record — the incumbent category most exposed to agentic displacement

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
