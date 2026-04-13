---
type: source
title: Ring Attention with Blockwise Transformers for Near-Infinite Context
source_id: 01KJVBR6K0DFPR7G3P6NG2AVGN
source_type: paper
authors:
- Hao Liu
- Matei Zaharia
- Pieter Abbeel
published_at: '2023-10-03 00:00:00'
theme_ids:
- adaptive_computation
- long_context_and_attention
- model_architecture
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Ring Attention with Blockwise Transformers for Near-Infinite Context

**Authors:** Hao Liu, Matei Zaharia, Pieter Abbeel
**Published:** 2023-10-03 00:00:00
**Type:** paper

## Analysis

# Ring Attention with Blockwise Transformers for Near-Infinite Context
2023-10-03 · paper · Hao Liu, Matei Zaharia, Pieter Abbeel
https://arxiv.org/pdf/2310.01889

---

### Motivation & Prior Limitations
- Transformer self-attention has memory cost quadratic in sequence length, creating a hard wall on context size that prevents processing of long videos, codebases, scientific data, and multi-modal sequences.
  - Even with a batch size of 1, processing 100 million tokens requires over 1000 GB of memory for a modest model with hidden size 1024 — far exceeding the <100 GB HBM available on contemporary GPUs and TPUs.
  - The state-of-the-art prior to this work, Blockwise Parallel Transformers (BPT), reduced activation memory to 2bsh bytes per layer by computing attention and feedforward block-by-block, but still required storing all layer outputs across the full sequence length, since subsequent self-attention layers require access to all prior outputs — making single-device memory the hard constraint.
- Prior sequence-parallelism approaches using ring topology (e.g., Jacobs et al.) incurred non-overlapped communication overhead because their arithmetic intensity was insufficient to hide transfer latency behind compute, making them infeasible at large context sizes.
  - Tensor parallelism reduces only part of activation memory and is bounded by attention head count; standard sequence parallelism introduces communication overhead that cannot be fully overlapped with computation.

---

### Proposed Approach
- Ring Attention distributes long sequences across multiple devices by assigning each device a fixed-size input block, then circulating key-value blocks through a logical ring of hosts while fully overlapping that inter-device communication with blockwise attention and feedforward computation.
  - Each host is responsible for the outer loop of blockwise attention over its own query block; for the inner loop, it sends its current key-value block to the next host and simultaneously receives key-value blocks from the previous host, exploiting the permutation invariance of the inner KV-block loop to allow arbitrary ordering of partial attention computations.
  - The key insight enabling zero-overhead communication is arithmetic intensity: as long as the compute time for a block (4dc² FLOPs for attention) exceeds the transfer time (4cd bytes), communication is fully hidden. This requires block size c ≥ F/B (FLOPs-to-bandwidth ratio), which is approximately 1K tokens for TPUs and NVLink-connected GPUs, and ~25K for InfiniBand-connected GPUs.
- Ring Attention builds directly on BPT's blockwise computation but adds the ring communication primitive, replacing the single-device memory bottleneck with a distributed one: per-device activation memory becomes 6bch bytes (six blocks: one query, two current KV, two incoming KV, one output), entirely independent of total sequence length s.
  - The approach is architecture-agnostic (evaluated on LLaMA) and composable with existing parallelism strategies (FSDP, tensor parallelism); the implementation requires only a collective permute operation (jax.lax.ppermute) wrapping existing memory-efficient attention kernels.

---

### Results & Capabilities
- Ring Attention achieves context lengths that scale linearly with device count, enabling training sequences up to device-count times longer than the prior state-of-the-art BPT, with zero added communication or computation overhead.
  - On 32× A100 GPUs, Ring Attention supports over 1 million tokens context for a 7B model — a 32× improvement over BPT's 128K.
  - On TPUv4-1024, Ring Attention enables 8 million tokens context for a 7B model and 2 million tokens for a 30B model — a 512× and 256× improvement over BPT, respectively, with training of sequences exceeding 100 million tokens demonstrated without any approximation to exact attention.
- Model FLOP utilization (MFU) is maintained at competitive levels relative to BPT despite the dramatically larger context, with only a predictable and modest reduction attributable to the higher proportion of self-attention FLOPs (which have lower MFU than feedforward).
  - On 32× A100, Ring Attention trains a 13B model at 2048K context with negligible MFU degradation compared to BPT at 64K context.
- In reinforcement learning, applying Ring Attention to the Agent Transformer (AT) on ExoRL allows scaling from 32 to 128 trajectories (each 4000 tokens), which was OOM for all prior baselines; AT+Ring Attention achieves a total average return of 113.66 across six tasks versus 111.13 for AT+BPT at 32 trajectories.
- A LLaMA-13B model finetuned with Ring Attention to 512K context on 32× A100 GPUs maintains high retrieval accuracy on the long-range line-retrieval benchmark at context lengths where GPT-3.5-turbo-16K, Vicuna-16B-16K, and Claude-2-100K all fail.

---

### Implications
- Ring Attention eliminates the per-device memory wall as the binding constraint on context length, replacing it with a device-count-scalable distributed memory budget — fundamentally decoupling context length from hardware generation and enabling a practical path to near-infinite context for exact (non-approximate) attention.
- The architecture is immediately composable with FSDP and tensor parallelism, meaning existing large-scale training infrastructure can adopt Ring Attention incrementally without re-engineering the full training stack.
- Extending exact attention to millions of tokens opens qualitatively new application classes: long-video and audio-language models, in-context reinforcement learning over extended trial-and-error histories, full-codebase comprehension, and processing of scientific sequences (e.g., genomics) that were previously intractable even with approximate methods.
- The demonstration that ring-topology communication can be fully overlapped with blockwise computation — a result requiring only a FLOPs/bandwidth ratio condition — suggests the pattern is broadly portable to future ha

