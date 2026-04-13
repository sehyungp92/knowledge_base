---
type: source
title: 'LMFusion: Adapting Pretrained Language Models for Multimodal Generation'
source_id: 01KJV5SBG07KYAVYZW3MP8Q5PK
source_type: paper
authors:
- Weijia Shi
- Xiaochuang Han
- Chunting Zhou
- Weixin Liang
- Xi Victoria Lin
- Luke Zettlemoyer
- Lili Yu
published_at: '2024-12-19 00:00:00'
theme_ids:
- finetuning_and_distillation
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# LMFusion: Adapting Pretrained Language Models for Multimodal Generation

LMFusion introduces a parameter-efficient architecture for retrofitting pretrained text-only LLMs into unified multimodal generative systems — handling text, image understanding, and image generation — without catastrophic forgetting and at half the compute cost of training from scratch, by introducing parallel modality-specific transformer modules while freezing the original language weights.

**Authors:** Weijia Shi, Xiaochuang Han, Chunting Zhou, Weixin Liang, Xi Victoria Lin, Luke Zettlemoyer, Lili Yu
**Published:** 2024-12-19
**Type:** paper

---

## Motivation

The dominant approach to unified multimodal generation — models like Transfusion, Chameleon, and Unified-IO — trains from scratch on interleaved text and image data. This is wasteful on two axes. First, training a competitive text-only LLM like Llama-3 already requires over 15 trillion tokens; building multimodal capability on top demands equivalent additional compute for image data and joint optimization. Second, and more fundamentally, from-scratch multimodal models never match the language quality of their text-only counterparts: Transfusion trained on 0.5T tokens (half language, half image-caption) underperforms Llama-3 by 11.6% on HellaSwag.

The obvious alternative — finetuning a pretrained LLM on multimodal data — fails due to catastrophic forgetting. With equal learning rates for text and image components, HellaSwag drops 15% immediately and never recovers, sustaining a persistent 7% gap even after extended training. Learning rate decoupling (ratio 0.1) narrows this to 2% but proportionally degrades image capability — confirming that for dense architectures, the language-vision tradeoff is structurally intractable.

---

## Approach

LMFusion resolves this by architectural separation rather than optimization tricks.

