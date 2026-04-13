---
type: entity
title: Fréchet Video Distance (FVD)
entity_type: metric
theme_ids:
- creative_content_generation
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- robotics_and_embodied_ai
- robot_learning
- synthetic_data_generation
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0006555960196617512
staleness: 0.0
status: active
tags: []
---
# Fréchet Video Distance (FVD)

> Fréchet Video Distance (FVD) is the de facto standard metric for evaluating the quality of generated video, extending the logic of FID (Fréchet Inception Distance) from images to the temporal domain. By comparing the statistical distributions of real and generated videos in a learned feature space, FVD captures both visual fidelity and temporal coherence — making it an essential benchmark signal as video generation has matured into a core capability across robotics, embodied AI, and generative media.

**Type:** metric
**Themes:** [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

FVD adapts the Fréchet distance — a measure of similarity between two probability distributions modelled as multivariate Gaussians — to video by embedding clips through a temporally-aware feature extractor (typically a network pre-trained on action recognition, such as I3D). The mean and covariance of these embeddings are computed separately for a real-video reference set and a set of generated samples; FVD is the Fréchet distance between those two Gaussians. Lower values indicate that the generated distribution more closely matches the real one, both in average appearance and in variance across samples.

Because it operates at the distribution level rather than on individual clips, FVD is sensitive to mode collapse (generated videos that are high quality but lack diversity) and to systematic temporal artifacts (flickering, motion inconsistency) that per-frame metrics like PSNR or SSIM would miss.

## Role in Video Generation Evaluation

FVD has become the primary headline number for comparing video generation systems, appearing consistently in evaluations of world foundation models like Cosmos and action-world models like WorldVLA. In these contexts it is rarely used alone — it is paired with task-specific geometric or physical consistency metrics that FVD cannot directly capture.

For Cosmos, multi-view geometry consistency is assessed through Temporal Sampson Error and Cross-view Sampson Error, while trajectory consistency is measured via TAE-ATE and RPE-t against real-world video reference baselines. Cosmos-Predict1-7B post-trained models achieve trajectory consistency (TAE-ATE 0.54) approaching real-world video (TAE-ATE 0.49), far surpassing VideoLDM-MultiView (TAE-ATE 0.88) — results that complement whatever FVD scores are reported by grounding quality claims in physically interpretable quantities.

This pairing reveals a structural limitation of FVD: it is agnostic to the *physical plausibility* of motion. A model could achieve a good FVD by producing visually convincing but physically incoherent motion trajectories. For robotics and embodied AI applications — where generated video must serve as a credible world model for downstream planning — supplementary metrics are not optional.

## Limitations and Open Questions

**Feature extractor dependency.** FVD scores are only as meaningful as the embedding space used. I3D was trained on human action recognition datasets; its feature space may not be well-calibrated for industrial, robotic, or synthetic-domain video, which is precisely the content targeted by physical AI systems like Cosmos. This creates a potential mismatch between FVD rankings and downstream utility.

**Distribution size sensitivity.** Reliable Gaussian parameter estimation requires large sample sets. Reported FVD scores are often computed on a few hundred to a few thousand clips, making them noisy and difficult to compare across papers that use different sample counts or reference sets.

**No temporal grounding.** FVD captures that generated and real distributions differ temporally, but not *how* or *why*. A model with poor multi-view consistency (Cross-view Sampson Error 6.48 for VideoLDM-MultiView vs. 2.11 for Cosmos) may still produce an FVD competitive with a geometrically accurate model if the overall appearance distribution is similar.

**Mode collapse is only partially visible.** FVD penalises low variance in the generated distribution, but it is not robust to subtle forms of diversity collapse where the model generates plausible-looking but semantically homogeneous video.

**Conditioning quality is invisible.** Whether a generated video faithfully follows a text prompt, trajectory condition, or action sequence cannot be assessed by FVD at all. For conditioned generation — which is the dominant paradigm in world models — FVD must be supplemented by conditional alignment metrics.

## Connections

FVD sits at the intersection of [[themes/video_and_world_models|video and world models]] and [[themes/synthetic_data_generation|synthetic data generation]]: a model must score well on FVD to be plausible as a data source, but passing FVD does not guarantee the synthetic data will improve downstream task performance. This gap between distributional realism and functional utility is an open research problem across robotics, VLA training (see WorldVLA), and gameplay ideation (see World and Human Action Models towards gameplay ideation). The field is actively exploring whether richer metrics — physics-aware, goal-conditioned, or human-preference-based — should replace or augment FVD as the primary evaluation signal for the next generation of video foundation models.

## Key Findings

## Relationships

## Sources
