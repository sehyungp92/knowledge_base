---
type: entity
title: Monte Carlo Tree Search (MCTS)
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.005453982033933189
staleness: 0.0
status: active
tags: []
---
# Monte Carlo Tree Search (MCTS)

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A heuristic search algorithm that uses random rollouts (simulations) to estimate the value of tree nodes. Applied to LLM reasoning but requires many rollouts, making it computationally expensive.

## Key Findings

1. PPM outperforms both ORM and Q-value-score-based PRM (PQM) across all challenging math benchmarks in System 2 reasoning (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
2. O1-CODER integrates reinforcement learning and Monte Carlo Tree Search to enhance System-2 thinking capabilities for coding tasks (from "o1-Coder: an o1 Replication for Coding")
3. The Process Preference Model (PPM) is trained using preference pairs derived from Q-values with pairwise ranking loss, avoiding direct use of Q-values as reward labels (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
4. Step-by-step verified reasoning trajectories significantly outperform GPT-4 distillation (NuminaMath-CoT, MetaMath) and rejection sampling as SFT training data (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
5. rStar-Math with a 7B PPM outperforms Qwen Best-of-N baselines that use a 10x larger 72B reward model across all benchmarks (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
6. Terminal nodes in MCTS are scored as +1 for correct answers and -1 for incorrect answers, with Q-values of intermediate nodes updated through backpropagation based on these terminal scores (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
7. rStar-Math improves Qwen2.5-Math-7B from 58.8% to 90.0% on the MATH benchmark, surpassing o1-preview by 4.5% (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
8. Small language models (1.5B-7B) can rival or surpass OpenAI o1 math reasoning without distillation from superior models (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
9. rStar-Math solves an average of 53.3% (8/15) of AIME 2024 problems, ranking among the top 20% of the brightest high school math students (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
10. Code-augmented CoT synthesis retains only steps with successfully executed Python code, filtering erroneous intermediate steps (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
11. Starting from round 2, the 7B rStar-Math model with MCTS surpasses GPT-4o on MATH benchmark (86.6% vs 76.6%) (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
12. The four-round self-evolution process progressively improves both the policy SLM and PPM, covering 90.25% of 747k math problems by round 4 (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
13. PPM-augmented MCTS in round 3 significantly increases coverage of Olympiad-level problems in training data from 56.04% to 62.16% (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
14. The PPM is initialized from the fine-tuned policy model with its next-token prediction head replaced by a scalar-value head using tanh activation to constrain outputs to [-1, 1] (from "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking")
15. Two main challenges for applying self-play RL to code generation are result evaluation (assessing code quality) and defining thinking/search behaviors (state transition and process reward granularity) (from "o1-Coder: an o1 Replication for Coding")

## Relationships

## Limitations and Open Questions

## Sources
