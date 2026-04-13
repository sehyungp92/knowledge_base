---
type: entity
title: Agentic AI
entity_type: theory
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- chain_of_thought
- frontier_lab_competition
- generative_media
- model_commoditization_and_open_source
- multi_agent_coordination
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.005421726918722997
staleness: 0.0
status: active
tags: []
---
# Agentic AI

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/chain_of_thought|chain_of_thought]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

AI systems that take sequences of autonomous actions in an environment to accomplish goals, beyond single-turn question answering. Requires tools (search, code execution, browsers), planning, and reasoning capabilities.

## Key Findings

1. Model weights are frozen after training; all users receive the same fixed checkpoint and no further training occurs during inference. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
2. o1 was primarily a technology demonstration rather than a polished or broadly useful product, being mostly good at solving puzzles. (from "How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek")
3. AlphaGo Zero was trained purely through self-play from scratch without any human game data, rediscovering all Go knowledge autonomously. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")
4. Pretraining (imitation learning) initializes a model from random weights and adapts them to imitate large amounts of human-generated data. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
5. In AI there are four distinct layers: semiconductors, foundation models, tooling, and apps. (from "Elad Gil on AI, Crypto, and What’s Next")
6. AlphaGo was initially trained via supervised learning on human amateur go games to predict which moves players would make. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")
7. Reinforcement learning post-training enables models to go beyond imitation and optimize for a reward signal, potentially surpassing human performance. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
8. Chain of thought is the thinking process of language models verbalized using human words and human concepts. (from "How GPT-5 Thinks — OpenAI VP of Research Jerry Tworek")
9. MuZero was motivated by the need to handle real-world tasks where a perfect simulator of the environment is unavailable. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")
10. Reward hacking is a core challenge in RL post-training for language: models exploit weaknesses in imperfect reward models rather than learning the intended behavior. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
11. Alpha Zero generalized AlphaGo Zero's approach to chess, Go, and Shogi using a single algorithm and network structure without game-specific knowledge. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")
12. Current LLMs hallucinate: they can be prompted to produce factually incorrect statements, and achieving 100% factual accuracy remains an unsolved challenge. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
13. Determining reward in language tasks is fundamentally difficult because there is no ground-truth metric for quality of open-ended outputs such as poems or summaries. (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
14. The two-phase training process (pretraining/imitation learning followed by reinforcement learning) used for AlphaGo and AlphaStar is essentially the same process used to train current large language m (from "Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals")
15. AlphaGo combined deep neural networks with Monte Carlo Tree Search to plan and evaluate move sequences. (from "Are We Misreading the AI Exponential? Julian Schrittwieser on Move 37 & Scaling RL (Anthropic)")

## Known Limitations

- Enterprise demand for agentic AI structurally outstrips customers' ability to productionize agents without significant forward-deployed engineering support — self-serve deployment is not viable at sca (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
