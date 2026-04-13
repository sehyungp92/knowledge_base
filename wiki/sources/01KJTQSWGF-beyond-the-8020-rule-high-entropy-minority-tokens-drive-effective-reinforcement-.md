---
type: source
title: 'Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement
  Learning for LLM Reasoning'
source_id: 01KJTQSWGFZP6G4KFH7FXBA089
source_type: paper
authors:
- Shenzhi Wang
- Le Yu
- Chang Gao
- Chujie Zheng
- Shixuan Liu
- Rui Lu
- Kai Dang
- Xionghui Chen
- Jianxin Yang
- Zhenru Zhang
- Yuqiong Liu
- An Yang
- Andrew Zhao
- Yang Yue
- Shiji Song
- Bowen Yu
- Gao Huang
- Junyang Lin
published_at: '2025-06-02 00:00:00'
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning

**Authors:** Shenzhi Wang, Le Yu, Chang Gao, Chujie Zheng, Shixuan Liu, Rui Lu, Kai Dang, Xionghui Chen, Jianxin Yang, Zhenru Zhang, Yuqiong Liu, An Yang, Andrew Zhao, Yang Yue, Shiji Song, Bowen Yu, Gao Huang, Junyang Lin
**Published:** 2025-06-02 00:00:00
**Type:** paper

## Analysis

# Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning
2025-06-02 · paper · Shenzhi Wang, Le Yu, Chang Gao, Chujie Zheng, Shixuan Liu et al. (18 total)
https://arxiv.org/pdf/2506.01939

---

### Motivation & Prior Limitations
- Existing RLVR implementations train over all tokens uniformly, without understanding which tokens actually facilitate reasoning, treating all positions in a chain-of-thought as equally important.
  - Prior algorithmic work (DAPO, VAPO, GRPO) focuses on objective design or sampling strategies, leaving the question of token-level contribution to reasoning performance entirely unaddressed.
  - This neglect of heterogeneous token roles potentially hinders performance by failing to prioritize critical decision points in sequential reasoning trajectories.
- The mechanisms by which RLVR improves reasoning are poorly understood, limiting principled improvements to the training procedure.
  - Related work analyzing RLVR (Gandhi et al., Li et al.) identifies that format matters more than content, but operates at the sequence or structural level rather than the token level.

---

### Proposed Approach
- The paper introduces a token-entropy perspective on RLVR, identifying high-entropy tokens as "forking tokens" — positions where the model faces genuine uncertainty between multiple reasoning pathways — and restricts policy gradient updates exclusively to these tokens.
  - Token entropy is computed as $H_t = -\sum_{j=1}^{V} p_{t,j} \log p_{t,j}$ for each position using the training policy's output distribution, not the sampled token identity, making it a measure of the model's local uncertainty rather than a property of the token itself.
  - The method modifies the DAPO objective by masking gradients for all but the top-$\rho$ fraction of highest-entropy tokens within each batch (with $\rho = 20\%$ in main experiments), adjusting both the advantage term via an indicator function and the token-count normalization accordingly.
  - Unlike entropy bonus (which increases entropy uniformly across all tokens) or KL penalty approaches, this method targets only the high-entropy minority that already governs reasoning direction, leaving the low-entropy majority undisturbed.
- The paper first establishes two empirical entropy patterns in CoT reasoning through analysis of over $10^6$ tokens from Qwen3-8B: the majority of tokens ($>50\%$) have entropy below $10^{-2}$, while only 20% have entropy above 0.672; and high-entropy tokens lexically correspond to logical connectors and pivots ("wait," "however," "suppose," "since") rather than word completions or mathematical subexpressions.
  - Controlled temperature-modulation experiments confirm the causal role of forking tokens: increasing temperature selectively on high-entropy positions improves AIME scores, while doing so on low-entropy positions causes incoherence.

---

### Results & Capabilities
- Training with only the top 20% highest-entropy tokens matches or surpasses full-gradient DAPO across all three model scales tested, with gains that grow substantially with model size.
  - Qwen3-32B: +7.71 on AIME'24 (55.83 → 63.54) and +11.04 on AIME'25 (45.63 → 56.67), setting a new SoTA for RLVR on base models under 600B parameters; extending max response length from 20k to 29k further raises AIME'24 to 68.12.
  - Qwen3-14B: +5.21 on AIME'24, +4.79 on AIME'25; Qwen3-8B: approximately neutral (within ~1 point), consistent with the hypothesis that smaller models lack capacity to exploit increased exploration.
