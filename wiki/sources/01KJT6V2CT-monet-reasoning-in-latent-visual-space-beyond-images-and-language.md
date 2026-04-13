---
type: source
title: 'Monet: Reasoning in Latent Visual Space Beyond Images and Language'
source_id: 01KJT6V2CT4CZGBH976JATB9H5
source_type: paper
authors:
- Qixun Wang
- Yang Shi
- Yifei Wang
- Yuanxing Zhang
- Pengfei Wan
- Kun Gai
- Xianghua Ying
- Yisen Wang
published_at: '2025-11-26 00:00:00'
theme_ids:
- finetuning_and_distillation
- latent_reasoning
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# Monet: Reasoning in Latent Visual Space Beyond Images and Language

**Authors:** Qixun Wang, Yang Shi, Yifei Wang, Yuanxing Zhang, Pengfei Wan, Kun Gai, Xianghua Ying, Yisen Wang
**Published:** 2025-11-26 00:00:00
**Type:** paper

## Analysis

# Monet: Reasoning in Latent Visual Space Beyond Images and Language
2025-11-26 · paper · Qixun Wang, Yang Shi, Yifei Wang, Yuanxing Zhang, Pengfei Wan et al. (8 total)
https://arxiv.org/pdf/2511.21395

---

### Motivation & Prior Limitations
Existing "think with images" approaches for multimodal reasoning are fundamentally constrained by dependence on external tools, preventing flexible, human-like visual reasoning within an internal perceptual space.
- Methods that acquire intermediate auxiliary images via bounding box prediction, depth estimation tools, or code interpreters cannot generalize beyond their specific tool set — a model trained to predict bounding boxes fails at visual math or spatial reasoning requiring operations outside that toolkit.
  - Tool-dependent pipelines also increase training complexity and require asynchronous, multi-turn inference, increasing deployment latency.
- Prior latent visual reasoning approaches introduced two specific failure modes that Monet addresses: high computational cost from aligning thousands of image token embeddings, and insufficient supervision of the latent embeddings themselves.
  - Methods such as Yang et al. used mean pooling to compress image embeddings before alignment, distorting detailed visual features; Li et al. restricted alignment to cropped regions, failing to encode whole-image visual operations.
  - Existing SFT pipelines apply cross-entropy loss only on text tokens following latent embeddings, making it trivial for the model to memorize subsequent tokens rather than learn meaningful latent representations.
- Standard GRPO reinforcement learning cannot optimize continuous latent embeddings because its policy gradient objective is defined only over discrete text tokens, leaving the latent reasoning component entirely untrained during the RL stage.

---

### Proposed Approach
Monet is a training framework built on Qwen2.5-VL-7B that enables MLLMs to generate continuous latent embeddings as intermediate visual thoughts during chain-of-thought reasoning, replacing explicit auxiliary images with internally generated visual representations.

- The SFT pipeline proceeds in three stages: a warm-up stage that adapts the model to image-text interleaved reasoning patterns, a distillation stage that produces high-quality target latent embeddings using a teacher-student setup, and a final stage that trains the model to generate those embeddings without access to ground-truth auxiliary images.
  - In Stage 2, dual supervision is applied: cosine alignment between observation-token hidden representations under teacher (with auxiliary image) and student (with latent embeddings) conditions, combined with a controlled attention mask that routes visual information strictly along the path auxiliary image → latent embeddings → observation tokens.
  - A critical design constraint enforces that the alignment loss backpropagates exclusively through the latent embeddings — not through surrounding text or image representations — preventing the model from exploiting shortcut paths. Ablation shows removing this "latent-only backpropagation" causes accuracy to drop from 82.20% to 46.07% on V*.
  - Stage 3 aligns generated latent embeddings across all transformer layers (not just the final layer, as in prior work) against the frozen targets from Stage 2, providing stronger multi-layer supervision.

