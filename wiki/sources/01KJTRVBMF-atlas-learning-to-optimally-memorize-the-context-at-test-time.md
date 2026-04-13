---
type: source
title: 'ATLAS: Learning to Optimally Memorize the Context at Test Time'
source_id: 01KJTRVBMFVYDEM72NMZ36C1ZK
source_type: paper
authors:
- Ali Behrouz
- Zeman Li
- Praneeth Kacham
- Majid Daliri
- Yuan Deng
- Peilin Zhong
- Meisam Razaviyayn
- Vahab Mirrokni
published_at: '2025-05-29 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- post_training_methods
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ATLAS: Learning to Optimally Memorize the Context at Test Time

**Authors:** Ali Behrouz, Zeman Li, Praneeth Kacham, Majid Daliri, Yuan Deng, Peilin Zhong, Meisam Razaviyayn, Vahab Mirrokni
**Published:** 2025-05-29 00:00:00
**Type:** paper

## Analysis

# ATLAS: Learning to Optimally Memorize the Context at Test Time
2025-05-29 · paper · Ali Behrouz, Zeman Li, Praneeth Kacham, Majid Daliri, Yuan Deng et al. (8 total)
https://arxiv.org/pdf/2505.23735

---

### Motivation & Prior Limitations
Modern recurrent neural networks (linear RNNs) were developed to escape Transformers' quadratic memory and time complexity in long-context settings, but they introduced their own structural failures that the authors decompose into three distinct and disjoint design flaws.
- The **online nature** of recurrent memory updates is a fundamental bottleneck: these models optimize their internal memory objective with respect to only the current input token while retaining the prior memory state, causing greedy, token-by-token memorization that ignores broader contextual structure.
  - This contrasts with softmax attention, which is a non-parametric optimizer that globally minimizes its internal objective across all past tokens simultaneously — a distinction the authors formalize through the attentional bias framework.
- **Limited memory capacity** constrains how many independent key-value associations a fixed-size memory can store: a matrix-valued memory with d_k × d_v parameters using gradient descent can store at most O(d_k) linearly independent key-value pairs (Proposition 1), which is sub-linear relative to parameter count.
  - Deep memory modules (MLPs) improve this to O(d_k · d_v) (Theorem 1), but the upper bound remains sub-quadratic, leaving a substantial gap between expressiveness and capacity.
- **Weak memory management** compounds both problems: nearly all existing recurrent models use first-order gradient descent to optimize their internal memory objective, making them vulnerable to convergence at spurious local minima, especially under the distributional pressures of very long sequences.
  - Prior work such as Titans attempted to address the online limitation by splitting surprise into "momentary" and "past" components with momentum, but this still memorizes individual tokens rather than token contexts, and still uses first-order optimization.

---

### Proposed Approach
The paper presents Atlas, a long-term neural memory module that simultaneously addresses all three limitations through three interacting innovations: the Omega learning rule for context-aware memory updates, polynomial feature kernels for superlinear memory capacity, and the Muon optimizer for locally optimal second-order memory management.

- The **Omega rule** replaces the standard online (single-token) update with a sliding-window optimization objective: at each time step t, the memory is updated by minimizing a weighted sum of attentional bias losses over the most recent c tokens, using input-dependent decay gates γ_i^(t) ∈ [0,1] that allow the model to directly prune irrelevant context tokens from the optimization.
  - At c=1, Omega reduces exactly to the Delta rule (online gradient descent); at c=∞, it becomes global optimization over the entire sequence. The sliding-window formulation preserves efficiency while filling the gap between these extremes.
  - Parallel training is achieved by chunking the sequence and computing all gradients within a chunk relative to the last state of the prior chunk, using a sliding-window mask applied during einsum broadcasting; this adds negligible overhead over the c=1 online case.