- Training exclusively on the bottom 80% low-entropy tokens causes severe performance degradation across all model sizes, despite those tokens constituting 80% of the gradient signal in standard RLVR.
  - This asymmetry — 20% of tokens driving all gains while 80% contribute nothing or are harmful — constitutes the central empirical claim of the paper.
- RLVR training largely preserves the base model's entropy patterns: at convergence (step 1360), over 86% of top-20% high-entropy positions are shared between the base and final RLVR model, and RLVR disproportionately increases the entropy of already-high-entropy tokens while leaving low-entropy tokens nearly unchanged.
  - This finding supports the view that RLVR refines rather than restructures the reasoning topology established during pretraining.
- The forking-token approach generalizes out-of-distribution: models trained on DAPO-Math-17K with only top 10–20% high-entropy tokens outperform vanilla DAPO on LiveCodeBench (coding), suggesting the high-entropy signal is domain-general for reasoning.
- An ablation over $\rho \in \{10\%, 20\%, 50\%, 100\%\}$ shows that 20% optimally balances exploration (measured by overall entropy trajectory during training) and final performance; deviating in either direction reduces overall entropy and degrades results.
  - The clip-higher mechanism in DAPO is identified as preferable to entropy bonus precisely because it preferentially raises importance ratios for high-entropy tokens, whereas entropy bonus uniformly perturbs all tokens including the low-entropy majority.

---

### Implications
- The identification of forking tokens as the locus of RLVR's effect provides a mechanistic explanation for why RL generalizes while SFT memorizes: RL preserves or amplifies entropy at forking positions, maintaining flexibility of reasoning paths, whereas SFT collapses logit distributions toward one-hot targets, eliminating that flexibility.
- Token entropy offers a computationally cheap, model-intrinsic signal for identifying which positions matter in reasoning, without requiring output-correctness labels or external classifiers — this could be used to improve not only RLVR but also inference-time sampling, distillation targeting, and SFT curriculum design.
- The strong scaling trend (gains increasing from 8B to 14B to 32B) suggests that the forking-token strategy becomes more valuable as model capacity increase

## Key Claims

1. In Chain-of-Thought reasoning, only a minority of tokens exhibit high entropy while the majority are generated with low entropy, with over 50% of tokens having entropy below 10^-2 and only 20% having 
2. High-entropy tokens in CoT reasoning function as pivotal decision points ('forks') that determine the trajectory of reasoning among multiple potential pathways, while low-entropy tokens tend to comple
3. High-entropy tokens in CoT reasoning include logical connectors such as 'wait', 'however', 'unless', 'thus', 'since', 'suppose', 'assume', and 'define', while low-entropy tokens are often word suffixe
4. Moderately increasing the temperature (entropy) of forking tokens during decoding leads to measurable improvements in reasoning performance, while artificially reducing their entropy results in perfor
5. RLVR largely preserves the base model's entropy patterns, with the positions of the top 20% high-entropy tokens overlapping by more than 86% between the base model and the converged RLVR model.
6. RLVR predominantly alters the entropy of high-entropy tokens, while the entropy of low-entropy tokens remains comparatively stable with minimal variation throughout training.
7. Training RLVR using only the top 20% highest-entropy (forking) tokens in the policy gradient loss achieves performance comparable to full-gradient updates on Qwen3-8B and significantly surpasses full-
8. Training exclusively on the bottom 80% lowest-entropy tokens leads to a marked decline in RLVR reasoning performance, demonstrating that low-entropy tokens contribute minimally or even negatively to r
9. The RLVR forking-token approach exhibits a strong scaling trend: performance gains over vanilla DAPO increase with model size, with the 32B model showing the largest improvements and 8B showing the sm
10. A Qwen3-32B model trained with DAPO using only the top 20% forking tokens achieves AIME'24 score of 63.5 and AIME'25 score of 56.7, setting a new state-of-the-art for reasoning models trained from bas

## Capabilities