**Modality-specific parallel modules.** Rather than shared weights across modalities, LMFusion introduces independent QKV projections, output projections, FFNs, and layer normalizations for text and image respectively. Cross-modal interaction is preserved by concatenating queries, keys, and values from both streams before computing self-attention — with a hybrid mask: causal for text tokens, bidirectional for image tokens (following [[themes/unified_multimodal_models|Transfusion]]'s design).

**Initialization and freezing.** Both text-specific and image-specific modules are initialized from pretrained Llama-3 8B weights. During training, text modules are entirely frozen (learning rate = 0); only image-specific modules and U-Net components are updated. This means text-only data is unnecessary — training runs exclusively on image-caption pairs, halving total FLOPs relative to Transfusion's matched compute budget.

**Image processing.** A VAE encoder compresses 256×256 images to 32×32×8 latent tensors, further reduced by a 2-block U-Net downsampler to 256 patch tokens. Generation is supervised via DDPM loss; language tokens via standard autoregressive cross-entropy. The combined objective mirrors Transfusion: `L = L_LM + λ · L_DDPM`.

**Parameter count vs. FLOPs.** LMFusion has twice as many parameters as Transfusion — but identical FLOPs, since only half the parameters activate per token. The cost is memory, not compute.

---

## Results

In a FLOPs-matched comparison against Transfusion:

| Metric | Transfusion | LMFusion | Delta |
|---|---|---|---|
| HellaSwag | 51.0 | 60.0 | +17.6% |
| WinoGrande | 64.3 | 72.8 | +13.2% |
| MS-COCO CIDEr (image understanding) | — | +20% | — |
| MS-COCO FID (image generation) | 14.4 | 13.9 | −3.5% |

LMFusion achieves these results using only **50% of Transfusion's total FLOPs**, with the advantage consistent throughout training — not just at convergence — suggesting the Llama-3 initialization provides a sustained head start in both modalities.

**Ablation findings** confirm the joint necessity of both design choices:
- Deep separation (modality-specific FFNs + attention) outperforms shallow separation (FFNs only), which outperforms no separation — with the gap most pronounced in image generation.
- Freezing text modules in a dense (non-separated) model severely harms image capability. Freezing in the deep separation setting simultaneously preserves language performance *and* enables strong image learning. The two choices are mutually reinforcing, not independently sufficient.

**Image editing** is demonstrated qualitatively on MagicBrush after finetuning on 8K examples — object replacement and scene modification tasks — though no quantitative metrics are reported.

**LLaVAFusion** extends the same recipe to LLaVA-NeXT 8B (an existing VLM), adding image generation capability while preserving multimodal understanding, achieving competitive or leading performance across MMMU (41.7), ChartQA (69.5), RealWorldQA (60.0), MME-P (1603.7), and FID (8.2) — outperforming Chameleon, Janus, Show-O, and Transfusion on most benchmarks.

---

## Limitations & Open Questions

**Memory overhead.** The 2x parameter count is a real deployment cost. Despite FLOPs parity with Transfusion, serving LMFusion requires twice the GPU memory — a significant constraint on memory-bound hardware.

**Resolution ceiling.** All training and evaluation uses center-cropped 256×256 images. Performance at higher resolutions is entirely untested, leaving LMFusion's practical utility for real-world image generation uncharacterized.

**Training data scope.** Training uses exclusively image-caption pairs from a single commercial source (Shutterstock, 380M pairs). There are no interleaved multimodal documents in training, which substantially limits the "arbitrary interleaved sequences" claim in the headline — the model has never seen text-image interleaving during training at all.

**Frozen text modules.** Permanently freezing text weights means the LLM cannot learn from image-caption data or benefit from any multimodal signal. Language capability is preserved but capped at the original Llama-3 checkpoint — the model cannot improve on language tasks by seeing more multimodal data.

**Context length.** The 4096-token context limit, combined with each 256×256 image consuming 256 tokens after downsampling, caps practical multimodal context at ~15 images per sequence.

**Evaluation narrowness.** Image generation is evaluated only on MS-COCO at 256×256 using FID and CLIP scores — no compositional prompts, text-in-image rendering, or aesthetic benchmarks. Image editing is qualitative only, with no quantitative comparison, ablation of fidelity vs. quality, or comparison to dedicated editing models.

---

## Significance

LMFusion addresses a structural problem in [[themes/multimodal_models|multimodal model]] development: the [[themes/finetuning_and_distillation|field's massive investment in text-only pretraining]] has been treated as incompatible with multimodal capability. By demonstrating that deep modality separation + weight freezing completely eliminates catastrophic forgetting — achieving this without any text-only data in training — the paper establishes a viable pathway for retrofitting existing LLMs as [[themes/unified_multimodal_models|unified multimodal systems]].

The implication is architectural modularity: improvements to the base LLM (a future Llama-4) or improvements to the image generation stack can be made independently and composed. This decouples the capability development roadmaps for language and vision in a way that from-scratch unified models cannot support.

The paper also partially resolves the [[themes/unified_multimodal_models|catastrophic forgetting bottleneck]] in multimodal adaptation — though the resolution comes with the tradeoff that the language model cannot continue learning from multimodal context, which may become a limitation as training scales and interleaved data becomes more central to capability development.

---

## Related Work

- [[themes/unified_multimodal_models|Unified Multimodal Models]] — the broader landscape of models handling text and image generation jointly
- [[themes/image_generation_models|Image Generation Models]] — diffusion-based [[themes/generative_media|generative media]] approaches LMFusion builds on
- [[themes/post_training_methods|Post-Training Methods]] — the adaptation and [[themes/finetuning_and_distillation|finetuning]] context in which LMFusion operates

## Key Concepts

- [[entities/clip-score|CLIP Score]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/variational-autoencoder|Variational Autoencoder]]
