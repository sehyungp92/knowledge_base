---
type: source
title: 'Nested Learning: The Illusion of Deep Learning Architecture'
source_id: 01KKT3NJ4Y51SX78R5M5XTFGQV
source_type: paper
authors: []
published_at: '2025-12-02 00:00:00'
theme_ids:
- continual_learning
- in_context_and_meta_learning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Nested Learning: The Illusion of Deep Learning Architecture

> This paper proposes **Nested Learning (NL)**, a unifying theoretical paradigm that reframes all major components of deep learning — architectures, optimizers, in-context learning, and continual learning — as instances of nested associative memory systems operating at different timescales. From this lens, the paper derives new optimizers (Delta Gradient Descent, M3), a self-modifying sequence model (Self-Referential Titans), a multi-frequency memory architecture (Continuum Memory System), and a combined continual learning module (Hope) that achieves state-of-the-art among attention-free models while reducing catastrophic forgetting.

**Authors:** Behrouz et al.
**Published:** 2025-12-02
**Type:** paper
**URL:** https://abehrouz.github.io/files/NL.pdf

---

## Core Argument

The prevailing view of deep neural networks as flat stacks of parametric layers obscures a hidden design axis: **update frequency**. The paper argues that architectures and optimizers are not independent choices but tightly coupled components of a single nested optimization system. When viewed through this lens:

- Attention mechanisms are non-parametric solutions to regression objectives on tokens, updating at frequency ∞
- MLP blocks are associative memories updated at frequency 1/|dataset| during pretraining
- Popular optimizers (Adam, SGD+momentum, AdaGrad, Muon, Shampoo) are all instances of **Nested Systems of Associative Memories (NSAM)** optimized by gradient descent
- Modern sequence architectures (softmax attention, linear attention, DeltaNet, RWKV) differ not in kind but in the objective they solve and the timescale at which they operate

The headline claim — that deep learning architecture is an "illusion" — means that apparent heterogeneity between attention, RNNs, and MLPs dissolves under NL's framework: all reduce to feedforward networks operating at different nested levels with different objectives.

---

## Theoretical Contributions

### Optimizers as Associative Memories

The paper formally shows that all major gradient-based optimizers — RMSProp, SignSGD, NAdam, AMSGrad, RAdam, Lion, Shampoo, SOAP, AdaGrad — can be reformulated as associative memories that aim to compress gradients. Notably, **Adam is proven to be the optimal associative memory** with respect to an element-wise L2 regression objective on gradients.

This unification is more than aesthetic: it exposes a fundamental limitation of standard momentum. With β=0.9, only the last ~43 gradient steps contribute 99% of the momentum state, meaning the optimizer has no effective memory of the broader loss landscape. Standard momentum acts as a low-pass filter — smoothing without selective retrieval — and cannot recover historically relevant gradient subspace information needed for long-horizon learning.

From this diagnosis, the paper derives:

- **Delta Gradient Descent (DGD):** extends standard GD with an L2 regression loss objective for the associative memory update, yielding a closed-form rule via Sherman-Morrison. Unlike standard GD, DGD's update depends on both the current input *and* the current network weight state, capturing inter-sample dependencies without assuming i.i.d. inputs — important for token sequences where this assumption is structurally violated.
- **Delta Momentum:** a momentum variant with gradient-dependent weight decay that converges faster on time-varying curvature by decaying or stopping when momentum becomes misaligned with the current gradient.
- **Multi-scale Momentum Muon (M3):** multiple momentum terms encoding multi-frequency gradient compression, outperforming both AdamW and Muon on ViT pretraining on ImageNet-21K.

### Architectures as Optimization Levels

Under NL, the familiar Transformer/RNN/MLP taxonomy is replaced by a classification based on update frequency and optimization objective. Softmax attention solves a non-parametric regression at every token; linear attention solves a cheaper variant; deep memory modules like Titans introduce a parametric middle level. The key insight: stacking more transformer layers does not necessarily increase computational depth (Merrill et al. 2022; Sanford et al. 2024), and parameter capacity of some architecture classes shows marginal improvement with increasing depth or width.

This implies that **the ability to fast-adapt, continually learn, or generalize out-of-distribution does not improve with layer stacking** — it requires a fundamentally different design principle: multiple nested levels at different timescales.

