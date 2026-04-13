---
type: source
title: Qwen2.5-VL Technical Report
source_id: 01KJV42M0KB822AY266HGWP4JD
source_type: paper
authors:
- Shuai Bai
- Keqin Chen
- Xuejing Liu
- Jialin Wang
- Wenbin Ge
- Sibo Song
- Kai Dang
- Peng Wang
- Shijie Wang
- Jun Tang
- Humen Zhong
- Yuanzhi Zhu
- Mingkun Yang
- Zhaohai Li
- Jianqiang Wan
- Pengfei Wang
- Wei Ding
- Zheren Fu
- Yiheng Xu
- Jiabo Ye
- Xi Zhang
- Tianbao Xie
- Zesen Cheng
- Hang Zhang
- Zhibo Yang
- Haiyang Xu
- Junyang Lin
published_at: '2025-02-19 00:00:00'
theme_ids:
- finetuning_and_distillation
- generative_media
- model_architecture
- multimodal_models
- post_training_methods
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Qwen2.5-VL Technical Report

> Qwen2.5-VL is Alibaba's next-generation vision-language model series that advances multimodal perception through four coordinated architectural innovations: window attention in the visual encoder (reducing complexity from quadratic to linear), absolute-time-aligned MRoPE for consistent temporal grounding across variable frame rates, absolute-coordinate spatial grounding across 10,000+ object categories, and a unified HTML-format omni-document parsing capability. The 72B flagship matches GPT-4o and Claude 3.5 Sonnet across diverse benchmarks while remaining open-source, with the series scaling from a deployable 3B edge model to the full 72B, trained on a 4.1T token corpus more than triple the size of its predecessor.

**Authors:** Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, Junyang Lin
**Published:** 2025-02-19
**Type:** paper
**Link:** https://arxiv.org/pdf/2502.13923

---

## Motivation

Prior large vision-language models (LVLMs) occupied what the authors call "the middle layer of a sandwich cookie" — capable but not exceptional. Three structural bottlenecks constrained progress:

1. **Quadratic ViT complexity.** Full self-attention over variable-resolution images scales quadratically with patch count, making native-resolution processing of large images and long videos computationally prohibitive.
2. **FPS-dependent temporal encoding.** In Qwen2-VL, MRoPE temporal position IDs were tied to frame count rather than wall-clock time. A model trained on 24 FPS video could not reliably generalize to 1 FPS video representing the same events, and second-level event localization was structurally inaccessible.
3. **Pipeline-based document parsing.** Extracting structured content from documents required chaining separate specialist models for layout analysis, OCR, chart interpretation, and formula recognition, rather than a single unified pass.

The pre-training corpus was also limited to 1.2T tokens in Qwen2-VL, constraining the breadth of grounded visual knowledge.

---

## Architecture

### Visual Encoder

The ViT is trained from scratch (initialized from DataComp and in-house data via CLIP pre-training, followed by vision-language alignment and end-to-end fine-tuning) rather than adapted from a frozen encoder. It uses RMSNorm and SwiGLU activations to align with LLM design principles.

The key efficiency change is **windowed attention**: only four layers (indices 7, 15, 23, 31) employ full self-attention; all remaining layers use windowed attention with a maximum 112×112 pixel window (corresponding to 8×8 patches). This reduces encoder complexity from quadratic to linear in patch count while preserving native resolution processing. For video inputs, two consecutive frames are grouped during 3D patch partitioning, further compressing the token sequence fed downstream.

### Vision-Language Merger

Rather than passing raw patch features directly to the LLM, an MLP-based merger groups spatially adjacent sets of four patch features, concatenates them, and projects through a two-layer MLP to LLM embedding dimension. This 4× compression reduces visual token sequences before they enter the language model.

### Multimodal Rotary Position Embedding Aligned to Absolute Time (MRoPE-AT)

The temporal component of MRoPE is now derived from actual timestamps rather than frame indices. The model learns temporal pace through the inter-ID intervals: a video sampled at 1 FPS and one at 24 FPS representing the same event receive consistent temporal position signals. No additional parameters or compute are required. This directly enables cross-FPS generalization and second-level event localization in hour-long videos.

### Grounding

Bounding boxes and point coordinates are expressed in **absolute pixel values** rather than normalized fractions. This allows the model to learn real-world scale information inherently, rather than treating a 10×10 pixel object identically in a 100×100 and a 4000×3000 image. Training covers 10,000+ object categories, with copy-paste augmentation and synthesis from Grounding DINO and SAM to build both bounding-box and point-level datasets.

### Omni-Document Parsing

