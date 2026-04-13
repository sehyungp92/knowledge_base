---
type: source
title: 'Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning'
source_id: 01KJTFKNRPVQ69FKYFEDB0X5RW
source_type: paper
authors:
- Xin Qiu
- Yulu Gan
- Conor F. Hayes
- Qiyao Liang
- Yinggan Xu
- Roberto Dailey
- Elliot Meyerson
- Babak Hodjat
- Risto Miikkulainen
published_at: '2025-09-29 00:00:00'
theme_ids:
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning

**Authors:** Xin Qiu, Yulu Gan, Conor F. Hayes, Qiyao Liang, Yinggan Xu, Roberto Dailey, Elliot Meyerson, Babak Hodjat, Risto Miikkulainen
**Published:** 2025-09-29 00:00:00
**Type:** paper

## Analysis

# Evolution Strategies at Scale: LLM Fine-Tuning Beyond Reinforcement Learning
2025-09-29 · paper · Xin Qiu, Yulu Gan, Conor F. Hayes, Qiyao Liang, Yinggan Xu et al. (9 total)
https://arxiv.org/pdf/2509.24372

---

### Motivation & Prior Limitations
Reinforcement learning has become the dominant LLM fine-tuning paradigm but carries four compounding failure modes that this paper frames as fundamental rather than incidental.
- RL methods suffer from low sample efficiency and high gradient estimator variance when rewards are sparse and long-horizon, as is typical in outcome-only fine-tuning; credit assignment at the token level is difficult and may be actively counterproductive.
  - Prior theoretical analysis (Vemula et al., 2019) showed that parameter-space exploration complexity scales quadratically with parameter count, while action-space exploration scales quartically with horizon — a basis for the orthodox view that ES could not work at LLM scale.
- RL fine-tuning performance is inconsistent across base LLMs, with Gandhi et al. (2025) documenting that RL methods simply fail to improve certain models on the Countdown benchmark.
- RL systematically incentivizes reward hacking — learning to game the reward function rather than acquire the intended behavior — when no explicit penalty is added.
- RL fine-tuning is often unstable across multiple runs under identical hyperparameters, substantially increasing effective compute cost (Choshen et al., 2020; Zhong et al., 2025).
- Evolution Strategies (ES) was widely assumed to be inapplicable to billion-parameter LLMs: prior successful ES applications topped out at a few million parameters, and workarounds (final-layer-only ES, low-rank adapter ES, action-space evolutionary search) all avoided direct optimization of the full parameter space.

---

### Proposed Approach
This paper scales ES to full-parameter fine-tuning of LLMs at the multi-billion-parameter scale for the first time, without any dimensionality reduction, through a memory-efficient implementation of a simplified Natural Evolution Strategies (NES) variant based on the OpenAI ES design (Salimans et al., 2017).
- The core algorithm samples N perturbed models per iteration by adding i.i.d. Gaussian noise to all parameters, evaluates each perturbed model to obtain a reward score, normalizes rewards via z-score, and updates parameters as a noise-weighted sum — requiring only inference, no backpropagation or gradient computation.
  - This contrasts with RL methods (PPO, GRPO) which operate in action space and require gradient calculations; ES operates entirely in parameter space, making reward hacking structurally harder because it optimizes a solution distribution rather than a single solution.
- Seven engineering adaptations make the approach feasible at scale: random-seed-based noise retrieval (storing seeds rather than full noise tensors), fully parallel GPU evaluation across population members, layer-level in-place perturbation and restoration to minimize peak GPU memory, z-score reward normalization across iterations, greedy (deterministic) decoding so all performance variance is attributable to parameter-space exploration rather than sampling stochasticity, decomposed layer-by-layer parameter updates, and absorption of the noise scale σ into the learning rate to simplify parameterization.
- The population size used is N=30 across all experiments — orders of magnitude smaller than the N≥10,000 used in prior ES work on million-parameter models — demonstrating that the approach is practically feasible without massive compute.
- Common algorithmic enhancements from OpenAI ES (rank transformation, mirrored sampling, weight decay, virtual batch normalization, Adam optimizer) are intentionally withheld to isolate the core ES contribution and demonstrate a performance floor.

---

### Results & Capabilities
ES outperforms all tested RL baselines (PPO, GRPO with group sizes 8 and 30, Dr.GRPO) across all seven evaluated models on the Countdown symbolic reasoning benchmark, using a single fixed hyperparameter configuration while RL required per-model grid search.
- On the Countdown task, ES achieved 14.4%, 37.3%, 60.5%, 66.8% accuracy for Qwen-2.5 at 0.5B, 1.5B, 3B, and 7B respectively; the best RL baseline (Dr.GRPO-v) reached 13.5%, 31.0%, 43.8%, and 57.5% for the same models — ES margins range from ~6 to ~17 percentage points across the Qwen family.
- ES similarly outperformed all RL baselines on the Llama-3.2 (1B, 3B) and Llama-3.1-8B models, achieving 16.8%, 51.6%, and 61.2% versus Dr.GRPO-v's 13.9%, 47.8%, and 50.2%.
- ES is robust across model families and sizes: where RL failed to improve some models, ES delivered consistent gains across the full Qwen-2.5 and Llama-3 families.
- ES maintains consistent fine-tuning behavior without reward hacking, in contrast to RL which requires explicit penalties to suppress degenerate reward-gaming strategies; this behavioral stability arises structurally from optimizing a population distribution.
- ES training runs are more consistent across random seeds than RL runs, reducing the expected compute cost of fine-tuning by eliminating the need to run multiple trials and discard failed runs.
- The approach was additionally applied to two challenging puzzle problems that base LLMs fail on, and used to fine-tune for response conciseness, demonstrating generalization beyond math reasoning benchmarks.

