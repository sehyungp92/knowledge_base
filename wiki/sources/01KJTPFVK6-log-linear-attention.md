---
type: source
title: Log-Linear Attention
source_id: 01KJTPFVK63FP9BRNCF5F7XXC2
source_type: paper
authors:
- Han Guo
- Songlin Yang
- Tarushii Goel
- Eric P. Xing
- Tri Dao
- Yoon Kim
published_at: '2025-06-05 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Log-Linear Attention

**Authors:** Han Guo, Songlin Yang, Tarushii Goel, Eric P. Xing, Tri Dao, Yoon Kim
**Published:** 2025-06-05 00:00:00
**Type:** paper

## Analysis

# Log-Linear Attention
2025-06-05 · paper · Han Guo, Songlin Yang, Tarushii Goel, Eric P. Xing, Tri Dao et al. (6 total)
https://arxiv.org/pdf/2506.04761

---

### Motivation & Prior Limitations
- Softmax attention's quadratic compute and linear memory costs remain fundamental bottlenecks for long-sequence modeling, limiting both new applications and scaling of existing ones.
  - Even hardware-optimized implementations (FlashAttention) do not eliminate the asymptotic quadratic-compute, linear-memory constraint.
- Linear attention and SSMs achieve linear-time, constant-memory inference by compressing all context into a fixed-size hidden state matrix, but this fixed-size constraint is itself a fundamental limitation.
  - A fixed-size hidden state is provably insufficient for tasks requiring associative recall over arbitrary context (Arora et al., 2024); linear attention variants consistently underperform softmax attention on MQAR and NIAH benchmarks.
  - Modern gated variants (Mamba-2, Gated DeltaNet) and delta-rule models close some of the gap but cannot escape the core expressiveness limitation imposed by bounded state size.
- No prior efficient architecture simultaneously achieves sub-quadratic training compute, sub-linear decoding memory, and a state that grows with sequence length to capture more context.
  - Long convolution models (Hyena, Toeplitz NN) achieve O(T log T) training via FFT but retain linear memory during inference, eliminating the memory advantage. SSMs like S4 get constant memory but lose data-dependence.

---

### Proposed Approach
- Log-linear attention replaces the single fixed-size hidden state of linear attention with a logarithmically growing set of hidden states, partitioned via a Fenwick-tree (binary indexed tree) decomposition of the prefix.
  - Each prefix [0, t) is decomposed into at most O(log T) disjoint buckets of exponentially increasing size; recent tokens are stored at fine granularity while distant tokens are summarized more coarsely, introducing a natural multi-scale inductive bias.
  - Each bucket level ℓ maintains an independent recurrent state S^(ℓ)_t ∈ R^{d×d}; at each step, a learned per-head scalar λ^(ℓ)_t (computed as a linear function of the current input) weights the contribution of each level to the output, enabling adaptive emphasis across temporal scales.
- The key theoretical insight is that this hierarchical partitioning induces a data-dependent hierarchical (HODLR-type) masking matrix M_H that replaces the semiseparable causal mask of linear/gated linear attention, yielding a matmul-rich parallel form with O(T log T) compute and O(log T) memory.
  - The parallel form is O = (QK^T ⊙ M_H) V, where M_H inherits structured low-rank off-diagonal blocks from the Fenwick decomposition; the structure is strictly between general H-matrices and semiseparable matrices (termed "quasi-H matrix").
- Log-linear attention is a general framework: any linear attention model with a structured chunkwise-parallel primitive can be "lifted" to its log-linear variant by composing its temporal mask with M_H. The paper instantiates this for Mamba-2 (scalar gating, semiseparable mask) and Gated DeltaNet (delta-rule transition, semiseparable mask).
- Training uses a two-stage chunkwise algorithm: an intra-chunk stage handles fine-grained (level < ℓ_C) interactions as dense O(C²) blocks; an inter-chunk stage handles coarser levels via O(log T/C) calls to existing linear attention primitives, each costing O(T), giving overall O(T log T) complexity. The custom Triton kernel incorporates level fusion to reduce memory-bandwidth overhead.

