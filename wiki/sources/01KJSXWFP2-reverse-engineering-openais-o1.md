---
type: source
title: Reverse engineering OpenAI’s o1
source_id: 01KJSXWFP2NBXQ0AZRVD5FFTZG
source_type: article
authors: []
published_at: '2024-09-16 00:00:00'
theme_ids:
- ai_market_dynamics
- frontier_lab_competition
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reverse engineering OpenAI’s o1

**Authors:** 
**Published:** 2024-09-16 00:00:00
**Type:** article

## Analysis

# Reverse engineering OpenAI's o1
2024-09-16 · article
https://www.interconnects.ai/p/reverse-engineering-openai-o1

---

## Briefing

**o1 is the first production deployment of language model search — a system trained with large-scale RL to generate and self-evaluate reasoning trajectories at inference time, revealing new inference scaling laws that are orthogonal to pretraining compute. This matters because it proves a second axis of capability scaling exists, shifts compute spend from training to inference, and makes the current capability overhang deeper without triggering a market correction — a paradigm shift more comparable to GPT-3 than ChatGPT.**

### Key Takeaways
1. **Inference scaling laws are real and distinct from training scaling laws** — o1's performance improves log-linearly with both train-time RL compute and test-time thinking compute, confirmed by OpenAI's own benchmark plots showing a continuous performance dial.
2. **Exploration is the missing ingredient in open-source RL reproductions** — Models like Reflection 70B are just GPT-4o with special prompting tokens; true o1-style gains require genuine RL exploration into novel state spaces, which no open model has achieved.
3. **o1 is likely one model acting as both generator and process reward model** — Rather than a modular multi-model pipeline, the architecture appears to be a single model with interleaved scoring tokens or a regression head, handling candidate generation and step-rating simultaneously.
4. **The released o1-preview is significantly scaled down from the full o1** — AIME benchmark scores and the training/inference compute plots reveal that users are accessing a middle-tier configuration, not the top-performing system OpenAI has internally.
5. **Per-step process reward models (PRMs) are the reward signal backbone** — Credit assignment across long reasoning chains requires rating each reasoning step, not just the final answer; OpenAI's "Let's Verify Step By Step" paper is the technical foundation.
6. **Forward-only generation is a practical engineering constraint that shaped the architecture** — Backtracking in a KV-cache system is hard to serve at scale; the system generates rambling forward trajectories rather than true tree search with backtracking, mapping more cleanly to agent-environment RL frameworks.
7. **Parallel candidate generation at each reasoning step explains the pricing anomaly** — The high cost of o1 is not from a larger model but from generating multiple candidate steps and scoring them before proceeding, requiring a fundamentally different inference stack.
8. **Reproducing o1 open-source requires solving several orthogonal hard problems simultaneously** — State space formulation, diversity of reasoning steps, strong PRMs, harder evaluations, and compute for online RL training must all be solved; none exist in the open ecosystem yet.
9. **OpenAI seeded training with expensive human-annotated forward reasoning paths** — High-skill annotators likely created complex, multi-path reasoning trajectories over a year before release; contrastive examples were probably also needed, making reasoning trace copying insufficient.
10. **o1 is explicitly not product-market fit yet** — Boris Power (OpenAI applied research lead) compared it to GPT-3, not ChatGPT: a new paradigm requiring users to define the use cases, with a "ChatGPT moment" still ahead.
11. **The ratio of post-training compute to pretraining compute is increasing structurally** — o1-style completions can be 10–1000x more expensive than standard LM completions, and RL requires hundreds of thousands of such samples, creating a compute barrier only a few players can clear.
12. **Closed-loop self-correction is o1's most consequential behavioral property** — Without a grading heuristic at each step, LMs cannot recover from errors; PRMs in the loop give o1 the same error-correction dynamic that made AlphaGo's MCTS powerful.

---

### o1 as a System: Architecture and Identity

- **o1 is best understood as a system, not a model**, even though OpenAI officially describes it as "one model" in developer AMAs — the funneling and recycling of computations to create coherent outputs is described as "far closer to closed-loop control than anything we have seen in the language modeling space."
  - The lineage runs from Q* (tree-of-reasoning search for high-value trajectories) → Strawberry (a model trained with Q* that reasons as it generates) → o1 (the deployed system built on top).
  - The "one model" framing may be technically accurate at inference time while obscuring that training used multiple models as heuristics and that the architecture embeds scoring behavior inside generation.
- **The model is GPT-4o scale or potentially smaller**, not a larger model — high inference costs are not explained by model size but by the generation strategy.
  - The pricing ($15/M input tokens, $60/M output tokens) matches Claude 3 Opus and applies to intermediate reasoning tokens not shown to users.
  - If the model were simply bigger, the compute allocation would look different; the anomaly points to parallel decoding as the cost driver.
- **OpenAI is not exposing the reasoning trace to users** and has sent cease-and-desist emails to users attempting to jailbreak it out — the trace is a strategic secret because streaming it would reveal the non-autoregressive generation process.
  - Normal streaming doesn't work when each step requires parallel candidate consideration before proceeding.

---

### The RL Training Process

