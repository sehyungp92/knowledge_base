---
type: source
title: 'KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation'
source_id: 01KJV8BD2M08NZNP5XVEDCJ3KC
source_type: paper
authors:
- Lei Liang
- Mengshu Sun
- Zhengke Gui
- Zhongshu Zhu
- Zhouyu Jiang
- Ling Zhong
- Yuan Qu
- Peilong Zhao
- Zhongpu Bo
- Jin Yang
- Huaidong Xiong
- Lin Yuan
- Jun Xu
- Zaoyang Wang
- Zhiqiang Zhang
- Wen Zhang
- Huajun Chen
- Wenguang Chen
- Jun Zhou
published_at: '2024-09-10 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- knowledge_and_memory
- post_training_methods
- reasoning_and_planning
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation

KAG proposes a neurosymbolic framework that tightly couples knowledge graphs with LLM-based generation to overcome the fundamental limitations of vector-similarity retrieval in professional domains. Rather than grafting graph structures onto RAG as a retrieval scaffold, KAG rebuilds the retrieval-reasoning pipeline around a symbolic logical form solver, a multi-layer knowledge representation standard (LLMFriSPG), and offline semantic alignment — achieving 12–19% F1 improvements over SOTA RAG on multi-hop QA benchmarks and 25+ percentage-point precision gains in production E-Government and medical deployments.

**Authors:** Lei Liang, Mengshu Sun, Zhengke Gui, Zhongshu Zhu, Zhouyu Jiang, Ling Zhong, Yuan Qu, Peilong Zhao, Zhongpu Bo, Jin Yang, Huaidong Xiong, Lin Yuan, Jun Xu, Zaoyang Wang, Zhiqiang Zhang, Wen Zhang, Huajun Chen, Wenguang Chen, Jun Zhou
**Published:** 2024-09-10
**Type:** paper

---

## Motivation

Standard [[themes/retrieval_augmented_generation|RAG]] systems retrieve by vector cosine similarity — a measure of textual proximity, not inferential relevance. This architectural choice has cascading consequences in professional domains:

- A query about "cataract patients visiting public leisure spaces" cannot retrieve a document about "facilities for the visually impaired" via embedding similarity, because the bridge requires the `isA` semantic relation — knowledge the vector space does not encode.
- LLMs' autoregressive next-token mechanism is inherently weak at deterministic operations: numerical comparisons, temporal ordering, set intersections, and logical entailment are all treated as undifferentiated token prediction problems.
- Existing GraphRAG extensions (GraphRAG, HippoRAG, ToG 2.0, DALK) introduce graph structures at the information-extraction level but do not address semantic directionality, logical sensitivity, or the granularity mismatch between OpenIE-extracted facts and validated domain knowledge. GraphRAG's hierarchical community summaries are structurally incompatible with multi-hop Q&A and incremental updates.

The result is that professional domain services — law, medicine, government — which require simultaneous accuracy, completeness, and logical rigor, are systematically underserved by the entire existing RAG family.

---

## Architecture

KAG is organized into five tightly coupled components:

### LLMFriSPG: Three-Layer Knowledge Representation

KAG upgrades the SPG knowledge standard into a three-layer hierarchy:
- **Raw chunks (RC):** original document segments
- **Graph information layer (KG\_fr):** schema-free OpenIE extraction
- **Knowledge layer (KG\_cs):** schema-constrained expert knowledge

Both layers coexist on the same entity types, allowing applications to tune precision/recall by choosing how much of each to populate. Each instance carries system built-in properties (`supporting_chunks`, `description`, `summary`, `belongTo`) forming a bidirectional inverted index — every graph node links back to its source text, preserving evidence traceability.

### Mutual Indexing

KAG-Builder constructs a mutual index between KG structure and text chunks via semantic chunking, context-enriched entity/event extraction, and domain knowledge injection. The chunk ID scheme encodes document adjacency directly into identifier space, making neighboring content structurally adjacent in the index.

### Logical Form Solver (LFS)

The core innovation. The LFS translates natural language questions into an executable symbolic language with five function types:

| Function | Role |
|---|---|
| `Retrieval` | SPO-structured graph lookup |
| `Sort` | ordering over retrieved sets |
| `Math` | LaTeX-syntax set operations |
| `Deduce` | entailment and comparison |
| `Output` | final answer assembly |

The planner decomposes complex queries into a DAG of logical sub-expressions. Each node executes via `GraphRetrieval` (structured KG traversal) first, falling back to `HybridRetrieval` (sparse + dense vector search over chunks) when graph results are absent or below threshold.

