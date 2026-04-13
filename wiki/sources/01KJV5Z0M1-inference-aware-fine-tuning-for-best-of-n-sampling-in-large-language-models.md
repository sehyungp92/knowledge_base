---
type: source
title: Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models
source_id: 01KJV5Z0M13PSHR7W5AF96FMPP
source_type: paper
authors:
- Yinlam Chow
- Guy Tennenholtz
- Izzeddin Gur
- Vincent Zhuang
- Bo Dai
- Sridhar Thiagarajan
- Craig Boutilier
- Rishabh Agarwal
- Aviral Kumar
- Aleksandra Faust
published_at: '2024-12-18 00:00:00'
theme_ids:
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models

> This paper introduces inference-aware fine-tuning, a training paradigm that directly co-optimises LLM objectives with the Best-of-N (BoN) inference strategy rather than treating inference as a post-hoc design choice. By resolving the non-differentiability of BoN selection via a variational formulation, the authors derive five concrete algorithms that measurably improve both accuracy and diversity on math reasoning and code generation — while revealing that standard SFT and RL actively degrade BoN performance by collapsing output diversity.

**Authors:** Yinlam Chow, Guy Tennenholtz, Izzeddin Gur, Vincent Zhuang, Bo Dai, Sridhar Thiagarajan, Craig Boutilier, Rishabh Agarwal, Aviral Kumar, Aleksandra Faust
**Published:** 2024-12-18
**Type:** paper
**Themes:** [[themes/finetuning_and_distillation|Fine-tuning & Distillation]] · [[themes/policy_optimization|Policy Optimization]] · [[themes/post_training_methods|Post-Training Methods]] · [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/reinforcement_learning|Reinforcement Learning]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Motivation

Standard fine-tuning (SFT and RL) is agnostic to the inference strategy used at deployment. If a model will be evaluated under Best-of-N sampling — selecting the best response from N independent samples — training it to produce a single optimal response is systematically suboptimal. No prior fine-tuning paradigm had formalised or optimised for this gap.

The stakes are high: prior work (Snell et al., 2024) suggests investing in inference-time compute may prove more beneficial than scaling pretraining compute. Yet the models being deployed under BoN inference are not trained for it. Worse, the paper demonstrates that naively applying standard SFT and RL makes things actively worse: standard SFT degrades BoN performance relative to the base model through overfitting, and RL with N'=1 collapses output diversity by over-optimising for immediate reward.

The core technical obstacle is the non-differentiability of the argmax operator in the BoN selection procedure, which makes direct gradient-based optimisation of BoN objectives intractable.

---

## Approach

### Variational BoN Formulation

The paper resolves the non-differentiability of argmax via a variational approximation of the BoN policy:

$$\pi_{\text{bon}}(y|x) \propto \pi(y|x) \cdot \exp(\lambda_N Q^\pi(x,y))$$

where $Q^\pi(x,y)$ is the expected win-rate of response $y$ over the base policy under the verifier score, and $\lambda_N$ scales monotonically with N. This decomposes the gradient into two interpretable terms: one pushing toward expert likelihood (exploitation) and one regularising toward exploratory, high-win-rate responses — directly encoding the exploration-exploitation trade-off in the objective itself.

### Five Algorithms

| Algorithm | Setting | Key Property |
|---|---|---|
| **BoN-SFT** | Offline, verifier-based, positive examples only | Baseline inference-aware SFT |
| **BoN-RL-V** | Online RL with separate verifier | Optimises robustness to verifier selection |
| **BoN-RL-S** | Online RL with environment reward | Uses task feedback instead of verifier |
| **BoN-RLB** | Binary reward, closed-form gradient | Asymmetric difficulty-weighted updates (positive + negative examples) |
| **BoN-RLB(P)** | Binary reward, closed-form, positive only | Most sample-efficient variant |

BoN-RLB's gradient has a particularly illuminating structure: harder problems (high $P_{\text{fail}}$) have their positive samples upweighted exponentially and their negative samples penalised aggressively, driving implicit exploration without explicit exploration mechanisms.

### Co-Scaling Law

The paper also formalises a power-law co-scaling law for BoN:

$$\text{pass@}N(T) \approx \exp(a(T) \cdot N^{b(T)})$$

quantifying the interaction between temperature $T$ and sample count $N$. Optimal temperature is positively correlated with both N and problem difficulty — easy problems cluster at low $(T^*, N^*)$; hard problems require high $(T^*, N^*)$.

---

## Results

On Hendrycks MATH (Gemma 2B):

