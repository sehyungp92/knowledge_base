---
type: source
title: Video models are zero-shot learners and reasoners
source_id: 01KJTG79VBC96CY7VWVCFC7R79
source_type: paper
authors:
- Thaddäus Wiedemer
- Yuxuan Li
- Paul Vicol
- Shixiang Shane Gu
- Nick Matarese
- Kevin Swersky
- Been Kim
- Priyank Jaini
- Robert Geirhos
published_at: '2025-09-24 00:00:00'
theme_ids:
- chain_of_thought
- generative_media
- multimodal_models
- reasoning_and_planning
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Video models are zero-shot learners and reasoners

**Authors:** Thaddäus Wiedemer, Yuxuan Li, Paul Vicol, Shixiang Shane Gu, Nick Matarese, Kevin Swersky, Been Kim, Priyank Jaini, Robert Geirhos
**Published:** 2025-09-24 00:00:00
**Type:** paper

## Analysis

# Video models are zero-shot learners and reasoners
2025-09-24 · paper · Thaddäus Wiedemer, Yuxuan Li, Paul Vicol, Shixiang Shane Gu, Nick Matarese et al. (9 total)
https://arxiv.org/pdf/2509.20328

---

### Motivation & Prior Limitations
Machine vision remains fragmented into task-specific specialist models — one for segmentation (SAM), another for detection (YOLO variants), another for edge detection — whereas NLP underwent a unification through LLMs that eliminated the need for per-task fine-tuning and bespoke architectures.
- No existing vision model can solve arbitrary tasks through prompting alone, making zero-shot transfer to novel visual tasks rare or impossible without task-specific training or inference heads.
  - Models like SAM require specifying categories or location prompts; they do not generalize to arbitrary unseen task formulations.
- The state of machine vision in 2025 resembles NLP circa 2018–2020: excellent specialists exist, but no general-purpose foundation model supports the full vision stack via prompting.
  - The core claim is that the same primitives that enabled LLM generalism — large generative models trained on web-scale data — now apply to generative video models, and have not yet been fully exploited for zero-shot vision.

---

### Proposed Approach
The paper proposes no new architecture or training method; instead, it demonstrates that prompting a capable off-the-shelf video model (Veo 3) with an initial image and a text instruction suffices to elicit zero-shot solutions across a broad spectrum of vision tasks, establishing that emergent generalism in video models is already present.
- The evaluation strategy mirrors how LLM zero-shot capabilities were characterized: prompt the model with a task instruction and initial image (used as the first frame), generate an 8-second 720p video, and evaluate frames for task completion — no fine-tuning, no task-specific heads, no gradient updates.
  - The system is treated as a black box (LLM-based prompt rewriter + video generator via Vertex AI), and the authors verify that the reasoning does not reduce entirely to the LLM rewriter by confirming that Gemini 2.5 Pro alone cannot reliably solve key spatial tasks (maze, navigation, symmetry) from the same image inputs.
- The "chain-of-frames" (CoF) concept is introduced as an analogy to chain-of-thought in LLMs: video generation proceeds frame-by-frame, and each frame can represent an incremental step in a multi-step reasoning process, allowing the model to apply sequential spatial and temporal manipulations to solve problems that require step-by-step planning.
  - This framing distinguishes video models from image models as the more general framework, since video handles both temporal and spatial dimensions simultaneously.
- 18,384 generated videos are analyzed across 62 qualitative and 7 quantitative tasks, organized into a four-level hierarchy: Perception → Modeling → Manipulation → Reasoning, each layer building on the previous.

---

### Results & Capabilities
Veo 3 demonstrates zero-shot performance across the full vision stack — perception, world modeling, manipulation, and spatial reasoning — with consistent and large performance gains over its predecessor Veo 2, which was released approximately six months earlier.