A multi-round reflection loop stores sub-answers in global working memory, judges sufficiency, generates supplementary queries, and re-enters the planning stage — enabling iterative refinement that single-pass retrieval cannot achieve. Unlike IRCoT or naive ensemble retrieval, inter-step variable dependencies are made explicit and symbolic, enabling deterministic numerical reasoning that LLM token prediction alone cannot reliably perform.

### Knowledge Alignment via Semantic Reasoning

Six semantic relation types — `synonym`, `isA`, `isPartOf`, `contains`, `belongTo`, `causes` — are predicted offline and applied online:

- **Offline:** entity disambiguation and fusion, instance-to-concept linking, and concept hierarchy completion propagate through `KG_fr` to increase connectivity and reduce synonymous node redundancy.
- **Online:** when a structured type match fails (e.g., `Political Party` not found), semantic reasoning predicts `Political Party contains Political Faction` and re-routes the query — replacing brittle type-matching with soft semantic navigation.

Knowledge alignment improves multi-hop retrieval top-5 recall by an average of 15.7% over baseline mutual-indexing across three datasets.

### KAG-Model

A general LLM fine-tuned across three axes — NLU, NLI (semantic reasoning), and NLG — using instruction reconstruction strategies (label bucketing, flexible I/O formats, task-guideline instructions). A `OneGen` module adds retrieval tokens to the LLM vocabulary and trains retrieval and generation jointly in a single forward pass, eliminating the separate retriever model entirely. KAG-Llama3 achieves 38.26% MRR on English hypernym discovery vs 23.47% for Llama3-8B and 30.04% for ChatGPT-3.5.

---

## Results

### Multi-hop QA Benchmarks (DeepSeek-V2 backbone, vs. IRCoT+HippoRAG)

| Dataset | EM improvement | F1 improvement |
|---|---|---|
| HotpotQA | +11.5pp | +12.5pp (76.2 vs 63.7) |
| 2WikiMultiHopQA | +19.8pp | +19.1pp |
| MuSiQue | +10.5pp | +12.2pp |

### Production Deployments

**E-Government Q&A (492 samples):**
- KAG: 91.6% precision, 71.8% recall
- NaiveRAG: 66.5% precision, 52.6% recall

**Medical KG (production):** 1.8M entities, 400K term sets, 5M relations, 700+ expert-authored DSL rules enabling deterministic medical indicator interpretation.

### Efficiency Trade-offs

| Method | Latency vs. CRref3 | F1 vs. LFSHref3 |
|---|---|---|
| LFSHref3 (KG+vector) | −100 to −150% slower | baseline |
| LFSref3 (KG-only) | −12 to −22% faster than LFSHref3 | −0.1 to −2.2pp |
| CRref3 (chunk-only) | +101 to +149% faster | significantly lower |

---

## Limitations and Open Questions

KAG's advances come with substantial hidden costs and unresolved failure modes:

**Construction bottleneck.** High-quality professional domain KG construction with strict schema constraints relies heavily on manual expert annotation — schema design, entity normalisation, authoring 700+ DSL rules. This is expensive and limits scalability to new domains. The production medical KG required a dedicated team of clinical experts. OpenIE-based alternatives introduce irrelevant noise that can significantly undermine retrieval precision — a fundamental tension with no clean resolution yet.

**Error propagation.** Incomplete or erroneous SPO triples from automated construction propagate through multi-hop reasoning chains, causing incorrect sub-query answers that cascade to wrong final answers. This degrades reliability in proportion to chain length — the system's core strength (multi-hop reasoning) is also its most fragile point.

**Latency.** Hybrid KG+vector multi-step reasoning (LFSHref3) is 100–150% slower than simple chunk retrieval. For production real-time applications, this is a blocking constraint. The KG-only variant (LFSref3) reduces computation by 12–22% with minimal F1 cost, but remains substantially slower than naive retrieval.

**Generalisation gaps.** All experiments are confined to three multi-hop QA benchmarks. There is no evaluation on open-domain retrieval, low-resource domains without pre-existing expert knowledge bases, or domains with sparse coverage. It is unknown how KAG degrades as domain KG completeness decreases.

**Instruction diversity.** Simply reformatting existing NLP datasets as instruction-tuning data achieves comparable performance on trained tasks but fails to generalise NLU capabilities to unseen domains. KAG-Model's 20,000+ diverse NLU instructions address this partially, but the generalisation boundary is not well characterized.

