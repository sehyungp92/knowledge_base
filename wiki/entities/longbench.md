---
type: entity
title: LongBench
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- context_engineering
- hallucination_and_reliability
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- retrieval_augmented_generation
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0049865602511126785
staleness: 0.0
status: active
tags: []
---
# LongBench

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/context_engineering|context_engineering]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/scaling_laws|scaling_laws]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Mixed-environment benchmark for long-context understanding covering 21 tasks and 4,750 samples.

## Key Findings

1. DIFF Transformer produces significantly lower top activation values in attention logits and hidden states compared to Transformer, with top-1 attention logit outlier of 38.8 vs 318.0. (from "Differential Transformer")
2. The differential attention mechanism computes attention scores as the difference between two separate softmax attention maps, which cancels noise and promotes sparse attention patterns. (from "Differential Transformer")
3. The learnable scalar λ in differential attention is re-parameterized as the difference of two exponentials to synchronize learning dynamics. (from "Differential Transformer")
4. A 6.8B-size DIFF Transformer achieves a validation loss comparable to an 11B-size Transformer, requiring only 62.2% of parameters. (from "Differential Transformer")
5. DIFF Transformer trained on 160B tokens achieves comparable language modeling performance to Transformer trained on 251B tokens, consuming only 63.7% of training tokens. (from "Differential Transformer")
6. DIFF Transformer outperforms Transformer in many-shot in-context learning with improvement in average accuracy ranging from 5.2% to 21.6% across four classification datasets. (from "Differential Transformer")
7. Softmax attention has quadratic compute and linear memory complexity with respect to sequence length, which is a fundamental bottleneck. (from "Log-Linear Attention")
8. The log-linear extension adds less than 3% additional parameters for Mamba-2 and less than 0.4% for Gated DeltaNet. (from "Log-Linear Attention")
9. DIFF Transformer requires only about 65% of model size or training tokens needed by Transformer to achieve comparable language modeling performance. (from "Differential Transformer")
10. The differential attention mechanism computes attention scores as the difference between two separate softmax attention maps, canceling common-mode noise. (from "Differential Transformer")
11. Log-linear attention is a general framework applicable on top of existing linear attention variants. (from "Log-Linear Attention")
12. Log-linear attention replaces the fixed-size hidden state with a logarithmically growing set of hidden states, achieving O(T log T) compute and O(log T) memory complexity. (from "Log-Linear Attention")
13. Log-linear attention uses Fenwick-tree decomposition to partition the token prefix into logarithmically many buckets of exponentially increasing size, creating an inductive bias where recent tokens ha (from "Log-Linear Attention")
14. Linear attention enables linear-time, constant-memory sequence modeling by replacing the softmax kernel with a linear kernel, allowing reformulation as a linear RNN with matrix-valued hidden states. (from "Log-Linear Attention")
15. A 6.8B DIFF Transformer achieves validation loss comparable to an 11B Transformer, requiring only 62.2% of parameters. (from "Differential Transformer")

## Relationships

## Limitations and Open Questions

## Sources