- VLPO (Visual-latent Policy Optimization) extends GRPO to directly optimize continuous latent embeddings by modeling each generated latent embedding as a sample from a Gaussian distribution centered on the policy's current output.
  - The ratio r_{i,t}(θ) for a latent step is computed as exp(−(1/2σ²)‖h^old_{i,t} − h^θ_{i,t}‖²), meaning a positive advantage signal pulls the policy's latent embedding toward the rollout embedding that led to a correct answer — a form of reward-weighted latent regression.
  - No separate reward is given for invoking latent reasoning itself; only outcome accuracy and answer format rewards are used, preventing the model from triggering latent reasoning indiscriminately.

- The Monet-SFT-125K dataset is constructed through a three-stage curation pipeline: filtering out samples solvable from the original image alone (ensuring auxiliary images are necessary), verifying that auxiliary images actually enable correct answers via Qwen2.5-VL-72B, and using Deepseek-V3.1 and Gemini 2.5 Pro to annotate which text tokens correspond to crucial visual observations for fine-grained latent supervision.

---

### Results & Capabilities
Monet-7B consistently outperforms Qwen2.5-VL-7B across fine-grained perception and reasoning benchmarks spanning real-world, chart, and OCR domains, with relative improvements ranging from +4.25% to +9.75%.

- On MME-RealWorld-Lite, Monet-7B achieves 55.50% overall compared to the base model's 45.75%, a +9.75% gain; on V*, it reaches 83.25% vs. 76.44% baseline.
  - Monet-7B matches or exceeds Deepeyes (83.25%) on V* while also outperforming it substantially on MME-RealWorld (55.50% vs. 54.28%) and VisualPuzzles (35.02% vs. 32.96%).
  - Vanilla SFT + GRPO trained on the same data achieves 78.53% on V* and 30.99% on VisualPuzzles, underperforming Monet-7B on both, confirming that GRPO is not well-suited for latent reasoning.

- Monet-7B demonstrates strong out-of-distribution generalization on VisualPuzzles — abstract visual logic puzzles unseen during training — achieving 35.02% versus the base model's 32.71%, with notably large gains on algorithmic (+6.09%) and analogical (+8.78%) subtasks.
  - VLPO is the key driver of OOD generalization: ablation shows that Monet-SFT without VLPO scores 30.48% on VisualPuzzles, worse than the base model, while adding VLPO lifts it to 35.02%.
  - On VisualPuzzles, using Ktest > 0 latent embeddings at inference benefits only the VLPO-enhanced model, not the SFT-only model, confirming that SFT alone cannot produce latent representations general enough to help on unseen visual reasoni

## Key Claims

1. Existing 'think with images' methods for visual reasoning are fundamentally limited by external tools, preventing flexible human-like visual reasoning.
2. Reliance on external tools or interpreters for visual reasoning necessitates asynchronous, multi-turn inference, complicating deployment and increasing latency.
3. The next-token-prediction (NTP) objective provides insufficient supervision for latent embeddings, as the model can memorize following tokens instead of learning effective latent representations.
4. Applying GRPO after latent visual reasoning SFT primarily enhances text-based reasoning rather than latent reasoning.
5. Mean pooling to compress image tokens for latent alignment distorts detailed visual features.
6. Monet introduces a three-stage distillation-based SFT pipeline that enables MLLMs to generate continuous latent embeddings as intermediate visual thoughts without requiring external tools.
7. VLPO directly optimizes latent embeddings by pulling policy latent embeddings toward 'good-action' latent embeddings that led to positive outcome rewards, an ability GRPO fundamentally lacks.
8. Latent-only backpropagation is essential: allowing the alignment loss to update non-latent representations causes sharp performance degradation because the model exploits shortcut paths.
9. The warm-up SFT stage is necessary because an unadapted base model achieves almost no improvement from auxiliary images in predicting observation tokens.
10. SFT Stage 3 aligns all layers of latent embeddings rather than only the final layer, providing stronger supervision than prior latent visual reasoning work.

## Capabilities

