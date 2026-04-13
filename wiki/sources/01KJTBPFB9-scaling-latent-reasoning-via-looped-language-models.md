---
type: source
title: Scaling Latent Reasoning via Looped Language Models
source_id: 01KJTBPFB9EF7VP6MZJSW5PM5M
source_type: paper
authors:
- Rui-Jie Zhu
- Zixuan Wang
- Kai Hua
- Tianyu Zhang
- Ziniu Li
- Haoran Que
- Boyi Wei
- Zixin Wen
- Fan Yin
- He Xing
- Lu Li
- Jiajun Shi
- Kaijing Ma
- Shanda Li
- Taylor Kergan
- Andrew Smith
- Xingwei Qu
- Mude Hui
- Bohong Wu
- Qiyang Min
- Hongzhi Huang
- Xun Zhou
- Wei Ye
- Jiaheng Liu
- Jian Yang
- Yunfeng Shi
- Chenghua Lin
- Enduo Zhao
- Tianle Cai
- Ge Zhang
- Wenhao Huang
- Yoshua Bengio
- Jason Eshraghian
published_at: '2025-10-29 00:00:00'
theme_ids:
- adaptive_computation
- chain_of_thought
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Scaling Latent Reasoning via Looped Language Models

**Authors:** Rui-Jie Zhu, Zixuan Wang, Kai Hua, Tianyu Zhang, Ziniu Li, Haoran Que, Boyi Wei, Zixin Wen, Fan Yin, He Xing, Lu Li, Jiajun Shi, Kaijing Ma, Shanda Li, Taylor Kergan, Andrew Smith, Xingwei Qu, Mude Hui, Bohong Wu, Qiyang Min, Hongzhi Huang, Xun Zhou, Wei Ye, Jiaheng Liu, Jian Yang, Yunfeng Shi, Chenghua Lin, Enduo Zhao, Tianle Cai, Ge Zhang, Wenhao Huang, Yoshua Bengio, Jason Eshraghian
**Published:** 2025-10-29 00:00:00
**Type:** paper

## Analysis

# Scaling Latent Reasoning via Looped Language Models
2025-10-29 · paper · Rui-Jie Zhu, Zixuan Wang, Kai Hua, Tianyu Zhang, Ziniu Li et al. (33 total)
https://arxiv.org/pdf/2510.25741

---

### Motivation & Prior Limitations
Modern LLMs treat reasoning as an afterthought — a post-training capability bolted on via chain-of-thought prompting rather than baked into the pre-training objective, which underutilizes the pre-training compute budget and forces reasoning into the output token sequence rather than the model's internal representations.
- Chain-of-thought reasoning scales inference cost by extending the output sequence, causing context-length bloat and conflating the reasoning mechanism with its textual readout, which a growing body of work shows may be post-hoc rationalization rather than causal computation.
  - Linear probe studies on Qwen3-4B-Thinking show ROC AUC of ~0.99 when predicting the model's final answer from early hidden states, indicating the thinking process "almost does not affect the results" and the model commits to answers before generating its visible reasoning trace.
- Looped language models (universal transformers and their descendants) had been explored at modest scales but their frontier-level scaling behavior — whether iterative weight-sharing yields genuine reasoning improvements at multi-trillion-token regimes — remained undemonstrated.
- Naive adaptive computation in recurrent architectures suffers from collapse: under standard gradient descent, the exit distribution concentrates on the deepest step (maximum loops) due to a self-reinforcing feedback loop in which late steps receive more training signal and attract more probability mass, eliminating the compute-accuracy flexibility the architecture is designed to provide.

---

### Proposed Approach
The paper introduces Looped Language Models (LoopLM) — decoder-only transformers with a single weight-shared block of N layers applied iteratively for up to T_max recurrent steps — and scales pre-training to 7.7T tokens, producing the Ouro 1.4B and 2.6B model family with a multi-stage training pipeline and two-stage adaptive gating scheme.

- The core architectural innovation is iterative latent computation: the same transformer stack is applied t times, where each application refines hidden states h^(t) before projecting to vocabulary space, effectively creating a variable-depth computational graph decoupled from parameter count.
  - This is equivalent to two complementary views: (1) an extreme form of parameter sharing (analogous to ALBERT) that reduces memory footprint; (2) latent chain-of-thought where each recurrent step is a non-verbal "thought" refining internal representations — without extending the output sequence.
  - Ouro 2.6B upcycles the 1.4B's 24-layer stack to 48 layers via layer duplication starting from Stage 1b, which is made smooth by the weight-sharing property of the recurrent architecture.

