---
type: entity
title: State Space Models
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- frontier_lab_competition
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- software_engineering_agents
- test_time_compute_scaling
- transformer_alternatives
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.00439600252135241
staleness: 0.0
status: active
tags: []
---
# State Space Models

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Neural architectures (e.g., Mamba, S4) that use recurrent state-based formulations to achieve O(N) sequence processing complexity, positioned as transformer alternatives for long-context tasks.

## Key Findings

1. DoRA-finetuned Hymba-1.5B achieves 40.0% / 37.9% on RoleBench instruction/role generalization, outperforming RoleLlama-7B by 4.5% and 4.4% respectively (from "Hymba: A Hybrid-head Architecture for Small Language Models")
2. Replacing global full attention with sliding window attention in all layers causes a recall accuracy drop of over 20% on recall-intensive tasks (from "Hymba: A Hybrid-head Architecture for Small Language Models")
3. The relative importance of attention versus SSM heads in the same layer is input-adaptive and varies across tasks (from "Hymba: A Hybrid-head Architecture for Small Language Models")
4. At 1B scale under identical training conditions, Hymba achieves 1.74% higher average score than the second-best architecture (from "Hymba: A Hybrid-head Architecture for Small Language Models")
5. Sequential hybrid models that stack attention and SSM layers can introduce bottlenecks when one layer type is not well-suited for specific tasks, requiring compensation from subsequent layers (from "Hymba: A Hybrid-head Architecture for Small Language Models")
6. Combining local and global attention with cross-layer KV sharing improves throughput by 3x and reduces cache by almost 4x compared to using only parallel attention+SSM heads (from "Hymba: A Hybrid-head Architecture for Small Language Models")
7. Meta tokens can be precomputed offline at inference time since they are fixed and appear at the beginning of every input sequence (from "Hymba: A Hybrid-head Architecture for Small Language Models")
8. The SSM head in the first layer is critical for language modeling; removing it causes accuracy to drop to random-guess levels (from "Hymba: A Hybrid-head Architecture for Small Language Models")
9. Using global attention in only three layers (first, middle, and last) is sufficient to recover recall-intensive accuracy while maintaining commonsense reasoning accuracy, achieving 2.7x throughput and (from "Hymba: A Hybrid-head Architecture for Small Language Models")
10. In Llama-3.2-3B, more than 50% of attention is focused on the BOS token (from "Hymba: A Hybrid-head Architecture for Small Language Models")
11. Attention heads provide high-resolution recall while SSM heads enable efficient context summarization (from "Hymba: A Hybrid-head Architecture for Small Language Models")
12. Transformers have quadratic computational cost and high memory demands that pose efficiency challenges (from "Hymba: A Hybrid-head Architecture for Small Language Models")
13. Hymba integrates transformer attention mechanisms with state space models in parallel within the same layer, allowing each layer to simultaneously process inputs through both attention heads and SSM h (from "Hymba: A Hybrid-head Architecture for Small Language Models")
14. Hymba-1.5B-Base outperforms all sub-2B public models and surpasses Llama-3.2-3B with 1.32% higher average accuracy, 11.67x cache size reduction, and 3.49x throughput (from "Hymba: A Hybrid-head Architecture for Small Language Models")
15. Cross-layer KV sharing improves throughput by 1.15x while maintaining comparable recall accuracy and boosting commonsense accuracy by +0.60% (from "Hymba: A Hybrid-head Architecture for Small Language Models")

## Relationships

## Limitations and Open Questions

## Sources
