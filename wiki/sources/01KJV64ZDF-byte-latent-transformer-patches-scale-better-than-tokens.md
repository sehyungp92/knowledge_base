---
type: source
title: 'Byte Latent Transformer: Patches Scale Better Than Tokens'
source_id: 01KJV64ZDFQ7S86XPVP6FNANGM
source_type: paper
authors:
- Artidoro Pagnoni
- Ram Pasunuru
- Pedro Rodriguez
- John Nguyen
- Benjamin Muller
- Margaret Li
- Chunting Zhou
- Lili Yu
- Jason Weston
- Luke Zettlemoyer
- Gargi Ghosh
- Mike Lewis
- Ari Holtzman
- Srinivasan Iyer
published_at: '2024-12-13 00:00:00'
theme_ids:
- adaptive_computation
- model_architecture
- pretraining_and_scaling
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Byte Latent Transformer: Patches Scale Better Than Tokens

Pagnoni et al. (2024) introduce the Byte Latent Transformer (BLT), the first tokenizer-free architecture to match tokenization-based LLM performance in a rigorous FLOP-controlled scaling study, while simultaneously opening a new scaling axis — co-scaling model size and patch size at fixed inference cost — that is structurally unavailable to BPE-based models. The central mechanism is entropy-based dynamic patching: a small auxiliary language model identifies high-uncertainty byte positions and places patch boundaries there, concentrating expensive computation where information density is highest and skipping it where prediction is easy.

