---
type: source
title: 'Learning to (Learn at Test Time): RNNs with Expressive Hidden States'
source_id: 01KJVM69GCN7QYSPPE2KFMZ0Y5
source_type: video
authors: []
published_at: '2024-07-12 00:00:00'
theme_ids:
- in_context_and_meta_learning
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
# Learning to (Learn at Test Time): RNNs with Expressive Hidden States

> This paper introduces Test-Time Training (TTT), a meta-learning approach that replaces the attention mechanism in Transformers with an RNN whose hidden state is updated via gradient descent on a learned self-supervised reconstruction loss. By having an outer loop learn the inner loop's loss function, TTT achieves linear-complexity sequence modeling with expressiveness that matches or exceeds softmax attention — including better in-context learning than Transformers with full context access.

**Authors:** Yu Sun et al.
**Published:** 2024-07-12
**Type:** Video (paper walkthrough)
**Source:** [YouTube](https://www.youtube.com/watch?v=I9Ghw2Z7Gqk&t=105s)

---

## The Problem: The Expressiveness-Efficiency Tradeoff

Standard softmax attention is quadratic in sequence length. The culprit is the QK^T matrix: the softmax forces full materialisation of this matrix, causing memory to scale quadratically with context. Linear attention approaches address this in two ways — remove the softmax, or replace attention entirely with a new mechanism. TTT takes the latter path.

The natural alternative is an RNN, which processes sequences in constant memory. But RNNs have a known failure mode: the fixed-size hidden state must compress all prior context, and as sequence length grows, this compression becomes lossy. The perplexity of even the best RNN (Mamba) levels off as token index increases — the model stops benefiting from additional context. This is the core bottleneck TTT targets: [[themes/long_context_and_attention|long context and attention]].

The two failure modes of classical RNNs make this hard:
- **Without gating (sigmoid):** the hidden state accumulates an unbounded sum of tokens and diverges.
- **With sigmoid gating:** divergence is prevented but expressiveness is crushed — the sigmoid bounds the hidden state between 0 and 1, limiting how much information can be retained.

Softmax attention sidesteps this entirely: with a KV cache, the "hidden state" is every key and every value — the model has uncompressed access to the full context. TTT asks whether a fixed-size hidden state can be made expressive enough to match this.

---

## The TTT Architecture: Learning to Learn

TTT introduces a two-level [[themes/in_context_and_meta_learning|meta-learning]] structure:

- **Outer loop:** a standard Transformer processing the main next-token prediction task.
- **Inner loop:** replaces the self-attention and feed-forward layers; an RNN whose hidden state W is updated at each token via gradient descent on a learned loss.

The key insight is that the outer loop *learns the inner loop's loss function*. The inner loop is not optimising model parameters — it is only updating the hidden state W. The outer loop learns how to construct a loss signal that causes the inner loop to maintain a maximally useful hidden state for downstream prediction.

### Inner Loop: The Reconstruction Loss

At each new token, the hidden state is updated by computing the gradient of a self-supervised reconstruction loss:

- A learnable neural network f takes a corrupted token, the current token, and the current hidden state W.
- It attempts to reconstruct a down-projected version of the token.
- The gradient of this reconstruction loss with respect to W updates the hidden state.

**Why reconstruction?** Tokens that are harder to reconstruct carry more information — they generate larger gradients, causing larger updates to W. The hidden state is implicitly weighted toward informative tokens.

**Why doesn't it collapse?** The down-projection targets are parameters of the *outer* loop, not the inner loop. The inner model can only optimise W; it cannot optimise the projection matrices. The outer loop is thus incentivised to set projections that yield representations useful for next-token prediction, not for reconstruction itself. Collapse is prevented structurally.

The outer loop also learns an adaptive, data-dependent learning rate (Ada) for the inner loop's gradient steps — the step size itself is a function of the input, learned end-to-end.

### Hidden State Instantiation

The update function f can be instantiated as either:
- An **MLP** (four-times expansion and back) — equivalent to a standard Transformer feed-forward block.
- A **square weight matrix W** — a simpler linear variant.

Both are stable. The MLP variant is more expressive but more expensive.

---

## Parallelising Training

A classical RNN cannot be parallelised during training — each step depends on the previous hidden state, forcing sequential forward and backward passes that underutilise GPUs. TTT addresses this via **mini-batch gradient descent** on the inner loop updates: hidden state updates within a mini-batch are computed in parallel, then applied together.

This restores GPU parallelism, but introduces a tradeoff: larger mini-batch sizes improve throughput but degrade perplexity. The parallelisation-accuracy tradeoff is a live [[themes/model_architecture|architectural]] bottleneck — efficiency and maximum performance cannot currently be achieved simultaneously.

---

## Capabilities

| Capability | Maturity | Evidence |
|---|---|---|
| Linear-complexity RNN matching Transformer/Mamba perplexity on language modeling | Research only | Comparable perplexity on Pile; TTT levels off later than Mamba and Transformer |
| Better in-context learning than Transformers with full context access | Research only | TTT outperforms Transformer with full KV cache on in-context tasks |
| Parallelizable RNN training via mini-batch gradient descent | Research only | Demonstrated GPU-efficient training |
| Theoretical equivalence between learned-loss RNN updates and linear/self-attention | Research only | Formal derivation in the paper |

The in-context learning result is striking: a fixed-size hidden state, without access to the raw context, outperforms a Transformer that has every token available. This directly challenges the assumption that unbounded context access is necessary for strong in-context learning. See [[themes/test_time_learning|test-time learning]] for related work.

---

## Limitations and Open Questions

**Batch size / accuracy tradeoff.** The mini-batch parallelisation that makes training feasible degrades perplexity as batch size increases. There is no current solution that achieves both efficient training and optimal accuracy. *(Severity: significant, trajectory: unclear)*

**Vector vs. matrix hidden state.** TTT uses a vector hidden state, while Mamba uses a matrix. The expressiveness gap this creates is unquantified, and whether scaling the hidden state to a matrix would help is an open question. *(Severity: significant, trajectory: unclear)*

**Stability requires learnable w0.** A learnable initial hidden state is necessary for stable training; rows without it cannot train stably, despite the +0.4 perplexity cost. This is a surprising hard constraint with no clear theoretical explanation yet. *(Severity: significant, trajectory: stable)*

**Narrow evaluation.** All benchmarks are on the Pile (standard language modeling). Whether TTT's in-context learning advantage generalises to reasoning tasks, coding, or few-shot evaluation is unknown. *(Severity: significant, trajectory: unclear)*

**Backbone matters significantly.** The Mamba-based backbone outperforms the Transformer-based backbone, and the Transformer uses substantially more FLOPs. Architectural choices interact strongly with the TTT mechanism in ways not yet understood. *(Severity: significant, trajectory: unclear)*

**Loss function design is not automatic.** The outer loop must design a reconstruction loss that avoids collapse and extracts useful signal. What makes a good inner loss is not yet principled — it requires domain intuition. *(Severity: significant, trajectory: unclear)*

---

## Connections and Implications

TTT sits at the intersection of several active research fronts:

- **[[themes/transformer_alternatives|Transformer alternatives]]:** directly competes with Mamba and other linear-complexity architectures. The result that a learned-loss RNN can match Transformer perplexity while being linear in memory is a meaningful datapoint in this competition.
- **[[themes/in_context_and_meta_learning|In-context and meta-learning]]:** the outer loop learning the inner loop's loss is a clean instantiation of learning-to-learn. The in-context learning result — surpassing Transformers with full context — may have implications for how we understand what drives ICL performance.
- **[[themes/test_time_learning|Test-time learning]]:** updating the hidden state via gradient descent at each token is a form of test-time computation that goes beyond standard inference. This connects to broader questions about where learning happens and what counts as a model "parameter."
- **[[themes/post_training_methods|Post-training methods]]:** the meta-learning framing — an outer loop shaping an inner loop's learning — is structurally related to MAML-style approaches and may generalise beyond sequence modeling.

The theoretical equivalence between TTT's learned-loss updates and linear attention is notable: it suggests that what TTT is doing can be understood as a learned, adaptive linear attention mechanism, with the meta-learning providing the expressiveness that fixed linear attention kernels lack.

---

## Key Open Question

Does TTT scale? The benchmarks are on small models on the Pile. Whether the in-context learning advantage persists at scale, whether the parallelisation tradeoff becomes more or less severe, and whether the method works on tasks requiring multi-step reasoning remain entirely open. The architecture is theoretically motivated and empirically promising, but its position in the long-run [[themes/transformer_alternatives|transformer alternatives]] landscape depends on answers that do not yet exist.

## Key Concepts

- [[entities/kv-cache|KV Cache]]
- [[entities/linear-attention|Linear Attention]]
- [[entities/perplexity|Perplexity]]
- [[entities/in-context-learning-icl|in-context learning (ICL)]]