- **Polynomial feature kernels** φ_p(x) = [x^β]_{|β|≤p} are applied to keys and queries to increase effective input dimensionality without increasing input projection parameter count, raising memory capacity to O(d_k^p) for a matrix-valued memory (Proposition 2).
  - These kernels are theoretically motivated as truncated Taylor series approximations of the softmax exponential kernel, with learnable coefficients a_i initialized at 1/i! that can be interpreted as input-level feature gates. Using the infinite-dimensional exponential kernel φ*(x) in place of polynomial kernels yields DeepTransformers, a family of architectures proven to be strict generalizations of original softmax Transformers.

- Atlas uses the **Muon optimizer** (a momentum-based method applying Newton-Schulz orthogonalization to the gradient momentum term) to optimize the Omega objective, making it the first parallelizable recurrent architecture to approximate second-order information in memory updates.
  - The Newton-Schulz iteration count k acts as an internal test-time compute knob: as k→∞, the update converges to the nearest semi-orthogonal matrix to the momentum term, approximating a true second-order step. The momentum recurrence in Atlas is shown to be independent of the memory state within a chunk, enabling all Newton-Schulz operations across a chunk to be computed in parallel.

- The paper additionally introduces **OmegaNet** (Omega rule + polynomial kernels + gradient descent), **DeepTransformers** (deep memory + exponential kernels as strict Transformer generalization), **Dot** (DeepTransformers + Omega rule), **DLA** (deep gated linear attention baseline), and hybrid variants MAG and MAL that combine Atlas memory with sliding window attention.

---

### Results & Capabilities
Atlas and OmegaNet consistently outperform both Transformers and state-of-the-art linear RNNs across language modeling, commonsense reasoning, long-context needle-in-haystack, synthetic recall, and memorization benchmarks, with the most dramatic gains at long context lengths.

- On language modeling with 760M parameters trained on 30B tokens, Atlas achieves perplexity 18.92 on WikiText versus Transformer++'s 25.21, Titans' 20.04, and Gated DeltaNet's 21.18, while its MAG hybrid reaches 18.62. At 1.3B parameters / 100B tokens, Atlas scores 14.97 versus Transformer++'s 18.53 and Titans' 15.60.
  - Downstream commonsense accuracy (average across PIQA, HellaSwag, WinoGrande, ARC, SIQA, BoolQ) for Atlas at 760M is 52.77, outperforming Transformer++ at 48.69, Titans at 51.56, and matching or exceeding hybrid models li

## Key Claims

1. Transformers have quadratic memory and time complexity, which bounds their applicability to longer sequences.
2. Modern recurrent neural networks (long-term recurrent memory modules) struggle with long context understanding and extrapolation to longer sequences despite recent success in diverse downstream tasks.
3. The shortcomings of modern recurrent models arise from three disjoint design aspects: limited memory capacity, online nature of update, and less expressive management of fixed-size memory.
4. Atlas, built on the Omega rule and Muon optimizer, surpasses the performance of Transformers and recent linear recurrent models on language modeling, common-sense reasoning, recall-intensive, and long
5. Atlas achieves +80% accuracy improvement over Titans on the BABILong benchmark at 10M context length.
6. Attention functions as an associative memory that computes direct pairwise token dependencies, causing at least N×d operations per token for output calculation.
7. Modern recurrent architectures can be unified as associative memory modules optimizing an internal objective termed 'attentional bias'.
8. The online nature of memory updates in most recurrent models—where memory is optimized with respect to only the current input—leads to memorization of individual tokens without considering broader con
9. Most recent recurrent models use gradient descent relying on first-order information about token dynamics, which causes memory to converge to spurious local minima and learn less effective key-value m
10. Atlas is the first parallelizable recurrent architecture that optimizes memory using an approximation of second-order information, giving it a locally optimal memory module.

## Capabilities

