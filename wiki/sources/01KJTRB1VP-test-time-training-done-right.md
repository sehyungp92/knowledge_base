---
type: source
title: Test-Time Training Done Right
source_id: 01KJTRB1VP2VZMT0SSXYTA3S4A
source_type: paper
authors:
- Tianyuan Zhang
- Sai Bi
- Yicong Hong
- Kai Zhang
- Fujun Luan
- Songlin Yang
- Kalyan Sunkavalli
- William T. Freeman
- Hao Tan
published_at: '2025-05-29 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- post_training_methods
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Test-Time Training Done Right

**Authors:** Tianyuan Zhang, Sai Bi, Yicong Hong, Kai Zhang, Fujun Luan, Songlin Yang, Kalyan Sunkavalli, William T. Freeman, Hao Tan
**Published:** 2025-05-29 00:00:00
**Type:** paper

## Analysis

# Test-Time Training Done Right
2025-05-29 · paper · Tianyuan Zhang, Sai Bi, Yicong Hong, Kai Zhang, Fujun Luan et al. (9 total)
https://arxiv.org/pdf/2505.23884v1

---

### Motivation & Prior Limitations
- Existing Test-Time Training (TTT) methods have failed to demonstrate practical effectiveness on long sequences because their TTT layers operate at extremely low hardware utilization, often below 5% of peak FLOPS on modern GPUs.
  - The root cause is the use of small mini-batch (chunk) sizes — updating fast weights every 1 to 64 tokens — which yields poor compute-to-memory ratios and prevents efficient parallelism along the sequence dimension.
  - Small chunks also enforce fine-grained block-wise causal dependencies, making TTT architectures structurally incompatible with unordered or N-dimensional data like image sets or video grids.
- Prior TTT approaches scaled state sizes poorly: existing methods maintain a state-to-parameter ratio of only 0.1% to 5%, severely limiting memory capacity relative to model size.
  - Achieving even modest GPU utilization required cumbersome custom CUDA kernel implementations that constrain fast weights to evolve independently within streaming multiprocessors, ruling out large nonlinear states or sophisticated optimizers like Muon.
- The dominant alternative for long-context modeling — softmax attention — scales quadratically with sequence length, and linear recurrence variants (Mamba, GLA, DeltaNet) use per-token updates that cannot efficiently exploit large nonlinear fast-weight networks.

---

### Proposed Approach
- LaCT (Large Chunk Test-Time Training) inverts the conventional assumption by using extremely large chunks — from 2,048 to 1 million tokens — as the atomic unit for fast-weight updates, dramatically improving hardware utilization without requiring custom kernels.
  - The compute-to-memory ratio for a matrix multiply between fast weights (h×h) and chunk input (b×h) is bounded by min(h/2, b); large b directly raises this ratio toward GPU arithmetic throughput, achieving up to 70% utilization on NVIDIA A100s in pure PyTorch.
  - Because tokens within a chunk are treated as an unordered set for the TTT update, window attention (local self-attention covering intra-chunk structure) is integrated alongside the TTT layer to capture locality and data-specific structure; this hybrid gives quadratic compute for local dependencies and linear compute for global context.
- The fast-weight network is a SwiGLU-MLP (three weight matrices W1, W2, W3) with a dot-product loss for key-value association, and weight updates use L2 normalization after gradient descent to prevent magnitude explosion — analogous to post-layer norm in transformers applied over the time dimension.
  - The Muon optimizer (which normalizes gradient spectral norm via Newton-Schulz iterations, approximating UV^T from the SVD of the gradient) is used as the default test-time update rule, providing scale-invariant updates that improve stability and decouple learning rate from absolute gradient magnitude.
- Different causal dependency structures (full, block-wise causal, shifted block-wise causal, strided block-wise causal) are realized by varying the execution order of the TTT "update" and "apply" operations within a chunk, analogous to different attention masks, without architectural changes.
- Large-chunk updates support context parallelism (CP) by sharding tokens within a chunk across devices and summing gradients via all-reduce, incurring only 1–3% throughput overhead — a regime inaccessible to small-chunk TTT which requires tensor parallelism over heads instead.
- The state-to-parameter ratio scales to ≥40% (up to 12d² per block in ablations), an order of magnitude larger than prior TTT methods, enabled by the efficiency headroom that large chunks provide.

