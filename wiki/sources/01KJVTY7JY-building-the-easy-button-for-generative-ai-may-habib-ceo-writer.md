---
type: source
title: Building the Easy Button for Generative AI | May Habib, CEO, Writer
source_id: 01KJVTY7JY0MEKFWN0T3J276MT
source_type: video
authors: []
published_at: '2024-11-21 00:00:00'
theme_ids:
- ai_business_and_economics
- knowledge_and_memory
- retrieval_augmented_generation
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Building the Easy Button for Generative AI | May Habib, CEO, Writer

Writer's CEO May Habib traces the company's evolution from an AI writing assistant into a full-stack enterprise generative AI platform, detailing the architectural and product decisions — particularly around graph-based RAG, LLM-based guardrails, and synthetic data training — that differentiate it from point solutions and commodity LLM wrappers. The source is especially valuable for its frank treatment of where enterprise DIY AI implementations break down and why controlling the full stack enables qualitatively different outcomes.

**Authors:** May Habib
**Published:** 2024-11-21
**Type:** video

---

## Overview

Writer is a full-stack generative AI platform targeting enterprises in financial services, healthcare, and retail/CPG. Founded in 2020 by May Habib and co-founder Wasim — who had worked together for roughly a decade at their prior company Cordoba (focused on machine translation) — Writer's original pitch was narrow: AI writing assistance using Transformers rather than hand-coded linguistic rules. The rapid capability jump in generative models reshaped the company's trajectory entirely. By the time Transformers proved capable of generating, synthesizing, and reasoning over enterprise data, Writer had built enough scaffolding around LLMs to productize it as AI Studio. The $200M funding round at a $1.9B valuation (following a $100M Series B in 2023) reflects the market's bet that full-stack vertical AI control compounds into durable advantage.

---

## Architecture and Technical Approach

### Full-Stack Philosophy

Writer has controlled its own LLM layer since inception — a deliberate choice that separates it from orchestration layers built on top of third-party models. The full stack accreted over time: first the base LLM, then guardrails, then the knowledge graph, then orchestration and observability. This structure allows Writer to claim that customers are buying a solution where every layer is co-optimized, rather than assembling independent point products.

### Graph-Based RAG

The most technically distinctive element is Writer's approach to [[themes/retrieval_augmented_generation|retrieval-augmented generation]]. Rather than chunking documents into vector embeddings, Writer trained a purpose-built LLM to extract knowledge graph triples (entity–relation–entity). The graph is stored as flat JSON in PostgreSQL — no graph database, no predefined ontology required. This matters practically because:

- **Structured data handling.** Vector-based RAG flattens documents, destroying table structure, nested relationships, and numerical context. The graph approach preserves these by construction.
- **Update efficiency.** In vector-based systems, updating a single document requires discarding and reprocessing the entire embedding store. Graph updates are localized.
- **Context window optimization.** Writer applies *retrieval-aware compression* to condense what enters the context window, and uses *Fusion-in-Decoder* (originating from FAIR) to integrate multiple retrieved passages via the LLM's memory layer rather than naive concatenation.

Microsoft's Graph RAG paper (using GPT-4 to build graphs at inference time) validated the approach directionally, but at ~$55,000 per benchmark run — illustrating why training a dedicated graph-construction LLM is not just an architectural preference but a scalability requirement.

### LLM Family

Writer's Palula X family includes core reasoning models and domain-specific variants for healthcare, financial services, and creative applications. Synthetic data has been central to training efficiency: Writer uses LLM-optimized synthetic data (not low-quality web-scraped filler) to achieve competitive 100B–200B parameter models with substantially lower compute than internet-scale training paradigms assume. Additional algorithmic innovations on the vanilla Transformer architecture compound this efficiency.

### Guardrails

Compliance guardrails in Writer are LLM-based, not rule-based. Simple keyword/reject filters fail to capture semantic meaning; effective guardrails require LLM-level understanding of what constitutes PII, brand-compliant phrasing, or regulatory adherence. Writer's approach applies post-processing LLM rewrites rather than binary filtering.

### AI Studio

AI Studio is a low-code environment for building custom enterprise applications, enabling business users to compose AI workflows without deep ML expertise. Writer is itself the primary consumer of AI Studio, which has accelerated its own customer-facing application development.

---

## Enterprise Use Cases

Writer's vertical focus shapes where it competes:

- **Financial services:** Earnings call summaries, company/sector deep dives, search over M&A and merger proxy documents.
- **Insurance:** Policy review, claim adjudication, agent knowledge assistance (e.g., CSAA).
- **Retail/CPG:** Regulatory affairs research (e.g., federal packaging regulations), compliance content generation.
- **Sales/Marketing:** SEO rewrites, compliance-reviewed marketing materials, Slack-integrated content review (e.g., Salesforce deployment).

