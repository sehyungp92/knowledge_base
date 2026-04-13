---
type: entity
title: Sequence Parallelism
entity_type: method
theme_ids:
- adaptive_computation
- ai_market_dynamics
- audio_and_speech_models
- compute_and_hardware
- creative_content_generation
- generative_media
- long_context_and_attention
- model_architecture
- multimodal_models
- pretraining_and_scaling
- scaling_laws
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0017643319567204137
staleness: 0.0
status: active
tags: []
---
# Sequence Parallelism

Sequence parallelism is a distributed training strategy that shards the sequence dimension of transformer activations across multiple devices, addressing the fundamental memory bottleneck that makes scaling context length prohibitively expensive on individual accelerators. Its most significant instantiation — Ring Attention — effectively decouples context length from per-device memory constraints, enabling training on sequences that were previously computationally infeasible and opening a new axis of scaling orthogonal to model size.

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/scaling_laws|scaling_laws]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

The core problem sequence parallelism addresses is well-established: transformer self-attention carries memory cost quadratic in sequence length, and modern accelerators — typically providing less than 100GB of high-bandwidth memory, with limited prospects for significant expansion due to physical and manufacturing constraints — cannot hold long-context activations for large models. Tensor parallelism offers only partial relief, reducing some activation memory but leaving other components intact. Prior sequence parallelism approaches introduced non-overlapped communication overheads that imposed real throughput penalties.

Ring Attention, described in Ring Attention with Blockwise Transformers for Near-Infinite Context, resolves the communication overhead problem through a key architectural insight: the inner key-value block loop in blockwise attention is permutation invariant — because self-attention accumulates contributions from all key-value pairs and the result is independent of ordering, blocks can be processed in any sequence. This property allows Ring Attention to pipeline the communication of key-value blocks between hosts with the blockwise attention computation itself. When block computation time exceeds block transfer time, the two processes fully overlap, yielding zero additional communication overhead compared to standard transformers.

The memory profile is correspondingly clean. The total maximum activation size per Ring Attention layer is `6bch` bytes — where `b` is batch size, `c` is block size, and `h` is hidden size — completely independent of input sequence length `s`. Combined with Blockwise Parallel Transformers (BPT), which independently reduce transformer layer activation memory to `2bsh` bytes, the result is a system where context length scales linearly with device count rather than being bounded by any single device's HBM.

## Key Findings

### What Ring Attention Achieves

The empirical results are striking. On TPUv4-1024, Ring Attention enables a 512x increase in context size for 3B and 7B models, reaching training sequences of over 16 million and 8 million tokens respectively. For large models in the 7B–65B range, context sizes over 4 million tokens are achievable with negligible MFU overhead compared to baseline BPT. The headline figure is that Ring Attention enables training sequences more than 500 times longer than prior memory-efficient state-of-the-art transformers. At the time of publication, this stood in dramatic contrast to production context windows: GPT-3.5 at 16K tokens, GPT-4 at 32K, MosaicML MPT at 65K, and Anthropic Claude at 100K.

Context scaling also improves downstream task performance, not merely theoretical capacity. On the ExoRL benchmark, an agent transformer augmented with Ring Attention — which could scale to 128 trajectories instead of being limited to 32 — achieved a total average return of 113.66 versus 111.13 for the BPT-only baseline, demonstrating that longer context translates into measurable capability gains.

### The Overlap Condition

The zero-overhead guarantee is conditional. For communication to be fully overlapped with computation, the block size `c` must satisfy `c ≥ F/B`, where `F` is FLOPS per host and `B` is inter-host bandwidth. In practice, this imposes minimum viable sequence lengths that vary significantly by interconnect technology: for A100 GPUs connected via NVLink, approximately 6,200 tokens per device; for A100 GPUs connected via InfiniBand, approximately 149,000 tokens per device. The InfiniBand figure is particularly significant — clusters using commodity networking must commit to very long per-device sequences before the overlap guarantee activates, constraining where Ring Attention is practical without modification.

## Limitations and Open Questions

The sequence length floor for full overlap efficiency is a genuine constraint. On slower interconnects, the "zero overhead" property degrades gracefully rather than catastrophically, but the practical minimum of ~149K tokens per device on InfiniBand means the technique is not uniformly deployable across hardware configurations.

Sequence parallelism addresses the memory bottleneck but does not reduce the computational cost of attention — quadratic FLOP complexity remains. For very long sequences, compute rather than memory may become the binding constraint, particularly as efficient attention approximations (sparse, linear, or structured) continue to mature. How sequence parallelism interacts with these approaches — whether they compose cleanly or require rearchitecting — remains an active question.

The permutation invariance property that enables Ring Attention applies to standard self-attention. Architectural variants with positional dependencies in the attention computation, or attention mechanisms where ordering of key-value processing matters, may not admit the same ring-based decomposition without modification.

Finally, the relationship between sequence parallelism and topology-aware decoding strategies (as explored in Tree Attention) and large-scale multimodal contexts (as in Movie Gen) points toward an open engineering frontier: how to optimally distribute not just uniform text sequences but heterogeneous multimodal token streams across network topologies with non-uniform bandwidth.

## Relationships

Ring Attention is the primary realization of sequence parallelism in the literature covered here, and its properties are entirely derived from the blockwise computation framework of Blockwise Parallel Transformers. The technique is positioned as complementary to tensor parallelism and data parallelism — addressing the specific failure mode (per-device HBM limits on sequence length) that those strategies leave unresolved.

Sequence parallelism is directly relevant to any domain where long context is not merely useful but structurally necessary: multi-document reasoning, long video understanding (see [[themes/video_and_world_models|Video and World Models]]), extended agent trajectories, and genomic or scientific sequence modeling. The 500x context extension figure suggests that many tasks previously treated as requiring architectural innovation (e.g., recurrent state for long-range dependencies) may instead be solvable with standard transformers given sufficient distributed memory.

## Sources
