---
type: source
title: Energy-Based Transformers are Scalable Learners and Thinkers
source_id: 01KJTNZS7X36EGSKTVH7B5S18M
source_type: paper
authors:
- Alexi Gladstone
- Ganesh Nanduru
- Md Mofijul Islam
- Peixuan Han
- Hyeonjeong Ha
- Aman Chadha
- Yilun Du
- Heng Ji
- Jundong Li
- Tariq Iqbal
published_at: '2025-07-02 00:00:00'
theme_ids:
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Energy-Based Transformers are Scalable Learners and Thinkers

Energy-Based Transformers (EBTs) propose a unified architecture that reframes prediction as gradient-descent energy minimisation over a learned verifier function, enabling System 2 Thinking — iterative self-refinement with built-in verification — to emerge purely from unsupervised pretraining, without reward signals, modality assumptions, or external verifiers. The paper demonstrates that EBTs out-scale the standard Transformer++ recipe across six training axes and both discrete (text) and continuous (visual) modalities, and that additional inference-time compute yields measurable gains — an improvement not available to standard feed-forward architectures.

**Authors:** Alexi Gladstone, Ganesh Nanduru, Md Mofijul Islam, Peixuan Han, Hyeonjeong Ha, Aman Chadha, Yilun Du, Heng Ji, Jundong Li, Tariq Iqbal
**Published:** 2025-07-02
**Type:** paper

---

## Motivation and Prior Limitations

The paper's central premise is that existing inference-time compute ("System 2 Thinking") techniques are too constrained to function as a general paradigm. Each current approach is broken along at least one axis:

- **RL-based reasoning models** (O1, R1, Grok3) require verifiable rule-based rewards and are therefore limited to math and coding. They demonstrably degrade on open-ended tasks like writing. More fundamentally, recent evidence suggests they may not induce genuinely new reasoning patterns — they may simply increase the probability of patterns already known to the base model, limiting performance on problems requiring exploration of novel solution paths.
- **Diffusion models** support iterative inference but cannot benefit from denoising steps beyond their training budget, require an external verifier to improve System 2 Thinking, and do not provide explicit uncertainty estimates in continuous state spaces.
- **Modern RNNs** update state only with new information and cannot "think longer" per prediction. Variants that support recurrent depth still lack explicit prediction verification, amortising gradient prediction of the energy function rather than modelling it directly.
- **Standard feed-forward Transformers** (Transformer++) have three structural gaps: fixed depth/width prevents dynamic per-prediction compute allocation; they cannot model uncertainty in continuous state spaces without discretisation tricks (Vector Quantisation, ELBO); and they are not trained as explicit verifiers, requiring external models for any per-prediction inference-time improvement.

The paper also addresses a long-standing gap in Energy-Based Models (EBMs): historically, EBMs suffered from training instability, long training times, and curse-of-dimensionality problems with contrastive training. No publicly known foundation-scale EBM existed prior to this work.

---

## The Energy-Based Transformer Architecture

EBTs frame every prediction as optimisation: instead of a single forward pass producing an output, the model assigns a scalar energy (unnormalized log-probability) to every (context, candidate-prediction) pair, then refines an initial random prediction by descending the gradient of this energy until convergence.

This single design choice simultaneously resolves three structural limitations of the Transformer++:

| Gap | EBT Resolution |
|-----|---------------|
| Fixed compute per prediction | Variable gradient-descent steps — more steps for harder predictions |
| No uncertainty modelling in continuous spaces | Energy scalar is a direct unnormalized probability; no discretisation required |
| No self-verification | Energy function *is* the verifier; no external model needed |

Two variants are released: a **decoder-only EBT** (GPT-style, autoregressive) and a **bidirectional EBT** (BERT/DiT-style). Both use an optimization-based EBM objective rather than contrastive methods, avoiding the curse of dimensionality by implicitly regularising the energy landscape through gradient-descent training itself.

Training backpropagates through the entire optimisation process using Hessian-vector products. These second-order gradients scale linearly with model size — comparable to standard first-order backpropagation — but still impose meaningful overhead. Crucially, unlike diffusion models which predict the *gradient* of the energy (the score function), EBTs learn the energy function directly, enabling per-step self-verification without an external verifier.

