---
type: source
title: 'RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive
  Verifiable Environments'
source_id: 01KJT9Y9806J44GMSZR626YZEF
source_type: paper
authors:
- Zhiyuan Zeng
- Hamish Ivison
- Yiping Wang
- Lifan Yuan
- Shuyue Stella Li
- Zhuorui Ye
- Siting Li
- Jacqueline He
- Runlong Zhou
- Tong Chen
- Chenyang Zhao
- Yulia Tsvetkov
- Simon Shaolei Du
- Natasha Jaques
- Hao Peng
- Pang Wei Koh
- Hannaneh Hajishirzi
published_at: '2025-11-10 00:00:00'
theme_ids:
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments

**Authors:** Zhiyuan Zeng, Hamish Ivison, Yiping Wang, Lifan Yuan, Shuyue Stella Li, Zhuorui Ye, Siting Li, Jacqueline He, Runlong Zhou, Tong Chen, Chenyang Zhao, Yulia Tsvetkov, Simon Shaolei Du, Natasha Jaques, Hao Peng, Pang Wei Koh, Hannaneh Hajishirzi
**Published:** 2025-11-10 00:00:00
**Type:** paper

## Analysis

# RLVE: Scaling Up Reinforcement Learning for Language Models with Adaptive Verifiable Environments
2025-11-10 · paper · Zhiyuan Zeng, Hamish Ivison, Yiping Wang, Lifan Yuan, Shuyue Stella Li et al. (17 total)
https://arxiv.org/pdf/2511.07317

---

### Motivation & Prior Limitations
- RL training for language models increasingly saturates on finite training datasets, making it difficult to continue scaling without new data sources or approaches.
  - ProRL-1.5B-v2, trained for over 20,000 H100 GPU hours to saturation on ~136,000 diverse problems, yielded only a 0.49% absolute average improvement across six benchmarks when training was simply continued on the same dataset using 3,600 additional H100 GPU hours.
- Static problem distributions — where difficulty is fixed throughout training — create a fundamental learning signal collapse: problems that were appropriately challenging early in training become trivially easy later, while very hard problems provide consistently poor rewards that block gradient-based updates.
  - The "effective prompt ratio" (fraction of prompts whose rollouts yield non-identical rewards) drops to zero when a model masters the hardest problems in a static distribution, completely stalling learning; static distributions set too high leave only a small fraction of problems at the right difficulty, severely impairing learning efficiency.
- Collecting large-scale RLVR datasets with ground-truth answers is expensive: DeepMath-103K cost roughly $138,000 USD and 127,000 GPU hours to construct, representing a major practical bottleneck for scaling RL data.

---

### Proposed Approach
- RLVE (Reinforcement Learning with Adaptive Verifiable Environments) replaces fixed datasets with procedurally generating environments that (1) produce an unbounded number of problems at configurable difficulty levels and (2) provide algorithmically verifiable rewards — and critically, dynamically adjust difficulty as the policy model's capabilities improve.
  - Each verifiable environment is a tuple E = (I, P, R): an input template I, a problem generator P that samples parameters conditioned on a difficulty level d, and a verifier R (a program, not a lookup against pre-computed answers) that computes scalar rewards for model outputs.
  - Adaptive difficulty is implemented by maintaining a per-environment difficulty range [ℓπ, hπ] during training. When the model's rollout accuracy at the upper-bound level hπ exceeds a threshold τacc (90% in experiments), hπ is incremented by 1; a sliding window of width d∆ prevents the range from growing so wide that hard problems are rarely sampled.
- RLVE-GYM is a manually engineered suite of 400 verifiable environments built on two principles: environments are pedagogical tools for reasoning (the model must manually solve tasks, not replace an executable program) and verification exploits asymmetries between solving and checking — including NP-complete problems (SAT, Hamiltonian path, Sudoku) where verification is polynomial but solving is intractable.
  - Environment sources include programming competitions, mathematical operations (integration, optimization), classical algorithms (sorting), logical puzzles, and NP-complete problems; difficulty scaling is designed so solving any lower-difficulty problem is a subproblem of higher-difficulty ones, ensuring monotone difficulty.
  - The RL algorithm used is DAPO (a GRPO variant) with dynamic sampling that discards prompts with identically-rewarded rollouts; RLVE is algorithm-agnostic and compatible with any RLVR-compatible RL method.
- Environment scaling — increasing the number of distinct training environments — is identified as a separate and critical axis for improving generalizable reasoning beyond simply generating more data from a single environment.

---

### Results & Capabilities
- Starting from ProRL-1.5B-v2 (one of the strongest open-source 1.5B reasoning LMs, already saturated on its training data), RLVE achieves a 3.37% absolute average improvement across six reasoning benchmarks within approximately 1,100 H100 GPU hours — versus only 0.49% absolute improvement from continuing original RLVR training with over 3× the compute (3,600 H100 GPU hours).
  - Benchmarks span mathematics (AIME 2024/2025, OMEGA-500, OlympiadBench), code generation (LiveCodeBench), and logical reasoning (BBEH), confirming transfer to real-world reasoning tasks despite RLVE-GYM environments being synthetic and pedagogical rather than benchmark-aligned.
- In a compute-constrained scenario starting from OpenThinker3-1.5B (the strongest 1.5B SFT model without prior reasoning RL), RLVE outperforms RLVR training on DeepMath-103K by approximately 2% absolute average across the same six benchmarks under identical training setups.
  - RLVE particularly dominates on non-mathematical benchmarks (LiveCodeBench, BBEH), while matching or slightly exceeding DeepMath-103K on most mathematical benchmarks including OMEGA-500 and OlympiadBench; AIME 2024/2025 performance is comparable with RLVE's peak exceeding DeepMath-103K by roughly one point.
  - This is achieved with no benchmark-specific data, while DeepMath-103K was explicitly engineered for mathematical reasoning and cost ~$138,000 USD to construct.
