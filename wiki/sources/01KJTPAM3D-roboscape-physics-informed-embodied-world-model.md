---
type: source
title: 'RoboScape: Physics-informed Embodied World Model'
source_id: 01KJTPAM3DXFNX3FEHJJTZ73H3
source_type: paper
authors:
- Yu Shang
- Xin Zhang
- Yinzhou Tang
- Lei Jin
- Chen Gao
- Wei Wu
- Yong Li
published_at: '2025-06-29 00:00:00'
theme_ids:
- generative_media
- robotics_and_embodied_ai
- robot_learning
- spatial_and_3d_intelligence
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# RoboScape: Physics-informed Embodied World Model

**Authors:** Yu Shang, Xin Zhang, Yinzhou Tang, Lei Jin, Chen Gao, Wei Wu, Yong Li
**Published:** 2025-06-29 00:00:00
**Type:** paper

## Analysis

# RoboScape: Physics-informed Embodied World Model
2025-06-29 · paper · Yu Shang, Xin Zhang, Yinzhou Tang, Lei Jin, Chen Gao et al. (7 total)
https://arxiv.org/pdf/2506.23135

---

### Motivation & Prior Limitations
Current embodied world models are over-reliant on visual token fitting (RGB pixel prediction) without physical awareness, leading to unrealistic video generation in contact-rich robotic scenarios — particularly for deformable objects like cloth.
- Existing models fail to maintain motion plausibility and spatial consistency, producing artifacts such as unrealistic object morphing and discontinuous motion that compromise downstream policy learning.
  - IRASim and iVideoGPT, the representative embodied world model baselines, achieve LPIPS of 0.6674 and 0.4963 respectively vs. 0.1259 for RoboScape, and show poor long-horizon motion modeling.

Three prior approaches to injecting physical knowledge each carry disqualifying tradeoffs.
- Physics-prior regularization methods (e.g., local rigidity or rotational similarity on Gaussian Splatting features) are limited to narrow domains like human motion or rigid-body dynamics and do not generalize to diverse robotic scenes.
- Physics simulator-based knowledge distillation yields reliable priors but creates cascaded pipelines with excessive computational complexity, hindering practical deployment.
- Material field modeling methods are confined to object-level modeling and cannot be applied to scene-level generation.

Joint RGB-depth prediction explored in some contemporaneous world models remains coarse — learning at the whole-image level — and incurs a performance trade-off where 3D perception gains come at the cost of reduced RGB fidelity, without addressing fine-grained motion dynamics or object deformation critical for manipulation.

---

### Proposed Approach
RoboScape is a unified physics-informed embodied world model built on a dual-branch co-autoregressive Transformer (DCT) that jointly learns RGB video generation, temporal depth prediction, and adaptive keypoint dynamics tracking within a single multi-task learning framework, eliminating external cascaded models.

**Temporal Depth Prediction for Geometry Consistency.**
- Two parallel branches (FRGB and FDepth) share the same Spatial-Temporal Transformer (ST-Transformer) blocks using causal temporal attention and bidirectional spatial attention; depth branch features are injected additively into each RGB branch block via learned linear projections (`h_RGB^l = h_RGB^l + W^l(h_depth^l)`), providing hierarchical geometric constraints throughout generation.
- Unlike prior joint RGB-depth models that fuse at the image level, this hierarchical feature fusion propagates depth structure information into every transformer layer of the RGB branch.

**Adaptive Keypoint Dynamics Learning for Implicit Material Modeling.**
- SpatialTracker densely samples N₀ keypoints in the initial frame and tracks their trajectories; the top-K most active keypoints are selected by cumulative motion magnitude, automatically identifying contact-rich regions without requiring expensive segmentation masks.
- A temporal consistency loss enforces that predicted visual tokens at keypoint locations across frames remain aligned to their initial-frame tokens (`L_Keypoint`), implicitly encoding material properties (rigidity, elasticity) from motion behavior rather than explicit physical modeling.
- A keypoint-guided attention map up-weights cross-entropy loss in spatiotemporal regions intersected by high-motion keypoint trajectories (weight γ = 5), directing the model's learning capacity to the most physically dynamic regions.

