---
type: source
title: 'PAN: A World Model for General, Interactable, and Long-Horizon World Simulation'
source_id: 01KJT8GR214F2422CXSF044WAG
source_type: paper
authors:
- PAN Team
- Jiannan Xiang
- Yi Gu
- Zihan Liu
- Zeyu Feng
- Qiyue Gao
- Yiyan Hu
- Benhao Huang
- Guangyi Liu
- Yichi Yang
- Kun Zhou
- Davit Abrahamyan
- Arif Ahmad
- Ganesh Bannur
- Junrong Chen
- Kimi Chen
- Mingkai Deng
- Ruobing Han
- Xinqi Huang
- Haoqiang Kang
- Zheqi Liu
- Enze Ma
- Hector Ren
- Yashowardhan Shinde
- Rohan Shingre
- Ramsundar Tanikella
- Kaiming Tao
- Dequan Yang
- Xinle Yu
- Cong Zeng
- Binglin Zhou
- Zhengzhong Liu
- Zhiting Hu
- Eric P. Xing
published_at: '2025-11-12 00:00:00'
theme_ids:
- generative_media
- latent_reasoning
- multimodal_models
- reasoning_and_planning
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# PAN: A World Model for General, Interactable, and Long-Horizon World Simulation

**Authors:** PAN Team, Jiannan Xiang, Yi Gu, Zihan Liu, Zeyu Feng, Qiyue Gao, Yiyan Hu, Benhao Huang, Guangyi Liu, Yichi Yang, Kun Zhou, Davit Abrahamyan, Arif Ahmad, Ganesh Bannur, Junrong Chen, Kimi Chen, Mingkai Deng, Ruobing Han, Xinqi Huang, Haoqiang Kang, Zheqi Liu, Enze Ma, Hector Ren, Yashowardhan Shinde, Rohan Shingre, Ramsundar Tanikella, Kaiming Tao, Dequan Yang, Xinle Yu, Cong Zeng, Binglin Zhou, Zhengzhong Liu, Zhiting Hu, Eric P. Xing
**Published:** 2025-11-12 00:00:00
**Type:** paper

## Analysis

# PAN: A World Model for General, Interactable, and Long-Horizon World Simulation
2025-11-12 · paper · PAN Team, Jiannan Xiang, Yi Gu, Zihan Liu, Zeyu Feng et al. (34 total)
https://arxiv.org/pdf/2511.09057

---

### Motivation & Prior Limitations
- Video generation models like Sora, Wan, and Gen-3 produce visually realistic sequences but operate in an open-loop, prompt-to-full-video manner that lacks causal action control, real-time interactivity, and long-horizon consistency — properties essential for purposeful reasoning and planning.
  - These models lack explicit notions of state, action, and object-level representations, making them unable to evaluate counterfactual outcomes or support decision-making under different action alternatives.
- Existing world modeling efforts are fragmented across restricted domains (robotics simulators, game environments, autonomous driving, 3D scene navigation) and fail to generalize across diverse environments and interaction formats.
  - 3D world models (e.g., World Labs) capture geometric structure but lack temporal dynamics and interactivity; game-focused models (e.g., Genie 2) are domain-constrained with restrictive action spaces.
- Latent-space predictive architectures like JEPA suffer from representation collapse: the model can minimize its objective by mapping all observations to a constant vector, and learned latent transitions remain ungrounded in observable world dynamics, a problem the authors term "indefinability."
  - Fixes such as DINO-WM stabilize the latent space using frozen DINOv2 features but still permit transitions that are semantically valid in feature space yet physically implausible, since the representations are not optimized for temporal consistency.
- Naive sequential extension of video diffusion models to long-horizon simulation causes local inconsistency between adjacent video chunks and rapid quality degradation through error accumulation, as conditioning on only the last generated frame propagates artifacts forward.

---

### Proposed Approach
- PAN introduces the Generative Latent Prediction (GLP) architecture, which formalizes world modeling as a hierarchical generative process: an encoder maps observations to latent states, an autoregressive predictive module evolves those states conditioned on language actions, and a diffusion decoder reconstructs perceptually grounded observations — coupling latent prediction with observation-space supervision to avoid collapse and indefinability.
  - Unlike JEPA-style latent matching objectives, GLP supervises transitions by requiring the decoder to reconstruct the next observable frame, ensuring every latent transition corresponds to a realizable sensory change.
  - The GLP formulation absorbs stochasticity and unseen content (e.g., novel viewpoints, occluded regions) as intrinsic properties of physical reality rather than obstacles, delegating fine-grained variability to the diffusion decoder while the backbone models smooth causal transitions.
