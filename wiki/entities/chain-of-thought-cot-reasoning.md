---
type: entity
title: Chain-of-Thought (CoT) Reasoning
entity_type: method
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- policy_optimization
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0003398826391123917
staleness: 0.0
status: active
tags: []
---
The page synthesises three main threads from the source material:

1. **Entropy structure** — the 80/20 finding that high-entropy "forking" tokens are where reasoning actually happens, and that RLVR preserves this structure from the base model (86%+ overlap). This is the most structurally significant finding because it implies the reasoning skeleton is fixed at pretraining.

2. **Pretraining as the binding constraint** — MobileLLM-R1's result that ~2T high-quality tokens can match models pretrained on 36T, and that identical SFT produces different CoT outcomes depending on pretraining quality. FineWeb-Edu's role is highlighted as a cross-domain connector, not just a math/code corpus.

3. **DRO for open-ended domains** — the reference-policy-only self-referential reward design that avoids external judges, with rubric-gating as a stability mechanism. The connection between R3's reasoning-reflective tokens and the entropy concentration finding is drawn explicitly — they're converging on the same underlying insight from different angles.

Key open questions flagged: the inherited-vs-shaped reasoning structure problem, the replication gap on the 2T claim, self-referential bias in DRO, and the unresolved CoT length/efficiency question.

## Overview

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
