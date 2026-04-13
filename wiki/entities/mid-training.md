---
type: entity
title: Mid-training
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- chain_of_thought
- frontier_lab_competition
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00018828690741924095
staleness: 0.0
status: active
tags: []
---
# Mid-training

> Mid-training designates the phase between large-scale pretraining and task-specific fine-tuning in which labs use structured data, synthetic reasoning traces, or RL environments to bake durable capabilities — navigation, tool use, mathematical reasoning — directly into a model's weights. Emerging as a distinct stage in the modern training pipeline, it has become a critical lever for compressing data requirements, shaping the reasoning substrate that downstream RL can exploit, and determining which skills generalize across contexts.

**Type:** method
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/chain_of_thought|Chain of Thought]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/pretraining_data|Pretraining Data]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/synthetic_data_generation|Synthetic Data Generation]]

---

## Overview

Mid-training occupies the space between the broad knowledge acquisition of pretraining and the targeted optimization of RL-based post-training. Rather than treating pretraining and fine-tuning as the only two meaningful phases, frontier labs now increasingly treat mid-training as a place to shape the *reasoning substrate* itself — the primitive operations, chain-of-thought patterns, and domain coverage that downstream RL will either amplify or fail to unlock.

The clearest illustration of mid-training's leverage comes from **Thinking Augmented Pre-Training (TPT)**, which interleaves synthetic reasoning traces with standard pretraining data. TPT improves pretraining data efficiency by a factor of 3: an 8B model trained on 100B tokens with TPT reaches performance comparable to LLaMA-3.1-8B trained on 15 trillion tokens — 150× more data. The benchmark improvements are stark: GSM8k accuracy jumps from 19.2% to 50.1%, and MATH scores more than double from 9.1% to 21.8%, all at the same compute budget. For smaller models the gains are even more pronounced — a 3B model sees a 3× lift on AIME24 (5.8% → 18.6%). Importantly, TPT requires no human annotation and imposes no structural constraints on source documents, making it applicable to any text corpus.

---

## The Interplay With Pretraining and RL

A controlled experimental study using 100M-parameter Qwen2.5-style models — trained on a 30B-token synthetic dataset generated via the GSM-Infinite framework — isolates the causal contributions of each training phase. The framework uses explicit atomic operations and parseable step-by-step traces, with reasoning complexity quantified as `op(G) = |E|` (edge count in the dependency graph), enabling systematic manipulation of task difficulty from basic arithmetic to complex multi-step composition. Crucially, a prediction is only considered correct when *both* the reasoning steps and the final answer match ground truth, enforcing process-level correctness beyond answer matching alone.

Two generalization dimensions emerge:

- **Contextual (breadth) generalization** — whether a model can transfer reasoning primitives to novel domains that share the same underlying computation graph but differ in surface form.
- **Extrapolative (depth) generalization** — whether a model can solve problems more complex than those seen during training by composing learned primitives in deeper dependency structures.

The most consequential finding concerns the relationship between pretraining coverage and RL: **RL incentivizes contextual generalization only when the relevant primitives or base skills are already present in the base model.** Without any pretraining exposure to a given context, RL does not induce transfer. Even very sparse coverage (≥1%) provides a sufficient seed for robust cross-context generalization, but zero coverage leaves RL with nothing to amplify. This reframes mid-training from an optional optimization step into a gating condition for RL's effectiveness — what RL can do is bounded by what pretraining (and mid-training) put there first.

---

## Limitations and Open Questions

The efficiency gains from TPT are demonstrated primarily on mathematical and reasoning benchmarks; whether the 3× data efficiency advantage holds for broader language capabilities, coding, or multimodal tasks remains untested. The 100M-parameter experimental models used to study phase interplay are far smaller than frontier systems, and scaling behavior of these dynamics is not yet characterized.

The "sufficient seed" finding (≥1% pretraining coverage enables RL generalization) is established in a controlled synthetic setting with clean dependency graphs. Real-world pretraining corpora are noisy and unstructured — whether the threshold behaves the same way, or whether surface-form diversity in natural text changes the dynamics, is an open question.

More broadly, mid-training as a named, distinct phase is still being institutionalized. The precise boundary between a "mid-training run" and "continued pretraining on curated data" is not standardized across labs, making cross-lab comparisons difficult. As RL-based post-training scales (see [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]), the stakes of what mid-training provides as a substrate will only increase — making the interplay dynamics documented here increasingly strategically significant for [[themes/frontier_lab_competition|Frontier Lab Competition]].

---

## Related Sources

- On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models
- Thinking Augmented Pre-training
- Thoughts on AI Progress (Dec 2025)

## Key Findings

## Relationships

## Sources
