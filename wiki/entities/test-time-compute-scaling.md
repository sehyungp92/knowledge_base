---
type: entity
title: Test-Time Compute Scaling
entity_type: method
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_for_scientific_discovery
- ai_governance
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- benchmark_design
- chain_of_thought
- compute_and_hardware
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- interpretability
- knowledge_and_memory
- latent_reasoning
- mathematical_and_formal_reasoning
- medical_and_biology_ai
- model_architecture
- model_behavior_analysis
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
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- spatial_and_3d_intelligence
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 18
sources_since_update: 0
update_count: 1
influence_score: 0.013252037770648163
staleness: 0.0
status: active
tags: []
---
# Test-Time Compute Scaling

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

A scaling law introduced by RLVR that allows controlling model capability as a function of inference-time computation by generating longer reasoning traces and increasing 'thinking time'.

## Key Findings

1. Humans achieve approximately 85% accuracy on ARC challenges, while the best LLMs achieve only 18%. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
2. 42% of the Deep architecture's solutions came from generations 2–4, demonstrating the value of iterative refinement over single-generation generation. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
3. ARC-AGI-1 is now saturating — a large ensemble of low-compute Kaggle solutions can score 81% on the private eval. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
4. The author achieved 53.6% accuracy on ARC-AGI-Pub using Claude Sonnet 3.5, setting a new public record. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
5. Efficiency (compute cost) is now a required metric when reporting performance on ARC-AGI, not just raw score. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
6. The method generates Python functions rather than output grids directly because functions can be executed and verified for correctness whereas grids cannot. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")
7. o3 still fails on some very easy tasks, indicating fundamental differences with human intelligence, and the author does not consider o3 to be AGI. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
8. The high-efficiency configuration used 6 samples per task; the low-efficiency configuration used 1024 samples, representing approximately 172x more compute. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
9. ARC-AGI-1 took 4 years to progress from 0% with GPT-3 in 2020 to only 5% with GPT-4o in 2024. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
10. A high-compute (172x) o3 configuration scored 87.5% on the Semi-Private Evaluation set. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
11. o3 scored 75.7% on the ARC-AGI-1 Semi-Private Evaluation set at the high-efficiency ($10k) compute limit. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
12. A human can solve ARC-AGI tasks for approximately $5 per task, while o3-preview requires approximately $27 per task in low-compute mode. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
13. OpenAI trained the o3 tested by ARC Prize on 75% of the Public Training set. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
14. o3 scored 82.8% on the Public Eval set at high-efficiency and 91.5% at low-efficiency. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
15. The previous state-of-the-art on ARC-AGI-Pub was 43%, achieved by Ryan Greenblatt. (from "How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute")

## Capabilities

- Test-time compute scaling (o1, o3) unlocks capabilities that larger base models cannot achieve by allowing models to 'think longer' at inference (maturity: narrow_production)
- Test-time compute scaling via evolutionary search with LLM mutation sustains meaningful capability gains well beyond what repeated sampling achieves, reaching regimes of genuine scientific discovery (maturity: demo)
- Test-time compute scaling (extended reasoning) demonstrably improves healthcare response quality, particularly on completeness — suggesting reasoning models will continue to push the health performanc (maturity: demo)
- Log-linear inference-time scaling for biological sequence design: increasing beam search width predictably improves chromatin accessibility design quality, demonstrating test-time compute scaling in b (maturity: research_only)
- Test-time compute scaling applied to CUDA kernel optimization: evolutionary search over increasing kernel proposals yields monotonically improving runtime performance (maturity: research_only)

## Known Limitations

- No extended thinking / chain-of-thought reasoning: Kimi K2 is explicitly a 'reflex-grade model without long thinking', lacking the test-time compute scaling that thinking models provide (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
