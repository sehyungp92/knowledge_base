---
type: entity
title: GRPO (Group Relative Policy Optimization)
entity_type: method
theme_ids:
- agent_systems
- chain_of_thought
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- in_context_and_meta_learning
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
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.004982429292912749
staleness: 0.0
status: active
tags: []
---
# GRPO (Group Relative Policy Optimization)

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A policy gradient algorithm used in LLM post-training that computes advantages relative to a group of rollouts per prompt, used in DeepSeek and several open RLVR works.

## Key Findings

1. Expanding the collection of training environments consistently leads to better performance on held-out (OOD) environments, across all model types tested. (from "RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments")
2. RLPT derives reward signals directly from pre-training data, eliminating the dependency on human annotation. (from "Reinforcement Learning on Pre-Training Data")
3. RLVE with joint training across 400 environments achieves a 3.37% absolute average gain within approximately 1,100 H100 GPU hours, versus 0.49% for continued original RLVR training using more than 3×  (from "RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments")
4. Standard RLVR with ground truth rewards improves Qwen 2.5 Math 7B MATH-500 score by +24.6 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
5. RLMT uses 7.5K prompts from the WildChat-IF subset of the Tulu 3 SFT mixture, which prioritizes conversational prompts covering a wide range of realistic user queries (from "Language Models that Think, Chat Better")
6. RLPT used as initialization for RLVR yields additional improvements of 2.3 and 1.3 in Pass@1, and 3.7 and 2.0 in Pass@8, on AIME24 and AIME25 respectively. (from "Reinforcement Learning on Pre-Training Data")
7. One-Shot RL (using a single example) improves Qwen 2.5 Math 7B MATH-500 by +21.4 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
8. Training Qwen 2.5 Math 7B with majority vote rewards improves MATH-500 by +23.2 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
9. Rewarding only for the presence of \boxed{} formatting improves Qwen 2.5 Math 7B MATH-500 by +19.8 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
10. Random rewards (awarding 1 reward per rollout prompt with a fixed probability in GRPO) improve Qwen 2.5 Math 7B MATH-500 by +15.8 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
11. Rewarding only incorrect answers improves Qwen 2.5 Math 7B MATH-500 by +21.2 points. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
12. RLMT (RL with Model-rewarded Thinking) trains language models to generate long chain-of-thought reasoning before final answers using online RL algorithms such as GRPO, evaluated against a preference-b (from "Language Models that Think, Chat Better")
13. When reward is never assigned in GRPO, the policy gradient is always 0 and no learning occurs. (from "Reinforcement learning with random rewards actually works with Qwen 2.5")
14. DeepMath-103K required roughly $138,000 USD and 127,000 GPU hours to build, whereas RLVE-GYM is substantially more cost-efficient to construct. (from "RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments")
15. When applied to Qwen3-4B-Base, RLPT yields absolute improvements of 3.0, 5.1, 8.1, 6.0, 6.6, and 5.3 on MMLU, MMLU-Pro, GPQA-Diamond, KOR-Bench, AIME24, and AIME25 respectively. (from "Reinforcement Learning on Pre-Training Data")

## Relationships

## Limitations and Open Questions

## Sources
