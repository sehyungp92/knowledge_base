---
type: source
title: 'Genie: Generative Interactive Environments'
source_id: 01KJVB7Y3J05KH3VMSWQMDBNAD
source_type: paper
authors:
- Jake Bruce
- Michael Dennis
- Ashley Edwards
- Jack Parker-Holder
- Yuge Shi
- Edward Hughes
- Matthew Lai
- Aditi Mavalankar
- Richie Steigerwald
- Chris Apps
- Yusuf Aytar
- Sarah Bechtle
- Feryal Behbahani
- Stephanie Chan
- Nicolas Heess
- Lucy Gonzalez
- Simon Osindero
- Sherjil Ozair
- Scott Reed
- Jingwei Zhang
- Konrad Zolna
- Jeff Clune
- Nando de Freitas
- Satinder Singh
- Tim Rocktäschel
published_at: '2024-02-23 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- generative_media
- robotics_and_embodied_ai
- robot_learning
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Genie: Generative Interactive Environments

**Authors:** Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, Tim Rocktäschel
**Published:** 2024-02-23 00:00:00
**Type:** paper

## Analysis

# Genie: Generative Interactive Environments
2024-02-23 · paper · Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi et al. (25 total)
https://arxiv.org/pdf/2402.15391v1

---

### Motivation & Prior Limitations
- Existing world models require action-labeled training data, making them fundamentally dependent on costly domain-specific annotation and limiting their ability to exploit the vast corpus of unlabelled Internet video.
  - Prior approaches such as GAIA-1 and UniSim require both text and action labels for training, constraining the scale and diversity of usable data.
  - Playable Video Generation (PVG) works that do use latent actions are limited to domain-specific static examples and cannot generalize to new environments via prompting.
- Video generation models, while increasingly capable, operate at the video level and lack frame-level action controllability, leaving a large gap between passive video generation and interactive experience.
  - There is no mechanism in standard video models for a user or agent to steer generation step-by-step, making them unsuitable as interactive environments or simulation substrates for RL.
- The lack of rich, diverse, scalable training environments is one of the key bottlenecks for reinforcement learning research, and existing world model approaches cannot leverage unlabelled video at Internet scale to address this.

---

### Proposed Approach
- Genie is an 11B-parameter foundation world model trained entirely from unlabelled Internet video that learns a discrete latent action space in a fully unsupervised manner, enabling frame-by-frame interactive control at inference time without any ground-truth action annotations.
  - Unlike prior world models, Genie requires only raw video at training time; it infers latent actions implicitly by learning what information between consecutive frames is most predictive of future frames.
- The architecture consists of three components trained in two phases: (1) a spatiotemporal video tokenizer (ST-ViViT, VQ-VAE-based) that compresses frames into discrete tokens while preserving temporal dynamics; (2) a Latent Action Model (LAM) that infers a discrete latent action between each frame pair using a VQ codebook of size |A|=8; and (3) a MaskGIT-based autoregressive dynamics model that predicts the next frame tokens conditioned on past tokens and the latent action embedding.
  - The LAM is trained with a VQ-VAE objective where an encoder sees both past and future frames and a decoder must reconstruct the future frame from only the history and the quantized latent action — the information bottleneck forces the latent code to capture the most meaningful inter-frame change. The entire LAM except its VQ codebook is discarded at inference time.
  - The ST-transformer architecture used throughout interleaves spatial attention (over H×W tokens within a timestep) and temporal attention (over T timesteps per spatial position), making the dominant computational cost scale linearly rather than quadratically in the number of frames — a critical efficiency gain over alternatives like C-ViViT.
- At inference, users or agents select a discrete latent action (an integer in [0, 8)) at each step, which is looked up in the VQ codebook and added as an embedding to the dynamics model to autoregressively generate the next frame, enabling interactive play from any image prompt.
- To demonstrate cross-domain generality, a 2.5B-parameter variant is trained on the RT1 robotics dataset using identical hyperparameters, treating all robot demonstration videos as action-free.

---

### Results & Capabilities
- The 11B Genie model trained on 30,000 hours of 2D platformer gameplay videos generalizes robustly to out-of-distribution image prompts — including Imagen2-generated images, hand-drawn sketches, and real-world photographs — producing interactive environments with consistent game-like behaviour and character movement.
  - This OOD generalization would not have been feasible with action-annotated training, which would have constrained the data diversity.
- Scaling analysis across model sizes from 40M to 2.7B parameters and batch sizes from 128 to 448 shows consistent, smooth improvements in training loss, confirming the approach scales gracefully; the final 11B model is trained on 942B tokens using 256 TPUv5p chips for 125k steps.
- The ST-ViViT tokenizer outperforms both spatial-only ViT (FVD 114.5 → 81.4) and C-ViViT (FVD 272.7 → 81.4) while using significantly less memory than C-ViViT (0.9GB vs. 1.6GB at matched parameter count), with C-ViViT showing overfitting tendencies despite higher memory cost.
- Pixel-input to the LAM produces superior controllability (ΔtPSNR 1.91 vs. 1.33 on Platformers; 2.07 vs. 1.65 on Robotics) compared to token-input, indicating that tokenization discards fine-grained motion information relevant to action inference.
- Latent actions learned from Internet videos transfer to unseen RL environments: a LAM-labelled behavioural cloning policy matches an oracle BC agent (which has access to ground-truth actions) on CoinRun with as few as 200 expert samples for latent-to-real-action mapping, despite almost certainly never having seen CoinRun during pretraining.
- The robotics-trained model (FVD 82.7 on the RT1 test split) learns semantically meaningful and consistent latent actions — corresponding to directions such as up, down, and left — purely from video, and captures object deformation and interaction dynamics without any action labels.
- Emergent physical understanding is observed, including parallax emulation (foreground moving faster than background) and deformable object simulation (e.g., chip bags), suggesting the model develops implicit 3D scene and physics representations from 2D video alone.

