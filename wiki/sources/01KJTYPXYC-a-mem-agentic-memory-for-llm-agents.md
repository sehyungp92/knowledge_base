---
type: source
title: 'A-MEM: Agentic Memory for LLM Agents'
source_id: 01KJTYPXYCXN0MEW6SXXMSVFST
source_type: paper
authors:
- Wujiang Xu
- Zujie Liang
- Kai Mei
- Hang Gao
- Juntao Tan
- Yongfeng Zhang
published_at: '2025-02-17 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# A-MEM: Agentic Memory for LLM Agents

**Authors:** Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
**Published:** 2025-02-17 00:00:00
**Type:** paper

## Analysis

# A-MEM: Agentic Memory for LLM Agents
2025-02-17 · paper · Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan et al. (6 total)
https://arxiv.org/pdf/2502.12110

---

### Motivation & Prior Limitations
Existing LLM agent memory systems provide only basic storage and retrieval, requiring developers to predefine memory structures, storage points, and retrieval timing in advance, which fundamentally limits adaptability across diverse tasks.
- Prior systems such as MemGPT, MemoryBank, and ReadAgent rely on rigid operational patterns that constrain both memory writing and retrieval, leading to poor generalization in new environments and limited effectiveness in long-term interactions.
  - MemGPT uses a cache-like architecture prioritizing recency but cannot forge novel connections or reorganize knowledge as it evolves.
  - Mem0 incorporates graph databases for structure, but predefined schemas and relationships prevent the system from developing new organizational patterns when knowledge evolves — for example, when an agent learns a novel mathematical solution, it can only categorize within a preset framework.
- Agentic RAG systems exhibit agency in the retrieval phase (deciding when and what to retrieve) but maintain static knowledge bases, failing to address the deeper need for autonomous memory structure evolution during storage.

---

### Proposed Approach
A-MEM introduces an agentic memory system inspired by the Zettelkasten knowledge management method, enabling LLM agents to dynamically organize, link, and evolve memories without predefined structures or fixed workflows.

- **Note Construction:** Each new memory interaction is processed into a structured note `mi = {ci, ti, Ki, Gi, Xi, ei, Li}` containing the original content, timestamp, LLM-generated keywords (`Ki`), LLM-generated tags (`Gi`), a rich contextual description (`Xi`), a dense embedding vector (`ei`) computed from the concatenation of all textual fields, and a link set (`Li`).
  - The LLM generates semantic components autonomously from the raw interaction using prompt templates, enabling implicit knowledge extraction beyond surface content.

- **Link Generation:** When a new memory note is added, cosine similarity over embeddings identifies the top-k nearest historical memories, and an LLM then analyzes these candidates to determine whether meaningful connections should be established — capturing nuanced causal, conceptual, or attribute-based relationships that embedding similarity alone cannot detect.
  - This implements Zettelkasten's flexible linking principle while going beyond simple vector proximity, allowing a single memory to belong to multiple overlapping "boxes" (clusters) simultaneously.

- **Memory Evolution:** After link generation, each retrieved neighbor memory is re-evaluated by the LLM in light of the new memory and its other neighbors; its contextual description, keywords, and tags are updated if warranted, replacing the original entry.
  - This process mimics human memory consolidation: as new experiences accumulate, the entire memory network continuously refines itself, enabling higher-order patterns and attributes to emerge organically over time.

- **Retrieval:** At inference time, query embeddings are compared via cosine similarity to all stored note embeddings; the top-k retrieved memories (default k=10) are injected as context, and linked memories within the same "box" are automatically co-retrieved, enriching multi-hop reasoning chains.

---

### Results & Capabilities
A-MEM achieves state-of-the-art performance across six foundation models (GPT-4o-mini, GPT-4o, Qwen2.5 1.5B/3B, Llama 3.2 1B/3B) on the LoCoMo long-term conversational QA benchmark, consistently ranking first across models and task categories.

- On LoCoMo multi-hop tasks, A-MEM with GPT-4o-mini achieves an F1 of 27.02 versus MemGPT's 26.65 and LoCoMo baseline's 25.02, and on temporal reasoning tasks it reaches F1 45.85 — approximately 80% higher than MemGPT's 25.52 — demonstrating particular strength where complex cross-session reasoning chains are required.
  - For smaller open-source models (e.g., Llama 3.2 3B), A-MEM achieves average F1/BLEU rankings of 1.0 across all five categories, outperforming all baselines by wide margins, suggesting the approach compensates effectively for weaker base model capacity.

- On the DialSim dataset (derived from TV show long-term multi-party dialogues, ~350,000 tokens, 1,300 sessions), A-MEM achieves F1 of 3.45 — a 35% improvement over LoCoMo baseline (2.55) and 192% improvement over MemGPT (1.18) — with gains across all six evaluation metrics (F1, BLEU-1, ROUGE-L, ROUGE-2, METEOR, SBERT Similarity).

- A-MEM is highly token-efficient: each memory operation requires approximately 1,200 tokens, representing an 85–93% reduction compared to LoCoMo and MemGPT baselines (which use ~16,900 tokens), at a cost under $0.0003 per operation with commercial APIs.
  - Processing time averages 5.4 seconds with GPT-4o-mini and 1.1 seconds with locally-hosted Llama 3.2 1B on a single GPU.

- Retrieval scales sub-linearly in practice: at 1 million stored memories, retrieval time grows from 0.31µs to only 3.70µs, and storage overhead is identical (linear O(N)) to simpler baselines like MemoryBank, confirming no architectural penalty for the richer representation.

- Ablation study confirms that both Link Generation (LG) and Memory Evolution (ME) contribute independently and complementarily: removing both causes severe degradation (multi-hop F1 drops from 27.02 to 9.65); removing only ME yields intermediate performance (21.35), establishing LG as the foundational component and ME as an essential refinement layer.

