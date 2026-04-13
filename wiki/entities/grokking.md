---
type: entity
title: grokking
entity_type: theory
theme_ids:
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- alignment_and_safety
- alignment_methods
- continual_learning
- finetuning_and_distillation
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- software_engineering_agents
- synthetic_data_generation
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.008791967935193016
staleness: 0.0
status: active
tags: []
---
# grokking

**Type:** theory
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Phenomenon where generalization occurs suddenly after training loss has saturated, heavily dependent on regularization methods like weight decay. Distinguished from post-saturation generalization in 1-shot RLVR, which is driven primarily by policy gradient loss.

## Key Findings

1. Post-saturation generalization occurs in 1-shot RLVR: training accuracy saturates near 100% rapidly but test performance continues improving for hundreds or thousands of additional steps (from "Reinforcement Learning for Reasoning in Large Language Models with One Training Example")
2. Tulu 3 uses a three-stage post-training pipeline: Supervised Fine-Tuning (SFT), Direct Preference Optimization (DPO), and Reinforcement Learning from Verifiable Rewards (RLVR). (from "Everything You Wanted to Know About LLM Post-Training, with Nathan Lambert of Allen Institute for AI")
3. RLVR with a single training example can achieve performance comparable to using datasets with thousands of examples for mathematical reasoning (from "Reinforcement Learning for Reasoning in Large Language Models with One Training Example")
4. The AI Scientist produces each paper at a cost of less than $15. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
5. The AI Scientist can produce a full research paper at a cost of less than $15 per paper. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
6. The AI Scientist uses chain-of-thought and self-reflection techniques via LLM agent frameworks to improve decision-making quality. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
7. Aider, the LLM-based coding assistant used by The AI Scientist, achieves a success rate of 18.9% on the SWE Bench benchmark with frontier models. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
8. GPT-style language models have an approximate memorization capacity of 3.6 bits per parameter (from "How much do language models memorize?")
9. The automated reviewer achieves near-human performance, achieving 65% vs 66% balanced accuracy when evaluated on ICLR 2022 OpenReview data. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
10. RLVR with two examples slightly exceeds the performance of using 1.2k examples and matches the performance of using 7.5k MATH training examples (from "Reinforcement Learning for Reasoning in Large Language Models with One Training Example")
11. In 1-shot RLVR, even after overfitting (training responses become multilingual gibberish), test responses remain interpretable and maintain high accuracy (from "Reinforcement Learning for Reasoning in Large Language Models with One Training Example")
12. The AI Scientist uses chain-of-thought and self-reflection to improve decision-making during idea generation. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
13. 1-shot RLVR effectiveness has been confirmed across multiple base models including Qwen2.5-Math-1.5B, Qwen2.5-Math-7B, Llama3.2-3B-Instruct, and DeepSeek-R1-Distill-Qwen-1.5B (from "Reinforcement Learning for Reasoning in Large Language Models with One Training Example")
14. Aider achieves a 18.9% success rate on SWE Bench with frontier models. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")
15. The AI Scientist's automated reviewer achieves near-human performance, with 65% balanced accuracy compared to 66% for human reviewers on ICLR 2022 OpenReview data. (from "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery")

## Relationships

## Limitations and Open Questions

## Sources
