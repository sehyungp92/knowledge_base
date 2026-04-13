---
type: source
title: Training Agents Inside of Scalable World Models
source_id: 01KJTG66GD67MFRM8VACHXW41N
source_type: paper
authors:
- Danijar Hafner
- Wilson Yan
- Timothy Lillicrap
published_at: '2025-09-29 00:00:00'
theme_ids:
- generative_media
- policy_optimization
- reinforcement_learning
- robotics_and_embodied_ai
- robot_learning
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Training Agents Inside of Scalable World Models

**Authors:** Danijar Hafner, Wilson Yan, Timothy Lillicrap
**Published:** 2025-09-29 00:00:00
**Type:** paper

## Analysis

# Training Agents Inside of Scalable World Models
2025-09-29 · paper · Danijar Hafner, Wilson Yan, Timothy Lillicrap
https://arxiv.org/pdf/2509.24527

---

### Motivation & Prior Limitations
- Prior world model agents (e.g., Dreamer 3) achieved state-of-the-art performance on narrow environments but lacked the architectural capacity to fit complex real-world distributions, preventing accurate prediction of object interactions and game mechanics in rich environments like Minecraft.
  - Dreamer 3 used 64×64 pixel inputs with abstract crafting actions; Dreamer 4 operates at 640×360 with raw mouse and keyboard control, representing a qualitatively different regime of embodied complexity.
- Controllable video models such as Genie 3, Oasis, and Lucid-v1 have scaled to diverse video distributions but still fail to simulate precise physics and game mechanics, and many require multiple GPUs to run at real-time speeds, making them impractical for imagination training.
  - In a 16-task interactive evaluation, Lucid-v1 passed 0 tasks and Oasis (large) passed only 5, compared to Dreamer 4's 14; the large Oasis model requires multi-GPU hosting and is estimated at ~5 FPS on a single H100.
- No prior agent had obtained diamonds in Minecraft from purely offline data without any environment interaction, a constraint directly relevant to robotics and other safety-critical domains where online interaction with a partially trained policy is unsafe or logistically prohibitive.

---

### Proposed Approach
- Dreamer 4 is a three-phase agent: (1) pretraining a causal tokenizer and dynamics model on video (with optional action conditioning), (2) finetuning a task-conditioned policy and reward model via behavioral cloning, and (3) running reinforcement learning purely inside the world model ("imagination training") without touching the real environment.
  - The separation of world model pretraining from agent finetuning allows the bulk of knowledge to be absorbed from unlabeled video, with action grounding learned from a small fraction of paired data — 100 hours of action labels suffices for 85% PSNR of a fully labeled model.
- The core technical novelty is the **shortcut forcing objective**, which combines diffusion forcing (assigning per-timestep noise levels in sequences) with shortcut models (conditioning on step size to enable 2–4 denoising steps at inference instead of 64+), formulated in x-prediction space rather than v-prediction space to prevent high-frequency error accumulation during autoregressive rollouts.
  - X-prediction targets are more structured than velocity targets; computing the bootstrap loss in x-space with a ramp loss weight (linearly increasing with signal level τ) substantially reduces FVD from 306 to 57 compared to the naive diffusion forcing transformer baseline.
- Both the tokenizer and the dynamics model share a **block-causal 2D transformer** that separates spatial and temporal attention layers, applies temporal attention only every 4 layers, uses GQA to reduce KV cache size, and supports alternating batch lengths during training for efficient long-context learning.
  - This achieves 21 FPS on a single H100 at 640×360 resolution with a 9.6-second context window — 6× longer context than previous Minecraft world models while maintaining real-time interactive inference.
- Reinforcement learning inside imagination uses **PMPO** (a sign-of-advantage objective) with a reversed KL behavioral prior, which avoids return normalization and provides equal focus across tasks with differing reward scales.

---

