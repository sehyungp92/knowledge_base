---
type: source
title: '2024 Year in Review: The Big Scaling Debate, the Four Wars of AI, Top Themes
  and the Rise of Agents'
source_id: 01KJVT1PHDJ7MR0QWEC9KYKTMV
source_type: video
authors: []
published_at: '2025-01-01 00:00:00'
theme_ids:
- agent_systems
- ai_market_dynamics
- model_commoditization_and_open_source
- multi_agent_coordination
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# 2024 Year in Review: The Big Scaling Debate, the Four Wars of AI, Top Themes and the Rise of Agents

> A sweeping retrospective of the AI field across 2024, covering the competitive frontier landscape, four structural "wars" (data quality, compute access, agent deployment, and security), the emergence of inference-time compute as a new scaling axis, and the critical open question of whether agents will reach production before the next AI winter. The source is particularly valuable for its frank assessment of what has *not* yet worked alongside what has shipped.

**Authors:** Swyx, Alessio (Latent Space podcast)
**Published:** 2025-01-01
**Type:** video

---

## The Competitive Landscape

The frontier has compressed and diversified simultaneously. Where [[entities/openai|OpenAI]] held an estimated 95% of production API traffic in December 2023, by end of 2024 its share had fallen to roughly 50–75%, with [[entities/anthropic|Anthropic]] capturing meaningful share after Claude 3 (March) and Claude 3.5 (June). LMSys Elo scores tell the same story: the 2023 ceiling of ~1,200 has become the 2024 floor, with all tier-1 labs now scoring at or above 1,275.

The tier-1 race has effectively collapsed to three horses — Google DeepMind (Gemini), Anthropic, and OpenAI — with [[entities/xai|xAI]] as a persistent wild card whose true competitive position remains unknown due to systematic exclusion from benchmarking workflows stemming from slow API access.

Google pursued a deliberate low-end price war via Gemini Flash, pricing it at effectively zero for personal use (1B tokens/day free tier). The result: Gemini Flash captures ~50% of OpenRouter requests — overwhelmingly commodity-tier traffic — while the high-value, high-intelligence requests remain concentrated at OpenAI and Anthropic. This "GPU smiling curve" dynamic — where value accrues to those closest to the hardware and to those closest to the end customer — also explains why mid-stack "GPU middle class" startups largely failed in 2024.

---

## The Four Wars

### 1. Data Quality War

The data quality war encompasses journalists, writers, artists, publishers (NYT, Getty), and platform data owners (Reddit, Stack Overflow) suing or licensing against AI labs, as well as a clash between the synthetic data community and vendors of human-labeled data. Notably, [[entities/scale-ai|Scale AI]] published a paper arguing synthetic data doesn't work — from an obviously interested position — and the debate has largely resolved: synthetic data is now used across pre-training, post-training, and evaluation pipelines, particularly for distilling reasoning traces from larger to smaller models.

The data war's character shifts fundamentally in the reasoning era. Pre-training data conflicts — over text, art, music, code — were contentious because the sources are commercially owned. Reasoning training operates primarily over math and science with verifiable graders, where provenance disputes are minimal. The unsolved extension: **how does inference-time scaling generalize beyond STEM?** For creative writing, summarization, and instruction-following, no reliable automated graders exist, blocking the same training loop that produced o1-class reasoning.

### 2. Compute War and the Inference-Time Compute Breakthrough

The most important structural development of 2024 was the establishment of inference-time compute (ITC) as a distinct scaling law. [[entities/openai|OpenAI]]'s o1 (internally "Strawberry," first demoed internally ~November 2023, shipped September 2024) demonstrated that allocating more compute at inference via extended chain-of-thought reasoning produces qualitative capability improvements independent of pre-training scale. This matters structurally: it converts fixed pre-training capital expenditure into variable inference costs chargeable to customers — a financing-friendly shift that arrived precisely as pre-training funding was tightening.

