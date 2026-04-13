---
type: entity
title: WebShop
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- chain_of_thought
- computer_use_and_gui_agents
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0027504224496840593
staleness: 0.0
status: active
tags: []
---
# WebShop

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]]

## Overview

A web shopping simulation benchmark where agents navigate a realistic web interface to find and purchase products matching user specifications. Performance is measured by average score and average success rate.

## Key Findings

1. LATS achieves 81.1% pass@1 on MBPP with GPT-3.5, outperforming all baselines including Reflexion (70.0%) and RAP (71.4%). (from "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models")
2. As the number of task objectives increases, peak token usage of all baseline methods scales nearly linearly, while MEM1 maintains an almost constant peak token count. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
3. LATS achieves state-of-the-art pass@1 accuracy of 92.7% on HumanEval with GPT-4. (from "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models")
4. LATS achieves 83.8% pass@1 on HumanEval with GPT-3.5, outperforming Reflexion (68.1%), ToT (54.4%), and RAP (63.1%). (from "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models")
5. MEM1-7B reduces memory usage by 3.7× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
6. MEM1 uses XML-style tags to structure agent context: <IS> for internal state, <query> for environment queries, <answer> for responses, and <info> for external observations. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
7. LAMER is evaluated using Qwen3-4B as the base model across all primary experiments. (from "Meta-RL Induces Exploration in Language Agents")
8. DreamGym uses an outcome-based reward scheme, assigning r=1 only at the final step when the task is successfully completed and r=0 otherwise. (from "Scaling Agent Learning via Experience Synthesis")
9. RL training for LLM agents is challenging due to costly rollouts, limited task diversity, unreliable reward signals, and infrastructure complexity. (from "Scaling Agent Learning via Experience Synthesis")
10. LATS uses a value function combining a self-generated LM score and a self-consistency score, weighted by a hyperparameter lambda. (from "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models")
11. LATS uses UCT (Upper Confidence bounds applied to Trees) for selection to balance exploration and exploitation during tree search. (from "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models")
12. MEM1-7B improves task performance by 3.5× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
13. Transformer-based LLMs incur O(N²) compute cost, or O(N) with Key-Value caching, and O(N) memory usage as context length N increases. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
14. At any given turn, the MEM1 agent retains at most two <IS> elements, two <query> elements, and one <info> element, ensuring bounded memory usage. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")
15. On the 16-objective task, MEM1 requires only 27.1% of the peak tokens and 29.3% of the total inference time compared to Qwen2.5-14B-Instruct. (from "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents")

## Relationships

## Limitations and Open Questions

## Sources
