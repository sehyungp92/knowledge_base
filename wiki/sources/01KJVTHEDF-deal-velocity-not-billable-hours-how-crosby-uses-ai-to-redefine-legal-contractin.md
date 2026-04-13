---
type: source
title: 'Deal Velocity, Not Billable Hours: How Crosby Uses AI to Redefine Legal Contracting'
source_id: 01KJVTHEDFHEP9QXAWVYP0H1VZ
source_type: video
authors: []
published_at: '2025-09-02 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- multi_agent_coordination
- software_engineering_agents
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Deal Velocity, Not Billable Hours: How Crosby Uses AI to Redefine Legal Contracting

> This source profiles Crosby, an AI-first law firm built entirely around automating contract negotiations, revealing how the combination of per-customer fine-tuning, document-based pricing, and tightly coupled lawyer-engineer teams produces a novel organizational model for professional services automation — and exposing where current AI capability still requires expert supervision.

**Authors:** Ryan, John (Crosby founders)
**Published:** 2025-09-02
**Type:** video

---

## Core Thesis

Crosby's central bet is that contract negotiation — one of the most routine yet high-stakes forms of legal work — can be dramatically accelerated by AI if the organizational structure is rebuilt from the ground up. Rather than building legal software, they built a law firm: one where lawyers and engineers sit at alternating desks, billing is per-document instead of per-hour, and every contract processed generates proprietary training signal that foundation models never see.

The implication is not simply that AI can do legal work. It's that the structural barriers to AI adoption in professional services are organizational and economic, not purely technical.

---

## Organizational Architecture

### The Law Firm as the Right Vehicle

Traditional law firm partnership structures are structurally hostile to technology investment. Partners cannot sell equity, and only partners can take recourse loans, making speculative investment in infrastructure effectively impossible. This explains why legal software has historically come from outside law firms rather than inside them.

Crosby inverts this by building as a law firm from the start — gaining access to confidential contract data that external software vendors cannot touch, embedding liability and oversight natively, and treating legal services as a [[themes/vertical_ai_and_saas_disruption|vertically integrated product]].

> "Legal services are a credence good — you only know how good it is after the fact, and only an expert can truly evaluate it."

This means human oversight is not a temporary concession to regulatory pressure. It is structurally necessary: lawyers provide something close to quality insurance. The design implication is that AI in legal contexts should be optimized to reduce the cost and frequency of expert review, not to eliminate it.

### The Lawyer-Engineer Feedback Loop

The physical arrangement of Crosby's office — lawyer, engineer, lawyer, engineer — is not incidental. It reflects a theory about how domain expertise gets encoded into AI systems: not through batch evals, but through constant, daily interaction between people who understand legal risk and people who build the models.

This creates a feedback loop that surfaces friction at the level of individual word choices — whether a redline is precisely correct, whether a specific clause reflects the client's risk profile — rather than aggregate accuracy metrics. The result is instrumented iteration: every contract generates a trail of touchpoints (review counts, step durations, human interventions) that can be analyzed to identify and automate the highest-value steps.

---

## Capability Profile

### What Works

Crosby's production experience reveals a clear pattern of AI strengths in the contract domain:

- **Summarization and explanation** — AI reliably generates concise commentary explaining contract changes. More importantly, a well-reasoned explanation for why specific language is being pushed or rejected measurably reduces negotiation rounds. The optimization target shifts from accuracy alone to explanation quality.
- **Routing and triage** — A paralegal agent handles incoming work distribution, routing contracts to appropriate reviewers and managing workflow across the firm. This is functioning at production scale.
- **Personalized review alignment** — Fine-tuned models can be aligned to individual lawyers' decision-making patterns, since even two lawyers at the same firm will differ in how they handle edge cases.
- **Baseline contract review** — NDAs, MSAs, and DPAs can be reviewed, redlined, and annotated with AI assistance at what Crosby characterizes as narrow production maturity. NDAs are substantially simpler; MSAs represent the frontier of current capability.

### The 90% Trap

Foundation models reach approximately 90% accuracy on contract tasks essentially for free. The dangerous trap is treating this as near-complete. The gap from 90% to 99% — and especially to 99.99% — is not linear. It is extremely costly, requiring per-customer fine-tuning, per-customer eval pipelines, and careful context engineering. For high-ACV enterprise clients with unique risk profiles, this is the core engineering challenge.

> "One of the dangerous traps of language models today is they get to 90% for basically free. Getting them to 99 or 99.99 is actually extremely difficult."

---

## Limitations and Open Questions

These limitations are grounded in production experience, not theoretical caution:

