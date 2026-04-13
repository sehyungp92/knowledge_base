---
type: source
title: Parallel Scaling Law for Language Models
source_id: 01KJTVCEFHGF3NFXRV13JG401A
source_type: paper
authors:
- Mouxiang Chen
- Binyuan Hui
- Zeyu Cui
- Jiaxi Yang
- Dayiheng Liu
- Jianling Sun
- Junyang Lin
- Zhongxin Liu
published_at: '2025-05-15 00:00:00'
theme_ids:
- adaptive_computation
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Parallel Scaling Law for Language Models

**Authors:** Mouxiang Chen, Binyuan Hui, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Jianling Sun, Junyang Lin, Zhongxin Liu
**Published:** 2025-05-15 00:00:00
**Type:** paper

## Analysis

# Parallel Scaling Law for Language Models
2025-05-15 · paper · Mouxiang Chen, Binyuan Hui, Zeyu Cui, Jiaxi Yang, Dayiheng Liu et al. (8 total)
https://arxiv.org/pdf/2505.10475

---

### Motivation & Prior Limitations
- Parameter scaling requires prohibitive memory overhead that blocks edge deployment, while inference-time scaling imposes high latency costs and requires specialized training data and reward signals, leaving no universal, efficient scaling path.
  - DeepSeek-V3's 672B parameters impose memory requirements inaccessible to edge devices; the most powerful reasoning models generate up to 900 reasoning tokens for trivial problems like "2+3=?".
  - Inference-time scaling (o1, DeepSeek-R1, QwQ) is restricted to generation tasks where reward signals are available, and serial chain-of-thought scaling causes "overthinking" problems.
- Classifier-free guidance (CFG) demonstrates that two forward passes over the same model with perturbed inputs outperform a single forward pass, but no theoretical account exists for why doubling computation helps, and CFG cannot benefit from training-time scaling due to its fixed heuristic rules.
  - The fundamental question of whether model capacity is determined by parameters or computation — and in what ratio — had not been quantitatively answered before this work.

---

### Proposed Approach
- PARSCALE (parallel scaling) applies P diverse, learnable transformations to the input, runs P parallel forward passes through the same model, and dynamically aggregates the outputs — scaling computation by reusing existing parameters without changing model architecture.
  - Unlike parameter scaling (more weights) or inference-time scaling (more serial tokens), PARSCALE occupies a third axis: parallel computation at both training and inference time, applicable to any model structure, optimizer, data, or task.
  - Input transformation uses prefix tuning (P different learned prefix embeddings, implemented as distinct KV-cache entries), adding only ~0.2% parameters per stream; output aggregation uses a small MLP to compute dynamic weighted sums over the P stream outputs.
- A theoretical scaling law is derived from the Chinchilla framework: assuming each stream obeys the Chinchilla power law and streams have correlated residual errors with coefficient ρ, aggregating P streams yields L = (A / (N · P^(1/α) · DIVERSITY))^α + E, where DIVERSITY = [(P−1)ρ+1]^(−1/α), showing P parallel streams are equivalent to scaling parameters by O(P^(1/α) · DIVERSITY).
  - Empirically, the diversity term follows a logarithmic trend, yielding the practical law L = (A / (N · (k log P + 1)))^α + E, fitted to R² = 0.998 across 500M–4.4B parameter models on two corpora.
  - The logarithmic equivalence means P parallel streams match parameter scaling by O(N log P); k = 0.39 for coding (Stack-V2) versus k = 0.33 for general text (Pile), quantifying that computation contributes more to reasoning than to memorization.
- A two-stage training strategy decouples the training cost: stage 1 is conventional pre-training on the full dataset (e.g., 1T tokens), and stage 2 applies PARSCALE with randomly initialized prefix/aggregation parameters on a small continuation (e.g., 20B tokens, 2% of stage 1), allowing PARSCALE to be retrofitted onto existing trained models at low cost.

---