## Key Claims

1. Transformer self-attention has memory cost quadratic in input sequence length, making it challenging to scale to longer sequences.
2. Ring Attention enables context length to scale linearly with the number of devices while maintaining performance, eliminating the memory bottleneck imposed by individual devices.
3. Ring Attention enables training sequences more than 500 times longer than prior memory-efficient state-of-the-art transformers.
4. Contemporary GPUs and TPUs typically have less than 100GB of high-bandwidth memory, and prospects for significant HBM expansion are hindered by physical limitations and high manufacturing costs.
5. Ring Attention overlaps communication of key-value blocks between hosts with blockwise attention computation, achieving zero additional communication overhead when block computation time exceeds block
6. Ring Attention total maximum activation size per layer is 6bch bytes, independent of input sequence length s, where b is batch size, c is block size, and h is hidden size.
7. The minimum block size required to overlap communication with computation is c >= F/B, where F is FLOPS per host and B is inter-host bandwidth.
8. For A100 GPUs connected via NVLink, the minimum sequence length per device to enable overlap is approximately 6,200 tokens; for A100 GPUs connected via InfiniBand, the requirement is approximately 149
9. Blockwise Parallel Transformers (BPT) reduce memory overhead of a transformer layer to 2bsh bytes of activation, independent of improvements from Ring Attention.
10. Prior ring-topology sequence parallelism for self-attention incurred non-overlapped communication overheads, making it infeasible for large context sizes.

## Capabilities

- Ring Attention enables exact (no-approximation) self-attention over sequences scaling linearly with device count — demonstrated at 16M+ tokens (7B model, TPUv4-1024) and 1M+ tokens (7B model, 32x A100), up to 500x longer than prior memory-efficient state-of-the-art
- LLaMA-13B finetuned to 512K context window on 32 A100 GPUs maintains high retrieval accuracy on the long-range line retrieval benchmark, outperforming GPT-3.5-turbo-16K, Vicuna-16B-16K, and Claude-2-100K at long contexts
- Ring Attention applied to Transformer-based RL (Agent Transformer) enables conditioning on 128 trajectories (vs prior maximum of 32) by scaling context, improving total average ExoRL return from 111.13 to 113.66 across six tasks
- Training large models (7B–65B parameters) at context lengths over 4M tokens with negligible MFU overhead compared to baseline memory-efficient transformers, on TPUv4-1024 hardware

## Limitations

- GPUs connected via InfiniBand (slower interconnect) require a minimum sequence length of ~149K tokens per device for zero-overhead operation — roughly 24x stricter than NVLink or TPU — making Ring Attention impractical on commodity distributed GPU clusters at modest context lengths
- Ring Attention incurs lower model FLOP utilization (MFU) than baseline transformers at equivalent sequence lengths because the larger context disproportionately increases self-attention FLOPs relative to feedforward, and self-attention has inherently lower MFU
- Memory cost per device still scales with block size (6bch bytes), meaning context length ultimately scales with the total number of devices — very long contexts (tens of millions of tokens) require hundreds to thousands of accelerators, making this inaccessible outside large-scale research infrastru
- Cloud compute budget constraints limited LLM finetuning experiments to 512K context even though the method supports millions of tokens — indicating that practical use at extreme context lengths is prohibitively expensive with current infrastructure
- The zero-overhead guarantee breaks if hardware interconnect becomes a bottleneck — when block transfer time exceeds block computation time, Ring Attention incurs communication overhead, degrading to inefficient operation
- The paper evaluates long-context capability exclusively on synthetic line retrieval tasks and controlled RL benchmarks (ExoRL), not on complex real-world long-document understanding, multi-hop reasoning, or production workloads — leaving generalization to practical use cases undemonstrated
- No training data exists at the scale of millions of tokens for coherent long-form tasks — while Ring Attention removes the architectural memory barrier, it does not address the conspicuous absence of naturally occurring training corpora with millions of semantically coherent tokens
- Implementation is in JAX using jax.lax.ppermute for host-to-host communication, with no PyTorch implementation described — restricting practical adoption to JAX/TPU ecosystems at time of publication
- All experiments are conducted in full precision (bfloat16/float32), not mixed precision — leaving open whether Ring Attention's overlap guarantees and MFU numbers hold under mixed-precision training, which is standard in production
- Ring Attention does not reduce the inherent quadratic compute cost of self-attention — it distributes the memory footprint across devices but each pair of devices still collectively performs O(s²) operations, so wall-clock training time still grows quadratically with sequence length at fixed device 

## Bottlenecks

- Individual device HBM capacity (typically under 100GB) imposes a hard ceiling on per-device context length for exact attention, requiring either approximations or novel distributed schemes to exceed hundreds of thousands of tokens
- Interconnect bandwidth between distributed accelerators (especially InfiniBand at 12.5 GB/s) constrains the minimum practical block size for zero-overhead Ring Attention, setting a floor on per-device sequence length requirements that limits scalability on commodity GPU clusters

## Breakthroughs

- Ring Attention with Blockwise Parallel Transformers: first demonstration that exact self-attention can be distributed across arbitrarily many devices via ring communication with zero communication overhead, enabling context lengths that scale linearly with device count — 500x beyond prior memory-eff

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]

## Key Concepts

- [[entities/infiniband|InfiniBand]]
- [[entities/llama|LLaMA]]
- [[entities/nvlink|NVLink]]
- [[entities/ring-attention|Ring Attention]]
- [[entities/sequence-parallelism|Sequence Parallelism]]
- [[entities/tensor-parallelism|Tensor Parallelism]]
