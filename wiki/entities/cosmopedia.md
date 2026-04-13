---
type: entity
title: Cosmopedia
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- latent_reasoning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- scaling_laws
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0011813721766860226
staleness: 0.0
status: active
tags: []
---
# Cosmopedia

> Cosmopedia is a large-scale synthetic pretraining corpus developed at HuggingFace, designed to generate high-quality educational and encyclopedic text across code, mathematics, and general knowledge domains. It represents one of the most prominent demonstrations that carefully constructed synthetic data can serve as a viable — and in some cases superior — substitute for web-scraped pretraining corpora, particularly for small language models where data quality has outsized impact.

**Type:** dataset
**Themes:** [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/pretraining_data|pretraining_data]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/scaling_laws|scaling_laws]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Overview

Cosmopedia is a synthetic pretraining corpus spanning three broad domain categories — Code, Math, and Knowledge — generated using frontier language models to produce textbook-style, instructive content. It was developed as part of HuggingFace's push toward high-quality small model training, closely associated with the SmolLM lineage and Loubna Ben Allal's work on synthetic and compact models (see Best of 2024: Synthetic Data / Smol Models).

The core thesis behind Cosmopedia is that web-scraped data, while abundant, is noisy and pedagogically unstructured. By generating synthetic content conditioned on educational objectives — textbooks, exercises, explanations — a smaller but denser corpus can achieve better sample efficiency, especially for reasoning-heavy benchmarks.

## Role in MobileLLM-R1

Cosmopedia's most concrete downstream validation comes from its inclusion in the data mixture for MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes. The MobileLLM-R1 training pipeline incorporates Cosmopedia across its Code, Math, and Knowledge tracks as part of a curated pretraining mix designed to maximise reasoning capability at sub-billion parameter scale.

The results are striking. MobileLLM-R1-950M achieves an AIME score of 15.5 versus 0.6 for OLMo-2-1.48B and 0.3 for SmolLM-2-1.7B, and attains 5× higher MATH accuracy than OLMo 1.24B and 2× higher than SmolLM2 1.7B — despite having fewer parameters than either baseline. Crucially, MobileLLM-R1-950M matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks while training on only 11.7% of Qwen3's proprietary 36T-token corpus. This delta is not attributable to architecture or post-training alone; it implicates data quality and composition, with Cosmopedia as a central ingredient.

This positions Cosmopedia as evidence for a broader claim in [[themes/scaling_laws|scaling laws]] research: at small model scales, data quality and pedagogical structure may partially substitute for raw token count.

## Significance for Synthetic Data Research

Cosmopedia sits at the intersection of two trends. First, the recognition that [[themes/pretraining_data|pretraining data]] curation — rather than just scale — is a primary lever for capability. Second, the emergence of [[themes/synthetic_data_generation|synthetic data generation]] as a practical alternative to crawled corpora, made viable by the availability of capable teacher models.

What distinguishes Cosmopedia from simpler augmentation approaches is its domain breadth and its orientation toward knowledge density. Rather than paraphrasing existing web content, it generates structured educational material designed to make concepts learnable — a property that appears to transfer into reasoning performance downstream.

## Open Questions and Limitations

Several important questions remain open. The attribution problem is non-trivial: MobileLLM-R1's performance gains arise from a combination of pretraining data (including Cosmopedia), post-training with reinforcement learning, and architectural choices. Isolating Cosmopedia's specific contribution requires ablations not yet publicly available.

There is also the question of coverage depth versus breadth. Cosmopedia's synthetic generation process is conditioned on prompts derived from web sources, meaning its knowledge distribution is not independent of the web — it may inherit blind spots and biases while removing surface-level noise. Whether this trades one class of distributional problem for another is unclear.

Finally, the scaling behaviour of synthetic corpora like Cosmopedia beyond the sub-billion regime is underexplored. The evidence base is strongest for small models where data quality has high leverage; whether the advantages persist at 7B+ parameters and trillion-token scales is an open empirical question, touching on fundamental tensions in [[themes/pretraining_and_scaling|pretraining and scaling]] research.

## Relationships

Cosmopedia is closely associated with HuggingFace's SmolLM and SmolLM2 model families, which share overlapping training data lineage. It feeds into the MobileLLM-R1 mixture alongside other curated sources, collectively enabling the open training recipe described in MobileLLM-R1. Its development is contextualised in Best of 2024: Synthetic Data / Smol Models, which situates Cosmopedia within the broader 2024 trend of synthetic data gaining traction as a first-class pretraining ingredient. Thematically, it connects to [[themes/finetuning_and_distillation|finetuning and distillation]] via its use of frontier models as generators, and to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] through the post-training stages that build on its pretraining foundation.

## Key Findings

## Limitations and Open Questions

## Sources
