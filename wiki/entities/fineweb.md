---
type: entity
title: FineWeb
entity_type: dataset
theme_ids:
- agent_evaluation
- agent_systems
- ai_for_scientific_discovery
- ai_market_dynamics
- benchmark_design
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- scaling_laws
- scientific_and_medical_ai
- software_engineering_agents
- synthetic_data_generation
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0028136968241272643
staleness: 0.0
status: active
tags: []
---
# FineWeb

**Type:** dataset
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Web-scale pretraining dataset used as the validation set for the NanoGPT Speedrun, with a target cross-entropy loss of 3.28.

## Key Findings

1. The benchmark consumed approximately 6,840 × 8 H100 hours across 6,840 agent runs for its full evaluation. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
2. The NanoGPT Speedrun community effort reduced GPT-2 training time from 45 minutes to below 3 minutes between June 2024 and May 2025. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
3. Recent reasoning LLMs combined with state-of-the-art scaffolds struggle to reimplement already-known scientific innovations even when given detailed hints. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
4. All tested AI agents fail to recover more than 20% of the speedup achieved by human solutions when given no hints. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
5. Gemini-2.5-Pro and Claude-3.7-Sonnet achieve the lowest IQM performance among tested models, lagging behind even the open-weights DeepSeek-R1. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
6. Pseudocode hints are the most effective individual hint format, enabling o3-mini to recover approximately 40% of the human speedup. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
7. In cumulative speedrun experiments, agent performance drops sharply after the first record, recovering only ~20% of speedup for the third record versus ~60% for the second. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
8. Claude-3.7-Sonnet generates significantly more buggy nodes than other models, with buggy node fraction gradually overtaking working nodes in the search tree. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
9. Gemini-2.5-Pro produces more robust (less buggy) code than other models but fails to correctly implement the efficient solutions described in hints. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
10. DeepSeek-R1 agents perform worse with individual hints than without them, producing buggy code when trying to implement complex described changes. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
11. Automated reproducibility (reimplementing experiments from descriptions) is a necessary but not sufficient skill for autonomous research agents. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
12. o3-mini generally achieves equal or better Fraction of Speedup Recovered than other models for all hint levels. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
13. The Muon optimizer, invented through the NanoGPT Speedrun, has been demonstrated to show training benefits for much larger modern LLMs beyond GPT-2 scale. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
14. Multi-AIDE search scaffold outperforms all other scaffold variants in aggregate IQM evaluation. (from "The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements")
15. Synthetic data is now used throughout the entire LLM pipeline, including both pre-training and post-training stages. (from "Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace [LS Live! @ NeurIPS 2024]")

## Relationships

## Limitations and Open Questions

## Sources
