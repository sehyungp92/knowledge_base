---
type: source
title: Autoregressive Image Generation without Vector Quantization
source_id: 01KJV6ZWE5FB28K6MXQ6G4S161
source_type: paper
authors:
- Tianhong Li
- Yonglong Tian
- He Li
- Mingyang Deng
- Kaiming He
published_at: '2024-06-17 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- model_architecture
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Autoregressive Image Generation without Vector Quantization

This paper challenges the foundational assumption that autoregressive image generation requires discrete, vector-quantized tokens. By introducing **Diffusion Loss** — a per-token continuous distribution modeled by a small denoising MLP — and unifying standard AR, random-order AR, and masked generative models under a single **Masked Autoregressive (MAR)** framework, the authors demonstrate that continuous-valued tokens paired with bidirectional attention can surpass the quality and speed of all prior VQ-based autoregressive systems, achieving FID 1.55 on ImageNet 256×256 at under 0.3 seconds per image.

**Authors:** Tianhong Li, Yonglong Tian, He Li, Mingyang Deng, Kaiming He
**Published:** 2024-06-17
**Type:** paper
**Themes:** [[themes/generative_media|Generative Media]], [[themes/image_generation_models|Image Generation Models]], [[themes/model_architecture|Model Architecture]], [[themes/representation_learning|Representation Learning]]

---

## Motivation

Autoregressive image generation has been practically synonymous with vector quantization since its inception. VQ tokenizers discretize image patches into codebook indices, enabling next-token prediction with categorical cross-entropy — a well-understood objective. But VQ is an engineering convention, not a conceptual requirement. Its costs are real: VQ tokenizers are hard to train, sensitive to gradient approximation strategies, and impose a reconstruction quality ceiling that propagates irreversibly into generation quality. The gap is quantifiable — VQ-16 achieves a reconstruction FID of 5.87 versus 1.43 for the KL-regularized continuous counterpart (KL-16) on ImageNet.

The prevailing belief that discrete representations are *required* for next-token prediction had foreclosed the field from applying autoregressive models directly in continuous-valued domains. A secondary motivation: masked generative models (MaskGIT, MAGE) and standard AR models were treated as entirely separate paradigms despite sharing structural similarities. No unified framework existed.

---

## Core Contributions

### Diffusion Loss

The central innovation is a parameterized loss function that replaces categorical cross-entropy. For each token position, the autoregressive backbone (Transformer) produces a conditioning vector **z**. A small MLP denoising network, conditioned on **z**, is trained jointly via the standard DDPM denoising objective:

> *"the loss function of an underlying probability distribution p(x|z) can be formulated as a denoising criterion"*

This models p(x|z) as an arbitrary continuous distribution without requiring discretization. At inference, the denoising MLP runs a reverse-diffusion sampler conditioned on z, with 100 steps yielding near-peak quality. Gradients flow continuously through z back into the Transformer backbone, enabling end-to-end joint training.

Conceptually, Diffusion Loss behaves as a form of score matching related to the score function of p(x|z) — analogous in spirit to adversarial or perceptual losses, but integrated into the likelihood framework.

**Temperature control** is supported by scaling the noise term σ_t δ in the reverse sampler by τ, providing a continuous analogue to categorical temperature that controls sample diversity. Unlike discrete models, stochasticity cannot be fully eliminated — generation is non-deterministic by design.

### Masked Autoregressive (MAR) Framework

The paper unifies three previously distinct paradigms under a single principle: *next set-of-tokens prediction*.

| Model type | Order | Attention | Tokens per step |
|---|---|---|---|
| Standard AR | Raster | Causal | 1 |
| Random-order AR | Random | Causal | 1 |
| MAR (MaskGIT-style) | Random | Bidirectional | Many |

Bidirectional attention (MAE-style encoder-decoder) replaces causal attention in MAR, allowing all known tokens to attend to each other and unknown tokens to attend to all known tokens. This directly challenges conventional wisdom:

> *"In contrast to conventional wisdom, the broad concept of 'autoregression' (next token prediction) can be performed with bidirectional attention"*

At inference, MAR uses a cosine masking schedule over 64 steps (default), progressively unmasking tokens. Multiple tokens are predicted simultaneously per step, compensating for the loss of KV-cache — the key inference optimization that bidirectional attention forfeits.

---

## Results

On ImageNet 256×256 class-conditional generation:

| Model | Params | FID (w/ CFG) | Speed |
|---|---|---|---|
| MAR-L (default) | 479M | 1.78 | < 0.3s/image |
| MAR-H (best) | 943M | **1.55** | — |
| DiT-XL/2 (baseline) | 675M | 2.27 | slower |
| MAGVIT-v2 | — | 1.78 | — |

Diffusion Loss consistently outperforms cross-entropy loss across all AR and MAR variants. The relative FID reduction is most dramatic in the MAR setting: from 3.69 to 1.98 with CFG — roughly 50–60% relative improvement.

