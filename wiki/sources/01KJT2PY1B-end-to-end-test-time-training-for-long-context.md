---
type: source
title: End-to-End Test-Time Training for Long Context
source_id: 01KJT2PY1BKRBNJRKVNMDZTGD5
source_type: paper
authors:
- Arnuv Tandon
- Karan Dalal
- Xinhao Li
- Daniel Koceja
- Marcel Rød
- Sam Buchanan
- Xiaolong Wang
- Jure Leskovec
- Sanmi Koyejo
- Tatsunori Hashimoto
- Carlos Guestrin
- Jed McCaleb
- Yejin Choi
- Yu Sun
published_at: '2025-12-29 00:00:00'
theme_ids:
- continual_learning
- in_context_and_meta_learning
- long_context_and_attention
- model_architecture
- post_training_methods
- pretraining_and_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# End-to-End Test-Time Training for Long Context

TTT-E2E proposes reformulating long-context language modeling as a continual learning problem, using meta-learning at training time to prepare a sliding-window Transformer to continue learning at test time via next-token prediction — achieving the same context-length scaling quality as full attention while maintaining constant inference latency, at the cost of significant training overhead and complete failure on recall-intensive tasks.

**Authors:** Arnuv Tandon, Karan Dalal, Xinhao Li, Daniel Koceja, Marcel Rød, Sam Buchanan, Xiaolong Wang, Jure Leskovec, Sanmi Koyejo, Tatsunori Hashimoto, Carlos Guestrin, Jed McCaleb, Yejin Choi, Yu Sun
**Published:** 2025-12-29
**Type:** paper
**Source:** https://arxiv.org/pdf/2512.23675

---

## Problem & Motivation

Long-context language modeling has been treated primarily as an architecture design problem, but no existing efficient architecture achieves the same scaling behavior as full attention as context length grows. The alternatives all fail in different ways:

- **Full attention** scales quadratically in prefill (O(T²)) and linearly in decode (O(T)), becoming prohibitively expensive at 128K+ tokens — yet it remains the only approach whose loss consistently improves with longer context.
- **RNNs** (Mamba 2, Gated DeltaNet) have constant cost per token but degrade in quality at longer contexts, empirically failing to match full attention's loss delta even at 32K tokens.
- **Sliding-window attention (SWA)** and hybrid architectures maintain constant cost but suffer severe quality degradation beyond the window boundary.
- **Prior TTT approaches** (TTT-KVB, MesaNet, Titans) use a layer-wise key-value binding reconstruction loss rather than end-to-end next-token prediction, creating an objective mismatch at test time; their hidden states are also severely constrained by chip memory.
- **Dynamic evaluation** (the historical TTT precursor) trains with a naive loss that ignores the fact that weights will be updated at test time, producing only marginal gains over static baselines.

This paper's core diagnostic: the failure of prior TTT approaches is almost entirely attributable to the training-test mismatch — switching from the layer-wise reconstruction loss to a single global next-token prediction objective accounts for nearly all of the performance gain.

---

## Approach

### The Inner Loop: Test-Time Training

At test time, the model performs mini-batch gradient descent on the next-token prediction loss over successive chunks of context tokens, updating only the MLP layers of the **last 1/4 of Transformer blocks**. Sliding-window attention (window size k=8K) handles local context within each mini-batch, ensuring no token loss within a batch. Context is thereby compressed into MLP weights rather than maintained as a KV cache.

Computational complexity: **O(T) prefill, O(1) decode** — compared to O(T²) / O(T) for full attention.

### The Outer Loop: Meta-Learning the Initialization

At training time, each sequence is treated as a test sequence: TTT is performed in the inner loop, and gradients of gradients (second-order, MAML-style) propagate through the inner-loop updates to optimize the initialization for post-TTT performance. This is what makes the method "end-to-end" — the training loss matches the actual test loss after TTT, eliminating the training-test mismatch that cripples TTT-naive.

Three critical implementation choices:
1. Only MLP layers are updated during TTT (freezing attention, embeddings, normalization avoids instability).
2. Only the last 1/4 of blocks are TTT'd, trading state size for compute efficiency.
3. A static second MLP layer is added to each TTT'd block as a "safe harbor" for pre-trained knowledge, with other MLP dimensions reduced to keep total parameter count constant.

Because the hidden state is stored as regular MLP weights, TTT-E2E requires **no custom kernels** and uses standard training infrastructure (sharding, FlashAttention at inference) — overcoming the chip-memory limitations that force prior constant-cost methods to fit state onto individual GPU chips.

---

## Results

### Context-Length Scaling

For 3B models trained on 164B tokens, TTT-E2E is the only method besides full attention whose loss consistently improves from 8K to 128K context. Mamba 2, Gated DeltaNet, SWA, and TTT-KVB all show progressively worse loss at longer contexts.

Notably, TTT-E2E achieves **lower token-level loss than full attention throughout the entire context window** — the advantage is largest for early tokens, even before the first TTT gradient step at t=1K. The explanation: TTT-E2E weights need only to be good at a focused present mini-batch, not all possible futures.

Adding TTT-E2E on top of full attention (k=8K) improves loss by 0.018 — the benefit is orthogonal to local attention quality.

### Latency

- **Prefill at 128K:** 2.7× faster than full attention on H100
- **Training at 8K:** 3.4× *slower* than full attention (the critical bottleneck for pre-training)

### Scaling Behavior

TTT-E2E initially underperforms full attention at small compute budgets (< 760M parameters, < 48B training tokens) but converges to the same scaling trend above these thresholds — a minimum training investment is required before the method functions as advertised.

---

## Limitations & Open Questions

### Fundamental

