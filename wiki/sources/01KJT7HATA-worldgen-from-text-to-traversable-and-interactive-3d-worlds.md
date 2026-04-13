---
type: source
title: 'WorldGen: From Text to Traversable and Interactive 3D Worlds'
source_id: 01KJT7HATAE1FWWZQRA88CSKAP
source_type: paper
authors:
- Dilin Wang
- Hyunyoung Jung
- Tom Monnier
- Kihyuk Sohn
- Chuhang Zou
- Xiaoyu Xiang
- Yu-Ying Yeh
- Di Liu
- Zixuan Huang
- Thu Nguyen-Phuoc
- Yuchen Fan
- Sergiu Oprea
- Ziyan Wang
- Roman Shapovalov
- Nikolaos Sarafianos
- Thibault Groueix
- Antoine Toisoul
- Prithviraj Dhar
- Xiao Chu
- Minghao Chen
- Geon Yeong Park
- Mahima Gupta
- Yassir Azziz
- Rakesh Ranjan
- Andrea Vedaldi
published_at: '2025-11-20 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- robotics_and_embodied_ai
- spatial_and_3d_intelligence
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# WorldGen: From Text to Traversable and Interactive 3D Worlds

**Authors:** Dilin Wang, Hyunyoung Jung, Tom Monnier, Kihyuk Sohn, Chuhang Zou, Xiaoyu Xiang, Yu-Ying Yeh, Di Liu, Zixuan Huang, Thu Nguyen-Phuoc, Yuchen Fan, Sergiu Oprea, Ziyan Wang, Roman Shapovalov, Nikolaos Sarafianos, Thibault Groueix, Antoine Toisoul, Prithviraj Dhar, Xiao Chu, Minghao Chen, Geon Yeong Park, Mahima Gupta, Yassir Azziz, Rakesh Ranjan, Andrea Vedaldi
**Published:** 2025-11-20 00:00:00
**Type:** paper

## Analysis

# WorldGen: From Text to Traversable and Interactive 3D Worlds
2025-11-20 · paper · Dilin Wang, Hyunyoung Jung, Tom Monnier, Kihyuk Sohn, Chuhang Zou et al. (25 total)
https://arxiv.org/pdf/2511.16825

---

### Motivation & Prior Limitations
- Creating 3D content for interactive experiences is complex, time-consuming, and requires significant expertise, and existing 3D generative AI had only addressed single-object generation rather than the full pipeline needed for game-ready worlds.
  - Generating a single 3D object is only a small fraction of what is needed for full experiences, which also require scenes, navigability, interactions, gameplay mechanics, and more.
  - Interactive video generators that produce pixels directly from prompts are "likely many years away from becoming a mature technology that can displace traditional world creation paradigms," meaning traditional 3D representations compatible with game engines remain necessary.
- Even state-of-the-art text-to-image models struggle to generate scenes that are functionally traversable, meaning generated scenes could not be reliably navigated by characters without obstruction.
  - Without structural constraints, image generators cannot guarantee navigability — characters may get "stuck" due to obstructions in the generated geometry.
- There is no sufficiently large training set of 3D scenes to enable direct text-to-scene learning, forcing reliance on image-mediated pipelines.
  - This data scarcity required a two-stage strategy: pre-training on generic objects, then fine-tuning on a curated scene dataset the authors had to construct themselves.
- Prior compositional scene generators based on Gaussian splats (e.g., Marble from World Labs) achieve photorealism near a conditioned viewpoint but degrade in fidelity within just 3–5 meters of camera movement and are incompatible with standard game engines like Unreal and Unity.
  - Gaussian splat representations are not natively supported by game engines or standard artist toolsets, require specialized rendering pipelines, and are orders of magnitude slower to render than optimized meshes on mobile and low-end hardware.
- Monolithic image-to-3D reconstruction methods are non-compositional and produce insufficient geometry and texture resolution for direct use in game engines, particularly at scene scale.
  - Single-shot image-to-3D models reconstruct only what is visible and cannot complete geometry behind occlusions, leaving large regions unresolved in complex scenes.

---

### Proposed Approach
- WorldGen is a four-stage end-to-end pipeline that transforms a single text prompt into a fully textured, traversable, compositional 3D scene exported as game-engine-ready assets, by chaining LLM-driven procedural layout, navmesh-conditioned 3D reconstruction, autoregressive scene decomposition, and per-object enhancement.
  - Unlike monolithic scene generators, WorldGen outputs a scene as a set of individually textured and editable 3D mesh objects with a valid navmesh, making it directly compatible with Unreal and Unity without specialized rendering infrastructure.

