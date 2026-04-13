---
type: source
title: Long Live Context Engineering - with Jeff Huber of Chroma
source_id: 01KJVK1H1AAMMZ39G04CH7AJRV
source_type: video
authors: []
published_at: '2025-08-19 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- knowledge_and_memory
- retrieval_augmented_generation
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Long Live Context Engineering - with Jeff Huber of Chroma

Jeff Huber (CEO of Chroma) makes the case that "RAG" is an outdated and misleading frame, and that the real discipline practitioners need is *context engineering* — the systematic optimization of what goes into a model's context window at each generation step. The conversation covers empirical evidence of context degradation, the emerging multi-stage retrieval pattern, code-specific retrieval strategies, and a forward-looking view on how parallel LLM inference will reshape the retrieval stack.

**Authors:** Jeff Huber (Chroma)
**Published:** 2025-08-19
**Type:** video

---

## Context Engineering vs. RAG

The term RAG conflates three distinct concepts — retrieval, augmentation, and generation — and has collapsed in practice to mean little more than single-pass dense vector search. Huber argues this framing obscures what actually matters: **context engineering**, a discipline within [[themes/retrieval_augmented_generation|AI engineering]] focused on deciding *what should be in the context window* for any given generation step.

Context engineering has two loops:
- **Inner loop** — for this query, which information do I include?
- **Outer loop** — over time, how do I improve my selection and prioritization strategy?

This framing applies universally: static knowledge-base chat, [[themes/agent_systems|agentic systems]], and [[themes/agent_memory_systems|agent memory]] all share the same fundamental problem of curating the right context. The distinction matters because it names the real optimization target and encourages systematic improvement rather than one-time setup.

---

## Context Rot: Empirical Evidence

Chroma published a technical report formalizing what practitioners had informally suspected: **LLM performance is not invariant to token count**. As context windows fill, models attend to fewer tokens and reason less effectively — a phenomenon Huber calls *context rot*.

Key findings:
- Frontier model marketing around "needle in a haystack" benchmarks (perfect green charts at 1M tokens) is misleading and does not reflect real utilization quality.
- In multi-turn agent interactions where the full conversation window is passed, token counts explode quickly and instructions clearly present in context begin to be ignored.
- The research originated from studying [[themes/agent_systems|agent learning]] — specifically whether giving agents access to prior successes/failures on SWE-bench would boost performance.

There is an open question about whether reasoning models handle context rot better than autoregressive models. Autoregressive models move strictly left-to-right and may miss earlier information; reasoning models can theoretically loop back and reconnect. This remains an active research area.

**This is arguably the most important limitation in the current AI stack**: developers cannot reliably leverage the large context windows frontier labs advertise.

---

## Limitations

- **Context degradation at scale** — model performance declines measurably with token count despite increasing context window sizes, making large-context claims by frontier labs difficult to trust in practice (severity: significant, trajectory: stable).
- **Marketing misalignment** — frontier labs publish "perfect" needle-in-a-haystack benchmarks while actual context utilization degrades, and they have no incentive to publish internal optimization findings (severity: significant, trajectory: stable).
- **Developer practices lag** — most developers building AI applications are still "yeeting everything into the context window" without any optimization (severity: significant, trajectory: improving).
- **Parallel inference constraints** — running 300 parallel LLM calls for reranking is impractical today due to tail latency and API availability issues, even when per-token costs are low (severity: significant, trajectory: improving).
- **Embedding-to-language roundtrip** — current retrieval architectures embed documents into latent space, then convert back to natural language for the model. Huber flags this as architecturally inefficient; direct embedding-to-model pipelines may emerge.
- **Continual retrieval adoption gap** — adaptive/continual retrieval during generation has been demonstrated in research (e.g., a paper teaching DeepSeek-R1 to retrieve mid-generation) but is not widely adopted in production, with limited tooling and ecosystem support.

---

## The Multi-Stage Retrieval Pattern

