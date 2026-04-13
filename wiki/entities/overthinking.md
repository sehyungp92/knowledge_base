---
type: entity
title: Overthinking
entity_type: theory
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
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0007112774285332798
staleness: 0.0
status: active
tags: []
---
# Overthinking

Overthinking is a failure mode observed in Large Reasoning Models (LRMs) where the model continues exploring and revising reasoning paths well beyond the point of arriving at a correct answer, producing excessively long decoding sequences at significant computational cost without proportional accuracy gains. As reasoning-capable models have become more powerful — exemplified by systems like DeepSeek-R1 and the techniques behind them — this phenomenon has emerged as one of the central efficiency challenges in the test-time compute scaling paradigm.

**Type:** theory
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

The overthinking phenomenon sits at the intersection of training dynamics and inference efficiency. RL-trained reasoning models are rewarded purely on final answer correctness — as in DeepSeek-R1-Zero's GRPO setup, where "the reward signal is solely based on the correctness of final predictions against ground-truth answers, without imposing constraints on the reasoning process itself." This reward structure creates a training signal that is agnostic to trace length, allowing models to develop habits of extended self-verification, backtracking, and re-exploration even when an early segment of the chain already contains the correct solution. The problem is especially pronounced on challenging inputs, but it also surfaces on simpler problems where a model finds the right answer early and then wastefully continues to audit it.

## The RL Training Root

Understanding why overthinking emerges requires understanding how modern reasoning models are trained. DeepSeek-R1-Zero demonstrated that "reasoning abilities of LLMs can be incentivized through pure reinforcement learning, obviating the need for human-labeled reasoning trajectories." Critically, the design bypassed conventional supervised fine-tuning before RL, based on the hypothesis that human-defined reasoning patterns might constrain model exploration. This gave the model freedom to develop its own reasoning strategies — but without length penalties, those strategies naturally drifted toward verbosity. The result is a model that can achieve 86.7% on AIME 2024 with self-consistency decoding (up from 15.6% pass@1 before RL), but does so through reasoning traces that may be far longer than necessary.

## Evidence from Trace Efficiency Research

The contrast between Chain of Thought and more compact alternatives illuminates how severe the problem is in practice. Chain of Draft research shows that standard CoT on GSM8K requires approximately 200 tokens per response to achieve ~95% accuracy for GPT-4o and Claude 3.5 Sonnet. CoD achieves 91% accuracy using only ~40 tokens per response — an 80% reduction in output token count — with latency reductions of 76.2% (GPT-4o) and 48.4% (Claude 3.5 Sonnet). On sports understanding tasks in BIG-bench, CoT becomes especially pathological for Claude 3.5 Sonnet: CoD reduces average output from 189.4 tokens to 14.3 (a 92.4% reduction) while *improving* accuracy from 93.2% to 97.3%. The excess tokens were not contributing to correctness — they were overthinking.

## Mitigation: Reasoning Shaping

The most direct intervention studied is GRSP (Gradient-based Reasoning Segment Penalization), which adds structured length penalties during RL training. Rather than applying uniform penalties, GRSP assigns descending penalty weights from shorter to longer reasoning segment clusters — penalizing short segments more heavily while applying weaker penalties to longer ones. The rationale is asymmetric: a model that reaches a solution in few segments and then halts deserves a lighter hand than one that spins out many segments unproductively. Empirically, GRSP produces an average of 21.07 reasoning segments versus 26.66 from models trained without penalty, confirming it can regulate segment count without collapsing reasoning quality.

## Open Questions and Limitations

Overthinking is not simply "more tokens = worse efficiency." The same models that overthink on simple problems genuinely need extended chains for hard ones — the difficulty is that the model cannot reliably calibrate when to stop. CoD itself is not a universal solution: it underperforms CoT on small models under 3B parameters (accuracy gaps of 8.3%–27.2% on GSM8K), and in zero-shot settings GPT-4o CoT at 94.8% beats CoD at 84.4% on GSM8K, showing that few-shot prompting is load-bearing for compact reasoning to work.

The deeper open question is whether overthinking is an artifact of the reward function or something more structural. If RL training with only correctness rewards systematically fails to teach models *when* a chain is complete, then length penalties and compact prompting are patches rather than cures. A more principled fix might require process-level reward signals — as explored in work on Process Reward Models — that directly supervise reasoning adequacy at each step rather than only at the terminal answer. Whether such signals can be provided without reintroducing the human-annotation bottleneck that RL-first training was designed to avoid remains an active tension in the field.

## Related Entities

- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] — overthinking is the pathological limit of scaling inference compute; the core challenge is making that scaling efficient
- [[themes/chain_of_thought|Chain of Thought]] — CoT is the substrate on which overthinking manifests; compact variants like CoD are direct responses
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — the training paradigm most responsible for inducing overthinking via unconstrained trace length
- [[themes/reward_modeling|Reward Modeling]] — process reward models represent a potential structural fix by supervising intermediate steps

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
