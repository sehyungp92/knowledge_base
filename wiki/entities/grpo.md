---
type: entity
title: GRPO
entity_type: method
theme_ids:
- startup_and_investment
- code_and_software_ai
- vision_language_models
- finetuning_and_distillation
- reinforcement_learning
- image_generation_models
- ai_market_dynamics
- continual_learning
- unified_multimodal_models
- scaling_laws
- rl_theory_and_dynamics
- long_context_and_attention
- multi_agent_coordination
- startup_formation_and_gtm
- agent_self_evolution
- software_engineering_agents
- computer_use_and_gui_agents
- chain_of_thought
- agent_systems
- ai_for_scientific_discovery
- test_time_compute_scaling
- pretraining_and_scaling
- reward_modeling
- generative_media
- mathematical_and_formal_reasoning
- frontier_lab_competition
- hallucination_and_reliability
- multimodal_models
- model_architecture
- synthetic_data_generation
- retrieval_augmented_generation
- policy_optimization
- adaptive_computation
- test_time_learning
- scientific_and_medical_ai
- code_generation
- benchmark_design
- agent_memory_systems
- agent_evaluation
- reasoning_and_planning
- evaluation_and_benchmarks
- tool_use_and_agent_protocols
- post_training_methods
- alignment_and_safety
- knowledge_and_memory
- in_context_and_meta_learning
- transformer_alternatives
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.06018722833780498
staleness: 0.0
status: active
tags: []
---
# GRPO

**Type:** method
**Themes:** [[themes/startup_and_investment|startup_and_investment]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/vision_language_models|vision_language_models]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/image_generation_models|image_generation_models]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/continual_learning|continual_learning]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/scaling_laws|scaling_laws]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/chain_of_thought|chain_of_thought]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reward_modeling|reward_modeling]], [[themes/generative_media|generative_media]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/multimodal_models|multimodal_models]], [[themes/model_architecture|model_architecture]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/policy_optimization|policy_optimization]], [[themes/adaptive_computation|adaptive_computation]], [[themes/test_time_learning|test_time_learning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/code_generation|code_generation]], [[themes/benchmark_design|benchmark_design]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_evaluation|agent_evaluation]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/post_training_methods|post_training_methods]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Overview

A policy optimization method used for fine-tuning LLMs on tool use tasks; fine-tuning Qwen2.5-7B-Instruct on 100 examples raises BFCL multi-step tool-use accuracy from 55% to 78%.

## Key Findings

1. Learning has historically superseded search for hard AI problems such as Go and protein folding. (from "Learning to Discover at Test Time")
2. Standard RL exploration is problematic for discovery because the policy can collapse to safe, high-reward actions rather than risky ones that might achieve discovery. (from "Learning to Discover at Test Time")
3. TTT-Discover achieves a denoising score of 0.71 on the single-cell analysis problem, compared to the best human score of 0.64. (from "Learning to Discover at Test Time")
4. Prior evolutionary search methods such as AlphaEvolve store past attempts in a buffer and use them to generate new prompts, but the LLM itself cannot improve because its weights remain frozen. (from "Learning to Discover at Test Time")
5. TTT-Discover sets the new state of the art in almost all scientific and engineering problems it attempted, spanning mathematics, GPU kernel engineering, algorithm design, and biology. (from "Learning to Discover at Test Time")
6. Naive RL is misaligned with discovery because it optimizes average performance and is indifferent to the state of the art, whereas discovery success is determined by the maximum. (from "Learning to Discover at Test Time")
7. TTT-Discover achieves a value of 0.380876 on Erdős' minimum overlap problem, surpassing the previous best human result of 0.380927 and previous best AI result of 0.380924. (from "Learning to Discover at Test Time")
8. TTT-Discover achieves a GPU kernel runtime of 1161 µs on the GPUMode TriMul competition on H100, faster than the best human result of 1371 µs. (from "Learning to Discover at Test Time")
9. TTT-Discover performs reinforcement learning at test time, allowing the LLM to continue training with experience specific to the test problem, unlike prior work that prompts a frozen LLM. (from "Learning to Discover at Test Time")
10. The cost of TTT-Discover test-time training runs is only a few hundred dollars per problem. (from "Learning to Discover at Test Time")
11. TTT-Discover achieves a score of 567,062 on the AtCoder Heuristic Contest 39, slightly surpassing the best human score of 566,997. (from "Learning to Discover at Test Time")
12. All TTT-Discover results are achieved with an open model (OpenAI gpt-oss-120b), in contrast to previous best results that required closed frontier models. (from "Learning to Discover at Test Time")
13. Discovery problems require ideas not only beyond the model's training data but also beyond all existing knowledge of humanity, making out-of-distribution generalization especially hard. (from "Learning to Discover at Test Time")
14. TTT-Discover outperforms ThetaEvolve when using the same model and compute budget, due to its special learning objective and search subroutine. (from "Learning to Discover at Test Time")
15. As β approaches infinity, the entropic objective tends toward the maximum reward; however, too large β early in training causes instabilities, while too small β later makes advantages vanish. (from "Learning to Discover at Test Time")

## Capabilities

- Relative within-group trajectory ranking sidesteps LLM-as-judge score calibration problems, enabling reliable GRPO reward signals from an otherwise poorly-calibrated judge (maturity: demo)

## Relationships

## Limitations and Open Questions

## Sources