- MLLMs can reason directly in continuous latent visual space by generating latent embeddings as intermediate visual thoughts, eliminating dependence on external visual tools and enabling flexible abstract visual reasoning
- Visual-latent Policy Optimization (VLPO) enables reinforcement learning to directly optimize continuous latent embeddings via Gaussian probability estimation, producing strong OOD generalization on abstract visual reasoning tasks not seen during training
- Test-time scaling of latent embedding count improves MLLM reasoning performance beyond training-time configurations — performance peaks at Ktest larger than Ktrain, with VLPO extending this scaling to OOD scenarios

## Limitations

- GRPO and standard policy gradient RL methods cannot optimize continuous latent embeddings — the GRPO objective is defined only over text tokens, leaving latent visual reasoning components entirely untrained during RL
- SFT training alone cannot induce robust OOD generalization in latent visual reasoning — only VLPO-based RL causes latent embeddings to generalize to unseen abstract visual tasks; SFT-only models show no benefit from latent embeddings on OOD benchmarks
- Next-token prediction provides insufficient supervision for latent embeddings — the model can memorize subsequent tokens without learning effective latent representations, and NTP gradients reach latent embeddings only indirectly
- Latent-visual alignment during training is computationally prohibitive — auxiliary images contain hundreds to thousands of image embeddings, making direct token-level alignment expensive in both compute and memory
- Tool-dependent visual reasoning methods (bounding box prediction, depth estimation, code interpreters) cannot generalize to tasks requiring complex visual operations beyond their fixed tool vocabulary — visual math, spatial reasoning, and graphic reasoning all fall outside supported operations
- Multi-stage SFT pipeline for latent reasoning substantially increases training complexity — three sequential SFT stages plus a separate RL stage, each with distinct teacher/student configurations, add significant orchestration overhead
- Reward design for latent visual reasoning is entirely unexplored — current VLPO uses only final-answer accuracy and format rewards, providing no signal about intermediate latent representation quality; optimizing only outcomes may leave latent reasoning quality underspecified
- Mean pooling to compress image tokens for latent alignment destroys detailed visual features — a known failure mode in prior latent visual reasoning approaches that causes performance degradation on fine-grained visual tasks
- VLPO uses a Gaussian approximation to estimate latent embedding probability — the scalar σ hyperparameter is predefined rather than learned, and the true distribution of latent embeddings in MLLM hidden space may be non-Gaussian
- Latent embedding count K must be manually selected at test time from a discrete candidate set {8, 10, 12, 16} — the model has no mechanism to dynamically determine the optimal reasoning depth, adding a test-time hyperparameter search cost
- Existing image-text interleaved CoT training datasets have systematic quality flaws: many samples are trivially solvable without auxiliary images, auxiliary images are sometimes inaccurate, and no annotation identifies which tokens encode critical visual observations
- Teacher-student training for latent reasoning requires maintaining two full MLLM copies simultaneously in memory — the frozen teacher model must remain loaded throughout Stage 2 training, approximately doubling GPU memory requirements

## Bottlenecks

- Standard policy gradient RL methods (GRPO and variants) are fundamentally incompatible with continuous latent embedding optimization, blocking reward-based improvement of non-discrete visual reasoning components and preventing RL-based OOD generalization in MLLMs with latent reasoning
- Training MLLMs to reason in latent visual space requires multi-stage teacher-student pipelines with prohibitive per-stage compute overhead, blocking efficient and scalable development of latent reasoning capabilities beyond research-scale 7B models

## Breakthroughs

- VLPO (Visual-latent Policy Optimization) enables reinforcement learning to directly optimize continuous latent embeddings via Gaussian probability estimation, breaking the fundamental incompatibility between discrete policy gradient methods and continuous visual reasoning spaces
- Monet demonstrates that MLLMs can learn to perform abstract visual reasoning in a fully internal latent space without external tools, auxiliary images at inference, or image generation — extending 'thinking with images' to a tool-free, continuous-space paradigm that generalizes to unseen visual reas

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/qwen25-vl-7b|Qwen2.5-VL-7B]]
- [[entities/vlmevalkit|VLMEvalKit]]
