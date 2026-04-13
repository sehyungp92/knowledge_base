---
type: source
title: Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning
source_id: 01KJV3AME561KWT5RJ1EJ0BTQ3
source_type: paper
authors:
- Yuxiao Qu
- Matthew Y. R. Yang
- Amrith Setlur
- Lewis Tunstall
- Edward Emanuel Beeching
- Ruslan Salakhutdinov
- Aviral Kumar
published_at: '2025-03-10 00:00:00'
theme_ids:
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning

**Authors:** Yuxiao Qu, Matthew Y. R. Yang, Amrith Setlur, Lewis Tunstall, Edward Emanuel Beeching, Ruslan Salakhutdinov, Aviral Kumar
**Published:** 2025-03-10 00:00:00
**Type:** paper

## Analysis

# Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning
2025-03-10 · paper · Yuxiao Qu, Matthew Y. R. Yang, Amrith Setlur, Lewis Tunstall, Edward Emanuel Beeching et al. (7 total)
https://arxiv.org/pdf/2503.07572

---

### Motivation & Prior Limitations
- Standard outcome-reward RL (e.g., GRPO with 0/1 correctness reward) does not efficiently utilize test-time compute because it only incentivizes eventual success, not meaningful progress toward it.
  - Analysis of DeepSeek-R1-Distill-Qwen-32B on AIME 2024 and OmniMATH shows that for problems requiring many reasoning episodes (41–45 episodes), accuracy does not increase—and sometimes degrades—with each additional episode generated, meaning the model fails to make steady progress.
  - A naive strategy of majority voting over fewer, shorter episodes often outperforms long sequential chains of thought on a FLOPs-matched basis, indicating that existing SoTA models are not implementing even simple explore-exploit strategies.
- Training with a fixed token budget and only outcome reward creates a misalignment between training and deployment: models trained this way lack incentive to develop succinct responses for easy problems, yet may also prematurely commit to an approach on hard problems without discovering better alternatives.
  - Explicitly adding a length penalty to address token inefficiency reduces accuracy (e.g., DeepScaleR-1.5B length-penalized GRPO drops avg. benchmark score by 3.7 points relative to the base model), confirming that length control and accuracy are in tension under outcome-only reward.
- Prior work fine-tuning LLMs on search traces risks memorization of unfamiliar behavior and is limited in generalization; RL-based approaches that reward self-correction (SCoRe, RISE) focus each episode on its own outcome reward, making them too exploitative and not budget-agnostic.

---

### Proposed Approach
- The paper formalizes optimizing test-time compute as a **meta-reinforcement learning (meta-RL)** problem, viewing the LLM's output stream as a sequence of episodes implementing an in-context explore-exploit algorithm on each test problem.
  - This reframing allows cumulative regret—the cumulative gap between the probability of success of the current model and an oracle comparator, summed over episodes—to serve as a principled metric for evaluating test-time compute efficacy.
  - The key insight is that minimizing cumulative regret is equivalent to maximizing steady "progress": each episode should increase the probability that a meta-prover policy μ (the same LLM, forced to terminate its thinking block and produce its best guess) arrives at the correct answer.
