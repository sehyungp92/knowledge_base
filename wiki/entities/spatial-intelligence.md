---
type: entity
title: Spatial Intelligence
entity_type: theory
theme_ids:
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- frontier_lab_competition
- generative_media
- multimodal_models
- pretraining_and_scaling
- robotics_and_embodied_ai
- scaling_laws
- spatial_and_3d_intelligence
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0003682791534206476
staleness: 0.0
status: active
tags: []
---
# Spatial Intelligence

> Spatial intelligence is the capacity of AI systems to perceive, reason about, and act within physical and virtual spaces — encompassing distance estimation, object orientation, physics prediction, navigation, and the grounding of language and action in geometric reality. It has emerged as a defining frontier beyond language modeling, with advocates like Fei-Fei Li arguing it is the missing layer between disembodied reasoning and agents that can operate in the real world.

**Type:** theory
**Themes:** [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/generative_media|Generative Media]], [[themes/multimodal_models|Multimodal Models]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]], [[themes/scaling_laws|Scaling Laws]], [[themes/spatial_and_3d_intelligence|Spatial and 3D Intelligence]], [[themes/unified_multimodal_models|Unified Multimodal Models]], [[themes/video_and_world_models|Video and World Models]], [[themes/vision_language_action_models|Vision-Language-Action Models]]

---

## Overview

Spatial intelligence describes what an agent must do to be genuinely embedded in a world rather than merely a processor of text about one. It covers the full loop from perception (interpreting raw visual signals as geometry and physics) through reasoning (inferring distances, orientations, affordances, consequences of actions) to grounded action (moving through, manipulating, and navigating space). Researchers at World Labs and elsewhere have framed this as the natural successor to large language models: where LLMs learned to reason symbolically over language, spatial AI systems must learn to reason structurally over three-dimensional reality.

The practical test case for this capability is embodied agents operating in complex 3D environments, where every decision requires integrating visual context, physical prediction, and goal-directed planning simultaneously.

---

## Key Findings

### SIMA 2 as a Proof of Concept

The clearest concrete evidence for the current state of spatial intelligence comes from SIMA 2: A Generalist Embodied Agent for Virtual Worlds, which represents Google DeepMind's attempt to build a generalist agent capable of operating across diverse 3D game worlds using only the same interface a human would use: RGB video at 720p and keyboard-and-mouse actions. No privileged environment information is provided. The action space covers 96 standard keyboard keys, mouse clicks, and discretized relative mouse movements, all generated as structured text output rather than discrete tokens, reflecting the challenge of mapping language-model architectures onto fine-grained spatial control.

SIMA 2 is built on a Gemini Flash-Lite foundation model and trained through supervised finetuning on a mixture of gameplay and non-gameplay Gemini pretraining data. That mixture turns out to be critical: dropping non-gameplay data degrades vision understanding, dialogue, and general reasoning, which suggests that spatial grounding and general cognitive capability are not yet separable. You cannot specialize into spatial competence without preserving the broader representational substrate.

### The Gap SIMA 1 Revealed

SIMA 1 illustrated the hard floor beneath spatial intelligence. It was trained with language encoding from scratch (despite using pretrained vision encoders), which constrained its instruction-following to the vocabulary of annotated gameplay it had seen. It could process only text instructions and current images, producing only keyboard-and-mouse outputs: no reasoning trace, no dialogue, no multimodal prompts. The practical consequence was brittleness: SIMA 1 handled short, direct instructions but failed to generalize to novel phrasing or indirect goals, and could not explain or modify its own behavior.

SIMA 2 addresses this structurally. By building on a pretrained multimodal foundation, it inherits general reasoning and gains the ability to generate internal reasoning that modifies its own behavior before producing actions. This enables it to handle nuanced, indirect, or compositional instructions not seen in training data, and to engage in dialogue with users while acting.

### Bridge Data and the Annotation Gap

