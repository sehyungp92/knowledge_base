---
type: source
title: No Priors Ep. 85 | CEO of Braintrust Ankur Goyal
source_id: 01KJVK9P0TD59FFK4CTS15KV0T
source_type: video
authors: []
published_at: '2024-10-08 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- ai_business_and_economics
- alignment_and_safety
- evaluation_and_benchmarks
- hallucination_and_reliability
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# No Priors Ep. 85 | CEO of Braintrust Ankur Goyal

> Ankur Goyal, CEO of Braintrust, provides a practitioner's-eye view of how enterprise teams are actually building and evaluating LLM products in production — covering the shift from fine-tuning to instruction tuning, the retreat from fully autonomous agents toward hybrid architectures, the emergence of TypeScript as the dominant AI engineering language, and the coming disruption of OLAP data infrastructure by embeddings and semantic search.

**Authors:** Ankur Goyal, No Priors
**Published:** 2024-10-08
**Type:** video

---

## Overview

Braintrust is an end-to-end developer platform for LLM-based products, serving companies like Notion, Airtable, Instacart, Zapier, and Vercel. Unlike generic observability tools, it covers the full development loop: prompt templating and management, real-time prompt serving, model proxy, eval infrastructure, and logging. Its traction comes from early adopters who had already tried and failed to build internal versions — discovering firsthand how hard systematic evaluation is to do well.

The episode is as much a diagnosis of the current AI tooling landscape as a product pitch. Goyal offers unusually candid signal on what's actually working in production, what practitioners have abandoned, and what architectural patterns are emerging as the field matures.

---

## Key Themes

- [[themes/agent_evaluation|Agent Evaluation]]
- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/hallucination_and_reliability|Hallucination and Reliability]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

---

## Capabilities in Production

### RAG Is the Default

Approximately 50% of production AI use cases observed through Braintrust involve [[themes/agent_systems|RAG]] in some form — not as an experimental technique but as standard infrastructure. This is arguably the single cleanest signal in the episode: retrieval-augmented generation has crossed the threshold from research pattern to production default.

### Instruction Tuning Has Replaced Fine-Tuning

Almost all Braintrust customers have moved off fine-tuned models onto instruction-tuned models and are seeing comparable or better performance. Goyal frames fine-tuning as a technique mistaken for an outcome — the actual outcome people want is *automatic optimization of their workloads*, and fine-tuning is just one (difficult, expensive, risky) path toward it.

Fine-tuning modifies or supplements model weights directly, which makes it slower, more expensive, and brittle: it's easy to degrade model performance on real-world tasks while improving performance on training examples. Instruction tuning — collecting data that guides model behavior and nudging the model toward it — achieves the same goal at dramatically lower cost and complexity. The historical context matters: fine-tuning GPT-3.5 was one of the few quality levers available before GPT-4 was cheap and easy to run. That era is over.

> **Limitation:** Fine-tuning risks injuring the model and making it worse on real-world use cases. It is a much harder path to the same destination. *(severity: significant, trajectory: improving)*

### LLM-Based Evaluation Is Standard

More than half of evals run in Braintrust are LLM-based. The key insight driving adoption is asymmetric difficulty: it is significantly easier for an LLM to *validate* an existing output than to *generate* one from scratch — analogous to checking a math proof versus deriving it. This asymmetry makes frontier models viable as evaluators even when they're not perfect generators.

LLM-based evaluators also unlock a use case inaccessible to human reviewers: automated evaluation of production logs containing PII. Evaluators can be run continuously on a sampled fraction of logs, enabling quality measurement at scale without human review bottlenecks.

> **Limitation:** Standardized evaluation practices and benchmarks are absent across enterprises; teams lack common frameworks for systematic quality measurement. *(severity: significant, trajectory: improving)*

---

## Architectural Shifts

### The Retreat from Autonomous Agents

Companies that went deep into fully autonomous, free-form agent architectures have largely walked back from that approach. Goyal identifies the root cause: error rates compound rapidly over multi-step tasks, making end-to-end autonomy unreliable in production environments.

The emerging architecture is different in kind, not just degree: **deterministic control flow managed by code, with LLM calls distributed pervasively throughout the architecture** rather than everything inside an agent loop. The LLM becomes a capable component invoked at specific decision points, not an orchestrator trusted with end-to-end task execution. This hybrid model trades theoretical generality for practical reliability.

> **Limitation:** Fully autonomous agents exhibit compounding failure rates; multi-step error accumulation makes end-to-end autonomy a blocking limitation for production systems. *(severity: blocking, trajectory: improving)*

