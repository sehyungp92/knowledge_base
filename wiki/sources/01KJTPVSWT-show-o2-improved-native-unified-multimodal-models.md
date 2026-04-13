---
type: source
title: 'Show-o2: Improved Native Unified Multimodal Models'
source_id: 01KJTPVSWTK7XQS7HT1TQQVXV2
source_type: paper
authors:
- Jinheng Xie
- Zhenheng Yang
- Mike Zheng Shou
published_at: '2025-06-18 00:00:00'
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
# Show-o2: Improved Native Unified Multimodal Models

Show-o2 advances the state of native unified multimodal models by demonstrating that a single architecture — combining autoregressive language modeling with flow-matching-based image/video generation — can achieve competitive performance across text, image, and video understanding and generation simultaneously, without requiring massive web-scale text corpora or separate encoder architectures. Its core contributions are a dual-path spatial-temporal fusion mechanism within a shared 3D causal VAE latent space, and a two-stage training recipe that preserves base LLM capabilities while jointly learning visual modalities.

**Authors:** Jinheng Xie, Zhenheng Yang, Mike Zheng Shou
**Published:** 2025-06-18
**Type:** paper
**Themes:** [[themes/multimodal_models|Multimodal Models]] · [[themes/unified_multimodal_models|Unified Multimodal Models]] · [[themes/generative_media|Generative Media]] · [[themes/image_generation_models|Image Generation Models]] · [[themes/video_and_world_models|Video and World Models]]

---

## Motivation

Prior native unified multimodal models — Chameleon, [[entities/show-o|Show-o]], Transfusion, Emu3 — were largely constrained to text and image modalities. Scaling to video within a single native architecture without architectural compromise remained unsolved. More fundamentally, these models faced two structural tensions:

1. **Understanding vs. generation feature conflict.** Multimodal understanding benefits from high-level semantic representations (as learned by encoders like SigLIP); generation requires low-level structural fidelity. Existing unified representations optimized for one at the expense of the other.

2. **Language knowledge degradation.** Joint training of visual generation and language modeling consistently caused catastrophic forgetting. One-stage co-training with RefinedWeb collapses MMLU from 60.20% to 28.25% on the 1.5B model, and from 71.75% to 28.43% on the 7B — effectively destroying the LLM backbone's reasoning capabilities.

Encoder-free LMMs (those without pre-aligned visual encoders) also consistently underperformed their aligned counterparts on understanding tasks, motivating a hybrid representation approach rather than a purely end-to-end visual encoding strategy.

---

## Architecture

### Unified Visual Representation: Dual-Path Spatial-Temporal Fusion

Show-o2 operates within the latent space of the **3D causal VAE from Wan2.1** (8× spatial, 4× temporal compression). Rather than feeding VAE latents directly to the LLM, it constructs unified visual representations via two parallel paths:

- **Semantic layers S(·):** SigLIP ViT blocks pre-distilled from SigLIP-so400m-patch14-384, extracting high-level semantic features. Distilled features achieve ~0.9 average cosine similarity to original SigLIP features on clean latents, using cosine similarity loss on 66M image-text pairs.
- **Projector P(·):** Retains complete low-level structural information from the VAE latents without lossy semantic compression.

These paths are fused via concatenation → RMSNorm → MLP into unified representations `u = STF(S(x_t), P(x_t))`. For video, this fusion is applied with full temporal alignment across frames — distinguishing it from image-only predecessors. A timestep embedding `t` is prepended for generative conditioning; `t=1.0` is used for clean images during understanding.

Ablation confirms the value of this fusion: spatial-temporal fusion improves MME-p from 1164.7 to 1187.8, GQA from 56.2 to 57.6, and reduces FID-5K from 21.8 to 20.5 compared to a baseline without it.

### Dual-Head Language Model

A pre-trained Qwen2.5 (1.5B or 7B Instruct) backbone is augmented with:

