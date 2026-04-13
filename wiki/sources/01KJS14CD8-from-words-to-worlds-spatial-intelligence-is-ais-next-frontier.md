---
type: source
title: 'From Words to Worlds: Spatial Intelligence is AI’s Next Frontier'
source_id: 01KJS14CD8CNXHESNTN3PENY1V
source_type: article
authors: []
published_at: '2025-11-10 00:00:00'
theme_ids:
- generative_media
- pretraining_and_scaling
- robotics_and_embodied_ai
- scaling_laws
- spatial_and_3d_intelligence
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# From Words to Worlds: Spatial Intelligence is AI’s Next Frontier

**Authors:** 
**Published:** 2025-11-10 00:00:00
**Type:** article

## Analysis

# From Words to Worlds: Spatial Intelligence is AI's Next Frontier
2025-11-10 · article
https://drfeifei.substack.com/p/from-words-to-worlds-spatial-intelligence

---

## Briefing

**Fei-Fei Li argues that spatial intelligence — the capacity to perceive, reason about, generate, and interact with 3D physical and virtual worlds — is AI's defining next frontier, and that current LLMs and MLLMs are structurally incapable of achieving it. The path forward requires a new class of generative models called world models, defined by three essential properties: geometric and physical consistency in generation, multimodal input/output, and interactive state-prediction given actions. Without this, AI cannot drive robots, accelerate science, or truly augment human creative and cognitive capability.**

### Key Takeaways
1. **LLMs are eloquent but ungrounded** — State-of-the-art MLLMs perform near chance on distance estimation, object rotation, maze navigation, and basic physics prediction — revealing that language-scale training does not confer spatial understanding.
2. **World models are architecturally distinct from LLMs** — They must reconcile semantic, geometric, dynamic, and physical consistency simultaneously, making their representational challenge vastly harder than next-token prediction over a 1D signal.
3. **The universal task function for world models is unsolved** — Defining an equivalent of next-token prediction that honors geometric and physical laws is the central open research problem; it does not yet exist.
4. **Current tokenization is the wrong primitive for space** — 1D/2D sequence tokenization (used in both MLLMs and video diffusion) makes trivially spatial tasks — counting chairs in a video, maintaining room memory — unnecessarily hard; 3D/4D-aware tokenization is a required architectural shift.
5. **World models unlock robot training data at scale** — Robotic learning is bottlenecked by scarce training data; world models can simulate diverse environments to close the sim-to-real gap and enable generalizable robot policies.
6. **Spatial memory via grounded frames outperforms attention-only context** — World Labs' RTFM model uses spatially-grounded frames as persistent spatial memory, enabling real-time generation with world consistency — a proof-of-concept for non-Transformer spatial architecture.
7. **Internet-scale video is abundant but shallow** — RGB video collections are massive and accessible, but extracting genuine 3D spatial understanding from 2D projections requires fundamentally new algorithms; depth and tactile data are critical supplements.
8. **Synthetic data and novel sensors are underrated** — High-quality synthetic data and additional modalities (depth, tactile) fill critical gaps in training that internet-scale RGB data alone cannot cover.
9. **Interactivity distinguishes world models from video generators** — A world model must predict the next world state given an action input, not just generate plausible-looking video; this action-conditioned rollout is the bridge to embodied agents.
10. **Marble is the first public instantiation** — World Labs' Marble generates consistent, explorable 3D environments from multimodal prompts, targeting creative and storytelling workflows as the first near-term application vertical.
11. **Spatial intelligence is evolutionarily prior to language** — Li frames spatial perception-action loops as the evolutionary engine of intelligence itself, predating and scaffolding all higher cognition — suggesting language models invert the natural order of intelligence development.
12. **The scientific and healthcare applications require the longest horizon** — Creative tools are deployable now; robotics is a mid-term challenge; molecular simulation, drug discovery, and ambient healthcare monitoring are longer-horizon but highest-impact use cases.

---

### Why LLMs Fail at Space: The Grounding Gap

- **LLMs are "wordsmiths in the dark"** — they produce fluent language about the physical world without any internal model of its geometry, physics, or dynamics.
  - Multimodal LLMs introduced some spatial awareness by training on images and video, but this is surface-level pattern matching, not geometric reasoning.
  - Concrete failure modes: near-chance performance on distance/orientation/size estimation, inability to mentally rotate objects by regenerating them from new viewpoints, failure to navigate mazes or identify shortcuts.
  - AI-generated videos lose coherence after seconds — revealing that video diffusion models do not maintain a persistent world state.
- The root cause is representational: language is a 1D sequential signal; the physical world is a 3D dynamic structure with continuous geometry and causal physical laws. Compressing the latter into the former's representational substrate is architecturally ill-suited.
- **Wittgenstein inverted**: Li reframes the "limits of language are limits of world" in the AI direction — language's limits are AI's limits, and spatial intelligence is the capability beyond that boundary.

---

### The Evolutionary Case for Spatial Intelligence as the Foundation of Cognition

