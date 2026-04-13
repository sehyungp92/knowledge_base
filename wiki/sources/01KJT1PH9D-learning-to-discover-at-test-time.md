---
type: source
title: Learning to Discover at Test Time
source_id: 01KJT1PH9D6HPVJBM5HXVKQ0W7
source_type: paper
authors:
- Mert Yuksekgonul
- Daniel Koceja
- Xinhao Li
- Federico Bianchi
- Jed McCaleb
- Xiaolong Wang
- Jan Kautz
- Yejin Choi
- James Zou
- Carlos Guestrin
- Yu Sun
published_at: '2026-01-22 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- scientific_and_medical_ai
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Learning to Discover at Test Time

**Authors:** Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan Kautz, Yejin Choi, James Zou, Carlos Guestrin, Yu Sun
**Published:** 2026-01-22 00:00:00
**Type:** paper

## Analysis

# Learning to Discover at Test Time
2026-01-22 · paper · Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb et al. (11 total)
https://arxiv.org/pdf/2601.16175

---

### Motivation & Prior Limitations
- Existing test-time scaling approaches for scientific discovery rely on prompting a frozen LLM to search the solution space, meaning the model itself cannot improve from problem-specific experience — only its inputs change.
  - Methods like AlphaEvolve use evolutionary search with hand-crafted mutation and cross-over heuristics to construct better prompts from past attempts, but the LLM weights remain static throughout, analogous to a student who can try new guesses but never internalize the underlying ideas.
  - Discovery problems are fundamentally out-of-distribution by definition — they require solutions beyond not just the model's training data but all existing human knowledge — and static models have no mechanism to adapt their internal representations to this novel territory.
- Standard RL objectives are misaligned with the goal of scientific discovery: they maximize expected reward (average performance across many rollouts) rather than the maximum reward (a single exceptional solution surpassing the state of the art).
  - A kernel achieving 1900µs versus 2000µs state-of-the-art requires a genuine breakthrough, yet without complicated reward shaping both receive nearly identical expected-reward gradients.
  - Starting each attempt from scratch limits the effective horizon of any single rollout, preventing the emergence of complex multi-step solutions that require building on prior partial successes.

---

### Proposed Approach
- TTT-Discover (Test-Time Training to Discover) performs reinforcement learning directly on the single test problem at test time using LoRA fine-tuning, so the LLM's weights themselves improve from problem-specific experience rather than only its context.
  - Unlike all prior evolutionary search methods (AlphaEvolve, ShinkaEvolve, ThetaEvolve), the policy parameters θ are updated online across training steps, not merely re-prompted with richer context derived from past attempts.
  - The method instantiates a full MDP environment from the problem description: state = candidate solution (e.g., kernel code or step function), action = thinking tokens + code, reward = continuous verifiable signal (inverse runtime, certified bound, test score), with 50 training steps of 512 rollouts each using gpt-oss-120b with LoRA rank 32.
- The entropic objective replaces the standard expected-reward objective to prioritize maximum-reward actions: $J_\beta(\theta) = \mathbb{E}_{s}[\log \mathbb{E}_{a}[e^{\beta(s) R(s,a)}]]$, which in the limit $\beta \to \infty$ converges to maximizing the best outcome rather than the average.
  - $\beta$ is set adaptively per initial state by constraining KL divergence of the induced policy rather than as a fixed constant, because large $\beta$ early in training causes instabilities while small $\beta$ later makes advantages vanish as marginal improvements become harder to distinguish.
  - The gradient of $J_\beta$ re-weights the policy gradient by $w_\beta(a) = e^{\beta R(a)} / \mathbb{E}[e^{\beta R}]$, placing exponentially more weight on high-reward rollouts in each batch.
- State reuse via a PUCT-inspired selection rule replaces both naive i.i.d. sampling and standard $\epsilon$-greedy exploration to balance exploitation of promising solutions with diversity.
  - Each buffered state $s$ is scored as $Q(s) + c \cdot P(s) \cdot \sqrt{1 + T/(1 + n(s))}$, where $Q(s)$ is the *maximum* (not mean) child reward, $P(s)$ ranks states by reward as a prior, and the exploration bonus prevents over-exploitation of a few high-reward states.
  - This effectively extends the horizon of each rollout by warm-starting generation from prior partial solutions, allowing increasingly complex constructions (e.g., 600-piece step functions, fused GPU kernels) to emerge over the course of training.

