---
type: source
title: 'Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level
  Computation'
source_id: 01KJTN8HBDDB552EK3Q950SYDQ
source_type: paper
authors:
- Sangmin Bae
- Yujin Kim
- Reza Bayat
- Sungnyun Kim
- Jiyoun Ha
- Tal Schuster
- Adam Fisch
- Hrayr Harutyunyan
- Ziwei Ji
- Aaron Courville
- Se-Young Yun
published_at: '2025-07-14 00:00:00'
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
# Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation

Mixture-of-Recursions (MoR) introduces a unified pretraining framework that simultaneously achieves parameter efficiency through weight tying and adaptive computation through learned token-level routing, assigning each token a dynamic recursion depth — how many times a single shared parameter block is applied — while maintaining a coherent KV caching strategy. By training lightweight routers end-to-end, MoR establishes a new Pareto frontier: at equal training FLOPs and smaller model sizes, it outperforms both vanilla and recursive Transformer baselines on validation perplexity and few-shot accuracy while delivering up to 2.06× inference throughput.

**Authors:** Sangmin Bae, Yujin Kim, Reza Bayat, Sungnyun Kim, Jiyoun Ha, Tal Schuster, Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Aaron Courville, Se-Young Yun
**Published:** 2025-07-14
**Type:** paper

---

## Motivation

[[themes/model_architecture|Model Architecture]] research has pursued efficiency along two largely separate axes: **parameter sharing** (recursive/layer-tied Transformers) and **adaptive computation** (early-exiting, conditional compute). Neither axis alone was sufficient:

- Prior recursive Transformers (Universal Transformer, Relaxed Recursive Transformers) apply a fixed recursion depth to every token, ignoring that subword continuations like "-ensively" are far simpler to predict than semantically loaded first tokens — yet receive identical compute.
- Post-hoc adaptivity via early-exiting requires separate training phases that degrade performance, and creates a structural KV cache consistency problem: when a token exits early, its KV pairs at deeper layers are missing, forcing stale-entry reuse or costly parallel decoding.
- No prior architecture achieved all three simultaneously in a single pretraining framework: parameter sharing, learned adaptive computation, and a coherent KV caching strategy.

---

## Architecture

### Middle-Cycle Parameter Sharing

MoR uses a single "Middle-Cycle" shared parameter block — unique first and last layers, with shared intermediate layers cycled up to N_r times per token. Among four sharing strategies tested (Cycle, Sequence, Middle-Cycle, Middle-Sequence), Middle-Cycle consistently achieves the lowest validation loss at both 135M and 360M scales.

### Routing Strategies

Two routing approaches are explored, each with distinct trade-offs:

**Expert-choice routing** — each recursion depth selects its top-k tokens via hierarchical filtering (only tokens active at recursion r are eligible for r+1). This guarantees a static compute budget and perfect load balancing but violates causal attention during training through future-token information leakage. The best configuration uses sigmoid activation with a linear router and an auxiliary loss that approximates token selection at inference without future-token access. The auxiliary loss produces near-perfectly binary router outputs, but this creates a downstream limitation: inference-time capacity factors become difficult to adjust post-training.

**Token-choice routing** — a single upfront routing decision commits each token to a fixed full recursion path, preserving causality. However, it suffers from persistent load imbalance for nearly half of training steps, and an explicit balancing loss with a softmax-MLP router is required for stability. Despite this, token-choice underperforms expert-choice significantly: 40.0% vs. 42.6% average few-shot accuracy at N_r=3.

### KV Caching Strategies

Two purpose-designed caching strategies address the consistency problem that plagues prior adaptive-depth models:

**Recursion-wise caching** — stores only KV pairs of tokens active at each recursion depth, restricting attention to locally cached tokens. Reduces KV memory and IO to approximately (N_r+1)/(2N_r) of vanilla cost, and per-layer attention FLOPs to (k/N_ctx)², making it the preferred strategy for expert-choice routing.

**Recursive KV sharing** — caches all KV pairs exclusively at the first recursion and reuses them across all subsequent depths. Reduces KV memory to 1/N_r but only cuts attention FLOPs by k/N_ctx rather than the squared factor achievable with recursion-wise caching. Benefits token-choice routing where richer contextual information compensates for weaker routing decisions, but creates a persistent decoding bottleneck from high KV IO volume — and is incompatible with expert-choice routing due to large performance degradation.

### Continuous Depth-Wise Batching

Because all tokens at different recursion stages use the same shared parameter block, MoR groups them into a single batch, eliminating idle GPU bubbles and providing practical throughput gains beyond raw FLOPs savings.

---

## Results

### Equal-FLOPs Comparison (16.5e18 FLOPs budget)

MoR with expert-choice routing and N_r=2 achieves:
- Lower validation NLL: 2.7511 vs. 2.7824 for vanilla Transformer
- Higher few-shot accuracy: 43.1% vs. 42.3%
- ~50% fewer parameters: 167M vs. 315M
- More training tokens within the same compute: 27B vs. 20B

### Fixed Data Comparison (20B tokens)

MoR (N_r=2) outperforms both vanilla and recursive baselines while consuming **25% fewer training FLOPs**, reducing training time by 19% and peak memory by 25%.

### IsoFLOP Scaling Analysis

Across four model scales (135M, 360M, 730M, 1.7B) and three compute budgets:
- MoR consistently outperforms recursive baselines at all scales
- At ≥360M parameters, matches or exceeds vanilla Transformer — particularly under low-to-mid compute budgets
- At 135M, a persistent gap versus vanilla remains, attributed to a **recursive capacity bottleneck**

### Inference Throughput

