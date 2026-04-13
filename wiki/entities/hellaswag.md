---
type: entity
title: HellaSwag
entity_type: dataset
theme_ids:
- agent_memory_systems
- continual_learning
- finetuning_and_distillation
- generative_media
- image_generation_models
- interpretability
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- mechanistic_interpretability
- model_architecture
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0028354365602462897
staleness: 0.0
status: active
tags: []
---
# HellaSwag

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/representation_learning|representation_learning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A zero-shot commonsense reasoning benchmark used in Titans/MIRAS evaluation.

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

## Relationships

## Limitations and Open Questions

## Sources
