---
type: source
title: 'Titans: Learning to Memorize at Test Time'
source_id: 01KJV5HWSHN2WAY8MNS8DJ7GGR
source_type: paper
authors:
- Ali Behrouz
- Peilin Zhong
- Vahab Mirrokni
published_at: '2024-12-31 00:00:00'
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
# Titans: Learning to Memorize at Test Time

Titans introduces a neural long-term memory module (LMM) that learns to memorize historical context directly into its parameters via online gradient descent during inference, resolving the fundamental tension between Transformers (accurate but quadratic) and linear recurrent models (efficient but memory-limited). By framing memory formation as a meta-learning problem driven by a biologically-inspired surprise metric — gradient magnitude with momentum and adaptive decay — Titans achieves state-of-the-art performance on language modeling, long-context retrieval, and reasoning benchmarks while scaling to context windows exceeding 2M tokens.

**Authors:** Ali Behrouz, Peilin Zhong, Vahab Mirrokni
**Published:** 2024-12-31
**Type:** paper
**Source:** https://arxiv.org/pdf/2501.00663

---

## Motivation

The field has long been caught between two unsatisfying choices. [[themes/long_context_and_attention|Transformers]] model token dependencies accurately but incur quadratic O(n²) time and memory complexity, making them impractical beyond fixed context windows. [[themes/transformer_alternatives|Linear Transformers and SSMs]] reduce this to linear complexity, but compress history into a fixed-size matrix-valued state — a fundamental contradiction: these models are most advantageous at very long contexts, yet least capable of faithfully representing them.

The deeper problem is architectural: no prior sequence model simultaneously provides short-term memory, long-term memory, meta-memory, and the ability to actively learn and memorize abstractions of past history at test time — capabilities that human memory systems combine naturally. Prior fast-weight / associative memory models (DeltaNet, GLA, Mamba2) rely only on momentary surprise, missing the temporal flow of surprise across a sequence, and most lack proper forgetting gates, causing memory to degrade over long sequences.

---

## Core Contribution: Neural Long-Term Memory

The central innovation is a **neural long-term memory module** — a deep MLP (≥1 layer) whose weights are updated at test time via gradient descent on an associative memory objective:

```
ℓ(M; x) = ‖M(k_t) − v_t‖²
```

The gradient magnitude with respect to this loss serves as a **surprise metric**: inputs that violate the model's current expectations produce large gradients and are memorized more strongly, mirroring biological long-term memory formation. This framing treats memory update as online meta-learning, not state compression.

### Surprise Decomposition

Surprise is decomposed into two components, analogous to gradient descent with momentum:

- **Momentary surprise** — the current gradient, capturing immediate expectation violation
- **Past surprise** — a momentum term S_{t-1} with data-dependent decay η_t, enabling sustained attention to an event across time even after initial surprise fades

A key design choice: the decay η_t is **data-dependent**, conditioned on contextual relevance between tokens. Surprise from previous tokens may be irrelevant in the current context (high decay) or critically important (low decay). This data-dependency is what distinguishes Titans from prior momentary-surprise-only approaches.

Raw gradient-magnitude surprise can vanish after consecutive surprising events — causing memory learning to stall in flat loss landscape regions and miss subsequent important information. The momentum term directly addresses this failure mode.

### Adaptive Forgetting

An adaptive weight decay α_t ∈ [0,1] allows selective erasure of stale information. The paper proves this mechanism generalizes the gating of Mamba, Griffin, and other modern RNNs as special cases — these architectures' forgetting mechanisms are special cases of a more general framework.

### Why Deep Memory?

Using a matrix-valued memory W is equivalent to online linear regression — it can only capture linear dependencies in historical data. Deep MLP memory (L_M ≥ 2) is strictly more expressive by classical MLP expressivity results, and the paper validates this empirically: deeper memory achieves better perplexity at all sequence lengths, with greater robustness at longer contexts. The cost is a linear per-depth training overhead, creating a direct tradeoff between representational capacity and efficiency.