With continuous depth-wise batching at maximum batch size:
- MoR-2: 1.60× speedup
- MoR-3: 1.95× speedup
- MoR-4: 2.06× speedup

### Compute-Optimal Scaling

MoR's optimal scaling path favors allocating resources to larger models trained for fewer steps, making it **less data-hungry than vanilla Transformers** — a distinct behavior under [[themes/scaling_laws|Scaling Laws]] that has implications for how compute budgets should be allocated.

---

## Capabilities

| Capability | Maturity |
|---|---|
| Token-level adaptive recursion depth via end-to-end learned routers | research_only |
| Up to 2.06× inference throughput via depth-wise batching + early-exit | research_only |
| Recursive Transformer matching vanilla at 360M–1.7B with ~⅓ unique parameters | research_only |
| Recursion-wise KV caching reducing memory/IO to (N_r+1)/2N_r | research_only |
| 19% training time reduction, 25% peak memory reduction vs. vanilla at equal data | research_only |
| Test-time scaling via adjustable recursion depth at inference | research_only |
| FSDP distributed training efficiency multiplied N_r-fold via weight reuse | research_only |

The test-time scaling capability is particularly notable: allocating additional recursion steps at inference improves generation quality without any additional training, enabling compute-quality trade-offs in base models — a capability with implications for [[themes/adaptive_computation|Adaptive Computation]] beyond training efficiency.

---

## Limitations and Open Questions

### Architectural Constraints

**Scale validation gap** — all experiments are limited to 1.7B parameters due to compute constraints. Whether the Pareto efficiency advantage persists at production-relevant scales (3B+) on large corpora is entirely untested, and this is explicitly identified as the primary next step.

**Routing capacity inflexibility** — expert-choice routing with auxiliary loss produces near-perfectly binary router outputs (selected tokens near 1.0, unselected near 0.0), which is mechanically impressive but means inference-time top-k capacity factors cannot be adjusted post-training. This creates a mismatch problem for deployment environments where compute budgets differ from training assumptions.

**Causality-performance trade-off** — expert-choice (higher performing) violates causal attention during training and requires auxiliary workarounds; token-choice (causality-safe) underperforms by 2.6 percentage points and fails to balance loads for nearly half of training. No routing strategy simultaneously achieves causal correctness, load balance, and peak performance.

**Recursive KV sharing incompatibility** — recursive KV sharing offers better memory footprint but is incompatible with expert-choice routing (the higher-performing variant), and its decoding bottleneck from high KV IO volume makes it impractical for the best-performing configuration.

### Distribution and Domain Gaps

**English-only evaluation** — all experiments use FineWeb-Edu, a single English corpus. Routing behavior under multilingual, domain-specific, or low-resource distributions is entirely untested.

**Post-training compatibility unknown** — no demonstration of compatibility with instruction tuning, RLHF, or reasoning dataset fine-tuning. The paper explicitly flags as crucial future work how the router adapts when chain-of-thought reasoning requires deeper computation across all tokens.

**Sparse efficiency interactions unexplored** — compatibility with pruning, quantization, and other sparse algorithms for compound efficiency gains remains unvalidated. How adaptive depth routing interacts with sparse weight activation patterns is an open question.

### Scale Threshold

MoR underperforms vanilla Transformer at 135M parameters due to a recursive capacity bottleneck, revealing a minimum viable scale threshold for the architecture. This gap closes rapidly at larger scales, but it constrains applicability in edge/mobile deployment scenarios.

---

## Open Bottlenecks

**Inference-time compute flexibility** — routing capacity factors baked in at training prevent dynamic adjustment of computation budgets for different inference environments. Resolving this would enable true deployment-time adaptive compute. *Horizon: 1–2 years.*

**KV IO bandwidth in recursive sharing** — maximizing memory reduction via recursive KV sharing forces full-sequence reads at each depth that dominate decoding time, preventing simultaneous optimization of memory footprint and throughput. *Horizon: 1–2 years.*

**Scale validation** — the Pareto efficiency claims are unestablished above 1.7B parameters; industry adoption depends on evidence at 7B+ scales that existing compute budgets have not yet supported. *Horizon: months.*

**Load balancing in causal routing** — token-choice routing fails to distribute computation evenly for nearly half of training steps. A routing strategy that is simultaneously causally correct, load-balanced, and high-performing remains an unsolved problem. *Horizon: 1–2 years.*

---

## Significance

MoR is a notable breakthrough in [[themes/pretraining_and_scaling|Pretraining and Scaling]] as the first architecture to unify parameter efficiency (weight tying) and adaptive token-level computation (variable recursion depth) in a single end-to-end pretraining framework. Prior work addressed these as separate problems; MoR combines them with a mechanically coherent KV caching design that prior adaptive-depth architectures lacked.

The architectural contribution also feeds into the [[themes/transformer_alternatives|Transformer Alternatives]] theme by demonstrating that recursive Transformers need not trade performance for parameter efficiency — the efficiency gains can be applied to process more tokens within a fixed compute budget, effectively making the architectural improvement budget-neutral from a capabilities standpoint.

The compute-optimal scaling behavior — favoring larger models over more tokens — is an underemphasized finding with implications for [[themes/scaling_laws|Scaling Laws]] research: if MoR architectures have systematically different optimal token-to-parameter ratios than vanilla Transformers, existing scaling law frameworks may not transfer directly.

---

## Related Themes

- [[themes/adaptive_computation|Adaptive Computation]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/transformer_alternatives|Transformer Alternatives]]

## Key Concepts

- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/low-rank-adaptation|Low-Rank Adaptation]]
- [[entities/z-loss|z-loss]]
