---
type: entity
title: Self-Taught Reasoner (STaR)
entity_type: method
theme_ids:
- alignment_and_safety
- alignment_methods
- chain_of_thought
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
influence_score: 0.0008841168925436058
staleness: 0.0
status: active
tags: []
---
# Self-Taught Reasoner (STaR)

> Self-Taught Reasoner (STaR) is an expert iteration technique in which a language model generates solution trajectories, filters them to those containing correct answers, and finetunes on the successful subset iteratively until convergence. Originally a method for bootstrapping reasoning chains, it has been adapted to improve search-based models and reward modelling, making it a key primitive in post-training pipelines that push language models toward stronger reasoning through self-generated signal.

**Type:** method
**Themes:** [[themes/alignment_and_safety|Alignment and Safety]], [[themes/alignment_methods|Alignment Methods]], [[themes/chain_of_thought|Chain of Thought]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

STaR operates on a deceptively simple premise: rather than requiring human-curated reasoning traces, let the model generate its own, keep the ones that work, and train on those. Each iteration sharpens the model's ability to produce correct trajectories, enabling gradual self-improvement without external supervision at each step.

The method has proven useful far beyond its original context. In Stream of Search (SoS): Learning to Search in Language, STaR is applied to SoS models trained to emit explicit search trajectories through problem spaces. After policy improvement with STaR combined with APA (Advantage-weighted Policy Adjustment), the finetuned SoS models solve 36% of problems previously unsolved by any symbolic search strategy. This is a meaningful result: the model is not just recovering known solutions more efficiently, it is reaching territory previously unreachable by any heuristic. The broader SoS pretraining approach (training on full search trajectories rather than only optimal paths) increases search accuracy by approximately 25 percentage points over models trained solely on optimal trajectories, and the SoS model achieves 51.27% accuracy on held-out inputs compared to 25.73% for the optimal-path baseline despite training on fewer "correct" examples in the traditional sense.

In Generative Reward Models, STaR is applied to preference modelling under two variants: STaR-SFT (standard supervised finetuning on correct preference judgements) and STaR-DPO (trained with direct preference optimisation). The results split sharply by task type. STaR-SFT achieves only 67.4% in-distribution accuracy, essentially no improvement over the base LLM, suggesting that filtering and finetuning on correct preference traces alone is insufficient when the base model is already near the in-distribution ceiling. STaR-DPO, however, exhibits a striking strength on safety evaluation: 91.0% accuracy on the Safety category, compared to 81.8% for PairRM. This suggests that reasoning-based finetuning is particularly well-suited to domains requiring nuanced comparative judgment rather than surface-level pattern matching.

## Relationship to Generative Reward Models

The Generative Reward Models paper frames STaR as one component within a richer architecture. GenRM replaces the Bradley-Terry reward modelling objective with a more general preference modelling framework that does not assume a pointwise reward estimate or a special model architecture. GenRM achieves in-distribution accuracy comparable to Bradley-Terry models while outperforming them on out-of-distribution tasks by 10-45%, and surpasses LLM-as-a-judge baselines on both in-distribution (by 9-31%) and out-of-distribution tasks (by 2-6%). Chain-of-thought prompting alone boosts zero-shot LLM evaluator performance substantially: from 52.25% to 67.75% on UltraFeedback and from 60.60% to 75.18% on RewardBench. Majority voting at 32 samples adds further consistent gains of 1.6-4.9% depending on benchmark.

STaR's contribution within this ecosystem is enabling the reward model itself to reason, not just score. The STaR-DPO results indicate that when the reasoning process is shaped by preference signal (rather than just correctness signal), the model develops qualitatively better evaluative capability, particularly on safety-critical comparisons.

## Limitations and Open Questions

Several constraints limit confidence in STaR's generality. The SoS application is restricted to the Countdown game; while Countdown has a high branching factor and variable goal states that capture meaningful search complexity, the step to more complex real-world tasks remains undemonstrated. Search trajectories for 5-number Countdown problems can exceed 60,000 tokens, making them impractical for standard LM context windows, and the 4-number restriction used in experiments is itself a concession to this scaling constraint.

The STaR-SFT null result on in-distribution preference accuracy is a meaningful caution: expert iteration does not uniformly improve performance, and its benefit may be tied to specific training objectives (DPO vs. SFT) and task types (safety vs. general preference). The mechanism behind STaR-DPO's safety advantage is not fully explained; it is unclear whether it reflects better calibration, better generalisation from reasoning traces, or an artefact of the safety category's structure.

Finally, only 57% of the 500,000 SoS training trajectories lead to a solution, yet the model still outperforms baselines trained on only correct solutions. This is a useful data point for the [[themes/synthetic_data_generation|synthetic data generation]] question of whether filtering to success is always optimal, and suggests that learning from failure trajectories may carry its own signal, though the mechanism is not yet well characterised.

## Relationships

STaR is closely related to [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] approaches more broadly: its filtering-and-finetuning loop is a form of policy optimisation without an explicit reward model, and it sits upstream of methods like RLHF and DPO in the post-training stack. Within [[themes/reward_modeling|Reward Modeling]], its role in GenRM connects it to debates about whether scalar reward models can be replaced by generative preference models that reason about outputs. Its dependence on the model's own search capacity ties it to [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], since the quality of generated trajectories constrains the quality of the finetuning signal.

## Key Findings

## Sources