**Single-step retrieval ceiling.** Single-step vector retrieval produces results that are all highly similar to each other, failing to surface the semantically diverse intermediate steps required for multi-hop reasoning. This is not a failure of the KAG system — it is a fundamental limitation of the retrieval paradigm that KAG was designed to replace, and it highlights why any system relying on single-pass retrieval has a structural ceiling for complex queries.

---

## Connections

### Related Approaches

KAG sits at the intersection of [[themes/retrieval_augmented_generation|retrieval-augmented generation]] and [[themes/knowledge_and_memory|structured knowledge and memory]]. It differs from prior work in direction: while GraphRAG and HippoRAG graft graph structures onto retrieval pipelines, KAG treats the knowledge graph as the primary reasoning substrate and uses vector retrieval as a fallback.

The Logical Form Solver shares architectural philosophy with [[themes/reasoning_and_planning|chain-of-thought and planning]] approaches — specifically with IRCoT and ReAct — but externalises the reasoning trace into symbolic form rather than natural language, enabling deterministic computation at each step.

The KAG-Model fine-tuning strategy connects to [[themes/finetuning_and_distillation|fine-tuning and distillation]] work on instruction diversity and generalisation. The finding that naive dataset reformatting fails to generalise NLU capabilities echoes broader findings in the instruction-tuning literature about the importance of task and format diversity.

OneGen's unification of retrieval and generation tokens in a single forward pass is a notable architectural move within [[themes/post_training_methods|post-training methods]] — it eliminates the separate retriever model entirely, with implications for inference cost and deployment complexity.

### Implications for the Landscape

KAG makes concrete a claim that has been implicit in several research threads: **vector similarity is the wrong primitive for knowledge-intensive reasoning**. The gap is not merely quantitative (better embeddings) but qualitative — semantic relations like `isA`, `causes`, and `contains` are not recoverable from distance in embedding space, regardless of model scale. This has implications beyond RAG:

- Any [[themes/retrieval_augmented_generation|agentic retrieval]] system that relies solely on embedding similarity faces the same architectural ceiling for professional domain tasks.
- The production deployment results (E-Government, medical) suggest that the precision gap between vector retrieval and hybrid KG+vector retrieval is large enough to matter for real applications — not just benchmark performance.
- The latency overhead (2-3x) sets up a clean engineering trade-off that will likely drive research into approximate KG traversal, cached semantic alignment, and lightweight symbolic reasoning.

The hidden cost of expert annotation is the most underappreciated constraint. KAG's production deployments required domain expert teams — a cost that does not appear in benchmark comparisons. Any honest assessment of KAG-style systems for broad deployment must account for this, and it is an open question whether the annotation burden can be substantially reduced without sacrificing the precision advantages that motivate the approach.

---

## Key Claims

1. RAG retrieves by vector similarity, which conflates textual proximity with inferential relevance — producing incomplete and redundant results in professional domains.
2. LLMs are structurally weak at numerical reasoning, temporal comparisons, and logical operations — making pure generative approaches unreliable for typed knowledge tasks.
3. KAG achieves +19.6% relative F1 on HotpotQA and +33.5% on 2WikiMultiHopQA compared to SOTA RAG methods.
4. KAG outperforms IRCoT+HippoRAG with EM increases of 11.5%, 19.8%, and 10.5% on HotpotQA, 2WikiMultiHopQA, and MuSiQue respectively.
5. Multi-step retrieval generally outperforms single-step retrieval for multi-hop QA — single-step results cluster too closely to provide diverse intermediate reasoning steps.
6. E-Government Q&A: KAG achieves 91.6% precision and 71.8% recall vs 66.5% and 52.6% for NaiveRAG on 492 samples.
7. KG-only retrieval (LFSref3) reduces computation by 12–22% vs hybrid retrieval with only 0.1–2.2% F1 decrease — a viable latency/quality trade-off.
8. Knowledge alignment shifts node degree distributions rightward, improving top-5 recall by 9.2–28.4% across datasets.
9. KAG-Llama3 achieves 38.26% MRR on English hypernym discovery vs 23.47% for Llama3-8B and 30.04% for ChatGPT-3.5.
10. Errors in SPO triple extraction during KG construction propagate through multi-hop chains, causing cascading failures in final answers.

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/exact-match-em|Exact Match (EM)]]
- [[entities/graphrag|GraphRAG]]
- [[entities/hipporag|HippoRAG]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/ircot|IRCoT]]
- [[entities/musique|MuSiQue]]
- [[entities/personalized-pagerank|personalized PageRank]]