A unified HTML-based ground truth format encodes layout bounding boxes, text content, tables, charts, equations, music sheets, and chemical formulas within a single structured representation. This allows a single model pass to replace the multi-model document parsing pipeline.

---

## Training

### Pre-training

Three phases with increasing sequence length and data diversity:

1. ViT-only training on image captions, knowledge, and OCR data at sequence length 8192.
2. Full model training on diverse multimodal data at a longer sequence length.
3. A final phase at maximum sequence length with the full data mixture.

The corpus scales from 1.2T tokens (Qwen2-VL) to **4.1T tokens**, a 3.4× increase. To handle variable image sizes, samples are dynamically packed based on input sequence lengths to maintain consistent GPU computational loads across batches.

### Post-training

A two-stage pipeline: **SFT** on approximately 2 million entries (50% pure text, 50% multimodal) followed by **DPO** for preference alignment. The ViT is frozen throughout both stages. The DPO phase focuses exclusively on image-text and pure text data, processing each sample only once.

**Rejection sampling for CoT reasoning:** An intermediate Qwen2.5-VL checkpoint generates chain-of-thought responses on annotated datasets. Only samples where model output matches ground truth are retained. Rule-based filters then remove responses with code-switching, excessive length, or repetition. This confines enhanced reasoning training to tasks with verifiable answers — a significant scope limitation.

---

## Results

### General VQA (72B)

| Benchmark | Qwen2.5-VL-72B | Prior SoTA |
|---|---|---|
| MMBench-EN | 88.6 | 88.3 |
| MMStar | 70.8 | 69.5 |
| MMVet | 76.2 | 74.0 |
| MuirBench | 70.7 | 63.5 |

### Document & OCR (72B)

| Benchmark | Score | Comparison |
|---|---|---|
| OCRBench | 885 | vs. InternVL2.5-78B 854 |
| DocVQA | 96.4 | leads GPT-4o, Claude 3.5 Sonnet |
| InfoVQA | 87.3 | leads all compared models |
| OCRBench_v2 (EN) | — | +9.6% vs. Gemini 1.5-Pro |
| OCRBench_v2 (ZH) | — | +20.6% vs. Gemini 1.5-Pro |

### Video Understanding (72B)

| Benchmark | Qwen2.5-VL-72B | GPT-4o |
|---|---|---|
| LVBench | 47.3 | 30.8 |
| MLVU | 74.6 | 64.6 |
| Video-MME (no subs) | 73.3 | — |
| Charades-STA (mIoU) | 50.9 | 35.7 |
| LongVideoBench | 60.7 | 66.7 |

Charades-STA validates MRoPE-AT for temporal grounding. The LongVideoBench gap (60.7 vs. GPT-4o 66.7) signals that proprietary models retain advantages in sustained long-form comprehension.

### Spatial Grounding (72B)

- RefCOCO/+/g: 92.7 / 94.6 / 89.7 / 88.9 / 92.2 / 89.9, competitive with specialist Grounding DINO
- ODinW-13: 43.1 mAP (vs. Grounding DINO specialist 55.0; Gemini 1.5-Pro 36.7)
- CountBench: 93.6 (leads Claude 3.5 Sonnet 89.7)
- PointGrounding: 67.5 (vs. Molmo 72B 69.2)

### GUI Agents (72B)

- AndroidWorld: 35% (state-of-the-art on mobile)
- MobileMiniWob++: 68%
- ScreenSpot Pro: 43.6% (vs. Aguvis-72B 23.6%; Qwen2-VL 1.6%)
- OSWorld (desktop): **8.83%** (vs. Claude 14.90%)

The 85% relative improvement on ScreenSpot Pro is the most striking GUI result, but the OSWorld figure exposes a persistent gap between grounding capability and operational reliability in complex desktop environments.

### Pure Text (72B, no degradation from multimodal training)

- HumanEval: 87.8
- MATH: 83.0
- IFEval: 86.3

---

## Capabilities

- [[themes/model_architecture|Linear-complexity native-resolution ViT]] via window attention, enabling production-scale processing of high-resolution images and extended videos.
- [[themes/video_and_world_models|Hour-long video comprehension]] with second-level event localization through absolute-time MRoPE.
- [[themes/multimodal_models|Cross-FPS temporal generalization]] without additional parameters, resolving the frame-rate dependency of prior MRoPE formulations.
- [[themes/vision_language_models|Omni-document parsing]] handling handwriting, tables, charts, equations, music sheets, and chemical formulas through a unified HTML-format ground truth.
- Scale-aware spatial grounding with absolute coordinates across 10,000+ object categories.
- GUI agent operation on mobile platforms (AndroidWorld, MobileMiniWob++) without Set-of-Mark auxiliary marks.
- Edge deployment at 3B parameters with competitive multimodal performance.
- Maintained pure-text performance after multimodal training, contradicting the common assumption of capability tradeoff.

