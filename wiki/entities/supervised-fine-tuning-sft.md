---
type: entity
title: Supervised Fine-Tuning (SFT)
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- alignment_and_safety
- alignment_methods
- chain_of_thought
- finetuning_and_distillation
- hallucination_and_reliability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- medical_and_biology_ai
- multi_agent_coordination
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
- scientific_and_medical_ai
- search_and_tree_reasoning
- startup_and_investment
- synthetic_data_generation
- test_time_compute_scaling
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 9
sources_since_update: 0
update_count: 1
influence_score: 0.005617140454851896
staleness: 0.0
status: active
tags: []
---
# Supervised Fine-Tuning (SFT)

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/startup_and_investment|startup_and_investment]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_models|vision_language_models]]

## Overview

A fundamental LLM alignment approach that minimizes cross-entropy loss between model output and ground-truth labeled data.

## Key Findings

1. LLaVA-CoT decomposes answer generation into four structured reasoning stages: summary, caption, reasoning, and conclusion (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
2. InternLM-XComposer2.5-Reward was used as the reward model to judge generation quality during test-time scaling experiments (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
3. Ours-72B achieves 13/30 on AIME2024 compared to O1-preview's 12/30, with fewer average output tokens (8016 vs 9083). (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
4. O1-preview achieves 85.5% on MATH500 with an average of 1501 output tokens, while the distilled 72B model achieves 87.2% with 2235 average output tokens. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
5. O1-mini achieves 21/30 on AIME2024 with an average of 9903 output tokens, significantly outperforming the distilled 72B model. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
6. With test-time scaling via SWIRES, LLaVA-CoT improves from 62.4% to 65.5% average across six benchmarks (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
7. On the MATH dataset, DeepSeek-Math-7b enhanced with Q* achieves 55.4% accuracy, surpassing Gemini Ultra (4-shot) at 53.2%. (from "Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning")
8. Q* formalizes multi-step LLM reasoning as a Markov Decision Process where state is the concatenation of input prompt and reasoning steps, and action is the next reasoning step. (from "Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning")
9. Distillation-based O1 replication still shows a noticeable performance gap compared to O1-mini (13/30 vs 21/30 on AIME2024), indicating incomplete replication of O1-level capabilities. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
10. The base model for mathematical distillation experiments is Qwen2.5-Math-72B, selected for its exceptional foundational capability in mathematical reasoning. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
11. The distilled 72B model achieves 87.2% on MATH500, surpassing O1-preview's 85.5%, under comparable inference cost constraints. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
12. Q* proposes three approaches to estimate optimal Q-values: offline reinforcement learning (Fitted Q-iteration), learning from rollout (best sequence), and completion with a stronger LLM. (from "Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning")
13. On GSM8K, Q* with PRM+QVM achieves 80.8% accuracy on Llama-2-7b fine-tuned with MetaMath, surpassing ChatGPT-turbo (77.7%). (from "Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning")
14. SWIRES retraces to a previous reasoning stage when all candidate responses at the current stage fall below a reward threshold (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
15. The validation dataset for RFT training had no overlap in correct genes with the training dataset, ensuring the model must generalize rather than memorize. (from "Reinforcement Fine-Tuning—12 Days of OpenAI: Day 2")

## Known Limitations

- Supervised fine-tuning (SFT) on small domain-specific medical datasets degrades conversational quality and management plan appropriateness, particularly for dermatology and ECG tasks — making SFT coun (severity: significant, trajectory: stable)

## Relationships

## Limitations and Open Questions

## Sources
