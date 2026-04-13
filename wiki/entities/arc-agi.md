---
type: entity
title: ARC-AGI
entity_type: dataset
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- frontier_lab_competition
- interpretability
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- model_behavior_analysis
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 16
sources_since_update: 0
update_count: 1
influence_score: 0.01501744679712881
staleness: 0.0
status: active
tags: []
---
# ARC-AGI

**Type:** dataset
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Abstraction and Reasoning Corpus for Artificial General Intelligence — a benchmark designed to measure fluid intelligence in AI systems through novel visual reasoning puzzles that require on-the-fly adaptation rather than pattern retrieval from training data.

## Key Findings

1. Fitness evaluation for ARC transform functions uses a two-tier scoring: primary score is the number of fully correct example grids, secondary score is the number of correct individual cells for non-pe (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
2. The ARC-AGI benchmark remains unbeaten as of December 5, 2024, five years after its creation. (from "ARC Prize 2024: Technical Report")
3. The method generates Python functions rather than output grids directly because functions can be executed and verified for correctness whereas grids cannot. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
4. The Evolutionary Test-time Compute method generates up to 500 Python transform functions using 31 dynamic prompts per ARC challenge. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
5. ARC is a more tractable target for test-time compute approaches than general AGI tasks because ARC solutions are easy to verify by running candidate functions against provided examples. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
6. ARC-AGI-Pub restricts internet-connected programs to the public leaderboard, making them ineligible for prize money. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
7. The author achieved 53.6% accuracy on ARC-AGI-Pub using Claude Sonnet 3.5, setting a new public record. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
8. Humans achieve approximately 85% accuracy on ARC challenges, while the best LLMs achieve only 18%. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
9. 42% of the Deep architecture's solutions came from generations 2–4, demonstrating the value of iterative refinement over single-generation generation. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
10. The previous state-of-the-art on ARC-AGI-Pub was 43%, achieved by Ryan Greenblatt. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
11. Pooling multiple parent functions into a single revision prompt helps address the local maxima problem by ensuring at least one solution for each example case is represented. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
12. Chain-of-Thought prompting is effective for ARC reasoning tasks because it guides LLMs to produce step-by-step reasoning before outputting a solution. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
13. The evolutionary approach can get stuck at local maxima when top-performing parents all share the same partial solution pattern, missing diverse solutions from other lineages. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
14. Pooling prompts are not always superior to single-parent prompts because LLMs pay less attention to longer contexts and higher token counts increase computational cost. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
15. ARC-AGI measures generalization on novel tasks rather than skill at tasks that can be prepared for in advance. (from "ARC Prize 2024: Technical Report")

## Capabilities

- Test-Time Fine-Tuning (TTFT) combined with AIRV achieves 58% accuracy on the ARC-AGI private test set — the highest score recorded during the 2024 ARC Kaggle competition — using only a single P100 GPU (maturity: research_only)

## Relationships

## Limitations and Open Questions

## Sources
