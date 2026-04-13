---
type: source
title: 'AToken: A Unified Tokenizer for Vision'
source_id: 01KJTHGA5BCZVCN40DFCS6MMV8
source_type: paper
authors:
- Jiasen Lu
- Liangchen Song
- Mingze Xu
- Byeongjoo Ahn
- Yanjun Wang
- Chen Chen
- Afshin Dehghan
- Yinfei Yang
published_at: '2025-09-17 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AToken: A Unified Tokenizer for Vision

AToken introduces the first visual tokenizer to simultaneously achieve high-fidelity reconstruction and semantic understanding across images, videos, and 3D assets in a single framework. By unifying all three modalities in a sparse 4D latent space and replacing adversarial training with Gram matrix loss, the work directly attacks the fragmentation that has kept vision representations from achieving the cross-task generalization that language benefits from through BPE tokenization.

**Authors:** Jiasen Lu, Liangchen Song, Mingze Xu, Byeongjoo Ahn, Yanjun Wang, Chen Chen, Afshin Dehghan, Yinfei Yang
**Published:** 2025-09-17
**Type:** paper

---

## Expert Analysis

### Motivation: The Fragmentation Problem

Visual representations remain fundamentally fragmented in ways that language representations are not. The field has bifurcated into two incompatible specializations: VAE-based tokenizers (SD-VAE, FLUX.1, Hunyuan) that excel at reconstruction by preserving low-level visual detail, and contrastive encoders (CLIP, SigLIP2, VideoPrism) that excel at semantic understanding by extracting high-level features. No single model achieves both simultaneously.

Fragmentation compounds across modalities: image tokenizers cannot model temporal dynamics, video tokenizers cannot process 3D geometry, and 3D tokenizers like Trellis-SLAT cannot leverage large-scale image/video pretraining. Prior unification attempts (VILA-U, UniTok) cover images only, and understanding accuracy lags specialized encoders by 4–5 percentage points.

A second structural problem: transformer-based visual tokenizers — which scale better than CNNs — suffer from severe GAN training instability. GigaTok and ViTok demonstrate that the discriminator rapidly dominates the generator, causing diverging logits and mode collapse. The field has consequently been pushed back toward convolutional architectures for reconstruction quality, sacrificing scalability.

A third problem lurks in discrete tokenizers specifically: poor cross-dataset generalization. UniTok degrades from 0.362 rFID on ImageNet to 3.918 rFID on COCO; GigaTok shows even larger gaps.

### Proposed Approach

**Unified 4D latent space.** AToken assigns each modality to natural subspaces of a shared (t, x, y, z) coordinate system: images occupy the (x, y) plane at t=z=0, videos extend along t with z=0, and 3D assets populate (x, y, z) at t=0. Space-time patchification produces feature-coordinate pairs z = {(z_i, p_i)}, enabling a single transformer encoder to process all modalities without architectural modification or resolution padding.

**SigLIP-initialized encoder with 4D RoPE.** The encoder initializes from the pretrained SigLIP-SO400M-naflex vision tower, extended to 4D via space-time patch embedding with zero-initialized temporal weights (preserving pretrained image semantics) and 4D Rotary Position Embeddings applied at every attention layer. The decoder is trained from scratch. Both encoder and decoder contain 27 transformer blocks with hidden dimension 1152 and 16 attention heads.

**Dual-projection design.** Reconstruction and understanding are extracted from the same latent z: reconstruction uses per-position latents projected to low-dimensional z_r (with optional FSQ quantization), while understanding aggregates via attention pooling into a global representation aligned with text embeddings via SigLIP-style contrastive objectives. For image semantic alignment, knowledge is distilled from a frozen SigLIP2 encoder using KL divergence between temperature-scaled vision-text similarity distributions.

**Gram matrix loss.** The core training innovation follows from decomposing rFID: approximately 86.6% of reconstruction error stems from the covariance component (texture and style), while only 13.4% comes from mean feature differences. This motivates replacing GAN objectives entirely with a combination of L1, LPIPS, CLIP perceptual loss, and Gram matrix loss — the Gram matrix directly optimizes second-order feature statistics without adversarial dynamics. Video and 3D use only L1, relying on cross-modal transfer from images for fine-grained detail.

