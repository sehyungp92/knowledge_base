---
type: source
title: 'Sarah Guo and Elad Gil: The Future of AI Investing'
source_id: 01KJVR0B99DNB238SCFEE07RYH
source_type: video
authors: []
published_at: '2024-02-01 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- frontier_lab_competition
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Sarah Guo and Elad Gil: The Future of AI Investing

> A wide-ranging investor conversation between Sarah Guo (Conviction) and Elad Gil tracing the emergence of the AI wave from GPT-3 through ChatGPT, mapping the five waves of human capital entering the field, and stress-testing defensibility theses for foundation models, tooling, and application companies — with a particular emphasis on the $3.5T services market as the primary opportunity horizon for generative AI startups.

**Authors:** Sarah Guo, Elad Gil
**Published:** 2024-02-01
**Type:** video

---

## Overview

This conversation captures how two sophisticated AI investors understood the landscape roughly fourteen months after ChatGPT's launch. Rather than treating ChatGPT as the beginning of AI, both situate it as a *starting gun for the mainstream* — the actual capability inflection having occurred with GPT-3 and GPT-3.5, which were visible to a small group paying close attention. The central analytical contribution is the segmentation of the AI opportunity space: a $500B software market dwarfed by a $3.5T services payroll addressable by generative AI, with each new model generation unlocking new verticals that the prior generation couldn't serve.

---

## The Emergence Timeline

The conversation reconstructs how the current wave actually unfolded for those watching closely:

- **GPT-3** was the real inflection — a qualitative step up from GPT-2 that attracted serious investor attention and the first wave of AI-native founders
- **GPT-3.5** was an even larger step function, triggering a major wave of AI company funding
- **ChatGPT** (November 2022) was a research preview that "just took off like crazy" — but the consumer reaction was unexpected even by investors who had been tracking the technology

This matters because it frames the current moment: if ChatGPT was the starting gun for *most people*, and meaningful enterprise adoption is still nascent, the S-curve has a long way to run. The compounding dynamic — small attentive ecosystem → massive funded ecosystem — is still early.

---

## The Five Waves of Human Capital

A useful taxonomic framework for understanding who is building what and when:

1. **AI-native builders** — researchers from Google, OpenAI, Facebook building LLMs and foundation models first, then apps. Examples: Noam (Character.ai), Aravind (Perplexity)
2. **Hardcore dev/infra people** — providing the stack for models and tooling. Examples: Baseten, Braintrust
3. **B2B app founders** — heard about ChatGPT, quit jobs ~6 months later, building vertical software. Example: Harvey in legal
4. **Consumer wave** — slightly behind the B2B wave
5. **Enterprise adoption wave** — actual enterprise deployment, the slowest to move

This staggering creates predictable market structure: the infrastructure for early waves is already being built; the application opportunity for waves 3–4 is now open; enterprise (wave 5) will take years.

---

## The Core Market Thesis

The central framing is a market size reorientation:

- US software spend: ~**$500B**
- US services headcount payroll addressable by generative AI: ~**$3.5T**

If even 5–10% of services spend converts to software, that roughly reproduces the entire existing software market. This is the logic behind [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]] — not displacing existing SaaS, but converting labor spend into software spend.

The **capability ladder** dynamic is critical here: each new model generation unlocks new verticals. GPT-3 couldn't do legal; GPT-4 enabled Harvey. Each subsequent capability step opens the next rung of services markets previously inaccessible to AI.

---

## Foundation Models: Capital, Scaling, and Specialization

### Scaling Trajectory

Continuing to scale language model training at state-of-the-art levels will cost **tens to hundreds of billions of dollars** if no new breakthroughs occur. This is a [[themes/frontier_lab_competition|frontier lab]] constraint — only a handful of entities can participate. However, scaling laws (characterized here as "Jensen's laws") work in favor of the ecosystem: for equivalent compute, capabilities are getting cheaper to train, and inference costs fall as well.

### The Specialization Matrix

Not all domains will be served by general-purpose models. The expected structure:

- Some domains absorbed by general foundation models
- Some requiring specialized architectures (e.g., AlphaFold combines transformers with domain-specific structure)
- A **matrix of performance vs. generalizability** with different companies occupying different cells

Modality expansion is explicit: voice (TTS/STT), image diffusion, video, audio, code, biology, physics, materials science, mathematics. Some of these specialized model companies will be first-of-their-kind, like Mistral in open-source.

### Open Source Dynamics

Mistral is characterized as a "first of its kind" open-source play, demonstrating that competitive performance is achievable without proprietary infrastructure. Open-source progress will continue in parallel with proprietary scaling, creating ongoing competitive pressure on API pricing and defensibility.

---

## Capabilities in Evidence

| Capability | Maturity | Evidence |
|---|---|---|
| LLMs solving complex domain problems | Narrow production | Decades-long open problems being solved |
| Vision-language models (GPT-V) for OCR and visual reasoning | Narrow production | Enterprise image understanding APIs |
| Image generation at commercial scale | Broad production | Midjourney: reported hundreds of millions in revenue |
| Video generation | Narrow production | Pika, Haen as emerging commercial applications |
| Code assistance | Narrow production | Copilot/ChatGPT in engineering workflows |
| Specialized science models | Narrow production | AlphaFold hybrid architecture |
| Open-source competitive models | Narrow production | Mistral/Mixtral mixture-of-experts |
| Consumer AI at scale | Broad production | OpenAI: ~$1.6B revenue, majority consumer |
| Foundation models for robotics/physical domains | Demo | Increasingly tractable, not yet production |