**Data Pipeline.**
- The AGIBOT-World dataset is processed through a multi-stage pipeline: camera-boundary detection (TransNetV2), action-semantic slicing (InternVL), motion quality filtering (FlowNet), and clip categorization by action difficulty (three levels) and scene type — supporting curriculum learning from simpler to harder tasks.
- Depth pseudo-labels are generated with Video Depth Anything; keypoint trajectories with SpatialTracker — both are off-the-shelf, keeping the pipeline scalable.

---

### Results & Capabilities

**Video Generation Quality.**
RoboScape achieves state-of-the-art across all six evaluation metrics — appearance fidelity (LPIPS 0.1259, PSNR 21.85), geometric consistency (AbsRel 0.360, δ₁ 0.621, δ₂ 0.831), and action controllability (ΔPSNR 3.34) — outperforming all four baselines (IRASim, iVideoGPT, Genie, CogVideoX).
- Genie, the strongest general world model baseline, achieves LPIPS 0.1683 and PSNR 19.76 but has substantially inferior geometric consistency (AbsRel 0.443); CogVideoX generates high-quality video but cannot follow action commands (ΔPSNR not reported due to absence of action-conditioning capability).

Ablation confirms that the two physics components are complementary and non-redundant.
- Removing depth prediction degrades geometric consistency substantially (AbsRel rises from 0.360 to 0.392, δ₁ drops from 0.621 to 0.579) with negligible improvement to RGB metrics, while removing keypoint learning hurts action controllability most severely (ΔPSNR drops from 3.34 to 2.95) and visual fidelity.

**Robotic Policy Training with Synthetic Data.**
Diffusion Policy trained on 200 synthetic trajectories from RoboScape achieves 91% success on Robomimic Lift — matching real-data performance (92%) — while scaling synthetic data consistently improves success rates from 40% at 50 clips to 91% at 200 clips.
- On LIBERO (multi-object, cluttered, long-horizon tasks), π₀ augmented with 800 synthetic trajectories reaches 79.1% average success across spatial/object/goal subtasks, compared to 65.2% on real data alone (200 trajectories), demonstrating that RoboScape synthetic data surpasses equivalent real data for this regime.

**Policy Evaluation.**
RoboScape achieves Pearson correlation of 0.953 (R² = 0.908) between its predicted rollout success rates and ground-truth simu

## Key Claims

1. Current embodied world models exhibit limited physical awareness, particularly in modeling 3D geometry and motion dynamics, resulting in unrealistic video generation for contact-rich robotic scenarios
2. Existing embodied world models predominantly focus on video generation with training objectives centered on optimizing RGB pixels, failing to maintain crucial physical properties such as motion plausi
3. In robotic manipulation tasks involving deformable objects such as cloth, generated videos frequently contain artifacts such as unrealistic object morphing or discontinuous motion.
4. Physics-prior regularization methods are limited to narrow domains like human motion or rigid-body dynamics, hindering generalization to diverse robotic scenarios.
5. Material field modeling methods for physics integration are confined to object-level modeling and are hard to apply to scene-level generation.
6. RoboScape is a physics-informed world model that jointly learns RGB video generation and physics knowledge through two auxiliary tasks: temporal depth prediction and adaptive keypoint dynamics learnin
7. RoboScape uses a dual-branch co-autoregressive Transformer (DCT) for joint prediction of RGB and depth, where depth features are injected into the RGB branch via cross-branch interaction pathways to e
8. Physical material understanding can emerge from self-supervised tracking of contact-driven keypoint dynamics, eliminating the need for explicit material modeling.
9. The most informative keypoints for motion modeling are empirically characterized by large motion magnitudes, enabling adaptive keypoint selection without costly segmentation masks.
10. RoboScape outperforms all baselines across six evaluation metrics (LPIPS, PSNR, AbsRel, δ1, δ2, ΔPSNR), achieving LPIPS of 0.1259, PSNR of 21.8533, and ΔPSNR of 3.3435.

## Capabilities

