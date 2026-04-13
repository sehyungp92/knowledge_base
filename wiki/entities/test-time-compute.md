---
type: entity
title: Test-time compute
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- context_engineering
- evaluation_and_benchmarks
- frontier_lab_competition
- knowledge_and_memory
- latent_reasoning
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- software_engineering_agents
- spatial_and_3d_intelligence
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 14
sources_since_update: 0
update_count: 1
influence_score: 0.006180740783690335
staleness: 0.0
status: active
tags: []
---
# Test-time compute

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/context_engineering|context_engineering]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Inference-time computation that scales model capabilities, boosted as a byproduct of scaling RL training compute in reasoning models like o3.

## Key Findings

1. Sleep-time compute is implemented by prompting a model to draw inferences and rewrite context in a way that may be useful at test-time, producing a re-represented context c′. (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
2. Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the primary constraint and the new frontier is reliable interaction with the external world. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
3. o3 was trained with tools through reinforcement learning, teaching it not just how to use tools but to reason about when to use them. (from "OpenAI's o3: Over-optimization is back and weirder than ever")
4. R1-Zero uses a simple binary rule-based reward: the model receives reward if it answers correctly and no reward if it answers incorrectly. (from "Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5")
5. DeepSeek R1-Zero is trained using pure reinforcement learning with no human preference data, no human demonstration data, no supervised fine-tuning, and no reward model. (from "Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5")
6. DeepSeek R1 uses no Monte Carlo Tree Search, no structured search algorithm, and no process reward model. (from "Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5")
7. Sleep-time compute provides a pareto improvement over the test-time compute vs. accuracy curve, meaning the same accuracy is achievable with less test-time compute or higher accuracy at the same budge (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
8. Scaling sleep-time compute can increase accuracy by up to 13% on Stateful GSM-Symbolic. (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
9. Scaling sleep-time compute can increase accuracy by up to 18% on Stateful AIME. (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
10. Multi-Query GSM-Symbolic was generated synthetically by using o3-mini to produce additional question-answer pairs from existing GSM-Symbolic context-question pairs. (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
11. Over-optimization occurs when the optimizer is stronger than the environment or reward function it uses to learn, causing it to find bugs or lapses in the training context and produce unusual or negat (from "OpenAI's o3: Over-optimization is back and weirder than ever")
12. TRM with self-attention and 7M parameters outperforms HRM with 27M parameters on all tested benchmarks, achieving 85.3% vs 74.5% on Maze-Hard, 44.6% vs 40.3% on ARC-AGI-1, and 7.8% vs 5.0% on ARC-AGI- (from "Less is More: Recursive Reasoning with Tiny Networks")
13. Sleep-time compute reduces the test-time compute needed to achieve the same accuracy by approximately 5× on Stateful GSM-Symbolic and Stateful AIME. (from "Sleep-time Compute: Beyond Inference Scaling at Test-time")
14. DeepSeek V3 is a mixture of experts architecture with 671 billion total parameters and 37 billion parameters active at inference time. (from "Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5")
15. DeepSeek R1-Zero is trained using pure reinforcement learning with no human preference data, no human demonstration data, no supervised fine-tuning, and no reward model. (from "Emergency Pod: Reinforcement Learning Works! Reflecting on Chinese Models DeepSeek-R1 and Kimi k1.5")

## Capabilities

- Test-time compute scaling (o1, o3) unlocks capabilities that larger base models cannot achieve by allowing models to 'think longer' at inference (maturity: narrow_production)
- Open-source MoE LLM (32B activated / 1T total params) achieving 65.8% SWE-bench Verified single-attempt agentic coding, 71.6% with parallel test-time compute sampling, and 47.3% on SWE-bench Multiling (maturity: narrow_production)
- Test-time compute scaling via evolutionary search with LLM mutation sustains meaningful capability gains well beyond what repeated sampling achieves, reaching regimes of genuine scientific discovery (maturity: demo)
- Test-time compute scaling (extended reasoning) demonstrably improves healthcare response quality, particularly on completeness — suggesting reasoning models will continue to push the health performanc (maturity: demo)
- Log-linear inference-time scaling for biological sequence design: increasing beam search width predictably improves chromatin accessibility design quality, demonstrating test-time compute scaling in b (maturity: research_only)

## Known Limitations

- No extended thinking / chain-of-thought reasoning: Kimi K2 is explicitly a 'reflex-grade model without long thinking', lacking the test-time compute scaling that thinking models provide (severity: significant, trajectory: improving)
- RULER has only been tested as a training-time reward signal; its use as a runtime test-time compute mechanism for improving agent reliability remains unvalidated (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
