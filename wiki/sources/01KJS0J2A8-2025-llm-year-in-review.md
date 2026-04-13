---
type: source
title: 2025 LLM Year in Review
source_id: 01KJS0J2A8PVG73TJQY37AQKXH
source_type: article
authors: []
published_at: '2025-12-19 00:00:00'
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# 2025 LLM Year in Review

**Authors:** 
**Published:** 2025-12-19 00:00:00
**Type:** article

## Analysis

# 2025 LLM Year in Review
2025-12-19 · article
https://karpathy.bearblog.dev/year-in-review-2025/

---

## Briefing

**2025 was defined by six paradigm shifts in LLMs: RLVR displaced pretraining as the primary capability lever (introducing test-time compute as a new scaling axis), LLM intelligence revealed itself to be fundamentally alien and jagged rather than human-like, and the application layer crystallized into a distinct product category (Cursor, Claude Code) while vibe coding began to terraform software production itself. The single most important implication: the industry has realized less than 10% of LLM potential at current capability levels, and the field is conceptually wide open.**

### Key Takeaways
1. **RLVR is the new pretraining** — Training against verifiable rewards produced most of 2025's capability gains, consuming compute originally destined for pretraining and yielding similar-sized models with dramatically longer RL runs.
2. **Test-time compute is a new scaling axis** — RLVR unlocked a knob and associated scaling law where capability increases with longer reasoning traces at inference time, not just model size or training FLOPs.
3. **LLMs are "ghosts, not animals"** — They are fundamentally different entities from humans: optimized for imitating text and collecting puzzle rewards, not jungle survival, making animal/human analogies actively misleading.
4. **Intelligence is jagged, and benchmarks are broken** — LLMs spike in verifiable domains via RLVR, making benchmarks unreliable; "benchmaxxing" (growing jaggies to cover test sets) is now a recognized lab practice.
5. **The LLM app layer is thick and real** — Cursor demonstrated a distinct product category: context engineering + multi-call DAG orchestration + application-specific GUI + autonomy slider, for specific verticals.
6. **Claude Code defined the local agent paradigm** — The key insight is not cloud vs. local compute but access to an already-running computer's context, secrets, and low-latency environment; Anthropic got this right, OpenAI didn't.
7. **Vibe coding makes code free and ephemeral** — Building software through English and discarding it after single use is now practical; this democratizes programming and enables professionals to produce software that would otherwise never exist.
8. **Regular people benefit more from LLMs than professionals** — Unlike all prior technology, LLMs invert the diffusion curve; vibe coding is a concrete instance of this power redistribution.
9. **The LLM GUI revolution is coming** — Text chat is the 1980s console; Gemini Nano banana hints at visual/spatial output (images, infographics, animations) as the next interface paradigm.
10. **The industry has realized under 10% of LLM potential** — Even at current capability, the application surface is vastly underexplored; the author holds rapid continued progress and substantial remaining work as simultaneously true.

---

### RLVR: The New Dominant Training Stage

- The pre-2025 production LLM recipe was stable and three-stage: pretraining (GPT-2/3 era, ~2020), supervised fine-tuning (InstructGPT, ~2022), and RLHF (~2022).
  - This recipe was proven but limited: SFT and RLHF are computationally thin — minor finetunes that cannot optimize deeply because human reward signals are gameable and sparse.
- **RLVR adds a fourth stage** by training against automatically verifiable, objective reward functions (math correctness, code test passage) that cannot be gamed.
  - This allows substantially longer optimization runs without reward hacking, unlocking a regime that SFT and RLHF could not reach.
  - The DeepSeek R1 paper is cited as the key reference for the emergent reasoning behaviors this produces.
- **Reasoning strategies emerge spontaneously** — LLMs learn to decompose problems into intermediate calculations and develop backtracking/recovery strategies.
  - These strategies would have been "very difficult to achieve in the previous paradigms because it's not clear what the optimal reasoning traces and recoveries look like for the LLM — it has to find what works for it."
- **RLVR offers high capability-per-dollar**, diverting compute from pretraining budgets into RL runs.
  - Result: 2025 saw similar-sized models but dramatically longer RL training — capability progress came from exhausting the RLVR overhang, not from scaling model size.
- **Test-time compute scaling is RLVR's unique new knob** — a scaling law linking capability to inference-time compute via longer reasoning traces ("thinking time").
  - OpenAI o1 (late 2024) was the proof of concept; **o3 (early 2025) was the inflection point where the qualitative difference became intuitively obvious**.

---

### Jagged Intelligence and the Death of Benchmarks

- 2025 is when the author (and the broader industry) internalized the "shape" of LLM intelligence — not a smooth curve but deeply jagged.
  - In verifiable domains where RLVR applies, LLMs spike to genius-polymath performance; in adjacent unverifiable domains they can fail at grade-school tasks.
  - The visual framing: "they are at the same time a genius polymath and a confused and cognitively challenged grade schooler, seconds away from getting tricked by a jailbreak."
- **The "ghosts vs. animals" reframe** is the author's preferred conceptual anchor for this phenomenon.
  - Human neural nets are optimized for tribal jungle survival; LLM neural nets are optimized for text imitation, math-puzzle reward collection, and LM Arena upvotes.
  - These are fundamentally different optimization pressures producing fundamentally different intelligence shapes — the animal/human lens is not just imprecise but actively misleading.
- **Benchmarks are now epistemically compromised** because they are, by construction, verifiable environments.
  - RLVR and synthetic data generation can be targeted at benchmark-adjacent embedding space pockets — "growing jaggies to cover them."
  - "Training on the test set is a new art form" — benchma

## Key Claims