- **Large-scale RL with exploration is the core technical breakthrough**, not prompt engineering or chain-of-thought fine-tuning — "Our large-scale reinforcement learning algorithm teaches the model how to think productively using its chain of thought in a highly data-efficient training process."
  - Performance improves consistently with more RL compute (train-time) and more thinking time (test-time), two independent scaling axes.
  - The constr

## Key Claims

1. o1 is trained on long reasoning chains with reinforcement learning and deployed as an online search system
2. o1's deployment confirms the existence of inference scaling laws, where spending more on inference yields better performance
3. o1 performance consistently improves with both more RL training compute and more test-time thinking compute
4. The scaling constraints for o1's RL-based approach differ substantially from those of LLM pretraining
5. The released o1 preview is a substantially scaled-down version of the full o1 system, positioned between GPT-4o and full o1 on benchmarks
6. Traditional RLHF assigns a single binary preference reward to the entire trajectory, making it hard to identify where reasoning went wrong
7. Process reward models (PRMs) rate each individual step in a reasoning chain, enabling per-step credit assignment
8. Exploration is the critical ingredient for continued improvement in RL-trained language models; without it, more RL training leads to overfitting or performance collapse
9. o1's RL state space complexity is unmatched by any previous real-world RL success, operating on reasoning chains of 100,000 to 200,000 tokens
10. Proximal Policy Optimization (PPO) has been the most successful RL algorithm for deployment on language models

## Capabilities

- Large-scale RL-trained language model search system deployed commercially, performing online test-time search over reasoning trajectories in production
- Inference scaling laws confirmed in production: o1 performance improves consistently with more test-time compute, establishing a new scaling axis independent of pretraining
- RL exploration enabling language models to discover qualitatively new reasoning trajectories beyond their pretraining distribution — producing backtracking, self-questioning, and error-correction patterns
- Single generative model acting as both generator and process reward model, rating candidate reasoning steps before proceeding — enabling parallel/branching decoding at inference
- Process reward models (PRMs) providing per-step credit assignment in reasoning RL training, rating each step in a reasoning tree to overcome sparse-reward problems

## Limitations

- o1 is drastically inefficient for simple queries — consumes ~10x more tokens than necessary (225 tokens for problems solvable in 10-12), with no mechanism to detect query difficulty
- Parallel/branching decoding is fundamentally incompatible with streaming output — real-time token streaming is impossible for o1-class reasoning models
- o1 inference is prohibitively expensive — $15/M input and $60/M output tokens including hidden reasoning tokens — with costs applying to intermediate steps the user never sees
- OpenAI cannot serve the strongest o1 configuration to users — the deployed preview model sits substantially below the fully-trained model in benchmark scores
- o1 shows only comparable performance to Claude 3.5 Sonnet on ARC-AGI and aider coding benchmarks — reasoning gains are not uniform and fail to generalise across all domains
- o1-style RL training accessible only to a handful of labs — generating training trajectories costs 10-1000x more than standard RLHF, with hundreds of thousands of samples needed
- Without genuine RL exploration (not prompt-based imitation), training levels off or collapses — all current open-source 'reasoning' models use special prompting, not exploration
- Hierarchical RL — needed to handle reasoning chains of 100-200k tokens with temporal abstraction — has not been successfully applied in any noteworthy real-world deployment
- Value functions learned during o1 RL training are not interpretable — their relationship to final model behaviour is opaque, making it impossible to understand how the model is learning
- OpenAI hides reasoning traces from users and sends cease-and-desist to those extracting them — fundamental opacity about what the model is reasoning through
- Open-source reproduction of o1 is blocked simultaneously by missing seed trajectories, process reward models, exploration training, and compute — all required together
- o1 lacks clear product-market fit — even OpenAI does not know the right use cases, and slow feedback cycles make it unsuitable for general assistant use without automatic routing
- Training compute threshold-based AI regulation (e.g. SB 1047) is already outdated — inference-time compute scaling means capability cannot be assessed from training FLOPs alone

## Bottlenecks

- RL exploration in language model state spaces — getting models to genuinely discover new reasoning trajectories (not just imitate reasoning patterns) is unsolved outside top-tier labs
- Extreme per-trajectory compute cost of generating o1-style RL training data — 10-1000x more expensive than RLHF trajectories, requiring hundreds of thousands of samples, concentrating this capability in a handful of labs
- Expert-annotated seed trajectories required to bootstrap o1-style RL training — high-skill human annotations of complex multi-path reasoning cannot be sourced from public datasets
- Inference infrastructure for parallel/branching decoding does not yet exist at scale — existing forward-only autoregressive serving stacks are incompatible with o1-style generation, blocking cost-competitive deployment

## Breakthroughs

- First large-scale commercial deployment of RL-trained language model search system (o1), confirming inference-time compute scaling laws and establishing a second scaling axis beyond pretraining
- Successful application of full-state RL with genuine exploration to language models, producing qualitatively different reasoning behaviour (backtracking, self-correction, wandering) not achievable through prompting or SFT

## Themes

- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/arc-agi|ARC-AGI]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
- [[entities/o1|o1]]
- [[entities/test-time-compute|test-time compute]]
