---
type: entity
title: FVD
entity_type: metric
theme_ids:
- audio_and_speech_models
- creative_content_generation
- generative_media
- image_generation_models
- multimodal_models
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0008204406948529209
staleness: 0.0
status: active
tags: []
---
# FVD

> Fréchet Video Distance (FVD) is an evaluation metric for generative video models that measures the statistical distance between distributions of generated and real video features. Analogous to FID for images, it has become a standard benchmark across video generation, world modeling, and multimodal research — but its relationship to human-perceived quality and creative utility remains an open question.

**Type:** metric
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

FVD extends the logic of Fréchet Inception Distance to the temporal domain, embedding videos into a feature space and computing the Fréchet distance between the generated and real distributions. Lower scores indicate that generated video statistics more closely match those of real footage, capturing both visual fidelity and temporal coherence in a single scalar. Because it operates on distributions rather than individual samples, FVD is sensitive to mode collapse and diversity failures — failure modes that per-sample metrics like PSNR or SSIM miss entirely.

Its ubiquity as an evaluation standard reflects a broader challenge in generative media: video quality is harder to quantify than image quality, and human evaluation is expensive and noisy. FVD fills this gap as a tractable proxy, appearing across architectures as different as diffusion transformers, autoregressive world models, and flow-matching frameworks.

## Role in Evaluated Systems

FVD appears as a primary quality signal across a wide range of video generation research. In Movie Gen, it contextualizes the overall video generation quality achieved by Movie Gen Video, which uses a unified architecture treating images as single-frame videos to jointly generate images and video. That system outperforms OpenAI Sora on realness by an 11.62% net win rate beyond two standard deviations — a human evaluation result that FVD scores are expected to correlate with, though the alignment is imperfect.

In world modeling research — particularly Diffusion Models Are Real-Time Game Engines — FVD takes on an additional role as a *consistency* metric: measuring not just whether generated frames look real in isolation, but whether the video as a whole is temporally coherent. This is the setting where FVD's connection to scaling laws is most directly demonstrated.

## Scaling Behaviour

One of FVD's most consequential properties, documented in work on world models, is its *predictable scaling*: FVD for video consistency reliably improves as a function of model size and FLOPs, following smooth power-law curves that enable accurate loss prediction via extrapolation. This makes FVD a practical tool for compute-optimal model planning — researchers can fit scaling curves at smaller model sizes and predict FVD at scales that would be prohibitively expensive to evaluate directly.

This behavior positions FVD alongside perplexity and FID as metrics that scale predictably enough to anchor resource allocation decisions, which is a non-trivial property. Many evaluation metrics saturate, become noisy, or break under distribution shift as models and datasets grow; FVD's demonstrated scaling regularity in at least one setting suggests it captures something structurally stable about video quality.

## Known Limitations and Open Questions

FVD's standing as a standard metric should not be confused with a settled understanding of what it actually measures. Several limitations constrain its interpretive value:

**Preliminary validation at limited scale.** The correlation between FVD and human-perceived creative utility has been established only through a preliminary analysis at a single model size (894M parameters). Whether this relationship holds across architectures, domains, or model scales remains unverified. A metric that correlates well with human judgment at one point on the scaling curve may diverge at others — particularly if the distribution of failure modes shifts with scale.

**Distribution sensitivity.** Like FID, FVD is sensitive to the choice of reference distribution, the feature extractor used, and the number of samples. Results are not always comparable across papers using different evaluation protocols, which complicates the use of published FVD numbers as absolute benchmarks.

**Temporal coherence vs. creative quality.** FVD captures statistical fidelity to real video distributions, but creative video generation — cinematic output, stylized animation, abstract visual storytelling — may deliberately deviate from naturalistic distributions. A model generating highly stylized but coherent and compelling video might score poorly on FVD while being genuinely useful. This gap between distributional fidelity and creative value is not addressed by the metric design.

**Decoupled from audio.** As video generation systems become increasingly multimodal — integrating audio, motion control, and semantic conditioning — FVD remains a purely visual metric. Systems like Movie Gen Audio, which generate synchronized audio alongside video and are evaluated on synchronization and correctness scores (separate from FVD), highlight the incompleteness of any single-modality metric for assessing holistic video generation quality.

## Relationships

FVD is most directly relevant to [[themes/video_and_world_models|video_and_world_models]] and [[themes/generative_media|generative_media]], where it functions as the dominant quantitative benchmark. Its scaling behavior ties it to [[themes/scaling_laws|scaling_laws]] and [[themes/pretraining_and_scaling|pretraining_and_scaling]] research. Systems evaluated with FVD include those from Movie Gen and Diffusion Models Are Real-Time Game Engines, as well as work on human animation scaling from OmniHuman-1. As multimodal video systems mature, FVD's role is likely to shift from primary benchmark to one component of a broader evaluation suite that accounts for audio fidelity, temporal synchronization, and semantic alignment.

## Key Findings

## Limitations and Open Questions

## Sources
