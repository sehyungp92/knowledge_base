---
type: entity
title: System 1 / System 2 Reasoning
entity_type: theory
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- latent_reasoning
- mathematical_and_formal_reasoning
- model_architecture
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- search_and_tree_reasoning
- test_time_compute_scaling
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0029220645775369677
staleness: 0.0
status: active
tags: []
---
# System 1 / System 2 Reasoning

**Type:** theory
**Themes:** [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Daniel Kahneman's cognitive science framework distinguishing fast, automatic, intuitive processing (System 1) from slow, deliberate, analytical reasoning (System 2). Applied to LLMs: standard autoregressive generation is System 1; iterative latent refinement approaches System 2.

## Key Findings

1. Embodied reasoning is applicable across multiple agent types including humans, animals, robot arms, humanoid robots, and autonomous vehicles. (from "2025-3-18")
2. The physical common sense benchmark contains 604 questions from 426 videos, with 49.33% about Time, 37.4% about Fundamental Physics, and 13.25% about Space. (from "2025-3-18")
3. Cosmos-Reason1 uses InternViT-300M-V2.5 as the vision encoder, generating 1,024 visual tokens per frame which are downsampled to 256 tokens using PixelShuffle. (from "2025-3-18")
4. Building reasoning models for Physical AI is an open problem that is far from being solved. (from "2025-3-18")
5. Cosmos-Reason1 uses a decoder-only multimodal LLM architecture with a hybrid Mamba-MLP-Transformer backbone for efficient long-sequence processing. (from "2025-3-18")
6. The Cosmos-Reason1 paper leaves the 'Learn from Interactions' embodied reasoning capability as future work, focusing only on the first three capabilities. (from "2025-3-18")
7. Embodied reasoning is organized in a two-dimensional ontology encompassing four key reasoning capabilities across five types of embodied agents. (from "2025-3-18")
8. Physical common sense is organized into a hierarchical ontology with three major categories — Space, Time, and Fundamental Physics — divided into 16 fine-grained subcategories. (from "2025-3-18")
9. Cosmos-Reason1 is trained in four stages: vision pre-training, general SFT, Physical AI SFT, and Physical AI reinforcement learning. (from "2025-3-18")
10. Vision pre-training dataset consists of 130M samples including both human-annotated data and model-generated captions. (from "2025-3-18")
11. The general SFT dataset consists of 6M image-text samples and 2M video-text samples. (from "2025-3-18")
12. Cosmos-Reason1 models understand the physical world and generate embodied decisions in natural language through long chain-of-thought reasoning processes. (from "2025-3-18")
13. During vision pre-training, the LLM backbone and vision encoder are kept frozen while only the two-layer MLP projector is trained. (from "2025-3-18")
14. Cosmos-Reason1 processes video input by uniformly sampling up to 32 frames at a maximum rate of 2 frames per second, resizing each frame to 448×448 pixels. (from "2025-3-18")
15. Cosmos-Reason1-8B is trained with Tensor Parallelism of 4, while Cosmos-Reason1-56B uses Tensor Parallelism of 8 and Pipeline Parallelism of 2 to support longer video training. (from "2025-3-18")

## Relationships

## Limitations and Open Questions

## Sources
