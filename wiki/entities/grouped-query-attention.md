---
type: entity
title: Grouped Query Attention
entity_type: method
theme_ids:
- adaptive_computation
- continual_learning
- finetuning_and_distillation
- generative_media
- model_architecture
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- transformer_alternatives
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0014225227472662535
staleness: 0.0
status: active
tags: []
---
# Grouped Query Attention

Grouped Query Attention (GQA) is an architectural efficiency technique for transformer-based models that reduces the memory and computational cost of multi-head attention without sacrificing the representational capacity needed for high-quality inference. Rather than maintaining a distinct key-value (KV) head for every query head — as in standard multi-head attention — GQA groups query heads so that each group shares a single pair of key and value heads. This compresses the KV cache proportionally to the number of groups, making GQA one of the most practically impactful architectural choices in scaling modern language and world models to long contexts and fast inference.

**Type:** method
**Themes:** [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/video_and_world_models|Video and World Models]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

The KV cache is a fundamental bottleneck in transformer inference: at every decoding step, keys and values for all previous tokens and all heads must be stored in memory. In standard multi-head attention (MHA), this grows linearly with both sequence length and head count. Multi-query attention (MQA) collapses this to a single KV head shared across all queries, reducing memory dramatically but at some quality cost. GQA occupies the middle ground — by grouping queries and assigning one KV pair per group, it recovers most of MQA's efficiency while preserving quality much closer to MHA.

In practice, GQA has become the default choice in frontier model architectures. The Qwen3 Technical Report confirms its adoption across the dense and MoE Qwen3 model families, where it is combined with QK-Norm for training stability (replacing the QKV-bias used in Qwen2) and paired with a three-stage pre-training curriculum over approximately 36 trillion tokens. GQA also appears in world model contexts: in Dreamer 4, it is applied to all layers of the dynamics model to reduce KV cache footprint and accelerate autoregressive rollout, where inference speed directly affects planning quality.

## Key Findings

The impact of GQA is best understood not in isolation but through the broader architectural packages it enables. In the Qwen3 family, the combination of GQA with improved data pipelines and MoE routing produces a striking efficiency curve: Qwen3-8B achieves performance comparable to Qwen2.5-14B, and Qwen3-32B-Base outperforms Qwen2.5-72B-Base on 10 of 15 evaluation benchmarks despite having fewer than half the parameters. GQA is one structural ingredient enabling this parameter efficiency — by keeping inference cost low, it allows the training budget to be redirected toward data quality and scale rather than compensating for inference overhead.

The MoE models extend this pattern further. Qwen3 MoE base models match their dense counterparts while activating only 1/5 of parameters per token (128 total experts, 8 activated, no shared experts). The flagship Qwen3-235B-A22B, which outperforms DeepSeek-V3-Base on 14 of 15 benchmarks with roughly 1/3 the total parameter count, relies on GQA as part of the architecture that makes its inference economics viable. These results show that KV cache compression through GQA is not merely a deployment convenience — it is a lever that reshapes what is achievable at a given compute budget.

The integration of GQA with reasoning-oriented post-training is also notable. Qwen3's unified thinking/non-thinking model demonstrates that compute-efficient architectures can support variable inference regimes: the thinking budget mechanism allows users to allocate more or fewer tokens to chain-of-thought, and GQA keeps the per-step memory cost predictable across both regimes. Evidence shows that scaling the thinking budget produces consistent performance improvements across task types — an affordance that would be harder to provide if the KV cache were the binding constraint.

Beyond language models, the Training Agents Inside of Scalable World Models source illustrates GQA's role in embodied AI: applying it to all dynamics model transformer layers in Dreamer 4 is a pragmatic choice driven by the need to run many parallel rollouts during planning. In this setting, inference speed is not just an operational concern but a direct determinant of agent capability.

## Limitations and Open Questions

GQA introduces a design tradeoff that has not been fully resolved: the optimal group size is task- and scale-dependent, and there is limited principled guidance for choosing it. Smaller group counts approach MQA and risk quality degradation on tasks requiring fine-grained attention differentiation; larger group counts approach MHA and recover less memory. The Qwen3 and Dreamer 4 implementations do not publish ablations on group size choice, making it difficult to disentangle GQA's contribution from other simultaneous architectural changes.

A deeper open question is whether GQA's efficiency gains at inference time translate into equivalent gains during training, or whether the training dynamics differ in ways that require compensatory changes (such as QK-Norm in Qwen3). The removal of QKV-bias alongside the introduction of QK-Norm suggests that architectural combinations involving GQA require careful co-design rather than being drop-in replacements. Whether the stability benefits of QK-Norm are specific to GQA or would be needed in MHA at similar scale is not yet clear from public evidence.

Finally, as context lengths extend — Qwen3's long-context stage reaches 32,768 tokens — the absolute size of even a compressed KV cache grows substantially. GQA defers rather than eliminates this scaling problem. Whether it remains sufficient at context lengths of hundreds of thousands of tokens, or whether architectural alternatives such as linear attention or state-space mechanisms become necessary, remains an active area without settled answers.

## Relationships

GQA sits at the intersection of [[themes/model_architecture|model architecture]] and [[themes/test_time_compute_scaling|test-time compute scaling]], linking directly to work on inference efficiency and long-context serving. It is architecturally adjacent to multi-query attention and to sliding-window or sparse attention patterns discussed in [[themes/transformer_alternatives|transformer alternatives]] research. In the Qwen3 context it is bundled with MoE routing, connecting to [[themes/pretraining_and_scaling|pretraining and scaling]] tradeoffs between total and activated parameters. In the Dreamer 4 context it connects to [[themes/video_and_world_models|video and world models]] and [[themes/robotics_and_embodied_ai|robotics and embodied AI]], where inference throughput shapes planning horizon and agent capability.

Sources: Qwen3 Technical Report, Training Agents Inside of Scalable World Models

## Sources
