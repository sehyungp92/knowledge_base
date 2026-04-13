---
type: entity
title: Chain-of-Thought Prompting
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_for_scientific_discovery
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- hallucination_and_reliability
- in_context_and_meta_learning
- interpretability
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- medical_and_biology_ai
- model_behavior_analysis
- multimodal_models
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
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- spatial_and_3d_intelligence
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
- video_and_world_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.027475438077081662
staleness: 0.0
status: active
tags: []
---
# Chain-of-Thought Prompting

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A prompting technique where models generate intermediate reasoning steps before producing a final answer; the foundation upon which inference-time scaling and reasoning models were built by scaling 10-100X.

## Key Findings

1. ARC-AGI-Pub restricts internet-connected programs to the public leaderboard, making them ineligible for prize money. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
2. Quiet-STaR achieves zero-shot improvements on CommonsenseQA from 36.3% to 47.2% without any fine-tuning on the task. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
3. ARC is a more tractable target for test-time compute approaches than general AGI tasks because ARC solutions are easy to verify by running candidate functions against provided examples. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
4. Pooling prompts are not always superior to single-parent prompts because LLMs pay less attention to longer contexts and higher token counts increase computational cost. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
5. The evolutionary approach can get stuck at local maxima when top-performing parents all share the same partial solution pattern, missing diverse solutions from other lineages. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
6. Chain-of-Thought prompting is effective for ARC reasoning tasks because it guides LLMs to produce step-by-step reasoning before outputting a solution. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
7. The previous state-of-the-art on ARC-AGI-Pub was 43%, achieved by Ryan Greenblatt. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
8. Pooling multiple parent functions into a single revision prompt helps address the local maxima problem by ensuring at least one solution for each example case is represented. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
9. The method generates Python functions rather than output grids directly because functions can be executed and verified for correctness whereas grids cannot. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
10. Fitness evaluation for ARC transform functions uses a two-tier scoring: primary score is the number of fully correct example grids, secondary score is the number of correct individual cells for non-pe (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
11. The Evolutionary Test-time Compute method generates up to 500 Python transform functions using 31 dynamic prompts per ARC challenge. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
12. Humans achieve approximately 85% accuracy on ARC challenges, while the best LLMs achieve only 18%. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
13. 42% of the Deep architecture's solutions came from generations 2–4, demonstrating the value of iterative refinement over single-generation generation. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
14. The author achieved 53.6% accuracy on ARC-AGI-Pub using Claude Sonnet 3.5, setting a new public record. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
15. Quiet-STaR achieves zero-shot improvements on GSM8K from 5.9% to 10.9% without any fine-tuning on the task. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")

## Relationships

## Limitations and Open Questions

## Sources
