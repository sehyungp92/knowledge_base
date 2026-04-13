---
type: entity
title: HyDE
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0005364147161145057
staleness: 0.0
status: active
tags: []
---
# HyDE

> HyDE (Hypothetical Document Embeddings) is a query-time retrieval technique that instructs an LLM to generate a hypothetical document that would answer a given query — in zero-shot, without any relevant labels — and then uses the embedding of that hypothetical document rather than the raw query embedding to search the corpus. By shifting retrieval into document space, HyDE bridges the systematic semantic gap between terse user queries and the richer language of stored documents, making it particularly valuable for agent memory retrieval where query phrasing rarely matches how knowledge was originally encoded.

**Type:** method
**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/context_engineering|Context Engineering]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]

## Overview

The core intuition behind HyDE is that query embeddings and document embeddings occupy meaningfully different regions of the embedding space. A user asking "what are the risks of deploying autonomous agents?" will embed differently than a paper paragraph describing those risks, even when they express the same underlying concern. HyDE sidesteps this mismatch by using an LLM to produce a plausible document — a hypothetical answer, explanation, or passage — and embedding *that* as the retrieval vector. Because the generated text is stylistically and structurally similar to the corpus it is meant to search, the resulting embedding sits closer to real documents than the query alone would.

In the context of agent memory systems, HyDE is classified as a memory retrieval technique — the third of three operators governing memory dynamics (formation, evolution, retrieval) identified in frameworks like Memory in the Age of AI Agents. It operates specifically on token-level memory: externally stored, discrete, human-inspectable text. When an agent needs to recall relevant experience or factual knowledge, HyDE transforms the retrieval step from a query-similarity search into a document-similarity search, improving recall for the kinds of rich, multi-sentence memory units that make up experiential and factual memory stores.

## Relationship to Graph-Based and Dual-Level Retrieval

HyDE is a query-rewriting strategy that is orthogonal to, and composable with, structural retrieval paradigms. Systems like LightRAG adopt dual-level retrieval — low-level retrieval targeting specific entities and their relational attributes, high-level retrieval targeting broader topics and themes — and incorporate graph structures into indexing to capture inter-entity dependencies that flat vector search misses. HyDE could in principle augment either level: a hypothetical document about a specific entity would improve low-level recall, while a hypothetical thematic overview would improve high-level recall.

Similarly, PathRAG prunes retrieval by extracting relational paths through a knowledge graph, prioritising structurally connected evidence over scattered fragments. Where PathRAG filters *what* gets retrieved after candidate generation, HyDE reshapes *how* candidates are generated in the first place. The two approaches address adjacent failure modes: HyDE corrects for query-document semantic distance; PathRAG corrects for relevance noise in graph-structured results.

## Limitations and Open Questions

HyDE carries several non-trivial limitations that constrain its deployment in real knowledge systems:

**Hallucination propagation.** The hypothetical document is generated without access to the actual corpus. If the LLM generates plausible-sounding but factually incorrect content, the embedding may retrieve documents that share the hallucinated framing rather than the true answer. In evidence-traced systems where every claim must link to a verbatim source snippet, this is a meaningful concern — HyDE retrieval can surface documents that appear topically similar to a wrong hypothesis.

**Latency cost.** Generating a hypothetical document adds a full LLM call before retrieval begins. In agentic pipelines where retrieval is invoked repeatedly across multi-step reasoning, this cost compounds. Architectures that use query decomposition to fan out multiple parallel sub-queries — like the `decompose_and_retrieve()` approach pairing each sub-query with hybrid search — would multiply this overhead if each sub-query required a HyDE expansion step.

**Query complexity scaling.** HyDE is well-calibrated for factual or expository queries where a plausible document can be imagined. It is less obviously useful for queries about *absence* ("what does source X not address?"), *relational structure* ("what connects concept A to concept B?"), or *temporal trajectory* ("how has this bottleneck evolved?"). These query types — common in landscape-model interrogation — may generate hypothetical documents that are structurally incompatible with the actual retrieval targets.

**Embedding model alignment.** HyDE's benefit depends on the embedding model treating hypothetical and real documents as near-neighbours. If the embedding model encodes stylistic or authorial features that differ between LLM-generated prose and the original corpus documents, the technique may yield less improvement than expected or even degrade over a strong query baseline.

The key open question is empirical: under what corpus conditions, query distributions, and embedding models does HyDE reliably outperform direct query embedding? The technique is theoretically well-motivated but its advantage is not uniform, and the agent memory literature has not yet produced rigorous ablations across memory store types (factual vs. experiential vs. working).

## Relationships

HyDE is positioned within the retrieval augmented generation literature alongside dual-level and graph-based retrieval strategies explored in LightRAG and PathRAG. Its memory-layer semantics — as a retrieval operator over token-level, externally stored memory — are situated within the agent memory taxonomy developed in Memory in the Age of AI Agents, which distinguishes retrieval from formation and evolution as a distinct phase of the memory lifecycle.

## Key Findings

## Sources
