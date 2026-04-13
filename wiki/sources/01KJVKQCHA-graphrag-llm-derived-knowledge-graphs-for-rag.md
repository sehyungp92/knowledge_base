---
type: source
title: 'GraphRAG: LLM-Derived Knowledge Graphs for RAG'
source_id: 01KJVKQCHAW52432VG8DSK3X0Q
source_type: video
authors: []
published_at: '2024-05-04 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- alignment_and_safety
- hallucination_and_reliability
- knowledge_and_memory
- multi_agent_coordination
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GraphRAG: LLM-Derived Knowledge Graphs for RAG

> This source presents Microsoft's GraphRAG system, which augments retrieval-augmented generation with LLM-derived knowledge graphs. It demonstrates that vector similarity search is architecturally incapable of answering holistic dataset questions or multi-hop relational queries, and shows how graph-structured indices with hierarchical community detection overcome these limitations — at significant cost in tokens and latency.

**Authors:** Microsoft Research
**Published:** 2024-05-04
**Type:** Video

---

## Overview

[[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]] in its baseline form has a fundamental architectural ceiling: vectorizing a query and retrieving nearest neighbors cannot produce answers that require aggregating meaning across an entire document collection. GraphRAG is a parallel indexing and retrieval architecture designed to overcome this ceiling.

The system operates in two phases. First, an **indexing phase** processes private text data through an LLM, extracting not just named entities but the *relationships* between those entities and the *semantic weight* of those relationships — producing a knowledge graph richer than traditional co-occurrence networks. Second, an **orchestration phase** uses those pre-built indices to serve two retrieval modes: local search (entity neighborhood lookup) and global search (community summary aggregation). The resulting system can answer questions that baseline RAG demonstrably cannot.

---

## How It Works

### Indexing: From Text to Knowledge Graph