---

### Results & Capabilities
- TTT-Discover sets the new state of the art in almost every problem attempted, using only the open model gpt-oss-120b, while all previous best AI results required closed frontier models (Gemini 2.0/2.5 Pro, GPT-5, Claude Sonnet 4).
- On Erdős' minimum overlap problem (combinatorics, open since 1955), TTT-Discover improves the upper bound from 0.380924 (AlphaEvolve) to 0.380876 — an improvement 16× larger than AlphaEvolve's gain over the prior human record of 0.380927, via a novel asymmetric 600-piece step function versus AlphaEvolve's symmetric 95-piece construction.
- On the first autocorrelation inequality (AC1), TTT-Discover achieves $C_1 \leq 1.50286$ with a 30,000-piece step function, surpassing ThetaEvolve (1.50313) and AlphaEvolve V2 (1.50317); notably, TTT-Discover with the weaker Qwen3-8B model outperforms ThetaEvolve which used the stronger DeepSeek-R1-0528-Qwen3-8B variant.
- On the GPUMode TriMul kernel engineering competition, TTT-Discover achieves 1161µs on H100 versus the best human submission of 1371µs — a >15% improvement — and 2198µs on A100 versus the best human's 4531µs (>50% faster), generalizing across GPU architectures (A100, H100, B200, MI300X) despite training only on H100 reward signals.
  - The discovered kernels identify memory bandwidth as the primary bottleneck and systematically fuse LayerNorm, sigmoid gating, and output operations while delegating the O(N³) matmul to cuBLAS/rocBLAS in FP16 — a strategy the GPUMode expert reviewers note is similar to the best human approach "but executed better."
- On AtCoder Heuristic Contests (ahc039 and ahc058), TTT-Discover achieves scores of 567,062 and 848,414,228 respectively — both would have placed 1st if submitted during competition, outperforming ShinkaEvolve (which used a multi-model ensemble including frontier models) and ALE-Agent.
- On the OpenProblems single-cell RNA-seq denoising benchmark, TTT-Discover achieves a score of 0.71/0.73 on PBMC

## Key Claims

1. TTT-Discover performs reinforcement learning at test time, allowing the LLM to continue training with experience specific to the test problem, unlike prior work that prompts a frozen LLM.
2. TTT-Discover sets the new state of the art in almost all scientific and engineering problems it attempted, spanning mathematics, GPU kernel engineering, algorithm design, and biology.
3. TTT-Discover achieves a value of 0.380876 on Erdős' minimum overlap problem, surpassing the previous best human result of 0.380927 and previous best AI result of 0.380924.
4. TTT-Discover achieves a GPU kernel runtime of 1161 µs on the GPUMode TriMul competition on H100, faster than the best human result of 1371 µs.
5. TTT-Discover achieves a score of 567,062 on the AtCoder Heuristic Contest 39, slightly surpassing the best human score of 566,997.
6. TTT-Discover achieves a denoising score of 0.71 on the single-cell analysis problem, compared to the best human score of 0.64.
7. All TTT-Discover results are achieved with an open model (OpenAI gpt-oss-120b), in contrast to previous best results that required closed frontier models.
8. The cost of TTT-Discover test-time training runs is only a few hundred dollars per problem.
9. Discovery problems require ideas not only beyond the model's training data but also beyond all existing knowledge of humanity, making out-of-distribution generalization especially hard.
10. Prior evolutionary search methods such as AlphaEvolve store past attempts in a buffer and use them to generate new prompts, but the LLM itself cannot improve because its weights remain frozen.

## Capabilities

