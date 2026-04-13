---
type: source
title: 'Movie Gen: A Cast of Media Foundation Models'
source_id: 01KJV79X7AQ5A1HM6FJ7H94JEY
source_type: paper
authors:
- Adam Polyak
- Amit Zohar
- Andrew Brown
- Andros Tjandra
- Animesh Sinha
- Ann Lee
- Apoorv Vyas
- Bowen Shi
- Chih-Yao Ma
- Ching-Yao Chuang
- David Yan
- Dhruv Choudhary
- Dingkang Wang
- Geet Sethi
- Guan Pang
- Haoyu Ma
- Ishan Misra
- Ji Hou
- Jialiang Wang
- Kiran Jagadeesh
- Kunpeng Li
- Luxin Zhang
- Mannat Singh
- Mary Williamson
- Matt Le
- Matthew Yu
- Mitesh Kumar Singh
- Peizhao Zhang
- Peter Vajda
- Quentin Duval
- Rohit Girdhar
- Roshan Sumbaly
- Sai Saketh Rambhatla
- Sam Tsai
- Samaneh Azadi
- Samyak Datta
- Sanyuan Chen
- Sean Bell
- Sharadh Ramaswamy
- Shelly Sheynin
- Siddharth Bhattacharya
- Simran Motwani
- Tao Xu
- Tianhe Li
- Tingbo Hou
- Wei-Ning Hsu
- Xi Yin
- Xiaoliang Dai
- Yaniv Taigman
- Yaqiao Luo
- Yen-Cheng Liu
- Yi-Chiao Wu
- Yue Zhao
- Yuval Kirstain
- Zecheng He
- Zijian He
- Albert Pumarola
- Ali Thabet
- Artsiom Sanakoyeu
- Arun Mallya
- Baishan Guo
- Boris Araya
- Breena Kerr
- Carleigh Wood
- Ce Liu
- Cen Peng
- Dimitry Vengertsev
- Edgar Schonfeld
- Elliot Blanchard
- Felix Juefei-Xu
- Fraylie Nord
- Jeff Liang
- John Hoffman
- Jonas Kohler
- Kaolin Fire
- Karthik Sivakumar
- Lawrence Chen
- Licheng Yu
- Luya Gao
- Markos Georgopoulos
- Rashel Moritz
- Sara K. Sampson
- Shikai Li
- Simone Parmeggiani
- Steve Fine
- Tara Fowler
- Vladan Petrovic
- Yuming Du
published_at: '2024-10-17 00:00:00'
theme_ids:
- audio_and_speech_models
- creative_content_generation
- generative_media
- multimodal_models
- pretraining_and_scaling
- scaling_laws
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Movie Gen: A Cast of Media Foundation Models

Meta AI's Movie Gen introduces a unified family of large-scale media foundation models — a 30B-parameter text-to-video/image transformer and a 13B-parameter video-to-audio model — that collectively set new state-of-the-art benchmarks across video generation, personalization, instruction-based editing, and cinematic audio synthesis. The work's core contribution is demonstrating that a single scalable architecture trained with Flow Matching on internet-scale data can achieve simultaneous leadership across five distinct media generation tasks, while surfacing deep structural limitations around compute concentration, evaluation methodology, and the fundamental separateness of audio and video generation pipelines.

**Authors:** Adam Polyak, Amit Zohar, Andrew Brown, Andros Tjandra, Animesh Sinha, Ann Lee, Apoorv Vyas et al. (88 total)
**Published:** 2024-10-17
**Type:** Paper
**Source:** https://arxiv.org/pdf/2410.13720
**Themes:** [[themes/generative_media|Generative Media]], [[themes/video_and_world_models|Video & World Models]], [[themes/audio_and_speech_models|Audio & Speech Models]], [[themes/multimodal_models|Multimodal Models]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/scaling_laws|Scaling Laws]], [[themes/creative_content_generation|Creative Content Generation]]

---

## What This Paper Does

Movie Gen's thesis is architectural unification at scale: rather than building specialist systems for video synthesis, editing, personalization, and audio separately, a single transformer backbone — adapted from LLaMA3 and trained with Flow Matching — serves as the common substrate for all five tasks. The paper reports decisive state-of-the-art over Runway Gen3, LumaLabs, Sora, and Kling1.5 on video quality, and over all prior video-to-audio models on synchronization and correctness.

The claims are backed by large-scale human evaluation (automated metrics are explicitly rejected as unreliable), which itself becomes one of the paper's most significant meta-contributions: the acknowledgment that no valid automated metrics exist for video generation quality.

---