Baseline RAG chunks documents, embeds them, and stores them in a vector database. GraphRAG runs a parallel process over the same text chunks: each sentence is passed to an LLM, which performs reasoning operations to extract entities, the relationships between them, and the strength of those relationships. This is where model capability becomes critical — [[themes/knowledge_and_memory|GPT-4's semantic understanding]] of relationships enables weighted graph construction that goes far beyond simple co-occurrence counts.

Once the knowledge graph exists, **graph machine learning** performs hierarchical community detection — semantic agglomeration that partitions the graph into labeled communities at multiple granularities, from high-level topic clusters down to individual nodes. This produces a granular semantic filter allowing queries at any level of topic specificity across the full dataset.

### Retrieval: Local and Global Search

Two retrieval modes address different query types:

- **Local search**: Traverses entity neighborhoods in the knowledge graph. Suited for questions about specific entities, their relationships, and the chains between them. Enables multi-hop inference without requiring the entire document collection in context.
- **Global search**: Aggregates over pre-generated community summaries. Suited for holistic questions — themes, trends, cross-document patterns — that require dataset-wide semantic aggregation.

### Hallucination Mitigation

GraphRAG includes two grounding mechanisms. First, provenance tracking links each retrieved claim back to the originating source chunk, making it possible to audit answers against raw text. Second, an independent verification agent evaluates the answer against the provided context and produces a hallucination score — an after-the-fact grounding assessment that does not require modifying the generation process itself.

---

## Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| LLM-derived entity and relationship extraction | Demo | Produces semantically weighted graphs; quality depends on model capability |
| Hierarchical semantic community detection | Demo | Enables topic hierarchies at arbitrary granularity via graph ML |
| Holistic dataset analysis (themes, trends, aggregations) | Demo | Overcomes the core limitation of vector-only RAG |
| Multi-hop entity relationship inference | Demo | Traverses relationship chains across documents without massive context |
| Answer grounding with hallucination verification | Demo | Independent agent scores claim-context consistency |

The benchmark comparison is stark: when asked to identify specific targets associated with a paramilitary group, baseline RAG (including prompt-engineered variants) failed entirely. GraphRAG retrieved specific named targets — national television company, radio station, bank, terror attack locations — by traversing relationship chains distributed across source documents.

---

## Limitations and Open Questions

### Cost and Latency

GraphRAG is substantially more expensive than baseline RAG. The demonstrated comparison: **50,000 tokens and 71 seconds** for GraphRAG versus **5,000 tokens and 8 seconds** for baseline RAG — a 10× token cost and 9× latency increase. This is not incidental; it reflects the architectural requirement to aggregate over community summaries. For latency-sensitive or cost-constrained applications, this is a significant barrier. The trajectory of this limitation is **unclear** — it is partly a function of LLM pricing trends and partly structural.

### Upfront Indexing Cost

The knowledge graph must be pre-built across the entire document collection before retrieval is possible. This is a one-time but potentially expensive operation: every document must be processed by a capable LLM to extract entity-relationship signal. Dynamic or rapidly-updating corpora require re-indexing. This contrasts with baseline RAG, where documents can be added incrementally.

### Model Dependency

The quality of the knowledge graph is directly coupled to the semantic understanding of the LLM performing extraction. Weaker models produce lower-quality relationship signals, degrading the graph's utility downstream. This creates a dependency on frontier models for the indexing phase — raising cost and reducing portability. As model capabilities improve and costs fall, this limitation is expected to **improve**.

### What GraphRAG Still Cannot Do

The video does not address cases where the source documents themselves are ambiguous, contradictory, or thin. GraphRAG surfaces what is in the documents; it does not resolve conflicts between sources or identify gaps in coverage. Hallucination verification via a second agent is post-hoc — it detects grounding failures but does not prevent them during generation.

---

## Landscape Contributions

### Bottlenecks Addressed

GraphRAG directly targets two structural bottlenecks in [[themes/retrieval_augmented_generation|RAG systems]]:

1. **Holistic dataset analysis**: Vector similarity retrieval cannot answer queries like "what are the top themes in this dataset?" because vectorizing the query finds nearest neighbors to the query text, not semantic aggregates over the collection. GraphRAG's community detection and global search resolve this.

2. **Multi-hop relational reasoning**: Vector search cannot follow relationship chains between entities across documents. A query about "what targets did organization X identify?" requires traversing entity-relationship links, not finding similar text. GraphRAG's knowledge graph enables this directly.

Both bottlenecks were previously addressable only by loading entire document collections into a very large context window — expensive, slow, and bounded by context limits.

### Breakthrough

The core architectural contribution is demonstrating that **LLM-derived knowledge graphs with relationship-aware retrieval orchestration** can overcome the aggregation ceiling of vector-only RAG. This is characterized as a major breakthrough: it is not an incremental improvement to embedding quality or retrieval algorithms, but a structural addition that enables qualitatively different queries. See [[themes/knowledge_and_memory|knowledge and memory]] for related developments in how AI systems structure and access prior context.

---

## Connections

- **[[themes/agent_memory_systems|Agent Memory Systems]]**: The knowledge graph functions as a persistent, structured memory over a document collection — an externalized memory representation the orchestration layer can query. This connects to broader questions about how agents should store and retrieve structured knowledge versus raw embeddings.
- **[[themes/hallucination_and_reliability|Hallucination and Reliability]]**: The dual-mechanism approach (provenance tracking + independent verification agent) is notable as a practical hallucination mitigation strategy that does not require modifying the base model.
- **[[themes/multi_agent_coordination|Multi-Agent Coordination]]**: The use of an independent verification agent to evaluate the primary agent's output is a simple instance of multi-agent checking — a pattern with broader relevance for reliability in agentic systems.
- **[[themes/agent_systems|Agent Systems]]**: The orchestration layer that selects between local and global search based on query type is a lightweight form of agentic routing.
- **[[themes/alignment_and_safety|Alignment and Safety]]**: Provenance tracking and hallucination scoring are practical grounding mechanisms relevant to trustworthy AI deployment in analyst workflows.

---

## Open Questions

- At what corpus size and update frequency does GraphRAG's upfront indexing cost become prohibitive relative to its retrieval advantages?
- How does knowledge graph quality degrade as source documents become noisier, more contradictory, or more domain-specialized?
- Can the local/global retrieval modes be dynamically selected by the orchestration layer rather than requiring user specification?
- Does hierarchical community detection produce stable, interpretable communities across different document types, or is the granularity sensitive to corpus characteristics?
- What is the minimum model capability threshold for relationship extraction to produce graphs of useful quality?

## Key Concepts

- [[entities/graphrag|GraphRAG]]
