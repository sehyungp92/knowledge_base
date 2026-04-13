---
type: source
title: Training Language Models to Self-Correct via Reinforcement Learning
source_id: 01KJV83GN1RMMXTNYQWH3W34F5
source_type: paper
authors:
- Aviral Kumar
- Vincent Zhuang
- Rishabh Agarwal
- Yi Su
- John D Co-Reyes
- Avi Singh
- Kate Baumli
- Shariq Iqbal
- Colton Bishop
- Rebecca Roelofs
- Lei M Zhang
- Kay McKinney
- Disha Shrivastava
- Cosmin Paduraru
- George Tucker
- Doina Precup
- Feryal Behbahani
- Aleksandra Faust
published_at: '2024-09-19 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Training Language Models to Self-Correct via Reinforcement Learning

This paper diagnoses why intrinsic self-correction fails in LLMs and proposes SCoRe (Self-Correction via Reinforcement Learning), a two-stage multi-turn RL procedure that trains a single model to genuinely revise its own outputs using entirely self-generated data — achieving the first significantly positive intrinsic self-correction results in the literature on both math and code benchmarks.

**Authors:** Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D Co-Reyes, Avi Singh, Kate Baumli, Shariq Iqbal, Colton Bishop, Rebecca Roelofs, Lei M Zhang, Kay McKinney, Disha Shrivastava, Cosmin Paduraru, George Tucker, Doina Precup, Feryal Behbahani, Aleksandra Faust
**Published:** 2024-09-19
**Type:** Paper
**Link:** https://arxiv.org/pdf/2409.12917

---

## Why Intrinsic Self-Correction Has Failed

The paper opens by documenting a consistent empirical failure: LLMs cannot reliably improve their own outputs without external feedback. Base Gemini 1.5 Flash exhibits a **−11.2% Δ(t1,t2)** — meaning self-correction actively hurts it. Naive prompting approaches like Self-Refine produce −1.0% delta and either degrade performance or secretly depend on privileged oracle information (e.g., ground-truth answers during refinement), rendering their reported gains misleading.

Fine-tuning approaches that avoid external supervision fail in two structural ways:

**Distribution shift.** Models trained on offline correction traces learn to fix errors made by the *data-collection policy* — but at inference time, they must correct their *own* (different) errors. The trained model's error distribution diverges from training data, so correction gains vanish. STaR applied to self-correction achieves only +0.4% Δ(t1,t2) on MATH; Pair-SFT achieves only +1.8%.

**Behavior collapse.** Whether via SFT or standard multi-turn RL, models converge to a degenerate strategy: produce the best possible first attempt, then make superficial or no edits on the second attempt. This achieves high reward without learning any correction meta-strategy. The phenomenon is structurally analogous to memorization in meta-learning — the "direct" strategy (optimize t1, copy to t2) is always at least as reward-optimal as the correction strategy on training data, so learning is biased toward it by default.

A further symptom: STaR-style training on successful correction traces does not reduce the c→i (correct→incorrect) degradation rate. Δ(c→i) remains at 19.6% for STaR versus 15.8% for the base model, indicating the model has no learned sense of *when not* to modify a correct answer.

---

## SCoRe: The Approach

SCoRe eliminates all external supervision requirements. A single model is trained to both solve and self-correct using on-policy, self-generated data throughout — so correction training always operates on errors the model actually makes.

The key insight is that genuine self-correction requires *decoupling* the two attempts before optimizing them jointly. Without decoupling, multi-turn RL immediately collapses to the degenerate strategy.

### Stage I: Decoupled Initialization

Stage I trains the model to produce high-reward second attempts while holding the first-attempt distribution *fixed* via a strict KL-divergence penalty against the base model. The optimization problem is:

$$\max_\pi \mathbb{E}[r(y_2)] - \beta \cdot \text{KL}(\pi(\cdot | x, y_1) \| \pi_{\text{base}}(\cdot | x, y_1))$$

with $y_1$ sampled from the base model. This forces the two attempts to become functionally decoupled — the model learns to correct without yet being allowed to optimize first attempts — creating an initialization that resists collapse when joint training begins.

### Stage II: Joint Multi-Turn RL with Reward Shaping

Stage II runs joint multi-turn RL from the Stage I checkpoint, using REINFORCE with a KL penalty against a reference policy (extended to the multi-turn MDP formalism). The critical addition is a **progress-based reward bonus** at the second attempt:

$$\hat{b}(y_2|y_1, y^*) = \alpha \cdot (\hat{r}(y_2, y^*) - \hat{r}(y_1, y^*))$$

This bonus positively rewards i→c (incorrect→correct) transitions and heavily penalizes c→i transitions. Rather than rewarding absolute correctness at t2, it rewards *improvement* — biasing optimization toward learning the correction meta-strategy over the degenerate direct-answer strategy.

All three components are load-bearing. Ablations show: removing multi-turn training yields Δ(t1,t2) = −2.4%; removing Stage I drops Δ(t1,t2) from 4.4% to 2.2%; removing reward shaping drops it to 2.6%.

---

## Results

| Setting | Metric | Base Model | SCoRe |
|---|---|---|---|
| MATH (Gemini 1.5 Flash) | Accuracy@t2 | 41.4% | 64.4% |
| MATH | Δ(t1,t2) | −11.2% | **+4.4%** |
| MATH | i→c correction rate | 4.6% | 5.8% |
| MATH | c→i degradation | 15.8% | **1.4%** |
| HumanEval (Gemini 1.0 Pro) | Δ(t1,t2) | +3.1% | **+12.2%** |
| MBPP-R (offline repair) | Accuracy | 47.3% | 60.6% |