---

## Architectural Contributions

### Self-Referential Titans

A sequence model in which the projection matrices (keys, values, queries, learning rates, forget gates) are themselves adaptive memories updated in-context. The model generates its own latent values and modifies its key/value projections during inference — a form of self-modification. Training uses a chunk-wise parallel algorithm compatible with existing sequence-parallel infrastructure.

**Known limitation:** the current design shares keys and values across all memory components and lacks full self-modification where the model changes its own learning process rather than just its weights.

### Continuum Memory System (CMS)

Rather than the binary long-term/short-term memory distinction, CMS generalizes memory into a continuous spectrum of update frequencies. A chain of MLP blocks is trained at different frequencies; when one level forgets, the knowledge may still reside in adjacent levels, enabling **partial knowledge recovery** via multi-level backpropagation loops.

Crucially, pre-trained Transformer MLP blocks can initialize CMS levels via ad-hoc level stacking, allowing continual learning to be grafted onto existing models through continued pretraining without full retraining.

### Hope

Hope combines Self-Referential Titans (high-frequency, expressive learning rule, small capacity) with CMS (lower-frequency, simpler learning rule, large capacity) and uses DGD as its internal optimizer — motivated specifically by the token correlation problem that violates standard GD's i.i.d. assumption. Average per-step parameter update cost is O(1/f̂ × L_layer/5 × d²_in).

---

## Empirical Results

### Language Modeling and Reasoning

Hope outperforms all attention-free baselines and Transformers on language modeling perplexity and common-sense reasoning at both evaluated scales:

| Model | WikiText PPL (760M/30B) | Avg CSR (760M) | WikiText PPL (1.3B/100B) | Avg CSR (1.3B) |
|---|---|---|---|---|
| Hope | 18.68 | 52.28% | 14.39 | 58.04% |
| Titans | 20.08 | 51.68% | 15.60 | 56.82% |
| Transformer++ | 24.18 | — | 17.92 | — |

Hope also shows **higher performance gain from parameter scaling** than other attention-free models.

### Formal Language Recognition

Hope achieves perfect scores on all formal language recognition tasks — including non-star-free regular, counter, parallel, and parity languages — where Transformers score near zero. This directly exposes Transformers' structural limitation on non-parallelizable tasks requiring true recurrence.

### Long-Context

On BABILong, Hope maintains competitive performance at **10M token context length** due to CMS, where GPT-4, GPT-4o-mini, and competing small models fail or degrade sharply. However: *all small models including Hope drop significantly in performance without fine-tuning at this scale* — 10M token compression requires sufficient capacity in addition to architectural memory management.

### Continual Learning

On class-incremental text classification (CLINC, Banking, DBpedia) using Llama-3 as the backbone, Hope-enhanced models outperform ICL, EWC, and InCA (which uses an external learner). On the Continual Translation of Novel Languages (CTNL) task — sequentially learning Manchu and Kalamang — Hope's multi-level memory substantially reduces catastrophic forgetting while vanilla ICL shows dramatic performance collapse.

### Ablations

All components of Hope (DGD, momentum, weight decay, CMS, inner projections for k and v) contribute positively. The removal of **inner projection for v** causes the largest single degradation: perplexity rises from 12.24 to 13.90 and average accuracy drops from 58.1% to 55.1% — indicating a brittle dependence on this one architectural element.

---

## Limitations and Open Questions

### Theoretical Limitations

- The DGD derivation requires normalized inputs (‖x_t‖₂ = λ), restricting applicability to architectures with normalization layers.
- The associative memory reformulation of optimizers is a purely theoretical framework with no direct empirical evidence that the *perspective itself* yields training improvements — only that new optimizers *derived from* the perspective do.
- The claim that architecture and optimizer must be co-designed is logically compelling but lacks systematic empirical evidence across architectures.

### Scale and Generalization

- Hope is validated only at 760M and 1.3B parameters on 30B–100B tokens. **There is no evidence of behavior at frontier scales** (tens or hundreds of billions of parameters). This is the central open question for the framework's practical significance.
- Hope has **higher memory usage** than methods like Cartridges, making compute-controlled comparisons infeasible — a meaningful caveat for claims about efficiency.
- Continual learning results are validated on specific empirically-studied tasks; generalization to arbitrary non-stationary distributions is unverified.

