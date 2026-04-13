---
type: entity
title: Neural Scaling Laws
entity_type: theory
theme_ids:
- ai_for_scientific_discovery
- interpretability
- mechanistic_interpretability
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0009335391565029979
staleness: 0.0
status: active
tags: []
---
# Neural Scaling Laws

Neural scaling laws describe the empirical and theoretical relationships governing how model performance improves as a function of scale — measured in parameters, data, or compute. First characterized as power-law relationships of the form ℓ ∝ N^{-α}, they have become one of the most consequential organizing principles in modern AI research, shaping architectural choices, resource allocation, and long-range predictions about capability development. Their significance lies not just in what they predict, but in what they reveal about the geometry of learning itself.

**Type:** theory
**Themes:** [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]], [[themes/interpretability|Interpretability]], [[themes/mechanistic_interpretability|Mechanistic Interpretability]], [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/representation_learning|Representation Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Overview

The canonical formulation of neural scaling laws — test loss decreasing predictably with model size as a power law — rests on deeper assumptions about how neural networks approximate functions in high-dimensional spaces. On logarithmic plots, power-law relationships appear as straight lines whose slope equals the scaling exponent, making them visually tractable and empirically testable across orders of magnitude. The theoretical underpinnings, however, are far from settled.

A central tension is between the **expressiveness** of function approximators and their **sample efficiency** in high dimensions. The Universal Approximation Theorem guarantees that sufficiently wide networks can approximate any continuous function, but crucially offers no bound on how the required neuron count N(ε) scales with error tolerance ε. In practice, N can grow exponentially with input dimension d — the curse of dimensionality (COD). This is not a failure of the theorem; it is the theorem's silence on the most practically important question.

---

## Architecture and the Scaling Exponent

Different architectural families imply different theoretical scaling exponents, and this is where recent work on KAN: Kolmogorov-Arnold Networks becomes relevant. Classical MLPs with piecewise polynomial activations of order k achieve a scaling exponent of at most α = (k+1)/d — meaning performance degrades rapidly as input dimensionality d increases. The curse of dimensionality is baked into the exponent itself.

Splines, by contrast, are highly accurate for low-dimensional functions and allow local adjustment and resolution switching. For KANs using cubic splines, the theoretical scaling exponent reaches α = 4, a substantially better rate. But splines inherit the same fundamental limitation: they cannot exploit compositional structures, so their advantages collapse in high-dimensional settings.

KANs attempt to resolve this by combining two sources of representational power. External degrees of freedom — the computational graph structure, analogous to MLP architecture — handle learning of compositional structure across multiple variables. Internal degrees of freedom — the grid points inside each spline — optimize univariate functions to high accuracy. The claim is that this separation of concerns allows KANs to sidestep the COD in the way that deep networks generally can, by decomposing high-dimensional problems into compositions of lower-dimensional ones.

Mechanistically, KANs place learnable activation functions on **edges** rather than fixed activations on **nodes**, with no linear weight matrices — every weight parameter is replaced by a univariate function parametrized as a residual combination of a SiLU basis function and a B-spline. A KAN of depth L, uniform width N, and spline order k on G grid intervals carries O(N²LG) parameters, compared to O(N²L) for an equivalent MLP. The parameter overhead is real, but the architecture enables a form of progressive refinement: a coarse-grained KAN can be extended to a finer-grained one via grid extension without retraining from scratch, directly trading compute for accuracy along the scaling curve.

---

## Scaling Laws and the Structure of Data

Neural scaling laws are not purely about model architecture — they implicitly encode assumptions about the structure of the data distribution. The MNIST example is instructive: handwritten digit images nominally live in 784-dimensional space (28×28 pixels), but the valid digit manifold occupies a far lower-dimensional subset. Effective learning exploits this low-dimensional structure; scaling laws in practice reflect how quickly models can discover and exploit it.

Large autoregressive language models like GPT-3 (vocabulary size 50,257) operate under a similar logic at scale. They are trained to predict the next token as a function of preceding context, and their scaling behavior on this objective — documented extensively in the Chinchilla and original OpenAI scaling law work — follows remarkably clean power laws across many orders of magnitude. The logarithmic linearity of loss versus scale, visible in plots from these studies, is both a practical forecasting tool and a theoretical puzzle: why should the structure of natural language compress so neatly into a power-law approximation manifold?

---

## Open Questions and Limitations

Several questions remain unresolved and structurally important:

**Where do scaling laws break?** Power-law fits hold over observed ranges but there is no theoretical guarantee they continue indefinitely. Phase transitions — emergent capabilities appearing discontinuously at certain scales — suggest the smooth power-law picture is incomplete. The relationship between loss on the training objective and performance on downstream tasks is not itself governed by simple scaling laws.

**What does the exponent measure?** The scaling exponent α encodes something about both the architecture's inductive biases and the intrinsic dimensionality of the task. Disentangling these contributions remains an open problem. KAN's claim of α = 4 for cubic splines is a theoretical result about function approximation under specific smoothness assumptions — how it translates to the messy empirical setting of large-scale training is unclear.

**Test-time compute as an orthogonal axis.** Recent interest in [[themes/test_time_compute_scaling|test-time compute scaling]] suggests that the parameter count / training compute axes of classical scaling laws are not the only levers. The empirical relationships governing how performance scales with inference-time computation — chain-of-thought length, search depth, verifier iterations — are less well characterized and potentially follow different functional forms.

**Compositional structure and the COD.** The theoretical argument that deep networks escape the curse of dimensionality by exploiting compositional structure is compelling but not fully formalized for the architectures actually in use. It is an assumption embedded in scaling law intuitions more than a proven theorem.

---

## Relationships

Neural scaling laws connect directly to [[themes/pretraining_and_scaling|pretraining and scaling]] as their primary empirical domain, and to [[themes/model_architecture|model architecture]] through the dependence of scaling exponents on architectural choices. The KAN literature sits at the intersection of [[themes/transformer_alternatives|transformer alternatives]] and the theoretical foundations of scaling. Implications extend to [[themes/test_time_compute_scaling|test-time compute scaling]] — a regime where the classical parameter-centric framing must be generalized — and to [[themes/reasoning_and_planning|reasoning and planning]], where the relationship between scale and systematic reasoning capability remains contested.

## Key Findings

## Limitations and Open Questions

## Sources
