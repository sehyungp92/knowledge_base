---
type: source
title: 'Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned
  Representations'
source_id: 01KJTPP5WBNZNR9WY0VMZ7TH3T
source_type: paper
authors:
- Jiaming Han
- Hao Chen
- Yang Zhao
- Hanyu Wang
- Qi Zhao
- Ziyan Yang
- Hao He
- Xiangyu Yue
- Lu Jiang
published_at: '2025-06-23 00:00:00'
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
claim_count: 20
tags: []
---
# Vision as a Dialect: Unifying Visual Understanding and Generation via Text-Aligned Representations

> This paper introduces Tar (Text-Aligned Representation), a unified multimodal LLM that resolves the longstanding conflict between visual understanding and generation by tokenizing images into a discrete semantic space seeded directly from a frozen LLM's vocabulary. By eliminating modality-specific encoders and alignment pre-training stages, Tar demonstrates that a shared representation enables the two tasks to mutually reinforce each other — overturning the prevailing assumption that joint training necessarily creates inter-task interference.

**Authors:** Jiaming Han, Hao Chen, Yang Zhao, Hanyu Wang, Qi Zhao, Ziyan Yang, Hao He, Xiangyu Yue, Lu Jiang
**Published:** 2025-06-23
**Type:** paper

---

## Problem Statement

Unified multimodal LLMs that handle both visual understanding and generation have long been hampered by a fundamental representation conflict. Prior approaches split into three flawed camps:

- **Pixel-level discrete tokenizers** (VQVAE, used in Emu3 and Chameleon) encode pixel dependencies but lack high-level semantics — Chameleon scores only 22.4 on MMMU and 0.39 on GenEval.
- **Separate-encoder designs** (Janus) use CLIP for understanding and VQVAE for generation, preventing unified reasoning and complicating multi-turn editing; ablations show joint training under separate representations actually *hurts* rather than helps.
- **Hybrid tokenizers** (UniTok, VILA-U) jointly optimize pixel reconstruction and image-text alignment losses but fail to converge optimally for both tasks, offering no understanding improvement over VQVAE alone.
- **Diffusion-in-LLM methods** (Show-o, Transfusion) break the autoregressive paradigm, complicating unification and reducing scalability.

A secondary problem is initialization: prior works require expensive separate alignment pre-training on 50M+ samples because visual token embeddings have no natural grounding in the LLM's vocabulary space.

---

## Approach

### TA-Tok: Text-Aligned Tokenizer

The core contribution is **TA-Tok**, a visual tokenizer whose VQ codebook is initialized as:

```
C = EW
```

where `E` are **frozen** LLM token embeddings (from Qwen2.5, 150K vocab) and `W` is a learned projection matrix. Only `W` is trained. This ensures every visual token is a projected version of an existing LLM token embedding, placing visual and textual tokens in the same semantic space from the outset.

65,536 representative LLM embeddings are selected by maximum average distance to ensure broad semantic coverage. The resulting codebook is then transferred directly as the LLM's visual embedding initialization — eliminating any separate alignment stage and matching pre-alignment performance on 25M samples vs. 75M+ required otherwise.

A SigLIP2 encoder feeds into **Scale-Adaptive Pooling (SAP)** with scale factors s∈{1,2,3}, yielding {729, 169, 81} tokens per image. A lightweight ViT decoder (SAD) reconstructs pre-quantized features via cosine reconstruction loss supervised by a frozen SigLIP2 teacher; the decoder is discarded at inference.

### Generative De-Tokenizers

Since TA-Tok's semantic tokens lack pixel-level information, two complementary de-tokenizers handle image reconstruction:

- **AR-DTok**: an autoregressive LLaMA-architecture model predicting VQVAE tokens conditioned on TA-Tok's semantic tokens. Trained from scratch; offers fast sequential inference.
- **Dif-DTok**: a diffusion model fine-tuned from pretrained SANA-0.6B, using TA-Tok tokens as cross-attention conditioning. Achieves good convergence in as few as 5M samples; provides stronger generation priors for complex scenes.

### Pre-Training Tasks

Two novel tasks bridge understanding and generation during MLLM pre-training:

