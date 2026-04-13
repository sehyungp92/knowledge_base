---
type: source
title: On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language
  Models
source_id: 01KJT4XPFEX1F9NKS76D8Q7Y62
source_type: paper
authors:
- Charlie Zhang
- Graham Neubig
- Xiang Yue
published_at: '2025-12-08 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models

**Authors:** Charlie Zhang, Graham Neubig, Xiang Yue
**Published:** 2025-12-08 00:00:00
**Type:** paper

## Analysis

# On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models
2025-12-08 · paper · Charlie Zhang, Graham Neubig, Xiang Yue
https://arxiv.org/pdf/2512.07783

---

### Motivation & Prior Limitations
The central unresolved question motivating this work is whether RL post-training genuinely extends a model's reasoning ability beyond what was acquired during pre-training, or whether it merely sharpens pre-existing skills.
- The literature offers directly conflicting views: some work characterizes RL as a capability refiner (Yue et al., Wu et al., Shao et al., Yeo et al.), while others present evidence of substantial reasoning gains beyond pre-training (Wen et al., Yuan et al., Sun et al.).
  - This discrepancy is attributed to the use of uncontrolled training environments — modern LMs are pre-trained on massive, opaque internet corpora whose composition is fundamentally unknown, making it impossible to isolate the causal effect of post-training.
- Mid-training (also called continued pre-training/CPT) has emerged as a key but underexamined component of modern pipelines, and its interaction with both pre-training and RL is poorly understood.
  - Because mid-training may explain why RL sometimes generalizes dramatically and sometimes fails, its absence from controlled analyses is a major gap in prior work.

---

### Proposed Approach
The paper constructs a fully controlled experimental framework to causally isolate the individual and joint contributions of pre-training, mid-training, and RL post-training on reasoning generalization.
- The framework is built on the GSM-Infinite data generation pipeline, using dependency graphs (DAGs) where nodes are variables and edges encode arithmetic dependencies, giving precise control over reasoning complexity via operation count `op(G) = |E|`.
  - Contextual rendering layers natural language templates (e.g., animals–zoo, teachers–school) over the same underlying DAG structure, enabling factorized control over structural complexity and surface form independently.
  - Training distributions for each stage are kept strictly disjoint to prevent contamination and enable clean causal attribution.
- Reasoning generalization is evaluated along two orthogonal axes: extrapolative (depth) generalization — solving problems with more operations than seen in pre-training — and contextual (breadth) generalization — transferring reasoning primitives across novel surface templates with identical underlying logic.
- A process-verified evaluation scheme parses model solutions into predicted dependency graphs and compares them against gold graphs at the step level; correctness requires both the reasoning process and final answer to match, using `pass@k` as the primary metric.
- A 100M-parameter Qwen2.5-style decoder-only model is pre-trained on 10B tokens (100× parameters, following Chinchilla scaling) across operation ranges `op=2–10`, with GRPO used for RL post-training on curated subsets targeting generalization.

---

### Results & Capabilities
RL produces genuine capability gains (measured via pass@128) only when two conditions hold simultaneously: the task was not heavily covered during pre-training (leaving sufficient headroom), and the RL training data is calibrated to the model's edge of competence — tasks that are difficult but not yet out of reach.
- When RL data are well-calibrated to this boundary, extrapolative pass@128 improves by up to +42%; when the data are either too easy (in-domain) or too hard (fully out-of-distribution), RL sharpens existing skills without inducing genuine generalization.

Contextual generalization via RL requires minimal but non-zero pre-training exposure to the target context: near-zero exposure causes RL to fail at transfer entirely, but sparse coverage of ≥1% provides a sufficient seed that RL can robustly reinforce.
- With ≥1% pre-training exposure, RL yields up to +60% pass@128 on contextual generalization; without it, the same RL procedure produces no meaningful transfer.

Introducing a mid-training phase between pre-training and RL substantially improves both in-domain and out-of-distribution performance under a fixed compute budget, with mid-training + RL outperforming RL alone by +10.8% on OOD-hard tasks.
- Mid-training narrows the data distribution to tasks at the model's emerging competence boundary (similar to RL data), providing structured supervision that stabilizes optimization and strengthens higher-level reasoning priors before RL amplifies them.

Process-level rewards reduce reward hacking and improve reasoning fidelity relative to outcome-only rewards.
- Incorporating process verification into the reward function aligns reinforcement signals with valid intermediate reasoning behavior, yielding measurable improvements in both accuracy and generalization under complex, compositional settings.

---

### Implications
This work reconciles the conflicting literature on whether RL genuinely improves reasoning or merely refines it: both views are correct under different conditions, and the disagreement reflects uncontrolled variation in pre-training coverage and RL data calibration rather than a true empirical contradiction.
- The "edge of competence" principle — that RL data must target tasks at the boundary of current capability — provides a concrete, actionable criterion for RL data curation in real training pipelines.

