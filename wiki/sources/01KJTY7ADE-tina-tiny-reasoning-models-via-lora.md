---
type: source
title: 'Tina: Tiny Reasoning Models via LoRA'
source_id: 01KJTY7ADE12N1YDN13ZP47JP5
source_type: paper
authors:
- Shangshang Wang
- Julian Asilis
- Ömer Faruk Akgül
- Enes Burak Bilgin
- Ollie Liu
- Willie Neiswanger
published_at: '2025-04-22 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Tina: Tiny Reasoning Models via LoRA

**Authors:** Shangshang Wang, Julian Asilis, Ömer Faruk Akgül, Enes Burak Bilgin, Ollie Liu, Willie Neiswanger
**Published:** 2025-04-22 00:00:00
**Type:** paper

## Analysis

# Tina: Tiny Reasoning Models via LoRA
2025-04-22 · paper · Shangshang Wang, Julian Asilis, Ömer Faruk Akgül, Enes Burak Bilgin, Ollie Liu et al. (6 total)
https://arxiv.org/pdf/2504.15777

---

### Motivation & Prior Limitations
RL-based reasoning training is effective but computationally expensive, making it inaccessible to most researchers and creating a barrier to reproducing and extending frontier reasoning model results.
- Existing SOTA RL reasoning models (STILL-3, DeepScaleR, Open-RS) use full-parameter training on top of already-distilled base models, requiring thousands of dollars in compute, hundreds of training hours, and hundreds of thousands of training samples.
  - DeepScaleR-1.5B-Preview cost ~$3,629 and 240 hours; STILL-3-1.5B-preview cost ~$2,268 and 150 hours.
- SFT-based distillation approaches (e.g., STILL, s1) risk instilling shallow imitation rather than generalized reasoning, and depend on costly expert demonstrations.
- No prior work had demonstrated that parameter-efficient fine-tuning via LoRA could substitute for full-parameter updates in RL reasoning settings — the assumption in virtually all open-source reasoning replicas was that full-parameter training was necessary.

---

