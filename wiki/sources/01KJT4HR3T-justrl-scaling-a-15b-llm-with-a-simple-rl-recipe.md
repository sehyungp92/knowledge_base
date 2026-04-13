---
type: source
title: 'JustRL: Scaling a 1.5B LLM with a Simple RL Recipe'
source_id: 01KJT4HR3TEMPSE4GSAZTX81PK
source_type: paper
authors:
- Bingxiang He
- Zekai Qu
- Zeyuan Liu
- Yinghao Chen
- Yuxin Zuo
- Cheng Qian
- Kaiyan Zhang
- Weize Chen
- Chaojun Xiao
- Ganqu Cui
- Ning Ding
- Zhiyuan Liu
published_at: '2025-12-18 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# JustRL: Scaling a 1.5B LLM with a Simple RL Recipe

JustRL challenges the prevailing assumption that reinforcement learning for small language models requires elaborate multi-stage pipelines, demonstrating that a single-stage GRPO recipe with fully fixed hyperparameters can match or exceed the performance of far more complex approaches at 1.5B scale — while using half the compute.

**Authors:** Bingxiang He, Zekai Qu, Zeyuan Liu, Yinghao Chen, Yuxin Zuo, Cheng Qian, Kaiyan Zhang, Weize Chen, Chaojun Xiao, Ganqu Cui, Ning Ding, Zhiyuan Liu
**Published:** 2025-12-18
**Type:** paper

---

## Background & Motivation

The standard path for improving [[themes/pretraining_and_scaling|small language models]] (SLMs) has been distillation from larger teachers. But distillation has a hard ceiling: once the teacher model plateaus, further gains require [[themes/reinforcement_learning|reinforcement learning]], not more data. The field's response to the challenges of RL at small scale has been a proliferation of stabilization techniques — multi-stage training pipelines, dynamic hyperparameter schedules, adaptive temperature, length penalties, reference model resets, curriculum learning — each motivated by a specific failure mode observed in prior work.

