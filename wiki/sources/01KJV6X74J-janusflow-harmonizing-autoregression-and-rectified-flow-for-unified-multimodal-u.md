---
type: source
title: 'JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal
  Understanding and Generation'
source_id: 01KJV6X74JDVGQFRCVXY0381BG
source_type: paper
authors:
- Yiyang Ma
- Xingchao Liu
- Xiaokang Chen
- Wen Liu
- Chengyue Wu
- Zhiyu Wu
- Zizheng Pan
- Zhenda Xie
- Haowei Zhang
- Xingkai yu
- Liang Zhao
- Yisong Wang
- Jiaying Liu
- Chong Ruan
published_at: '2024-11-12 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation

JanusFlow presents a 1.3B unified multimodal model that integrates rectified flow directly into a standard autoregressive LLM framework, achieving state-of-the-art performance among unified models on both image generation (GenEval 0.63, MJHQ FID 9.51) and multimodal understanding (MMBench 74.9), while surpassing several specialized models two to five times its size. Its central contributions are a decoupled encoder design that prevents representational interference between understanding and generation, and a representation alignment regularization (REPA) technique that injects semantic structure into the noisy-input feature space during generation training.

**Authors:** Yiyang Ma, Xingchao Liu, Xiaokang Chen, Wen Liu, Chengyue Wu, Zhiyu Wu, Zizheng Pan, Zhenda Xie, Haowei Zhang, Xingkai Yu, Liang Zhao, Yisong Wang, Jiaying Liu, Chong Ruan
**Published:** 2024-11-12
**Type:** paper

---

## Problem Context

Unified multimodal models have consistently underperformed relative to specialized counterparts, for two structural reasons:

**Architectural coupling.** Systems that bolt a pre-trained diffusion model onto an LLM (SEED-X, DreamLLM, Emu) are not truly unified: the LLM only generates conditioning signals while the generative component remains architecturally separate. SEED-X at 17B achieves GenEval 0.49, well below dedicated flow models.

**Discretization ceiling.** Vector-quantized autoregressive methods (Chameleon, Show-o, LWM) are bounded by the fidelity of image tokenization. Show-o at 1.3B achieves FID 15.18 on MJHQ and GenEval 0.53, below dedicated flow-based models like SDXL.

**Shared encoder conflict.** Unified models that integrate diffusion with LLMs (Transfusion, Show-o) typically use a single shared encoder for both understanding and generation. This creates a representational conflict: understanding benefits from rich semantic encoders (SigLIP, CLIP), while generation requires encoders conditioned on noisy continuous latents. Janus (1.3B) demonstrated the value of decoupled encoders for the discrete case but did not incorporate continuous flow-based generation.

---

## Architecture

JanusFlow is built on a 1.3B autoregressive LLM with two entirely separate visual encoder pathways and a lightweight convolutional generation decoder.

### Decoupled Encoders

- **Understanding encoder:** [[entities/siglip|SigLIP]]-Large-Patch/16 (pretrained, ~300M params), producing rich semantic features for comprehension tasks.
- **Generation encoder:** Freshly initialized ConvNeXt blocks (~70M params), encoding noisy SDXL-VAE latent states during rectified flow training.
- **Generation decoder:** Paired ConvNeXt decoder predicting velocity vectors in the VAE latent space.

Ablation (Exp. B vs. F) confirms the necessity of this split: a shared ConvNeXt encoder collapses understanding quality (GQA 44.04 vs. 54.83) while providing only marginal FID improvement.

### Rectified Flow Integration

Rather than requiring bidirectional attention (Transfusion) or hybrid attention masks (Show-o), JanusFlow passes noisy latent states through the LLM under standard causal attention, then decodes velocity vectors with the generation decoder. Euler integration iterates this loop across 30 steps to produce the final image. The finding that causal attention suffices is a key result, though it rests on preliminary experiments rather than a systematic ablation.

Classifier-free guidance is applied by randomly dropping 10% of text prompts during training, using Stable Diffusion 3's logit-normal time distribution.

### Representation Alignment Regularization (REPA)

During generation training, intermediate LLM features (after the 6th transformer block) are projected via a small MLP and aligned to stop-gradient SigLIP features of the target image via cosine similarity loss. This injects semantic structure into the LLM's noisy-input feature space without back-propagating into the understanding encoder. Prior work demonstrated REPA's utility for diffusion transformers; JanusFlow extends this to LLM-based architectures, a novel architectural context.

Removing REPA raises FID from 17.61 to 19.84 and lowers CLIP score from 26.40 to 24.94, confirming dual benefits for both image quality and semantic alignment.

### Three-Stage Training

1. **Adaptation:** Freeze the LLM and SigLIP; train only the generation encoder/decoder and projection layers.
2. **Unified pre-training:** Unfreeze all components except SigLIP; train with higher understanding data ratio initially.
3. **Supervised fine-tuning:** Unfreeze SigLIP; shift data ratios progressively toward generation to accommodate slower diffusion convergence.

This curriculum is a workaround for a structural problem: autoregressive understanding and rectified flow generation have mismatched convergence rates that resist single-stage end-to-end training.

---

## Results

### Generation