- Li grounds the argument in evolutionary biology: **spatial perception-action loops preceded all higher cognition**, including language, social bonding, and abstract reasoning.
  - The capacity to sense external stimuli (light, texture) created a perception-survival bridge that drove the elaboration of nervous systems across hundreds of millions of years.
  - This positions spatial intelligence not as one cognitive module among many but as the substrate from which intelligence emerged.
- Human spatial fluency is automatic and pre-linguistic: parking by feel, catching thrown objects, navigating crowds, pouring coffee without looking — none of these require deliberate reasoning.
  - Firefighters navigate collapsing buildings using spatial judgment, gesture, and embodied professional instinct with no linguistic substitute.
  - Pre-verba

## Key Claims

1. State-of-the-art multimodal LLMs rarely perform better than chance on estimating distance, orientation, and size, or on mentally rotating objects by regenerating them from new angles.
2. Current AI-generated videos often lose coherence after a few seconds.
3. Current AI cannot navigate mazes, recognize shortcuts, or predict basic physics.
4. LLMs are knowledgeable but lack grounding in physical and spatial reality.
5. AI's spatial capabilities remain far from human level despite recent multimodal progress.
6. Current MLLM and video diffusion architectures typically tokenize data into 1D or 2D sequences, making simple spatial tasks unnecessarily difficult.
7. World model research lacks a universal task function as simple and elegant as next-token prediction in LLMs.
8. The dimensionality of representing a world is vastly more complex than that of a one-dimensional sequential signal like language.
9. Training data is scarce for robotic research, unlike for language models.
10. Multimodal LLMs trained with multimedia data have introduced some basics of spatial awareness into AI.

## Capabilities

- Large language models producing coherent text, code, photorealistic images, and short video clips at scale, used as productivity and creativity tools by billions
- Multimodal LLMs analyzing pictures, answering visual questions, and generating hyperrealistic images and short videos with basic spatial awareness
- Advanced robots manipulating objects and tools using breakthroughs in sensors and haptics, within highly constrained environments
- Marble: a world model that accepts multimodal inputs to generate and maintain consistent 3D environments for interactive exploration and creative workflows
- RTFM: real-time generative frame-based model using spatially-grounded frames as spatial memory for efficient real-time generation with persistent world state

## Limitations

- State-of-the-art MLLMs perform at near-chance level on spatial estimation tasks: distance, orientation, size, and mental object rotation
- Current AI cannot navigate mazes, recognize spatial shortcuts, or predict basic physics — core requirements for embodied and autonomous systems
- AI-generated videos lose coherence after only a few seconds, failing to maintain consistent geometry, object identity, and scene continuity
- LLMs are fundamentally ungrounded — they process language without embodied experience, leaving them unable to interact with or reason about physical reality
- Current MLLM and video diffusion architectures tokenize spatial data as 1D or 2D sequences, making inherently spatial tasks (e.g., counting objects in video, long-range scene memory) unnecessarily difficult
- No universal task function analogous to next-token prediction exists for world models; the training objective for spatial AI remains an open research problem
- Training world models requires extracting 3D spatial information from inherently 2D RGB image/video signals, a technically unsolved and lossy inverse problem
- World model training requires better sensor systems, more robust signal extraction algorithms, and more powerful neural simulation methods that do not yet exist at the required scale
- Robotic learning data is extremely scarce compared to language data, blocking the training of generalizable robot policies
- Advanced robots can only manipulate objects and tools in highly constrained environments — not in open-world, unstructured settings
- Autonomous robots remain speculative and far from practical daily-life deployment despite decades of promise
- AI for accelerating scientific discovery in drug discovery, materials science, and particle physics remains largely unfulfilled despite substantial investment
- The dimensionality of world representation is vastly more complex than language, requiring entirely new approaches that have not yet been established
- AI immersive/interactive experiences that truly understand and empower creators — filmmakers, architects, students exploring molecular chemistry — remain beyond reach

## Bottlenecks

- No universal training objective for world models exists — the field lacks the equivalent of next-token prediction to unify learning across spatial, geometric, physical, and dynamic domains
- Current architectures tokenize spatial data as 1D/2D sequences, structurally incompatible with the 3D/4D geometric nature of world representation
- Extracting 3D spatial information from 2D internet-scale image/video data at the scale needed to match LLM training has no solved algorithmic path
- Scarcity of robot interaction data prevents training generalizable robot policies, with no scalable path to data collection matching language model pretraining
- Sensor infrastructure, signal extraction algorithms, and neural simulation methods for world model training are not yet capable of providing the required data quality and diversity
- The sim-to-real gap limits world models' ability to serve as robot training simulators — perceptual fidelity and physical accuracy of simulation are not yet sufficient for transfer

## Breakthroughs

- Marble: first demonstrated world model generating and maintaining consistent 3D environments from multimodal prompts (images, video, text) for interactive exploration and creative use
- RTFM demonstrates that spatially-grounded frame-based memory enables real-time generative world models with persistent state — a departure from stateless video generation

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/imagenet|ImageNet]]
- [[entities/scaling-laws|Scaling Laws]]
- [[entities/spatial-intelligence|Spatial Intelligence]]
- [[entities/world-labs|World Labs]]
- [[entities/world-model|World Model]]
