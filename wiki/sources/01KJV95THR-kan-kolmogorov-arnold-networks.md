---
type: source
title: 'KAN: Kolmogorov-Arnold Networks'
source_id: 01KJV95THR703F5DVYH4ERZZAJ
source_type: paper
authors:
- Ziming Liu
- Yixuan Wang
- Sachin Vaidya
- Fabian Ruehle
- James Halverson
- Marin Soljačić
- Thomas Y. Hou
- Max Tegmark
published_at: '2024-04-30 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- interpretability
- mechanistic_interpretability
- model_architecture
- scientific_and_medical_ai
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# KAN: Kolmogorov-Arnold Networks

KAN introduces a neural network architecture that replaces every scalar weight in an MLP with a learnable univariate spline function placed on edges rather than nodes, grounding this design in the Kolmogorov-Arnold representation theorem and generalizing it to arbitrary depth. The paper demonstrates that this architecture achieves dramatically faster neural scaling laws (empirical exponent α≈4 vs. α≈1 for MLPs), superior parameter efficiency on small-scale scientific tasks, and a new mode of human-in-the-loop symbolic discovery — while being honest about the hard limitations that currently confine it to niche scientific settings.

**Authors:** Ziming Liu, Yixuan Wang, Sachin Vaidya, Fabian Ruehle, James Halverson, Marin Soljačić, Thomas Y. Hou, Max Tegmark
**Published:** 2024-04-30
**Type:** paper

---

## Motivation

The dominant neural building block — the MLP — places fixed nonlinear activations on nodes and learns only linear weights between them. This creates a structural tension: MLPs avoid the curse of dimensionality through feature learning but cannot efficiently optimize univariate functions, while spline methods are accurate in low dimensions but cannot exploit compositional structure and scale catastrophically with input dimensionality. Neither approach alone is adequate for structured scientific tasks.

The [[themes/transformer_alternatives|transformer alternatives]] angle is pointed: in transformers, MLPs consume almost all non-embedding parameters yet remain the least interpretable component, typically requiring post-hoc analysis to understand at all. The MLP scaling exponent α≈1 under standard theory improves slowly and plateaus quickly, limiting how much can be gained by scaling.

The Kolmogorov-Arnold representation theorem had been "sentenced to death" in machine learning — theoretically sound but practically dismissed because its original depth-2, width-(2n+1) construction produces potentially non-smooth, even fractal inner functions, and prior implementations predated backpropagation.

---

## Proposed Architecture

KANs are built from the Kolmogorov-Arnold representation theorem:

> f(x) = Σ Φ_q(Σ ϕ_{q,p}(x_p))

Rather than treating this as a fixed two-layer construction, the paper defines a **KAN layer** as a matrix of 1D functions {ϕ_{q,p}} that can be composed to arbitrary depth. Nodes perform only summation with no nonlinearity — all learned transformation happens on the edges.

Each activation function is parametrized as a residual combination:

> ϕ(x) = w_b · silu(x) + w_s · spline(x)

with Xavier-initialized w_b and near-zero initial spline coefficients. Spline grids are updated on the fly to track activation ranges during training.

A KAN of depth L, uniform width N, and spline order k on G grid intervals has O(N²LG) parameters — compare O(N²L) for an equivalent MLP.

### Key Mechanisms

**Grid extension.** A coarse-grid KAN is trained first, then spline grids are refined by least-squares fitting without full retraining — progressive refinement analogous to multigrid methods, unavailable to MLPs. This introduces a new scaling axis (grid resolution) orthogonal to width and depth.

**Symbolification.** A learned spline can be fitted to a candidate symbolic form y ≈ cf(ax+b)+d via grid search and linear regression. This enables a human-in-the-loop pipeline: train → sparsify → prune → symbolify → interpret.

**Sparsity pipeline.** L1 regularization on activation functions plus entropy regularization drives sparse, prunable networks whose structure can be visualized with magnitude-proportional edge transparency.

---

## Results

### Scaling Laws

