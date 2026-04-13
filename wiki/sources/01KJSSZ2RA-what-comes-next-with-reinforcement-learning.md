---
type: source
title: What comes next with reinforcement learning
source_id: 01KJSSZ2RA0ANWBV2BZQM3N605
source_type: article
authors: []
published_at: '2025-06-09 00:00:00'
theme_ids:
- pretraining_and_scaling
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# What comes next with reinforcement learning

**Authors:** 
**Published:** 2025-06-09 00:00:00
**Type:** article

## Analysis

# What comes next with reinforcement learning
2025-06-09 · article
https://www.interconnects.ai/p/what-comes-next-with-reinforcement

---

## Briefing

**The next phase of RL scaling splits into three distinct paths — extending current RLVR techniques, pushing into sparser reward domains, and true continual learning — and the author argues these paths differ dramatically in their feasibility and timeline.** Scaling existing RLVR is happening now and will yield more frequent model releases; sparser domain RL faces deep algorithmic barriers comparable to unsolved robotics problems; true continual learning is both technically far off and potentially undesirable given alignment risks. The core thesis is that practitioners must resist conflating these three very different frontiers.

### Key Takeaways
1. **Three RL frontiers are not equivalent** — Scaling existing RLVR, tackling sparser rewards, and continual learning are fundamentally different in difficulty and timeline, and conflating them produces misleading optimism.
2. **Current RLVR scaling path is clear but bounded** — Extending math/code-style verifiable reward training to more domains and data is ongoing and predictable; it does not require algorithmic breakthroughs.
3. **Deep Research doesn't do long-horizon RL** — OpenAI trained Deep Research on individual browser/tool-use sub-tasks, not end-to-end sparse trajectories; the long-horizon behavior emerges from prompting, not credit assignment.
4. **Sparse credit assignment is the hardest open problem** — Attributing learning signal across 1M–100M token episodes to per-token updates creates extreme overoptimization risk, with no proven solution at language model scale.
5. **Sparser domain RL resembles unsolved robotics RL** — End-to-end RL is not state-of-the-art in robotics; pushing LMs into similarly sparse, real-world feedback domains risks hitting the same wall.
6. **Off-policy RL at scale requires replay-buffer-like stability** — As episode completion times become variable across parallel environments, policy gradient algorithms must tolerate training on significantly stale rollouts.
7. **Pretraining frequency will fall, RL run length will rise** — The post-training phase becomes the dominant development axis; intermediate RL checkpoints can be safety-tuned and shipped, making releases feel continuous.
8. **True continual learning is an unpredictable algorithmic leap** — Unlike inference-time scaling (a 10–100× amplification of chain-of-thought), continual learning from experience requires an unexpected scientific breakthrough, not a scaling law.
9. **Continual learning at frontier scale poses serious alignment risk** — A powerful model with a rapid, personalized feedback loop to a corporate training pipeline creates a "destiny to dystopia" dynamic the author explicitly does not want enabled at scale.
10. **Memory-based personalization is the safer alternative** — Context-window memory of past interactions approximates continual learning benefits without updating weights, breaking the most dangerous feedback loop.
11. **Human preference remains the dominant reward signal for long-horizon tasks** — For tasks like code refactoring or deep research where multiple valid outputs exist, human taste is unavoidably the terminal reward, not verifiable metrics.
12. **Parallelism is prerequisite for sparse RL — and breaks down in real domains** — Current RLVR success depends on showing models many similar problems many times in parallel; real-world scientific or robotics tasks cannot be parallelized the same way.

---

### The Three-Way Taxonomy of RL Progress

- Scaling current RLVR is the near-term, ongoing path, involving more data and more domains with existing verifiable reward infrastructure, no algorithmic novelty required.
  - Current training generates 10K–100K tokens per answer; this path extends those techniques, not the next leap to 1M–100M token episodes.
  - This is a continuation of the "deep learning works, keep pushing" paradigm applied to post-training.

- Pushing RL to sparser domains targets tasks with multi-hour or multi-day feedback loops — scientific experiments, robotics, complex software engineering.
  - **This is the most contested frontier**: the author falls "slightly on the side of pessimism" due to structural similarity to robotics RL, where end-to-end RL is not state-of-the-art.
  - As existing RLVR domains saturate, labs will naturally redirect research effort here, but difficulty compounds sharply.

- True continual learning — models updating parameters from real-world interaction experience — is ARC Prize's framing of intelligence as "skill acquisition efficiency."
  - Dwarkesh Patel frames this as the crucial missing ingredient for human-like intellectual adaptability.
  - **This requires an unpredictable algorithmic breakthrough**, not scaling of existing methods.

- The three paths are not a progression; they are parallel bets with very different probability distributions and timelines.

---

### What's Actually Happening in Long-Horizon RL (Deep Research Case Study)

- OpenAI described Deep Research as trained "using the same reinforcement learning methods behind o1" on "real-world tasks requiring browser and Python tool use."
  - **The key read**: training targets individual sub-tasks within a trajectory, not the sparse terminal outcome of the full trajectory.
  - Long-horizon behavior is assembled at inference via prompting and extended inference, not learned end-to-end via credit assignment.

- This same interpretation applies to Claude Code and Codex-style agents — RL makes individual tool-use and coding steps more robust, not the aggregate multi-day project outcome.
  - **The final reward signal for long-horizon tasks is closer to human preferences than verifiable outcomes**, because multiple valid solutions exist and human taste is the discriminator.

