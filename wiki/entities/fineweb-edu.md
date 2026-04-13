---
type: entity
title: FineWeb-Edu
entity_type: dataset
theme_ids:
- adaptive_computation
- ai_market_dynamics
- chain_of_thought
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- latent_reasoning
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 9
sources_since_update: 0
update_count: 1
influence_score: 0.009168538656930472
staleness: 0.0
status: active
tags: []
---
# FineWeb-Edu

**Type:** dataset
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

A large-scale web-crawl-based educational dataset with a dedicated quality classifier. In this paper's LOO analysis, its removal caused the largest performance degradation across all capability domains, attributed to its broad cross-domain coverage acting as binding glue between heterogeneous knowledge domains.

## Key Findings

1. The surprise metric is decomposed into past surprise (momentum) and momentary surprise to prevent information loss after large surprising events. (from "Titans: Learning to Memorize at Test Time")
2. The neural memory module defines surprise as the gradient of the neural network with respect to its input — the larger the gradient, the more surprising and thus more memorable the input. (from "Titans: Learning to Memorize at Test Time")
3. Memory retrieval from the neural memory module is performed via a standard forward pass without weight update. (from "Titans: Learning to Memorize at Test Time")
4. The neural memory module training is equivalent to optimizing a meta neural network with mini-batch gradient descent, momentum, and weight decay. (from "Titans: Learning to Memorize at Test Time")
5. The surprise metric with momentum is mathematically equivalent to gradient descent with momentum, where the momentum term acts as a memory of surprise across sequence positions. (from "Titans: Learning to Memorize at Test Time")
6. At test time in Titans, the neural long-term memory module continues learning by updating its weights, while persistent memory is fixed and attention performs in-context learning. (from "Titans: Learning to Memorize at Test Time")
7. All major current LLMs (Llama, Mistral, Bloom, Falcon, Gemini, GPT, Claude) share the same underlying architecture: a transformer-based, decoder-only language model pretrained to predict the next toke (from "Large Concept Models: Language Modeling in a Sentence Representation Space")
8. SSMs possess O(1) memory and linear compute cost during autoregressive generation due to their recurrent formulation. (from "The Zamba2 Suite: Technical Report")
9. The SONAR embedding space supports text input and output in 200 languages, speech input in 76 languages, and speech output in English. (from "Large Concept Models: Language Modeling in a Sentence Representation Space")
10. Transformers have quadratic time and memory complexity with respect to context length, limiting their applicability to long sequences (from "Titans: Learning to Memorize at Test Time")
11. 4-bit quantization of Zamba2-2.7B reduces its memory footprint from 5.38 GB to 1.55 GB; adding 4-bit quantized LoRA parameters yields a final model at 1.7 GB. (from "The Zamba2 Suite: Technical Report")
12. Zamba2-1.2B and Zamba2-2.7B were trained for 3 trillion tokens; Zamba2-7.4B was trained for 2 trillion tokens due to compute limitations. (from "The Zamba2 Suite: Technical Report")
13. MobileLLM-R1-950M achieves an AIME score of 15.5, dramatically outperforming OLMo-2-1.48B (0.6) and SmolLM-2-1.7B (0.3) despite having fewer parameters. (from "MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes")
14. Pretraining the 7.4B model required two-way tensor parallelism across 16 nodes of 8xH100 SXM GPUs with 3.2 Tbps Infiniband, while smaller models only required data parallelism. (from "The Zamba2 Suite: Technical Report")
15. All major LLMs (Llama, Mistral, Bloom, Falcon, Gemini, GPT, Claude) share the same underlying architecture: a transformer-based, decoder-only language model pretrained to predict the next token. (from "Large Concept Models: Language Modeling in a Sentence Representation Space")

## Relationships

## Limitations and Open Questions

## Sources
