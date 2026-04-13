---
type: source
title: Emerging Properties in Unified Multimodal Pretraining
source_id: 01KJTT03GZHVCFHR1G67X3WN2K
source_type: paper
authors:
- Chaorui Deng
- Deyao Zhu
- Kunchang Li
- Chenhui Gou
- Feng Li
- Zeyu Wang
- Shu Zhong
- Weihao Yu
- Xiaonan Nie
- Ziang Song
- Guang Shi
- Haoqi Fan
published_at: '2025-05-20 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- pretraining_and_scaling
- pretraining_data
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Emerging Properties in Unified Multimodal Pretraining

**Authors:** Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, Guang Shi, Haoqi Fan
**Published:** 2025-05-20 00:00:00
**Type:** paper

## Analysis

# Emerging Properties in Unified Multimodal Pretraining
2025-05-20 · paper · Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li et al. (12 total)
https://arxiv.org/pdf/2505.14683

---

### Motivation & Prior Limitations
- A substantial gap existed between open-source unified multimodal models and proprietary systems like GPT-4o and Gemini 2.0, with the root cause identified as reliance on image-text paired data rather than large-scale interleaved multimodal data.
  - Prior unified open-source models such as Janus-Pro and Emu3 were trained predominantly on image-text pairs, missing the richer cross-modal supervision that video and web-interleaved data provide.
  - Benchmark evaluations (cited in reference [10]) documented this capability gap but the underlying techniques of proprietary systems remained undisclosed.

- Existing unified architectures introduced explicit information bottlenecks between understanding and generation modules that constrained scaling and long-context reasoning.
  - "External Diffuser" designs compress LLM context into a small set of latent tokens before handing off to a diffusion model, causing substantial information loss in long-context multimodal reasoning scenarios.
  - "Quantized AR" approaches use discrete visual tokenizers that empirically underperform diffusion-based generation quality and suffer from sequential inference latency.

- Standard benchmarks for multimodal understanding (MME, MMMU) and generation (GenEval) did not capture compositional, world-knowledge-intensive, or free-form manipulation capabilities, leaving a measurement gap for emergent abilities.
  - Classical editing benchmarks like GEdit-Bench do not require multi-step reasoning or world knowledge integration, making them insensitive to the highest-order capabilities the authors were targeting.

---

### Proposed Approach
- BAGEL is a decoder-only, bottleneck-free Integrated Transformer with 7B active / 14B total parameters using a Mixture-of-Transformers (MoT) architecture, where a full-size understanding expert and a full-size generation expert share self-attention at every layer but process tokens through separate FFNs, enabling lossless long-context interaction between modalities.
  - Unlike MoE designs that only duplicate the FFN, MoT duplicates all trainable parameters, giving each modality its own optimization trajectory while keeping FLOPs identical to a dense baseline.
  - Hard routing assigns VAE tokens exclusively to the generation expert and text/ViT tokens to the understanding expert, following the Qwen-VL series strategy.
  - Ablations at 1.5B scale confirm MoT consistently outperforms both Dense and MoE variants, with the largest gap on MSE (generation) loss.

- The model uses two separate visual encoders: SigLIP2-so400m/14 (up to 980×980, NaViT native-aspect-ratio) for semantic understanding, and a frozen FLUX VAE (8× downsample, 16 latent channels) for pixel-level generation, with Rectified Flow used for visual token prediction.
  - A generalized causal attention mechanism partitions tokens by modality split, allows full bidirectional attention within vision splits, and uses causal attention for text; clean VAE and ViT tokens are cached for KV reuse, while noised VAE tokens are replaced by clean counterparts once generation is complete.
  - Diffusion Forcing is applied for multi-image interleaved generation, adding independent noise levels to different images and conditioning each on noisy predecessors.

- Training on ~5.1T tokens proceeds through four stages (Alignment → Pre-training at 2.5T → Continued Training at 2.6T with higher resolution and increased interleaved ratio → SFT at 72.7B), with generation data sampled at roughly 4× the rate of understanding data based on controlled ablations showing this reduces MSE loss without degrading CE loss.
  - The interleaved data pipeline combines 45M video-derived sequences (inter-frame captions distilled from a Qwen2.5-VL-7B captioner) and 20M web-derived documents (two-stage fastText + LLM topic selection, caption-first scaffolding strategy) alongside standard VLM and T2I pairs.
  - 500K reasoning-augmented examples with chain-of-thought traces (inspired by DeepSeek-R1) are constructed across text-to-image, free-form manipulation, and conceptual edit categories to enable language-mediated visual planning.