**Authors:** Artidoro Pagnoni, Ram Pasunuru, Pedro Rodriguez, John Nguyen, Benjamin Muller, Margaret Li, Chunting Zhou, Lili Yu, Jason Weston, Luke Zettlemoyer, Gargi Ghosh, Mike Lewis, Ari Holtzman, Srinivasan Iyer
**Published:** 2024-12-13
**Type:** Paper · [arxiv](https://arxiv.org/pdf/2412.09871v1)

---

## The Problem with Tokenization

Tokenization is the last major heuristic preprocessing step that sits outside end-to-end training in LLMs. Its consequences are pervasive and mostly negative:

- **Domain/modality sensitivity**: BPE compression is corpus-dependent, so out-of-domain text is systematically under-served.
- **Input noise fragility**: small perturbations (typos, formatting changes) produce radically different token sequences.
- **Orthographic blindness**: the model learns token-level patterns but has no direct access to the characters that compose them.
- **Multilingual inequity**: low-resource scripts receive far fewer bytes per token, consuming disproportionate inference budget.
- **Uniform compute allocation**: every token, regardless of informational complexity, receives identical FFN processing — compute-optimal nowhere.

The vocabulary size vs. average token size tradeoff makes these problems structurally hard to escape within BPE. Llama 3 quadrupled its embedding table compared to Llama 2 to increase average token size from 3.7 to only 4.4 bytes — nearly no gain in inference efficiency for enormous parameter cost. See [[themes/pretraining_and_scaling|Pretraining and Scaling]] for how this tradeoff propagates across the BPE scaling regime.

Prior byte-level approaches failed at scale because the FFN layers — not attention — dominate compute at scale, and they run on every byte in naive byte-level transformers. MegaByte (Yu et al., 2023) showed static fixed-stride patching could match tokenizer-based models at 1B parameters, but fell behind under rigorous FLOP-controlled comparison against compute-optimally trained Llama 3.

---

## Architecture

BLT uses three components:

**Local Encoder** (lightweight) — Alternating transformer and cross-attention layers map raw bytes into patch representations. Patch representations act as queries; byte representations act as keys/values (Perceiver-style). Critically augmented with **hash n-gram embeddings**: all byte n-grams of sizes 3–8 are mapped via polynomial hashing to embedding tables (up to 500K hashes each), providing cheap local byte context that proves essential for matching BPE performance.

**Latent Global Transformer** (large) — The expensive backbone. Operates entirely on patch representations, not individual bytes. This is where the bulk of parameters live; all expensive FFN computation is gated behind patch boundaries. Scales independently of byte sequence length.

**Local Decoder** (lightweight) — Inverts the encoder: byte representations become queries, patch representations become keys/values. Reconstructs per-byte predictions from patch-level representations.

This architecture connects directly to [[themes/model_architecture|Model Architecture]] and [[themes/transformer_alternatives|Transformer Alternatives]]: BLT is a transformer, but the patching mechanism fundamentally alters the compute topology compared to standard autoregressive transformers.

---

## Entropy-Based Patching

The patching strategy is central to everything BLT achieves. Three variants are explored:

**Strided patching** (baseline) — Fixed patch size, no information-awareness. Wastes compute on predictable bytes (e.g., whitespace in code), starves compute on information-dense bytes (e.g., mathematical notation).

**Space patching** — Boundaries placed after space-like bytes. Simple and effective; achieves larger average patch size (6.1 bytes) and significant inference savings, but cannot gracefully handle all scripts and cannot vary patch size dynamically. BLT-Space underperforms Llama 3 on 6 of 7 downstream tasks despite equivalent compute.

**Entropy patching** — A separately trained 100M-parameter byte-level language model computes next-byte entropy H(xᵢ) during preprocessing. Patch boundaries are placed at high-entropy positions (via global threshold θ_g or an approximate monotonic constraint). This satisfies **incremental patching** — boundaries for a prefix are independent of future bytes — which BPE does *not* satisfy. BPE's non-incrementality is a fundamental property: the same prefix can tokenize differently depending on the continuation.

The entropy model is a preprocessing artifact, not jointly trained with BLT. End-to-end joint learning of patching and generation remains an open direction.

---

## Results

**Compute-optimal FLOP parity:** BLT-Entropy (8B parameters, 4.5T bytes) outperforms Llama 3 (8B, 1T tokens) on 4 of 7 downstream tasks (Arc-E: 79.6 vs. 77.6, HellaSwag: 80.6 vs. 79.1, MBPP: 41.8 vs. 40.2, HumanEval: 35.4 vs. 31.1) at roughly equivalent FLOP budgets. This is the first time a byte-level model has achieved this at this scale.

**Beyond compute-optimal:** In fixed-inference-FLOP scaling experiments, BLT models surpass BPE scaling trends at approximately 2.5–3× the BPE compute-optimal training budget — a regime that is common in practice (Llama 3.1 is trained ~100× beyond compute-optimal). BLT ps=8 models are 1.6–1.7× the parameter count of the Llama 2 baseline at matched inference FLOPs, implying up to ~50% inference FLOP savings vs. a same-sized BPE model.

**Robustness:** On noised HellaSwag (5 noise types), BLT averages 64.3 vs. 56.9 for same-data Llama 3 — and ties Llama 3.1 (trained on 16× more data) despite the data disadvantage. The robustness gains are not recoverable through additional BPE training; they appear to be a structural consequence of byte-level representation.

**Character-level understanding:** BLT achieves 99.9% on spelling tasks and a 25+ point advantage over BPE models on the CUTE benchmark. These gains persist against Llama 3.1 trained on 16× more data, confirming they are not a data-quantity effect.

**Low-resource translation:** +2.0 BLEU average into English and +0.5 from English over Llama 3 on FLORES-101. Gains are especially large on low-resource scripts: Bengali into English 12.7 vs. 4.7, Georgian 7.4 vs. 1.7.

**Initialization from pretrained weights:** BLT's global transformer can be initialized from Llama 3.1 weights ("byte-ifying") with the local encoder/decoder trained from scratch at 10× lower learning rate. This significantly outperforms both Llama 3 and scratch-trained BLT baselines under matched FLOP budgets.

---

## The New Scaling Axis

The most structurally significant contribution is conceptual: BLT breaks the fixed tradeoff between vocabulary size, inference cost, and model capacity that constrains all BPE-based scaling. Because patch size can be increased arbitrarily — with saved compute reallocated to a larger Latent Transformer — model capacity and inference efficiency can be co-scaled simultaneously. This is unavailable to token-based models.

This connects to [[themes/adaptive_computation|Adaptive Computation]] and [[themes/scaling_laws|Scaling Laws]]: existing scaling laws are calibrated for BPE models and may be significantly suboptimal for byte-level architectures with their different compute topology. BLT's current experiments use BPE-derived compute-optimal ratios from Llama 3, which introduces an unknown but potentially large source of suboptimality.

---

## Limitations and Open Questions

**Infrastructure gap.** BLT achieves theoretical FLOP parity but not wall-clock parity. ML infrastructure — CUDA kernels, Flash Attention, training frameworks — is deeply optimized for static fixed-vocabulary tokenization. BLT's dynamic patch-dependent attention masks are incompatible with Flash Attention, requiring the slower Flex Attention. This is a significant integration bottleneck for production deployment, estimated to resolve on a 1–2 year horizon.

**Separate entropy model.** The 100M-parameter patching model is a preprocessing artifact, not jointly learned. End-to-end learning of patching and generation has not been demonstrated; it is an open research direction.

**Unknown BLT scaling laws.** Current experiments use BPE-derived compute-optimal ratios. BLT's optimal data/parameter/patch-size tradeoffs are unknown and potentially very different from BPE. The scaling behavior at frontier scale (70B, 400B+) is entirely unexplored.

**Training budget threshold.** BLT requires ~2.5–3× the compute-optimal training budget before surpassing BPE models. In training-compute-constrained settings, BPE remains superior. This is the regime where most academic research operates.

**Local encoder/decoder scaling imbalance.** Growing total parameters 20× (400M to 8B) only roughly doubles local model parameters. The local encoder/decoder scale significantly more slowly than the global latent transformer, suggesting an architectural imbalance that may require separate design work as scale increases.

**Scale threshold for large patches.** BLT with patch size 8 performs significantly worse than BPE at 1B scale, becoming competitive only at 7B+. The new scaling axis is inaccessible without substantial compute.

**Entropy drift on structured content.** Entropy-based patching generates pathologically large patches on structured/repetitive content (e.g., MMLU multiple-choice questions), requiring ad-hoc mitigations. The interaction between entropy-based patching and structured evaluation formats is not cleanly resolved.

**Word-level manipulation.** BLT underperforms BPE on word deletion and insertion tasks on CUTE, suggesting byte-level representations must laboriously construct word-level abstractions that BPE models receive for free. This is a minor but conceptually interesting limitation: byte-level models are not uniformly superior in character/word understanding — they excel at character manipulation but not at word-boundary-dependent operations.

**Initialization from pretrained weights.** The "byte-ifying" approach shows significant performance drops on most tasks (HellaSwag, PIQA, MBPP) before recovering; the recovery trajectory and ultimate ceiling relative to scratch-trained BLT are not fully characterized.

---

## Connections

- [[themes/adaptive_computation|Adaptive Computation]] — Entropy patching is a form of input-conditional compute allocation; patch boundaries concentrate expensive global transformer steps where prediction is most uncertain.
- [[themes/model_architecture|Model Architecture]] — The three-component architecture (local encoder / global latent transformer / local decoder) is a significant departure from standard autoregressive transformer design.
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — BLT is evaluated in the compute-optimal and beyond-compute-optimal training regimes; its advantages compound past the compute-optimal point.
- [[themes/scaling_laws|Scaling Laws]] — BLT introduces a new scaling axis (patch size co-scaled with model size) that existing scaling laws do not capture; deriving BLT-specific scaling laws is an open problem.
- [[themes/transformer_alternatives|Transformer Alternatives]] — BLT challenges the assumption that BPE tokenization is a necessary component of high-performance LLMs; it is a transformer-based alternative to the standard tokenize-then-transform pipeline.

## Key Concepts

- [[entities/flexattention|FlexAttention]]