KANs achieve a theoretical scaling exponent α = k+1 = 4 (cubic splines), empirically saturated on synthetic datasets. MLPs across all depths (2–5 layers) plateau far above KAN error at the same parameter count — the gap widens as parameters increase rather than closing.

On five toy datasets with known KA representations (Bessel function, exp(sin(πx)+y²), xy, a 100-dimensional generalized additive function, and a four-variable nested composition), KANs follow the N⁻⁴ prediction while all MLP variants plateau.

### Parameter Efficiency

On knot theory signature classification (DeepMind dataset): a [17,1,14] KAN with ~200 parameters achieves **81.6% test accuracy** versus DeepMind's 4-layer width-300 MLP with ~300,000 parameters at 78.0% — roughly **1500× parameter efficiency improvement**.

For PDE solving (Poisson equation, PINN framework): a width-10 two-layer KAN achieves L2 error ~10⁻⁷ while a width-100 four-layer MLP reaches only ~10⁻⁵ — **100× accuracy improvement with 100× fewer parameters**.

### Scientific Discovery

For the Generalized Aubry-André Model (GAAM), KAN-assisted analysis achieves 99.0% accuracy with a formula closely matching the ground truth αE + 2λ − 2 = 0. For the Modified Aubry-André Model (MAAM), human-KAN collaboration progressively simplifies an auto-generated formula toward the known analytic mobility edge E + exp(p) − λcosh(p) = 0, reaching 95.4–97.7% accuracy.

In unsupervised mode on knot invariant data, KANs independently rediscover three known mathematical relations across 200 training runs with different seeds, without any manual input/output partitioning.

### Continual Learning

KANs exhibit local plasticity through the locality of B-spline bases: new data modifies only nearby spline coefficients, leaving previously learned regions intact. MLPs remodel the entire function space on new data exposure. (See limitations for significant caveats on this result.)

---

## Capabilities

These capabilities are currently **research-only** — none have been validated at production scale or outside small scientific datasets.

- Superior accuracy-to-parameter ratios over MLPs on function fitting, with empirical scaling exponent α≈4 vs. MLPs' slower empirical scaling
- Interactive human-AI symbolic regression: visualize learned activation functions, prune, set symbolic forms to rediscover mathematical and physical laws
- ~1500× parameter efficiency on knot theory classification vs. a large MLP baseline
- Natural resistance to catastrophic forgetting via local spline plasticity (restricted to 1D demonstrations — see limitations)
- Progressive accuracy refinement via grid extension without full retraining
- 100× lower PDE solving error with 100× fewer parameters on Poisson equation
- Unsupervised structural relation discovery without manual variable partitioning

---

## Limitations

The paper is unusually candid about its failure modes. Several limitations are fundamental rather than engineering gaps.

**Computational cost.** KAN training is approximately **10× slower than equivalent MLPs**. This is a hard block on latency-sensitive or large-scale applications and prevents integration into standard GPU-accelerated deep learning pipelines. The authors flag this directly and offer no near-term resolution. (severity: significant)

**Scale gap.** All advantages are demonstrated exclusively on small-scale AI+Science tasks. Performance on large-scale NLP, language modeling, vision, or LLM-scale tasks is entirely untested. The headline results cannot be extrapolated to the settings where MLP alternatives would matter most. (severity: significant)

**No deep KA theorem.** There is no theoretical generalization of the Kolmogorov-Arnold theorem for networks deeper than 2 layers. Deep KANs are empirically motivated but **formally unjustified** — the paper explicitly acknowledges this gap and offers no proof. (severity: significant)

**Compositional structure dependency.** KANs only beat the curse of dimensionality when smooth Kolmogorov-Arnold representations exist for the target function. Without this structural property, COD scaling is not avoided — and verifying that a function admits a compact KA representation before training is generally impossible. (severity: significant)

**Niche-specific advantage.** KANs show **no accuracy advantage over MLPs on the Feynman physics dataset** — smooth, monotonic function dependencies eliminate KAN's structural advantage, revealing the approach is not universally superior even within scientific domains. (severity: significant)