---

### Implications
- Genie establishes that interactive world models with frame-level controllability can be learned at scale from raw Internet video, removing the action-annotation bottleneck

## Key Claims

1. Genie is the first generative interactive environment trained in an unsupervised manner from unlabelled Internet videos.
2. Genie at 11B parameters can be considered a foundation world model.
3. Genie enables frame-by-frame action control in generated environments without any ground-truth action labels during training.
4. Genie's learned latent action space facilitates training agents to imitate behaviors from unseen videos.
5. Genie was trained on over 200,000 hours of publicly available Internet gaming videos.
6. The Platformers training dataset contains 6.8M 16-second video clips totaling 30,000 hours, filtered from 55M clips.
7. Genie is comprised of three components: a spatiotemporal video tokenizer, an autoregressive dynamics model, and a latent action model.
8. The Latent Action Model learns discrete latent actions in a fully unsupervised manner using a VQ-VAE-based objective.
9. The latent action vocabulary is limited to 8 discrete codes to permit human playability and enforce controllability.
10. The entire LAM (except the VQ codebook) is discarded at inference time and replaced with user-provided actions.

## Capabilities

- Generative interactive environment trained entirely from unlabelled internet video, enabling frame-by-frame action-controllable world generation from text, images, sketches, or photos without any ground-truth action labels
- Unsupervised latent action discovery from raw video pairs — a VQ-VAE-based latent action model learns a discrete action codebook (8 codes) from video without any action annotation, producing consistent and semantically meaningful latent actions that transfer across environments
- Out-of-distribution image prompting for interactive world generation — Genie generalises to text-to-image generated images, hand-drawn sketches, and real-world photographs as starting frames, producing game-like interactive behaviour from inputs visually distinct from training data
- Policy learning via latent action imitation from internet videos — a frozen LAM labels expert videos with latent actions, and a small adapter (200 expert samples) maps latent to real actions, achieving oracle-level behavioral cloning performance on unseen RL environments
- Emergent physics understanding from video — Genie learns parallax depth layering and deformable object dynamics (e.g., bags of chips) purely from 2D platformer video, without explicit physics supervision
- Foundation world model for robotics trained from action-free demonstration video — a 2.5B model trained on RT1 robot video (no action labels) learns distinct, consistent, semantically meaningful latent actions including directional movements and object interactions
- Efficient spatiotemporal video transformer (ST-ViViT) that scales linearly with frame count rather than quadratically, enabling tractable training on long video sequences with up to O(10^4) tokens

## Limitations

- Inference runs at approximately 1 FPS, making real-time interactive use completely impractical — orders of magnitude too slow for playable game-speed interaction or live agent training loops
- Memory is capped at 16 frames (1.6 seconds at 10 FPS), preventing long-horizon coherence and making sustained environment consistency across extended interactions impossible
- Hallucination of physically unrealistic future frames — as an autoregressive model, Genie can generate frame sequences that violate physical consistency or game logic
- Training limited to 2D platformer games at 160x90 resolution — the flagship 11B model is trained exclusively on this narrow domain; robotics is a separate smaller model, raising generality questions for the main system
- Low training resolution (160×90) constrains perceptual richness; higher resolution output requires a separately trained, larger decoder not reported in the main model metrics
- Latent action space is restricted to only 8 discrete codes — this small vocabulary may fail to capture the full diversity and granularity of actions in complex or non-platformer environments
- Policy transfer from latent to real actions still requires a small paired action dataset — the system is not fully unsupervised end-to-end for downstream agent deployment
- Latent action semantics are opaque and inconsistent at first use — users cannot predict which of the 8 codes maps to which behaviour before trying them, limiting controllability for new environments
- Training requires massive compute (256 TPUv5p for 125k steps at 11B parameters, trained on 942B tokens), making reproduction or extension inaccessible to the broader research community
- Model weights and training data are withheld from public release, blocking community-driven research, safety auditing, and reproducibility verification
- No quantitative evaluation of long-horizon consistency — all metrics (FVD, ΔPSNR) measure short-window quality; degradation behaviour over sequences longer than 16 frames is uncharacterised
- No evaluation of safety or potential for misuse of world generation (deepfakes, non-consensual content generation) despite the general-purpose nature of the model

## Bottlenecks

- Interactive world model inference speed is approximately 1 FPS — autoregressive frame generation at foundation scale (11B parameters, 25 MaskGIT steps per frame) is ~10-30x too slow for real-time human interaction or agent training loop integration
- Short temporal context window (16 frames / 1.6 seconds) in generative world models prevents coherent long-horizon environment simulation — agents cannot form plans or maintain consistent world state beyond a very brief window
- No scalable evaluation framework for interactive world model quality beyond short clips — existing metrics (FVD, PSNR) measure 4-16 frame windows and cannot capture long-horizon coherence, controllability consistency, or semantic correctness of generated environments

## Breakthroughs

- First demonstration that a foundation world model can be trained at scale from unlabelled internet video alone — without action annotations, text labels, or domain-specific data — while remaining frame-level controllable via learned latent actions

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/generative_media|generative_media]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/fréchet-video-distance|Fréchet Video Distance]]
- [[entities/genie|Genie]]
- [[entities/vq-vae|VQ-VAE]]
- [[entities/behavioral-cloning|behavioral cloning]]