### Energy Landscape Regularisation

Three techniques proved essential for strong System 2 Thinking to emerge:

1. **Replay buffer** — defines the energy landscape near minima, preventing mode collapse
2. **Langevin dynamics** — random noise perturbation encourages exploration of the energy landscape; disabling it improves single-path thinking but degrades combined thinking-plus-self-verification performance
3. **Randomised step size and number of optimisation steps** — improves generalisation across diverse optimisation paths; removing this nearly eliminates thinking gains in ablations

### Inference Modes

EBTs support two distinct System 2 Thinking modes at inference:

- **Thinking Longer** — increasing optimisation steps per prediction, analogous to chain-of-thought depth
- **Self-Verification / Best-of-N** — generating N candidate predictions and selecting the minimum-energy one, generalised to both discrete and continuous modalities without external supervision

---

## Results

### Scaling

EBTs achieve up to **35% higher scaling rate** than Transformer++ during pretraining across six axes — data, batch size, depth, parameters, FLOPs, and embedding dimension — the first architecture class to out-scale the standard recipe across multiple axes and modalities without modifying the tokenizer.

- Data and batch scaling for language: >30% higher scaling rate
- Width/parameter scaling for video: >33% higher scaling rate
- EBT video models scale more than 33% faster than Transformer++ on next-frame prediction

### Inference-Time Improvement

Standard Transformer++ gains **zero improvement** from additional forward passes at inference. EBTs improve language modelling perplexity by up to **29% more** through thinking (additional optimisation steps and self-verification).

Self-verification scales with data: the benefit of Best-of-5 sampling grows from 4–8% improvement to 10–14% as training data increases — suggesting substantially larger gains at foundation-model scale.

### Out-of-Distribution Generalisation

EBTs with slightly worse pretraining perplexity still outperform Transformer++ on most downstream tasks. There is a **strong linear relationship** between distributional shift magnitude and thinking benefit: the more OOD the evaluation data, the larger the perplexity improvement from System 2 Thinking — directly paralleling human reliance on deliberate cognition for novel situations.

Downstream comparisons (small scale, from scratch):
- GSM8K: EBT 43.3 vs. Transformer++ 49.6 (note: EBT slightly behind here, at much smaller scale)
- BigBench Elementary Math QA: EBT 72.6 vs. Transformer++ 79.8
- BigBench Dyck Languages: EBT 125.3 vs. Transformer++ 131.5

### Image Generation and Denoising

Bidirectional EBTs outperform Diffusion Transformers on both in-distribution and OOD image denoising (up to 3.5 dB PSNR improvement) while using **99% fewer forward passes**, and achieve approximately 10× higher ImageNet class-conditional generation quality at equivalent compute.

---

## Capabilities

- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] — System 2 Thinking emerges from purely unsupervised pretraining, generalising across discrete and continuous modalities without any RL or reward signal *(research only)*
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — EBTs are the first architecture class to out-scale Transformer++ across multiple training axes simultaneously *(research only)*
- [[themes/model_architecture|Model Architecture]] — Built-in coupled verifier-generator enables Best-of-N self-verification per individual prediction, not just per full sequence *(research only)*
- [[themes/scaling_laws|Scaling Laws]] — EBT scaling advantage compounds with data; self-verification benefit grows with training data scale *(research only)*
- Calibrated uncertainty estimation in continuous state spaces (per-token energy correlates with prediction difficulty; per-frame energy with scene unpredictability) without explicit supervision *(research only)*

---

## Limitations and Open Questions

### Architectural and Training Constraints

- **Incompatible with existing checkpoints.** EBTs must be trained from scratch — the architecture is incompatible with existing foundation models, blocking transfer learning and fine-tuning. Adoption requires matching or exceeding the training compute of existing models from a cold start.
- **Additional hyperparameters.** The optimisation process introduces step size and step count as hyperparameters whose misconfiguration frequently causes training instability.
- **Second-order compute overhead.** Hessian-vector products are required during backpropagation, making EBT training and inference more expensive than standard feed-forward models, even if the overhead scales linearly.

### Scale and Validation

