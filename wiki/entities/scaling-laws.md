---
type: entity
title: Scaling Laws
entity_type: theory
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- compute_and_hardware
- computer_use_and_gui_agents
- context_engineering
- continual_learning
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- interpretability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- model_architecture
- model_behavior_analysis
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- spatial_and_3d_intelligence
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 20
sources_since_update: 0
update_count: 1
influence_score: 0.030069820845165792
staleness: 0.0
status: active
tags: []
---
# Scaling Laws

**Type:** theory
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Empirical relationships linking data volume and model size to performance improvements in language models, demonstrated over the past decade. Considered the key unlock for world models if architectures can leverage visual data at comparable scale.

## Key Findings

1. Nvidia describes itself as an accelerated compute company, not a GPU company (from "Ep18. Jensen Recap - Competitive Moat, X.AI, Smart Assistant | BG2 w/ Bill Gurley & Brad Gerstner")
2. ChatGPT launched in November 2022 (from "Sarah Guo and Elad Gil: The Future of AI Investing")
3. Jensen Huang views the data center as the unit of compute (from "Ep18. Jensen Recap - Competitive Moat, X.AI, Smart Assistant | BG2 w/ Bill Gurley & Brad Gerstner")
4. ChatGPT was released on November 30, 2022, marking the beginning of the current AI era (from "Superintelligence, Bubbles And Big Bets: AI Investing in 2024 | Matt Turck & Aman Kabeer, FirstMark")
5. Conviction was founded in October 2022, focused on AI-native software companies (from "Sarah Guo and Elad Gil: The Future of AI Investing")
6. DeepSeek's MoE architecture uses both shared experts (run on every token, dense) and routed experts (only top-K activated per token, sparse). (from "How DeepSeek Changes the LLM Story")
7. AlphaGo Zero was trained purely through self-play from scratch without any human game data, rediscovering all Go knowledge autonomously. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")
8. DeepSeek V3 has 671 billion total parameters but only 37 billion are activated for any given token due to its sparse mixture of experts architecture. (from "How DeepSeek Changes the LLM Story")
9. For the 3B LLaMA model, TPT mid-training improves AIME24 performance from 5.8% to 18.6%, a 3x increase. (from "Thinking Augmented Pre-training")
10. For a 3B parameter model, TPT improves post-training performance by over 10% on several challenging reasoning benchmarks. (from "Thinking Augmented Pre-training")
11. Pretraining (imitation learning) initializes a model from random weights and adapts them to imitate large amounts of human-generated data. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
12. Model weights are frozen after training; all users receive the same fixed checkpoint and no further training occurs during inference. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
13. Total LLM pre-training tokens have scaled from 300B for GPT-3 to over 10T tokens within a few years. (from "Thinking Augmented Pre-training")
14. o1 was primarily a technology demonstration rather than a polished or broadly useful product, being mostly good at solving puzzles. (from "How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek")
15. TPT requires no human annotation and imposes no constraints on document structure, making it universally applicable to any text data. (from "Thinking Augmented Pre-training")

## Capabilities

- Ultra-sparse MoE architecture with sparsity 48 (384 total experts, 8 active per token) achieving 1.69x FLOP reduction over sparsity 8 at equivalent validation loss, validated by empirical sparsity sca (maturity: narrow_production)

## Relationships

## Limitations and Open Questions

## Sources
