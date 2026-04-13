---
type: source
title: No Priors Ep. 59 | With Sarah Guo & Elad Gil
source_id: 01KJVS00V26Z39NDSVB07QJT1D
source_type: video
authors: []
published_at: '2024-04-11 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_market_dynamics
- frontier_lab_competition
- model_commoditization_and_open_source
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# No Priors Ep. 59 | With Sarah Guo & Elad Gil

This episode captures a wide-ranging investor discussion on the AI landscape as of April 2024, covering the rapid commoditization of frontier model capability, the shifting economics of model development, and the structural dynamics determining where value accrues across the stack. Sarah Guo and Elad Gil examine which market opportunities remain underexplored, identify the most consequential unresolved technical bottlenecks in robotics, time series reasoning, and video generation, and analyze how prosumer AI is outpacing enterprise adoption. The conversation is notable for its candid framing of what is not yet being built and why.

**Authors:** Sarah Guo, Elad Gil
**Published:** 2024-04-11
**Type:** Video / Podcast

---

## Model Commoditization and the Shifting Frontier

The most significant structural shift discussed is the unexpected speed at which GPT-4-level capability has become achievable outside of OpenAI. By April 2024, both [[entities/mistral|Mistral]] and Databricks (with DBRX) had demonstrated that tens of millions of dollars in compute, rather than hundreds of millions or more, could reach this capability tier. DBRX's mixture-of-experts architecture is highlighted specifically for making models fast in tokens per second and cost-effective to serve.

Databricks introduced what they termed **Mosaic's Law**: the cost to train a model of a given capability level will fall by 75% per year due to hardware and algorithmic improvements. This reframing has direct consequences for investment theses and for how soon open-source models close the gap with closed frontier models.

The expected monopolistic or oligopolistic model landscape has not materialized as predicted. However, at the true state-of-the-art frontier, compute scaling remains the dominant input. The hosts argue that oligopoly likely persists at that level for the next few years, driven not only by capital requirements but by a self-reinforcing dynamic: capable models can assist in building successor models through data labeling, RLHF, and AI-assisted feedback loops. This makes the frontier compound rather than simply scale.

---

## Value Capture: Clouds, Not Models

The proliferation of open and third-party models creates a counterintuitive value redistribution. Because cloud providers host all of these models, their revenue grows regardless of which model wins. Microsoft Azure's AI-related revenue grew approximately 5% in its last reported quarter, adding roughly $1.0 to $1.5 billion per quarter. This gives hyperscalers a durable incentive to continue funding foundation model development.

The implication for [[themes/startup_and_investment|startup and investment strategy]] is significant: most capital flowing into foundation models comes from hyperscalers and large tech companies, not venture capitalists. VC investment in new language foundation models is expected to contract, while funding for other modality models (music, video, biology, robotics, physics, materials science) will increase as a second wave of foundation model development begins. That wave will likely follow a similar pattern: early VC rounds followed by strategic acqui-funding once value is demonstrated.

Microsoft's hiring of Mustafa Suleyman is read as both a need for AI-aware product and research leadership and a hedge against over-dependence on OpenAI, reinforcing the theme that large incumbents are managing their optionality rather than betting on any single model provider.

---

## Where the Opportunities Are (and Why They Aren't Being Pursued)

Guo and Gil apply a framework of **identifying missing capabilities with large commercial surface area** rather than following mimetic investment trends. Two examples stand out:

**Time series reasoning.** The ability to reason over time series data with general knowledge and broader context remains largely unsolved. Applications span anomaly detection, infrastructure monitoring, security, healthcare, and consumer behavior modeling. The commercial opportunity is large and the architectural problem is tractable but underexplored. This is flagged as a bottleneck with a wide blast radius across multiple industries.

**Cross-domain AI adoption gaps.** There is insufficient cross-pollination between AI researchers and domain experts in fields like accounting, finance, and enterprise operations. Foundation models capable of operating on financial or accounting data with real reasoning ability would be highly commercially valuable, but the gap between who understands these models and who understands the domain remains a structural blocker.