- **BoN-RL-V** (N'=32): Bo32 accuracy 26.8% → **30.8%**; pass@1 also improves 22% → 26%, suggesting broadly better policy not just N-specific overfitting
- **BoN-RL-S** (N'=32): pass@32 60.0% → **67.0%**; standard RL (N'=1) slightly *degrades* pass@32
- Standard inference-unaware RL-V fails due to reward hacking

On HumanEval code generation (Gemma 2B):

- **BoN-RLB(P)**: pass@16 61.6% → **67.1%**
- Standard RL (N'=1): pass@16 degrades to 59.8%

BoN-aware models also **generalise** to held-out benchmarks (Functional MATH, MathOdyssey) and to non-training temperatures ($T \in \{0.1, 1.0, 1.5\}$).

An emergent finding: BoN-aware models implicitly learn a meta-strategy that interleaves high-quality exploitative responses with diverse exploratory responses suited to BoN selection — a behaviour not explicitly trained for, analogous to exploration-exploitation in RL.

---

## Limitations & Open Questions

**Immediately significant:**

- **Verifier sensitivity.** The training verifier must match the test-time verifier — BoN methods using environment reward (BoN-RL-S, BoN-RLB) show substantially worse BoN *accuracy* than BoN-RL-V, which uses the verifier directly. At high temperatures, verifiers make Type II errors (selecting random noisy outputs), corrupting the gradient signal.
- **Binary reward restriction.** The efficient closed-form gradient (BoN-RLB) requires binary success/failure metrics. Continuous or non-binary reward domains must use the general BoN-RL formulation, which is sample-inefficient.
- **Sample inefficiency at large N.** Estimating both the value baseline and policy gradient requires repeated sampling from the BoN distribution, imposing quadratic-like overhead as N grows. Current experiments are limited to N ≤ 32.
- **BoN-RL-V accuracy vs. diversity trade-off.** Optimising for verifier robustness and optimising for output diversity are partially opposing objectives — BoN-RL-V improves accuracy but does not significantly improve pass@N.

**Scale and scope gaps:**

- All experiments use Gemma 2B and 9B — effectiveness at frontier scale (70B+) is untested.
- Evaluation is confined to tasks with automatic grading (math answer matching, code unit tests). Performance on tasks without binary verifiers — open-ended generation, multi-step agentic tasks — is unknown.
- The inference-aware paradigm is only instantiated for BoN. The paper explicitly defers more complex inference algorithms (MCTS, critique-and-revise, tree search) to future work.

---

## Bottlenecks Addressed & Remaining

**Partially resolved:** The core disconnect between single-response training objectives and multi-sample inference strategies — the paper provides a principled formulation and demonstrates it works. But the approach is currently limited to small models and binary-reward domains.

**Still blocking:**

- Scaling inference-aware training to frontier models (70B+) or large N — quadratic sampling cost is the primary obstacle (horizon: 1-2 years)
- Extending the paradigm beyond BoN to richer inference graphs (MCTS, beam search, iterative refinement) — formalisation not yet attempted (horizon: 1-2 years)
- Applying inference-aware training outside narrow verifier-supported domains — verifier quality remains the hard ceiling, and no path to open-ended tasks is demonstrated (horizon: 3-5 years)

---

## Implications

**For practitioners:** The finding that standard SFT and RL (N'=1) actively degrade BoN performance is a cautionary result. If a system will use multi-sample inference at deployment, the training procedure should account for it — and off-the-shelf RLHF pipelines may be counterproductive.

**For the test-time compute scaling literature:** The co-scaling law between $T$ and $N$ provides theoretically grounded guidance for choosing inference hyperparameters, complementing broader scaling law research. It also suggests that the gains attributed to inference-time compute in prior work may be substantially understated relative to what inference-*aware* training could unlock.

**For the training paradigm more broadly:** Inference strategy as a first-class citizen of the training objective is a design principle with implications beyond BoN — any system combining LLM generation with search, re-ranking, or verification could in principle benefit from co-optimised training.

---

## Key Claims

1. Decoupling training from inference-time computation is suboptimal; fine-tuning should account for the inference strategy to be used at test time.
2. Standard SFT (N'=1) *degrades* BoN performance relative to the base model — overfitting reduces diversity needed for multi-sample selection.
3. Standard RL (N'=1) *reduces* pass@16 on HumanEval from 61.6% to 59.8% by collapsing output distribution toward exploitative modes.
4. BoN-aware fine-tuning improves Bo32 MATH accuracy 26.8% → 30.8%, pass@32 60.0% → 67.0%, and pass@16 HumanEval 61.6% → 67.1%.
5. pass@N follows $\exp(a(T) \cdot N^{b(T)})$; optimal temperature is positively correlated with N and problem difficulty.
6. BoN-aware models implicitly learn a meta-strategy interleaving exploitative and exploratory responses — an emergent behaviour from the objective structure.
7. Training-time and test-time verifiers must match; verifier mismatch substantially degrades BoN accuracy gains.
8. Inference-time compute may be more beneficial than pretraining compute scaling (citing Snell et al., 2024).

## Key Concepts

- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/reinforce|REINFORCE]]
- [[entities/restem|ReSTEM]]
- [[entities/star|STaR]]
