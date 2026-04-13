---
type: entity
title: Qwen2.5
entity_type: entity
theme_ids:
- adaptive_computation
- agent_systems
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- image_generation_models
- knowledge_and_memory
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.004184112620003601
staleness: 0.0
status: active
tags: []
---
# Qwen2.5

**Type:** entity
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A family of open-source AR language models used for continual pretraining into TiDAR 1.5B and as AR baselines. Also used for hardware profiling (Qwen3-32B) to demonstrate free token slot phenomenon.

## Key Findings

1. Janus-style separate-encoder representation does not allow the understanding and generation tasks to benefit each other under joint training. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
2. TA-Tok's LLM-aligned codebook (65K entries, 1536 dim) substantially outperforms a conventional random-initialized low-dimensional codebook (32K entries, 16 dim) on visual understanding tasks. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
3. TA-Tok achieves the highest visual generation performance across all data scales compared to VQVAE, Janus, and Hybrid representations. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
4. TA-Tok nearly matches continuous-semantic representations (Janus) in visual understanding, scoring 93 vs. 94 at 10M data scale. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
5. The Self Reflect strategy, which uses the model's visual understanding capability to assess image-prompt alignment, consistently improves generation quality, especially for weaker/earlier-stage models (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
6. Tar-1.5B achieves a DPG Bench score of 82.96, outperforming Janus-Pro-1B and approaching Janus-Pro-7B. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
7. Tar unifies visual understanding and generation within a single autoregressive MLLM using a fully discrete, shared semantic representation, eliminating the need for modality-specific designs. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
8. Tar achieves GenEval overall scores of 0.76 (1.5B) and 0.84 (7B), surpassing all unified models on the GenEval benchmark. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
9. Using a shared visual representation (VQVAE or TA-Tok) enables understanding and generation to mutually benefit each other, yielding ~8.1% and ~5.3% improvement respectively in generation when trained (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
10. The Hybrid tokenizer (joint pixel reconstruction + semantic alignment) does not scale effectively with increasing data, unlike TA-Tok. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
11. TA-Tok converts images into discrete tokens using a text-aligned codebook initialized from a large language model's vocabulary via a learnable projection matrix, while keeping LLM embeddings frozen. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
12. Scale-Adaptive Pooling at 729 tokens yields the best visual understanding performance, while 169 tokens are sufficient for text-to-image generation. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
13. The LLM token embeddings in TA-Tok's codebook are always frozen; only the projection matrix W is trained. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
14. Tar-7B matches the performance of Janus-Pro-7B, a state-of-the-art continuous-token model, on visual understanding benchmarks. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")
15. Initializing MLLM embeddings with the TA-Tok codebook outperforms both random initialization and a separate pre-alignment stage using 25M data, matching pre-align with 75M+ data. (from "Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations")

## Relationships

## Limitations and Open Questions

## Sources
