---
type: entity
title: sim-to-real gap
entity_type: theory
theme_ids:
- finetuning_and_distillation
- generative_media
- post_training_methods
- robotics_and_embodied_ai
- robot_learning
- spatial_and_3d_intelligence
- synthetic_data_generation
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00035668756341262337
staleness: 0.0
status: active
tags: []
---
# sim-to-real gap

> The sim-to-real gap describes the systematic performance degradation that occurs when policies or models trained in simulation are deployed on physical hardware, arising from mismatches in physics fidelity, visual appearance, sensor characteristics, and contact dynamics. It remains one of the central bottlenecks in robotics and embodied AI, simultaneously motivating advances in simulation realism, domain randomization, and data-efficient transfer — and increasingly serving as a forcing function for world model research that aims to replace handcrafted simulators altogether.

**Type:** theory
**Themes:** [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/generative_media|Generative Media]], [[themes/post_training_methods|Post-Training Methods]], [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]], [[themes/robot_learning|Robot Learning]], [[themes/spatial_and_3d_intelligence|Spatial & 3D Intelligence]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/video_and_world_models|Video & World Models]], [[themes/vision_language_action_models|Vision-Language-Action Models]]

## Overview

The sim-to-real gap is not a single failure mode but a family of transfer problems: calibration imperfections cause predicted contact forces to diverge from physical reality; sensor noise distributions in simulation rarely match those of actual cameras or depth sensors; and visual textures, lighting, and object geometry are imperfect approximations at best. Even state-of-the-art physics engines like MuJoCo produce conditions sufficiently distant from the real world that policies trained exclusively on simulated trajectories exhibit measurable performance drops when transferred — a degradation classified as both **blocking** in severity for many tasks and largely **stable** in trajectory, meaning the problem persists despite considerable effort.

The dominant contemporary response is not to close the gap by making simulations more realistic, but to make policies robust to it — through domain randomization, procedural scene generation, and distillation pipelines that leverage simulation for privileged training signals before transferring to vision-only student policies. A second and more speculative response is to replace engineered simulators with learned world models that can generate training environments directly from data.

## Key Findings

### Procedural Generation as a Bridge

The Proc4Gem work offers one of the clearest illustrations of a modern sim-to-real pipeline. The approach uses a hierarchical procedural generation system to sample diverse indoor scenes — living-room configurations built from a VLM-captioned asset dataset — generating variation in object placement, target identity, and scene layout at scale. This diversity is the mechanism by which the gap is addressed: rather than closing it, the system makes the policy's prior broad enough that real-world conditions fall within its training distribution.

The training pipeline itself is layered. A privileged RL expert is first trained using full state information — positions, object identities — achieving 68.9% success across procedurally-generated simulated scenes and 85.4% in a fixed simulation scene. This expert is then distilled into a student policy that operates only on RGB images and language instructions, the interface available at deployment. Gemini is fine-tuned on the resulting trajectory data using behavioral cloning with next-token prediction loss, inheriting the expert's coverage without requiring access to state information at test time.

The real-world results expose where the gap remains and where it has been meaningfully narrowed. When tested with 3D-scanned real assets, the Gemini-based agent achieves 70.0% success on the fixed simulation scene versus the SPOC baseline's 62.1% — a notable margin, but still substantially below the privileged expert's ceiling. The gap is most visible on out-of-distribution targets: a toy giraffe plushie produced a 0% success rate for the SPOC baseline while Gemini achieved 70%, suggesting that the foundation model's pretrained visual representations provide genuine robustness that narrower baselines lack. Gemini is also used upstream to generate five natural language descriptions per asset at increasing specificity, enriching the diversity of language commands the agent must learn to follow.

### World Models as Learned Simulators

A structurally different response to the sim-to-real gap is to abandon handcrafted simulators in favour of learned environment models. Genie 3 represents this direction: architected explicitly as an environment model rather than an agent, it generates interactive worlds from text prompts in real time, with the intent that agents train inside these generated environments rather than in scripted simulations. The distinction matters — Genie 3 does not plan or act, it simulates experiences for agents to learn from.

The practical implications for the sim-to-real gap are significant in principle but not yet demonstrated at scale. Genie 3 maintains persistent spatial memory — world state is preserved when an agent looks away and returns — moving toward the consistency properties that physical simulation provides automatically but that generative models have historically struggled to maintain. Earlier versions (Genie 2) already lacked this property; Genie 3 achieves it for durations exceeding one minute. However, the current design is constrained to approximately one minute of persistent memory due to real-time generation trade-offs, and the three objectives of minute-plus memory, real-time generation, and higher resolution present conflicting technical demands within a single model. Genie 3 remains a research preview with no public release timeline, meaning its contribution to closing the sim-to-real gap is currently theoretical.

The generational shift from image-prompted (Genie 1, Genie 2) to text-prompted (Genie 3) generation also matters here: a text-driven environment model is far more composable with the kinds of procedural generation pipelines used in approaches like Proc4Gem, where language descriptions of assets and scenes are already the interface.

## Known Limitations

The sim-to-real gap itself is a limitation — and it stratifies by severity. For manipulation tasks with well-understood contact models, the gap is **significant** but not blocking; calibrated pipelines like Proc4Gem can achieve competitive real-world performance. For tasks requiring precise contact dynamics, deformable objects, or sensor modalities (e.g., tactile) that are poorly modelled in simulation, the gap remains **blocking**. Real-world performance is consistently lower than simulation for all evaluated tasks in Proc4Gem, with calibration imperfections and sensor noise cited as persistent contributors.

The world-model route introduces its own limitations. Learned simulators like Genie 3 cannot yet provide the physical accuracy that model-free RL requires for contact-rich tasks; they are better suited to training perception and navigation policies than manipulation policies that depend on precise force feedback. The one-minute memory ceiling also constrains the kinds of long-horizon tasks for which such environments could serve as training grounds.

Open questions cluster around three axes: whether procedural diversity can substitute for physical fidelity at scale, whether learned world models will ever match engineered simulators on contact dynamics, and whether real-world data augmentation (3D scanning, teleoperation) can eventually make simulation a secondary rather than primary data source.

## Relationships

The sim-to-real gap sits at the intersection of several adjacent concepts. It is the primary motivation for **domain randomization** and **procedural scene generation** as training strategies. It connects to [[themes/synthetic_data_generation|synthetic data generation]] through the use of simulation as a scalable data source and to [[themes/finetuning_and_distillation|finetuning and distillation]] through the expert-to-student transfer that makes simulated trajectories usable by vision-only policies. The world-model route links it to [[themes/video_and_world_models|video and world models]], where Genie 3's architecture as a learned environment model represents a bet that generative simulation can eventually supplant physics engines. The gap also shapes [[themes/vision_language_action_models|vision-language-action models]] like the Gemini-based agent in Proc4Gem, where pretrained visual and language representations provide a form of implicit robustness to distribution shift that narrower task-specific models lack.

Key sources: Proc4Gem: Foundation models for physical agency through procedural generation, Google DeepMind Lead Researchers on Genie 3 & the Future of World-Building, Self-Driving Expert Unpacks the Biggest Breakthroughs and Bottlenecks

## Limitations and Open Questions

## Sources