## Architecture

### Movie Gen Video (30B)

The model uses the LLaMA3 transformer architecture (48 layers, 6144 hidden dim, 48 heads, SwiGLU, RMSNorm) adapted for video generation with full bidirectional attention, cross-attention for text conditioning, and adaptive layer norm for flow-step conditioning. Ablations demonstrate this outperforms the standard Diffusion Transformer architecture by **+18.6% quality** and **+12.6% text alignment** — a result the paper treats as a significant architectural finding that displaces DiT as the default choice for video generation at scale.

**Temporal Autoencoder (TAE):** 8× spatiotemporal compression across all three dimensions (T, H, W) using 2.5D convolutions (2D spatial + 1D temporal), producing 16-channel latents. A custom Outlier Penalty Loss (OPL) eliminates high-norm "latent dot" artifacts by penalizing latent values beyond 3 standard deviations from the mean — a failure mode that standard VAE training objectives produce and that required a non-obvious fix.

**Text conditioning:** Three complementary encoders combined — UL2 (text reasoning), Long-prompt MetaCLIP finetuned to 256-token length (visual-language alignment), and ByT5 (character-level, for visual text generation) — projected and concatenated to 6144 dimensions.

**Spatial Upsampler:** A separate 7B model performs 2× super-resolution from 768px to 1080p HD using Flow Matching, with MultiDiffusion ensuring temporal consistency across sliding windows during inference.

**Inference speedup:** A linear-quadratic timestep schedule achieves ~20× reduction in diffusion steps (50 steps emulating 250-step quality) through an inference-only optimization requiring only a few lines of code, with no retraining.

### Movie Gen Audio (13B)

A DiT-based model with 36 layers and attention/feed-forward dimensions of 4608/18432. Operates on latents from a custom **DAC-VAE** that removes residual vector quantization, achieving 3× lower frame rate (75Hz→25Hz) and 2× higher audio fidelity (24kHz→48kHz) over Encodec — the improvement comes from eliminating codec information loss that degrades quality in token-based generation.

The model jointly generates diegetic ambient sound, Foley sound effects, and non-diegetic instrumental music from video and optional text prompts. A single model supports generation, bidirectional extension, and infilling — the same architecture handles all three via masked audio prediction.

---

## Training

### Data & Curation

Video captions are generated by finetuned **LLaMA3-Video** (8B and 70B) models, preferred by human raters 67% over frame-based captioning. Video captions improve motion alignment by +10.7% and high-motion prompt alignment by +16.1%.

Three-stage filtering pipeline: visual (resolution, aesthetics, borders) → motion (static detection, VMAF, jitter) → content (deduplication via copy-detection embeddings, inverse-square-root resampling by cluster size). The final landscape mix targets 60% landscape / 40% portrait, though the data imbalance likely depresses portrait video quality.

### Curriculum

Multi-stage training: T2I warmup at 256px (1536 GPUs) → joint T2I/V at 256px (6144 GPUs, ~395M video samples) → joint T2I/V at 768px → supervised finetuning on curated high-quality videos → model averaging across SFT checkpoints.

**Training objective:** Flow Matching with optimal transport paths and logit-normal timestep sampling consistently outperforms v-prediction diffusion with zero-terminal SNR across all model sizes.

### Scaling Laws

A notable finding: **LLM compute-optimal scaling laws transfer accurately to video generation**. Compute-optimal model sizes for Movie Gen Video align closely with LLaMA3 predictions across the 5B–30B range, enabling LLM cost-performance intuitions to be applied to video model development — an unexpected cross-domain transfer.

The audio model scales consistently from 300M to 13B parameters across all metrics: quality win rate +29.9% (3B vs 300M), +34.6% (9B vs 3B), CLAP score improving from 0.23 to 0.38.

---

## Post-Training Specializations

### Personalization (PT2V)

Extends Movie Gen Video by encoding a masked face image through a trainable Long-prompt MetaCLIP vision encoder and concatenating identity features with text embeddings. Three-stage curriculum:

1. Short video identity injection
2. Long video recovery
3. Cross-paired training (reference image from a *different* video of the same person)

**The core tension:** Training on paired data (reference from same video) causes copy-paste overfitting — the model replicates reference pose and expression rather than generating diverse motion. Cross-paired training resolves this but creates a **fundamental identity-naturalness trade-off**: improving motion naturalness (+26.14%) and text alignment (+27.36%) consistently reduces identity similarity scores. No solution is offered; the paper records this as an open constraint.

Personalization is **limited to human subjects** with no demonstrated generalization to objects, animals, or non-human characters.