- T-SNE visualizations of memory embeddings show that A-MEM produces tighter, more coherent clusters compared to the base system without LG and ME, providing geometric evidence that the evolved memory network develops meaningful internal structure.

---

### Implications
A-MEM reframes agent memory a

## Key Claims

1. Current memory systems for LLM agents enable basic storage and retrieval but lack sophisticated memory organization, despite recent attempts to incorporate graph databases.
2. Existing memory systems have fixed operations and structures that limit their adaptability across diverse tasks.
3. Graph database-based memory systems like Mem0 rely on predefined schemas and relationships, which fundamentally limits their adaptability to novel knowledge.
4. In A-MEM, each memory note is structured with seven components: original content, timestamp, LLM-generated keywords, LLM-generated tags, LLM-generated contextual description, a dense embedding vector,
5. A-MEM generates dense vector representations for memory notes by concatenating content, keywords, tags, and contextual description before encoding with a text encoder.
6. A-MEM's LLM-driven link generation can identify subtle patterns, causal relationships, and conceptual connections that go beyond what simple embedding similarity can detect.
7. A-MEM's agentic memory approach is distinct from agentic RAG: while agentic RAG applies agency at retrieval time, A-MEM applies agency at the storage and evolution level, enabling the memory structure
8. A-MEM achieves superior performance over all baselines for non-GPT foundation models across all task categories on the LoCoMo dataset.
9. A-MEM achieves at least double the performance of GPT-based baselines on Multi-Hop tasks that require complex reasoning chains.
10. A-MEM achieves an F1 score of 3.45 on DialSim, representing a 35% improvement over LoCoMo's 2.55 and 192% improvement over MemGPT's 1.18.

## Capabilities

- Zettelkasten-inspired agentic memory system (A-MEM) enables LLM agents to dynamically organize memories into self-evolving knowledge networks without predefined schemas — each memory note contains structured attributes (keywords, tags, contextual descriptions, embeddings), automatically links to rel
- Agentic memory with autonomous link generation and evolution achieves at least 2x improvement on multi-hop reasoning tasks requiring synthesis across conversation sessions, compared to prior static memory systems
- Dynamic memory network retrieval scales to 1 million memory entries with sub-4µs retrieval time (3.70µs at 1M entries vs 0.31µs at 1K), achieving O(N) linear space complexity with no additional storage overhead compared to flat vector stores
- Selective top-k memory retrieval with LLM-driven link traversal reduces token usage per memory operation by 85–93% compared to full-context methods (LoCoMo, MemGPT), dropping from ~16,900 tokens to ~1,200 tokens per operation while achieving superior reasoning performance
- Memory evolution mechanism enables existing agent memories to update their contextual descriptions, keywords, and tags in response to new incoming experiences — allowing the memory network to discover higher-order patterns and relationships over time without any human curation

## Limitations

- Memory organization quality is inherently bounded by the underlying LLM's capabilities — different base models produce different contextual descriptions and connection patterns, introducing model-dependent variance into the memory structure's accuracy and usefulness
- A-MEM is limited to text-only modalities and cannot process or store multimodal memory (images, audio) — a significant gap for agents operating in real-world environments where interactions span multiple modalities
- Each memory write operation requires multiple sequential LLM calls (note construction, link generation, memory evolution) resulting in 5.4 seconds latency with GPT-4o-mini — making real-time memory updates impractical for high-frequency agent interactions
- Memory retrieval performance plateaus and sometimes degrades at high k values — retrieving too many memories introduces noise and exceeds the model's effective processing capacity, creating a hard ceiling on useful context richness
- Evaluation is entirely confined to conversational QA benchmarks (LoCoMo, DialSim) — no evaluation in actual agentic task execution contexts (tool use, multi-step planning, computer use), leaving real-world agent memory performance unvalidated
- Absolute performance on long-term conversational benchmarks remains low even with best system — F1 of 3.45 on DialSim and 27.02% on LoCoMo multi-hop tasks reveals hard remaining problems in long-term memory utilization regardless of memory architecture improvements
- No mechanism for handling conflicting or contradictory memories — when new experiences contradict existing memories, the evolution mechanism updates contextual descriptions without explicit conflict detection or resolution, risking silent misinformation accumulation in the memory network
- No privacy or security analysis for personal memory storage — verbatim interaction history with timestamps and dense semantic links creates a rich personal profile, but the paper provides no discussion of access control, encryption, data retention, or extraction risk
- A-MEM's retrieval is consistently slower than simpler flat vector stores at all scales — at 1M entries, A-MEM retrieves in 3.70µs vs MemoryBank's 1.91µs — the richer memory structure imposes a persistent latency premium even though it is sub-millisecond in absolute terms

## Bottlenecks

- Memory write latency from multiple sequential LLM calls (note construction + link generation + memory evolution) creates a practical barrier for deploying dynamic agentic memory in high-frequency real-time interactions — 5.4 seconds per write with API models blocks synchronous memory updates
- Effective context processing limit constrains how many retrieved memories can be usefully synthesized per LLM call — performance plateaus and degrades when retrieved memory count exceeds model capacity, blocking deep historical synthesis even when all relevant memories have been correctly retrieved

## Breakthroughs

- A-MEM demonstrates that Zettelkasten-style atomic note-taking with autonomous link generation and memory evolution eliminates the need for predefined memory schemas in LLM agent systems — the memory network self-organizes, forms cross-memory semantic connections, and evolves memory representations w

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]

## Key Concepts

- [[entities/bleu-1|BLEU-1]]
- [[entities/mem0|Mem0]]
- [[entities/memorybank|MemoryBank]]
- [[entities/readagent|ReadAgent]]
- [[entities/agentic-rag|agentic RAG]]
