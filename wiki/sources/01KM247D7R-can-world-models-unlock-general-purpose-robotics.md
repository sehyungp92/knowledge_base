---
type: source
title: Can world models unlock general purpose robotics?
source_id: 01KM247D7RX47AXT5A9B5MSKRD
source_type: article
authors: []
published_at: '2026-03-10 00:00:00'
theme_ids:
- generative_media
- pretraining_and_scaling
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Can World Models Unlock General-Purpose Robotics?

> This article from Bessemer Venture Partners argues that world models, neural networks that learn physics from internet video, represent the most credible structural solution to the data bottleneck blocking general-purpose robotics. Drawing on results from Meta's V-JEPA 2 (80% zero-shot manipulation), DeepMind's Dreamer 4, and frontier models like Genie 3 and Sora, it maps both the directional promise and the critical remaining gaps: inference latency, serving economics, tactile sensing, long-horizon coherence, and the distance between 80% lab success and 99.9% production reliability.

**Authors:** Bessemer Venture Partners
**Published:** 2026-03-10
**Type:** Article
**Source:** https://www.bvp.com/atlas/can-world-models-unlock-general-purpose-robotics

---

## Context

This piece builds on BVP's prior analysis identifying manipulation and data as the central bottlenecks in robotics. It frames world models as the most promising structural response to both, drawing an explicit analogy to how large language models displaced hand-coded grammar rules in NLP. The argument is that the same transition is now underway in robotics, one epoch later, and for the same underlying reason: learned representations scale with compute; hand-engineered systems scale with headcount.

---

## The Core Analogy: NLP 2005

Robotics today is where NLP was in 2005. The dominant paradigm relies on hand-built physics simulators to train robots, programming how objects behave, how surfaces feel, how gravity acts. These simulators cannot generalize. A robot trained to pick up a cup in simulation fails when the cup moves, the lighting shifts, or an unfamiliar object is introduced. These are not edge cases; they are the default conditions of deployment.

LLMs escaped this trap by replacing hand-coded rules with learned representations trained on internet-scale text. World models offer the same escape route for robotics: replace hand-coded physics with representations learned from internet-scale video.

The obstacle is that text was already digitized and freely available. Robot experience is not. There is no internet of robot experience. Teleoperation requires physical hardware, human operators, and real-world environments, making data collection intrinsically slow and expensive. Even as the industry races to collect across every modality, **aggregate robotic data costs are estimated to exceed $3 billion within two years**, and the resulting corpus will still be orders of magnitude smaller than LLM training sets.

---

## What World Models Contribute

A world model is a neural network trained on video to develop an internal representation of physical dynamics: how fabric drapes, how liquids pour, how objects deform under contact. It learns physics through observation rather than through equations, analogous to how a child learns that a ball rolls off a table without solving Newton's laws.

Two properties make world models specifically valuable for robotics:

**Physical intuition.** Internet video contains a vast long tail of object interactions that cannot feasibly be hand-programmed. A world model trained on that video inherits an implicit physics model spanning materials, lighting conditions, deformable objects, and fluid dynamics.

**Imagination.** A world model can simulate "what happens if I grab this mug from the left?" before acting, allowing a robot to learn from thousands of imagined failures without physical risk. This enables reinforcement learning in simulation without requiring a physics engine at all.

The key conceptual separation is between world knowledge and action knowledge. World knowledge (how objects behave, how gravity works, how liquids pour) is universal and transferable across robot bodies. Only a small amount of embodiment-specific data is needed on top of a pre-trained world model to condition it for a particular robot. This separation is what makes internet video a viable pre-training substrate.

---

## Demonstrated Capabilities

### Meta's V-JEPA 2: 80% Zero-Shot Manipulation

The most direct evidence for the world model thesis comes from Meta's V-JEPA 2, pre-trained on over one million hours of internet video. Researchers then added action conditioning from just 62 hours of *unlabeled* robot video, with no task-specific training. The result: **80% zero-shot pick-and-place success on real robot arms across different labs**, with no task-specific training. This demonstrates that internet video provides sufficient physical intuition for meaningful transfer to physical manipulation, and that the required embodiment-specific data can be surprisingly small.

