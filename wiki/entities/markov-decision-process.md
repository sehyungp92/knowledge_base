---
type: entity
title: Markov Decision Process
entity_type: theory
theme_ids:
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- finetuning_and_distillation
- generative_media
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- synthetic_data_generation
- tool_use_and_agent_protocols
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.001021772674129628
staleness: 0.0
status: active
tags: []
---
# Markov Decision Process

> The Markov Decision Process (MDP) is the foundational mathematical framework for formalizing sequential decision-making under uncertainty, and has become the standard substrate for modeling agentic AI tasks — from robotic manipulation to multi-turn tool use. Its tuple of states, actions, transitions, and rewards provides the precise language needed to train, evaluate, and reason about agents that must act across time to achieve goals.

**Type:** theory
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

The MDP provides a formal grammar for any problem where an agent must take a sequence of actions in an environment, observe consequences, and optimize for long-term cumulative reward. Concretely, it is defined by a state space, action space, transition dynamics, observation function, reward signal, initial state distribution, and discount factor. The agent's goal is to learn a policy — a mapping from states to actions — that maximizes expected discounted return.

What makes the MDP so pervasive is its generality: the same formalism applies whether the "environment" is a robot arm, a web browser, or a multi-model tool-calling pipeline. In recent work on LLM-based agents, the MDP framing has been extended to incorporate real-world concerns that classical RL ignores — user preferences, monetary costs, inference latency, and output correctness — making it a richer model of what it actually means to deploy an intelligent agent responsibly.

## Key Findings

### MDP as the Lingua Franca for Agentic Tool Use

ToolOrchestra offers the most explicit recent instantiation: its agentic task is formalized as an MDP $\mathcal{M} = (\mathcal{U}, \mathcal{S}, \mathcal{A}, \mathcal{O}, \mathcal{T}, \mathcal{Z}, r, \rho, \gamma)$, where $\mathcal{U}$ encodes user preferences alongside the standard state and action spaces. This extension signals a maturation of the framework — the reward function is no longer just about task success, but explicitly balances three objectives: correctness of the final outcome, efficiency in resource usage, and alignment with user preferences. This tripartite reward design reflects a growing recognition that optimizing for accuracy alone produces agents that are costly or misaligned with how real users want to work.

The rollout structure in ToolOrchestra follows a reasoning–action–observation loop capped at 50 turns, a concrete instantiation of the MDP's sequential structure. The result is an Orchestrator-8B model that achieves 37.1% on Humanity's Last Exam — outperforming GPT-5 (35.1%) — while being 2.5× more computationally efficient, and surpassing GPT-5 on τ2-Bench and FRAMES at roughly 30% of the cost. These results demonstrate that MDP-grounded end-to-end RL, with well-designed reward shaping, can produce policies that dominate larger models on both capability and efficiency axes simultaneously.

### Reward Design as the Critical Lever

The MDP formalism does not prescribe how rewards are structured — it only requires that they exist. How reward functions are designed turns out to be decisive for what agents learn. DreamGym uses a sparse, outcome-based reward: $r = 1$ only at the final step upon task success, $r = 0$ everywhere else. This binary delayed signal is maximally principled — it avoids reward hacking and credit assignment artifacts from shaped intermediates — but it also makes the learning problem harder, since the agent receives no gradient signal during the trajectory.

This tension between reward sparsity and learning tractability is a central open problem in RL-based agent training. DreamGym's framing acknowledges the broader challenge: RL training for LLM agents remains difficult due to costly rollouts, limited task diversity, unreliable reward signals, and infrastructure complexity. The MDP is the right language for describing the problem, but it does not automatically solve the practical obstacles that make applying it at scale expensive.

### MDP in Embodied and Vision-Language-Action Settings

The MDP framework extends naturally to robotic manipulation, where state spaces are continuous, observations are high-dimensional, and action spaces may be discrete tokens or continuous motor commands. UniVLA operates in exactly this regime, autoregressively modeling vision, language, and action signals as discrete token sequences within a unified shared vocabulary. The policy operates over an implicit MDP where states are visual scenes, actions are tokenized motor commands, and rewards come from task success in simulation or real hardware.

UniVLA's results are state-of-the-art across multiple benchmarks: an average sequence length of 4.41 on CALVIN ABC→D (exceeding Seer-Large's 4.28), 95.5% average success on LIBERO (vs. π0-FAST's 85.5%), and a jump from 42.7% to 69.8% on SimplerEnv-WidowX. Notably, incorporating world model post-training — which requires no action annotations and trains on large-scale video data — substantially improves long-horizon policy learning, lifting LIBERO-Long from 69.0% to 94.0%. This points to an important insight: the transition dynamics component of the MDP can be learned implicitly via video prediction, decoupling world knowledge acquisition from action supervision.

## Limitations and Open Questions

The MDP formalism assumes that the Markov property holds — that the current state captures all information relevant to future rewards. In practice, LLM-based agents operate over conversation histories that are neither fully observable nor cleanly stationary, making the MDP an approximation. Partially observable MDPs (POMDPs) are more accurate but computationally harder; most current systems use the MDP fiction as a useful simplification.

The reward signal remains the deepest unsolved problem. Correctness rewards require automated verifiers (which may themselves be wrong or gameable), user preference rewards require preference models (which may be misspecified), and cost/latency rewards introduce non-stationarities as infrastructure changes. DreamGym's acknowledgment that reward signals are "unreliable" is an honest concession that the MDP machinery is only as good as its weakest component.

Finally, the MDP assumes a fixed environment, but in multi-agent settings — including orchestration architectures like ToolOrchestra, where the tools themselves include other LLMs — the environment is non-stationary and other agents are simultaneously adapting. Extending the single-agent MDP to handle strategic interdependencies is an active frontier, bridging into game theory and multi-agent RL.

## Relationships

The MDP is the theoretical substrate underlying most of [[themes/reinforcement_learning|reinforcement_learning]] and [[themes/policy_optimization|policy_optimization]]. Its reward-maximization framing directly shapes [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]] and [[themes/post_training_methods|post_training_methods]]. In embodied settings it connects to [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], and [[themes/vision_language_action_models|vision_language_action_models]] — all of which require sequential decision policies. The tool-use instantiation ties to [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]] and [[themes/agent_systems|agent_systems]], while the world model extension bridges to [[themes/video_and_world_models|video_and_world_models]].

Key source connections: ToolOrchestra (explicit MDP formalization for tool-use agents), DreamGym (outcome-based sparse reward design), UniVLA (MDP instantiation in vision-language-action modeling).

## Sources
