---
type: entity
title: System 2 Reasoning
entity_type: theory
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- model_architecture
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- reward_modeling
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0003565294070638128
staleness: 0.0
status: active
tags: []
---
# System 2 Reasoning

> Borrowed from Daniel Kahneman's dual-process theory, System 2 Reasoning in AI refers to the deliberate, slower mode of inference in which a model does not simply generate a single response but instead searches over a space of possible reasoning steps, evaluating candidates with a reward model before committing to an answer. Where System 1 corresponds to fast, single-pass generation, System 2 introduces a policy-plus-verifier architecture at test time, fundamentally shifting where computation is spent and what kind of performance is achievable.

**Type:** theory
**Themes:** [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/representation_learning|Representation Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Overview

System 2 Reasoning operationalizes the intuition that reasoning quality can be improved by spending more computation at inference time rather than solely at training time. The canonical instantiation couples a policy model (which generates candidate reasoning steps) with a process reward model (which scores intermediate steps rather than only final answers). A search procedure, typically Monte Carlo Tree Search (MCTS), explores the space of step sequences, backpropagating terminal scores to guide the search toward high-quality trajectories.

The appeal of this paradigm is architectural: it offers a path to strong reasoning without necessarily scaling the base model, because the reward model and search procedure can compensate for a weaker policy. The practical question is whether small models can bootstrap both the policy and the verifier from scratch, without distilling from a frontier model that already exhibits System 2 behavior.

---

## Key Findings

### Self-Evolution as the Core Mechanism

The rStar-Math paper presents the most detailed empirical account of System 2 reasoning in small models. The central contribution is a four-round self-evolution loop in which the policy model and the Process Preference Model (PPM) are trained jointly and iteratively. In each round, MCTS generates new reasoning trajectories; the PPM scores those trajectories; the higher-quality data re-trains the policy; and a stronger PPM is trained on the updated Q-values. After four rounds, 90.25% of 747k math problems are successfully incorporated into the training set, with Olympiad-level coverage rising from 56.04% to 62.16% between rounds 2 and 3 alone.

This iterative structure is significant because it avoids the bootstrapping problem that plagues naive self-training: early-round data is noisy, but the PPM provides a signal dense enough (step-level rather than answer-level) to filter erroneous trajectories before they corrupt the policy.

### The Process Preference Model

The PPM is the architectural novelty that makes System 2 reasoning tractable at this scale. Rather than using Q-values directly as scalar reward labels (which would require calibrated magnitudes), the PPM is trained on preference pairs derived from MCTS Q-values, using pairwise ranking loss. Terminal nodes are scored +1 for correct answers and -1 for incorrect ones, with intermediate node values updated via standard backpropagation. The PPM head replaces the next-token prediction head with a scalar linear layer followed by tanh, constraining outputs to [-1, 1] and is initialized from the fine-tuned policy model.

Ablations show that the PPM outperforms both outcome reward models (ORM) and a Q-value-score-based process reward model (PQM) across all challenging benchmarks. The ORM underperforms because it provides only a single terminal signal; PQM underperforms relative to PPM likely because raw Q-values are noisy labels compared to the relative ordering captured by preference pairs.

### Verified Trajectories as Training Data

A key methodological finding is that the type of synthetic data matters as much as the quantity. Code-augmented chain-of-thought synthesis filters out any step where the accompanying Python code does not execute successfully, ensuring that intermediate reasoning steps are grounded in computational verification rather than plausible-sounding text. Fine-tuning on step-by-step verified trajectories substantially outperforms GPT-4 distillation approaches (NuminaMath-CoT, MetaMath) and rejection sampling, even though the latter two use data from a much larger model.

### Performance: Small Models at Frontier Level

The headline results challenge the assumption that frontier-level math reasoning requires frontier-scale models. Qwen2.5-Math-7B improves from 58.8% to 90.0% on MATH, surpassing o1-preview by 4.5 percentage points. Phi3-mini-3.8B improves from 41.4% to 86.4%. On AIME 2024 (a genuinely hard olympiad benchmark), rStar-Math solves an average of 53.3% (8 out of 15 problems), placing it among the top 20% of high school math competitors nationally. The 7B PPM also outperforms Qwen Best-of-N baselines that use a 10x larger 72B reward model, suggesting that process-level verification is a more efficient use of parameters than scaling the verifier alone.

Self-evolution compounds: starting from round 2, the 7B model with MCTS already surpasses GPT-4o on MATH (86.6% vs 76.6%), and further rounds continue to improve performance.

---

## Limitations and Open Questions

The empirical case for System 2 reasoning is almost entirely in mathematical and formal domains. Math has an unambiguous verifier: the answer is correct or it is not. This makes terminal scoring trivial and Q-value backpropagation well-defined. It is not clear how this framework generalizes to open-ended reasoning, coding tasks with partial credit, or any domain where correctness cannot be determined programmatically.

The compute overhead at inference time is substantial. MCTS with a PPM is orders of magnitude more expensive per query than single-pass generation. This cost may be acceptable in research contexts or high-stakes queries, but it limits deployment at scale unless future work dramatically reduces the search budget without sacrificing quality.

There is also a question of what System 2 reasoning actually learns. The rStar-Math self-evolution loop generates increasingly high-quality trajectories, but it is trained on a fixed distribution of math problems (747k problems drawn from existing benchmarks). Whether the resulting policy generalizes to genuinely novel problem types, or whether it is primarily learning to navigate the solution structures common in benchmark training sets, is not tested.

System 2 Reasoning Capabilities Are Nigh and François Chollet on OpenAI o-models and ARC raise a harder challenge: benchmark saturation may be masking a lack of genuine reasoning generalization. High scores on MATH and AIME are striking, but these benchmarks are well-represented in pretraining and fine-tuning corpora. The ARC-AGI challenge, designed specifically to resist memorization, remains much harder for System 2 approaches than for humans, suggesting the gap between search-augmented pattern matching and genuine novel reasoning has not closed.

Finally, the PPM's dependence on a policy model for initialization means the quality of the verifier is upper-bounded by the quality of the policy at each round. This circular dependency may limit how far self-evolution can proceed without an external signal injection.

---

## Relationships

System 2 Reasoning is the conceptual parent of [[themes/test_time_compute_scaling|test-time compute scaling]], which treats inference-time search as a first-class design variable alongside training compute. It is operationalized through [[themes/search_and_tree_reasoning|MCTS and tree search]], evaluated via [[themes/reward_modeling|process reward models]], and trained using [[themes/synthetic_data_generation|synthetic verified trajectories]]. The [[themes/chain_of_thought|chain-of-thought]] literature provides the step-level decomposition that makes MCTS applicable to language generation. The [[themes/post_training_methods|post-training]] loop (self-evolution) connects it to [[themes/reinforcement_learning|RL-style iterative improvement]], though without an explicit reward signal beyond answer correctness.

## Sources
