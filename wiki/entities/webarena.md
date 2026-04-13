---
type: entity
title: WebArena
entity_type: dataset
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- alignment_and_safety
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.011148236756684735
staleness: 0.0
status: active
tags: []
---
# WebArena

**Type:** dataset
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A benchmark for evaluating web navigation and computer-use agents in realistic web environments.

## Key Findings

1. Most open-source LMMs are unsuitable for web navigation because they reduce image resolution to 224x224 or 336x336, making smaller fonts unrecognizable. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
2. All three LMM backbones (GPT-4V, Claude-3-Opus, GPT-4o) significantly outperform the text-only setting on WebVoyager tasks. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
3. WebVoyager uses Set-of-Mark inspired numerical labeling of interactive web elements on screenshots to facilitate action decision-making, implemented via a rule-based JavaScript tool without any object (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
4. Visual grounding issues account for 24.8% of WebVoyager failures. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
5. GPT-4V's agreement with human annotators reaches kappa=0.70 when provided the full trajectory, on par with inter-human annotator agreement. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
6. WebVoyager operates on real websites via Selenium rather than local simulations, exposing it to real-world challenges like floating ads, pop-up windows, and constant updates. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
7. WebVoyager uses context clipping, retaining only the three most recent observations while keeping the full history of thoughts and actions, to prevent agent confusion from excessive web page observati (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
8. WebVoyager achieves a 59.1% task success rate on the WebVoyager benchmark, significantly surpassing GPT-4 (All Tools) at 30.8% and text-only WebVoyager at 40.1%. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
9. GPT-4V-based automatic evaluation achieves 85.3% agreement with human judgment, making it a reliable evaluator for open-ended web agents. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
10. WebVoyager follows the ReAct prompting paradigm, generating a natural language thought process before producing action code. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
11. Navigation stuck (running out of steps) is the most common failure mode for WebVoyager, accounting for 44.4% of failures. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
12. WebVoyager achieves 30% task success rate on the SeeAct online test set, compared to the best SeeAct autonomous agent's 26%. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
13. Hallucination accounts for 21.8% of WebVoyager failures. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
14. The WebVoyager benchmark consists of 643 tasks across 15 popular websites, with 99.68% of pairwise task similarities below 0.6, demonstrating high task diversity. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")
15. GPT-4o achieves a higher kappa (0.72) with human evaluators than GPT-4V (0.70), while Claude-3-Opus is less reliable with kappa of 0.6. (from "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models")

## Capabilities

- Computer-Using Agent (CUA) achieving 38.1% on OSWorld, 58.1% on WebArena, and 87% on WebVoyager — available via API for automating browser workflows and OS-level tasks (maturity: demo)

## Relationships

## Limitations and Open Questions

## Sources
