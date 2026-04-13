---
type: source
title: Continuous Autoregressive Language Models
source_id: 01KJTC07QHXTVC9GWGEYAQ5VW0
source_type: paper
authors:
- Chenze Shao
- Darren Li
- Fandong Meng
- Jie Zhou
published_at: '2025-10-31 00:00:00'
theme_ids:
- model_architecture
- pretraining_and_scaling
- representation_learning
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Continuous Autoregressive Language Models

**Authors:** Chenze Shao, Darren Li, Fandong Meng, Jie Zhou
**Published:** 2025-10-31 00:00:00
**Type:** paper

## Analysis

# Continuous Autoregressive Language Models
2025-10-31 · paper · Chenze Shao, Darren Li, Fandong Meng, Jie Zhou
https://arxiv.org/pdf/2510.27688

---

### Motivation & Prior Limitations
- Autoregressive LLMs are fundamentally bottlenecked by sequential, token-by-token generation, where computational cost scales directly with sequence length, limiting scalability and accessibility of long-form generation and extended-context processing.
  - The historical shift from character-level to subword tokenization improved efficiency by increasing information density per unit, but discrete tokens have now hit a hard ceiling: with vocabularies of 32,000–256,000 entries, each token encodes only 15–18 bits of information.
  - Expanding discrete vocabulary size to encode larger semantic units (e.g., phrases) would require exponential growth in vocabulary, making the final softmax computation an untenable bottleneck — the discrete paradigm is therefore not a scalable path forward.
- A profound mismatch has emerged between model representational capacity (which has scaled enormously) and the task itself (predicting single low-information discrete tokens), meaning massive models are forced to laboriously predict simple units one at a time.
- Existing approaches to parallel generation — non-autoregressive translation, speculative decoding, hierarchical models like MegaByte and Large Concept Models — all retain iterative decoding at some level or rely on computationally heavy autoencoders (e.g., SONAR) with diffusion-based generation that reintroduces inference bottlenecks.

---

### Proposed Approach
- CALM replaces next-token prediction over discrete tokens with next-vector prediction over continuous vectors, where a single autoregressive step now predicts a dense continuous vector representing a chunk of K discrete tokens, reducing sequence length by a factor of K.
  - A lightweight variational autoencoder (VAE) compresses K tokens into a single continuous latent vector z ∈ ℝˡ and reconstructs the original tokens with >99.9% accuracy; critically, the autoencoder is context-free, processing each token chunk independently for computational efficiency.
  - The autoencoder is trained with three robustness techniques beyond vanilla reconstruction: (1) variational regularization with KL divergence (β = 0.001) to smooth the latent manifold, (2) KL clipping per dimension at floor λ_KL = 0.5 to prevent posterior collapse, and (3) dual dropout — 15% on input tokens (CBOW-style) and 15% on the latent vector — to force redundant, perturbation-resilient representations.
- Since continuous vector prediction renders likelihoods intractable, CALM adopts an Energy Transformer as the generative head — a small stack of residual MLP blocks that refines a noise vector ε conditioned on the Transformer's hidden state in a single forward pass, trained via the Energy Score (a strictly proper scoring rule) rather than maximum likelihood.
  - The Energy Score (Equation 10) is entirely likelihood-free: it measures alignment between predictions and observations via sample distances, using N=8 model samples and M=100 target samples drawn from the variational posterior to estimate an unbiased Monte Carlo loss.
  - The generative head contains only ~10% of total model parameters and requires a single forward pass at inference, avoiding the dozens-to-hundreds of steps required by diffusion or flow matching alternatives.
- The model's autoregressive input uses discrete token embeddings (not the latent vectors themselves), compressed via a lightweight two-layer MLP, which empirically outperforms continuous input by a large margin (BrierLM 4.70 vs. 3.25) because compact latent vectors are difficult for the Transformer to unpack semantically.
- CALM introduces three novel infrastructure components: (1) BrierLM, a likelihood-free evaluation metric based on the Brier score estimated via two model samples using an indicator-function estimator, (2) exact likelihood-free temperature sampling via a two-stage rejection algorithm grounded in the Bernoulli Factory, and (3) an approximate batch temperature sampling algorithm for low-temperature regimes that is asymptotically unbiased.

