---
type: source
title: 'FlowRL: Matching Reward Distributions for LLM Reasoning'
source_id: 01KJTF5CHPXC8WZR89PTDGTKM8
source_type: paper
authors:
- Xuekai Zhu
- Daixuan Cheng
- Dinghuai Zhang
- Hengli Li
- Kaiyan Zhang
- Che Jiang
- Youbang Sun
- Ermo Hua
- Yuxin Zuo
- Xingtai Lv
- Qizheng Zhang
- Lin Chen
- Fanghao Shao
- Bo Xue
- Yunchong Song
- Zhenjie Yang
- Ganqu Cui
- Ning Ding
- Jianfeng Gao
- Xiaodong Liu
- Bowen Zhou
- Hongyuan Mei
- Zhouhan Lin
published_at: '2025-09-18 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# FlowRL: Matching Reward Distributions for LLM Reasoning

**Authors:** Xuekai Zhu, Daixuan Cheng, Dinghuai Zhang, Hengli Li, Kaiyan Zhang, Che Jiang, Youbang Sun, Ermo Hua, Yuxin Zuo, Xingtai Lv, Qizheng Zhang, Lin Chen, Fanghao Shao, Bo Xue, Yunchong Song, Zhenjie Yang, Ganqu Cui, Ning Ding, Jianfeng Gao, Xiaodong Liu, Bowen Zhou, Hongyuan Mei, Zhouhan Lin
**Published:** 2025-09-18 00:00:00
**Type:** paper

## Analysis

# FlowRL: Matching Reward Distributions for LLM Reasoning
2025-09-18 · paper · Xuekai Zhu, Daixuan Cheng, Dinghuai Zhang, Hengli Li, Kaiyan Zhang et al. (23 total)
https://arxiv.org/pdf/2509.15207

---

### Motivation & Prior Limitations
Reward-maximizing RL methods (PPO, GRPO, REINFORCE) used for LLM post-training systematically overfit to dominant reward modes, producing mode collapse and reducing diversity among generated reasoning paths.
- GRPO's advantage normalization and clipping concentrate probability mass on high-reward solutions while neglecting less frequent but valid reasoning trajectories, as visualized by KL divergence of 8.68 versus FlowRL's 0.11 between policy and reward distribution.
- In long chain-of-thought reasoning specifically, entropy-based regularization techniques struggle to counteract reward-maximizing pressure because the extended trajectory length (up to 8K tokens) dilutes the regularization signal.
- Prior GFlowNet-based approaches to language model fine-tuning operated on short sequences in small discrete spaces, leaving gradient explosion and off-policy sampling mismatch as unsolved problems when naively applying trajectory balance to long CoT generation.

---

### Proposed Approach
FlowRL reframes LLM policy optimization as reward distribution matching rather than reward maximization, using a learnable partition function to normalize scalar rewards into a target distribution and minimizing reverse KL divergence between the policy and that distribution.
- The core objective is π_θ(y|x) ∝ exp(βr(x,y)), achieved by introducing a learnable 3-layer MLP partition function Z_φ(x) that estimates the normalizing constant, avoiding the need to enumerate all trajectories explicitly.
- A gradient equivalence proof (Proposition 1) connects this KL objective to the trajectory balance loss from GFlowNets, reformulating distribution matching as minimizing `(log Z_φ(x) + log π_θ(y|x) − βr̂(x,y) − log π_ref(y|x))²`, which is a stable squared loss rather than direct KL optimization.
- Two practical extensions adapt the trajectory balance objective to long CoT training: length normalization rescales log π_θ(y|x) by 1/|y| to prevent gradient norms from scaling with sequence length, and importance sampling with PPO-style clipping reweights off-policy rollouts using a gradient-detached ratio w = clip(π_θ/π_old, 1−ε, 1+ε) to enable data-efficient multi-step micro-batch updates.
- The reference model π_ref is incorporated directly into the reward shaping term as exp(βr(x,y)) · π_ref(y|x), constraining the target distribution to remain close to the pretrained model's prior.

