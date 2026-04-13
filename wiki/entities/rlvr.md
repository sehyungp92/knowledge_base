---
type: entity
title: RLVR
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- chain_of_thought
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.0038463171287654477
staleness: 0.0
status: active
tags: []
---
# RLVR

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Reinforcement Learning with Verifiable Rewards — a training paradigm where RL is applied using rewards from verifiable correctness signals, enabling models to acquire skills for solving downstream tasks.

## Key Findings

1. In the standard LongCoT RL environment the state size is unbounded, with |st| = O(t) as actions are appended, causing quadratic computation cost for attention-based policies. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
2. Scaling thinking from n to nS tokens costs O(n²S²) FLOPs under LongCoT-RL but only O(n²S) FLOPs under Delethink, making Delethink linear in S. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
3. With test-time scaling, Delethink continues to improve where LongCoT-RL plateaus. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
4. Delethink enforces a hard cap on state size of O(C) at every step for a fixed per-chunk budget C, making the policy's effective context independent of total reasoning length. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
5. Delethink turns the quadratic compute of attention into compute that is quadratic only in the constant chunk size C; overall training cost scales linearly with the number of thinking tokens. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
6. The standard RL reasoning environment makes the state unbounded, growing with longer thoughts, and forces attention-based policies to pay quadratic compute as thoughts lengthen. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
7. JustRL's results are limited to mathematical reasoning at 1.5B scale; generalization to other domains (coding, general QA) and larger model sizes remains unexplored. (from "JustRL: Scaling a 1.5B LLM with a Simple RL Recipe")
8. Delethink is an RL environment that structures reasoning into fixed-size chunks; at chunk boundaries the context is reset and the prompt is reinitialized with a short carryover from the previous chunk (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
9. JustRL uses GRPO with binary outcome rewards and a lightweight rule-based verifier from DAPO, without symbolic math libraries like SymPy. (from "JustRL: Scaling a 1.5B LLM with a Simple RL Recipe")
10. Delethink does not modify the model architecture and is not quadratic in context length; it decouples reasoning length from context length. (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
11. Markovian Thinking is a paradigm in which the policy advances reasoning while conditioning on a constant-size state, decoupling thinking length from context size, yielding linear compute with constant (from "The Markovian Thinker: Architecture-Agnostic Linear Scaling of Reasoning")
12. JustRL cannot definitively isolate which specific components (hyperparameters, verifier design, training data) are most critical to its success. (from "JustRL: Scaling a 1.5B LLM with a Simple RL Recipe")
13. AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world champions in Go, chess, shogi, and Stratego (from "A Survey of Reinforcement Learning for Large Reasoning Models")
14. JustRL trains on two 1.5B models using 32 A800-80GB GPUs for approximately 15 days each. (from "JustRL: Scaling a 1.5B LLM with a Simple RL Recipe")
15. Curriculum RL training on composed GSM8K problems achieves a 2.06× improvement on AIME 2024 relative to the instruct model baseline (from "h1: Bootstrapping LLMs to Reason over Longer Horizons via Reinforcement Learning")

## Capabilities

- RL with verifiable rewards enables LLMs to autonomously develop advanced problem-solving strategies without explicit step-by-step human supervision (DeepSeek R1-style RLVR) (maturity: narrow_production)
- Rule-based verifiable RL rewards can be constructed for physical AI reasoning tasks (spatial puzzles, arrow-of-time, object permanence) by using self-supervised MCQ formats, extending RLVR beyond math (maturity: demo)

## Relationships

## Limitations and Open Questions

## Sources