The demonstration that mid-training is a powerful but underexplored lever reframes it as a first-class design decision rather than an optional preprocessing step, with significant implications for how practitioners should allocate compute across training stages.
- Because mid-training under fixed compute outperforms equivalent RL-only compute, the optimal training pipeline likely involves deliberate distributional bridging before reward optimization rather than scaling RL data alone.

The finding that ≥1% pre-training exposure suffices for RL-driven contextual transfer has practical i

## Key Claims

1. RL produces true capability gains (measured by pass@128) only when pre-training leaves sufficient headroom and RL data targets the model's edge of competence — tasks at the boundary that are difficult
2. RL-based post-training can yield up to +42% pass@128 improvement when RL data difficulty is well-calibrated to the model's competence boundary.
3. Contextual generalization requires minimal yet sufficient pre-training exposure; RL fails to induce contextual transfer with near-zero pre-training exposure but generalizes robustly with sparse exposu
4. Mid-training combined with RL outperforms RL alone by +10.8% on OOD-hard tasks under a fixed compute budget.
5. Process-level rewards reduce reward hacking and improve reasoning fidelity in RL-trained language models.
6. The conflicting views in the literature about whether RL genuinely improves reasoning are reconcilable: RL sharpens existing abilities when pre-training already covers the task, and produces genuine n
7. Without any pre-training exposure to a new context, RL does not induce contextual transfer; even very sparse coverage (≥1%) provides a sufficient seed for robust cross-context generalization.
8. Mid-training is an underexplored but powerful lever in training design that substantially strengthens both in-domain and out-of-domain performance under a fixed compute budget.
9. A major source of discrepancy in RL effectiveness research is that prior analyses rely on uncontrolled training environments where pre-training corpora are opaque, making it impossible to ascertain wh
10. Mid-training acts as an intermediate distributional bridge between broad pre-training corpora and specialized post-training objectives, expanding primitive coverage and aligning internal representatio

## Capabilities

- RL calibrated to a model's edge of competence (tasks at the boundary of pre-training coverage — difficult but not yet out-of-reach) produces genuine extrapolative reasoning gains of up to +42% pass@128, rather than merely eliciting pre-existing skills
- A mid-training stage bridging pre-training and RL distributions substantially improves out-of-distribution reasoning under fixed compute, outperforming RL-only by +10.8% on OOD-hard tasks
- Sparse pre-training exposure to a target context (≥1%) is sufficient for RL to robustly induce cross-context reasoning transfer, yielding up to +60% pass@128 gains where zero exposure produces none
- Process-level reward verification during RL training — verifying intermediate reasoning steps against a ground-truth dependency graph — measurably reduces reward hacking and improves reasoning fidelity in compositional tasks

## Limitations

- RL cannot produce genuine reasoning capability extension when the task domain was already substantially covered during pre-training — it only sharpens existing abilities, not extends them
- RL fails to induce cross-context reasoning transfer without at least minimal pre-training exposure to the target context — near-zero exposure yields zero transfer regardless of RL data quality
- The opacity of real-world pre-training corpora makes it impossible in practice to know which reasoning primitives a base model has already internalized, preventing principled RL data calibration relative to the model's actual edge of competence
- Outcome-only (scalar) rewards in RL are vulnerable to reward hacking on complex compositional reasoning — models find shortcuts satisfying the reward without producing valid intermediate reasoning steps
- All controlled findings are derived from 100M parameter models on fully synthetic reasoning tasks — whether the pre-training/RL headroom dynamics hold at frontier scale (10B–100B+ parameters) on natural language tasks is unvalidated
- The paper demonstrates that edge-of-competence RL calibration is critical but provides no automated method to identify where a model's edge of competence lies in practice — this is only controlled in the synthetic experimental setting
- Experiments use fully synthetic reasoning tasks with explicit DAG dependency structure — applicability to real-world natural language reasoning with implicit dependencies, ambiguity, and open-ended domains is not demonstrated
- Mid-training stage design — what data to use, which objectives, optimal duration, and how to scope the distributional bridge between pre-training and RL — remains systematically underexplored with no principled framework

## Bottlenecks

- Opacity of real-world pre-training corpora prevents principled RL data calibration to the model's edge of competence — without knowing which reasoning primitives are already internalized, systematic design of RL data that produces genuine capability extension (rather than elicitation) is intractable
- Absence of principled frameworks for mid-training data selection, objectives, and duration prevents systematic exploitation of mid-training as a compute-efficient lever despite its demonstrated +10.8% OOD improvement over RL-only approaches

## Breakthroughs

- Controlled causal framework reconciling conflicting RL-for-reasoning views: RL produces genuine capability gains only when (a) pre-training left sufficient headroom in the task domain AND (b) RL data target the model's precise edge of competence — both conditions jointly required
- Mid-training empirically demonstrated as a compute-efficient training lever with causal attribution: under a fixed compute budget, mid-training + RL outperforms RL alone by +10.8% on OOD-hard reasoning tasks, establishing mid-training as an independent and central pipeline stage

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/mid-training|Mid-training]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/passk|pass@k]]
