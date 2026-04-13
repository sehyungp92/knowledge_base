---
type: source
title: Evolution Strategies at the Hyperscale
source_id: 01KJT7VEK3FBEDGCWJ1VC36NCT
source_type: paper
authors:
- Bidipta Sarkar
- Mattie Fellows
- Juan Agustin Duque
- Alistair Letcher
- Antonio León Villares
- Anya Sims
- Clarisse Wibault
- Dmitry Samsonov
- Dylan Cope
- Jarek Liesen
- Kang Li
- Lukas Seier
- Theo Wolf
- Uljad Berdica
- Valentin Mohl
- Alexander David Goldie
- Aaron Courville
- Karin Sevegnani
- Shimon Whiteson
- Jakob Nicolaus Foerster
published_at: '2025-11-20 00:00:00'
theme_ids:
- model_architecture
- policy_optimization
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Evolution Strategies at the Hyperscale

**Authors:** Bidipta Sarkar, Mattie Fellows, Juan Agustin Duque, Alistair Letcher, Antonio León Villares, Anya Sims, Clarisse Wibault, Dmitry Samsonov, Dylan Cope, Jarek Liesen, Kang Li, Lukas Seier, Theo Wolf, Uljad Berdica, Valentin Mohl, Alexander David Goldie, Aaron Courville, Karin Sevegnani, Shimon Whiteson, Jakob Nicolaus Foerster
**Published:** 2025-11-20 00:00:00
**Type:** paper

## Analysis

# Evolution Strategies at the Hyperscale
2025-11-20 · paper · Bidipta Sarkar, Mattie Fellows, Juan Agustin Duque, Alistair Letcher, Antonio León Villares et al. (20 total)
https://arxiv.org/pdf/2511.16652

---

### Motivation & Prior Limitations
Evolution Strategies (ES) are theoretically attractive for large-scale training — they are gradient-free, parallelisable, and can handle non-differentiable or discrete objectives — but naïve ES is computationally infeasible at billion-parameter scale on modern GPU hardware.
- The core bottleneck is arithmetic intensity: naïve ES requires generating full-rank matrix perturbations that replicate the entire parameter set per population member, then evaluating each via a separate batched matrix multiplication sequence, which has inherently low arithmetic intensity (the ratio of FLOPs to memory traffic).
  - In billion-parameter regimes, memory inflation and low-intensity matrix ops dominate wall-clock time, limiting practical ES to small models and small populations (prior work used population sizes on the order of hundreds, with Salimans et al. 2017 maxing at 1,440).
- Prior attempts to use ES for LLM fine-tuning (MeZO, Yu et al., Korotyshova et al., Qiu et al.) either used two-point zeroth-order estimators unsuitable for pretraining, required SFT warm-starts before applying ES, or capped population sizes at ~100 due to throughput constraints — meaning each perturbation was evaluated across hundreds of rollouts to amortise GPU cost rather than using maximally diverse populations.
- Backpropagation, the standard alternative, requires gradient communication across devices, special handling for low-precision datatypes, and is inapplicable to truly non-differentiable architectures (e.g., pure integer models, symbolic modules, discrete parametrisations).

---

### Proposed Approach
EGGROLL (Evolution Guided GeneRal Optimisation via Low-rank Learning) restructures ES perturbations as rank-*r* matrices — analogous to LoRA adapters in gradient-based training — enabling highly efficient batched evaluation on GPUs without restricting the overall parameter update to be low-rank.
- Instead of sampling a full-rank perturbation matrix E ∈ ℝ^{m×n}, EGGROLL samples A ∈ ℝ^{m×r} and B ∈ ℝ^{n×r} with r ≪ min(m,n) and forms E = (1/√r)AB^⊤, reducing auxiliary storage from mn to (m+n)r per layer.
  - The key hardware insight is that the forward pass decomposes as u(M + σE)^T = uM^T + (σ/√r)(uB)A^T, preserving the efficient general matrix multiplication for the base weights while adding cheap low-rank work per perturbation — exactly the structure exploited by batched LoRA inference systems like vLLM.
  - A counter-based deterministic RNG reconstructs noise on demand so perturbation matrices never need to persist in memory; workers share only scalar fitness values.
