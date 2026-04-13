---
type: entity
title: Reasoning Gym
entity_type: dataset
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012731618195134067
staleness: 0.0
status: active
tags: []
---
# Reasoning Gym

Reasoning Gym is a procedural dataset framework designed for training and evaluating reasoning models on logic-related tasks. Its defining feature is parameterised difficulty control: for each task type, the framework exposes knobs governing problem complexity, enabling unlimited synthetic data generation at any desired difficulty level. This makes it particularly well-suited as a training domain for reinforcement learning pipelines, where reward signal density and curriculum progression are critical to sustained improvement.

**Type:** dataset
**Themes:** [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory & Dynamics]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

Reasoning Gym provides a family of logic-structured challenges — puzzles, constraint satisfaction problems, and other formal reasoning tasks — each governed by explicit difficulty parameters. Because data generation is programmatic and unbounded, it avoids the saturation problem that afflicts fixed benchmarks: a model cannot memorise the test set when the test set is generated fresh at evaluation time. This positions Reasoning Gym as both a training corpus and a live evaluation surface.

## Role in RL Training Pipelines

Reasoning Gym appears as a central component in ProRL, NVIDIA's prolonged RL training experiment on Qwen-1.5B. The 136K-problem training corpus spans math, code, STEM, logic puzzles, and instruction-following — with Reasoning Gym covering the logic puzzle domain. The inclusion matters because logic puzzles provide dense, verifiable reward signal: answers are right or wrong by construction, and difficulty can be tuned to stay just ahead of the model's current capability. The results were striking: Nemotron-Research-Reasoning-Qwen-1.5B improved reward on Reasoning Gym logic puzzles by **54.8%** over its base model (DeepSeek-R1-Distill-Qwen-1.5B), despite the base model struggling with both formatting and challenging subtasks in this domain.

This gain is large relative to the math benchmark improvements (~15.7% average) and coding improvements (~14.4% pass@1), suggesting that logic puzzle tasks may represent a regime where the base model's pre-training distribution is especially thin — and thus where RL has more room to manoeuvre.

## Limitations and Open Questions

The strong absolute improvement on Reasoning Gym logic puzzles should be read against the broader findings of The Invisible Leash, which analysed RLVR dynamics across models and domains including Reasoning Gym. That work found that across all evaluated models and domains, support retention rates remain very high (SRR ≈ 0.93–0.99) while genuine discovery of novel solutions is rare (NDR ≤ 0.04). In plain terms: RLVR reliably amplifies solutions the base model could already produce at low probability, but rarely discovers solution types that were genuinely absent from the base distribution.

This raises a pointed question for Reasoning Gym specifically: is the 54.8% improvement on logic puzzles a case of genuine skill acquisition, or of the model learning to reliably surface and format solutions it could already generate? The base model's struggles with formatting on Reasoning Gym tasks are acknowledged in ProRL's own evidence — which suggests some fraction of the measured gain may reflect format conditioning rather than deeper reasoning capability.

The entropy-reward trade-off identified by the Invisible Leash compounds this concern. RLVR increases precision while narrowing exploration; at high sampling budgets (pass@8192), base models can outperform their RLVR-trained counterparts because they retain broader solution coverage. Whether this dynamic holds in the Reasoning Gym logic domain — where tasks are programmably varied and the solution space may be less dominated by rare high-quality paths than in competition math — remains an open question.

## Relationships

Reasoning Gym is used as a training domain and evaluation surface in ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models, and appears as an evaluation domain in The Invisible Leash: Why RLVR May or May Not Escape Its Origin. Its design philosophy — parameterised difficulty, unlimited generation, verifiable reward — connects it to the broader [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] literature's emphasis on scalable verifier-based training signals, as surveyed in A Survey of Reinforcement Learning for Large Reasoning Models. Its logic puzzle domain sits within [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]] but is distinct from competition math benchmarks like AIME, occupying a more procedurally generative niche closer to algorithmic and constraint-based tasks.

## Key Findings

## Sources
