---
type: entity
title: domain randomization
entity_type: method
theme_ids:
- finetuning_and_distillation
- post_training_methods
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
- synthetic_data_generation
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012141410612675203
staleness: 0.0
status: active
tags: []
---
# domain randomization

Domain randomization is a sim-to-real transfer technique that randomizes simulation parameters — physics properties, visual textures, object configurations — across training episodes, forcing policies to learn robust behaviors that generalize across a distribution of environments rather than overfitting to any single simulated setting. It has become a foundational component in robot learning pipelines, particularly as the field increasingly relies on simulation data to compensate for the scarcity of real-world action-labeled training data.

**Type:** method
**Themes:** [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/post_training_methods|post_training_methods]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Domain randomization addresses a fundamental tension in robot learning: simulation data is cheap and safe to generate at scale, but it inevitably diverges from reality in physics fidelity and visual rendering. As Jim Fan articulates, no graphics pipeline eliminates the sim-to-real gap entirely — physics will always differ, and visual rendering will never perfectly match the real world. At the same time, internet-scale data lacks the motor control signals needed to train robot foundation models directly, making simulation with domain randomization one of the few viable paths to large-scale action-labeled training data.

## Key Findings

The most significant recent development in domain randomization is its automation via language models. DrEureka demonstrates that GPT-4 can automatically construct both reward functions and domain randomization distributions given only a physics simulation of the target task — removing the need for human experts to manually tune randomization parameters. The results are striking: DrEureka-trained policies outperform human-designed configurations on quadruped locomotion by 34% in forward velocity and 20% in distance traveled, and on dexterous manipulation achieve nearly 300% more in-hand cube rotations than the human-developed baseline. DrEureka operates by sampling 16 domain randomization configurations and evaluating all resulting policies in the real world in parallel, using reward feedback to iterate — a design that treats DR parameter search as an outer optimization loop guided by LLM priors.

This builds on the broader Eureka paradigm described by Jim Fan, where LLMs generate reward functions as code against a simulator API, replacing manual reward engineering. The key insight is that LLMs encode substantial implicit knowledge about physics, plausible parameter ranges, and task structure — enough to bootstrap domain randomization configurations that would previously require significant human expert time.

Proc4Gem takes a complementary approach: rather than randomizing low-level physics parameters, it uses hierarchical procedural generation to randomize the scene itself — sampling realistic indoor environments from a VLM-captioned asset dataset. Gemini is then fine-tuned on trajectory data collected in these procedurally generated scenes via behavioral cloning. The approach shows strong out-of-distribution generalization: on a highly out-of-distribution target (toy giraffe), the SPOC baseline achieves 0% success while Gemini achieves 70%, suggesting that scene-level diversity during training transfers more robustly than policies trained on fixed simulation environments.

The Proc4Gem training pipeline also reveals how domain randomization interacts with privileged-information distillation. A privileged RL expert — trained with access to full state information across randomized scenes — achieves 68.9% success in procedurally-generated scenes and 85.4% in fixed scenes. This expert is then distilled into a student policy that operates only on RGB images and language commands, with Gemini generating five natural language descriptions per asset at varying levels of detail. The distillation step is where domain randomization pays off most clearly: exposure to diverse simulated conditions during RL training forces the privileged expert to learn genuinely generalizable behaviors, which then transfer through distillation to the vision-language student.

## Limitations and Open Questions

The sim-to-real gap remains a fundamental limitation even with aggressive domain randomization. Randomizing simulation parameters broadens the distribution the policy sees, but cannot guarantee the real world falls within that distribution — particularly for contact-rich manipulation where small differences in friction, object compliance, or sensor noise can cascade into policy failure. The Proc4Gem results are encouraging but the evaluation is limited to structured pick-and-place in living-room scenes; it remains unclear how far scene-level procedural randomization scales to tasks requiring finer motor control.

DrEureka's approach of evaluating all 16 DR configurations in the real world in parallel is effective but expensive — it externalizes the evaluation cost to physical hardware. Automating the inner loop of DR search without real-world rollouts remains an open problem.

A deeper question is whether domain randomization is a transitional technique or a permanent component of the stack. If simulation fidelity improves to the point where the sim-to-real gap is negligible (the "digital twin" regime), randomization becomes less necessary. Conversely, if world models trained on video can generate action-conditioned simulation data, the need for physics-based simulation may itself diminish. The value of domain randomization is tightly coupled to the long-term role of physics simulation in robot training — a question that remains unresolved.

## Relationships

Domain randomization is closely coupled with sim to real transfer as its primary application context, and with reward modeling through the Eureka/DrEureka line of work that co-optimizes reward functions and DR distributions. It intersects with synthetic data generation at the scene-level procedural generation approach in Proc4Gem, and with behavioral cloning and knowledge distillation in pipelines that use DR-trained RL experts as teachers. The broader motivation — compensating for the absence of internet-scale action data — connects it to debates around robot foundation models and the role of simulation versus real-world data collection.

**Sources:** DrEureka: Language Model Guided Sim-To-Real Transfer, Proc4Gem: Foundation models for physical agency through procedural generation, Jim Fan on Nvidia's Embodied AI Lab and Jensen Huang's Prediction that All Robots will be Autonomous

## Sources
