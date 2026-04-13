---
type: source
title: 'TiDAR: Think in Diffusion, Talk in Autoregression'
source_id: 01KJT9KDWV6TTNJE8D2DTFH3FE
source_type: paper
authors:
- Jingyu Liu
- Xin Dong
- Zhifan Ye
- Rishabh Mehta
- Yonggan Fu
- Vartika Singh
- Jan Kautz
- Ce Zhang
- Pavlo Molchanov
published_at: '2025-11-12 00:00:00'
theme_ids:
- adaptive_computation
- model_architecture
- reasoning_and_planning
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# TiDAR: Think in Diffusion, Talk in Autoregression

TiDAR introduces a sequence-level hybrid architecture that resolves the long-standing quality-parallelism tradeoff in diffusion language models by using bidirectional diffusion attention to draft speculative tokens and causal autoregressive attention to verify them — both in a single forward pass. It is the first reported system to simultaneously close the quality gap with AR baselines and exceed the throughput of speculative decoding methods like EAGLE-3, achieving 4.71×–5.91× speedups over AR counterparts at 1.5B and 8B scales without quality loss.

**Authors:** Jingyu Liu, Xin Dong, Zhifan Ye, Rishabh Mehta, Yonggan Fu, Vartika Singh, Jan Kautz, Ce Zhang, Pavlo Molchanov
**Published:** 2025-11-12
**Type:** Paper · [arxiv](https://arxiv.org/pdf/2511.08923v1)

**Themes:** [[themes/model_architecture|Model Architecture]] · [[themes/adaptive_computation|Adaptive Computation]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] · [[themes/transformer_alternatives|Transformer Alternatives]] · [[themes/reasoning_and_planning|Reasoning & Planning]]

---

## Motivation

### The Memory-Bandwidth Ceiling of Autoregressive Decoding

AR models are fundamentally memory-bound during inference: at small batch sizes, latency is dominated by loading model weights and KV cache rather than compute. Generating one token per forward pass means GPU compute density is chronically underutilised. Speculative decoding offers a partial fix — generating multiple draft tokens then verifying them — but existing approaches have structural limits:

- **Separate draft models** have low acceptance rates due to weaker capacity.
- **Shared-weight approaches** (EAGLE-series, DeepSeek-V3 MTP) still draft autoregressively and sequentially, preventing true parallelism.

### The Diffusion Parallelism Trap

Diffusion language models (dLMs) promise native parallel token generation, but in practice face a hard quality-parallelism tradeoff. Decoding $k$ tokens in a single denoising step factorises the joint distribution as a product of independent marginals — an approximation that degrades sequence-level coherence. The failure mode is concrete: **Dream-7B loses 10% accuracy on GSM8K when moving from 1 to 2 tokens per step** using entropy-based sampling. Best quality for dLMs requires decoding one token per step, which collapses back to AR-like sequential behaviour.

A compounding problem: bidirectional attention in dLMs prevents exact KV caching, forcing either full recomputation per denoising step or approximate caching schemes (Fast-dLLM, d-KV Cache) that trade quality for efficiency.

---

## Approach

### The Core Insight: Free Token Slots

For a given prefix length, sending $k$ additional token slots through a forward pass incurs near-zero latency increase until the compute-bound regime is reached — verified empirically on Qwen3-32B on H100. TiDAR exploits these "free token slots" by simultaneously:

1. **Verifying** the previous step's diffusion drafts via AR rejection sampling (causal attention, joint distribution).
2. **Pre-drafting** the next step's tokens via diffusion (bidirectional attention, marginal distribution).

Both happen in one forward pass with no additional parameters.

### Hybrid Attention Mask

The attention mask is a structured causal–bidirectional hybrid:
- **Prefix tokens** attend causally — enabling the chain-factorised AR joint distribution and standard NTP loss.
- **Appended mask tokens** attend bidirectionally within each block — enabling the marginal diffusion distribution for parallel drafting.

A pre-initialised mask is sliced at each step via Flex Attention rather than recomputed. This design resolves a problem that blocked Block Diffusion: because TiDAR's prefix is purely causal, **next-token prediction loss on the prefix is computable without label leakage**, enabling joint AR + diffusion training on the same data sample.

### Training Strategy

TiDAR uses a dual-loss objective: AR next-token prediction on the causal prefix + diffusion cross-entropy on a **fully masked suffix** (all diffusion-section tokens set to `[MASK]`, not randomly corrupted). This "full masking" strategy yields three compounding benefits:

- Denser diffusion loss signal — all tokens contribute.
- Consistent loss scale between AR and diffusion terms, enabling straightforward balancing via a scalar $\alpha$.
- Train–test consistency, since inference also starts with fully masked inputs.

Training initialises from existing AR checkpoints (Qwen2.5 1.5B, Qwen3 4B/8B) via continual pretraining — 50B tokens for 1.5B, 150B tokens for 8B — making it data-efficient relative to training from scratch.

### Inference Loop

At each step:
1. Draft tokens from the **previous step** are verified by AR rejection sampling over the causal joint distribution.
2. Simultaneously, the **next step's drafts** are pre-computed in parallel for all possible acceptance prefixes — so regardless of how many tokens are accepted, corresponding next-step drafts are already available.
3. Accepted KV entries are cached; rejected entries are evicted. No redundant recomputation.

Unlike Apple's MTP, drafting is fully parallel (bidirectional diffusion over all mask tokens simultaneously) rather than autoregressive. Unlike EAGLE-3, no separate draft module or additional parameters are required.

---

## Results

| Model | vs. Base | Throughput Speedup | Avg T/NFE |
|---|---|---|---|
| TiDAR 1.5B | Qwen2.5 1.5B | **4.71×** | 7.45 |
| TiDAR 8B | Qwen3 8B Base | **5.91×** | 8.25 |

- TiDAR 1.5B scores 44.03% average across HumanEval, MBPP, GSM8K, and Minerva Math — surpassing Block Diffusion 1.5B (38.41%) under matched conditions.
- TiDAR 8B outperforms EAGLE-3 speculative decoding (AngelSlim and Tengyunw weights on Qwen3-8B Instruct) in wall-clock tokens/second, attributed to higher T/NFE acceptance rates and superior NFE-to-TPS conversion from parallel drafting.
- Unlike confidence-based dLM decoding (which collapses: confidence > 0.6 yields 3.81 T/NFE at 22.56% HumanEval vs. TiDAR 8B at 8.25 T/NFE), TiDAR's AR rejection sampling has **no hyperparameters to tune at inference time**.

---

## Landscape Contributions

### Capabilities Unlocked

- **Quality-parity + throughput**: First architecture to simultaneously close the quality gap with AR and exceed speculative decoding throughput at production-relevant model sizes. [[themes/model_architecture|Model Architecture]]
- **Exact KV caching in a diffusion-hybrid**: Structured causal-bidirectional masking enables standard incremental decoding — no full recomputation, no approximate caching. [[themes/adaptive_computation|Adaptive Computation]]
- **Hyperparameter-free diffusion inference**: AR rejection sampling eliminates the entropy/confidence thresholds that every prior dLM requires at decoding time.
- **Likelihood evaluation parity with AR**: TiDAR evaluates likelihoods identically to AR models using pure causal masking, eliminating the Monte Carlo approximation problem that made dLM comparisons unreliable.

### Bottlenecks Addressed

**Partially resolved — [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]:**
The memory-bandwidth ceiling of AR decoding (one token per forward pass, GPU compute underutilised) is directly addressed by TiDAR's parallel drafting. However, this advantage is demonstrated only at batch size = 1.

**Partially resolved:**
Bidirectional attention blocking exact KV caching in dLMs is resolved for the hybrid architecture, though pure dLMs remain affected.

**Structurally bypassed, not solved:**
The intra-step token independence assumption of masked diffusion — the fundamental source of the quality-parallelism tradeoff — is circumvented by offloading quality to the AR rejection sampling pass rather than fixed within the diffusion framework itself.

---

## Limitations and Open Questions

**Scaling to long context is deferred.** Training doubles sequence length by appending full-mask tokens, creating memory and compute scaling problems beyond the 4096-token training length. The authors explicitly defer this.

**Batch size = 1 only.** All throughput benchmarks are on a single H100 at batch size = 1. The "free token slot" advantage relies on the memory-bandwidth-bound regime; at production batch sizes where AR models shift toward compute-bound operation, the advantage may shrink or invert. The authors note TiDAR *can* handle larger batches but provide no data.

**No instruction-tuned or chat evaluation.** Results are exclusively on base model versions. Whether the dual AR/diffusion training mode interferes with instruction following, safety alignment, or RLHF stability is unknown.

**Quality gap not fully closed.** A residual quality gap from fine-tuned AR models remains at 1.5B scale; at 8B, throughput gains come with "minimal loss" rather than lossless parity. The authors attribute this to insufficient continual pretraining data rather than architectural ceiling.

**Substantial compute cost to convert.** 50B–150B tokens of continual pretraining on H100 clusters is required to adapt an existing AR checkpoint. This is a non-trivial hidden cost that concentrates who can create or reproduce TiDAR variants.

**Native PyTorch underperforms.** Current implementation uses Flex Attention without custom CUDA kernels. The authors note that custom kernels for the structured hybrid attention mask would yield substantially higher throughput — meaning reported numbers are a lower bound, but also that reproducibility requires significant systems engineering.

**Confidence-based strategies are not rehabilitated.** The paper conclusively shows that entropy/confidence-based decoding for pure dLMs collapses beyond ~2–3x speedup. TiDAR's gains are not transferable to existing dLMs using those strategies — its advantages are architectural.

**Narrow evaluation scope.** Benchmarks cover short-output code and math tasks (HumanEval, MBPP, GSM8K, Minerva Math) plus commonsense. Performance on long-form generation, multi-turn dialogue, retrieval-augmented tasks, or tool use is uncharacterised.

---

## Connections and Implications

**Vs. Block Diffusion:** Block Diffusion introduced segmented bidirectional attention but cannot compute NTP loss on the prefix due to label leakage. TiDAR's causal prefix resolves this, enabling cleaner joint training and exact KV caching.

**Vs. EAGLE-3 / DeepSeek-V3 MTP:** Those approaches draft autoregressively, preserving sequential dependency. TiDAR drafts via parallel masked diffusion, achieving higher T/NFE at the cost of marginal (not joint) draft quality — which is then corrected by AR rejection sampling.

**Implication for [[themes/transformer_alternatives|Transformer Alternatives]]:** The paper reframes diffusion LMs not as replacements for AR models but as draft generators within an AR verification loop. This hybrid framing may be the productive path forward for other non-AR generative architectures seeking deployment viability.

**Implication for [[themes/adaptive_computation|Adaptive Computation]]:** The "free token slot" insight — that memory-bound decoding leaves compute capacity unused that can be filled with parallel drafts — is a general principle applicable beyond this specific architecture. The precise compute-vs.-memory-bound transition point becomes a key hyperparameter for future hybrid designs.

## Key Concepts

- [[entities/autoregressive-language-model|Autoregressive Language Model]]
- [[entities/diffusion-language-model|Diffusion language model]]
- [[entities/gsm8k|GSM8K]]
- [[entities/llada|LLaDA]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/qwen3|Qwen3]]
- [[entities/speculative-decoding|Speculative Decoding]]
