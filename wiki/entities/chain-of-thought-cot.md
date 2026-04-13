---
type: entity
title: Chain-of-Thought (CoT)
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- generative_media
- hallucination_and_reliability
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- search_and_tree_reasoning
- test_time_compute_scaling
- tool_use_and_agent_protocols
- transformer_alternatives
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.0070622669564567786
staleness: 0.0
status: active
tags: []
---
# Chain-of-Thought (CoT)

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

Technique of having language models generate intermediate reasoning steps before producing a final answer; in LLMs the function is generating useful context for the final answer rather than faithfully representing the model's internal reasoning process.

## Key Findings

1. Coconut uses the last hidden state of the LLM as a 'continuous thought' representation of the reasoning state, feeding it back as the next input embedding directly in continuous space instead of decod (from "Training Large Language Models to Reason in a Continuous Latent Space")
2. ProsQA is a new logical reasoning dataset based on directed acyclic graphs (DAGs) of logical relationships, designed to require sophisticated planning and search strategies beyond what ProntoQA demand (from "Training Large Language Models to Reason in a Continuous Latent Space")
3. Coconut continuous thoughts are fully differentiable, allowing end-to-end optimization by gradient descent. (from "Training Large Language Models to Reason in a Continuous Latent Space")
4. HRM executes sequential reasoning tasks in a single forward pass without explicit supervision of the intermediate process. (from "Hierarchical Reasoning Model")
5. TORL-1.5B achieves 48.5% average accuracy across mathematical benchmarks, surpassing Qwen2.5-Math-1.5B-Instruct (35.9%) and Qwen2.5-Math-1.5B-Instruct-TIR (41.3%). (from "ToRL: Scaling Tool-Integrated RL")
6. HRM operates without pre-training or CoT data, using only input-output pairs and randomly initialized weights. (from "Hierarchical Reasoning Model")
7. HRM features two coupled recurrent modules: a high-level module for abstract deliberate reasoning and a low-level module for fast detailed computations, inspired by hierarchical processing in the brai (from "Hierarchical Reasoning Model")
8. TORL uses a rule-based reward function: correct answers receive +1, incorrect answers receive -1, and responses containing non-executable code incur an additional -0.5 penalty. (from "ToRL: Scaling Tool-Integrated RL")
9. RLMT (RL with Model-rewarded Thinking) trains language models to generate long chain-of-thought reasoning before final answers using online RL algorithms such as GRPO, evaluated against a preference-b (from "Language Models that Think, Chat Better")
10. TORL uses the GRPO algorithm with rollout batch size of 128, 16 samples per problem, no KL loss, and temperature of 1 to enhance model exploration. (from "ToRL: Scaling Tool-Integrated RL")
11. TORL-7B achieves 43.3% accuracy on AIME24, surpassing RL without tool integration by 14% and the best existing Tool-Integrated Reasoning model by 17%. (from "ToRL: Scaling Tool-Integrated RL")
12. AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world champions in Go, chess, shogi, and Stratego (from "A Survey of Reinforcement Learning for Large Reasoning Models")
13. The TORL training dataset consists of 28,740 high-quality verifiable mathematical questions derived from Olympic-level competition problems after filtering and difficulty balancing. (from "ToRL: Scaling Tool-Integrated RL")
14. TORL-7B reaches 62.1% average accuracy across benchmarks, representing a 14.7% absolute improvement over other open-source models with the same base model. (from "ToRL: Scaling Tool-Integrated RL")
15. RLMT uses 7.5K prompts from the WildChat-IF subset of the Tulu 3 SFT mixture, which prioritizes conversational prompts covering a wide range of realistic user queries (from "Language Models that Think, Chat Better")

## Relationships

## Limitations and Open Questions

## Sources
