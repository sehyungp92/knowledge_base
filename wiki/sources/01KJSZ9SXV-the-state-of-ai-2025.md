---
type: source
title: The State of AI 2025
source_id: 01KJSZ9SXVD86JCE15747DC7Y9
source_type: article
authors: []
published_at: '2025-08-12 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- computer_use_and_gui_agents
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The State of AI 2025

> A sweeping structural analysis of the AI startup landscape three years post-ChatGPT, arguing that agentic AI, browser-native execution, and autonomous workflows are systematically dismantling legacy enterprise software moats — not as a productivity layer, but as a replacement layer. Bessemer Venture Partners characterizes two distinct AI startup archetypes (Supernovas and Shooting Stars), maps the degradation of SaaS incumbents, and identifies persistent memory and evaluation infrastructure as the critical unsolved bottlenecks for the next phase of enterprise AI deployment.

**Authors:** Bessemer Venture Partners
**Published:** 2025-08-12
**Type:** article

---

## Expert Analysis

Three years post-ChatGPT, the AI startup landscape has bifurcated into two archetypes — "Supernovas" with unprecedented but fragile growth, and "Shooting Stars" with durable SaaS-like compounding — while the deeper structural story is that agentic AI, browser-native execution, and autonomous workflows are systematically dismantling the moats of legacy enterprise software. The most consequential shift is not AI as a productivity layer but AI as a replacement layer: systems of action replacing systems of record, with the browser as the new programmable operating environment.

---

## New Economics of AI Startups

Two distinct archetypes have emerged, with fundamentally different risk profiles:

**Supernovas** represent a new asset class with no precedent in software history:
- Year 1 ARR ~$40M, Year 2 ARR ~$125M — velocity that breaks historical SaaS benchmarking
- $1.13M ARR per FTE, reflecting extreme headcount-light capital efficiency
- Gross margins ~25%, often negative in Year 1, driven by inference costs and competitive pricing
- Structural risk: proximity to foundation model functionality invites "thin wrapper" critique; low switching costs may underlie rapid adoption; competitive dynamics compress margins toward zero

**Shooting Stars** are the more durable archetype:
- $3M → $12M → $40M → $103M ARR across four years — faster than SaaS predecessors, without fragility
- ~60% gross margins, slightly below pure SaaS peers due to model costs, but with strong retention and expansion dynamics
- ~$164K ARR per FTE, indicative of an organization scaling with product complexity

The **Q2T3 benchmark** (quadruple, quadruple, triple, triple, triple) has replaced T2D3 as the growth standard for elite AI startups — a compression of product development, GTM, and distribution cycles that would have been impossible in prior software eras. The authors note this may prove aspirational; Q2T1D2 may be the honest ceiling.

See [[themes/startup_and_investment|Startup & Investment]] and [[themes/startup_formation_and_gtm|Startup Formation & GTM]].

---

## SaaS Disruption: Systems of Record Under Siege

The core thesis is that legacy SaaS moats — deep product surfaces, implementation complexity, data centrality — are **actively degrading**, not cyclically softening:

- Salesforce, SAP, Oracle, and ServiceNow held dominant positions through switching costs built over decades
- AI's ability to structure unstructured data and generate migration code on demand has made switching faster, cheaper, and more feasible than at any point in enterprise software history
- Implementation time has collapsed 90% via codegen and natural-language business logic translation — destroying one of the core lock-in mechanisms of legacy vendors
- Data migration that required multi-year consultant-heavy engagements can now complete in days

This is characterized as a **structural shift, not a cyclical one** — the moats are not weakening temporarily but dissolving permanently as AI commoditizes the capabilities that made migration prohibitively expensive.

See [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]] and [[themes/ai_market_dynamics|AI Market Dynamics]].

---

## Agentic AI and the Browser as Operating Layer

The analysis identifies the **browser as the emerging programmable operating environment** for autonomous agents:

- [[entities/perplexity|Perplexity]]'s Comet browser represents the thesis: an agentic browser that observes and executes across the full digital environment, not merely navigates it
- The shift is from AI as a tool you invoke to AI as an ambient layer that monitors and acts
- Fully autonomous consumer agent execution for high-friction tasks (travel, e-commerce) remains immature — still requiring too much manual user intervention despite clear demand

**[[entities/anthropic|Anthropic]]'s Model Context Protocol (MCP)**, introduced in late 2024 and rapidly adopted by [[entities/openai|OpenAI]], Google DeepMind, and Microsoft, is crystallizing as the universal specification for agents to access external APIs and real-time data. This is not a proprietary bet — it is becoming infrastructure.

Foundation model labs are vertically integrating beyond model provision into agent deployment — coding agents, computer use agents, MCP integrations — compressing the runway for thin-wrapper startups sitting between models and users.

See [[themes/agent_systems|Agent Systems]] and [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]].

---

## Vertical AI: Succeeding Where Vertical SaaS Failed

Industries previously characterized as "technophobic" are showing accelerated AI adoption because **the failure mode was the software, not the industry**:

- Prior software couldn't handle multimodal, language-heavy, high-friction workflows
- AI can — driving faster adoption than historical SaaS penetration curves in healthcare (clinical notes, coding), legal (demand packages, contract review), and education
- AI-native FP&A tools enabling financial analysts to centralize data across silos without data engineering support
- Enterprise search copilots trained on internal knowledge replacing SharePoint and Notion search
- Consumer mental health and emotional wellness applications with long-term memory — deployed commercially with real user bases

