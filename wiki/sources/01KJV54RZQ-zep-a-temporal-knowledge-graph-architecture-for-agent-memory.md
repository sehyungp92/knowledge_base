---
type: source
title: 'Zep: A Temporal Knowledge Graph Architecture for Agent Memory'
source_id: 01KJV54RZQPDJQRT35JX596THH
source_type: paper
authors:
- Preston Rasmussen
- Pavlo Paliychuk
- Travis Beauvais
- Jack Ryan
- Daniel Chalef
published_at: '2025-01-20 00:00:00'
theme_ids:
- agent_evaluation
- agent_memory_systems
- evaluation_and_benchmarks
- knowledge_and_memory
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Zep: A Temporal Knowledge Graph Architecture for Agent Memory

Zep introduces Graphiti, a bi-temporal dynamic knowledge graph engine, as a production memory layer for LLM agents — demonstrating that selective graph-based retrieval can simultaneously outperform full-context prompting in accuracy (+18.5% on LongMemEval) while reducing latency by 90%, while also exposing the inadequacy of prevailing benchmarks and the genuine difficulty of enterprise-scale agent memory.

**Authors:** Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef
**Published:** 2025-01-20
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

[[themes/retrieval_augmented_generation|RAG]] systems are architecturally tied to static corpora — they retrieve from documents that don't change. Enterprise agent deployments break this assumption: conversation histories, user preferences, and business records evolve continuously, and no amount of context window expansion resolves the structural problem of maintaining a *valid* model of a changing world.

The prior SOTA, MemGPT, uses archival storage without temporal awareness and cannot be straightforwardly evaluated on demanding benchmarks. More fundamentally, the dominant evaluation benchmark (DMR) uses only 60-message conversations that fit comfortably inside modern context windows and tests only single-turn fact retrieval — meaning published accuracy numbers are essentially upper-bounded by what full-context prompting already achieves.

### Architecture: Three-Tier Temporal Graph

Zep's knowledge graph G = (N, E, φ) organizes memory into three hierarchical subgraphs:

1. **Episode subgraph** — raw messages stored non-lossily, preserving the original conversational record
2. **Semantic entity subgraph** — extracted entities and facts with deduplication, representing what the agent *knows*
3. **Community subgraph** — high-level entity clusters with summarizations, enabling thematic retrieval

This mirrors the episodic/semantic distinction from cognitive psychology: episodes are distinct events; semantics are durable concept associations. It extends [[entities/graphrag|GraphRAG]]'s community detection and AriGraph's episodic/semantic split — but adds temporal tracking present in neither.

### Bi-Temporal Modeling

The critical architectural innovation is the **bi-temporal model** with two independent timelines:

- **T** — chronological order of real-world events (resolves relative references like "two weeks ago")
- **T′** — transactional ingestion order (enables auditing and replay)

Each edge stores four timestamps: `t′_created`, `t′_expired` (transactional timeline) and `t_valid`, `t_invalid` (event timeline). When new facts contradict existing edges, an LLM detects the contradiction and invalidates the old edge by setting `t_invalid` to the new fact's `t_valid`. The graph represents a world where facts *change* rather than accumulate indefinitely — a fundamental shift from append-only vector stores.

### Retrieval Pipeline

Memory retrieval operates in three stages:

1. **Search (φ)** — hybrid: cosine semantic similarity + BM25 full-text + breadth-first graph traversal
2. **Reranker (ρ)** — RRF, MMR, episode-mention frequency, node-distance, or cross-encoder LLM scoring
3. **Constructor (χ)** — formats facts with date ranges and entity summaries into a structured context string

Entity extraction uses a Reflexion-inspired reflection technique to minimize hallucinations. Entity embeddings occupy a 1024-dimensional vector space. Crucially, graph updates use predefined Cypher queries rather than LLM-generated ones — a deliberate choice to enforce schema consistency and eliminate hallucination risk in the write path.

For community detection, Zep uses label propagation rather than the Leiden algorithm used by GraphRAG, enabling dynamic extension without full community refreshes (at the cost of gradual community divergence over time — see limitations).

---

## Results

| Benchmark | Model | Zep | Baseline | Delta |
|---|---|---|---|---|
| DMR | gpt-4-turbo | 94.8% | 94.4% | +0.4% |
| DMR | gpt-4o-mini | 98.2% | — | — |
| LongMemEval | gpt-4o-mini | 63.8% | 48.6% | +15.2% |
| LongMemEval | gpt-4o | 71.2% | 52.7% | +18.5% |

The DMR results are deliberately contextualized as near-meaningless: the benchmark is solved by full-context prompting. LongMemEval (avg. 115,000-token conversations) is where Zep's value becomes legible — and where gains concentrate in the hardest question types: single-session-preference (+77.7% to +184%), temporal-reasoning (+38–48%), multi-session (+16–30%).

Latency drops from ~30 seconds to ~3 seconds by compressing 115,000-token conversations to ~1,600-token graph contexts.

---

## Capabilities

