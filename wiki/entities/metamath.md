---
type: entity
title: MetaMath
entity_type: dataset
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 3.5117951975158245e-05
staleness: 0.0
status: active
tags: []
---
# MetaMath

> MetaMath is a math-specific supervised fine-tuning dataset that became a foundational baseline in the literature on LLM mathematical reasoning. Its primary significance lies not in its own performance but in how it serves as a launchpad for subsequent techniques: process reward models like MATH-SHEPHERD are evaluated against MetaMath-trained baselines, making it a consistent reference point for measuring gains from step-level supervision, reinforcement learning, and verification.

**Type:** dataset
**Themes:** [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/search_and_tree_reasoning|Search & Tree Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

MetaMath is a supervised fine-tuning dataset designed specifically for mathematical reasoning, most notably used to fine-tune Llama-2-7B and lift its GSM8K accuracy from 49.5% to 65.2%. That gain alone established it as a credible starting point for math reasoning research and made MetaMath-tuned models the standard policy from which subsequent work measures further improvement.

Its role in the literature is largely infrastructural. Papers like Math-Shepherd treat MetaMath fine-tuned models as the supervised fine-tuning baseline, then layer process reward models, reinforcement learning, and verification on top to demonstrate additive gains. This makes MetaMath both a benchmark reference and a ceiling to surpass, rather than a final solution.

## Significance as a Baseline

The MetaMath baseline is what gives MATH-SHEPHERD's results their legibility. Starting from a MetaMath-trained Mistral-7B at 77.9% GSM8K accuracy, step-by-step PPO supervised by MATH-SHEPHERD pushes it to 84.1% on GSM8K and from 28.6% to 33.0% on the harder MATH dataset. Adding MATH-SHEPHERD as a verifier on top of the PPO-trained model further raises those figures to 89.1% and 43.5% respectively. The consistent finding is that reinforcement learning and verification are complementary rather than redundant: the PPO-trained Mistral-7B outperforms the supervised fine-tuning baseline by 7.2% on MATH with self-consistency as verifier, suggesting that MetaMath-level SFT leaves substantial room that RL and process supervision can exploit.

At the high end, DeepSeek-67B achieves 93.3% on GSM8K and 48.1% on MATH with MATH-SHEPHERD verification, described as unprecedented for open-source models not relying on additional tools. MetaMath's original 65.2% on Llama-2-7B contextualises how far the field has moved in a short period.

## Role in Process Reward Model Research

MetaMath's influence extends into the construction and evaluation of process reward models. MATH-SHEPHERD's central insight, that step quality can be estimated automatically via Monte Carlo-style completion (inspired by MCTS), was validated in part by showing that soft estimation (SE) of step quality converges toward human-annotated distributions as the number of completions N increases, whereas hard estimation (HE) does not. This distinction matters because it determines how reliably automated PRM training data represents ground truth, and MetaMath-trained completers are used to generate that data.

The quality of the completer model used to generate PRM training data proves significant: larger completers produce higher-quality process annotations, and the training data quality of the completer itself has downstream effects on annotation quality. This creates a recursive dependency where the value of a dataset like MetaMath is partly a function of what gets built on top of it, and how well those downstream models are trained.

## Limitations and Open Questions

MetaMath's ceiling is visible in the data. Its contribution is in supervised fine-tuning, and SFT alone increasingly appears insufficient for frontier math reasoning. The gains from RL and PRM layered on top of MetaMath-tuned baselines consistently exceed the SFT baseline, which implies that the dataset's format (fine-tuning on demonstrations) captures something real but leaves implicit reasoning quality on the table.

PRM methods show superior data efficiency over ORM: PRM outperforms ORM by roughly 4% accuracy with only 10k training instances and has a higher performance ceiling. If that ceiling is the relevant comparison, MetaMath's demonstration-based approach sits below both. Whether MetaMath-style SFT remains a necessary first stage or can be bypassed entirely by stronger RL regimes is an open question, particularly as methods like rStar-Math and Q* push toward self-evolved and search-augmented reasoning without relying on static fine-tuning datasets.

The cost of generating high-quality PRM training data via automated completion remains a practical constraint. MATH-SHEPHERD acknowledges that the completion process demands significant compute, though it remains far cheaper than human annotation. Human annotation is described as a bottleneck that hinders PRM advancement, particularly for intricate multi-step tasks requiring advanced annotator skill. MetaMath sidesteps this by relying on demonstration data, but that choice trades annotation cost for a shallower signal about reasoning quality.

## Relationships

MetaMath is tightly coupled with Math-Shepherd as the baseline policy from which RL and PRM gains are measured. It connects to the broader [[themes/synthetic_data_generation|Synthetic Data Generation]] theme through the question of whether automatically constructed training data can substitute for human-annotated process supervision. Its use in rStar-Math and Q* contexts situates it within the [[themes/search_and_tree_reasoning|Search & Tree Reasoning]] lineage, where MCTS-inspired step evaluation is compared against and built upon static SFT datasets. The trajectory from MetaMath's 65.2% to DeepSeek-67B's 93.3% with MATH-SHEPHERD verification illustrates the compound effect of layering [[themes/post_training_methods|post-training methods]] and [[themes/reward_modeling|reward modeling]] on a strong but bounded SFT foundation.

## Key Findings

## Sources
