---
type: entity
title: MMLU
entity_type: metric
theme_ids:
- adaptive_computation
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- continual_learning
- finetuning_and_distillation
- generative_media
- hallucination_and_reliability
- image_generation_models
- interpretability
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- mechanistic_interpretability
- model_architecture
- model_behavior_analysis
- model_commoditization_and_open_source
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- representation_learning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.007849072148425056
staleness: 0.0
status: active
tags: []
---
# MMLU

**Type:** metric
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/image_generation_models|image_generation_models]], [[themes/interpretability|interpretability]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/representation_learning|representation_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

Measuring Massive Multitask Language Understanding benchmark; widely-cited evaluation using binary grading with no credit for uncertainty expressions, creating incentives for confident guessing over calibrated abstention.

## Key Findings

1. Training unified multimodal models from scratch requires immense computation; Transfusion was trained on 2T tokens. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
2. Training on noisy images for I2T (understanding) tasks degrades image understanding performance, with more noise causing greater degradation. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
3. X-Fusion's dual-tower design is flexible and can be extended to additional modalities (e.g., audio) by introducing dedicated modality-specific towers. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
4. Training on clean images for image-to-text (understanding) samples improves both image understanding and image generation performance simultaneously. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
5. Dual Tower achieves FID of 14.20 vs Single Tower's 19.10, Gated Tower's 24.51, and Dual Projection's 20.22, with all methods maintaining LLaMA 32.2 MMLU except Single Tower. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
6. The dual-tower design maintains the same attention FLOPs as single-tower alternatives by omitting cross-modal query computation in each tower. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
7. Gated Tower architecture performs worst among all tested architectures on both image generation and understanding tasks. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
8. Feature alignment with pretrained CLIP representations (REPA) accelerates convergence for smaller models (1B, 3B) but provides diminishing benefit at larger scales (8B). (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
9. X-Fusion's dual-tower architecture keeps LLM parameters frozen while introducing a separate trainable vision tower, preserving original language capabilities. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
10. Dual Tower achieves 23% lower FID than Single Tower while maintaining the same number of training parameters. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
11. X-Fusion achieves competitive training efficiency, processing only 0.08T tokens compared to Transfusion's 2T tokens. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
12. Vision tower blocks in X-Fusion are initialized by copying parameters from corresponding language transformer layers. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
13. Fine-tuning the LLM backbone (Single Tower) causes catastrophic forgetting, dropping MMLU from 32.2 to 25.0 (chance-level for 4-choice MCQ). (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
14. X-Fusion uses LLaMA-3 family as pretrained LLMs and flow matching scheduler following Stable Diffusion 3 for training. (from "X-Fusion: Introducing New Modality to Frozen Large Language Models")
15. Decoder Transformers do not make explicit latent decisions about the stream of symbols to generate; their only decisions are the choices of the tokens themselves. (from "The Free Transformer")

## Known Limitations

- MMLU-STEM performance across BoLT iterations fell within noise floor (< 28%), revealing that extended math-focused pretraining actively degrades general STEM knowledge; general domain NLL on DCLM corp (severity: significant, trajectory: worsening)

## Relationships

## Limitations and Open Questions

## Sources
