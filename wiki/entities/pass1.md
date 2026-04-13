---
type: entity
title: Pass@1
entity_type: metric
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_software_engineering
- alignment_and_safety
- chain_of_thought
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- hallucination_and_reliability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- search_and_tree_reasoning
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 13
sources_since_update: 0
update_count: 1
influence_score: 0.002345733036151321
staleness: 0.0
status: active
tags: []
---
# Pass@1

Pass@1 is the foundational evaluation metric for language model problem-solving ability: the probability that a single sampled response to a problem is correct. Deceptively simple in definition, it sits at the center of a large methodological tension in modern LLM evaluation, where the gap between headline numbers (averaged over many samples) and true single-shot performance reveals both the genuine capabilities and the hidden inference costs of frontier reasoning systems.

**Type:** metric
**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/ai_software_engineering|AI Software Engineering]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/chain_of_thought|Chain of Thought]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/multimodal_models|Multimodal Models]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/scaling_laws|Scaling Laws]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], [[themes/vision_language_models|Vision-Language Models]]

## Overview

Pass@1 estimates the probability that a single model generation solves a given problem. In practice, it is typically measured by sampling N responses and computing the fraction that are correct, with JustRL using N=4 or N=32 depending on the benchmark. This averaging procedure matters enormously: a model that achieves 35% pass@1 on AIME25 might appear to hit 45-50% when headline numbers draw on multi-sample aggregation, masking the real cost in inference compute.

The metric serves as the primary signal across a wide range of reasoning and coding benchmarks, from AIME and HMMT in competition mathematics to GPQA in science and SWE-bench in software engineering. Its apparent simplicity makes it universally comparable across papers, but that same simplicity invites abuse: reported numbers frequently conflate single-sample pass@1 with Avg@k or consensus@k, making cross-paper comparisons treacherous.

## The Aggregation Problem

The most active recent research direction around pass@1 is not improving it directly but rather improving how multiple low-pass@1 samples are combined. The Majority is not always right introduces AggLM, a 1.7B aggregator model trained with reinforcement learning from verifiable rewards to review, reconcile, and synthesize a final answer from a candidate set of solutions. The core result is that AggLM-1.7B aggregating 8 solutions beats majority voting over 16 solutions on AIME25, HMMT24, and HMMT25, achieving comparable performance with half the generation budget.

The gains are not uniform. AggLM's advantage over majority voting is largest when candidate solutions are maximally diverse, meaning when the majority answer cluster is small and the correct answer is likely to appear in a minority of solutions. This is precisely the regime where majority voting fails: it recovers the modal answer, not the correct one. By contrast, AggLM can identify and elevate a minority-correct solution when the reasoning quality warrants it.

Several nuances govern when this generalizes. AggLM-1.7B transfers effectively to solutions from Qwen3-8B despite being trained only on 1.7B solution distributions, and it handles non-thinking model outputs despite training exclusively on thinking-mode distributions. It also generalizes to candidate set sizes both smaller and larger than the k=8 training setting, with performance improving monotonically as k increases. The curve rises more steeply than majority voting's, suggesting the aggregator becomes more valuable as the solution pool grows.

## What Drives the Gains

A key finding is that training data composition, not data scale, drives AggLM's performance. Training on hard examples only produces suboptimal results; including all easy examples offers only marginal improvement over an untrained aggregator. The critical ingredient is a balanced mixture of easy and hard examples, specifically 5-50% easy examples relative to hard. Within that range, performance is stable. The interpretation is that hard examples teach the aggregator to recover minority-correct answers, while easy examples teach it to reliably confirm majority-correct answers; without both skills, it fails in complementary regimes.

A natural alternative, simply training the solution model on additional data rather than training a separate aggregator, does not close the performance gap. This rules out the explanation that AggLM's edge comes from extra training signal rather than the learned aggregation capability itself.

Reward model selection, a common alternative approach using Best-of-N or weighted majority with a verifier, performs poorly relative to standard majority voting when applied to thinking-mode solutions. AggLM-1.7B outperforms reward-model selection baselines with 72B parameters on all four math competition benchmarks, at roughly one-third the per-generation token cost of the solution models.

## Frontier Numbers and Their Caveats

At the high end, o4-mini achieves 99.5% pass@1 (and 100% consensus@8) on AIME 2025 with Python interpreter access, ranking as the best-performing benchmarked model on both AIME 2024 and AIME 2025. This represents a qualitative ceiling for competition mathematics: a system that is essentially always correct in a single attempt, when given code execution as a tool.

The limitation is context-specific. AIME24 and GPQA frontier results are frequently reported as Avg@32 and Avg@8 respectively, not true single-sample pass@1. Achieving those headline numbers requires 8-32x the inference compute of a single generation. The practical implication is that reported frontier performance substantially overstates what a deployed system can deliver at standard cost; the gap between pass@1 and Avg@k is a direct measure of how much reliability has to be bought through repeated sampling rather than baked into the model.

## Open Questions

The relationship between pass@1 and the aggregation benefit remains partially unresolved. AggLM's gains are largest at moderate pass@1 values, where solutions are diverse and the correct answer is not always in the majority. As pass@1 approaches 1, aggregation is unnecessary; as it approaches 0, no aggregation strategy recovers signal. The practical utility of learned aggregation therefore peaks in the middle of the difficulty curve, which happens to be where current frontier models sit on the hardest benchmarks. Whether the same pattern holds outside competition mathematics, in coding, science, or agentic tasks, is an open question that existing evaluations only partially address.

## Relationships

Pass@1 is closely related to [[entities/best-of-n-sampling|Best-of-N Sampling]] and [[entities/majority-voting|Majority Voting]] as competing aggregation strategies at inference time. It is the baseline metric against which [[entities/test-time-compute-scaling|test-time compute scaling]] improvements are measured. The AggLM findings connect directly to [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] via the verifiable reward training setup, and to [[themes/reward_modeling|Reward Modeling]] through the comparison with reward model selection baselines. The distinction between pass@1 and Avg@k is a recurring concern in [[themes/scaling_laws|Scaling Laws]] analysis, where it affects whether inference compute or training compute is the operative variable.

## Key Findings

## Limitations and Open Questions

## Sources
