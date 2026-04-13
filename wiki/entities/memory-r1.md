---
type: entity
title: Memory-R1
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- evaluation_and_benchmarks
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00031816189049932973
staleness: 0.0
status: active
tags: []
---
# Memory-R1

> Memory-R1 is a reinforcement learning framework that trains two specialized agents — a Memory Manager and an Answer Agent — to perform adaptive memory operations (ADD, UPDATE, DELETE, NOOP) and reason over curated memory stores. It addresses the fundamental statelesness of LLMs by learning when and how to modify memory through outcome-driven rewards rather than imitation, achieving strong cross-task generalization from minimal training data.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/context_engineering|Context Engineering]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/policy_optimization|Policy Optimization]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

Memory-R1 is motivated by a structural limitation in current LLMs: they are fundamentally stateless, and their context windows — while growing — remain finite against an effectively unbounded space of potentially relevant information. Rather than treating memory as a retrieval problem alone, Memory-R1 frames memory management as a learned policy problem. Two RL-trained agents divide the work: the **Memory Manager** decides which CRUD operation to apply to the memory store given new conversational input, and the **Answer Agent** pre-selects relevant memory entries before reasoning toward a final answer.

The key architectural insight is that memory management need not be supervised by labeled operation trajectories. Instead, the Memory Manager is trained with an **outcome-driven reward**: its operations are evaluated solely by their downstream effect on QA quality (via exact-match), requiring no human annotation of what the "correct" memory operation was. This places Memory-R1 within the broader trend of reward-shaping from task outcomes rather than behavior cloning — a design validated by its outperformance of Memory-SFT, which uses GPT-5-generated trajectories for supervised fine-tuning. The RL approach wins despite the SFT baseline having access to a far more powerful teacher model, underscoring that imitation of even near-optimal behavior is a weaker signal than direct outcome optimization.

## Performance and Generalization

Memory-R1 achieves its results with a notably small training footprint: only 152 QA pairs from the LoCoMo benchmark. Despite this, models trained exclusively on LoCoMo generalize zero-shot to MSC and LongMemEval, two structurally distinct benchmarks. On LoCoMo itself, Memory-R1-GRPO on LLaMA-3.1-8B outperforms MemoryOS by 28.5% F1, 34.0% BLEU-1, and 30.2% LLM-as-a-Judge, representing a substantial margin over what was previously the strongest baseline.

A compound effect is observable across agent configurations: the Answer Agent's gains are significantly larger when paired with a stronger Memory Manager. With GPT-4o-mini managing memory, the Answer Agent improvement reaches F1 +19.72 and BLEU-1 +18.19, compared to F1 +10.10 and BLEU-1 +10.81 with a LLaMA-3.1-8B manager. This suggests the two components are not independent modules — memory quality propagates directly into answer quality, and both need to be strong for the system to reach its ceiling.

Ablation results reinforce this dependency: removing the RL-fine-tuned Memory Manager under PPO drops F1 from 41.0 to 34.5, BLEU-1 from 32.9 to 28.1, and LLM-as-a-Judge from 57.5 to 49.0. The learned memory policy is not incidental — it is load-bearing.

## Positioning Within the Memory Landscape

Memory-R1 operates at the **token-level memory** layer, as described in Memory in the Age of AI Agents, where information is stored as persistent, discrete, externally accessible units. Its CRUD operations correspond to the formation and evolution operators in that work's formalism — the Memory Manager effectively implements a learned policy over memory formation and consolidation, while the Answer Agent handles structured retrieval.

From the efficiency framing in Toward Efficient Agents, Memory-R1 contributes to the `Imem · Costmem` term in agent cost: by learning to issue targeted, high-quality operations rather than indiscriminate memory writes, it reduces unnecessary memory overhead while improving downstream utility. The framework is closer to **experiential memory** than simple factual storage — it learns operational behavior from task execution rather than passively recording interaction history.

## Limitations and Open Questions

Several limitations and open questions remain. First, the training regime relies entirely on LoCoMo, a single conversational QA dataset; zero-shot generalization to MSC and LongMemEval is promising but does not cover domains requiring structured knowledge, procedural memory, or multi-hop reasoning over large fact stores. Whether the learned CRUD policy transfers to non-conversational settings is unestablished.

Second, the outcome-driven reward is a noisy signal: exact-match QA scores are brittle proxies for memory quality, especially for open-ended or multi-sentence answers. The BLEU-1 and LLM-as-a-Judge metrics partially compensate, but the reward shaping problem is not fully solved — it's possible the Memory Manager learns to optimize for metric artifacts rather than genuinely useful memory states.

Third, the compound dependency between the two agents introduces a training stability concern. If the Memory Manager's policy shifts during RL training, the Answer Agent's learned pre-selection behavior may become misaligned, and vice versa. Whether the two agents are trained jointly or sequentially, and how sensitive the system is to that choice, is not fully addressed.

Finally, the 152-example training efficiency result is striking but the mechanism is unclear. It is not obvious whether this reflects genuine data efficiency from RL's outcome signal, the representativeness of LoCoMo's distribution, or both — and whether this efficiency would hold in lower-resource or more domain-specific settings.

## Relationships

Memory-R1 is directly connected to the challenge of LLM statelesness and finite context, framed in both Toward Efficient Agents and Memory in the Age of AI Agents. It extends the RL-for-reasoning lineage (e.g., DeepSeek-R1, GRPO-based methods) into the memory management domain, making it adjacent to work on [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] that uses outcome rewards to shape structured behavior. Its two-agent decomposition relates to broader [[themes/agent_systems|multi-agent systems]] design, and its emphasis on cross-task generalization with minimal data connects to [[themes/evaluation_and_benchmarks|benchmark generalization]] questions that remain open across agent memory research.

## Key Findings

## Sources