- **Validated only to ~800M parameters.** All claims about foundation-model-scale advantages are extrapolations from controlled small-scale experiments (100B tokens, up to 800M parameters — roughly 1/1000th of modern foundation model training data and parameter count). The advantage may not hold at scale.
- **Thinking emergence requires sufficient data scale.** System 2 Thinking capabilities only emerge with large enough data, blocking evaluation of thinking at limited compute budgets.
- **No Chain-of-Thought baseline.** Because models are pretrained from scratch at small scale, EBT thinking results cannot be directly compared to chain-of-thought reasoning in large foundation models.

### Generative Modelling

- **Struggles with multi-modal distributions.** EBTs currently fail at class-conditional image generation and other tasks with many modes in the target distribution, likely because the convex energy landscape assumption is violated. This is a significant gap for generative applications.

### Data Constraints

- **Video data scarcity.** Current video datasets are too small relative to text corpora, requiring repeated training epochs and making data exhaustion a near-term constraint for video EBT scaling — fundamentally different from the data-abundant text regime.

---

## Relationship to Broader Themes

### System 2 Thinking as Architecture, Not Fine-Tuning

The core claim that [[themes/test_time_compute_scaling|inference-time compute scaling]] can emerge from unsupervised pretraining — without RL, verifiable rewards, or modality-specific design — is a significant architectural position. It argues that the bottleneck blocking general-purpose System 2 Thinking is not data or compute but *architectural inexpressivity*: standard feed-forward architectures cannot self-verify and cannot allocate variable compute per prediction.

If this holds at scale, it repositions [[themes/reasoning_and_planning|reasoning capabilities]] as an emergent property of architecture choice rather than a post-hoc training regime, with implications for how we evaluate and compare reasoning approaches.

### Transformer Alternatives at Scale

EBTs are positioned within the [[themes/transformer_alternatives|transformer alternatives]] landscape as the first energy-based architecture to demonstrate competitive — and in some axes superior — [[themes/scaling_laws|scaling behaviour]] relative to the Transformer++. The historical failure mode of EBMs (contrastive training instability) is addressed by the optimisation-based objective, but the multimodal distribution limitation suggests EBTs are not a drop-in replacement for generative modelling use cases.

### Verifier-Generator Coupling

A recurring tension in current AI systems is the separation between generation and verification — a model generates candidates, a separate model scores them. EBTs collapse this into a single coupled system. The theoretical motivation (verifying solutions is exponentially easier than generating them; verifiers generalise better than generators) is established; the practical question is whether the EBT training regime successfully teaches the energy function to serve as a reliable verifier at scale.

---

## Open Questions

1. Do the scaling advantages hold beyond 800M parameters and 100B tokens, or is there a regime where the second-order compute overhead outweighs the scaling rate benefit?
2. Can the convex energy landscape constraint be relaxed (e.g., via mixture-of-experts energy functions or normalising flow priors) to handle class-conditional and diverse generative tasks?
3. Does the linear relationship between OOD shift and thinking benefit persist at foundation model scale, and if so, what does this imply for deployment in highly novel domains?
4. Is there a path from a pretrained Transformer++ to an EBT that avoids full from-scratch training — e.g., using the Transformer++ as an initialised feature extractor with a learned energy head?
5. As training data scale increases and self-verification benefit grows (4–8% → 10–14% with more data), what is the asymptotic ceiling, and does it eventually match or exceed chain-of-thought gains in large RL-trained reasoning models?

---

*Themes: [[themes/model_architecture|Model Architecture]] · [[themes/pretraining_and_scaling|Pretraining and Scaling]] · [[themes/reasoning_and_planning|Reasoning and Planning]] · [[themes/scaling_laws|Scaling Laws]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] · [[themes/transformer_alternatives|Transformer Alternatives]]*

## Key Concepts

- [[entities/diffusion-transformer-dit|Diffusion Transformer (DiT)]]
- [[entities/gsm8k|GSM8K]]
- [[entities/imagenet-1k|ImageNet-1K]]
- [[entities/replay-buffer|Replay Buffer]]
- [[entities/squad|SQuAD]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/self-verification|Self-Verification]]
- [[entities/transformer|Transformer++]]
