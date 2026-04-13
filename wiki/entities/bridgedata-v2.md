---
type: entity
title: BridgeData V2
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- generative_media
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- synthetic_data_generation
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0019266793965706042
staleness: 0.0
status: active
tags: []
---
# BridgeData V2

BridgeData V2 is a large-scale robotic manipulation dataset collected across diverse real-world environments, designed to support generalizable robot learning. It is one of the foundational datasets in the Open X-Embodiment collection and has been adopted as a benchmark domain in TokenBench for evaluating video tokenizer performance on physical manipulation scenarios — making it a reference point at the intersection of robot learning and generative world modeling for Physical AI.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

BridgeData V2 sits within the broader ecosystem of robot manipulation datasets that power generalist robot policies. It forms part of the Open X-Embodiment corpus — the training foundation for models like OpenVLA — which aggregates 970k real-world demonstrations across diverse embodiments and tasks. The dataset's inclusion in TokenBench signals its dual role: not only as training data for policy learning, but as a challenging evaluation domain for video tokenizers tasked with compressing manipulation-relevant visual dynamics for world models in Physical AI pipelines such as Cosmos.

The significance of BridgeData V2 stems partly from what it represents structurally: even the largest robot manipulation datasets, including collections that subsume BridgeData V2, cap out at roughly 100K–1M examples. This is orders of magnitude below Internet-scale vision-language pretraining corpora, creating a persistent data imbalance that constrains how much VLA models can rely on robot-specific supervision versus transferred visuolinguistic representations.

## Role in Training Generalist Policies

Within the Open X-Embodiment mixture used to train OpenVLA, datasets like BridgeData V2 were subject to heuristic reweighting inherited from Octo: less diverse datasets were down-weighted, while datasets with broader task and scene coverage were up-weighted. This mixing strategy acknowledges a tension in robot learning — raw volume matters less than diversity, and BridgeData V2's multi-environment coverage made it a relatively high-value contributor to the mixture.

The OpenVLA results demonstrate what is possible when such datasets are combined with a strong VLM backbone. Fine-tuned on this corpus, OpenVLA outperformed RT-2-X (55B parameters) by 16.5% in absolute task success rate across 29 tasks while using 7× fewer parameters, and exceeded Diffusion Policy by 20.4% on multi-task environments involving multiple objects and language grounding. These gains trace partly to architectural choices — the fused SigLIP-DinoV2 visual encoder, full vision encoder fine-tuning during VLA training, and action discretization into 256 bins using quantile-based bounds — but the quality and diversity of the underlying data is a prerequisite.

## Role in Video Tokenizer Evaluation

BridgeData V2's inclusion in TokenBench reflects a second trajectory: as robot manipulation becomes a target domain for world models, the field needs tokenizers that preserve the fine-grained spatial and temporal structure of manipulation video — contact dynamics, gripper state, object pose — rather than treating it like generic natural video. This is non-trivial. Tokenizers optimized for cinematic or synthetic data may smooth over precisely the low-level cues that matter for policy conditioning or planning in physical systems.

## Limitations and Open Questions

The dataset's coverage, while broad by robotics standards, remains narrow relative to the combinatorial space of real-world manipulation. Existing learned policies trained on data of this kind — including those using BridgeData V2 — still lack robustness to scene distractors, novel objects, and unseen task instructions. The closed-dataset problem also lingers: much of the highest-quality robot data remains proprietary, limiting the ability of open datasets like BridgeData V2 to close the gap with commercial systems.

A deeper open question is whether scaling manipulation datasets along existing axes (more demonstrations, more environments, same embodiment distribution) will yield the generalization improvements needed for Physical AI, or whether structural changes — synthetic augmentation, simulation-to-real transfer, or world-model-generated rollouts — are necessary to break through the current ceiling. BridgeData V2's simultaneous presence in training pipelines and tokenizer benchmarks positions it as a useful probe for tracking progress on both fronts.

## Relationships

BridgeData V2 is embedded in the [[themes/robotics_and_embodied_ai|robotics and embodied AI]] landscape through its role in the Open X-Embodiment corpus and its relationship to [[themes/vision_language_action_models|vision-language-action models]] like OpenVLA. Its use in TokenBench connects it to [[themes/video_and_world_models|video and world models]], particularly the Cosmos platform's effort to build Physical AI-ready tokenizers. The data scarcity it exemplifies is a live bottleneck linking [[themes/pretraining_and_scaling|pretraining and scaling]] concerns to [[themes/synthetic_data_generation|synthetic data generation]] as a potential relief valve.

## Key Findings

## Sources
