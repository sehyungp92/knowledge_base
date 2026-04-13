---
type: source
title: 'AdaWorld: Learning Adaptable World Models with Latent Actions'
source_id: 01KKT4WS4TX57SJ2WT5PC0AME8
source_type: paper
authors:
- Shenyuan Gao
- Siyuan Zhou
- Yilun Du
- Jun Zhang
- Chuang Gan
published_at: '2025-03-24 00:00:00'
theme_ids:
- finetuning_and_distillation
- generative_media
- post_training_methods
- robotics_and_embodied_ai
- robot_learning
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AdaWorld: Learning Adaptable World Models with Latent Actions

**Authors:** Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, Chuang Gan
**Published:** 2025-03-24 00:00:00
**Type:** paper

## Analysis

# AdaWorld: Learning Adaptable World Models with Latent Actions
2025-03-24 · paper · Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, Chuang Gan
https://arxiv.org/pdf/2503.18938

---

### Motivation & Prior Limitations
- Most existing world models require substantial action-labeled data and expensive training to acquire precise action controllability, making them brittle when adapting to novel environments with heterogeneous action spaces.
  - Defining a unified action format across diverse environments is fundamentally infeasible, and current methods require costly retraining for each new action specification.
  - Pseudo-labeling approaches (e.g., Baker et al., 2022; Zhang et al., 2022) can annotate videos, but scale poorly across the breadth of environments an intelligent agent might encounter.
- The dominant pretraining paradigm uses action-agnostic video prediction, which leaves the world model without any internalized notion of action structure, forcing it to learn action semantics from scratch during expensive downstream finetuning.
  - Methods like iVideoGPT (Wu et al., 2024) and DIAMOND (Agarwal et al., 2025) initialize from pretrained video models but still depend on large quantities of action-labeled interactions to achieve controllability in new environments.
- No prior work established a transferable, context-invariant action representation that could be extracted from unlabeled video and reused across environments without further training — the gap between human-like action transfer and machine world models remained wide.

---

### Proposed Approach
- AdaWorld introduces action-aware pretraining: rather than treating videos as purely action-agnostic sequences, it extracts latent actions from unlabeled video in a self-supervised manner and conditions a world model on these latent actions during pretraining, giving the model a prior over action structure before any environment-specific finetuning.
  - This contrasts with prior work that adds action conditioning only at finetuning time (e.g., iVideoGPT), and with Genie (Bruce et al., 2024), which uses discrete VQ-VAE codes focused on playability rather than transferable representations.
- The core component is a **latent action autoencoder** built on a spatiotemporal Transformer. The encoder takes two consecutive frames and compresses their transition into a compact continuous latent vector (the "latent action") via a β-VAE objective; the decoder then reconstructs the subsequent frame from the latent action and the preceding frame alone. The information bottleneck forces the latent action to capture only the dominant inter-frame transition — disentangling action from scene context.
  - The β hyperparameter explicitly controls the expressiveness-vs-disentanglement trade-off: lower β yields more discriminative but context-entangled codes; the authors set β = 2×10⁻⁴ by default based on UMAP cluster analysis across Habitat, Minecraft, and DMLab.
  - Continuous latent space (vs. discrete VQ codes) enables action composition by linear interpolation and averaging of latent embeddings, a capability not available in prior discrete-action world models.