- **Image-to-Image (I→I)**: FLUX generates two images from the same prompt; the model must understand the first and generate a semantically similar second.
- **Text-Image-to-Image (TI→I)**: a prompt is split into text and image placeholder; the model generates a target image conditioned on both a reference image and text simultaneously.

Adding these tasks improves DPG generation score from 66.4 to 70.7 in controlled ablations and accelerates convergence.

### Self-Reflect Inference

A **Self Reflect** strategy leverages the model's own visual understanding capability to assess image-prompt alignment and iteratively improve generation outputs — a strategy uniquely enabled by the unified architecture.

---

## Results

| Model | GenEval Overall | DPG Bench |
|---|---|---|
| Chameleon-7B | 0.39 | — |
| Janus-Pro-7B | 0.80 | 84.19 |
| **Tar-7B** | **0.84** | **84.19** |
| **Tar-7B + Self Reflect** | **0.85** | **84.65** |

Tar-7B reaches 0.92 on Two Objects, 0.83 on Counting, and 0.80 on Position — substantially outperforming all unified models on these subtasks. On DPG Bench Relation, Tar achieves 93.50–93.98, exceeding even generation-only specialists like DALL·E 3 (90.58) and SD3-Medium (80.70).

Tar-1.5B (0.76 GenEval overall) already surpasses Janus-Pro-1B (0.73) and approaches Janus-Pro-7B on DPG Bench (82.96).

---

## Key Findings

**Shared representation is the enabling condition for mutual task benefit.** Joint understanding-generation training yields ~8.1% and ~5.3% improvements respectively *only* when tasks share a representation (VQVAE or TA-Tok). Janus-style separate encoders receive no benefit from joint training — confirming the representation conflict hypothesis.

**TA-Tok dominates at scale.** While hybrid tokenizers start higher, they plateau early; TA-Tok continues improving with data across all scales. Janus-style representations actively underperform VQVAE in generation despite being better in understanding, likely due to task conflict from incompatible signal types sharing a training budget.

**Codebook initialization is load-bearing.** High-dimensional (1536D) randomly initialized codebooks fail to converge during VQ training entirely. LLM-vocabulary initialization is not merely convenient — it is a convergence requirement at this design point.

**Token count creates a fundamental per-task tension.** 729 tokens per image yield best understanding performance; 169 tokens are sufficient for generation. A unified model must resolve this mismatch at inference time.

---

## Capabilities

| Capability | Maturity |
|---|---|
| Unified understanding + generation via shared discrete semantic tokens | research_only |
| LLM-vocabulary-initialized VQ codebook eliminating separate alignment stage | research_only |
| Scale-adaptive tokenization (81/169/729 tokens) for per-task tradeoff control | research_only |
| Self-Reflect inference: model assesses and refines its own generation | research_only |
| Emergent subject-driven generation and style transfer from unified pretraining | research_only |
| Cross-lingual image generation (Chinese prompts) via inherited LLM multilingualism | demo |

The emergent capabilities are particularly notable: subject-driven generation and reference-based style transfer arise from I→I and TI→I pretraining *without* explicit training objectives for those tasks, suggesting the unified representation learns compositional visual concepts as a side effect.

---

## Limitations & Open Questions

**Quantization ceiling on fine-grained understanding.** Vector quantization in TA-Tok introduces irreducible information loss. Despite mitigating this with a larger codebook and extended training, fine-grained tasks like OCR remain impaired. This is not an engineering gap — it reflects a structural property of the discretization operation. *Trajectory: improving, but ceiling unclear.*

**Faithful reconstruction is architecturally blocked.** The many-to-one mapping from pixel space to semantic space means conditioning on semantic tokens cannot uniquely determine pixel-level output. Tar excels at *diverse* generation but underperforms pixel-level tokenizers at *faithful* reconstruction — a fundamental tradeoff, not a training gap. This limits applications requiring input fidelity (editing, inpainting, reconstruction).

**Spatial reasoning loss in semantic tokens.** Position attribute generation remains substantially weaker (Tar-1.5B: 0.57 vs. Janus-Pro-7B: 0.79 on GenEval Position), suggesting semantic tokens discard spatial relational structure that continuous representations preserve. The severity of this gap warrants investigation into whether positional encodings or spatial-aware discretization can recover it.

