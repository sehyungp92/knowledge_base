---
type: entity
title: Dynamic Cheatsheet
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_systems
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- knowledge_and_memory
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00033873050638364067
staleness: 0.0
status: active
tags: []
---
# Dynamic Cheatsheet

> Dynamic Cheatsheet is a test-time learning method that equips language model agents with a persistent, reusable memory of procedural knowledge and problem-solving workflows. Rather than treating each task independently, it accumulates successful strategies across episodes, enabling models to dramatically improve performance on structured reasoning tasks without any weight updates.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/context_engineering|Context Engineering]], [[themes/continual_learning|Continual Learning]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/test_time_learning|Test-Time Learning]]

## Overview

Dynamic Cheatsheet, introduced in Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory, addresses a structural inefficiency in how agents interact with tasks: each episode begins from scratch, discarding everything learned in prior attempts. The method counters this by maintaining an external memory of reusable procedural heuristics and workflow templates that the agent can consult and extend over time.

Two variants are proposed with different memory management strategies. **DC-Cu (Cumulative)** appends all experiences to the cheatsheet as they accumulate, preserving the full trace of learned knowledge but risking memory bloat. **DC-RS (Synthesis)** compresses prior experiences periodically, distilling them into compact, generalized insights that better survive distribution shift across tasks. The distinction matters: cumulative memory tends to excel early, while synthesis may generalize better over longer horizons.

The results reported in the originating paper are striking. GPT-4o's success rate on the Game of 24 increased from roughly 10% to 99% after the model discovered and persisted a Python-based solution strategy. On AIME 2024, Claude 3.5 Sonnet jumped from 23% to 50% accuracy under DC-Cu, more than doubling its baseline by retaining algebraic and combinatorial reasoning templates across problems. These gains reflect the core intuition: structured reasoning tasks share latent solution patterns, and a model that can recognize and reuse them gains a compounding advantage.

## Position in the Emerging Landscape

Dynamic Cheatsheet arrived as an early, influential demonstration that test-time learning through memory could yield substantial gains without retraining. It has since become a prominent baseline against which successor methods position themselves, which is itself revealing.

Agentic Context Engineering (ACE) reports outperforming Dynamic Cheatsheet by an average of 7.6% on the AppWorld benchmark in the online setting. More telling are the efficiency gaps: ACE achieves a 91.5% reduction in adaptation latency and an 83.6% reduction in token cost compared to Dynamic Cheatsheet on FiNER. This suggests that while Dynamic Cheatsheet's approach is effective, it is not particularly efficient: full-context rewrites or unbounded accumulation impose costs that compound at scale. ACE's architecture of incremental delta updates sidesteps this by making only localized edits rather than regenerating the full memory context.

ArcMemo similarly uses Dynamic Cheatsheet as a point of comparison when evaluating memory-assisted abstract reasoning on ARC-AGI-1. ArcMemo-PS achieves an official Oracle@2 score of 70.83 and a direct score of 59.33, representing a 7.5% relative gain over the no-memory baseline, on a task domain where the procedural knowledge Dynamic Cheatsheet specializes in is less obviously applicable.

Evo-Memory includes Dynamic Cheatsheet within its broader evaluation of test-time learning frameworks, treating it as a representative of the memory accumulation paradigm.

## Limitations and Open Questions

The primary limitation of Dynamic Cheatsheet is its accumulation model. Both DC-Cu and DC-RS face a form of the stability-plasticity dilemma: cumulative memory grows without bound, while synthesis compression risks discarding task-specific knowledge that doesn't generalize. Neither variant includes a principled mechanism for selectively forgetting outdated or incorrect heuristics, which matters increasingly as the agent encounters distribution shift across task types.

There is also a latent question about when procedural memory helps. The method's strongest reported results involve tasks with stable, reusable solution templates: symbolic puzzles, mathematical competition problems. It is less clear whether the same gains transfer to open-ended agentic tasks where the space of relevant procedures is larger and less structured. The comparison against ACE on AppWorld, a more complex multi-step task environment, suggests a performance gap in precisely this regime.

A further open question is the interaction between memory quality and model capability. The observed jump from 23% to 50% on AIME 2024 depends on the model first generating a correct solution that is then worth retaining. If the base model struggles to produce correct strategies in the first place, the memory mechanism has little to accumulate from. Dynamic Cheatsheet thus partially inherits its gains from model capability rather than the memory architecture alone.

Despite these limitations, Dynamic Cheatsheet remains a conceptually clean and empirically validated proof of concept: persistent procedural memory can substantially improve test-time performance without any weight updates, and the gains can be dramatic in the right task regime. Its role as a widely-used baseline reflects both its influence and the field's recognition that the memory design space it opened is far from exhausted.

## Key Findings

## Relationships

## Sources
