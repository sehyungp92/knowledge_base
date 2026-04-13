---
type: entity
title: OpenWebMath
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- interpretability
- latent_reasoning
- mechanistic_interpretability
- model_architecture
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0005827793650497297
staleness: 0.0
status: active
tags: []
---
# OpenWebMath

> OpenWebMath is a math-focused pretraining corpus curated from web text, used to study the effect of domain-specific data on language model reasoning. Its primary significance lies in demonstrating that high-density reasoning contexts during pretraining — even without task-specific supervision — yield measurable zero-shot gains on mathematical benchmarks, a finding made prominent through its use in Quiet-STaR.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/interpretability|interpretability]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

OpenWebMath is a web-scraped corpus filtered to emphasize mathematical content — derivations, proofs, worked examples, and formal reasoning found across the open web. Unlike curated problem-set datasets, it is broad and unstructured, which makes it a useful testbed for studying how reasoning-dense pretraining data interacts with methods that try to elicit implicit thinking.

Its most documented use is as the continued pretraining corpus for Quiet-STaR experiments. The choice was deliberate: mathematical web text was expected to have a higher density of positions where generating an internal rationale would be predictively useful, compared to general web corpora like C4. Experiments confirmed this — training on OpenWebMath yielded larger zero-shot reasoning improvements than training on C4, supporting the hypothesis that data token-density for reasoning is a meaningful variable in latent thinking methods.

A notable and somewhat counterintuitive finding associated with OpenWebMath is the asymmetry between math and code transfer: while code pretraining (e.g. StarCoder) demonstrably benefits mathematical reasoning, the reverse is weaker — math-focused corpora benefit code less. This challenges the folk assumption that the math–code relationship is symmetric, and suggests the transfer may be directional, perhaps because code has syntactic structure that scaffolds generalisation in ways that mathematical prose does not.

## Role in Quiet-STaR

Within the Quiet-STaR framework, OpenWebMath served as the substrate on which the model learned to generate silent multi-token rationales at every token position. Quiet-STaR's training signal — REINFORCE rewards based on whether a rationale improves prediction of the next true token — is highly sensitive to whether the surrounding context actually rewards deeper processing. Mathematical text provides more such positions than general text, making OpenWebMath a favorable environment for learning useful internal thought tokens.

The gains are concrete: continued pretraining with Quiet-STaR on OpenWebMath pushed zero-shot GSM8K accuracy from 5.9% to 10.9% and CommonsenseQA from 36.3% to 47.2%, with neither benchmark requiring any fine-tuning. These improvements scaled with the number of thought tokens used, suggesting that the corpus contributed to learning rationale quality rather than merely calibrating token probabilities.

## Open Questions and Limitations

Several questions remain unresolved around OpenWebMath's role in this class of methods:

- **Generality**: All documented Quiet-STaR results used OpenWebMath as a continued pretraining corpus on top of an already-pretrained model. Whether the same gains hold when training from scratch — where the base representations are shaped by OpenWebMath from the start — is unknown.
- **Density hypothesis**: The intuition that math text has higher "reasoning token density" is supported by the C4 comparison but has not been rigorously quantified. It is unclear whether the gains stem from mathematical content specifically, or from the structural properties of formal exposition more broadly (definitions, conditionals, step-by-step derivations).
- **Asymmetric transfer**: The weaker math→code transfer compared to code→math is an empirical observation without a mechanistic account. Whether this reflects properties of OpenWebMath specifically (prose-heavy, less syntactically regular), of mathematical reasoning at large, or of current model architectures remains an open question.
- **Coverage**: As a web-sourced corpus, OpenWebMath inherits the biases and coverage gaps of what gets written about publicly — strong in certain areas of applied math and competition problems, likely thin in others.

## Relationships

OpenWebMath is most directly connected to Quiet-STaR, where it served as the primary training corpus. It sits adjacent to discussions of [[themes/pretraining_data|pretraining data]] composition and its downstream effects on [[themes/reasoning_and_planning|reasoning]], and relates to broader questions in [[themes/scaling_laws|scaling laws]] about whether data quality (measured as reasoning density) scales differently from data quantity. The math–code transfer asymmetry connects it to debates in [[themes/pretraining_and_scaling|pretraining and scaling]] about what properties of a corpus drive capability generalisation.

## Key Findings

## Limitations and Open Questions

## Sources
