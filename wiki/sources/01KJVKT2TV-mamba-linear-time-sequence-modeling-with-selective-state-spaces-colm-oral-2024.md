---
type: source
title: 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces (COLM Oral
  2024)'
source_id: 01KJVKT2TVK6WMW0WAEW1GQAD8
source_type: video
authors: []
published_at: '2024-10-16 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- pretraining_and_scaling
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Mamba: Linear-Time Sequence Modeling with Selective State Spaces (COLM Oral 2024)

State-space models with three targeted innovations, namely large state expansion, input-dependent selective updates, and hardware-efficient algorithms, close the long-standing performance gap between recurrent architectures and attention-based Transformers. This talk by Albert Gu situates Mamba within a unified framework of the "autoregressive state," explains why earlier SSMs fell short, details the architectural choices that make Mamba competitive, and introduces the hybrid attention-SSM paradigm that has since become a practical path to both quality and efficiency gains.

**Authors:** Albert Gu
**Published:** 2024-10-16
**Type:** video (COLM Oral)

---

## The Autoregressive State: A Unifying Lens

Any sequence model, regardless of architecture, can be characterized by its *autoregressive state*: what information the model retains between time steps. This framing cleanly separates the trade-space that Mamba is designed to navigate.

**Recurrent models (RNNs, SSMs)** maintain a fixed-size hidden state. No matter how long the context, time and memory per generation step remain constant, and cost scales linearly over a full sequence. The penalty is compression: the entire history must be squeezed into that vector, which creates a hard ceiling on recall for information-dense or retrieval-heavy tasks.

**Attention** sits at the opposite extreme. It retains a full KV cache of all past tokens, enabling direct sparse comparisons with any point in history. The cost is the famous quadratic scaling: inference time grows linearly with cache size, and aggregated over a sequence this becomes O(T²).

The central insight is that neither extreme is optimal. Mamba's goal is to control *what goes into the state* rather than accepting either full compression or no compression.

---

## What Makes Mamba Work

Three ingredients differentiate Mamba from older SSMs like S4:

### 1. State Expansion
The hidden state is blown up by a controllable factor N (typically 10–100x the input dimension), giving the model far more capacity to hold history. Crucially, this large state is never explicitly materialized in slow GPU HBM memory; it lives in fast SRAM, keeping the expansion computationally practical. This is analogous to how FlashAttention exploits the GPU memory hierarchy to make attention efficient in practice.

### 2. Selective State Updates (Input-Dependent Transitions)
In classical SSMs, the state transition matrices are fixed regardless of the input. Mamba makes these matrices functions of the current input, a mechanism closely related to gating in LSTMs. This selectivity allows the model to decide, at each step, what to incorporate and what to discard, giving far finer-grained control over the state contents than earlier linear recurrences.

### 3. Hardware-Aware Algorithms
Even with a large state, the model avoids materializing intermediate activations in HBM. Mamba 2 extended this by drawing an explicit connection between SSMs and attention, enabling the use of tensor cores (the specialized matrix-multiply units on modern GPUs and TPUs). The result is that Mamba achieves its efficiency gains not through theoretical complexity alone but through careful exploitation of real hardware.

---

## Capabilities

- **Linear-time inference across modalities.** Mamba achieves strong performance on language, vision, graphs, audio, and DNA with O(T) inference complexity. Industry adoption includes Microsoft, Nvidia, Mistral, TII, Zeta, and AI21. (maturity: broad_production)

- **Hybrid attention-SSM models.** Strategically combining attention layers with Mamba layers yields 2.5x faster inference on long-context tasks relative to pure Transformer baselines, while maintaining competitive quality. This shifts the design question from "Transformers or RNNs?" to "how should they be combined?" (maturity: demo)

- **Hardware-efficient SSM kernels.** Memory-hierarchy-aware algorithms enable practical scaling on modern GPU/TPU hardware. Mamba 2's tensor-core-compatible formulation closes the gap with heavily optimized attention kernels. (maturity: narrow_production)

- **Distillation from Transformers.** Strong Transformer models such as Llama can be distilled into Mamba-like architectures while preserving much of their performance, offering a practical upgrade path. (maturity: demo)

