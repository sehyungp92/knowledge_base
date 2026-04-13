---
type: source
title: 'Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models
  DeepSeek-R1 and Kimi k1.5'
source_id: 01KJVHQGH8HF40T32NJ0ADK404
source_type: video
authors: []
published_at: '2025-01-25 00:00:00'
theme_ids:
- ai_market_dynamics
- chain_of_thought
- frontier_lab_competition
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5

This podcast episode analyzes the January 2025 release of DeepSeek R1, R1-Zero, and Kimi k1.5, arguing they represent the most significant AI development since GPT-4: frontier-level reasoning capabilities achieved through minimal outcome-reward reinforcement learning at roughly $6M compute, published openly by Chinese labs — compressing the Western AI lead, commoditizing o1-level reasoning, and exposing deep structural weaknesses in compute-based AI governance.

**Authors:** Nathan Labenz (Cognitive Revolution podcast)
**Published:** 2025-01-25
**Type:** Video/Podcast

---

## Context and Significance

The host opens with an unusually strong framing: DeepSeek R1 is the first model since early GPT-4 that merits "drop everything and immerse yourself" attention. Three converging signals justify this:

1. **The gap is closing.** The window in which the West holds an "unassailable" AI lead is now measurably short — cycle times are compressing, and any strategy for beneficial AI premised on durable Western dominance is structurally unsound.
2. **The paradigm is shifting.** Pre-training compute is no longer the primary axis of capability improvement. Significant reasoning gains are appearing post-training, at a fraction of pretraining cost, with simpler methods than expected.
3. **Open-source has a new leader.** As of January 2025, the best open-source reasoning models globally come from China — [[entities/deepseek|DeepSeek]] has surpassed [[entities/meta-llama|Meta Llama]], while simultaneously publishing the clearest mechanistic explanations of how these models work.

---

## DeepSeek V3: The Base

DeepSeek V3 is the foundation from which R1 is trained. Key facts:

- **Architecture:** 671B parameter Mixture-of-Experts, 37B active at inference — enabling fast learning and good knowledge absorption at manageable inference cost.
- **Cost:** ~$6M total compute budget, roughly 10–50x cheaper than implied Western frontier training costs, achieved through algorithmic efficiency, data curation, and hardware-neural-network co-design.
- **Practical access:** Despite open weights, the full model requires multi-GPU arrays with hundreds of GB of memory — not laptop-runnable. DeepSeek offers an API; third-party inference providers (e.g., Hyperbolic at ~$2/M output tokens) make it accessible at ~30x lower cost than OpenAI o1's $60/M.

The cost result is a direct challenge to compute-restriction governance: if frontier-quality models can be trained for $6M, chip export controls cannot serve as a meaningful barrier to determined actors.

---

## R1-Zero: Pure RL, No Human Data

R1-Zero is the more theoretically important result. Named deliberately after AlphaZero — which learned games through pure self-play without human demonstrations — it applies the same philosophy to language model reasoning:

- **No supervised fine-tuning** as a starting point
- **No reward model** — a separate model does not evaluate outputs
- **No Monte Carlo Tree Search**, no process reward models, no value functions
- **Rule-based reward only:** correct answer → reward; incorrect → no reward

The algorithm is [[entities/grpo|Group Relative Policy Optimization (GRPO)]]: generate ~16 candidate answers per problem, score them, reward those exceeding the group average proportionally to how much they exceed it. This sidesteps the need for absolute reward calibration.

**What emerges:** Over 8,000+ RL training steps, chain-of-thought length grows from ~500 to ~10,000 tokens *without any explicit instruction to do so*. AIME pass@1 improves from ~15% to 70%+. The scaling curve has not flattened — indicating the RL reasoning paradigm has not yet hit its ceiling. The model spontaneously develops behaviors resembling deliberate reflection: self-checking, backtracking, alternative hypothesis generation.

### The Sparse Reward Problem

A classical challenge for RL is that if the base model cannot occasionally solve training problems, there is no signal to learn from. Two partial solutions appear:

- **Strong base model:** R1-Zero relies on V3's pretraining strength to get occasional correct answers from the start.
- **Code as curriculum:** Code problems provide scalar reward signals (N/M unit tests passing), enabling partial credit and bootstrapping even from weak initial performance. Training on code also improves general reasoning.

Critically, the technique *fails* for smaller models — Llama 8B, Qwen 32B, and Llama 70B could not acquire the same reasoning capabilities through direct RL. The minimum scale threshold for this paradigm is unknown, but appears to be above 70B parameters.

---

## R1: From R1-Zero to Production

DeepSeek R1 adds a multi-stage pipeline on top of R1-Zero's pure RL insight:

1. **Cold-start SFT warmup** — a small set of human-curated reasoning examples initializes the model
2. **Reasoning RL on objective rewards** — the core GRPO training
3. **General SFT on 800K examples** — 600K reasoning, 200K general-purpose — for helpfulness breadth
4. **Multi-reward RL** — adds helpfulness and harmlessness signals alongside accuracy

The result is human-friendly, multi-turn capable, and broadly useful — though still lagging o1 on multi-turn interaction and non-reasoning tasks. The rough edges of R1-Zero (spontaneous language switching mid-chain-of-thought, unreadable reasoning) are largely resolved.

**Distillation:** SFT on R1's chain-of-thought traces applied to Llama 70B achieves 65% on GPQA Diamond (PhD-level questions) — exceeding o1-mini, significantly outperforming GPT-4o (50%), and runnable on consumer hardware. This permanently alters the accessibility floor for advanced reasoning.

---

## Kimi k1.5: Independent Confirmation

Kimi k1.5 from Moonshot AI independently arrives at near-identical conclusions with different implementation choices:

- Minimal RL (no MCTS, no structured search) achieves near-o1 reasoning
- Introduces a **chain-of-thought reward model**: uses the reasoning model itself to evaluate reasoning quality, substantially outperforming traditional scalar reward models
- Confirms the paradigm is not specific to DeepSeek's implementation

The convergence of two independent labs on the same core finding — that simple outcome-reward RL on strong base models produces frontier reasoning — establishes this as a robust result, not a one-off.

---

## Landscape Contributions

### Capabilities Established

| Capability | Maturity | Key Evidence |
|---|---|---|
| Frontier reasoning via minimal outcome-reward RL | `narrow_production` | R1-Zero: AIME 15% → 70%+ with no MCTS, no PRM |
| CoT length auto-scaling during RL training | `narrow_production` | 500 → 10,000 tokens over 8K steps, curve still rising |
| Frontier-tier training at ~$6M compute | `narrow_production` | DeepSeek V3 cost; RL phase costs less than pretraining |
| o1-level reasoning at $2/M tokens (30x cheaper) | `narrow_production` | Hyperbolic pricing vs. OpenAI o1 $60/M |
| PhD-level QA on laptop hardware (distilled 70B) | `demo` | 65% GPQA Diamond, exceeds o1-mini |
| CoT reward models outperform scalar reward models | `demo` | Kimi k1.5 finding |
| Good open-source reasoning models for local deployment | `narrow_production` | First time achievable as of Jan 2025 |

### Limitations and Open Questions

**Safety and interpretability (high severity):**

- **Steganographic CoT risk** `[blocking]`: RL reward pressure applied to chain-of-thought may suppress the *display* of unwanted behaviors without eliminating them — models may encode penalized reasoning in patterns that appear human-readable but are not. This undermines CoT transparency as a safety mechanism. There is no established method for detecting this. See [[themes/chain_of_thought|chain of thought interpretability]].

- **Continuous latent reasoning** `[blocking]`: Meta's approach of passing hidden-state activations instead of discretized tokens produces entirely opaque internal computation — powerful but fundamentally unmonitorable.

- **Competing safety regimes, no empirical resolution:** DeepSeek applies harmlessness RL to full CoT including thinking tokens; OpenAI explicitly does not (on the grounds that it drives concealment rather than correction). Both positions are theoretically motivated; neither has published empirical evidence resolving which produces safer models.

