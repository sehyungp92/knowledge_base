---
type: entity
title: Outcome-Based Reward
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- computer_use_and_gui_agents
- frontier_lab_competition
- hallucination_and_reliability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0032533135862036454
staleness: 0.0
status: active
tags: []
---
# Outcome-Based Reward

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

A reward signal derived only from whether the final answer is correct, as opposed to per-step process rewards. o1 and RLVR both rely primarily on this signal.

## Key Findings

1. ReTool (Qwen2.5-32B-Instruct backbone) achieves 67.0% accuracy on AIME 2024 with only 400 training steps, outperforming the text-based RL baseline which achieves 40.0% with over 1000 training steps. (from "ReTool: Reinforcement Learning for Strategic Tool Use in LLMs")
2. DreamGym uses an outcome-based reward scheme, assigning r=1 only at the final step when the task is successfully completed and r=0 otherwise. (from "Scaling Agent Learning via Experience Synthesis")
3. ReTool sets the KL coefficient to 0.0 during RL training. (from "ReTool: Reinforcement Learning for Strategic Tool Use in LLMs")
4. RL training for LLM agents is challenging due to costly rollouts, limited task diversity, unreliable reward signals, and infrastructure complexity. (from "Scaling Agent Learning via Experience Synthesis")
5. ReTool (DeepSeek-R1-Distill-Qwen-32B backbone) achieves 72.5% accuracy on AIME 2024, surpassing OpenAI o1-preview by 27.9 percentage points. (from "ReTool: Reinforcement Learning for Strategic Tool Use in LLMs")
6. The experience model is trained via SFT with a joint objective over reasoning trace generation and next-state prediction, ensuring it learns causal reasoning and consistent state generalization. (from "Scaling Agent Learning via Experience Synthesis")
7. DreamGym is orthogonal to specific RL algorithms and focuses on scaling the synthesis of diverse, informative experiences to amplify RL training effectiveness. (from "Scaling Agent Learning via Experience Synthesis")
8. The cold-start model (SFT only, no RL) achieves 40.9% on AIME 2024, closely matching the text-based RL baseline (40.0%) and substantially surpassing the untrained base model (26.7%). (from "ReTool: Reinforcement Learning for Strategic Tool Use in LLMs")
9. Real environments involve long interaction sequences, high computational cost per step, and sparse reward feedback, making large-scale data collection prohibitively expensive. (from "Scaling Agent Learning via Experience Synthesis")
10. The experience model uses interaction history, task instruction, and retrieved past experiences as additional contexts beyond the current state-action pair to improve state prediction quality. (from "Scaling Agent Learning via Experience Synthesis")
11. On WebArena, DreamGym outperforms all baselines by over 30%. (from "Scaling Agent Learning via Experience Synthesis")
12. Curriculum task generation selects seed tasks based on high reward entropy — tasks where successes and failures are evenly balanced — to maximize information gain for credit assignment. (from "Scaling Agent Learning via Experience Synthesis")
13. WebArena is not RL-ready because it inherently lacks scalable data collection, environment reset mechanisms, and incurs high computational costs. (from "Scaling Agent Learning via Experience Synthesis")
14. The experience model predicts the next state and reward via chain-of-thought reasoning, enabling consistent and informative transition and feedback that reflects the consequences of agent actions. (from "Scaling Agent Learning via Experience Synthesis")
15. Open web environments are highly dynamic and produce noisy reward signals, lack reliable reset mechanisms, and introduce safety risks during large-scale exploration. (from "Scaling Agent Learning via Experience Synthesis")

## Relationships

## Limitations and Open Questions

## Sources
