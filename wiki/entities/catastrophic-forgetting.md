---
type: entity
title: Catastrophic Forgetting
entity_type: theory
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- benchmark_design
- chain_of_thought
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- hallucination_and_reliability
- image_generation_models
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- medical_and_biology_ai
- model_architecture
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- scientific_and_medical_ai
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
- unified_multimodal_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 17
sources_since_update: 0
update_count: 1
influence_score: 0.03488842114610083
staleness: 0.0
status: active
tags: []
---
# Catastrophic Forgetting

**Type:** theory
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/image_generation_models|image_generation_models]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A known failure mode in neural network adaptation where learning new tasks degrades performance on previously learned tasks. Identified as a key risk in agent-centric adaptation paradigms.

## Key Findings

1. By freezing text modules and only training image modules, LMFusion preserves language capabilities while developing visual understanding and generation abilities (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
2. The LMFusion framework can be extended to existing vision-language models (VLMs) such as LLaVA-NeXT to add image generation capabilities while preserving multimodal understanding (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
3. Freezing text modules during training eliminates the need to include text-only data in training, significantly reducing computational demands (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
4. Training a state-of-the-art text-only LLM like Llama-3 requires training over 15 trillion tokens (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
5. Learning rate decoupling (ratio 0.1) reduces the language performance gap from 7% to 2% in dense models but comes at the cost of consistently reduced image capabilities (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
6. Deep modality separation (modality-specific FFNs and attention) outperforms shallow separation (modality-specific FFNs only), with both outperforming no separation (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
7. Naive finetuning of pretrained text-only LLMs on multimodal data leads to significant degradation of language processing capabilities (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
8. LMFusion uses modality-specific QKV projections and FFNs to process text and image data independently while shared self-attention allows cross-modal interaction (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
9. LMFusion applies a causal attention mask to text tokens and a bidirectional mask to image tokens in the shared self-attention layer (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
10. LMFusion improves image understanding by 20% and image generation by 3.6% compared to Transfusion while using only 50% of the FLOPs (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
11. LMFusion outperforms Transfusion on language-only tasks by 11.6% due to initialization from Llama-3 (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
12. LMFusion initializes both text-specific and image-specific transformer modules from the pretrained Llama-3 8B model (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
13. LMFusion has twice as many parameters as Transfusion but uses the same FLOPs because only half of the parameters are activated for each input token (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
14. With equal learning rates for text and image components during naive finetuning, HellaSwag performance drops by 15% initially and never recovers to original level, maintaining a persistent 7% gap (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")
15. LMFusion uses a VAE encoder to compress 256x256 images into 32x32x8 tensors, then a 2-block U-Net downsampler reduces them to 256 patches (from "LMFusion: Adapting Pretrained Language Models for Multimodal Generation")

## Capabilities

- Hope model learns two novel languages sequentially in-context with minimal catastrophic forgetting using multi-level memory, while vanilla ICL shows dramatic performance drop in the same continual tra (maturity: research_only)
- Inference-time domain specialization (state-aware reasoning framework) can achieve strong multimodal medical performance without training-time fine-tuning, avoiding catastrophic forgetting while deliv (maturity: research_only)

## Known Limitations

- Domain-specific supervised fine-tuning of foundation models for medical tasks causes catastrophic forgetting, degrading performance on other critical consultation aspects (e.g., management plan approp (severity: significant, trajectory: stable)
- Standard momentum optimizer acts as a low-pass filter that smooths gradient updates without selective retrieval, meaning it cannot recover historically relevant gradient subspace information needed to (severity: significant, trajectory: improving)
- Catastrophic forgetting is not solved — it is a fundamental consequence of compression, where limited network capacity forces the model to forget prior information to retain capacity for new informati (severity: blocking, trajectory: unclear)
- Existing continual learning approaches beyond in-context learning are computationally expensive, require external components, lack generalization, and/or suffer from catastrophic forgetting (severity: significant, trajectory: improving)
- Continual bootstrapping risks catastrophic forgetting during iterative pretraining; the paper required a special warmup-stable-decay (WSD) learning rate schedule and careful initialization to mitigate (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
