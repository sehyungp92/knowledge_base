---
type: entity
title: Bitter Lesson
entity_type: theory
theme_ids:
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- context_engineering
- frontier_lab_competition
- generative_media
- knowledge_and_memory
- model_commoditization_and_open_source
- multimodal_models
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- scaling_laws
- search_and_tree_reasoning
- software_engineering_agents
- spatial_and_3d_intelligence
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- tool_use_and_agent_protocols
- unified_multimodal_models
- vc_and_startup_ecosystem
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 9
sources_since_update: 0
update_count: 1
influence_score: 0.005986125036727832
staleness: 0.0
status: active
tags: []
---
# Bitter Lesson

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

Rich Sutton's principle that methods leveraging general learning and search at scale consistently outperform methods that encode human knowledge and heuristics, applied here to argue that prompting-based agent engineering will be superseded by learned planning.

## Key Findings

1. Sora learned that taking a bite out of a hamburger leaves a bite mark, demonstrating emergent understanding of object-state changes from video data. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
2. Generating long HD videos with Sora currently takes at least a few minutes of compute time, limiting democratized access. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
3. Sora currently has significant limitations in modeling complex long-term physical object-to-object interactions, such as a soccer ball vaporizing mid-scene. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
4. The OpenAI team believes models like Sora are on the critical pathway to AGI because generating realistic video requires learning models of how people, animals, and objects behave and interact. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
5. Sora can generate videos at aspect ratios ranging from 1:2 to 2:1, as well as images, making it a generalist visual generation model. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
6. SpaceTime patches serve as the tokenization primitive for Sora, analogous to tokens in language models, enabling training on video data of arbitrary resolution, aspect ratio, and duration. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
7. Increasing training compute for Sora consistently improves output quality, demonstrating that video diffusion Transformers follow scaling laws. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
8. Sora learned 3D scene understanding without any explicit 3D supervision, purely from training on video data. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
9. The team believes that simply predicting data at scale—as done with next-token prediction in language models—is the most effective methodology for learning intelligence in a scalable manner, and is di (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
10. Sora currently only accepts text as input, which constrains the precision with which users can specify desired outputs. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
11. Prior video generation models were constrained to fixed resolutions and durations (e.g., 256x256 pixels, exactly 4 seconds), severely limiting the diversity of training data. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
12. Sora uses a diffusion Transformer architecture that combines diffusion-based video generation with a Transformer backbone. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
13. Sora builds on research from both the DALL-E models and the GPT models at OpenAI. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
14. Sora is a generative video model that accepts text prompts and returns visually coherent clips up to one minute long. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")
15. The Sora team views the model as the "GPT-1 moment" for visual generative models, with capabilities expected to improve substantially with scale. (from "No Priors Ep.61 | OpenAI's Sora Leaders Aditya Ramesh, Tim Brooks and Bill Peebles")

## Relationships

## Limitations and Open Questions

## Sources
