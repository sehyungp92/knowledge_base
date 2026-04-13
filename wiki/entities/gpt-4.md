---
type: entity
title: GPT-4
entity_type: entity
theme_ids:
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- code_and_software_ai
- code_generation
- frontier_lab_competition
- hallucination_and_reliability
- in_context_and_meta_learning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.005369819507940711
staleness: 0.0
status: active
tags: []
---
# GPT-4

**Type:** entity
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

The large language model used as the backbone LLM in DrEureka for reward function generation and domain randomization configuration sampling.

## Key Findings

1. VOYAGER interacts with GPT-4 via blackbox queries, bypassing the need for model parameter fine-tuning. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
2. If VOYAGER gets stuck after 4 rounds of code generation, it queries the curriculum for another task. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
3. Replacing the automatic curriculum with a random one drops the discovered item count by 93%. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
4. VOYAGER unlocks the wooden tool level 15.3× faster, stone tool level 8.5× faster, and iron tool level 6.4× faster than baselines. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
5. VOYAGER's iterative prompting mechanism incorporates three types of feedback: environment feedback, execution errors, and self-verification. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
6. EUREKA conducts 5 independent runs per environment, with 5 iterations per run and 16 samples per iteration, using multiple random restarts for global optimization. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
7. EUREKA generates reward functions that outperform expert human-engineered rewards on 83% of tasks across 29 RL environments, with an average normalized improvement of 52%. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
8. EUREKA requires no task-specific prompts, reward templates, or few-shot examples, unlike prior LLM-based reward design methods such as L2R. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
9. GPT-4 significantly outperforms GPT-3.5 in code generation, obtaining 5.7× more unique items. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
10. GPT-4 API is 15× more expensive than GPT-3.5, representing a significant cost barrier for VOYAGER. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")
11. EUREKA enables a gradient-free in-context RLHF approach that incorporates human textual feedback to steer reward generation without model updating. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
12. Using EUREKA rewards combined with curriculum learning, a simulated Shadow Hand achieves dexterous pen spinning for the first time. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
13. EUREKA takes raw environment source code (without reward code) as context to enable zero-shot generation of executable reward functions. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
14. EUREKA's in-context evolutionary search iteratively refines the best reward from the previous iteration by appending reward reflection and a mutation prompt to the LLM context. (from "Eureka: Human-Level Reward Design via Coding Large Language Models")
15. VOYAGER discovers 63 unique items within 160 prompting iterations, 3.3× more than baselines. (from "Voyager: An Open-Ended Embodied Agent with Large Language Models")

## Capabilities

- Multi-step agentic tool use in constrained customer service domains: 70.6 Tau2-retail, 56.5 Tau2-airline, 65.8 Tau2-telecom (Avg@4), 76.5 AceBench — with Tau2-telecom scores exceeding reported Claude  (maturity: narrow_production)
- State-of-the-art math reasoning among non-thinking models: AIME 2024 69.6 Avg@64, AIME 2025 49.5 Avg@64, MATH-500 97.4%, HMMT 2025 38.8 Avg@32, GPQA-Diamond 75.1 Avg@8 — surpassing GPT-4.1, Claude Son (maturity: narrow_production)
- Small, cheap LLMs now match or exceed the healthcare response quality of earlier frontier models — GPT-4.1 nano outperforms GPT-4o while costing 25x less (maturity: narrow_production)
- SWE-Terminal-Bench leading score of 37.5%, outperforming o3 (30.2%), GPT-4.1 (30.3%), Claude 4 Sonnet (35.5%), and Gemini 2.5 Pro (25.3%) on terminal-based agentic software engineering (maturity: narrow_production)
- Web search tool in API achieving 90% on SimpleQA (GPT-4o search preview) and 88% (GPT-4o mini search preview), with inline citations and source links, available in Responses API and Chat Completions A (maturity: broad_production)

## Known Limitations

- GPT-5 is significantly worse at natural language writing quality than GPT-4.5 and GPT-4o, producing 'LinkedIn-slop' style responses that don't preserve user tone (severity: significant, trajectory: unclear)
- Despite vast implicit knowledge, frontier models like GPT-4 still make basic reasoning errors and lose coherence on long tasks. (severity: significant, trajectory: improving)
- SimpleQA factual accuracy (31.0%) is notably lower than GPT-4.1 (42.3%), suggesting factual grounding and precise retrieval of specific facts remain a relative weakness in the current architecture (severity: significant, trajectory: unclear)
- tau-bench retail evaluations require a superior instruction-following model (GPT-4.1) as the user simulator — the benchmark scores depend on the quality of the synthetic user, not just the agent, mask (severity: significant, trajectory: stable)
- State-of-the-art frontier models without TTT (Claude 3.5 Sonnet: 21%, GPT-4o: 9%, o1 preview: 21%, DeepSeek R1: 20.5%) show extremely poor ARC performance, confirming that scale and RLHF alone do not  (severity: significant, trajectory: stable)

## Relationships

## Limitations and Open Questions

## Sources
