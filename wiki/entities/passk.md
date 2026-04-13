---
type: entity
title: pass@k
entity_type: metric
theme_ids:
- code_and_software_ai
- search_and_tree_reasoning
- vision_language_models
- finetuning_and_distillation
- reinforcement_learning
- ai_market_dynamics
- scaling_laws
- latent_reasoning
- rl_theory_and_dynamics
- multi_agent_coordination
- agent_systems
- chain_of_thought
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
- policy_optimization
- video_and_world_models
- adaptive_computation
- test_time_learning
- scientific_and_medical_ai
- code_generation
- benchmark_design
- reasoning_and_planning
- evaluation_and_benchmarks
- tool_use_and_agent_protocols
- post_training_methods
- alignment_and_safety
- knowledge_and_memory
- context_engineering
- transformer_alternatives
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.02226468475137104
staleness: 0.0
status: active
tags: []
---
# pass@k

**Type:** metric
**Themes:** [[themes/code_and_software_ai|code_and_software_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/vision_language_models|vision_language_models]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/latent_reasoning|latent_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reward_modeling|reward_modeling]], [[themes/generative_media|generative_media]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/multimodal_models|multimodal_models]], [[themes/model_architecture|model_architecture]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/policy_optimization|policy_optimization]], [[themes/video_and_world_models|video_and_world_models]], [[themes/adaptive_computation|adaptive_computation]], [[themes/test_time_learning|test_time_learning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/code_generation|code_generation]], [[themes/benchmark_design|benchmark_design]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/post_training_methods|post_training_methods]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/context_engineering|context_engineering]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Overview

A metric measuring the probability that at least one of k sampled solutions passes a correctness criterion. Noted in TTT-Discover as the target metric explored by concurrent work using the entropic objective for binary-reward RL at training time.

## Key Findings

1. TTT-Discover outperforms ThetaEvolve when using the same model and compute budget, due to its special learning objective and search subroutine. (from "Learning to Discover at Test Time")
2. Standard RL exploration is problematic for discovery because the policy can collapse to safe, high-reward actions rather than risky ones that might achieve discovery. (from "Learning to Discover at Test Time")
3. All TTT-Discover results are achieved with an open model (OpenAI gpt-oss-120b), in contrast to previous best results that required closed frontier models. (from "Learning to Discover at Test Time")
4. Learning has historically superseded search for hard AI problems such as Go and protein folding. (from "Learning to Discover at Test Time")
5. The cost of TTT-Discover test-time training runs is only a few hundred dollars per problem. (from "Learning to Discover at Test Time")
6. Naive RL is misaligned with discovery because it optimizes average performance and is indifferent to the state of the art, whereas discovery success is determined by the maximum. (from "Learning to Discover at Test Time")
7. TTT-Discover performs reinforcement learning at test time, allowing the LLM to continue training with experience specific to the test problem, unlike prior work that prompts a frozen LLM. (from "Learning to Discover at Test Time")
8. TTT-Discover achieves a value of 0.380876 on Erdős' minimum overlap problem, surpassing the previous best human result of 0.380927 and previous best AI result of 0.380924. (from "Learning to Discover at Test Time")
9. TTT-Discover achieves a score of 567,062 on the AtCoder Heuristic Contest 39, slightly surpassing the best human score of 566,997. (from "Learning to Discover at Test Time")
10. Prior evolutionary search methods such as AlphaEvolve store past attempts in a buffer and use them to generate new prompts, but the LLM itself cannot improve because its weights remain frozen. (from "Learning to Discover at Test Time")
11. TTT-Discover sets the new state of the art in almost all scientific and engineering problems it attempted, spanning mathematics, GPU kernel engineering, algorithm design, and biology. (from "Learning to Discover at Test Time")
12. Discovery problems require ideas not only beyond the model's training data but also beyond all existing knowledge of humanity, making out-of-distribution generalization especially hard. (from "Learning to Discover at Test Time")
13. TTT-Discover achieves a denoising score of 0.71 on the single-cell analysis problem, compared to the best human score of 0.64. (from "Learning to Discover at Test Time")
14. TTT-Discover achieves a GPU kernel runtime of 1161 µs on the GPUMode TriMul competition on H100, faster than the best human result of 1371 µs. (from "Learning to Discover at Test Time")
15. As β approaches infinity, the entropic objective tends toward the maximum reward; however, too large β early in training causes instabilities, while too small β later makes advantages vanish. (from "Learning to Discover at Test Time")

## Known Limitations

- Under equivalent inference token budgets, thinking and non-thinking models converge to comparable pass@k performance on MATH-500, suggesting LRM advantages on standard math benchmarks may not reflect  (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
