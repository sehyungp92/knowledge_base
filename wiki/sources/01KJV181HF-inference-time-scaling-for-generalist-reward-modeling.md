---
type: source
title: Inference-Time Scaling for Generalist Reward Modeling
source_id: 01KJV181HFVKR27CWM4VXF83J8
source_type: paper
authors:
- Zijun Liu
- Peiyi Wang
- Runxin Xu
- Shirong Ma
- Chong Ruan
- Peng Li
- Yang Liu
- Yu Wu
published_at: '2025-04-03 00:00:00'
theme_ids:
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Inference-Time Scaling for Generalist Reward Modeling

**Authors:** Zijun Liu, Peiyi Wang, Runxin Xu, Shirong Ma, Chong Ruan, Peng Li, Yang Liu, Yu Wu
**Published:** 2025-04-03 00:00:00
**Type:** paper

## Analysis

# Inference-Time Scaling for Generalist Reward Modeling
2025-04-03 · paper · Zijun Liu, Peiyi Wang, Runxin Xu, Shirong Ma, Chong Ruan et al. (8 total)
https://arxiv.org/pdf/2504.02495

---

### Motivation & Prior Limitations
Reward modeling for general domains lacks the explicit ground truth and well-defined criteria available in verifiable tasks like math and code, making accurate reward generation substantially harder to achieve and scale.
- Scalar reward models cannot benefit from inference-time sampling because they produce invariant outputs for the same input, yielding no diversity across samples and blocking compute-scaling strategies.
  - Pairwise RMs compound this with an input flexibility problem: they cannot rate single responses and require extra techniques to handle more than two candidates, limiting their use as a general-purpose signal.
- Existing learning methods for generative reward models (GRMs) improve reward quality but do not target the connection between learned behavior and inference-time scalability, resulting in marginal performance gains from increased compute.
  - Preliminary experiments showed that self-generated principles barely improve reward quality, but a filtered subset of correct-trajectory principles yields significant boosts (e.g., Gemma-2-27B Chat Hard: 59.1 → 68.0), indicating that models can generate useful principles but cannot yet reliably select or produce them on demand.

---

### Proposed Approach
The paper proposes Self-Principled Critique Tuning (SPCT), a two-phase post-training method that teaches pointwise generative reward models to adaptively generate evaluation principles and then produce critiques guided by those principles, enabling meaningful diversity across parallel samples at inference time.
- The foundation is pointwise GRM, which assigns individual integer scores (1–10) to each response within a single language generation, unifying single, paired, and multiple-response rating in one format without requiring separate paradigms.
  - This contrasts with pairwise GRMs (e.g., PairRM, LLM-as-a-Judge) which cannot score single responses, and scalar RMs which cannot generate diverse outputs across samples.
- Phase 1 (Rejective Fine-Tuning, cold start) trains the GRM to generate principles and critiques in the correct format using trajectories filtered by whether predicted rewards agree with ground-truth preference labels; both hinted sampling (with the correct answer appended) and non-hinted sampling are used, and trajectories that take shortcuts (identified in hinted samples) motivate the subsequent RL phase.
- Phase 2 (Rule-Based Online RL via GRPO) rewards the model +1 if it correctly identifies the best response using its self-generated principles and −1 otherwise, with no format reward but a larger KL penalty coefficient to stabilize format; this encourages the model to learn which principles actually lead to correct rewards rather than superficially plausible ones.
- At inference time, k independent samples are drawn with temperature=0.5, each producing a distinct set of principles and corresponding critiques; pointwise scores are summed across samples (Voting@k), expanding the effective reward space by a factor of k and enabling finer-grained discrimination.
- A meta RM (a scalar pointwise model trained on GRM trajectories labeled by correctness) filters the k samples down to the top kmeta by meta-reward score before aggregating, suppressing low-quality or biased principle-critique pairs.

---

### Results & Capabilities
DeepSeek-GRM-27B trained with SPCT achieves competitive greedy-decoding performance (69.9% overall across RewardBench, PPE, RMB benchmarks) versus strong public models including GPT-4o (71.3%) and Nemotron-4-340B-Reward (70.5%), using a 27B dense model trained on Gemma-2-27B.
- Inference-time scaling delivers substantial and consistent gains: Voting@8 improves overall score from 67.9 to 70.6 (+2.7), compared to +0.3 for CLoud-Gemma-2-27B and +0.6 for LLM-as-a-Judge at the same k; Voting@32 with meta RM reaches 72.8%, surpassing all reported baselines.
  - The SPCT-trained model improves more than twice as much per unit of inference compute as the RFT-only model (+2.7 vs. +1.5 at Voting@8), confirming that the RL phase specifically induces scalable behavior rather than just better base quality.
- DeepSeek-GRM-27B with inference-time scaling outperforms training-time scaling across model sizes up to 671B MoE parameters (DeepSeek-V3), establishing that compute invested at inference time can substitute for substantially larger models.
- SPCT substantially reduces the domain bias characteristic of scalar and semi-scalar RMs, which show strong performance on verifiable tasks (PPE Correctness) but degrade on open-ended benchmarks; DeepSeek-GRM-27B achieves more balanced ranks across all four benchmark categories.
- Ablations confirm that every component contributes: removing principle generation drops Voting@8 from 70.6 to 68.0; removing the RL stage (RFT only) drops greedy overall from 69.9 to 68.8; removing general instruction data from training causes a large drop to 63.3%.

---