---

### Results & Capabilities
FlowRL achieves a 10.0% average improvement over GRPO and 5.1% over PPO on six math reasoning benchmarks using Qwen2.5-32B-Base, and outperforms all baselines on three code reasoning benchmarks using DeepSeek-R1-Distill-Qwen-7B.
- On math tasks with the 32B model, FlowRL reaches 48.39% average Avg@16 accuracy versus GRPO's 38.34% and PPO's 43.25%, with particularly large gains on Olympiad (+30.46% over backbone) and Minerva (+11.22% over backbone).
- On code tasks, FlowRL achieves a Codeforces rating of 1549.47 (83.3rd percentile) versus PPO's 1403.07 (73.7th percentile) and GRPO's 1313.82 (67.1th percentile), and scores 37.43% Avg@16 on LiveCodeBench versus GRPO's 32.75%.
- Ablation shows importance sampling is critical: removing it drops average math accuracy from 35.63% to 26.71% on the 7B model, confirming that correcting for distribution mismatch between rollout generation and policy training is essential to the method's effectiveness.
- GPT-4o-mini-judged diversity scores on AIME 24/25 rollouts show FlowRL scoring 2.28 versus PPO's 1.31, GRPO's 1.23, and REINFORCE++'s 1.11 — nearly doubling the strongest baseline — providing direct empirical evidence that the distribution-matching objective achieves mode coverage rather than mode collapse.
- A qualitative case study on an AIME box geometry problem shows GRPO applying AM-GM three times and cycling through identity loops without progress, while FlowRL introduces the symmetry assumption a=b, derives and solves a cubic equation a³−27a+46=0, and reaches the correct answer of 721.

---

### Implications
FlowRL demonstrates that framing LLM post-training as distribution matching rather than reward maximization is a viable and empirically superior alternative to PPO/GRPO, suggesting that the RLHF and RLVR communities have been operating under an unnecessarily restrictive optimization paradigm.
- The GFlowNet trajectory balance formulation provides a theoretically grounded connection between generative modeling and policy optimization, opening a path for richer cross-pollination between probabilistic generative modeling methods and RL-based LLM training.
- The finding that diversity of reasoning trajectories directly predicts downstream benchmark performance strengthens the case that self-play and expert iteration approaches should explicitly reward or measure diversity rather than treating it as a byproduct of entropy regularization.
- Length normalization and importance sampling as developed here are domain-agnostic adaptations of GFlowNet objectives to long-sequence generation, potentially enabling GFlowNet-style training in other long-horizon generation tasks beyond math and code.
- The use of a lightweight 3-layer MLP as the learnable partition function Z_φ demonstrates that the computational overhead of distribution matching over reward maximization is minimal, lowering the barrier to adoption.

---

### Remaining Limitations & Next Steps
The paper evaluates only on math and code reasoning domains using outcome-based (binary correct/incorrect) reward signals, leaving open whether distribution matching generalizes to tasks with dense, continuous, or multi-objective reward functions such as instruction following or RLHF from human preferences.
- All experiments use models in the 7B–32B range trained on publicly available cura

## Key Claims

1. FlowRL achieves a 10.0% average improvement over GRPO and 5.1% over PPO on math benchmarks.
2. FlowRL transforms scalar rewards into a normalized target distribution using a learnable partition function and minimizes the reverse KL divergence between the policy and the target distribution.
3. Minimizing the KL objective between the policy and the reward-weighted distribution is gradient-equivalent to minimizing the trajectory balance loss from GFlowNets.
4. Applying trajectory balance directly to long CoT reasoning causes exploding gradients because the log-probability term scales with sequence length.
5. FlowRL uses length normalization to address gradient explosion by rescaling log-probabilities with respect to sequence length.
6. The trajectory balance objective assumes fully on-policy sampling, creating a sampling mismatch when integrated into existing RL pipelines that reuse trajectories from an old policy.
7. FlowRL employs importance sampling with PPO-style clipping to correct for distribution mismatch between generated rollouts and the current policy.
8. Removing importance sampling causes a large performance drop in FlowRL, from 35.63% to 26.71% average accuracy on math benchmarks.
9. FlowRL with β=15 achieves the best performance among tested hyperparameter values.
10. FlowRL achieves an average math accuracy of 48.39% with the 32B model, surpassing PPO (43.25%) and GRPO (38.34%).

