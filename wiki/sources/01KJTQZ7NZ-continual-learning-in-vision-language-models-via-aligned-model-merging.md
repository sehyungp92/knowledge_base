---
type: source
title: Continual Learning in Vision-Language Models via Aligned Model Merging
source_id: 01KJTQZ7NZ2SYVQ3B1TP79G4RQ
source_type: paper
authors:
- Ghada Sokar
- Gintare Karolina Dziugaite
- Anurag Arnab
- Ahmet Iscen
- Pablo Samuel Castro
- Cordelia Schmid
published_at: '2025-05-30 00:00:00'
theme_ids:
- continual_learning
- finetuning_and_distillation
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Continual Learning in Vision-Language Models via Aligned Model Merging

**Authors:** Ghada Sokar, Gintare Karolina Dziugaite, Anurag Arnab, Ahmet Iscen, Pablo Samuel Castro, Cordelia Schmid
**Published:** 2025-05-30 00:00:00
**Type:** paper

## Analysis

# Continual Learning in Vision-Language Models via Aligned Model Merging
2025-05-30 · paper · Ghada Sokar, Gintare Karolina Dziugaite, Anurag Arnab, Ahmet Iscen, Pablo Samuel Castro et al. (6 total)
https://arxiv.org/pdf/2506.03189

---

### Motivation & Prior Limitations
- Sequential fine-tuning is the dominant continual learning (CL) paradigm but is structurally biased toward recently learned tasks, inherently favoring plasticity over the stability needed to retain prior knowledge, causing catastrophic forgetting.
  - Standard fine-tuning on a 6-task CoIN visual QA sequence produces an average accuracy of 43.36% and backward transfer of −39.51%, compared to 76.46% when each task is trained independently with its own LoRA.
- Parameter-efficient fine-tuning methods like LoRA, while reducing compute costs, were originally designed for single-task settings and carry forward the same forgetting problem when applied sequentially.
  - Prior LoRA-based CL approaches (O-LoRA, I-LoRA, MoELoRA) either continuously accumulate parameters, require task identifiers at inference, or still suffer significant forgetting.
- Post-training model merging techniques (TIES, TALL) reduce interference by pruning misaligned weights after training, but pruning causes measurable capacity loss — TIES applied post-training reduces task accuracy by 7.44% compared to no alignment, as 29.41% of parameters across layers become misaligned during unconstrained fine-tuning.

---

### Proposed Approach
- The paper reframes continual learning as a model merging problem: instead of sequentially overwriting a shared LoRA, each new task fine-tunes a temporary LoRA copy which is then merged (element-wise averaged) back into a single global LoRA that evolves over time.
  - This contrasts with prior work that either accumulates separate task-specific modules (O-LoRA) or fine-tunes a single shared module in place; here, a permanent global module is iteratively updated via merging rather than direct gradient updates from new tasks.
- The core algorithmic contribution is PAM (Parameter Alignment for Merging), which during training periodically identifies weights in the current task's LoRA whose signs conflict with the top-p% (by magnitude) weights in the global LoRA, and re-initializes those conflicting weights — either to zero or to the global LoRA's values — before continuing training.
  - This periodic during-training alignment prevents task weights from diverging into sign-conflicting configurations, so that post-training averaging produces less interference than merging weights that were allowed to drift freely.
  - The alignment percentage p (default 50%) acts as a continuous stability-plasticity knob: higher p enforces stronger alignment with prior tasks, trading plasticity for stability, while lower p allows more task-specific adaptation.
- The approach is built on LoRA (rank r=32) with fixed pretrained weights, using PaliGemma as the base VLM, and runs on the big_vision JAX/Flax framework on TPUv2.

---

### Results & Capabilities
- PAM achieves 49.89% average accuracy on CoIN (6-task image QA sequence) averaged over three task orderings, compared to 43.36% for sequential fine-tuning, 46.53% for O-LoRA, 46.59% for MoELoRA, and 45.74% for MagMax, while also outperforming on backward transfer (−19.45 vs. −39.51 for fine-tuning).
  - PAM achieves this using a single evolving LoRA, without parameter expansion over time, and without task identity at inference — advantages over O-LoRA and MoELoRA which grow in size or require routing.
- Merging-based methods, including PAM, are substantially more robust to task ordering than fine-tuning: PAM's standard deviation across three task orderings is ±1.66 ACC compared to ±8.18 for fine-tuning and ±9.98 for MoELoRA.
- During-training alignment in PAM outperforms post-training alignment (TIES) on both ACC (49.89 vs. 47.78) and BWT (−19.45 vs. −22.87), confirming that constraining weight drift during training is more effective than pruning after the fact.
- Combining PAM with TALL's post-training weight localization yields 51.97% ACC and −9.27 BWT on CoIN — the best result across all compared methods — demonstrating PAM is composable with other merging techniques.
- PAM generalizes across benchmark types: on an extended 10-task CoIN (with remote sensing and multi-choice QA), PAM reduces forgetting (BWT −14.10 vs. −22.19 for fine-tuning); on a 3-task video QA sequence, BWT improves to −1.95 vs. −16.66 for fine-tuning.
- PAM improves existing CL methods when used as a complement: LWF+PAM achieves forward transfer and forgetting reduction comparable to Experience Replay without requiring stored past data, and ER+PAM further improves over ER alone.

---