### Video Editing (Movie Gen Edit)

Three-stage progressive training requiring **zero supervised video editing data**:

- **Stage I:** Multitask image editing + T2V with randomly sampled temporal positional embeddings
- **Stage II:** Animated frame editing (affine-augmented synthetic videos) + generative instruction-guided video segmentation (SAM2 + DINO)
- **Stage III:** Backtranslation (generate edited video → re-caption → use as training pair)

The backtranslation technique — adapted from NLP — is the critical insight: it bootstraps training data from the model's own generations, removing the fundamental barrier of supervised data scarcity. Results: human annotators prefer Movie Gen Edit **74% of the time** over prior state-of-the-art EVE.

The prior state-of-the-art EVE's Factorized Diffusion Distillation is **an order of magnitude more memory-intensive** than Movie Gen's approach, making EVE effectively unscalable to large base models.

---

## Capabilities

| Capability | Maturity | Key Evidence |
|---|---|---|
| 1080p HD text-to-video up to 16s with synchronized audio | demo | State-of-the-art over Sora, Gen3, LumaLabs, Kling1.5 |
| Physics-aware video generation (motion, geometry, causality) | demo | Learned from internet-scale video pre-training |
| Identity-preserving personalized video from single face image | demo | Outperforms all baselines on identity/quality/alignment |
| Instruction-based video editing without supervised data | demo | 74% human preference over EVE |
| 48kHz cinematic audio (SFX + music) synchronized to video | demo | 33.8–72.8% better synchronization vs. all baselines |
| Long-form audio via multi-diffusion extension | demo | Quality on par with or better than one-shot generation |
| Bidirectional audio infilling and extension | demo | Single model handles all three generation modes |
| Text-to-image generation (highest ELO vs. Flux, DALL-E 3, MJ v6.1) | demo | Joint image-video training benefits both modalities |
| ~20x inference speedup via linear-quadratic timestep schedule | demo | Training-free, inference-only optimization |
| 6,144 H100 GPU training with combined FSDP/tensor/sequence/context parallelism | narrow\_production | Meta infrastructure only |

---

## Limitations

### Fundamental Capability Gaps

**No speech or voice generation.** Movie Gen Audio explicitly excludes diegetic speech (dialogue, narration) and vocal music — a major gap for any video production workflow requiring voice acting. The paper identifies transcript-free speech synthesis as unsolved and notes that generated video artifacts compound the difficulty of audio-visual lip synchronization.

**No joint audio-video generation.** Video and audio models are trained entirely separately. Temporal coherence between visual content and sound relies on post-hoc conditioning rather than co-generation. The paper explicitly identifies joint audio-video generation as important future work.

**Maximum 16-second video length.** The 73K token context window cap prevents single-pass generation of longer videos. The extension approach introduces coherence risks at chunk boundaries.

**English-only.** All text conditioning is English-language, blocking multilingual deployment.

**Human subjects only for personalization.** No demonstrated generalization beyond human faces.

### Evaluation Infrastructure Failures

The paper makes a pointed critique of the field's measurement apparatus:

- **No valid automated metrics for video quality:** FVD, IS, and CLIP-based metrics do not correlate with human perceptual judgments. Every model development decision requires expensive large-scale human evaluation.
- **No valid automated metrics for video-conditioned audio:** FAD/KLD require reference audio unavailable for generated video; ImageBind is systematically biased against non-diegetic music.
- **VGGSound benchmark contamination:** The primary public benchmark for video-to-audio contains pervasive training/evaluation duplicates, making published results unreliable for cross-model comparison.
- **TGVE+ benchmark is obsolete:** Tests video editing on 480×480px, 3–8 second, square, 10–16 FPS videos that do not reflect real production conditions.

### Compute Concentration

Training requires **up to 6,144 H100 GPUs at 700W each** — infrastructure accessible only to a handful of organizations globally. The paper contains no discussion of distillation, efficient training, or accessibility paths for the research community. Frontier video generation capability is functionally concentrated at hyperscalers.

The audio model alone requires 384 GPUs for 14 days of pre-training.

### Architectural Trade-offs

Full bidirectional attention foregoes the ~2× computational efficiency of causal masking available to autoregressive LLMs and is incompatible with Grouped Query Attention — making context parallelism ~8× less communication-efficient than for GQA-based LLMs.

Training speed scales as approximately O(T²) in latent frames, making long-video training computationally prohibitive and forcing multi-stage curriculum that may introduce distribution mismatch.

### Quality Ceilings and Failure Modes

