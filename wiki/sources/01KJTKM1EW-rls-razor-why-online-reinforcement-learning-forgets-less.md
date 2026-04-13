---
type: source
title: 'RL''s Razor: Why Online Reinforcement Learning Forgets Less'
source_id: 01KJTKM1EWG4GWAA0QWYRY6RJ5
source_type: paper
authors:
- Idan Shenfeld
- Jyothish Pari
- Pulkit Agrawal
published_at: '2025-09-04 00:00:00'
theme_ids:
- continual_learning
- finetuning_and_distillation
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# RL's Razor: Why Online Reinforcement Learning Forgets Less

**Authors:** Idan Shenfeld, Jyothish Pari, Pulkit Agrawal
**Published:** 2025-09-04 00:00:00
**Type:** paper

## Analysis

# RL's Razor: Why Online Reinforcement Learning Forgets Less
2025-09-04 00:00:00 · paper · Idan Shenfeld, Jyothish Pari, Pulkit Agrawal
https://arxiv.org/pdf/2509.04259

---

### Motivation & Prior Limitations
- Foundation models are largely static after deployment, yet the vision of long-lived continual agents requires post-training methods that add new capabilities without erasing old ones — a goal systematically undermined by catastrophic forgetting.
  - Catastrophic forgetting (McCloskey & Cohen, 1989; Kirkpatrick et al., 2017) remains persistent even as models scale, and existing mitigations (EWC, feature preservation, output regularization) address symptoms rather than identifying the underlying cause.
- Prior work lacked a reliable, practically measurable predictor of forgetting that generalizes across training algorithms and hyperparameters; proposed candidates such as weight-change magnitude, gradient rank, and activation drift all failed to explain observed forgetting behavior consistently.
  - In controlled experiments (ParityMNIST), Fisher-weighted L2 weight change achieved only R²=0.58 and activation shift metrics showed distinct curves per training objective, confirming they are not general predictors.
- The comparative behavior of SFT versus RL with respect to forgetting had not been studied; prior comparisons focused solely on new-task performance, leaving the retention-of-prior-knowledge dimension unexamined.

---

### Proposed Approach
- The paper identifies an empirical forgetting law: the forward KL divergence between the fine-tuned policy and the base policy, measured on the new task distribution (Ex∼τ[KL(π₀‖π)]), reliably predicts the degree of catastrophic forgetting across methods, hyperparameters, and model scales.
  - Unlike prior predictors tied to weight space or past-task data, this metric requires only the new task distribution to compute, making it practically accessible during fine-tuning without access to prior task data.
- The paper names a principle called RL's Razor: among the many policies that achieve high performance on a new task, on-policy RL methods are implicitly biased toward those with minimal KL divergence from the base model, while SFT can converge to arbitrarily distant distributions depending on the labeling used.
  - This bias arises mechanistically from on-policy sampling: at each update, RL samples outputs already assigned non-negligible probability by the current policy, then reweights them by advantage, producing conservative distribution shifts rather than pulling toward an external target.
  - Theorem 5.2 formalizes this: under suitable regularity conditions, policy gradient converges to π† = argmin_{π∈P*∩Π} KL(π‖π₀), the KL-minimal optimal policy within the representable family, even without explicit KL regularization.
- To isolate the causal factor, the paper constructs a 2×2 ablation across on-policy vs. offline and positive-only vs. positive+negative gradient methods (GRPO, 1-0 Reinforce, SFT, SimPO), determining that on-policy sampling — not negative examples — is the key mechanism.

---

### Results & Capabilities
- Across three LLM tasks (math reasoning, science Q&A, tool use on Qwen 2.5 3B-Instruct) and one robotic manipulation task (pick-and-place on OpenVLA 7B), RL achieves Pareto-superior retention of prior knowledge at matched new-task performance compared to SFT.
  - On math reasoning, even small SFT accuracy gains on the new task correspond to sharp drops across benchmarks including Hellaswag, TruthfulQA, MMLU, IFEval, Winogrande, and HumanEval; RL shows near-flat prior-task performance across the same new-task accuracy range.
- In the controlled ParityMNIST setting, forward KL divergence fits a quadratic forgetting curve with R²=0.96 across all methods and SFT label distributions; in LLM experiments, the same quadratic fit achieves R²=0.71 with mean-zero residuals attributable to estimation noise.
  - The forgetting-KL curve is shared across GRPO, 1-0 Reinforce, SFT, and oracle SFT runs — confirming that the algorithm per se does not govern forgetting, only the resulting KL shift does.
- An oracle SFT distribution — analytically constructed to minimize KL while achieving 100% accuracy on ParityMNIST — outperforms even RL in prior-task retention, validating that RL's advantage is not intrinsic to RL but to its implicit KL minimization.
  - SFT trained on data generated by an RL-trained model (distillation) matched RL's accuracy-forgetting trade-off, further confirming that the learned distribution governs forgetting rather than the optimization algorithm.
- The effect generalizes beyond large-scale transformers: an MLP trained on ParityMNIST reproduces the same RL-vs-SFT forgetting gap, showing the principle is a general property of fine-tuning deep generative models.
- The sparsity hypothesis (Mukherjee et al., 2025) — that RL updates are sparse while SFT updates are dense — is refuted: apparent sparsity was an artifact of bfloat16 precision; training in float32 produced identical performance with no weight update sparsity, and all algorithms yielded full-rank weight updates.

---