**Four-stage progressive curriculum.** Stage 1 establishes image reconstruction from SigLIP2 foundations. Stage 2 extends to video with temporal tiling and KV-caching. Stage 3 incorporates 3D assets as surface voxels in 64³ grids. Stage 4 optionally adds FSQ quantization (8 codebooks × 6D, 4096-entry each) for discrete generation compatibility. Round-robin sampling with gradient accumulation ensures semantic alignment is preserved throughout all stages.

### Results

AToken-So/C is the first tokenizer to simultaneously achieve competitive reconstruction and semantic understanding across all three modalities:

- **Images:** 0.21 rFID / 82.2% ImageNet zero-shot accuracy — outperforming UniTok (0.36 rFID / 78.6% accuracy) while being within 1.2% of the understanding-only SigLIP2 baseline (83.4%)
- **Video:** 3.01 rFVD / 40.2% MSR-VTT R@1 retrieval
- **3D:** 28.28 PSNR / 90.9% Toys4k classification accuracy

A counter-intuitive finding: multimodal training enhances rather than degrades single-modality performance. Image rFID improves 19% across progressive stages (0.258 → 0.209), and video reconstruction improves when 3D is added in Stage 3 (35.63 → 36.07 PSNR on TokenBench). This cross-modal benefit is capacity-dependent — the 192M-parameter Base model degrades 49% on ImageNet rFID when extended to video, while the 800M So400m model improves continuously.

When integrated as a frozen vision encoder in SlowFast-LLaVA-1.5, AToken outperforms the Oryx-ViT baseline across most benchmarks: +1.3% RW-QA, +1.0% SQA, +1.3% TextVQA at 7B scale. For image generation, AToken-So/C achieves 1.56 gFID using Lightning-DiT, competitive with specialized tokenizers (VAVAE: 1.35, REPA: 1.42) despite joint optimization across modalities.

---

## Capabilities

- **First unified reconstruction + understanding tokenizer across three modalities.** The dual-projection design resolves the generation/understanding split that has fragmented vision representations, albeit with persistent accuracy taxes versus specialists. (maturity: research_only)

- **Sparse 4D latent space with 4D RoPE.** A single transformer encoder natively handles images, videos, and 3D assets at arbitrary resolutions and temporal durations without modality-specific architectural branches. (maturity: research_only)

- **Adversarial-free transformer tokenizer training.** Gram matrix loss achieves SOTA reconstruction quality for transformer-based tokenizers (0.21 rFID), resolving the training instability that has long forced the field toward convolutional architectures. (maturity: research_only)

- **Cross-modal training benefit.** The progressive curriculum demonstrates that video and 3D training measurably improves image reconstruction quality — contradicting the assumed trade-off between modality coverage and per-modality performance. (maturity: research_only)

- **Discrete unified tokenization.** FSQ quantization applied after Stage 3 produces the first discrete tokenizer covering all three modalities, enabling autoregressive generation pipelines across images, video, and 3D. (maturity: research_only)

---

## Limitations & Open Questions

### Persistent Specialist Gap

**Semantic understanding tax** (minor, improving): Unified tokenizers pay ~1–2% on image classification and ~5–10% on retrieval versus understanding-only encoders. AToken achieves 82.2% ImageNet accuracy versus SigLIP2's 83.4%.

**Video semantic understanding gap** (significant, improving): AToken achieves 40.2% R@1 on MSRVTT versus 52.7% for VideoPrism-g — a 12.5-point gap attributed to insufficient video-text training data within the unified training budget.

**Long-form video** (significant, unclear): Oryx-ViT outperforms AToken on MLVU long-form understanding, hypothesised to result from dedicated long-video retrieval pretraining that AToken lacks.

**Image-to-3D generation** (significant, unclear): Generated assets fail to consistently preserve the colour and style of conditioning images. Performance does not match Trellis-SLAT, attributed to the 8x latent channel reduction (64 → 8) required for the generation pipeline.

