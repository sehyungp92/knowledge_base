---
type: source
title: 'X-Fusion: Introducing New Modality to Frozen Large Language Models'
source_id: 01KJTX3RQ3MZQ0CY18MF5J80HC
source_type: paper
authors:
- Sicheng Mo
- Thao Nguyen
- Xun Huang
- Siddharth Srinivasan Iyer
- Yijun Li
- Yuchen Liu
- Abhishek Tandon
- Eli Shechtman
- Krishna Kumar Singh
- Yong Jae Lee
- Bolei Zhou
- Yuheng Li
published_at: '2025-04-29 00:00:00'
theme_ids:
- finetuning_and_distillation
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# X-Fusion: Introducing New Modality to Frozen Large Language Models

**Authors:** Sicheng Mo, Thao Nguyen, Xun Huang, Siddharth Srinivasan Iyer, Yijun Li, Yuchen Liu, Abhishek Tandon, Eli Shechtman, Krishna Kumar Singh, Yong Jae Lee, Bolei Zhou, Yuheng Li
**Published:** 2025-04-29 00:00:00
**Type:** paper

## Analysis

# X-Fusion: Introducing New Modality to Frozen Large Language Models
2025-04-29 · paper · Sicheng Mo, Thao Nguyen, Xun Huang, Siddharth Srinivasan Iyer, Yijun Li et al. (12 total)
https://arxiv.org/pdf/2504.20996

---

### Motivation & Prior Limitations
Existing approaches to building unified vision-language models either require training from scratch at enormous computational cost or fine-tune LLM backbones in ways that degrade inherited language capabilities.
- Training unified models from scratch (e.g., Transfusion, trained on 2T tokens) demands immense compute and requires full retraining for each new modality, making iteration expensive and impractical.
- Fine-tuning the LLM backbone to acquire visual capabilities consistently degrades text performance, as demonstrated by the Single Tower baseline in this paper dropping from 32.2 to 25.0 on MMLU (chance-level for a 4-way multiple-choice task).
- Approaches that merge LLMs with separate pretrained generation models (e.g., DreamLLM, GILL) are not unified architectures, which limits cross-modal reasoning, restricts in-context learning, and increases error accumulation.
- Visual instruction tuning methods (e.g., LLaVA) align text and vision feature spaces but are restricted to understanding tasks and do not address image generation in the same model.

---

### Proposed Approach
X-Fusion introduces a dual-tower architecture that adds a trainable vision tower alongside a frozen LLM (text tower), enabling multimodal understanding and generation without modifying any language weights.
- Each transformer layer contains both a frozen text block (Ftxt) and a trainable vision block (Fimg); both process the full interleaved token sequence, but text tokens are routed to text-tower outputs and vision tokens to vision-tower outputs, so modality routing is enforced at the feature selection step rather than via separate input streams.
  - The vision tower is initialized by copying the corresponding language transformer layer (self-attention + MLP + normalization), then trained jointly; the architecture is explicitly asymmetric-capable, meaning the vision tower need not mirror the language tower's design.
  - An optional X-Fuse operation allows cross-tower feature fusion via learnable scalar weights (α, β), trading additional FLOPs for improved performance on both tasks.
- Training combines autoregressive cross-entropy loss (λAR = 0.2) for language with flow-matching diffusion loss (λDM = 1) for image generation, following the Transfusion hybrid objective but initializing from a pretrained frozen LLaMA-3 rather than training from scratch.
- A key data-centric finding is that image-to-text (understanding) samples should be provided as clean images with no added diffusion noise, contrary to the Transfusion practice of capping noise at 50%T; this yields better semantic visual representations that improve both understanding and generation simultaneously.
- The framework is designed to extend to additional modalities (e.g., audio) by adding modality-specific towers without touching existing towers, providing a modular scaling path.

---

