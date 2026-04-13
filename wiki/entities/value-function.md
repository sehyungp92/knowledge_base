---
type: entity
title: value function
entity_type: method
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- software_engineering_agents
- test_time_compute_scaling
- video_and_world_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.00377734905157358
staleness: 0.0
status: active
tags: []
---
# value function

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A function that estimates the expected return from a given state, learned via self-play in the context of game-playing AI (e.g., AlphaGo).

## Key Findings

1. The methods that defeated world chess champion Kasparov in 1997 were based on massive, deep search, not human-knowledge-based approaches. (from "The Bitter Lesson")
2. Computer Go showed the same pattern as chess — human-knowledge approaches eventually proved irrelevant once search and learning were applied at scale — but the transition was delayed by approximately  (from "The Bitter Lesson")
3. Learning by self-play to learn a value function was an important component of the breakthrough in computer Go. (from "The Bitter Lesson")
4. Search and learning are the two most important classes of techniques for utilizing massive amounts of computation in AI research. (from "The Bitter Lesson")
5. Self-play learning, like search, enables massive computation to be brought to bear on a problem. (from "The Bitter Lesson")
6. In the DARPA-sponsored speech recognition competition in the 1970s, statistical methods based on hidden Markov models outperformed methods that incorporated human knowledge of words, phonemes, and the (from "The Bitter Lesson")
7. Deep learning methods rely even less on human knowledge than prior statistical methods, using more computation and huge training sets to produce dramatically better speech recognition systems. (from "The Bitter Lesson")
8. In computer vision, early feature-engineering approaches (edges, generalized cylinders, SIFT features) have been entirely discarded in favor of deep learning neural networks. (from "The Bitter Lesson")
9. Breakthrough progress in AI consistently arrives through an approach based on scaling computation via search and learning, rather than building in human knowledge. (from "The Bitter Lesson")
10. The contents of minds are irredeemably complex, and AI systems should not attempt to encode simplified models of space, objects, agents, or symmetries. (from "The Bitter Lesson")
11. Encoding researcher discoveries directly into AI systems makes it harder to develop the discovering process itself. (from "The Bitter Lesson")
12. The eventual success of computation-first approaches is psychologically difficult to absorb because it represents victory over a human-centric approach that researchers personally favored. (from "The Bitter Lesson")
13. The victory of statistical methods over human-knowledge methods in speech recognition led to a major change in all of natural language processing, gradually shifting the field toward statistics and co (from "The Bitter Lesson")
14. Incorporating human knowledge into AI systems was ultimately counterproductive and a waste of research time once massive computation became available through Moore's Law. (from "The Bitter Lesson")
15. Building human knowledge into AI agents helps in the short term and is personally satisfying to researchers, but in the long run plateaus and inhibits further progress. (from "The Bitter Lesson")

## Known Limitations

- RLHF bypassed core RL capabilities — value functions, exploration, world models, temporal abstraction — making current systems structurally incapable of deep autonomous learning (severity: significant, trajectory: improving)
- Value function estimation from long, incomplete experience streams is an unsolved problem in current RL methods, blocking effective long-horizon credit assignment (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
