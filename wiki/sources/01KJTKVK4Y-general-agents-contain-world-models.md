---
type: source
title: General agents contain world models
source_id: 01KJTKVK4Y2PFK1WTGG8AFGW50
source_type: paper
authors:
- Jonathan Richens
- David Abel
- Alexis Bellot
- Tom Everitt
published_at: '2025-06-02 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- generative_media
- interpretability
- mechanistic_interpretability
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# General agents contain world models

**Authors:** Jonathan Richens, David Abel, Alexis Bellot, Tom Everitt
**Published:** 2025-06-02 00:00:00
**Type:** paper

## Analysis

# General agents contain world models
2025-06-02 00:00:00 · paper · Jonathan Richens, David Abel, Alexis Bellot, Tom Everitt
https://arxiv.org/pdf/2506.01622

---

### Motivation & Prior Limitations
- The central open question in AI is whether world models are a necessary ingredient for flexible, goal-directed behaviour, or whether model-free learning can suffice as a shortcut to human-level AI.
  - The model-free paradigm, motivated by Brooks' "Intelligence without representation" (1991), aims to achieve general agents while side-stepping the challenges of learning explicit world models, and has produced capable agents (Reed et al., 2022; Brohan et al., 2023; Black et al., 2024).
  - Mounting evidence suggested model-free agents may implicitly learn world models and exhibit emergent planning, but no formal proof existed establishing whether this was necessary or coincidental.
- Safety and alignment proposals (Bengio et al., 2024; Dalrymple et al., 2024) require accurate predictive models of the agent-environment system, but faced the reasonable concern that model-free agent capabilities would outpace our ability to learn such models — including cases where agents already solve prediction tasks in domains humans cannot yet model (Abramson et al., 2024; Merchant et al., 2023).
- Existing theoretical accounts like the Good Regulator Theorem (Conant & Ross Ashby, 1970) attempted to establish that controllers must model their systems, but only showed that entropy-minimizing agents must have a deterministic policy — a much weaker and ambiguous result that does not demonstrate learning of environment dynamics.

---

### Proposed Approach
- The paper provides a formal proof that any agent satisfying a regret bound for a sufficiently diverse set of multi-step goal-directed tasks must have learned an accurate predictive model of its environment, encoded in its policy.
  - The framework models environments as controlled Markov processes (cMPs) and defines agents as goal-conditioned policies over composite goals expressed in Linear Temporal Logic (LTL), with goals structured as sequential sub-goals of varying depth n.
  - A "bounded goal-conditioned agent" (Definition 5) is defined by two parameters: a failure rate δ (lower bound on goal-achievement probability relative to optimal) and a maximum goal depth n; no rationality assumptions are imposed, only a competence bound.
- The proof proceeds by reduction: an algorithm (Algorithm 1) queries the agent's policy with carefully constructed either-or composite goals corresponding to binomial trials of specific transitions, exploiting the agent's goal-switching behaviour to estimate each transition probability ˆP_ss'(a) with bounded error.
  - The algorithm is universal (works for all agents satisfying Definition 5 and all environments satisfying Assumption 1), unsupervised (input is only the agent's policy, not its activations or architecture), and works even when agent weights are inaccessible.
  - This fills the third direction in the triad: planning uses (environment, goal) → policy; IRL uses (policy, environment) → goal; this work uses (policy, goal) → environment transition function, analogous to how IRL requires optimal policy across multiple environments to identify reward.
- Theorem 2 establishes a sharp boundary: for myopic agents (optimizing only immediate outcomes, n=1), no procedure can extract any non-trivial bound on transition probabilities from the policy, confirming that world models are necessary only for multi-step goal-directed behaviour.

---

### Results & Capabilities
- Theorem 1 gives quantitative error bounds: the extracted world model satisfies |ˆP_ss'(a) − P_ss'(a)| ≤ √(2P_ss'(a)(1−P_ss'(a)) / ((n−1)(1−δ))), scaling as O(δ/√n) + O(1/n) for δ ≪ 1, n ≫ 1.
  - World model accuracy increases strictly as the agent's performance improves (δ → 0) or as the maximum goal depth n increases; for any δ < 1, arbitrarily accurate models can be recovered with sufficiently large n.
  - Low-probability transitions have large relative error for any finite n and δ > 0, matching the intuition that sub-optimal or finite-horizon agents need only sparse world models covering common transitions.
- Experiments on a randomly generated 20-state, 5-action cMP confirm the theoretical scaling: mean world model error decreases as O(n^{-1/2}) with maximum goal depth, and decreases with agent training data (Nsamples from 500 to 10,000 trajectories).
  - Algorithm 2 recovers accurate transition functions even when the agent violates the regret bound assumption (achieving worst-case regret δ = 1 for some goals), with average error scaling similarly to the theoretical bound as long as average regret over goals remains low.
  - At Nsamples = 10,000 and goal depth 50, mean error reaches approximately 0.034 ± 0.002, demonstrating practical recovery in small environments.
