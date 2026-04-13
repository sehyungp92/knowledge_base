---
type: entity
title: GPQA
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- hallucination_and_reliability
- interpretability
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- mechanistic_interpretability
- model_architecture
- multi_agent_coordination
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.006268620340276801
staleness: 0.0
status: active
tags: []
---
# GPQA

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

A challenging evaluation benchmark consisting of graduate-level questions in biology, chemistry, and physics used to measure frontier model reasoning capabilities.

## Key Findings

1. Claude 3.7 Sonnet's 'action scaling' allows it to iteratively call functions, respond to environmental changes, and continue until an open-ended task is complete. (from "Claude's extended thinking")
2. Prompt injection defenses for computer use improved from preventing 74% to 88% of attacks, with a 0.5% false-positive rate. (from "Claude's extended thinking")
3. Using 256 independent samples, a learned scoring model, and a maximum 64k-token thinking budget, Claude 3.7 Sonnet achieved 84.8% on GPQA. (from "Claude's extended thinking")
4. Developers can set a 'thinking budget' to control precisely how long Claude spends on a problem. (from "Claude's extended thinking")
5. Parallel test-time compute works by sampling multiple independent thought processes and selecting the best one without knowing the true answer ahead of time. (from "Claude's extended thinking")
6. In CBRN-related controlled studies, model-assisted participants showed uplift over non-assisted ones, but all attempts contained critical failures preventing end-to-end success. (from "Claude's extended thinking")
7. Claude 3.7 Sonnet can allocate more turns, time, and computational power to computer use tasks than its predecessor. (from "Claude's extended thinking")
8. The visible thought process was not subjected to Claude's standard character training, resulting in thinking that is more detached and less personal than default outputs. (from "Claude's extended thinking")
9. Claude was given basic memory, screen pixel input, and function calls to sustain Pokémon gameplay through tens of thousands of interactions beyond its usual context limits. (from "Claude's extended thinking")
10. The visible thought process in Claude 3.7 Sonnet is intended as a research preview only. (from "Claude's extended thinking")
11. Claude 3.7 Sonnet successfully defeated three Pokémon Gym Leaders and won their Badges in Pokémon Red. (from "Claude's extended thinking")
12. Prompt injection defenses combine new training, a system prompt instructing the model to ignore such attacks, and a classifier that triggers on potential injections. (from "Claude's extended thinking")
13. Parallel test-time compute scaling is not available in the deployed Claude 3.7 Sonnet model and remains a research direction. (from "Claude's extended thinking")
14. Expert red-teamers found that the frequency of critical failures in CBRN task attempts was too high for successful end-to-end task completion. (from "Claude's extended thinking")
15. Extended thinking mode does not switch to a different model; it allows the same model to spend more time and effort on a problem. (from "Claude's extended thinking")

## Capabilities

- State-of-the-art math reasoning among non-thinking models: AIME 2024 69.6 Avg@64, AIME 2025 49.5 Avg@64, MATH-500 97.4%, HMMT 2025 38.8 Avg@32, GPQA-Diamond 75.1 Avg@8 — surpassing GPT-4.1, Claude Son (maturity: narrow_production)

## Known Limitations

- AIME24 and GPQA results reported as Avg@32 and Avg@8 respectively — single-sample pass@1 performance is substantially lower, requiring 8-32x inference compute overhead to achieve reported frontier num (severity: minor, trajectory: stable)
- GPQA graduate-level science QA at 79.1% — 5-9 point gap behind Grok4 (87.7%) and Gemini 2.5 Pro (84.4%), indicating persistent weakness in expert scientific reasoning not addressed by current RL curri (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