---

## Limitations and Open Questions

Several limitations are treated as structurally important, not incidental:

**Capital concentration** — Training frontier models at state-of-the-art requires capital that structurally excludes most actors. This is not expected to resolve soon (trajectory: stable).

**Productivity claims vs. reality** — The "10x engineer" framing from AI coding tools is questioned. The claimed productivity multipliers are not consistently observed in practice. This is a significant limitation for enterprise sales cycles and adoption justifications.

**SMB addressability** — True small businesses (5-person companies) are not viable AI customers. They buy only 3–4 things total. The $3.5T services thesis applies to mid-market and enterprise services, not small business.

**Chat interface limitations** — Chat-only interfaces are insufficient for most valuable AI applications. Multimodal interfaces, action-taking agents, and integration with proprietary data sources are prerequisites for many high-value use cases.

**Model differentiation opacity** — The line between fine-tuning on large unique datasets and pre-training is becoming blurry. Communicating actual performance differences between custom models and base models to customers is genuinely difficult, undermining defensibility narratives.

**Copyright and provenance** — The training data copyright situation is unresolved and worsening. Even removing original works from training sets may be insufficient if derivative works already saturate distributions. A long-term resolution mechanism (potentially Web3-based provenance tracking) is needed but not near.

**Hardware device constraints** — Standalone AI hardware devices are less performant than cloud-based models unless solving specific physical sensing problems. The hardware-first AI interface thesis is structurally disadvantaged.

**Agent identity and verification** — Multi-agent delegation requires robust identity systems. The technical infrastructure for blockchain-based identity exists; the agent verification layer does not yet. This is a blocking constraint for trustworthy autonomous agent applications.

---

## Bottlenecks

The conversation surfaces several active bottlenecks in the [[themes/ai_business_and_economics|AI business landscape]]:

**Training data availability** (1–2 year horizon) — Novel data collection is becoming a limiting factor for continued scaling. Synthetic data generation and new contribution mechanisms are potential partial mitigations.

**Scaling vs. architecture decision** (1–2 year horizon) — Whether continued capital deployment into scaling will yield proportional capability gains, or whether new architectural breakthroughs are required, is undecided. This is the central capital allocation question for frontier labs.

**Application defensibility** (1–2 year horizon) — As base models commoditize, identifying sustainable moats for application companies is the critical [[themes/startup_and_investment|startup investment]] question. Data network effects, workflow integration depth, and distribution are the primary candidates.

**Legal/regulatory clarity on IP** (3–5 year horizon) — Content provenance, copyright, and rights structures for AI-generated media require resolution before some market segments can sustainably scale.

**Specialized vs. general model allocation** (1–2 year horizon) — Which domains require purpose-built architectures vs. general model fine-tuning is still being determined empirically, complicating capital allocation.

**Agent identity infrastructure** (3–5 year horizon) — Trustworthy multi-agent systems require verification layers that don't yet exist at production scale.

---

## Breakthroughs Referenced

- **GPT-3**: Established viability of large language models for commercial applications; triggered first investor wave (major)
- **ChatGPT**: Demonstrated consumer willingness to pay for AI at scale; 1.6B revenue rumored within ~14 months of launch (major)
- **Image generation (Midjourney, Stable Diffusion)**: Market displacement of creative professionals faster than anticipated, with simultaneous market expansion (major)
- **Open-source models (Mistral/Mixtral)**: Competitive performance without proprietary infrastructure (notable)
- **Scaling law cost reduction**: Equivalent capabilities becoming cheaper to train over time (notable)
- **GPT-V (vision-language)**: New enterprise application domains opened by multimodal reasoning (notable)
- **Foundation models in physical domains**: Biology, physics, materials science becoming tractable (notable)

---

## Investment Framing

Several patterns are articulated as durable for [[themes/vc_and_startup_ecosystem|VC and startup ecosystem]] participants:

- **Timing asymmetry**: Being slightly early or slightly late is acceptable; being out of the market entirely is not. Experimentation beats precision timing.
- **Founder wave matching**: The type of founder building right now (wave 3, B2B app) is different from the right type for foundation models (wave 1). Mismatching founder profile to market moment is a persistent failure mode.
- **First wave failure pattern**: Early AI founders who focused on building their own models rather than finding customers — many of those companies will not survive.
- **Consumer underweight**: The startup ecosystem has overcorrected toward B2B SaaS playbooks. Consumer AI is significantly underdone relative to demonstrated market size (Midjourney, OpenAI consumer revenue).
- **Figma-style distribution**: Individual contributor adoption inside enterprises, then expanding upward — a proved distribution motion now available to AI-native tools.

---

## Related Themes

- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/frontier_lab_competition|Frontier Lab Competition]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/ai-agent|AI Agent]]
- [[entities/alphafold|AlphaFold]]
- [[entities/characterai|Character.AI]]
- [[entities/diffusion-model|Diffusion Model]]
- [[entities/diffusion-models|Diffusion Models]]
- [[entities/figma|Figma]]
- [[entities/fine-tuning|Fine-tuning]]
- [[entities/foundation-model|Foundation Model]]
- [[entities/harvey|Harvey]]
- [[entities/midjourney|Midjourney]]
- [[entities/mistral|Mistral]]
- [[entities/no-priors-podcast|No Priors Podcast]]
- [[entities/perplexity|Perplexity]]
- [[entities/pika|Pika]]
- [[entities/scaling-laws|Scaling Laws]]
