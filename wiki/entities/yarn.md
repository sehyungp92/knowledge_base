---
type: entity
title: YARN
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- finetuning_and_distillation
- generative_media
- model_architecture
- model_commoditization_and_open_source
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00491160460255002
staleness: 0.0
status: active
tags: []
---
# YARN

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

Yet Another RoPE extensioN — a context length extension technique used in Qwen3 during inference to enable sequence lengths beyond the training window.

## Key Findings

1. Qwen3 introduces a thinking budget mechanism that allows users to allocate computational resources adaptively during inference, balancing latency and performance based on task complexity. (from "Qwen3 Technical Report")
2. Qwen3 expands multilingual support from 29 to 119 languages and dialects compared to its predecessor Qwen2.5. (from "Qwen3 Technical Report")
3. Qwen3 is pre-trained on approximately 36 trillion tokens covering 119 languages and dialects. (from "Qwen3 Technical Report")
4. The flagship model Qwen3-235B-A22B achieves 85.7 on AIME'24, 81.5 on AIME'25, 70.7 on LiveCodeBench v5, and 70.8 on BFCL v3. (from "Qwen3 Technical Report")
5. Increasing the thinking budget for thinking tokens leads to consistent improvement in model performance across various tasks. (from "Qwen3 Technical Report")
6. Qwen3 removes QKV-bias used in Qwen2 and introduces QK-Norm to the attention mechanism to ensure stable training. (from "Qwen3 Technical Report")
7. Qwen3 MoE models have 128 total experts with 8 activated experts per token and exclude shared experts, unlike Qwen2.5-MoE. (from "Qwen3 Technical Report")
8. Qwen3 pre-training follows a three-stage process: a general stage on 30T tokens, a reasoning stage on 5T higher-quality tokens, and a long-context stage extending sequence length to 32,768 tokens. (from "Qwen3 Technical Report")
9. Qwen3 optimizes data mixture at the instance level through ablation experiments on small proxy models, unlike prior work that optimizes at the data source or domain level. (from "Qwen3 Technical Report")
10. Qwen3 pre-training data is expanded using Qwen2.5-VL for PDF text extraction and Qwen2.5-Math and Qwen2.5-Coder for synthetic data generation across dozens of domains. (from "Qwen3 Technical Report")
11. Qwen3 MoE base models achieve similar performance to Qwen3 dense base models with only 1/5 of activated parameters. (from "Qwen3 Technical Report")
12. Qwen3 dense base models achieve performance comparable to Qwen2.5 models at significantly higher parameter scales (e.g., Qwen3-8B comparable to Qwen2.5-14B). (from "Qwen3 Technical Report")
13. Qwen3-32B-Base outperforms Qwen2.5-72B-Base in 10 of 15 evaluation benchmarks despite having less than half the parameters. (from "Qwen3 Technical Report")
14. Qwen3-235B-A22B-Base outperforms DeepSeek-V3-Base on 14 of 15 benchmarks with only about 1/3 the total parameters and 2/3 the activated parameters. (from "Qwen3 Technical Report")
15. Qwen3 integrates thinking mode and non-thinking mode into a single unified model, eliminating the need to switch between separate chat and reasoning models. (from "Qwen3 Technical Report")

## Known Limitations

- 128k context window achieved via positional extrapolation (YaRN) rather than native training — model only trained natively at 32k, with long-context capability relying on untrained extrapolation that  (severity: minor, trajectory: stable)

## Relationships

## Limitations and Open Questions

## Sources
