---
type: source
title: 'The Zamba2 Suite: Technical Report'
source_id: 01KJV6RRM0P2ZKE7JH4GXYJTWQ
source_type: paper
authors:
- Paolo Glorioso
- Quentin Anthony
- Yury Tokpanov
- Anna Golubeva
- Vasudev Shyam
- James Whittington
- Jonathan Pilault
- Beren Millidge
published_at: '2024-11-22 00:00:00'
theme_ids:
- ai_market_dynamics
- model_architecture
- model_commoditization_and_open_source
- pretraining_and_scaling
- pretraining_data
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Zamba2 Suite: Technical Report

Zamba2 is a family of hybrid Mamba2-transformer language models (1.2B, 2.7B, 7.4B parameters) that simultaneously achieves state-of-the-art quality among open-weight models at each parameter class and delivers substantially better inference efficiency than pure transformers — establishing that the Pareto frontier of quality vs. efficiency for small models no longer belongs to transformers alone. The report covers architecture design, the Zyda-2 pretraining dataset, training methodology, quantization, context extension, and instruction tuning.

**Authors:** Paolo Glorioso, Quentin Anthony, Yury Tokpanov, Anna Golubeva, Vasudev Shyam, James Whittington, Jonathan Pilault, Beren Millidge
**Published:** 2024-11-22
**Type:** paper

---

## Context & Motivation

The dominant transformer architecture faces a structural tension at inference time: attention's KV cache grows linearly with context length, creating hard memory limits for long-context serving on constrained hardware. Pure [[themes/transformer_alternatives|SSM models]] (Mamba, RWKV, GLA) offer O(1) memory and linear compute during autoregressive generation, but they underperform transformers on in-context learning and long-context retrieval — a gap documented by Grazzi et al. (2024) and Park et al. (2024).

No prior hybrid architecture had resolved this tradeoff cleanly. At the time of publication, every leading open-weight model (Llama 3.2, Mistral 7B, Gemma2) was a pure transformer, leaving the hybrid Pareto frontier unexplored at the 1–8B scale.

A parallel trend provides useful background: levels of performance once associated with 100B+ parameter models are now achievable below 10B parameters, driven primarily by dramatic improvements in pretraining data quality and scale. Leading 7B models now outperform the original GPT-3 on many classic evaluations — making the 1–8B range the most competitively contested frontier in open-weight modeling.

---

## Architecture

### Hybrid Backbone

Zamba2 uses a Mamba2 backbone with a small number of **shared attention blocks** interleaved at a roughly 6:1 Mamba2-to-attention ratio. This ratio directly determines the KV cache footprint: because only the shared attention invocations require KV cache, a 6:1 ratio yields a 6× reduction in KV cache memory vs. a comparable pure transformer.

Compared to the predecessor Zamba1 (single shared attention block), Zamba2 uses **two alternating shared attention blocks**, which improves quality over parameter-matched baselines while using fewer inference FLOPs. The benefit of two shared blocks diminishes at smaller scales, likely because there are fewer total attention layers to share across.

The switch from Mamba1 to Mamba2 is significant on its own: Mamba2 blocks deliver approximately 4× higher throughput than standard transformer blocks at comparable perplexity, freeing a FLOP budget that is reinvested into a larger SSM state size.

### LoRA Expressivity Injection

A key failure mode of sharing attention blocks is that the block is forced to apply identical computations at every layer position. Zamba2 addresses this by applying **non-shared Low-Rank Adapters (LoRAs)** to each invocation of the shared transformer blocks, giving each position distinct expressivity without the full parameter cost of separate attention layers.

### Positional Embeddings

**Rotary Position Embeddings (RoPE)** are added to the shared attention blocks. This was discovered to improve performance empirically — but the discovery came after training had already begun for the 2.7B model, meaning Zamba2-2.7B lacks RoPE while the 7.4B model includes it. This architectural inconsistency across the suite is a direct consequence of running architecture search in parallel with production training.

---

## Pretraining

### Zyda-2 Dataset

The Zyda-2 dataset comprises 5 trillion tokens assembled from cross-deduplicated and model-quality-filtered versions of:

- **FineWeb-Edu** and **DCLM** — filtered for educational quality, providing strong boosts to factual knowledge recall and reasoning
- **Zyda-1** — with additional model-based quality filtering applied
- **Dolma-common-crawl** — similarly quality-filtered

Cross-deduplication across sources and model-based filtering distinguish Zyda-2 from prior datasets. Zyda-2 outperformed previous state-of-the-art datasets in annealing ablation tests and is publicly released — meaning Zamba2's outlier performance on the quality-per-training-token curve cannot be attributed to a secret dataset.

### Training Runs

- **Zamba2-1.2B and 2.7B:** 3 trillion tokens
- **Zamba2-7.4B:** 2 trillion tokens (compute and time constraints)

The 7.4B shortfall is a meaningful limitation: the smaller models received 50% more training tokens, likely leaving performance on the table for the largest model.

### Annealing

Following standard pretraining, a learning rate re-warm and rapid decay phase runs over ~100B tokens of high-quality factual, math, code, and instruction-following data. A **60% replay fraction** from phase-1 data is maintained throughout annealing to mitigate catastrophic forgetting.

---

## Results

### Benchmark Quality

Zamba2 achieves state-of-the-art across standard [[themes/pretraining_and_scaling|language modeling benchmarks]] at every scale vs. comparable open-weight models:

| Model | MMLU 5-shot | Comparators |
|---|---|---|
| Zamba2-1.2B | 43.1 | Gemma2-2B: 32.8, Llama3.2-1.2B: 36.83, SmolLM-1.7B: 27.65 |
| Zamba2-7B | 67.2 | Llama3.2-8B: 65.18, Mistral-7B: 62.2, Gemma-7B: 62.9 |