### Results & Capabilities
The Dual Tower architecture achieves a 23% lower FID than the Single Tower baseline on MS-COCO text-to-image evaluation while preserving full language capability (32.2 MMLU vs. 25.0 for Single Tower), establishing it as the best-performing variant across all compared architectures.
- On architecture comparison with LLaMA-3.2-1B: Dual Tower scores FID 14.20 / CLIP 22.81 / BLIP 31.3 vs. Single Tower at FID 19.10 / CLIP 22.63 / BLIP 30.2, and vs. Dual Projection at FID 20.22 / CLIP 22.46 / BLIP 30.9; Gated Tower performs weakest at FID 24.51 / BLIP 14.5.
- Incorporating image understanding data (I2T) asymmetrically benefits generation: holding T2I token count fixed, increasing I2T proportion consistently lowers FID and raises CLIP scores, while adding T2I data does not improve understanding (BLIP). The recommended training ratio is 2:1 T2I to I2T.
- Using clean images for understanding samples produces higher-quality layer-wise features as measured by ImageNet linear probe accuracy, confirming the mechanism: better semantic representations in the vision tower transfer to generation quality.
- CLIP-feature alignment (REPA-style cosine loss on layer 8 of the vision tower) accelerates convergence and improves performance at 1B and 3B scales but provides diminishing returns at 8B and slightly degrades performance at 100k iterations for the 8B model.
- The X-Fusion(Pretrained DiT) variant — which initializes the vision tower from an in-house pretrained text-to-image diffusion transformer rather than from copied LLM weights — achieves stronger image generation with competitive understanding, demonstrating that vision-tower knowledge transfer is viable within the frozen-LLM framework.
- After fine-tuning on four downstream tasks simultaneously (image editing, localization, inpainting/outpainting, VQA), a single X-Fusion model handles all tasks without task-specific weights, and shows strong instruction-following for object-level editing on PIE-Bench and SmartEdit benchmarks.

---

### Implications
X-Fusion demonstrates a practical path to unified multimodal models that does not sacrifice the accumulated language knowledge in pretrained LLMs, which matters especially as LLM capabilities continue to scale and retraining from scratch becomes prohibitively expensive.
- The frozen-LLM paradigm decouples language capability from multimodal adaptation, suggesting that future models could add modalities incrementally — audio, video, sensor data — by stacking towers without destabilizing existing capabilities, a meaningful architectural signal for modular AI systems.
- The asymmetric data finding (understanding aids generation, but not vice versa) has concrete implications for training data curation: teams building text-to-image systems should invest in high-quality captioned image data for understanding even when 

## Key Claims

1. X-Fusion's dual-tower architecture keeps LLM parameters frozen while introducing a separate trainable vision tower, preserving original language capabilities.
2. Fine-tuning the LLM backbone (Single Tower) causes catastrophic forgetting, dropping MMLU from 32.2 to 25.0 (chance-level for 4-choice MCQ).
3. Dual Tower achieves 23% lower FID than Single Tower while maintaining the same number of training parameters.
4. Gated Tower architecture performs worst among all tested architectures on both image generation and understanding tasks.
5. Dual Tower achieves FID of 14.20 vs Single Tower's 19.10, Gated Tower's 24.51, and Dual Projection's 20.22, with all methods maintaining LLaMA 32.2 MMLU except Single Tower.
6. Training on clean images for image-to-text (understanding) samples improves both image understanding and image generation performance simultaneously.
7. A 2:1 ratio of T2I to I2T training data is recommended as the optimal balance for unified multimodal models.
8. Feature alignment with pretrained CLIP representations (REPA) accelerates convergence for smaller models (1B, 3B) but provides diminishing benefit at larger scales (8B).
9. Training unified multimodal models from scratch requires immense computation; Transfusion was trained on 2T tokens.
10. X-Fusion achieves competitive training efficiency, processing only 0.08T tokens compared to Transfusion's 2T tokens.

## Capabilities

