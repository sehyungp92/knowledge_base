---
type: entity
title: Outcome Reward Model (ORM)
entity_type: method
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00024907053631477823
staleness: 0.0
status: active
tags: []
---
# Outcome Reward Model (ORM)

> An Outcome Reward Model (ORM) is a reward modeling approach that evaluates only the final answer of a reasoning trajectory, assigning a scalar score based on whether the output is correct or not. As a method for guiding LLM reasoning, ORMs are foundational but increasingly understood to be insufficient for complex multi-step problems, where step-level credit assignment is necessary to reliably direct search and training.

**Type:** method
**Themes:** [[themes/chain_of_thought|Chain of Thought]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

An Outcome Reward Model evaluates a completed reasoning trajectory by inspecting only its final output, typically assigning +1 for a correct answer and -1 for an incorrect one. This is the simplest form of reward signal for [[themes/rl_for_llm_reasoning|RL-trained reasoning models]]: it requires only ground-truth answer verification and no annotation of intermediate steps. ORMs are cheap to train and easy to apply at inference time for best-of-N selection, making them the natural baseline against which more sophisticated reward approaches are measured.

The core limitation is sparse feedback. Because every intermediate reasoning step receives no direct signal, an ORM cannot distinguish a lucky correct answer reached via flawed reasoning from a correct answer reached via sound reasoning. In [[themes/search_and_tree_reasoning|tree-search settings]] like MCTS, this sparsity forces all credit to backpropagate from terminal nodes, which is workable but noisy, particularly for long or difficult problems where the search tree is deep and correct trajectories are rare.

## Empirical Standing Relative to Process Reward Models

Evidence from the rStar-Math system directly benchmarks ORMs against step-level alternatives and finds them consistently weaker on challenging mathematical reasoning tasks. The rStar-Math framework uses MCTS where terminal nodes are scored exactly as an ORM would score them: +1 for correct, -1 for incorrect, with Q-values of intermediate nodes updated by backpropagation from these terminal scores. This is already richer than a flat ORM applied post-hoc, yet even this configuration is outperformed by process-level approaches.

Specifically, the paper reports that both the Q-value-score-based PRM (PQM) and the Process Preference Model (PPM) outperform ORM by providing denser step-level reward signals, translating to higher accuracy on complex math tasks. The margin is not merely about richer signal in principle; it is large enough to change which base models can solve Olympiad-level problems at all. The PPM-augmented MCTS, which learns preferences between reasoning steps rather than scoring only final outputs, enables a 7B model to surpass GPT-4o on the MATH benchmark starting from training round 2 (86.6% vs. 76.6%), and ultimately brings Qwen2.5-Math-7B from 58.8% to 90.0%, surpassing o1-preview by 4.5%.

The efficiency argument is also decisive: the rStar-Math 7B PPM outperforms Qwen Best-of-N baselines that use a 10x larger 72B ORM across all benchmarks. This means the density of reward signal from a small process model dominates the raw capacity of a much larger outcome model. The implication for [[themes/test_time_compute_scaling|test-time compute scaling]] is that scaling search iterations is far more productive with a step-level verifier than with a final-answer verifier.

## Role in the rStar-Math Self-Evolution Pipeline

Within rStar-Math, ORM-style scoring is not discarded but is used structurally: it provides the ground signal that bootstraps process reward learning. Terminal MCTS nodes are labeled +1 or -1 based on correctness, and Q-values are backpropagated through the tree. These Q-values are then used not as direct training labels for a reward model (which would constitute a PRM trained on Q-values, the PQM variant), but as a ranking criterion to construct preference pairs of reasoning steps. The PPM is trained on these pairs with a pairwise ranking loss, which avoids the overconfidence and calibration issues of regressing directly on Q-value scalars.

This architecture reveals an important epistemic role for the ORM signal: it is the only supervision available when there is no human annotation of intermediate steps, and it can be leveraged indirectly to bootstrap richer process-level supervision. The four-round self-evolution loop that covers 90.25% of 747k math problems by round 4 depends entirely on this chain. Without the ORM-style terminal scoring, there is no Q-value signal, no preference pair construction, and no PPM to train.

Code-augmented chain-of-thought synthesis adds another filter: only reasoning steps paired with successfully executable Python code are retained, which provides an independent, execution-based correctness signal that complements the ORM terminal score and helps filter erroneous intermediate steps before they contaminate the training set.

## Limitations and Open Questions

The central limitation is structural: final-answer binary feedback cannot assign credit to the specific steps that caused a correct or incorrect outcome. For short problems this may be tolerable; for multi-step mathematical reasoning or long agentic tasks, it forces the search process to treat the trajectory as an indivisible unit. This makes exploration inefficient, since a nearly-correct trajectory that errs only on the last step receives the same -1 as a trajectory that fails immediately.

There are also training data efficiency concerns. ORMs require many trajectory samples to learn a useful signal from sparse supervision, while PRMs can provide useful gradients from a single trajectory containing multiple annotated steps. As the survey of RL for large reasoning models notes, the field has largely moved toward process-level methods for tasks where step quality is the bottleneck.

An underexplored question is whether ORM-style verification remains competitive in domains where step-level annotation is inherently ambiguous or expensive, but final answers are cleanly verifiable (e.g., formal theorem proving with a checker, code execution with test suites). In those settings, the ORM signal may be dense enough in practice to compensate for its theoretical sparsity, since every execution constitutes a verification event. Whether this changes the comparative picture against PRMs in non-mathematical domains is not yet settled.

## Relationships

The ORM stands in direct contrast to Process Reward Model (PRM) and the PPM variant developed in rStar-Math, both of which assign rewards at the step level. It is a component within [[themes/search_and_tree_reasoning|MCTS-based reasoning]] pipelines, where it provides terminal node scores. Its output feeds into [[themes/synthetic_data_generation|self-evolved training data generation]] when Q-values derived from ORM terminal labels are used to construct process preference pairs. The broader context of when ORM suffices versus when process rewards are necessary is central to [[themes/reward_modeling|reward modeling]] research and directly shapes practical choices in [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] systems.

## Key Findings

## Sources
