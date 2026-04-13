---
type: source
title: Latent Action Pretraining from Videos
source_id: 01KJV7DD3SM8YFQ5FA54VAY8AJ
source_type: paper
authors:
- Seonghyeon Ye
- Joel Jang
- Byeongguk Jeon
- Sejune Joo
- Jianwei Yang
- Baolin Peng
- Ajay Mandlekar
- Reuben Tan
- Yu-Wei Chao
- Bill Yuchen Lin
- Lars Liden
- Kimin Lee
- Jianfeng Gao
- Luke Zettlemoyer
- Dieter Fox
- Minjoon Seo
published_at: '2024-10-15 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- pretraining_and_scaling
- robotics_and_embodied_ai
- robot_learning
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Latent Action Pretraining from Videos

LAPA introduces the first unsupervised method for pretraining Vision-Language-Action models from raw video without any ground-truth robot action labels. By learning discrete latent action representations via a VQ-VAE objective, it unlocks internet-scale human video as a training source for robotics foundation models — and surpasses the supervised state-of-the-art (OpenVLA) on real-world manipulation despite never seeing a robot action label during pretraining.

**Authors:** Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, Lars Liden, Kimin Lee, Jianfeng Gao, Luke Zettlemoyer, Dieter Fox, Minjoon Seo
**Published:** 2024-10-15
**Type:** Paper
**Source:** https://arxiv.org/pdf/2410.11758

---

## Motivation

The fundamental bottleneck in [[themes/vision_language_action_models|Vision-Language-Action]] (VLA) model development has been data: every prior approach required ground-truth robot action labels collected via expensive human teleoperation. OpenVLA, the state-of-the-art supervised VLA, used 970k demonstrations from the Open X-Embodiment Dataset — almost entirely teleoperated. This is costly, hardware-dependent, and structurally unscalable.

Internet video offers abundant human behavioral and physical interaction data at orders-of-magnitude greater scale, but two problems block its use:
1. **No explicit action labels** — web video carries no end-effector positions, joint angles, or control signals.
2. **Distribution gap** — embodiments and environments in web video are fundamentally different from robotic systems.

Prior attempts to extract signal from unlabeled video (visual affordances, hand pose retargeting, IDMs on world model rollouts) were task-specific, required aligned human-to-robot data, or needed labeled data to train the IDM itself. LAPA removes all these constraints.

---

## Approach

LAPA is a three-stage pipeline operating entirely without action priors during pretraining.

### Stage 1 — Latent Action Quantization

An encoder-decoder model with a VQ-VAE objective takes pairs of frames $(x_t, x_{t+H})$ and learns discrete latent action tokens $z_t$ representing the "delta" between consecutive observations. No action priors are used — no end-effector positions, no joint angles.

The architecture is a modified **C-ViViT tokenizer** with spatial-temporal transformer encoder and spatial-only transformer decoder. Crucially, cross-attention (rather than additive embedding as used in GENIE) conditions $z_t$ on $x_t$, yielding more semantically meaningful latent actions.

Two training stability measures are applied:
- **NSVQ** replaces standard VQ-VAE vector quantization error to prevent gradient collapse.
- **Codebook replacement** is applied during early training to maximize codebook utilization.
- **Stop gradient** on patch embeddings of $x_t$ during decoding prevents representation collapse.

### Stage 2 — Latent Pretraining

The Stage 1 encoder labels all unlabeled video frames with latent action tokens. A pretrained 7B VLM (LWM-Chat-1M) is then trained via behavior cloning to predict $z_t$ from the current image $x_t$ and a language instruction. A separate MLP latent action head (vocab size $|C|$) replaces the standard LM head; the vision encoder is frozen while the language model is unfrozen.

Because no ground-truth actions are needed, any raw video paired with language is valid training data — including internet-scale human manipulation video with no robot involvement. This is the key scaling unlock: the latent tokenization learned in Stage 1 plays the role that byte-pair encoding plays for LLMs.

### Stage 3 — Action Finetuning

The latent action head is discarded and replaced with a new action head. The model is finetuned on a small labeled robot dataset to map VLM internal representations to delta end-effector actions using discretized continuous action bins. This is the only stage requiring robot action labels.

---

## Results

### Simulation (Language Table)

| Setting | LAPA (seen) | LAPA (unseen) |
|---|---|---|
| In-domain | 62.0% | 49.6% |
| Cross-task | 73.2% | 54.8% |
| Cross-environment | 33.6% ± 12.7 | 29.6% ± 12.0 |

LAPA outperforms VPT across all settings and substantially exceeds UNIPI and SCRATCH. The supervised baseline ACTIONVLA achieves 64.8% in cross-environment seen — roughly a 2× gap that persists despite internet-scale pretraining.

### Real-World Tabletop Manipulation

- **+6.22%** over OpenVLA on real-world tasks requiring language conditioning, generalization to unseen objects, and semantic generalization to unseen instructions.
- **>30× greater pretraining efficiency** compared to OpenVLA.
- Training exclusively on **Something-Something v2** (human manipulation video, no robot data) outperforms models pretrained on BridgeV2, one of the largest open-source robotic datasets.

### Neural Simulation

The Stage 1 decoder can function as a generative world model: LAPA predicts a latent action, the decoder synthesizes the next frame, and the loop continues entirely through neural inference — constituting a rudimentary neural simulator for closed-loop rollout evaluation. This capability is demonstrated qualitatively only.

