---
type: entity
title: Zep
entity_type: entity
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- context_engineering
- evaluation_and_benchmarks
- knowledge_and_memory
- model_commoditization_and_open_source
- multi_agent_coordination
- retrieval_augmented_generation
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0021584271266422454
staleness: 0.0
status: active
tags: []
---
# Zep

> Zep is a commercial memory management platform for AI agents, built around a temporal knowledge graph engine called Graphiti. It addresses a fundamental limitation of LLM-based agents — the inability to maintain accurate, evolving memories across long interaction histories — by preserving timestamped facts, resolving entity contradictions automatically, and enabling hybrid retrieval across semantic, lexical, and graph dimensions. Zep has emerged as one of the more rigorously evaluated commercial memory systems, benchmarked against both MemGPT and full-context baselines on datasets designed to stress long-horizon memory.

**Type:** entity
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/context_engineering|Context Engineering]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/software_engineering_agents|Software Engineering Agents]]

## Overview

Zep is built on the premise that agent memory is not a retrieval problem but a *temporal consistency* problem. Facts change, preferences evolve, and contradictions accumulate across sessions. Its underlying engine, Graphiti, tracks four timestamps per fact edge — `t'_created` and `t'_expired` on the transactional timeline, and `t_valid` and `t_invalid` on the event timeline — enabling the system to distinguish between when something was recorded and when it was actually true in the world. When new edges contradict semantically related existing edges with overlapping temporal validity, an LLM comparison step automatically invalidates the outdated facts rather than accumulating conflicting state.

Entity extraction feeds this graph: after extraction, each entity name is embedded into a 1024-dimensional vector space to support cosine similarity search for entity resolution, linking new mentions to existing nodes before incorporation. To reduce hallucinations and improve extraction coverage, Zep applies a reflection technique inspired by Reflexion immediately after the initial extraction pass. Once resolved, facts are written using predefined Cypher queries rather than LLM-generated queries — a deliberate tradeoff that sacrifices flexibility for schema consistency and hallucination resistance.

For community detection within the graph, Zep uses label propagation rather than the Leiden algorithm employed by GraphRAG. The choice reflects an operational constraint: label propagation supports incremental, dynamic extension without requiring full recomputation, which matters for a system ingesting new conversational data continuously.

## Retrieval Architecture

Zep exposes three search functions against the knowledge graph: cosine semantic similarity search (ϕ_cos), Okapi BM25 full-text search (ϕ_bm25), and breadth-first search over the graph structure (ϕ_bfs). Each targets a distinct similarity axis — lexical overlap, semantic meaning, and contextual neighborhood respectively — allowing the system to surface facts that a single-modality approach would miss. On top of these, Zep applies a graph-based episode-mentions reranker that boosts results based on how frequently an entity or fact has been mentioned within a conversation, approximating a salience signal without explicit annotation.

## Empirical Performance

On the Deep Memory Retrieval (DMR) benchmark established by the MemGPT team, Zep achieves 94.8% accuracy versus MemGPT's 93.4%. However, this benchmark has a structural limitation that Zep's own paper is candid about: DMR conversations contain only around 60 messages, which easily fit within current LLM context windows. This means a naive full-context approach performs competitively, making DMR a weak differentiator for memory systems.

LongMemEval provides a more demanding test. Conversations average approximately 115,000 tokens in length — still within the context windows of frontier models, but at a scale where memory selectivity and organization begin to matter. Against full-context baselines on LongMemEval, Zep achieves accuracy improvements of up to 18.5% while reducing response latency by 90%. The gains are not uniform: they are most pronounced on complex question types — single-session-preference (184% improvement with GPT-4o), temporal reasoning, and multi-session questions — where the knowledge graph's structured temporal representation offers the largest advantage over flat retrieval.

## Limitations and Open Questions

Zep's performance profile has a notable weak spot. On single-session-assistant questions, performance *drops* relative to baseline — by 17.7% for GPT-4o and 9.06% for GPT-4o-mini. This suggests the graph construction and retrieval pipeline introduces noise or omissions that hurt in scenarios where the raw conversational context would have sufficed. The system itself acknowledges this as an area requiring further development.

More broadly, the benchmark situation for memory systems remains unsatisfying. Both DMR and LongMemEval have structural properties — short conversations or frontier-model-fitting lengths respectively — that limit their ability to stress-test memory systems in the regimes where they are most needed: very long interaction histories across many sessions with evolving user state. Zep's strong results on LongMemEval are meaningful, but the benchmark's conversation lengths still sit within frontier context windows, softening the case for graph-based memory over selective summarization or full-context approaches.

## Relationships

Zep's architecture directly competes with Mem0, which takes a different approach to long-term memory through hierarchical memory stores rather than a temporal knowledge graph. The DMR benchmark, originally designed to evaluate MemGPT, serves as a shared comparison point between systems. Zep is also evaluated in the context of the broader [[themes/agent_memory_systems|agent memory systems]] landscape, where the core open question is whether structured graph representations outperform retrieval-augmented approaches over flat stores as conversation length and session count scale. The 2024 Year in Review situates Zep within the commercial infrastructure layer emerging around agents, where memory management is becoming a distinct product category alongside inference and orchestration.

## Key Findings

## Sources