The pattern the hosts observe is a mimetic clustering of startup activity around obvious opportunities (robotics, LLMs, biotech) alongside conspicuous absence from areas that are clearly commercially viable. This is attributed partly to the knowledge gap above, and partly to the difficulty of identifying the correct product substantiation in high-complexity domains: in consumer apps, the analogy is Instagram winning the photo app wave not through raw capability but through product judgment (the feed, the social layer). In robotics and biotech, the equivalent product judgment is harder to identify and therefore harder to fund.

---

## Capabilities in Focus

**Voice cloning.** Multiple companies possess voice cloning technology but have withheld it from aggressive deployment for one to two years due to regulatory and societal concerns about deepfakes. ElevenLabs has gained traction in this space. The hesitancy is not a capability limitation but a deliberate policy choice, making voice cloning one of the clearest examples of a capability that exists at production quality but is being gated by non-technical factors. See: [[themes/ai_business_and_economics|AI business and economics]].

**Video generation.** Progress from short clips with obvious artifacts to Pika and Sora-quality output has been rapid. However, the commercial viability of video generation requires solving deep product problems beyond raw generative quality: controllability, interface design, avatar manipulation (replacing speech while preserving gesture and motion), and length. These are described as unsolved and as constituting a genuinely hard product research challenge, not merely an engineering execution problem.

**Autonomous agents.** The Devin UI is highlighted as a meaningful paradigm shift: rather than black-box automation, it surfaces the agent's planning, execution, and code generation in real time, allowing users to observe and redirect. This human-in-the-loop transparency is identified as a prerequisite for user trust in autonomous operation. Most users do not want to wait passively while an agent operates; they want visibility and control.

**Foundation models in robotics and biotech.** Early results from applying foundation model approaches to robotics benchmarks are described as leading. In biotech, long context windows are enabling improvements in protein folding tasks. Both are flagged as research-stage, with significant unresolved questions about productization and data infrastructure.

---

## Limitations and Open Questions

The episode is unusually direct about what remains unsolved. The most significant limitations:

**Embodied data for robotics.** Internet and video data are insufficient for robotics. The core requirement is embodied action and controls data, which is expensive and slow to collect. Efficient real-world data collection is described as one of the central unsolved questions for robotics companies. The trajectory is unclear: this is not a problem that scales away with more compute.

**Enterprise adoption lag.** Consumer and prosumer AI adoption has significantly outpaced enterprise adoption. Canva's reported figures are cited: approximately $1 billion of its $1.7 billion ARR is prosumer. Enterprise sales cycles, security review processes, and organizational risk tolerance create a structural lag that cannot be bridged purely through capability improvement.

**Frontier compute requirements.** Even as Mosaic's Law drives down the cost of matching yesterday's frontier, reaching tomorrow's frontier still requires capital at a level that excludes most independent research teams. The next generation of frontier models likely requires sponsorship from hyperscalers or equivalently capitalized entities.

**Video controllability.** The set of capabilities required to make video generation commercially useful (controllability, length, interface design, avatar manipulation) constitutes a deep product problem that pure research advances have not yet addressed.

---

## Landscape Connections

- [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]]: Databricks and Mistral as case studies; Mosaic's Law as a structural claim
- [[themes/frontier_lab_competition|Frontier Lab Competition]]: self-reinforcing compute advantages at the frontier; oligopoly persistence
- [[themes/ai_market_dynamics|AI Market Dynamics]]: value capture shifting to clouds; hyperscaler funding dominance
- [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]]: mimetic investment patterns; cross-domain knowledge gaps
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]: time series as an underexplored vertical opportunity; enterprise vs prosumer dynamics

## Key Concepts

- [[entities/applied-intuition|Applied Intuition]]
- [[entities/devin|Devin]]
- [[entities/elevenlabs|ElevenLabs]]
- [[entities/foundation-model|Foundation Model]]
- [[entities/harvey|Harvey]]
- [[entities/heygen|HeyGen]]
- [[entities/mistral|Mistral]]
- [[entities/pika|Pika]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/sora|Sora]]
- [[entities/stargate|Stargate]]
