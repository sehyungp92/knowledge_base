---
type: entity
title: Knowledge Distillation
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- alignment_and_safety
- chain_of_thought
- compute_and_hardware
- continual_learning
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- software_engineering_agents
- startup_and_investment
- transformer_alternatives
- vc_and_startup_ecosystem
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.009317572197420066
staleness: 0.0
status: active
tags: []
---
# Knowledge Distillation

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]]

## Overview

A training technique where a smaller student model (SLM specialist) is trained to mimic the outputs of a larger teacher model (generalist LLM) on a task-specific dataset, transferring nuanced capabilities.

## Key Findings

1. Ours-72B achieves 13/30 on AIME2024 compared to O1-preview's 12/30, with fewer average output tokens (8016 vs 9083). (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
2. Distillation-based O1 replication still shows a noticeable performance gap compared to O1-mini (13/30 vs 21/30 on AIME2024), indicating incomplete replication of O1-level capabilities. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
3. O1-preview achieves 85.5% on MATH500 with an average of 1501 output tokens, while the distilled 72B model achieves 87.2% with 2235 average output tokens. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
4. The distilled 72B model achieves 87.2% on MATH500, surpassing O1-preview's 85.5%, under comparable inference cost constraints. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
5. O1-mini achieves 21/30 on AIME2024 with an average of 9903 output tokens, significantly outperforming the distilled 72B model. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
6. The base model for mathematical distillation experiments is Qwen2.5-Math-72B, selected for its exceptional foundational capability in mathematical reasoning. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
7. A 72B base model fine-tuned on tens of thousands of O1-distilled long-thought chains outperforms O1-preview on AIME with minimal technical complexity. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
8. Qwen2.5-Math-72B was selected as the base model for distillation experiments due to its exceptional foundational capability in mathematical reasoning. (from "O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson?")
9. Distillation using forward KL divergence on logits only (without LM cross-entropy loss) is the retraining strategy used for accuracy recovery after pruning. (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
10. Llama 3.1-Minitron-4B models perform favorably compared to their teacher (Llama 3.1 8B) using 150x fewer training tokens (94B vs. 15T). (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
11. MN-Minitron-8B outperforms Llama 3.1 8B on common benchmarks while using 40x fewer training tokens (380B vs. 15T). (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
12. The Minitron compression approach uses 32 NVIDIA DGX H100 nodes for distillation-based retraining. (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
13. Structured pruning with knowledge distillation requires an order of magnitude fewer training tokens than training from scratch to reach state-of-the-art accuracy: MN-Minitron-8B uses 380B tokens vs. 1 (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
14. Width-pruned Llama 3.1-Minitron-4B achieves MMLU of 60.5% vs. 58.7% for the depth-pruned variant. (from "LLM Pruning and Distillation in Practice: The Minitron Approach")
15. Structured pruning combined with knowledge distillation can produce small language models using significantly fewer training tokens and compute resources compared to training from scratch. (from "LLM Pruning and Distillation in Practice: The Minitron Approach")

## Relationships

## Limitations and Open Questions

## Sources
