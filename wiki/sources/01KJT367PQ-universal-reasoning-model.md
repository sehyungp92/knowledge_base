---
type: source
title: Universal Reasoning Model
source_id: 01KJT367PQH5AMY5RR637P4TC2
source_type: paper
authors:
- Zitian Gao
- Lynx Chen
- Yihao Xiao
- He Xing
- Ran Tao
- Haoming Luo
- Joey Zhou
- Bryan Dai
published_at: '2025-12-16 00:00:00'
theme_ids:
- adaptive_computation
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- reasoning_and_planning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Universal Reasoning Model

This paper investigates why Universal Transformers (UTs) outperform vanilla Transformers on abstract reasoning tasks, isolating the true sources of performance gain through systematic ablation, then proposes the Universal Reasoning Model (URM) — a principled enhancement using ConvSwiGLU and Truncated Backpropagation Through Loops (TBPTL) — achieving state-of-the-art results among small models trained from scratch on ARC-AGI 1 (53.8% pass@1) and ARC-AGI 2 (16.0% pass@1).

**Authors:** Zitian Gao, Lynx Chen, Yihao Xiao, He Xing, Ran Tao, Haoming Luo, Joey Zhou, Bryan Dai
**Published:** 2025-12-16
**Type:** paper
**Source:** https://arxiv.org/pdf/2512.14693

---

## Expert Analysis

### Motivation & Prior Limitations

[[themes/transformer_alternatives|Transformer Alternatives]] research had produced a cluster of Universal Transformer variants — notably HRM (34.4% pass@1 on ARC-AGI 1) and TRM (40.0%) — that demonstrated strong results on reasoning-intensive tasks like ARC-AGI and Sudoku. However, the specific architectural mechanisms responsible for their gains were poorly understood, leading to increasingly elaborate designs without principled justification. Prior work attributed performance gains to high-level structural innovations — multi-timescale recurrence, explicit hierarchy, gating mechanisms — without rigorously validating these attributions through controlled ablation.

Meanwhile, standard (non-recurrent) Transformers exhibit a fundamental coupling between parameter count and inference compute that makes them inefficient for multi-step [[themes/reasoning_and_planning|reasoning]]: at 32× parameter count, vanilla Transformers still fail to match even a base UT at 4× parameters, and simply scaling depth or width yields diminishing returns or active degradation on abstract reasoning tasks. Gradient instability in recurrent training — analogous to vanishing/exploding gradients in RNNs — remained an unaddressed obstacle as loop counts grew.

### Proposed Approach

The paper proceeds in two stages: first, systematic ablation to isolate true performance drivers; then, targeted architectural modification informed by those findings.

**Ablation findings** reveal that ARC-AGI performance gains arise primarily from two factors: (1) the recurrent inductive bias — parameter-shared depth iteration — which converts fixed parameter budgets into increased effective depth, and (2) strong nonlinear components. Architectural elaborations layered on top contribute little independently. The evidence for nonlinearity is unusually direct: progressively removing nonlinear components causes monotonic performance collapse:

| Nonlinearity removed | ARC-AGI 1 pass@1 |
|---|---|
| Full model (SwiGLU) | 53.8% |
| SwiGLU → SiLU | 45.3% |
| SiLU → ReLU | 29.75% |
| Remove attention softmax | 2.0% |

This sharp degradation directly implicates expressive nonlinearity as the key functional bottleneck in recurrent reasoning architectures.

**ConvSwiGLU** augments the standard SwiGLU feed-forward block with a depthwise 1D short convolution (kernel size k=2) applied after the MLP expansion. This introduces lightweight local token mixing within an already-nonlinear subspace without increasing sequence-level complexity. Critically, insertion position matters:

- Convolution placed **after MLP expansion** yields the dominant benefit
- Convolution placed **inside the attention pathway** (after SDPA, value, key, or query projections) provides no gain or degrades performance

This asymmetry supports a functional interpretation: the [[themes/model_architecture|MLP — not attention — constitutes the primary locus of expressive nonlinearity]] in Universal Transformers. ConvSwiGLU works by enhancing inter-channel information flow, producing more diverse and structured attention distributions compared to the sparse, homogeneous patterns of the base UT.

**Truncated Backpropagation Through Loops (TBPTL)** addresses gradient instability by partitioning the inner-loop rollout into a forward-only prefix and a trainable suffix, computing gradients only on the loss accumulated over the latter segment. With 8 total inner loops, the optimal configuration runs the first 2 in forward-only mode and backpropagates through the last 6. More aggressive truncation (≥5 forward-only loops) degrades performance, indicating a balance between optimization stability and long-horizon coordination.

The final URM architecture is decoder-only, uses 4 layers with hidden size 512 and 8 attention heads, runs 8 inner-loop steps (first 2 forward-only) plus an outer [[themes/adaptive_computation|ACT loop]] of up to 16 steps, and is trained from scratch on ARC-AGI task data without internet-scale pretraining.

### Results

URM achieves state-of-the-art performance among single small models trained from scratch on ARC-AGI tasks:

| Benchmark | HRM | TRM | URM |
|---|---|---|---|
| ARC-AGI 1 pass@1 | 34.4% | 40.0% | **53.8%** |
| ARC-AGI 1 pass@1000 | 60.5% | 64.4% | **85.1%** |
| ARC-AGI 2 pass@1 | 5.4% | 4.6% | **16.0%** |
| ARC-AGI 2 pass@1000 | 18.6% | 13.6% | **41.3%** |
| Sudoku accuracy | 63.9% | 66.8% | **77.6%** |

Notably, URM's advantage **widens under larger sampling budgets**, indicating that iterative refinement enables richer candidate diversity rather than brittle deterministic prediction. Both ConvSwiGLU and TBPTL are individually necessary: removing short convolution drops ARC-AGI 1 pass@1 from 53.8% to 45.3%; removing truncated backpropagation drops it to 40.0%.

An additional finding: the **Muon optimizer** achieves roughly 2× faster convergence than AdamAtan2 (reaching 11.5% on ARC-AGI 2 in ~600K steps vs. >1.3M), but both converge to the same asymptotic accuracy (~53.8% / 16.0%), cleanly separating optimization efficiency from architectural capacity.

---

## Capabilities

- **URM on ARC-AGI 1/2**: 53.8% pass@1 on ARC-AGI 1 and 16.0% on ARC-AGI 2 — state-of-the-art for small models trained from scratch *(maturity: research_only)*
- **UT parameter efficiency**: A UT with only 4× parameters achieves 40.0 pass@1 on ARC-AGI 1, dramatically outperforming vanilla Transformers at 32× parameters *(maturity: research_only)*
- **ConvSwiGLU**: Depthwise short convolution after MLP expansion boosts ARC-AGI 1 reasoning by ~8.5 percentage points *(maturity: research_only)*
- **TBPTL**: Gradient truncation over early inner-loop iterations yields ~4 percentage point improvement and stabilises optimisation *(maturity: research_only)*
- **Muon optimizer**: ~2× faster convergence than Adam-based optimisers for recurrent UT training *(maturity: research_only)*

---

## Limitations & Open Questions

**Fundamental scope constraints:**
- URM is trained from scratch on task-specific datasets — results do not demonstrate general-purpose reasoning capability and cannot be interpreted as broadly applicable *(severity: significant)*
- The 53.8% ARC-AGI 1 figure excludes test-time scaling, ensembling, and visual methods, making it incommensurable with o3-style high-compute approaches (75–87%) *(severity: significant)*

**Persistent capability gaps:**
- ARC-AGI 2 remains ~84% unsolved at pass@1 — iterative recurrent refinement leaves a deep and persistent gap in abstract visual reasoning even at state-of-the-art for this model class *(severity: blocking, trajectory: improving)*
- Reasoning performance is fragile with respect to nonlinear components — removing attention softmax causes near-total collapse to 2.0% pass@1, suggesting capability is contingent on specific architectural choices in ways not yet well understood *(severity: significant)*

**Architectural and optimisation constraints:**
- TBPTL is a workaround for gradient instability, not a principled solution — the optimal truncation ratio is empirically determined under a fixed 8-loop regime without broader sensitivity analysis *(severity: significant)*
- Short convolution inside the attention pathway consistently degrades performance — local convolutional perturbations are architecturally incompatible with the global attention mechanism *(severity: minor)*
- Muon achieves faster convergence but identical final accuracy — the limiting factor on generalisation is architectural capacity, not optimisation *(severity: minor)*

**Evaluation scope:**
- URM is evaluated under a single fixed hyperparameter regime (4 layers, hidden size 512, 8 attention heads) without broader scaling or sensitivity analysis — generalisability of ConvSwiGLU and TBPTL to other scales is unvalidated *(severity: minor)*

---

## Landscape Contributions

### Bottlenecks Addressed

**[[themes/reasoning_and_planning|Abstract visual reasoning]]** — ARC-AGI 2 remains largely unsolved (16.0% pass@1 vs. ~85% human level). Requirements for abstract pattern induction and compositional generalisation are not met by recurrent refinement alone. *(horizon: 3–5 years)*

**Recurrent depth scaling** — Gradient instability limits how many refinement loops can be effectively trained. TBPTL is a partial workaround but the optimal truncation ratio is sensitive and the principled solution remains open. *(horizon: 1–2 years)*

### Breakthrough Signal

The systematic ablation constitutes a genuine [[themes/model_architecture|architectural insight]]: the field had been over-attributing UT performance to structural innovations (hierarchy, gating, multi-timescale recurrence) and underweighting the role of **recurrent inductive bias and expressive nonlinearity**. This reframes the design space — instead of elaborating architecture, the productive direction is enhancing nonlinear capacity within the recurrent block and improving gradient flow across loop iterations.

---

## Themes

- [[themes/adaptive_computation|Adaptive Computation]]
- [[themes/latent_reasoning|Latent Reasoning]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/transformer_alternatives|Transformer Alternatives]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/swiglu|SwiGLU]]
- [[entities/universal-transformer|Universal Transformer]]
- [[entities/passk|pass@k]]
