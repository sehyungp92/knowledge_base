---
type: entity
title: Group Relative Policy Optimization (GRPO)
entity_type: method
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- chain_of_thought
- context_engineering
- finetuning_and_distillation
- generative_media
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
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
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- test_time_learning
- tool_use_and_agent_protocols
- video_and_world_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 18
sources_since_update: 0
update_count: 1
influence_score: 0.01254146733069925
staleness: 0.0
status: active
tags: []
---
# Group Relative Policy Optimization (GRPO)

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A policy gradient RLVR method that estimates advantages from sparse outcome rewards relative to a group of rollouts for the same question. Used as the primary baseline in this paper.

## Key Findings

1. DeepSeek-V3 scores 88.5 on MMLU, 75.9 on MMLU-Pro, and 59.1 on GPQA, outperforming all other open-source models (from "DeepSeek-V3 Technical Report")
2. DeepSeek-V3 employs node-limited routing ensuring each token is sent to at most 4 nodes, enabling near-full computation-communication overlap in MoE training (from "DeepSeek-V3 Technical Report")
3. MLA also performs low-rank compression on attention queries to reduce activation memory during training (from "DeepSeek-V3 Technical Report")
4. DeepSeek-V3 pre-training was remarkably stable with no irrecoverable loss spikes or rollbacks (from "DeepSeek-V3 Technical Report")
5. DeepSeek-V3 pre-training on 14.8T tokens costs 2.664M H800 GPU hours and was completed in less than two months (from "DeepSeek-V3 Technical Report")
6. Conventional auxiliary loss solutions for MoE load balancing impair model performance when the loss is too large (from "DeepSeek-V3 Technical Report")
7. Total training cost of DeepSeek-V3 is approximately $5.576M at $2/GPU-hour rental rates (from "DeepSeek-V3 Technical Report")
8. DeepSeekMoE uses finer-grained experts and isolates some experts as shared ones, compared with traditional MoE architectures like GShard (from "DeepSeek-V3 Technical Report")
9. The core of MLA is low-rank joint compression of attention keys and values to reduce KV cache during inference (from "DeepSeek-V3 Technical Report")
10. Training DeepSeek-V3 on each trillion tokens requires only 180K H800 GPU hours (3.7 days on 2048 H800 GPUs) (from "DeepSeek-V3 Technical Report")
11. DeepSeek-V3 full training requires only 2.788M H800 GPU hours (from "DeepSeek-V3 Technical Report")
12. DeepSeek-V3 is a Mixture-of-Experts model with 671B total parameters and 37B activated per token (from "DeepSeek-V3 Technical Report")
13. DeepSeek-V3 outperforms all other open-source models and achieves performance comparable to GPT-4o and Claude-3.5-Sonnet (from "DeepSeek-V3 Technical Report")
14. DeepSeek-V3 is the top-performing model for coding competition benchmarks including LiveCodeBench (from "DeepSeek-V3 Technical Report")
15. MTP modules can be discarded during inference, allowing the main model to function independently, or repurposed for speculative decoding to improve generation latency (from "DeepSeek-V3 Technical Report")

## Relationships

## Limitations and Open Questions

## Sources
