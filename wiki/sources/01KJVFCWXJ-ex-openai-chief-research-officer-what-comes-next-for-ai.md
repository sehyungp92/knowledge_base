---
type: source
title: 'Ex-OpenAI Chief Research Officer: What Comes Next for AI?'
source_id: 01KJVFCWXJSP7QVB33VJHB0FQG
source_type: video
authors: []
published_at: '2024-12-18 00:00:00'
theme_ids:
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- frontier_lab_competition
- pretraining_and_scaling
- robotics_and_embodied_ai
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Ex-OpenAI Chief Research Officer: What Comes Next for AI?

A candid inside-view assessment of the AI scaling landscape from a former OpenAI Chief Research Officer, covering the mechanics of pre-training progress, the emergence of test-time compute as a new scaling axis, the practical barriers to agentic deployment, and a sober reckoning with where hype outpaces reality across robotics, enterprise integration, and job automation.

**Authors:** Bob McGrew (former OpenAI Chief Research Officer)
**Published:** 2024-12-18
**Type:** video

---

## AI Progress: The Inside View vs. Outside View

One of the source's central claims is that external perception of AI progress diverges sharply from what practitioners inside the major labs understand. Outside observers see dramatic capability gains; insiders understand that each pre-training generation requires approximately a **100x increase in effective compute** — achieved through a combination of more chips, larger data centers, and algorithmic improvements — and that these infrastructure buildouts are inherently **multi-year processes**. This gap explains why the question "has a data wall been hit?" is structurally different when asked from the outside versus inside.

The trajectory from GPT-2 → GPT-3 → GPT-4 illustrates the pattern: each step required roughly 100x more effective compute, with algorithmic improvements contributing a relatively modest 2–3x. The rest comes from raw infrastructure. This makes [[themes/pretraining_and_scaling|pre-training progress]] a construction problem as much as a research problem — new data centers, not new ideas, are the critical path. See [[themes/scaling_laws|scaling laws]] for the broader quantitative backdrop.

---

## Test-Time Compute: A New Scaling Axis

The most significant technical contribution in this source is the framing of **o1 as a new generation** rather than an incremental update. Despite the branding decision to avoid "GPT-5," o1 represents approximately a 100x effective compute increase over GPT-4 — but achieved through **reinforcement learning at inference time** rather than pre-training expansion.

The mechanism: RL training produces longer, coherent chains of thought. A model spending hours to generate an answer involves roughly **10,000x more compute** than one answering in seconds. Crucially, this compute is drawn from inference time, not from building new data centers. OpenAI had been exploring test-time compute utilization since around 2020; o1 is the first practical implementation that avoids wasting that compute.

This opens a new scaling frontier with significant room for algorithmic improvement:

> *"There's no reason in theory why the same sort of fundamental principles and ideas that are used to get o1 thinking for minutes couldn't be extended to hours or even days."*

The open question — and a key bottleneck — is **how pre-training progress will stack with the RL process** when the next generation is trained. Stacking these two axes remains the critical unknown for near-term capability trajectories.

**Limitation:** Scaling test-time compute from minutes to days is not straightforward. Training stability and efficiency problems at longer horizons are unsolved, and there is no demonstrated path from the techniques working at minute-scale to working at day-scale. (Severity: blocking; trajectory: improving; horizon: 1–2 years.)

---

## Agentic Form Factors and Reliability

The source argues that GPT-4-class models already handle most current chatbot interactions adequately. The capability gap that matters now is not raw intelligence but **form factor** — the interaction paradigm needed to unlock o1-class reasoning for real-world tasks.

The underlying breakthrough in o1 is coherent chains of thought applied not just to reasoning but to **planning and action sequences**. This maps naturally onto long-horizon agentic tasks: booking, purchasing, code review, drafting policy documents. But the gap between capability and deployment is reliability.

**The reliability scaling problem:** Going from 90% to 99% reliability requires an order-of-magnitude increase in compute; 99% to 99.9% requires another. For agents taking irreversible actions — sending emails, pushing PRs, making purchases — the required reliability floor is well above current levels. The source is skeptical that 99.999% reliability is achievable in the near term.

**Computer use agents** are identified as the most general agentic form factor: one model controlling mouse, keyboard, and screen via screenshot loops, eliminating the need for application-specific integrations. However:

- Token consumption is **10–100x higher** than programmatic API integrations due to sequential screenshot-action-screenshot loops
- Inference latency makes real-time use impractical
- Reliability at the required threshold "might prove difficult"

