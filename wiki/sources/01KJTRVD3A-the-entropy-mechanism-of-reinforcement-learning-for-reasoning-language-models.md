---
type: source
title: The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models
source_id: 01KJTRVD3AM86939WPGGACX5SP
source_type: paper
authors:
- Ganqu Cui
- Yuchen Zhang
- Jiacheng Chen
- Lifan Yuan
- Zhi Wang
- Yuxin Zuo
- Haozhan Li
- Yuchen Fan
- Huayu Chen
- Weize Chen
- Zhiyuan Liu
- Hao Peng
- Lei Bai
- Wanli Ouyang
- Yu Cheng
- Bowen Zhou
- Ning Ding
published_at: '2025-05-28 00:00:00'
theme_ids:
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models

**Authors:** Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang, Yuxin Zuo, Haozhan Li, Yuchen Fan, Huayu Chen, Weize Chen, Zhiyuan Liu, Hao Peng, Lei Bai, Wanli Ouyang, Yu Cheng, Bowen Zhou, Ning Ding
**Published:** 2025-05-28 00:00:00
**Type:** paper

## Analysis

# The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models
2025-05-28 · paper · Ganqu Cui, Yuchen Zhang, Jiacheng Chen, Lifan Yuan, Zhi Wang et al. (17 total)
https://arxiv.org/pdf/2505.22617

---

### Motivation & Prior Limitations
- Scaling RL compute for LLM reasoning is blocked by a consistent and previously understudied phenomenon: policy entropy collapses to near zero within the first few hundred gradient steps, causing the policy to become overconfident and exploration to cease.
  - Across 11 base models (0.5B–32B), 4 model families, and 4 RL algorithms, over 93% of performance gains and 94% of entropy loss occur in the first third of training, leaving the remaining two-thirds of compute yielding negligible returns.
  - Standard entropy interventions from classical RL — entropy loss and KL penalty against a reference model — are shown to be ineffective: small coefficients barely affect entropy, large coefficients cause entropy explosion or performance degradation, and none reliably improve final accuracy.
- The underlying mechanism driving this collapse was not theoretically characterized for softmax LLM policies, leaving practitioners without principled tools to counteract it.

---

### Proposed Approach
- The paper establishes an empirical law R = −a exp(H) + b linking validation performance R to policy entropy H, then derives a theoretical account of why entropy decays monotonically, and uses this understanding to design two token-level covariance regularization techniques.
  - The empirical law is fitted across all tested model families and tasks using only two coefficients, with log-linear scaling of the coefficients a and b with model size — directly paralleling neural scaling laws and enabling performance prediction across model scales from smaller runs.
  - Theoretically, entropy change under policy gradient algorithms is shown to be proportional to the covariance between a token's log-probability and its advantage-weighted logit change: high-probability tokens with high advantage (high covariance) drive entropy down, while low-probability tokens with high advantage increase it.
- **Clip-Cov** randomly detaches a small fraction (∼2×10⁻⁴) of tokens with high covariance from the gradient computation, preventing their outsized contribution to entropy collapse. **KL-Cov** instead applies a KL penalty against the rollout policy specifically to the top-k (∼2×10⁻³) highest-covariance tokens, imposing a soft update constraint on the most entropy-compressing actions.
  - Both methods modify only ∼10⁻⁴ to 10⁻³ of tokens per batch yet produce dramatically different entropy trajectories, revealing that a small set of "pivotal" tokens dominates the entropy dynamics of LLMs.
  - Unlike the related clip-higher technique (which raises the PPO importance sampling upper bound, indirectly including more low-covariance tokens), Clip-Cov and KL-Cov use covariance directly as the selection criterion, giving finer-grained control over entropy.

---

### Results & Capabilities
- Both Clip-Cov and KL-Cov outperform vanilla GRPO and the clip-higher baseline across all 7 mathematical reasoning benchmarks tested, with improvements that scale with model size.
  - For Qwen2.5-7B, average accuracy improves by +2.0% over GRPO (40.4% for Clip-Cov, 40.6% for KL-Cov vs. 38.6% baseline).
  - For Qwen2.5-32B, average improvement reaches +6.4% over GRPO (50.3% Clip-Cov, 52.2% KL-Cov vs. 45.8% baseline), with AIME 2024 and AIME 2025 gains of approximately 15% and 14.6% respectively — the authors attribute the larger gains to the 32B model's greater pre-training potential being unlocked once exploration is sustained.
- The fitted entropy-performance curve enables accurate early-stage prediction: using only the first 15% of training steps (36 steps), final performance can be predicted with average RMSE of 0.9% on math and 1.2% on coding across the Qwen2.5 family.
- Empirical validation of the theoretical covariance derivation shows the measured covariance term and the step-wise entropy difference track each other closely throughout training; covariance remains consistently positive, directly explaining monotonic entropy decay.
- KL-Cov produces stabler entropy curves than Clip-Cov across training, and both methods correlate with longer response lengths, consistent with the model exploring more diverse reasoning paths rather than converging early.

---

### Implications
- Policy entropy is a fundamental bottleneck for RL compute scaling in LLMs — not merely a hyperparameter concern — and managing it is a prerequisite for continued performance gains from increased post-training compute, analogous to how data and parameter scaling laws constrain pre-training.
- The R = −a exp(H) + b law, with model-size-dependent coefficients scaling log-linearly, suggests a new class of RL scaling laws specific to the post-training regime, enabling cross-scale extrapolation of RL performance from small-model experiments before committing to large runs.
- The ceiling imposed by entropy collapse provides conditional support for the hypothesis that RL merely elicits latent pre-training knowledge, but the authors reframe this: the ceiling is an artifact of the entropy mechanism of softmax LLMs, not an intrinsic limitation of RL — implying the ceiling can be raised by preserving exploration rather than by fundamentally redesigning RL objectives.
- The covariance framework offers a principled diagnostic and design lens for future RL algorithms: understanding which tokens drive entropy dynamics provides a new axis for analyzing why certain RL methods succeed or fail on reasoning tasks.

