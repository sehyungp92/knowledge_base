---
type: source
title: Hierarchical Reasoning Model
source_id: 01KJTMPYR9ZD888R6EKRFPSX4J
source_type: paper
authors:
- Guan Wang
- Jin Li
- Yuhao Sun
- Xing Chen
- Changling Liu
- Yue Wu
- Meng Lu
- Sen Song
- Yasin Abbasi Yadkori
published_at: '2025-06-26 00:00:00'
theme_ids:
- adaptive_computation
- chain_of_thought
- latent_reasoning
- model_architecture
- reasoning_and_planning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Hierarchical Reasoning Model

> This paper introduces HRM, a recurrent architecture with coupled high-level and low-level modules that achieves state-of-the-art performance on ARC-AGI and solves tasks completely intractable for frontier CoT models — using only 27M parameters and ~1000 training examples — by performing sequential reasoning in continuous latent space without any pre-training or chain-of-thought supervision.

**Authors:** Guan Wang, Jin Li, Yuhao Sun, Xing Chen, Changling Liu, Yue Wu, Meng Lu, Sen Song, Yasin Abbasi Yadkori
**Published:** 2025-06-26
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

Standard Transformer-based LLMs are architecturally shallow despite their scale, placing them in computational complexity classes (AC0 or TC0) that prevent solving problems requiring polynomial time — making them non-Turing-complete for complex algorithmic reasoning. A Transformer scaled to 872M parameters still fails to reach peak accuracy on Sudoku-Extreme-Full, while HRM at 27M achieves near-perfect accuracy. Increasing model width yields no improvement on tasks like Sudoku-Extreme that require tree-search and backtracking; only depth helps, yet naive depth stacking hits vanishing gradients and saturates well below optimal performance.

[[themes/chain_of_thought|Chain-of-Thought]] prompting compensates for shallow computation by externalizing reasoning into token sequences, but creates its own failure modes: brittle human-defined decompositions, high token counts, slow inference, and large data requirements. State-of-the-art CoT models including o3-mini-high and DeepSeek R1 achieve 0% accuracy on Sudoku-Extreme and Maze-Hard benchmarks that HRM solves with 1000 training examples. CoT tethers reasoning to token-level linguistic patterns rather than operating in a continuous latent space, which is both biologically implausible and computationally wasteful since all tokens receive equal computation regardless of reasoning difficulty.

Standard recurrent architectures (RNNs) present a natural alternative but suffer from premature convergence — hidden states settle to fixed points early, stalling computation — and require Backpropagation Through Time (BPTT), which demands O(T) memory and is biologically implausible.

---

### Proposed Architecture

HRM is a recurrent sequence-to-sequence architecture with two coupled modules:

- **High-level (H) module** — slow, abstract planning; updates once per cycle
- **Low-level (L) module** — fast, detailed computation; updates T times per cycle conditioned on H's fixed state, then resets

This mirrors the brain's hierarchical cortical processing across timescales — slow theta waves (4–8 Hz) guiding fast gamma-frequency (30–100 Hz) local computations — though the modules are conceptual abstractions rather than direct neural frequency maps.

The key innovation is **hierarchical convergence**: rather than preventing premature convergence (as prior work attempted), HRM exploits it. Each cycle, L stabilizes to a local equilibrium, H reads L's final state and updates, then L resets and begins converging toward a new local equilibrium determined by the updated H context. This sustains high computational activity over NT total steps without instability.

**Training innovations** allow this without the usual costs of deep recurrence:

- A **one-step gradient approximation** avoids BPTT entirely, requiring only O(1) memory regardless of timestep count, grounded in the Implicit Function Theorem applied to Deep Equilibrium Models. Gradients flow only through final states: output head → final H state → final L state → input embedding.
- A **deep supervision mechanism** runs multiple independent forward-pass "segments," updating parameters after each with the hidden state detached — providing frequent feedback to the H-module and acting as a regularizer.
- **Adaptive Computation Time (ACT)** uses a Q-learning head on H's final state to decide whether to halt or continue, dynamically allocating compute based on task complexity. Q-learning stability is achieved implicitly through Post-Norm RMSNorm layers and AdamW optimizer.

---

### Results & Capabilities

| Benchmark | HRM (27M) | o3-mini-high | DeepSeek R1 | Claude 3.7 8K |
|---|---|---|---|---|
| ARC-AGI-1 | **40.3%** | 34.5% | 21.0% | 21.2% |
| ARC-AGI-2 | **5.0%** | 3.0% | 0.9% | 1.3% |
| Sudoku-Extreme | **55%** | 0% | 0% | 0% |
| Maze-Hard (30×30) | **74.5%** | 0% | 0% | 0% |

HRM is trained from scratch on ~1000 examples with randomly initialized weights — no pre-training, no CoT supervision. A vanilla 175M-parameter Transformer trained on 1 million maze examples achieved below 20% accuracy using pass@64; HRM achieves 74.5% with 1000 examples and a single inference pass.

Intermediate state visualizations reveal that HRM adapts its internal reasoning strategy per task type:
- **Sudoku** — depth-first search with backtracking pattern
- **Maze** — parallel path exploration then elimination, preliminary solution construction, iterative refinement
- **ARC tasks** — incremental hill-climbing progression