The ablation reveals that both attention pattern and token ordering are independently important:

- Raster → Random order: FID 19.23 → 13.07 (w/o CFG)
- Causal → Bidirectional attention: FID 13.07 → 3.43 (w/o CFG)

The denoising MLP is computationally lightweight: ~5% additional parameters (21M at 1024 width for MAR-L) and ~10% inference overhead relative to the main Transformer.

---

## Limitations and Open Questions

**Resolution ceiling.** All evaluations are at 256×256. Scalability to 512×512 or 1024×1024 — standard for production image generation — is entirely undemonstrated. Whether the MAR framework scales to higher resolutions without architectural modification is unknown.

**Text conditioning absent.** Only class-conditional generation is validated. Text-to-image generation — the dominant production paradigm — is not addressed. The most commercially relevant use case remains unvalidated.

**No KV cache.** Bidirectional attention forfeits KV cache, the critical inference optimization for causal AR models. MAR compensates by generating multiple tokens per step, but the trade-off is approximate and task-dependent. This is a structural constraint of the architecture.

**Per-token diffusion latency floor.** Even with a small MLP, 100 diffusion steps per token prediction creates an irreducible inference overhead for continuous-token AR models. This constrains deployment in interactive or real-time generation settings. The trajectory is improving (distillation, fewer steps) but not yet resolved.

**Compute inaccessibility.** Training MAR-H for 800 epochs required Google TRC TPU access. Reproducing SOTA results is out of reach for most academic groups, and the practical compute requirements for the method at scale are not reported.

**Raster ordering as a diagnostic.** The 12× FID gap between raster-scan (FID 19.23) and random-order MAR (FID 1.55) reveals that raster ordering is a severe structural constraint for image autoregression. This suggests that prior VQ-based AR models evaluating in raster order (e.g., VQGAN + GPT-style models) have been operating under a significant self-imposed handicap.

**Evaluation metric limitations.** All results are reported via FID and IS, which measure distribution-level statistics and cannot detect systematic failure modes such as object hallucination, compositional errors, or mode-specific collapse.

**Engineering workarounds.** The MAR encoder requires padding 64 [cls] tokens when the masking ratio is high (resulting in very short input sequences), an ad-hoc fix for training instability rather than a principled solution.

---

## Implications

**Decoupling AR from discrete tokenization.** The most significant implication is architectural: autoregressive sequence models are no longer constrained to operate over discrete codebooks. This opens paths for applying AR models directly to continuous-valued domains — video, audio, robotics trajectories, scientific time-series — without incurring the reconstruction penalty of quantization.

**Attention pattern as an independent design axis.** The demonstration that bidirectional attention can perform autoregression separates attention pattern from generation order as orthogonal design choices. Future work can explore attention patterns beyond causal and bidirectional (e.g., sparse, local, hierarchical) independently of whether generation is sequential or masked.

**Unification of masked and autoregressive paradigms.** Showing that MaskGIT and MAGE are instances of random-order next-set-of-tokens prediction within a common MAR framework simplifies the landscape of generative sequence models. Research insights from masked and AR communities now transfer bidirectionally within a unified theoretical frame.

**Modular design principle.** The complementary decomposition — autoregression for inter-token dependence, diffusion for intra-token distribution — demonstrates a general modular principle: different modeling components can address different statistical structures. This suggests a design pattern applicable to other hybrid generative architectures where joint dependencies and marginal distributions have different structural characteristics.

**Bottleneck resolution for VQ-based AR.** This work partially resolves the long-standing bottleneck where VQ tokenizer reconstruction quality capped AR image generation fidelity. By eliminating VQ from the generation pipeline entirely, the information-loss ceiling is removed — generation quality is now bounded by the continuous tokenizer's reconstruction quality (rFID 1.43 for KL-16) rather than the VQ reconstruction quality (rFID 5.87 for VQ-16).

---

## Connections

- **MaskGIT / MAGE** — formalized as special cases of MAR; the framework directly subsumes their masked prediction mechanism
- **DiT (Diffusion Transformer)** — the primary quality baseline; MAR-L outperforms DiT-XL/2 with fewer parameters and higher speed
- **GIVT** — prior continuous-token AR model using Gaussian mixture models; Diffusion Loss is a strictly more expressive alternative without a fixed number of mixture components
- **DDPM / score matching** — the theoretical foundation for Diffusion Loss; per-token diffusion is the operational mechanism
- [[themes/representation_learning|Representation Learning]] — VQ vs. continuous tokenizer quality is the upstream bottleneck this work partially circumvents

## Key Concepts

- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/diffusion-policy|Diffusion Policy]]
- [[entities/diffusion-transformer|Diffusion Transformer]]
- [[entities/fréchet-inception-distance|Fréchet Inception Distance]]
- [[entities/imagenet|ImageNet]]
- [[entities/masked-autoencoder|Masked Autoencoder]]