---

## Capabilities

- **Unsupervised latent action discovery** from raw video frame pairs via VQ-VAE, enabling robot policy pretraining with zero ground-truth action labels. (maturity: research only)
- **Internet-scale video pretraining** that surpasses supervised VLA baselines (OpenVLA, trained on 970k teleoperated demos) on real-world manipulation. (maturity: research only)
- **Cross-embodiment transfer** from human manipulation video to robot tasks, suggesting physical interaction priors are partially embodiment-agnostic. (maturity: research only)
- **Unified quantized latent action representations** learned end-to-end across diverse robotic embodiments without per-embodiment priors. (maturity: research only)
- **Neural closed-loop rollout simulation** using the latent action quantization decoder as a world model. (maturity: research only, qualitative only)

---

## Limitations & Open Questions

### Fundamental Constraints
- **Finetuning requirement is irreducible (currently).** Latent actions are not executable on real robots — a supervised finetuning stage on labeled robot trajectories is always required. Fully label-free robot policy learning from web video remains unachieved.
- **Embodiment gap is reduced, not closed.** Web video distribution is "fundamentally different from the embodiments and environments of typical robotic systems." The ~2× cross-environment generalization gap versus supervised baselines confirms this gap persists.

### Generalization Gaps
- **Cross-environment generalization deficit.** 33.6% vs ACTIONVLA's 64.8% in cross-environment seen scenarios — the hardest regime — indicates internet-scale pretraining has not solved environment-level transfer. This blocks reliable deployment on diverse robots without environment-specific finetuning.
- **Real-world evaluation scope is narrow.** All real-world results come from a single robot (Franka Panda) in tabletop settings across only 3 tasks. Cross-embodiment real-world generalization is not demonstrated.

### Reliability Concerns
- **High performance variance.** Standard errors up to ±12.7pp on means of ~33% indicate significant evaluation instability. Deployment reliability is unverified.
- **Simulation data bias.** SIMPLER simulation finetuning data is collected from another VLA model's successful rollouts (not human teleoperation), which may inflate simulation benchmark performance.

### Practical Deployment Gaps
- **Inference latency is never discussed.** No evidence that a 7B parameter VLA backbone can operate at typical robot control frequencies (10–50 Hz).
- **Full finetuning required.** Parameter-efficient methods (LoRA, adapters) are not applied and left as future work — full 7B parameter finetuning per downstream task creates cost barriers.
- **Temporal context is minimal.** Only two consecutive frames are used as context due to computational constraints. Multi-step manipulation requiring temporal memory is limited.

### World Model Qualification
- **Neural simulation is qualitative only.** No quantitative evaluation of rollout fidelity, frame quality, or closed-loop evaluation accuracy is provided.
- **Video diffusion generalization cliff.** The UNIPI baseline (video diffusion pretraining) fails for longer-horizon tasks, indicating video generative pretraining approaches have a planning horizon ceiling unrelated to LAPA's latent approach.

---

## Bottlenecks Addressed & Remaining

**Partially resolved:** The action-label bottleneck in [[themes/pretraining_and_scaling|VLA pretraining]] is solvable via learned latent tokenization. Internet-scale video is now a viable — and competitive — data source for robotics foundation model pretraining, analogous to how text tokenization enabled LLM scaling.

**Still blocking:**
1. **Labeled finetuning remains mandatory.** Even with unsupervised pretraining, downstream robot deployment requires labeled trajectories. Fully eliminating human teleoperation from the pipeline is a 1–2 year horizon problem.
2. **Cross-environment/embodiment transfer.** Reliable generalization across environments and embodiments from video-pretrained policies without environment-specific finetuning remains ~50% below supervised baselines — a 3–5 year horizon problem.

---

## Key Breakthrough

LAPA is the first demonstration that VLA models pretrained entirely without robot action labels — using only unsupervised latent action discovery from video — can surpass the best supervised VLA baselines on real-world manipulation tasks. This result breaks the assumed equivalence between data quality (teleoperated labels) and pretraining effectiveness, opening a path toward internet-scale [[themes/robotics_and_embodied_ai|robotics foundation model]] pretraining.

---

## Connections

- **[[themes/vision_language_action_models|Vision-Language-Action Models]]** — LAPA is a direct contribution to this space, extending VLA pretraining to unlabeled video.
- **[[themes/pretraining_and_scaling|Pretraining and Scaling]]** — The latent tokenization framing is explicitly analogous to BPE for LLMs; the scaling argument is central to the paper's thesis.
- **[[themes/robotics_and_embodied_ai|Robotics and Embodied AI]]** — Real-world evaluation and cross-embodiment transfer are the primary empirical targets.
- **[[themes/robot_learning|Robot Learning]]** — The unsupervised discovery of action representations connects to imitation learning and inverse dynamics model literature.
- **[[themes/finetuning_and_distillation|Finetuning and Distillation]]** — Stage 3 action finetuning is a structured knowledge transfer from latent to executable action space.
- **[[themes/post_training_methods|Post-Training Methods]]** — The three-stage pipeline (pretraining → latent pretraining → action finetuning) follows a post-training alignment structure.

## Key Concepts

- [[entities/genie|Genie]]
- [[entities/open-x-embodiment-dataset|Open X-Embodiment Dataset]]
- [[entities/vq-vae|VQ-VAE]]
