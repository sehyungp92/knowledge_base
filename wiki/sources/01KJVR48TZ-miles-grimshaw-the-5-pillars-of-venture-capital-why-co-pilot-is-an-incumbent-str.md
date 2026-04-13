---
type: source
title: 'Miles Grimshaw: The 5 Pillars of Venture Capital & Why Co-Pilot is an Incumbent
  Strategy | E1061'
source_id: 01KJVR48TZQRMPK7TYA97Q7CKV
source_type: video
authors: []
published_at: '2023-09-18 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Miles Grimshaw: The 5 Pillars of Venture Capital & Why Co-Pilot is an Incumbent Strategy | E1061

This source blends a practitioner's account of venture capital philosophy with a substantive analysis of the 2023 AI application layer — arguing that the transition from ML-specialist tooling to general-purpose AI development frameworks represents a tectonic shift analogous to Rails and Docker, while diagnosing why most AI startups remain structurally fragile and why autonomous AI ("sell the work") is still blocked by model capability ceilings.

**Authors:** Miles Grimshaw
**Published:** 2023-09-18
**Type:** video

---

## The 2012 Cloud Wave as Historical Frame

Grimshaw opens with a retrospective on 2012 — a moment when building modern web apps felt like wielding superpowers — to anchor his reading of the current AI moment. Cloud spend grew from ~$10B in 2012 to $300–400B by 2022, a shift he calls "tectonic." His point is that waves of this scale reward those who stay close to first principles rather than trying to be clever: *"it wasn't necessary to be too smart in many ways, especially when it's still that early in the cycle, but stick to the fundamentals."*

The implied thesis: the AI application layer is at a similarly early, pre-framework stage, where the most durable positioning comes from building the infrastructure others will depend on.

---

## The 5 Pillars of VC

Grimshaw organises venture practice around five "S's":

1. **Sourcing** — deal flow generation
2. **Selecting** — evaluation and conviction formation
3. **Signing** — closing
4. **Supporting** — post-investment value add
5. **Summiting** (or *Separating*) — realising the investment via distribution to shareholders

He notes that the framing of the fifth pillar matters: an investment is only complete when shares are distributed to a broader shareholder base. Investors who forget this conflate paper gains with exits.

His personal emphasis falls on **selecting and supporting** — particularly the work of connecting strategy to sequencing in terms of organisation and operations.

### Diligence as Adventure Planning

A recurring theme is the texture of the investor-founder relationship during diligence. Grimshaw argues diligence should feel like *planning an adventure together*, not an examination: *"it should feel like planning an adventure, where there are still serious topics you've got to grapple with, rather than a colonoscopy."*

The rate of learning and willingness to engage with discomfort matter more than polish: *"the best ones are just making new mistakes each time — the slope and pace of learning is the most important."*

### 'First to Call' vs. 'First Call'

