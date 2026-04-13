---
type: entity
title: ARC-Easy
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- latent_reasoning
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- scaling_laws
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00016465212828283812
staleness: 0.0
status: active
tags: []
---
# ARC-Easy

ARC-Easy (AI2 Reasoning Challenge — Easy subset) is a widely adopted commonsense science reasoning benchmark developed by the Allen Institute for AI. It presents multiple-choice questions drawn from elementary and middle-school science exams, targeting general scientific knowledge and basic inferential reasoning rather than deep domain expertise. Its significance lies in its ubiquity as a standard evaluation target: virtually any new approach to language model reasoning, multi-agent coordination, or training methodology uses ARC-Easy to anchor comparative claims, making it a consistent reference point across otherwise heterogeneous experimental setups.

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/in_context_and_meta_learning|In-Context & Meta-Learning]], [[themes/knowledge_and_memory|Knowledge & Memory]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/pretraining_data|Pretraining Data]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_learning|Test-Time Learning]], [[themes/transformer_alternatives|Transformer Alternatives]]

## Overview

ARC-Easy consists of science questions that are answerable by most retrieval-based systems, as opposed to the harder ARC-Challenge split which requires more complex multi-hop reasoning. Questions cover topics like biology, physics, and earth science at a level that tests broad factual grounding and shallow inferential ability. The benchmark is part of the broader ARC corpus (Clark et al., 2018) and has become a staple of NLP evaluation suites — appearing in BIG-Bench, the Open LLM Leaderboard, and countless ablation tables.

## Role as an Evaluation Target

Within the papers in this knowledge base, ARC-Easy appears primarily as one benchmark within multi-benchmark evaluation suites rather than as the central object of study. The most direct evidence comes from Latent Collaboration in Multi-Agent Systems, where it is one of 9 benchmarks used to evaluate **LatentMAS** — a training-free framework that enables LLM agents to collaborate entirely in latent space rather than through text tokens.

The LatentMAS results on this benchmark are representative of the broader pattern observed across all 9 evaluation tasks: the framework achieves up to 14.6% higher accuracy than text-based multi-agent baselines while simultaneously reducing output token usage by 70.8–83.7% and delivering 4×–4.3× faster end-to-end inference. The mechanism behind this is architecturally significant — rather than generating tokens for inter-agent communication, LatentMAS transfers layer-wise KV caches between agents, so each successive agent's generation is conditioned on both the predecessor's full working memory and its latent reasoning trace. This transfer is provably information-preserving (Theorem 3.3 in the source), meaning no signal is lost relative to explicit token exchange.

ARC-Easy also appears as an evaluation surface in Diffusion Beats Autoregressive in Data-Constrained Settings and Transformer-Squared: Self-Adaptive LLMs, where it serves a similar role: a stable, well-understood benchmark against which novel architectural or training approaches can be measured without ambiguity about task difficulty or scoring.

## Limitations and Open Questions

ARC-Easy's very accessibility is also its principal limitation as a discriminating benchmark. Because most current frontier models saturate or near-saturate the easy split, marginal accuracy differences on ARC-Easy reveal little about the depth or robustness of reasoning; they primarily confirm that a method does not regress on basic factual recall. The benchmark cannot distinguish between a model that retrieves the answer from parametric memory and one that reasons its way to it — a critical gap for systems like LatentMAS, where the *quality* of latent reasoning (not just the final answer) is the primary innovation.

This saturation problem raises an open question that runs through several papers in the library: **as commonsense benchmarks age, what replaces them as reliable discriminators?** ARC-Easy was designed at a time when even modest retrieval systems struggled; it no longer stress-tests the upper end of current architectures. The harder ARC-Challenge split partially addresses this, but both splits are increasingly viewed as insufficient proxies for genuine reasoning capability.

A secondary concern is distribution shift: ARC-Easy questions reflect a particular cultural and curricular context (US elementary science education), which may not generalise to the kinds of implicit scientific reasoning required in research or professional settings — precisely the domain that a knowledge engine like this project targets.

## Relationships

ARC-Easy is closely associated with **ARC-Challenge** (the harder companion split) and shares evaluation infrastructure with benchmarks like **HellaSwag**, **WinoGrande**, and **PIQA**, all of which appear in the same evaluation suites. Within this library it is most directly connected to the LatentMAS work (Latent Collaboration in Multi-Agent Systems) and, more peripherally, to architectural comparison papers (Diffusion Beats Autoregressive, Transformer-Squared) that use it to anchor broad capability comparisons.

## Key Findings

## Sources
