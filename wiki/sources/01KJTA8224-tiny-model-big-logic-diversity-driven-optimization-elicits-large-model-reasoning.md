---
type: source
title: 'Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning
  Ability in VibeThinker-1.5B'
source_id: 01KJTA8224N9N2ACQDG5KN4HQ9
source_type: paper
authors:
- Sen Xu
- Yi Zhou
- Wei Wang
- Jixin Min
- Zhibin Yin
- Yingwei Dai
- Shixi Liu
- Lianyu Pang
- Yirong Chen
- Junlin Zhang
published_at: '2025-11-09 00:00:00'
theme_ids:
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B

**Authors:** Sen Xu, Yi Zhou, Wei Wang, Jixin Min, Zhibin Yin, Yingwei Dai, Shixi Liu, Lianyu Pang, Yirong Chen, Junlin Zhang
**Published:** 2025-11-09 00:00:00
**Type:** paper

## Analysis

# Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B
2025-11-09 · paper · Sen Xu, Yi Zhou, Wei Wang, Jixin Min, Zhibin Yin et al. (10 total)
https://arxiv.org/pdf/2511.06221

---

### Motivation & Prior Limitations
The prevailing industry consensus holds that scaling model parameters is necessary for robust reasoning, with frontier models like DeepSeek R1 (671B) and Kimi K2 (>1T) representing the dominant approach, while compact models (≤1.5B) are widely considered incapable of matching their logical reasoning performance.
- The conventional SFT-then-RL pipeline is suboptimal because SFT is trained to maximize single-shot accuracy (Pass@1), which artificially constrains the exploration space available to the subsequent RL phase and caps the performance ceiling RL can reach.
  - Models fine-tuned on Qwen2.5-Math-1.5B using standard methods typically score in the single digits on AIME24 (e.g., Dynamic Fine-Tuning achieves 6.87), suggesting prior post-training methodologies fail to unlock the model's latent reasoning capacity.
- Extreme parameter scaling concentrates frontier AI research within a handful of resource-rich companies (OpenAI, Anthropic, Google, xAI), marginalizing universities and smaller organizations that possess talent but lack compute.
  - Training DeepSeek R1 costs ~$294K and MiniMax-M1 ~$535K, compared to the base model's 0.0 scores on coding benchmarks, illustrating the steep barrier to entry under the scaling paradigm.
- Prior small reasoning models (DeepScaleR, ProRL, Qwen3-1.7B) showed promise but had not fully demonstrated reasoning parity with large models, particularly on competition-level mathematics and coding benchmarks.

---

### Proposed Approach
The paper introduces the Spectrum-to-Signal Principle (SSP), a post-training framework that decouples SFT and RL into complementary roles: SFT maximizes output diversity (the "Spectrum Phase") and RL amplifies the correct signal from that diverse pool (the "Signal Phase"), in contrast to conventional pipelines where both stages optimize for Pass@1.
- Unlike standard SFT which targets a single best answer, the Spectrum Phase employs Two-Stage Diversity-Exploring Distillation: (1) Domain-Aware Diversity Probing partitions the mathematical domain into N=4 subdomains (algebra, geometry, calculus, statistics), trains intermediate checkpoints, and selects the specialist checkpoint maximizing Pass@K per subdomain; (2) Expert Model Fusion merges these specialists via unweighted parameter averaging (w_i = 1/N) into a single unified SFT model with maximized solution diversity.
  - The core theoretical claim is that a high-Pass@K SFT checkpoint provides a richer candidate space for RL to search, raising the upper bound on what RL can achieve compared to a high-Pass@1 but low-diversity checkpoint.
- The RL phase uses MaxEnt-Guided Policy Optimization (MGPO), which extends GRPO by weighting the advantage of each training problem by its entropy deviation from the maximum-uncertainty state (p_c(q) = 0.5), using the KL divergence from the observed accuracy to the ideal 0.5 distribution.
  - Problems where the model is close to 50% accuracy receive the highest weight (exp(-λ · D_ME)), while problems that are nearly always correct or nearly always wrong are suppressed; this creates an implicit curriculum that dynamically steers gradient updates toward the model's current learning frontier.
  - When λ=0, MGPO degrades to standard GRPO, making the entropy-weighting an additive mechanism rather than a replacement architecture.