The +4.4% Δ(t1,t2) on MATH is described as the first significantly positive intrinsic self-correction result in the literature. The dramatic reduction in c→i degradation (15.8% → 1.4%) is equally important: SCoRe doesn't just correct more errors, it also learns when *not* to change a correct answer.

**Cross-task generalization.** SCoRe trained only on MBPP generalizes to HumanEval (+12.2% Δ), suggesting the correction meta-strategy is transferable across code tasks.

**Inference efficiency.** Combining sequential self-correction with parallel sampling is strictly more compute-efficient than parallel-only sampling. With a 32-sample budget on MATH, parallel-only sampling yields +7.4% accuracy; combining parallel with one round of sequential self-correction yields +10.5%. Some of the inference budget is better spent on correction than on additional independent samples.

---

## Capabilities

- **[[themes/reinforcement_learning|Reinforcement Learning]] for intrinsic self-correction** — Multi-turn on-policy RL (SCoRe) enables genuine self-correction without oracle feedback, achieving +4.4% Δ(t1,t2) on MATH and +12.2% on HumanEval (maturity: research_only)
- **Progress-based reward shaping** — Rewarding improvement transitions rather than final correctness prevents behavior collapse and enables stable self-correction policy learning (maturity: research_only)
- **Compute-efficient inference scaling** — Sequential self-correction combined with parallel sampling outperforms parallel-only inference at equal compute budgets (maturity: research_only)

---

## Limitations and Open Questions

**Requires verifiable rewards.** SCoRe depends on binary reward signals — answer checkers for math, test case execution for code. This restricts applicability to domains with automated verification and cannot be extended to open-ended generation without a substitute reward signal. This is currently a **blocking limitation** for generalizing the approach.

**Single-round only.** Training is limited to two turns (one correction round) due to infrastructural constraints. Whether stable multi-turn RL can be extended to longer correction chains remains untested and is an active bottleneck for leveraging sequential test-time compute more fully.

**Two-stage overhead.** Stage I and Stage II must be run sequentially, introducing operational overhead and potential optimization misalignment. Unifying them into a single procedure is noted as future work.

**Offline repair vs. online self-correction gap.** Pair-SFT achieves strong offline repair performance (MBPP-R: 59.8%) but *degrades* online self-correction by −1.8% Δ. This reveals a fundamental gap: performance on static repair benchmarks does not predict on-policy correction ability, and benchmark choice matters critically when evaluating self-correction methods.

**Latent knowledge elicitation.** The paper observes that LLMs often possess the knowledge needed for correct solutions but fail to elicit it without external framing — sub-problems succeed with hints but fail from scratch. SCoRe makes progress here but the underlying generation bottleneck remains partially open.

---

## Connections and Implications

### For [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]

SCoRe is an early demonstration that [[themes/reinforcement_learning|RL]] can instill generalizable *meta-strategies* — not just object-level task performance — in language models. The behavior collapse phenomenon establishes that any multi-turn meta-strategy learning (not just self-correction) requires explicit regularization to suppress shortcut solutions. This has direct implications for training models to backtrack, decompose problems, or iteratively refine hypotheses.

### For [[themes/post_training_methods|Post-Training Methods]]

The distribution shift failure of SFT-based self-correction is a specific instance of a general problem: offline fine-tuning on traces generated by a different policy produces policies that perform well on training data but fail at inference time. SCoRe's on-policy RL framing is the natural remedy, at the cost of infrastructure complexity.

### For [[themes/reasoning_and_planning|Reasoning and Planning]]

The reward shaping formulation — rewarding *correctness transitions* rather than absolute correctness — is a general design pattern for any multi-turn RL problem where a sequential improvement strategy must be distinguished from a degenerate direct-answer strategy. It may generalize to planning, multi-step tool use, and iterative hypothesis testing.

### For [[themes/policy_optimization|Policy Optimization]]

The Stage I KL-constrained decoupling step is a structural solution to the collapse problem in multi-turn RL. It is analogous to the role of initialization in non-convex optimization: the basin of attraction matters, and naïve initialization leads to degenerate local optima. The two-stage formulation may generalize to other multi-turn RL settings where joint optimization over correlated decisions is unstable.

---

## Open Bottlenecks

**Behavior collapse as a general barrier.** [[themes/reinforcement_learning|RL]]-trained LLMs on multi-turn objectives consistently collapse to degenerate single-turn solutions unless explicit structural interventions are applied. This is the fundamental barrier to training models to learn any generalizable meta-strategy (self-correction, backtracking, iterative refinement). SCoRe resolves this for two-turn correction, but the general multi-turn case remains open. (Horizon: 1–2 years)

**Covariate shift in offline self-correction training.** Error distributions from data-collection policies differ systematically from errors made by the trained model, making all SFT-based approaches structurally inadequate. Scalable alternatives to on-policy RL sampling for this domain remain an active research problem. (Horizon: 1–2 years)

**Multi-round iterative self-correction.** Extending SCoRe-style training to more than two turns is blocked by infrastructure complexity and training instability. (Horizon: months)

---

## Themes

- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/finetuning_and_distillation|Finetuning and Distillation]]
- [[themes/policy_optimization|Policy Optimization]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]

## Key Concepts

- [[entities/math-dataset|MATH Dataset]]
- [[entities/score|SCoRe]]
- [[entities/star|STaR]]
- [[entities/self-consistency-decoding|Self-Consistency Decoding]]
- [[entities/self-refine|Self-Refine]]
