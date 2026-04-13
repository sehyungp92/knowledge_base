---
type: entity
title: self-play
entity_type: method
theme_ids:
- agent_systems
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- compute_and_hardware
- frontier_lab_competition
- generative_media
- interpretability
- medical_and_biology_ai
- model_behavior_analysis
- model_commoditization_and_open_source
- multi_agent_coordination
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- search_and_tree_reasoning
- startup_and_investment
- synthetic_data_generation
- test_time_compute_scaling
- vc_and_startup_ecosystem
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.007728873343430681
staleness: 0.0
status: active
tags: []
---
# self-play

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/interpretability|interpretability]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/startup_and_investment|startup_and_investment]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A training paradigm where AI agents play against or interact with copies of themselves to generate synthetic training data, enabling learning beyond human-labeled datasets.

## Key Findings

1. AlphaGo's policy network was initially trained via supervised learning on a large set of human professional games (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
2. Planning, in-context learning, and reliability/robustness are the three critical challenges for AI agents to solve (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
3. Reliability for AI agents requires the ability to detect and recover from their own mistakes (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
4. AlphaGo's policy network recommended the most promising moves given a board position (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
5. Games are a limited proxy for the real world, which is unbounded and far more complex (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
6. AlphaZero resolved AlphaGo's issues with hallucinations, blind spots, and robustness (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
7. AlphaGo's value network estimated the winning probability from any given board position (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
8. Removing human data as a starting point (AlphaZero vs AlphaGo) expanded applicability to domains where insufficient human data exists (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
9. AlphaZero uses the same policy network and value network architecture as AlphaGo, combined with MCTS (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
10. AlphaGo used policy gradient reinforcement learning via self-play to improve the policy network after supervised pretraining (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
11. A fundamental limitation of LLMs is the availability of human training data — the 'data wall' (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
12. AlphaZero required access to a perfect simulator of the world (i.e., perfect knowledge of game rules), which MuZero eliminated (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
13. AlphaGo used two neural networks: a policy network and a value network (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
14. AlphaGo used MCTS as the most efficient method for search and planning over future game states (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")
15. AlphaGo used minmax search to find the optimal action by simulating opponent responses (from "From AlphaGo to AGI ft ReflectionAI Founder Ioannis Antonoglou")

## Relationships

## Limitations and Open Questions

## Sources
