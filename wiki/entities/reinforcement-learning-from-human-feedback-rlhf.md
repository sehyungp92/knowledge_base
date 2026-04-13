---
type: entity
title: Reinforcement Learning from Human Feedback (RLHF)
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- finetuning_and_distillation
- frontier_lab_competition
- knowledge_and_memory
- mathematical_and_formal_reasoning
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
- scaling_laws
- search_and_tree_reasoning
- startup_and_investment
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 14
sources_since_update: 0
update_count: 1
influence_score: 0.004468296155692219
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning from Human Feedback (RLHF)

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/startup_and_investment|startup_and_investment]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

An RL approach where rewards are provided by a neural reward model trained on human-annotated preference pairs, primarily used for aligning model outputs with human values.

## Key Findings

1. The first TPO optimization step yields the largest performance improvement, with subsequent steps being comparatively less impactful. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
2. TPO requires a foundational level of instruction-following proficiency in the policy model; weaker models like Llama-3.1-8B-Instruct fail to maintain alignment under TPO. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
3. After only a few TPO steps, the unaligned Llama-3.1-70B-SFT model can surpass the aligned Llama-3.1-70B-Instruct model. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
4. TPO can be viewed as a synthesis of parallel sampling and sequential revision from the perspective of test-time scaling. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
5. Mistral-Small-Instruct-2409 (22B parameters) with TPO achieves an LC score of 53.4% on AlpacaEval 2 and WR of 72.2% on Arena-Hard, comparable to GPT-4-Turbo. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
6. TPO-D2-N5 (2 iterations, 5 samples per iteration, 15 total samples) surpasses Best-of-N sampling with 30 and 60 samples, achieving average win-rates of 65.2% and 57.5% respectively. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
7. TPO scales efficiently with both search width (number of candidates per iteration) and depth (number of iterations) during inference. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
8. Test-Time Preference Optimization (TPO) aligns LLM outputs with human preferences during inference without updating model parameters. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
9. TPO performs gradient descent in textual form: computing a textual loss, deriving a textual gradient, and updating a textual variable, analogous to numerical gradient descent. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
10. In TPO, the highest- and lowest-scoring responses among candidates are designated as 'chosen' and 'rejected' responses to compute the textual loss. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
11. TPO searches for an optimal contextual parameter rather than optimal model parameters, re-allocating probability mass with model weights fixed. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
12. After only two TPO steps, an unaligned SFT model can match or exceed the performance of fully aligned models trained on tens of thousands or millions of samples. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
13. Increasing search width from 5 to 20 in TPO consistently boosts performance before plateauing, and smaller width can compensate via additional revision rounds. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
14. With TPO using Llama-3.1-Tulu-3-8B-RM, Llama-3.1-70B-SFT surpasses Llama-3.1-70B-Instruct on all metrics except LC on AlpacaEval 2, including a WR of 70.5 on Arena-Hard that exceeds Llama-3.1-405B-Ins (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")
15. TPO is implemented on top of the TextGrad framework, adapting its gradient computation and variable optimization prompts while customizing the loss calculation prompt for preference optimization. (from "Test-Time Preference Optimization: On-the-Fly Alignment via Iterative Textual Feedback")

## Relationships

## Limitations and Open Questions

## Sources
