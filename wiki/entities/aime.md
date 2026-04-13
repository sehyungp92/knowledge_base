---
type: entity
title: AIME
entity_type: dataset
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- chain_of_thought
- context_engineering
- finetuning_and_distillation
- hallucination_and_reliability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.00791084935259859
staleness: 0.0
status: active
tags: []
---
# AIME

**Type:** dataset
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

American Invitational Mathematics Examination — used as a benchmark for evaluating mathematical reasoning capabilities of LLMs.

## Key Findings

1. Balancing easy and hard training examples is critical for AggLM to learn both minority-correct answer recovery and majority-correct answer handling. (from "The Majority is not always right: RL training for solution aggregation")
2. AggLM's performance gains over majority voting are largest when the majority answer size is small, i.e., when candidate solutions are more diverse. (from "The Majority is not always right: RL training for solution aggregation")
3. AggLM-1.7B generalizes to non-thinking model solutions despite being trained exclusively on thinking-mode distributions. (from "The Majority is not always right: RL training for solution aggregation")
4. AggLM trains an aggregator model using reinforcement learning from verifiable rewards to review, reconcile, and synthesize a final correct answer from candidate solutions. (from "The Majority is not always right: RL training for solution aggregation")
5. AggLM-1.7B raises Qwen3-1.7B's accuracy on AIME25 from 35% to 50%, outperforming majority voting at 45%. (from "The Majority is not always right: RL training for solution aggregation")
6. Training the solution model on additional data does not close the performance gap with a trained aggregator, showing gains arise from learning to aggregate rather than from more data. (from "The Majority is not always right: RL training for solution aggregation")
7. AggLM-1.7B generalizes to candidate set sizes k both smaller and larger than the k=8 used during training. (from "The Majority is not always right: RL training for solution aggregation")
8. AggLM-1.7B outperforms reward model selection baselines with 72B parameters on all four math competition benchmarks. (from "The Majority is not always right: RL training for solution aggregation")
9. Reward model-based selection (Best-of-N and weighted majority) is often inferior to standard majority voting when aggregating thinking-mode solutions. (from "The Majority is not always right: RL training for solution aggregation")
10. Training AggLM on hard examples only results in suboptimal performance; including all easy examples offers only marginal improvement over an untrained aggregator. (from "The Majority is not always right: RL training for solution aggregation")
11. The AggLM aggregator uses roughly one-third as many tokens per generation as the solution models. (from "The Majority is not always right: RL training for solution aggregation")
12. Including 5–50% easy examples relative to hard examples consistently enhances AggLM performance and results are stable within this range. (from "The Majority is not always right: RL training for solution aggregation")
13. AggLM-1.7B generalizes effectively to solutions from stronger models (Qwen3-8B) not present in its training data. (from "The Majority is not always right: RL training for solution aggregation")
14. On AIME25, HMMT24, and HMMT25, aggregating 8 solutions with AggLM-1.7B achieves higher performance than majority voting over 16 solutions. (from "The Majority is not always right: RL training for solution aggregation")
15. A single multitask model trained for both solution generation and aggregation achieves performance close to separately trained models. (from "The Majority is not always right: RL training for solution aggregation")

## Capabilities

- State-of-the-art math reasoning among non-thinking models: AIME 2024 69.6 Avg@64, AIME 2025 49.5 Avg@64, MATH-500 97.4%, HMMT 2025 38.8 Avg@32, GPQA-Diamond 75.1 Avg@8 — surpassing GPT-4.1, Claude Son (maturity: narrow_production)
- AIME24 91.0% (Avg@32) on olympiad-level mathematics, competitive with o3 (90.3%) and ahead of Gemini 2.5 Pro (88.7%); MATH 500 at 98.2% (maturity: narrow_production)
- o4-mini achieves 99.5% pass@1 (100% consensus@8) on AIME 2025 with Python interpreter access, ranking as best-performing benchmarked model on both AIME 2024 and AIME 2025 (maturity: narrow_production)

## Known Limitations

- The $4.6 trillion opportunity is framed as a 'next five years' projection — the vast majority of the claimed addressable market is aspirational and not currently being captured by AI systems (severity: significant, trajectory: improving)
- AIME24 and GPQA results reported as Avg@32 and Avg@8 respectively — single-sample pass@1 performance is substantially lower, requiring 8-32x inference compute overhead to achieve reported frontier num (severity: minor, trajectory: stable)
- AIME performance with tool access (Python interpreter) cannot be meaningfully compared to scores from unaided models — tool-augmented evaluation results are fragmented from the existing benchmark base (severity: significant, trajectory: worsening)
- Standard math benchmarks (MATH-500, AIME24) are likely contaminated with training data, making it difficult to distinguish genuine reasoning capability gains from memorization (severity: significant, trajectory: worsening)

## Relationships

## Limitations and Open Questions

## Sources