1. Reinforcement Learning from Verifiable Rewards (RLVR) emerged as the de facto new major stage in LLM training in 2025, added on top of the existing pretraining, SFT, and RLHF pipeline.
2. RLVR causes LLMs to spontaneously develop reasoning strategies such as breaking problems into intermediate calculations and backtracking, which could not be achieved through SFT or RLHF.
3. RLVR allows significantly longer optimization runs than SFT or RLHF because it trains against objective, non-gameable reward functions.
4. RLVR offers high capability per dollar and diverted compute originally intended for pretraining, making longer RL runs the dominant source of capability progress in 2025.
5. RLVR introduced test-time compute scaling as a new knob for capability, allowing models to generate longer reasoning traces and increase 'thinking time'.
6. OpenAI o1 (late 2024) was the first RLVR model, but o3 (early 2025) was the intuitive inflection point where the difference was clearly felt.
7. LLM intelligence is fundamentally different from human or animal intelligence — it is best conceptualized as 'summoning ghosts' rather than growing animals, because the architecture, training data, al
8. LLMs display jagged performance characteristics — simultaneously performing at genius-polymath level in some domains and at confused grade-schooler level in others, often seconds away from being jailb
9. Benchmarks are unreliable for measuring general LLM capability because they are verifiable environments susceptible to RLVR and synthetic data generation, a process called 'benchmaxxing'.
10. Cursor revealed a distinct new layer of LLM applications that bundle and orchestrate LLM calls for specific verticals, doing context engineering, multi-call DAG orchestration, application-specific GUI

## Capabilities

- RLVR as the de facto new canonical training stage: LLMs trained against automatically verifiable rewards spontaneously develop structured problem-solving and recovery strategies, with o3 as the clear inflection point
- Test-time compute as a continuous capability scaling knob — generating longer reasoning traces and increasing thinking time yields measurable capability improvements governed by an associated scaling law
- Vibe coding: building functional, non-trivial software from English descriptions alone without explicitly writing or understanding code — including custom domain-specific tools in systems languages like Rust
- LLM apps as a distinct orchestration layer: bundling multiple LLM calls into domain-specific DAGs with context engineering, application-specific GUIs, and tunable autonomy sliders (Cursor-style)
- Local AI agent paradigm: AI agents running on the developer's own computer with full access to private environment, data, secrets, and configuration — enabling low-latency, context-rich agentic workflows
- Integrated multimodal generation combining text generation, image generation, and world knowledge in a single model — enabling LLM-native visual outputs (infographics, slides, whiteboards) as early GUI-style AI interface

## Limitations

- Benchmarks are structurally compromised as progress metrics: any verifiable benchmark environment is immediately susceptible to targeted capability spiking via RLVR and synthetic data generation adjacent to the benchmark's embedding space
- LLMs exhibit inherently jagged intelligence: simultaneous expert-level performance in verifiable domains and trivial, unpredictable failures in adjacent areas — the profile is structurally different from human intelligence
- RLVR capability gains are confined to verifiable domains (math, code puzzles): open-ended language, creative tasks, and unstructured agentic behaviors cannot benefit from the same extended RL optimization due to absence of objective rewards
- LLMs remain easily jailbroken despite frontier reasoning capabilities — adversarial prompt robustness is not addressed by RLVR training and constitutes a persistent, unresolved security vulnerability
- Benchmark saturation does not imply AGI progress: maximal benchmark performance through targeted training does not generalize to broadly capable intelligence — the metric and the target have decoupled
- RLVR diverted compute from pretraining: capability progress in 2025 came from longer RL runs on similar-sized models rather than model scale increases — implying the pretraining scaling overhang was not compounded
- Text-chat interaction paradigm is misaligned with human cognitive preferences: people process information better visually and spatially, making the dominant LLM interface suboptimal for broad adoption
- Cloud-first agent deployment is architecturally inferior for current jagged capability era: lacks access to developer's existing environment, private data, secrets, configuration, and low-latency interaction that make agents effective
- Human analytical frameworks for understanding intelligence (animal/growth metaphors) systematically mischaracterize LLM failure modes and capabilities, leading to poor predictions and evaluation design

## Bottlenecks

- RLVR-induced benchmark contamination: the same optimization mechanism driving capability improvements renders all verifiable benchmarks structurally untrustworthy as general capability measures — progress measurement is fundamentally broken
- RLVR applicability confined to verifiable domains: the extended RL optimization that drives capability gains cannot be applied to open-ended language, creative tasks, or unstructured agentic behaviors due to absence of objective reward signals
- Absence of LLM-native GUI paradigm: text-chat is a console-era interaction model mismatched with human visual/spatial cognitive preferences, blocking mainstream non-technical adoption and high-bandwidth human-AI collaboration

## Breakthroughs

- RLVR established as the canonical new LLM training stage: LLMs self-discover effective reasoning strategies through extended optimization against verifiable rewards — o3 (early 2025) marked the obvious inflection point where capabilities were intuitively different
- Vibe coding crossed a practical threshold: AI can now build functional, non-trivial software (including custom systems-language tools) from English alone, making programming accessible to non-programmers and making code effectively free and disposable
- Claude Code established a new local-first AI agent paradigm: AI living on the developer's computer as a persistent, context-rich agent rather than a stateless cloud service — a genuinely new interaction model distinct from 'AI as website'

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/claude-code|Claude Code]]
- [[entities/context-engineering|Context Engineering]]
- [[entities/cursor|Cursor]]
- [[entities/jagged-intelligence|Jagged Intelligence]]
- [[entities/openai-o3|OpenAI o3]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-verifiable-rewards|Reinforcement Learning from Verifiable Rewards]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/vibe-coding|Vibe Coding]]