With N candidate chunks and Y available context slots, the problem is classic optimization: cull from tens of thousands of candidates to the handful that matter. A two-stage pattern is emerging:

1. **First-stage retrieval** — broad signals (vector search, full-text search, metadata filtering) reduce ~10,000 candidates to ~300.
2. **LLM reranker** — a language model brute-forces the ~300 down to 20–30 most relevant chunks.

LLM reranking is becoming cost-effective (some practitioners report ~$0.01 per million input tokens running models themselves), and purpose-built reranker models are likely to be displaced as general LLMs become 100–1000x faster and cheaper — analogous to how CPUs/GPUs displaced specialized ASICs for most workloads. The bottleneck today is tail latency across parallel inference calls, not cost.

**Generative benchmarking** (also from Chroma) enables quantitative evaluation of this pipeline: LLMs generate query-chunk pairs from existing document chunks, creating a golden dataset suitable both for retrieval evaluation and, in many cases, fine-tuning.

---

## Code Retrieval

Code search illustrates the complementary relationship between different retrieval modalities:

- **Regex/exact-match** handles approximately 85–90% of code queries and remains underappreciated. It excels when the developer knows exactly what they are looking for (function names, specific patterns). Google Code Search and GitHub Code Search both lean heavily on it.
- **Embeddings** cover the remaining 10–15% — queries based on semantic intent rather than known keywords. They are still early and underrated for code specifically.
- **Chunk rewriting** — generating a natural language description of a code chunk before embedding — meaningfully improves retrieval quality for code corpora by bridging the vocabulary gap.

The general principle: **invest heavily at ingestion time** (metadata extraction, chunk rewriting) to simplify the query-time task.

---

## Infrastructure: Why Modern Search for AI is Different

Huber argues that modern retrieval infrastructure for AI isn't just a rebrand of legacy search — it is a full rethinking driven by four structural differences:

| Dimension | Traditional Search | AI Search |
|---|---|---|
| **Technologies** | Inverted indexes, BM25 | Vector search, hybrid retrieval, embeddings |
| **Workload** | Web/enterprise patterns | AI-driven, agent-scale, high-parallelism |
| **Developer persona** | Legacy search engineers | AI/ML engineers, prompt-first mindset |
| **Result consumer** | Human (last-mile synthesis) | LLM (can digest orders of magnitude more) |

The last point is the most consequential: when an LLM is the consumer of search results, the design constraints change entirely. Systems like Chroma are built on modern distributed primitives (Rust, separation of storage/compute, multi-tenancy, object storage) that weren't available when legacy systems like Elasticsearch were designed.

---

## Connections

- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]] — core theme; Huber explicitly argues to retire this frame in favor of context engineering
- [[themes/agent_memory_systems|Agent Memory Systems]] — context rot research originated from agent learning experiments; adaptive retrieval during generation is a near-term capability direction
- [[themes/agent_systems|Agent Systems]] — multi-turn agent conversations are where context rot manifests most severely
- [[themes/knowledge_and_memory|Knowledge and Memory]] — the outer loop of context engineering is effectively a knowledge management problem
- [[themes/software_engineering_agents|Software Engineering Agents]] — code retrieval strategies (regex vs. embeddings, chunk rewriting) directly inform tool design for coding agents

---

## Open Questions

1. Do reasoning models (which can loop back through context) degrade less severely with token count than autoregressive models?
2. Will direct embedding-to-model pipelines emerge, eliminating the latent-space-to-natural-language roundtrip in retrieval?
3. Will continual/adaptive retrieval (retrieving mid-generation) become a standard capability, or remain a research artifact?
4. As frontier labs internalize context engineering, will they publish findings — or will this remain a dark art for the few companies with scale?
5. What is the right abstraction layer for the outer loop of context engineering — an evaluation framework, a fine-tuning pipeline, or something else?

## Key Concepts

- [[entities/context-engineering|Context Engineering]]
- [[entities/context-rot|Context rot]]
- [[entities/hybrid-search|Hybrid Search]]