---

### Results & Capabilities
- CALM establishes a new performance-compute Pareto frontier: CALM-M (371M parameters, K=4) achieves BrierLM comparable to Transformer-S (281M) while requiring 44% fewer training FLOPs and 34% fewer inference FLOPs per token.
  - CALM-XL (1.82B parameters) reaches BrierLM 8.53, approaching Transformer-L (849M, BrierLM 8.98) while using 19.5×10²⁰ training FLOPs versus 22.5×10²⁰ for Transformer-L — a larger model achieving comparable performance at similar or lower compute.
- BrierLM correlates extremely strongly with cross-entropy perplexity across models and training checkpoints, with Pearson correlation −0.966 and Spearman rank correlation −0.991, validating it as a reliable likelihood-free substitute that applies universally to any implicit generative model family including diffusion-based LMs.
- The Energy Transformer generative head outperforms both flow matching and diffusion alternatives in final BrierLM, achieves its peak in a single inference step versus flow matching's near-optimal at 4 steps and diffusion's requirement of ~100 steps.
  - At N=2 model samples, training cost drops to 0.82× but BrierLM falls from 4.70 to 4.37; at N=12 the score saturates at 4.72 with 1.13× cost, establishing N=8 as the efficient operating point.
- Chunk size K is validated as a new scaling axis: moving from K=1 to K=2 nearly halves compute with marginal performance loss; K=4 surpasses the discrete baseline compute-performance frontier; K=8 degrades performance, likely due to insufficient model capacity at the tested scale.
  - K=1 CALM underperforms discrete baselines at equivalent FLOPs, confirming the harder continuous prediction task requires K>1 to unlock efficiency gains — the efficiency benefit is not free.
- The approximate temperature sam

## Key Claims

1. Discrete tokens in modern LLMs carry only 15 to 18 bits of information per token, representing a fundamental ceiling on information density for discrete representations.
2. Increasing discrete token information density requires exponential vocabulary growth, making the softmax computation over a larger vocabulary an untenable bottleneck.
3. CALM's continuous vector representation allows information capacity to scale gracefully by increasing vector dimensionality, unlike discrete representations which require exponential vocabulary growth
4. For K=4, a latent vector of just 10 dimensions is sufficient to achieve token-level reconstruction accuracy of over 99.9%.
5. KL clipping at a floor threshold prevents posterior collapse in the variational autoencoder, ensuring all latent dimensions remain informative.
6. For K=4 with robust training, a 128-dimensional latent vector maintains token-level accuracy exceeding 99.9% despite a latent perturbation of σ≈0.3.
7. The Energy Score is a strictly proper scoring rule that is entirely likelihood-free, measuring alignment between prediction and observation via sample distances rather than probability densities.
8. The CALM generative head accounts for only about 10% of total model parameters, making its computational overhead minimal relative to the Transformer backbone.
9. Using predicted latent vectors as Transformer input causes performance degradation; using discrete tokens from the previous chunk as input improves performance.
10. BrierLM is highly consistent with cross-entropy loss, exhibiting a Pearson correlation of -0.966 and a Spearman rank correlation of -0.991.

## Capabilities

- Continuous autoregressive language modeling (CALM) compresses K discrete tokens into a single continuous vector, reducing autoregressive generation steps by a factor of K. At K=4, achieves performance comparable to a strong discrete baseline with 44% fewer training FLOPs and 34% fewer inference FLOP
- High-fidelity variational autoencoder compresses a chunk of K=4 tokens into a 128-dimensional continuous vector, maintaining >99.9% token-level reconstruction accuracy despite significant Gaussian noise perturbation (σ≈0.3) on the latent.
- BrierLM: a strictly proper, likelihood-free language model evaluation metric based on the Brier score, computed via unbiased Monte Carlo sampling with no access to model likelihoods. Achieves Pearson −0.966 and Spearman −0.991 correlation with cross-entropy loss, enabling principled evaluation of im
- Provably exact likelihood-free temperature sampling from implicit discrete distributions using a two-stage rejection sampling algorithm grounded in Bernoulli Factory theory, requiring only a black-box sampler interface.
- Energy Transformer generative head achieves single-step continuous vector generation, outperforming both diffusion-based and flow-matching generative heads while eliminating iterative decoding overhead entirely.

