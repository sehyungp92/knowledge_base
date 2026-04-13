---
type: entity
title: Diffusion Transformer
entity_type: method
theme_ids:
- audio_and_speech_models
- creative_content_generation
- finetuning_and_distillation
- generative_media
- image_generation_models
- latent_reasoning
- model_architecture
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- scaling_laws
- transformer_alternatives
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.004403302599215316
staleness: 0.0
status: active
tags: []
---
# Diffusion Transformer

**Type:** method
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/creative_content_generation|creative_content_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/representation_learning|representation_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

A generative architecture combining transformer attention with diffusion-based training for high-quality video or image generation, used as the backbone of Wan2.1 and PAN's video diffusion decoder.

## Key Findings

1. The Multi-Scale Representation Alignment strategy uses a scale-wise consistency loss that aligns intermediate DiT backbone hidden states with final semantic representations via MSE minimization. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
2. Multi-Scale Learnable Query Tokens are designed to capture image information at three granularity levels: global layout (4x4), major objects and mid-level structures (8x8), and fine textures and detai (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
3. Among unified understanding-and-generation models on GenEval, Janus-Pro-1B achieves 0.73 overall accuracy, outperforming Ming-Lite-Uni's 0.62. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
4. Ming-Lite-Uni integrates a FlowMatching loss directly into a separate diffusion model, allowing generation quality to improve in tandem with end-to-end training while keeping the MLLM frozen. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
5. Training data filtering applies aspect ratio (≤2.5), watermark detection (≤0.5), and CLIP alignment (≥0.45) thresholds. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
6. To reduce the length of visual tokens, Ming-Lite-Uni concatenates adjacent 2×2 image tokens into a single token and uses an MLP to reduce the dimension, downsampling the visual representation. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
7. Ming-Lite-Uni fixes the MLLM and fine-tunes the diffusion model through multi-scale learnable tokens, multi-scale representation alignment, and a connector, unlike prior works that focused on understa (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
8. Ming-Lite-Uni compresses image representations into a sequence of continuous tokens, which are combined with discrete text tokens and processed by a scaled auto-regressive Transformer. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
9. Ming-Lite-Uni replaces the original 1D-RoPE in Llama with M-RoPE to enable unified positional encoding across textual, image, video, and audio modalities and generalization to longer sequences. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
10. Scale boundary markers (START and END learnable tokens) are prepended and appended to each scale's query tokens to preserve scale-specific semantics in the multi-scale token sequence. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
11. Ming-Lite-Uni enables native multimodal AR models to perform both text-to-image generation and instruction-based image editing tasks by leveraging a fixed MLLM and a learnable diffusion model. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
12. Ming-Lite-Uni's M2-omni LLM is initialized with pre-trained weights from the Llama3 series, specifically Llama3.1-8B or Llama3.3-70B. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
13. Ming-Lite-Uni is an open-source multimodal framework featuring a unified visual generator and a native multimodal autoregressive model for unifying vision and language. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
14. Style transfer training data includes a high-quality subset of WikiArt covering 27 painting styles and StyleBooth featuring 67 styles, totaling 81,444 and 80,922 samples respectively. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")
15. Ming-Lite-Uni uses NaViT as its vision encoder, capable of processing images of arbitrary resolution. (from "Ming-Lite-Uni: Advancements in Unified Architecture for Natural Multimodal Interaction")

## Capabilities

- Dual-system VLA architecture generates closed-loop motor actions at 120Hz (System 1 diffusion transformer) conditioned on scene understanding computed at 10Hz (System 2 VLM), with 63.9ms inference for (maturity: narrow_production)

## Relationships

## Limitations and Open Questions

## Sources
