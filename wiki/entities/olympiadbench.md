---
type: entity
title: OlympiadBench
entity_type: dataset
theme_ids:
- agent_systems
- alignment_and_safety
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 14
sources_since_update: 0
update_count: 1
influence_score: 0.0013227055620985897
staleness: 0.0
status: active
tags: []
---
# OlympiadBench

OlympiadBench is a challenging benchmark dataset comprising olympiad-level mathematics problems, designed to probe the upper limits of advanced mathematical reasoning in large language models. Its difficulty makes it a discriminating evaluation surface where even state-of-the-art models diverge sharply, and it has become a key signal in the emerging literature on reinforcement learning for reasoning — particularly for distinguishing genuine reasoning capability from superficial pattern matching on easier benchmarks.

**Type:** dataset
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/multimodal_models|Multimodal Models]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], [[themes/vision_language_models|Vision-Language Models]]

## Overview

OlympiadBench sits at the harder end of the mathematical reasoning evaluation spectrum. Unlike benchmarks such as MATH or GSM8K that saturate with capable models, OlympiadBench preserves a meaningful spread even among frontier systems, making it useful for evaluating models trained with reinforcement learning where gains on easier benchmarks can be misleading. In the JustRL framework, it is evaluated using an `avg@4` metric — averaging over four independent samples — which reduces variance and gives a more reliable signal of the model's reasoning distribution than single-pass accuracy.

## Key Findings

The most striking result involving OlympiadBench comes from Skywork R1V2, where a 38B parameter multimodal model achieves **62.6%** on OlympiadBench — substantially outperforming much larger models: Qwen2.5-VL-72B reaches only 40.4%, and QvQ-Preview-72B manages just 33.2%. This near-doubling of performance at less than half the parameter count is a strong argument that training methodology — specifically the combination of reinforcement learning and careful curriculum design — matters far more than raw scale on this benchmark.

R1V2's approach is notable for what it omits as much as what it includes. It eliminates the supervised fine-tuning stage that preceded RL in its predecessor R1V1, based on evidence that SFT can inadvertently undermine subsequent reinforcement learning and reasoning processes. The model instead acquires multimodal reasoning skills directly through RL, without teacher model distillation — a departure from the standard recipe that the OlympiadBench score appears to validate.

The training dynamics behind this result are instructive. R1V2 employs a **Selective Sample Buffer (SSB)** mechanism to combat the GRPO vanishing advantages problem, where all responses within a query group converge toward uniform correctness or incorrectness, draining the relative advantage signal that RL relies on. Without SSB, effective training samples (those with non-zero advantages) fall from roughly 60% at training start to under 40% in later phases. Incorporating SSB as a filtered prompt pool during offline rollout yields over 10% improvement in training efficiency in the initial optimization phase — a meaningful practical gain on a benchmark where marginal improvements are hard-won.

R1V2 also applies Multimodal Preference Optimization (MPO) to address the brittleness of binary preference pairs for complex reasoning paths, and observes that this reduces repetitive chain-of-thought and overthinking artifacts in model outputs — pathologies that, in olympiad-level reasoning, can consume compute on unproductive reasoning branches.

## Limitations and Open Questions

OlympiadBench's discriminating power comes with caveats. The benchmark evaluates mathematical reasoning in a relatively narrow sense: symbolic manipulation, proof strategies, and competition-style problem solving. It does not measure whether models can reason about the structure of novel mathematical domains or transfer insights across problem classes — capabilities that would be required for genuine mathematical research assistance.

A persistent tension visible across the results is the **generality-specialization tradeoff**: models optimized heavily for mathematical reasoning often show degraded performance on everyday visual and general tasks, while general-purpose models struggle with complex analytical reasoning. OlympiadBench performance thus risks being a local optimum. R1V2 attempts to avoid this by training on a dataset spanning visual perception, scientific inquiry, and abstract reasoning, and reports high transferability between text and vision modalities — but whether this holds at the tail of the distribution remains an open question.

There is also a deeper concern about reinforcement signal calibration. Excessive reinforcement signals have been observed to induce **visual hallucinations** in vision-language models — a phenomenon R1V2 systematically monitors and mitigates through calibrated reward shaping. This suggests that optimizing hard for a benchmark like OlympiadBench, where the reward signal is clear and binary, may inadvertently degrade reliability in other modalities or task types. The benchmark thus measures a capability that, if over-targeted, may come at a hidden cost to model robustness.

Finally, the `avg@4` evaluation protocol used in JustRL reduces variance but also obscures the shape of the model's reasoning distribution. A model that is reliably mediocre and one that occasionally produces exceptional solutions but frequently fails can produce identical `avg@4` scores — yet their utility profiles differ substantially. Whether OlympiadBench, under this protocol, is measuring stable reasoning capability or peak performance remains an open methodological question.

## Relationships

OlympiadBench intersects most directly with [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]] and [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], where it serves as a hard evaluation target for post-training methods. Its use in Skywork R1V2 connects it to the broader [[themes/multimodal_models|multimodal reasoning]] literature, and its appearance in JustRL ties it to [[themes/scaling_laws|scaling]] debates about whether small models trained with principled RL can match or exceed larger models on hard reasoning tasks. The vanishing advantages dynamics observed during OlympiadBench training speak directly to [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], while the visual hallucination risk surfaces [[themes/hallucination_and_reliability|reliability]] as a live concern when pushing hard benchmarks with reinforcement learning.

## Sources