---

## Limitations and Open Questions

### Confirmed Weaknesses

**Desktop agent performance collapse.** OSWorld scores sit at 8.83% for Qwen2.5-VL-72B versus 14.90% for Claude. The jump from 87.1% on standard ScreenSpot to 43.6% on ScreenSpot Pro, and then to single-digit task completion on OSWorld, reveals that grounding accuracy and agent reliability are qualitatively different problems. Complex desktop software interaction remains a [[themes/vision_language_models|major unsolved challenge]].

**Hallucination regression.** Qwen2.5-VL-72B scores 55.2 on HallBench versus 58.1 for both the prior open-source SoTA and its predecessor Qwen2-VL-72B. Capability improvements in perception and reasoning appear to trade off against object hallucination, a pattern worth monitoring across model generations.

**Multimodal CoT visual grounding.** Intermediate chain-of-thought reasoning steps fail to adequately integrate visual information, either ignoring relevant visual cues or misinterpreting them. VLM CoT degrades toward text-only reasoning, particularly when multiple reasoning steps are required before returning to visual evidence. This is a [[themes/post_training_methods|structural limitation of current CoT training paradigms]] applied to multimodal inputs.

**Frame budget ceiling.** A hard cap of 768 frames and 24,576 video tokens per query limits temporal resolution for hour-long video analysis. This is not a model capability but a practical inference constraint, and it imposes a ceiling on the LVBench and MLVU results reported.

**Point grounding below specialist.** Despite significant investment in pointing datasets, Qwen2.5-VL-72B (67.5) trails the specialist Molmo 72B (69.2) on PointGrounding, suggesting that generalist training still leaves gaps versus focused specialist training.

**Long-form video gap vs. proprietary models.** LongVideoBench (60.7 vs. GPT-4o 66.7) and MMVU (62.9 vs. GPT-4o 67.4) show consistent underperformance on sustained temporal comprehension tasks, even while dominating on pure long-video retrieval (LVBench, MLVU).

### Structural Limitations of Training Method

**Rejection sampling requires verifiable answers.** The CoT reasoning enhancement pipeline begins with ground-truth annotations and filters by answer correctness. This confines enhanced reasoning training to tasks with computable correct answers, excluding open-ended visual analysis, aesthetic judgment, and scientific hypothesis generation.

**Interleaved web data quality.** The authors acknowledge that most available interleaved image-text web data lacks meaningful image-text co-reference and is often noisy. This limits what can be learned from scale in multimodal pre-training, a bottleneck that affects the entire field, not just this work.

**Open-source data variability.** Synthetic and web-sourced datasets require extensive multi-stage filtering pipelines before becoming useful, introducing significant preprocessing cost and potential distribution artifacts in the final training mixture.

---

## Landscape Significance

This paper contributes to several active themes:

- **[[themes/model_architecture|Model Architecture]]:** Window attention in ViT and absolute-time MRoPE are transferable techniques addressing known scaling bottlenecks in vision encoders and temporal encoding.
- **[[themes/multimodal_models|Multimodal Models]] / [[themes/vision_language_models|Vision-Language Models]]:** The open/closed-source frontier gap in multimodal benchmarks is substantially narrowed. The 72B model is the strongest open-source generalist VLM at its size class as of its release.
- **[[themes/video_and_world_models|Video and World Models]]:** Absolute-time positional encoding is a concrete solution to a previously identified bottleneck in temporal grounding. The technique is lightweight and architecture-agnostic.
- **[[themes/post_training_methods|Post-training Methods]]:** The SFT + DPO pipeline with frozen ViT is a stable recipe, but the hallucination regression raises questions about whether DPO alignment for capability improvements inadvertently relaxes grounding fidelity constraints.
- **[[themes/finetuning_and_distillation|Finetuning and Distillation]]:** The 3B and 7B models suggest effective capability distillation from the larger training setup, relevant to edge deployment research.

The most significant open questions this paper leaves: (1) why does expanded capability correlate with increased hallucination, and how can this tradeoff be broken; (2) whether multimodal CoT can be redesigned to maintain visual attention across multiple reasoning steps; and (3) whether absolute-time MRoPE generalizes to other temporal modalities beyond video (audio, sensor streams).

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
- [[entities/screenspot|ScreenSpot]]
