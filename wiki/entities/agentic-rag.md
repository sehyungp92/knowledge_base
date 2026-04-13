---
type: entity
title: agentic RAG
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- reasoning_and_planning
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00040473258791025237
staleness: 0.0
status: active
tags: []
---
# agentic RAG

> Agentic RAG is a retrieval-augmented generation paradigm in which an LLM agent actively controls the retrieval process — deciding when, what, and how to query — as part of an autonomous, multi-step reasoning loop. Unlike passive RAG pipelines that retrieve once at query time, agentic RAG treats retrieval as a tool the agent wields iteratively, making it the closest RAG variant to genuine agent memory and a foundational building block for long-horizon reasoning systems.

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Agentic RAG emerges from the recognition that static, single-shot retrieval is insufficient for tasks requiring multi-hop reasoning, long conversational histories, or dynamically evolving knowledge. In the agentic framing, retrieval becomes a first-class action: the agent plans what information it needs, issues queries, integrates the results into its reasoning state, and decides whether additional retrieval passes are necessary before producing output. This loop-based architecture is what distinguishes agentic RAG from conventional RAG, and what makes it structurally analogous to how memory works in cognitive systems — formation, evolution, and retrieval as distinct, composable operations.

## Key Findings

### Memory as Structured, Evolving State

The most developed instantiation of agentic RAG principles in recent literature is A-MEM: Agentic Memory for LLM Agents, which treats each retrieved or stored unit not as a raw text chunk but as a richly structured *memory note*. Each note carries seven components: original content, timestamp, LLM-generated keywords, tags, a contextual description, a dense embedding vector, and inter-note links. The embedding is computed over a concatenation of all textual fields — content, keywords, tags, and description — rather than content alone, which allows retrieval to match on synthesized context rather than surface similarity.

Crucially, A-MEM includes two modules absent from conventional RAG: **Link Generation**, which constructs associative edges between notes, and **Memory Evolution**, which consolidates and updates notes over time. Ablation results confirm both are load-bearing: removing them causes substantial degradation, particularly on multi-hop reasoning and open-domain tasks. This points to a structural insight — agentic RAG's advantage over passive RAG is not just in *when* it retrieves, but in whether the memory substrate itself evolves through use.

### Scalability and Efficiency

A persistent concern with agentic memory systems is whether they remain tractable at scale. A-MEM's retrieval time grows from 0.31µs at 1,000 memories to 3.70µs at 1,000,000 — near-linear and practically negligible. By contrast, ReadAgent's retrieval degrades catastrophically, exceeding 120,000µs at the same scale. Both systems share O(N) linear space complexity, so the divergence is entirely in retrieval architecture.

Token efficiency tells a similar story: A-MEM uses approximately 1,200 tokens per memory operation, an 85–93% reduction versus LoCoMo and MemGPT which consume ~16,900 tokens per operation. Processing latency averages 5.4 seconds with GPT-4o-mini and drops to 1.1 seconds with a locally-hosted Llama 3.2 1B, suggesting the approach is viable even in resource-constrained deployments.

These numbers matter because they constrain where agentic RAG is deployable in practice. The benchmark results — 35% F1 improvement over LoCoMo and 192% over MemGPT on DialSim, tested on conversations averaging 9K tokens across up to 35 sessions — are only meaningful if the system remains tractable at that conversational depth.

### Reasoning Integration

Agentic Reasoning extends the agentic RAG concept toward deep research tasks, pairing retrieval with a **Mind-Map** knowledge graph that stores and structures real-time reasoning context by transforming the model's raw reasoning chain into graph form. This treats the reasoning trace itself as a memory substrate — not just a scratchpad but a retrievable, structured artifact. The result narrows the open-source/proprietary gap to 2.8% on Humanity's Last Exam and achieves 81.2% on GPQA with DeepSeek-R1, surpassing o3-mini-high's 79.7% and improving nearly 10 percentage points over the base model.

Memory in the Age of AI Agents formalizes the underlying dynamics through three operators: *formation* (transforming artifacts into memory candidates), *evolution* (integrating and consolidating candidates), and *retrieval* (reconstructing relevant context). This taxonomy maps cleanly onto what distinguishes agentic RAG from its predecessors — passive RAG implements retrieval only; agentic RAG implements all three.

## Limitations and Open Questions

Several tensions remain unresolved. The reliance on LLM-generated keywords, tags, and contextual descriptions during memory formation means that errors or hallucinations in those fields propagate into the retrieval index — a failure mode distinct from embedding drift and harder to detect. The evaluation settings also warrant scrutiny: A-MEM uses all-minilm-l6-v2 with k=10 as defaults, and performance sensitivity to these hyperparameters across different memory sizes and domain types is not fully characterized.

More fundamentally, the benchmark conversations used for evaluation (LoCoMo at ~9K tokens, up to 35 sessions) are substantially longer than prior datasets but remain far shorter than the conversational histories that would accumulate in long-running agent deployments. Whether the scalability results hold and whether the Link Generation and Memory Evolution modules remain coherent as memory size grows into the tens of thousands of notes is an open empirical question.

The Mind-Map approach in Agentic Reasoning raises a related question: constructing a knowledge graph from reasoning traces requires the model to produce well-structured outputs amenable to graph transformation — a constraint that may not hold uniformly across task types or model families weaker than DeepSeek-R1.

## Relationships

Agentic RAG sits at the intersection of [[themes/retrieval_augmented_generation|retrieval_augmented_generation]] and [[themes/agent_memory_systems|agent_memory_systems]], and its practical realization depends heavily on [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]] — retrieval must be a callable tool the agent can invoke conditionally. Its connection to [[themes/reasoning_and_planning|reasoning_and_planning]] is direct: multi-step retrieval planning *is* reasoning, and systems like Agentic Reasoning make this explicit by unifying the two into a single loop. The memory evolution component intersects with [[themes/agent_self_evolution|agent_self_evolution]], since a memory system that consolidates and rewrites its own notes over time is a form of self-modification. The token efficiency findings are relevant to [[themes/context_engineering|context_engineering]], where the question is not just what to put in context but how to construct it cheaply.

## Sources