---

### Results & Capabilities
- Log-Linear Mamba-2's custom Triton kernel outperforms FlashAttention-2 (forward + backward) at sequence lengths beyond 8K, and the full model (with MLP layers) surpasses Transformer throughput at 32K tokens despite additional architectural components like depthwise convolutions.
  - Benchmarks on an H100 GPU show log-linear Mamba-2 achieves higher tokens/s than FlashAttention-2 for sequences ≥ 8K; the naive repeated-primitive baseline is much slower, confirming the necessity of the custom kernel.
- On the MQAR synthetic associative recall benchmark, log-linear variants consistently outperform their linear counterparts: Log-Linear Mamba-2 improves from 89.6% to 92.9% accuracy at dimension 64, and Log-Linear Gated DeltaNet improves from 79.0% to 84.4% at dimension 32.
- On language modeling (50B token pretraining, 700M–800M parameters, 16K sequence length), Log-Linear Gated DeltaNet outperforms its linear counterpart on WikiText perplexity (21.45 vs. 21.73) and LAMBADA (18.09 vs. 19.71), outperforming the layer-matched Transformer on all metrics and the parameter-matched Transformer on half.
  - Per-position loss analysis on Book3 shows log-linear variants consistently reduce loss at all context positions, indicating improved utilization of long-range context relative to their linear counterparts.
- On Needle-In-A-Haystack (NIAH) from the RULER benchmark, Log-Linear Mamba-2 improves on 8/9 single-needle metrics and 8/9 multi-needle metrics over linear Mamba-2; Log-Linear Gated DeltaNet improves on all multi-needle metrics.
  - For example, Mamba-2 single-needle pass-key retrieval at 8K improves from 56.8% to 99.8%; multi-key retrieval at 4K improves from 27.2% to 43.2%.
  - A significant performance gap to Transformers remains across all benchmarks; the paper explicitly does not claim log-linear attention is the best subquadratic architecture, only that it consistently improves over its linear baselines.

---

### Implications
- Log-linear attention establishes a new point on the compute-memory-expressiveness Pareto frontier: O(T log T) compute and O(log T) memory at inference, filling a gap between constant-memory SSMs and full softmax attention, with a principled theoretical basis in hierarchical matrix theory.
- The framework is architecture-agnostic and composable: any existing linear attention or

## Key Claims

1. Softmax attention has quadratic compute and linear memory complexity with respect to sequence length, which is a fundamental bottleneck.
2. Linear attention enables linear-time, constant-memory sequence modeling by replacing the softmax kernel with a linear kernel, allowing reformulation as a linear RNN with matrix-valued hidden states.
3. Linear attention's use of a fixed-size hidden state is a fundamental limitation for certain capabilities such as associative recall over a given context.
4. Log-linear attention replaces the fixed-size hidden state with a logarithmically growing set of hidden states, achieving O(T log T) compute and O(log T) memory complexity.
5. Log-linear attention is a general framework applicable on top of existing linear attention variants.
6. Many efficient attention mechanisms—including linear attention, SSMs, and long convolution models—can be unified under the formulation P = A ⊙ M, O = PV, where the structure of M determines compute an
7. Log-linear attention uses Fenwick-tree decomposition to partition the token prefix into logarithmically many buckets of exponentially increasing size, creating an inductive bias where recent tokens ha
8. Log-linear attention maintains a separate recurrent memory state for each bucket and adaptively weights contributions from different temporal scales using learned per-level coefficients λ.
9. When all per-level λ coefficients are the same (or linearly related across time), log-linear attention collapses to standard linear attention, making distinct λ values essential for capturing multi-sc
10. The parallel form of log-linear attention corresponds to structured matrix multiplication with a hierarchical (HODLR) matrix, establishing a direct connection between log-linear attention and hierarch

## Capabilities