---

### Remaining Limitations & Next Steps
- The empirical law R = −a exp(H) + b is explicitly noted as not universal: other work with different policy initializations (e.g., instruct models) or off-policy data shows distinct entropy patterns, and the paper calls for more in-depth analysis under varied conditions.
  - The predictabili

## Key Claims

1. Policy entropy collapses sharply at the early stage of RL training for LLMs, dropping to near zero monotonically without entropy intervention.
2. Without entropy intervention, the relationship between policy entropy H and downstream validation performance R follows the exponential law R = -a·exp(H) + b, where a and b are fitting coefficients.
3. Over 93% of policy performance gains and 94% of entropy losses occur within the first 800 gradient steps (1/3 of training), leaving over 2/3 of training steps yielding marginal returns.
4. The performance ceiling of a policy undergoing RL is fully predictable: at H=0 (entropy exhausted), maximum achievable performance is R = -a + b.
5. The coefficients a and b in the entropy-performance law are algorithm-independent; different RL algorithms (GRPO, RLOO, REINFORCE++) produce the same fitted curve for the same model and data.
6. The entropy-performance fitted curve from the first 15% of training steps (first 36 steps) can predict final performance with an average RMSE of 0.9% on math and 1.2% on code tasks.
7. For softmax policies (including LLMs), the step-wise change in policy entropy is determined by the negative covariance between the log-probability of an action and the change in its output logit.
8. Under Policy Gradient algorithms, logit change is proportional to action probability times advantage, so a high-probability action with high advantage decreases entropy, while a rare action with high 
9. The covariance term between log-probability and logit change remains positive throughout RL training, explaining why policy entropy decreases monotonically.
10. Easier training examples (higher model accuracy) exhibit higher covariance values than harder examples during RL training.

## Capabilities

- RL training performance for LLM reasoning can be predicted from early training dynamics: fitting the entropy-performance curve R = -a·exp(H) + b using only 15% of training steps achieves RMSE of 0.9–1.9% for all subsequent steps and 0.5–1.9% for final performance prediction
- Covariance-aware entropy regularization (Clip-Cov and KL-Cov) prevents policy entropy collapse during RL training by restricting gradient updates on the small fraction of tokens with highest covariance between log-probability and advantage, achieving 2.0% average improvement over GRPO on 7B models a
- RL training performance of large models within a family can be extrapolated from small model training runs: entropy-performance curve coefficients (a, b) scale log-linearly with parameter count, enabling prediction of large model RL performance without executing full training

## Limitations

- Policy entropy collapses to near-zero in the first 1/12 of RL training steps — over 93% of performance gains and 94% of entropy losses occur in the first third of training, rendering more than two-thirds of total training compute waste with marginal returns
- RL compute scaling for LLM reasoning has a hard, predictable performance ceiling: as policy entropy approaches zero, performance saturates at R = -a + b — additional training compute beyond the entropy exhaustion point yields no improvement
- Standard entropy regularization methods from classical RL (entropy bonus, KL divergence to reference model) fail for LLM RL training: small coefficients have negligible effect on entropy collapse while large coefficients either trigger entropy explosion or degrade task performance
- LLM pretraining structurally limits exploration capacity during RL — narrowed output distributions from maximum-likelihood training create a tension where generation quality and RL exploratory potential are in direct opposition
- The entropy-performance predictability law is not universal — experiments using off-policy data or different base model architectures show distinct entropy patterns, meaning the exponential relationship may not transfer across training regimes
- All entropy-performance findings are restricted to verifiable task domains (math and coding) — the entire framework assumes binary verifiable rewards and cannot be directly applied to open-ended or creative tasks
- No principled method exists to determine the optimal policy entropy level for RL training — whether a target entropy that maximally balances exploration and training stability exists is an open theoretical question
- Entropy dynamics in LLM RL are governed by an extremely heavy-tailed covariance distribution — the top 0.02% of tokens have covariance >2000x the mean, making the entire system's exploratory capacity hostage to a tiny number of 'pivotal' tokens

## Bottlenecks

- Policy entropy exhaustion creates a hard, predictable ceiling on RL compute scaling for LLM reasoning — without entropy management, the entire performance gain is front-loaded and further compute investment is structurally futile
- Absence of a principled target entropy value for RL training blocks systematic and reproducible entropy management — practitioners cannot select optimal exploration levels without empirical search, and the exploration-exploitation tradeoff is not theoretically characterized for LLMs

## Breakthroughs

- Discovery of a universal empirical law R = -a·exp(H) + b precisely quantifying the exponential tradeoff between policy entropy and RL training performance, validated across 11 models (0.5B–32B), 4 model families, 4 RL algorithms, and math/coding task domains
- Theoretical derivation of the entropy dynamics mechanism for softmax LLMs under policy gradient algorithms: entropy change equals the negative covariance between action log-probability and logit change (proportional to advantage), identifying a small set of high-covariance tokens as the proximate dr

## Themes

- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/math500|MATH500]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/prime|PRIME]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/policy-entropy|policy entropy]]
- [[entities/verl|verl]]
