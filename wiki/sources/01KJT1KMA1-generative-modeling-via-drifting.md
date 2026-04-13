---
type: source
title: Generative Modeling via Drifting
source_id: 01KJT1KMA1W14HTT19W306GYQV
source_type: paper
authors:
- Mingyang Deng
- He Li
- Tianhong Li
- Yilun Du
- Kaiming He
published_at: '2026-02-04 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- model_architecture
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Generative Modeling via Drifting

**Authors:** Mingyang Deng, He Li, Tianhong Li, Yilun Du, Kaiming He
**Published:** 2026-02-04 00:00:00
**Type:** paper

## Analysis

# Generative Modeling via Drifting
2026-02-04 · paper · Mingyang Deng, He Li, Tianhong Li, Yilun Du, Kaiming He
https://arxiv.org/pdf/2602.04770

---

### Motivation & Prior Limitations
Prevailing generative paradigms — diffusion and flow-based models — perform their core distribution-matching work iteratively at inference time, requiring multiple expensive network evaluations (NFE) to generate a single sample.
- Existing single-step methods derived from these paradigms (distillation-based or from-scratch approaches such as iCT, Shortcut, MeanFlow) still depend on SDE/ODE trajectory approximations, inheriting the conceptual baggage of differential-equation formulations even when reduced to one step.
  - The best prior 1-NFE result on ImageNet 256×256 in latent space was iMeanFlow at FID 1.72; in pixel space, GANs such as StyleGAN-XL achieved FID 2.30 but required 1574G FLOPs per sample.
- No prior framework reframes iterative neural network training itself as the mechanism for distribution evolution, leaving a conceptual gap between how models are trained (iterative optimization) and how they generate (iterative inference).

---

### Proposed Approach
Drifting Models shift the iterative pushforward of distributions from inference time to training time: the single-pass generator f learns by having its output distribution q evolved toward the data distribution p across training iterations, so that at inference only one forward pass is needed.
- A **drifting field** V_{p,q}(x) governs how generated samples should move at each training step; it is defined to be anti-symmetric (V_{p,q} = −V_{q,p}), which guarantees equilibrium (V = 0) exactly when q = p, without adversarial optimization.
  - The field is instantiated as attraction toward data samples minus repulsion from generated samples using a mean-shift-inspired kernel k(x,y) = exp(−‖x−y‖/τ), computed via a softmax over negative samples analogous to InfoNCE.
  - The training loss minimizes ‖V‖² via a stop-gradient fixed-point formulation (following SimSiam/EDM style): the network prediction is regressed toward a frozen target x + V(x), avoiding the need to back-propagate through the distribution.
- To handle high-dimensional image data, the drifting loss is computed in a **feature space** using a pre-trained self-supervised encoder (latent-MAE, MoCo, SimCLR) across multiple scales, rather than raw pixel space — the encoder is used only at training time and does not affect one-step inference.
- **Classifier-free guidance** is integrated as a training-time behavior: negative samples are drawn from a mixture of generated and unconditional real data, parameterized by a mixing rate γ, preserving the 1-NFE property at inference while allowing CFG scale to be varied post-training.

---

### Results & Capabilities
Drifting Models achieve state-of-the-art 1-NFE FID of **1.54** on ImageNet 256×256 in latent space (L/2 model, 463M generator parameters), surpassing all prior single-step methods trained from scratch.
- In latent space, the Base-size Drifting Model (133M params, FID 1.75) matches or beats prior XL-size (675M) single-step models including MeanFlow (3.43), AdvFlow (2.38), and iMeanFlow (1.72).
- In pixel space without a VAE tokenizer, the L/16 Drifting Model achieves FID **1.61** using only 87G FLOPs, outperforming StyleGAN-XL (2.30 FID, 1574G FLOPs) and matching multi-step pixel-space diffusion methods such as PixelDiT (1.61 FID, 200 NFE).
- Applied to robotic control (Diffusion Policy benchmark), the 1-NFE Drifting Policy matches or exceeds the 100-NFE Diffusion Policy baseline across most of 6 tasks (e.g., ToolHang State: 0.38 vs. 0.30; Can State: 0.98 vs. 0.96), demonstrating generality beyond image generation.
- Ablations confirm that anti-symmetry of V is critical: breaking it by even a 1.5× imbalance between attraction and repulsion raises FID from 8.46 to over 40 on the B/2 ablation model.
- Feature encoder quality is a key determinant: scaling the latent-MAE encoder width from 256 to 640 and pre-training epochs from 192 to 1280 reduces FID from 8.46 to 4.28, and adding classifier fine-tuning further drops it to 3.36.

---

### Implications
Drifting Models establish a new conceptual axis for generative modeling: rather than using iterative inference to decompose a hard mapping, training iteration itself serves as the distribution-evolution mechanism, opening a path toward architecturally simple, high-quality one-step generators that do not inherit the SDE/ODE framework.
- The strong performance of a Base-size Drifting Model against XL-size diffusion models suggests that the training paradigm — not parameter count — may be a primary driver of generation quality in the single-step regime, with implications for compute-efficient generative systems.
- The formal connection to contrastive learning (positive/negative samples, InfoNCE-style softmax, dependence on feature encoder quality) suggests that advances in self-supervised representation learning directly improve generation quality in this framework, creating a tight coupling between the two research areas relevant to representation_learning.
- The feature-space drifting loss is orthogonal to latent-space generation (the generator can be latent while the encoder operates in pixel space), making the framework composable with existing tokenizer and VAE infrastructure.
- The robotics result indicates that Drifting Models can substitute for diffusion-based policy generators in embodied AI without domain-specific modification, with potential for real-time control applications that are currently bottlenecked by multi-step inference.

