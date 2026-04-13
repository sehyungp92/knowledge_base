---
type: entity
title: LIBERO Benchmark
entity_type: dataset
theme_ids:
- chain_of_thought
- generative_media
- multimodal_models
- reasoning_and_planning
- robotics_and_embodied_ai
- robot_learning
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00011254984436415276
staleness: 0.0
status: active
tags: []
---
# LIBERO Benchmark

> LIBERO is a simulation benchmark for robot manipulation that has become a standard evaluation suite for vision-language-action models. Comprising four task suites — LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long — each with 10 diverse tasks and 50 human-teleoperated demonstrations, it tests progressively harder competencies: spatial reasoning, object interaction, goal understanding, and long-horizon sequential manipulation. Its LIBERO-Long suite in particular has emerged as a key proving ground for world-model-augmented policy learning.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/generative_media|generative_media]], [[themes/multimodal_models|multimodal_models]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

LIBERO structures its evaluation across four suites that isolate distinct manipulation competencies. LIBERO-Spatial and LIBERO-Object probe lower-level perception and object handling; LIBERO-Goal tests instruction-following fidelity; and LIBERO-Long — the hardest suite — demands sustained coherence across extended action sequences. The 50 human-teleoperated demonstrations per task provide a modest but standardized supervision signal, making performance differences across models particularly diagnostic: gains here reflect genuine architectural or training improvements rather than data volume advantages.

The benchmark has become especially revealing as a testbed for long-horizon task completion, where the compounding of errors over time exposes weaknesses in models that perform well on shorter horizons.

## Key Findings

### LIBERO as a Differentiator for World-Model Approaches

The most striking result on LIBERO comes from UniVLA, which achieves a 95.5% average success rate across all four suites, surpassing π0-FAST's 85.5% by a substantial margin. The gains are not uniform: UniVLA's most significant improvement is on LIBERO-Long, where it reaches 94.0% against a prior state-of-the-art of 69.0% — a 25-point jump that the authors attribute directly to world model post-training. This is a meaningful signal. LIBERO-Long has historically been the hardest suite precisely because it requires maintaining task coherence over longer horizons, and it is here that the compounding benefit of learning from large-scale unannotated video — which UniVLA's two-stage training enables — is most apparent.

The core mechanism is that world model post-training requires no action annotations, allowing the model to absorb temporal dynamics and scene evolution from internet-scale video before ever seeing robot-specific supervision. This separates capability acquisition (what can happen in the world) from policy learning (what the robot should do), and LIBERO-Long results suggest this decomposition pays off most when tasks are structurally complex.

### Architectural Diversity Among Top Performers

LIBERO results also illuminate the architectural diversity of current top-performing VLA models. UniVLA adopts an encoder-free, fully autoregressive design — 8.5 billion parameters, identical architecture to Emu3, treating vision, language, and action as discrete token sequences in a shared vocabulary with no ViT backbone. WorldVLA, by contrast, initializes from Chameleon and uses a VQ-GAN image tokenizer (compression ratio 16, codebook size 8192) alongside an action tokenizer that discretizes each of 7 action dimensions into 256 bins. Both converge on discrete token representations as the unifying abstraction, but differ in how they handle image encoding and action conditioning.

WorldVLA's action attention masking strategy — which ensures each action is conditioned solely on textual and visual inputs, not on prior actions — is a design choice with direct implications for LIBERO evaluation: it prevents the model from learning spurious action-to-action shortcuts that could inflate performance on shorter tasks while degrading generalization.

### Benchmark Coverage and Blind Spots

LIBERO's simulation setting is both its strength and its limitation. The controlled environment makes results reproducible and comparable, but it abstracts away real-world distribution shift, sensor noise, and the physical contact dynamics that often determine real-robot success. High LIBERO scores — even at 95%+ — do not straightforwardly transfer to physical platforms, as results on SimplerEnv-WidowX (where UniVLA achieves 69.8%, up from SpatialVLA's 42.7%) show different rank orderings and lower absolute performance. LIBERO is better understood as a necessary but insufficient condition for real-world capability.

## Open Questions

The 25-point improvement on LIBERO-Long from world model post-training raises a natural question: how much of this gain is specific to the simulation distribution versus genuinely transferable temporal reasoning? UniVLA's authors acknowledge that their investigation into post-training scalability is still in early stages due to limited compute, leaving open whether further scaling of the video post-training phase would continue to improve long-horizon performance or plateau. The benchmark itself, with only 50 demonstrations per task, may also be approaching a ceiling where data quality and task diversity — rather than model capacity — become the binding constraint on further progress.

## Relationships

- Unified Vision-Language-Action Model — primary source of LIBERO benchmark results, including the 95.5% average and 94.0% on LIBERO-Long
- WorldVLA — evaluates on LIBERO using discrete token representations and action attention masking
- CoT-VLA — references LIBERO in the context of chain-of-thought reasoning for manipulation tasks
- [[themes/video_and_world_models|Video and World Models]] — world model post-training is the key mechanism behind LIBERO-Long improvements
- [[themes/vision_language_action_models|Vision-Language-Action Models]] — LIBERO is the central simulation benchmark for this theme
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]] — situates LIBERO within the broader challenge of transferring simulation competence to physical systems

## Limitations and Open Questions

## Sources
