---
type: entity
title: OmniMath
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
- test_time_compute_scaling
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 2.1199373492161388e-05
staleness: 0.0
status: active
tags: []
---
# OmniMath

> OmniMath is a competition-level mathematical reasoning dataset comprising 4,428 problems and solutions sourced from official competitions. It has become a key resource for benchmarking and training advanced reasoning systems, serving both as a training corpus for reinforcement-based pre-training approaches and as a rigorous evaluation suite for step-level process verifiers.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|Chain of Thought]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

OmniMath consists of 4,428 competition-level mathematical problems drawn from official competition sources, paired with full solutions. This positions it at the harder end of the mathematical reasoning spectrum — well beyond grade-school or olympiad-lite benchmarks — making it suitable for probing genuine symbolic and multi-step reasoning rather than pattern matching. A curated 1K subset of OmniMath's problem-prefix pairs appears in ProcessBench, where it serves to evaluate step-level verifiers on their ability to identify errors at intermediate reasoning steps rather than only at final answers.

## Role in Reinforcement Pre-Training

The most substantial use of OmniMath documented in the library is as the training corpus for Reinforcement Pre-Training (RPT). RPT reframes next-token prediction as a reasoning task: given a context in the pre-training corpus, the model generates a chain of thought before predicting the next token, and correctness of that prediction serves as the verifiable reward signal. OmniMath's competition problems and solutions provide suitably complex, high-entropy token sequences where standard next-token prediction requires genuine reasoning rather than surface-level pattern completion.

Crucially, RPT applies token-level data filtering before training — using DeepSeek-R1-Distill-Qwen-1.5B as a lightweight proxy model to identify tokens that are difficult to predict. This concentrates training compute on the genuinely challenging portions of the OmniMath corpus, avoiding wasted steps on easy or low-information tokens. The base model used in these experiments is DeepSeek-R1-Distill-Qwen-14B, selected because its existing reasoning capabilities make it a productive starting point for RL-based training. Optimization proceeds via GRPO, implemented through the `verl` library with `vllm` for inference.

The reward signal in RPT is notably clean by RL standards: a prefix-matching reward checks whether the model's next-token prediction is correct, including predictions that span multiple tokens or involve out-of-vocabulary tokens. This rule-based, direct grounding in ground-truth corpus tokens inherently limits reward hacking — a standing problem with learned reward models — and removes the dependency on costly human preference annotations that constrains RLHF at scale.

## Significance for Scaling and Generalization

OmniMath's role in RPT connects it to several broader claims about scaling. RPT exhibits favorable scaling properties on the dataset: next-token prediction accuracy improves consistently as training compute increases, suggesting the corpus is rich enough that more compute continues to yield signal rather than saturating quickly. Beyond in-distribution accuracy, RPT trained on OmniMath improves zero-shot performance on downstream tasks and provides a stronger foundation for subsequent reinforcement fine-tuning — meaning gains from harder pre-training on competition mathematics transfer beyond the mathematics domain itself.

This positions OmniMath not merely as a mathematics evaluation tool but as a proving ground for the thesis that RL-based pre-training on genuinely hard, verifiable corpora can substitute for domain-specific annotation pipelines. The dataset's coverage of official competition problems gives it sufficient difficulty and diversity to expose the limits of reasoning without extensive curation effort.

## Limitations and Open Questions

The primary structural limitation is scope: at 4,428 problems OmniMath is large enough for meaningful experiments but small relative to the scale of general pre-training corpora. It is also intrinsically domain-specific — competition mathematics — which leaves open whether the scaling and generalization benefits observed in RPT would replicate on equally challenging corpora from other structured domains (formal proofs, code, scientific reasoning). The token-level filtering approach mitigates data efficiency concerns somewhat, but the regime where OmniMath exhausts its training signal has not been characterized.

As a benchmark subset within ProcessBench, the 1K problem-prefix sample raises standard questions about representativeness: whether this slice captures the difficulty distribution of the full dataset and whether step-level verifier performance on it predicts performance on held-out competition problems from different sources.

## Related Sources

- Reinforcement Pre-Training — primary source; uses OmniMath as the RL pre-training corpus
- Process Reward Models That Think — includes OmniMath as a benchmark component within ProcessBench
- Optimizing Test-Time Compute via Meta Reinforcement Fine-Tuning — adjacent work on RL-based reasoning improvement

## Key Findings

## Relationships

## Sources