### Parallelizable Training

Despite being recurrent in structure, the LMM can be trained in O(N) FLOPs via reformulation as chunk-wise mini-batch gradient descent entirely in terms of matrix multiplications, building on the TTT tensorization insight and using parallel associative scan for the momentum recurrence. This is what makes Titans practically trainable at scale.

---

## Architecture: Three Integration Variants

Titans combines the LMM (long-term memory), a sliding-window or full attention module (short-term memory), and **persistent memory** (learnable but input-independent parameters prepended to the sequence, encoding task-level knowledge) in three configurations:

| Variant | Design | Character |
|---|---|---|
| **MAC** (Memory as Context) | Retrieve past memory as context prepended to each attention window | Attention gates which historical memory is used |
| **MAG** (Memory as Gate) | Parallel sliding-window attention and LMM branches, combined via non-linear gating | Symmetric integration of short- and long-term paths |
| **MAL** (Memory as Layer) | Sequential stack of LMM then sliding-window attention | Consistent with H3-style hybrid designs |

Persistent memory tokens serve a dual function: encoding task-level priors, and mitigating the implicit bias of causal attention toward initial sequence positions — without them, attention weights over-concentrate on early tokens.

---

## Results

### Language Modeling (FineWeb-Edu, 340M–760M parameters)

All three Titans variants outperform Transformer++, Mamba, Mamba2, GLA, DeltaNet, TTT, Gated DeltaNet, Samba, and Gated DeltaNet-H2 across scales. At 400M:

- **Titans (MAG)**: 23.59 wiki perplexity, 48.60% avg commonsense accuracy
- **Transformer++**: 30.63 perplexity, 45.64% accuracy
- **Gated DeltaNet**: 25.47 perplexity, 47.26% accuracy

### Long-Context Retrieval (RULER S-NIAH, 16K tokens)

| Model | S-NIAH-1 | S-NIAH-2 | S-NIAH-W |
|---|---|---|---|
| Titans (MAC) | 98.4% | 97.4% | 95.2% |
| TTT | 88.4% | 4.4% | 0.0% |
| Mamba2 | 5.4% | 0.0% | 0.0% |

Mamba2's collapse to 0% on word-level retrieval at 16K tokens reflects the fundamental architectural failure of SSM gating without erasure: irrelevant content accumulates in the fixed-size state and cannot be removed.

### Long-Context Reasoning (BABILong)

A small fine-tuned Titans (MAC) outperforms GPT-4, GPT-4o-mini, Qwen2.5-72B, Llama3.1-70B, Llama3.1-8B+RAG, Mamba, and RMT — despite having approximately 70× fewer parameters than GPT-4. This result is striking but should be read carefully: BABILong tests specific compositional reasoning patterns, not general capability.

### Context Scaling

Titans scale to context windows exceeding **2M tokens** while maintaining higher needle-in-haystack accuracy than all baselines — a capability Transformers cannot match due to quadratic complexity. Notably, training was conducted at only 4K tokens; the 2M+ inference context is entirely out-of-distribution for the learned memory, and long-context robustness under training distribution has not been systematically validated.

---

## Theoretical Position

Titans are provably more expressive than Transformers and most modern linear recurrent models, capable of solving problems in state tracking beyond the TC0 complexity class — the ceiling that limits Transformers, diagonal linear recurrent models, and DeltaNet. This matters because TC0-hard problems include many structured reasoning and state tracking tasks that current architectures struggle with.

---

## Limitations and Open Questions

**Scale validation is absent.** All experiments top out at 760M parameters. Scaling behavior to frontier sizes (7B, 13B, 70B+) is entirely unvalidated, and it is not known whether the architectural advantages hold at scale or whether optimization dynamics change. The paper acknowledges this explicitly, noting that frontier-scale experiments are in progress.

**Training vs. inference context mismatch.** Training uses 4K token context while inference demonstrations reach 2M+. Long-context performance emerges from the memory's generalization properties, not from training signal at those lengths — a genuine unknown for production reliability.

