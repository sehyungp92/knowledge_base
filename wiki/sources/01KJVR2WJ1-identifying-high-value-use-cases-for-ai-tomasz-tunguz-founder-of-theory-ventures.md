---
type: source
title: Identifying high-value use cases for AI | Tomasz Tunguz (Founder of Theory
  Ventures)
source_id: 01KJVR2WJ1ZQPBM0QNT2P4DPK0
source_type: video
authors: []
published_at: '2024-06-26 00:00:00'
theme_ids:
- ai_business_and_economics
- interpretability
- model_behavior_analysis
- startup_and_investment
- startup_formation_and_gtm
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Identifying High-Value Use Cases for AI | Tomasz Tunguz (Theory Ventures)

> Tomasz Tunguz, founder of Theory Ventures, maps the structural dynamics of the current AI wave — from why incumbents hold the advantage to how evaluations, accuracy curves, and compounding error rates define where LLMs can and cannot yet be trusted. The talk offers a practitioner's framework for identifying high-value AI use cases by locating demographic labor shortages, rote toil, and the right point on the copilot-to-agent spectrum.

**Authors:** Tomasz Tunguz
**Published:** 2024-06-26
**Type:** Video
**Source:** https://www.youtube.com/watch?v=ULWKnWcqAJ0

---

## Two Waves of LLM Adoption

Tunguz argues we are approaching the peak of the *first* wave of AI adoption, characterized by treating the LLM itself as a complete product — raw input-to-output pipelines with no surrounding infrastructure. This wave is revealing its inadequacy: non-deterministic outputs, hallucinations, and uncontrolled error rates make bare LLMs insufficient for most serious applications.

The **second wave** will be catalyzed not by better models alone, but by the maturation of the surrounding stack: security systems, monitoring, classifiers, hallucination suppression, and evaluation infrastructure. The second wave is less about the model and more about making the model *trustworthy*.

A structural observation underlies both waves: unlike mobile or internet, where startups dominated early platform shifts, AI incumbents hold an asymmetric advantage. Google controls roughly 60% of top AI PhDs alongside the data, compute, and distribution that startups cannot replicate. This is a fundamentally different competitive dynamic.

---

## The LLM Data Stack

Tunguz draws a close parallel between the modern data stack and emerging LLM infrastructure:

| Modern Data Stack | LLM Equivalent |
|---|---|
| ETL / data pipelines | Document chunking, RAG ingestion |
| Cloud data warehouse | Vector database |
| BI / reporting | LLM-powered analytics |
| ML inference | LLM agent / copilot |
| Data transformation | Embedding generation |

Every organization deploying LLMs will converge on some version of this architecture: chunking and retrieval systems, embedding pipelines, vector stores, and multiple production consumers downstream. Superlinked (a Theory portfolio company) is building a vector computer that combines numerical and textual data with real-time updates — the underlying mechanism behind TikTok and YouTube Shorts recommendation systems.

A less-discussed consequence: the organizational fusion of AI teams into software engineering. These two disciplines — historically siloed — now need a common language. Software engineers must understand data structuring; data engineers must learn production system discipline. This is a significant organizational bottleneck.

---

## The Evaluation Problem

The deepest technical challenge Tunguz identifies is **evaluation** — and he argues it is primarily a resource problem, not a technology problem.

### Why Evaluations Are Hard

- **Non-determinism across versions:** Upgrading an LLM version or changing its training data breaks 20–40% of existing prompts. This means every version upgrade requires re-evaluating the full prompt library.
- **Low inter-annotator agreement:** Human graders agree only ~60% of the time on the same output. Two of three raters will agree; the third will not. This limits how reliable human-graded golden sets can be.
- **Context-specificity:** A tax auditor, a CFO, and a public markets investor all read the same income statement differently. No universal evaluation set exists. Every company must build its own.

### The Golden Set

Businesses respond by developing a *golden set*: the specific evaluations most critical to their use case. These are expensive to construct, maintain, and update — more akin to software testing than model research.

The failure to solve this at industry scale has a compounding consequence: **vendor lock-in**. When switching from one LLM version to another (or from proprietary to open-source) requires re-validating thousands of context-specific evaluations, migration costs become prohibitive. The rate of innovation slows accordingly.

### The Future of Evaluations

Tunguz's bet: analytics platforms that *observe* user interactions with AI, cluster conversation patterns, and *synthetically generate* evaluation test cases from actual behavior. Context (another Theory portfolio company, founded by ex-Google engineers) is building in this direction.

---

## The Accuracy Curve