- Adaptive difficulty consistently outperforms all static difficulty baselines (d~[0,1], d~[0,20], d~[0,100]) on both in-distribution and OOD accuracy, and maintains a higher effective prompt ratio throughout training, confirming that the adaptivity mechanism itself — not just access to harder problems — drives the gains.
  - Even when the static distribution is set to [0,20] to oracle-match the range that adaptive difficulty reaches at step 400, static training is consistently outperformed, because different environments define difficulty independently and require per-environment tuning that is impractical at scale.
- Expanding the training environment collection from 1 to 4 to 16 to 256 environments consistently improves OOD accuracy o

## Key Claims

1. Static data distributions in RL training lead to vanishing learning signals when problems become either too easy or too hard for the policy model.
2. In typical LM RL training, the problem distribution is predetermined by a specific dataset and remains static, preventing adaptation to the policy model's evolving capabilities.
3. Models' RL improvement increasingly saturates on finite training data.
4. Adaptive difficulty prevents learning stalls and avoids inefficiency caused by a large proportion of inappropriately challenging problems, compared to any static difficulty distribution.
5. When a static environment has a relatively low upper-bound difficulty, the effective prompt ratio eventually drops to zero as the model masters the hardest problems, causing both ID and OOD accuracies
6. Training with a high static upper-bound difficulty that the model cannot master keeps the effective prompt ratio nonzero but substantially below adaptive difficulty, significantly impairing both learn
7. Expanding the collection of training environments consistently leads to better performance on held-out (OOD) environments, across all model types tested.
8. Scaling the number of training environments is more important for generalizable reasoning than increasing data volume, echoing findings from classical RL research and other LM training stages such as 
9. DeepMath-103K required roughly $138,000 USD and 127,000 GPU hours to build, whereas RLVE-GYM is substantially more cost-efficient to construct.
10. The inference engine typically constitutes the computational bottleneck in LM RL training.

## Capabilities

- Adaptive verifiable environments dynamically adjust RL training problem difficulty to match evolving model capability, preventing saturation on easy problems and training stalls on too-hard ones — maintaining a high effective prompt ratio throughout training
- Scaling the number of distinct verifiable training environments (environment scaling) consistently improves generalizable reasoning on held-out unseen environments, independently of data volume — establishing environment diversity as a new orthogonal scaling axis for RL training
- RLVE joint training across 400 procedural environments achieves 3.37% absolute average improvement on six reasoning benchmarks starting from a model already at RLVR data saturation, with less than one-third the compute of continued RLVR training which yields only 0.49%
- Procedural environment engineering produces RL training capability improvements more cost-efficiently than curated static RLVR datasets — RLVE outperforms DeepMath-103K on non-mathematical benchmarks without the approximately $138,000 and 127,000 GPU-hour build cost

## Limitations

- LLMs cannot reliably automate the construction of high-quality verifiable training environments — they fail at producing unambiguous input templates, reliable problem generators, and robust verifiers, especially environments that exploit solve-verify computational asymmetry
- RLVE is structurally restricted to algorithmically verifiable domains — it cannot be applied to open-ended tasks like creative writing or deep research where no binary correctness criterion can be programmatically checked
- Non-verifiable open-ended environments have no tractable notion of parametric difficulty — difficulty control is structurally undefined for tasks like creative writing, making adaptive curriculum learning impossible outside constrained domains
- Static RL training on finite datasets causes a sharp learning cliff at saturation — effective prompt ratio drops to zero when the model masters the hardest problems in the fixed distribution, causing training to stall completely with no recoverable gradient signal
- High-difficulty static distributions avoid early saturation but suffer severe chronic learning inefficiency — only a small fraction of problems are appropriately challenging, wasting the majority of rollout compute and significantly degrading both in-distribution and OOD performance
- The inference engine — not gradient computation — is the primary computational bottleneck in LM RL training: dynamic sampling requires repeated inference queries to obtain prompts with non-trivial reward variance, with wasted compute scaling inversely with effective prompt ratio
- All RLVE experiments are conducted at 1.5B (primarily) and 7B parameter scales — there is no validation at frontier model scales (70B+) where training dynamics, saturation behaviour, and environment scaling benefits may differ substantially
- Manually engineering high-quality verifiable environments requires substantial expert effort and cannot yet be automated — building 400 environments required a large multi-institution research team, making domain breadth expansion costly and slow
- RLVE-GYM environments are synthetic pedagogical proxies (sorting, integration, Sudoku, Hamiltonian path) deliberately designed to not resemble real LM tasks — the scope of reasoning transfer to real-world use cases is demonstrated empirically on benchmarks but not mechanistically characterised

## Bottlenecks

- Scaling adaptive RL training to new domains is gated on manual expert environment engineering — LLMs cannot reliably automate high-quality verifiable environment construction, particularly environments exploiting solve-verify computational asymmetry
- Adaptive difficulty RL has no tractable extension to non-verifiable open-ended domains — lacking both a correctness oracle and a parametric difficulty axis, the RLVE mechanism structurally cannot operate on creative writing, research, or subjective generation tasks

## Breakthroughs

- Environment diversity — not data volume — is the primary scaling axis for generalizable RL training: expanding the number of distinct verifiable training environments consistently improves OOD reasoning across all model types, while unbounded data from a single environment quickly plateaus
- Adaptive difficulty in verifiable environments is strictly superior to any static difficulty distribution including oracle-tuned ones — demonstrating that difficulty adaptation is a principled necessity, not merely a practical engineering convenience, even when static distributions are configured wi

## Themes

- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