**Stage I — Scene Planning:** An LLM parses the text prompt into structured JSON parameters (terrain type, density, verticality, placement regularity) that drive a modular procedural generation (PG) pipeline, producing a 3D blockout, navmesh (via Recast), and a reference image conditioned on the blockout's isometric depth map via a depth-conditioned diffusion model.
  - The PG pipeline runs terrain generation (Perlin noise or rule-based heightmaps), spatial partitioning (binary space partitioning and Voronoi diagrams for structured vs. organic environments), and hierarchical three-pass asset placement (hero → medium → decorative), guaranteeing navigability by construction.
  - The semantic meaning of blockout volumes is deliberately left unspecified; the image generator interprets each box as a tree, building, or rock, allowing stylistic diversity while maintaining structural constraints.

**Stage II — Scene Reconstruction:** AssetGen2, a latent 3D diffusion model using the VecSet representation (unordered set of latent vectors decoding a signed distance field via Marching Cubes), is fine-tuned for navmesh-conditioned generation, sampling from p(z | R, S) rather than p(z | R) alone.
  - The navmesh is tokenized using a VecSet-style encoder (FPS downsampling + cross-attention over dense points) and integrated into the AssetGen2 denoising transformer via additional cross-attention layers; end-to-end fine-tuning of the full transformer (not just the new conditioning layers) was found empirically superior.
  - A volumetric texture is applied to the holistic mesh using a retrained TRELLIS model (trained on in-house object- and scene-level data) to provide low-resolution colorization sufficient to guide the enhancement stage.

**Stage III — Scene Decomposition:** AutoPartGen is extended and accelerated by replacing its fixed lexicographical generation order with a connectivity-degree ordering — pivot parts (most connected, e.g., terrain/ground) are generated first, then remaining geometry is recovered via connected-component analysis of the residual.
  - A binary flag token signals the model to generate all remaining geometry in a single forward pass after four pivot parts, reducing decomposition time from ~10 minutes to ~1 minute for complex scenes.
  - AutoPartGen is fine-tuned on a curated scene-level dataset created by the authors: 3D scenes were mined from an internal repository using a VLM to identify multi-object environments, then processed through a four-step pipeline (connected components, ground detection, small-part merging, quality filtering) to produce part annotations.

**Stage IV — Scene Enhancement:** Each decomposed low-resolution object is individually enhanced through three sequential steps — image enhancement via an LLM-VLM conditioned on a top-down scene render (with target object highlighted in red) plus the glob

## Key Claims

1. WorldGen enables automatic creation of large-scale, interactive 3D worlds directly from text prompts, producing traversable, fully textured environments explorable within standard game engines.
2. No sufficiently large training set of 3D scenes exists to allow learning a direct mapping from text prompt to 3D scene.
3. Even the best image generators struggle to imagine scenes that are functional and traversable.
4. Interactive video generators that generate pixels directly from high-level prompts and user interactions are likely many years away from displacing traditional world creation paradigms.
5. WorldGen reduces 3D scene generation to first generating an image of the 3D scene followed by image-to-3D reconstruction, leveraging text-to-image models trained on billions of images.
6. WorldGen uses an LLM to map user-provided text prompts to structured JSON parameters that configure a procedural generation pipeline for scene layout.
7. The procedural generation pipeline constructs the scene blockout in three steps: terrain generation, spatial partitioning, and hierarchical asset placement.
8. For structured environments, WorldGen uses binary space partitioning, uniform grids, or k-d trees; for natural or irregular landscapes, it uses Voronoi diagrams, noise-based partitions, or Drunkard's 
9. The procedural generation does not assign semantic meaning to placed objects; instead, it leaves the image generator free to interpret blocks as trees, rocks, or buildings.
10. The navmesh is extracted from the blockout geometry using the Recast algorithm, which identifies exterior traversable surfaces while excluding indoor areas.

## Capabilities

- End-to-end generation of large-scale (~50×50m) traversable, compositional 3D worlds from a single text prompt, producing individually editable, fully textured meshes with valid navigation meshes deployable directly in standard game engines (Unreal, Unity) in approximately 5 minutes
- LLM-driven mapping from natural language scene descriptions to structured procedural generation parameters (terrain type, density, verticality, layout), enabling text-controlled functional 3D layout generation with guaranteed navigability via rule-based procedural constraints
- Navmesh-conditioned holistic 3D scene reconstruction from a single reference image, achieving 40–50% lower Chamfer distance alignment with navigation constraints compared to image-only baselines, enabling spatial editing via navmesh modification rather than image editing
- Automated decomposition of holistic scene meshes into semantically meaningful, individually editable 3D objects in approximately 1 minute — down from 10 minutes for prior AutoPartGen — while outperforming all prior methods on Chamfer distance and F-score across all thresholds
- Per-object geometry, texture, and mesh enhancement using LLM-VLM guided image generation with top-down scene context, maintaining global style consistency across individually refined objects within a compositional 3D scene