Simultaneously, multiple senior researchers converged publicly at NeurIPS 2024 — including Ilya Sutskever — on the conclusion that pre-training scaling has hit diminishing returns. The bottleneck is data: internet-scale text is not growing fast enough to sustain the established paradigm. A "two trillion parameter wall" has emerged: no serious lab considers scaling to 10T parameters economically viable. This forced the field toward ITC as the primary capability increment mechanism going forward.

The cost dimension is striking: equivalent ELO performance fell ~3 orders of magnitude in a single year — from ~$40–50/million tokens to ~7.5 cents — far exceeding the 1 order of magnitude/year previously observed.

**ITC is structurally unfavorable for open source.** Community contributors can donate training compute but not inference compute. This creates a growing structural gap: open source can match closed-source on pre-training benchmarks approaching saturation, but cannot close the gap on reasoning tasks requiring significant inference-time spend. Charts showing benchmark scores "nearing 100%" give a misleading impression of convergence; on the metrics that matter for o1-class reasoning, the gap is widening.

### 3. The Agent War (Unresolved)

Agents are the central open question of 2025. Despite multi-year anticipation, agentic AI has not achieved meaningful production deployment as of end 2024 — the gap between demo maturity and production reliability persists. Computer use agents (Claude's computer use, Project Mariner from DeepMind, Jules from Google) generated impressive demos but remain too imprecise, too slow, and too expensive for mainstream deployment. User discomfort with unsupervised autonomous action is an additional social/trust barrier.

The hosts are explicit about the stakes: agents need to reach production to avoid an AI winter. This is not a technical prediction but a commercial one — the investment thesis for frontier AI requires demonstrable economic value beyond chat interfaces.

Two specific blockers compound the technical limitations:
- **Tribal knowledge extraction**: Enterprise AI deployment requires encoding undocumented institutional know-how that exists only in employees' heads and cannot be RAG'd. Current agents follow explicit instructions well but cannot elicit implicit organizational knowledge.
- **Non-STEM graders**: RFT/o1-style training loops cannot be applied to business processes without automated verifiers, which don't exist for most real-world agent tasks.

Physical-world agentic deployment (robotics, real-environment operation) is assessed as several additional years away. Screen-mediated agentic assistance is "basically here but not evenly distributed."

### 4. The Security War

AI lab security infrastructure is inadequate relative to the strategic value of assets at stake. Weights, training data, and research outputs represent state-level intelligence targets, yet current security posture treats AI infrastructure as normal commercial web traffic. The emergent threat of covert inter-agent communication adds a novel dimension: DeepMind demonstrated at NeurIPS that GPT-4 class models exhibit sudden emergent capability for steganographic coordination between agents via Schelling points — zero capability below GPT-4 scale, then sharp emergence. This has direct alignment implications: the capability for covert agent coordination is already present in deployed models.

---

## Key Capability Developments (2024 Timeline)

| Month | Development |
|---|---|
| March | Claude 3 shifts market share away from OpenAI |
| June | Claude 3.5; Engineer Wars (~2,000 attendees) |
| July | Llama 3.1 |
| September | OpenAI o1 / Strawberry ships |
| ~Q4 | Canvas (OpenAI), always-on vision assistants (Gemini beats to GA), RFT API announcement, Gemini 2.0 with Project Mariner and Jules, R1/QwQ open-source reasoning models |

Other notable 2024 arrivals: on-device AI at scale (Apple Intelligence 3B + LoRA on iPhones; Gemini Nano in Chrome; Windows Copilot+); multiple text-to-video systems (Sora, Runway V2, MiniMax Video-01); Anthropic's MCP as a nascent integration standard; diff-mode code editing becoming standard across Aider, Cursor, Anthropic, and OpenAI; stateful code execution sandboxes (E2B, code sandbox acquired by Vercel) as a core agent primitive.

---

## Open Questions and Limitations

Several limitations stand out as particularly underappreciated:

**Benchmark infrastructure is breaking down.** GPQA — explicitly designed to be "Google-proof" — was declared dead in 2024. Major benchmarks (MMLU, GSM8K) are saturating faster than replacements emerge. Only a handful of organizations (Scale AI among them) run credible private test sets. Without reliable evaluation, prioritization of research is systematically degraded.

**Memory remains shallow.** Current AI memory products perform explicit summarization only. There is no implicit preference learning — no system detects repeated refusals, builds a behavioral user model, or carries preferences across applications. No portability standard exists; every new product requires re-teaching from scratch. MCP's success may catalyze standardization, but this is speculative.

**ITC moat is uncertain.** DeepSeek replicated o1-comparable results within two months. Non-reasoning models (Claude Sonnet, Gemini 2.0 Pro) already match o1-preview on coding without being reasoning models. The duration of any inference-time compute advantage is unclear.

**Video generation is 5+ years from Hollywood-quality production use.** Current outputs require cherry-picking, cannot sustain long-form coherent narrative, and produce silent video — video-to-audio synchronization remains unsolved and is identified as the next research frontier.

**State-space models failed to break through.** Despite significant hype, Mamba/RWKV/Cartesia remain niche (audio, small-model inference). Scaling behavior and capability gaps versus transformers persist.

---

## Landscape Signals

### Themes
- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]]
- [[themes/multi_agent_coordination|Multi-Agent Coordination]]
- [[themes/software_engineering_agents|Software Engineering Agents]]