## Limitations

- CALM with K=1 (continuous prediction of single tokens) performs worse than a standard discrete Transformer at the same compute budget, revealing that the continuous domain makes the prediction task fundamentally harder, not easier.
- CALM cannot use standard RL post-training methods (PPO, DPO, RLHF) because these require log-probabilities of generated samples — a quantity that is intractable in the continuous likelihood-free framework.
- Standard knowledge distillation is incompatible with CALM because KL divergence between teacher and student distributions cannot be computed without access to the full probability mass function.
- Exact likelihood-free temperature sampling becomes computationally catastrophic at temperatures near T→1, where the expected number of sampler calls scales up to |V|^K — the full chunk vocabulary size.
- Exact temperature sampling in the low-temperature regime requires drawing n=⌊1/T⌋ identical samples — an event with vanishingly small probability — causing an extremely high rejection rate and practical infeasibility.
- Performance degrades substantially at K=8 chunk size, indicating that current CALM model capacities cannot exploit higher semantic bandwidths, requiring proportionally larger models for higher K values.
- The CALM autoencoder is context-free — it encodes each K-token chunk independently with no access to surrounding sequence context — limiting the semantic richness and robustness of the compressed representations.
- CALM's autoencoder latent space lacks semantic structure — nearby vectors do not correspond to semantically similar token sequences — because training optimizes only for reconstruction fidelity, not semantic proximity.
- Standard perplexity and likelihood-based evaluation metrics are entirely inapplicable to CALM, requiring a completely new evaluation framework and making direct comparison with existing literature non-trivial.
- Using continuous latent vectors directly as Transformer input leads to substantial performance degradation, requiring the model to decode back to discrete tokens for input grounding — partially defeating the continuous representation paradigm.
- Naive incorporation of a variational objective causes severe posterior collapse: in experiments, 71 of 128 latent dimensions collapsed to the standard normal prior, becoming uninformative and injecting noise into downstream generative model training.
- CALM scaling laws are entirely uncharacterized: the optimal chunk size K for a given model size and compute budget is unknown, preventing principled architecture search and hyperparameter selection.
- CALM's approximate temperature sampling algorithm (Algorithm 2) is biased for any finite batch size N, because the output probability is determined by the ratio of counts in a single stochastic batch; only asymptotically unbiased as N→∞.
- Latent dimension selection exhibits a brittle sweet spot: dimensions too small (l=32) produce fragile representations, while dimensions too large (l=256) cause the generative model to waste capacity modeling noise or irrelevant features.
- CALM exhibits a slower initial learning curve than equivalent-parameter discrete Transformers, requiring more training steps before the model begins effectively leveraging its parameter count — likely creating a disadvantage in low-compute or fast-iteration regimes.

## Bottlenecks

- Standard LLM post-training alignment pipelines (RLHF, PPO, DPO, knowledge distillation) cannot be applied to likelihood-free continuous autoregressive models, blocking practical deployment and alignment of the CALM model family.
- Absence of CALM-specific scaling laws leaves the optimal chunk size K for a given compute budget undetermined, preventing principled scale-up and blocking deployment at scales larger than tested (~2B parameters on ~230B tokens).
- Context-free autoencoder architecture limits the semantic quality of compressed representations, preventing CALM from achieving higher effective semantic bandwidths (K>4 without performance degradation) and blocking further efficiency gains beyond 4x step reduction.

## Breakthroughs

- CALM establishes continuous next-vector prediction as a viable and superior performance-compute paradigm for language modeling, shifting the fundamental unit of autoregressive generation from a discrete token to a continuous vector encoding K tokens, and achieving a better performance-compute fronti
- BrierLM introduces the first strictly proper, likelihood-free LM evaluation metric that can faithfully assess implicit generative models (diffusion LMs, CALM) without ELBO approximations, solving a longstanding evaluation gap for the growing class of non-autoregressive language models.

## Themes

- [[themes/model_architecture|model_architecture]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/representation_learning|representation_learning]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/transformer_alternatives|transformer_alternatives]]