- Physics-informed world model (RoboScape) generates synthetic robotic training data that approaches real-data performance parity: 91% success rate with 200 synthetic trajectories vs 92% with 200 real trajectories on Diffusion Policy / Robomimic Lift
- Physics-informed embodied world model serves as a reliable offline policy evaluator, achieving 0.953 Pearson correlation (R²=0.908) with ground-truth simulator outcomes — versus -0.134 and -0.195 for prior embodied world models
- Joint physics-informed training (temporal depth + keypoint dynamics) enables physically plausible generation of deformable object interactions (cloth, soft materials) in robotic manipulation videos, capturing material properties implicitly without explicit physics engines
- Automated robotic data processing pipeline with physical prior annotation (depth maps, keypoint trajectories, action difficulty ranking, scene categorisation) enabling curriculum-ordered training at scale from raw teleoperation video

## Limitations

- Current embodied world models (pre-RoboScape baselines) lack physical awareness in 3D geometry and motion dynamics, producing unrealistic artifacts in contact-rich scenarios such as unrealistic object morphing and discontinuous motion
- Physics simulator-based world model pipelines introduce excessive computational complexity, blocking practical deployment
- Physics regularization methods for video generation are limited to narrow domains (human motion, rigid-body dynamics), blocking generalisation to diverse robotic scenarios involving soft, deformable, or articulated objects
- Material field modelling approaches for video physics are confined to object-level and cannot scale to full scene-level generation — a hard architectural boundary
- RoboScape is evaluated exclusively on manipulation tasks; no evidence of capability in locomotion, navigation, or non-manipulation robotics domains — a controlled-conditions limitation
- Complex multi-step tasks (LIBERO suite) still require real data warm-up — the system cannot bootstrap from synthetic data alone for harder, long-horizon manipulation
- Training RoboScape requires 32 NVIDIA A800-80GB GPUs running for 24 hours — substantial compute cost that limits accessibility for most robotics research labs
- Adding keypoint dynamics learning degrades geometric consistency metrics: AbsRel worsens from 0.3417 (w/o keypoint) to 0.3600 (full model), and δ1 drops from 0.6497 to 0.6214 — a performance trade-off between motion fidelity and depth accuracy
- World model policy evaluation requires manual human judgment to determine success — there is no automated success detection when the policy interacts with the world model, creating a bottleneck for scalable offline evaluation
- Model is trained and evaluated solely on a single dataset (AgiBotWorld-Beta, 50K clips, 147 tasks, 72 skills) — cross-dataset and out-of-distribution generalisation is unvalidated
- No real-world robot deployment testing is reported — the entire experimental validation remains in simulation and benchmark settings; real-world sim-to-real gap is unexplored
- Generation horizon is limited to 16 frames sampled at 2Hz (~8 seconds); insufficient for long-horizon manipulation tasks that may span minutes
- Existing joint RGB-depth world models trade off 3D perception gains against RGB prediction fidelity — a fundamental multi-task tension observed in prior work that RoboScape only partially resolves

## Bottlenecks

- World models lack physically grounded representations of 3D geometry and material dynamics, preventing reliable use as training data generators or policy evaluators for contact-rich robotic manipulation
- High cost of real-world robot teleoperation data collection prevents scaling robot policy training, and no automated scalable alternative has reached production; world models generating synthetic data offer a partial mitigation but not yet a full replacement
- Automated offline policy evaluation without human judgment or physical simulators remains unsolved: existing world models produce unreliable success estimates, blocking scalable policy selection and iteration pipelines

## Breakthroughs

- RoboScape achieves 0.953 Pearson correlation (R²=0.908) between world-model policy evaluations and ground-truth simulator outcomes — demonstrating that physics-informed world models can serve as reliable policy evaluators for the first time
- Synthetic data from a physics-informed world model achieves near-parity with real demonstration data for robotic policy training: 200 synthetic trajectories yield 91% success vs 92% for 200 real trajectories on Diffusion Policy / Robomimic Lift

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/diffusion-policy|Diffusion Policy]]
- [[entities/genie|Genie]]
- [[entities/libero|LIBERO]]
- [[entities/lpips|LPIPS]]
- [[entities/psnr|PSNR]]