- Adaptive depth allocation is learned through a two-stage gating mechanism. In Stage I (pre-training), an exit gate outputs per-step survival probabilities, and the training objective is an entropy-regularized expected task loss equivalent to a variational ELBO with a uniform prior: L = Σ_t p_φ(t|x)L^(t) − β·H(p_φ(·|x)), where the uniform prior prevents the gate from collapsing to always using T_max steps.
  - A uniform prior is chosen specifically to be depth-unbiased, decoupling exit decisions based on input difficulty from any global compute preference, contrasting with geometric or Poisson-lognormal priors (used by PonderNet) that softly favour early halting.
  - In Stage II, the LM parameters are frozen and only the exit gate is fine-tuned on an adaptive loss (Eq. 6) that trains the gate to match a greedy signal based on measured per-step loss improvements I^(t) = max(0, L^(t-1)_stop − L^(t)_stop), explicitly penalising both underthinking (exiting when improvement remains) and overthinking (continuing when gains have stalled).

- The training pipeline has five stages over 7.7T tokens: Stable Training I (8 recurrent steps, 3T tokens), Stable Training II (reduced to 4 steps for stability, 3T tokens), CT Annealing (high-quality data, 1.4T tokens, sequence length 16K), LongCT (64K sequences, 20B tokens), and Mid-training (diverse high-quality SFT-quality data, 300B tokens), followed by Reasoning SFT on 8.3M examples to produce Ouro-Thinking variants.
  - Stability required reducing recurrent steps from 8 to 4 (loss spikes and gradient oscillations emerged at 8 steps, attributed to compounded gradient flow amplifying perturbations), progressively scaling batch size from 4M to 8M tokens, and reducing the KL coefficient β from 0.1 to 0.05 to reduce conflicting gradients between task loss and depth regularization.

---