### Proposed Approach
Tina applies LoRA-based parameter-efficient fine-tuning during reinforcement learning (specifically GRPO-style RL) on DeepSeek-R1-Distill-Qwen-1.5B, a 1.5B parameter model, training only the low-rank adapter parameters rather than the full model weights.
- This differs from all major open-source reasoning replicas (STILL-3, DeepScaleR, Open-RS, SimpleRL, PRIME, s1, OpenThinker), which universally use full-parameter RL post-training.
- LoRA modifies only a small fraction of parameters via low-rank decomposition of weight updates, enabling training on two NVIDIA L40S GPUs (~$1/GPU-hour on commodity cloud) rather than large distributed clusters.
- The training pipeline builds on OpenR1 (HuggingFace's open DeepSeek-R1 reproduction), using the same datasets and reward structures as the baselines to enable fair comparison. Hyperparameters were intentionally not tuned — established configurations from prior work were adopted and held fixed across experiments, keeping tuning overhead negligible.
- The authors hypothesize that LoRA's efficiency stems from a "rapid format adaptation" mechanism: RL rewards structurally formatted reasoning outputs (step-by-step chains), and LoRA efficiently learns this output structure while preserving the base model's pre-trained knowledge — avoiding the costly knowledge re-integration that full-parameter updates may entail.

---

### Results & Capabilities
Tina models match or outperform all full-parameter SOTA baselines trained on the same base model, while using a fraction of the compute.
- The best Tina model (Tina-Open-RS2) achieves 50.60% average across AIME24/25, AMC23, MATH500, GPQA Diamond, and Minerva, versus 48.74% for the strongest baseline (DeepScaleR-1.5B-Preview), at an estimated 260x cost reduction.
- Tina-Open-RS2 achieves 43.33% Pass@1 on AIME24 — matching both Tina-DeepScaleR and Tina-Open-RS1 on that benchmark — at a total post-training and evaluation cost of $9 USD (best checkpoint only) or $31 USD (all checkpoints in that run).
- The entire paper's experimental program — all main experiments and all ablations — cost $526 USD in total compute, with all main tasks costing $275 USD.
- Ablations show that dataset quality dominates dataset size: Tina trained on 7k examples (Open-RS) outperforms Tina trained on 93.7k examples (OpenR1, 49.26% avg), with the smallest dataset (LIMR, 1.39k samples) still achieving 48.47%.
- LoRA rank is robustly effective across ranks 8–32, with rank 16 performing best (48.92%) and rank 64 actually degrading performance — confirming that very low-rank updates suffice.
- Training dynamics reveal a consistent phase transition: format reward peaks and completion length reaches a minimum at a "turning point," and the best-performing checkpoint occurs just *before* this transition, suggesting that LoRA rapidly saturates format adaptation and that further training degrades generalization.
- Dr.GRPO reaches equivalent peak performance (49.53% vs 49.45% for GRPO) but converges at only 17% of an epoch versus 57%, suggesting faster sample efficiency with the debiased normalization.

---

### Implications
The work directly challenges the assumption that full-parameter RL post-training is necessary for strong reasoning, democratizing access to RL reasoning research to groups with minimal compute budgets.
- If LoRA-based RL is sufficient for reasoning format adaptation — the paper's central hypothesis — then the primary function of RL in reasoning post-training may be structural/stylistic rather than substantive knowledge acquisition, which reframes how the field should think about what RL actually teaches a model.
- The cost floor for reproducing a competitive 1.5B reasoning model drops to ~$9–$85, enabling university labs and individual researchers without cloud TPU allocations or multi-GPU clusters to participate in RL reasoning research.
- The "less compute yields more performance" phenomenon (LoRA performance *inversely* correlating with FLOPs beyond a threshold, unlike full-parameter models) suggests that over-training LoRA adapters is a meaningful failure mode to study and avoid — a finding relevant to any LoRA-based finetuning pipeline.
- The open release of all code, training logs, model weights, and checkpoints (including intermediate checkpoints) makes Tina a reproducible baseline and testbed for future work on efficient reasoning, LoRA dynamics, and RL training analysis.

---

### Remaining Limitations & Next Steps
The paper's evaluation is confined to a 1.5B parameter model, and whether LoRA-based RL scales equivalently to larger models (7B, 32B) remains untested.
- The authors explicitly note that the absolute reasoning ceiling of a 1.5B model is lower than larger models on complex multi-step prob

## Key Claims

1. Applying LoRA during RL post-training of a 1.5B parameter model achieves reasoning performance competitive with, and sometimes surpassing, SOTA RL reasoning models built on the same base model.
2. The best Tina model achieves a greater than 20% reasoning performance increase and 43.33% Pass@1 accuracy on AIME24 at a total post-training and evaluation cost of only $9 USD.
3. Tina's $9 training approach represents an estimated 260x cost reduction compared to existing SOTA models on the same base model.
4. LoRA's effectiveness and efficiency in RL reasoning stem from rapidly adapting the model to the structural format of reasoning rewarded by RL, while largely preserving the base model's underlying know
5. Supervised fine-tuning via distillation risks instilling shallow imitation in the learning model rather than fostering dynamic exploration of reasoning paths.
6. Reinforcement learning enables models to learn directly and flexibly from verifiable reward signals derived from curated data, and can lead models to explore a greater variety of logical paths.
7. RL pipelines are often complex and notoriously resource-intensive, typically involving substantial compute.
8. All five Tina models achieve average reasoning scores in the range of 48.16% to 50.60% across AIME24/25, AMC23, MATH500, GPQA, and Minerva benchmarks.
9. Nearly all Tina models outperform their corresponding full-parameter-trained baseline models on average reasoning score despite using only parameter-efficient LoRA updates.
10. Strong Tina reasoning results are achieved with only 19% to 57% of a full training epoch, indicating rapid adaptation.

## Capabilities

- LoRA-based RL post-training on a 1.5B parameter model achieves reasoning performance competitive with full-parameter SOTA models at 260x lower computational cost — best checkpoint reaches 43.33% Pass@1 on AIME24 at $9 total training and evaluation cost
- High-quality small datasets (~7k examples) for RL reasoning training outperform much larger datasets (~94k examples) on mathematical reasoning benchmarks, with average scores of 50.60% vs 49.26% — data quality dominates data quantity for LoRA-based RL
- LoRA-based RL reasoning training exhibits a reliable phase transition in format metrics (format reward peak, completion length minimum) that consistently predicts the optimal checkpoint location — best performance occurs just before format metric destabilization

## Limitations

- LoRA-based RL reasoning is bounded by the absolute capability ceiling of small (1.5B parameter) models — complex multi-step reasoning problems requiring larger world knowledge stores remain out of reach regardless of post-training efficiency
- Reasoning skills trained via LoRA-based RL on mathematical benchmarks have not been tested for transfer to non-mathematical domains such as coding — cross-domain generalization of the learned reasoning format is unverified
- LoRA-based RL performance exhibits an inverse relationship with compute beyond the optimal checkpoint — overtrained LoRA models degrade in reasoning performance, unlike full-parameter models which continue to benefit from extended training
- Tina's results are predicated on starting from a distillation-pretrained base model (DeepSeek-R1-Distill-Qwen-1.5B) with pre-existing strong reasoning aptitude — LoRA-based RL effectiveness on generic pretrained models of equivalent size is untested and likely substantially weaker
- Accuracy reward curves in LoRA-based RL training are decoupled from format metric phase transitions — no reliable in-training signal identifies when the optimal checkpoint is reached without offline evaluation across multiple checkpoints
- Benchmark evaluation results across AI reasoning research are unreliable for cross-paper comparison — different evaluation frameworks and inference settings produce significantly different scores for identical models, systematically distorting the competitive landscape
- LoRA format adaptation is structurally limited to modifying output structure rather than expanding the model's knowledge base — the mechanism explicitly preserves rather than updates the base model's world knowledge, capping what reasoning can be applied to
- Hyperparameter optimization was entirely bypassed to minimize cost — optimal LoRA rank, learning rate, and RL algorithm configurations for this specific setup remain unexplored, with reported performance representing a near-default configuration

## Bottlenecks

- No principled in-training early stopping criterion for LoRA-based RL reasoning — accuracy reward curves are decoupled from the format phase transition that predicts optimal checkpoint timing, requiring expensive post-hoc multi-checkpoint evaluation to identify the best model

## Breakthroughs

- LoRA-based RL post-training achieves reasoning performance competitive with or exceeding full-parameter SOTA at 260x lower computational cost — reducing the cost to train a competitive AIME-level reasoning model from thousands of dollars to $9

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/low-rank-adaptation|Low-Rank Adaptation]]
- [[entities/math500|MATH500]]
- [[entities/minerva|Minerva]]
- [[entities/pass1|Pass@1]]