---

### Results & Capabilities
- On novel view synthesis (NVS) with 48 input images at 512×512 resolution, LaCT achieves comparable rendering quality to full-attention models while reducing prefill latency from 16.1 seconds to 1.4 seconds and increasing rendering speed from 2.3 FPS to 38.7 FPS, with O(n) prefill compute versus O(n²) for full attention.
  - On the DL3DV scene dataset at 960×536 resolution with up to 128 input images (1 million tokens), LaCT outperforms 3D Gaussian Splatting with sparse views and surpasses LongLRM (Mamba + full attention) which is limited to 32 views.
- On language modeling, LaCT (3B parameters, 60B training tokens, 32K context) achieves lower per-position validation loss at large token indices than GLA+SWA and DeltaNet+SWA, indicating stronger utilization of long context, and consistently outperforms both on S-NIAH retrieval accuracy at all tested sequence lengths.
  - Training throughput at 3B scale with 32K sequences on A100s is 4.3K tokens/second for the Muon variant, comparable to GLA SWA (5.0K) and DeltaNet SWA (5.1K), meaning the performance gains come at minimal throughput cost.
- Autoregressive video diffusion: LaCT adapts the 14-billion-parameter Wan 2.1 bidirectional diffusion transformer into an autoregressive model handling sequences of 56,160 visual tokens (107K tokens under teacher-forcing), achieving validation loss comparable to the full block-wise causal attention baseline while outperforming both Mamba2+SWA and SWA-only baselines.
- Ablations confirm monotonic scaling: increasing state size from 0.375d² to 12d² consistently improves both NVS and language model performance, with the performance gap widening at longer sequences; nonlinear (SwiGLU) fast weights outperform linear fast weights even when the linear variant uses a larger state size; and Muon consistently outperforms vanilla gradient descent and momentum across both task domains.

---

### Implications
- LaCT reframes the efficiency-expressivity tradeoff in recurrent sequence modeling: by demonstrating that large online minibatch sizes are computationally superior to small ones and enable richer state representations, it 

## Key Claims

1. Existing TTT methods operate with extremely low FLOPs utilization in their TTT layers, often below 5% peak FLOPS on modern GPUs.
2. The low GPU utilization in existing TTT methods is caused by small online mini-batch sizes (e.g., updating fast weights every 16 or 64 tokens), which results in poor parallelism and low compute intens
3. Small mini-batch sizes in TTT make the approach unsuitable for data beyond 1D ordered sequences, such as sets or N-dimensional grids like images or videos.
4. Large Chunk Test-Time Training (LaCT) uses chunk sizes ranging from 2048 to 1 million tokens as the basic unit for fast weight updates.
5. LaCT achieves GPU utilization of up to 70% on NVIDIA A100s using only a few dozen lines of pure PyTorch code, without requiring custom kernel implementations.
6. LaCT achieves a state-to-parameter size ratio of at least 40%, which is an order of magnitude larger than previous TTT methods' ratio of 0.1% to 5%.
7. Custom kernel implementations used by prior TTT methods are incompatible with large nonlinear fast weight states because they require fast weights to evolve independently within SMs to reduce communic
8. LaCT adopts SwiGLU-MLP without bias terms as the fast-weight network, consisting of three weight matrices, enabling nonlinear memory storage.
9. LaCT uses a dot product loss function (negative inner product) between the transformed key and value vectors as its fast-weight learning objective.
10. Different orderings of the 'update' and 'apply' operations in LaCT produce different effective attention masks, enabling the modeling of diverse data dependencies analogous to different attention mask

## Capabilities

