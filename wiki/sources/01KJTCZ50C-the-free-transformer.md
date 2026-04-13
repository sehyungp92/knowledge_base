---
type: source
title: The Free Transformer
source_id: 01KJTCZ50CQY58RKSCCE1Q1SBS
source_type: paper
authors:
- François Fleuret
published_at: '2025-10-20 00:00:00'
theme_ids:
- latent_reasoning
- model_architecture
- reasoning_and_planning
- representation_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Free Transformer

**Authors:** François Fleuret
**Published:** 2025-10-20 00:00:00
**Type:** paper

## Analysis

# The Free Transformer
2025-10-20 · paper · François Fleuret
https://arxiv.org/pdf/2510.17558

---

### Motivation & Prior Limitations
- Standard decoder Transformers are purely autoregressive: every latent decision about sequence structure must be inferred post-hoc from already-generated tokens rather than made explicitly before generation begins.
  - The paper illustrates this with a coin-flip example: a simple distribution over sequences that is conditionally independent given a latent variable Z becomes a complex, error-prone recurrence when expressed purely autoregressively (Equation 2).
  - This forces the model to carry running probability estimates (e.g., "is the target here?") across token steps, where estimation errors compound — demonstrated concretely on a synthetic position-finding task where a vanilla Transformer must infer the location of a buried pattern from tokens alone.
- Three specific failure modes follow from pure autoregression: unnecessarily complex computation to implicitly resolve latent structure, susceptibility to derailment by early erroneous or ambiguous tokens, and concepts that emerge only post-hoc to fit training samples rather than from natural factorization — a potential out-of-distribution weakness.
- Prior VAE-Transformer hybrids (OPTIMUS, CVAE, AdaVAE) all fine-tune pre-trained models and focus on guided generation or topic modeling, rather than training from scratch to improve general-purpose language modeling quality.

---

### Proposed Approach
- The Free Transformer extends a standard decoder-only Transformer by injecting a sequence of discrete latent random variables Z at the model's midpoint, trained end-to-end as a conditional Variational Autoencoder (cVAE) without any supervised signal on the latent.
  - Z is a sequence of one-hot vectors of dimension 2^H (H=16, so 65,536 categories), sampled during generation from a uniform prior; during training, an encoder produces the posterior Q(Z|S) via a Binary Mapper that samples H independent bits and encodes them as a one-hot index with gradient pass-through via straight-through estimation.
  - The encoder shares the first L/2 Transformer blocks with the decoder, adding only a single non-causal Transformer block and two linear layers — a 3.1–3.6% compute/memory overhead over the baseline, far cheaper than a full second model.
  - The encoder uses a learned constant query embedding ζ (not the token representation) to discourage token-wise copying and encourage capture of global sequence properties.
