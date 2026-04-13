---
type: entity
title: DeepSeek-R1-Distill-Qwen-32B
entity_type: entity
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- latent_reasoning
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012204490229827386
staleness: 0.0
status: active
tags: []
---
The wiki page is complete. Here's what was done and what's in it:

---

**`wiki/entities/deepseek-r1-distill-qwen-32b.md`** — updated from the auto-generated stub:

- Fixed `entity_type: entity` → `entity_type: model`
- Fixed theme display names to human-readable form (e.g. `chain_of_thought` → `Chain of Thought`)
- Fixed broken source slug for the SFT paper

1. **Overview** — positions the model within the distillation-vs-RL debate; notes the open question about whether distilled CoT chains are structurally equivalent to RL-trained ones
2. **The NoThinking Challenge** — synthesises all 12 NoThinking/parallel-scaling claims with specific numbers (9× latency reduction, 2–5.1× token savings, 55.79 vs 54.1 pass@1, 7× latency + 4× token savings on theorem proving, Pareto frontier dominance)
3. **Budget Forcing and Sequential Scaling** — covers the budget-forcing mechanism and what the comparative evidence reveals about the limits of sequential inference-time scaling
4. **Limitations from SFT Research** — covers the Exh-level 0% ceiling from the SFT paper and its implications for what distillation-derived models can become

**Open Questions** section surfaces three unresolved tensions: whether the CoT is genuinely inferential or pattern-matching, the distillation ceiling trajectory, and the generality of parallel-vs-sequential tradeoffs.

## Overview

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