- IntelligentBench is introduced as a new 350-example evaluation suite for free-form image manipulation requiring world knowledge and multi-step reasoning, scored by GPT-4o on request fulfillment, visual consistency, and knowledge-grounded creativity.

---

### Results & Capabilities
- BAGEL-7B outperforms all open-source unified models on multimodal understanding, achieving 85.0 on MMBench, 55.3 on MMMU, 67.2 on MM-Vet, and 73.1 on MathVista — exceeding specialized understanding-only models Qwen2.5-VL-7B and InternVL2.5-7B on most benchmarks.
  - These gains come without freezing any backbone components, unlike MetaQuery-XL which relies on a frozen Qwen2.5-VL backbone and thus has limited adaptability.

- On GenEval text-to-image generation, BAGEL achieves 0.82 overall without an LLM rewriter and 0.88 with one, surpassing FLUX.1-dev (0.82), SD3-Medium (0.74), and Janus-Pro-7B (0.80).
  - On the WISE world-knowledge benchmark, BAGEL scores 0.52 without reasoning and 0.70 with Self-CoT, surpassing all open-source models (previous SOTA MetaQuery-XL: 0.55) and approaching GPT-4o (0.80).

- On GEdit-Bench image editing, BAGEL achieves overall scores (G_O) of 6.52 (EN) and 6.50 (CN), competitive with the specialist Step1X-Edit (6.70) and surpassing Gemini 2.0 (6.32 EN), while natively supporting Chinese prompts without translation.

- On IntelligentBench, BAGEL scores 44.9 (55.3 with Self-CoT), dramatically outperforming the best open-source alternative Step1X-Edit (14.9) and approaching Gemini 2.0 (57.6), with a large gap remaining to GPT-4o (78.9).

- The paper documents a clear emergent capability ordering as trai

## Key Claims

1. There is a substantial gap in unified multimodal understanding and generation between academic models and proprietary systems such as GPT-4o and Gemini 2.0.
2. The key to closing the gap between academic and proprietary unified multimodal models lies in scaling with carefully structured multimodal interleaved data integrating texts, images, videos, and web s
3. Scaling with diverse multimodal interleaved data causes BAGEL to exhibit emerging capabilities in complex multimodal reasoning including free-form image manipulation, future frame prediction, 3D manip
4. As BAGEL scales with interleaved multimodal pretraining, capabilities emerge in a specific sequence: basic understanding and high-fidelity generation first, then complex editing and free-form visual m
5. The Mixture-of-Transformers (MoT) architecture consistently outperforms both Dense and Mixture-of-Experts (MoE) designs, with the gap most pronounced on multimodal generation tasks.
6. Decoupling parameters for generation from those for understanding mitigates optimization challenges arising from competing modality-specific learning objectives.
7. The External Diffuser approach introduces an explicit bottleneck between understanding and generation modules, risking substantial information loss particularly in long-context multimodal reasoning.
8. Autoregressive visual generation with discrete tokenizers produces empirically inferior visual quality compared to diffusion-based models and suffers from higher inference latency.
9. The Integrated Transformer approach demands substantially higher training compute than the External Diffuser solution but maintains a bottleneck-free context enabling lossless interaction between gene
10. BAGEL has 7B active parameters and 14B total parameters, using a Mixture-of-Transformers architecture initialized from Qwen2.5 LLM.

## Capabilities

- Open-source 7B active parameter (14B total) unified model achieves both multimodal understanding (surpassing top-tier open-source VLMs on standard leaderboards) and text-to-image generation quality competitive with SD3 and FLUX.1-dev, in a single decoder-only architecture trained on interleaved mult
- Free-form visual manipulation as emergent capability: unified model performs open-ended image editing (rotation, 3D manipulation, multiview synthesis, conceptual edits) not constrained to predefined editing operations, extending beyond classical image editing scope
- Future frame prediction and world navigation as emergent capabilities in a unified multimodal model, arising from interleaved video pretraining without task-specific architectures — model learns temporal continuity and spatial navigation from video data as part of general pretraining
- Staged emergence of compositional multimodal capabilities from scaling interleaved pretraining: capabilities appear in a predictable sequence — basic understanding+generation convergence first, then complex editing and free-form manipulation, then long-context reasoning that synergizes previously in
- Language-based chain-of-thought reasoning before image generation: model generates explicit reasoning traces (R1-style CoT) to clarify visual goals and improve planning before producing output images, enabling abstract conceptual edits grounded in multimodal understanding
- Bottleneck-free unified multimodal architecture using Mixture-of-Transformers (MoT) with shared self-attention: separate expert parameter spaces for understanding and generation coexist with full information flow, enabling long-context interaction without the compression losses of adapter-based appr