- KL collapse is prevented using token-wise free bits: only KL terms above threshold κ per token contribute to the loss, with κ tuned between 0.5 and 2 bits per token in experiments.
  - This directly controls how much global information the latent is allowed to encode, with collapse observed at κ = 4 bits (exceeding the model's cross-entropy of ~2.59 bits).
- The authors explicitly draw an analogy to chain-of-thought reasoning in latent space: the Free Transformer achieves in the continuous latent what reasoning models achieve via discrete token chains and RL (DeepSeek-R1 style), and suggest combining the two is a promising direction.

---

### Results & Capabilities
- Across both 1.5B (47B tokens) and 8B (200B tokens) models, the Free Transformer shows substantial gains specifically on reasoning-intensive benchmarks while leaving perceptual/associative tasks largely unchanged.
  - On HumanEval+: +44–56% for 1.5B, +7–19% for 8B; on MBPP: +9–36% for 1.5B, +7–19% for 8B; on GSM8K: +6–30% for 1.5B, +10–20% for 8B.
  - On MMLU and CSQA, the 8B model at κ=½ bit gains +11% and +26% respectively, but these gains are sensitive to κ — other κ values hurt MMLU and CSQA on the 8B model.
- At the most realistic scale (8B model, 1T tokens, κ=½ bit), gains are more moderate but consistent: HumanEval+ +11.4%, MMLU +5.2%, CSQA +5.8%, GSM8K +2.8%, MBPP +2.8% at final checkpoint; averaging over the last third of training (to smooth instability) gives +4–6% on reasoning tasks and near-zero change on pattern/associative tasks.
- The synthetic dataset experiment confirms the latent encodes interpretable structure: at low κ the model behaves like vanilla autoregression; at moderate κ it encodes target position into Z enabling consistent coherent generation across sequences sharing the same Z; at high κ it encodes the full sequence, collapsing into a memorization regime.
- The cross-entropy during training degrades by only ~0.01 (relative to ~1.8–2.0 baseline) across all non-collapsing κ values, indicating the latent provides conditional structure rather than simply making the prediction task easier.

---

### Implications
- The result that ~3% compute overhead produces consistent gains on code and math benchmarks — tasks widely associated with multi-step reasoning — suggests that explicit latent sampling before token generation is a more natural inductive bias for structured outputs than purely autoregressive factorization.
- This work challenges the assumption that autoregression is the uniquely correct generative formulation for language: introducing unsupervised latent variables recovers a richer density model that the chain rule alone obscures, potentially changing how future architectures are designed from scratch rather than retrofitted.
- The parallel to chain-of-thought reasoning (latent-space decisions vs. token-space scratchpads) opens a research direction in which internal stochastic structure and external reasoning traces are combined, with neither replacing the other.
- For representation_learning, the encoder's use of a constant query embedding to extract global sequence properties — rather than token-level features — is a novel design choice that may inform how learned latent representations generalize across tasks and domains.

---

### Remaining Limitations & Next Steps
- The optimization hyperparameters were tuned for the baseline and left unchanged for the Free Transformer; the authors explicitly note this i

## Key Claims

1. Decoder Transformers do not make explicit latent decisions about the stream of symbols to generate; their only decisions are the choices of the tokens themselves.
2. The autoregressive modelling paradigm of Transformers has remained essentially unchallenged for nearly a decade despite improvements in other aspects of the architecture.
3. Purely autoregressive models require unnecessarily complicated computation and greater capacity to implicitly make post-hoc latent decisions from the generated tokens.
4. Purely autoregressive models can be sent off track during generation if a few early tokens are erroneous, ambiguous, or contradictory.
5. In purely autoregressive models, key concepts are built post-hoc by necessity rather than emerging from the natural factorization of the distribution, which may be a fundamental out-of-distribution we
6. The Free Transformer extends the decoder Transformer by conditioning its generative process on random latent variables learned without supervision via a variational procedure.
7. The Free Transformer injects the latent random state Z at the middle layer of the decoder, sharing the first half of Transformer blocks between encoder and decoder to minimize overhead.
8. The Free Transformer requires only a single additional non-causal Transformer block and two linear layers for the encoder, resulting in 3.6% compute/memory overhead for the 1.5B model and 3.1% for the
9. The encoder block in the Free Transformer is non-causal and uses a learned constant token as its query input, rather than the sequence representation, to capture global rather than token-wise properti
10. The Free Transformer uses a Binary Mapper to convert H=16 logits into a one-hot vector of dimension 2^H = 65,536 with gradient pass-through via sigmoid monotonicity.

## Capabilities

- Decoder Transformer conditioned on unsupervised learned latent variables via VAE procedure (Free Transformer) achieves 11% improvement on HumanEval+ and 5% on MMLU/CSQA at 8B/1T scale, with only ~3.1% compute and memory overhead over standard decoder Transformers.
- Encoder-sharing architecture for efficient VAE conditioning: injecting latent Z at the midpoint of the decoder shares half the transformer blocks between encoder and decoder, achieving ~3.1–3.6% overhead for full latent variable conditioning in pretraining-scale models.
- Unsupervised structural latent encoding: the Free Transformer encoder learns to capture discrete structural properties of sequences (e.g., position of a target pattern) in a low-dimensional latent space without explicit supervision, enabling coherent conditioned generation from a shared latent Z.

## Limitations

- Training instability from coupled encoder-decoder optimization: performance curves are often unstable during training, and no optimization recipes specific to the joint encoder-decoder structure exist — all experiments reuse hyperparameters tuned for decoder-only baselines.
- Reported improvements are likely a lower bound: optimization hyperparameters were not adapted for the Free Transformer, meaning the architecture is systematically undertrained relative to the baselines it is compared against.
- KL collapse above ~2–3 bits per token: setting κ = 4 log(2) causes the encoder to channel the full token sequence into Z, making the decoder degenerate and collapsing downstream task performance entirely.
- Unknown behavior at scale beyond 8B parameters and 1T training tokens — frontier-scale behavior (70B+, multi-trillion tokens) is entirely uncharacterized.
- Consistent performance degradation on factual recall and cultural knowledge tasks across all scales and bit budgets: NQ and TQA show persistent negative deltas (up to -15% on NQ at 1.5B) that the paper does not acknowledge or explain.
- Improvements are narrowly concentrated on reasoning-intensive benchmarks (code, math, MMLU, CSQA); most commonsense, reading comprehension, and factual benchmarks show near-zero or negative deltas — the approach does not uniformly improve language model quality.
- Latent embedding design is entirely arbitrary — the binary mapper, one-hot encoding, and 2^16 dimensionality were not validated against alternatives, leaving the architecture potentially far from optimal.
- Encoder computation required at KV cache pre-filling time: the non-causal encoder pass must run over any prefilled context at inference time, adding overhead beyond pure generation that is absent from standard decoder-only deployments.
- No method proposed for adapting pretrained decoder models to the Free Transformer format — all experiments train from scratch, leaving open whether the approach can be applied to existing frontier models via continued pretraining or supervised fine-tuning.
- Pure autoregressive models are theoretically suboptimal on data with latent structure: they must implicitly infer latent decisions post-hoc from generated tokens, requiring disproportionately greater capacity and suffering error accumulation when early tokens are ambiguous.

## Bottlenecks

- Absence of training recipes optimized for joint encoder-decoder language model pretraining blocks reliable and efficient training of latent-variable decoder transformers, making current results likely underestimates and preventing practical adoption of the approach.
- KL collapse fragility constrains the usable latent information budget in VAE-extended language models: the narrow window between useful conditioning (sub-2-bit) and catastrophic collapse (≥4 bits) limits representable latent structure and requires careful per-model threshold calibration.

## Breakthroughs

- A standard decoder Transformer can be extended with unsupervised latent variable conditioning via a VAE procedure at only ~3% computational overhead, achieving consistent improvements on reasoning-intensive benchmarks (code, math, MMLU) across 1.5B and 8B scales without any hyperparameter tuning for

## Themes

- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/representation_learning|representation_learning]]

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/mmlu|MMLU]]
- [[entities/rmsnorm|RMSNorm]]
- [[entities/swiglu|SwiGLU]]
