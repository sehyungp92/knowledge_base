---
type: entity
title: PRM800K
entity_type: dataset
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0006183211263111066
staleness: 0.0
status: active
tags: []
---
```markdown
# PRM800K

PRM800K is a dataset of approximately 800,000 math problem-solution pairs with human-verified step-level correctness labels (totaling roughly 712K process labels), released by OpenAI to enable training of process reward models (PRMs) for mathematical reasoning. It represents the gold standard for step-level supervision in multi-step reasoning: each intermediate step in a solution chain is explicitly labeled correct or incorrect by human annotators, providing a richer training signal than outcome-only approaches. Its significance extends well beyond its direct use; it defines the benchmark for what automated annotation pipelines are trying to approximate, and it anchors the training of PRMs that now underpin test-time compute scaling strategies across much of the field.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

PRM800K emerged from OpenAI's work on let-models-verify-their-own-reasoning, providing a large-scale human-curated corpus of step-level labels for math solutions. The dataset directly addresses the observation that outcome reward models (ORMs) are brittle on longer reasoning chains: they cannot distinguish a correct answer reached by flawed reasoning from one reached correctly, and they fail to localize where a solution goes wrong. By contrast, PRMs trained on PRM800K can score each step independently, enabling more precise verification and richer training signal for both reinforcement learning and inference-time search.

The dataset's influence is dual. First, it is the primary training corpus for discriminative PRMs. Second, it serves as a quality filter and calibration reference for automated annotation pipelines (most prominently, THINKPRM's synthetic data pipeline) that attempt to replicate human step-level judgment at scale. As annotation costs make direct replication of PRM800K prohibitive for most researchers, the dataset has become a kind of ceiling against which cheaper alternatives are measured.

## Key Findings

### The Core Problem PRM800K Solves

Human step-level annotation is expensive, and the expense is not incidental. Intricate multi-step reasoning tasks require annotators with advanced mathematical skills, meaning annotation costs scale with problem difficulty rather than just volume. This cost has historically constrained who can train competitive PRMs and has motivated the entire line of research into automated process labeling. The tension between annotation quality and annotation cost is the defining tension in this space.

### What Step-Level Labels Enable

PRMs trained on step-level data consistently outperform ORMs on complex benchmarks. The advantage is modest on simpler datasets like GSM8K, which require fewer reasoning steps and leave less room for intermediate error, but grows substantially on harder benchmarks like MATH, where the longer solution chains give step-level supervision more information to work with. This pattern suggests the value of PRM800K scales with problem difficulty: the harder the task, the more the step-level signal matters.

PRM800K also enables superior data efficiency. At modest training set sizes (around 10K examples), PRM-based models outperform ORM-based models by roughly 4 percentage points in accuracy, and the gap between their performance ceilings favors PRMs as data scales. This efficiency advantage has practical consequences: researchers working with limited annotation budgets get more from step-level labels than from outcome labels.

### Automated Alternatives and Their Tradeoffs

The primary automated alternative to PRM800K-style annotation is Monte Carlo completion: run a model forward from each intermediate step multiple times, observe what fraction of completions reach the correct final answer, and use that frequency as a proxy for step quality. This produces two estimators. Hard Estimation (HE) labels a step as good if any single completion reaches the correct answer; Soft Estimation (SE) uses the fraction across all completions. SE converges toward the human-annotated distribution as the number of completions increases, while HE does not, making SE the more principled choice for approximating PRM800K-style signal.

This completion-based approach is substantially cheaper than human annotation, but it is not free. The completion process is compute-intensive, and the quality of the resulting labels depends heavily on the capability of the model used to generate completions: larger completors produce better training data, and the quality of the data used to train the completor is itself a factor. There is a compounding dependency between model capability and annotation quality that does not exist with human annotation.

### Integration with Reinforcement Learning

Step-level supervision from PRM800K-style data is complementary to policy optimization rather than a substitute for it. Models trained with step-by-step PPO supervised by process reward signals outperform those trained with vanilla PPO using only outcome rewards, and both outperform supervised fine-tuning baselines. The gains stack: a model improved through step-by-step PPO and then verified at inference time with a process reward model achieves better results than either intervention alone. For example, Mistral-7B trained with step-by-step PPO and verified with Math-Shepherd reaches 89.1% on GSM8K and 43.5% on MATH, substantially above the baseline.

The size relationship between the policy model and the reward model also matters asymmetrically: using a larger reward model to verify a smaller generator improves performance, while using a smaller reward model to verify a larger generator degrades it. This implies that PRM800K's value as a training corpus is partly indexed to whether the resulting PRM is large enough to be a credible judge of the models it is evaluating.

### Downstream Use in Test-Time Compute Scaling

PRM800K sits upstream of several test-time compute strategies described in Scaling LLM Test-Time Compute Optimally and related work. PRMs trained on this data serve as verifiers in beam search, best-of-N selection, and tree-structured search (MCTS variants), where the quality of the reward signal directly determines how well additional compute translates into better answers. The dataset is also the calibration reference for THINKPRM, which trains a thinking-based PRM using synthetic data filtered against PRM800K's human judgments.

## Open Questions and Limitations

The central open question is whether automated annotation can close the gap with human labels at scale, or whether there is a persistent quality ceiling below the human-annotation floor. SE improves with more completions, but the compute cost of high-N Monte Carlo estimation may approach the cost of human annotation for hard problems, undermining the economic case for automation on the hardest tasks.

A second limitation is domain specificity. PRM800K covers mathematical reasoning, and the generalization of PRM-based verification to other multi-step domains (code, scientific reasoning, planning) remains an active research question. The dataset's influence on the field is substantial precisely because math provides clean ground truth; it is less clear how to construct analogous datasets in domains where correctness is harder to verify.

Finally, the asymmetric scaling relationship between policy and reward model size suggests that PRM800K's value is not static: as policy models grow larger, the PRM trained on this data may become a limiting factor rather than an enabler, creating pressure for either larger or more capable verifiers.

## Relationships

PRM800K is directly referenced in Math-Shepherd, which motivates its automated annotation pipeline as a response to the cost of human labeling at PRM800K scale. It appears as the training corpus and calibration reference in Process Reward Models That Think (THINKPRM). Its role in enabling test-time compute scaling is implicit throughout Scaling LLM Test-Time Compute Optimally and Inference Time Compute. Q* relies on process reward signals of this type for its deliberative planning framework. The dataset connects thematically to [[themes/reward_modeling|reward_modeling]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], and [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]] as a foundational resource whose scarcity has shaped the direction of research in all three areas.
```

## Limitations and Open Questions

## Sources