- The **autoregressive world model** is initialized from Stable Video Diffusion (SVD, Blattmann et al., 2023) and modified to denoise one frame at a time rather than a full clip, conditioned on the latent action concatenated with the timestep and CLIP image embeddings. Up to 6 historical frames are encoded and concatenated with the noise latent to preserve temporal context; noise augmentation on historical frames during training mitigates long-term drift.
- Adaptation to a new environment with discrete actions requires collecting only ~100 samples per action, averaging their extracted latent actions to initialize control embeddings, and finetuning for ~800 steps. For continuous action spaces, a lightweight two-layer MLP maps raw action inputs to the latent action interface, trainable in under 30 seconds on a single GPU.
- Pretraining uses approximately 2 billion frames drawn from 1016 Gym Retro and Procgen environments plus EPIC-Kitchens (Goyal et al., 2017), Ego4D (Grauman et al., 2022), Open X-Embodiment (O'Neill et al., 2024), and RoboVQA (Ju et al., 2024), spanning ego, third-person, game, and real-world robot perspectives.

---

### Results & Capabilities
- On action transfer (zero-shot replication of demonstrated actions in new contexts), AdaWorld achieves FVD of 767.0 and ECS of 0.804 on LIBERO and FVD of 473.4 and ECS of 0.639 on SSv2, compared to the next-best baseline (optical flow conditioning) at FVD 1409.5 / ECS 0.724 on LIBERO and FVD 702.8 / ECS 0.611 on SSv2 — roughly a 2× FVD improvement.
  - In human evaluation on 50 video pairs per dataset, 70.5% of AdaWorld transfers were judged successful on LIBERO and 61.5% on SSv2, versus 2% and 10.5% respectively for optical flow conditioning.
- After 800 finetuning steps on 100 samples per action, AdaWorld achieves the best simulation fidelity across all four held-out environments: PSNR 23.58 / LPIPS 0.327 (Habitat), 21.59 / 0.457 (Minecraft), 22.92 / 0.335 (DMLab), and 21.60 / 0.436 (nuScenes), outperforming the action-agnostic baseline by 3+ dB PSNR in most settings.
  - All action-aware pretraining variants significantly outperform the action-agnostic baseline, confirming that the benefit arises from the pretraining paradigm rather than model architecture alone.
- In visual planning on Procgen game environments using MPC/CEM, AdaWorld (with finetuning) achieves a 56.67% average success rate across Heist, Jumper, Maze, and CaveFlyer, compared to 26.00% for the action-agnostic baseline and 27.17% for Q-learning. Even without finetuning — using only averaged latent action embeddings — AdaWorld achieves 44.83%, still outperforming the finetuned action-agnostic model.
  - The Oracle (ground-truth simulator for MPC) achieves 80.67%, indicating AdaWorld closes a substantial fraction of the gap between learned and ground-truth simulators

## Key Claims

1. AdaWorld incorporates action information during pretraining by extracting latent actions from videos in a self-supervised manner, enabling efficient adaptation to new environments.
2. Recent world models are typically initialized from pretrained video models.
3. Defining a unified action format for general environments is challenging, causing existing methods to require costly retraining when adapting to new environments with varying action specifications.
4. AdaWorld can transfer a demonstrated action to various contexts without further training, given one demonstration video.
5. AdaWorld can be efficiently adapted into specialized world models with raw action inputs via minor interactions and finetuning.
6. The latent action autoencoder uses an information bottleneck design with a Transformer architecture to extract compact, context-invariant action representations from pairs of consecutive frames.
7. The latent action autoencoder uses a spatiotemporal Transformer with interleaved spatial and temporal attention modules to encode temporal dynamics between two input frames.
8. The world model component of AdaWorld is initialized from Stable Video Diffusion (SVD) and uses diffusion-based next-frame prediction conditioned on latent actions.
9. AdaWorld supports frame-level control rather than video-clip-level prediction, offering finer granularity for interaction.
10. For discrete action environments, averaged latent action embeddings consistently represent the intended action, enabling efficient initialization of specialized world models.

## Capabilities

- Self-supervised latent action extraction from unlabeled videos using an information bottleneck VAE, producing context-invariant action representations transferable across environments
- Zero-shot action transfer from a demonstration video to novel contexts without any additional training or finetuning
- Efficient world model adaptation to new environments with as few as 100 interaction samples per action and 800 finetuning steps, outperforming action-agnostic pretraining baselines
- Action composition by averaging latent action vectors in continuous space, producing semantically meaningful composite actions (e.g., 'jump' + 'right' = 'jump right')
- World model-based visual planning via MPC (cross-entropy method and MPPI) achieving 56.67% average success rate in game environments, substantially outperforming Q-learning (27.17%) under the same interaction budget
- Cross-domain generalization of action representations: latent actions trained on real-world robot videos (OpenX) improve performance on unseen 2D virtual game environments (Procgen)

## Limitations

- AdaWorld does not operate at real-time frequency, making it unsuitable for interactive applications requiring low-latency response
- World model cannot generate novel content beyond the initial scene context when rollout extends beyond observed frames, limiting open-ended imagination
- Model fails to maintain coherence in extremely long-term rollouts, with quality degrading over extended autoregressive chains
- Requires 2000 million frames of pretraining data across 1016+ environments for strong generalization, representing massive scale and compute requirements not accessible to most practitioners
- Success rates on fine-grained robot manipulation tasks remain very low (5-30% range), suggesting substantial gap between game-like environments and dexterous physical control
- No evaluation on real physical robot hardware — all robot experiments conducted in simulation (Robosuite, RoboDesk), leaving sim-to-real transfer gap unaddressed
- Substantial gap remains between AdaWorld and oracle (ground truth simulator) performance: 56.67% vs 80.67% average success rate in game planning, indicating world model fidelity as a planning ceiling
- Latent action disentanglement is imperfect — noise exists in action representations when actions cannot be executed in certain states, undermining context-invariance assumptions
- Sensitive hyperparameter β controls the tradeoff between expressiveness and disentanglement; reducing β improves differentiation but destroys cross-environment action invariance, suggesting no principled automatic setting exists
- Approach assumes agents' actions drive dominant visual variation, which may fail in passive observation scenarios, multi-agent environments with complex background dynamics, or environments with decoupled agent-observation frames

## Bottlenecks

- World models require substantial action-labeled data and costly retraining to adapt to new environments with different action specifications — blocking scalable deployment across heterogeneous domains
- Diffusion-based world model inference is too slow for real-time interactive applications (games, robotics), blocking deployment in latency-sensitive settings
- Autoregressive world models cannot maintain coherence in very long rollouts, blocking use in long-horizon planning and persistent simulation tasks

## Breakthroughs

- AdaWorld demonstrates that pretraining world models with self-supervised latent actions extracted from unlabeled video enables zero-shot and few-shot adaptation to new environments — fundamentally reducing the action label bottleneck for world model transfer

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/generative_media|generative_media]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/fréchet-video-distance|Fréchet Video Distance]]
- [[entities/libero|LIBERO]]
- [[entities/lpips|LPIPS]]
- [[entities/model-predictive-control|Model Predictive Control]]
- [[entities/psnr|PSNR]]
- [[entities/vq-vae|VQ-VAE]]
