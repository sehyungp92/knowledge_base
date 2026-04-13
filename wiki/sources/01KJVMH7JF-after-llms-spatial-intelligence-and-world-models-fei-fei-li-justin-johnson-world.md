---
type: source
title: 'After LLMs: Spatial Intelligence and World Models — Fei-Fei Li & Justin Johnson,
  World Labs'
source_id: 01KJVMH7JFEX2PR1P5D2C80B55
source_type: video
authors: []
published_at: '2025-11-25 00:00:00'
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
# After LLMs: Spatial Intelligence and World Models — Fei-Fei Li & Justin Johnson, World Labs

> A wide-ranging conversation between Fei-Fei Li and Justin Johnson of World Labs on the architectural demands of spatial intelligence, the nature of 3D world generation, and the fundamental differences between language and spatial cognition — grounded in the capabilities and limitations of their Marble system and broader arguments for why physical-world reasoning cannot be fully reduced to token sequences.

**Authors:** Fei-Fei Li, Justin Johnson
**Published:** 2025-11-25
**Type:** video

---

## Core Argument

The central thesis is that spatial intelligence is a genuinely distinct cognitive modality — not a variant of language intelligence that can be subsumed by sufficiently large LLMs. Language operates over 1D sequential signals. The physical world is 3D and 4D, structured by forces, causality, and embodied interaction that cannot be faithfully compressed into token sequences. This is simultaneously an architectural argument (different representation demands), a data argument (visual/spatial data is far higher bandwidth), and a philosophical argument about the nature of understanding.

The framing is not adversarial toward language models — it is complementary. World Labs positions spatial intelligence as a second major frontier after language, requiring its own models, representations, and scaling trajectories.

---

## The Representation Problem

### Why Pixels Over Tokens

Language is often treated as categorically distinct from vision, but at the biological level it is processed through the same visual substrate. Text is a visual object. Even audio can be rendered as a 2D correlogram. The key observation is that tokenised representations are *lossy*: they discard font, layout, spatial arrangement, and visual structure that sometimes carries meaning.

Pixels are a more general and lossless representation — closer to the actual substrate of human perceptual experience. The counterargument is efficiency: passing rendered text through vision models is computationally heavier than feeding tokens to a transformer. But examples like DeepSeek suggest this can work at surprising scale.

### The 1D vs. 3D Gap

Standard language model architectures were designed around 1D generative signals. The physical world is fundamentally 3D and 4D (including motion over time). Even where architectures can be adapted — transformers are theoretically general — the *representations* optimised for language do not transfer cleanly to spatial reasoning. This manifests most clearly in the limitation that LLMs systematically fail at spatial reasoning tasks that humans find trivial: a Harvard study fed orbital mechanics patterns to an LLM, which then failed to predict the orbit of a planet in a novel configuration. The model had learned correlations, not the underlying physical law.

---

## Marble and the Gaussian Splat Architecture

Marble is World Labs' generative model of 3D worlds. It accepts text or image inputs and outputs 3D scenes natively represented as Gaussian splats. This representational choice is central to what makes Marble distinctive from video generative models.

**Why Gaussian splats:**
- Real-time rendering on client-side devices including 4-year-old iPhones and VR headsets (30–60 FPS)
- Enables *precise camera placement and movement control* — the model maintains an internal 3D spatial representation, so the user can specify exact viewpoints rather than learning to prompt a director's vocabulary
- Enables downstream simulation: splats can have physical properties (mass, spring coupling to neighbours) attached post-generation, allowing physics simulation on top of a generated scene

The contrast with frame-by-frame video generative models is sharp: those models produce temporally coherent pixels but have no stable internal 3D structure, so camera control is indirect and imprecise.

**Current constraints:**
- Splat density is bounded by rendering target — consumer VR headsets and older iPhones impose significant limits on splat count per scene
- Marble does not simulate dynamics or physics; scenes are static 3D environments with visual coherence but no force modelling
- High-resolution, high-fidelity rendering at target frame rates requires either high-end hardware or relaxed quality

**RTFM** is a companion model from World Labs that generates 3D frames one at a time as the user interacts, where the atomic unit is a single frame rather than a complete scene.

---

## The Physics Understanding Problem

This is the deepest open question the conversation surfaces. Marble can generate visually realistic arches. Does it *understand* the structural physics of an arch?

The answer depends on the use case:
- **For film/VFX/gaming**: plausibility is sufficient. If the output matches what a real arch should look like, the model is doing its job.
- **For architecture or engineering**: the answer changes entirely. Physical correctness is safety-critical. A model that learned to imitate the *appearance* of load-bearing structures without modelling compressive forces is dangerous.

Two approaches to grounding physics in spatial models:

| Approach | Mechanism | Risk |
|---|---|---|
| **Explicit supervision** | Train on physics simulation data; hope model learns underlying laws | May learn to imitate simulation outputs without recovering causal structure |
| **Latent emergence** | Train end-to-end; hope physics emerges implicitly in latent space | No guarantee representations align with true causal dynamics |

The core limitation of deep learning is that it is fundamentally a pattern-fitting system. It recovers statistical regularities in training data. Humans appear to build abstractions that hold across much wider variation, with longer time horizons and richer causal structure — though whether this is a categorical difference or a difference in the scope and abstraction level of pattern matching remains philosophically contested.

---

## The Compute Trajectory

The historical argument for spatial intelligence as the next scaling frontier draws on the compute trajectory of deep learning:

- From AlexNet to present: ~1000× improvement in GPU performance per card
- Total compute available for a single training run: ~1 million× increase over the same period
- Training on hundreds to tens of thousands of GPUs simultaneously is now standard practice

The key insight is that visual and spatial data requires significantly more compute to process than language data. This creates *demand* that will absorb newly available compute headroom — the same dynamic that drove language model scaling now applies to spatial models. This is not presented as speculation; it is presented as a structural consequence of the data modality.

**Hardware ceiling caveat:** The conversation also notes that performance-per-watt improvements from Hopper to Blackwell are already showing signs of diminishing returns. Matrix-multiplication-centric GPU design may not scale indefinitely, and there is no clear successor architecture in view.

---

## Landscape Contributions

### Capabilities

- **Interactive 3D world generation** from text/image inputs with real-time rendering at 30–60 FPS on mobile/VR via Gaussian splat representation — currently at narrow production maturity, deployed in gaming, VFX, and film contexts
- **Precise camera control** in generated 3D scenes, a direct consequence of maintaining an internal spatial representation rather than generating frame sequences
- **Language-conditioned 3D generation** combining text prompts with spatial output — part of a multimodal stack where language and spatial models complement rather than replace each other
- **Spatial intelligence as a distinct modality** — capable of reasoning about 3D structure, movement, and interaction; currently at demo maturity for general-purpose spatial reasoning

### Limitations

| Limitation | Severity | Trajectory |
|---|---|---|
| No causal understanding of physics — models fit patterns, not forces | Significant | Stable |
| Static scenes only — Marble lacks dynamics, mass, or physical simulation | Significant | Improving |
| Resolution-constrained rendering on mobile/VR hardware | Significant | Improving |
| Unpredictable emergent capabilities — unclear whether scaling yields implicit physics | Significant | Unclear |
| LLMs fail at spatial reasoning tasks trivial to humans | Significant | Stable |
| Tokenisation is lossy relative to visual/spatial input | Minor | Stable |
| No theory of mind or emotional intelligence | Significant | Stable |
| Massive bandwidth gap: language ≪ embodied sensorimotor experience | Significant | Stable |
| Models lack embodied grounding for physical causality | Significant | Stable |

### Bottlenecks

- **Physics-aware spatial generation**: Cannot simultaneously achieve visual fidelity *and* causal physics understanding. Whether scaling alone bridges this gap is explicitly uncertain. Blocking production-ready 3D generation for engineering and safety-critical applications. (~1–2 year horizon)
- **Architectural mismatch**: Transformers optimised for 1D sequences may not be optimal for 3D spatial reasoning despite theoretical generality. Blocking unified multimodal architectures. (~1–2 year horizon)
- **Hardware efficiency ceiling**: Performance-per-watt scaling showing early signs of saturation. No clear post-GPU successor architecture in view. (~3–5 year horizon)

### Breakthroughs

- **Gaussian splat-based 3D generation at mobile/VR scale** — achieving real-time interactive rendering on consumer hardware while maintaining precise spatial control. This enables world model deployment outside data centres.
- **Spatial intelligence framing** — positioning spatial cognition as a complementary modality to language with distinct processing demands, rather than a downstream capability of sufficiently large LLMs.

---

## Open Questions

1. Can models learn implicit physics from visual data at scale, or does explicit supervision on simulation data remain necessary for physical correctness?
2. Does the emergent capability dynamic observed in language models generalise to physical reasoning — and if so, at what scale?
3. Is the architecture of transformers a fundamental constraint for spatial reasoning, or merely a convenience that can be adapted with sufficient effort?
4. What is the right boundary between "plausibility is enough" and "physical correctness is required"? For which applications does visual coherence without causal grounding become a liability rather than an asset?
5. If classical physics engines cannot solve problems with the required generality, and learned models cannot yet recover causal structure — what fills the gap?

---

## Themes

- [[themes/spatial_and_3d_intelligence|Spatial and 3D Intelligence]]
- [[themes/video_and_world_models|Video and World Models]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/generative_media|Generative Media]]
- [[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]

## Key Concepts

- [[entities/imagenet|ImageNet]]
- [[entities/spatial-intelligence|Spatial Intelligence]]
- [[entities/world-models|World Models]]