- The overall EGGROLL parameter update is the weighted average of N rank-r matrices, giving rank min(Nr, m, n) — which in all reported experiments exceeds min(m,n), making the cumulative update full-rank despite individual perturbations being low-rank.
- EGGROLL uses the Gaussian score function (Ŝ(E) = −E) as a tractable approximation, motivated by the central limit theorem: AB^⊤ is a sum of independent outer products, so its distribution converges to Gaussian N(0, I_m, I_n) as r increases.
- For the theoretical analysis, the paper proves convergence of general Gaussian ES in high dimensions, identifying three regimes (linearisation, critical, divergence) gated by a critical noise scaling σ_d = o(d^{-1/2}), and separately proves EGGROLL converges to the true ES gradient at rate O(r^{-1}) — faster than the O(r^{-1/2}) generic CLT rate due to symmetry cancelling all odd cumulants.

---

### Results & Capabilities
EGGROLL achieves up to 91% of the throughput of pure batch inference (versus 34% for PPO and 0.41% for naïve OpenES), representing a >100× training speed improvement for billion-parameter models at large population sizes.
- **Pretraining integer models (training_infrastructure / architectural_innovation):** EGGROLL stably pretrains EGG, a nonlinear RNN language model operating entirely in int8 with no explicit activation functions (implicit nonlinearity from integer clipping), achieving 3.40 bits/byte on character-level prediction versus 3.58 bits/byte for a fp32 Transformer trained with backprop SGD — a feat requiring population sizes up to 2^{20} = 1,048,576, three orders of magnitude beyond Salimans et al. 2017, on a single GPU.
- **Reinforcement learning (reinforcement_learning):** Across 16 tabula rasa RL environments (Navix, Craftax, Brax, Kinetix, Jumanji) using a fixed 3-layer MLP policy, EGGROLL matches or outperforms OpenES on 14/16 environments, outperforms on 7/16, and delivers substantial wall-clock speedups due to batched low-rank structure; it also demonstrates competitive multi-agent RL (MARL) performance.
- **LLM post-training / reasoning (reinforcement_learning / self_play_and_expert_iteration):** On the countdown task with RWKV-7 1.5B, EGGROLL converges to 35% validation accuracy versus GRPO's 23% given equal wall-clock time, by allowing 1,024 parallel generations per GPU (1,048,576 total at scale) versus GRPO's 64. On GSM8K with RWKV-7 7B across 8 GPUs, EGGROLL outperforms GRPO in validation score. On AIME24/25 using a 14B RWKV-7 model fine-tuned for 12 hours on 32 GPUs, accuracy improves from 13% → 30% (AIME24) and 7% → 33% (AIME25).
- **Quantised model fine-tuning:** EGGROLL successfully performs model distillation into int8-quantised RWKV-7 7B models using KL-divergence fitness, recovering partial GSM8K problem-solving capability from a baseline of zero — a task impossible with gradient-based methods that cannot differentiate through quantisation.
- **GRPO limitation bypass:** EGGROLL can directly optimise pass@k (a known limitation of GRPO) and is feasible for 14B parameter models where GRPO is memory-infeasible due to Adam optimizer state.

---

### Implications
EGGROLL reposition

## Key Claims

1. Naive Evolution Strategies (ES) becomes prohibitively expensive at scale on GPUs due to low arithmetic intensity of batched matrix multiplications with unstructured random perturbations.
2. EGGROLL achieves a hundredfold increase in training speed for billion-parameter models at large population sizes compared to standard ES.
3. EGGROLL achieves up to 91% of the throughput of pure batch inference.
4. EGGROLL enables stable pretraining of nonlinear recurrent language models that operate purely in integer datatypes.
5. EGGROLL is competitive with GRPO for post-training LLMs on reasoning tasks.
6. EGGROLL does not compromise performance compared to ES in tabula rasa RL settings despite being faster.
7. ES does not require differentiability and can optimize a broader class of models including those with discrete parametrisations.
8. ES is highly amenable to parallel scaling because fitness evaluations are independent across population members and require only communication of scalar fitnesses, yielding near-linear speedups on lar
9. Backpropagation requires special care when training models with low-precision datatypes, whereas ES can directly optimize any model with the same datatypes used at inference time.
10. Naïve ES requires generating full-rank matrix perturbations that replicate the entire parameter set for every population member, inflating memory costs and forcing frequent movement of large weight te