Grimshaw explicitly rejects the "first call" investor mindset (being the founder's first call in a crisis) as reactive. He prefers being *first to call* — the investor who initiates, who is proactively engaged rather than waiting to be needed. This reframes the support pillar from reactive availability to proactive partnership.

### Founder Respect over Founder Friendly

He prefers "founder respect" to "founder friendly" — arguing that genuine respect involves sharing hard truths rather than cheerleading. The distinction matters because the aspiration of VC is to help founders make the very best decisions, which requires clarity and a different perspective, not validation.

---

## Where VCs Cause Harm

The clearest failure mode Grimshaw identifies is applying **procedures and checklists** to situations that require **bespoke strategy**. When VCs don't understand the specific strategic context and substitute generic frameworks, the result is distraction and burden rather than value. He also flags the danger of false confidence — assuming you always have the right answer.

The constructive framing: *"if you think about a couple really important decisions over the course of each year over the course of 10 years, you tilt those odds each time."* The cumulative effect of better decisions is the actual value proposition.

---

## The AI Application Layer: A New Computing Paradigm

The second major strand of the source is a structural analysis of where the AI ecosystem sits in 2023.

### The Developer Wave

Tens of millions of developers are becoming AI developers — a claim Grimshaw anchors to the Docker analogy. Docker scaled to tens of millions of developer accounts by containerising application development. The thesis is that an analogous framework for AI application development will follow the same trajectory, and LangChain is positioned as the candidate framework.

The key structural distinction: AI app development is **generative**, not retrieval-based. *"It's not retrieving from the database — it's generative."* This breaks the mental models that enterprise buyers and developers bring from database-centric architectures, which is simultaneously a limitation and a moat for whoever solves the tooling problem.

### Capabilities in Production (as of mid-2023)

- **AI co-pilot integrations** broadly shipped across major enterprise software — GitHub Copilot, full Microsoft Office suite — represent the first wave of broad production deployment. See [[themes/vertical_ai_and_saas_disruption|vertical AI and SaaS disruption]].
- **ReAct-style reasoning and acting** — models reasoning, taking actions, and issuing self-feedback in loops — established early agentic behaviour, though still at research stage. See [[themes/agent_systems|agent systems]].
- **LLaMA 2 fine-tuning** made domain-specific model customisation accessible to startups as a service, removing the prior requirement for ML specialisation.
- **LangChain and similar frameworks** enabled general-purpose engineers to build retrieval, chaining, and agentic behaviour without ML expertise.

The mid-2022 emergence of **unexpected reasoning capabilities** — analogical reasoning, arithmetic, apparent generalisation beyond text statistics — is flagged as the inflection point that established LLMs as a potential general computing paradigm. This is the source's primary breakthrough claim. See [[themes/agent_systems|agent systems]].

---

## Limitations and Open Questions

This source is notably candid about structural fragility in the current ecosystem. Several limitations are worth holding alongside the capability claims:

**Ecosystem immaturity.** The AI application development stack lacks the observability, monitoring, and standardised tooling that comparable paradigm shifts eventually produced (Rails + New Relic, Docker + surrounding ecosystem). The comparison is meant to be optimistic about trajectory but honest about current state. See [[themes/tool_use_and_agent_protocols|tool use and agent protocols]].

**Non-determinism as a fundamental problem.** LLM outputs are stochastic. *"There's randomness to it — how do you measure excellence of it?"* This blocks the kind of performance guarantees that enterprise software buyers expect and makes quality benchmarking genuinely unsolved. Severity: significant, trajectory unclear.

**The thin wrapper problem.** Most AI startups are building minimal proprietary differentiation on top of foundation models. *"They're all just wrappers on top of large language models."* This creates structural vulnerability to both incumbents and model providers. Grimshaw acknowledges some exceptions but treats the general condition as a serious concern for [[themes/startup_and_investment|startup investment]].

**Enterprise churn.** Early enterprise AI adoption is showing cancellation — experimental AI seats (even at Walmart scale) are being abandoned, revealing that current products are not delivering retained value. Severity: significant, trajectory unclear.

**The co-pilot ceiling.** The most structurally important limitation: current models are not capable enough to reliably deliver autonomous outcome-based work — "sell the work" — without human oversight. This locks AI into assistive co-pilot mode. The implication is that the co-pilot strategy is **an incumbent strategy**, not a startup strategy: incumbents can distribute thin AI integrations through existing relationships, while startups need the step-change to autonomous delivery to differentiate. Fine-tuning accessibility and open-source model quality (pre-LLaMA 2) compounded this ceiling. See [[themes/vertical_ai_and_saas_disruption|vertical AI and SaaS disruption]].

**Content abundance without discovery.** Generative AI dramatically lowers content creation costs while leaving discovery mechanisms unchanged, making signal-to-noise worse rather than better. *"That suddenly expands your competition by 100x — then discovery..."* Severity: significant, trajectory unclear.

**Trust-sensitive domain blockage.** LLM trustworthiness for high-stakes content (media, legal) is unresolved. Libel risk and inability to attribute outputs to authoritative sources blocks adoption in trust-sensitive domains entirely. Severity: blocking. See [[themes/ai_business_and_economics|AI business and economics]].

---

## Bottlenecks

Three structural bottlenecks are implicit in the analysis:

1. **Framework layer gap** — No mature, standardised framework exists for building, deploying, and monitoring LLM-powered applications. The Rails/Docker analogy frames this as a 1–2 year horizon problem. Blocking: broad developer adoption of AI application development.

2. **Model capability ceiling** — Current models insufficient for reliable autonomous outcome delivery, blocking the transition from assistive to agentic AI and from co-pilot to "sell the work" SaaS disruption. Horizon: 1–2 years.

3. **Fine-tuning accessibility** — Until LLaMA 2, startups lacked viable paths to customise models. As of recording, this bottleneck was partially resolving. Horizon: months.

---

## VC Philosophy: Founder, Product, Market

On the classic trilemma, Grimshaw lands on integration: *"ultimately, it's about the integration of all three factors."* For later-stage investing specifically, he positions as a **data-second investor** — data should validate theories, not generate them. Strong prior views on product and customer should exist absent data; data is confirmatory, not originary.

The Amazon "Working Backwards" discipline (from *Working Backwards* by Colin Bryar and Bill Carr) is cited as an exemplar of the user-grounded approach Grimshaw advocates: *"who's the user and why do they care?"* is the question he returns to as the tether to reality when frameworks and terminology proliferate.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/benchmark|Benchmark]]
- [[entities/benchmark-capital|Benchmark Capital]]
- [[entities/figma|Figma]]
- [[entities/hugging-face|Hugging Face]]
- [[entities/scale-ai|Scale AI]]
- [[entities/agentic-ai|agentic AI]]
