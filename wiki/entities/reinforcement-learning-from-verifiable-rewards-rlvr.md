---
type: entity
title: Reinforcement Learning from Verifiable Rewards (RLVR)
entity_type: method
theme_ids:
- agent_evaluation
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- mathematical_and_formal_reasoning
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.006857760203404063
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning from Verifiable Rewards (RLVR)

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A training technique where LLMs are trained against automatically verifiable rewards (e.g., math/code puzzles), causing them to spontaneously develop reasoning-like strategies including problem decomposition and backtracking. Became the dominant capability-scaling paradigm in 2025.

## Key Findings

1. On hard-to-verify tasks with Qwen-4B-Base, HERO achieves 66.3, surpassing RM-only training (54.6) by +11.7 points and verifier-only training (57.1) by +9.2 points. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
2. HERO (Hybrid Ensemble Reward Optimization) integrates sparse verifier signals with dense reward model scores via stratified normalization and variance-aware weighting. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
3. The HardVerify_Math benchmark consists of 250 hard-to-verify math problems including Olympiad questions, MATH test set questions prone to false negatives due to complex answer formats, and Big-Math qu (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
4. The math_reward.py verifier (verl) has near-zero false positive rate (0.3%) but extremely low recall (10.1%) on hard-to-verify math problems, failing to recognize most correct answers. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
5. AceMath-7B-RM (a math-focused reward model) achieves 91.7% recall on hard-to-verify math problems at threshold 1, substantially surpassing rule-based verifiers, but with lower precision (67.7%). (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
6. In Gaia2, environment time passes independent of whether the agent acts or not, and the environment state is continuously updated with random or scheduled events. (from "ARE: Scaling Up Agent Environments and Evaluations")
7. The TIGER-Lab/general-verifier (a generative model-based verifier) achieves 49.5% recall and 89.3% precision on hard-to-verify math problems, with a false positive rate of 6.3%. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
8. ARE environments are event-based, time-driven simulations that run asynchronously from the agent and the user. (from "ARE: Scaling Up Agent Environments and Evaluations")
9. Gaia2 is composed of 1,120 verifiable, annotated scenarios taking place in a Mobile environment that mimics a smartphone with apps such as email, messaging, and calendar. (from "ARE: Scaling Up Agent Environments and Evaluations")
10. ARE environments run deterministically given a fixed starting state and seed, ensuring reproducible evaluations. (from "ARE: Scaling Up Agent Environments and Evaluations")
11. The math_verify library extends rule-based coverage with normalization heuristics but remains brittle for mismatched orderings such as lists vs. sets, yielding only 38.6% recall. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
12. Binary verifiable rewards are brittle because many tasks admit partially correct or alternative answers that verifiers under-credit, and all-or-nothing supervision limits learning. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
13. HERO's stratified normalization bounds reward-model scores within verifier-defined correctness groups, ensuring dense feedback refines learning only within responses deemed correct by the verifier. (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")
14. OpenAI initiated the reasoning/inference-scaling/RLVR revolution in September 2024 with o1 and o1-mini (from "2025: The year in LLMs")
15. HERO's variance-aware weighting down-weights easy prompts where most responses are uniformly correct or incorrect, and up-weights harder prompts where reward-model scores provide valuable discriminati (from "Hybrid Reinforcement: When Reward Is Sparse, It's Better to Be Dense")

## Relationships

## Limitations and Open Questions

## Sources
