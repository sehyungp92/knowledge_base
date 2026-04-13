---
type: entity
title: Flow Matching
entity_type: method
theme_ids:
- audio_and_speech_models
- creative_content_generation
- finetuning_and_distillation
- generative_media
- image_generation_models
- latent_reasoning
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 9
sources_since_update: 0
update_count: 1
influence_score: 0.008036997695259998
staleness: 0.0
status: active
tags: []
---
# Flow Matching

**Type:** method
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/creative_content_generation|creative_content_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A generative modeling paradigm (Lipman et al., 2022) that formulates noise-to-data mappings through ODEs, requiring iterative multi-step inference. Represents the primary competing paradigm that Drifting Models aim to replace for single-step generation.

## Key Findings

1. The drifting model cannot be made to work on ImageNet without a feature encoder; raw pixel/latent kernel similarity is insufficient for effective training. (from "Generative Modeling via Drifting")
2. Classifier-free guidance in Drifting Models is a training-time behavior implemented by mixing negative samples from different class distributions, preserving 1-NFE inference. (from "Generative Modeling via Drifting")
3. Drifting Models shift the iterative pushforward evolution from inference time to training time, enabling native single-step generation without SDE/ODE formulations. (from "Generative Modeling via Drifting")
4. The drifting field is designed as an attraction-repulsion mechanism: generated samples are attracted toward the data distribution and repelled from the current generated distribution. (from "Generative Modeling via Drifting")
5. The drifting loss objective is equivalent to minimizing the squared norm of the drifting field, with a stop-gradient formulation used to avoid direct back-propagation through the generated distributio (from "Generative Modeling via Drifting")
6. The best-performing Drifting Model uses a CFG scale of 1.0, which corresponds to no guidance in diffusion-based terminology. (from "Generative Modeling via Drifting")
7. Drifting Models achieve a new state-of-the-art 1-NFE FID of 1.54 on ImageNet 256x256 in latent space among single-step methods. (from "Generative Modeling via Drifting")
8. Drifting Models achieve 1.61 FID on ImageNet 256x256 in pixel space with a single function evaluation, outperforming or competing with previous multi-step pixel-space methods. (from "Generative Modeling via Drifting")
9. Anti-symmetry of the drifting field is a necessary condition for achieving equilibrium; breaking it causes catastrophic failure in generation quality. (from "Generative Modeling via Drifting")
10. A drifting field with anti-symmetry property guarantees that when the generated distribution q matches the data distribution p, all drift becomes zero, achieving equilibrium. (from "Generative Modeling via Drifting")
11. Larger positive and negative sample sets improve generation quality under fixed training compute budgets, analogous to findings in contrastive representation learning. (from "Generative Modeling via Drifting")
12. The Drifting Model's Base-size (133M parameter) variant is competitive with previous XL-size single-step models trained from scratch. (from "Generative Modeling via Drifting")
13. Toy experiments demonstrate that Drifting Models can recover bimodal distributions without mode collapse from multiple initializations, including collapsed single-mode initializations. (from "Generative Modeling via Drifting")
14. Previous single-step diffusion and flow models achieve single-step generation by distilling or approximating multi-step SDE/ODE trajectories, whereas Drifting Models do not rely on this approach. (from "Generative Modeling via Drifting")
15. Drifting Models achieve 1.61 FID in pixel space using only 87G FLOPs, compared to StyleGAN-XL which produces 2.30 FID using 1574G FLOPs. (from "Generative Modeling via Drifting")

## Relationships

## Limitations and Open Questions

## Sources
