---
type: entity
title: GraphRAG
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- chain_of_thought
- context_engineering
- evaluation_and_benchmarks
- finetuning_and_distillation
- hallucination_and_reliability
- knowledge_and_memory
- multi_agent_coordination
- post_training_methods
- reasoning_and_planning
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.003957561930812384
staleness: 0.0
status: active
tags: []
---
# GraphRAG

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A retrieval-augmented generation approach that derives an entity knowledge graph from source documents and applies community detection to extract hierarchical summaries, enabling flexible retrieval at varying granularities.

## Key Findings

1. The DMR benchmark is inadequate for evaluating memory systems because conversations contain only 60 messages, which easily fit within current LLM context windows, making simple full-context approaches (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
2. Entity names are embedded into a 1024-dimensional vector space to enable cosine similarity search for entity resolution (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
3. Zep outperforms MemGPT on the Deep Memory Retrieval benchmark with 94.8% accuracy versus MemGPT's 93.4% (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
4. Zep implements an episode-mentions reranker that prioritizes results based on frequency of entity or fact mentions within a conversation (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
5. Zep implements three search functions: cosine semantic similarity search, Okapi BM25 full-text search, and breadth-first search over the knowledge graph (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
6. Zep shows decreased performance on single-session-assistant questions (17.7% drop for gpt-4o, 9.06% for gpt-4o-mini), suggesting further development is needed (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
7. Zep achieves accuracy improvements of up to 18.5% on LongMemEval while reducing response latency by 90% compared to full-context baseline implementations (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
8. Graphiti tracks four timestamps per fact edge: t'_created and t'_expired on the transactional timeline, and t_valid and t_invalid on the event timeline (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
9. When new edges contradict existing edges with temporally overlapping validity, Graphiti automatically invalidates the affected existing edges using LLM comparison (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
10. Zep uses a label propagation algorithm for community detection rather than the Leiden algorithm used by GraphRAG, because label propagation supports straightforward dynamic extension (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
11. Zep shows the largest accuracy gains on complex question types: single-session-preference (184% improvement with gpt-4o), temporal-reasoning, and multi-session questions (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
12. Zep uses predefined Cypher queries rather than LLM-generated database queries to ensure consistent schema formats and reduce hallucinations (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
13. The three search methods target different aspects of similarity: full-text search identifies word similarities, cosine similarity captures semantic similarities, and BFS reveals contextual similaritie (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
14. LongMemEval conversations average approximately 115,000 tokens in length and remain within context windows of current frontier models (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")
15. Zep uses a reflection technique inspired by Reflexion to minimize hallucinations and enhance extraction coverage during entity extraction (from "Zep: A Temporal Knowledge Graph Architecture for Agent Memory")

## Relationships

## Limitations and Open Questions

## Sources
