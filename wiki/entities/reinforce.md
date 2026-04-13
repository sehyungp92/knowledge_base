---
type: entity
title: REINFORCE++
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 9
sources_since_update: 0
update_count: 1
influence_score: 0.0039224414892669686
staleness: 0.0
status: active
tags: []
---
# REINFORCE++

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

An enhanced REINFORCE RL algorithm variant. Showed weakest RL performance in Agent-R1 experiments (average EM 0.3300); adding a baseline (REINFORCE++Baseline) improved it to 0.3619.

## Key Findings

1. MEM1-7B improves task performance by 3.5× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
2. As the number of task objectives increases, peak token usage of all baseline methods scales nearly linearly, while MEM1 maintains an almost constant peak token count. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
3. FlowRL achieves a 10.0% average improvement over GRPO and 5.1% over PPO on math benchmarks. (from "FlowRL: Matching Reward Distributions for LLM Reasoning")
4. Strong open-source models including Qwen2.5-72B-Instruct and DeepSeek-R1-Distill-Qwen-32B perform poorly on multi-subject tasks, achieving only 22.6% and 21.7% respectively. (from "Crossing the Reward Bridge: Expanding RL with Verifiable Rewards Across Diverse Domains")
5. Transformer-based LLMs incur O(N²) compute cost, or O(N) with Key-Value caching, and O(N) memory usage as context length N increases. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
6. MEM1 uses XML-style tags to structure agent context: <IS> for internal state, <query> for environment queries, <answer> for responses, and <info> for external observations. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
7. GRPO achieved the best overall RL performance (average EM 0.3877) on multi-hop QA, closely followed by PPO (0.3719) and RLOO (0.3716). (from "Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning")
8. RLVR update sparsity (fraction of unchanged parameters) ranges from 36% to 92% across models, while SFT sparsity is consistently low at 0.6%–18.8%. (from "The Path Not Taken: RLVR Provably Learns Off the Principals")
9. FlowRL transforms scalar rewards into a normalized target distribution using a learnable partition function and minimizes the reverse KL divergence between the policy and the target distribution. (from "FlowRL: Matching Reward Distributions for LLM Reasoning")
10. Removing importance sampling causes a large performance drop in FlowRL, from 35.63% to 26.71% average accuracy on math benchmarks. (from "FlowRL: Matching Reward Distributions for LLM Reasoning")
11. All RL-trained agents substantially outperform both the Base Tool Call and Naive RAG baselines on multi-hop QA tasks, with even the weakest RL agent surpassing RAG by approximately 2.5x. (from "Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning")
12. MEM1-7B reduces memory usage by 3.7× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
13. FlowRL achieves an average math accuracy of 48.39% with the 32B model, surpassing PPO (43.25%) and GRPO (38.34%). (from "FlowRL: Matching Reward Distributions for LLM Reasoning")
14. At any given turn, the MEM1 agent retains at most two <IS> elements, two <query> elements, and one <info> element, ensuring bounded memory usage. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
15. On the 16-objective task, MEM1 requires only 27.1% of the peak tokens and 29.3% of the total inference time compared to Qwen2.5-14B-Instruct. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")

## Relationships

## Limitations and Open Questions

## Sources