- Large-chunk TTT (LaCT) achieves up to 70% GPU utilization on NVIDIA A100s using pure PyTorch code (no custom CUDA kernels), compared to below 5% for existing TTT methods with dedicated custom kernels
- TTT fast-weight state sizes scaled to 40% of total model parameter size, an order of magnitude larger than previous TTT methods at 0.1%–5%, enabling qualitatively better long-context memory capacity
- Novel view synthesis processing 1M tokens (128 input images at 960×536 resolution) with linear prefill compute, outperforming 3D Gaussian Splatting on challenging scene datasets
- Autoregressive video diffusion at 14B parameter scale generating consistent videos up to 56,000 visual tokens (8.8-second clips at 480×832, 16 FPS) by replacing bidirectional attention layers with LaCT
- LaCT language models at 760M and 3B scale outperform GLA and DeltaNet on long-context retrieval (S-NIAH) and per-position loss when equipped with nonlinear fast weights and Muon optimizer
- Nonlinear SwiGLU-MLP fast weights for online TTT memory compression consistently outperform linear fast weights at matched or smaller state sizes across both NVS and language modeling tasks
- Muon optimizer (Newton-Schulz spectral norm normalization of gradients) integrated into TTT fast-weight updates outperforms both vanilla gradient descent and momentum variants across all evaluated tasks

## Limitations

- LaCT fast-weight components (SwiGLU-MLP and linear variants) lack rotation invariance, making them incompatible with relative positional encodings such as RoPE; practical implications for positional reasoning remain underexplored
- Reasoning ability of LaCT is not validated due to compute budget limitations; state-based models are explicitly acknowledged as structurally weak at reasoning relative to transformers, and this weakness is expected to apply
- LaCT lacks per-token causality within each chunk — the fast-weight update treats chunk tokens as an unordered set, requiring compensating window attention for local ordering; this hybrid dependency introduces architectural complexity and limits pure TTT deployment
- Linear large-chunk recurrence alone underperforms per-token recurrence methods (GLA, DeltaNet) on language modeling; nonlinear fast weights and Muon optimizer are both jointly required to surpass these baselines, limiting modularity
- Performance advantages of large-chunk TTT are data-structure-dependent: gains are largest when natural chunks align with data structure (images, video frames) and weakest for unstructured 1D text, revealing sensitivity to structural alignment assumptions
- No reliable or distinguishable metric exists to measure scalability of autoregressive video diffusion models; video evaluation is limited to validation loss, which cannot adequately differentiate quality improvements from architectural changes
- LaCT evaluation covers only 3 tasks; harder variants such as unposed 3D reconstruction (without camera pose priors) are explicitly excluded, and reasoning-heavy NLP benchmarks are absent, limiting generalization claims
- Muon optimizer for fast-weight updates reduces training throughput from ~5.0K tokens/second (vanilla GD) to ~4.3K tokens/second, a ~14% slowdown — trading efficiency for the quality gains it provides
- Video diffusion fine-tuning uses an internal proprietary dataset with AI-generated captions, making video generation results non-reproducible and preventing independent benchmark comparison
- TTT during inference still requires backward-pass gradient computation for fast-weight updates; LaCT dramatically improves efficiency but cannot eliminate this fundamental coupling of training and inference compute

## Bottlenecks

- Absence of rotation invariance in TTT fast-weight networks (SwiGLU-MLP and linear variants) blocks direct integration of relative positional encodings (RoPE, ALiBi), preventing TTT-based architectures from matching transformer positional awareness in sequence-order-sensitive tasks
- State-based model architectures (SSMs, TTT variants including LaCT) are structurally weak at reasoning tasks; this structural weakness, combined with prohibitive compute costs to validate reasoning at sufficient training scale, blocks sub-quadratic architectures from replacing transformers on reason

## Breakthroughs

- LaCT demonstrates that TTT layers can achieve 70% GPU utilization via large-chunk updates (2K–1M tokens) using pure PyTorch, eliminating the requirement for custom CUDA kernels while enabling fast-weight state sizes up to 40% of total model parameters
- A 14B parameter production video diffusion model (Wan 2.1) is successfully converted to autoregressive generation at 56K token sequences by replacing all bidirectional attention with LaCT, demonstrating TTT scalability to frontier model scale on a generative task

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/test_time_learning|test_time_learning]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/context-parallelism|context parallelism]]