| Benchmark | JanusFlow 1.3B | Janus 1.3B | Show-o 1.3B | SDXL 2.6B | Transfusion 7.3B |
|---|---|---|---|---|---|
| GenEval | 0.63 | 0.61 | 0.53 | 0.55 | 0.63 |
| MJHQ FID | 9.51 | 10.10 | 15.18 | — | — |
| DPG-Bench | 80.09% | — | — | 74.65% | — |

JanusFlow matches Transfusion at 1/5th the parameter count and surpasses DALL-E 2 (6.5B, GenEval 0.52). DPG-Bench performance (80.09%) is comparable to Emu3-Gen at 8B.

A weakness surfaces in compositional generation: Two-Object score (0.59) lags behind Janus (0.68) despite overall GenEval parity, suggesting that flow-based generation trades some compositional precision for overall quality.

### Understanding

| Benchmark | JanusFlow 1.3B | LLaVA-v1.5 7B | Qwen-VL-Chat 7B |
|---|---|---|---|
| MMBench | 74.9 | 64.3 | — |
| SeedBench | 70.5 | — | — |
| GQA | 60.3 | — | 57.5 |
| VQAv2 | 79.8 | — | — |
| POPE | 88.0 | — | — |

These results establish that a 1.3B unified model can exceed dedicated 7B understanding models on several benchmarks, though the comparison is selective.

---

## Limitations and Open Questions

**Reasoning ceiling.** MMMU score is 29.3 vs. Qwen2-VL 7B's 54.1, a 25-point gap indicating the unified architecture imposes significant costs on advanced reasoning tasks. The understanding-generation trade-off is deeper than headline benchmarks suggest.

**MM-Vet regression.** Rectified flow integration causes MM-Vet to drop from 34.3 (Janus) to 30.9 (JanusFlow), despite improvements elsewhere. The mechanism is uncharacterized: it may reflect data ratio shifts, representational interference, or LLM capacity partitioning between tasks.

**Resolution constraint.** Generation is fixed at 384×384. No higher resolution capability is demonstrated or discussed. Production-grade specialized models routinely support 1024×1024 or higher, making this a significant quality gap for practical use.

**TextVQA gap.** Score of 55.5 versus Qwen2-VL's 84.3, a ~29-point deficit, reveals a pronounced performance cliff on fine-grained text recognition within images.

**Text rendering in generation.** Evaluation benchmarks (GenEval, DPG-Bench, FID) do not assess legibility or accuracy of text within generated images. This omission conceals a likely critical weakness for production applications.

**Inference cost.** 30 sampling steps, each requiring a full LLM forward pass, combined with CFG doubling the compute per step, creates substantial latency. No throughput or latency metrics are reported.

**Training cost.** ~1,600 A100 GPU days across three stages, comparable to or exceeding specialized models at equivalent scale. The efficiency argument for unified architectures does not yet hold at training time.

**Causal attention assumption.** The finding that causal attention suffices is based on "preliminary experiments" only. Whether bidirectional or structured attention patterns could improve generation quality at larger scale remains an open question.

**Sequence length ceiling.** The LLM supports a 4,096 token context, creating hard constraints on multi-image reasoning, long conversations, and high-resolution processing.

**Temporal modality gap.** Video understanding and generation are architecturally excluded. Temporal reasoning remains entirely unaddressed.

---

## Landscape Contributions

### Bottlenecks Addressed (Partially)

**Task interference in unified encoders** (see [[themes/unified_multimodal_models|Unified Multimodal Models]]): JanusFlow's decoupled encoder design demonstrates that architectural separation is necessary but introduces additional parameters and prevents fully joint optimization. This sidesteps rather than solves the underlying representational conflict.

**Convergence rate mismatch:** The three-stage training curriculum with dynamic data ratios manages the conflicting training dynamics of autoregressive understanding and flow-based generation. A single-stage end-to-end approach remains out of reach.

**Inference latency for LLM-integrated generation:** Multi-step ODE solving at LLM scale blocks real-time or interactive deployment. This bottleneck is acknowledged implicitly but not addressed.

### New Bottleneck Surfaced

The paper reveals that integrating continuous flow-based generation into a unified LLM framework does not eliminate the understanding-generation trade-off; it relocates it. Task interference shifts from the encoder (solved by decoupling) to the LLM backbone itself, visible in the MM-Vet regression and MMMU gap. Architectural separation of encoders is a necessary but insufficient condition for true unification without capability degradation.

---

## Connections

- [[themes/generative_media|Generative Media]]
- [[themes/image_generation_models|Image Generation Models]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/unified_multimodal_models|Unified Multimodal Models]]
- [[themes/vision_language_models|Vision-Language Models]]

**Related systems:** Janus (predecessor, discrete AR), Transfusion (7.3B LLM+diffusion, matched on GenEval), Show-o (hybrid attention, VQ-based), SDXL (specialized generation baseline), SigLIP (understanding encoder used).

**Techniques carried forward:** REPA (from DiT literature, extended to LLM-based architectures), ConvNeXt as generation encoder/decoder, logit-normal time distribution (from SD3).

## Key Concepts

- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/fréchet-inception-distance|Fréchet Inception Distance]]
- [[entities/geneval|GenEval]]
- [[entities/mmbench|MMBench]]
- [[entities/rectified-flow|Rectified Flow]]
- [[entities/show-o|Show-o]]
- [[entities/vqav2|VQAV2]]
