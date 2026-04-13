---
type: source
title: A Masterclass in Building AI Applications From Legora's CEO
source_id: 01KJVTN6C7Z8MWFBKEBA05ZF9K
source_type: video
authors: []
published_at: '2025-05-27 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_pricing_and_business_models
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# A Masterclass in Building AI Applications From Legora's CEO

> A practitioner-level account of building AI-native legal software from Legora's CEO, tracing the journey from early BERT experiments to multi-agent workflow automation. The source offers unusually candid analysis of where AI genuinely works in legal practice, where it fails, and how the economics of model pricing, billing structures, and enterprise adoption friction shape what is actually deployable—making it a grounded counterweight to more speculative takes on AI's impact on professional services.

**Authors:** Legora CEO
**Published:** 2025-05-27
**Type:** video

---

## AI's Impact on Legal Processes

### The Paradigm Shift: From BERT to GPT-3.5

The history of legal AI compresses a remarkable capability jump into a few years. Early BERT-based models circa 2020 were "horrendously bad" for non-English languages like Swedish—barely useful for real legal work. The arrival of GPT-3.5 marked the inflection point: not just an incremental improvement but a threshold event that moved the industry from experimentation to actual end-to-end implementation.

The practical consequence is immediate and concrete. Due diligence—once requiring physical data room access, FTP tools, and manual Ctrl+F searches across documents—now means uploading documents to a platform, specifying requirements, and receiving a generated report. This is not a demo capability; it is [[themes/vertical_ai_and_saas_disruption|broad production]] today.

### The Workflow Paradigm Shift

The deeper structural change is in how AI is applied. The progression has two distinct phases:

1. **Query phase**: Static queries against a dataset—ask a question, get an answer
2. **Agent phase**: Define a process, give an agent access to tools, let it plan and execute multi-step workflows, and receive an end-to-end work deliverable

This shift from retrieval to execution is what makes current AI qualitatively different from earlier iterations. The surrounding infrastructure—function calling, MCP, tool integration—is where the greatest leverage now lives, beyond raw model improvements alone.

### Legal Work as a Complexity Spectrum

Legal work can be visualized on a scale from simple data extraction at the bottom to complex drafting (share purchase agreements, SPA negotiations) at the top. The current frontier:

- **Bottom quartile** (data extraction, routine clause review): already fully automated
- **Middle range** (NDA review, MSA processing, risk control): largely automated, especially for in-house counsel
- **Upper range** (complex drafting, novel legal arguments): partially assisted, not automated

AI is "slowly but surely moving up" this spectrum. The ceiling is not fixed—it shifts with each model generation.

---

## The Legal Software Consolidation

### From Fragmentation to Unified Platforms

The legacy legal software landscape was highly fragmented: separate tools for document translation, clause comparison, legal search, contract review. Each point solution addressed one workflow. AI's cross-stack capabilities dissolve this fragmentation—the same underlying model can handle translation, comparison, search, and review within a single interface.

This creates the conditions for new unified platforms to emerge and capture value previously distributed across dozens of vendors. The [[themes/vertical_ai_and_saas_disruption|consolidation dynamic]] parallels broader SaaS disruption patterns but is accelerated by AI's generality.

### In-House Counsel vs. Law Firms

A structural distinction shapes adoption patterns differently across the market:

- **In-house counsel**: Primarily repetitive, standardized work (NDAs, MSAs, risk control). High automation fit. Less resistance because efficiency directly benefits them.
- **Law firms**: More one-off, complex, precedent-light work. Automation fit is lower at the high end. Resistance historically stronger due to billing structure misalignment.

Despite these differences, nearly all legal work reduces to five core categories: reviewing, reading, drafting, writing, and researching—all addressable by current AI capabilities to varying degrees.

---

## Economics and Incentive Structures

### The Billing Model Paradox

The hourly billing model creates an apparent structural barrier: if AI makes a lawyer 50% more efficient, that's 50% fewer billable hours. Many predicted this would block adoption.

The actual dynamics are more complex. Several forces override the billing misalignment:

**Competitive pressure as prisoner's dilemma**: If any competitor adopts AI for efficiency, every other firm must follow or be seen as billing for tasks others don't charge for. "As soon as somebody moves down, it forces everybody to do the same because there is very little differentiation on those types of tasks." This is the classic [[themes/ai_business_and_economics|race-to-adoption]] dynamic in professional services.

**Client pressure**: Large corporate and PE clients who are themselves adopting AI internally are increasingly demanding that outside counsel demonstrate AI usage—or face questions about why they're billing hours for tasks that should be automated.

**Outsourcing pressure**: Large US firms are already outsourcing contract review because it isn't profitable to staff associates at $800/hour on such work. AI makes this economics problem more acute, not less.

**Due diligence commoditization**: Due diligence fees—once a significant revenue source—are becoming line items clients refuse to pay for. The service is being commoditized whether firms adopt AI or not.

### The $1 Trillion Market Conversion

The legal software market is approximately $20 billion. The legal services market is approximately $1 trillion. AI has the potential to convert portions of the services market into software revenue—a structural shift that dwarfs the existing software opportunity. This is not speculative; the blurring of "software" and "service" is already visible in platforms like Legora that deliver work outputs, not just tools.