**Transformer vs. convolutional reconstruction ceiling** (significant, improving): AToken achieves 29.72 PSNR versus Hunyuan's 33.32 PSNR (convolutional) — a 3.6 dB gap indicating transformers have not yet matched CNNs on raw reconstruction quality despite the Gram matrix advance.

### Discrete Tokenization Problems

**Continuous vs. discrete gap** (significant, stable): AToken-So/D achieves 22.16 rFVD versus 3.01 for AToken-So/C on video — a 7x quality degradation. Discrete tokenization remains far behind continuous for temporal modalities.

**Cross-dataset generalisation failure** (significant, stable): AToken-So/D rFID degrades 8.6x from ImageNet (0.379) to COCO (3.270). This is a persistent problem across discrete tokenizers (UniTok: 0.362 → 3.918; GigaTok: comparable gaps), suggesting a fundamental issue rather than an AToken-specific one.

### Structural Constraints

**Model capacity threshold** (significant, stable): Unified multimodal tokenization catastrophically fails below ~800M parameters. The 192M Base model degrades 49% on ImageNet rFID when extended to video. This hard threshold blocks efficient unified tokenizers for edge deployment and research iteration.

**Fixed 64³ voxel grid for 3D** (significant, unclear): Geometric fidelity is bounded by voxel resolution, preventing scaling to higher-resolution 3D assets without architectural changes.

**Latent space dimensionality mismatch** (significant, 1–2 year horizon): Downstream generative architectures are designed for 8-channel latents; AToken requires 48 channels to accommodate multimodal information. This blocks plug-and-play substitution into existing generation pipelines.

**Training cost** (significant, improving): 138,000 GPU hours across four stages (~22 days on 256 H100s) makes unified multimodal tokenizer development inaccessible to most research groups.

**Semantic separability under compression** (minor, unclear): T-SNE visualizations of 48-dim latents show intermixed class clustering, raising unresolved questions about whether semantic separability is partially lost through compression.

**No unified downstream evaluation** (significant, unclear): Due to compute constraints, no single model combining all modalities and tasks is evaluated simultaneously. Whether unified tokenizers enable emergent cross-modal capabilities in downstream models remains untested.

---

## Breakthroughs

**Unified reconstruction + understanding across images, video, and 3D** (major): The first demonstration that a single visual tokeniser can simultaneously achieve high-fidelity reconstruction and rich semantic understanding across all three modalities, breaking the assumption that specialization is a hard constraint rather than an engineering limitation.

**Adversarial-free transformer tokenizer training** (notable): Gram matrix loss resolves the GAN instability that has constrained transformer-based tokenizers, enabling SOTA reconstruction quality without mode collapse. The decomposition of rFID into mean (13.4%) and covariance (86.6%) components provides a principled diagnostic for reconstruction error that may generalize beyond this architecture.

---

## Bottlenecks Surfaced

**Minimum capacity threshold for unified tokenization** (3–5 year horizon): Cross-modal interference dominates cross-modal benefit below ~800M parameters. This blocks efficient unified tokenizers for edge deployment and research iteration at scale.

**Latent space dimensionality incompatibility** (1–2 year horizon): Generative architectures (diffusion, autoregressive) expect low-dimensional latents; unified multimodal tokenizers require high-dimensional spaces. Plug-and-play substitution requires either new generation architectures or effective channel compression without quality loss.

**Video-text data scarcity within unified training budgets** (1–2 year horizon): Insufficient video-text paired training prevents unified models from matching dedicated video-language encoders. Competitive video semantic understanding in a unified system requires either data scaling or more sample-efficient video-language alignment methods.

---

## Themes

- [[themes/generative_media|Generative Media]]
- [[themes/image_generation_models|Image Generation Models]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/unified_multimodal_models|Unified Multimodal Models]]
- [[themes/video_and_world_models|Video and World Models]]

## Key Concepts

- [[entities/gaussian-splatting|Gaussian Splatting]]
- [[entities/lpips|LPIPS]]
- [[entities/psnr|PSNR]]
