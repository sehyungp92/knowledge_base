---
type: entity
title: Speculative Decoding
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- chain_of_thought
- context_engineering
- interpretability
- knowledge_and_memory
- model_architecture
- model_behavior_analysis
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.003949263153105743
staleness: 0.0
status: active
tags: []
---
# Speculative Decoding

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

An inference acceleration technique where a smaller draft model generates candidate tokens which are then validated by a larger base model via modified rejection sampling. Accelerates generation but is limited by draft model quality and sequential drafting-verification.

## Key Findings

1. Conventional auxiliary loss solutions for MoE load balancing impair model performance when the loss is too large (from "DeepSeek-V3 Technical Report")
2. DeepSeek-V3 employs node-limited routing ensuring each token is sent to at most 4 nodes, enabling near-full computation-communication overlap in MoE training (from "DeepSeek-V3 Technical Report")
3. DeepSeek-V3 is a Mixture-of-Experts model with 671B total parameters and 37B activated per token (from "DeepSeek-V3 Technical Report")
4. DeepSeek-V3 is the top-performing model for coding competition benchmarks including LiveCodeBench (from "DeepSeek-V3 Technical Report")
5. DeepSeek-V3 pre-training was remarkably stable with no irrecoverable loss spikes or rollbacks (from "DeepSeek-V3 Technical Report")
6. Training DeepSeek-V3 on each trillion tokens requires only 180K H800 GPU hours (3.7 days on 2048 H800 GPUs) (from "DeepSeek-V3 Technical Report")
7. DeepSeek-V3 scores 88.5 on MMLU, 75.9 on MMLU-Pro, and 59.1 on GPQA, outperforming all other open-source models (from "DeepSeek-V3 Technical Report")
8. DeepSeek-V3 full training requires only 2.788M H800 GPU hours (from "DeepSeek-V3 Technical Report")
9. DeepSeek-V3 pre-training on 14.8T tokens costs 2.664M H800 GPU hours and was completed in less than two months (from "DeepSeek-V3 Technical Report")
10. DeepSeek-V3 outperforms all other open-source models and achieves performance comparable to GPT-4o and Claude-3.5-Sonnet (from "DeepSeek-V3 Technical Report")
11. DeepSeekMoE uses finer-grained experts and isolates some experts as shared ones, compared with traditional MoE architectures like GShard (from "DeepSeek-V3 Technical Report")
12. Total training cost of DeepSeek-V3 is approximately $5.576M at $2/GPU-hour rental rates (from "DeepSeek-V3 Technical Report")
13. MLA also performs low-rank compression on attention queries to reduce activation memory during training (from "DeepSeek-V3 Technical Report")
14. The core of MLA is low-rank joint compression of attention keys and values to reduce KV cache during inference (from "DeepSeek-V3 Technical Report")
15. MTP modules can be discarded during inference, allowing the main model to function independently, or repurposed for speculative decoding to improve generation latency (from "DeepSeek-V3 Technical Report")

## Relationships

## Limitations and Open Questions

## Sources
