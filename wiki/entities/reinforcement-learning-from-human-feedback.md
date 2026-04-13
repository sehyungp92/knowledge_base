---
type: entity
title: Reinforcement Learning from Human Feedback
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- compute_and_hardware
- context_engineering
- creative_content_generation
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- hallucination_and_reliability
- interpretability
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- medical_and_biology_ai
- model_architecture
- model_behavior_analysis
- model_commoditization_and_open_source
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.028401214532280967
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning from Human Feedback

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/context_engineering|context_engineering]], [[themes/creative_content_generation|creative_content_generation]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

A pre-2025 training stage using human preference signals as rewards. Considered a 'thin/short' finetune compared to RLVR, with gameable reward signals.

## Key Findings

1. Games are a limited proxy for the real world, which is unbounded and far more complex (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
2. Planning, in-context learning, and reliability/robustness are the three critical challenges for AI agents to solve (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
3. AlphaGo's policy network recommended the most promising moves given a board position (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
4. Reliability for AI agents requires the ability to detect and recover from their own mistakes (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
5. AlphaZero required access to a perfect simulator of the world (i.e., perfect knowledge of game rules), which MuZero eliminated (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
6. AlphaZero resolved AlphaGo's issues with hallucinations, blind spots, and robustness (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
7. AlphaZero uses the same policy network and value network architecture as AlphaGo, combined with MCTS (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
8. AlphaGo used policy gradient reinforcement learning via self-play to improve the policy network after supervised pretraining (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
9. Removing human data as a starting point (AlphaZero vs AlphaGo) expanded applicability to domains where insufficient human data exists (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
10. A fundamental limitation of LLMs is the availability of human training data — the 'data wall' (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
11. AlphaGo's policy network was initially trained via supervised learning on a large set of human professional games (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
12. AlphaGo's value network estimated the winning probability from any given board position (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
13. AlphaGo used two neural networks: a policy network and a value network (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
14. AlphaGo used MCTS as the most efficient method for search and planning over future game states (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
15. AlphaGo used minmax search to find the optimal action by simulating opponent responses (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")

## Relationships

## Limitations and Open Questions

## Sources
