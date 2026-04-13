---
type: entity
title: RLHF
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- alignment_methods
- chain_of_thought
- continual_learning
- finetuning_and_distillation
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
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.005180648873935252
staleness: 0.0
status: active
tags: []
---
# RLHF

**Type:** method
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Reinforcement Learning from Human Feedback — training paradigm that uses human preference signals as a reward model to fine-tune language models, associated with ChatGPT-era models.

## Key Findings

1. VinePPO inherits all of PPO's hyperparameters and modifies only the advantage estimation stage, allowing isolation of the effect of improved credit assignment. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
2. VinePPO computes unbiased Monte Carlo-based value estimates by sampling auxiliary rollouts from each intermediate state and averaging their returns. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
3. The auxiliary rollouts in VinePPO are used exclusively for value estimation and do not directly contribute to policy gradient updates. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
4. Language generation as an MDP has deterministic, known transition dynamics because states are always constructed by concatenating tokens. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
5. VinePPO uses K=9 as the default number of auxiliary MC rollouts per state. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
6. Auxiliary rollouts in VinePPO are used exclusively for value estimation and do not contribute directly to policy gradient updates. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
7. VeriFree bypasses answer verification and instead uses RL to directly maximize the probability of generating the reference answer. (from "Reinforcing General Reasoning without Verifiers")
8. AlphaGo and AlphaZero, learning exclusively through self-play and reward feedback, surpassed world champions in Go, chess, shogi, and Stratego (from "A Survey of Reinforcement Learning for Large Reasoning Models")
9. VinePPO computes unbiased Monte Carlo-based value estimates for intermediate states by sampling auxiliary rollouts from the current policy at each state. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
10. VinePPO consistently outperforms standard PPO, GRPO, RLOO, RestEM, and DPO+ on both MATH and GSM8K datasets across model sizes. (from "VinePPO: Refining Credit Assignment in RL Training of LLMs")
11. o3 was trained with tools through reinforcement learning, teaching it not just how to use tools but to reason about when to use them. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
12. In RLVR, a rule-based program assigns a reward of 1 if the final answer is correct and 0 otherwise. (from "Reinforcing General Reasoning without Verifiers")
13. Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the primary constraint and the new frontier is reliable interaction with the external world. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
14. The Autoregressive Reward Model parametrizes the reward of a complete response as a log probability, enabling a natural token-level factorization into the sum of log probabilities conditioned on past  (from "GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time Alignment")
15. The Autoregressive RM parametrization is theoretically proven to be expressive enough to guide frozen LLMs toward any distribution achievable by traditional trajectory-level RMs within the KL-regulari (from "GenARM: Reward Guided Generation with Autoregressive Reward Model for Test-time Alignment")

## Known Limitations

- RLHF bypassed core RL capabilities — value functions, exploration, world models, temporal abstraction — making current systems structurally incapable of deep autonomous learning (severity: significant, trajectory: improving)
- State-of-the-art frontier models without TTT (Claude 3.5 Sonnet: 21%, GPT-4o: 9%, o1 preview: 21%, DeepSeek R1: 20.5%) show extremely poor ARC performance, confirming that scale and RLHF alone do not  (severity: significant, trajectory: stable)

## Relationships

## Limitations and Open Questions

## Sources
