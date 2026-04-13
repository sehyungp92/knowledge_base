---
type: entity
title: NuminaMATH
entity_type: dataset
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00013930410811023266
staleness: 0.0
status: active
tags: []
---
# NuminaMATH

NuminaMATH is a large-scale mathematical problem dataset primarily used as the supervised fine-tuning (SFT) warm-up corpus in large reasoning model (LRM) training pipelines. Its significance lies not in any algorithmic novelty of its own, but in its role as the empirical baseline against which more sophisticated training data strategies are measured: work such as rStar-Math and Meta Reinforcement Fine-Tuning consistently uses NuminaMATH-derived training as the starting condition, making it the de facto reference point for evaluating self-evolved and process-reward-augmented data generation.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

NuminaMATH is a curated collection of mathematical problems spanning competition-level difficulty, used specifically to initialize policy models before iterative self-improvement begins. Its companion derivative, NuminaMATH-CoT, extends the raw problem set with chain-of-thought annotations generated via GPT-4 distillation, which represents a standard but increasingly outdated approach to producing reasoning traces for SFT.

The dataset's scope encompasses problems up to Olympiad level, providing the 747k-problem corpus that rStar-Math's four-round self-evolution pipeline draws from. Of those, only 90.25% are successfully covered by round 4, with Olympiad-level problems proving persistently harder to synthesize verified trajectories for (56.04% coverage before PPM-augmented MCTS, rising to 62.16% after).

## Key Findings

### As a Baseline Condition for Self-Evolution

NuminaMATH occupies the starting point of the rStar-Math pipeline. Before any self-evolved data exists, the policy model is warm-started with SFT on NuminaMATH problems, giving it the minimal mathematical competence needed to generate plausible reasoning traces that MCTS can then search over. This initialization role is load-bearing: without a reasonably capable starting policy, MCTS would fail to generate any usable rollouts.

The dataset's scale (747k problems) and difficulty distribution are what enable the multi-round self-evolution to accumulate meaningful signal. Round 1 can only generate trajectories for a subset of problems; subsequent rounds, with stronger PPMs providing denser process-level reward signals, expand coverage progressively. By round 2, the 7B rStar-Math model already surpasses GPT-4o on the MATH benchmark (86.6% vs 76.6%), a threshold crossed before the full problem corpus is covered.

### NuminaMATH-CoT as a Superseded Baseline

NuminaMATH-CoT, the GPT-4-distilled chain-of-thought variant, is explicitly outperformed by step-by-step verified trajectories generated through PPM-augmented MCTS. The comparison is instructive: distillation from a stronger model produces fluent but unverified reasoning steps, whereas MCTS with process preference rewards filters out erroneous intermediate steps and retains only trajectories with confirmed terminal correctness. Code-augmented CoT synthesis further tightens this filter by discarding any step whose associated Python code fails to execute, eliminating an additional class of plausible-sounding but incorrect reasoning.

The gap between NuminaMATH-CoT and rStar-Math's self-evolved data is not marginal. This suggests that the bottleneck in mathematical SFT is not the problem distribution or quantity (which NuminaMATH provides adequately) but the quality and verifiability of the reasoning traces used for training.

### Process Reward Signal and Coverage Limits

A persistent open question concerns Olympiad-level coverage. Even with PPM-augmented MCTS in round 3, coverage of the hardest problems reaches only 62.16%, leaving roughly a third of the most challenging problems without verified training trajectories. This ceiling reflects the fundamental difficulty that even a strong process preference model cannot reliably distinguish correct from incorrect reasoning at the frontier of mathematical difficulty, and that MCTS rollouts from a 7B model may simply not produce correct terminal answers for the hardest problems often enough to generate useful preference pairs.

The PPM itself is trained on Q-value-derived preference pairs (pairwise ranking loss rather than direct Q-value regression), initialized from the fine-tuned policy with a tanh-constrained scalar head. This design choice avoids the instability of regressing directly onto noisy Monte Carlo Q-values, but it means the PPM's quality is bounded by the quality of MCTS rollouts in the previous round, creating a chicken-and-egg dependency that the iterative self-evolution loop is designed to unwind gradually.

### Relationship to Test-Time Compute Scaling

Beyond the training pipeline, NuminaMATH problems serve as the evaluation substrate for test-time compute scaling experiments. The progress dense reward framing in Meta Reinforcement Fine-Tuning quantifies reward as the change in likelihood of eventual success for each reasoning block, a signal that can only be meaningfully calibrated against a problem set with known correct answers. NuminaMATH's competition-grade problems, where correctness is unambiguous, make it suitable for this kind of process-level reward evaluation.

## Limitations and Open Questions

The dataset's primary limitation as a training corpus is that it cannot generate its own verification signal. Problem correctness is known, but reasoning-step correctness is not, which is precisely why process reward models and code execution verification are necessary additions. NuminaMATH provides the problems; the hard work of deciding which reasoning trajectories are worth learning from happens entirely outside the dataset.

Coverage gaps at Olympiad difficulty remain unresolved. Whether additional self-evolution rounds would close this gap, or whether a fundamentally different search strategy is required, is an open empirical question. The 10% of problems that remain uncovered after four rounds may represent a structural limit of MCTS with current 7B policy models, or simply a matter of more compute.

It is also worth noting that NuminaMATH's problem distribution skews toward formal competition mathematics. Whether models trained primarily on this corpus generalize to informal mathematical reasoning in applied domains is underexplored in the literature citing it.

## Related Sources

- rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking
- Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning
- Mitigating Overthinking through Reasoning Shaping

## Relationships

## Sources