---

### Implications
The central implication is that the design space of post-training algorithms is significantly larger than previously assumed — gradient-based and RL-based methods are not the only viable paradigm, and backpropagation-free optimization of full LLM parameters is now a legitimate research and engineering direction.
- For RLHF and reward modeling pipelines, ES offers a structural mitigation for reward hacking: because ES optimizes a distribution of solutions rather than a single policy, the optimization pressure is distributed in a way that 

## Key Claims

1. Evolution Strategies (ES) can successfully fine-tune LLMs at the billion-parameter scale through direct full-parameter optimization without dimensionality reduction.
2. RL methods incur low sample efficiency and high variance of the gradient estimator when handling long-horizon rewards, which is common in LLM fine-tuning with outcome-only rewards.
3. Token-level credit assignment for RL fine-tuning methods is difficult and possibly unhelpful.
4. RL fine-tuning techniques are sensitive to the choice of base LLMs, resulting in inconsistent fine-tuning performance across different models.
5. RL fine-tuning techniques tend to incentivize hacking the reward function, leading to undesirable behaviors.
6. RL fine-tuning is often unstable across multiple runs even with identical hyperparameter settings, significantly increasing fine-tuning cost.
7. ES was previously assumed to be unscalable to modern LLM sizes because prior applications typically contained no more than a few million parameters.
8. The assumed complexity of parameter-space exploration increases quadratically with the number of parameters, making ES appear infeasible for billion-parameter LLMs.
9. ES can find good solutions in multi-billion-parameter spaces using a population size as small as 30, whereas previous ES implementations required populations of 10,000 or more for models with millions
10. ES only requires inference for fine-tuning, requiring no gradient calculations, which saves significant GPU memory.

## Capabilities

- Evolution Strategies (ES) can directly optimize the full parameter space of multi-billion-parameter LLMs during fine-tuning without dimensionality reduction, achieving strong post-training performance across Qwen2.5 (0.5B–7B) and Llama3 (1B–8B) families
- ES fine-tuning maintains stable, non-reward-hacking behavior because it optimizes a solution distribution (population) rather than a single solution, making reward exploitation structurally harder than in RL
- ES fine-tuning requires only inference (no gradient calculations or backpropagation), significantly reducing GPU memory requirements compared to RL-based post-training methods
- A single fixed hyperparameter set (N=30, σ=0.001, α=5×10⁻⁴) enables effective ES fine-tuning across diverse LLM families and sizes, while RL requires per-model hyperparameter sweeps to function at all
- A population size of just 30 is sufficient for ES to achieve strong fine-tuning in multi-billion-parameter LLMs, compared to the 10,000+ population sizes required in previous ES applications on models with only millions of parameters

## Limitations

- ES fine-tuning is validated only up to 8B parameter models; scaling to 70B+ parameters is unproven, and theoretical analysis shows parameter-space exploration complexity increases quadratically with parameter count
- ES evaluation uses greedy decoding exclusively; all performance differences arise from parameter-space exploration rather than stochastic sampling, and behavior under temperature-based decoding is uncharacterized
- ES fine-tuning is evaluated only on symbolic reasoning and math tasks (Countdown, math benchmarks); there is no evidence it transfers to instruction following, creative generation, code synthesis, or preference-based alignment
- ES fine-tuning has not been demonstrated for human preference learning (RLHF) settings where rewards come from a learned reward model rather than verifiable outcome-based signals
- ES fine-tuning requires N parallel inference passes per iteration (N=30 in experiments); compute cost scales with population size, model size, and sequence length, making costs at 70B+ scale potentially prohibitive without large GPU clusters
- The ES implementation intentionally excludes established algorithmic enhancements (rank transformation, mirrored sampling, Adam optimizer, weight decay, virtual batch normalisation), meaning reported numbers are a conservative lower bound of optimised ES performance
- RL fine-tuning (PPO, GRPO) has low sample efficiency and high gradient variance when handling long-horizon sparse outcome rewards, and token-level credit assignment is both difficult and possibly counterproductive
- RL fine-tuning performance is sensitive to the choice of base LLM, producing inconsistent results across model families and failing entirely on some base models without per-model hyperparameter tuning
- RL fine-tuning is unstable across multiple runs with identical hyperparameters, significantly increasing expected total compute cost due to failed or suboptimal training runs

## Bottlenecks

- ES fine-tuning has only been validated at up to 8B parameter scale; whether parameter-space exploration remains effective or computationally feasible at 70B+ parameters is unknown, blocking adoption as a practical post-training paradigm for frontier-scale LLMs
- ES fine-tuning as demonstrated requires verifiable, outcome-based reward signals; no evidence for ES with learned reward models (RLHF-style) blocks broader adoption for instruction-following and preference alignment use cases

## Breakthroughs

- First successful application of Evolution Strategies to full-parameter fine-tuning of multi-billion-parameter LLMs without dimensionality reduction, directly overturning the assumption that ES is inherently unscalable to modern model sizes

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/kl-divergence-penalty|KL-Divergence Penalty]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/reward-hacking|Reward Hacking]]
