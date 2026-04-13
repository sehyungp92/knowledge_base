---
type: source
title: 'Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and
  Generation'
source_id: 01KJV7CCFG6EWQVMGT0J196AVQ
source_type: paper
authors:
- Chengyue Wu
- Xiaokang Chen
- Zhiyu Wu
- Yiyang Ma
- Xingchao Liu
- Zizheng Pan
- Wen Liu
- Zhenda Xie
- Xingkai Yu
- Chong Ruan
- Ping Luo
published_at: '2024-10-17 00:00:00'
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
# Janus: Decoupling Visual Encoding for Unified Multimodal Understanding and Generation

Janus proposes a simple but consequential architectural fix to unified multimodal models: instead of forcing a single visual encoder to serve both understanding and generation, it uses two independent, task-specific encoders routed through one shared autoregressive transformer. The result is a 1.3B parameter model that simultaneously outperforms 7B+ understanding specialists and all prior unified models on generative benchmarks — establishing decoupled encoding as a more principled foundation for multimodal generalism.

**Authors:** Chengyue Wu, Xiaokang Chen, Zhiyu Wu, Yiyang Ma, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, Chong Ruan, Ping Luo
**Published:** 2024-10-17
**Type:** paper

---

## The Core Problem: Representational Conflict

Prior unified multimodal models — Chameleon, [[entities/show-o|Show-o]], VILA-U — assumed a single visual encoder could serve both understanding and generation. Janus identifies this as architecturally flawed:

- **Understanding** requires high-level semantic abstractions capturing object categories, attributes, and relational structure
- **Generation** requires low-dimensional encodings that preserve fine-grained spatial structure and textural detail

These are fundamentally incompatible granularity requirements. Forcing them into one shared representational space means the encoder must compromise on both. The consequence is visible in the numbers: Chameleon (7B) scored only 0.39 on GenEval and 22.4 on MMMU; Show-o (1.3B) scored 948 on MME-Perception — well below understanding-only specialists at comparable or larger scales.

A parallel failure mode afflicted hybrid approaches like Emu and NExT-GPT, which coupled a multimodal LLM with an external diffusion model. These are not truly unified: the LLM itself cannot generate images, and generation quality is capped by the external model rather than the LLM's own capabilities.

---

## Architecture: Two Encoders, One Transformer

Janus's solution is structurally minimal: replace the single encoder with two independent pathways while keeping everything else — the autoregressive transformer backbone — unchanged.

**Understanding encoder:** SigLIP-Large-Patch16-384, extracting high-dimensional semantic features from images. These features are flattened and projected into the LLM's input space via a two-layer MLP adaptor.

**Generation encoder:** A VQ tokenizer (codebook size 16,384, 16× spatial downsampling) producing discrete image token IDs suitable for next-token prediction. A separate two-layer MLP adaptor and a randomly initialized image prediction head handle generation outputs.

Both encoders feed into the same unified transformer. No custom attention masks are required — standard autoregressive attention processes all modalities uniformly. The understanding encoder populates the LLM's existing text head; the generation encoder uses its own dedicated head.

At inference, classifier-free guidance (CFG scale=5) is applied for image generation, enabled by replacing 10% of training text conditions with a pad token during pretraining.

### Three-Stage Training

1. **Stage I — Adaptor warmup:** Encoders and LLM frozen; only MLP adaptors and image prediction head trained on paired image-text data
2. **Stage II — Unified pretraining:** LLM unfrozen; trained across text, interleaved image-text, captioning, and generation data; generation begins with ImageNet to establish pixel-level dependencies before open-domain generation
3. **Stage III — Supervised fine-tuning:** All parameters except the generation encoder fine-tuned on instruction data across all task types

Loss is standard cross-entropy applied uniformly to the autoregressive sequence — text tokens for understanding tasks, image tokens for generation tasks — without task-adaptive weighting.

---

## Results

### Multimodal Understanding

At 1.3B parameters, Janus outperforms 7B task-specific specialists:

| Model | Params | POPE | MMBench | SEED-Bench | MME |
|---|---|---|---|---|---|
| LLaVA-v1.5 | 7B | 85.9 | 64.3 | 58.6 | — |
| Qwen-VL-Chat | 7B | — | — | — | — |
| Show-o (best prior unified) | 1.3B | — | — | — | 948 |
| **Janus** | **1.3B** | **87.0** | **69.4** | **63.7** | **1338** |

The +41% MME improvement and +30% GQA improvement over Show-o are driven entirely by the decoupled encoder design — not additional parameters or data.

### Image Generation

| Model | Params | GenEval Overall | COCO FID | MJHQ FID |
|---|---|---|---|---|
| DALL-E 2 | 6.5B | 0.52 | — | — |
| SDXL | 2.6B | 0.55 | — | — |
| Show-o | 1.3B | 0.53 | 9.24 | 15.18 |
| **Janus** | **1.3B** | **0.61** | **8.53** | **10.10** |

Position accuracy (0.46 vs 0.11 for Show-o) and color attribution (0.42 vs 0.28) show particularly strong compositional instruction-following gains.

### Ablation: The Encoder Matters Most

The critical ablation directly tests the decoupling hypothesis:

