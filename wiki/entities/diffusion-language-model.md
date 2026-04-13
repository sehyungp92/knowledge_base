---
type: entity
title: Diffusion language model
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- chain_of_thought
- knowledge_and_memory
- latent_reasoning
- model_architecture
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- retrieval_augmented_generation
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.001481364859863312
staleness: 0.0
status: active
tags: []
---
# Diffusion language model

> A class of generative architectures that produce tokens in parallel via iterative denoising rather than left-to-right autoregression. Diffusion language models have attracted significant interest as a path toward faster inference and richer bidirectional context, but they face a fundamental tension between parallelism and quality that has so far limited their practical competitiveness with autoregressive models on sequential reasoning tasks.

**Type:** method
**Themes:** [[themes/model_architecture|Model Architecture]], [[themes/transformer_alternatives|Transformer Alternatives]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/pretraining_and_scaling|Pretraining & Scaling]]

## Overview

Diffusion language models generate text by starting from a fully masked sequence and progressively unmasking tokens across multiple denoising steps. The appeal is straightforward: because all tokens in a segment can be sampled in parallel, the architecture sidesteps the strict left-to-right dependency of autoregressive (AR) models and, in principle, can saturate hardware far more efficiently. In practice, however, the quality of parallel decoding degrades sharply as more tokens are decoded per step. As shown with Dream-7B, accuracy on GSM8K drops by roughly 10% when moving from one to two tokens decoded per denoising step, illustrating that the quality-parallelism tradeoff is not merely gradual but steep (from TiDAR: Think in Diffusion, Talk in Autoregression).

A second structural limitation concerns sequential tool use. Because diffusion models draft tokens from a marginal distribution without a strict causal ordering, they cannot naturally integrate interleaved tool calls (search queries, code execution) whose outputs must condition subsequent generation. This stands in contrast to the "Think, Search, Act" primitive stack that defines the current generation of reasoning models (from Thinking, Searching, and Acting). The inability to condition on intermediate external results is not a tuning problem; it is architecturally intrinsic to fully parallel decoding.

## The Hybrid Response: TiDAR

The most direct answer to these limitations in the literature is the sequence-level hybrid architecture introduced by TiDAR (Think in Diffusion, Talk in Autoregression). TiDAR separates the generation process into two phases along a single forward pass: a *thinking* phase that drafts candidate tokens via masked diffusion with bidirectional attention, and a *talking* phase that commits final output tokens autoregressively with causal attention. The two phases share a single model, using a structured causal-bidirectional hybrid attention mask over the input sequence.

This design yields several practical advantages over prior speculative decoding approaches. Because the draft model is the base model itself rather than a smaller auxiliary network, draft capacity is high. Drafting is fully parallelized across the diffusion segment. And, unlike traditional diffusion models, TiDAR supports exact KV caching: the prefix (AR section) KV cache is preserved while rejected token caches are evicted, so the efficiency gains do not come at the cost of recomputation overhead.

TiDAR also introduces a training simplification: rather than randomly masking tokens in the diffusion section, all tokens in that section are set to mask tokens. This eliminates masking schedule complexity, enables denser diffusion loss during training, and allows one-step diffusion inference. The models are trained via continual pretraining (50B tokens for the 1.5B model; 150B tokens for the 8B model) on NVIDIA H100s.

## Empirical Results

At the 1.5B scale, TiDAR achieves lossless quality relative to its AR counterpart while delivering a 4.71x relative throughput speedup, averaging 7.45 tokens per neural function evaluation (NFE) across coding and math benchmarks. At 8B, the speedup reaches 5.91x with minimal quality loss and an average of 8.25 tokens per NFE. These figures represent the state of the art for hybrid diffusion-AR architectures as of early 2025.

The throughput gains come specifically from the pre-drafting strategy, inspired by Apple's MTP work: TiDAR pre-drafts next-step tokens in parallel conditioned on all possible outcomes of the current-step rejection sampling. This means that regardless of how many tokens are accepted in the current step, corresponding drafts for the next step are already available, eliminating sequential draft latency.

## Open Questions and Limitations

The fundamental parallelism-quality tradeoff in masked diffusion models remains unresolved. TiDAR's hybrid architecture works around it by confining diffusion to the speculative drafting phase and using autoregression for committed outputs, but this means diffusion is not doing the generation work per se; it is doing the speculative work. Whether diffusion can ever match AR quality at equivalent token budgets on open-ended, sequential reasoning tasks is an open question the literature has not yet settled.

The sequential tool use constraint remains unaddressed by TiDAR and the broader diffusion LM literature. As reasoning models increasingly depend on interleaved search and code execution (the three-primitive architecture described in Thinking, Searching, and Acting), fully parallel decoding architectures face a structural disadvantage that hybrids only partially mitigate.

Finally, TiDAR's training data requirements (50-150B tokens of continual pretraining) suggest that the approach is not cheap to retrofit onto existing AR checkpoints. Whether the efficiency gains justify the pretraining cost relative to standard speculative decoding with a small draft model depends heavily on deployment context.

## Relationships

TiDAR is directly related to [[themes/transformer_alternatives|Transformer Alternatives]] insofar as diffusion LMs represent a distinct architectural paradigm from both standard transformers and SSM-based models. The quality-parallelism tradeoff connects to [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]: parallelism that degrades quality is antithetical to the inference-scaling paradigm where quality at test time is the primary currency. The tool-use limitation links directly to [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], where sequential conditioning on external results is a first-class requirement.

## Key Findings

## Limitations and Open Questions

## Sources