The consistent pattern is high-stakes, knowledge-intensive tasks where the cost of a wrong answer is real — not chatbots for website deflection. A representative example: a CPG call-centre agent answering whether a product contains phthalates needs to synthesize regulatory documents accurately and quickly. That is the problem Writer is designed for.

---

## Landscape Contributions

### Capabilities

| Capability | Maturity |
|---|---|
| Graph-based RAG with automatic triple extraction | `narrow_production` |
| LLM-based compliance guardrails with semantic rewriting | `narrow_production` |
| Domain-specific fine-tuned LLM family (Palula X) | `broad_production` |
| Autonomous action orchestration for knowledge workflows | `narrow_production` |
| Efficient training via LLM-optimized synthetic data | `broad_production` |
| Algorithmic Transformer efficiency improvements | `demo` |
| Multimodal model development | `demo` |
| AI Studio low-code enterprise application builder | `narrow_production` |

### Limitations

**Structural RAG limitations (significant, improving).** Vector-based RAG fundamentally fails with tables, nested structures, and numerical data. Writer's graph approach addresses this, but the limitation exposes how much of enterprise data is poorly served by the dominant RAG paradigm. See [[themes/retrieval_augmented_generation|RAG limitations]].

**Autonomous action amplifies LLM weaknesses (significant, unclear trajectory).** Current agentic demos tend to surface, rather than conceal, the underlying reasoning limitations of LLMs. Writer's approach — starting with the most knowledge-intensive nodes of a workflow — is conservative precisely because the failure modes are visible. Reliable multi-step automation remains a 3–5 year horizon problem.

**Guardrail complexity (significant, improving).** Semantic compliance guardrails require LLM-based understanding, which makes them expensive and architecturally complex. Off-the-shelf reject filters don't work; building something that does requires deep integration with the generation layer.

**Market segmentation by technical sophistication (significant, improving).** Current enterprise AI buyers capable of evaluating Writer's approach are concentrated among technically sophisticated early adopters. Mainstream enterprise sales require re-framing and abstraction — an addressable market constraint, not just a messaging problem.

**DIY RAG does not scale (blocking, worsening).** Customers attempting to build their own RAG stacks consistently fail to reach production quality despite sustained engineering investment. The systems are brittle, hard to maintain, and don't meet accuracy requirements. This is the primary problem Writer positions against — and the difficulty is real, not manufactured.

**Knowledge graph maintenance overhead (minor, improving).** Despite automation, density tuning and light ontology management remain necessary by domain experts for high-complexity enterprise data. The zero-preprocessing claim is mostly true but not universally so.

### Bottlenecks

| Bottleneck | Horizon |
|---|---|
| Production-grade document understanding at enterprise scale | 1–2 years |
| Compliant AI in regulated industries | 1–2 years |
| Reliable multi-step workflow automation | 3–5 years |
| Broad enterprise adoption beyond early adopters | 1–2 years |

### Breakthroughs

- **Graph RAG with trained triple extraction** significantly outperforms vector approaches for structured enterprise documents. The Microsoft validation (despite its cost unsustainability) confirms the architectural direction.
- **LLM-optimized synthetic data** enables competitive large-model training at materially lower compute cost, challenging the assumption that scale requires internet-scale data.

---

## Connections

- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]] — Writer's graph RAG is a direct response to the well-documented failure modes of vector-based RAG on structured enterprise data.
- [[themes/knowledge_and_memory|Knowledge and Memory]] — The knowledge graph architecture and Fusion-in-Decoder technique address the memory and retrieval layers of LLM systems.
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]] — Writer exemplifies the full-stack vertical AI thesis: owning every layer to achieve accuracy and reliability that point solutions cannot.
- [[themes/ai_business_and_economics|AI Business and Economics]] — The funding trajectory, DIY failure patterns, and enterprise GTM constraints are a case study in how AI platform companies create and capture value.
- [[themes/startup_and_investment|Startup and Investment]] — Seed term sheet signed March 3, 2020 (pandemic week); evolution from writing assistant to platform illustrates non-linear product-market fit in a fast-moving capability landscape.

---

## Open Questions

- How does Writer's graph RAG perform on entirely unstructured, narrative-heavy documents where vector approaches are typically stronger? The source focuses on structured data advantages without benchmarking the converse.
- As base LLM capabilities improve, how much of Writer's graph-construction advantage is durable versus commoditizable by frontier model providers?
- The "autonomous action starts with knowledge-intensive nodes" framing is conservative — what is the concrete reliability threshold Writer targets before expanding agentic scope?
- Synthetic data quality is asserted as high-signal; what failure modes exist when the generating model's biases propagate into the training distribution?

## Key Concepts

- [[entities/graph-based-rag|Graph-based RAG]]