- Atlas recurrent architecture achieves over 80% accuracy at 10M token context length on BABILong benchmark, maintaining performance where Titans degrades significantly
- First parallelizable recurrent architecture using second-order (Muon) memory optimization, achieving locally optimal memory management without substantial training overhead versus first-order online recurrence
- Omega rule enables context-level memorization in recurrent models by optimizing memory based on a sliding window of past tokens rather than individual tokens, parametrically mirroring sliding window attention
- DeepTransformers family strictly generalizes softmax Transformers using deep memory with exponential kernel, outperforming Transformer++ at both 760M and 1.3B parameter scales on perplexity and downstream accuracy
- Polynomial feature mappings of degree p on keys provide O(d_k^p) memory capacity — superlinear scaling relative to key dimension — without incurring additional parameter overhead on input projections
- Hybrid Atlas variants (MAG, MAL) extrapolate to context lengths 4x their training window (trained at 4K, tested at 16K) with competitive needle-in-haystack performance against full-attention baselines
- Newton-Schulz iteration count (k) in Atlas serves as a tunable test-time compute parameter for memory quality — more steps yield better memorization, enabling quality-vs-latency trade-offs at inference

## Limitations

- Recurrent models including Atlas still significantly underperform Transformers on in-context recall tasks — 43.70 vs 53.55 average score across SWDE, NQ, DROP, FDA, SQUAD, TQA benchmarks
- Global context optimization (optimizing memory w.r.t. all past tokens) is computationally infeasible at extreme sequence lengths and produces sub-optimal performance due to irrelevant context mid-sequence
- Deep memory module capacity upper bound remains subquadratic in key and value dimensions even with deep MLPs — theoretical gap persists versus Transformers' unbounded KV cache
- First-order gradient descent memory optimization converges to spurious local minima, limiting quality of key-value mappings — identified as a core design flaw in all prior modern RNN architectures including Titans
- All Atlas experiments trained on 4K context length — 10M context BABILong results rely on fine-tuning from a 4K-pretrained checkpoint, not end-to-end long-context pretraining
- Naive Omega rule implementation requires materializing c full gradient matrices (each R^{d_in × d_in}), causing memory footprint and I/O cost proportional to context window size times model dimension squared
- Global memory optimization via Sherman-Morrison direct solution is limited to linear matrix-valued memory only and is non-parallelizable — excludes deep or non-linear memory architectures from exact solutions
- Learnability experiments show models fail worst on tasks requiring memory of prior inputs under sliding window attention — learning algorithm appears unable to selectively forget old inputs, degrading performance relative to global attention
- Chunked parallel training approximates gradient computation w.r.t. the last state of the previous chunk — intra-chunk gradient fidelity is reduced compared to exact sequential recurrent updates
- Learnability experiments with randomly initialized attention vectors produce near-uniform attention matrices (attention outputs close to mean of values) — the experimental setup does not replicate the sharp, task-specific attention patterns of trained LLMs

## Bottlenecks

- First-order-only memory optimization in all existing parallelizable recurrent architectures causes convergence to local optima in long-context memorization tasks — no prior parallelizable model used second-order information for internal memory updates
- Online-only memory update in recurrent models — optimizing solely with respect to the last input token — prevents context-level understanding and forces greedy, suboptimal memorization of individual tokens

## Breakthroughs

- Omega rule enables parametric recurrent memory to optimize over a sliding context window rather than a single token — context-level memorization (analogous to sliding window attention) within a parallelizable fixed-size memory framework
- Atlas is the first parallelizable recurrent architecture using second-order (Muon/Newton-Schulz) memory optimization, achieving locally optimal memory management with k Newton-Schulz steps as a tunable test-time compute parameter
- DeepTransformers proved to be strict generalizations of softmax Transformers — the original Transformer is a special case (non-parametric, infinite-dimensional kernel) of a broader parametric deep-memory sequence model family

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/test_time_learning|test_time_learning]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/associative-memory|Associative memory]]
- [[entities/babilong-benchmark|BABILong benchmark]]
- [[entities/delta-rule|Delta Rule]]
- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/sliding-window-attention|Sliding Window Attention]]
