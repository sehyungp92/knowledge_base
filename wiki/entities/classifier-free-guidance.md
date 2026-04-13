---
type: entity
title: Classifier-Free Guidance
entity_type: method
theme_ids:
- adaptive_computation
- creative_content_generation
- finetuning_and_distillation
- generative_media
- image_generation_models
- latent_reasoning
- long_context_and_attention
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.008589829766927204
staleness: 0.0
status: active
tags: []
---
# Classifier-Free Guidance

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/creative_content_generation|creative_content_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

Inference technique used in MMaDA's image generation to improve text-image alignment by combining conditional and unconditional model predictions. Applied with guidance scale 3.5.

## Key Findings

1. Text-to-image generation rewards combine a CLIP Reward (measuring text-image alignment) and an ImageReward (reflecting human preference scores), both scaled by 0.1 (from "MMaDA: Multimodal Large Diffusion Language Models")
2. MMaDA excels over SDXL and Janus in text-to-image generation (from "MMaDA: Multimodal Large Diffusion Language Models")
3. MMaDA-8B surpasses LLaMA-3-7B and Qwen2-7B in textual reasoning (from "MMaDA: Multimodal Large Diffusion Language Models")
4. Show-o and Transfusion combine autoregressive and diffusion modeling for text and visual semantics respectively within a shared architecture (from "MMaDA: Multimodal Large Diffusion Language Models")
5. MMaDA uses discrete tokenization for both text and image modalities, enabling a single unified masked-token-prediction modeling objective (from "MMaDA: Multimodal Large Diffusion Language Models")
6. Image tokenization based on MAGVIT-v2 converts a 512×512 pixel image into a sequence of 1024 discrete tokens using a downsampling factor of 16 and a codebook size of 8192 (from "MMaDA: Multimodal Large Diffusion Language Models")
7. MMaDA formulates both image and text generation as a mask token prediction problem, predicting all masked tokens simultaneously under a unified cross-entropy loss (from "MMaDA: Multimodal Large Diffusion Language Models")
8. MMaDA outperforms Show-o and SEED-X in multimodal understanding (from "MMaDA: Multimodal Large Diffusion Language Models")
9. Adapting autoregressive GRPO to diffusion models faces three critical challenges: local masking dependency, mask ratio sensitivity, and non-autoregressive sequence-level likelihoods (from "MMaDA: Multimodal Large Diffusion Language Models")
10. LLaDA employs Monte Carlo sampling over 128 mask ratios for on-policy RL, incurring high computational costs (from "MMaDA: Multimodal Large Diffusion Language Models")
11. The d1 approach to diffusion RL fixes the mask ratio and randomizes question masking, reducing noise diversity and ignoring the multi-step denoising nature of diffusion models (from "MMaDA: Multimodal Large Diffusion Language Models")
12. UniGRPO uses a structured noising strategy where masking ratio is sampled uniformly to expose the model to various stages of the diffusion denoising process (from "MMaDA: Multimodal Large Diffusion Language Models")
13. UniGRPO approximates sequence-level log-likelihood by averaging over masked tokens rather than accumulating token-level probabilities via a chain rule (from "MMaDA: Multimodal Large Diffusion Language Models")
14. Textual reasoning RL uses a Correctness Reward of 2.0 for a correct answer and a Format Reward of 0.5 for correct formatting, trained on GSM8K (from "MMaDA: Multimodal Large Diffusion Language Models")
15. For text generation inference, MMaDA uses sequence length 1024 with 512 denoising steps divided into 64-token blocks, unmasking the 2 lowest-confidence tokens per step (from "MMaDA: Multimodal Large Diffusion Language Models")

## Relationships

## Limitations and Open Questions

## Sources