**Semantic granularity in legal language** — The difference between "commercially reasonable" and "reasonable" is substantively significant to a lawyer. In embedding space, these terms appear nearly identical. Current AI models struggle with the subtle ways contract language changes meaning at the margin — the exact precision that legal work demands. This is not a solvable problem through prompt engineering alone; it reflects a representational limitation of current embedding-based approaches. (severity: significant, trajectory: stable)

**Data scarcity in the legal domain** — Foundation models are not specifically tuned for contracts because there is insufficient contract data in training corpora. The best available public source (EDGAR filings) is overused and covers a narrow slice of contract types. Crosby's structural advantage is that operating as a law firm gives them access to confidential data that creates a proprietary fine-tuning corpus — a moat that software-only competitors cannot replicate.

**The accuracy ceiling requires human oversight indefinitely** — Reaching production-grade accuracy on subtle legal language distinctions, combined with the credence-good nature of legal services, means human lawyers will remain in the loop for the foreseeable future. This is not simply a regulatory constraint; it is a quality-assurance requirement that the current generation of models cannot satisfy autonomously. The bottleneck is not throughput but expert attention bandwidth. (severity: blocking, horizon: 5+ years)

**Narrow contract scope** — Current production capability is limited to NDAs, MSAs, and DPAs. Expanding to the full range of contract types — and eventually to the complexity level of a junior associate — is the stated next step, but represents a significant capability jump.

**Creative negotiation remains human** — AI can apply rules to routine contract negotiations. It cannot generate novel negotiation strategies or handle unconventional counterparty positions. The creative, relational dimension of deal-making is not currently delegable.

---

## Business Model as Technical Enabler

The shift from billable hours to per-document pricing is not merely a commercial decision — it is a technical one. Billable hours align incentives with time spent; per-document pricing aligns incentives with speed and outcome. This creates internal pressure to reduce human touchpoints per contract, which drives the instrumentation and automation investment.

The billable hour has survived approximately 70 years of predicted obsolescence, having only become standard practice in the 1950s. Crosby's hypothesis is that predictive capability around contract complexity now makes per-document pricing viable where it previously was not — and that this pricing model, combined with AI, creates a fundamentally different cost structure than traditional legal services.

---

## Landscape Connections

| Signal Type | Theme |
|---|---|
| Paralegal routing agent in production | Agent Systems |
| Lawyer-engineer tight coupling as org innovation | AI Business and Economics |
| Per-customer fine-tuning pipeline | Vertical AI and SaaS Disruption |
| Multi-agent work routing and triage | Multi-Agent Coordination |
| AI-assisted professional services delivery | Software Engineering Agents |

### Key Bottlenecks Identified

1. **Legal domain data scarcity** — Insufficient diverse contract data prevents foundation models from achieving reliable performance on specialized legal terminology. Crosby's services-layer approach is a direct structural response. (horizon: 1–2 years)
2. **The 90→99% accuracy gap** — The jump from usable to production-grade accuracy is extremely costly and currently requires per-customer fine-tuning infrastructure. (horizon: 3–5 years)
3. **Semantic legal precision** — Embedding-based representations cannot distinguish fine-grained legal terminology. This bottleneck blocks fully autonomous contract editing without human review. (horizon: 3–5 years)
4. **Human oversight as throughput ceiling** — Lawyer-in-the-loop requirement constrains scaling by expert attention bandwidth; this is unlikely to change while legal services remain credence goods. (horizon: 5+ years)

### Notable Discovery

In May 2025, Crosby observed that the quality of AI-generated explanations for contract positions — not just the accuracy of the redline itself — directly reduced negotiation rounds and improved counterparty acceptance. This shifted optimization focus from output correctness toward reasoning clarity, with measurable impact on deal velocity.

---

## Open Questions

- At what accuracy level does per-customer fine-tuning become economically unviable for mid-market clients (not just high-ACV enterprise)?
- Can the lawyer-engineer co-location model be replicated at scale, or does it require the small-team density Crosby currently operates at?
- Will the proprietary data moat remain durable as foundation model training datasets expand to include more legal corpora?
- What is the lower bound on human review time per contract before quality assurance breaks down — and is that bound set by current AI capability or by liability structures that persist regardless?

## Key Concepts

- [[entities/context-engineering|Context Engineering]]
- [[entities/gemini-25-pro|Gemini 2.5 Pro]]
- [[entities/harvey|Harvey]]
- [[entities/reinforcement-fine-tuning|Reinforcement Fine-Tuning]]
- [[entities/services-as-software|Services as Software]]