A significant bottleneck in training spatial agents is that human gameplay does not contain explicit reasoning or dialogue: annotators act but do not narrate. SIMA 2 resolves this through "bridge data," synthetically generated by Gemini Pro to annotate human gameplay with causally consistent internal reasoning and dialogue. This makes it possible to train agents that simultaneously act, reason, and communicate, but it also means training depends on the quality of synthetic annotation rather than ground-truth human reasoning traces. The fidelity of that synthetic signal is an open question.

### Reinforcement Learning and Generalization Limits

After supervised learning, SIMA 2 is trained with reinforcement learning from verifiable rewards. Tasks are defined as tuples of initial game state, text instruction, and verifiable reward signal. Critically, RL training is explicitly restricted to training environments and excludes held-out environments such as ASKA and MineDojo. This boundary between what the RL signal can shape and what must transfer zero-shot is a persistent limitation: the agent's capacity to generalize across environments comes from the foundation model and supervised pretraining, not from reward-driven adaptation in novel settings.

Despite this, SIMA 2 demonstrates generalization to previously unseen environments, including photorealistic worlds generated on-the-fly by Genie 3, substantially closing the gap with human performance across a diverse portfolio of games. Whether this extends to the physical world (with its richer physics, continuous action spaces, and real-world perceptual noise) remains the central open question.

### Self-Improvement as a Path Forward

SIMA 2 demonstrates a capacity for open-ended self-improvement by using Gemini to generate tasks and provide reward signals autonomously, allowing the agent to acquire new skills from scratch in new environments. The architecture uses three foundation models in concert: a task setter, the agent itself, and a reward model, alongside a general world model. This three-model loop enables autonomous skill acquisition without human-specified reward functions.

This is significant because it suggests that spatial intelligence may bootstrap itself over time, with the agent generating its own curriculum. However, the quality of the emergent skills depends entirely on what the task-setter and reward model value, and whether these models can reliably judge spatial competence in novel contexts is unverified.

---

## Limitations and Open Questions

The current state of spatial intelligence carries several structural limitations:

**Generalization from virtual to physical.** SIMA 2's gains are in 3D game environments with physics engines and discrete rendering pipelines. Transfer to physical robotics involves continuous action spaces, sensor noise, and real-world physics variability that game environments do not faithfully represent.

**RL confinement to training domains.** The agent's RL-trained skills apply only to training environments. Held-out settings rely on zero-shot generalization from pretraining, which has limits that remain poorly characterized.

**Dependency on synthetic annotations.** Bridge data resolves the annotation gap but introduces dependency on synthetic reasoning quality. If Gemini Pro's annotations contain systematic biases in how it narrates spatial reasoning, those biases propagate into the agent.

**Capability-generality tradeoff.** Finetuning on gameplay data degrades base model capabilities unless non-gameplay data is mixed in, suggesting that spatial and general reasoning are not yet cleanly composable. Future architectures may need to treat spatial competence as an additive module rather than a fine-tuning target.

**What "spatial intelligence" means for language-grounded tasks.** The World Labs framing (Fei-Fei Li, Justin Johnson) positions spatial intelligence as foundational for AI's next frontier, but the path from embodied game-playing to general spatial reasoning across modalities (3D reconstruction, physical manipulation, robot navigation) is not yet clear. The claim is compelling as a research agenda; the execution is early-stage.

---

## Relationships

Spatial intelligence intersects most directly with [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]], where the grounding problem is most concrete, and with [[themes/video_and_world_models|Video and World Models]], since predicting future visual states requires implicit geometric reasoning. The self-improvement loop in SIMA 2 connects to [[themes/agent_self_evolution|Agent Self-Evolution]], while the use of a foundation model base ties to [[themes/pretraining_and_scaling|Pretraining and Scaling]] dynamics. The competitive framing from Fei-Fei Li's World Labs situates it within [[themes/frontier_lab_competition|Frontier Lab Competition]] as a post-LLM differentiator.

Key sources: From Words to Worlds: Spatial Intelligence is AI's Next Frontier, SIMA 2: A Generalist Embodied Agent for Virtual Worlds, After LLMs: Spatial Intelligence and World Models (Fei-Fei Li & Justin Johnson), "The Future of AI is Here" — Fei-Fei Li.

## Sources