### Implications
- The empirical forgetting law reframes continual learning research: rather than designing mitigations for forgetting's effects (weight regularization, replay, feature preservation), the field should target KL divergence from the base model as the primary design variable for post-training algorithms.
- RL's Razor provides a unified explanation for why KL regularization — used in RLHF pipelines (Stiennon et al., 2020; Ouyang et al., 2022) primarily as a reward-hacking stabilizer — also incidentally reduces forgetting, elevating it from heuristic to principled design choice.
- The finding that oracle SFT surpasses RL in forgetting retention suggests a productive hybrid design space: offline methods can match or beat RL if guided to KL-minimal distributions, opening a path toward continual learning that combines SFT efficiency

## Key Claims

1. RL fine-tuning forgets less than SFT even when both methods achieve the same performance on the new task
2. The degree of catastrophic forgetting is accurately predicted by the KL divergence between the fine-tuned and base policy evaluated on the new task distribution
3. On-policy RL is implicitly biased toward KL-minimal solutions among the many policies that solve the new task
4. SFT can converge to output distributions arbitrarily far from the base model depending on the provided labels
5. Forward KL divergence predicts catastrophic forgetting with R²=0.71 in LLM experiments
6. SFT trained on data generated by an RL-trained model matches RL's accuracy-forgetting trade-off, reinforcing that the learned distribution governs forgetting rather than the optimization algorithm
7. The critical factor explaining RL's resistance to forgetting is on-policy training, not the presence of negative gradient examples
8. Policy gradient methods converge to the KL-minimal optimal policy within the representable policy family even without explicit KL regularization
9. Theorem 5.2 proves that policy gradient converges to the policy that minimizes KL divergence to the initialization among all optimal representable policies
10. Sparse weight updates attributed to RL were an artifact of bfloat16 numerical precision, not a fundamental property of on-policy training

## Capabilities

- On-policy RL fine-tuning (GRPO, 1-0 REINFORCE) preserves prior capabilities significantly better than SFT when adapting foundation models to new tasks, achieving comparable new-task performance with substantially higher retention on prior benchmarks — validated across math reasoning, science Q&A, to
- KL divergence between fine-tuned and base model evaluated on the new task is a reliable, real-time, task-accessible predictor of catastrophic forgetting across training objectives and hyperparameters — R²=0.96 in controlled setting, R²=0.71 in LLMs — without requiring access to past-task data
- Oracle SFT trained on the analytically derived KL-minimal labeling distribution achieves less forgetting than RL itself, demonstrating that KL minimization — not the RL algorithm per se — is the operative mechanism for catastrophic forgetting reduction
- RL fine-tuning of robotic vision-language-action foundation models (OpenVLA 7B) for new manipulation tasks preserves prior robot policy capabilities better than SFT at matched new-task performance
- Policy gradient methods provably converge to the KL-minimal optimal policy within the representable family — on-policy RL's resistance to forgetting is not a heuristic property but a theoretical guarantee from the geometry of probability space

## Limitations

- Foundation models are largely static once deployed — not designed to self-improve or continuously acquire new capabilities, making long-lived continual adaptation a fundamental unsolved problem
- SFT systematically causes catastrophic forgetting when learning new tasks — improvements in new-task performance come at the direct expense of prior-task retention, with no Pareto-optimal solution matching RL's trade-off
- RL training is computationally expensive and cannot easily be run to convergence at LLM scale, making the systematic investigation of the KL-forgetting relationship in large models difficult
- The mechanistic account of why larger KL shifts on the new task disrupt prior knowledge is entirely absent — whether through representational interference, implicit capacity limits, or other dynamics is unknown
- The KL-forgetting empirical law is validated only at moderate model scales (3B–7B parameters) — its behaviour at frontier scales and in more diverse generative domains is unknown and may not hold
- The KL-forgetting relationship is significantly weaker in LLMs (R²=0.71) than in toy models (R²=0.96), suggesting additional noise factors at scale that reduce predictive precision
- Off-policy RL algorithms — which are widely used in practice — are not studied, leaving a gap in understanding whether RL's Razor generalizes beyond on-policy methods
- Prior continual learning methods (EWC, weight regularization, feature preservation) targeted the wrong variable — weight changes — rather than the true governing variable (KL divergence), meaning a large body of prior work was misdirected
- bfloat16 training produces artifactually sparse weight updates in RL that disappear entirely under float32 — a precision artifact that has likely caused incorrect mechanistic interpretations of why RL differs from SFT in prior work
- The oracle KL-minimal SFT distribution — which surpasses RL for forgetting preservation — is analytically derivable only for toy tasks with tractable output spaces; it is uncomputable for real LLM tasks
- RL experiments use only binary success indicators as rewards — the effect of more complex, dense, or shaped reward signals on the KL-forgetting relationship is entirely untested

## Bottlenecks

- No post-training algorithm explicitly optimizes KL minimization from the base model as a first-class objective — RL achieves this implicitly but expensively, SFT does not achieve it, and a principled method combining SFT's data efficiency with explicit KL minimization does not exist
- No principled method exists to construct or approximate KL-minimal training distributions for complex generative tasks at LLM scale — the oracle that surpasses RL is analytically tractable only in toy settings

## Breakthroughs

- RL's Razor: KL divergence between fine-tuned and base model on the new task identified as the governing empirical law of catastrophic forgetting — unifying the forgetting behaviour of all training algorithms under a single, measurable, task-accessible metric, and providing theoretical proof that on-

## Themes

- [[themes/continual_learning|continual_learning]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reinforcement_learning|reinforcement_learning]]

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/elastic-weight-consolidation|Elastic Weight Consolidation]]
- [[entities/grpo|GRPO]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