On a performance-per-training-token plot, Zamba2 models appear as clear outliers above the sigmoidal curve traced by leading transformer models — comparable only to Gemma2 (which uses knowledge distillation).

### Inference Efficiency

- **30–50% reduction** in time-to-first-token vs. comparable pure transformers
- **6× reduction** in KV cache memory requirements
- Mamba2 blocks contribute ~4× throughput advantage over standard attention blocks

These efficiency gains compound: on memory-constrained hardware (mobile, edge), the 6× KV cache reduction directly enables context lengths that would be physically impossible with a pure transformer of equivalent size.

### Instruction Tuning

Instruction-tuned variants are competitive with official instruct fine-tunes using only open-source data and methods. Zamba2-7B-Instruct achieves MT-Bench 7.42 vs. Mistral-7B-Instruct-v0.3 at 7.37. However, IFEval scores reveal a meaningful gap on structured instruction-following: Zamba2-2.7B-Instruct scores 48.0 vs. Llama3.2-3B-Instruct at 75.3.

---

## Quantization

4-bit quantization of Zamba2-2.7B-Instruct reduces memory from 5.38 GB to 1.55 GB (1.7 GB with quantized LoRAs) — a 71% reduction. Standard transformer quantization approaches generalize well to hybrid models with one important asymmetric constraint: **SSM-specific matrices (A matrix, dt projection, convolutional state) are numerically sensitive and must be kept in higher precision**. This creates a small but permanent quantization overhead relative to pure transformer models.

---

## Context Length Extension

Two distinct approaches are demonstrated, each with different tradeoffs:

**NTK-aware RoPE scaling (7B model):** Scaling factor s=16 extends effective context from 4096 to ~17,000 tokens with no additional training. Applicable only to the 7B model, which has RoPE.

**Stepwise curriculum finetuning (2.7B model):** Doubling context length every 100 steps from 4096 to 65,536 tokens extends the model to 65k with accurate passkey retrieval across the full range. The **primary blocker for further extension is RAM cost** at extreme sequence lengths — not model capacity or gradient instability. This places 100k+ context extension out of reach via gradient-based finetuning without significant infrastructure changes.

An important observation: LM loss generalizes beyond the training window, but passkey retrieval fails shortly outside the training window without explicit intervention. Loss generalization is not a reliable proxy for practical long-context capability.

---

## Limitations & Open Questions

**In-context learning gap in pure SSMs.** Hybridization with full attention is necessary to match transformer ICL capability. The architectural mechanism behind this gap remains incompletely understood — it is unclear whether the SSM recurrent state is fundamentally insufficient for ICL or whether scale and training are the real variables.

**Instruction-following deficit.** The IFEval gap (48.0 vs. 75.3 at the 3B scale) suggests that hybrid models may have a structural disadvantage on tasks requiring precise adherence to complex, structured instructions — possibly related to how attention-sparse architectures handle constraint tracking. This is marked as trajectory-unclear.

**Context extension ceiling.** The 65k token ceiling is set by training RAM, not by model design. Approaches like gradient checkpointing, activation offloading, or ring attention could potentially push this further, but none have been demonstrated for hybrid SSM-transformer models at this scale.

**Unresolved asymptotic quality relationship.** The field lacks rigorous, controlled head-to-head comparisons of pure SSMs vs. hybrid models vs. pure transformers at scale. Whether the quality gap between pure transformers and well-designed hybrids converges to zero at sufficient scale, or remains positive, is an open question with significant implications for [[themes/model_architecture|architecture]] investment decisions.

**Sublinear returns on pretraining tokens.** Performance improvement from additional pretraining tokens is strongly sublinear in the Chinchilla-overtrained regime. The authors argue this shifts the value of architectural innovation relative to data scaling: a better architecture provides a multiplicative constant on performance that becomes relatively more important as data scaling yields diminishing returns. This has implications for how the [[themes/ai_market_dynamics|AI market]] should allocate R&D resources.

**Heterogeneous model suite.** Running architecture search in parallel with production training forced the release of a suite with inconsistent features across scales — a structural consequence of the 20–60 day training runs required per model on 16 nodes of 8×H100 SXM. This replication barrier limits the pace of [[themes/pretraining_and_scaling|pretraining]] experimentation.

---

## Landscape Contributions

### Breakthroughs

**Hybrid efficiency-quality Pareto frontier established at small scale.** Zamba2 is the first open-weight model family to simultaneously match or exceed SOTA pure transformer quality and deliver large inference efficiency gains (30–50% TTFT, 6× KV cache) at 1.2B–7.4B parameters. This undermines the prior assumption that transformer architectures define the quality ceiling for small models.

### Bottlenecks Highlighted

- **RAM cost at 65k+ sequence lengths** blocks gradient-based context extension for hybrid SSM-transformer models — blocking efficient 100k+ context windows (horizon: 1–2 years)
- **Coupled architecture search and production training** blocks delivering uniformly optimal hybrid models across scales without multi-month delays (horizon: months)

---

## Themes

- [[themes/transformer_alternatives|Transformer Alternatives]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/pretraining_data|Pretraining Data]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]

## Key Concepts

- [[entities/chinchilla-scaling-laws|Chinchilla Scaling Laws]]
- [[entities/dclm|DCLM]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/ifeval|IFEval]]
- [[entities/kv-cache|KV Cache]]
- [[entities/mmlu|MMLU]]
- [[entities/mt-bench|MT-Bench]]
- [[entities/qlora|QLoRA]]
- [[entities/rotary-position-embedding|Rotary Position Embedding]]
- [[entities/state-space-model|State Space Model]]
- [[entities/tensor-parallelism|Tensor Parallelism]]
