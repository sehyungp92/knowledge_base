---
type: entity
title: LIBERO
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- generative_media
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- spatial_and_3d_intelligence
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0005759590982245998
staleness: 0.0
status: active
tags: []
---
# LIBERO

> LIBERO is a challenging robotic manipulation benchmark suite comprising four sub-benchmarks — Spatial, Object, Goal, and 10 — designed to stress-test robot learning policies on complex multi-object manipulation tasks with extended action horizons. It has become a standard evaluation harness for vision-language-action models, most notably serving as a testbed for pi0 policy learning with synthetic data generation.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/generative_media|Generative Media]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]], [[themes/robot_learning|Robot Learning]], [[themes/spatial_and_3d_intelligence|Spatial and 3D Intelligence]], [[themes/video_and_world_models|Video and World Models]], [[themes/vision_language_action_models|Vision-Language-Action Models]]

## Overview

LIBERO structures robot manipulation evaluation along four distinct axes. **LIBERO-Spatial** tests whether a policy can resolve spatial relationships between objects (e.g., left of, inside, on top of). **LIBERO-Object** probes generalisation to novel object instances within familiar task structures. **LIBERO-Goal** varies the target goal state while holding the scene fixed, requiring goal-conditioned reasoning. **LIBERO-10** is a harder aggregate of ten long-horizon tasks that demand sequential subtask completion — the most demanding of the four.

This decomposition makes LIBERO particularly useful for diagnosing *where* a policy fails rather than just *whether* it fails: a model that collapses on LIBERO-Spatial but handles LIBERO-Object reveals a specific spatial grounding deficit rather than a general manipulation failure. Extended action horizons in LIBERO-10 additionally expose compounding error accumulation, a known weakness of imitation-learned policies.

LIBERO has been used to evaluate pi0 policy learning under synthetic data regimes, probing how well data generated without real robot demonstrations transfers to complex manipulation. This positions LIBERO at the intersection of [[themes/robot_learning|robot learning]] and [[themes/generative_media|generative media]] — synthetic data quality directly determines LIBERO scores.

## Key Findings (claims mentioning this entity)

The claims surfaced from 2025-3-18 cluster around the broader embodied reasoning context in which LIBERO sits, rather than LIBERO-specific ablations. Taken together they sketch the landscape:

**Embodied reasoning is a multi-agent, multi-capability problem.** The field frames embodied intelligence across humans, animals, robot arms, humanoids, and autonomous vehicles simultaneously, with a two-dimensional ontology covering four reasoning capabilities across five agent types. LIBERO, as a robot-arm manipulation suite, sits at one node of this taxonomy — useful precisely because it isolates manipulation from locomotion and navigation concerns.

**Physical common sense is a recognised gap.** The benchmarks emerging alongside LIBERO (e.g., the 604-question physical common sense suite covering Space, Time, and Fundamental Physics) reflect a shared diagnosis: that current models lack grounded physical understanding. LIBERO's spatial and goal sub-benchmarks are a concrete instantiation of this gap in the manipulation domain.

**Reasoning model development for Physical AI remains unsolved.** Work like Cosmos-Reason1 — which pairs a hybrid Mamba-MLP-Transformer backbone with four training stages (vision pre-training on 130M samples, general SFT on 8M samples, Physical AI SFT, and Physical AI RL) — treats LIBERO-style benchmarks as downstream validation targets. The explicit acknowledgement that "building reasoning models for Physical AI is an open problem that is far from being solved" contextualises LIBERO scores: current state-of-the-art is not saturating these benchmarks, and improvement trajectories remain steep.

**Synthetic data and chain-of-thought are active levers.** Cosmos-Reason1's use of long chain-of-thought reasoning to generate "embodied decisions in natural language" and its reliance on model-generated captions in pre-training signal that the field is betting on synthetic supervision — exactly the regime under which pi0's LIBERO evaluations are conducted. Whether synthetic data generalises across the four LIBERO sub-benchmarks at equal rates is an open empirical question.

## Relationships

LIBERO is most directly connected to [[themes/vision_language_action_models|vision-language-action models]] as a benchmark for evaluating policies that must jointly interpret language goals and visual scenes. Its four-way decomposition makes it a reference point in [[themes/spatial_and_3d_intelligence|spatial and 3D intelligence]] discussions — particularly the Spatial sub-benchmark.

The synthetic data angle links it to [[themes/generative_media|generative media]] and [[themes/finetuning_and_distillation|finetuning and distillation]] research: if world models like RoboScape or AdaWorld can generate high-fidelity manipulation rollouts, LIBERO is the natural evaluation surface for that claim. The extended horizon of LIBERO-10 additionally makes it relevant to [[themes/reasoning_and_planning|reasoning and planning]] — sequential task completion requires more than reactive control.

The "learn from interactions" capability noted as future work in Cosmos-Reason1 is precisely what LIBERO-10's long-horizon structure would stress — closing that loop remains an open direction where LIBERO could serve as a longitudinal benchmark for online RL approaches in [[themes/reinforcement_learning|reinforcement learning]] and [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

## Limitations and Open Questions

## Sources
