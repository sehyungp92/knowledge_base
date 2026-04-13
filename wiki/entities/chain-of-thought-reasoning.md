---
type: entity
title: chain-of-thought reasoning
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- alignment_methods
- audio_and_speech_models
- chain_of_thought
- computer_use_and_gui_agents
- finetuning_and_distillation
- frontier_lab_competition
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- spatial_and_3d_intelligence
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
- vertical_ai_and_saas_disruption
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 17
sources_since_update: 0
update_count: 1
influence_score: 0.019332848922277664
staleness: 0.0
status: active
tags: []
---
# chain-of-thought reasoning

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A technique where language models generate explicit intermediate reasoning steps before producing a final answer, improving performance on complex tasks. o1 extends this by training the model end-to-end via RL on long reasoning chains.

## Key Findings

1. Physical Intelligence aims to build general-purpose robotic foundation models capable of controlling any robot to perform any task. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
2. Physical Intelligence's current robots can fold laundry and clean kitchens in new environments. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
3. Physical Intelligence has demonstrated robots capable of folding laundry and cleaning up kitchens in new homes. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
4. Robot arm costs have decreased from $400,000 (PR2, circa 2014) to $30,000 to approximately $3,000 at Physical Intelligence today, and could be reduced further. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
5. The π0 model is a vision-language model adapted for motor control, incorporating both a vision encoder and an action expert (action decoder). (from "Fully autonomous robots are much closer than you think – Sergey Levine")
6. Physical Intelligence robots demonstrated unprogrammed error recovery behaviors such as righting a tipped shopping bag and discarding an extra accidentally-grasped T-shirt. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
7. Physical Intelligence aims to build general-purpose robotic foundation models capable of controlling any robot to perform any task. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
8. The ultimate goal for home robots is not single-task execution but sustained autonomous operation over months, handling a full household agenda with minimal prompting. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
9. The π0 model is a vision-language model adapted for motor control, combining a vision encoder with an action expert (action decoder), analogous to a visual cortex plus motor cortex. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
10. Moravec's paradox holds that in AI the cognitively 'easy' physical tasks (perception, manipulation) are actually the hardest engineering problems, while tasks humans find cognitively demanding (chess, (from "Fully autonomous robots are much closer than you think – Sergey Levine")
11. Physical Intelligence considers its current work as the very early beginning—basic building blocks rather than the end goal. (from "Fully autonomous robots are much closer than you think – Sergey Levine")
12. Robot arm cost has decreased from $400,000 (PR2 in 2014) to $30,000 (Berkeley research arms) to approximately $3,000 (current Physical Intelligence arms). (from "Fully autonomous robots are much closer than you think – Sergey Levine")
13. When and how to perform search in ReSearch is steered by previous text-based thinking, and search results influence subsequent text-based thinking. (from "ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning")
14. All baselines compared against ReSearch in Figure 1 are built upon Qwen2.5-32B-Instruct. (from "ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning")
15. ReSearch is trained from scratch without any labeled data on reasoning chains. (from "ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning")

## Capabilities

- Latent thought models can perform chain-of-thought reasoning in a latent space Z (rather than the observed text space X), and this consistently outperforms raw-text-space CoT at inference time on math (maturity: research_only)

## Known Limitations

- No extended thinking / chain-of-thought reasoning: Kimi K2 is explicitly a 'reflex-grade model without long thinking', lacking the test-time compute scaling that thinking models provide (severity: significant, trajectory: improving)
- TTT applied to chain-of-thought reasoning traces is explicitly left unexplored, leaving open whether TTT could compound gains from intermediate reasoning steps. (severity: minor, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
