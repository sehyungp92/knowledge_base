---
type: entity
title: RT2
entity_type: method
theme_ids:
- finetuning_and_distillation
- in_context_and_meta_learning
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0004057810224892767
staleness: 0.0
status: active
tags: []
---
# RT2

> Robotics Transformer 2 (RT2) is a model developed at Google that connects pre-trained vision-language models to robotics data, establishing that internet-scale pretraining can provide the semantic grounding robots need to generalize to novel manipulation tasks. Its significance lies in demonstrating a viable path away from hand-coded primitive libraries and toward foundation models that transfer web knowledge directly into embodied action.

**Type:** method
**Themes:** [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

RT2 emerged from a simple but consequential observation: the dominant approach to robotics (manually writing code to explain what a robot sees and control its limbs task-by-task, accumulating a library of hardcoded primitives) had hit a ceiling. The bottleneck was never hardware. Teleoperation proved that hardware had been physically capable for years; what was missing was the intelligence to generalize. RT2's core contribution was showing that a VLM pre-trained on internet data already contains the semantic understanding needed to recognize and reason about objects, and that combining this with even a small corpus of robotics data allows a robot to generalize to objects it has never directly encountered in training.

The approach is now treated as a foundational reference point for the [[themes/vision_language_action_models|vision-language-action model]] paradigm: use web-scale pretraining to build broad world knowledge, then bridge into the action space through targeted robotics fine-tuning.

## Key Findings

### The VLM-to-Robotics Transfer Insight

The central finding RT2 demonstrated was that internet-scale pretraining and robotic manipulation are not separate problems. A VLM's web-derived understanding of objects, scenes, and language can transfer into robotic generalization. This shifted the framing from "how do we build a robot that knows about objects" to "how do we connect a model that already knows about objects to the robot's action space."

### The Fine-Tuning Tension and Knowledge Insulation

The approach is not without a critical failure mode. Fine-tuning a VLM solely on robotics data causes the model to lose the generalization capabilities it was trained to have, degrading both as a vision-language model and in training dynamics. This tension is central to making the paradigm work in practice.

The response developed at Physical Intelligence (where many RT2-era researchers continued this line of work) is a technique called knowledge insulation: continuing to co-train on non-robotics web data alongside robotics data during fine-tuning. The goal is to preserve the VLM's broad capabilities while acquiring robotic control. This is a multifaceted approach, and its necessity highlights a fundamental challenge: the robotics data distribution is narrow relative to the pretraining distribution, and naive fine-tuning collapses the model toward that narrow distribution.

### From RT2 to Production-Scale Models

The trajectory from RT2 runs through subsequent models at Physical Intelligence, which raised over $400 million to pursue this direction. PI Zero, released within the first five to six months of the company's existence, demonstrated highly dexterous tasks including laundry folding, box building, and table busing across a wide range of robot embodiments. PI5 extended this to genuine out-of-distribution generalization: robots brought to entirely new homes they had never visited, performing long-horizon tasks such as cleaning a bedroom, making a bed, and putting dishes away.

The evaluation framework Physical Intelligence uses reflects the ambitions RT2 set in motion: progress is tracked along capability (tasks the model can perform at all), generalization (transfer to novel settings), and performance (reliability in deployment).

### Open Questions and Limitations

The most honest characterization of where this research stands is that current robotics foundation models are demo-ready but not deployment-ready. They still fail frequently. The gap between controlled demonstration and robust real-world deployment remains wide, and researchers are explicit that closing it requires further algorithmic work beyond what the VLM-to-robotics transfer paradigm has so far delivered.

The knowledge insulation problem also remains open in the sense that it is an active engineering challenge rather than a solved one. The right balance between web data and robotics data co-training, how that balance should shift across model scales, and whether the underlying tension can be resolved architecturally are all unresolved questions.

## Relationships

RT2 is most directly related to the [[themes/vision_language_action_models|VLA model]] family it helped establish, and to the broader [[themes/robotics_and_embodied_ai|robotics and embodied AI]] theme. Its method sits at the intersection of [[themes/finetuning_and_distillation|fine-tuning and distillation]] (specifically the knowledge insulation challenge) and [[themes/pretraining_and_scaling|pretraining and scaling]] (the claim that web-scale pretraining provides transferable grounding).

The work is documented across several sources: 2 Robotics Pioneers Unpack the Path to Generalist Robots, Robotics in the Age of Generative AI with Vincent Vanhoucke, and Robotics Research Update with Keerthana Gopalakrishnan and Ted Xiao.

## Limitations and Open Questions

## Sources