## Capabilities

- EGGROLL achieves up to 91% of pure batch inference throughput for ES training of billion-parameter models — a ~221x speedup over naive ES — by structuring perturbations as low-rank matrices and reusing base activations across population members
- Stable pretraining of nonlinear RNN language models that operate entirely in int8 integer datatypes, with no explicit activation functions — enabled by ES avoiding gradient requirements on low-precision arithmetic
- ES-based LLM fine-tuning (EGGROLL) matches or exceeds GRPO on reasoning benchmarks including GSM8K and countdown, while supporting larger parallel populations per GPU
- ES population sizes of over one million (2^20 = 1,048,576) simultaneously evaluated on a single GPU, three orders of magnitude larger than prior ES work
- Direct optimization of pass@k objectives via ES — not achievable with GRPO due to its variance-reduction assumptions — enabling training signals from population-level pass rates
- Gradient-free distillation of integer-quantized (int8) LLMs from full-precision teacher models, allowing quantized models to recover reasoning capability without backpropagation through discrete operations
- RWKV-7 14B parameter model fine-tuned via EGGROLL improves AIME24 accuracy from 13% to 30% and AIME25 from 7% to 33%, in a regime where GRPO is infeasible due to Adam optimizer memory cost

## Limitations

- ES pretraining with sufficiently large populations requires approximately 180x more GPU-hours than backpropagation baseline — compute parity with gradient-based methods is not achieved for pretraining
- Small-population ES (population size ~2, analogous to MeZO) completely fails at language model pretraining — large populations are a necessary condition, not an optional efficiency enhancement
- The EGG character-level language model only marginally outperforms a backprop-trained Transformer (3.40 vs 3.58 bits/byte) while consuming ~180x more GPU-hours — ES pretraining is compute-inefficient relative to gradient descent for language modeling
- EGGROLL convergence in high dimensions requires the noise scale σ to decay as o(d^{-1/2}) with parameter dimension — if this critical rate is violated, ES updates can diverge for smooth objectives
- EGGROLL underperforms naive OpenES on 2 out of 16 tabula rasa RL environments — the low-rank perturbation structure is not universally beneficial and may hurt exploration in some task geometries
- ES pretraining is only demonstrated at small model scale (6-layer, 256-dim hidden, character-level language modeling) — scalability of ES pretraining to frontier-scale models (billions of parameters) is not empirically validated
- GRPO and Adam-based RL fine-tuning are infeasible at >14B parameter scales due to optimizer state memory — limiting standard gradient-based RLHF/RLVR approaches to smaller models
- End-to-end neurosymbolic training via EGGROLL — training neural networks that interface with non-differentiable symbolic modules — is proposed as future work only, with no empirical demonstration in the paper
- Theoretical convergence guarantees for EGGROLL assume NTK-regime parametrization (weights scaled by d^{-1/2}) — standard architectures not in the NTK regime may not satisfy the required Lipschitz conditions on the Hessian
- ES and EGGROLL are restricted to mean-seeking optimization over a Gaussian population — they recover a linearized first-order gradient in high dimensions, losing access to higher-order curvature information that could accelerate convergence in low-dimensional or structured problems

## Bottlenecks

- Low arithmetic intensity of naive ES batched matrix multiplications blocks practical gradient-free training of billion-parameter models on GPU hardware — each population member requires a separate matrix-vector multiplication with an upper bound of 1 on arithmetic intensity regardless of population 
- ES pretraining compute overhead (~180x GPU-hours vs backprop) blocks practical adoption of ES as a general pretraining method — the efficiency gap makes pretraining frontier models via ES economically infeasible without dedicated infrastructure
- Gradient computation requirement in backpropagation blocks training of architectures with non-differentiable components (integer datatypes, discrete operations, symbolic modules, cellular automata) at billion-parameter scale

## Breakthroughs

- EGGROLL makes gradient-free evolutionary optimization practical at billion-parameter scale by achieving 91% of pure batch inference throughput — closing the ~200x compute gap between ES and gradient-based methods for large models
- Stable pretraining of a language model operating entirely in int8 integer datatypes via EGGROLL — the first demonstration that a language model can be trained from scratch at inference precision without floating-point arithmetic

## Themes

- [[themes/model_architecture|model_architecture]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/lora|LoRA]]
