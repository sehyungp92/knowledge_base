---
type: entity
title: Direct Preference Optimization
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- hallucination_and_reliability
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
- vertical_ai_and_saas_disruption
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.021186350250704384
staleness: 0.0
status: active
tags: []
---
# Direct Preference Optimization

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

Preference-based fine-tuning method that aligns models with human or automated preference signals without explicit reward modeling.

## Key Findings

1. Effective training samples (those with non-zero advantages) drop dramatically from approximately 60% at training start to under 40% in later phases without SSB. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
2. Skywork R1V2 (38B parameters) achieves 78.9% on AIME2024, 63.6% on LiveCodeBench, 73.6% on MMMU, and 62.6% on OlympiadBench. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
3. R1V2 outperforms Claude 3.5 Sonnet (70.4%), Gemini 2 Flash (70.7%), and Kimi k1.5 longcot (70.0%) on MMMU with a score of 73.6%. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
4. Applying preference optimization to complex multimodal reasoning remains relatively underexplored due to two critical limitations: binary preference pairs fail to capture complex reasoning paths, and  (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
5. R1V2 (38B) outperforms DeepSeek R1 (671B) on LiveBench (73.2% vs 71.6%) and BFCL (66.3% vs 60.3%), suggesting efficient learning with fewer parameters. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
6. Incorporating SSB into the rollout of offline inference in advance as a filtered prompt pool yields over 10% improvement in training efficiency during initial optimization. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
7. MPO reduces repetitive chain-of-thought and overthinking artifacts in model outputs. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
8. Excessive reinforcement signals can induce visual hallucinations in vision-language models. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
9. R1V2 acquires multimodal reasoning skills directly via reinforcement learning without teacher model distillation. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
10. Models optimized heavily for mathematical reasoning often demonstrate degraded performance on everyday visual tasks, while general-purpose models struggle with complex analytical reasoning. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
11. R1V2 eliminates the supervised fine-tuning (SFT) stage, unlike its predecessor R1V1, because SFT can inadvertently undermine subsequent reinforcement learning and reasoning processes. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
12. The GRPO vanishing advantages phenomenon arises when all responses within a query group converge toward uniform correctness or incorrectness, causing relative advantage signals to diminish and impedin (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
13. Capabilities in text and vision exhibit high transferability — improvements in one modality directly benefit the other. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
14. The Selective Sample Buffer (SSB) mechanism addresses the vanishing advantages problem by caching high-quality training examples with non-zero advantages and reintroducing them during policy updates. (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")
15. R1V2 achieves 62.6% on OlympiadBench, substantially outperforming larger models Qwen2.5-VL-72B (40.4%) and QvQ-Preview-72B (33.2%). (from "Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning")

## Relationships

## Limitations and Open Questions

## Sources
