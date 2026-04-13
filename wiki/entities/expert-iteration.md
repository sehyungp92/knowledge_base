---
type: entity
title: Expert Iteration
entity_type: method
theme_ids:
- agent_systems
- chain_of_thought
- generative_media
- mathematical_and_formal_reasoning
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- test_time_compute_scaling
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0006763918585759787
staleness: 0.0
status: active
tags: []
---
# Expert Iteration

Expert Iteration (ExIt) is a training paradigm in which a model iteratively improves itself by learning from its own successful outputs — generating candidate solutions, filtering for those that succeed, and fine-tuning on the winners. Originally formulated as a marriage of Monte Carlo Tree Search with neural network policy learning, it has become a foundational motif in modern AI training pipelines, surfacing in game-playing systems from AlphaGo to AlphaZero and now driving state-of-the-art results in formal theorem proving. Its significance lies in demonstrating that superhuman performance need not require human-curated expertise: given a verifiable signal of success, a model can bootstrap itself beyond the frontier of human knowledge.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/generative_media|Generative Media]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/video_and_world_models|Video and World Models]]

---

## Overview

Expert Iteration formalises a loop: a policy proposes solutions, a verifier filters for correct ones, and the filtered solutions become training data that improve the next generation of the policy. The "expert" in the name is not a human — it is the search process itself. By treating the search as a planning expert and the neural network as the apprentice that distills what the expert discovers, the paradigm sidesteps the need for large corpora of human demonstrations. The key requirement is a reliable, cheap verifier: a win/loss oracle in games, a type-checker in formal mathematics, or a unit-test suite in code.

In the context of DeepSeek-Prover-V2, Expert Iteration is the engine of the curriculum learning stage for subgoal-based theorem proving. The model first attempts to decompose hard theorems into lemmas using a Monte Carlo Tree Search variant guided by a subgoal decomposition policy. Proofs that close successfully via Lean's type-checker are harvested and used to fine-tune the prover, which is then redeployed in the next round of search. This curriculum is designed to handle theorems whose full proofs are too long to discover in a single shot — the subgoal structure makes search tractable, and Expert Iteration makes the learned policy progressively more capable of proposing useful subgoals.

---

## Key Findings

### Origins in game-playing AI

The conceptual lineage of Expert Iteration runs through the AlphaGo family. AlphaGo itself was not a pure instance: its first training phase relied on supervised learning from human amateur games — imitation of human expert moves — before RL and MCTS were applied on top. The departure came with AlphaGo Zero, which eliminated human game data entirely, training from random play through self-play alone. AlphaGo Zero rediscovered all established Go theory autonomously, and Move 37 — an unconventional move that shocked professional players during the Lee Sedol match — is the canonical demonstration that self-play can transcend the frontier of human knowledge, not merely approach it.

AlphaZero then generalised this to chess, Go, and Shogi with a single algorithm and no game-specific knowledge, establishing Expert Iteration's domain-agnostic character. The pattern was clear: given a perfect simulator (the game engine) and a binary reward, iterative self-improvement reliably produces superhuman policies.

MuZero extended the approach to settings without a known simulator, learning a latent world model alongside the policy. This matters for the broader applicability of Expert Iteration: real-world domains rarely offer perfect environment simulators, and MuZero's design signals an awareness that the paradigm must eventually confront imperfect or absent verifiers.

### Transfer to formal mathematics

Formal theorem proving is the most direct current application of Expert Iteration to language models. The verifier — Lean's type-checker — is deterministic and cheap, making it an ideal oracle. DeepSeek-Prover-V2-671B achieves 88.9% pass ratio on MiniF2F-test at Pass@8192, improving to 82.4% at the more practically relevant Pass@32. On the harder PutnamBench, it solves 47 out of 658 problems — more than five times the next best model. On ProofNet-test, which covers college-level mathematics, it solves 37.1% of problems at Pass@1024.

These numbers are striking, but so are the gaps they reveal. On 15 AIME 2024–2025 problems from the newly introduced ProverBench, the model solves 6 in formal proof mode, while DeepSeek-V3 solves 8 using informal majority voting. The formal system's verification guarantee comes at the cost of expressivity and flexibility — informal reasoning with majority voting still outperforms verified proof search on competition mathematics at current scales. This is a meaningful limitation: Expert Iteration's power is bounded by what the search process can express within the chosen formal language.

### Relationship to test-time compute scaling

Expert Iteration is intimately linked to [[themes/test_time_compute_scaling|test-time compute scaling]]. The pass ratios quoted above improve substantially as compute budget increases — Pass@32 to Pass@8192 on MiniF2F is a 6.5 percentage point gain. This mirrors the training-time scaling curve: more compute produces better performance, whether that compute is spent on training rollouts or inference-time search. The implication is that Expert Iteration and test-time scaling are two faces of the same coin — models trained with Expert Iteration are precisely the models that benefit most from extended inference-time search, because the training loop itself was shaped by search.

Speculations on test-time scaling suggest the curve is consistent across hard reasoning tasks, and AlphaZero's self-play demonstrates the same pattern in games. The open question is whether this scaling is bounded — whether there are tasks where the search landscape is too rugged or the verifier too unreliable for iterative improvement to converge.

---

## Limitations and Open Questions

**Verifier dependency.** Expert Iteration requires a reliable success signal. In games and formal mathematics, this is binary and cheap. In open-ended domains — scientific hypothesis generation, strategic planning, creative writing — no such oracle exists. Extensions of the paradigm to these domains (e.g., using reward models or LLM judges as verifiers) reintroduce the brittleness that the formal verifier eliminates.

**Curriculum design.** The subgoal decomposition curriculum in DeepSeek-Prover-V2 is hand-designed to make hard theorems tractable. The degree to which Expert Iteration generalises without such scaffolding is unclear. AlphaZero required no curriculum in games because the rules define a natural difficulty gradient; theorem proving does not have this property.

**Informal vs. formal gap.** The AIME comparison (6 formal vs. 8 informal solutions) highlights that formal reasoning under Expert Iteration has not yet matched the flexibility of informal chain-of-thought reasoning. Closing this gap — either by improving search efficiency in formal systems or by learning better subgoal proposals — is an active frontier.

**Exploration collapse.** Self-play systems risk converging on a narrow region of the policy space, especially when rewards are sparse. AlphaGo Zero's diversity was sustained by MCTS's explicit exploration; language model equivalents must manage this through temperature, diversity penalties, or novelty bonuses.

---

## Relationships

Expert Iteration is the training-time counterpart to [[themes/search_and_tree_reasoning|search and tree reasoning]] at inference time — the two are deeply coupled in both the AlphaGo lineage and in DeepSeek-Prover-V2. It instantiates [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] in the specific case where the reward is binary and verifiable. The subgoal decomposition it trains is a form of [[themes/chain_of_thought|chain-of-thought]] reasoning made formal. Its scaling properties link it to [[themes/test_time_compute_scaling|test-time compute scaling]] and [[themes/scaling_laws|scaling laws]] more broadly.

Key sources: DeepSeek-Prover-V2, Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL, Speculations on Test-Time Scaling (o1).

## Sources