V-JEPA 2 uses a latent (abstract representation) architecture rather than pixel prediction, operating in a compressed feature space rather than generating future frames. See [[themes/vision_language_action_models|Vision Language Action Models]] for context on competing architectural approaches.

### DeepMind's Dreamer 4: RL in Imagination

Dreamer 4 learned to collect diamonds in Minecraft, a task requiring over 20,000 sequential actions from raw pixels, using purely offline data with zero environment interaction. The world model's imagined rollouts substituted entirely for live environment access. This is a demonstration that world model imagination can replace the physical environment for RL training, not just augment it.

Practically, this matters because RL on physical robots is expensive, slow, and dangerous. If world model imagination can serve as the training substrate, the bottleneck shifts from robot-hours to compute-hours. Compute is far cheaper and scales more predictably.

### Emergent Physics at Scale

Both OpenAI's Sora and DeepMind's Genie 2 (11B parameters) exhibit emergent physical understanding: 3D consistency, object permanence, and realistic physics as purely scale-dependent phenomena, not from explicit programming. This parallels emergent capabilities in LLMs and suggests a similar scaling regime may be available for physical world modeling. See [[themes/scaling_laws|Scaling Laws]] and [[themes/pretraining_and_scaling|Pretraining and Scaling]] for the broader context on emergent capabilities.

---

## Critical Limitations and Open Problems

### Inference Speed: 100x Too Slow

V-JEPA 2 takes approximately 16 seconds per action. Production robot control requires sub-100ms latency. The gap is roughly 100x. This is a **blocking limitation** for real-time deployment, though the trajectory is improving as inference optimization research matures. Decart (an Israeli startup) claims a 400x cost reduction through a custom CUDA/C++ inference engine, suggesting the gap may close through hardware-software co-optimization rather than model architecture changes.

### Serving Economics: Structurally Broken

World model serving is economically disconnected from LLM serving in a structural way, not just a degree-of-magnitude way. A text model batches dozens of concurrent user requests on a single chip. A world model must generate per-user environment state in real time; each user effectively requires a dedicated GPU pipeline. Genie 3 costs approximately **$100 per hour per user**. A 70B-parameter LLM costs cents per hour. OpenAI has acknowledged that Sora's economics are "completely unsustainable."

This is not a problem that more efficient training will solve. It requires either architectural innovation that enables batching of stateful world generation, or a shift to explicit geometric representations that amortize computation differently.

### Long-Horizon Coherence: Minutes, Not Hours

Google's Genie 3, arguably the most capable interactive world model at publication, maintains coherent generation for only a few minutes. Over longer horizons, video-centric models suffer from spatial-temporal inconsistency: object permanence failures, spatial drift, causal violations. The world model's internal representation of the scene gradually drifts from coherence as rollout length increases.

Promising approaches are emerging. Explicit memory mechanisms (WorldMem, WorldPack) extend the coherence window by giving models explicit state storage and retrieval. Explicit geometric representations (as in [[entities/world-labs|World Labs]], which grounds generation in a persistent Gaussian splat scaffold) avoid drift by construction, since object positions are stored in the geometric state rather than inferred from frame-to-frame consistency. The tradeoff is that geometric approaches are computationally heavier and more constrained in scene variety.

See [[themes/video_and_world_models|Video and World Models]] for the architecture debate between pixel prediction, latent representation, and diffusion approaches.

### Tactile Sensing: Video Cannot Substitute

Video captures how things look, not how they feel. Force, pressure, and contact dynamics are critical for dexterous manipulation and cannot be learned from watching video. The high-frequency control layer (1,000 to 10,000 Hz) runs entirely on tactile and proprioceptive signals. More importantly, **the hardware for capturing tactile data at scale (sensor gloves, artificial skin) is still maturing**, meaning the data pipeline to train capable manipulation models does not yet exist at the required scale. This is a significant limitation with an improving but uncertain trajectory.

### Physics Laws vs. Pixel Correlations

Multiple recent studies show that scaling alone is insufficient for world models to uncover fundamental physical laws, because they learn statistical correlations from pixels rather than physical constraints. Specific failure modes persist regardless of model size. This is distinct from the long-horizon coherence problem: it means there are systematic gaps in physical reasoning that more data and compute cannot resolve, and that may require architectural changes (explicit physics priors, hybrid simulation-neural approaches) rather than just scale.

