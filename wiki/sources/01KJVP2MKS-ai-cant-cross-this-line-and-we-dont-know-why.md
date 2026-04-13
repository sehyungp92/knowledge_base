---
type: source
title: AI can't cross this line and we don't know why.
source_id: 01KJVP2MKSVAYJF4F716NXXEA2
source_type: video
authors: []
published_at: '2024-09-13 00:00:00'
theme_ids:
- model_architecture
- pretraining_and_scaling
- representation_learning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AI Can't Cross This Line and We Don't Know Why

> A rigorous technical explainer on neural scaling laws: how model performance follows predictable power-law relationships with compute, model size, and dataset size across orders of magnitude, why a fundamental irreducible floor prevents loss from reaching zero, and where the theory breaks down entirely — particularly around emergent capabilities, the theory-practice gap for natural language, and the open question of whether scaling laws reflect a law of nature or an artifact of current architectures.

**Authors:** (unknown/channel)
**Published:** 2024-09-13
**Type:** video
**Source:** [YouTube](https://www.youtube.com/watch?v=5eqRuVp65eY)

---

## The Compute-Optimal Frontier

When an AI model trains, its error rate drops quickly before leveling off. Train a larger model and that floor drops further, at the cost of more compute. Plot many such curves on logarithmic axes and a striking regularity appears: no model can cross a boundary called the **compute-optimal** or **compute-efficient frontier**. This is not an engineering limitation; it is an empirical law that has held across more than 13 orders of magnitude of compute, from 10⁻⁸ to over 200,000 petaflop-days.

This frontier is one expression of three broadly observed **neural scaling laws**: model error scales predictably as a power law of (1) compute, (2) model size (parameter count), and (3) dataset size. Remarkably, these relationships hold largely independent of model architecture or other algorithmic choices, provided those choices are reasonable.

The key empirical discoveries came from [[entities/openai|OpenAI]]'s January 2020 paper, which fit power-law equations to results across a wide range of scales for language models. On logarithmic plots, power laws appear as straight lines; the slope equals the power-law exponent, with steeper slopes indicating faster performance gains per unit of scale. That paper's largest tested model had 1.5 billion parameters, trained using approximately 10 petaflop-days of compute. By summer 2020, GPT-3 (175 billion parameters, 3,640 petaflop-days, trained on a 10,000-V100-GPU supercomputer built with Microsoft) validated the predicted trend line with striking accuracy — and showed no sign of flattening, implying further gains from further scaling.

An October 2020 follow-up paper extended this analysis to image and video modeling. Scaling trends on those tasks did eventually flatten before reaching zero error, consistent with a theoretical lower bound arising from irreducible uncertainty in the data.

---

## Why Loss Cannot Reach Zero

Large language models are autoregressive: they predict the next word (or sub-word token) from the preceding context. At each step, the model outputs a probability distribution over its vocabulary. GPT-3 has a vocabulary of 50,257 tokens; given an input sequence, it assigns a probability to each possible continuation.

Training minimizes **cross-entropy loss**, the negative log-probability the model assigns to the correct next token. This is preferred over simpler L1 loss because it penalizes low-confidence wrong answers much more severely, which empirically improves learning.

The critical constraint is that natural language is fundamentally ambiguous: any given context admits multiple plausible continuations. This inherent uncertainty is the **entropy of natural language**. Even a perfect model that fully captures the structure of language cannot produce a single deterministic next token; it can only distribute probability mass over realistic options. Cross-entropy loss can therefore never reach zero.

Fitting power-law models to empirical loss curves with an irreducible constant term (representing this floor) suggests that even an infinitely large model trained on infinite data cannot achieve an average cross-entropy loss better than approximately **1.69** on standard natural language corpora. This is a fundamental ceiling on language model performance, not an engineering constraint.

Estimating this floor precisely remains difficult. Even data from the largest deployed language models is insufficient to pin down the entropy of natural language with confidence.

---

## What Scaling Laws Cannot Explain

The empirical success of scaling laws conceals several significant gaps.

**Emergent capabilities.** Abilities such as arithmetic, word unscrambling, and multi-step reasoning do not improve gradually with scale. They appear to pop into existence at specific thresholds. Scaling law theory, built on continuous power-law relationships, provides no mechanism for these discrete transitions. Predicting when a given capability will emerge during scaling remains an open problem.

**The theory-practice gap for language.** A theoretical explanation for power-law scaling exists via the **manifold hypothesis**: deep learning models learn to represent high-dimensional data as lower-dimensional manifolds, where geometrically nearby points correspond to semantically similar concepts. Model performance should then scale with data density on this manifold, predicting the observed power-law form. When applied to natural language and calibrated against empirical scaling exponents (approximately −0.095 for language), the theory predicts an intrinsic dimension of roughly 42. Direct empirical measurement finds the intrinsic dimension of natural language to be approximately 100. This gap of nearly 60 points indicates the theoretical framework is materially incomplete for language, even if directionally correct.

**No unified theory.** The manifold hypothesis offers a compelling sketch but does not constitute a full derivation. There is no unified theoretical account of why power laws govern neural scaling across domains, what determines the exponent in any given setting, or where the limits of scalability lie. The empirical regularity is robust; the theoretical understanding behind it is not.

---

## Capabilities

| Capability | Maturity |
|---|---|
| Predict frontier model performance using power-law fits from smaller experiments (e.g., accurately predicting GPT-4 performance) | narrow production |
| Power-law scaling of model performance across compute, model size, and data; holds across language, image, and video | broad production |
| Language models produce multi-modal probability distributions that assign high probability to realistic continuations | broad production |
| Scaling laws remain predictive across 13+ orders of magnitude of compute | broad production |
| Neural networks learn lower-dimensional manifold representations where geometric proximity encodes semantic similarity | broad production |

---

## Limitations

**Irreducible performance floor.** Even infinitely large models trained on infinite data cannot achieve cross-entropy loss below approximately 1.69 on natural language. This is a consequence of linguistic entropy, not engineering failure. The trajectory is stable; no route around it is visible.

**Cannot predict emergence.** Scaling laws are highly predictive of next-word prediction loss but cannot anticipate the emergence of discrete capabilities (arithmetic, reasoning, multi-step planning) at particular scale thresholds. The mechanism is unknown.

**Theory-practice gap for language.** The manifold-hypothesis explanation predicts intrinsic dimension ~42 for natural language; empirical measurement finds ~100. This discrepancy blocks theoretical prediction of language model scaling behavior and limits confidence in extrapolations.

**Intractable entropy estimation.** Even with data from the largest available models, the entropy of natural language cannot yet be estimated with meaningful precision. This fundamental unknown constrains theoretical understanding of where model performance is heading.

**Massive training cost creates access barriers.** GPT-4 reportedly cost well over $100 million to train, requiring 25,000 A100 GPUs running for over three months (>200,000 petaflop-days). This cost structure concentrates capability development among a small number of actors. The trajectory is worsening as frontier models continue to grow.

**No unified theoretical framework.** The power-law form of scaling laws lacks a complete theoretical derivation. Without it, performance on novel tasks remains difficult to predict from first principles, and the ultimate limits of scaling are unknown.

---

## Open Questions

- Do scaling laws reflect a fundamental property of learning systems, or are they an artifact of current neural network architectures? Would alternative approaches to AI exhibit different scaling behavior?
- What determines the exponent of a power-law scaling relationship in a given domain? Why does language have an exponent of approximately −0.095?
- Will performance improvements continue indefinitely as compute, data, and model size grow, or will additional ceilings emerge beyond the entropy floor?
- What mechanism causes capabilities to emerge discretely at scale rather than improving continuously? Can emergence be predicted or engineered?
- Why does the manifold hypothesis underestimate intrinsic language dimensionality by roughly a factor of 2.5? What missing structure would close this gap?

---

## Bottlenecks Identified

**No unified theory of scaling** (horizon: 3-5 years). Without a complete theoretical account of why power laws govern neural scaling, predicting performance on novel tasks and understanding fundamental capability limits both remain constrained to empirical extrapolation.

**Unknown intrinsic dimensionality of language** (horizon: 1-2 years). The entropy of natural language cannot be estimated reliably from current models. This blocks theoretical predictions of scaling behavior and limits understanding of the irreducible performance floor.

**Theory-practice gap for language specifically** (horizon: 1-2 years). The manifold hypothesis gives wrong predictions for natural language dimensionality. A corrected or extended framework is needed before scaling theory can make reliable structural predictions for language.

**Unknown mechanism for emergent capabilities** (horizon: unknown). The discrete appearance of arithmetic, reasoning, and unscrambling abilities at specific scales is unexplained by continuous scaling theory. Until the mechanism is understood, emergence is fundamentally unpredictable.

---

## Themes

- [[themes/scaling_laws|Scaling Laws]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/representation_learning|Representation Learning]]
- [[themes/model_architecture|Model Architecture]]

## Key Concepts

- [[entities/autoregressive-language-model|Autoregressive Language Model]]
- [[entities/chinchilla-scaling-laws|Chinchilla Scaling Laws]]
- [[entities/gpt-4|GPT-4]]
- [[entities/neural-scaling-laws|Neural Scaling Laws]]
- [[entities/umap|UMAP]]
