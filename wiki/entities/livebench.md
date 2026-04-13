---
type: entity
title: LiveBench
entity_type: dataset
theme_ids:
- alignment_and_safety
- chain_of_thought
- hallucination_and_reliability
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0005837125152594612
staleness: 0.0
status: active
tags: []
---
# LiveBench

LiveBench is a continuously refreshed benchmark designed to address the pervasive contamination problem that undermines static AI evaluations. By automatically generating new questions on a rolling basis and using objective, verifier-friendly scoring, it provides a more reliable signal of model capability than fixed-date datasets whose contents leak into training corpora. Its structure spans multiple task categories — including mathematics and formal reasoning — making it a recurrent reference point in research on test-time compute scaling and inference-time search.

**Type:** dataset
**Themes:** [[themes/alignment_and_safety|Alignment & Safety]], [[themes/chain_of_thought|Chain of Thought]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/long_context_and_attention|Long Context & Attention]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/policy_optimization|Policy Optimization]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory & Dynamics]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

LiveBench addresses the contamination problem that plagues static benchmarks: when test questions are public and persistent, they eventually appear in training data, inflating scores and corrupting comparisons. By generating new questions continuously and scoring them with objective (non-LLM-judge) methods, LiveBench's difficulty signal remains trustworthy over time. It covers two primary domains relevant to recent scaling research — **LiveBench Math** and **LiveBench Reasoning** — making it particularly suited for evaluating models whose core capability claims centre on formal problem-solving.

The benchmark's design philosophy contrasts with "snapshot" datasets like AIME or MATH: rather than a fixed corpus frozen at a point in time, it is a temporal stream. This makes it resistant not only to inadvertent contamination but also to deliberate overfitting, since the distribution of questions shifts before it can be gamed.

## Role in Test-Time Compute Research

LiveBench appears most prominently as an evaluation surface in research on inference-time search. In Sample, Scrutinize and Scale, verification-based search (Verification@200 using Gemini 1.5 Pro) achieves **135/200 on LiveBench Math** and **97/140 on LiveBench Reasoning**, both surpassing o1-Preview — a result that holds across all four benchmarks tested in that work (AIME 2024, MATH, and both LiveBench splits). This matters because LiveBench's anti-contamination design gives the result a credibility that AIME and MATH scores increasingly lack as those datasets become long-lived.

The same paper demonstrates that even strong models retain meaningful error rates that verification can catch: o1-Preview fails to identify 20–30% of wrong responses, and the rewrite step in the verification pipeline matters — ablating it increases false positive and false negative rates by 1–5 percentage points across both MATH and AIME. LiveBench Reasoning provides a harder, less contamination-prone surface to validate that these improvements aren't artefacts.

## Relationship to RLVR and Base Model Coverage

LiveBench also appears indirectly in the context of The Invisible Leash, which studies whether RLVR training genuinely expands a model's solution support or merely concentrates probability mass on already-reachable solutions. The paper's central finding — that support shrinkage consistently exceeds expansion (ProRL-1.5B-v2 loses 175 completions while gaining only 48, a ~3.6:1 ratio), and that base models dominate RLVR models at high sampling budgets — is established across AIME 2024 and related benchmarks, with LiveBench as part of the evaluation landscape. RLVR's gains at pass@1 come at a cost: the trained model assigns higher perplexity to external reasoning traces (Claude Sonnet 4 traces on AIME2024 go from 8.76 to 14.91 after ProRL), indicating narrowing rather than generalisation.

## Limitations and Open Questions

LiveBench's anti-contamination guarantee weakens as generation time increases: any questions generated long enough ago may eventually surface in internet-crawled training data. The refresh cadence therefore becomes critical — if the update frequency falls behind crawl frequency, the contamination gap closes. This is an operational rather than theoretical limitation, but it means the benchmark's validity is contingent on maintenance discipline.

A second limitation is coverage: LiveBench Math and Reasoning are well-suited for evaluating the kinds of formal problem-solving that current scaling research prioritises, but they do not cover code execution, factual recall, long-document tasks, or multimodal reasoning. Research papers that use LiveBench alongside static benchmarks typically do so to sanity-check results rather than as a primary evaluation surface, which suggests the community has not yet fully adopted it as a replacement for older benchmarks.

Finally, the objective-scoring constraint that makes LiveBench contamination-resistant also constrains its task distribution: anything requiring nuanced human judgment — open-ended generation quality, argumentation, creative reasoning — falls outside what LiveBench can currently score reliably.

## Related Entities

- Sample, Scrutinize and Scale — primary source using LiveBench Math and Reasoning as evaluation benchmarks for verification-based search
- The Invisible Leash — uses overlapping benchmark suite; LiveBench as part of the broader evaluation context for RLVR support dynamics
- On the Fundamental Limits of LLMs at Scale — theoretical framing of hallucination inevitability and scaling saturation, relevant to what any benchmark including LiveBench can and cannot measure
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] — the primary research context in which LiveBench results appear
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — RLVR evaluation studies that benchmark against LiveBench-adjacent evaluation suites

## Key Findings

## Relationships

## Sources