Discussions about computer use agents predate Anthropic's public rollout, with OpenAI considering similar approaches internally from around 2020. The observation that application-specific computer use agents don't make technical sense — because the value is in training data that application providers should share with all foundation model labs rather than build isolated agents — points toward a [[themes/ai_market_dynamics|market structure]] implication: vertical-specific agents are likely a transitional form.

---

## Enterprise Integration

For enterprise deployment, the bottleneck is not model capability but **context**. Consumer applications can operate with minimal context; enterprise tasks require awareness of the codebase, team preferences, prior attempts, project documentation, and ambient organizational knowledge distributed across Slack, Figma, code repositories, and email.

Two paths exist:
1. **Custom connectors** — one-off integrations per data source, which whole platform businesses (e.g., Palantir) have been built around, with consulting firms currently doing well from the handholding this requires
2. **General computer use agents** — which sidestep integration entirely but reintroduce the token cost and reliability problems described above

No standard pattern for connecting LLMs to internal enterprise knowledge has emerged. The deployment gap remains significant, with expensive per-deployment integration work as the current norm. (Severity: significant; trajectory: improving; horizon: 1–2 years.)

---

## Robotics

The source expresses qualified optimism about **industrial robotics** and firm skepticism about **consumer robotics**.

**Foundation models** are identified as a genuine breakthrough for robotics: they dramatically accelerate the ability to get robotic systems operational and generalizing across tasks, replacing extensive domain-specific engineering. This applies both to vision-to-action pipelines and natural language control interfaces.

**Industrial bottleneck:** Robot simulators handle rigid bodies well but fail for deformable materials — cloth, cardboard, soft objects. A substantial fraction of warehouse and retail manipulation tasks involve exactly these materials. Real-world demonstrations remain the only approach for general manipulation, making training data collection manual, expensive, and slow. (Severity: blocking; trajectory: stable; horizon: 3–5 years for resolution.)

**Consumer robotics:** The source is explicitly bearish. Home environments are unconstrained; robot arms are physically dangerous to inhabitants, particularly children. This is not a capability problem but an **irreducible safety constraint** — the physical danger cannot be engineered away at acceptable cost for mass-market deployment. (Severity: blocking; trajectory: stable; horizon: 5+ years.)

See [[themes/robotics_and_embodied_ai|robotics and embodied AI]] for related coverage.

---

## What Is Overhyped

The source draws a sharp distinction between genuine progress and overhyped directions:

**New architectures:** Repeatedly fail to scale. The GPT-3 → GPT-4 jump required no foundational new techniques — both trained roughly the same way, with progress coming from pure scaling. Alternative architectures tend to look promising at small scale and collapse at production scale. (Severity: significant; trajectory: stable; horizon: 5+ years before any paradigm shift.)

**Benchmark validity:** Benchmark saturation is a persistent problem. GPQA moved from near-zero to complete exhaustion before GPT-4's release, rendering it uninformative. Standard benchmarks saturate faster than models are deployed, requiring constant creation of harder evaluations. This creates a structural gap in rigorous evaluation capability at the frontier.

**Job automation timelines:** Jobs are composed of many tasks, and real job analysis consistently reveals at least one task per role that resists automation. Even for highly technical knowledge work, direction-setting and goal-definition remain difficult to automate. Full job automation is a 5+ year horizon at minimum.

**AI productivity in GDP statistics:** Despite massive capability gains, measured productivity impact remains near zero. The 0.1% GDP growth attributed to AI is from compute capex, not model-driven productivity. The source flags this as a "deeply pessimistic" frame that is nonetheless the correct one to hold.

---

## Open Questions

- How will pre-training scaling stack with RL-based test-time compute in the next generation?
- Can test-time compute techniques extend from minutes to hours or days without training instability?
- What is the right form factor for unlocking o1-class models for non-programmer users?
- Will computer use agent reliability reach the threshold required for safety-critical autonomous action?
- How will enterprise context integration be standardized — connectors, computer use, or something else?

---

## Themes

- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]
- [[themes/alignment_and_safety|Alignment and Safety]]
- [[themes/frontier_lab_competition|Frontier Lab Competition]]
- [[themes/ai_governance|AI Governance]]

## Key Concepts

- [[entities/gpqa|GPQA]]
- [[entities/reinforcement-learning-for-reasoning|Reinforcement Learning for Reasoning]]
- [[entities/sora|Sora]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/o1|o1]]