### Implications
- Reframing CL as a merging problem, rather than an optimization-with-constraints problem, offers a structurally different and orthogonal axis of improvement that can be stacked on top of regularization and replay methods — suggesting that the field's existing taxonomy (regularization, architectural, replay) may benefit from a fourth category.
- The finding that simple element-wise averaging of LoRA weights, when combined with during-training sign alignment, outperforms sophisticated post-training merging methods (TIES, TALL standalone) implies that the quality of the merge is more sensitive to how weights were trained than to how they are combined — a principle that may generalize to other model merging applications beyond CL.
- PAM's single-LoRA design avoids parameter growth, which is a scaling concern for long task sequences; this makes the approach practically more viable for production CL systems on large VLMs than methods that expand module counts with each new task.
- The result that LoRA-based merging reduces task order sensitivity (low std across orderings) has practical implications for deployment: real-world task streams are not controllable, and robustness to order is a prerequisite for reliable production systems.

## Key Claims

1. Sequential fine-tuning inherently favors plasticity over the stability needed to retain prior knowledge in continual learning.
2. Catastrophic forgetting in continual learning arises from the inherent bias of sequential fine-tuning toward the most recently learned task.
3. Continual learning with large models poses the challenge that model size, often reaching billions of parameters, can be prohibitively expensive for continual full fine-tuning.
4. Direct application of PEFT in continual learning scenarios often leads to catastrophic forgetting.
5. Previous LoRA-based continual learning approaches face scalability issues due to continuous accumulation of parameters, require task identifiers at test time, and suffer from catastrophic forgetting.
6. Model merging can effectively address the stability-plasticity dilemma in continual learning.
7. PAM uses element-wise averaging to merge a temporary task-specific LoRA with a global evolving LoRA after each new task.
8. Merging alone effectively mitigates catastrophic forgetting of previous tasks even without incorporating sophisticated mechanisms.
9. Fine-tuning a single LoRA exhibits high sensitivity to task order, with performance fluctuating between steps depending on task similarity.
10. Merging-based continual learning exhibits greater robustness to task ordering compared to sequential fine-tuning.

## Capabilities

- Continual learning across sequential vision-language tasks via LoRA model merging (PAM), achieving reduced catastrophic forgetting without access to previous task data
- Task-order-robust continual learning in VLMs: merging-based approaches deliver stable performance regardless of task sequence, unlike sequential fine-tuning which is highly sensitive to order
- During-training parameter alignment for LoRA merging preserves plasticity while improving knowledge retention, outperforming post-training alignment methods that cause accuracy degradation
- Compatibility of PAM with existing CL strategies (regularization-based LWF, experience replay): PAM boosts performance of both, with PAM+LWF achieving near-ER performance without stored data

## Limitations

- PAM (single evolving LoRA via merging) fails to adequately handle highly dissimilar tasks — scenarios where new data significantly differs from previously learned tasks remain unaddressed
- Substantial accuracy gap remains between continual learning (PAM: 49.89%) and per-task oracle upper bound (Independent: 76.46%) — a ~27 point gap indicating catastrophic forgetting is far from solved
- Continual learning with LoRA merging still requires task boundary signals during training — the model must know when a new task arrives to clone the global LoRA and begin fine-tuning
- Significant compute requirement: 64 TPUs per task, 1–10 hours per task, ~20 hours for a 6-task sequence — impractical for resource-constrained settings despite LoRA efficiency gains
- Existing sophisticated model merging methods (TIES, TALL) designed for independent model initialization do not transfer well to LoRA continual merging — simple averaging often competitive or superior
- Post-training alignment of LoRA weights (e.g., TIES pruning) causes 7.44% accuracy reduction by removing capacity the model needs for new tasks — pruning misaligned parameters is destructive
- Intrinsic stability-plasticity tradeoff in continual learning cannot be eliminated — higher alignment percentage reduces forgetting but lowers plasticity (task accuracy), with no free-lunch setting
- Pretrained VLMs show poor zero-shot generalization to specialised downstream tasks despite large-scale pretraining — fine-tuning remains necessary, precluding truly general-purpose deployment
- PAM still exhibits substantial backward transfer (BWT = -19.45) — meaningful forgetting persists even with alignment and merging, and is not a solved problem
- Regularization alone (weight constraints) provides only marginal forgetting mitigation — a widely-used CL strategy is insufficient as a standalone solution
- Continual parameter accumulation in prior LoRA-based CL methods (O-LoRA) creates a scalability bottleneck — parameter count grows linearly with tasks

## Bottlenecks

- Catastrophic forgetting without access to previous task data remains the central unsolved bottleneck in continual learning for large VLMs — even state-of-the-art methods lose ~27 accuracy points vs per-task oracle
- Compute cost of iterative fine-tuning on large VLMs (even with LoRA) blocks practical continual learning at scale — 64 TPUs per task makes sequential adaptation expensive for long task streams
- Task dissimilarity handling in single-model continual learning — current merging methods degrade when new tasks are highly dissimilar from previous ones, blocking general-purpose lifelong learning
- Lack of principled LoRA-specific merging theory — existing merging methods were designed for full model weights and don't exploit LoRA's low-rank geometry, blocking reliable multi-task LoRA composition

## Breakthroughs

- Model merging replaces sequential fine-tuning as the continual learning paradigm for VLMs, yielding better stability-plasticity balance, robustness to task order, and improved generalization — without expanding parameter count

## Themes

- [[themes/continual_learning|continual_learning]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/lora-low-rank-adaptation|LoRA (Low-Rank Adaptation)]]
- [[entities/model-merging|Model Merging]]
- [[entities/scienceqa|ScienceQA]]
- [[entities/stability-plasticity-dilemma|Stability-Plasticity Dilemma]]
- [[entities/vqav2|VQAV2]]
