---
type: source
title: How much do language models memorize?
source_id: 01KJTQRXBY5D86ATF1V7EGZ234
source_type: paper
authors:
- John X. Morris
- Chawin Sitawarin
- Chuan Guo
- Narine Kokhlikyan
- G. Edward Suh
- Alexander M. Rush
- Kamalika Chaudhuri
- Saeed Mahloujifar
published_at: '2025-05-30 00:00:00'
theme_ids:
- alignment_and_safety
- hallucination_and_reliability
- pretraining_and_scaling
- pretraining_data
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How much do language models memorize?

**Authors:** John X. Morris, Chawin Sitawarin, Chuan Guo, Narine Kokhlikyan, G. Edward Suh, Alexander M. Rush, Kamalika Chaudhuri, Saeed Mahloujifar
**Published:** 2025-05-30 00:00:00
**Type:** paper

## Analysis

# How much do language models memorize?
2025-05-30 · paper · John X. Morris, Chawin Sitawarin, Chuan Guo, Narine Kokhlikyan, G. Edward Suh et al. (8 total)
https://arxiv.org/pdf/2505.24832

---

### Motivation & Prior Limitations
Prior work on language model memorization could not cleanly separate memorization from generalization, making capacity estimates unreliable and membership inference results ambiguous.
- Extraction-based definitions of memorization (Carlini et al., 2023; Nasr et al., 2023; Schwarzschild et al., 2024) treat a datapoint as memorized if the model can be induced to generate it, but this conflates genuine storage with generalization — a model can output "2+2=4" without ever having trained on that exact equation.
  - Even prefix-constrained extraction methods fail to resolve this: any string can be coerced from a language model under adversarial prompting (Geiping et al., 2024), so generation is not proof of memorization.
- No prior work had measured a principled upper bound on raw model capacity — how many bits of arbitrary information a transformer can store per parameter — leaving the relationship between parameter count, dataset size, and memorization without a quantitative foundation.
  - Allen-Zhu & Li (2024) estimated ~2 bits per parameter via quantization arguments, but this underestimates empirical capacity; Roberts et al. (2020) and Lu et al. (2024) noted linear fact-storage scaling without precise measurement.

---

### Proposed Approach
The paper formalizes memorization as an information-theoretic compression problem, decomposing total memorization into *unintended memorization* (information the model retains about a specific dataset) and *generalization* (information about the true data-generating process), and estimates each component using model likelihoods as proxies for Kolmogorov complexity.
- Unintended memorization of a sample x in trained model θ̂ is defined as the reduction in description length of x when θ̂ is available beyond what a reference model θ already provides: `memU(x, θ, θ̂) = HK(x | θ) − HK(x | θ, θ̂)`.
  - This differs from Brown et al. (2021), which defined memorization using conditional mutual information at the distribution level; the present approach operates at the instance level using algorithmic (Kolmogorov) rather than Shannon information, enabling measurement from a single model and a single sample without distributional assumptions.
  - Kolmogorov complexity is approximated using arithmetic coding tied to model likelihoods: `HK(x | θ̂) ≈ −log p(x | θ̂)` and `HK(x | θ̂, θ) ≈ −log max{p(x | θ̂), p(x | θ)}`.
- Capacity is measured by eliminating generalization entirely: models are trained on uniform random bitstrings (where no pattern is learnable), so all mutual information between data and model constitutes unintended memorization, giving a clean upper bound on bits stored per parameter.
- A scaling law for membership inference F1 is derived as a sigmoid over the capacity-to-dataset-size ratio: `MembershipF1(θ, D) = ½(1 + c₁σ(c₂(Capacity(θ)/|D| + c₃)))`, fit via nonlinear least squares and validated on models up to 1.5B parameters.

---

### Results & Capabilities
GPT-style transformer language models store approximately 3.6 bits of information per parameter, measured as a stable empirical constant across model sizes from 100K to 20M parameters and across architectural variants (depth 1–8 layers, width 32–512 hidden dimensions).
- Measured bits-per-parameter (α) ranges from 3.51 (bfloat16) to 3.83 (float32), with a mean of ~3.64 bfloat16 across all tested configurations; doubling numerical precision from bf16 to fp32 increases capacity by only ~9%, far less than the 2× increase in raw parameter bits, indicating most extra precision bits are not used for raw storage.
- Models exhibit a hard capacity plateau on random data: unintended memorization increases linearly with dataset size until the model saturates, then flatlines regardless of further data, confirming a genuine upper bound rather than a soft asymptote.

Double descent in language model training is explained quantitatively as the transition point where dataset size exceeds model capacity in bits, verified using exact capacity measurements.
- Test loss degrades and then recovers precisely when the dataset-to-capacity ratio crosses 1, matching the Nakkiran et al. (2019) double descent curve but now with exact rather than proxy measurements of both dataset information content and model capacity.
- The paper proposes a mechanistic account: once per-sample memorization is no longer viable, the model is forced to share capacity across samples, inducing generalization as a compression strategy rather than a deliberate inductive bias.

The membership inference scaling law predicts F1 scores within 1–2 percentage points of empirical values for GPT-2 Small (125M params) and GPT-2 XL (1.5B params), and extrapolates to conclude that all contemporary models trained at tokens-per-parameter ratios ≥10² are effectively immune to loss-based membership inference on average datapoints (predicted F1 ≈ 0.5).
- Membership inference is strictly easier than extraction in every tested condition: models can achieve F1 of 0.97 for membership detection with an extraction rate of 0, confirming these are distinct phenomena.
- Extraction rates for deduplicated text datasets converge to test-set extraction rates as dataset size grows, meaning all successful extraction at scale is attributable to generalization rather than memorization of specific training samples.