### Results & Capabilities
- PARSCALE with P = 8 streams applied to a 1.6B model achieves 22× less memory increase and 6× less latency increase compared to parameter scaling that reaches the same performance level (batch size = 1).
  - The memory advantage comes from PARSCALE's negligible additional parameters (~0.2% per stream) and small KV cache expansion, versus the large weight matrices added in parameter scaling.
  - The latency advantage comes from converting the memory-bandwidth bottleneck of LLM decoding into a compute bottleneck, which is GPU-friendly; the advantage shrinks at batch size 8 but PARSCALE remains more efficient than parameter scaling up to that point.
- In pre-training experiments (42B tokens, 500M–4.4B parameters), increasing P from 1 to 8 on a 1.6B model matches the coding performance of the 4.4B model (P=1) on HumanEval/MBPP, while matching only the 2.8B model on general commonsense tasks — confirming that parallel computation improves reasoning more than memorization.
- Under the two-stage strategy (1T tokens stage 1, 20B tokens stage 2) with a 1.8B model, scaling from P=1 to P=8 yields +34% relative improvement on GSM8K, +23% relative improvement on MMLU, and +4.3% on coding benchmarks using identical training data.
  - Combined with chain-of-thought at inference (CoT), PARSCALE P=8 achieves an additional ~8% gain on GSM8K, showing parallel and serial inference-time scaling are complementary, not competing.
- PARSCALE applied via parameter-efficient fine-tuning (PEFT) to the off-the-shelf Qwen-2.5-3B model (pre-trained on 18T tokens), freezing all backbone weights and only training prefix tokens and aggregation weights, still improves code generation Pass@1 from 47.4% (P=1) to 53.0% (P=8) and Pass@10 from 73.1% to 78.2%.
  - This enables dynamic parallel scaling: a single deployed backbone can switch P at inference time to trade capability for throughput without retraining.
- Instruction-tuned PARSCALE-Inst models show P=8 outperforming P=1 by +5.4% on IFEval, +7.5% on MMLU, and +5.8% on GSM8K, demonstrating that benefits transfer through post-training.

---

### Implications
- PARSCALE introduces a third axis to the scaling space — parallel computation — that is orthogonal to parameter count and token generation length, suggesting that future scaling laws and infrastructure decisions must account for all three dimensions simultaneously rather than treating parameters and compute as inseparable.
- The quantitative separation of parameters (driving memorization) from computation (driving reasoning) provides the first empirical scaling law grounding for the intuition that reasoning is compute-b

## Key Claims

1. Scaling P parallel streams is equivalent to scaling model parameters by O(log P), establishing a new parallel scaling law.
2. PARSCALE uses 22x less memory increase and 6x less latency increase compared to parameter scaling achieving the same performance, at batch size 1 for a 1.6B model scaled to P=8.
3. The parallel scaling law fit achieves a goodness of fit R² up to 0.9987, validating the parametric form L = (A / (N·(k·log P + 1)))^α + E.
4. Reasoning-intensive tasks (coding, math) benefit more from parallel computation scaling than memorization-heavy tasks.
5. Model parameters primarily impact memorization capacity, while computation primarily impacts reasoning capacity.
6. The k parameter in the parallel scaling law is higher for code/reasoning data (0.39 on Stack-V2) than for general memorization data (0.33 on Pile), quantifying the greater benefit of computation for r
7. Larger models benefit more from PARSCALE, as loss contours flatten with increasing parameters showing greater gains from computation increases.
8. PARSCALE introduces approximately 0.2% additional parameters per stream (prefix embeddings and aggregation weights), making its parameter overhead negligible.
9. PARSCALE converts the memory bottleneck in LLM decoding into a computational bottleneck, enabling better GPU utilization.
10. A two-stage training strategy where PARSCALE is applied only in the second stage with 20B tokens (2% of 1T total) greatly reduces training cost while preserving effectiveness.

## Capabilities