**Perception:** Veo 3 performs zero-shot edge detection at OIS 0.77 (pass@10, BIPEDv2), approaching the supervised reference (0.90 SOTA) without any task-specific training; qualitative edge maps are sometimes more detailed than ground truth, suggesting a dataset ceiling rather than a model ceiling.
- Zero-shot instance segmentation achieves mIoU 0.74 (best frame, pass@10) on a subset of LVIS, matching the image editing model Nano Banana (0.73) though below SAMv2; prompt wording materially affects performance (green background outperforms white by ~8 mIoU points, likely due to green-screen prevalence in training data).

**World Modeling / Physics:** Veo 3 correctly simulates rigid and soft body dynamics, air resistance, buoyancy, flammability, optical phenomena (refraction, reflection), additive and subtractive color mixing, and physically plausible object removal order (Visual Jenga task).
- The model maintains a consistent internal world-state memory across camera movements within a generated video, a prerequisite for grounded physical simulation.
- Object affordance understanding, category parsing, pattern recognition and generation (Omniglot-inspired), and object packing (which items fit in a backpack) are demonstrated qualitatively.

**Manipulation:** Object extraction (lining up all animals in a scene) reaches 93% pass@10 on Veo 3 vs. near-chance for Veo 2; image editing evaluated on Emu-edit shows Veo 3 excels at preserving texture fidelity across edits, rated highly by human evaluators on both fidelity and precision dimensions.

**Reasoning / Planning:** Maze solving on 5×5 grids achieves 78% pass@10 for Veo 3 vs. 14% for Veo 2; on 9×9 irregular mazes, Veo 3 reaches 75% pass@10 while Nano Banana fails entirely and Gemini 2.5 Pro (T2T) falls behind at larger sizes.
- Visual symmetry completion shows Veo 3 outperforming both Veo 2 and Nano Banana by a large margin; pass@1 varies by up to 64 percentage points across prompt formulations on the random pattern split, revealing high sensitivity to prompt engineering.
- Visual analogy solving (KiVA benchmark, four transformation types) shows Veo 3 correctly completing color and resize analogies but both models perform below chance (0.33) on reflect and rotate transformations, indicating a systematic spatial reasoning bias.
- Additional qualitative reasoning tasks include graph traversal, tree BFS, sequence completion, number sorting, rule extrapolation, Sudoku, and robot navigation.

---

### Implications
The emergence of zero-shot generalism in video models — using the same training primitives as LLMs (large-scale generative pretraining on web data) — suggests machine vision is approaching a "GPT-3 m

## Key Claims

1. Video models are on a trajectory to become unified, generalist vision foundation models, analogous to how LLMs became general-purpose language foundation models.
2. The same primitives that enabled zero-shot learning in LLMs — large generative models trained on web-scale data — also apply to today's generative video models.
3. Machine vision today resembles the state of NLP before LLMs: excellent task-specific models exist but no single model can solve any problem just by prompting.
4. Veo 3 demonstrates emergent perceptual abilities well beyond its training task, including interpreting ambiguous images such as the Dalmatian illusion and Rorschach blots.
5. Veo 3 can model physical properties zero-shot, including flammability, rigid and soft body dynamics, air resistance, and buoyancy.
6. Veo 3 maintains a memory of world state across time and camera movements within the video context.
7. Frame-by-frame video generation is analogous to chain-of-thought in language models, enabling video models to reason across time and space — termed 'chain-of-frames' (CoF).
8. Veo 3 achieves 0.77 OIS pass@10 on zero-shot edge detection on BIPEDv2, while task-specific SOTA achieves 0.90.
9. Veo 3 generates edge maps more detailed than ground truth in some cases (e.g., outlining foliage and tire profiles), suggesting dataset annotation limitations rather than model limitations.
10. Veo 3 achieves mIoU of 0.74 (best frame pass@10) on class-agnostic instance segmentation on LVIS, comparable to Nano Banana's 0.73.

## Capabilities

