---
type: entity
title: ScreenSpot
entity_type: dataset
theme_ids:
- agent_systems
- chain_of_thought
- computer_use_and_gui_agents
- finetuning_and_distillation
- generative_media
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00022326341695763134
staleness: 0.0
status: active
tags: []
---
# ScreenSpot

> ScreenSpot is a benchmark family for GUI grounding — the task of localizing UI elements (buttons, fields, icons) from natural language descriptions. It has become a standard evaluation suite for vision-language models and GUI agents, with two variants: ScreenSpot-V2 covering general consumer GUIs, and ScreenSpot-Pro targeting the harder regime of high-resolution professional environments where elements are small, dense, and visually complex.

**Type:** dataset
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

ScreenSpot occupies a specific niche in multimodal evaluation: rather than testing general visual comprehension, it tests *spatial grounding* — whether a model can translate a natural language instruction ("click the save button", "find the search field") into a precise pixel-level or bounding-box location on a real UI screenshot. This makes it particularly diagnostic for the growing class of GUI agents that must operate autonomously within desktop and web environments.

The benchmark family's two tiers reflect a deliberate difficulty gradient. ScreenSpot-V2 covers general consumer-facing GUIs — websites, mobile apps, desktop software — where elements are typically large and well-spaced. ScreenSpot-Pro raises the bar substantially by targeting professional tools (IDEs, CAD software, enterprise dashboards) where elements are small, visually similar, and embedded in cluttered high-resolution layouts. This distinction matters because many models that perform credibly on V2 degrade sharply on Pro, exposing a gap between coarse scene understanding and precise visual localization.

## Significance as an Evaluation Surface

ScreenSpot has attracted attention as a benchmark precisely because it surfaces limitations that general VQA or OCR benchmarks miss. Several architectural and training decisions in frontier VLMs are directly legible through ScreenSpot performance.

For instance, Qwen2.5-VL Technical Report reveals how deeply GUI grounding shaped design choices throughout the stack. The model's coordinate representation abandons normalization in favor of *actual image dimensions*, so that bounding boxes and points carry real-world scale information — a decision motivated in part by grounding benchmarks like ScreenSpot that demand precise localization rather than approximate region descriptions. Similarly, the introduction of window attention in the visual encoder, where only four layers use full self-attention while the rest use 112×112 pixel windows, is a trade-off between global context and computational cost that directly affects the model's ability to find small elements in large screenshots.

The coordinate representation choice is worth dwelling on: traditional VLMs normalize coordinates to [0, 1] regardless of image resolution, which loses scale information and makes it harder to distinguish a 5-pixel icon from a 50-pixel button at the same relative position. Qwen2.5-VL's raw-coordinate approach represents a deliberate inductive bias toward tasks like ScreenSpot-Pro, where element size is a meaningful signal.

## Connection to RL-Based GUI Training

GUI-G1 and Grounded Reinforcement Learning for Visual Reasoning situate ScreenSpot within an emerging training paradigm: using RL with verifiable rewards to improve GUI grounding without requiring dense human annotations. Because ScreenSpot provides ground-truth element coordinates, it can serve as a reward signal — a predicted click either lands on the correct element or it doesn't. This binary verifiability makes ScreenSpot-style data well-suited to GRPO and similar policy optimization methods, which require a reward function that doesn't need a learned critic.

This convergence of benchmark and training signal is notable. ScreenSpot is not just measuring capability; it is shaping how that capability gets trained. Models trained with RL against ScreenSpot-style rewards learn to reason about spatial layout explicitly, often generating chain-of-thought steps that describe element position before committing to a coordinate — a behavior that improves accuracy but also interpretability.

## Open Questions and Limitations

Several open questions surround ScreenSpot as an evaluation surface:

**Coverage of dynamic and interactive UIs.** ScreenSpot evaluates static screenshots. Real GUI agents must handle hover states, dropdowns that appear on interaction, and multi-step workflows where the target element only becomes visible after prior actions. Performance on ScreenSpot does not straightforwardly predict performance in live agentic loops.

**Instruction ambiguity.** Natural language instructions in the benchmark may not fully capture the ambiguity of real user commands. "Click the button on the right" is harder to ground when multiple buttons appear on the right, and it is unclear how consistently ScreenSpot's instructions probe this failure mode.

**The V2 / Pro gap as a diagnostic.** The performance gap between ScreenSpot-V2 and ScreenSpot-Pro is informative but not yet well-characterized mechanistically. It is unclear whether it primarily reflects resolution handling, visual token budget limitations, training data distribution, or some combination. Understanding this gap is important for knowing which architectural interventions (dynamic resolution, larger vision encoders, longer context windows) are most likely to close it.

**Generalization beyond the benchmark.** Models fine-tuned specifically on ScreenSpot-style data may show inflated benchmark numbers without corresponding improvements in downstream agentic tasks. The field lacks a clear protocol for distinguishing benchmark-specific fitting from genuine GUI grounding capability.

## Relationships

ScreenSpot is closely linked to the broader [[themes/computer_use_and_gui_agents|computer use and GUI agents]] landscape, serving as a shared reference point for models including Qwen2.5-VL, GUI-G1, and systems trained with grounded RL. Its two-tier structure (V2 / Pro) parallels the general trend in multimodal benchmarks toward harder, more realistic evaluation regimes. The benchmark intersects with [[themes/vision_language_models|vision language models]] at the level of coordinate representation and visual token design, and with [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] through its use as a verifiable reward signal in policy optimization pipelines.

## Key Findings

## Limitations and Open Questions

## Sources