- Frozen-backbone dual-tower architecture extends pretrained LLMs to simultaneous image understanding and generation without degrading language capability — MMLU preserved at 32.2 vs chance-level 25.0 for single-tower fine-tuning, with 23% lower FID on image generation
- Understanding data (I2T) cross-synergistically improves image generation quality in unified multimodal training — 66/33 T2I:I2T ratio achieves ~2.4x convergence acceleration and better generation quality than pure T2I training at equivalent generation token count
- Vision tower initialization from a pretrained text-to-image DiT model enables knowledge transfer into frozen-backbone unified models, accelerating convergence and improving image generation capability beyond random initialization
- Single unified multimodal model handling VQA, instruction-based image editing (including multi-object disambiguation), object localization, and in/out-painting simultaneously without task-specific weights
- Clean-image training strategy for unified diffusion-based multimodal models: using unnoised images for understanding samples simultaneously improves both understanding and generation quality, with linear probing confirming superior feature representations at all layers

## Limitations

- Image generation capability in frozen-backbone multimodal extensions must be learned entirely from scratch — there is no mechanism to directly inherit pretrained generation knowledge without an explicit transfer step
- Optimal output modeling paradigm for new modalities in unified LLM extensions is unresolved — diffusion, continuous autoregressive, and discrete autoregressive each have different tradeoffs and the best choice is acknowledged to be case-specific
- Feature alignment with external encoders (CLIP) imposes a hard performance ceiling bounded by that encoder's representational power — the model cannot exceed what the external encoder represents
- Feature alignment with CLIP slightly degrades 8B model performance at 100k training iterations — the alignment benefit inverts at larger scales
- Standard single-tower fine-tuning of LLMs for multimodal tasks causes catastrophic forgetting — MMLU drops to chance level (25.0 from 32.2) despite training only on vision tasks at 1B scale
- X-Fusion is trained on only 0.08T tokens — approximately 25x less than Transfusion (2T tokens) — making the absolute performance comparison with from-scratch SOTA methods deeply uncertain
- All image experiments conducted at 256×256 resolution — generalization to higher resolutions is untested and the approach's practical deployment ceiling is unknown
- Generation data (T2I) provides zero benefit to understanding quality (I2T) — the cross-task synergy is strictly asymmetric, meaning scaling generation data alone cannot improve semantic understanding
- Evaluation is restricted to MS-COCO FID and BLIP-ITM metrics with no comparison to production-quality generation models (DALL-E 3, SD3, Midjourney) or standard VLM benchmarks (MMBench, SeedBench, MMMU, VQAv2) — absolute capability level relative to industry state-of-the-art is unestablished
- Training uses an in-house proprietary licensed dataset with no public documentation of composition, scale, or quality — reproducibility is blocked and it is unclear whether gains reflect architecture or data quality
- Text processing flexibility in the dual-tower design (how text features propagate) affects image generation performance but has minimal impact on image understanding — indicating the understanding pathway is under-constrained

## Bottlenecks

- External encoder representational quality caps the ceiling of feature regularization in unified multimodal models — alignment losses (e.g., to CLIP) can only improve performance up to what the external encoder represents, and this ceiling becomes a constraint rather than a benefit at scale
- Frozen-backbone multimodal extension has no inherent mechanism to inherit pretrained image generation priors — vision towers must cold-start from language weight copies, requiring substantial generation-specific training even when strong generation models already exist

## Breakthroughs

- Dual-tower frozen-backbone architecture demonstrates that pretrained LLMs can be extended to simultaneous image understanding and generation with full preservation of language capability — validated across 1B, 3B, and 8B scales at 25x lower data cost than from-scratch approaches
- Empirical discovery of a strict asymmetric cross-task synergy in unified multimodal training: understanding data (I2T) consistently improves image generation quality at no cost to generation-specific training, but generation data (T2I) provides zero benefit to understanding — establishing a principl

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/clip-score|CLIP Score]]
- [[entities/fid|FID]]
- [[entities/flow-matching|Flow Matching]]
- [[entities/imagenet|ImageNet]]
- [[entities/mmlu|MMLU]]
