---
type: entity
title: LLM-as-a-Judge
entity_type: method
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.004186258141346834
staleness: 0.0
status: active
tags: []
---
# LLM-as-a-Judge

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

Post-training technique where a language model acts as a reward signal to evaluate and score its own outputs, scaled in Kimi K2's self-rewarding pipeline.

## Key Findings

1. TrustJudge achieves these improvements without requiring additional model training or human annotations. (from "TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them")
2. Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Pairwise Transitivity Inconsistency by 10.82% (from 15.22% to 4.40%). (from "TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them")
3. ReasoningBank on SWE-Bench-Verified improves resolve rate from 34.2% to 38.8% (Gemini-2.5-flash) and from 54.0% to 57.4% (Gemini-2.5-pro) over no-memory baselines while reducing interaction steps. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
4. Higher-quality memory directly amplifies the Best-of-N benefit from test-time scaling: without memory BoN improves from 39.0 to 40.6, while with ReasoningBank BoN improves from 49.7 to 52.4 at k=3. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
5. ReasoningBank improves overall success rate on WebArena by +8.3, +7.2, and +4.6 over memory-free agents using Gemini-2.5-flash, Gemini-2.5-pro, and Claude-3.7-sonnet respectively. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
6. Memory items in ReasoningBank are structured as three components: a title (concise identifier), a description (one-sentence summary), and content (distilled reasoning steps and insights). (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
7. Kimi K2 is a sparse mixture of experts (MoE) model with 1 trillion total parameters and 32 billion active parameters. (from "Kimi K2 and when "DeepSeek Moments" become normal")
8. MaTTS parallel scaling with ReasoningBank grows success rate from 49.7% at k=1 to 55.1% at k=5 on WebArena-Shopping. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
9. OpenAI delayed its forthcoming open-weight model to run additional safety tests and review high-risk areas. (from "Kimi K2 and when "DeepSeek Moments" become normal")
10. ReasoningBank distills generalizable reasoning strategies from both successful and failed agent experiences without requiring ground-truth labels. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
11. Kimi K2 is a non-thinking model that does not generate a long reasoning chain before answering, but was still trained extensively with reinforcement learning. (from "Kimi K2 and when "DeepSeek Moments" become normal")
12. Kimi K2 was trained on 15.5 trillion tokens. (from "Kimi K2 and when "DeepSeek Moments" become normal")
13. DeepSeek V3/R1 was trained on 14.8 trillion tokens with 671 billion total parameters and 37 billion active parameters. (from "Kimi K2 and when "DeepSeek Moments" become normal")
14. ReasoningBank uses a three-step closed-loop process: memory retrieval, memory construction, and memory consolidation. (from "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory")
15. Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Score-Comparison Inconsistency by 8.43% (from 23.32% to 14.89%). (from "TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them")

## Relationships

## Limitations and Open Questions

## Sources
