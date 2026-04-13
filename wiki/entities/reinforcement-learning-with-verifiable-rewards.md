---
type: entity
title: Reinforcement Learning with Verifiable Rewards
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- creative_content_generation
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- hallucination_and_reliability
- in_context_and_meta_learning
- interpretability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- mechanistic_interpretability
- model_commoditization_and_open_source
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
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 13
sources_since_update: 0
update_count: 1
influence_score: 0.005783240533043558
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning with Verifiable Rewards

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/creative_content_generation|creative_content_generation]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

RL training paradigm where rewards are given based on verifiable correctness of outputs, used in training o3 and similar reasoning models

## Key Findings

1. MemSearcher trained on Qwen2.5-3B-Instruct achieves +11% relative average improvement over strong baselines on seven public benchmarks. (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
2. MemSearcher's compact memory is constrained by a predefined maximum token length, ensuring per-turn context remains short and stable regardless of the number of interaction turns. (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
3. MaxEnt-Guided Policy Optimization (MGPO) dynamically prioritizes training on problems where the model's empirical accuracy is closest to 0.5 (maximum uncertainty), using KL divergence from the maximum (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
4. Data decontamination for VibeThinker used 10-gram matching to identify and exclude training samples with semantic overlap with evaluation sets, preceded by text standardization and normalization (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
5. ReAct-based search agents produce continuously growing LLM contexts because they concatenate all previous thoughts, actions, and observations at each turn. (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
6. MemSearcher was trained from scratch on the same dataset as Search-R1, enabling a controlled comparison. (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
7. MGPO degrades to standard GRPO when the regularization coefficient λ=0, and increases focus on uncertain problems as λ increases (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
8. The Spectrum-to-Signal Principle (SSP) redefines the SFT-RL pipeline by assigning distinct complementary objectives: SFT maximizes diversity (Pass@K) as a 'spectrum phase', while RL amplifies correct  (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
9. Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the primary constraint and the new frontier is reliable interaction with the external world. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
10. For VibeThinker-1.5B, Expert Model Fusion uses unweighted averaging (w_i = 1/N) across N specialist models to ensure equitable integration of subdomain capabilities (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
11. o3 was trained with tools through reinforcement learning, teaching it not just how to use tools but to reason about when to use them. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
12. MemSearcher uses the LLM itself as a memory manager to iteratively compress only essential information from each interaction, discarding reasoning traces, raw observations, and actions after each turn (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
13. VibeThinker-1.5B was trained at a total computational cost of approximately $7,800, consuming approximately 3,900 GPU hours on NVIDIA H800 GPUs (from "Tiny Model, Big Logic: Diversity-Driven Optimization Elicits Large-Model Reasoning Ability in VibeThinker-1.5B")
14. MemSearcher trained on Qwen2.5-7B-Instruct achieves +12% relative average improvement over strong baselines on seven public benchmarks. (from "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning")
15. Writing-R1, based on an in-house SFT thinking model fine-tuned with BRPO, achieves 8.68 on WritingBench and 3.93 on Writing Testset, outperforming its SFT base (8.56 and 3.31 respectively). (from "Writing-Zero: Bridge the Gap Between Non-verifiable Tasks and Verifiable Rewards")

## Relationships

## Limitations and Open Questions

## Sources