- Parallel scaling (PARSCALE) achieves equivalent model capacity to O(N log P) parameter scaling by running P parallel forward passes with learnable prefix transformations and dynamic MLP-based aggregation, reusing existing parameters without structural change
- PARSCALE achieves 22x less memory increase and 6x less latency increase at batch size=1 compared to parameter scaling that reaches the same model capacity, making capable models viable on memory-constrained edge hardware
- Existing pretrained LLMs can be recycled into parallelly scaled models via two-stage post-training on only ~20B tokens (2% of the original pretraining budget), with logarithmic capability gains matching from-scratch PARSCALE training
- Dynamic parallel scaling enables a single frozen backbone to serve multiple capability tiers at runtime by switching P — different trained aggregation heads per P value allow flexible quality-latency tradeoffs without any backbone retraining
- Parallel computation scaling provides greater benefit on reasoning-intensive tasks (coding, math) than memorization tasks, empirically separating the roles of parameters (memorization capacity) and computation (reasoning capacity) in model performance

## Limitations

- PARSCALE training cost scales approximately P times in floating-point operations, making full PARSCALE pretraining from scratch computationally prohibitive — a two-stage workaround exists but doesn't eliminate the fundamental training cost increase
- PARSCALE's memory and latency advantage over parameter scaling diminishes at larger batch sizes — at batch size=8 the gap is reduced, and at production-scale batch sizes common in server deployments the efficiency advantage may largely disappear
- Parallel scaling law has only been validated at ≤4.7B parameters and ≤1T training tokens; whether the O(log P) equivalence holds at frontier model scale (hundreds of billions of parameters, tens of trillions of tokens) is entirely unvalidated
- The DIVERSITY factor in the parallel scaling law cannot be derived analytically — the log P empirical fit is observed but not explained from first principles, leaving open whether growth can exceed O(log P) or whether a performance ceiling exists
- The interaction between data scaling and parallel scaling is entirely unstudied — all scaling law experiments fix training data at 42B tokens, leaving the Chinchilla-style three-way allocation across parameters, data, and P unknown
- PARSCALE expands KV cache by P times during inference; at long context lengths or large P, this growth could erode the memory savings — the headline 22x memory advantage is measured with short sequences (≤1024 tokens) and may not hold at long context
- Performance of PARSCALE for P≫8 is unknown — all experiments are bounded at P=8, with no evidence whether logarithmic scaling continues, saturates, or degrades; the practical ceiling for parallel stream scaling is uncharacterised
- Inference-time scaling (o1/R1-style chain-of-thought) requires specialised RL training with verifiable reward data, restricting its applicability to tasks with clear ground-truth verifiers and leaving most real-world tasks unaddressed
- PARSCALE compatibility with MoE architectures is uninvestigated despite obvious complementarity — MoE is parameter-heavy and latency-friendly while PARSCALE is memory-friendly, suggesting a potentially important combination that remains unexplored
- Optimal two-stage training division point is chosen empirically (1T vs 20B tokens, ~2% split) without theoretical justification — whether this ratio is close to optimal or leaves significant performance on the table is an open question

## Bottlenecks

- No principled framework for Chinchilla-style inference-optimal allocation across the three-way (parameters, data, parallel streams P) compute budget — PARSCALE introduces a new axis but the joint optimisation problem is unsolved, blocking deployment-optimal model design
- Memory-constrained edge hardware (smartphones, on-device robots, smart cars) blocks deployment of models with sufficient reasoning capability — parameter scaling creates memory requirements far exceeding edge device limits

## Breakthroughs

- PARSCALE establishes a third, independently controllable scaling axis — parallel computation during both training and inference — with a validated quantitative law showing P parallel streams are equivalent to O(N log P) parameter scaling at dramatically lower inference cost

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chinchilla-scaling-law|Chinchilla Scaling Law]]
- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/diversity|DIVERSITY]]
- [[entities/finemath|FineMath]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/gsm8k|GSM8K]]
- [[entities/ifeval|IFEval]]
- [[entities/mmlu|MMLU]]
