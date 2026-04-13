---
type: entity
title: Post-training
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- alignment_methods
- compute_and_hardware
- computer_use_and_gui_agents
- finetuning_and_distillation
- frontier_lab_competition
- knowledge_and_memory
- model_commoditization_and_open_source
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- scaling_laws
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.010290643878144488
staleness: 0.0
status: active
tags: []
---
# Post-training

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Training stage after pretraining (including RLHF, RLVR, SFT, etc.) where most current capability gains are being made at leading labs

## Key Findings

1. Tulu 3 uses a three-stage post-training pipeline: Supervised Fine-Tuning (SFT), Direct Preference Optimization (DPO), and Reinforcement Learning from Verifiable Rewards (RLVR). (from "Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI")
2. When users interact with Manus, they only communicate with the executor agent, not the knowledge or planner agents (from "Before you call Manus AI Agent, a GPT Wrapper!")
3. As early as 2017, OpenAI's Dota project demonstrated that pure RL from random initialization (no behavioral cloning) could produce sophisticated, reliable behaviors in neural networks. (from "Greg Brockman on OpenAI's Road to AGI")
4. GPT-5 is the first hybrid model released by OpenAI. (from "Greg Brockman on OpenAI's Road to AGI")
5. Closed labs use human annotators for preference data, while open groups like AI2 use LLM-as-judge because human preference annotation is cost-prohibitive. (from "Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI")
6. Each Manus session creates its own isolated sandbox, completely separate from other user sessions (from "Before you call Manus AI Agent, a GPT Wrapper!")
7. As early as 2017, OpenAI's Dota work demonstrated that pure RL from a randomly initialized neural net — with no behavioral cloning or human demonstrations — could produce sophisticated, correct behavi (from "Greg Brockman on OpenAI's Road to AGI")
8. After training GPT-4, OpenAI immediately identified that the next step required moving to a reinforcement learning / reasoning paradigm to close the reliability gap. (from "Greg Brockman on OpenAI's Road to AGI")
9. LLM-based agents involve many model calls, sometimes with multiple models and multiple prompt configurations (from "Some ideas for what comes next")
10. Error accumulation is a fundamental problem for agentic systems: per-step error rates compound over many steps, making reliability on meaningful tasks effectively impossible. (from "Reflection AI’s Misha Laskin on the AlphaGo Moment for LLMs | Training Data")
11. OpenAI's IMO gold result was achieved by a team of only three people and was not a massive dedicated effort. (from "Greg Brockman on OpenAI's Road to AGI")
12. Reinforcement learning was identified as the mechanism to achieve model reliability — by testing hypotheses in the world and getting feedback. (from "Greg Brockman on OpenAI's Road to AGI")
13. Manus has a multi-agent implementation including a knowledge agent, planner agent, and executor agent (from "Before you call Manus AI Agent, a GPT Wrapper!")
14. Language models were not trained for agency; they were trained for chat interaction and predicting text on the internet. (from "Reflection AI’s Misha Laskin on the AlphaGo Moment for LLMs | Training Data")
15. Each Manus session creates its own isolated sandbox, completely isolated from other user sessions (from "Before you call Manus AI Agent, a GPT Wrapper!")

## Capabilities

- Post-training optimization (fine-tuning, RL, distillation) substantially amplifies capabilities beyond what pretraining alone achieves (maturity: broad_production)
- General RL post-training with self-judging mechanism extending RL beyond verifiable rewards to open-ended tasks (e.g., research report writing): model acts as its own critic using rubric-based feedbac (maturity: demo)
- Physical AI RL post-training improves embodied reasoning accuracy by over 8% on top of SFT, and enables emergent behaviors like rejecting all choices when a question is ambiguous rather than forcing a (maturity: demo)
- Pretrained VLA foundation model achieves high data efficiency in post-training: GR00T N1 with only 10% of task data (42.6% avg success) nearly matches Diffusion Policy trained on full data (46.4%), ou (maturity: narrow_production)
- Neural trajectory co-training during post-training provides consistent additive gains over real-data-only finetuning: +4.2% to +8.8% in simulation and +5.8% on real humanoid across 8 tasks (maturity: demo)

## Known Limitations

- LLMs are largely static after deployment, successfully performing only tasks learned during pre- or post-training but unable to continually acquire new capabilities (severity: blocking, trajectory: improving)
- Model is not a conversational assistant (no SFT stage), restricting it to completion-mode prompts and limiting usability without additional post-training (severity: significant, trajectory: unclear)
- Post-training on narrow task distributions causes catastrophic forgetting of general pre-trained capabilities: a post-trained model that saw only right-hand tasks completely loses the emergent bimanua (severity: significant, trajectory: unclear)
- Novel initial frame generation for real-robot neural trajectory post-training requires manual object pose randomization by human operators — automatic generation via img2img diffusion is left as futur (severity: minor, trajectory: improving)
- Task-specific post-training of Evo 2 could potentially circumvent biosafety data exclusion measures, re-enabling pathogenic human virus design capability (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
