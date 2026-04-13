---
type: entity
title: CodeContests
entity_type: dataset
theme_ids:
- agent_systems
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- software_engineering_agents
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0002444849497475761
staleness: 0.0
status: active
tags: []
---
# CodeContests

> CodeContests is a competitive programming dataset originally released by DeepMind, widely adopted as a benchmark and training resource for code generation models. Its significance in recent work lies primarily in its role as a source of execution tracing data for training code world models — systems that learn to simulate program behavior rather than merely predict tokens.

**Type:** dataset
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

CodeContests consists of competitive programming problems paired with human-written solutions, making it a natural candidate for generating execution traces — solutions are self-contained, their correctness is verifiable, and they span a wide range of algorithmic patterns. In the context of CWM, the dataset was used specifically to produce *natural language execution traces*: 262k solutions were generated from CodeContests problems, and after filtering, 33k effective snippets with 70k traces were retained. These traces capture the step-by-step runtime behavior of code, forming part of the broader tracing corpus used to train CWM's world model capabilities.

## Role in CWM's Training Data

CodeContests contributes a small but specialized slice of CWM's tracing dataset. The bulk of the function-level tracing data — over 120 million traced Python functions — comes from standalone Python functions scraped more broadly. Natural language tracing produced 75 million trajectories from standalone functions and 110k from CodeContests specifically, reflecting that the competitive programming data, while high-quality and algorithmically rich, is necessarily narrow in volume compared to the general Python corpus.

The value of CodeContests in this pipeline is qualitative rather than quantitative: competitive programming solutions tend to involve non-trivial control flow, recursion, and data structure manipulation, which produces execution traces that stress-test a model's ability to simulate complex program states. This complements the repository-level tracing performed across 21,000+ repository images (yielding ~70,000 execution-traced commits) and the 3 million trajectories gathered by ForagerAgent from 3,150 repositories — each data source covering a different slice of real-world coding behavior.

## Broader Context

The downstream model trained on this data, CWM — a 32B dense decoder-only LLM with 131k token context — achieves strong results on code benchmarks including 65.8% pass@1 on SWE-bench Verified (with test-time scaling), 68.6% on LiveCodeBench-v5, 96.6% on Math-500, and 76.0% on AIME 2024. The use of CodeContests is one component of a multi-source training strategy that also spans general pre-training on 8T tokens, 5T token mid-training at extended context, and RL fine-tuning via a SWE RL agent operating with up to 128 turns over 131k context.

Separately, CodeContests appears in the [[themes/test_time_compute_scaling|test-time compute scaling]] literature — notably in work on repeated sampling — as a benchmark for measuring pass@k performance across varying numbers of samples, making it a touchstone for evaluating both training-time and inference-time scaling strategies.

## Limitations and Open Questions

The filtering rate in CWM's pipeline is notable: only ~33k of 262k generated solutions (roughly 13%) survived filtering to produce usable traces. This suggests either that execution tracing of competitive programming solutions is particularly brittle — due to missing dependencies, non-termination, or runtime errors — or that the quality bar for "effective snippets" was high. The exact filtering criteria are not detailed in the available claims, which leaves open the question of what kinds of solutions or trace structures were excluded and whether the resulting 70k traces are representative of the full difficulty spectrum in CodeContests.

More broadly, it remains unclear whether competitive programming data — with its emphasis on algorithmic correctness under tight constraints — produces execution traces that generalize well to the kinds of reasoning needed for repository-level software engineering tasks. The gap between CodeContests-style traces and the agent trajectories used in SWE RL training may represent an underexplored distribution mismatch in CWM's training data.

## Relationships

- CWM: An Open-Weights LLM for Research on Code Generation with World Models — primary source for CodeContests' use as execution tracing data
- Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL — uses CodeContests in the context of agent foundation model evaluation
- Large Language Monkeys: Scaling Inference Compute with Repeated Sampling — uses CodeContests as a benchmark for pass@k scaling analysis
- Related datasets: SWE-bench, LiveCodeBench, AIME, Math-500 — the broader evaluation suite in which CodeContests-trained capabilities are assessed

## Key Findings

## Sources
