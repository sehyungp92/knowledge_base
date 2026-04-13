---
type: source
title: Can 1B LLM Surpass 405B LLM? Rethinking Compute-Optimal Test-Time Scaling
source_id: 01KJV47G2KX4WPZ9E3Y2JY5AF1
source_type: paper
authors:
- Runze Liu
- Junqi Gao
- Jian Zhao
- Kaiyan Zhang
- Xiu Li
- Biqing Qi
- Wanli Ouyang
- Bowen Zhou
published_at: '2025-02-10 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Can 1B LLM Surpass 405B LLM? Rethinking Compute-Optimal Test-Time Scaling

This paper establishes a reward-aware framework for compute-optimal test-time scaling (TTS) that jointly optimizes over policy model, process reward model (PRM), and problem difficulty — demonstrating that a 3B LLM can consistently outperform a 405B LLM and a 7B distilled model can beat o1 and DeepSeek-R1, while using 100–1000× fewer total FLOPs.

**Authors:** Runze Liu, Junqi Gao, Jian Zhao, Kaiyan Zhang, Xiu Li, Biqing Qi, Wanli Ouyang, Bowen Zhou
**Published:** 2025-02-10
**Type:** paper

---

## Motivation

Prior work on external TTS (notably Snell et al., 2024) treated compute-optimal scaling as a hyperparameter selection problem over a fixed compute budget, ignoring the reward function as a first-class variable. This created two blind spots:

1. **PRM–policy mismatch was unmodeled.** Off-distribution PRMs reliably degrade search-based TTS, but no framework accounted for this. An on-policy PRM produces more accurate rewards for a given policy model's responses; off-policy use causes search to get trapped in local optima.

2. **Difficulty stratification was broken for strong models.** Quantile-based Pass@1 splits and fixed MATH-dataset difficulty labels become uninformative when a model like Qwen2.5-72B-Instruct achieves Pass@1 above 80% on 76.2% of MATH-500 problems — there is no meaningful "hard" tier at the bottom of the quantile.

The benchmarks used previously were also insufficiently challenging, motivating inclusion of AIME24 alongside MATH-500.

---

## Proposed Framework

The paper formalizes the objective as:

$$\theta^*_{x,\, y^*(x),\, \mathcal{R}}(N) = \arg\max_\theta \;\mathbb{E}_{y \sim \text{Target}(\theta,\, N,\, x,\, \mathcal{R})}[\mathbf{1}_{y = y^*(x)}]$$

making the reward function $\mathcal{R}$ an explicit conditioning variable — hence *reward-aware* compute-optimal TTS.

**Difficulty stratification** uses absolute Pass@1 thresholds rather than quantiles:
- Easy: 50–100%
- Medium: 10–50%
- Hard: 0–10%

**Methods evaluated:** Best-of-N (BoN), beam search, and Diverse Verifier Tree Search (DVTS), across 7 PRMs (1.5B–72B parameters) and 9+ policy models (0.5B–72B), on MATH-500 and AIME24. MCTS is excluded due to multi-step sampling inefficiency.

---

## Key Results

### Small Models Overtaking Giants

The headline result is a systematic demonstration that inference-time compute can substitute for orders-of-magnitude more parameters:

| Policy Model | TTS Result | Comparison |
|---|---|---|
| Llama-3.2-3B-Instruct | 78.2% MATH-500, 30.0% AIME24 | Beats Llama-3.1-405B (71.4% / 23.3%) — 135× parameter gap |
| Qwen2.5-0.5B-Instruct | 76.4% MATH-500 | Beats GPT-4o (74.6%) |
| DeepSeek-R1-Distill-Qwen-7B | 95.2% MATH-500, 83.3% AIME24 | Beats o1 (94.8% / 79.2%) and DeepSeek-R1 |

Total FLOPs for Llama-3.2-3B-Instruct: $1.62 \times 10^{23}$ vs $3.65 \times 10^{25}$ for Llama-3.1-405B — a 100–1000× reduction. Compute-optimal TTS also improves reasoning performance by up to 154.6% over CoT and is up to 256× more compute-efficient than majority voting for small policy models.

### Strategy Depends on Everything

No single TTS method dominates:
- **Small models (<7B), hard problems:** beam search outperforms BoN
- **Large models (72B):** BoN is best across all difficulty levels
- **PRM matters:** BoN dominates with Math-Shepherd and RLHFlow PRMs; search-based methods win with Skywork and Qwen2.5-Math PRMs

