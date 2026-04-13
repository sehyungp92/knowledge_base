---
type: entity
title: Diffusion Transformer (DiT)
entity_type: method
theme_ids:
- audio_and_speech_models
- creative_content_generation
- generative_media
- model_architecture
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.004660281760057527
staleness: 0.0
status: active
tags: []
---
# Diffusion Transformer (DiT)

**Type:** method
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

A Transformer architecture for diffusion models with bidirectional attention. Predicts noise rather than energy, cannot give unnormalized likelihood estimates at each denoising step, relies on a fixed denoising schedule, and requires external verifiers for System 2 Thinking beyond increasing denoising steps.

## Key Findings

1. Movie Gen Audio fine-tuning runs for 50K updates over 1 day on 64 GPUs with an effective batch size of 256 sequences. (from "Movie Gen: A Cast of Media Foundation Models")
2. Audio data is classified along two axes: audio type (voice, non-vocal music, general sound) and diegetic vs. non-diegetic, using AED and CAVTP models for automatic classification. (from "Movie Gen: A Cast of Media Foundation Models")
3. Movie Gen Audio represents 48kHz audio as compact 1D latent features at 25Hz frame rate using a DAC-VAE model, providing a lower frame rate than Encodec (75Hz→25Hz) and higher audio sampling rate (24k (from "Movie Gen: A Cast of Media Foundation Models")
4. The Movie Gen Audio DiT model has 36 layers with 4,608/18,432 attention/feed-forward dimensions, totaling 13B parameters (excluding Long-prompt MetaCLIP, T5, and DAC-VAE). (from "Movie Gen: A Cast of Media Foundation Models")
5. Movie Gen Audio outperforms all baselines on all metrics with large margins: 33.8% to 72.8% on synchronization, 27.5% to 82.2% on correctness, and 31.3% to 91.0% on overall quality for generated video (from "Movie Gen: A Cast of Media Foundation Models")
6. Text prompts can effectively guide the model to generate desired sound effects, increasing CLAP score from 0.21 (no text) to 0.37 (with text). (from "Movie Gen: A Cast of Media Foundation Models")
7. Movie Gen Audio uses flow-matching based generative models combined with a diffusion transformer (DiT) architecture for audio generation. (from "Movie Gen: A Cast of Media Foundation Models")
8. Movie Gen Video significantly outperforms OpenAI Sora on realness with an 11.62% net win rate beyond 2 standard deviations, and moderately wins on aesthetics with 6.45%. (from "Movie Gen: A Cast of Media Foundation Models")
9. Treating images as single-frame videos enables a single model to generate both images and videos using the same architecture. (from "Movie Gen: A Cast of Media Foundation Models")
10. Long-prompt MetaCLIP is used to extract 1024-dimensional embeddings per video frame, with the resampled sequence projected and added frame-by-frame to audio features for conditioning. (from "Movie Gen: A Cast of Media Foundation Models")
11. T5-base encodes audio captions into 768-dimensional features with sequence length capped at 512 tokens, and is injected via cross-attention layers in each DiT transformer block. (from "Movie Gen: A Cast of Media Foundation Models")
12. Movie Gen Audio pre-training runs for 500K updates over 14 days on 384 GPUs with an effective batch size of 1,536 sequences capped at 30 seconds each. (from "Movie Gen: A Cast of Media Foundation Models")
13. Audio extension is achieved by training the model with masked audio prediction, enabling generation, bidirectional extension, and infilling from a single model. (from "Movie Gen: A Cast of Media Foundation Models")
14. Fine-tuning data includes O(100K) cinematic video samples (O(1K) hours) and O(1M) high-quality audio samples (O(10K) hours), mixed at a 10:1 ratio during training. (from "Movie Gen: A Cast of Media Foundation Models")
15. Movie Gen Audio Bench is a new benchmark of 527 AI-generated videos covering 36 audio categories and 434 concepts, serving as the first large-scale synthetic benchmark for video-to-audio generation ev (from "Movie Gen: A Cast of Media Foundation Models")

## Relationships

## Limitations and Open Questions

## Sources