---

### Implications
This work establishes ~3.6 bits per parameter as a principled empirical constant for GPT-family transformers, providing a calibration tool for scaling law research: model capacity in bits is now a concrete, measurable quantity that can be incorporated into data-compute tradeoff analyses alongside Chinchilla-style token budgets.
- Knowing that a 7B parameter model has ~25GB of memorization capacity (≈3.6 × 7×10⁹ bits

## Key Claims

1. GPT-style language models have an approximate memorization capacity of 3.6 bits per parameter
2. Language models memorize training data until their capacity fills, at which point grokking begins and unintended memorization decreases as generalization starts
3. Double descent begins exactly when dataset size in bits exceeds model capacity in bits
4. GPT-style models trained in bfloat16 half precision have a capacity of approximately 3.51 bits per parameter; doubling to float32 increases this only to 3.83 bits per parameter
5. Most modern language models trained with a tokens-per-parameter ratio of 100 or higher cannot be reliably subject to loss-based membership inference on the average datapoint
6. Extraction (inducing a model to generate a training string) does not necessarily prove memorization, because language models can be coerced to output almost any string
7. Unintended memorization scales with dataset size but cannot exceed the total capacity of the model
8. For sufficiently large deduplicated datasets, all successful training data extraction is attributable to generalization rather than memorization
9. Membership inference is strictly easier than extraction in all measured cases; high membership inference F1 scores are achievable even with zero extraction rate
10. Model capacity scales linearly (roughly proportionally) with parameter count

## Capabilities

- Information-theoretic measurement of GPT-style language model memory capacity using Kolmogorov complexity approximated via arithmetic coding, yielding approximately 3.6 bits per parameter for GPT-family transformers across a wide range of depths and widths
- Scaling law predicting membership inference attack F1 score from model capacity and training dataset size, validated on GPT-2 small through GPT-2 XL (125M to 1.5B parameters), with predictions within 1–2 percentage points of observed values
- Formal instance-level separation of unintended memorization from generalization using Kolmogorov complexity, enabling per-datapoint measurement of how many bits a model retains about specific training examples independently of what could have been predicted from the data-generating process
- Dataset-to-capacity ratio as a precise predictor of double descent onset: double descent begins exactly when training dataset size in bits exceeds model capacity in bits, providing a quantitative explanation for the double descent phenomenon

## Limitations

- Loss-based membership inference attacks are practically impossible on all modern large language models trained with a tokens-per-parameter ratio of 100 or higher — covering essentially all contemporary frontier models — yielding F1 scores indistinguishable from random guessing
- Capacity measurements via gradient descent are inherently lower bounds — the true capacity of a model may exceed any observed measurement since gradient descent is not guaranteed to find the global optimum of memorization
- Exact Kolmogorov complexity — the theoretical foundation of the memorization measurement framework — is provably uncomputable, requiring practical approximations via arithmetic coding that systematically underestimate true complexity
- Doubling model parameter precision from bfloat16 to float32 increases measured memorization capacity by only ~9% (3.51 to 3.83 bpp) despite a 2x increase in raw parameter bit count — the vast majority of extra bits added by higher precision are not used for information storage
- The memorization measurement method requires a reference model — a larger model trained on a strict superset of the target model's training data — making it inapplicable to closed-source or third-party models where training data access is unavailable
- Scaling law for membership inference validated only on models up to 1.5B parameters — extrapolation to frontier models (7B–1T+ parameters) using different training pipelines, data mixtures, and architectural innovations may not hold
- Faithful memorization measurement requires perfect deduplication of the training dataset — even 1–2% duplicate sequences (which arise naturally when truncating to fixed sequence lengths) significantly distort extraction rate measurements
- Extraction-based memorization detection fails to detect training data membership in cases where membership inference succeeds — a model can achieve near-perfect membership inference F1 (0.97) while having extraction rate of zero, meaning prior extraction-based privacy auditing systematically underco
- The sigmoidal functional form for the membership inference scaling law is acknowledged to be slightly simplistic — fits deviate most significantly near the inflection point (predicted F1 ≈ 0.75), which is where predictions are least reliable in practice
- When the training dataset grows sufficiently large and deduplicated, extraction rates for training data converge to test extraction rates — all apparent extraction becomes attributable to generalization rather than memorization, making it impossible to distinguish training exposure from general know

## Bottlenecks

- Privacy auditing and training data attribution for modern frontier LLMs is effectively theoretically impossible using loss-based membership inference: the tokens-per-parameter ratios used in production (≥100:1) push membership inference to chance level, blocking any practical verification of what da
- No principled method exists to measure language model memorization or capacity without privileged access to a reference model trained on a superset of the target model's training data, preventing independent third-party memorization audits of closed-source frontier models

## Breakthroughs

- First information-theoretically grounded empirical upper bound on language model memorization capacity: GPT-family transformers store approximately 3.6 bits per parameter, with a clean linear relationship between capacity and parameter count that holds across architectural variations
- Formal framework resolving the memorization-vs-generalization ambiguity at the instance level: Kolmogorov complexity allows precise per-datapoint measurement of how many bits a model stores about a specific training example, independently of what could have been predicted from the data distribution

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/pretraining_data|pretraining_data]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/grokking|grokking]]