- The autoregressive world model backbone is built on Qwen2.5-VL-7B-Instruct, grounding latent dynamics in the massive text-based knowledge acquired during LLM pretraining and enabling natural language as the universal action interface across any domain.
  - Observations and actions are arranged in a multi-turn conversational format, with 256 learnable query embeddings per assistant turn representing the predicted next latent state; during inference, closed-loop rollouts feed back predicted states recursively.
- The video diffusion decoder is adapted from Wan2.1-T2V-14B (14B parameters) and extended with Causal Swin-DPM, a sliding-window mechanism that holds two video chunks at different noise levels (K and K/2 denoising steps) simultaneously, enabling smooth transitions by conditioning each new chunk on a partially-noised representation of the preceding one rather than a single sharp frame.
  - Chunk-wise causal attention masking prevents information leakage from future actions, preserving real-time interactivity; noise augmentation (fixed k=0.055) on the conditioning frame introduces controlled stochasticity to dampen error propagation across chunks.
  - The latent world state from the backbone conditions the decoder via a newly added cross-attention stream with zero-initialized linear projection; language actions are separately encoded with umT5 through the original text cross-attention pathway, and the two streams are summed.
- Training uses a two-stage curriculum: Stage 1 adapts the video diffusion decoder in isolation (960 H200 GPUs, 5 epochs) to learn the Causal Swin-DPM mechanism; Stage 2 jointly trains query embeddings and the decoder end-to-end with early stopping after 1 epoch, freezing the VLM backbone and using the GLP flow-matching loss.
- Training data consists of large-scale video–action pairs built from publicly accessible long-form videos segmented by shot-boundary detection, filtered through a multi-stage pipeline (rule-based motion/aesthetic filters → pretrained aesthetic and OCR detectors → a custom-trained VLM filter), and re-captioned with a VLM prompted to produce dense temporally grounded descriptions emphasizing dynamics rather than static scene attributes.

---

### Results & Capabilities
- PAN achieves state-of-the-art performance among open-source models on Action Simulation Fidelity with 70.3% on agent simulation and 47.0% on environment simulation (overall 58.6%), surpassing all open-source baselines and most commercial models including KLING and MiniMax.
  - The gap over standard video generators demonstrates that visual realism without causal grounding is insufficient for multi-step action–effect dynamics.
- On Long-Horizon Forecast, PAN scores 53.6% on Transition Smoothness and 64.1% on Simulation Consistency, substantially exceeding all baselines including closed-source commercial models, with baselines exhibiting temporal drift and amplified motion magnitudes over extended rollouts.
- In Simulative Reas

## Key Claims

1. Recent video generation models operate in an open-loop setting, producing complete videos from fixed prompts without real-time causal control or adaptive feedback.
2. Existing world modeling efforts often focus on restricted domains (physical, game, or 3D-scene dynamics) and struggle to generalize across diverse environments and interaction formats.
3. 3D world models capture static or geometric aspects of the environment but lack fine-grained temporal dynamics and interactivity.
4. PAN employs the Generative Latent Prediction (GLP) architecture that combines an autoregressive LLM-based latent dynamics backbone with a video diffusion decoder to unify latent-space reasoning and re
5. The GLP architecture separates the modeling of abstract causal dynamics from the generation of realistic and temporally consistent observations.
6. GLP treats uncertainties and unseen content as intrinsic aspects of physical reality during training rather than as obstacles to be avoided.
7. JEPA-style learning objectives are prone to representation collapse because the model can trivially minimize the loss by mapping all observations to a constant vector, leading to the indefinability pr
8. DINO-WM alleviates representation collapse by training on fixed DINOv2 features, but the learned transitions remain ungrounded in the observation space and do not correspond to realizable world dynami
9. PAN's generative supervision objective grounds latent predictions in observable outcomes, ensuring each latent transition corresponds to a realizable sensory change.
10. PAN uses the vision tower of Qwen2.5-VL-7B-Instruct as its vision encoder and the language model of Qwen2.5-VL-7B-Instruct as its autoregressive world model backbone.

## Capabilities

