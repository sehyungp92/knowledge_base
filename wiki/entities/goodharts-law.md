---
type: entity
title: Goodhart's Law
entity_type: theory
theme_ids:
- agent_evaluation
- agent_systems
- ai_market_dynamics
- benchmark_design
- evaluation_and_benchmarks
- frontier_lab_competition
- generative_media
- in_context_and_meta_learning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0007182848469332927
staleness: 0.0
status: active
tags: []
---
# Goodhart's Law

> Goodhart's Law — "when a measure becomes a target, it ceases to be a good measure" — is one of the most structurally important principles for understanding AI progress. In the AI context, it describes the systematic degradation of benchmarks as optimisation targets: once a capability measure gains prestige or prize money, competitive pressure drives methods that score well on the measure without necessarily advancing the underlying capability it was designed to proxy.

**Type:** theory
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/benchmark_design|Benchmark Design]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/generative_media|Generative Media]], [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/video_and_world_models|Video and World Models]]

## Overview

The principle that when a measure becomes a target, it ceases to be a good measure. Applied to AI evaluation, it captures how benchmark scores increasingly reflect optimisation-for-the-benchmark rather than the underlying capability the benchmark was intended to track. The ARC-AGI challenge provides a vivid case study, and the dynamic recurs across virtually every major benchmark in the field — from reasoning to coding to multimodal evaluation.

## The ARC-AGI Case Study

The Abstraction and Reasoning Corpus was designed by François Chollet as a benchmark resistant to the kind of pattern memorisation that has allowed models to saturate earlier tests. Its 1,000 tasks — 400 training, 400 public evaluation, and 200 held in an unpublished private set — were intended to measure fluid, generalising intelligence rather than recall. The private set's unpublished status was precisely a structural defence against Goodhart dynamics: you cannot overfit to data you cannot see.

Nevertheless, competitive pressure drove increasingly narrow optimisation. The 2020 Kaggle competition saw a winning method score roughly 21% on a private subset, with an ensemble of the top two methods reaching 31% — modest numbers achieved through program synthesis approaches tailored to ARC's grid structure. By 2023, MindsAI held first place at 34% on the private evaluation set, a position they maintained and extended to 43% by the time of the ARC-AGI $1 Million Reasoning Challenge write-up.

What is notable about these leading methods is how explicitly they close the loop between benchmark and training signal. MindsAI's core technique is automatic generation of large numbers of new ARC tasks as variations of the original training set — essentially synthetic data augmentation designed to expand coverage of the very distribution being tested. Their "active inference" approach further converts few-shot evaluation tasks into many-shot tasks by performing additional fine-tuning on augmented demonstrations at inference time. The result is a system highly adapted to the specific structure of ARC's evaluation regime.

The Greenblatt method, which drew significant attention for scoring 51% on the public evaluation set (on a 100-task sample, with a standard error of ~5%), illustrates the compute and engineering intensity that benchmark optimisation can require. His generate-test-revise loop prompted GPT-4o to generate approximately 5,000 Python programs per task, with prompts running to roughly 30,000 tokens — comparable in length to a 50-page thesis. The method was ultimately ineligible for the ARC Prize competition because it violated two structural rules: it required internet access (for the GPT-4o API) and exceeded the 12-hour runtime cap. The competition's constraints — no internet, 12-hour limit — are themselves Goodhart countermeasures, preventing the kind of unlimited compute and frontier model access that would make scores meaningless as proxies for general capability.

The $500,000 ARC Prize announced in June 2024, offering the grand prize for any program scoring 85% or higher on 100 private tasks, dramatically raised the stakes and, predictably, the intensity of targeted optimisation.

## The Structural Dynamic

What the ARC-AGI trajectory illustrates is a general pattern: as a benchmark gains prestige, resources, or prize money, the methods converging on it become increasingly specialised. Scores rise — but the gap between benchmark performance and the capability the benchmark was designed to measure widens. This is not fraud; it is the rational response of competitive optimisation to a fixed target. AlphaGo Zero's self-play from scratch, which rediscovered all of Go knowledge without human game data, represents the ideal of genuine capability acquisition. But benchmark competition rarely produces that kind of result — it produces MindsAI-style augmentation pipelines finely tuned to the test distribution.

The same dynamic operates at the frontier. Models like Grok 4 and Gemini 2.5 Pro can claim state-of-the-art performance on widely-cited benchmarks while underperforming on capability-focused evaluations less amenable to targeted optimisation. The source Failing to Understand the Exponential, Again examines how progress metrics can give a misleading picture of trajectory precisely because headline benchmark improvements compound the optimisation signal rather than the capability signal.

## Implications and Open Questions

Goodhart's Law implies that the value of a benchmark is inversely proportional to its popularity as a target — a deeply uncomfortable property for a field that needs shared measures to communicate progress. The ARC-AGI design choices (private test set, resource constraints, adversarial task construction) represent genuine attempts to extend the useful life of an evaluation, but the ceiling on such defences is not high: a sufficiently motivated and well-resourced competitor can always find the seams.

Several open questions follow from this:

- **What is the right architecture for evaluation?** Continuously refreshed private test sets, human-in-the-loop evaluation, and capability probes that are intrinsically hard to optimise directly are all candidate approaches, each with costs.
- **How do we separate genuine capability gains from benchmark adaptation?** The ARC score improvements from 21% (2020) to 43% (MindsAI) do not map cleanly to a proportional improvement in abstract reasoning; disentangling the two requires evaluation methods orthogonal to the training signal.
- **Does the dynamic self-correct?** When a benchmark saturates or loses credibility, the field moves on — but this transition is slow and the saturated scores persist in the literature as apparent evidence of progress.

Goodhart's Law is not merely a methodological caution. It is a structural feature of competitive optimisation against measurable proxies, and its operation is visible across the entire AI benchmark landscape. Understanding it is prerequisite to reading capability claims accurately.

## Related Sources

- On the "ARC-AGI" $1 Million Reasoning Challenge
- Failing to Understand the Exponential, Again
- Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
