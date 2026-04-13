---
type: entity
title: FID
entity_type: metric
theme_ids:
- creative_content_generation
- finetuning_and_distillation
- generative_media
- image_generation_models
- model_architecture
- multimodal_models
- post_training_methods
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00016901042750615654
staleness: 0.0
status: active
tags: []
---
# FID

Fréchet Inception Distance (FID) is the standard quantitative metric for evaluating generative image models, measuring how closely the statistical distribution of generated images matches that of real images in a learned feature space. It compares the mean and covariance of Inception network activations across generated and real image sets, with lower scores indicating higher quality and diversity. FID has become the lingua franca of image generation benchmarking — particularly on ImageNet at 256×256 resolution using 50K generated samples — making it the primary lens through which progress in the field is tracked and contested.

**Type:** metric
**Themes:** [[themes/creative_content_generation|creative_content_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

FID is computed by passing both real and generated images through a pretrained Inception network, extracting intermediate feature activations, fitting Gaussian distributions to each set, and computing the Fréchet distance between them. The metric penalizes both low quality (features far from the real distribution) and low diversity (collapsed covariance). By convention, ImageNet benchmarks report FID over 50K generated samples, enabling apples-to-apples comparison across architectures.

The metric's centrality to the field makes single-step generation quality particularly significant: achieving low FID with one neural function evaluation (1-NFE) rather than dozens of diffusion or flow steps represents both a scientific and practical advance — faster inference with no quality penalty.

## Key Findings

The most striking recent result comes from Generative Modeling via Drifting, which achieves a **state-of-the-art 1-NFE FID of 1.54 on ImageNet 256×256 in latent space** and 1.61 in pixel space — competitive with or surpassing prior multi-step methods. The significance is amplified by the efficiency angle: the pixel-space result uses only **87G FLOPs**, compared to StyleGAN-XL's 1,574G FLOPs for a worse 2.30 FID. A Base-size (133M parameter) Drifting Model competes with prior XL-size single-step models trained from scratch, suggesting architectural efficiency gains beyond raw scale.

What makes these FID results mechanistically interesting is how they are achieved. Drifting Models dispense with SDE/ODE inference trajectories entirely, instead learning a pushforward map that evolves at **training time** via an attraction-repulsion drifting field — generated samples are attracted toward the data distribution and repelled from the current generated distribution. The loss is equivalent to minimizing the squared norm of this drifting field, and an anti-symmetry property guarantees that equilibrium (where drift goes to zero everywhere) is reached if and only if the generated distribution matches the data distribution. Breaking anti-symmetry causes catastrophic FID failure, marking it as a necessary rather than optional constraint.

Classifier-free guidance (CFG) is handled unusually: it is a training-time behavior implemented by mixing negative samples from different class distributions, preserving the 1-NFE property at inference. The best-performing model (FID 1.54) uses a CFG scale of 1.0 — equivalent to *no* CFG in diffusion terminology — suggesting that the training-time guidance mechanism is doing real work rather than leaning on inference-time steering.

Toy experiments confirm the method does not exhibit mode collapse: even when the generated distribution is initialized as a single collapsed mode, the drifting field recovers the full bimodal target. Larger positive and negative sample sets consistently improve FID under fixed compute, echoing findings from contrastive representation learning about sample set size.

## Known Limitations and Open Questions

FID as a metric has implicit assumptions that the findings expose. The drifting approach **requires a feature encoder** — raw pixel or latent kernel similarity is insufficient for effective training on ImageNet. This dependency on Inception-derived feature spaces means both the *training signal* and the *evaluation metric* are anchored to the same learned representation, raising questions about whether FID optimization could converge toward Inception-aligned artifacts rather than genuinely high-quality images.

More broadly, FID conflates quality and diversity in a single number that is sensitive to the choice of reference statistics, sample count, and feature extractor. The benchmark convention of 50K samples and ImageNet classes makes results reproducible but not necessarily predictive of performance on distribution-shifted or out-of-domain generation tasks.

The results from Drifting Models, while impressive on FID, are reported in a controlled single-domain (ImageNet class-conditional) setting. How the method's FID advantage transfers to more complex, open-domain, or compositional generation — the regime where diffusion and flow models are most practically deployed — remains an open question. The reliance on a feature encoder trained on ImageNet also raises questions about generalization to non-photographic domains.

## Relationships

FID is the central evaluation axis for Generative Modeling via Drifting and appears as a comparative benchmark across [[themes/image_generation_models|image generation models]] broadly. It connects to [[themes/model_architecture|model architecture]] debates through the efficiency angle (FID per FLOP), and to [[themes/post_training_methods|post-training methods]] through the CFG and distillation comparisons that single-step methods implicitly contest. The metric's dependence on Inception features links it to [[themes/vision_language_models|vision language models]] as the field debates whether richer evaluation embeddings (e.g., CLIP-based FID variants) would better capture what humans care about in generated images.

## Limitations and Open Questions

## Sources