## Limitations

- Substantial performance gap remains between open-source unified multimodal models (including BAGEL) and proprietary systems like GPT-4o and Gemini 2.0, whose underlying techniques are undisclosed — the gap's full magnitude and the specific techniques required to close it are unknown
- Understanding (CE) loss exhibits high step-to-step fluctuations during joint multimodal training — an acknowledged instability arising from heterogeneous interleaved data — creating optimization challenges that worsen as data diversity increases
- Optimization landscapes for understanding and generation remain partially decoupled even in the bottleneck-free MoT architecture — full joint optimization of both objectives is explicitly acknowledged as not achieved
- VAE model frozen during all training stages, tying generation quality permanently to the pre-existing FLUX VAE's representational capacity and preventing end-to-end optimization of the full generation pipeline
- Architecture comparisons (Dense vs MoE vs MoT) conducted only at 1.5B parameter scale; the reported superiority of MoT is not directly validated at the deployed 7B active / 14B total parameter scale
- Distilled lightweight video captioning model suffers from hallucination, requiring caption length cap at 30 tokens — severely limiting the richness of temporal supervision in video-derived interleaved training data
- Standard public benchmarks fail to capture the emergent compositional multimodal capabilities of unified models — BAGEL's most distinctive capabilities are only revealed by a new proprietary benchmark (IntelligentBench), whose design and coverage are unverified by the community
- MoT architecture doubles total parameter count (7B active, 14B total) vs a dense baseline with identical FLOPs — significantly increasing memory requirements for serving and creating deployment barriers, particularly for resource-constrained settings
- Only 500K reasoning-augmented multimodal examples were constructed — a small fraction of the 5T+ token pretraining corpus — potentially limiting reasoning capability depth and restricting transfer between multimodal understanding and generation
- Constructing high-quality interleaved multimodal training data requires expensive multi-stage pipelines (large VLM inference for captioning, LLM-based topic classification and quality filtering, multi-stage rule-based filters) that are difficult to replicate without significant compute and engineeri
- Unified multimodal pretraining requires precise empirical tuning of data-sampling ratios and learning rates to balance understanding and generation signals — a manual process without principled guidelines, creating reproducibility barriers for the community
- Autoregressive (quantized AR) visual generation produces empirically inferior quality to diffusion-based models and suffers from high inference latency due to sequential token generation — limiting viability of the pure AR approach for visual generation

## Bottlenecks

- Constructing sufficient high-quality interleaved multimodal data at scale remains a critical bottleneck — internet data is not natively in semantically aligned interleaved format, requiring expensive multi-stage pipelines (LLM filtering, VLM captioning, quality control) that are difficult to scale b
- Joint understanding-generation optimization conflict in unified models: the two objectives steer model parameters toward different regions of parameter space, creating training instability and requiring manual hyperparameter tuning that limits reproducibility and automated scaling
- Scale bottleneck for reasoning-augmented multimodal generation data: generating high-quality chain-of-thought reasoning traces for multimodal generation tasks requires expensive chained VLM inference, limiting achievable volume to ~500K examples — insufficient to fully develop reasoning-to-generatio

## Breakthroughs

- Large-scale interleaved multimodal pretraining induces staged emergence of compositional capabilities in a unified model: free-form manipulation, world navigation, 3D manipulation, and future frame prediction emerge as scaling properties — not from task-specific architectures but from a single bottl
- Mixture-of-Transformers (MoT) architecture with shared self-attention resolves the unified model bottleneck-connector problem: dedicated parameter spaces for understanding and generation coexist with full lossless information flow, outperforming both dense transformers and MoE variants on joint unde

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/pretraining_data|pretraining_data]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/bagel|Bagel]]
- [[entities/flexattention|FlexAttention]]
- [[entities/qk-norm|QK-Norm]]
- [[entities/rectified-flow|Rectified Flow]]
