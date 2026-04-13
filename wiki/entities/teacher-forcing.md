---
type: entity
title: teacher forcing
entity_type: method
theme_ids:
- chain_of_thought
- generative_media
- image_generation_models
- latent_reasoning
- model_architecture
- multimodal_models
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.001924181252855826
staleness: 0.0
status: active
tags: []
---
# teacher forcing

Teacher forcing is a foundational training strategy for autoregressive models in which ground-truth tokens or frames — rather than the model's own prior predictions — are fed as inputs at each step during training. By decoupling the model's outputs from its inputs during training, teacher forcing provides clean, stable gradient signals and dramatically accelerates convergence. Its significance lies precisely in the tension it creates: a model trained this way never learns to recover from its own mistakes, yet must do exactly that at inference time when no ground truth is available.

**Type:** method
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]]

## Overview

Teacher forcing works by substituting the model's predicted output at step $t$ with the ground-truth value when constructing the input at step $t+1$. This makes every training step independent and well-conditioned: gradients flow through clean targets rather than through a cascade of potentially erroneous self-predictions. The technique has been standard in sequence-to-sequence models, language model pretraining, and increasingly in video and world model training where each frame is predicted from prior ground-truth frames.

The core problem teacher forcing introduces is **exposure bias**: the distribution of inputs seen during training (always ground-truth) diverges from the distribution seen at inference (always the model's own outputs). In token generation this manifests as compounding errors — a single wrong token shifts the context distribution, making subsequent predictions increasingly unreliable. In video and world model generation the effect is more visually dramatic and faster-moving: generative quality can collapse within 20–30 steps when the model encounters frame contexts it has never seen during training. The GameNGen work on neural DOOM simulation documents this precisely — without noise augmentation to bridge train/inference context distributions, autoregressive generation degrades rapidly, and auto-regressive generation is noted to be inherently unstable and prone to sampling divergence.

## Exposure Bias and Its Mitigations

The gap between teacher-forced training and closed-loop inference has motivated a line of partial remedies, none fully satisfying:

**Scheduled sampling** interpolates between ground-truth and model predictions as a curriculum, gradually withdrawing the training crutch. This improves robustness but complicates training dynamics.

**Noise augmentation**, used explicitly in GameNGen's video generation setting, injects noise into conditioning frames during training to simulate the distributional drift that accumulates in autoregressive rollouts. This is a domain-appropriate proxy for what scheduled sampling achieves in discrete sequences.

**Reinforcement learning on the model's own rollouts** bypasses teacher forcing entirely by training against rewards computed over full generated trajectories. This is computationally expensive but eliminates the distributional mismatch at the cost of requiring a reward signal. The emergence of [[themes/rl_for_llm_reasoning|RL-for-LLM-reasoning]] approaches (RLHF, PPO, GRPO) reflects this tradeoff being accepted at scale for reasoning quality gains.

**Direct sequence-level objectives** (minimum risk training, sequence-level distillation) optimise over whole sequences rather than per-step cross-entropy, which partially decouples training from step-wise ground-truth dependency.

## Relevance to World Models and Video Generation

The GameNGen system provides the most concrete evidence in this collection of teacher forcing's consequences in a high-dimensional generative setting. GameNGen trains a diffusion model to predict the next game frame conditioned on a context window of past frames and actions — a canonical teacher-forced autoregressive setup applied to continuous visual observations. The finding that quality degrades fast after 20–30 steps without noise augmentation is a direct empirical signature of exposure bias operating at frame level: the model was trained on DOOM frames; at inference, after several prediction errors, it encounters frame contexts increasingly unlike DOOM gameplay, and simulation quality degrades accordingly.

The mitigation — noise augmentation during training — implicitly regularises the model against small distributional perturbations in its conditioning context, making it more tolerant of its own imperfect predictions in the rollout. That only 4 DDIM denoising steps are needed for robust simulation, with no quality degradation versus 20+ steps, suggests the exposure bias problem in diffusion-based world models is partly orthogonal to the number of denoising steps — the bottleneck is the autoregressive frame-to-frame conditioning chain, not within-step denoising depth.

## Relevance to Language Model Pretraining and Reasoning

For large language models, teacher forcing during pretraining is so deeply embedded in the standard training loop that its limitations are often treated as background assumptions rather than active design choices. The pretraining cross-entropy objective over next-token prediction is teacher-forced by definition. At the scale of modern pretraining corpora, the exposure bias may be partially self-correcting: a model that sees enough diverse continuations of any given prefix learns a distribution robust enough that moderate prediction errors don't cascade catastrophically in ordinary generation.

However, teacher forcing becomes a live constraint in chain-of-thought and [[themes/latent_reasoning|latent reasoning]] settings, where the model generates extended reasoning traces during inference. These traces have no ground-truth analogue in standard pretraining; the model is in closed-loop over the entire reasoning chain. This is part of the motivation for RL-based fine-tuning of reasoning models — learning from the model's own rollout outcomes replaces teacher forcing with a training signal that is actually aligned with the inference-time regime.

The [[themes/test_time_compute_scaling|test-time compute scaling]] paradigm, in which models generate many candidate solutions and select among them, also works around teacher forcing limitations implicitly: by sampling many trajectories and selecting the best, the system tolerates individual trajectory degradation rather than demanding each rollout be reliable from a teacher-forced checkpoint.

## Open Questions

The fundamental tension teacher forcing creates — stable training vs. closed-loop inference reliability — has not been solved, only managed. Several open questions persist:

- **At what scale does exposure bias become negligible?** There is no clear empirical answer for LLMs. For video world models, the GameNGen evidence suggests it remains a problem even with strong generative priors.
- **Can noise augmentation be principled rather than heuristic?** The optimal noise schedule for bridging teacher-forced training to autoregressive inference in continuous domains is not well-characterised.
- **Does teacher forcing distort what a model implicitly "believes" about uncertainty?** A model trained on ground-truth conditioning has never needed to propagate uncertainty from its own prior predictions — its calibration in self-conditioned rollout regimes may be systematically miscalibrated.
- **In reasoning chains, does teacher forcing on scratchpad tokens during SFT hurt RL fine-tuning later?** If the model learns to rely on ground-truth scratchpad prefixes, the transition to generating its own reasoning traces may introduce exactly the distributional shift documented in the video generation setting.

## Relationships

Teacher forcing is structurally connected to [[themes/pretraining_and_scaling|pretraining and scaling]] as the default training regime for all autoregressive models trained at scale. Its failure mode — exposure bias — is the primary motivation for [[themes/reinforcement_learning|reinforcement learning]] fine-tuning of language models and for hybrid scheduled-sampling approaches in sequence generation. In the [[themes/video_and_world_models|video and world models]] domain, GameNGen provides direct empirical evidence of its instability signatures and documents noise augmentation as a practical mitigation. The concern recurs in [[themes/chain_of_thought|chain-of-thought]] and [[themes/latent_reasoning|latent reasoning]] settings, where extended closed-loop generation amplifies the train/inference gap that teacher forcing creates.

## Key Findings

## Limitations and Open Questions

## Sources