**Open questions on vertical AI durability:**
- Can domain AI startups maintain meaningful data advantages in industries where data is fragmented, privacy-sensitive, and structurally difficult to standardize?
- In verticals where incumbents are not passive, will scale and distribution advantages of established players ultimately dominate?
- AI-native ERP tools remain structurally blocked from serving complex enterprise customers — current solutions address only SMB/mid-market segments with simpler requirements; true enterprise ERP replacement is many years out

See [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]].

---

## Capabilities Mapped

| Capability | Maturity | Notes |
|---|---|---|
| Consumer general-purpose LLMs (ChatGPT ~600M, Gemini ~400M weekly active users) | Commoditized | Mass daily-use habit achieved |
| LLM-powered voice AI with emotional/contextual conversation | Broad production | Surpassed legacy assistants; latency, cost, and naturalness all improved dramatically in 2025 |
| Vertical AI workflow automation in healthcare, legal, education | Broad production | Formerly "technophobic" industries showing clear adoption signals |
| AI-accelerated enterprise system implementation and data migration | Narrow production | 90% faster implementation; days not years for migration |
| AI-native enterprise search (horizontal copilots) | Narrow production | Replacing SharePoint, Notion search |
| AI-native FP&A tooling | Narrow production | Cross-silo data centralization without data engineering |
| Consumer AI for mental health/emotional wellness with persistent memory | Narrow production | Rosebud, Finch deployed commercially |
| Agentic browser as ambient proactive interface | Demo | Perplexity Comet; autonomous web-scale execution not yet production-grade |

---

## Limitations and Open Questions

**Persistent cross-session memory** is the most consequential unsolved primitive. Large context windows (128K to 1M+ tokens) and RAG have enabled better single-session coherence, but truly adaptive, personalizing long-term memory — the kind that compounds competitive moat over time — remains an open engineering and product challenge. Whoever solves this likely dominates the personal AI assistant layer. *(severity: significant; trajectory: improving)*

**Enterprise evaluation infrastructure** is the blocking bottleneck for regulated and high-stakes deployment. Public benchmarks (MMLU, GSM8K, HumanEval) provide coarse-grained signals that systematically fail to capture workflow nuance, compliance constraints, and decision-critical production contexts. Private, continuous, use-case-specific evaluation is a prerequisite for trusted enterprise AI — and it largely doesn't exist at scale yet. *(severity: blocking; trajectory: improving)*

**The thin wrapper problem** creates existential unit economics risk for Supernova-pattern startups. Near-zero or negative gross margins, low switching costs, and proximity to foundation model functionality make revenue structurally vulnerable to upstream model improvements or direct competition from labs. *(severity: significant; trajectory: worsening)*

**Generative video** has not crossed commercial viability at scale as of this writing. Google Veo 3, Kling, Sora, and emerging open-source stacks are converging on controllability and realism, but compute intensity, training cost, evaluation complexity, and a weak open-source ecosystem remain blockers. 2026 is the expected inflection year. *(severity: significant; trajectory: improving)*

**Vertical data moat fragility** — in industries where data is fragmented, privacy-sensitive, and difficult to standardize, the defensibility of current vertical AI data advantages is unproven and may not survive competitive pressure. *(severity: significant; trajectory: unclear)*

**Domain expertise embedding** — the optimal techniques for embedding real-world context and domain expertise into AI systems at scale remain theoretically unresolved. The tension between general-purpose scaling laws and domain-specific fine-tuning is an open research and product question. *(severity: significant; trajectory: unclear)*

**Autonomous consumer agents** for high-friction tasks (travel, e-commerce) remain immature — clear demand exists but execution requires too much manual user intervention, and multi-step planning reliability across platforms has not reached production thresholds. *(severity: significant; trajectory: improving)*

---

## Bottlenecks

| Bottleneck | What It Blocks | Horizon |
|---|---|---|
| Absence of production-grade evaluation infrastructure | Broad enterprise AI adoption in regulated/high-stakes verticals | 1–2 years |
| Persistent cross-session memory architecturally unsolved | Truly personalized AI assistants; memory as compounding competitive moat | 1–2 years |
| Generative video: compute, cost, evaluation complexity, weak OSS ecosystem | Commercial-scale video generation across creator tools, studios, marketing | Months |
| AI-native ERP lacking breadth for complex manufacturing/supply chain | AI displacement of enterprise-scale SAP/Oracle in industrial verticals | 5+ years |
| Insufficient multi-step planning reliability for consumer agents | End-to-end autonomous consumer task completion | 1–2 years |

---

## Breakthroughs

**Voice AI mainstream breakout (2025):** LLM-powered voice surpassed legacy assistant paradigms — Alexa, Siri — across open-ended conversation, emotional awareness, and contextual depth. Driven by latency improvements, dramatic cost reductions, and naturalness gains. Classified as a major breakthrough with implications for consumer ambient computing and vertical AI interfaces. *(significance: major)*

**AI-enabled enterprise migration cost collapse:** The multi-year, consultant-heavy enterprise system migration is effectively dead as a switching cost barrier. AI-generated code and schema translation have collapsed implementation from years to days — destabilizing the lock-in economics that Salesforce, SAP, Oracle, and ServiceNow relied on for decades. *(significance: major)*

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business & Economics]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]
- [[themes/startup_and_investment|Startup & Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation & GTM]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]

## Key Concepts

- [[entities/the-bitter-lesson|The Bitter Lesson]]
- [[entities/vertical-ai|Vertical AI]]
