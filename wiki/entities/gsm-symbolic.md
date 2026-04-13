---
type: entity
title: GSM-Symbolic
entity_type: dataset
theme_ids:
- benchmark_design
- context_engineering
- evaluation_and_benchmarks
- interpretability
- knowledge_and_memory
- mathematical_and_formal_reasoning
- model_behavior_analysis
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0001001742801500074
staleness: 0.0
status: active
tags: []
---
# GSM-Symbolic

> GSM-Symbolic is a template-based symbolic variant of GSM8K designed to probe the robustness of mathematical reasoning in large language models by generating structurally varied problem instances from a fixed set of templates. It has become a key out-of-distribution evaluation benchmark for reasoning research, most notably surfacing fragilities in how models generalize arithmetic reasoning beyond the memorized distribution of the original GSM8K test set.

**Type:** dataset
**Themes:** [[themes/benchmark_design|benchmark_design]], [[themes/context_engineering|context_engineering]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_behavior_analysis|model_behavior_analysis]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

GSM-Symbolic was introduced in GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models as a controlled methodology for stress-testing LLM math reasoning beyond static benchmark memorization. The dataset is constructed from 100 GSM8K templates, each instantiated into 50 distinct samples, yielding 5,000 total problems organized into 50 dataset variants of 100 examples each. This design allows researchers to measure not just point accuracy but variance across symbolic perturbations of the same underlying problem structure — a much stronger signal of genuine reasoning than a single fixed test set. The benchmark includes difficulty tiers (P1 and P2) that modulate problem complexity while preserving the symbolic template structure.

## Key Findings

### Reasoning Robustness and What GSM-Symbolic Reveals

The core motivation behind GSM-Symbolic is the suspicion that LLM performance on GSM8K may partly reflect pattern matching on a familiar test distribution rather than robust mathematical reasoning. By generating many semantically equivalent but symbolically varied instances from the same templates, the benchmark makes it possible to detect sensitivity to surface-level variation that a genuine reasoner should be immune to. The variance in model performance across the 50 dataset variants — even when underlying problem structure is identical — is the key diagnostic signal: it exposes brittleness that aggregate accuracy scores obscure.

### Role in Long-Horizon Reasoning Research

GSM-Symbolic has been adopted as an out-of-distribution evaluation target in the h1 curriculum RL framework, where it serves as a probe for whether training on composed GSM8K chains generalizes beyond the training distribution. The h1 findings illuminate something structurally important about LLM reasoning: even before any RL training, single-step GSM8K accuracy stands at 82.79%, but long-horizon performance collapses far faster than independent-error compounding would predict (which would yield 68.54% at h=2 and 56.75% at h=3). Instead, observed accuracy is dramatically lower, implicating non-independent, correlated error sources — models are not failing randomly but systematically when required to chain dependent reasoning steps.

Standard RLVR on single-step (h=1) data can improve short-horizon accuracy without yielding any improvement at longer reasoning horizons, confirming that short-horizon training does not transfer. Curriculum RL on composed chains, by contrast, achieves a 175% improvement on explicit h=5 problems (3.57% → 9.82%), improves MATH-500 from 64.20% to 69.20%, and delivers a 2.06× gain on AIME 2024 (5.10% → 10.52%) — all without step-level labels, process reward models, or inference-time search. Notably, these gains also transfer to tasks entirely unrelated to GSM8K structure: propositional logic improves from 22.90% to 47.10% on ReasoningGym, and Hash-hop (ultra-long-context retrieval) improves from 15.98% to 18.73%.

### Connection to Test-Time Compute

The appearance of GSM-Symbolic in the context of Sleep-time Compute is peripheral — it emerges as an evaluation surface for a broader question about whether pre-processing context at sleep time (producing a re-represented context c′ before the query arrives) can substitute for inference-time scaling. The structural similarity is notable: both research threads use GSM-style problems to probe how far reasoning can be extended beyond standard single-pass inference.

## Limitations and Open Questions

GSM-Symbolic's template-based construction is both its strength and its constraint. Because all problems derive from a finite set of 100 GSM8K templates, it measures robustness within a specific narrow domain of elementary arithmetic word problems — not general symbolic reasoning or multi-domain mathematics. Performance on GSM-Symbolic does not straightforwardly predict behavior on harder competition mathematics (AIME, AMC) or on reasoning tasks with qualitatively different structure.

The gap between predicted and observed long-horizon performance (as surfaced by h1) remains mechanistically underexplained. That errors are non-independent suggests correlated failure modes — possibly attention drift, context management failures, or compounding representation errors — but the precise source has not been identified. Whether curriculum RL on composed GSM8K chains is truly teaching generalizable long-horizon reasoning or is learning a more sophisticated form of pattern matching that happens to transfer to structurally similar domains is an open question. The transfer to propositional logic and Hash-hop is encouraging but not conclusive.

It is also worth noting that h1's use of GSM-Symbolic as an OOD benchmark is itself a methodological choice: training on composed GSM8K chains while evaluating on GSM-Symbolic assumes sufficient distributional distance between the two, which may not hold perfectly given their shared template ancestry.

## Relationships

- **GSM-Symbolic paper** — primary source; introduces the benchmark construction methodology and uses it to probe mathematical reasoning fragility in frontier models
- **h1** — uses GSM-Symbolic (P1/P2) as an out-of-distribution test of curriculum RL generalization; findings on long-horizon error compounding are directly indexed against GSM8K performance
- **Sleep-time Compute** — peripheral appearance; uses GSM-style problems as evaluation substrate for pre-query context rewriting
- **[[themes/benchmark_design|benchmark_design]]** — GSM-Symbolic exemplifies the template-sampling approach to measuring reasoning robustness rather than raw accuracy
- **[[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]** — h1's curriculum RL results are benchmarked against GSM-Symbolic as a probe of OOD generalization from composed training data
- **[[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]** — central domain; the benchmark is specifically designed to test whether symbolic variation exposes the limits of LLM mathematical reasoning

## Sources