### Results & Capabilities
- Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data (no environment interaction), achieving a 0.7% diamond success rate over 1000 episodes, while VPT (finetuned on 270K hours of data) stalls at sticks (53%) and obtains diamonds only through rare edge cases.
  - Dreamer 4 uses 100× less data than VPT (finetuned) — only 2.5K hours of contractor video vs. 270K hours of annotated YouTube video — and achieves success rates above 90% up to the stone pickaxe and 29% for the iron pickaxe.
- In the 16-task human interaction benchmark, Dreamer 4 accurately simulates switching items, placing and breaking blocks, fighting monsters, riding boats, entering Nether portals, and interacting with crafting tables and furnaces — qualitatively demonstrating an understanding of game mechanics that prior models cannot match.
- Action conditioning generalizes out of distribution: a model trained with actions only on Minecraft's Overworld achieves 76% PSNR and 80% SSIM on the Nether and End dimensions, which it has never seen with action labels, indicating the world model learns a general action-grounding schema separable from environment-specific knowledge.
- On robotics video, Dreamer 4 generates accurate counterfactual physics — picking up objects, flipping bowls, pressing balls onto plates, moving towels — demonstrating that the architecture transfers beyond games to real-world manipulation data.
- The world model representations used as a backbone for behavioral cloning (WM+BC) outperform both training from scratch and finetuning from Gemma 3 (a vision-language model pretrained on far more compute), indicating that video prediction implicitly learns representations useful for decision-making.
  - Imagination training on top of WM+BC further improves not only success rates but also policy efficiency — milestones are reached faster in wall-clock time during 60-minute episodes.

---

### Implications
- The demonstration that a world model can absorb knowledge primarily from unlabeled video and require only a small fraction of action-labeled data is a concrete step toward learning general simulators from web-scale video, where action annotations are unavailable.
- Offline imagination training — achieving diamond-level Minecraft performance with zero environment interaction — directly enables the robotics workflow where deploying partially trained polic

## Key Claims

1. Previous world models have been unable to accurately predict object interactions in complex environments.
2. Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, without environment interaction.
3. The Dreamer 4 world model achieves real-time interactive inference on a single GPU through a shortcut forcing objective and an efficient transformer architecture.
4. The Dreamer 4 world model learns general action conditioning from only a small amount of labeled data, allowing it to extract the majority of its knowledge from diverse unlabeled videos.
5. Obtaining diamonds in Minecraft requires choosing sequences of over 20,000 mouse and keyboard actions from raw pixels.
6. Controllable video models like Genie 3, despite being trained on diverse real video and games, still struggle to learn the precise physics of object interactions and game mechanics, limiting their use
7. Controllable video models often require many GPUs to simulate a single scene in real time, reducing their practicality for imagination training.
8. Dreamer 4 substantially outperforms OpenAI's VPT offline agent while using 100× less data.
9. Learning from fixed datasets allows training agents purely in imagination without online interaction, which is valuable for robotics where deploying partially-trained policies is often unsafe.
10. Shortcut models generate high-quality samples with 2 or 4 sampling steps, compared to 64 or more steps for typical diffusion models.

## Capabilities

- Imagination training enables agents to solve long-horizon control tasks (>20,000 sequential mouse/keyboard actions) entirely from offline datasets without any environment interaction, demonstrated by obtaining diamonds in Minecraft from 2.5K hours of contractor footage
- 2B-parameter diffusion-based video world model achieves real-time interactive inference at 21 FPS on a single H100 GPU with 9.6-second context, enabling practical imagination training and live human interaction
- Shortcut forcing enables video world model generation with only 4 sampling steps approaching quality of 64-step diffusion forcing, yielding 16x inference speedup in a single training phase without schedules
- World models can learn accurate action conditioning from only ~4% of paired action data (100 hours out of 2500), absorbing the majority of knowledge from unlabeled video — achieving 85% PSNR and 100% SSIM relative to fully supervised baseline
- Action conditioning in world models generalizes out-of-distribution to environments seen only in unlabeled video (no paired actions), achieving 76% PSNR and 80% SSIM relative to fully supervised baseline on held-out Nether/End dimensions
- World model accurately predicts complex object interactions and game mechanics from raw pixels and mouse/keyboard actions, succeeding on 14/16 diverse interaction tasks where prior models achieved at most 5/16
- Video prediction pretraining implicitly learns world representations more useful for decision-making than VLM pretraining — world model representations outperform Gemma 3 for behavioral cloning on Minecraft tasks despite Gemma 3 being trained on substantially more compute and data
- World model trained primarily on video game data transfers to real-world robotics, producing accurate physics simulation and counterfactual interactions with real objects from a robotics dataset

