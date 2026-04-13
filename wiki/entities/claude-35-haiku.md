---
type: entity
title: Claude 3.5 Haiku
entity_type: entity
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- chain_of_thought
- computer_use_and_gui_agents
- frontier_lab_competition
- interpretability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- mechanistic_interpretability
- model_behavior_analysis
- post_training_methods
- reasoning_and_planning
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0013992972026861462
staleness: 0.0
status: active
tags: []
---
# Claude 3.5 Haiku

> Claude 3.5 Haiku is Anthropic's smaller, faster model in the Claude 3.5 family, serving as both a subject of mechanistic interpretability research and a benchmark participant in test-time learning experiments. Its significance spans two domains: as the model whose internal representations were probed in Anthropic's interpretability case studies, and as a reference point within the broader Claude 3.5 family whose Sonnet variant demonstrated dramatic performance gains under adaptive memory techniques.

**Type:** entity
**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/chain_of_thought|Chain of Thought]], [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/interpretability|Interpretability]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/mechanistic_interpretability|Mechanistic Interpretability]], [[themes/model_behavior_analysis|Model Behavior Analysis]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/test_time_learning|Test-Time Learning]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

Claude 3.5 Haiku is Anthropic's compute-efficient model in the Claude 3.5 generation, positioned as the interpretability case study subject in Tracing the thoughts of a large language model. A foundational tension defines this model family: Claude models are not directly programmed — they develop inscrutable internal strategies through training on large data corpora, making their reasoning behaviour opaque even to their own developers. This opacity is precisely what motivates Anthropic's interpretability research program, of which models in the Claude 3.5 family are the primary subjects.

## As an Interpretability Subject

The Claude 3.5 family sits at the centre of Anthropic's effort to reverse-engineer what language models are actually doing when they reason. The core challenge is structural: because these models learn rather than being explicitly programmed, the strategies they develop are not accessible through inspection of their weights in any human-readable form. The interpretability case studies treat Claude as both the object of study and, implicitly, a benchmark for how far [[themes/mechanistic_interpretability|mechanistic interpretability]] techniques have advanced. Whether the internal representations discovered generalise across the Haiku–Sonnet spectrum within the 3.5 family remains an open question — the lighter Haiku model may exhibit different circuit-level organisation given its smaller capacity, but this has not been systematically established.

## Performance Under Test-Time Learning

The closely related [[themes/test_time_learning|Dynamic Cheatsheet]] experiments — which used Claude 3.5 Sonnet as the primary evaluation model — reveal what is possible when the model family is augmented with adaptive external memory. Results were striking: on AIME 2024, accuracy more than doubled from 23% to 50% under the DC-Cu variant, and surged from 6.7% to 40.6% on AIME 2020–2024 under DC-RS. GPQA-Diamond performance rose from 59.6% to 68.7%, and MMLU-Pro Physics improved by 8 percentage points. A 30% accuracy gain on AIME 2025 was also recorded.

These gains are significant because they are achieved entirely at inference time, without modifying any model parameters — the system is compatible with black-box commercial APIs. The memory curator has no access to ground-truth labels and must self-assess correctness before updating the cheatsheet, which introduces an inherent reliability ceiling: the quality of retained insights is bounded by the model's self-evaluation accuracy.

Critically, naive memory approaches do not work. GPT-4o's AIME 2024 accuracy *fell* from 20% to 6.7% when using full-history appending, before recovering to 40% under DC-RS. This asymmetry between structured curation and raw context accumulation is one of the most practically important findings: more memory is not better memory; curated, compact, generalisable memory is what drives gains.

## Limitations and Open Questions

Several limitations bear emphasis. First, models in this family — including Haiku — operate by default in a stateless vacuum, processing each query independently with no carry-over of useful patterns across inference calls. Dynamic Cheatsheet addresses this architecturally, but the baseline limitation remains intrinsic to the model's design. Second, the interpretability findings surface a deeper epistemic problem: even after probing internal representations, the degree to which human-legible descriptions of model "strategies" reflect actual computational mechanisms is contested. Third, the performance gains from test-time learning are task-dependent — gains on structured mathematical reasoning (AIME, Game of 24) are larger and more consistent than on knowledge retrieval tasks, suggesting the technique amplifies procedural insight more than factual recall.

Whether Claude 3.5 Haiku specifically would exhibit comparable test-time learning gains to Sonnet — or whether capacity constraints limit the model's ability to generate and self-evaluate high-quality cheatsheet entries — is an open empirical question not addressed in the current literature.

## Relationships

- Tracing the thoughts of a large language model — primary interpretability source treating this model family as the study subject
- Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory — benchmark results on Claude 3.5 Sonnet demonstrating test-time adaptation
- Anthropic's Claude Computer Use Is A Game Changer — situates this model family within broader [[themes/computer_use_and_gui_agents|computer use and GUI agent]] capabilities
- Related entities: Claude 3.5 Sonnet (the higher-capacity sibling, primary benchmark subject), GPT-4o (cross-model comparison baseline in Dynamic Cheatsheet experiments)

## Key Findings

## Sources