---

## Model Economics and the Pricing Tension

### The Cost Escalation Problem

Early assumptions about the AI economics were that model prices would continuously decline as capabilities improved—a straightforward cost curve compression. This has not materialized cleanly. The pattern instead:

> "The LLM models are becoming so much better, but also more expensive."

OpenAI o3 performs "incredibly well" on legal tasks but is "very, very expensive." The best models for complex legal reasoning are not the cheap ones. This creates a fundamental tension: the tasks where AI provides the most value (complex reasoning, nuanced drafting) are served by the most expensive models, which are the hardest to price into a sustainable product.

### Model Routing as a Practical Response

Legora's engineering response to this tension is model routing: classification algorithms that automatically select the optimal model for each specific task based on complexity and cost tradeoffs. Simpler tasks route to cheaper models; complex tasks justify expensive reasoning models. This is currently at [[themes/ai_pricing_and_business_models|demo maturity]]—functional but not yet industry-standard practice.

### Reasoning Models: Capability vs. Commercializability

High-quality reasoning models (o1, o3) are "incredibly good" at legal work but "very hard to price." The challenge is not technical; it is economic. A model that costs 10x more per token to run cannot be passed through at 10x the subscription price without destroying the customer relationship. This is a [[themes/ai_pricing_and_business_models|blocking bottleneck]] for sustainable scaling of high-capability AI legal applications.

---

## Limitations and Open Problems

### Complex Drafting: The Hard Ceiling

Complex contract drafting—share purchase agreements, bespoke transaction documents—remains one of the hardest AI tasks. Two compounding reasons:

1. **Proprietary training data gap**: Many high-stakes contracts are not publicly available. Models trained on SEC/Edgar filings lack access to firm-specific precedents and templates that drive real drafting quality. The data that matters most is the data least available.
2. **Linguistic precision at the margin**: "A comma there or a word there can directly influence the meaning quite a lot." Legal drafting is not semantically robust—small surface changes carry large legal consequence. Models optimized for general fluency are not optimized for this kind of precision.

This limitation is **significant** in severity and currently on an **improving** trajectory as fine-tuning and retrieval-augmented generation mature, but it remains a real ceiling.

### Infrastructure Reliability at Scale

Early enterprise deployments revealed that reliability—correct chunking, consistent RAG delivery, handling concurrent user load—is a non-trivial engineering problem that causes direct customer churn when it fails. This bottleneck is **blocking** for enterprise adoption and is actively being resolved, but it required significant engineering investment that was underestimated.

### User Expectation Gap

When Legora launched its drafting capability, the first user query was "write me an SPA"—a single unstructured prompt for one of the most complex legal documents that exists. This illustrates the core adoption friction: lawyers lack mental models for AI-assisted workflows. They either expect too little (treating AI as a search engine) or too much (expecting autonomous completion of open-ended complex tasks).

> "It takes way more work than we thought it would... the expectation management has surprised me."

This is a **significant** and **improving** limitation, but the training and onboarding burden substantially increases deployment cost and slows adoption velocity.

### MCP: Underhyped and Overhyped Simultaneously

The MCP framework is genuinely important for enabling composable tool integration—it represents the right architectural direction. But it is simultaneously overhyped in the sense that production deployment requires resolving authentication, security, and reliability concerns that are not yet addressed in the specification. "Everybody's talking about it and trying to just plug things in" without those concerns resolved. Current status: **significant** limitation, **improving** trajectory, months horizon.

### Roadmap Uncertainty from Rapid Model Improvement

Model capabilities improve on 3-6 month cycles. Features that represent significant engineering investment can become obsolete when a new model makes them trivially achievable. There is "no perfect way of predicting what the model capabilities are going to be even tomorrow." This creates a product strategy problem: what to build vs. what to wait for the models to solve automatically.

---

## The Future of Legal Practice

### The Role Transformation

The traditional lawyer profile—valued for thoroughness and instruction-following—is shifting toward:

- **Entrepreneurial**: challenging established methods rather than following precedent
- **Creative**: discovering novel AI applications in practice
- **AI-fluent**: managing agents rather than executing tasks directly

"Lawyers may essentially become managers from day one of a bunch of AI agents." This is a fundamentally different skill set than being a diligence associate—and it implies that legal education must change to match.

### Market Entry Strategy: Lessons from Legora

Starting in a smaller, fragmented market (Sweden) allowed Legora to achieve dominance before facing the intense competition of the US market. The strategic logic: in a small market, the pressure to narrow scope (solve just one niche problem) is weaker, allowing the platform breadth needed to build a genuinely unified solution. Had they started in the US, competitive pressure would likely have forced premature specialization.

---

## Related Themes

- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]

## Key Concepts

- [[entities/braintrust|BrainTrust]]
- [[entities/gpt-35|GPT-3.5]]
- [[entities/hybrid-search|Hybrid Search]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/openai-o3|OpenAI o3]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/y-combinator|Y Combinator]]
- [[entities/o3|o3]]
