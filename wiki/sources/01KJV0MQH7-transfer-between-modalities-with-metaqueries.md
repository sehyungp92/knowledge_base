---
type: source
title: Transfer between Modalities with MetaQueries
source_id: 01KJV0MQH72KZW1YBBJRGX2510
source_type: paper
authors:
- Xichen Pan
- Satya Narayan Shukla
- Aashu Singh
- Zhuokai Zhao
- Shlok Kumar Mishra
- Jialiang Wang
- Zhiyang Xu
- Jiuhai Chen
- Kunpeng Li
- Felix Juefei-Xu
- Ji Hou
- Saining Xie
published_at: '2025-04-08 00:00:00'
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
# Transfer between Modalities with MetaQueries

MetaQueries introduces a lightweight learnable-query interface that bridges frozen autoregressive multimodal LLMs to diffusion decoders, resolving the long-standing joint optimization conflict in unified multimodal models. By keeping the MLLM backbone entirely frozen and training only a small set of randomly initialized queries alongside a connector network, the approach achieves SOTA-level image generation without degrading understanding capabilities — and, for the first time, successfully transfers in-context learning and world-knowledge reasoning from a frozen MLLM to image generation.

**Authors:** Xichen Pan, Satya Narayan Shukla, Aashu Singh, Zhuokai Zhao, Shlok Kumar Mishra, Jialiang Wang, Zhiyang Xu, Jiuhai Chen, Kunpeng Li, Felix Juefei-Xu, Ji Hou, Saining Xie
**Published:** 2025-04-08
**Type:** paper
**Source:** https://arxiv.org/pdf/2504.06256

---

## Motivation

Unified [[themes/multimodal_models|multimodal models]] that jointly handle image understanding and image generation have historically required complex, brittle training recipes. Most approaches — SEED-X, Emu, Chameleon, Show-o, EMU3, Janus, Transfusion — require fine-tuning the MLLM backbone to jointly model p(text, pixels), introducing multi-task balancing problems, multiple training stages, and architectural fragility where optimizing one task degrades the other.

An alternative, using frozen LLMs purely as conditional text encoders (Lumina-Next, Sana, Kosmos-G), sidesteps this but suppresses autoregressive reasoning: the last-layer embedding approach treats a decoder-only LLM as a text encoder, blocking in-context learning at generation time. This is confirmed empirically — last-layer embedding scores 0.48 on WiScore and 52.83 on CommonsenseT2I, versus 0.55 and 57.67 for MetaQuery. LMFusion partially addresses the joint-training problem but cannot plug into arbitrary pre-trained diffusion models and requires retraining separate generative modules per backbone.

---

## Approach

**MetaQueries** are N randomly initialized learnable queries Q ∈ R^(N×D) fed directly into a frozen MLLM to extract multimodal conditions C for a downstream diffusion model. Unlike prior frozen-LLM approaches that extract conditions from final token embeddings, MetaQueries query the MLLM's full latent space across layers, preserving its autoregressive and in-context learning dynamics even under causal masking.

A trainable connector — a 24-layer transformer encoder with bidirectional attention using an Enc-Proj architecture — maps extracted conditions into the input space of any conditional diffusion model, replacing its original text conditioning with no other architectural changes.

Training requires only paired image-caption data and the standard denoising objective: no additional losses, no reconstruction losses, no multi-stage curricula. The MLLM backbone (tested with LLaVA-OneVision-0.5B, Qwen2.5-VL 3B, and 7B) remains fully frozen throughout both pre-training (25M image-caption pairs, 8 epochs) and instruction tuning.

**Instruction tuning** avoids the scalability ceiling of expert-model-generated synthetic data. Instead, naturally occurring image pairs are mined from web corpora (mmc4), clustered by SigLIP caption similarity, and labeled with transformation instructions by Qwen2.5-VL 3B — yielding 2.4M pairs spanning a broader range of visual relationships than curated datasets. The instruction-tuned model runs for only 3 epochs with batch size 2048.

---

## Results

### Text-to-Image Generation

MetaQuery-XL achieves MJHQ-30K FID of 6.02, GenEval of 0.80, and DPG-Bench of 82.05. This matches or exceeds Janus-Pro-7B on prompt alignment (GenEval 0.80) while substantially outperforming it on visual quality (Janus-Pro MJHQ FID: 13.48 under the same conditions). The frozen MLLM + trained DiT configuration achieves FID 6.06, versus 6.28 for full end-to-end tuning.

### World Knowledge and Reasoning

MetaQuery is the first unified model to exceed standalone text-to-image models on world knowledge reasoning:

- **WISE benchmark:** MetaQuery-L scores 0.55 vs. best prior unified model Emu3 at 0.39, matching FLUX.1-dev (0.50)
- **CommonsenseT2I:** MetaQuery-L scores 57.67 (with negative prompts), surpassing SD-3-medium (47.17), FLUX.1-dev (22.50), Sana-1.6B (43.33), and all other unified models

These capabilities require the LLM to reason through multi-step questions (e.g., "the national flag of the country where Yellowstone National Park is located") before generating — a task structurally impossible for last-layer embedding approaches.

### Subject-Driven Generation

MetaQuery-B-Instruct achieves SOTA zero-shot subject-driven generation on DreamBench: DINO 0.737, CLIP-I 0.852, CLIP-T 0.301 — outperforming Kosmos-G (DINO 0.694) without requiring that model's explicitly constructed substitution-task datasets.

### Emergent Capabilities

Instruction tuning on naturally occurring pairs unlocks capabilities not explicitly supervised: generating novel views of identified specific object models (Porsche 911), inferring skyline perspectives from building images, and logo design from visual concepts.

---

## Capabilities

