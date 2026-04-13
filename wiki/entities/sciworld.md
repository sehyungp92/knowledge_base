---
type: entity
title: SciWorld
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- knowledge_and_memory
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 8.779751156330615e-05
staleness: 0.0
status: active
tags: []
---
# SciWorld

> SciWorld is a benchmark dataset of science-based game reasoning tasks designed to evaluate the sequential decision-making and long-horizon planning capabilities of LLM agents, measured by a Success Rate (SR) metric. Its significance lies in its exceptional sequential complexity — it demands the longest average trajectory lengths among commonly paired benchmarks — making it a stringent testbed for evaluating memory, credit assignment, and stepwise search strategies in agentic systems.

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/policy_optimization|policy_optimization]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

SciWorld presents agents with science-grounded interactive game environments where success requires navigating long sequences of actions to reach task completion. The benchmark includes 1,483 training episodes and 194/241 seen/unseen test episodes, and is routinely paired with ALFWorld and WebShop to provide a comparative view across task types and difficulty levels. Its defining characteristic is trajectory length: at 14.4 average turns, SciWorld episodes are roughly 40% longer than ALFWorld (10.1 turns) and nearly three times longer than WebShop (4.9 turns). This length makes it particularly sensitive to failures in memory management, sparse reward propagation, and compounding reasoning errors — precisely the failure modes that recent agentic research targets.

Crucially, like ALFWorld and WebShop, SciWorld provides only a single binary outcome reward at the end of each trajectory, giving no intermediate signal. This sparse reward structure is what makes it a meaningful proving ground for methods that must infer dense process rewards from outcome data alone.

## Key Findings

### SciWorld as a stress test for memory architectures

The AgeMem system demonstrates the value of SciWorld's length as a diagnostic. Without any memory, agents plateau; adding long-term memory (LTM) alone yields +14.2% on SciWorld, the largest single-component gain across the three benchmarks. The full AgeMem system — combining LTM, short-term memory (STM) context management, and three-stage progressive RL — achieves +21.7% overall, also the highest relative improvement across ALFWorld, SciWorld, and HotpotQA. This pattern suggests SciWorld's long horizons amplify the value of memory precisely because compounding context loss is more costly in extended task sequences.

The three-stage RL training within AgeMem deserves particular attention: the model first acquires LTM storage capabilities, then learns STM context filtering (evidenced by FILTER tool usage jumping from 0.02 to 0.31 on Qwen2.5-7B), and finally coordinates both under full task reward. RL contributes approximately 8.5–8.7 percentage points above the no-RL AgeMem variant, validating that memory management itself is a learnable skill — not just an architectural choice. The design ensures LTM persists across all training stages while context is reset between Stages 1 and 2 to prevent information leakage, a subtle but important detail for clean credit assignment.

### SciWorld as a proving ground for dense process rewards

QLASS uses SciWorld to evaluate whether Q-value-guided stepwise search can compensate for the absence of intermediate rewards. By applying the Bellman equation recursively over trajectory trees — estimating Q-values at intermediate nodes from outcome rewards stored at leaf nodes — QLASS converts terminal signals into dense process rewards. At each decision step, agents sample candidate actions and execute the one with the highest predicted Q-value, a form of inference-time search that requires no additional environment interaction. SciWorld's longer trajectories provide a stronger test of whether this Q-guided selection actually captures meaningful long-range structure rather than myopic preferences.

### Relationship to reward shaping and RL for agents

A recurring theme across both AgeMem and QLASS is the inadequacy of outcome-only rewards for long-horizon tasks. SciWorld operationalizes this inadequacy in a concrete, reproducible way. AgeMem addresses it by broadcasting terminal reward advantage to all preceding steps (step-wise GRPO), enabling long-range credit assignment. QLASS addresses it by learning a Q-function over trajectory trees and using it at inference time rather than training time. These are meaningfully different interventions — one shapes the training signal, the other shapes the search policy — and SciWorld's length makes their comparative advantages legible.

## Limitations and Open Questions

SciWorld's seen/unseen split (194 vs 241 test episodes) raises the question of how well improvements on seen tasks generalize to unseen configurations — a distinction that is underreported in current results. The benchmark also conflates different types of sequential complexity (task length, branching factor, scientific domain knowledge) without decomposing which factor most drives agent failures. It remains unclear whether gains on SciWorld transfer to real scientific reasoning or are artifacts of game-specific affordances. Finally, as a text-based game environment, SciWorld abstracts away perception and physical grounding, potentially overstating the readiness of memory and search strategies for embodied or multimodal settings.

## Relationships

SciWorld is most commonly evaluated alongside **ALFWorld** (household task completion) and **WebShop** (web-based shopping), forming a standard trio for benchmarking LLM agents across different action space and horizon profiles. It appears centrally in Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents (AgeMem) and QLASS: Boosting Language Agent Inference via Q-Guided Stepwise Search, and is referenced in the AgentGym-RL line of work on multi-turn RL for decision-making agents. Thematically, it sits at the intersection of [[themes/agent_memory_systems|agent memory systems]], [[themes/rl_for_llm_reasoning|RL for LLM reasoning]], and [[themes/search_and_tree_reasoning|search and tree reasoning]], making it a useful triangulation point for work that spans all three.

## Sources