### Implications
Demonstrating that inference-time scaling can outperform training-time model-size scaling for reward modeling directly challenges the assumption that capability gains require proportionally larger models, suggesting a compute-allocation design space where inference budget is a first-class variable alongside parameter count.
- Extending effective inference-time scaling beyond verifiable tasks to general domains removes a key bottleneck for applying RL post-training at scale in non-math, non-code settings, potentially enabling stronger alignment and instruction-following improvements without hand-crafted reward rules.
- The meta RM pattern — a lightweight judge trained to score the quality of another model's reasoning traces rather than the object-level response — is a transferable design primitive for any system where reasoni

## Key Claims

1. Scalar reward models cannot perform effective inference-time scaling because they generate invariant rewards with limited diversity across multiple samples.
2. Pairwise reward models lack flexibility to rate single responses and require extra techniques to handle multiple responses.
3. Pointwise generative reward modeling can unify scoring of single, paired, and multiple responses within pure language representation.
4. Self-generated principles barely improve reward quality, but filtered (correct) principles significantly boost reward quality for LLMs.
5. Current LLMs can generate diverse principles, but only a subset are proper for guiding reward generation, indicating potential for self-bootstrapping via online RL.
6. SPCT uses rule-based online RL with GRPO, applying a larger KL penalty coefficient instead of format rewards to ensure format correctness and avoid severe biases.
7. Hinted sampling in rejective fine-tuning sometimes causes GRMs to take shortcuts in generated critiques, especially for reasoning tasks, motivating the need for online RL.
8. Parallel sampling for inference-time scaling enables GRMs to generate diverse sets of principles and corresponding critiques, expanding the effective reward space by k times.
9. A meta reward model trained to identify correctness of GRM-generated principles and critiques can guide voting to filter low-quality samples and outperform naive voting.
10. DeepSeek-GRM-27B with inference-time scaling achieves better performance than training-time scaling to larger model sizes (up to 671B parameters).

## Capabilities

- Pointwise Generative Reward Modeling (GRM) trained with Self-Principled Critique Tuning (SPCT) enables inference-time scalable generalist reward modeling across diverse open-ended domains, achieving 69.9 overall on RM benchmarks at greedy decoding with 27B parameters
- Meta RM guided voting with 32 parallel samples achieves 72.8 overall on RM benchmarks using a 27B model — surpassing GPT-4o (71.3) and Nemotron-4-340B-Reward (70.5) which use greedy decoding
- Inference-time scaling of a 27B generative reward model outperforms training-time model size scaling up to 671B parameters — smaller model plus more inference compute beats a much larger model at greedy decoding
- SPCT enables GRMs to adaptively generate query-specific evaluation principles and critiques via online RL, producing diverse reward samples needed for inference-time voting aggregation in arbitrary domains

## Limitations

- Scalar and semi-scalar reward models cannot scale at inference time due to invariant reward generation — the same query-response pair produces identical scalar outputs regardless of sampling count
- GRM still faces unresolved challenges on specific task types — the approach does not universally succeed across all evaluated domains even with inference-time scaling
- Parallel sampling for inference-time GRM scaling is computationally expensive — k=32 samples multiplies inference compute 32x, creating an efficiency barrier for high-throughput deployment
- Current LLMs cannot reliably self-select appropriate principles for reward generation — self-generated principles produce near-zero performance improvement, indicating models cannot distinguish quality principles without RL training
- Pretrained GRMs without SPCT cannot generate correct rewards for a substantial fraction of queries — hinted sampling (revealing the ground-truth answer label in the prompt) is required as a cold-start fallback to produce any usable training data
- Hinted sampling introduces shortcut reasoning — when the correct answer is revealed in the prompt, the model constructs post-hoc rationalization rather than genuinely evaluating responses, particularly on reasoning tasks
- High-quality reward signals are only reliably obtainable in domains with verifiable ground truth (math, coding) — generalist reward modeling for open-ended domains lacks ground truth, making reward quality fundamentally harder to validate or train on
- Domain biases persist structurally in scalar and semi-scalar reward models — they excel on verifiable correctness tasks (PPE Correctness) while underperforming on open-ended benchmarks, and vice versa for generative RMs
- Majority voting for pairwise GRMs introduces structural bias — forced-choice per sample prevents tie representation, and subtle quality differences between responses cannot be quantified without continuous scores
- No evaluation of downstream RL training outcomes when SPCT-GRM is used as reward signal — all experiments use static benchmarks, leaving unknown whether the reward model actually improves LLM quality when used for RL post-training at scale
- Discrete integer reward scores (1–10 scale) produce coarse evaluation granularity at single-sample inference — meaningful differentiation between similar responses only emerges by summing many samples, requiring compute scaling to achieve reward precision

## Bottlenecks

- Absence of reliable automated reward assessment for open-ended responses blocks scaling RL post-training beyond verifiable domains — GRM with SPCT reduces but does not fully resolve this, as challenges remain in specific task types and efficiency constraints prevent broad deployment
- Linear compute scaling of parallel GRM sampling blocks practical deployment as reward signal in high-throughput RL training pipelines — k=32 evaluations per response multiplies reward computation cost 32x relative to scalar baselines

## Breakthroughs

- Inference-time scaling for reward modeling generalized beyond verifiable domains to arbitrary open-ended tasks via SPCT-trained GRM with meta RM guided voting — a 27B model with 32 samples surpasses GPT-4o and 340B scalar RMs at greedy decoding
- 27B generative reward model with inference-time scaling outperforms training-time model size scaling up to 671B parameters — establishing compute-equivalent substitution between model size and inference samples in reward modeling

## Themes

- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/grpo|GRPO]]
