---
type: entity
title: AMC
entity_type: dataset
theme_ids:
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
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 9.739179424769061e-05
staleness: 0.0
status: active
tags: []
---
# AMC

The American Mathematics Competition (AMC) is a standardized mathematical problem-solving benchmark that has become a standard evaluation dataset for assessing the mathematical reasoning capabilities of large language models. Alongside AIME 2024, MATH-500, and GPQA, it serves as one of the canonical checkpoints for measuring whether training interventions — particularly reinforcement learning approaches — produce genuine reasoning improvements or merely surface-level behavioral shifts.

**Type:** dataset
**Themes:** [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory & Dynamics]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/test_time_learning|Test-Time Learning]]

## Overview

AMC problems occupy a difficulty tier between MATH-500 (accessible) and AIME 2024 (highly challenging), making it useful for detecting whether performance gains on easier benchmarks generalize to harder mathematical reasoning. Its inclusion in multi-benchmark evaluations is standard practice precisely because models can exploit distributional shortcuts on any single benchmark, and AMC's intermediate difficulty helps reveal whether capability gains are real.

## Key Findings

### TTRL: Test-Time Reinforcement Learning as a Case Study

The most prominent role AMC plays in recent literature is as part of the evaluation suite for TTRL: Test-Time Reinforcement Learning. TTRL applied to Qwen2.5-Math-7B achieves an average gain of 76% across AIME 2024, AMC, MATH-500, and GPQA — with the AIME result alone showing a 211% boost (12.9% → 40.2% pass@1) using only unlabeled test data. The AMC result sits within this aggregate, serving as evidence that TTRL's gains are not confined to a single difficulty tier.

What makes TTRL particularly significant in this context is its mechanism: majority voting over N candidate outputs becomes the proxy label, with outputs matching the modal answer receiving reward. This means the model is, in effect, bootstrapping its own training signal from consensus — a process that on AMC-level problems is plausible but becomes increasingly fragile as problem difficulty rises and consensus becomes harder to achieve. TTRL's avg@64 after training consistently outperforms the initial model's maj@64, and crucially, it surpasses what should theoretically be the self-training upper bound (the initial model's majority voting accuracy), suggesting the process induces genuine capability improvement rather than simple recalibration.

### Spurious Rewards and the Qwen Anomaly

AMC also appears as a background evaluation context in Spurious Rewards: Rethinking Training Signals in RLVR, where the central puzzle concerns why Qwen2.5-Math-7B improves even under obviously wrong or meaningless reward signals. Training with incorrect label rewards yields 24.1% absolute improvement on MATH-500 versus 29.1% from ground truth — a gap far smaller than one would expect if reward correctness were the primary driver. A Python reward (triggered by the string 'python' appearing in any response) drives code reasoning frequency from 65% to over 90% within 20 training steps, and accuracy still rises.

This raises a pointed question for AMC as an evaluation: if improvements on MATH-500 can be induced by spurious rewards, how much of any reported AMC gain reflects genuine mathematical reasoning versus learned surface behaviors (like defaulting to code-format responses)? The paper finds that code reasoning is strongly predictive of accuracy — responses containing code achieve 60.9% accuracy versus 28.0% without — but this correlation is confounded by the fact that Qwen2.5-Math-7B already generates Python code in 65% of responses even without a code interpreter. The model may have been pre-trained on distributions that reward code-style formatting regardless of execution.

Critically, spurious rewards that work for Qwen models frequently fail to generalize to Llama3 or OLMo2, which means AMC-based results from Qwen-family models cannot be straightforwardly interpreted as evidence about RL training dynamics in general. The benchmark result is real; what it measures is model-family-dependent.

### Clipping and the Mechanics of Apparent Improvement

A technical finding from the spurious rewards work bears directly on how AMC improvements should be interpreted: removing the clipping term from GRPO eliminates the effect of random rewards entirely. With clipping present, random rewards can still produce performance changes; without it, gradients go to zero. This means some portion of reported AMC gains across the literature may be artifacts of optimizer mechanics rather than signal from the reward function itself.

## Open Questions

The AMC benchmark sits at an uncomfortable position: difficult enough to be meaningful, tractable enough for majority voting to produce reliable pseudo-labels, and popular enough that the literature has begun to show the characteristic signs of benchmark saturation. The key unresolved questions are:

- **What fraction of AMC gains under RL training reflect genuine mathematical reasoning versus format exploitation or pre-trained code-reasoning biases?** The spurious rewards results suggest the answer is not obvious even in controlled settings.
- **Does TTRL's majority-voting proxy degrade gracefully as problems get harder?** AMC is tractable enough that consensus emerges; it is unclear whether the same mechanism would hold on olympiad-level problems where the initial model rarely produces the correct answer in any output.
- **Are improvements on AMC transferable across model families?** The Qwen-specificity of spurious reward effects suggests that benchmark results on this dataset may not generalize.

## Relationships

AMC is closely coupled to **AIME 2024** and **MATH-500** as the standard trio of math reasoning evaluation benchmarks — findings about one typically report all three. The **Qwen2.5-Math-7B** model family is the primary subject in both source papers that feature AMC prominently, making it the de facto reference model for AMC-based RL training experiments. **GRPO** (used in both TTRL and the spurious rewards work) is the training algorithm whose dynamics most directly shape what AMC scores mean, and the clipping term within GRPO is a non-obvious confound for interpreting any result on this benchmark.

## Limitations and Open Questions

## Sources