## Limitations

- No sufficiently large training dataset of 3D scenes exists for learning a direct text-to-3D-scene mapping, forcing all current systems to use indirect proxy approaches via 2D image generation as a bridge
- State-of-the-art image generation models cannot reliably generate traversable, functionally coherent scenes without external structural guidance — even the best generators produce scenes that may be impassable or spatially incoherent
- Fixed latent representation capacity in 3D diffusion models causes geometric fidelity to degrade as scene complexity increases — more objects means less representational capacity per object, resulting in progressively lower-quality individual reconstructions
- No publicly available dataset of 3D scenes with part-level annotations exists, requiring systems to build their own via expensive VLM-assisted mining and heuristic pipelines
- LLM-VLM per-object image enhancement fails to generate style-consistent or reference-faithful images without explicit global scene context (top-down view) — conditioned only on global reference image, the model cannot infer an object's location, semantics, or style from its surroundings
- Generative image enhancement for per-object refinement routinely introduces geometric or stylistic drift — shape distortion, unexpected camera view changes, hallucinated geometry, and incorrect background compositing are common failure modes requiring iterative IoU-based verification
- WorldGen produces only static geometry — animation, character systems, gameplay mechanics, NPCs, physics interactions, and storylines are entirely absent, meaning AI-generated content covers only a small fraction of what a full 3D interactive experience requires
- End-to-end interactive video generators that would subsume world-creation via pixel generation from high-level prompts and user interactions are assessed by the authors as many years away from displacing traditional 3D representation pipelines
- View-based 3D scene generation methods — including radiance field approaches like Marble/Gaussian splatting — are limited to generating small 'bubbles' of a few meters, degrading rapidly as the observer moves 3–5m from the conditioned viewpoint
- Gaussian splat representations — despite superior photorealism near the conditioned viewpoint — are not natively supported by standard game engines (Unreal, Unity), require specialized rendering pipelines, and render orders of magnitude slower than optimized meshes, making them impractical for mobil
- The full WorldGen pipeline requires approximately 5 minutes and assumes sufficient parallel GPU availability — no indication of consumer-hardware feasibility, and real-time or interactive-rate world generation at this quality level is not demonstrated
- All existing part segmentation and decomposition models fail to generalize from object-level training to complex scene-level inputs — producing unstable decompositions, incorrect terrain segmentation, over-fragmented buildings, or merged ground-object geometry when applied to full outdoor scenes
- WorldGen's benchmark evaluation uses only 50 procedurally generated scenes with moderate terrain verticality and 10–30 objects — highly controlled conditions that likely do not reflect performance on extreme terrain, very dense environments, or diverse artistic prompts
- Image generators hallucinate objects not specified in the procedural blockout that are incompatible with navigation intent and may obstruct traversal, requiring navmesh conditioning as a downstream correction mechanism rather than eliminating the issue

## Bottlenecks

- Absence of large-scale annotated 3D scene training datasets blocks direct text-to-3D-scene generative modeling, forcing all systems to use 2D image generation as an indirect proxy — inheriting 2D limitations and preventing the quality ceiling of LLM-scale training from applying to 3D
- Fixed-capacity latent representations in 3D diffusion models cannot scale to complex multi-object scenes — the fixed token budget must distribute capacity across all scene geometry, causing per-object fidelity to degrade linearly with scene complexity
- Image generation models lack functional navigability objectives, requiring external procedural scaffolding or structural conditioning to produce traversable scenes — pure end-to-end text-to-functional-3D pipelines cannot yet bypass this dependency

## Breakthroughs

- WorldGen demonstrates end-to-end generation of large-scale (~50×50m), navigable, compositional 3D worlds from a text prompt in ~5 minutes — producing game-engine-compatible textured mesh scenes with individually editable objects and valid navigation meshes, at a scale 10x larger than prior 'bubble' 
- Navmesh conditioning for 3D reconstruction: incorporating explicit walkability constraints as a learned conditioning signal into a latent diffusion 3D model reduces navmesh alignment error by 40–50% and enables scene editing via navmesh manipulation rather than image editing — establishing that 3D f

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/video_and_world_models|video_and_world_models]]