- Open-domain, action-conditioned world simulation across diverse environments using free-form natural language action conditioning — PAN simulates visually coherent future world states in response to language instructions spanning physical, embodied, robotic, and general video domains
- Long-horizon video world simulation with maintained temporal consistency — Causal Swin-DPM enables smooth multi-step rollouts without quality degradation, substantially outperforming all open-source and most commercial baselines on transition smoothness and simulation consistency
- Simulative reasoning and planning via world model thought experiments — integrating a world model simulator enables an agent to test candidate actions before execution, improving manipulation task success by 23–27% over LLM-only baseline
- LLM backbone as world model dynamics predictor — a pretrained VLM (Qwen2.5-VL-7B) serves as the autoregressive world model backbone, grounding visual world-state transitions in text-based knowledge and enabling arbitrary natural-language action conditioning
- On-demand counterfactual and rare-event world simulation — the model synthesizes physically coherent tail events and counterfactual scenarios, enabling targeted robustness testing and safety-focused data augmentation

## Limitations

- World model history window capped at 10 interaction rounds — context constraint prevents coherent long-range reasoning over extended interaction histories, a hard architectural ceiling imposed by the VLM backbone's context window
- Extreme compute requirements render the approach inaccessible to most researchers — 960 NVIDIA H200 GPUs required for training, representing a frontier-scale resource barrier
- Open-loop compounding errors in autoregressive simulation — conditioning on own generated observations rather than ground truth means artifacts and motion drift accumulate forward, with Causal Swin-DPM only partially mitigating the degradation
- Scene-level environment simulation accuracy (47%) significantly trails agent simulation accuracy (70.3%) — a performance cliff for interventions requiring compositional object manipulation or scene-level state changes vs. simple agent trajectory following
- Domain-specific finetuning required for robotic manipulation tasks — all models are finetuned on Agibot data for the planning benchmarks, indicating that zero-shot transfer from general video pretraining to novel physical manipulation domains is not yet achieved
- Conditioning on fully-denoised frames causes error accumulation, requiring artificial noise injection as a workaround — the generation pipeline is unstable without adding Gaussian noise (k=0.055) to conditioning frames at each step
- Single visual modality only — the world model lacks audio, haptic, proprioceptive, or other sensory channels, creating a fundamental perceptual gap for embodied simulation tasks where multi-modal signals are critical
- Full GLP mixed discrete-continuous backbone not yet implemented — the complete theoretical formulation combining LLMs with diffusion embedders for mixed representation is deferred to future work; the present system is a simplified approximation of the intended architecture
- JEPA-style latent-only world model objectives are fundamentally prone to representational collapse and produce transitions not grounded in realizable world dynamics — an entire class of world model architectures is identified as theoretically unsound
- Action-conditioned temporal training data scarcity — existing public video datasets consist of short, independent clips lacking action annotations and temporal continuity, requiring extensive proprietary data pipeline construction to train interactive world models
- Joint training converges after only 1 of 5 planned epochs, suggesting rapid optimization saturation or instability in the two-stage training regime — the system may be capacity-limited or susceptible to overfitting under joint optimization

## Bottlenecks

- Action-conditioned long-horizon video data scarcity — public video corpora lack temporal continuity and action-annotation structure required for interactive world model training, forcing large-scale proprietary data pipeline construction as a prerequisite
- Error accumulation in long-horizon autoregressive video simulation — each generated frame inherits imperfections from prior frames; despite sliding-window mitigation, quality degrades over extended rollouts, blocking reliable simulation for long-horizon planning
- Absence of a principled, collapse-free world model training objective — JEPA-style latent matching collapses to trivial solutions while pixel reconstruction is unstable under high-frequency noise; this blocks reliable world model development without bespoke generative supervision designs

## Breakthroughs

- Generative Latent Prediction (GLP) as a principled, collapse-free training objective for general world models — GLP grounds latent predictions by anchoring them to observable reconstruction rather than latent matching, resolving the JEPA indefinability problem and proposing a candidate universal wor
- LLM as world model dynamics backbone — a pretrained large language model can serve as the core dynamics predictor in a video world model, grounding visual world-state transitions in text-based world knowledge and enabling free-form natural-language action conditioning across arbitrary domains
- Causal Swin-DPM: sliding temporal window denoising mechanism enabling coherent long-horizon video simulation — operates on fuzzy partially-noised representations of prior chunks rather than sharp single frames, suppressing error propagation between sequential generation steps

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/diffusion-transformer|Diffusion Transformer]]
- [[entities/flow-matching|Flow Matching]]
- [[entities/teacher-forcing|teacher forcing]]