### Results & Capabilities
Ouro 1.4B (4 recurrent steps) matches or exceeds 4B parameter dense models on most benchmarks, and Ouro 2.6B matches or exceeds 8B parameter models, representing a 2–3× parameter efficiency gain demonstrated under a full multi-trillion-token training regime comparable to state-of-the-art foundation models.
- On base model benchmarks: Ouro 1.4B achieves BBH 71.02 (vs. Qwen3-4B's 70.95), GSM8K 78.92 (vs. 72.86), and MATH500 82.40 (vs. Qwen3-4B's 59.60); Ouro 2.6B achieves MMLU-Pro 55.73 (vs. Qwen3-8B's 53.72), BBH 80.46 (vs. 77.65), and MATH500 90.85 (vs. 62.30).
- On reasoning benchmarks: Ouro-1.4B-Thinking achieves AIME24 pass@1 of 65.0 (competitive with Qwen3-4B's 61.3) and OlympiadBench 71.55; Ouro-2.6B-Thinking achieves AIME24 pass@1 of 64.7 (vs. Qwen3-8B's 73.0) and OlympiadBench 76.44 (vs. 75.25), matching an 8B model at 2.6B parameters.

Controlled experiments using the Physics-of-LMs framework establish that recurrence does not increase knowledge capacity — both looped and non-looped models store approximately 2 bits per parameter on the synthetic biography (Capo) task — but dramatically improves knowledge manipulation on tasks requiring fact composition a

## Key Claims

1. Ouro 1.4B and 2.6B LoopLM models match the performance of models up to 12B parameters across a wide range of benchmarks
2. LoopLM's performance advantage stems from superior knowledge manipulation capabilities, not from increased knowledge capacity
3. LoopLM yields reasoning traces more aligned with final outputs than explicit chain-of-thought (CoT), indicating greater causal faithfulness rather than post-hoc rationalization
4. Modern LLMs trained with chain-of-thought reasoning defer reasoning to post-training and under-leverage pre-training data
5. Recurrence in LoopLM does not increase raw knowledge storage, which remains approximately 2 bits per parameter for both looped and non-looped models
6. Recurrence dramatically enhances knowledge manipulation capabilities on tasks requiring fact composition and multi-hop reasoning
7. LoopLM reduces harmfulness on the HEx-PHI benchmark, and safety improves as recurrent steps increase, including for extrapolated steps beyond training
8. Loop depth constitutes a third scaling axis beyond model size and data
9. Ouro 1.4B and 2.6B models achieve 2-3x parameter efficiency gains relative to equivalently performing standard transformers
10. Adaptive exit gates without entropy regularization collapse to always using maximum depth (the final recurrent step)

## Capabilities

- 1.4B and 2.6B Looped Language Models (LoopLMs) trained on 7.7T tokens match the benchmark performance of 4B and 8B standard transformer models respectively, achieving 2-3× parameter efficiency across reasoning-intensive tasks including MATH500, BBH, and MMLU-Pro
- Learned adaptive early-exit gates allow LoopLMs to dynamically allocate fewer recurrent steps to easy inputs and more to hard ones, trading compute for accuracy at deployment time via a threshold hyperparameter without retraining
- Last-step KV cache reuse during auto-regressive decoding reduces memory overhead of a 4-step LoopLM by 4× with negligible performance loss (within 0.3 points on GSM8K), making deployment memory footprint comparable to standard transformers of similar parameter count
- LoopLM iterative latent updates produce reasoning traces that are more causally faithful to final answers than explicit chain-of-thought, satisfying a counterfactual intervention criterion at higher rates than CoT baselines as measured by linear probe ROC AUC
- Safety alignment in LoopLMs improves monotonically as recurrent steps increase — including when extrapolating beyond training depth (T>4) — with the model learning to better separate benign from harmful prompt representations in hidden space
- LoopLMs demonstrate superior sample efficiency on multi-hop compositional reasoning tasks: requiring fewer unique training examples than iso-parameter transformers to achieve comparable accuracy on 3-hop QA and modular arithmetic tree parsing

## Limitations

- LoopLM performance degrades when extrapolating beyond the trained maximum depth (T>4): benchmark accuracy drops at T=5 and continues degrading through T=8, meaning the compute-accuracy trade-off cannot be freely extended post-hoc to access more reasoning depth
- Standard RLVR training infrastructure (vLLM, SGLang) is fundamentally incompatible with LoopLM's variable-depth early-exit computation, blocking post-SFT RL alignment: both off-policy rollout and fixed-depth workaround approaches failed to surpass SFT checkpoints
- Training instability limits practical recurrent depth to 4 steps: 8-step training produced loss spikes and gradient oscillations requiring a reduction to 4, capping the architecture's reasoning depth ceiling without a principled resolution
- KV cache reuse during the prefilling (prompt processing) phase is not viable: sharing caches across recurrent steps during prefilling causes >10 point accuracy degradation on GSM8K, requiring full 4× KV cache overhead during prompt processing
- LoopLM provides no increase in raw knowledge storage capacity: looped and non-looped models of equal parameter count both achieve approximately 2 bits/parameter on factual memorisation benchmarks, meaning recurrence cannot substitute for larger models on knowledge-recall tasks
- First-step KV cache reuse during decoding causes catastrophic performance collapse (18.73 vs 78.92 on GSM8K), revealing a hard architectural constraint: all auto-regressive generation must be anchored to the final, fully-iterated recurrent step's representations
- Recurrent architectures require smaller learning rates than parameter-matched standard transformers; an exhaustive LR sweep was skipped due to compute constraints, meaning the reported results may be suboptimal and the true training cost for a well-tuned LoopLM is underreported
- LoopLM performance gains are limited on knowledge-heavy tasks and most pronounced on reasoning-heavy tasks; the architecture's advantage degrades as tasks shift from multi-hop composition toward pure factual retrieval
- Without entropy regularisation on the exit distribution, LoopLM training collapses to always using the maximum recurrent depth, losing adaptive computation benefits entirely; the entropy penalty is a mandatory training ingredient, not an optional add-on
- The SmolLM2 49K-vocabulary tokenizer is optimised for code and Latin-alphabet languages; Chinese characters fragment into multiple byte-level sub-tokens, forcing Chinese to be dropped after Stage 1 and making the model effectively English-and-code-only for the main training stages
- Post-SFT RL training on small LoopLMs (1.4B–2.6B) yields no measurable gains even under a fixed-depth workaround, suggesting these scales may have insufficient latent capability headroom for RL improvement after extensive supervised fine-tuning — with the mechanism unclear

## Bottlenecks

- No RL training infrastructure natively supports variable-depth early-exit computation graphs, blocking RLVR alignment for adaptive-computation architectures such as LoopLMs; both off-policy workarounds and fixed-depth approximations failed
- Compounding gradient flow through shared-weight recurrent iterations causes loss spikes and oscillations beyond 4 steps, capping the practical reasoning depth ceiling of LoopLMs and preventing access to deeper iterative computation
- KV cache memory scales linearly with recurrent depth during prefilling without any known reduction strategy, creating a hard memory cost floor that limits LoopLM deployment on memory-constrained hardware and for long-context workloads

## Breakthroughs

- Looped Language Models demonstrated at frontier training scale (7.7T tokens) to match models 2-3× larger in parameters, establishing loop depth as a viable third scaling axis beyond model size and data — resolving long-standing uncertainty about whether LoopLMs could deliver frontier-level gains
- Controlled experiments using physics-of-LMs synthetic tasks prove that recurrent depth enhances knowledge manipulation (multi-hop reasoning, compositional inference) without increasing knowledge storage capacity — identifying the precise mechanism of LoopLM's advantage for the first time and providi

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]

## Key Concepts

- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
- [[entities/universal-transformer|Universal Transformer]]
