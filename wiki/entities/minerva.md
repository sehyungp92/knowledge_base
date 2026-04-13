---
type: entity
title: Minerva
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0003008182418307379
staleness: 0.0
status: active
tags: []
---
# Minerva

> Minerva is a quantitative reasoning benchmark used to evaluate mathematical problem-solving in large language models. It serves as part of standard evaluation suites for RL-trained reasoning models, appearing alongside AIME24/25, AMC23, MATH500, and GPQA as a gauge of generalised mathematical capability after post-training.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

Minerva is a math reasoning benchmark covering quantitative reasoning problems, originally developed by Google to test whether language models can solve science and mathematics questions that require multi-step numerical and symbolic reasoning. In the recent RL post-training literature it has become a standard component of aggregate evaluation suites, where individual benchmark scores are averaged to assess broad mathematical aptitude rather than performance on any single distribution.

## Role in Recent RL Reasoning Research

Minerva appears prominently in two lines of work — FlowRL and Tina — where it functions as one node in a multi-benchmark average rather than a standalone target.

In the **Tina** evaluation, all five models achieve average reasoning scores between 48.16% and 50.60% across AIME24/25, AMC23, MATH500, GPQA, and Minerva collectively. Notably, nearly all Tina models outperform their full-parameter-trained baseline counterparts despite using only LoRA updates — a result achieved with as little as 19–57% of a single training epoch and at a total reproduction cost of $526 USD (best checkpoint: $9 USD). This positions Minerva as one of the benchmarks confirming that parameter-efficient RL post-training can produce genuine, broad mathematical gains rather than narrow benchmark overfitting.

**FlowRL** uses Minerva as part of its math benchmark suite to validate its distribution-matching objective. FlowRL transforms scalar rewards into a normalised target distribution via a learnable partition function (a randomly initialised 3-layer MLP taking the mean of hidden states as input) and minimises the reverse KL divergence between the policy and that distribution. Across the full suite including Minerva, FlowRL achieves 35.6% average accuracy with a 7B model and 48.4% with a 32B model — a 10.0% margin over GRPO and 5.1% over PPO. Ablations show that removing importance sampling collapses average accuracy from 35.63% to 26.71%, underscoring how distribution correction is load-bearing for the gains reflected in benchmarks like Minerva.

## Limitations and Open Questions

Because Minerva is used as part of aggregated averages in these studies, its individual contribution to reported gains is not isolated. It is unclear whether the improvements are uniform across all benchmarks in the suite or whether Minerva specifically is an easier or harder target for RL-trained models relative to, say, AIME24. The benchmark's overlap in problem style with MATH500 also raises questions about how much independent signal it adds to aggregate evaluations.

Tina's results further invite scrutiny: strong aggregate scores achieved in under one epoch suggest rapid surface-level adaptation, but whether this reflects robust generalisation across Minerva's full problem distribution or efficient exploitation of recurring problem structures remains an open question.

## Relationships

Minerva is co-evaluated with AIME24, AMC23, MATH500, and GPQA in both the Tina and FlowRL evaluation suites. The methods evaluated on it — FlowRL's KL-divergence matching and Tina's LoRA-based RL — both connect to broader debates in [[themes/policy_optimization|policy optimisation]] about whether PPO-style clipping, distribution matching, or parameter-efficient updates are the right inductive biases for mathematical reasoning. Its presence in these suites reflects a broader trend in [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] of using multi-benchmark aggregation to guard against single-distribution overfitting.

## Key Findings

## Sources