This represents a [[themes/agent_systems|significant architectural clarification]] for the field — not a retreat from AI capability, but a maturation of where LLM judgment is and isn't load-bearing.

### TypeScript as the Language of AI Engineering

A striking empirical finding: a vast majority of Braintrust customers use TypeScript, including teams that previously used Python. Goyal's explanation is structural rather than preferential: TypeScript's type system makes it inherently better suited for AI workloads because it can convert uncertain, variable model outputs into well-defined structures the rest of the software system can consume safely.

The broader framing is that **product engineers — not ML specialists — are now the primary drivers of AI product development**. TypeScript is the language of product engineering. The AI innovation happening in production is being driven by people who build software products, not people who train models.

This inverts the earlier assumption that ML expertise would be the bottleneck. Many of the most successful early LLM adopters had no ML staff at all.

---

## Open Source Models: Close But Not There

There was a watershed moment for Anthropic when Claude 3.5 Sonnet was released — a step-change in capability that drove broad adoption. A similar moment for open-source models feels close, but Llama 3.1 has not yet crossed that threshold. Practical adoption of open-source models remains limited; interest is high, but production deployment is not.

The barrier is not primarily cost. Enterprise customers are focused on two things: best possible user experience for their customers, and fastest iteration speed for their developers. Everything else — including token costs — is secondary. Until open-source models move the needle on one of those two axes, they will be difficult to adopt broadly.

> **Limitation:** Open-source models lack the performance and ecosystem advantages of frontier proprietary models for production use; cost-per-token advantages do not overcome UX and iteration speed gaps. *(severity: significant, trajectory: improving)*

---

## Data Infrastructure Disruption

### The OLAP Mismatch

Enterprises have accumulated large amounts of structured data in data warehouses, and an entire industry (DataRobot, etc.) was built around helping train models on that proprietary data. LLMs have disrupted this value proposition: a model trained on the internet outperforms what an enterprise can produce from its own structured data warehouse. The hoarded data is often insufficiently relevant to new AI use cases.

More structurally, OLAP data warehouse architecture is misaligned with AI workloads in two ways: (1) it is designed for ad-hoc SQL queries on structured data, neither of which is relevant for AI; (2) semantic search and embedding-based filtering cannot be easily added to traditional data warehouse architecture.

> **Bottleneck:** Traditional relational databases and data warehouses cannot efficiently serve semantic search and embedding-based filtering. OLAP architecture is more deeply disrupted by AI than OLTP because the mismatch is architectural, not incidental. *(horizon: 1–2 years)*

### Embeddings as the New Index

Goyal anticipates that embeddings and LLMs will become core to how enterprises query data, replacing traditional SQL-based relational indexes for most AI-related workloads. The relational model can be extended for OLTP use cases (semantic search can be added alongside existing structure), but OLAP is structurally incompatible with AI data patterns.

---

## Limitations and Open Questions

| Limitation | Severity | Trajectory |
|---|---|---|
| Fine-tuning is slow, expensive, and risks degrading model performance | Significant | Improving |
| Fully autonomous agents have compounding error rates | Blocking | Improving |
| Prototype-to-production quality gap is large and poorly understood | Significant | Stable |
| Open-source models not yet competitive on UX or iteration speed | Significant | Improving |
| Enterprise data warehouses are architecturally misaligned with AI workloads | Significant | Improving |
| Traditional ML expertise resists LLM-centric development approaches | Significant | Improving |
| Standardized eval benchmarks and frameworks absent across enterprises | Significant | Improving |

---

## Breakthroughs Identified

- **Instruction tuning displacing fine-tuning** — prompt-based guidance with few-shot examples achieves comparable performance at a fraction of the complexity and cost
- **Hybrid agentic architecture** — deterministic control flow with interspersed LLM calls proven superior to end-to-end agents for production reliability
- **Product engineers as AI builders** — LLM-based AI development does not require ML expertise; this has already happened in the most successful early adopters
- **LLM-based evaluation at scale** — frontier models can evaluate their own outputs accurately enough to replace human reviewers for most production quality assurance tasks
- **TypeScript's type system for AI** — static typing has proven structurally superior to Python for safely integrating uncertain model outputs into deterministic software systems

---

## Related Sources

*No cross-references available at index time.*

## Key Concepts

- [[entities/autogpt|AutoGPT]]
- [[entities/braintrust|BrainTrust]]
- [[entities/claude-35-sonnet|Claude 3.5 Sonnet]]
- [[entities/fine-tuning|Fine-tuning]]
- [[entities/llama-31|Llama 3.1]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/instruction-tuning|instruction tuning]]
