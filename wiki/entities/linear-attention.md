---
type: entity
title: Linear Attention
entity_type: method
theme_ids:
- agent_memory_systems
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.007714730704357474
staleness: 0.0
status: active
tags: []
---
# Linear Attention

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Attention mechanisms that approximate or replace standard softmax attention to achieve O(N) computational complexity instead of O(N²), enabling processing of very long sequences. Require training from scratch and face parallel training difficulties.

## Key Findings

1. TTT has two loops: an inner loop that trains the hidden state ML model on context via gradient steps (active learning), and an outer loop that trains the overall model for next-token prediction. (from "LLM Attention That Expands At Inference? Test Time Training Explained")
2. TTT (Test Time Training) is a new class of sequence modeling layers where the hidden state is an ML model and its update rule is a step of self-supervised learning. (from "LLM Attention That Expands At Inference? Test Time Training Explained")
3. RNN-inspired methods like Mamba offer linear complexity as an alternative to Transformers. (from "LLM Attention That Expands At Inference? Test Time Training Explained")
4. Transformers suffer from quadratic complexity with respect to context length. (from "LLM Attention That Expands At Inference? Test Time Training Explained")
5. Self-attention has a hidden state that grows with context, making its computational complexity quadratic; TTT and naive RNN both compress context into a fixed-size hidden state, keeping per-token cost (from "LLM Attention That Expands At Inference? Test Time Training Explained")
6. TTT's compression is updated (trained) at every step, allowing the model to dynamically adapt to the current input. (from "LLM Attention That Expands At Inference? Test Time Training Explained")
7. Memory retrieval from the neural memory module is performed via a standard forward pass without weight update. (from "Titans: Learning to Memorize at Test Time")
8. The neural memory module defines surprise as the gradient of the neural network with respect to its input — the larger the gradient, the more surprising and thus more memorable the input. (from "Titans: Learning to Memorize at Test Time")
9. At test time in Titans, the neural long-term memory module continues learning by updating its weights, while persistent memory is fixed and attention performs in-context learning. (from "Titans: Learning to Memorize at Test Time")
10. The surprise metric with momentum is mathematically equivalent to gradient descent with momentum, where the momentum term acts as a memory of surprise across sequence positions. (from "Titans: Learning to Memorize at Test Time")
11. The surprise metric is decomposed into past surprise (momentum) and momentary surprise to prevent information loss after large surprising events. (from "Titans: Learning to Memorize at Test Time")
12. The neural memory module training is equivalent to optimizing a meta neural network with mini-batch gradient descent, momentum, and weight decay. (from "Titans: Learning to Memorize at Test Time")
13. Log-linear attention replaces the fixed-size hidden state with a logarithmically growing set of hidden states, achieving O(T log T) compute and O(log T) memory complexity. (from "Log-Linear Attention")
14. Log-linear attention is a general framework applicable on top of existing linear attention variants. (from "Log-Linear Attention")
15. Log-linear attention uses Fenwick-tree decomposition to partition the token prefix into logarithmically many buckets of exponentially increasing size, creating an inductive bias where recent tokens ha (from "Log-Linear Attention")

## Known Limitations

- Most linear recurrent models (linear attention, RetNet, RWKV variants) lack knowledge transfer between frequency levels—their initial memory states are not meta-learned—limiting their higher-order in- (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