- **Motion completeness trade-off:** Movie Gen Video loses significantly to Kling1.5 on motion completeness (–10.04%) while winning on frame consistency (+13.5%). The model is conservative toward static or camera-only motion when uncertain.
- **Out-of-distribution subjects** (monsters, ghosts, unusual activities) produce insufficient motion.
- **Excessively detailed motion descriptions** introduce visual artifacts.
- **Dense or subtle motions** (tap dance, footsteps) cause audio desynchronization.
- **Diegetic on-screen music** (e.g., matching guitar chord fingering) is significantly harder than ambient sound.
- **TAE reconstruction** degrades for high-frequency spatial detail + fast motion combinations.
- **Portrait video quality** likely inferior due to 80/20 landscape/portrait data imbalance in fine-tuning.
- **Backtranslation** slightly degrades text faithfulness versus standard fine-tuning (semantic drift between original and backtranslated instructions).

---

## Open Bottlenecks

| Bottleneck | Horizon | Status |
|---|---|---|
| No reliable automated metrics for video generation quality | possibly fundamental | Blocking rapid iteration; forces human evaluation for every decision |
| No reliable automated metrics for video-conditioned audio | 1–2 years | FAD/KLD/ImageBind all invalid; benchmark contamination |
| Transcript-free diegetic speech generation | 1–2 years | Unsolved; blocks end-to-end cinematic production |
| Joint audio-video generation | 1–2 years | Separate training pipelines; no co-generation |
| General personalized video generation | 1–2 years | Identity-naturalness trade-off unresolved |
| Long-form video generation (>16s) | 1–2 years | Context window and memory constraints |
| Supervised video editing data scarcity | 1–2 years | Partially addressed by backtranslation; not eliminated |
| Cinematic audio training data scarcity | 1–2 years | Public datasets are amateur-only |
| Fine-grained audio-visual temporal alignment | 1–2 years | Fails on dense/subtle motions |
| Quadratic attention scaling with video length | 1–2 years | Blocks efficient long-form video training |
| Frontier training compute concentration | 3–5 years | 6,144 H100 GPUs inaccessible to research community |
| Visual/linguistic bias in training data | 3–5 years | Not addressable through current curation methods |

---

## Key Methodological Contributions

**Backtranslation for video editing** is the most transferable technique in the paper: generating synthetic training data by having the model edit videos and re-captioning the results bootstraps instruction-following without any supervised pairs. The NLP origin of this technique illustrates the continuing value of cross-modal technique transfer.

**Outlier Penalty Loss (OPL)** for suppressing VAE latent artifacts is a practical fix for a failure mode (high-norm "latent dot" artifacts) that emerges specifically with video temporal autoencoders and isn't addressed by standard VAE training objectives.

**Linear-quadratic inference scheduling** demonstrates that inference-time algorithmic improvements can yield ~20× speedups without any model changes — an underexplored axis relative to architectural and data scaling.

**LLaMA3 architecture transfer to video generation** — and the discovery that LLM scaling laws predict compute-optimal model sizes in the video domain — suggests that video generation modeling is converging toward the same infrastructure and intuitions as language modeling, with implications for how the field should invest in architecture research.

---

## Broader Significance

Movie Gen is notable less for any single technical breakthrough than for the breadth and rigor of its systems integration. It simultaneously resolves several previously separate research directions (video generation, audio generation, editing, personalization) under a common architectural framework while being unusually candid about what remains unsolved.

The paper's most significant long-term contribution may be its documentation of the measurement crisis in video generation: the absence of valid automated metrics creates a fundamental asymmetry where progress is expensive to measure, cherry-picking is structurally encouraged, and the research community cannot efficiently distinguish genuine improvements from presentation artifacts. Until this is resolved, claims of state-of-the-art in video generation — including Movie Gen's own — carry substantial epistemic uncertainty.

The compute concentration implications are equally significant. At 6,144 H100 GPUs for a single training run, frontier video generation capability is not merely expensive — it is structurally inaccessible to the broader research community in a way that text model training at comparable capability levels is not.

## Key Concepts

- [[entities/classifier-free-guidance-cfg|Classifier-Free Guidance (CFG)]]
- [[entities/diffusion-transformer|Diffusion Transformer]]
- [[entities/diffusion-transformer-dit|Diffusion Transformer (DiT)]]
- [[entities/fvd|FVD]]
- [[entities/flow-matching|Flow Matching]]
- [[entities/sequence-parallelism|Sequence Parallelism]]
- [[entities/tensor-parallelism|Tensor Parallelism]]
- [[entities/context-parallelism|context parallelism]]