- **Meta Reinforcement Fine-Tuning (MRT)** augments the standard outcome-reward RL objective with a dense progress reward bonus defined as the change in the meta-prover's probability of success before and after a given episode: r_prg(z_j; c) = J_r(μ(·|z_j, c)) − J_r(μ(·|c)).
  - Unlike step-level reward methods (e.g., Setlur et al.'s process reward model), progress is measured across episodes (complete reasoning blocks) rather than within a single attempt, operating at the meta-step level.
  - Unlike E-RL² (which only rewards the last episode, encouraging pure exploration) or RL² (which rewards every episode equally, encouraging pure exploitation), MRT strikes a balance by assigning information-gain-based rewards that reflect actual progress.
- Two concrete instantiations are developed: an **STaR variant** that filters self-generated traces by maximum cumulative progress and eventual correctness before running SFT, and an **RL variant** (on top of GRPO or PPO) that computes progress bonuses by sampling rollouts that either continue reasoning or terminate immediately at a prefix, then normalizes rewards across these rollouts to implicitly compute the progress bonus without branched rollouts.
  - The meta-prover μ is implemented practically by appending a "time is up" prompt suffix to the thinking trace and forcing the model to produce its best-guess answer—a mechanism analogous to how R1-style models are forced to terminate thinking in deployment.

---

### Results & Capabilities
- MRT consistently outperforms outcome-reward RL (GRPO) across all evaluated math benchmarks, with **2–3× larger relative gains over the base model** compared to GRPO's gains.
  - On DeepScaleR-1.5B-Preview fine-tuned on 919 AIME problems: MRT improves the average benchmark score by +1.4 points over the base vs. +0.5 for GRPO, achieving state-of-the-art for its size class on AIME 2024 (47.2%), AIME 2025 (39.7%), and AMC 2023 (83.1%).
  - On DeepSeek-R1-Distill-Qwen-1.5B fine-tuned on 4,000 NuminaMath problems: MRT achieves +2.2 avg. improvement vs. +1.1 for GRPO, with particularly strong gains on AMC 2023 (+3.0 vs. +0.6).
- MRT achieves **1.5× better token efficiency than GRPO** and **5× better token efficiency than the base model**, reducing output length while improving accuracy—unlike length penalties, which reduce length at the cost of accuracy.
  - In the backtracking search setting with Llama-3.1-8B (STaR) and 3B (RL) models, MRT improves linearized evaluation token efficiency by **1.6–1.7× over both RISE and GRPO**.
- MRT produces models with lower normalized cumulative regret at all tested token budgets (4K–16K) and continues to have the lowest regret when **extrapolated to 2× the training token budget** (up to 32K tokens) via budget forcing, demonstrating budget-agnostic generalization.
- The ablation showing that a training curriculum over token budget (e.g., DeepScaleR's 8K→16K schedule) implicitly maximizes progress and minimizes cumulative regret provides a theoretical explanation for an empirically observed but previously unexplained phenomenon: the 8K-trained checkpoint attains lower normalized regret than the 16K-trained checkpoint even when extrapolated to 16K evaluation tokens.

---

### Implications
- Formalizing test-time compute as meta-RL introduces a principled, quan

## Key Claims

1. Current methods for training models to use test-time compute via fine-tuning on search traces or outcome-reward RL do not efficiently utilize test-time compute.
2. The problem of optimizing test-time compute can be formalized as a meta-reinforcement learning (RL) problem.
3. Cumulative regret over output tokens is a principled measure of the efficacy of test-time compute usage.
4. Minimizing cumulative regret provides the best balance between exploration and exploitation in the token stream, analogous to how RL algorithms balance exploration and exploitation over training.
5. State-of-the-art LLMs trained with outcome-reward RL do not minimize cumulative regret.
6. The progress dense reward bonus is quantified by the change in the likelihood of eventual success for each subsequent block in the output stream.
7. MRT achieves a 2-3x relative gain in performance and roughly 1.5x gain in token efficiency for math reasoning compared to outcome-reward RL.
8. Training models with only outcome reward at a fixed token budget is suboptimal because it encourages redundancy and inefficient token use on problems where the typical solution length is below the max
9. Outcome-reward RL cannot differentiate between solutions that are on track versus not on track if both succeed or both fail.
10. A budget-agnostic LLM strategy can guarantee optimal performance for any test-time compute budget.

## Capabilities

- Meta Reinforcement Fine-Tuning (MRT) achieves 2–3x relative performance gain over outcome-reward RL (GRPO) for math reasoning by training with dense progress rewards rather than sparse outcome rewards, reaching state-of-the-art at 1.5B parameter scale across AIME 2024, AIME 2025, and AMC 2023
- Dense progress reward training produces budget-agnostic LLMs that continue improving even when deployed at token budgets 2x larger than those seen during training, without any budget-specific fine-tuning
- MRT achieves roughly 5x token efficiency improvement over the base model and 1.5x over GRPO-trained models on AIME 2024 while maintaining or improving accuracy — demonstrating that progress-based training reduces redundant token generation without sacrificing peak performance
- Cumulative regret over the output token stream serves as a principled metric for quantifying the efficacy of test-time compute use, enabling comparative evaluation of how efficiently existing reasoning models translate token budget into performance gains
- Backtracking-parameterised MRT with Markovian episode structure enables linearised sliding-window evaluation beyond training context length, supporting arbitrarily long sequential reasoning chains by discarding context between episodes

## Limitations

- SoTA models fine-tuned with outcome-reward RL fail to make steady progress with additional reasoning episodes — on complex problems requiring 41–45 episodes, accuracy does not increase and sometimes degrades with each subsequent episode, directly contradicting the implicit assumption that more reaso
- Long sequential chain-of-thought reasoning trained with outcome reward loses to naive majority voting over fewer episodes for complex problems — a long sequential reasoning trace cannot implement strategies that are trivially achievable by parallel sampling, revealing structural inefficiency
- Training LLMs with a fixed token budget commits them to that budget at deployment — models trained at 16K may fail to terminate at smaller budgets or waste tokens at larger ones, because outcome-reward RL provides no incentive to develop succinct, difficulty-proportional responses
- MRT requires substantially more train-time compute than outcome-reward RL due to multi-episode sampling and progress estimation via meta-prover rollouts, with no FLOPs-matched evaluation confirming that the gains survive this additional cost
- MRT is exclusively demonstrated on mathematical reasoning; there is no evidence it generalises to coding, agentic tasks, scientific reasoning, or open-ended language tasks, and the method structurally requires verifiable rewards that do not exist for most real-world domains
- Explicit length penalties consistently worsen pass@1 accuracy while improving token efficiency, revealing that there is no free lunch in token efficiency optimisation via reward shaping alone
- The optimal design of the meta-prover policy μ in MRT is an open question — using the same underlying LLM with forced termination is a simplification, and no alternative μ designs or μ-free parameterisations have been systematically explored
- Base models used in MRT produce only a narrow set of test-time strategies, capping the benefit of meta-RL orchestration — MRT's advantage over outcome-reward RL would be substantially larger if the base model had a richer strategic repertoire
- MRT's open-ended parameterisation cannot support linearised sliding-window evaluation beyond context length because open-ended episodes lack Markov structure — only the constrained backtracking variant supports true extrapolation beyond training context
- Completion length oscillates during RL training rather than monotonically decreasing, and length alone does not predict accuracy — standard proxy metrics for monitoring RL training quality are unreliable for reasoning models
- Fine-tuning on search traces that are structurally unfamiliar to the base model leads to memorisation rather than generalisation of reasoning strategies, limiting the effectiveness of SFT-based approaches to test-time compute scaling
- Applying dense rewards at end-of-trace (rather than per-episode) substantially increases policy gradient variance, degrading learning efficiency — but the alternative (true per-episode branched rollouts) is computationally expensive and lacks efficient implementation

## Bottlenecks

- Outcome-reward RL provides no training signal to incentivise steady per-episode progress — models are trained to eventually succeed but not to make each reasoning episode constructively advance toward the solution, creating a hard ceiling on test-time compute scaling efficiency
- No principled, scalable mechanism for training budget-agnostic reasoning models — current RL fine-tuning commits models to specific token budget regimes, making them systematically suboptimal when deployed at different budgets from those used during training

## Breakthroughs

- MRT formalises test-time compute optimisation as a meta-RL problem and introduces cumulative regret as a principled metric, empirically demonstrating that SoTA outcome-reward RL models systematically fail to optimise this metric — and providing a dense progress reward bonus that substantially correc

## Themes

- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/budget-forcing|Budget Forcing]]
- [[entities/grpo|GRPO]]
- [[entities/numinamath|NuminaMATH]]
- [[entities/omnimath|OmniMath]]
- [[entities/score|SCoRe]]
- [[entities/star|STaR]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
