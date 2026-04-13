---
type: entity
title: Best-of-N Sampling
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- finetuning_and_distillation
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 13
sources_since_update: 0
update_count: 1
influence_score: 0.005787190984497062
staleness: 0.0
status: active
tags: []
---
# Best-of-N Sampling

**Type:** method
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A baseline test-time strategy that generates N independent samples and selects the best one, typically by a reward/verifier model.

## Key Findings

1. Learning has historically superseded search for hard AI problems such as Go and protein folding. (from "Learning to Discover at Test Time")
2. Standard RL exploration is problematic for discovery because the policy can collapse to safe, high-reward actions rather than risky ones that might achieve discovery. (from "Learning to Discover at Test Time")
3. The cost of TTT-Discover test-time training runs is only a few hundred dollars per problem. (from "Learning to Discover at Test Time")
4. TTT-Discover achieves a denoising score of 0.71 on the single-cell analysis problem, compared to the best human score of 0.64. (from "Learning to Discover at Test Time")
5. Naive RL is misaligned with discovery because it optimizes average performance and is indifferent to the state of the art, whereas discovery success is determined by the maximum. (from "Learning to Discover at Test Time")
6. Prior evolutionary search methods such as AlphaEvolve store past attempts in a buffer and use them to generate new prompts, but the LLM itself cannot improve because its weights remain frozen. (from "Learning to Discover at Test Time")
7. Discovery problems require ideas not only beyond the model's training data but also beyond all existing knowledge of humanity, making out-of-distribution generalization especially hard. (from "Learning to Discover at Test Time")
8. All TTT-Discover results are achieved with an open model (OpenAI gpt-oss-120b), in contrast to previous best results that required closed frontier models. (from "Learning to Discover at Test Time")
9. TTT-Discover sets the new state of the art in almost all scientific and engineering problems it attempted, spanning mathematics, GPU kernel engineering, algorithm design, and biology. (from "Learning to Discover at Test Time")
10. TTT-Discover achieves a GPU kernel runtime of 1161 µs on the GPUMode TriMul competition on H100, faster than the best human result of 1371 µs. (from "Learning to Discover at Test Time")
11. TTT-Discover achieves a score of 567,062 on the AtCoder Heuristic Contest 39, slightly surpassing the best human score of 566,997. (from "Learning to Discover at Test Time")
12. TTT-Discover outperforms ThetaEvolve when using the same model and compute budget, due to its special learning objective and search subroutine. (from "Learning to Discover at Test Time")
13. TTT-Discover achieves a value of 0.380876 on Erdős' minimum overlap problem, surpassing the previous best human result of 0.380927 and previous best AI result of 0.380924. (from "Learning to Discover at Test Time")
14. TTT-Discover performs reinforcement learning at test time, allowing the LLM to continue training with experience specific to the test problem, unlike prior work that prompts a frozen LLM. (from "Learning to Discover at Test Time")
15. As β approaches infinity, the entropic objective tends toward the maximum reward; however, too large β early in training causes instabilities, while too small β later makes advantages vanish. (from "Learning to Discover at Test Time")

## Relationships

## Limitations and Open Questions

## Sources
