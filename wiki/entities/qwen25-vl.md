---
type: entity
title: Qwen2.5-VL
entity_type: entity
theme_ids:
- agent_systems
- audio_and_speech_models
- benchmark_design
- chain_of_thought
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- image_generation_models
- long_context_and_attention
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- search_and_tree_reasoning
- spatial_and_3d_intelligence
- synthetic_data_generation
- tool_use_and_agent_protocols
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.006897523447455795
staleness: 0.0
status: active
tags: []
---
# Qwen2.5-VL

**Type:** entity
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

The base vision-language model used as the foundation for Robix. Available in 7B and 32B parameter sizes; Robix is developed by continually training Qwen2.5-VL-7B and 32B on approximately 200 billion tokens.

## Key Findings

1. Robix-32B exceeds Gemini-2.5-Pro by 3.0 and 11.8 percentage points in accuracy on two out-of-distribution benchmark settings. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
2. In real-world evaluations, Robix-32B surpasses Gemini-2.5-Pro by 1.6 and 4.3 percentage points on task progress and outperforms all other baselines by 28.1–64.6 percentage points. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
3. Robix's pretraining uses a full cosine learning rate schedule starting at 1e-5 and decaying to 1e-6 with AdamW optimizer. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
4. Robix uses Seed-1.5-VL-thinking to generate step-by-step thought traces for task-centric reasoning QA pairs to enable deliberate high-level decision-making. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
5. Robix uses a three-stage training strategy: continued pretraining for embodied reasoning, supervised finetuning for interactive capabilities, and reinforcement learning for reasoning-action consistenc (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
6. Robix models interactive task execution as a unified reasoning-action sequence where each step predicts thought, action, and optional verbal response conditioned on current observations, user instruct (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
7. The 3D spatial understanding pretraining corpus for Robix contains over 30 million instruction pairs (~40B tokens) spanning five task types: multi-view correspondence, 3D bounding box detection, relat (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
8. Robix introduces novel capabilities including proactive dialogue, real-time interruption handling, and context-aware commonsense reasoning during task execution. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
9. Robix is a unified vision-language model that integrates robot reasoning, task planning, and natural language interaction within a single architecture, acting as the high-level cognitive layer in a hi (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
10. Robix is trained on approximately 200 billion tokens using a three-stage training pipeline, developing both 7B and 32B parameter variants based on Qwen2.5-VL. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
11. The visual grounding dataset for Robix pretraining contains over 50 million instruction-response pairs (~70B tokens), covering 2D bounding box annotations, point annotations, counting, and visual prom (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
12. The task-centric reasoning pretraining dataset contains over 5 million examples (~10B tokens) targeting task status verification, action affordance, and next action prediction. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
13. Robix outperforms both open-source and commercial baselines including GPT-4o and Gemini 2.5 Pro in interactive task execution. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
14. Robix is evaluated on five real-world scenarios (table bussing, grocery shopping, checkout packing, tableware organization & shipment, dietary filtering) under both human teleoperation and automatic V (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")
15. Robix retains only the latest N visual observations as explicit input to balance memory usage and maintain inference efficiency under a 32k token context length budget. (from "Robix: A Unified Model for Robot Interaction, Reasoning and Planning")

## Relationships

## Limitations and Open Questions

## Sources
