---
type: entity
title: Fréchet Inception Distance
entity_type: metric
theme_ids:
- generative_media
- image_generation_models
- model_architecture
- multimodal_models
- representation_learning
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00010820123624143229
staleness: 0.0
status: active
tags: []
---
# Fréchet Inception Distance

Fréchet Inception Distance (FID) is the dominant quantitative metric for evaluating the visual quality and distributional fidelity of generated images. By measuring the Fréchet distance between multivariate Gaussians fitted to Inception network feature activations for real and generated image sets, FID captures both the quality of individual samples and the diversity of the generated distribution — a dual sensitivity that makes it more informative than earlier metrics such as Inception Score. Its widespread adoption across generative modelling research has made it the de facto benchmark axis for comparing image generation systems, with lower scores indicating generated distributions closer to real data.

**Type:** metric
**Themes:** [[themes/generative_media|Generative Media]], [[themes/image_generation_models|Image Generation Models]], [[themes/model_architecture|Model Architecture]], [[themes/multimodal_models|Multimodal Models]], [[themes/representation_learning|Representation Learning]], [[themes/unified_multimodal_models|Unified Multimodal Models]], [[themes/vision_language_models|Vision Language Models]]

---

## Overview

FID operates by passing both real and generated images through a pretrained Inception-v3 network, extracting intermediate feature activations, and fitting a multivariate Gaussian to each set. The Fréchet (Wasserstein-2) distance between those two Gaussians is the score. This design embeds an inductive bias toward the perceptual feature space learned by Inception on ImageNet, which correlates reasonably well with human judgements of image fidelity and diversity, though not perfectly. The metric is typically computed over large sample sets — the MJHQ FID-30k variant, for instance, uses 30,000 samples drawn from the MJHQ-30K high-quality image benchmark — to ensure statistical stability of the Gaussian fits.

FID is now routinely reported alongside task-oriented benchmarks (GenEval, DPG-Bench) that test compositional generation fidelity. This reflects a recognition that distributional closeness to real images, as FID measures, and instruction-following accuracy, as GenEval measures, are complementary and not perfectly correlated — a model can look photorealistic but fail to bind attributes correctly, or vice versa.

---

## Key Findings

The clearest empirical window into FID's discriminative power comes from recent work on unified multimodal models, where generation quality must be preserved while sharing architectural capacity with visual understanding. The JanusFlow results from JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation illustrate the landscape precisely. Among 1.3B-parameter unified models, JanusFlow achieves an MJHQ FID-30k of **9.51**, compared to Show-o at 15.18 and the earlier Janus at 10.10 — a meaningful gap driven by JanusFlow's adoption of rectified flow in latent space (using a pretrained SDXL-VAE operating at 384×384) rather than discrete token-based generation. This suggests FID is sensitive enough to distinguish the representational choices that matter most: continuous latent generation with flow matching produces smoother, higher-fidelity distributions than autoregressive generation over quantized tokens, and FID captures that difference numerically.

The decoupled encoder design in JanusFlow — separate ConvNeXt-based encoders for generation versus a SigLIP-Large-Patch/16 encoder for understanding — also implicates FID indirectly. Task interference between understanding and generation degrades both understanding benchmarks and generation quality; eliminating it improves FID alongside multimodal comprehension scores (74.9 on MMBench, 70.5 on SeedBench, 60.3 on GQA). That JanusFlow surpasses dedicated text-to-image models including SDv1.5 and SDXL on FID while simultaneously performing well on understanding tasks reflects how architectural choices propagate into distributional quality.

---

## Limitations and Open Questions

FID carries well-documented limitations that constrain how confidently rankings should be interpreted. Its reliance on Inception-v3 features means it inherits that network's biases: images that resemble ImageNet-like content score better, while stylised, abstract, or domain-specific outputs may be penalised despite being high-quality on their own terms. The Gaussian assumption over feature activations is an approximation that can fail when distributions are multimodal or heavy-tailed, which is common in diverse generation settings.

The choice of reference set matters substantially — MJHQ-30K, COCO, and ImageNet produce non-interchangeable FID baselines, making cross-paper comparisons unreliable unless the same reference set is used. The 30k sample requirement also means FID is expensive to compute accurately, and results with fewer samples have high variance, creating pressure to under-report uncertainty.

More fundamentally, FID measures distributional closeness to *existing real images*, which rewards models that produce outputs similar to training data distributions rather than creative or out-of-distribution generations that might be more useful. As generation shifts toward instruction-following, long-context coherence, and multi-subject composition, task-oriented metrics like GenEval are increasingly preferred for capturing what actually matters. FID may be drifting toward a role as a necessary but insufficient baseline check — a floor on image quality rather than a ceiling on generation capability.

---

## Relationships

FID is closely paired with **GenEval** and **DPG-Bench** in contemporary evaluation suites, with the three metrics together covering distributional fidelity, compositional accuracy, and dense prompt adherence respectively. It is directly implicated in the comparison between JanusFlow, Janus, and autoregressive image generation without vector quantization approaches, where the shift from discrete to continuous generation is one of the key variables FID distinguishes. The metric's sensitivity to representation quality connects it to the broader tension in [[themes/unified_multimodal_models|unified multimodal models]] between task sharing and task interference — FID scores rise and fall with architectural choices that go well beyond the generation head itself.

## Sources
