---
type: entity
title: Tensor Parallelism
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- audio_and_speech_models
- chain_of_thought
- computer_use_and_gui_agents
- creative_content_generation
- generative_media
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- multimodal_models
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- scaling_laws
- transformer_alternatives
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.006547897391220098
staleness: 0.0
status: active
tags: []
---
# Tensor Parallelism

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/creative_content_generation|creative_content_generation]], [[themes/generative_media|generative_media]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/scaling_laws|scaling_laws]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A model parallelism technique that partitions model weights across multiple GPUs. For Lumine's 7B model with 4 KV heads, deployed on 4 NVIDIA H20 GPUs with TP degree 4 (one KV head per GPU), yielding a remarkable inference speedup.

## Key Findings

1. For A100 GPUs connected via NVLink, the minimum sequence length per device to enable overlap is approximately 6,200 tokens; for A100 GPUs connected via InfiniBand, the requirement is approximately 149 (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
2. At time of publication, leading LLM context windows were: GPT-3.5 at 16K tokens, GPT-4 at 32K tokens, MosaicML MPT at 65K tokens, and Anthropic Claude at 100K tokens. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
3. Ring Attention overlaps communication of key-value blocks between hosts with blockwise attention computation, achieving zero additional communication overhead when block computation time exceeds block (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
4. Ring Attention total maximum activation size per layer is 6bch bytes, independent of input sequence length s, where b is batch size, c is block size, and h is hidden size. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
5. Tensor parallelism can only reduce parts of activation memory and sequence parallelism introduces significant communication overhead that cannot be fully overlapped with computation. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
6. AT + Ring Attention outperforms AT with BPT on the ExoRL benchmark, achieving total average return of 113.66 vs 111.13, by scaling to 128 trajectories instead of 32. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
7. Transformer self-attention has memory cost quadratic in input sequence length, making it challenging to scale to longer sequences. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
8. Ring Attention enables training sequences more than 500 times longer than prior memory-efficient state-of-the-art transformers. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
9. Ring Attention enables context length to scale linearly with the number of devices while maintaining performance, eliminating the memory bottleneck imposed by individual devices. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
10. Contemporary GPUs and TPUs typically have less than 100GB of high-bandwidth memory, and prospects for significant HBM expansion are hindered by physical limitations and high manufacturing costs. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
11. The minimum block size required to overlap communication with computation is c >= F/B, where F is FLOPS per host and B is inter-host bandwidth. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
12. Blockwise Parallel Transformers (BPT) reduce memory overhead of a transformer layer to 2bsh bytes of activation, independent of improvements from Ring Attention. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
13. On TPUv4-1024, Ring Attention enables a 512x increase in context size for 3B and 7B models, allowing training sequences of over 16 million and 8 million tokens respectively. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
14. Ring Attention enables training large models (7B–65B) with context sizes over 4 million tokens with negligible MFU overhead compared to baseline blockwise parallel transformers. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")
15. Ring Attention's permutation invariance of the inner key-value block loop enables any ordering of blockwise computations, which is the key property exploited for ring-based communication. (from "Ring Attention with Blockwise Transformers for Near-Infinite Context")

## Known Limitations

- Kernel is bound to a single CUDA device via CUDAGuard — no multi-GPU tensor parallelism or model parallelism support, constraining scalability for large models that require distributed inference (severity: significant, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