**Continual learning is a toy result.** Local spline plasticity has only been demonstrated on a trivially simple 1D task. Generalization to high-dimensional settings is explicitly uncertain because 'locality' has no principled definition in high-dimensional input spaces. (severity: significant)

**Optimizer and training pipeline gap.** All experiments use LBFGS on small datasets. No experiments with Adam, SGD, minibatch training, or modern regularization — KAN performance in standard deep learning pipelines is completely unknown. (severity: significant)

**Symbolic discovery requires hand-crafting.** Auto-discovered formulas require additional inductive biases (e.g., assuming Padé representation, manual division) to approach the simplicity of formulas derived by human scientists. (severity: minor)

**Non-deterministic relation discovery.** Unsupervised discovery is seed-dependent with no principled method to enumerate the complete set of hidden relations — no coverage guarantee exists. (severity: significant)

**Grid scaling ceiling.** Optimization fails at very fine grid resolutions (G≈1000): training slows dramatically and LBFGS loss landscapes become pathological, suggesting a hard ceiling on grid-based scaling. (severity: minor)

**Architecture search cost.** Correct KAN shape must be known or discoverable — performance with wrong shapes degrades substantially, and auto-discovery via pruning is computationally expensive and may yield suboptimal architectures. (severity: significant)

---

## Open Questions

- Can KANs be integrated into transformers ("KANsformers") to improve the interpretability and accuracy of the MLP sublayers that dominate non-embedding parameters? The paper proposes this but provides no implementation.
- Does a "deep Kolmogorov-Arnold theorem" exist? Can one be proved, and would it constrain or enable architectural choices?
- Do the scaling law advantages hold under Adam/SGD with minibatches, or are they LBFGS artifacts?
- Can the locality-based continual learning advantage be extended beyond 1D — and if so, how is locality defined in high-dimensional input spaces?
- Can unsupervised relation discovery be made systematic rather than seed-dependent, enabling complete enumeration of structural relationships?

---

## Bottlenecks Addressed / Created

This paper is most relevant to the [[themes/model_architecture|model architecture]] and [[themes/interpretability|interpretability]] themes, and intersects with [[themes/ai_for_scientific_discovery|AI for scientific discovery]] and [[themes/scientific_and_medical_ai|scientific and medical AI]].

**Bottlenecks identified (not resolved):**

- **KAN training speed** (10× slower than MLPs) blocks practical adoption outside small-scale scientific tasks
- **Absence of a generalized KA theorem for depth > 2** blocks principled theoretical foundations and prevents formal guarantees about expressive capacity (horizon: 3–5 years)
- **Non-systematic unsupervised discovery** prevents reliable hypothesis enumeration in scientific datasets (horizon: 1–2 years)
- **Undefined locality in high dimensions** prevents the continual learning advantage from scaling beyond 1D toy tasks (horizon: 1–2 years)

**Breakthrough claimed:**

KAN is flagged as a *notable* architectural breakthrough — the first practical revival of the Kolmogorov-Arnold theorem as a viable MLP alternative, achieved by generalizing the original depth-2 formulation, introducing grid extension as a new scaling axis, and demonstrating empirical scaling exponents far beyond MLP theory.

---

## Relationship to Themes

- [[themes/model_architecture|Model Architecture]] — Core contribution: a new neural building block replacing fixed node activations with learnable edge splines
- [[themes/interpretability|Interpretability]] — Symbolic discovery pipeline, prunable sparse networks, human-in-the-loop refinement
- [[themes/mechanistic_interpretability|Mechanistic Interpretability]] — Direct visualization of learned activation functions; no need for post-hoc analysis tools
- [[themes/transformer_alternatives|Transformer Alternatives]] — Proposed as a replacement for MLP sublayers in transformers; not yet implemented
- [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]] — Primary validation domain; rediscovery of mobility edge laws and knot invariant relations
- [[themes/scientific_and_medical_ai|Scientific and Medical AI]] — Demonstrated on physics (GAAM, MAAM, PDE solving) and mathematics (knot theory)

## Key Concepts

- [[entities/neural-scaling-laws|Neural Scaling Laws]]