A recurring empirical pattern across ML systems: new innovations launch at ~75% accuracy and require **10–15 years** of iteration to reach 95–98% accuracy. The improvement curve is nonlinear — fast early gains, then a long tail of difficult percentage points.

This timeline has direct implications for [[themes/vertical_ai_and_saas_disruption|vertical AI adoption]] in regulated industries. A 75% accurate loan decision model is unusable for a bank. A 75% accurate image-of-a-cat model is perfectly acceptable for a consumer app. The same accuracy number means something entirely different depending on the stakes.

---

## Where AI Works Now: The Use Case Framework

### Consumer vs. Enterprise

**Consumer AI** is well-served by current capabilities because:
- The range of acceptable outputs is extremely wide
- The cost of an incorrect output is negligible
- There is no accountability chain

**Enterprise AI** is constrained by the inverse: narrow acceptable ranges, high costs of error, and regulatory accountability — especially in finance, healthcare, and legal.

### The Copilot-to-Agent Spectrum

Tunguz identifies three tiers of LLM deployment:

1. **LLM as product** (Wave 1): bare input-output. Insufficient.
2. **Copilot / sentence completion**: Human remains in the loop, reviewing AI suggestions. Provides ~50% productivity acceleration in coding and knowledge work. Well-validated, broadly deployed.
3. **Full task automation (agents)**: Still early. The core problem is **compounding error rates** — if each step in a multi-step task has a 20% error rate, errors multiply rapidly across the task horizon. Tunguz uses the analogy of "Tommy T the intern": you wouldn't let a new hire run unsupervised on a multi-week project.

The path to reliable agents runs through error correction: pairing LLM generation with classical ML validators or adversarial critic models that flag invalid suggestions at each step before they propagate.

### Finding High-Value Use Cases: Rote Toil + Demographic Shortage

Tunguz's investment framework for identifying genuinely high-value AI opportunities:

> *Look for rote toil — repetitive, unattractive work — in industries with demographic labor shortages.*

The canonical example: **long-haul truck driving**. The average US long-haul truck driver is over 60. Few young workers enter the profession. The work is repetitive and physically demanding. This creates a structural supply-demand mismatch that AI (in this case, autonomous vehicles) can fill without displacing a large willing workforce.

Applied to white-collar work, the same logic yields:

- **Security Operations Centers (SOCs):** Enterprises receive ~8,000 security alerts per day from ~75 different security products. Alert fatigue is severe; triage is repetitive. LLMs can classify and prioritize.
- **Accounting / ERP data entry:** 50–60 robotic process automation tasks around reading W2s, 1099s, and other financial documents. Structured enough for current LLM capabilities.
- **BDR / sales outreach:** AI can scale outbound activity significantly. The binding constraint is not AI capability but email platform rate limits (~50 outbound/day).

---

## Key Limitations and Open Questions

The talk is unusually candid about unresolved constraints:

- **Non-determinism is fundamental**, not incidental. It requires redesigning not just infrastructure but *product logic* and *sales processes*.
- **Agentic risk propagation** is not well understood. Long-horizon tasks accumulate errors in ways that are hard to predict or bound.
- **Inference costs** remain prohibitively high for large models at scale. Edge deployment (running models on laptops and phones) is an emerging mitigation — Google is already moving in this direction — but not yet broadly solved.
- **Organizational transformation** from siloed ML and software teams to integrated AI engineering is ongoing and painful. The tooling and common languages are still being invented.
- **Enterprise purchasing policy** is still unsettled. Many large buyers have not yet decided whether to run AI in cloud or on-premises, creating sales uncertainty for startups.

---

## Landscape Connections

### Themes
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]
- [[themes/model_behavior_analysis|Model Behavior Analysis]]
- [[themes/interpretability|Interpretability]]

### Bottlenecks Addressed
- Error compounding in multi-step tasks → blocks reliable agentic automation
- Evaluation standardization → blocks rapid LLM application iteration
- Accuracy improvement timelines → blocks regulated-industry adoption
- Organizational skill gaps → blocks efficient production deployment
- Vendor lock-in from non-determinism → slows industry-wide innovation
- Inference cost → limits deployment options and margin

### Breakthroughs Noted
- **Edge-based inference:** Running substantial language models on consumer devices rather than requiring data center GPUs
- **Error correction via classical ML validators:** Pairing LLM output with adversarial critic models to constrain per-step error rates
- **Analytics-driven evaluation generation:** Synthesizing evaluation cases from observed user interaction patterns

## Key Concepts

- [[entities/retrieval-augmented-generation|Retrieval Augmented Generation]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/agentic-ai|agentic AI]]
- [[entities/data-flywheel|data flywheel]]
