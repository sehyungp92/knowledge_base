---
type: entity
title: HotpotQA
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- chain_of_thought
- code_and_software_ai
- code_generation
- context_engineering
- finetuning_and_distillation
- hallucination_and_reliability
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.01046660815156927
staleness: 0.0
status: active
tags: []
---
# HotpotQA

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/context_engineering|context_engineering]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

A multi-hop question answering dataset used for training and in-domain evaluation in SKILLRL's search-augmented QA experiments.

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