**Guidance scale anomaly.** The unified model requires classifier-free guidance scale 10.0 vs. 1.5 for Llamagen baseline — indicating weaker conditioning adherence and potential for oversaturation or off-conditioning artifacts at inference. The cause is not fully characterized in the paper.

**Self-Reflect diminishing returns.** Improvement from Self-Reflect declines from +4.0% at 10K training steps to +1.6% at 60K steps — confirming the strategy corrects early-training alignment gaps rather than providing a general inference-time benefit for mature models.

**Resolution gap in benchmarking.** Primary generation results are reported at 256px AR-DTok resolution, limiting fair comparison with generation-only models optimized for 512px+. This understates the visual fidelity gap that may emerge at production resolutions.

**Resource barriers.** TA-Tok requires 200M images for training; the full pipeline (tokenizer + two de-tokenizers + MLLM) requires 350M+ data points across multiple stages — a significant barrier to reproduction and iteration.

**Codebook design constraint.** The requirement to seed the codebook from LLM vocabulary embeddings constrains design choices to what is representable as a linear projection of existing language embeddings. Whether this over-fits to linguistic feature structure at the expense of visual structure remains an open question.

---

## Bottlenecks Addressed & Introduced

This work **partially resolves** the representation conflict bottleneck in unified multimodal models by demonstrating that a shared discrete semantic space can support both tasks without the zero-sum tradeoff observed in prior work.

However, it **introduces or confirms** three persistent bottlenecks:

**Quantization ceiling** — Discrete unified models achieving full parity with continuous-token models on fine-grained visual tasks (OCR, localization, dense spatial understanding). Horizon: 1–2 years.

**Faithful reconstruction from semantic tokens** — Unified semantic-token models achieving both high-diversity generation and faithful input image reconstruction without separate pixel-level components. Horizon: 1–2 years.

**Resolution-agnostic generation** — End-to-end resolution-agnostic unified image generation without modular multi-stage de-tokenizer components. Horizon: months.

---

## Connections

**Architecture:** See [[themes/model_architecture|Model Architecture]] for the broader context of autoregressive vision-language design choices, and [[themes/unified_multimodal_models|Unified Multimodal Models]] for the competitive landscape this work enters.

**Representation:** The TA-Tok design sits at the intersection of [[themes/representation_learning|Representation Learning]] and [[themes/vision_language_models|Vision-Language Models]] — its core claim is that the right representational inductive bias (grounding in LLM vocabulary space) eliminates alignment overhead entirely.

**Generation:** Results on DPG Bench and GenEval position Tar within [[themes/image_generation_models|Image Generation Models]] and [[themes/generative_media|Generative Media]], where the benchmark comparison is primarily against Janus-Pro and diffusion specialists.

**Competing approaches:** The failure mode of hybrid tokenizers (convergence plateau with scale) is a direct counterargument to VILA-U and UniTok-style designs. The failure of Janus-style separate encoders under joint training challenges the prevailing design assumption that modality-specific encoders are necessary for quality.

---

## Open Questions

1. Can the quantization ceiling be pushed substantially lower with learned adaptive codebooks, or is the discretization-understanding tradeoff a hard limit at current VQ architectures?
2. Is the guidance scale anomaly (10.0 vs. 1.5) symptomatic of a conditioning weakness that degrades structured spatial outputs, and does it explain the position attribute gap?
3. Does the LLM-vocabulary seeding introduce linguistic priors into the visual representation that help (semantic grounding) or hurt (inappropriate feature structure for spatial/texture tasks)?
4. Would TA-Tok initialized from a vision-language model's vocabulary (e.g., SigLIP embeddings projected into a shared space) outperform pure LLM vocabulary seeding for visual tasks?
5. Can Self-Reflect be extended to a multi-step refinement loop without degeneration, or does the diminishing returns pattern reflect a fixed-point stability issue?

## Key Concepts

- [[entities/flux|FLUX]]
- [[entities/geneval|GenEval]]
- [[entities/qwen25|Qwen2.5]]