- Veo 3 performs zero-shot edge detection, instance segmentation, keypoint localization, super-resolution, blind deblurring, denoising, and low-light enhancement without any task-specific training — achieving segmentation mIoU of 0.74 pass@10, comparable to specialist image editing models
- Veo 3 zero-shot models intuitive physics — flammability, rigid and soft body dynamics, air resistance, buoyancy, refraction, reflection, and additive/subtractive color mixing — from web-scale video training alone
- Veo 3 performs zero-shot image editing (background removal, style transfer, colorization, inpainting, outpainting, text manipulation, novel view synthesis, 3D-aware reposing, scene composition) via video generation prompting alone
- Veo 3 solves visual reasoning tasks (mazes, graph traversal, BFS on trees, visual analogies, symmetry completion, sorting, connecting colors) through chain-of-frames generation — achieving 78% pass@10 on 5×5 mazes zero-shot
- Veo 3 recognizes object affordances and simulates dexterous tool use and manipulation (jar opening, ball throwing, rolling a burrito) in zero-shot from a still image and text prompt
- Veo 3 performs visual object extraction and tallying (extracting N animals from scenes and arranging them correctly in a row) at 93% pass@10, demonstrating accurate object counting via video generation

## Limitations

- Veo 3 zero-shot performance remains below task-specific SOTA across all evaluated vision tasks — edge detection achieves 0.77 pass@10 vs 0.90 for specialist models; segmentation lags SAMv2
- Video generation inference is substantially more expensive per task than running a bespoke computer vision model, blocking practical deployment as a drop-in replacement
- Reliable task performance requires multiple sampling attempts (pass@10 >> pass@1), and the optimal output frame is not identifiable a priori — making fully automated single-shot deployment impractical
- Veo 3 performs below chance on reflect and rotate visual analogies (pass@1 < 0.33), indicating a systematic geometric transformation blindspot baked into training
- Extreme prompt sensitivity: 40–64 percentage point performance swing between best and worst prompts on the same symmetry task, making results highly dependent on non-obvious prompt engineering
- Veo 3 has a systematic bias toward animating scenes during image editing — introducing unwanted camera movement and character animation — reducing editing precision
- Video generation continues animating after task completion — the last frame often degrades relative to the best frame — requiring external frame selection logic for any automated pipeline
- The Vertex API system includes an LLM-based prompt rewriter, making it impossible to cleanly attribute task success to the video model vs. the upstream language model — contaminating capability claims
- Maze solving performance collapses sharply at larger grid sizes — 5×5 grids achieve 78% pass@10 but 9×9 grids achieve only 22% pass@10 — revealing a fundamental visual planning depth limit
- Veo 3 fails on hard spatial planning tasks involving long-horizon physical constraint reasoning — folding laundry, planning furniture movement through doorways — suggesting a hard ceiling on CoF reasoning depth
- Segmentation evaluation uses only 50 easy images with 1–3 large objects from LVIS — real-world performance on complex cluttered scenes with many small objects is untested and likely significantly lower
- Veo 3 benchmarked on a green-background segmentation prompt that outperforms white background by 8pp — revealing that model performance is sensitive to visual prompt choices that exploit training data distribution artifacts (e.g. chroma key)

## Bottlenecks

- Video generation inference cost — producing an 8-second 720p video per task invocation — blocks practical deployment of generalist video models as drop-in replacements for specialized computer vision models
- Absence of automatic task-completion detection and frame selection in video models — the optimal output frame is unknown a priori, requiring either human review or an external verifier to extract usable results
- Systematic geometric transformation blindspot (reflection, rotation) in current video models blocks reliable abstract visual analogy solving and spatial reasoning benchmarks requiring these transformations

## Breakthroughs

- Veo 3 demonstrates that large-scale video generation models trained with a simple generative objective on web-scale data develop emergent zero-shot capabilities spanning the full vision stack — perception, intuitive physics modeling, image manipulation, and early-stage visual reasoning — without any
- Chain-of-frames (CoF) is identified and demonstrated as a visual analog to chain-of-thought reasoning — frame-by-frame video generation enables step-by-step visual problem solving across time and space without symbolic representations

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/generative_media|generative_media]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/video_and_world_models|video_and_world_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/veo-2|Veo 2]]
- [[entities/passk|pass@k]]
