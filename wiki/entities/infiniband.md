---
type: entity
title: InfiniBand
entity_type: entity
theme_ids:
- adaptive_computation
- ai_market_dynamics
- compute_and_hardware
- frontier_lab_competition
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0009650229873850225
staleness: 0.0
status: active
tags: []
---
# InfiniBand

> InfiniBand is a high-speed networking standard used to interconnect GPUs across compute nodes in distributed training clusters. In the context of long-context transformer training, it represents a meaningful bandwidth bottleneck: at roughly 12.5 GB/s inter-node throughput — roughly 24x slower than NVLink's intra-node 300 GB/s — InfiniBand sets hard constraints on the minimum sequence and block sizes required for distributed attention techniques like Ring Attention to operate efficiently, making it a critical infrastructure variable when scaling context lengths across multi-node GPU clusters.

**Type:** entity
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/compute_and_hardware|Compute & Hardware]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/long_context_and_attention|Long Context & Attention]], [[themes/model_architecture|Model Architecture]], [[themes/model_commoditization_and_open_source|Model Commoditization & Open Source]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/scaling_laws|Scaling Laws]]

---

## Overview

InfiniBand occupies a specific and revealing position in the distributed training stack: it is the interconnect that links GPU nodes when faster intra-node options (NVLink) are unavailable or insufficient, and its bandwidth characteristics directly constrain what distributed attention algorithms can achieve without incurring communication overhead.

The significance of InfiniBand becomes concrete in the analysis of Ring Attention, which distributes the self-attention computation across devices by passing key-value blocks in a ring topology. The core efficiency principle of Ring Attention is that communication and computation can be overlapped — as one device processes a block, it simultaneously sends and receives the next — so that zero additional overhead is added compared to standard transformers. But this overlap is only achievable if block computation time exceeds block transfer time. This yields the governing inequality: block size `c ≥ F/B`, where `F` is the host's FLOP rate and `B` is the inter-host bandwidth.

InfiniBand's relatively low bandwidth makes this threshold much harder to satisfy. For A100 GPUs connected via InfiniBand, the minimum sequence length per device required to enable full overlap is approximately **149,500 tokens**, with a corresponding minimum block size of roughly **24,500 tokens**. By contrast, A100s connected via NVLink — with bandwidth roughly 24x higher — require only ~6,200 tokens per device. The gap is not incidental; it directly reflects the F/B ratio, and illustrates how infrastructure choices at the networking layer propagate upward to constrain model training regimes.

---

## Key Findings

### InfiniBand as a Hard Constraint on Ring Attention Efficiency

The bandwidth asymmetry between InfiniBand and NVLink creates a two-tier world for long-context distributed training. Clusters relying on InfiniBand for inter-node communication face a steep entry cost: sequences must be long enough that each device is processing a block large enough to keep the network saturated but never idle. Below the ~149K token threshold, the ring communication stalls computation, and the zero-overhead promise of Ring Attention breaks down.

This is not merely a theoretical concern. At the time the Ring Attention paper was published, leading production context windows ranged from GPT-3.5's 16K to Anthropic's Claude at 100K tokens — placing most practical deployments well below the InfiniBand threshold even on a per-device basis. Only in very large-scale multi-node settings, distributing a very long sequence across many devices, would the per-device share exceed 149K tokens.

### The Broader Bottleneck: HBM Scarcity and Scale

InfiniBand's constraints appear alongside a parallel hardware limitation: individual GPUs and TPUs typically carry less than 100GB of high-bandwidth memory (HBM), and physical and manufacturing barriers make significant HBM expansion unlikely in the near term. Together, these two constraints — slow inter-node bandwidth and limited on-device memory — define the principal axes of difficulty for scaling context length. Ring Attention addresses the memory bottleneck (reducing activation memory to `6bch` bytes per layer, independent of sequence length), but its communication-overlap mechanism depends on InfiniBand being fast enough relative to compute — a condition that is often not met.

The contrast with NVLink-connected setups is instructive: on TPUv4-1024 clusters (which benefit from high-bandwidth interconnects), Ring Attention achieves a 512x increase in context size for 3B and 7B models, enabling training sequences over 16 million and 8 million tokens respectively, with negligible MFU overhead. These numbers are simply inaccessible to InfiniBand-connected deployments at the same scale.

### Tensor Parallelism and Sequence Parallelism Offer No Escape

One might expect existing parallelism strategies to sidestep these bandwidth constraints, but they do not. Tensor parallelism can only reduce parts of activation memory and does not address the sequence-length scaling problem. Sequence parallelism, the most direct alternative to Ring Attention for distributing long sequences, introduces significant communication overhead that cannot be fully overlapped with computation — precisely the property Ring Attention exploits and that InfiniBand's low bandwidth undermines. The net effect is that InfiniBand-constrained clusters face a genuine capability gap relative to high-bandwidth interconnect deployments, not merely a performance degradation.

### Implications for the Competitive Landscape

InfiniBand's constraint on minimum viable sequence lengths has indirect but meaningful implications for the [[themes/frontier_lab_competition|frontier lab competition]] and the broader [[themes/ai_market_dynamics|AI market dynamics]]. Labs and hyperscalers with proprietary high-bandwidth interconnects (NVLink clusters, custom TPU fabrics) can train on dramatically longer sequences with less infrastructure overhead than commodity InfiniBand clusters. This creates an infrastructure moat that is difficult to replicate without significant capital expenditure — and explains in part why context length scaling has been uneven across the field despite the theoretical availability of techniques like Ring Attention.

The DeepSeek-V3 and DeepSeek's broader strategy are relevant here: part of DeepSeek's efficiency narrative involves making capable models accessible on infrastructure that does not assume high-bandwidth NVLink topologies, reflecting awareness that most compute globally is InfiniBand-class.

---

## Open Questions

- **Can Ring Attention be restructured** to reduce the minimum viable block size on InfiniBand, enabling efficient long-context training on commodity clusters without requiring 149K+ tokens per device?
- **How does Tree Attention** (referenced in Tree Attention: Topology-aware Decoding) address InfiniBand's latency and bandwidth profile during inference, and does its topology-awareness offer a meaningful improvement over ring-based approaches in bandwidth-constrained settings?
- **As InfiniBand generations advance** (HDR, NDR), how do the minimum sequence length requirements shift, and at what bandwidth does InfiniBand effectively close the gap with NVLink for Ring Attention purposes?
- **Is the 149K token floor a training-only constraint**, or does it also affect inference-time distributed attention for long-context generation, where batch sizes and sequence distributions differ substantially?

---

## Related Sources

- Ring Attention with Blockwise Transformers for Near-Infinite Context — primary source establishing InfiniBand's bandwidth constraints on Ring Attention
- Tree Attention: Topology-aware Decoding for Long-Context Attention on GPU clusters — explores topology-aware alternatives for distributed attention
- DeepSeek-V3 Technical Report — context for efficient training on commodity cluster infrastructure
- How DeepSeek Changes the LLM Story — broader implications of infrastructure accessibility for competitive dynamics

## Limitations and Open Questions

## Relationships

## Sources
