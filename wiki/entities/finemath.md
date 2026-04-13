---
type: entity
title: FineMath
entity_type: dataset
theme_ids:
- adaptive_computation
- chain_of_thought
- latent_reasoning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 8.02287780461974e-05
staleness: 0.0
status: active
tags: []
---
# FineMath

> FineMath is a math-focused pretraining corpus that has emerged as a key ingredient in recent efforts to train capable small-scale reasoning models. It serves a dual role across the literature: as a domain-specific component of curated pretraining mixes targeting efficient reasoning emergence, and as the experimental substrate for studying whether language models can learn more effectively from latent reasoning traces rather than raw text alone.

**Type:** dataset
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/chain_of_thought|Chain of Thought]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/pretraining_data|Pretraining Data]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

FineMath is a curated corpus of mathematical text designed for pretraining language models on formal and semi-formal reasoning content. Its significance in recent work lies less in its raw scale and more in how it has been used to probe fundamental questions about data quality, reasoning emergence, and the limits of what can be learned from math-dense text alone.

Two distinct lines of research have converged on FineMath as a critical experimental variable. In the MobileLLM-R1 work, FineMath constitutes the Math (M) domain category within a carefully composed ~2T token pretraining mix, where its inclusion alongside FineWeb-Edu and code corpora enables surprisingly strong reasoning capabilities in sub-billion parameter models. In the BoLT (Reasoning to Learn from Latent Thoughts) work, FineMath serves as the primary corpus for testing whether augmenting pretraining data with synthesized latent thoughts yields measurable improvements over training on raw text.

## Key Findings

### FineMath as a Component of Efficient Pretraining

The MobileLLM-R1 results challenge the prevailing assumption that reasoning capabilities require massive pretraining corpora. By composing a high-quality ~2T token mix that includes FineMath in the math domain, the MobileLLM-R1-950M model achieves an AIME score of 15.5 versus 0.6 for OLMo-2-1.48B and 0.3 for SmolLM-2-1.7B, attains 5× higher MATH accuracy than OLMo 1.24B and 2× higher than SmolLM2 1.7B, and matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks despite using only 11.7% of Qwen3's 36T pretraining tokens.

These results suggest that FineMath's value is not simply additive; the composition of the full pretraining mix matters. Data ablations show that removing FineWeb-Edu causes the largest degradation across all capability domains (knowledge, math, and code), attributed to its broad web-based composition connecting diverse domains. This implies FineMath's contribution is more focused and domain-specific, likely most important for precise mathematical reasoning rather than general knowledge. The broader takeaway is that strong reasoning can emerge from quality-over-quantity data curation, where FineMath is a necessary but not sufficient ingredient.

The MobileLLM-R1 analysis also highlights a structural dependency between pretraining quality and post-training reasoning elicitation: models with stronger pre-training and mid-training, including exposure to FineMath, exhibit more robustly embedded knowledge that facilitates the emergence of reasoning capabilities during RL-based post-training, even when all models receive identical supervised fine-tuning.

### FineMath as a Substrate for Latent Thought Learning

The BoLT paper takes a different angle, using FineMath not just as training data but as the experimental ground for validating whether implicit reasoning traces (latent thoughts) can be synthesized and injected back into pretraining to improve learning efficiency. The core finding is stark: augmenting FineMath with GPT-4o-mini synthesized latent thoughts achieves 25.38% on the MATH benchmark, compared to just 5.74% when training on raw FineMath data and approximately 1× for synthetic chain-of-thought paraphrases. The BoLT EM algorithm's surrogate posterior achieves an importance-weighted ELBO that is provably tighter than the naive ELBO, and a 1B model can bootstrap its own performance across at least three EM iterations on FineMath without task-specific data.

This line of work frames FineMath as a useful proving ground precisely because its domain is dense enough in implicit reasoning structure that latent thought synthesis yields measurable signal. Whether this result generalizes beyond math-heavy corpora remains an open question.

## Known Limitations

The limitations exposed by FineMath-centric experiments are significant and somewhat sobering. The BoLT results are demonstrated exclusively on FineMath; transfer to general-domain pretraining data is unvalidated and may not yield measurable improvements. This is not a minor gap: the mechanism driving latent thought benefits (rich implicit reasoning structure in math text) may be specific to formal domains and absent from typical web text.

More critically, extended math-focused pretraining on FineMath actively degrades general capabilities. MMLU-STEM performance across BoLT iterations fell within the noise floor (below 28%), and general domain next-token-loss on the DCLM corpus worsened with each EM iteration. This reveals a real tension: the same properties that make FineMath valuable for eliciting mathematical reasoning create a domain-specialization cost. A model pretrained heavily on FineMath may be a stronger math reasoner but a weaker general knowledge model, a tradeoff that is not resolved by the current evidence.

This limitation matters for practical deployment: sub-billion models trained on FineMath-heavy mixes (like MobileLLM-R1) are compelling for math and code benchmarks, but the performance on broader knowledge tasks deserves scrutiny that the current ablation studies do not fully provide.

## Relationships

FineMath is closely paired with **FineWeb-Edu** in the MobileLLM-R1 pretraining mix; the two corpora appear to serve complementary roles (broad connective knowledge vs. focused mathematical depth). It is also functionally related to **MATH** (the benchmark by Hendrycks et al.) as the standard evaluation target for FineMath-trained models. The BoLT paper connects FineMath directly to the emerging theme of latent reasoning and synthetic data augmentation, situating it alongside work on chain-of-thought distillation and self-improvement via EM-style bootstrapping.

Sources: MobileLLM-R1: Exploring the Limits of Sub-Billion Language Model Reasoners with Open Training Recipes, Reasoning to Learn from Latent Thoughts, Parallel Scaling Law for Language Models

## Limitations and Open Questions

## Sources