### The 80% to 99.9% Gap

The most honest framing in the piece: current world model results are compelling in research but far from deployment-grade. The gap between 80% lab success and 99.9% production reliability is unresolved, and it is unclear whether the path is primarily more scale, better architecture, more diverse data, or something not yet identified.

---

## Architectural Landscape

No consensus has emerged on which world model architecture will dominate for robotics:

| Approach | Representative Models | Strengths | Weaknesses |
|---|---|---|---|
| Pixel prediction | Sora, Genie 3 | Rich visual fidelity, scales well | Drift, high inference cost |
| Latent representation (JEPA) | V-JEPA 2 | Faster inference, abstract reasoning | Less visual detail |
| Diffusion-based | Cosmos, GAIA-2 | High quality generation | Slow sampling |
| Explicit geometry | World Labs | Strong long-horizon consistency | Computationally heavy, limited scene variety |

The scale of investment is accelerating regardless: NVIDIA's Cosmos was trained on 10,000 H100 GPUs over three months; Wayve's GAIA-2 is at 8.4B parameters; Genie 3 at approximately 11B. **Frontier training runs cost tens to hundreds of millions of dollars**, creating meaningful barriers for non-hyperscaler participants.

---

## Simulator vs. World Model: Where Each Stands

Physics engines like MuJoCo and Isaac Sim remain effective for rigid-body locomotion (getting a quadruped to walk across rough terrain), where contact details are coarse and generalizable. They fail for dexterous manipulation, where contact is soft, distributed across a surface, and sensitive to friction and material properties. Simulating this accurately requires solving partial differential equations at fine spatial resolution in real time, which current simulators cannot do reliably.

World models address the manipulation gap precisely because they do not simulate contact from first principles; they learn its visual and dynamic signatures from data. But they inherit the tactile blindness described above. The practical picture is a split regime: simulators for locomotion, world models for manipulation planning, with dedicated hardware pipelines for the tactile control layer.

---

## Implications

**For [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]:** The world model thesis, if validated at scale, would shift the primary bottleneck from simulation fidelity to data collection and inference efficiency, changing where investment is most productive.

**For [[themes/robot_learning|Robot Learning]]:** The demonstration that imitation learning alone is insufficient for robust autonomy (only RL-based approaches have demonstrated 10+ hour uninterrupted operation) suggests that world model-enabled RL in imagination may be a necessary component of any production robotics system, not merely an efficiency optimization.

**For [[themes/generative_media|Generative Media]]:** The serving economics problem (structural inability to batch per-user stateful generation) is a constraint that applies equally to interactive media and robotics planning. Architectural solutions developed for one domain will likely transfer to the other.

**For [[themes/pretraining_and_scaling|Pretraining and Scaling]]:** The emergence of object permanence and physical consistency as scale phenomena in Sora and Genie 2 extends the scaling laws narrative to physical world modeling, with the important caveat that pixel-level correlations do not imply physical law learning.

---

## Open Questions

- Will abstract latent representations (JEPA-style) or pixel-prediction approaches dominate as the pre-training substrate for robot manipulation? The architectural debate is unresolved.
- Can explicit geometric representations scale to the scene richness and variety needed for real-world robotics, or does the consistency-diversity tradeoff remain fundamental?
- Is tactile sensing a data problem (solvable with better capture hardware) or an architectural problem (requiring hybrid modalities that video-first world models cannot accommodate)?
- What is the minimum embodiment-specific data required for reliable transfer from internet video? V-JEPA 2 used 62 hours; is that a floor or a ceiling?
- Can world model serving costs be reduced to near-LLM economics through inference optimization, or does the stateful per-user generation requirement impose a structural floor?

---

## Themes

- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]
- [[themes/robot_learning|Robot Learning]]
- [[themes/video_and_world_models|Video and World Models]]
- [[themes/vision_language_action_models|Vision Language Action Models]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/generative_media|Generative Media]]

## Key Concepts

- [[entities/genie-3|Genie 3]]
- [[entities/imitation-learning|Imitation Learning]]
- [[entities/sora|Sora]]
- [[entities/world-labs|World Labs]]
- [[entities/world-model|World Model]]
