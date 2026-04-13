---
type: entity
title: Reinforcement Learning with Verifiable Rewards (RLVR)
entity_type: method
theme_ids:
- agent_systems
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- medical_and_biology_ai
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
- scientific_and_medical_ai
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.007351173511493097
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning with Verifiable Rewards (RLVR)

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vision_language_models|vision_language_models]]

## Overview

A post-training paradigm where language models are trained using reinforcement learning with rewards derived from verifiable outcomes (e.g., correctness of a math answer), as opposed to human preference labels.

## Key Findings

1. Current RLHF applications rely on costly human preference data and learned reward models that are susceptible to reward hacking, limiting scalability. (from "Reinforcement Pre-Training")
2. RPT experiments use the OmniMATH dataset, which contains 4,428 competition-level mathematical problems and solutions. (from "Reinforcement Pre-Training")
3. RPT significantly improves the accuracy of next-token prediction. (from "Reinforcement Pre-Training")
4. RPT enhances zero-shot performance on various downstream tasks. (from "Reinforcement Pre-Training")
5. RPT experiments use token-level data filtering to prioritize training on challenging, high-entropy tokens that require greater computational effort to predict. (from "Reinforcement Pre-Training")
6. RPT uses a prefix matching reward that supports verifying predictions spanning multiple tokens or involving out-of-vocabulary tokens. (from "Reinforcement Pre-Training")
7. Reinforcement Pre-Training (RPT) reframes next-token prediction as a reasoning task trained with reinforcement learning, using verifiable rewards derived directly from the pre-training corpus. (from "Reinforcement Pre-Training")
8. RPT transforms vast unannotated text data into a massive dataset for general-purpose RL without requiring external annotations or domain-specific reward functions. (from "Reinforcement Pre-Training")
9. RPT exhibits favorable scaling properties where next-token prediction performance consistently improves with increased training compute. (from "Reinforcement Pre-Training")
10. RPT provides a stronger pre-trained foundation for subsequent reinforcement fine-tuning, leading to better final task performance. (from "Reinforcement Pre-Training")
11. RLVR is typically constrained by the scarcity of annotated data with verifiable answers, restricting its application to domain-specific fine-tuning rather than general-purpose pre-training. (from "Reinforcement Pre-Training")
12. RPT minimizes reward hacking risk by using direct, rule-based reward signals tied to the correctness of the predicted next token. (from "Reinforcement Pre-Training")
13. RPT uses DeepSeek-R1-Distill-Qwen-14B as the base model, chosen for its basic reasoning capabilities as a starting point for reinforcement learning. (from "Reinforcement Pre-Training")
14. Standard next-token prediction estimates the next token directly, while next-token reasoning performs reasoning over multiple tokens before making the prediction. (from "Reinforcement Pre-Training")
15. RPT uses the GRPO algorithm for on-policy reinforcement learning training. (from "Reinforcement Pre-Training")

## Relationships

## Limitations and Open Questions

## Sources
