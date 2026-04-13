---
type: entity
title: Proximal Policy Optimization (PPO)
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- frontier_lab_competition
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.008083566060398733
staleness: 0.0
status: active
tags: []
---
# Proximal Policy Optimization (PPO)

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

An RL fine-tuning method that introduces a clipped surrogate objective to limit update scale per step relative to the old policy, typically using a value model in an actor-critic manner. A predominant method for LLM fine-tuning.

## Key Findings

1. The Test Case Generator (TCG) achieves 80.8% pass rate on standard code after supervised fine-tuning (SFT) phase (from "o1-Coder: an o1 Replication for Coding")
2. O1-like planning models require knowledge of state updates following actions, shifting the paradigm toward model-based RL, unlike model-free RL methods like Q-learning (from "o1-Coder: an o1 Replication for Coding")
3. The Test Case Generator (TCG) achieves 89.2% pass rate after Direct Preference Optimization (DPO), a notable improvement over the SFT-only version (from "o1-Coder: an o1 Replication for Coding")
4. The O1-CODER framework uses a 'think before acting' approach where the model first generates detailed pseudocode and then generates the full executable code (from "o1-Coder: an o1 Replication for Coding")
5. The Process Reward Model (PRM) can be trained using either point-wise (absolute value prediction) or pair-wise (relative preference) formats derived from MCTS search tree data (from "o1-Coder: an o1 Replication for Coding")
6. Self-play enables the iterative cycle of new reasoning data generation, PRM updating, and policy improvement to achieve sustained model improvement (from "o1-Coder: an o1 Replication for Coding")
7. O1-CODER integrates reinforcement learning and Monte Carlo Tree Search to enhance System-2 thinking capabilities for coding tasks (from "o1-Coder: an o1 Replication for Coding")
8. Two main challenges for applying self-play RL to code generation are result evaluation (assessing code quality) and defining thinking/search behaviors (state transition and process reward granularity) (from "o1-Coder: an o1 Replication for Coding")
9. Vanilla LLMs face challenges in generating effective pseudocode, which is the motivation for SFT initialization and Self-Play+RL enhancement (from "o1-Coder: an o1 Replication for Coding")
10. Prior to o1, large language models primarily exhibited System-1 capabilities characterized by fast, intuitive responses trained on question-answer pairs without intermediate reasoning steps (from "o1-Coder: an o1 Replication for Coding")
11. Pseudocode-based reasoning generally decreases Pass@1 but significantly increases Average Sampling Pass Rate (ASPR), indicating pseudocode improves reasoning quality on correct paths (from "o1-Coder: an o1 Replication for Coding")
12. MCTS is used to construct step-level process reward data by exploring reasoning paths and backpropagating terminal node rewards to all preceding nodes (from "o1-Coder: an o1 Replication for Coding")
13. The terminal node reward in MCTS is computed as a weighted sum of compilation success rate and test case pass rate (from "o1-Coder: an o1 Replication for Coding")
14. Reward function generalization is a major challenge for deploying o1-like models in real-world applications beyond well-defined tasks (from "o1-Coder: an o1 Replication for Coding")
15. O1-like models cannot perform online behavior simulation during inference, preventing them from validating or correcting actions by returning to a previous state, leading to inability to backtrack (from "o1-Coder: an o1 Replication for Coding")

## Relationships

## Limitations and Open Questions

## Sources
