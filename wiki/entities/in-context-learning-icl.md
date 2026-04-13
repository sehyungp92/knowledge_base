---
type: entity
title: in-context learning (ICL)
entity_type: theory
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- in_context_and_meta_learning
- interpretability
- long_context_and_attention
- mechanistic_interpretability
- model_architecture
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0006272249962080167
staleness: 0.0
status: active
tags: []
---
# in-context learning (ICL)

> In-context learning (ICL) is the ability of large language models to adapt their behavior at inference time by conditioning on examples or instructions provided in the prompt, without any modification to model weights. It sits at the intersection of mechanistic interpretability, test-time learning, and architecture research: understanding *why* it works has revealed deep connections between attention, gradient descent, and implicit weight updates, while its limitations have motivated an entire generation of alternative architectures and training methods.

**Type:** theory
**Themes:** [[themes/benchmark_design|Benchmark Design]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]], [[themes/interpretability|Interpretability]], [[themes/long_context_and_attention|Long Context and Attention]], [[themes/mechanistic_interpretability|Mechanistic Interpretability]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_learning|Test-Time Learning]], [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Overview

In-context learning describes the capacity of a language model to learn new patterns from examples placed in the input prompt, with zero weight updates, even when those patterns were absent during training. What initially looked like an emergent empirical curiosity has, through mechanistic analysis, revealed itself to be a precise and mathematically tractable process — one that turns out to mirror classical gradient descent in a surprisingly exact way.

---

## Mechanistic Structure: Implicit Weight Updates

The most clarifying result in this space comes from Learning without training: The implicit dynamics of in-context learning, which shows that a transformer block implicitly transforms its context into a low-rank weight update of its MLP layer. More precisely, the implicit update takes the form of a rank-1 matrix: the product of a column vector `WδAx(Y)` and a row vector `A(C\Y,x)^T`. This is not an approximation; the formula is exact. The output of the contextual block with the full context is precisely equivalent to the output with reduced context and correspondingly modified weights.

This rank-1 structure has a clean interpretation: each context token contributes a rank-1 correction to the model's effective weights, and these corrections accumulate token by token. When a context token has no marginal effect on the contextual block output (i.e., the attention pattern is unchanged by its presence), its corresponding implicit weight update vanishes entirely. The iterative accumulation of these updates corresponds to stochastic gradient descent with a learning rate of `1/||A(x)||^2`. ICL, in this view, is gradient descent happening inside the forward pass.

---

## Scaling Limitations and the Architecture Bottleneck

Despite its elegance, standard softmax attention scales quadratically with sequence length: the `QK^T` matrix must be computed over all token pairs, so memory and compute grow as `O(n^2)`. This is a hard structural constraint. As context lengths grow, the cost of ICL via attention becomes prohibitive, which is precisely what motivated the test-time training (TTT) line of work described in Learning to (Learn at Test Time): RNNs with Expressive Hidden States.

Standard RNNs avoid the quadratic bottleneck by compressing context into a fixed-size hidden state, but they introduce a different failure mode: sequential computation. Each hidden state update depends on the previous one, so training cannot be parallelized across tokens, and GPU utilization collapses.

---

## Test-Time Training as Generalized ICL

TTT proposes a structural synthesis. Rather than using attention to implicitly perform gradient descent over the context, TTT makes the gradient descent explicit and hardware-efficient. The hidden state `W` is a small model (a matrix or a small MLP), and at each token the inner loop updates `W` via gradient descent on a learned self-supervised loss: a reconstruction loss over corrupted tokens. The outer loop learns the main next-token prediction objective, including learning the inner loss function itself. No model parameters (feed-forward weights, projection matrices, embeddings) are updated during inference; only the hidden state changes.

This framing makes ICL a special case of a broader test-time learning paradigm. Where standard attention performs an implicit, exact, rank-1 update per context token, TTT performs an explicit, approximate, but architecturally flexible update. The tradeoff is expressivity versus interpretability.

The practical stakes are real: deep learning with test-time fine-tuning reached 58% on the ARC-AGI private test set in 2024, according to DON'T THROW THE BABY OUT WITH THE BATHWATER: HOW, making it the strongest known result on a benchmark specifically designed to probe in-context generalization to novel patterns.

---

## Open Questions and Limitations

Several structural tensions remain unresolved.

The rank-1 update result is exact but limited in scope: it characterizes what a single transformer block does, not what the full multi-layer model does across diverse tasks. Whether the cumulative effect of many rank-1 updates across layers composes into something resembling task learning in any deep sense is still unclear.

The SGD-with-learning-rate interpretation raises questions about sample efficiency and stability. ICL does not perform multiple gradient steps over the same examples; each token is processed once. This is a severe constraint compared to standard fine-tuning, and may explain why ICL fails on tasks requiring sustained compositional reasoning.

TTT resolves the parallelism problem for the inner loop during training (by processing a fixed window of tokens in parallel), but the expressivity of the hidden state and the choice of self-supervised loss introduce new degrees of freedom that are poorly understood. The learned inner loss is trained end-to-end, which means its semantics are opaque.

More broadly, neither the implicit-update framework nor TTT fully explains when ICL works and when it fails. The ARC-AGI benchmark result suggests that for certain structured generalization tasks, explicit test-time fine-tuning vastly outperforms pure in-context prompting, but the conditions that determine which regime dominates remain an open research question.

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