**Recall is broken.** Full attention dramatically outperforms TTT-E2E on all Needle-in-a-Haystack benchmarks at every context length. Lossy compression discards exact token positions. This is not an implementation detail — the [[themes/long_context_and_attention|compression–recall tradeoff]] appears fundamental to any constant-inference-cost method, and it blocks deployment in document search, legal/medical fact retrieval, and code reference applications.

**Scale is unvalidated.** All experiments are limited to 3B parameters. The core claim — that context-length scaling benefits hold — is entirely unvalidated at the 70B–700B scales where deployment decisions are made.

### Engineering

**Training overhead blocks pre-training adoption.** The 3.4× training slowdown at short contexts is disqualifying: most pre-training compute is spent at short contexts. The root cause is that gradients-of-gradients are incompatible with cuDNN FlashAttention, preventing the single largest GPU utilisation improvement available. A custom attention kernel would resolve this but does not yet exist.

**Gradient checkpointing grows superlinearly.** Checkpointing through time introduces log(T) overhead, causing wall-clock training latency to grow between 8K and 32K context lengths even though FLOPs per token remain constant.

### Architectural Constraints

**Hard layer count threshold.** Updating fewer than 6 of 24 blocks (< 25%) eliminates the context-scaling advantage entirely. This creates a rigid architectural constraint with no smooth degradation.

**Minimum training budget.** The advantage over full attention collapses below ~760M parameters or ~48B training tokens. The method requires a minimum investment threshold to function at all.

### Evaluation Coverage

**Instruction-tuned and RLHF models untested.** The primary real-world use case — long chain-of-thought generation by post-trained models — is entirely unevaluated. Only uninstructed base models are assessed.

**Domain-narrow fine-tuning.** Long-context fine-tuning relies exclusively on the Books dataset; high-quality documents exceeding 128K tokens are largely absent from web-scraped corpora. Results may not transfer to heterogeneous real-world distributions.

**Tokenizer and data vintage sensitivity.** Switching from a 2023-vintage tokenizer/dataset to 2024 vintage improved advantage over full attention by ~0.01 for 3B models, indicating results are sensitive to recency of training data.

---

## Connections

### Thematic

- [[themes/test_time_learning|Test-Time Learning]] — the central mechanism; this work's primary contribution to the theme is demonstrating that the training-test objective mismatch in dynamic evaluation is the main source of failure, and that MAML-style meta-learning resolves it
- [[themes/continual_learning|Continual Learning]] — the reframing of long-context modeling as continual learning is the paper's conceptual anchor; MLP weights act as a continually-updated compressed memory
- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]] — meta-learning (MAML-style bi-level optimization) is the outer loop; the training-time meta-objective directly prepares the model for test-time learning
- [[themes/long_context_and_attention|Long Context and Attention]] — directly addresses the quadratic scaling problem; the compression-recall tradeoff surfaces a fundamental limitation of any constant-cost approach
- [[themes/model_architecture|Model Architecture]] — architectural choices (which layers to TTT, safe-harbor MLPs, SWA base) are load-bearing; the method is architecture-specific, not a general wrapper
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — scaling laws show TTT-E2E requires minimum compute thresholds; the 3.4× training overhead at short context is the key barrier to pre-training adoption
- [[themes/post_training_methods|Post-Training Methods]] — implications for instruction tuning and RLHF are acknowledged but entirely untested

### Conceptual Contrasts

- **vs. TTT-KVB / MesaNet / Titans:** Same family of test-time updating methods, but prior work uses layer-wise KVB reconstruction loss (deeply-supervised, layer-local); TTT-E2E switches to a single global next-token prediction objective, which is nearly the entire source of improvement.
- **vs. Dynamic evaluation (TTT-naive):** Dynamic evaluation is TTT-E2E without the outer meta-learning loop — it naively replicates the static training loss without accounting for weight changes at test time, yielding only marginal gains.
- **vs. Mamba 2 / Gated DeltaNet:** Both have constant inference cost but lack context-length scaling in quality; TTT-E2E matches full attention's loss trajectory while achieving the same constant decode cost.

---

## Key Claims (Selected)

| Claim | Evidence |
|---|---|
| TTT-E2E scales with context length identically to full attention for 3B/164B models | Loss delta vs. full attention stays near 0 from 8K to 128K |
| Constant inference latency; 2.7× faster than full attention at 128K on H100 | Direct latency benchmarks |
| End-to-end meta-learning (not layer-wise KVB) is the critical variable | Ablation: switching loss from KVB to NTP accounts for nearly all improvement |
| Online (b=1) inner-loop updates cause gradient explosion instability | Stability analysis in ablations |
| Second-order gradients feasible with minimal overhead in modern autodiff | Implementation benchmarks |
| Context-length scaling requires ≥6/24 blocks updated | Hard threshold ablation |

---

## Significance

TTT-E2E is a **major breakthrough** in efficient long-context modeling: it is the first constant-inference-cost method to match full-attention context-length scaling quality at the 3B scale. The conceptual reframing — treating long-context modeling as continual learning, and the training phase as meta-learning over test scenarios — is likely to influence subsequent work regardless of whether TTT-E2E itself reaches production.

The paper also makes a precise diagnostic contribution: it isolates the training-test objective mismatch as the primary failure mode of prior TTT work, providing a clear recipe for what "end-to-end" means in this setting.

The open problems are equally significant as the results. The compression-recall tradeoff appears to be a fundamental ceiling for all constant-cost approaches, not a fixable implementation gap. Until this tradeoff is resolved — or applications are found where lossy compression is acceptable — TTT-E2E and its successors will remain complementary to, rather than replacements for, full attention.