| Capability | Maturity |
|---|---|
| Unified multimodal model: SOTA understanding + SOTA-level generation via frozen MLLM + MetaQuery bridge | research_only |
| Knowledge-augmented image generation via frozen MLLM world knowledge and multi-step reasoning | research_only |
| In-context learning transferred from frozen MLLM to image generation | research_only |
| Zero-shot subject-driven generation (DreamBench DINO 0.737) | research_only |
| Scalable instruction-tuning data curation from web-mined image pairs | research_only |
| Image editing via 1,000-step lightweight fine-tuning of pre-trained MetaQuery | research_only |
| Emergent visual association and logo design from natural-pair instruction tuning | research_only |

---

## Limitations and Open Questions

**Architectural constraints:**

- **Causal masking on MetaQuery tokens** — learnable queries use causal rather than bidirectional attention, restricting information extraction from the frozen MLLM since queries cannot attend to future context. This is acknowledged as a simplification, not a design choice.
- **Prompt alignment vs. visual quality trade-off in token budget** — visual quality saturates around N=64 MetaQuery tokens while prompt alignment continues improving up to N=1024. No single token budget optimizes both dimensions simultaneously.
- **Frozen vs. tuned MLLM gap** — frozen MLLM achieves slightly lower prompt alignment than full MLLM tuning (visible in Table 2 GenEval scores). Preserving understanding capability comes at a measurable generation alignment cost.

**Generalization constraints:**

- **Diffusion vs. autoregressive generation paradigm trade-off** — diffusion models systematically fail at complex prompt following while autoregressive token-prediction models suffer visual artifacts. No single paradigm simultaneously dominates both dimensions; this structural tension remains unresolved. See [[themes/image_generation_models|Image Generation Models]] bottleneck.
- **Instruction tuning evaluated only at Base scale** — no evidence the 2.4M natural-pair pipeline scales comparably to the Larger (3B) or X-Large (7B) variants.
- **Non-image modalities undemonstrated** — extension to audio, video, and 3D is claimed as possible but entirely speculative.
- **Generation quality orthogonal to MLLM instruction tuning** — switching from pre-trained to instruction-tuned LLM backbone yields minimal generation improvement, suggesting MLLM alignment signal does not directly propagate to the generative side.

**Scale ceiling:**

- **Data scale ceiling blocks proprietary parity** — 25M image-caption pairs is insufficient to close the gap to GPT-4o-level systems. The paper offers no architectural solution, only data scaling as hypothesis. This is likely a 1–2 year horizon bottleneck for the [[themes/unified_multimodal_models|unified multimodal models]] space.

---

## Bottlenecks Addressed and Created

**Resolved:** The joint understanding-generation optimization conflict — MetaQueries demonstrates that a frozen MLLM interface can achieve SOTA understanding and SOTA-level generation without multi-task balancing, multiple training stages, or architectural complexity.

**Partially resolved:** The in-context learning transfer problem — frozen MLLM reasoning is now accessible to diffusion decoders for the first time, enabling world-knowledge-augmented generation.

**Persistent:** The diffusion vs. autoregressive generation paradigm trade-off remains open. MetaQuery's diffusion backbone produces higher visual quality but lower prompt alignment than Janus-Pro's autoregressive token prediction on certain benchmarks. Benchmark metrics conflate the two failure modes, making head-to-head comparison architecture-confounded.

**Newly surfaced:** The data scale ceiling — 25M pairs is the current pre-training limit, and proprietary-system parity requires unknown scale-up. The instruction-tuning pipeline's scalability to larger model variants is also unvalidated.

---

## Connections

- **[[themes/unified_multimodal_models|Unified Multimodal Models]]** — directly contributes to the central challenge of this theme: avoiding capability degradation during joint training
- **[[themes/image_generation_models|Image Generation Models]]** — engages the diffusion vs. autoregressive paradigm debate and the prompt-following limitation of diffusion models
- **[[themes/vision_language_models|Vision Language Models]]** — the frozen MLLM backbone (LLaVA-OneVision, Qwen2.5-VL) is the understanding component; MetaQuery depends on its quality without modifying it
- **[[themes/generative_media|Generative Media]]** — subject-driven generation, image editing, and visual association capabilities extend into creative media applications
- **[[themes/multimodal_models|Multimodal Models]]** — the modality bridge architecture is claimed to generalize beyond images to audio, video, and 3D (undemonstrated)

---

## Key Claims

1. MetaQueries act as an efficient interface between frozen autoregressive MLLMs and diffusion decoders, querying the MLLM's full latent space rather than extracting final-layer embeddings.
2. Training requires only paired image-caption data and standard diffusion objectives — no additional losses, multi-stage curricula, or multi-task balancing.
3. Frozen MLLM backbone achieves generation quality comparable to full MLLM fine-tuning, with slight prompt alignment cost but improved visual quality.
4. Last-layer LLM embedding approaches structurally cannot activate in-context learning for image generation, blocking knowledge-augmented generation.
5. MetaQuery is the first unified model to transfer world-knowledge reasoning from frozen MLLMs to image generation, exceeding standalone diffusion models on WISE and CommonsenseT2I.
6. Instruction-tuning data sourced from naturally occurring web image pairs outperforms or matches expert-model-generated synthetic pipelines while covering a broader range of visual relationships.
7. N=64 learnable tokens suffice for visual quality; N=1024 is needed for maximal prompt alignment and image reconstruction fidelity.
8. Generation quality is largely orthogonal to MLLM instruction-tuning quality — the generative bridge does not inherit alignment improvements from the backbone.

## Key Concepts

- [[entities/geneval|GenEval]]
- [[entities/llava-onevision|LLaVA-OneVision]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
- [[entities/siglip|SigLIP]]
