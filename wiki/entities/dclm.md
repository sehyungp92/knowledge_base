---
type: entity
title: DCLM
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- continual_learning
- finetuning_and_distillation
- knowledge_and_memory
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- representation_learning
- scaling_laws
- software_engineering_agents
- synthetic_data_generation
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.005464881852662503
staleness: 0.0
status: active
tags: []
---
# DCLM

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/representation_learning|representation_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

A large-scale pretraining corpus (Li et al., 2024) used as the background corpus for IDF computation in sparse memory finetuning; 1000 random batches are sampled to represent generic pretraining knowledge to preserve.

## Key Findings

1. 4-bit quantization of Zamba2-2.7B reduces its memory footprint from 5.38 GB to 1.55 GB; adding 4-bit quantized LoRA parameters yields a final model at 1.7 GB. (from "The Zamba2 Suite: Technical Report")
2. TF-IDF ranking is used to identify memory indices that are specifically important for a new input relative to a background corpus, borrowing the technique from document retrieval (from "Continual Learning via Sparse Memory Finetuning")
3. LoRA finetuning on new facts causes a 71% drop in NaturalQuestions F1 score (from "Continual Learning via Sparse Memory Finetuning")
4. Pretraining the 7.4B model required two-way tensor parallelism across 16 nodes of 8xH100 SXM GPUs with 3.2 Tbps Infiniband, while smaller models only required data parallelism. (from "The Zamba2 Suite: Technical Report")
5. AU-Net applies a contracting path that pools bytes into words, then word pairs, then up to four-word chunks, forming a multi-stage hierarchy with skip connections that expand back to fine-grained reso (from "From Bytes to Ideas: Language Modeling with Autoregressive U-Nets")
6. SSMs possess O(1) memory and linear compute cost during autoregressive generation due to their recurrent formulation. (from "The Zamba2 Suite: Technical Report")
7. Full finetuning on new facts causes an 89% drop in NaturalQuestions F1 score (from "Continual Learning via Sparse Memory Finetuning")
8. Sparse memory finetuning yields only an 11% drop in NaturalQuestions F1 while achieving the same level of new knowledge acquisition as full finetuning and LoRA (from "Continual Learning via Sparse Memory Finetuning")
9. Zamba2-1.2B and Zamba2-2.7B were trained for 3 trillion tokens; Zamba2-7.4B was trained for 2 trillion tokens due to compute limitations. (from "The Zamba2 Suite: Technical Report")
10. Sparse memory finetuning updates only the top t memory slots that are highly accessed on a batch relative to a background corpus using TF-IDF ranking (from "Continual Learning via Sparse Memory Finetuning")
11. Memory layers replace feedforward network layers with a trainable parametric memory pool queried via an attention-like mechanism (from "Continual Learning via Sparse Memory Finetuning")
12. A token sequence is on average 4.56 times shorter than its byte sequence when using the LLaMa 3 tokenizer on the DCLM corpus. (from "From Bytes to Ideas: Language Modeling with Autoregressive U-Nets")
13. Levels of performance previously thought to require 100B+ parameter models are now achievable with models of fewer than 10B parameters. (from "The Zamba2 Suite: Technical Report")
14. Naively finetuning a memory layer model (without TF-IDF-based slot selection) still causes catastrophic forgetting (from "Continual Learning via Sparse Memory Finetuning")
15. Sparse memory finetuning Pareto dominates full finetuning and LoRA across the learning–forgetting tradeoff frontier (from "Continual Learning via Sparse Memory Finetuning")

## Known Limitations

- MMLU-STEM performance across BoLT iterations fell within noise floor (< 28%), revealing that extended math-focused pretraining actively degrades general STEM knowledge; general domain NLL on DCLM corp (severity: significant, trajectory: worsening)

## Relationships

## Limitations and Open Questions

## Sources