- The paper establishes that domain generalization (adapting to new environments) requires strictly more knowledge than task generalization (generalizing to new goals): an optimal goal-conditioned agent needs only the transition function P_ss'(a), not the causal relations between concurrent environment variables, whereas causal world models are required for domain generalization (following Richens & Everitt, 2024).

---

### Implications
- For model-based RL and world models: the result removes the central motivation for model-free approaches by proving that world model learning cannot be avoided in any sufficiently general agent, directly motivating explicitly model-based architectures (LeCun, 2022; Hafner et al., 2023; Schrittwieser et al., 2020) that can directly attack model learning and exploit planning, sample efficiency, interpretability, and safety benefits.
- For mechanistic interpretability: the paper provides theoretical grounding for MI findings that model-free agents contain implicit world models, and offers a complementary method — recovering world models from agent behaviour (policy

## Key Claims

1. Any agent capable of generalizing to multi-step goal-directed tasks must have learned an accurate predictive model of its environment (a world model).
2. The world model of a general agent can be extracted from the agent's policy alone, without access to internal activations or architecture details.
3. Learning a general goal-conditioned policy is informationally equivalent to learning a world model.
4. There is no model-free shortcut to general AI: training an agent capable of generalizing to long horizon tasks cannot avoid learning a world model.
5. Myopic agents (those that only optimize for immediate outcomes, depth n=1) do NOT require world models; world models only become necessary for multi-step, sequential goal pursuit.
6. The accuracy of the world model extractable from an agent's policy increases as the agent's regret decreases (performance improves) and as the maximum goal depth n increases.
7. World model extraction error scales as O(n^{-1/2}) with goal depth n, both in theory and in experiments.
8. For long-horizon goals, even with a high failure rate, the agent must have learned a highly accurate world model because errors compound over time.
9. Sub-optimal or finite-horizon agents only need to learn relatively sparse world models covering common transitions; higher success rates or longer horizons require higher resolution world models.
10. The world model extraction algorithm (Algorithm 1) works by querying the agent's policy with carefully designed composite goals and observing the agent's first action choice, without requiring access 

## Capabilities

- Formal algorithm for extracting environment transition probabilities (a world model) from any goal-conditioned agent's policy, with error bounds that decrease as agent performance or goal depth increases
- Theoretical guarantee that any regret-bounded general agent implicitly encodes a recoverable world model, with error scaling as O(δ/√n) + O(1/n) where δ is failure rate and n is goal depth — proven architecture-agnostically
- World model extraction remains accurate even when agents violate worst-case regret bounds, as long as average regret across goals is low — relaxing the formal assumptions while preserving empirical utility

## Limitations

- Theorem only applies to fully observed (MDP) environments; what agents operating in partially observed environments (POMDPs) must learn about latent variables remains formally open
- Theoretical framework assumes finite, stationary, communicating Markov environments — assumptions almost universally violated in real-world agent deployments
- Extraction algorithms validated only on trivially small toy environments (20 states, 5 actions); zero evidence of scaling to real agents like LLMs, VLMs, or robotic policies
- No practical scalable algorithm proposed for extracting world models from deployed large neural agents — the theoretical guarantee does not yet translate into an actionable safety or interpretability tool
- Theorem proves existence of a world model in an agent's policy but cannot claim the agent uses it for planning — no epistemological claims about agent knowledge or subjective world model are licensed
- For any finite goal depth or non-zero failure rate, low-probability transitions may not be learned — agents can generalize with sparse world models that miss rare but potentially safety-critical transitions
- Realistic agents consistently violate worst-case regret bounds — achieving maximal regret (δ=1) on some goals even while performing well on average — meaning the formal theorem technically does not apply to them
- General AI capability is fundamentally bounded by the difficulty of accurately modeling open-ended real-world environments — a hard theoretical ceiling set by the curse of dimensionality, non-stationarity, and confounding
- Task generalization (the world model implicit in goal-directed behavior) does not require learning causal structure — causal knowledge requires the strictly harder problem of domain generalization, leaving implicit world models causally incomplete
- Algorithm requires querying agents with precisely structured LTL composite goals — not compatible with the natural language or standard API interfaces of deployed AI systems

## Bottlenecks

- No scalable practical algorithm exists for extracting world models from large neural agents — the theoretical guarantee of world model existence does not translate to a usable safety or interpretability tool for real LLMs, VLMs, or robotic policies
- The formal proof requires finite, fully observed, stationary, communicating environments — conditions not met by real-world AI deployments — blocking extension of world model necessity theorems to practical safety guarantees

## Breakthroughs

- Formal mathematical proof that any agent capable of generalizing to multi-step goal-directed tasks must contain an implicit world model extractable from its policy alone — settling the model-free vs model-based debate for general agents with theoretical finality

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/generative_media|generative_media]]
- [[themes/interpretability|interpretability]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/inverse-reinforcement-learning|Inverse Reinforcement Learning]]
- [[entities/world-model|World Model]]
- [[entities/sparse-autoencoder|sparse autoencoder]]