### PRM Quality Is Predictable

TTS performance follows a log-linear relationship with PRM quality:

$$Y = 7.66 \log(X) + 44.31$$

where $X$ is the ProcessBench score and $Y$ is MATH-500 accuracy — enabling PRM selection to forecast TTS outcomes before expensive search runs.

### Weak-to-Strong Supervision Signal

A 7B PRM (Qwen2.5-Math-PRM-7B) effectively supervises a 72B policy model, achieving 91.0% on MATH-500. This hints at a viable inversion of the current paradigm where supervision always flows from stronger to weaker models — with significant implications for [[themes/reward_modeling|reward modeling]] and scalable oversight.

---

## Limitations & Open Questions

### Critical Limitations

**PRM generalization failure** is the central practical blocker. PRMs trained on one policy model's outputs fail on others — OOD rewards cause search to find local optima worse than majority voting. Training an on-policy PRM per policy model is computationally prohibitive. This bottleneck directly prevents out-of-the-box deployment of compute-optimal TTS across diverse model families.

**No universal strategy exists.** Optimal method, PRM pairing, and hyperparameters all vary with policy model size, PRM quality, and problem difficulty. This forces expensive per-configuration search and raises the barrier to practical adoption.

**Diminishing returns at scale.** TTS improvement decreases sharply for stronger models: Qwen2.5-72B gains only 9.5% over CoT on MATH-500, vs 141.8% for Qwen2.5-0.5B. The technique's value proposition is concentrated in the small-model regime.

**Distillation gap on hard tasks.** Non-distilled 7B models with TTS achieve 36.7% on AIME24 vs 63.3% for DeepSeek-R1-Distill-7B — TTS cannot substitute for frontier-model distillation on hard competition math.

**PRM length bias.** PRMs develop systematic biases from training data statistics: RLHFlow-PRM-Mistral-8B assigns high rewards to short (often wrong) responses; RLHFlow-PRM-Deepseek-8B generates ~2× more inference tokens due to longer average step length in DeepSeek training data (58.4 vs 46.6 tokens/step). These biases are not detectable without careful analysis.

**The "1B beats 405B" claim is benchmark-scoped.** Llama-3.2-1B with N=512 beats Llama-3.1-405B on MATH-500 but underperforms on AIME24. Hard-task gains do not generalize equally.

### Deployment Constraints

- **Difficulty classification requires oracle Pass@1 data** per problem per model — unavailable at deployment time.
- **Very small models lack answer formatting** (e.g., `\boxed` notation), requiring a secondary 32B LLM for answer extraction — a hidden inference dependency not reflected in reported FLOPs.
- **MCTS not evaluated** — potentially understating achievable TTS performance at high compute budgets.

### Domain Restrictions

All results are on mathematical reasoning. Extension to coding, chemistry, and open-ended domains is explicitly unverified. Reliable PRMs require domains with objective ground truth; this structural dependency blocks compute-optimal TTS from generalizing beyond math and formal proofs for the foreseeable future (3–5 year horizon).

---

## Bottlenecks Identified

**PRM generalization across policy models** — every new policy model requires its own on-policy PRM to avoid OOD degradation, blocking scalable deployment. Horizon: 1–2 years.

**Absence of a universal TTS configuration** — prevents automated, generalizable compute-optimal TTS without expert-guided setup per deployment setting. Horizon: 1–2 years.

**TTS verifier availability outside mathematics** — reliable PRMs only exist for domains with objective ground truth, blocking extension to chemistry, open-ended reasoning, and other domains. Horizon: 3–5 years.

---

## Positioning

Compute-optimal TTS outperforms RL-trained and SFT long-CoT methods (rStar-Math, Eurus-2, SimpleRL, Satori) on both benchmarks, but underperforms DeepSeek-R1 distillation on AIME24 (36.7% vs 63.3% for 7B models). The technique sits above "direct RL or SFT on MCTS-generated data" but below "distillation from a 671B frontier reasoning model" for hard competition math.

---

## Themes

- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/search_and_tree_reasoning|Search & Tree Reasoning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]

## Key Concepts

- [[entities/deepseek-r1-distill|DeepSeek-R1-Distill]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/pass1|Pass@1]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/passk|pass@k]]
