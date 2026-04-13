---
type: entity
title: Graph-based RAG
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- ai_business_and_economics
- evaluation_and_benchmarks
- knowledge_and_memory
- retrieval_augmented_generation
- startup_and_investment
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00033684171293312
staleness: 0.0
status: active
tags: []
---
# Graph-based RAG

Graph-based Retrieval Augmented Generation (Graph-based RAG) is a family of retrieval methods that organizes text databases as graphs — where nodes represent entities or concepts and edges encode their relationships — enabling AI systems to answer queries that require synthesizing information across multiple document segments rather than retrieving isolated passages. Unlike flat vector search, graph-based RAG captures structural relationships between entities, making it particularly suited for global-level reasoning tasks such as temporal tracking, preference inference, and multi-session memory. Its significance has grown alongside the rise of long-horizon AI agents, where maintaining coherent, queryable memory across extended interactions is a core unsolved challenge.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/retrieval_augmented_generation|Retrieval Augmented Generation]], [[themes/startup_and_investment|Startup and Investment]], [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Overview

Graph-based RAG emerged as a response to the limitations of purely semantic vector search, which retrieves individual passages without regard for how entities relate across a document corpus. By structuring the retrieval substrate as a graph, these methods can traverse relational paths, detect contradictions between facts, and aggregate community-level summaries — capabilities that flat similarity search cannot provide.

The core design principle is that text is not just a bag of embeddings but a network of entities and their evolving relationships. Graph-based RAG systems typically combine multiple retrieval signals: cosine semantic similarity over entity embeddings, full-text keyword search (e.g., Okapi BM25), and graph traversal (e.g., breadth-first search) to capture contextual proximity. Each signal targets a different aspect of similarity — word overlap, semantic meaning, and relational context — and their combination is what gives graph-based RAG its advantage on complex question types.

## Key Findings

### Retrieval Architecture

The most concrete instantiation of graph-based RAG in the evidence base is Zep, which implements a three-pronged retrieval system: cosine similarity over a 1024-dimensional entity embedding space, BM25 full-text search, and breadth-first search over the knowledge graph. These three signals are complementary: full-text search handles lexical overlap, cosine similarity captures paraphrase and semantic drift, and BFS surfaces entities that are contextually linked even when not directly mentioned. Zep further augments this with an episode-mentions reranker that boosts results based on how frequently an entity or fact appears across a conversation — a graph-native signal that flat retrieval systems cannot easily replicate.

A notable architectural choice in Zep is its use of predefined Cypher queries rather than LLM-generated database queries for graph population. This trades flexibility for reliability: LLM-generated queries risk schema inconsistency and hallucinated graph structure, while predefined queries enforce stable formats. This design decision reflects a broader tension in graph-based RAG between expressiveness and robustness.

### Temporal Awareness

One of the structural advantages of graph-based RAG is its natural support for temporal reasoning. Zep's underlying graph engine, Graphiti, tracks four timestamps per fact edge — creation and expiration on the transactional timeline, and validity start and end on the event timeline. When new edges contradict existing ones with temporally overlapping validity windows, the system automatically invalidates the older edges using LLM comparison. This gives the knowledge graph a form of belief revision that flat retrieval systems lack entirely.

This temporal architecture directly enables one of Zep's most striking results: a 184% improvement on single-session-preference questions with GPT-4o on the LongMemEval benchmark, where conversations average ~115,000 tokens. Temporal and multi-session question types showed similarly large gains — precisely the categories where structural, time-aware retrieval provides the greatest leverage over naive full-context approaches.

### Community Detection

Graph-based RAG systems must also handle the problem of community structure — how to group related entities for summarization and routing. Microsoft's GraphRAG uses the Leiden algorithm for community detection. Zep diverges from this by using label propagation instead, motivated by label propagation's support for dynamic extension: as new entities and edges arrive continuously in a live agent memory system, the community structure must update incrementally rather than being recomputed from scratch. This is a practical architectural constraint that differentiates production-grade graph-based RAG from offline batch systems.

### Performance and Limitations

On the LongMemEval benchmark — currently the most demanding public evaluation for agent memory — Zep achieves up to 18.5% accuracy improvement over baseline full-context implementations while reducing response latency by 90%. This latency reduction is significant: full-context approaches that stuff 115,000-token conversations into the model context are computationally expensive and will not scale as memory grows. Graph-based retrieval offers a principled path toward bounded-cost memory access.

However, the results are not uniformly positive. Zep shows decreased performance on single-session-assistant questions — a 17.7% drop with GPT-4o — suggesting that graph construction overhead and potential extraction errors hurt performance in the simpler, shorter-horizon cases where full-context retrieval is already adequate. This points to a real limitation: graph-based RAG adds complexity that only pays off at scale or in high-relational-density scenarios.

### Benchmark Critique

A recurring theme in this evidence base is the inadequacy of existing benchmarks for evaluating memory systems. The Deep Memory Retrieval (DMR) benchmark — where Zep achieves 94.8% versus MemGPT's 93.4% — has been critiqued as misleading: conversations contain only 60 messages, easily fitting within current LLM context windows. A simple full-context approach achieves near-ceiling performance, making DMR inadequate as a discriminative test. LongMemEval, with its ~115,000-token conversations, is a more honest stress test of whether graph-based memory actually outperforms brute-force context stuffing.

## Relationships

Graph-based RAG is directly implemented by Zep via the Graphiti engine, which extends graph-based memory retrieval with temporal edge tracking. It is contrasted with flat vector RAG and full-context approaches in the evaluation literature, and is architecturally related to Microsoft's GraphRAG (which shares the community detection and entity extraction design philosophy but targets batch document corpora rather than live agent memory). The method is a central technical substrate for [[themes/agent_memory_systems|agent memory systems]] and feeds directly into capability assessments under [[themes/evaluation_and_benchmarks|evaluation and benchmarks]], particularly as the field moves toward long-horizon agentic tasks where memory coherence over thousands of conversational turns becomes a bottleneck. The commercial angle is relevant too: as noted in Building the Easy Button for Generative AI, enterprise AI adoption is increasingly gated on reliability and structured knowledge access — exactly the problem graph-based RAG targets.

## Limitations and Open Questions

## Sources