## Capabilities

- FlowRL performs reward distribution matching via a learnable partition function and GFlowNets trajectory balance objective, achieving +10.0% over GRPO and +5.1% over PPO on math benchmarks and consistently higher performance on code reasoning tasks at both 7B and 32B scale
- Flow-balanced RL optimization generates nearly 2× more diverse reasoning trajectories than reward-maximizing baselines (diversity score 2.28 vs 1.31 for PPO), enabling qualitatively different solution strategies rather than minor variations of dominant patterns
- Length normalization of sequence-level log-probabilities by response length prevents gradient explosion in long CoT RL training (up to 8K tokens), enabling stable trajectory balance optimization that was previously unstable at this scale
- GFlowNets trajectory balance objective is proven equivalent in expected gradients to minimizing reverse KL divergence between policy and reward-weighted distribution, providing a tractable surrogate for distribution-matching RL over intractable trajectory spaces

## Limitations

- Reward-maximizing RL methods (PPO, GRPO) systematically collapse to dominant reward modes, neglecting less frequent but valid reasoning paths and producing repetitive solution patterns that fail on hard problems requiring novel approaches
- Trajectory balance objective applied naively to long CoT reasoning (up to 8K tokens) causes gradient explosion because log-probability decomposes into a token-wise sum whose gradient norm scales with sequence length
- Trajectory balance objective assumes fully on-policy sampling, creating a fundamental mismatch with standard RL pipelines that reuse trajectories from an older policy for data efficiency (micro-batch updates)
- Enumerating or sampling all valid reasoning trajectories to recover the true reward distribution is computationally intractable, requiring the distribution to be approximated through a learnable partition function
- Standard entropy regularization is ineffective for long CoT reasoning — the regularization signal cannot meaningfully counteract mode collapse when trajectory lengths exceed ~8K tokens
- Removing importance sampling from FlowRL causes a catastrophic 8.9pp accuracy drop (35.63% → 26.71%), meaning the method is brittle without off-policy correction and cannot be used in its basic form without this component
- FlowRL is evaluated exclusively on verifiable domains (math, code) with clean scalar rewards; applicability to open-ended tasks relying on human preference signals is entirely undemonstrated and theoretically unclear
- FlowRL performance is meaningfully sensitive to the β hyperparameter controlling reward sharpness in the target distribution, with suboptimal values causing up to 4.3pp degradation (β=5: 31.34% vs β=15: 35.63%)
- Training 32B models with FlowRL requires 4 nodes with 32 H800 80GB GPUs, limiting practical access to large-scale compute infrastructure
- GRPO's mode collapse produces qualitatively degraded reasoning behavior — models apply familiar heuristics (AM-GM inequality) repetitively and enter algebraic identity loops, reaching logical contradictions rather than exploring alternative problem decompositions

## Bottlenecks

- Mode collapse in reward-maximizing RL (PPO, GRPO) systematically prevents diverse exploration of reasoning strategies — models over-exploit dominant solution patterns, failing to generalize to hard problems that require qualitatively different approaches
- Trajectory-level RL objectives face gradient explosion when applied to long CoT sequences (>8K tokens), because sequence-level log-probability sums accumulate gradients proportionally to sequence length — a regime prior GFlowNets research never encountered

## Breakthroughs

- FlowRL demonstrates that replacing reward maximization with reward distribution matching via GFlowNets trajectory balance produces consistent, substantial gains in both reasoning performance (+10% over GRPO, +5.1% over PPO) and solution diversity (~2×), establishing distribution matching as a superi

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/grpo|GRPO]]
- [[entities/minerva|Minerva]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
- [[entities/verl|verl]]
