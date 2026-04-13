---
type: entity
title: Proximal Policy Optimization
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- code_and_software_ai
- code_generation
- computer_use_and_gui_agents
- finetuning_and_distillation
- frontier_lab_competition
- in_context_and_meta_learning
- knowledge_and_memory
- mathematical_and_formal_reasoning
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.012149029808583019
staleness: 0.0
status: active
tags: []
---
# Proximal Policy Optimization

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A policy gradient RL algorithm that has been the most successful approach for training language models with reinforcement learning, using a value model to estimate expected returns.

## Key Findings

1. A larger LLM completer generates higher quality process annotation datasets; the quality of training data for the completer also significantly affects annotation quality. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
2. SE progressively aligns closer to the human-annotated distribution as N increases, in contrast to HE which does not exhibit similar behavior. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
3. DeepSeek-67B achieves 93.3% on GSM8K and 48.1% on MATH with MATH-SHEPHERD verification, which are unprecedented results for open-source models not relying on additional tools. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
4. Step-by-step PPO supervised by MATH-SHEPHERD outperforms vanilla PPO with ORM, demonstrating the potential of step-by-step supervision. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
5. Human annotation for PRM training is costly and hinders the advancement and practical application of PRM, especially for intricate multi-step reasoning tasks requiring advanced annotator skills. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
6. Reinforcement learning and verification with MATH-SHEPHERD are complementary: step-by-step PPO Mistral-7B outperforms supervised fine-tuning Mistral-7B by 7.2% on MATH with self-consistency as verifie (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
7. Step-by-step PPO with MATH-SHEPHERD significantly improves Mistral-7B accuracy from 77.9% to 84.1% on GSM8K and from 28.6% to 33.0% on MATH. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
8. With MATH-SHEPHERD verification on top of PPO-trained Mistral-7B, accuracy is further enhanced to 89.1% on GSM8K and 43.5% on MATH. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
9. The quality of a reasoning step in MATH-SHEPHERD is defined as its potential to deduce the correct final answer, inspired by Monte Carlo Tree Search. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
10. MATH-SHEPHERD as a verifier consistently outperforms self-consistency and ORM across two datasets with all generators tested. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
11. Using a larger reward model to validate the output of a smaller generator significantly enhances performance; conversely, a smaller reward model validating a larger generator adversely impacts perform (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
12. The completion process for constructing PRM training data demands significant computing resources, potentially limiting usage, though cost remains much lower than human annotation. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
13. Hard Estimation (HE) labels a step as good if any one of N completion paths reaches the correct answer, while Soft Estimation (SE) uses the frequency of correct answers across all N paths. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
14. PRM achieves a greater advantage over ORM on the more challenging MATH dataset than on the simpler GSM8K, because GSM8K requires fewer steps for problem-solving. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")
15. PRM exhibits superior data efficiency compared to ORM, outperforming ORM by approximately 4% accuracy when using a modest 10k training instances, and has a higher potential ceiling. (from "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations")

## Relationships

## Limitations and Open Questions

## Sources
