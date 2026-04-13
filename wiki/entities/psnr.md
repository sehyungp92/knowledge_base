---
type: entity
title: PSNR
entity_type: metric
theme_ids:
- finetuning_and_distillation
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- spatial_and_3d_intelligence
- synthetic_data_generation
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.002024271016105347
staleness: 0.0
status: active
tags: []
---
# PSNR

> Peak Signal-to-Noise Ratio (PSNR) is a logarithmic metric that quantifies reconstruction fidelity by measuring the ratio of maximum possible signal power to the power of corrupting noise. Ubiquitous across image compression, video synthesis, neural rendering, and generative model evaluation, PSNR provides a fast, deterministic baseline for comparing reconstruction quality — though its correlation with human perception remains contested, a tension that has grown more visible as generative models produce outputs that look compelling yet score poorly, or score well yet appear blurry.

**Type:** metric
**Themes:** [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/generative_media|Generative Media]], [[themes/image_generation_models|Image Generation Models]], [[themes/multimodal_models|Multimodal Models]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]], [[themes/robot_learning|Robot Learning]], [[themes/spatial_and_3d_intelligence|Spatial and 3D Intelligence]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/unified_multimodal_models|Unified Multimodal Models]], [[themes/video_and_world_models|Video and World Models]], [[themes/vision_language_action_models|Vision-Language-Action Models]]

## Overview

PSNR is computed as `10 · log₁₀(MAX² / MSE)`, where MAX is the maximum pixel value and MSE is mean squared error between the reference and reconstructed signal. Higher values indicate lower distortion: values above ~40 dB are generally considered high fidelity, while values around 30 dB are roughly comparable to lossy JPEG compression. Because it operates pixel-wise, PSNR is blind to structural or perceptual similarity — a globally shifted or blurred image may score comparably to a sharper but locally different one.

In the context of generative world models, neural video synthesis, and embodied AI, PSNR serves as a lower-bound sanity check rather than a definitive quality signal. It is fast to compute, differentiable proxies exist, and it provides a common anchor for cross-paper comparison — but it is routinely supplemented by SSIM, LPIPS, and human evaluation studies precisely because these capture dimensions PSNR misses.

## Key Findings

### PSNR as Anchor for Neural Game Simulation

The most prominent direct use of PSNR in this body of work comes from Diffusion Models Are Real-Time Game Engines, which introduces GameNGen — the first game engine driven entirely by a neural model. GameNGen's next-frame prediction achieves **a PSNR of 29.4**, a figure the authors explicitly benchmark against lossy JPEG compression to contextualise what that number means perceptually. This calibration move is revealing: the authors are acknowledging that PSNR alone is insufficient, and anchoring it to a familiar compression artefact helps readers develop intuition for the reconstruction quality. The fact that human raters perform only slightly better than chance when distinguishing GameNGen clips from real DOOM footage — even after five minutes of auto-regressive rollout — suggests that 29.4 dB, while modest by restoration standards, is sufficient for perceptual plausibility in this domain.

This dissociation between PSNR score and human judgement is a recurring theme. A metric that signals "comparable to JPEG" would, in most imaging contexts, indicate visible quality loss; yet in the context of a neural world model generating complex game state (health tallies, enemy damage, door interactions) at 20 frames per second on a single TPU, it represents a meaningful achievement. The gap between metric and perception highlights a fundamental limitation of PSNR when applied to generative rather than reconstructive tasks.

### Auto-Regressive Degradation and Metric Behaviour

GameNGen's training also surfaces an important failure mode relevant to PSNR interpretation in sequential generation settings. Without noise augmentation during training, auto-regressive generation quality degrades rapidly after 20–30 steps — a degradation that manifests both visually and in metric terms. The instability arises because auto-regressive conditioning compounds small errors across frames, leading to sampling divergence. PSNR, being a per-frame metric, captures this degradation frame-by-frame but does not directly model temporal coherence or error accumulation dynamics. This means a model can maintain acceptable per-frame PSNR while still exhibiting visible drift over longer trajectories — a limitation that motivates complementary temporal metrics and the noise augmentation strategy GameNGen employs.

### Breadth of Application Across Sources

Beyond GameNGen, PSNR appears as an evaluation axis across a wide range of work in this library: physics-informed embodied world models (RoboScape), autoregressive action world models (WorldVLA), large-scale physical AI foundation models (Cosmos), latent-action world models (AdaWorld), and unified vision tokenisation (AToken). This breadth reflects PSNR's role as a baseline lingua franca across subfields — it is cheap enough to report universally and interpretable enough to anchor comparisons, even when it is not the primary evaluation signal.

## Limitations and Open Questions

PSNR's core weakness is its indifference to human perception. Blurry reconstructions that minimise MSE often score higher than sharper, more structured outputs with localised errors. In generative settings — where the model is not constrained to reproduce a single ground-truth output — the metric becomes even more problematic: a diverse, high-quality sample from a diffusion model may score poorly against a single reference simply because it chose a different but equally valid realisation.

There is also the question of **what PSNR measures in auto-regressive world models specifically**. When frames are generated conditioned on past generations rather than ground-truth observations, PSNR against real game footage conflates two distinct sources of error: reconstruction quality (how well the model renders a given state) and trajectory divergence (how far the simulated trajectory has drifted from the reference). Disentangling these requires held-out trajectory alignment, which is rarely reported.

Finally, PSNR's prevalence across such disparate domains — from game simulation to robot learning to 3D reconstruction — raises the question of whether a single scalar metric can remain meaningful across contexts with fundamentally different perceptual tolerances and task requirements. The field's increasing reliance on LPIPS, FID, and human preference studies alongside PSNR suggests an implicit acknowledgement that it cannot, though the metric's computational simplicity ensures it will remain a fixture of evaluation suites for the foreseeable future.

## Relationships

PSNR is closely related to **SSIM** (Structural Similarity Index), which addresses some of its perceptual limitations by incorporating luminance, contrast, and structural comparisons, and to **LPIPS** (Learned Perceptual Image Patch Similarity), which uses deep feature activations to better align with human judgement. In the video domain, it connects to **FVD** (Fréchet Video Distance) as a complementary temporal quality signal.

Within this library, PSNR connects most directly to the [[themes/video_and_world_models|Video and World Models]] theme through GameNGen's simulation quality results, and to [[themes/spatial_and_3d_intelligence|Spatial and 3D Intelligence]] through its use in NeRF and 3D reconstruction evaluation. Its appearance in [[themes/vision_language_action_models|Vision-Language-Action Models]] and [[themes/robotics_and_embodied_ai|Robotics]] contexts reflects the growing overlap between video prediction quality and downstream policy performance — a connection that remains underexplored: it is not yet clear how PSNR of world model predictions correlates with robot task success rates.

## Sources
