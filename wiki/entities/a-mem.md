---
type: entity
title: A-MEM
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- multi_agent_coordination
- policy_optimization
- pretraining_and_scaling
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.0037478321628064484
staleness: 0.0
status: active
tags: []
---
# A-MEM

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Atomic structured note system (Zettelkasten-style) that converts interactions into notes with LLM-generated contextual descriptions, keywords, and tags, using generative memory evolution via link creation and note rewriting.

## Key Findings

1. Mem0's extraction phase uses both a conversation summary and a window of recent messages as complementary contextual sources for memory extraction. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
2. Mem0g marks conflicting relationships as invalid rather than physically removing them to enable temporal reasoning. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
3. Mem0 achieves 26% relative improvement in the LLM-as-a-Judge metric over OpenAI's memory system. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
4. Mem0 achieves 91% lower p95 latency compared to the full-context approach. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
5. AgeMem achieves the highest Memory Quality scores of 0.533 (Qwen2.5-7B) and 0.605 (Qwen3-4B) on HotpotQA, outperforming all LTM baselines. (from "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents")
6. In Mem0's experimental configuration, the system uses 10 previous messages for contextual reference and retrieves the top 10 similar memories for comparative analysis during updates. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
7. The multi-component All-Returns reward strategy achieves higher task performance (J=0.544) and memory quality (MQ=0.533) than the task-only Answer-Only strategy (J=0.509, MQ=0.479) on HotpotQA. (from "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents")
8. Mem0 uses an incremental processing paradigm consisting of an extraction phase and an update phase. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
9. Mem0 saves more than 90% token cost compared to the full-context approach. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
10. Mem0 with graph memory (Mem0g) achieves approximately 2% higher overall score than the base Mem0 configuration. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
11. The full AgeMem system achieves overall improvements of +13.9%, +21.7%, and +16.1% on ALFWorld, SciWorld, and HotpotQA over the no-memory baseline. (from "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents")
12. Adding LTM alone yields performance gains of +10.6%, +14.2%, and +7.4% on ALFWorld, SciWorld, and HotpotQA respectively over the no-memory baseline. (from "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents")
13. Mem0 uses the LLM's own reasoning capabilities to select memory operations rather than a separate classifier. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
14. Mem0 uses an asynchronous summary generation module that periodically refreshes the conversation summary without introducing processing delays. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")
15. Mem0's update phase uses an LLM to select among four memory operations: ADD, UPDATE, DELETE, and NOOP. (from "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory")

## Relationships

## Limitations and Open Questions

## Sources
