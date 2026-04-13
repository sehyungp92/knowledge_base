---
type: entity
title: Parametric Memory
entity_type: theory
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- multi_agent_coordination
- pretraining_and_scaling
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0034926120623387904
staleness: 0.0
status: active
tags: []
---
# Parametric Memory

**Type:** theory
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]]

## Overview

Memory stored directly in model parameters (weights, biases, adapters, LoRA modules). Two types: internal (embedded in original weights) and external (stored in auxiliary parameter sets). Implicit, abstract, generalizable but harder to update.

## Key Findings

1. HippoRAG uses the Personalized PageRank algorithm seeded on query concept nodes to perform multi-hop reasoning across a knowledge graph in a single retrieval step. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
2. HippoRAG performs online retrieval by extracting named entities from a query, linking them to KG nodes via embedding similarity, then running Personalized PageRank seeded at those query nodes to propa (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
3. HippoRAG achieves 11% R@2 and 20% R@5 improvement over the best single-step baseline (ColBERTv2) on 2WikiMultiHopQA. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
4. HippoRAG models the neocortex by using an LLM to transform a corpus into a schemaless knowledge graph that serves as the artificial hippocampal index. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
5. Single-step retrieval with HippoRAG achieves comparable or better performance than iterative retrieval methods like IRCoT while being 10–20 times cheaper and 6–13 times faster. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
6. HippoRAG outperforms state-of-the-art RAG methods on multi-hop QA by up to 20% on 2WikiMultiHopQA. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
7. HippoRAG uses an LLM as an artificial neocortex to extract open knowledge graph triples via OpenIE, forming a schemaless hippocampal index from the retrieval corpus. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
8. HippoRAG achieves R@2 improvements of 11% on MuSiQue and 20% on 2WikiMultiHopQA over the ColBERTv2 single-step retrieval baseline. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
9. HippoRAG uses dense retrieval encoders as synthetic parahippocampal regions, adding synonymy edges between similar but non-identical noun phrases in the KG to aid pattern completion. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
10. Pretraining (imitation learning) initializes a model from random weights and adapts them to imitate large amounts of human-generated data. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
11. Single-step retrieval with HippoRAG achieves comparable or better performance than iterative retrieval with IRCoT while being 10–20x cheaper and 6–13x faster. (from "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models")
12. Memory dynamics are formalized through three conceptual operators: formation (transforming artifacts into memory candidates), evolution (integrating and consolidating candidates), and retrieval (const (from "Memory in the Age of AI Agents")
13. Model weights are frozen after training; all users receive the same fixed checkpoint and no further training occurs during inference. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
14. Three dominant forms of agent memory exist: token-level, parametric, and latent memory. (from "Memory in the Age of AI Agents")
15. Agent memory can be classified by function into factual memory (recording knowledge from interactions), experiential memory (enhancing problem-solving via task execution), and working memory (managing (from "Memory in the Age of AI Agents")

## Relationships

## Limitations and Open Questions

## Sources
