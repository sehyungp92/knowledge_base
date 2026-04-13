---
type: entity
title: DeepScaleR Dataset
entity_type: dataset
theme_ids:
- agent_systems
- chain_of_thought
- multi_agent_coordination
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0001759507525325182
staleness: 0.0
status: active
tags: []
---
# DeepScaleR Dataset

> DeepScaleR is a mathematical reasoning dataset used as reinforcement learning training data for studying and improving LLM reasoning capabilities. It serves as a common benchmark substrate across multiple lines of research into RL-trained thinking paradigms — from multi-agent asynchronous organization to linear-scaling Markovian reasoning — enabling controlled comparisons of novel training environments against sequential and parallel thinking baselines.

**Type:** dataset
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

DeepScaleR is a curated collection of mathematical reasoning problems designed to serve as the RL training environment for language models learning to think. Its significance lies less in any single property of the dataset itself and more in its role as a shared training ground across research efforts that are independently rethinking the structure of the reasoning process — specifically, how to scale thinking length without incurring prohibitive compute costs.

Two distinct architectural proposals, AsyncThink and Delethink, both use DeepScaleR-style math data to train and evaluate their approaches, making it a de facto common currency for comparing reasoning paradigms. This shared substrate is what makes cross-paper comparisons meaningful: the dataset's properties (problem diversity, difficulty distribution, answer verifiability) are held constant while the training environment and inference-time architecture vary.

## Role in RL Reasoning Research

The core challenge that DeepScaleR training exposes is the compute-scaling problem of long chain-of-thought reasoning. In the standard RL reasoning environment, the state at step $t$ is the prompt concatenated with all prior reasoning tokens, making $|s_t| = O(t)$. For transformer-based policies, self-attention over this growing context means that scaling thinking from $n$ to $nS$ tokens costs $O(n^2 S^2)$ FLOPs — quadratic in both base length and scale factor. DeepScaleR's math problems, which benefit from extended reasoning, make this bottleneck directly observable and measurable.

**Delethink** addresses this by restructuring the RL environment rather than the model: reasoning is divided into fixed-size chunks of $C$ tokens (e.g., 8K), and at each chunk boundary the context is reset with a short carryover summary. This enforces $|s_t| = O(C)$ at every step, turning the quadratic cost in growing context into cost quadratic only in the constant $C$. Overall training cost then scales linearly in the number of thinking tokens. An R1-Distill 1.5B model trained this way on math data reasons in 8K-token chunks but can think up to 24K tokens, matching or surpassing a LongCoT-RL model trained with a full 24K budget — and crucially, Delethink continues to improve with test-time scaling where LongCoT plateaus.

**AsyncThink** uses math data (including countdown tasks from a related distribution) as its cold-start and RL training signal for a two-stage procedure: first, format fine-tuning on synthesized thinking-protocol data; then reinforcement learning. The organizer and worker roles share the same LLM backbone and differ only in their available action sets. Trained on countdown data, AsyncThink achieves 89.4% accuracy on out-of-domain 4×4 Sudoku — outperforming parallel thinking (84.2%) and sequential thinking (65.7%) — suggesting that math RL training generalizes to structural reasoning tasks beyond the training distribution. On the in-domain multi-solution countdown task, AsyncThink reaches 89.0% strict accuracy versus 68.6% for parallel and 70.5% for sequential baselines.

## Limitations and Open Questions

DeepScaleR's role as a training dataset raises several underexplored questions. The claims drawn from these papers focus on aggregate accuracy metrics, but say little about *which* problem types drive the gains — whether DeepScaleR's difficulty distribution is representative of the harder reasoning regimes where Delethink's linear scaling is most advantageous remains unclear.

There is also a transfer question: AsyncThink's strong Sudoku performance after countdown training is presented as evidence of generalization, but it is not established whether this is a property of the training paradigm, the dataset, or the model prior. The dataset itself is not analyzed as an independent variable.

Finally, the papers use DeepScaleR as a fixed backdrop without probing sensitivity: whether the relative rankings of sequential, parallel, AsyncThink, and Delethink approaches hold across datasets with different answer-verification structures (e.g., open-ended generation vs. numerical answers) is an open question.

## Relationships

DeepScaleR sits at the intersection of several converging research threads. It is directly used in "The Era of Agentic Organization" and "The Markovian Thinker", both of which treat it as a training and evaluation substrate for RL reasoning approaches. It also appears in the context of "e3: Learning to Explore Enables Extrapolation of Test-Time Compute", connecting it to the broader [[themes/test_time_compute_scaling|test-time compute scaling]] literature.

The dataset's mathematical structure aligns it with [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] and [[themes/policy_optimization|policy optimization]], while the multi-agent use in AsyncThink links it to [[themes/multi_agent_coordination|multi-agent coordination]] and [[themes/agent_systems|agent systems]] themes. The core tension it surfaces — long reasoning is valuable but expensive — is central to the [[themes/reasoning_and_planning|reasoning and planning]] and [[themes/chain_of_thought|chain of thought]] theme clusters.

## Key Findings

## Sources