- **Bi-temporal fact tracking** — four timestamps per edge separately recording when facts were recorded vs. when they were true, enabling temporal queries and auditable history *(narrow production)*
- **Context compression** — 115k → 1.6k tokens while improving accuracy, demonstrating retrieval architectures outperform brute-force full context even when windows are large enough *(narrow production)*
- **Hybrid graph search** — cosine similarity + BM25 + breadth-first traversal in a unified retrieval pipeline *(narrow production)*
- **Online incremental updates** — new episodes processed without reprocessing full history, enabling continuous memory formation *(narrow production)*
- **Temporal fact expiration** — automatic LLM-assisted contradiction detection with edge invalidation, maintaining a consistent world-state *(narrow production)*

---

## Limitations & Open Questions

### Confirmed Failure Modes

**Graph abstraction loses assistant-turn information.** On single-session-assistant questions, Zep underperforms full-context baseline by 9.06% (gpt-4o-mini) and 17.7% (gpt-4o). The entity/fact extraction pipeline discards information present in raw assistant turn text. This is the one consistent failure mode across both model scales and is currently unresolved.

**Weaker models struggle with bi-temporal metadata.** gpt-4o-mini fails to improve on knowledge-update questions (−3.36%) and shows inconsistent temporal reasoning. The bi-temporal representation adds complexity that smaller models cannot reliably exploit.

**Entity extraction has a 5-message context horizon.** Facts requiring longer contextual span for correct extraction are silently missed. This is a hard architectural constraint on the current ingestion implementation.

**Community summaries become stale.** Label propagation enables dynamic extension but causes community representations to gradually diverge from the global optimum. Periodic expensive full recomputation is required — the frequency of which is not specified.

**Multiple LLM calls per episode are expensive.** Graph construction requires entity extraction, entity resolution, fact extraction, temporal extraction, and edge invalidation checks per conversational episode. This makes high-throughput deployment economically challenging.

### Evaluation Gaps

**No benchmark for structured + unstructured fusion.** Zep's key enterprise differentiator — synthesizing conversational text with structured business data — has no published evaluation. Every benchmark used tests conversational-only memory.

**MemGPT cannot be compared on long-session benchmarks.** The framework lacks direct message history ingestion, leaving the competitive landscape unclear for the regime where Zep's temporal architecture matters most.

**Network latency confound.** Benchmarks were run client-in-Boston → AWS us-west-2, adding cross-continent latency to Zep measurements but not full-context baselines.

### Research Gaps Identified

- **Formal ontologies for LLM knowledge graphs** — current systems operate without ontological grounding, limiting schema consistency and domain-specific accuracy
- **Enterprise memory benchmarks** — DMR is inadequate; the field needs benchmarks combining structured business data, multi-session temporal reasoning, and realistic enterprise question types
- **Production scalability** — cost, latency, and throughput at enterprise scale are insufficiently addressed across the memory/RAG literature

---

## Landscape Position

### Themes
- [[themes/agent_memory_systems|Agent Memory Systems]]
- [[themes/knowledge_and_memory|Knowledge & Memory]]
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]
- [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]]
- [[themes/agent_evaluation|Agent Evaluation]]

### Bottlenecks Addressed / Exposed

**Addressed (partially):** The blocking limitation of static RAG for enterprise agents — Zep demonstrates a viable architecture for dynamic knowledge integration.

**Exposed (new):** Three bottlenecks crystallized:
1. LLM call overhead per episode blocks deployment at scale — fine-tuned extraction models are the identified path forward
2. Absence of enterprise memory benchmarks blocks reliable architecture comparison
3. Community summary staleness in dynamic graphs blocks accurate thematic retrieval without expensive periodic recomputation

### Breakthroughs

The simultaneous accuracy improvement and latency reduction on LongMemEval is significant: it falsifies the implicit assumption that larger context windows reduce the need for memory architecture. A 1,600-token graph context outperforms a 115,000-token raw context — the compression is not lossy in the aggregate, even if it loses specific assistant-turn detail.

The incremental online graph construction from conversational streams overcomes the static-corpus limitation that has constrained RAG since its introduction, enabling memory systems that continuously integrate new facts and automatically resolve contradictions without full reprocessing.

---

## Key Claims

1. Zep achieves 94.8% on DMR (gpt-4-turbo) vs. MemGPT's 93.4%, with marginal gains that contextualize how easy the benchmark has become.
2. On LongMemEval, Zep achieves +15.2% (gpt-4o-mini) and +18.5% (gpt-4o) over full-context baseline with 90% latency reduction.
3. Standard RAG is limited to static document retrieval; enterprise agents require dynamic synthesis of evolving conversation, preferences, and business data.
4. The bi-temporal model separates event timeline T from ingestion timeline T′, storing four timestamps per edge.
5. Contradicted edges are invalidated by setting `t_invalid` to the new fact's `t_valid` — not deleted, preserving historical record.
6. Three-tier graph hierarchy (episodes → entities → communities) mirrors episodic/semantic cognitive memory models.
7. Label propagation over Leiden enables dynamic community extension at the cost of gradual divergence from optimal community structure.
8. Predefined Cypher queries rather than LLM-generated queries enforce schema consistency in graph writes.
9. Single-session-assistant question performance regresses by up to 17.7%, revealing information loss in the graph abstraction layer.
10. No existing benchmark adequately evaluates the fusion of structured business data with conversational memory.

## Key Concepts

- [[entities/graph-based-rag|Graph-based RAG]]
- [[entities/graphrag|GraphRAG]]
- [[entities/longmemeval|LongMemEval]]
- [[entities/zep|Zep]]