---

## Limitations and Open Questions

### Compression as a Structural Tradeoff
The fixed-size autoregressive state means that recurrent models perform *very strong compression* of context history. This is both their efficiency advantage and their core limitation: tasks requiring fine-grained retrieval over long contexts remain challenging. Whether this tradeoff is fundamental or can be engineered away through better state update functions is an open question.

> "Compression is a feature, but sometimes it can lead to lower retrieval performance. So is it a bug or a feature?" (severity: significant, trajectory: improving)

### Data-Dependent Complexity
The appropriate model complexity, quadratic or linear, appears to depend on the information density of the data distribution. High-redundancy data may need only linear models; information-dense data may require quadratic attention. The relationship between data statistics and required model complexity is poorly theorized.

> "The complexity of your model might really depend on the data and the distribution." (severity: significant, trajectory: unclear)

### Why Do Hybrid Models Work?
Hybrid attention-SSM models outperform pure variants, but the mechanism is not understood. It is unclear whether performance comes from complementary capacity (attention covers what SSMs compress away), redundancy reduction, or some other factor. Without this understanding, hybrid architecture design remains empirical rather than principled. (severity: minor, trajectory: improving)

### Distributed Training and Inference Infrastructure
Efficient distributed training strategies for SSMs and inference optimization tooling (e.g., speculative decoding analogues) remain unsolved engineering problems compared to the mature Transformer ecosystem. (severity: significant, trajectory: improving)

### Cross-Modality Compression Strategies
Whether high-resolution modalities such as audio and video require fundamentally different compression ratios or state expansion strategies than language is uncharacterized. Relative information density across modalities is not yet well understood. (severity: minor, trajectory: unclear)

### Adaptive Computation
How to adjust model capacity or search depth based on problem difficulty at runtime, an idea analogous to test-time compute scaling in Transformers, remains an open research direction for the SSM family. (severity: significant, trajectory: improving)

---

## Breakthroughs

**Mamba overcomes the historical RNN performance ceiling.** Prior to Mamba, linear recurrent models were understood to trade quality for efficiency in a way that made them non-competitive with Transformers on language. The combination of state expansion, selectivity, and hardware awareness overturns this assumption. (significance: major)

**Hybrid models establish a new architectural paradigm.** The hybrid attention-SSM result demonstrates that the choice between Transformers and recurrent models is not binary. This opens a design space that was previously unexplored at scale, with measurable efficiency gains already demonstrated in production-scale settings. (significance: notable)

---

## Active Bottleneck

[[themes/model_architecture|Model Architecture]] research is currently blocked on understanding the *principles* governing hybrid attention-SSM performance: what ratio of attention to linear layers is optimal, and why. Without this, hybrid architecture design is driven by empirical search rather than mechanistic insight. This bottleneck is expected to resolve on a 1-2 year horizon as interpretability methods improve and more controlled experiments accumulate.

---

## Themes

- [[themes/transformer_alternatives|Transformer Alternatives]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/long_context_and_attention|Long Context and Attention]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]

---

## Related Claims (Selected)

| # | Claim | Source Snippet |
|---|-------|---------------|
| 6 | Recurrent models scale linearly per step regardless of context length | "because it has a fixed size vector when you're doing autoregressive generation..." |
| 10 | Three key Mamba ingredients: state size, selectivity, hardware efficiency | "at a high level to understand Mamba there are three key ingredients..." |
| 11 | Selectivity is closely related to LSTM gating mechanisms | "the transition functions of the SSM were made to be dependent on the input..." |
| 12 | Large state kept in GPU SRAM, not HBM, for efficiency | "we don't have to materialize it in GPU HBM instead we keep it in SRAM..." |
| 13 | Mamba 2 enables tensor core usage via SSM-attention connection | "by drawing the connection between state space and attention we have figured out..." |

## Key Concepts

- [[entities/flash-attention|Flash Attention]]
- [[entities/flashattention|FlashAttention]]
- [[entities/kv-cache|KV Cache]]
- [[entities/state-space-model|State Space Model]]