- Training proceeds in staged context windows (16K → 32K for math, then code), and data decontamination uses 10-gram matching to exclude training samples semantically overlapping with evaluation sets.

---

### Results & Capabilities
VibeThinker-1.5B surpasses the 400× larger DeepSeek R1-0120 (671B) on three competition mathematics benchmarks: AIME24 (80.3 vs. 79.8), AIME25 (74.4 vs. 70.0), and HMMT25 (50.4 vs. 41.7), all measured as average pass rate over 64 samples, at a total training cost of $7,800 (3,900 H800 GPU-hours at $2/hour).
- This represents a dramatic improvement over the base model (Qwen2.5-Math-1.5B), which scored 6.7/4.3/0.6 on AIME24/AIME25/HMMT25 respectively, and 0.0 on both LiveCodeBench V5 and V6.
- On coding, VibeThinker-1.5B achieves 55.9 on LiveCodeBench V5 and 51.1 on LiveCodeBench V6, slightly exceeding Magistral Medium's 50.3, and substantially outperforming GPT-4.1 on coding (51.1 vs. 44.7).
- Among sub-3B models, VibeThinker-1.5B leads by a large margin: it more than doubles Qwen3-1.7B's AIME25 score (74.4 vs. 36.8) and LiveCodeBench V6 score (51.1 vs. 26.9), and more than doubles SmolLM-3 3B's AIME25 score (74.4 vs. 36.7) despite having fewer parameters.
- Against top-tier non-reasoning models with 100–700× more parameters (Kimi K2, DeepSeek V3, GPT-4.1, Claude Opus 4, Gemini 2.5 Flash), VibeThinker-1.5B surpasses all on AIME24 and AIME25 mathematics benchmarks.
  - The base model's 0.0 coding score rising to 51.1 through post-training, combined with strong performance on 2025 benchmarks (AIME25, HMMT25) that postdate the base model's training cutoff, is presented as evidence against data contamination as an explanation for the results.
- The fused SFT model (MSFT_Merge) achieves simultaneous improvements on both Pass@K (diversity) and Pass@1 (accuracy), contradicting the assumption that diversity optimization trades off against single-answer accuracy.

---

### Implications
The central finding—that a 1.5B model trained for $7,800 can match or exceed reasoning performance of models 100–600× larger—directly challenges the dominant scaling law narrative for reasoning tasks, suggesting that algorithmic innovation in post-training can substitute for raw parameter scale in the reasoning regime.
- If small models can achieve reasoning parity through better training methodology rather than more parameters, the effective compute fron

## Key Claims

1. VibeThinker-1.5B (1.5B parameters) surpasses DeepSeek R1 (671B, over 400x larger) on AIME24 with a score of 80.3 vs. 79.8
2. VibeThinker-1.5B surpasses DeepSeek R1 on AIME25 with a score of 74.4 vs. 70.0
3. VibeThinker-1.5B surpasses DeepSeek R1 on HMMT25 with a score of 50.4 vs. 41.7
4. VibeThinker-1.5B achieves a score of 51.1 on LiveCodeBench V6, outperforming Magistral Medium's 50.3, despite its base model scoring 0.0 on the same benchmark
5. VibeThinker-1.5B was trained at a total computational cost of approximately $7,800, consuming approximately 3,900 GPU hours on NVIDIA H800 GPUs
6. VibeThinker-1.5B's post-training cost is 1/30 to 1/60 of DeepSeek R1 ($294K) and MiniMax-M1 ($535K)
7. Inference costs for the 1.5B parameter VibeThinker model are 20 to 70 times lower than state-of-the-art large-scale models
8. The prevailing industry consensus holds that scaling model parameters—as exemplified by DeepSeek R1 (671B), Kimi-K2, and Qwen3-Max (>1T)—is essential for enhancing logical reasoning capabilities, with
9. The Spectrum-to-Signal Principle (SSP) redefines the SFT-RL pipeline by assigning distinct complementary objectives: SFT maximizes diversity (Pass@K) as a 'spectrum phase', while RL amplifies correct 
10. The prevailing implicit assumption in the field—to select the SFT checkpoint maximizing Pass@1 accuracy before applying RL—is suboptimal because it artificially constrains the performance ceiling for 

## Capabilities

