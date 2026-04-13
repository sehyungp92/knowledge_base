---
type: entity
title: Minerva Math
entity_type: dataset
theme_ids:
- adaptive_computation
- chain_of_thought
- finetuning_and_distillation
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0006793271068046138
staleness: 0.0
status: active
tags: []
---
# Minerva Math

> Minerva Math is a quantitative reasoning benchmark released by Google DeepMind that tests a model's ability to solve problems spanning mathematics and the natural sciences — requiring not just symbolic manipulation but genuine multi-step scientific reasoning. Its difficulty and breadth have made it a canonical evaluation target for the current wave of reinforcement-learning-based reasoning research, where it serves as a stringent proxy for whether RL training translates into general quantitative competence rather than narrow benchmark hacking.

**Type:** dataset
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Overview

Minerva Math was developed by Google DeepMind as a benchmark requiring quantitative reasoning that goes beyond pattern-matched arithmetic — problems demand integration of scientific knowledge with formal derivation. In the context of recent RL-for-reasoning work, it is typically evaluated using **avg@4** (average accuracy over 4 sampled outputs), a protocol that partially controls for sampling variance while remaining computationally tractable. This makes it a middle ground between greedy Pass@1, which is sensitive to decoding noise at these scales, and the more optimistic Pass@k at large k.

---

## Role in RL Reasoning Research

Minerva Math has emerged as a standard checkpoint in suites used to validate that RL post-training generalises beyond the narrow distribution of training problems. In JustRL, it appears alongside AIME24/25, MATH500, and AMC as part of the evaluation battery for a 1.5B model trained with a simplified GRPO recipe — binary outcome rewards and a lightweight rule-based verifier derived from DAPO, without symbolic libraries like SymPy. The avg@4 protocol specifically is used here, suggesting the authors wanted a metric that reflects expected performance under light sampling rather than a single greedy decode.

The benchmark's presence in these suites reflects a broader methodological concern: can RL training on verifiable mathematical problems produce models that generalise to *quantitative science*, not just algebra or competition math? Minerva Math's science-adjacent problems are harder to game through surface-level pattern replication, making it a useful signal for genuine reasoning transfer.

---

## Evidence from Post-Training Methods

Several findings across papers touching this benchmark illuminate what drives improvements on it:

**RLPT** (Reinforcement Learning on Pre-Training Data) bypasses human annotation entirely by deriving reward signals from pre-training data structure — specifically, two tasks: Autoregressive Segment Reasoning (predicting the next sentence from preceding context) and Middle Segment Reasoning (predicting a masked span using bidirectional context). The reward is semantic consistency between predicted and reference segments, evaluated by a generative reward model. Applied to Qwen3-4B-Base, RLPT yields absolute improvements of 3.0, 5.1, 8.1, 6.0, 6.6, and 5.3 on MMLU, MMLU-Pro, GPQA-Diamond, KOR-Bench, AIME24, and AIME25 respectively, with gains consistent across Qwen3-8B-Base and Llama-3.2-3B-Base as well. When used as initialisation for standard RLVR (RL with verifiable rewards), it yields further improvements of 2.3 and 1.3 in Pass@1 on AIME24/25 — suggesting RLPT and RLVR are complementary rather than redundant.

**ProRL** (ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models) explored the effect of extended RL training, running approximately 16K GPU hours on 4 nodes of 8×H100-80GB GPUs. The framing — "expands reasoning boundaries" — positions Minerva Math as a boundary test rather than a ceiling, consistent with its role as a hard generalisation probe.

**TiDAR** (TiDAR: Think in Diffusion, Talk in Autoregression) evaluates on Minerva Math as part of validating a hybrid architecture that uses causal attention for the autoregressive output section and bidirectional attention for a masked diffusion prefix — effectively separating the "thinking" (parallel diffusion) from the "talking" (sequential AR generation). Its presence in the eval suite here tests whether architecture-level departures from pure AR can preserve or improve quantitative reasoning.

---

## Limitations and Open Questions

The benchmark's use across these papers also exposes several unresolved tensions:

**Scale gap.** JustRL's results are explicitly limited to 1.5B parameters. Whether the training recipes that improve Minerva Math performance at 1.5B transfer to larger models — where reasoning capabilities emerge more robustly from pretraining alone — remains untested by these works. The benchmark's difficulty may have different discriminative power at different scales.

**Causal opacity.** JustRL acknowledges it cannot definitively isolate which components — hyperparameters, verifier design, training data composition — are most responsible for improvements. Minerva Math gains attributed to a "simple RL recipe" may in fact be sensitive to choices that aren't yet understood.

**Domain coverage bias.** The benchmark skews toward STEM domains well-represented in pretraining corpora. Gains on Minerva Math may not predict performance on quantitative reasoning in less-represented domains (e.g., economics, social science methodology), and the avg@4 protocol may smooth over systematic failure modes on specific subdomains.

**Annotation-free reward signals.** RLPT's approach of deriving rewards from pre-training data structure is promising but introduces a new uncertainty: whether semantic consistency as measured by a generative reward model is well-calibrated for the types of multi-step science problems Minerva Math contains. The reward model is itself a potential bottleneck for this class of approach.

---

## Relationships

Minerva Math sits within a cluster of hard mathematical benchmarks — alongside **AIME24**, **AIME25**, **GPQA-Diamond**, and **MATH500** — that collectively define the current frontier for RL-trained reasoning models. It is specifically distinguished by its science-domain coverage, making it more complementary to than redundant with competition math benchmarks.

Methodologically, it connects to the [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] theme through its role in evaluating GRPO-based approaches, to [[themes/reward_modeling|Reward Modeling]] through RLPT's generative reward model design, and to [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] through the avg@4 evaluation protocol, which implicitly probes how sampling budget affects apparent capability.

## Key Findings

## Sources