The compounding problem is structural: ProRL-V2 uses a nine-stage pipeline with scheduled cosine length penalties; FastCuRL uses five stages alternating CoT compression and extension; BroRL scales rollouts to 512 per example for exhaustive solution space coverage. Because these works combine different technique subsets on top of already-complex baselines, **it is impossible to determine whether any single technique provides genuine benefits or merely compensates for instabilities introduced by prior complexity.** The accumulated "best practices" may be fighting each other rather than addressing the fundamental challenges of [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

---

## The JustRL Recipe

JustRL's core claim is methodological: deliberately minimal single-stage GRPO with no changes to data, prompting, or hyperparameters between models or across training.

**What's included:**
- GRPO with binary outcome rewards and a lightweight rule-based verifier (from DAPO, no SymPy)
- "Clip higher" — asymmetric clip ratio `[0.8, 1.28]`, treated as part of the stable baseline, not an added trick
- Fixed hyperparameters throughout: learning rate `1e-6` constant, temperature `1.0`, rollout `N=8`, train batch size `256`
- DAPO-Math-17k training data, no offline difficulty filtering or online dynamic sampling
- Hard 16K token context limit as the only length constraint

**What's excluded:**
- Explicit length penalties
- KL regularization
- Reference model resets
- Adaptive temperature
- Curriculum learning
- Dynamic sampling
- Multi-stage training

The identical configuration was applied without tuning to two distinct backbones: DeepSeek-R1-Distill-Qwen-1.5B (4,380 steps) and OpenMath-Nemotron-1.5B (3,440 steps), both on 32 A800-80GB GPUs over ~15 days each.

---

## Results

### Mathematical Reasoning Performance

| Model | Avg (9 benchmarks) | AIME 2024 | AIME 2025 | Compute |
|---|---|---|---|---|
| JustRL-DeepSeek-1.5B | 54.87% | 52.60% | 38.75% | 1.4×10⁸k tokens |
| ProRL-V2 | 53.08% | — | — | 2.8×10⁸k tokens |
| BroRL | ~57% AIME24 only | 57.50% | 36.88% | 6.8×10⁸k tokens |
| JustRL-Nemotron-1.5B | **64.32%** | — | — | 1.1×10⁸k tokens |
| QuestA | 63.81% | — | — | 2.6×10⁸k tokens |

JustRL-DeepSeek outperforms ProRL-V2's nine-stage pipeline at 2× lower compute. JustRL-Nemotron achieves reported state-of-the-art at 1.5B scale at 2.4× lower compute than QuestA — which additionally requires full reasoning trajectories from larger models to construct its curriculum. BroRL's brute-force compute scaling (4.9× more than JustRL-DeepSeek) yields narrower advantages on AIME 2024 while leaving most benchmarks unreported, suggesting diminishing returns.

### Training Dynamics

Training dynamics across 4,000+ steps show:
- **Smooth, monotonic reward improvement** — no plateaus or collapses
- **Policy entropy oscillating stably between 1.2–1.4** — no drift in either direction
- **Natural response length convergence** from ~8,000 initial tokens to 4,000–5,000 tokens within ~1,000 steps, without any explicit length penalty

This organic behavior stands in direct contrast to the instabilities (reward collapse, entropy drift, length explosion) that motivated the intervention-heavy techniques in prior work — suggesting those failure modes may be artifacts of complex training setups rather than fundamental properties of [[themes/policy_optimization|RL training for LLMs]].

---

## Ablations: When "Standard Tricks" Make Things Worse

Two widely-used interventions were tested and both degraded performance:

**Overlong penalty:** AIME 2024 plateaus at 50% vs. 55% baseline. Entropy collapses to 0.5–0.6 (vs. healthy 1.2–1.4), indicating premature convergence and collapsed exploration.

**Robust verifier:** AIME 2024 drops further to 45%. The more permissive verifier is hypothesized to reduce the nuanced learning signal that strict formatting requirements provide, removing the incentive for the model to develop precise internal computation. Entropy again collapses to 0.5–0.6.

The failure mode is the same in both cases: the intervention suppresses exploration rather than stabilizing training. This has a pointed implication for the broader literature — the instabilities that motivated these techniques may be symptoms of other design choices in those pipelines, not properties of RL itself.

---

## Landscape Contributions

### Capabilities

- **Single-stage RLVR achieves SOTA at 1.5B scale** — JustRL-Nemotron reaches 64.32% average across nine challenging [[themes/mathematical_and_formal_reasoning|mathematical reasoning]] benchmarks with no pipeline complexity *(maturity: research only)*
- **Fixed hyperparameters transfer across backbones** — the same configuration applied without tuning to both DeepSeek-R1-Distill and OpenMath-Nemotron produces stable monotonic improvement *(maturity: research only)*
- **RL surpasses distillation ceiling** — gains beyond what additional distillation data or extended SFT can achieve once saturation is reached *(maturity: research only)*
- **Organic response length self-regulation** — models compress from ~8,000 to 4,000–5,000 tokens without penalty terms, suggesting the objective itself incentivizes conciseness *(maturity: research only)*

### Limitations

- **Domain restriction:** Results are entirely from mathematical reasoning at 1.5B scale. Generalization to coding, general QA, and domains with noisier reward signals is untested and structurally unclear.
- **Common interventions are actively harmful:** Explicit length penalties and robust verifiers — both widely used across the literature — degrade performance in the JustRL setup, raising questions about how results from other pipelines should be interpreted.
- **Fragility of the "delicate balance":** Two reasonable modifications both made things worse. Whether the configuration is genuinely robust or happens to sit in a narrow optimum that other configurations miss is unresolved.
- **No training beyond ~4,000 steps:** Whether stable monotonic improvement persists at longer horizons, or whether instabilities eventually emerge, is unknown.
- **Opaque causal mechanism:** Success cannot be attributed to any single component — hyperparameters, dataset (DAPO-Math-17k), verifier design, and their interactions are not independently controlled.
- **Resource requirement remains high:** 32 A800-80GB GPUs × ~15 days per run is 2× cheaper than prior SOTA but still prohibitive for resource-constrained researchers.
- **All SLM-RLVR work starts from distilled bases:** Whether simple or complex RL works for raw pretrained models without distillation warmup is a conspicuous absence across the entire field.

### Bottleneck: Interpretability of the RL-for-SLM Literature

The accumulated complexity in this research area creates an uninterpretable stack. Techniques are validated on top of already-complex baselines, making it impossible to determine what actually drives improvements vs. what patches artifacts of other design choices. JustRL provides a minimal reference point, but a field-wide commitment to ablation-first methodology would be required to resolve this. *(Horizon: months)*

---

## Implications & Open Questions

The central challenge JustRL poses is not "does simplicity work?" — it demonstrably does here — but rather: **what does this mean for the existing literature?** If monotonic, collapse-free RL training is achievable with a minimal recipe, the instabilities that motivated nine-stage pipelines, curriculum systems, and aggressive regularization may have been self-inflicted. This would suggest a significant portion of complexity in published systems is compensatory rather than constitutive.

Key open questions:
- Do the stability advantages persist at 7B, 14B, or larger scales, or does genuine complexity emerge at scale?
- What is the minimal recipe for non-mathematical domains where reward signals are noisier?
- Does the hyperparameter transferability across backbones generalize beyond 1.5B distilled models?
- Is the fragility observed in ablations (two reasonable modifications both fail) a property of this specific optimum or a general feature of RLVR at small scales?

---

## Related Themes

- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/policy_optimization|Policy Optimization]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/grpo|GRPO]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/pass1|Pass@1]]
- [[entities/rlvr|RLVR]]
- [[entities/dynamic-sampling|dynamic sampling]]
- [[entities/policy-entropy|policy entropy]]
- [[entities/verl|verl]]