---

### Remaining Limitations & Next Steps
The theoretical guarantee only runs in one direction: q = p implies V = 0, but the converse (V → 0 implies q → p) does not hold in general, and the identifiability argument provided is a heuristic relying on non-degeneracy assumptions rather than a formal proof.
- The authors explicitly state: "it remains unclear 

## Key Claims

1. Drifting Models achieve a new state-of-the-art 1-NFE FID of 1.54 on ImageNet 256x256 in latent space among single-step methods.
2. Drifting Models achieve 1.61 FID on ImageNet 256x256 in pixel space with a single function evaluation, outperforming or competing with previous multi-step pixel-space methods.
3. Drifting Models shift the iterative pushforward evolution from inference time to training time, enabling native single-step generation without SDE/ODE formulations.
4. Anti-symmetry of the drifting field is a necessary condition for achieving equilibrium; breaking it causes catastrophic failure in generation quality.
5. A drifting field with anti-symmetry property guarantees that when the generated distribution q matches the data distribution p, all drift becomes zero, achieving equilibrium.
6. The drifting field is designed as an attraction-repulsion mechanism: generated samples are attracted toward the data distribution and repelled from the current generated distribution.
7. The drifting model cannot be made to work on ImageNet without a feature encoder; raw pixel/latent kernel similarity is insufficient for effective training.
8. Larger positive and negative sample sets improve generation quality under fixed training compute budgets, analogous to findings in contrastive representation learning.
9. Classifier-free guidance in Drifting Models is a training-time behavior implemented by mixing negative samples from different class distributions, preserving 1-NFE inference.
10. The Drifting Model's Base-size (133M parameter) variant is competitive with previous XL-size single-step models trained from scratch.

## Capabilities

- One-step (1-NFE) class-conditional image generation on ImageNet 256×256 in latent space achieving FID 1.54, surpassing all previous single-step methods trained from scratch and competitive with 250-step diffusion/flow models
- One-step (1-NFE) pixel-space image generation on ImageNet 256×256 achieving FID 1.61, outperforming all prior single-step methods and matching competitive multi-step diffusion models while using 18× fewer FLOPs than StyleGAN-XL
- One-step (1-NFE) generative action policy for robot manipulation matching or exceeding 100-step Diffusion Policy across diverse single-stage and multi-stage tasks
- Base-size (133M parameter) one-step image generator competitive with XL-size (675M parameter) one-step models, demonstrating strong parameter efficiency via the drifting paradigm

## Limitations

- Theoretical guarantee is incomplete: minimizing the drifting field (V→0) does not provably imply distribution matching (q→p) in the general case; convergence depends on uncharacterized sufficient conditions
- Method requires a strong pretrained feature encoder to function on high-dimensional data; without any feature encoder, Drifting Models cannot generate quality images on ImageNet
- Generation quality has a hard ceiling determined by feature encoder quality: FID degrades from 3.36 to 11.05 when switching from a fine-tuned latent-MAE to a standard SimCLR encoder
- No results beyond 256×256 resolution; scaling to 512×512 or higher — where commercial diffusion models routinely operate — is unvalidated
- All experiments are class-conditional on ImageNet; text-conditional or open-vocabulary generation is entirely absent, leaving the method's applicability to modern text-to-image use cases unknown
- Method is critically sensitive to anti-symmetry in the drifting field: intentionally breaking it causes catastrophic performance collapse (FID rises from 8.46 to 41–177), indicating a fragile architectural constraint
- Training requires large positive and negative sample batches for accurate V estimation; FID degrades from 8.46 to 20.43 when Npos drops from 64 to 1, implying substantial memory and compute requirements at scale
- Robotics experiments omit the feature space that image generation requires, applying drifting loss directly on raw control representations; the boundary conditions determining when a feature encoder is necessary versus optional are uncharacterized
- Design decisions for drifting field, kernel functions, feature encoder, and generator architecture are acknowledged as potentially sub-optimal; the method's current results are unlikely to represent a ceiling but the design space is poorly understood

## Bottlenecks

- Drifting Models require a strong pretrained SSL encoder to function; no such encoders exist for many target domains (video, audio, scientific data), blocking adoption of the paradigm beyond static image generation
- Absence of proof that V→0 implies q→p in general prevents principled design of drifting fields and formal guarantees about training convergence or distributional coverage

## Breakthroughs

- Drifting Models achieve FID 1.54 in a single inference step on ImageNet 256×256 without distillation from any pretrained model, surpassing all prior from-scratch one-step methods and matching 250-step diffusion/flow models

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/model_architecture|model_architecture]]

## Key Concepts

- [[entities/classifier-free-guidance-cfg|Classifier-Free Guidance (CFG)]]
- [[entities/diffusion-policy|Diffusion Policy]]
- [[entities/fid|FID]]
- [[entities/flow-matching|Flow Matching]]