## Limitations

- World model temporal consistency is limited to ~9.6 seconds of context — tasks requiring recall of events from earlier in long episodes (prior inventory, resource locations) are not supported
- Inventory state tracking is imprecise — inventory items are sometimes unclear or change unexpectedly over time in generated sequences, degrading agent performance on crafting-dependent tasks
- Diamond success rate collapses to 0.7% despite state-of-the-art performance — a sharp cliff from stone pickaxe (90%) to iron pickaxe (29%) to diamonds (0.7%) reveals extreme compounding failure over long action horizons
- Training requires 256–1024 TPU-v5p chips for a 2B-parameter model — the approach is inaccessible without large-scale compute infrastructure
- No language understanding integrated — tasks are specified via one-hot indicators, not natural language, blocking instruction-following generalization to novel objectives
- No automatic goal discovery — the 20-task diamond sequence must be manually specified as a linear prompt sequence; the agent cannot decompose novel long-horizon objectives it wasn't trained on
- Internet-scale pretraining on diverse web video has not been demonstrated — all results use a curated game-specific dataset (VPT contractor footage); generalization to open-domain video is aspirational
- Minimum ~100 hours of paired action-labeled video required for reliable action conditioning — zero-shot action grounding from purely unlabeled video is not yet feasible
- No corrective online data incorporation — the offline-only pipeline cannot improve from mistakes encountered during real deployment, creating a fixed performance ceiling set by the training data coverage
- Behavior cloning alone from offline data fails severely on hard long-horizon milestones — WM+BC without imagination RL achieves only 17% for iron pickaxe vs 29% with RL, and the gap widens at harder milestones, revealing a fundamental compounding covariate shift problem
- Time-factorized attention architecture introduces a measurable quality tradeoff — switching long-context layers from dense to time-only attention reduces FVD quality (91 vs prior), a limitation of the efficiency architecture
- World model fails 2/16 interaction tasks (12.5% failure rate) even in best-case controlled evaluation with human player — complex multi-step tasks like building precise structures remain unreliable

## Bottlenecks

- World model context length constrains agent planning horizon — current 9.6-second context prevents agents from reasoning about events from earlier in long episodes (prior inventory state, resource locations visited minutes ago)
- Absence of automatic subgoal discovery for long-horizon tasks — agents require manually specified linear task sequences, blocking generalization to novel objectives and autonomous task decomposition
- Open-domain internet video lacks action annotations at the scale and diversity needed to ground world model action conditioning — without a mechanism to infer or label actions in web video, pretraining on internet-scale video data remains unrealized

## Breakthroughs

- First agent to obtain diamonds in Minecraft purely from offline data without environment interaction — demonstrates that imagination training inside a high-fidelity world model can replace online RL for complex long-horizon control tasks
- Shortcut forcing objective achieves 16x inference speedup for diffusion world models in a single training phase — enabling 2B-parameter real-time interactive inference at 21 FPS on a single GPU, making imagination training tractable at scale
- World models can learn accurate action grounding from a small fraction (~4%) of paired data, with generalization to OOD environments seen only in unlabeled video — demonstrating that most world knowledge is absorbed from unlabeled observation

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/flow-matching|Flow Matching]]
- [[entities/gemma-3|Gemma 3]]
- [[entities/genie-3|Genie 3]]
- [[entities/grouped-query-attention|Grouped Query Attention]]
- [[entities/multi-token-prediction|Multi-Token Prediction]]
