---
type: entity
title: MuSiQue
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.00358811997775977
staleness: 0.0
status: active
tags: []
---
# MuSiQue

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A multi-hop question answering dataset used for out-of-domain evaluation in SKILLRL's search-augmented QA experiments.

## Key Findings

1. AGENTFLOW with a 7B-scale backbone outperforms top-performing baselines with average accuracy gains of 14.9% on search tasks. (from "In-the-Flow Agentic System Optimization for Effective Planning and Tool Use")
2. MATPO outperforms single-agent baselines by an average of 18.38% relative improvement across three benchmarks. (from "Multi-Agent Tool-Integrated Policy Optimization")
3. LoongRL substantially improves Qwen2.5-7B-Instruct long-context multi-hop QA accuracy by +23.5% absolute gain. (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
4. KeyChain uses 32-character UUID keys (characters sampled from 0-9 and A-F) to form linear key-value chains, where one chain resolves to the true question and multiple others resolve to distracting que (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
5. AGENTFLOW achieves average accuracy gains of 14.0% on broader agentic tasks, 14.5% on mathematical reasoning, and 4.1% on scientific reasoning over top-performing baselines. (from "In-the-Flow Agentic System Optimization for Effective Planning and Tool Use")
6. MATPO enables planner and worker agent roles to be trained within a single LLM instance using role-specific prompts via reinforcement learning. (from "Multi-Agent Tool-Integrated Policy Optimization")
7. GRPO achieved the best overall RL performance (average EM 0.3877) on multi-hop QA, closely followed by PPO (0.3719) and RLOO (0.3716). (from "Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning")
8. LoongRL substantially improves Qwen2.5-14B-Instruct long-context multi-hop QA accuracy by +21.1% absolute gain. (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
9. LoongRL-14B achieves a LongBench v1 average score of 74.2, rivaling o3-mini (74.5) and DeepSeek-R1 (74.9) despite being much smaller. (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
10. Ablation shows that replacing KeyChain data with equal amounts of regular long-context multi-hop QA data yields only 66.2 average vs 72.4 with KeyChain data, demonstrating KeyChain's unique contributi (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
11. All RL-trained agents substantially outperform both the Base Tool Call and Naive RAG baselines on multi-hop QA tasks, with even the weakest RL agent surpassing RAG by approximately 2.5x. (from "Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning")
12. KeyChain transforms short multi-hop QA datasets into high-difficulty long-context problems by extending inputs with distracting documents and inserting UUID chains that hide the true question across m (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
13. MATPO is derived from a principled credit assignment mechanism across planner and worker rollouts. (from "Multi-Agent Tool-Integrated Policy Optimization")
14. A two-way substring exact match reward verifier is used as a rule-based reward, where a trajectory receives reward 1 if the ground truth is a substring of the answer or vice versa. (from "LoongRL: Reinforcement Learning for Advanced Reasoning over Long Contexts")
15. MATPO achieves 42.60% on GAIA-text, 33.00% on WebWalkerQA, and 63.64% on FRAMES, compared to 32.16%, 30.14%, and 56.22% for single-agent GRPO. (from "Multi-Agent Tool-Integrated Policy Optimization")

## Relationships

## Limitations and Open Questions

## Sources