HRM also exhibits **inference-time scaling**: a model trained with Mmax=8 continues to gain accuracy when run with Mmax=16, with no additional training. ACT achieves performance near fixed-compute models while using substantially fewer mean compute steps.

A structural curiosity: HRM's high-to-low participation ratio (PR ratio H/L ≈ 2.98) closely matches that measured in the mouse cortex (≈ 2.25), emerging from training rather than architectural constraint.

---

## Landscape Contributions

### Capabilities

- **ARC-AGI-1 SOTA at tiny scale** — 40.3% with 27M parameters and ~1000 training examples, no pre-training or CoT, surpassing o3-mini-high (34.5%) *(maturity: research_only)*
- **ARC-AGI-2 SOTA** — 5.0% outperforming all listed CoT frontier models *(maturity: research_only)*
- **Inference-time scaling without retraining** — increasing Mmax at inference time yields strong accuracy gains on backtracking-intensive tasks *(maturity: research_only)*
- **Adaptive compute allocation** — Q-learning ACT dynamically allocates steps per problem, achieving comparable accuracy to fixed-compute at lower mean cost *(maturity: research_only)*
- **O(1) memory recurrent training** — one-step gradient approximation replaces BPTT's O(T) memory requirement *(maturity: research_only)*
- **End-to-end latent reasoning** — trains purely on input-output pairs, no intermediate reasoning traces required *(maturity: research_only)*

### Limitations

**Blocking**
- Fixed-depth Transformers are computationally limited to AC0/TC0 — cannot solve problems requiring polynomial time regardless of width or depth scaling. Increasing width provides zero performance gain on backtracking-intensive tasks.
- Standard RNNs suffer from premature convergence, capping effective computational depth and rendering subsequent computation useless.

**Significant**
- **Inference-time scaling helps minimally on ARC-AGI** — extra compute steps yield minimal gains on inductive pattern-finding tasks, suggesting the benefit is task-type specific.
- **Complete uninterpretability** — HRM cannot explain which reasoning algorithms it has learned; no linguistic audit trail exists.
- **Narrow evaluation scope** — tested exclusively on structured puzzle benchmarks with no testing on language generation, open-ended reasoning, semantic understanding, or real-world tasks.
- **Hidden ensemble compute cost** — ARC-AGI evaluation uses voting across 1000 augmented variants at test time, making fair comparison with CoT models difficult.
- **RL-based CoT training instability** — appears to unlock existing capabilities rather than discover new reasoning mechanisms.

**Minor**
- Causal link between hierarchical representational dimensionality and reasoning performance is unconfirmed — correlation with mouse cortex PR ratios does not establish mechanistic necessity.
- Element-wise addition for combining module inputs is acknowledged as suboptimal; gating mechanisms deferred to future work.
- No hierarchical memory — full O(n²) attention blocks application to long-context reasoning.
- One-step gradient approximation truncates the Neumann series, introducing gradient inaccuracies whose severity for deeply recurrent systems far from equilibrium is unknown.

### Bottlenecks Addressed

- **Transformer computational depth ceiling** — fixed-depth architectures in AC0/TC0 blocking all algorithmic reasoning requiring polynomial time *(horizon: 3–5 years)*
- **BPTT memory scaling** — O(T) memory requirement blocking practical deep recurrent training at scale *(horizon: 1–2 years)*
- **CoT brittleness** — human-defined decompositions where a single misstep derails the entire chain *(horizon: 1–2 years)*

### Breakthroughs

- **Tasks intractable for CoT become solvable** (0% → 55% Sudoku-Extreme, 0% → 74.5% Maze-Hard) — a qualitative shift, not incremental improvement *(significance: major)*
- **CoT shown unnecessary for complex reasoning** — latent recurrent reasoning without any CoT supervision achieves SOTA ARC-AGI results *(significance: major)*
- **Hierarchical convergence overcomes premature RNN convergence** — enables effective computational depth of NT steps through periodic high-level resets *(significance: notable)*
- **Spontaneous biological correspondence** — PR ratio H/L ≈ 2.98 matches mouse cortex ≈ 2.25, emerging from training rather than design *(significance: notable)*

---

## Themes

- [[themes/adaptive_computation|Adaptive Computation]]
- [[themes/chain_of_thought|Chain-of-Thought]]
- [[themes/latent_reasoning|Latent Reasoning]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Open Questions

1. Does HRM's approach generalize beyond narrow structured puzzles to open-ended language tasks, or is it fundamentally a specialist architecture?
2. Can the hierarchical convergence mechanism be incorporated into larger-scale pre-trained models, or does it require training from scratch?
3. What is the actual compute cost when accounting for the 1000-variant ensemble at test time — is ARC-AGI-1 SOTA claim fair?
4. What reasoning algorithms does the H-module encode? The emergent DFS and parallel-exploration patterns suggest structured strategies, but the mechanisms remain opaque.
5. Does the biological correspondence (PR ratio matching mouse cortex) reflect a principled inductive bias, or is it coincidence at this scale?

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/rmsnorm|RMSNorm]]
- [[entities/universal-transformer|Universal Transformer]]