- Log-linear attention achieves O(T log T) compute and O(log T) memory for sequence modeling via Fenwick-tree hierarchical state partitioning, with a custom Triton kernel for log-linear Mamba-2 that outperforms FlashAttention-2 throughput at sequence lengths beyond 8K
- Log-linear Gated DeltaNet outperforms its linear counterpart on all language modeling benchmarks and matches or exceeds a layer-matched Transformer across all standard short-context metrics at 700-800M parameter scale trained on 50B tokens
- Log-linear variants of Mamba-2 and Gated DeltaNet consistently reduce per-position loss across all sequence positions up to 16K compared to their linear counterparts, indicating improved long-range context utilization
- Log-linear attention framework provides a general upgrade mechanism: any linear attention or SSM architecture with structured memory and an efficient chunkwise-parallel primitive can be systematically lifted to log-linear complexity by composing its temporal mask with a hierarchical matrix
- Log-linear attention improves multi-query associative recall (MQAR) accuracy over vanilla linear attention variants, including over associative-recall-optimized architectures like Gated DeltaNet

## Limitations

- Log-linear attention still has a significant performance gap compared to full Transformers across all benchmarks, including language modeling perplexity and long-context retrieval
- Log-linear attention did not improve over linear attention baselines on many tasks, making its benefits task-dependent and not universally guaranteed
- Engineering complexity of log-linear attention is substantially higher than linear attention: intra-chunk operations require bespoke kernel implementations, and the backward pass requires manually computing gradients for the additional λ weighting terms
- Fenwick-tree partitioning introduces a fixed inductive bias — recent tokens receive fine-grained memory, distant tokens are aggressively compressed — which may be suboptimal for tasks requiring uniform long-range access or non-temporal patterns
- Compute constraints prevented any hyperparameter search for log-linear models: all 700-800M parameter runs were executed once, meaning reported results likely understate true performance potential and reproducibility cannot be assessed
- Log-linear Mamba-2 performance on UUID-in-haystack (S-NIAH-3) collapses to near zero at 16K context (2.0%), revealing a sharp performance cliff on retrieval tasks requiring distinguishing among hard-to-distinguish tokens at long range
- All sub-quadratic models including log-linear variants perform poorly on multi-needle long-context retrieval: Log-Linear Mamba-2 achieves only 21.2% on MK-NIAH at 16K, showing logarithmic memory is insufficient for simultaneous multi-trace long-context access
- The Hyena model, which also achieves log-linear compute but retains linear O(T) memory, has substantially worse perplexity (~29 vs <23 for other models), demonstrating that log-linear compute alone is insufficient — the memory complexity (O(log T) vs O(T)) is a co-determining factor of quality
- Log-linear attention has only been instantiated for Mamba-2 and Gated DeltaNet; coverage of the broader architecture space (xLSTM, MesaNet, and others) remains absent, leaving the generality claim empirically unverified
- Log-linear attention has only been validated at academic scale (~700-800M parameters, 50B tokens, 16K sequence length); behavior at frontier model scales (10B+ parameters, multitrillion tokens, 128K+ context) is entirely unknown
- The paper's authors explicitly frame experiments as demonstrating 'promise' rather than positioning log-linear attention as the best subquadratic architecture, indicating preliminary rather than conclusive evidence for the approach

## Bottlenecks

- Engineering complexity of log-linear attention — bespoke intra-chunk kernels and non-trivial manual backward pass — creates a significant adoption barrier and prevents systematic ablation studies, slowing iteration on the design space
- Compute cost of log-linear pretraining at 700-800M scale prevents comprehensive hyperparameter search, leaving the optimal λ parameterization unexplored and true performance ceiling unestablished
- No sub-quadratic architecture has closed the quality gap with full Transformers on multi-needle long-context retrieval: logarithmic memory compression remains insufficient for simultaneous access to multiple distinct long-range memory traces

## Breakthroughs

- Log-linear attention establishes a principled, implementable middle ground between linear attention (O(T) compute, O(1) memory) and softmax attention (O(T²) compute, O(T) memory), achieving O(T log T) compute and O(log T) memory via Fenwick-tree hierarchical state partitioning — with a custom Triton

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/linear-attention|Linear Attention]]
- [[entities/longbench|LongBench]]