- **Language head:** Standard next-token prediction with causal attention.
- **Flow head:** Flow matching with full attention within visual blocks, using adaLN-Zero modulated transformer layers (as in DiT) for timestep conditioning.

The **omni-attention mechanism** (from Show-o / Transfusion) enforces causal attention along the sequence while permitting full attention within unified visual representation blocks. The combined training loss is `L = L_NTP + α · L_FM`.

Scaling from 1.5B to 7B reuses the pre-trained flow head with a lightweight MLP transformation to align hidden dimensions, avoiding full retraining of generative components.

### Two-Stage Training Recipe

| Stage | Trainable Components | Data |
|-------|---------------------|------|
| Stage 1 | Projector, spatial(-temporal) fusion, flow head (LLM frozen) | ~66M image-text pairs → progressive addition of interleaved + video-text |
| Stage 2 | Full model except VAE | 9M understanding instruction data + 16M generation images + 1.6M video understanding samples |

The frozen LLM in Stage 1 is the critical design choice: it explicitly avoids needing a massive web-scale text corpus while preserving language knowledge. The approach achieves 56.75% vs 60.20% MMLU (1.5B) and 70.73% vs 71.75% (7B) relative to the Qwen2.5 base models — within 3–5 points rather than the ~50-point collapse seen with one-stage training.

---

## Results

### Multimodal Understanding

The 7B model outperforms Janus-Pro-7B across MME-p (1620.5 vs reported), GQA (63.1), MMMU-val (48.9), MMStar (56.6), and AI2D (78.6), and exceeds the 14B TokenFlow-XL on multiple benchmarks. The 1.5B model similarly outperforms Janus-Pro-1.5B (MME-p 1450.9 vs 1444.0; MMMU-val 37.1 vs 36.3) and substantially exceeds JanusFlow-1.5B.

### Image Generation

On DPG-Bench, Show-o2-7B achieves 86.14 — the highest reported among both generation-only models (SD3-Medium: 84.08, DALL-E 3: 83.50) and native unified models (Janus-Pro-7B: 84.19, Mogao-7B: 84.33), trained on only 66M image-text pairs versus Janus-Pro's 144M. GenEval scores 0.76 overall, competitive with Janus-Pro-7B (0.80) and above Show-o (0.68), Transfusion (0.63), and Emu3 (0.66).

### Video Generation

At 2B total parameters, Show-o2 achieves VBench Quality Score 81.34 and Semantic Score 82.10 — surpassing Show-1 (6B), Emu3 (8B), and VILA-U (7B), and competitive with CogVideoX-5B (81.61) and Step-Video-T2V-30B (81.83). Image-to-video Background Consistency reaches 98.83, the highest among compared methods.

### Video Understanding

The dedicated fine-tuned Show-o2†-7B achieves NExT-QA 79.0, VideoMME 57.4/60.9 (without/with subtitles) — competitive with LLaVA-OV-7B (79.4, 58.2/61.5) despite being a unified generation+understanding model.

---

## Limitations and Open Questions

### Blocking

**One-stage unified training causes catastrophic language collapse.** The fundamental incompatibility between flow-matching visual training and autoregressive language modeling, when applied simultaneously with full parameter updates, destroys LLM reasoning capabilities. MMLU drops from 60.20% → 28.25% (1.5B) and 71.75% → 28.43% (7B). The two-stage recipe is a workaround rather than a resolution — the underlying conflict between objectives remains.

**Video-capable training at 7B+ is computationally blocked.** A 2-second 480p clip at 17 frames generates 7,006 tokens in the sequence. Including interleaved and video data in the 7B model training was abandoned entirely due to compute cost. The 7B Show-o2 cannot generate or reason about video. This is a direct consequence of video context length scaling poorly with model scale.

### Significant