- **Exp-A (single VQ tokenizer for both tasks):** POPE collapses from 87.0 → 60.1; MMBench from 69.4 → 35.0
- **Exp-B (semantically distilled unified tokenizer, similar to VILA-U):** Partial recovery (POPE 82.4, MMBench 52.7) but generation FID degrades and understanding ceiling remains below Janus

The decoupling is the critical design decision — not the choice of specific encoders.

---

## Landscape Contributions

### Capabilities

Janus demonstrates three newly validated capabilities for the [[themes/unified_multimodal_models|unified multimodal models]] landscape:

1. A 1.3B unified autoregressive model can simultaneously achieve understanding parity with 7B specialists and outperform 7B+ generation models on compositional benchmarks — **maturity: research only**
2. Decoupled-encoder architecture closes most of the understanding gap between unified and specialist models, removing the previously assumed scale penalty — **maturity: research only**
3. Independent domain-optimal encoder pathways within a unified backbone can be extended to arbitrary new modalities (point clouds, EEG, audio) without architectural surgery — **maturity: research only**

### Bottlenecks Addressed and Remaining

Janus directly resolves the [[themes/multimodal_models|multimodal models]] bottleneck of representational conflict in shared-encoder unified models. However, two significant bottlenecks remain:

**Discrete VQ tokenization ceiling.** The 16× downsampling and 16,384-entry codebook impose a hard reconstruction quality limit. Janus COCO FID of 8.53 trails PixArt-α (7.32), RAPHAEL (6.61), and Imagen (7.27). Finer-grained tokenizers (e.g., MoVQGAN) and richer loss functions (perceptual loss, GAN loss) are identified but not implemented.

**Autoregressive error accumulation.** Sequential image token generation accumulates errors; the paper identifies parallel/bidirectional attention for the generation pathway as a mitigation not yet realized.

---

## Limitations

Several limitations constrain both the paper's claims and downstream adoption:

**Resolution:** All experiments are fixed at 384×384 pixels. Variable-resolution and high-resolution generation are undemonstrated. This is a significant practical constraint given that competing diffusion models routinely operate at 512×512 to 1024×1024.

**Counting failure.** GenEval counting score of 0.30 underperforms generation-only baselines DALL-E 2 (0.49) and SDv2.1 (0.44), despite Janus outperforming both overall. The counting sub-task weakness is not analyzed or explained.

**Frozen generation encoder in SFT.** Stage III fine-tuning freezes the generation encoder entirely. This means instruction-tuning cannot adapt generation representations, potentially creating misalignment as the LLM is further fine-tuned away from the generation encoder's learned priors.

**No task-adaptive loss weighting.** Cross-entropy loss is applied identically to text and image token prediction. The paper acknowledges this as a deliberate simplification, not a validated design choice — unstable training dynamics at scale are a plausible consequence.

**Single-image evaluation only.** All vision benchmarks use single-image inputs; cross-image reasoning and multi-image interleaved understanding are entirely unevaluated.

**No temporal or 3D understanding.** Despite claiming extensibility to point clouds, EEG, and audio, no experiments outside static images and text are reported.

**Compute barrier.** Training required 7 days on 128 A100 40GB GPUs (16 nodes × 8 GPUs), creating a substantial barrier to independent replication and ablation studies.

---

## Implications

**For unified model design:** The single-encoder assumption held across Chameleon, VILA-U, and Show-o is architecturally flawed. Decoupled encoding is a more principled foundation — and the performance gap is large enough that future unified models should be expected to adopt this or equivalent designs.

**For parameter efficiency:** Achieving competitive or superior performance to 7B+ specialists at 1.3B suggests the decoupled-encoder approach offers a more parameter-efficient path to multimodal generalism, with direct implications for on-device inference and deployment at scale.

**For [[themes/image_generation_models|image generation]] research:** Achieving 0.61 GenEval with an autoregressive discrete-token model at 1.3B suggests architectural decisions around representation may matter more for compositional generation quality than raw model scale or paradigm choice (autoregressive vs. diffusion).

**For modality extension:** Independent encoder slots provide a clean interface for adding new modalities. The framework is explicitly designed so that each modality can independently adopt domain-optimal encoding without affecting the shared backbone — a structural property that unified-encoder designs lack.

---

## Related Work

- [[themes/unified_multimodal_models|Unified Multimodal Models]] — thematic context for Janus's position in the landscape
- [[themes/vision_language_models|Vision-Language Models]] — understanding benchmarks (POPE, MMBench, SEED, GQA) situate Janus relative to VLM specialists
- [[themes/generative_media|Generative Media]] — generation benchmarks (GenEval, COCO FID, MJHQ FID) situate Janus relative to diffusion and autoregressive generation specialists
- [[themes/multimodal_models|Multimodal Models]] — broader architectural patterns for multi-encoder fusion

## Key Concepts

- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/fréchet-inception-distance|Fréchet Inception Distance]]
- [[entities/geneval|GenEval]]
- [[entities/mmbench|MMBench]]
- [[entities/show-o|Show-o]]
- [[entities/siglip|SigLIP]]
- [[entities/vqav2|VQAV2]]
- [[entities/vqav2|VQAv2]]
