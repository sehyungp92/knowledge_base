---
type: entity
title: Inference-Time Compute Scaling
entity_type: theory
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- ai_market_dynamics
- chain_of_thought
- finetuning_and_distillation
- frontier_lab_competition
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.005205195290760065
staleness: 0.0
status: active
tags: []
---
# Inference-Time Compute Scaling

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

The principle that allocating more computation at inference time (test-time compute) improves model performance on complex reasoning tasks.

## Key Findings

1. Marco-o1 is the first work to investigate large reasoning models on machine translation tasks, exploring inference-time scaling in the multilingual domain. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
2. Marco-o1 demonstrates o1-like reasoning characteristics but its performance still falls short of a fully realized o1 model. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
3. Token-level search in MCTS is currently impractical due to computational cost and difficulty designing an effective reward model at that granularity. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
4. Applying MCTS with ORM and PRM reward modeling is planned to reduce randomness and improve performance over the current confidence-score-based reward. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
5. Marco-o1-MCTS (step) achieves 90.40% accuracy on MGSM-En, a +6.17% improvement over the base Qwen2-7B-Instruct model. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
6. Using confidence score as the MCTS reward signal introduces significant randomness into tree search results. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
7. MCTS in Marco-o1 uses confidence scores derived from softmax-applied log probabilities of the top-5 alternative tokens to guide tree search toward more confident reasoning chains. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
8. MCTS-enhanced models show advantage over CoT-only fine-tuning at Test@1, but all models converge to similar high accuracy (~99%) at Test@32 on MGSM-En. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
9. No definitive conclusion can be drawn about which MCTS action granularity (step vs mini-step) is superior; results are inconsistent across English and Chinese subsets. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
10. A reflection mechanism triggered by the phrase 'Wait! Maybe I made some mistakes! I need to rethink from scratch.' causes the model to self-reflect and correctly solves approximately half of initially (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
11. The Marco-o1 CoT synthetic dataset of 10,000 samples was itself generated using MCTS to formulate complex reasoning pathways. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
12. Marco-o1 is built on Qwen2-7B-Instruct via full-parameter SFT using a combination of filtered Open-O1 CoT dataset, synthetic Marco-o1 CoT dataset, and Marco Instruction dataset totaling 60,266 samples (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
13. CoT fine-tuning on English data decreases Chinese MGSM performance compared to the base model (71.20% vs 76.80%), suggesting language-specific fine-tuning data is necessary for cross-lingual transfer. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
14. Using step-level actions is coarser and may cause the model to overlook nuanced reasoning paths; mini-steps of 32 or 64 tokens expand the solution space with finer granularity. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")
15. Reinforcement learning techniques are being explored to fine-tune the decision-making processes of Marco-o1 for complex real-world tasks. (from "Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions")

## Capabilities

- Inference-time compute scaling (increasing tokens sampled per base pair from 1 to 60) measurably improves DNA sequence design quality as measured by AUROC against desired chromatin accessibility patte (maturity: research_only)

## Relationships

## Limitations and Open Questions

## Sources