**Text rendering in generated images fails.** Text rendering scores are near zero (0.002) on OneIG-Bench for both standard-resolution models, versus 0.680 for OmniGen2. Root cause identified: text-rich images are structurally underrepresented in web-scale training corpora, and no automated filtering pipeline exists to curate them at scale. The 1024×1024 model improves slightly (0.125) but remains far behind.

**Spatial positioning lags in image generation.** GenEval Position score of 0.52 for the 7B model substantially trails Janus-Pro-7B (0.79) and Mogao-7B (0.84), despite competitive performance on other generation metrics. The gap is unexplained in the paper.

**Fine-grained document and chart understanding requires more image tokens.** At 729 image tokens, ChartQA is 48.00 vs LLaVA-OV-7B's 56.24. Increasing to ~3,600 tokens jumps ChartQA to 66.92 and DocVQA from 59.34 to 77.26, but at prohibitive sequence-length cost. Chart data underrepresentation in semantic layer distillation is cited as a contributing factor.

**Video understanding requires a separate fine-tuning phase.** The base unified model (trained for image understanding + video generation) does not achieve competitive video understanding. A dedicated 1.6M-sample fine-tuning phase is required, revealing that video understanding and video generation are not automatically unified by the shared architecture.

**Video generation is constrained to very short clips.** 2-second clips at 480p / 17 frames is the ceiling for practical training. Longer coherent video generation is not demonstrated.

**Encoder-free architectures still underperform.** Despite the dual-path fusion mechanism, fully encoder-free approaches (without SigLIP distillation) remain a step behind aligned-encoder counterparts. Show-o2 effectively re-introduces encoder knowledge through distillation, confirming that end-to-end visual encoding without pre-alignment remains an unsolved capability gap.

**Training costs reproduce poorly.** The 7B model requires 128 H100 GPUs for ~2.5 days — roughly 2× typical open-source VLM training, limiting reproducibility and iteration speed for the research community.

### Minor

**SEED-Bench residual gap.** The 7B model scores 69.8 vs Janus-Pro-7B's 72.1 and well below understanding-only models, suggesting a persistent understanding-generation tradeoff that spatial-temporal fusion does not fully eliminate.

---

## Bottlenecks Addressed and Remaining

Show-o2 makes progress on the bottleneck of **unified visual representations** that simultaneously serve understanding and generation — the dual-path fusion demonstrably improves both simultaneously. This was previously considered a fundamental architectural tension.

It does not resolve:

- **Video-capable unified models at frontier scales** — context length costs make this a 1–2 year horizon problem absent architectural innovation in sequence compression or attention efficiency.
- **Text rendering in image generation** — blocked by corpus curation infrastructure, not model architecture. Filtered text-rich datasets are the likely near-term unlock.
- **The broader understanding-generation tradeoff** — SEED-Bench and ChartQA gaps persist, and video understanding/generation remain separate training concerns despite sharing a single model.

---

## Significance

Show-o2's most transferable contributions are methodological rather than benchmark-driven:

1. **The two-stage recipe pattern** — freezing the LLM during Stage 1 visual alignment is a clean solution to language degradation that other unified model efforts can adopt without Show-o2's specific architecture.

2. **Dual-path fusion as a design principle** — explicitly separating semantic and structural paths within a shared latent space, then merging them, offers a reusable pattern for any architecture trying to unify understanding and generation in continuous latent spaces.

3. **The scaling transfer trick** — reusing the pre-trained flow head with a lightweight MLP adapter when scaling LLM backbone size demonstrates that generative components can be decoupled from LLM scaling, with implications for how future unified models manage scale.

The video capability at 2B parameters competitive with 30B dedicated models is a notable efficiency result, though the 7B model's inability to include video due to compute cost reveals the limits of this efficiency at practical frontier scales.

## Key Concepts

- [[entities/bagel|Bagel]]
- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/flow-matching|Flow Matching]]
- [[entities/geneval|GenEval]]
- [[entities/llava-onevision|LLaVA-OneVision]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/siglip|SigLIP]]
