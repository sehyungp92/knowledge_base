---
type: entity
title: DeepSeek-R1-Distill-Qwen-1.5B
entity_type: entity
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0008353029900604019
staleness: 0.0
status: active
tags: []
---
# DeepSeek-R1-Distill-Qwen-1.5B

> DeepSeek-R1-Distill-Qwen-1.5B is a 1.5-billion parameter language model produced by distilling the reasoning capabilities of DeepSeek-R1 into the Qwen architecture. Despite its small size, it has become a standard proving ground for post-training research — particularly RL-based reasoning, adaptive compute, and distillation techniques — owing to its unusually strong mathematical reasoning baseline and the low cost of experimentation at this scale.

**Type:** entity
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

DeepSeek-R1-Distill-Qwen-1.5B occupies a unique position in the post-training literature: it is small enough to be trained extensively on modest hardware yet capable enough to exhibit the long-chain reasoning behaviours that make it an interesting subject for study. Its origin through knowledge distillation from a much larger reasoning model means it arrives with reasoning patterns already baked in — making it useful both as a starting point for further RL fine-tuning and as a controlled baseline against which algorithmic improvements can be measured.

The model has been adopted across a notably diverse set of research threads simultaneously, from pure RL recipe ablations (JustRL) to adaptive thinking mode selection (AdaptThink, Thinkless), representation learning augmentation (LLM-JEPA), and mechanistic investigations into how RL updates actually propagate through parameters (The Path Not Taken).

## Role as a Research Substrate

The model's most prominent role is as the base for JustRL-DeepSeek, where it is trained using GRPO with binary outcome rewards and a lightweight rule-based verifier drawn from DAPO — deliberately avoiding symbolic math libraries like SymPy. The resulting training run consumes roughly 15 days across 32 A800-80GB GPUs, a meaningful but accessible compute budget. JustRL's central claim is that simplicity works at this scale: no elaborate reward shaping, no verifier complexity. The honest limitation the authors acknowledge is that they cannot isolate which specific components — hyperparameters, verifier design, or training data composition — are actually doing the work.

AdaptThink treats the model as the subject of an efficiency intervention rather than a capability one. Starting from DeepSeek-R1-Distill-Qwen-1.5B, it applies a constrained optimisation objective that maximises the probability of "NoThinking" (direct answer) responses while keeping overall accuracy at or above the reference model's level. The results are striking: on GSM8K, MATH500, and AIME2024, response lengths drop by 50.9%, 63.5%, and 44.7% respectively, while accuracy marginally improves across all three. The difficulty-adaptive behaviour is qualitatively interesting — NoThinking is selected for 97.7% of Level 1 MATH problems, falling to 50.7% for Level 5, suggesting the model learns a genuine difficulty signal rather than a blanket policy. Thinkless achieves a comparable result via a different mechanism (DeGRPO, which decomposes the hybrid reasoning objective into a mode-selection loss and a response loss), reducing long-form reasoning usage by 50–90% on similar benchmarks.

## What the Model Reveals About RL Dynamics

The Path Not Taken uses this model (alongside others) to study parameter-level sparsity during RLVR training. RL update sparsity — the fraction of parameters that change substantially — ranges from 36% to 92% across models, compared to a consistently low 0.6%–18.8% for SFT. This order-of-magnitude difference suggests RL training is doing something structurally distinct from supervised fine-tuning: it concentrates updates in a sparse subset of parameters rather than distributing them broadly. What this means for the model's internal representations remains an open question, but it complicates any naive interpretation of RL as "just more fine-tuning."

LLM-JEPA's engagement with the model is indirect — it uses comparable small models (Llama-3.2-1B-Instruct) as testbeds for joint-embedding predictive architecture augmentation, achieving substantial accuracy gains on NL-RX-SYNTH (51.6% vs 37.0% baseline) and GSM8K (70.4% vs 56.0%). The relevance to DeepSeek-R1-Distill-Qwen-1.5B is as a comparison point for what representation-level interventions can achieve versus reasoning-level ones.

## Limitations and Open Questions

Several structural limitations of working at this scale are acknowledged across the literature. JustRL's results are explicitly bounded to mathematical reasoning at 1.5B parameters; whether the same simple RL recipe transfers to coding, general QA, or larger model sizes is untested. AdaptThink's experiments were constrained to 1.5B and 7B models due to compute, leaving open whether difficulty-adaptive mode selection scales gracefully or requires re-tuning. Similarly, Nemotron-Research-Reasoning-Qwen-1.5B — a competing 1.5B model trained on 136K problems across five domains — required 16K GPU hours on H100s to produce a generalist model, illustrating that the cost of pushing beyond narrow mathematical reasoning grows sharply even at small scales.

A deeper open question concerns the nature of the distilled capabilities themselves. DeepSeek-R1-Distill-Qwen-1.5B inherits reasoning patterns from a much larger teacher, but it is unclear how much of this is robust generalisation versus pattern matching compressed into a small model. The high RL update sparsity observed during further fine-tuning may reflect the model reaching quickly to a small set of adjustable degrees of freedom — or it may indicate that the distilled representations are largely frozen under RL pressure, with only surface-level behaviour shifting.

## Relationships

DeepSeek-R1-Distill-Qwen-1.5B is directly related to [[themes/finetuning_and_distillation|finetuning and distillation]] as a product of that process, and to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] as the primary arena in which it is studied. Its use across AdaptThink and Thinkless connects it to [[themes/test_time_compute_scaling|test-time compute scaling]] — specifically the question of when extended reasoning is worth its cost. The parameter sparsity findings from The Path Not Taken link it to [[themes/rl_theory_and_dynamics|RL theory and dynamics]] and raise questions for [[themes/representation_learning|representation learning]] about what RL is actually modifying inside a distilled model.

## Key Findings

## Sources