### Catastrophic Forgetting Is Not Solved

The paper is candid: **catastrophic forgetting is a fundamental consequence of compression**, not an architectural accident. Finite network capacity forces forgetting to retain room for new information. CMS reduces its severity through multi-level knowledge recovery, but does not eliminate it. This is acknowledged as potentially a 5+ year horizon problem.

### Attention-Free vs. Transformer Trade-offs

- On in-context recall, Transformers still outperform Hope — the gap is narrowed but not closed.
- Hope-Attention shows inconsistent improvements on needle-in-a-haystack tasks, with mixed or slightly worse results on S-NIAH-3 (UUID retrieval), suggesting CMS benefits are not universal across retrieval task types.
- M3 is slower than Muon due to maintaining multiple momentum states, and may suffer from significant computational overhead at larger scales.

---

## Connections to the Landscape

### Bottlenecks Addressed

This paper directly addresses several bottlenecks in the [[themes/continual_learning|continual learning]] and [[themes/model_architecture|model architecture]] landscapes:

- **Static LLM weights after deployment** — CMS and Hope demonstrate a credible path toward architectures that can acquire new knowledge post-deployment, moving the horizon from "structurally impossible" to "demonstrated at 1.3B scale."
- **Optimizer memory capacity** — M3 and Delta Momentum directly extend the effective gradient memory horizon beyond the ~43-step limit of standard EMA momentum.
- **Transformer state tracking failures** — Hope's perfect scores on formal language tasks validate what theory predicts and quantify the gap in a concrete benchmark.
- **Fragmented optimizer theory** — the associative memory unification provides the first principled cross-optimizer theoretical framework, though its practical payoff depends on future architecture-specific optimizer work.

### Open Bottlenecks Exposed

- **Architecture-optimizer co-design** at frontier scales: the NL framework implies that the current practice of applying AdamW uniformly to all architectures is suboptimal, but the practical magnitude of this cost is unknown.
- **Multi-timescale update mechanisms at scale**: CMS's compute and memory overhead makes scaling to 7B+ parameters an open engineering problem.
- **Global loss landscape understanding**: even with M3, no optimizer demonstrated here captures truly global landscape information — the compression capacity is improved but the fundamental EMA structure remains.

### Theme Connections

- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]]: The NL framework formally connects ICL to nested optimization, positioning it as a non-parametric solution to a specific regression objective rather than an emergent mystery.
- [[themes/test_time_learning|Test-Time Learning]]: Self-Referential Titans and CMS are architectural implementations of test-time learning — the model modifies its own weights during inference without external supervision.
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]: The paper challenges naive scaling assumptions: more layers do not necessarily increase computational depth, and multi-timescale training is predicted to outperform uniform-update-rate pretraining.
- [[themes/post_training_methods|Post-Training Methods]]: Ad-hoc level stacking using pre-trained Transformer MLP blocks as CMS initializers is a novel post-training adaptation strategy that does not require full retraining.

---

## Summary Judgment

Nested Learning is a theoretically ambitious unification that succeeds at the level of framework design and proof-of-concept demonstration. Its core insight — that update frequency is the missing design dimension in deep learning — is well-motivated and generates concrete, testable predictions. The Hope architecture's results at 760M–1.3B scale are strong and multi-faceted: best-in-class on formal languages, long-context, and continual learning, while competitive on language modeling.

The central question the paper cannot yet answer is whether these results hold at frontier scales. The memory and compute overhead of CMS and self-referential mechanisms are real obstacles. And the paper's most honest acknowledgment — that catastrophic forgetting is a consequence of compression, not architecture — is also a reminder that the framework describes the problem with unusual clarity without solving it.

For a field that has largely treated architecture and optimizer as independent variables, the NL paradigm offers a productive reorientation regardless of whether Hope itself scales.

## Key Concepts

- [[entities/associative-memory|Associative memory]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/delta-rule|Delta Rule]]
- [[entities/elastic-weight-consolidation|Elastic Weight Consolidation]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/linear-attention|Linear Attention]]
- [[entities/muon-optimizer|Muon Optimizer]]