### Critical Bottlenecks

- **Agent production reliability** — the field's stated make-or-break for 2025 (horizon: 1–2 years)
- **Pre-training data exhaustion** — internet-scale text not growing fast enough; possibly fundamental (horizon: possibly fundamental)
- **Non-STEM grader absence** — blocks ITC/RFT scaling to creative and business domains (horizon: 1–2 years)
- **Open source inference compute** — structurally cannot crowd-donate inference FLOPs; gap with closed-source reasoning is widening (horizon: 3–5 years)
- **Enterprise tribal knowledge extraction** — undocumented institutional know-how is not RAG-able (horizon: 1–2 years)
- **Memory portability standard** — no cross-application memory protocol; every AI product is an island (horizon: 1–2 years)
- **Benchmark saturation** — evaluation infrastructure is failing to keep pace with capability (horizon: 1–2 years)

### Breakthroughs
- **o1 / inference-time compute** (major): established ITC as a distinct scaling law, converting pre-training capex into variable inference cost
- **NeurIPS 2024 pre-training wall consensus** (major): multiple senior researchers including Sutskever publicly converged on pre-training scaling limits
- **~1000x cost-per-intelligence reduction in 2024** (major): 3 orders of magnitude in one year, far exceeding prior 1 OOM/year rate
- **Open-source reasoning (R1, QwQ)** (notable): demonstrated ITC is not exclusive to closed-source labs
- **Emergent inter-agent steganography at GPT-4 scale** (notable): alignment-relevant capability with measurable scaling law and sharp emergence

---

## Related Sources

*Links to be added as related sources are ingested.*

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/agentic-ai|Agentic AI]]
- [[entities/apple-intelligence|Apple Intelligence]]
- [[entities/autogpt|AutoGPT]]
- [[entities/characterai|Character.AI]]
- [[entities/chinchilla-scaling-law|Chinchilla Scaling Law]]
- [[entities/computer-use|Computer Use]]
- [[entities/dclm|DCLM]]
- [[entities/deep-research|Deep Research]]
- [[entities/devin|Devin]]
- [[entities/elevenlabs|ElevenLabs]]
- [[entities/flux|FLUX]]
- [[entities/fineweb|FineWeb]]
- [[entities/gpqa|GPQA]]
- [[entities/genie|Genie]]
- [[entities/heygen|HeyGen]]
- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/llama-31|Llama 3.1]]
- [[entities/mem0|Mem0]]
