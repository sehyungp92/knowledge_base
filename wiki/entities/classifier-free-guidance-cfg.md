---
type: entity
title: Classifier-Free Guidance (CFG)
entity_type: method
theme_ids:
- audio_and_speech_models
- creative_content_generation
- generative_media
- image_generation_models
- model_architecture
- multimodal_models
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0008774862670162062
staleness: 0.0
status: active
tags: []
---
# Classifier-Free Guidance (CFG)

> Classifier-free guidance is a conditioning technique that improves the quality and fidelity of conditional generative models by implicitly learning an unconditional baseline alongside the conditional model, then interpolating — or extrapolating — between them at inference time. Originally formulated as an inference-time trade-off between sample quality and diversity, CFG has become a cornerstone of modern diffusion and flow-based generative systems, and recent work on Generative Modeling via Drifting has challenged its conventional framing by moving it entirely into training.

**Type:** method
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

In its canonical form, CFG operates at inference time: a model trained jointly on conditional and unconditional objectives produces two score estimates per denoising step, and the guidance scale interpolates between them to sharpen conditioning at the cost of sample diversity. This inference-time mechanism has been widely adopted across image, video, and audio generation pipelines — including large-scale systems like Movie Gen and Diffusion Models Are Real-Time Game Engines — precisely because it is modular and requires no architectural change.

Drifting Models reframe CFG fundamentally. Rather than applying guidance as a post-hoc inference step, the technique is absorbed into the training objective: negative samples are drawn from an unconditional data distribution and mixed according to a rate γ, while the network is explicitly conditioned on the CFG scale α as an input. The result is that guidance becomes a learned behavior rather than an algebraic operation, and the one-function-evaluation (1-NFE) property at inference is preserved unconditionally.

## Key Findings

### CFG as a Training-Time Behavior

The core insight of the Drifting Models reformulation is that CFG and single-step generation are compatible if guidance is internalized during training rather than applied iteratively afterward. In conventional diffusion models, running CFG at inference requires at least two forward passes per step, which compounds with multi-step sampling to produce substantial compute overhead. By conditioning the model on the guidance scale α during training and exposing it to mixed unconditional samples via γ, the Drifting framework achieves the same qualitative effect without adding inference-time cost.

Notably, the best-performing Drifting Model uses a CFG scale of 1.0 — which in diffusion terminology corresponds to *no guidance*. This suggests the training-time exposure to unconditional signal is sufficient to shape the model's conditional behavior, making the inference-time guidance lever redundant for this architecture.

### Performance Context

The practical consequence of this design is competitive: Drifting Models achieve a 1-NFE FID of 1.54 on ImageNet 256×256 in latent space and 1.61 in pixel space, the latter using only 87G FLOPs compared to StyleGAN-XL's 2.30 FID at 1574G FLOPs. The Base-size (133M parameter) variant competes with prior XL-size single-step models, suggesting the training-time CFG formulation is not merely an efficiency trick but contributes substantively to model quality.

### The Broader Role of CFG

Across generative media pipelines more broadly, CFG functions as the primary quality-diversity dial, used in image, video, and audio generation alike. Its simplicity — a single scalar applied at inference — has made it almost universally adopted despite its theoretical cost (doubling forward passes). The Drifting Models result is an early signal that this inference-time tax may not be fundamental, and that the guidance effect can be baked into model behavior through training distribution design.

## Limitations and Open Questions

The training-time CFG formulation in Drifting Models raises questions that remain open. The mechanism relies on the model correctly internalizing the unconditional signal from mixed samples — but the relationship between the mixing rate γ, the guidance scale α, and the resulting conditional sharpness is not yet well characterized. The finding that the optimal CFG scale is 1.0 (no guidance) may reflect specific properties of the drifting loss rather than a generalizable principle.

More broadly, whether training-time CFG can replicate the *controllability* of inference-time CFG — the ability to dial guidance dynamically per generation — is unclear. Inference-time CFG allows users to trade quality against diversity at generation time; baking the scale into training fixes this choice, which may be acceptable for benchmark settings but limiting for deployment contexts where users expect flexible control.

There is also a dependency on a feature encoder: Drifting Models cannot be trained effectively on ImageNet without one, because raw pixel or latent kernel similarity fails to describe the data distribution meaningfully. This is a practical constraint that applies to the full pipeline including its CFG formulation.

## Relationships

CFG is most directly associated with the [[themes/image_generation_models|image generation]] and [[themes/generative_media|generative media]] themes, where it originated and remains most studied. Its presence in [[themes/audio_and_speech_models|audio]] and [[themes/video_and_world_models|video]] pipelines (e.g., Movie Gen) reflects how thoroughly it has propagated across modalities. The Drifting Models reformulation connects CFG to [[themes/model_architecture|model architecture]] questions about the boundary between training and inference, and to [[themes/pretraining_and_scaling|scaling]] questions about what aspects of inference-time computation can be amortized into training.

## Sources