**Throughput penalty.** The neural memory module is slower in training throughput than Mamba2 and Gated DeltaNet due to deeper memory and the absence of hardware-optimized custom CUDA kernels. This is framed as an engineering gap rather than a fundamental limitation, but it matters for fair benchmarking and practical adoption. Custom kernel development for novel architectures typically lags model publication by months.

**Variant inconsistency.** MAL at 760M shows dramatically degraded SIQA performance (30.98) versus MAC (41.87) and MAG (40.38), revealing that architecture variant choice interacts with task type in ways not yet understood. Users cannot simply pick any variant without task-specific validation.

**Parallelism-expressiveness tradeoff.** Making memory update parameters (α, θ, η) chunk-level rather than token-level enables faster training but sacrifices expressive power — a fundamental tradeoff with no clear resolution.

**Scope of memory architecture.** The paper restricts memory to simple MLPs. Whether more expressive memory architectures (hypernetworks, attention-based memory) would yield additional gains is left open, and the ablation does not distinguish depth effects from nonlinearity effects cleanly.

**Evaluation coverage.** Experiments use exclusively English FineWeb-Edu and Pile datasets. Multilingual capability, domain generalization, and instruction-following quality are entirely undemonstrated.

---

## Connections and Implications

This work sits at the intersection of several active themes:

- **[[themes/test_time_learning|Test-Time Learning]]**: Titans is the most principled instantiation of the test-time learning paradigm for sequence modeling, extending TTT (Yu Sun et al. 2024) with momentum, weight decay, and deep memory. The key advance over TTT is temporal surprise flow rather than momentary surprise.

- **[[themes/transformer_alternatives|Transformer Alternatives]]**: Titans does not replace attention — it augments it. The MAC variant in particular treats neural memory and attention as complementary systems (long-term vs. short-term), which may be a more durable architectural principle than pure attention-replacement approaches.

- **[[themes/model_architecture|Model Architecture]]**: The three-layer memory decomposition (persistent, long-term neural, short-term attention) is a principled decomposition that maps onto cognitive memory systems. The persistent memory finding — that prepended learnable parameters mitigate causal attention's initial-token bias — is a practically useful insight independent of the broader Titans framework.

- **[[themes/long_context_and_attention|Long Context and Attention]]**: The 2M+ token capability, if it holds at scale and training distribution, would represent a qualitative shift in what sequence models can process. The caveat is that this is demonstrated at research scale on a narrow benchmark distribution.

- **[[themes/post_training_methods|Post-Training Methods]]**: The BABILong result — a small fine-tuned model outperforming much larger instruction-tuned models — raises questions about whether architectural memory advantages compound with fine-tuning or are specific to the pre-training evaluation regime.

---

## Summary Assessment

Titans makes a credible case that gradient-based neural memory is a superior alternative to fixed-size state compression for long-context sequence modeling, both theoretically (expressivity beyond TC0, generalization of prior forgetting mechanisms) and empirically (consistent benchmark improvements, 2M+ context scaling). The surprise-with-momentum design is biologically motivated, well-ablated, and cleanly connected to prior work.

The primary open question is scale. Everything demonstrated here is at 760M parameters and 4K training context. Whether the architectural advantages persist at frontier scale — where Transformer infrastructure advantages, training stability at long context, and instruction-following quality become critical — remains entirely unknown. The throughput gap relative to optimized SSM implementations is a real deployment concern until custom kernels exist.

The most durable contribution may be the conceptual framework: decomposing sequence memory into persistent (task-level), long-term (learned, surprise-driven), and short-term (attentive) components, with the memory module updating via gradient descent at inference time. This framing is likely to influence [[themes/model_architecture|architecture design]] beyond the specific Titans instantiation.

## Key Concepts

- [[entities/babilong-benchmark|BABILong benchmark]]
- [[entities/delta-rule|Delta Rule]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/linear-attention|Linear Attention]]
- [[entities/sliding-window-attention|Sliding Window Attention]]
- [[entities/transformer|Transformer++]]