- A 1.5B-parameter model (VibeThinker-1.5B) trained via the Spectrum-to-Signal Principle achieves math reasoning scores that surpass models 400x larger — AIME24 80.3 vs. DeepSeek R1's 79.8, AIME25 74.4 vs. 70.0, HMMT25 50.4 vs. 41.7 — demonstrating that frontier-level reasoning is achievable without e
- The Spectrum-to-Signal Principle (SSP) decouples SFT and RL into complementary objectives — SFT maximises Pass@K (solution diversity) via subdomain-specialist model merging, while RL amplifies the correct signal via MaxEnt-Guided Policy Optimization — producing frontier reasoning in compact models v
- MaxEnt-Guided Policy Optimization (MGPO) dynamically up-weights RL training on problems where the model's empirical pass rate is near 0.5 (maximum entropy / maximum uncertainty), creating an implicit curriculum that concentrates gradient updates at the model's current learning frontier
- Post-training a 1.5B reasoning model for under $8K achieves benchmark performance previously requiring $294K–$535K, enabling frontier-competitive math reasoning at academic budgets and potentially democratising access to large-model-quality reasoning
- 1.5B reasoning models support deployment on edge devices (mobile phones, vehicle-embedded systems) at 20–70x lower inference cost than large-scale state-of-the-art models, making on-device competitive-level math and code reasoning feasible

## Limitations

- Small models (1.5B scale) face a substantial, potentially inherent capacity ceiling for general world knowledge — VibeThinker-1.5B scores 46.7 on GPQA-Diamond versus 76.8–82.8 for frontier models, a 20–40 point gap that persists across all comparisons regardless of reasoning methodology
- The entire SSP/MGPO methodology is validated only on domains with verifiable binary reward signals (math, code) — applicability to open-ended reasoning, instruction following, dialogue, or knowledge-intensive tasks is untested and structurally uncertain, since MGPO requires computable pass-rate entr
- Coding performance is hard-gated by base model pretraining coverage — the math-only pretraining of Qwen2.5-Math-1.5B produced a base scoring 0.0 on LiveCodeBench, and despite post-training improvements (0.0→55.9/51.1), a visible gap versus large models on coding remains (DeepSeek R1 scores 65.9 on L
- VibeThinker-1.5B is explicitly not a deployable system — no evaluation of instruction following, safety alignment, multi-turn dialogue, refusal behaviour, or production robustness is presented; the entire evaluation is confined to benchmark pass rates on math, code, and GPQA
- Benchmark performance is reported as average pass rate over 64 samples per math problem (Pass@64 averaged), not single-pass greedy generation — this significantly inflates apparent performance relative to single-query production use, where only one response is generated
- Extremely long reasoning chains at inference — maximum response length of 40K tokens, with math evaluation generating 64 samples per problem — creates substantial per-query inference cost and latency even for a 1.5B model, partially undermining the edge deployment and cost efficiency claims
- Expert Model Fusion uses uniform equal-weight averaging across subdomain specialist checkpoints — no principled method for optimal weight selection is provided, leaving performance potentially below what task-adaptive or learned fusion weights could achieve
- Benchmark contamination in base models is an unresolved field-wide concern — while the authors present evidence their results are not contamination artifacts, the underlying debate about Qwen2.5-Math and other widely-used bases remains open and affects interpretation of all derivative models

## Bottlenecks

- Small model parameter count creates a hard knowledge storage ceiling that post-training methodology cannot overcome — even frontier-level reasoning training leaves a 20–40 point GPQA gap versus large models, blocking deployment of efficient small models in knowledge-intensive production tasks
- The most effective post-training reasoning methodology (SSP + MGPO) requires verifiable binary reward signals, restricting its application to constrained domains with automated ground-truth checkers and blocking generalisation of small-model reasoning gains to open-ended or knowledge-intensive tasks

## Breakthroughs

- A 1.5B-parameter model (VibeThinker-1.5B) surpasses a 671B-parameter model (DeepSeek R1) on three competitive math benchmarks through post-training methodology innovation alone, trained at 1/37th the cost ($7.8K vs. $294K), empirically falsifying the consensus that reasoning performance is primarily
- The Spectrum-to-Signal Principle (SSP) establishes that decoupling SFT and RL into complementary objectives — diversity maximisation (Pass@K) then signal amplification — produces better outcomes than the implicit industry standard of optimising both phases for Pass@1, while simultaneously maximising

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/long-chain-of-thought|Long Chain-of-Thought]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/passk|pass@k]]
