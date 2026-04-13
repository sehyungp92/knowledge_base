---
type: source
title: Getting the Most From AI With Multiple Custom Agents ft Dust’s Gabriel Hubert
  and Stanislas Polu
source_id: 01KJVV0PNMHV3X43F3SXA1BSP9
source_type: video
authors: []
published_at: '2024-11-26 00:00:00'
theme_ids:
- ai_business_and_economics
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Getting the Most From AI With Multiple Custom Agents ft Dust's Gabriel Hubert and Stanislas Polu

A practitioner-level conversation with the co-founders of Dust on why multi-model architectures beat single-model bets, where enterprise AI deployment is actually working, and why reasoning — the capability that matters most — has been conspicuously flat for two years. Recorded in late 2024, the discussion offers grounded evidence from real deployments alongside a frank assessment of the limits that most AI commentary glosses over.

**Authors:** Gabriel Hubert, Stanislas Polu
**Published:** 2024-11-26
**Type:** video

---

## The Multi-Model Thesis

Dust was founded in early 2023 by Gabriel Hubert and Stanislas Polu, both alumni of Stripe and OpenAI, on a contrarian conviction: one model would not rule them all. At a moment when GPT-3.5 appeared to dominate, they built toward a world of competing models and multi-model integration as the locus of value.

Their reasoning was structural, not speculative. To those close to the market, multiple labs were visibly emerging and competitive dynamics were predictable. The real insight was about the customer layer: regardless of which model wins any given benchmark, enterprises need to switch between models based on use case, data sensitivity, and performance — and that switching requires a stable interface layer above the models.

Two scenarios justify this thesis regardless of how the technology evolves:

1. **Continued rapid progress**: Frontier labs keep competing, scale keeps driving gains, and customers always want the latest best model. Switching value persists indefinitely.
2. **Technology plateau and commoditization**: Models stop improving, costs collapse, every company trains its own. The router layer disappears — but so does the single-model winner.

In either world, the application and workflow layer retains value. The founders have so far been vindicated: Dust now integrates models from OpenAI, Anthropic, Google (Gemini), and Mistral, and reports real customer switching behavior driven by performance and sensitivity requirements.

---

## The Stochastic Shift

The hosts frame the current AI transition as the biggest shift in tool usage since the advent of the computer: the move from **deterministic** to **stochastic** technology experiences. Deterministic tools do exactly what you specify; stochastic tools produce drafts, suggestions, and probabilistic outputs.

Early adopters succeed precisely because they accept this trade-off: they tolerate variable outputs in exchange for a clear 10x upside on specific tasks. The organizational challenge is that most enterprise users — and most evaluation frameworks — were built for deterministic systems. This mismatch accounts for much of the friction in enterprise adoption.

This framing connects directly to the measurement problem observed in deployments: the same AI system may deliver 80% productivity gains in one function and only 5% in another, and organizations often cannot tell which is which in advance. Use cases emerge from organic user exploration, not upfront planning.

---

## Where Enterprise Deployment Is Actually Working

The clearest production deployments cluster around enablement of customer-facing and support functions:

- **Sales, support, and marketing teams** synthesizing proprietary data with AI-generated drafts — support ticket responses, call prep, content generation
- **Personal coaching assistants** providing daily or weekly feedback to individual employees, often used by early-career workers seeking career and decision-making guidance
- **Cross-functional data translation** — giving non-technical employees the ability to query codebases, understand pull requests, and extract technical context into plain language

The key unlock in all of these is access to **proprietary data in enterprise silos**. Generic AI assistants without this access cannot substitute for human knowledge workers. With it, they can draft, synthesize, and retrieve at a level that delivers measurable gains.

---

## Limitations and Open Problems

These are the findings that carry the most analytical weight.

### Reasoning Has Plateaued

The most significant signal in this conversation: **frontier model reasoning capabilities have been approximately flat for roughly two years** as of late 2024 — roughly since GPT-4. Context windows have grown, modalities have expanded (audio, image, video), but the core reasoning capability most relevant to real-world impact has not kept pace.

The hosts acknowledge the counterargument — that progress may be exponential but only sampled discontinuously, creating an illusion of flatness. They remain skeptical, and treat OpenAI's o1 as an incremental rather than fundamental advance in reasoning. This is the primary bottleneck they see blocking the next phase of AI impact.

### Training Cutoffs Are Not Solvable via Fine-Tuning

Models cannot be continuously updated with recent information. Training cutoffs are fixed, and **fine-tuning on company data is explicitly assessed as a bad idea** for most enterprise use cases — it is expensive, requires continuous retraining as data changes, and does not deliver expected gains at scale. The practical solution is retrieval-augmented generation (context injection), but this does not solve the problem of understanding what happened inside a company in the last week.

### Frontier Models Cannot Be Locally Deployed at Scale

Even open-weight versions of the best models require expensive GPU infrastructure to run. This blocks true edge deployment: for latency-critical or privacy-critical applications that cannot use API calls, there are no frontier-quality on-device options. The combination of this constraint with the reasoning plateau creates a gap: the models capable of complex reasoning are the ones that cannot be run locally.

### Enterprise Access Control Has Not Caught Up

Access control and data governance frameworks were designed for humans. An agentic AI system with autonomous data access breaks these assumptions: what does it mean for an AI to have "read access" to a file? What audit trails exist? How are permissions scoped for non-human actors? This is flagged as an unsolved problem that blocks enterprise-scale agentic deployment.

### Open Source Still Lags

Open-source models continue to trail closed-source frontier models in reasoning quality. Meta/Facebook is identified as the most important actor to watch, given their demonstrated willingness to release models openly and their resources to train at scale. But even if a competitive open-source model is released, deployment cost may render it inaccessible — if running it requires high-end GPU infrastructure, the practical difference between open-weight and proprietary narrows considerably.

---

## On the Shape of Progress

The conversation surfaces a productive disagreement on the trajectory of AI capabilities. The optimistic view (attributed to Kevin Scott) holds that progress is genuinely exponential but sampled infrequently, creating a perceptual illusion of flatness. The founders' view is more cautious: the *perception* of flatness in reasoning capabilities reflects actual slower progress, not sample bias.

This uncertainty is practically significant. Organizations building on AI need to make architectural bets on whether the next 2–3 years will bring another capability jump or continued incremental refinement. The Dust thesis — that the application and integration layer retains value either way — is partly a hedge against this uncertainty.

---

## Relevant Themes

- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/application-layer|Application layer]]
- [[entities/codex|Codex]]
- [[entities/fine-tuning|Fine-tuning]]
- [[entities/gpt-35|GPT-3.5]]
- [[entities/gpt-4|GPT-4]]
- [[entities/on-device-inference|On-Device Inference]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
