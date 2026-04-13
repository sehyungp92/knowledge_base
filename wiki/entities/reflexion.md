---
type: entity
title: Reflexion
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- chain_of_thought
- context_engineering
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.010640053646792644
staleness: 0.0
status: active
tags: []
---
# Reflexion

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A technique where an agent reflects after each turn and reuses self-generated reflections as memories for subsequent agent turns.

## Key Findings

1. Reflexion improves AlfWorld decision-making performance by an absolute 22% over strong baseline approaches in 12 iterative learning steps. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
2. Reflexion's policy optimization via natural language may still succumb to non-optimal local minima solutions. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
3. Reflexion allows for more nuanced forms of feedback (targeted changes in actions) compared to scalar or vector rewards that are challenging for accurate credit assignment. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
4. Reflexion reinforces language agents through linguistic feedback rather than weight updates, maintaining reflective text in an episodic memory buffer. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
5. The Self-Reflection model generates nuanced and specific feedback from a sparse reward signal (e.g., binary success status), current trajectory, and persistent memory, storing it in the agent's memory (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
6. Omitting internal test generation and execution (while keeping self-reflection) reduces Reflexion's HumanEval Rust accuracy to 52%, below the 60% baseline, because the agent cannot determine if the cu (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
7. Reflexion converts binary or scalar environment feedback into verbal feedback (textual summary) that acts as a semantic gradient signal for the agent. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
8. Reflexion improves HotPotQA reasoning performance by 20% over baseline approaches. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
9. Reflexion has the disadvantage of relying on the LLM's self-evaluation capabilities and lacks a formal guarantee for success. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
10. Reflexion achieves 91% pass@1 accuracy on HumanEval, surpassing the previous state-of-the-art GPT-4 which achieves 80%. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
11. Reflexion is lightweight and does not require fine-tuning the LLM, unlike traditional RL approaches. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
12. Reflexion provides a more explicit and interpretable form of episodic memory over prior experiences and more explicit hints for actions in future episodes. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
13. CoT with ground-truth context (CoT GT) still fails to correctly infer the answer for 39% of HotPotQA questions, but Reflexion helps improve accuracy by 14% without access to the ground-truth answer. (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
14. Reflexion's programming implementation uses self-generated unit test suites produced with Chain-of-Thought prompting, filtered for syntactic validity via AST construction, with a maximum of 6 tests pe (from "Reflexion: Language Agents with Verbal Reinforcement Learning")
15. Test-driven development for code generation has practical limitations including non-deterministic functions, impure functions interacting with APIs, hardware-dependent outputs, and parallel/concurrent (from "Reflexion: Language Agents with Verbal Reinforcement Learning")

## Relationships

## Limitations and Open Questions

## Sources