- OpenAI's early o1 development involved manually curated optimal trajectories — the Q* rumor per

## Key Claims

1. Current RLVR training generates 10K-100K tokens per answer for math or code problems during training.
2. Next-generation RL training problems are expected to require 1M-100M tokens per answer, involving multiple inference calls, prompts, and environment interactions within a single episode.
3. RL will not autonomously enable end-to-end training of language models to make entire codebases more efficient, run real-world scientific experiments, or generate complex strategies without major disc
4. Scaling RL for current language models implies scaling techniques similar to current models, not unlocking complex new domains.
5. Very-long-episode RL is deeply connected with the concept of continual learning, where language models improve through real-world interaction.
6. Longer RL training runs will result in more frequent model releases, as intermediate RL checkpoints can have safety post-training applied and be shipped to users.
7. Previously, pretraining needed to finish before post-training could begin, making final model performance hard to predict; iterative RL-based releases will change this paradigm.
8. True continual learning—where a model updates its parameters based on experienced failures—would require an algorithmic innovation far less predictable than inference-time scaling.
9. The inference-time scaling paradigm shift was achieved by scaling Chain-of-Thought prompting 10-100X rather than introducing a fundamentally new method.
10. RL is better suited to multi-datacenter training than pretraining because policy gradient updates do not need to communicate as frequently as next-token prediction updates.

## Capabilities

- RLVR training on math and code reasoning tasks routinely generates 10K–100K tokens per answer during training, representing the current operational scale of inference-time search in post-training
- Long-horizon agent behavior (Deep Research, coding agents) assembled by training component sub-tasks with RL and composing them at inference time via prompting — not end-to-end sparse RL
- Iterative model releases enabled by taking intermediate RL training checkpoints, applying preference and safety post-training, and shipping — making pretraining completion no longer a prerequisite for release
- RL training infrastructure can support multiple parallel GPU clusters for acting, generation, and learning — structurally better suited to multi-datacenter deployment than pretraining's constant next-token-prediction gradient communication

## Limitations

- End-to-end RL training on truly long-horizon tasks (1M–100M token episodes involving multiple tool calls and environment interactions) is not currently achievable — the infrastructure and algorithmic requirements do not yet exist
- Sparse reward domains are not yet producing training results — labs do not know how to set up reward signals that cause models to meaningfully improve on long multi-step tasks
- Deep Research and comparable long-horizon agents do not use sparse credit assignment — their long-horizon behaviour is a prompting-time composition of component capabilities, not a trained end-to-end policy; labs' descriptions conspicuously avoid claiming otherwise
- As reward sparsity increases, overoptimisation risk intensifies — the optimizer can credit-assign over many more intermediate tokens in undetectable adversarial ways to achieve a distant reward signal
- True continual learning — models that update their weights from real-world interaction experiences the way humans learn from feedback — is not achievable with any current or near-term method and requires an unpredictable algorithmic breakthrough
- Harder real-world RL tasks cannot be parallelised or repeated at the scale required by RL training — the massive-parallelism and multiple-attempts conditions that made math/code RLVR work do not transfer to scientific, robotics, or open-ended tasks
- Long-horizon agentic task quality is measured by human preference, not verifiable reward — Deep Research performance cannot be evaluated with ground-truth signals, making RLVR inapplicable as the primary training driver for these tasks
- Off-policy and multi-datacenter RL training for variable-duration long-horizon episodes is not yet operational — algorithms are not stable when learning from batches of rollouts arriving asynchronously from multiple environments at highly variable latencies
- Manually curated expert trajectories may provide a warm-start for complex RL tasks but whether they are sufficient to bootstrap large-scale RL training that produces durable capability gains is unknown
- Frontier AI inference is supply-constrained, not demand-constrained — capacity limits, not market saturation, are the binding constraint on revenue and usage growth at leading labs
- Maximum-capability (Ultra-tier) models are economically unservable at scale — their inference latency and cost force labs to serve the next-generation Pro-tier model instead, leaving top-of-capability-curve performance inaccessible to most users
- End-to-end RL on complete complex trajectories (entire codebases, multi-day scientific experiments) produces qualitatively different and much harder problems than current domain-specific RLVR — scaling existing techniques is insufficient

## Bottlenecks

- Sparse credit assignment at episode lengths of 1M–100M tokens: attributing outcome-level rewards back to individual token decisions across full long-horizon multi-step episodes is algorithmically unsolved at this scale
- Off-policy stability for highly variable episode durations: RL training algorithms are not stable when learning from asynchronously arriving rollouts with wildly different completion times across a multi-datacenter actor pool
- Absence of verifiable reward signals for long-horizon open-ended tasks: complex research, creative, and multi-solution engineering tasks have no ground-truth checkable outcome, forcing reliance on expensive human preference signals that cannot scale to RL training loops
- Simulation and parallelism requirements incompatible with real-world complex tasks: RL training at the scale required for hard domains depends on massively parallel simulators that cannot be constructed for unique, non-repeatable real-world events
- Continual learning algorithmic barrier: no known training paradigm enables safe, stable weight updates for frontier-scale models from heterogeneous real-world interaction feedback; this requires an unpredictable scientific breakthrough rather than engineering scale-up

## Themes

- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/deep-research|Deep Research]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/replay-buffer|Replay Buffer]]
- [[entities/continual-learning|continual learning]]