- Test-time RL training on a single discovery problem (TTT-Discover) enables an LLM to surpass both human experts and prior AI systems (including AlphaEvolve) across four distinct scientific domains: mathematical open problems, GPU kernel engineering, algorithm engineering competitions, and biological
- An open 120B model (gpt-oss-120b) with test-time RL training achieves scientific discovery results previously requiring closed frontier models (Gemini-2.0 Pro), demonstrating competitive open-model performance on frontier-difficulty discovery tasks.
- AI discovers GPU kernels that outperform top human expert submissions by over 15% across all GPU types, including 50% faster than the best human on A100s, using only H100 training signals that incidentally generalise across architectures.
- AI achieves first-place ranking in real-world competitive algorithm engineering contests (AtCoder Heuristic Contests), surpassing both human experts and prior AI systems that used expensive closed frontier model ensembles.
- State-of-the-art scientific discovery achievable at approximately $500 per problem using test-time RL training on an open model, making frontier-level discovery economically tractable for academic labs.
- Small open 8B model (Qwen3-8B) with TTT-Discover outperforms ThetaEvolve using the same model and surpasses AlphaEvolve's Gemini-based results on autocorrelation inequalities, demonstrating that learning at test time is more compute-efficient than evolutionary search at matched sampling budgets.
- TTT-Discover improved the Erdős minimum overlap upper bound by a margin 16× larger than AlphaEvolve's improvement over prior human work, discovering an asymmetric 600-piece construction where prior AI and human solutions were symmetric — suggesting TTT's exploration mechanism accesses qualitatively 

## Limitations

- TTT-Discover is entirely restricted to problems with continuous, verifiable reward functions — it cannot be applied to open-ended scientific writing, hypothesis generation, experimental design, or any domain lacking a programmatic evaluation oracle.
- Each TTT-Discover run is problem-specific and produces non-transferable weights — the adapted model is discarded after one problem, so the ~$500 cost-per-problem scales linearly with the number of discovery targets, blocking systematic deployment across large scientific workloads.
- MLA-Decode kernels generated by TTT-Discover do not achieve statistically significant improvements over the best human submission on any of three independently tested AMD MI300X instances, indicating the approach fails to reliably beat human experts on certain GPU architectures.
- TTT-Discover's biology benchmark gains are confined to a proxy MSE metric; expert review explicitly warns that metric improvements may not transfer to biologically meaningful downstream tasks, making the scientific value of the discovered algorithm uncertain.
- The 32,768-token context window on the Tinker API forces aggressive prompt compression and token-budget management, truncating reasoning chains and potentially preventing solutions that require extended exploratory traces.
- Setting a fixed entropic objective temperature β that works across task types is empirically intractable — adaptive per-state β scheduling is necessary, adding a hyperparameter that required non-trivial engineering and that ablation shows degrades performance when held constant.
- TTT-Discover made no improvement on the second autocorrelation inequality (C2 = 0.959 vs AlphaEvolve V2's 0.961), demonstrating inconsistent discovery even across closely related mathematical problems within a single paper.
- Cross-architecture kernel generalisation is incidental rather than principled — GPU kernels trained only on H100 hardware 'happened to generalise' to other GPU types, with no guarantee this holds for future problems or more architecture-specific optimisations.
- Discovered MLA-Decode kernels rely on torch.compile() rather than hand-crafted Triton code, limiting fine-grained optimisation and flexible deployment — explicit Triton kernels are faster but TTT-Discover failed to discover competitive ones as the primary output.
- Discovered GPU kernels use FP16 precision to satisfy competition tolerances, but expert review warns this could produce numerical stability issues in full production workloads with wider input ranges — benchmark-optimised solutions may sacrifice robustness for performance.
- Significant instance-level variance across AMD MI300X hardware makes reliable kernel performance evaluation impossible without multi-instance testing — the best kernel differed across three separate instances, making single-instance benchmarking of kernel discovery fundamentally unreliable.
- The method's problem selection is constrained to domains where (a) competitive human baselines exist, (b) evaluation is automated and continuous, and (c) solutions can be expressed as code — excluding the vast majority of scientific discovery problems.

## Bottlenecks

- All test-time RL approaches including TTT-Discover are blocked from application to open-ended scientific domains because RL requires a programmatic reward oracle — precluding use in hypothesis generation, experimental design, or any domain where correctness cannot be automatically verified.
- Non-transferable problem-specific weight updates mean every distinct scientific problem requires a fresh $500 training run with no amortisation across related problems, blocking scalable deployment across large scientific workloads.

## Breakthroughs

- TTT-Discover demonstrates that RL weight updates during inference on a single problem enable LLMs to consistently and substantially exceed frozen-model evolutionary search (AlphaEvolve, Best-of-N, ShinkaEvolve) across diverse scientific discovery domains at matched compute budgets.

## Themes

- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/grpo|GRPO]]
- [[entities/kl-divergence-penalty|KL Divergence Penalty]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/passk|pass@k]]
