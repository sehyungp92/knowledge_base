---
type: entity
title: PRIME
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.005370210824643842
staleness: 0.0
status: active
tags: []
---
# PRIME

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Retrieval system using fast-slow thinking for timing decisions and a Planner Agent for global retrieval planning before decomposition into sub-queries.

## Key Findings

1. AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world champions in Go, chess, shogi, and Stratego (from "A Survey of Reinforcement Learning for Large Reasoning Models")
2. SWiRL does not require golden labels or human annotations, relying entirely on model-based judgments for data generation, filtering, and RL optimization. (from "Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use")
3. TTRL on Qwen2.5-Math-7B achieves an average gain of 76% across AIME 2024, AMC, MATH-500, and GPQA (from "TTRL: Test-Time Reinforcement Learning")
4. TTRL boosts the pass@1 performance of Qwen-2.5-Math-7B by approximately 211% on AIME 2024 using only unlabeled test data (from "TTRL: Test-Time Reinforcement Learning")
5. OpenAI o3 achieves 75.7% success rate on ARC-AGI-1 but only 4% on the more recently released ARC-AGI-2 (from "TTRL: Test-Time Reinforcement Learning")
6. TTRL uses majority voting as a proxy label estimator: given N candidate outputs, the most frequent predicted answer becomes the estimated label, and each output matching that label receives a reward o (from "TTRL: Test-Time Reinforcement Learning")
7. TTRL surpasses the traditional self-training upper bound (initial model's majority voting accuracy), demonstrating it exceeds the anticipated performance ceiling (from "TTRL: Test-Time Reinforcement Learning")
8. TTRL consistently surpasses the upper limit of the initial model's maj@n, even though it is only supervised by maj@n during training (from "TTRL: Test-Time Reinforcement Learning")
9. TTRL on Qwen2.5-Math-7B avg@64 consistently outperforms the same model's maj@64 across all benchmarks after training (from "TTRL: Test-Time Reinforcement Learning")
10. Memory dynamics are formalized through three conceptual operators: formation (transforming artifacts into memory candidates), evolution (integrating and consolidating candidates), and retrieval (const (from "Memory in the Age of AI Agents")
11. Policy entropy collapses sharply at the early stage of RL training for LLMs, dropping to near zero monotonically without entropy intervention. (from "The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models")
12. Three dominant forms of agent memory exist: token-level, parametric, and latent memory. (from "Memory in the Age of AI Agents")
13. Agent memory can be classified by function into factual memory (recording knowledge from interactions), experiential memory (enhancing problem-solving via task execution), and working memory (managing (from "Memory in the Age of AI Agents")
14. Token-level memory stores information as persistent, discrete, externally accessible units including text tokens, visual tokens, and audio frames. (from "Memory in the Age of AI Agents")
15. Without entropy intervention, the relationship between policy entropy H and downstream validation performance R follows the exponential law R = -a·exp(H) + b, where a and b are fitting coefficients. (from "The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models")

## Relationships

## Limitations and Open Questions

## Sources