- RLVR training restricted to the top 20% highest-entropy 'forking' tokens achieves performance comparable to or significantly exceeding full-gradient RLVR, with gains of +11.04 on AIME'25 and +7.71 on AIME'24 for Qwen3-32B, and a strong positive scaling trend with model size
- Qwen3-32B trained with forking-token RLVR sets new SoTA for reasoning models under 600B parameters: 63.5 on AIME'24 and 56.7 on AIME'25, further improving to 68.1 on AIME'24 with a 29k token response length budget
- Token entropy analysis of Chain-of-Thought reasoning mechanistically identifies 'forking tokens' — the critical ~20% minority that determine reasoning trajectory — with a quantitative entropy threshold (80th percentile) distinguishing them from near-deterministic continuation tokens
- Applying higher decoding temperature selectively to high-entropy forking tokens while maintaining lower temperature for low-entropy tokens measurably improves mathematical reasoning; the reverse (lowering forking-token temperature) causes sharp performance degradation
- Forking-token RLVR trained exclusively on math data generalises out-of-distribution to coding benchmarks (LiveCodeBench), significantly outperforming vanilla full-gradient DAPO despite using only 10–20% of tokens in gradient updates

## Limitations

- Standard RLVR implementations uniformly apply policy gradient updates to all tokens, wasting the majority of gradient compute on the ~80% low-entropy tokens that contribute minimally or negatively to reasoning improvement
- Uniformly applied entropy bonus in RLVR is suboptimal and can degrade performance by raising entropy for the low-entropy majority of tokens that should remain near-deterministic
- Small models (~8B parameters) show minimal benefit from forking-token RLVR compared to full-gradient training, suggesting a model-capacity bottleneck on the ability to exploit exploration diversity
- RLVR cannot create fundamentally new reasoning decision points — it can only amplify existing high-entropy positions from the base model, meaning base model pretraining quality sets a hard ceiling on RL-driven capability expansion
- SFT collapses entropy at forking tokens toward one-hot distributions, permanently reducing reasoning path flexibility and degrading out-of-distribution generalisation — a structural limitation relative to RLVR
- Forking-token findings are validated only on the Qwen model family; application to Llama-3.1-8B required cold-start SFT and yielded less convincing AIME results, limiting generalisability claims
- Results are restricted to mathematical reasoning; application to programming, ARC-AGI, or open-ended tasks with different entropy distributions remains untested and the 20% threshold may not transfer
- The optimal forking-token fraction (20%) occupies a narrow operating range — reducing to 10% weakens exploration by removing useful tokens, while increasing to 50–100% dilutes signal with low-entropy noise, producing sharp performance cliffs in both directions
- RLVR mechanisms remain fundamentally poorly understood — the paper's findings are empirical characterisations that explain what happens at the token level but not why the base model's entropy pattern has the specific structure it does, or what controls the forking token distribution

## Bottlenecks

- Uniform token-level gradient application in RLVR wastes compute on the ~80% low-entropy majority that contribute minimally to reasoning, while nearly all performance gains come from the high-entropy 20% minority — standard RLVR is systematically compute-inefficient
- RLVR capability expansion is fundamentally bounded by the base model's pretraining entropy patterns — RLVR can amplify existing forking-token diversity but cannot create new decision points, making base model pretraining quality the hard ceiling for what RL can achieve in reasoning

## Breakthroughs

- Discovery that in RLVR training, only ~20% of tokens ('forking tokens', identified by high entropy) drive essentially all reasoning performance gains — training on only this minority matches or significantly outperforms full-gradient RLVR with a strong positive scaling trend across model sizes
- Mechanistic characterisation of LLM CoT token entropy as bimodal: >50% of tokens have entropy below 0.01 (near-deterministic word completions) while only 20% exceed 0.672 (genuine branching decision points), fundamentally distinguishing LLM reasoning from traditional RL and explaining why uniform ex

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/amc-2023|AMC 2023]]
- [[entities/chain-of-thought-cot-reasoning|Chain-of-Thought (CoT) Reasoning]]
- [[entities/cold-start-sft|Cold-Start SFT]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/math500|MATH500]]
- [[entities/minerva|Minerva]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/qwen3|Qwen3]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/verl|verl]]