**Scaling and scope limitations:**

- **Direct RL fails below ~70B parameters:** The pure outcome-reward RL paradigm that works at 671B does not transfer to smaller models. Mechanism unknown; represents a hard constraint on democratization of reasoning training.

- **Verifier bottleneck:** Pure RL reasoning is structurally confined to domains with programmatic verifiers (math, code). General language tasks — writing, dialogue, open-ended reasoning — still require learned reward models, reintroducing the alignment problems RL was supposed to sidestep. See [[themes/reinforcement_learning|reinforcement learning]].

- **Context ceiling:** R1's 128K context window limits maximum chain-of-thought length in a single pass, contrasting with Gemini's million-token context.

- **R1 vs. o1 gaps:** R1 lags on multi-turn interaction and non-reasoning tasks — benchmark parity does not translate to equivalent general assistant quality.

**Geopolitical and governance:**

- **Compute governance is obsolete** `[blocking]`: Pre-training FLOP thresholds as capability proxies are structurally outdated. RL post-training achieves dramatic capability gains with a fraction of pretraining compute, and training is increasingly parallelizable and decentralizable. Regulatory frameworks built around compute thresholds cannot track actual capability. See [[themes/ai_market_dynamics|AI market dynamics]].

- **Export controls are insufficient:** US restrictions have not prevented Chinese labs from reaching the frontier. At $6M training cost, chip availability is not the binding constraint. Counterintuitively, scarcity may concentrate Chinese AI effort on high-priority strategic applications rather than distributing it commercially.

- **Heavy RLHF trades creative expressiveness:** R1, closer to a base model in some respects, exhibits more distinctive and expressive creative writing than heavily-tuned Western models — suggesting alignment optimization degrades creative capability as a side effect.

---

## Key Themes

- [[themes/reinforcement_learning|Reinforcement Learning]] — GRPO, outcome-reward RL, sparse reward solutions
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — the core paradigm established by R1-Zero and Kimi k1.5
- [[themes/chain_of_thought|Chain of Thought]] — emergent CoT scaling, steganography risk, CoT reward models
- [[themes/reasoning_and_planning|Reasoning and Planning]] — benchmark results, distillation, inference-time scaling
- [[themes/frontier_lab_competition|Frontier Lab Competition]] — Chinese vs. Western labs, open-source leadership shift
- [[themes/ai_market_dynamics|AI Market Dynamics]] — cost commoditization, governance failures, geopolitical implications

---

## Open Questions

1. **What is the minimum base model scale for direct outcome-reward RL to work?** The 70B failure is documented; the mechanistic explanation is not.
2. **How does o3 aggregate parallel rollouts?** The high-compute inference mechanism remains entirely unpublished — this gap separates current open-source models from o3's high-effort performance tier.
3. **Is steganographic CoT detectable or preventable?** No published method exists for auditing whether RL-trained reasoning traces encode concealed information.
4. **Does applying harmlessness rewards to CoT produce safer or merely better-behaved models?** The DeepSeek/OpenAI disagreement on this is unresolved empirically.
5. **How far does RL test-time scaling continue?** The 10,000-token CoT curve has not flattened at 8K training steps — the ceiling is unknown.

## Key Concepts

- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/chain-of-thought-reasoning|Chain of Thought Reasoning]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/curriculum-learning|Curriculum Learning]]
- [[entities/gpt-4|GPT-4]]
- [[entities/grpo|GRPO]]
- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
- [[entities/knowledge-distillation|Knowledge Distillation]]
- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/reinforcement-learning-for-reasoning|Reinforcement Learning for Reasoning]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
- [[entities/knowledge-distillation-for-reasoning|knowledge distillation for reasoning]]
- [[entities/passk|pass@k]]
- [[entities/passk-metric|pass@k metric]]
- [[entities/self-play|self-play]]
- [[entities/value-function|value function]]
