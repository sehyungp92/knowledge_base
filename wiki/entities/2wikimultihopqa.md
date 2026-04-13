---
type: entity
title: 2WikiMultihopQA
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- chain_of_thought
- finetuning_and_distillation
- knowledge_and_memory
- long_context_and_attention
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
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.001517212968235532
staleness: 0.0
status: active
tags: []
---
# 2WikiMultihopQA

> 2WikiMultihopQA is a multi-hop question answering benchmark that requires reasoning across multiple Wikipedia articles to answer questions. Its structure — chaining evidence across documents — has made it a standard evaluation dataset for RL-trained reasoning agents, retrieval-augmented systems, and long-context models, serving as a proving ground for frameworks that must integrate search, planning, and multi-step inference.

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

2WikiMultihopQA requires models to retrieve and chain evidence across multiple Wikipedia documents to resolve questions — a task structure that demands genuine multi-step reasoning rather than surface-level pattern matching. This makes it a natural testbed for frameworks that integrate search with reasoning, and its in-domain status in Agent-R1 experiments has anchored its role as a benchmark for RL-trained agents.

The dataset sits at the intersection of retrieval, reasoning, and long-context processing. Its multi-hop structure exposes a clear failure mode in simpler systems: Naive RAG achieves only 0.1328 exact match in Agent-R1 evaluations, and the Base Tool Call baseline performs even worse (0.0847). All RL-trained agents substantially outperform both, with even the weakest RL agent surpassing Naive RAG by approximately 2.5x — a finding from Agent-R1 that underscores how significantly end-to-end RL changes the capability profile for multi-hop tasks.

## RL Methods and Performance

Among RL training algorithms, GRPO achieves the best overall performance on multi-hop QA (average EM 0.3877), closely followed by PPO (0.3719) and RLOO (0.3716). This rough parity between methods suggests that the architecture and reward signal matter more than the specific policy optimization algorithm — a useful calibration for practitioners choosing between them.

ReSearch uses 2WikiMultihopQA as a key evaluation benchmark for its approach of training LLMs to reason with search via RL (specifically GRPO), without any supervised reasoning-step data. The framework interleaves text-based thinking with search queries and retrieval results, treating search as part of the reasoning chain rather than a preprocessing step. It trains on Qwen2.5-7B(-Instruct) and Qwen2.5-32B(-Instruct) models.

AGENTFLOW reports broader gains across search-intensive tasks — average accuracy improvements of 14.9% on knowledge-intensive search and 14.0% on broader agentic tasks over top-performing baselines — positioning multi-hop retrieval as the domain where agentic system optimization yields the largest returns.

## As a Source for Long-Context Synthesis

LoongRL takes a different angle: rather than evaluating on 2WikiMultihopQA in its standard form, it uses the dataset as raw material for **KeyChain**, a synthetic data generation method that transforms short multi-hop QA problems into high-difficulty long-context challenges. KeyChain inserts 32-character UUID chains (characters from 0-9 and A-F) into extended documents, where one chain resolves to the true question and multiple others resolve to distractors — forcing models to both navigate extended context and maintain coherent multi-hop chains simultaneously.

The payoff is substantial: RL training with KeyChain data drives LoongRL-14B to a LongBench v1 average of 74.2, rivaling o3-mini (74.5) and DeepSeek-R1 (74.9). Ablation confirms KeyChain's unique contribution — replacing it with equal amounts of regular long-context multi-hop QA data yields only 66.2 average versus 72.4 with KeyChain data. Absolute gains on long-context multi-hop QA reach +23.5% for Qwen2.5-7B-Instruct and +21.1% for Qwen2.5-14B-Instruct. The reward function is a two-way substring exact match: a trajectory receives reward 1 if the ground truth is a substring of the model's boxed answer or vice versa.

## Open Questions and Limitations

The strong RL results across all methods raise a question of ceiling and generalization: performance gains on 2WikiMultihopQA may reflect optimization toward its specific hop-and-retrieve structure rather than general multi-step reasoning. The fact that GRPO, PPO, and RLOO converge to similar performance levels suggests the benchmark may be approaching saturation for RL-trained agents, which would reduce its discriminative power as a frontier evaluation.

The KeyChain transformation — while demonstrating impressive improvements — also introduces synthetic artifacts (UUID chains, inserted distractors) that don't appear in natural documents. Whether models trained on KeyChain-augmented data generalize to naturally long multi-hop problems or primarily learn to handle its specific distributional quirks remains an open question.

The dataset's Wikipedia grounding also creates a temporal limitation: as Wikipedia articles are updated, the multi-hop chains that were valid at dataset construction time may become inconsistent, quietly degrading benchmark reliability over time.

## Relationships

- Agent-R1 uses 2WikiMultihopQA as its primary in-domain evaluation for comparing RL algorithms and agent architectures.
- LoongRL extends it via KeyChain to create long-context training data, achieving near-frontier performance on LongBench.
- ReSearch evaluates search-integrated RL reasoning against it.
- AGENTFLOW demonstrates large gains on knowledge-intensive search tasks that include this dataset.
- Related benchmarks in the multi-hop QA space include HotpotQA and MuSiQue; 2WikiMultihopQA is distinguished by its explicit cross-Wikipedia article structure and controlled hop count.

## Key Findings

## Limitations and Open Questions

## Sources
