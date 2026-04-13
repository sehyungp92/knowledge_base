---
type: source
title: 'OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation
  Models'
source_id: 01KJV4QZ2D36W4SHVYMB30SQEQ
source_type: paper
authors:
- Gaojie Lin
- Jianwen Jiang
- Jiaqi Yang
- Zerong Zheng
- Chao Liang
published_at: '2025-02-03 00:00:00'
theme_ids:
- creative_content_generation
- generative_media
- multimodal_models
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models

**Authors:** Gaojie Lin, Jianwen Jiang, Jiaqi Yang, Zerong Zheng, Chao Liang
**Published:** 2025-02-03 00:00:00
**Type:** paper

## Analysis

# OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models
2025-02-03 · paper · Gaojie Lin, Jianwen Jiang, Jiaqi Yang, Zerong Zheng, Chao Liang
https://arxiv.org/pdf/2502.01061v1

---

### Motivation & Prior Limitations
- Existing end-to-end audio-driven human animation models cannot scale up the way general video generation models (e.g., DiT-based text-to-video) have, because they require heavily filtered training data that discards the vast majority of available video.
  - State-of-the-art methods report retaining less than 10% of raw data after filtering for lip-sync accuracy and pose stability, making direct dataset scaling cost-ineffective.
  - Prior methods are restricted to narrow scenarios: typically front-facing portraits or half-body shots with static backgrounds, fixed aspect ratios, and limited input styles.
- Most existing full-body audio-driven methods require a two-stage hybrid strategy (using gesture sequences as a strong auxiliary condition) to manage hand quality, rather than true end-to-end generation.
  - CyberHost attempts one-stage audio-driven body generation via codebook design, but the field broadly has not demonstrated scaling-law behavior analogous to LLMs, VLMs, or T2I/T2V models.
- Human animation models have remained small in both data scale (generally under 1,000 hours) and model size (generally under 2B parameters), with no prior work systematically investigating scaling effects in this domain.

---

### Proposed Approach
- OmniHuman is a Diffusion Transformer (MMDiT)-based framework that enables data scaling for human animation by training with mixed motion-related conditions — text (weak), audio (medium), and pose (strong) — simultaneously rather than filtering data down to a single-condition regime.
  - This contrasts with prior work that trains exclusively on audio-conditioned data and discards everything that fails lip-sync or stability filters; OmniHuman repurposes that discarded data under weaker conditions (text/image-to-video), allowing 18.7K hours of in-house data to be used, of which only 13% meets the stricter audio+pose criteria.
- Two core training principles govern the omni-conditions strategy: (1) tasks with stronger conditioning can leverage weaker-conditioned tasks and their data to scale up training; (2) the stronger the condition, the lower its training ratio should be, to prevent the model from overfitting to the stronger signal and neglecting weaker ones.
  - Training proceeds in three stages: Stage 1 uses text+image-to-video on the broadest data; Stage 2 adds audio; Stage 3 adds pose. Training ratios are progressively halved for stronger conditions (text 90%, audio 50%, pose 25% in the final stage).
- For condition injection, audio features are extracted via wav2vec and injected into every MMDiT block through frame-wise cross-attention; pose is encoded via a pose guider and concatenated channel-wise with noisy latents; reference image appearance conditioning reuses the denoising DiT backbone itself (no parallel reference network), with 3D RoPE temporal components zeroed for reference tokens to distinguish them from video tokens.
  - This minimalist design avoids duplicating the full backbone (as prior reference network approaches do), keeping extra parameters minimal and maximizing multimodal interaction within shared weights.

---

### Results & Capabilities
- OmniHuman outperforms all compared audio-driven portrait and body animation baselines across nearly all metrics on CelebV-HQ, RAVDESS, and CyberHost test sets using a single unified model.
  - On portrait animation (CelebV-HQ), OmniHuman achieves Sync-C of 5.199 and FID of 31.435, versus the next-best Loopy at Sync-C 4.849 and FID 33.204. On RAVDESS, Sync-C reaches 5.255 vs. Loopy's 4.814.
  - On body animation (CyberHost test set), OmniHuman achieves HKV of 47.561 (hand motion richness) and HKC of 0.898, compared to CyberHost's 24.733 HKV and 0.884 HKC — roughly doubling gesture richness while also improving hand quality.
- On pose-driven animation, OmniHuman also surpasses dedicated pose-driving methods (DisCo, AnimateAnyone, MimicMotion, CyberHost) despite being a unified multi-condition model: FVD of 7.3184 and AKD of 2.136 vs. CyberHost's 7.7178 FVD and 3.123 AKD.
- OmniHuman is the first reported method to support audio-driven human animation for input images of any aspect ratio and body proportion (face close-up, portrait, half-body, full-body) in a single model, and handles both speech and singing, human-object interactions (e.g., playing instruments, holding objects), stylized and cartoon characters, and diverse image styles.
  - The hybrid-driven training (IAP) decouples hand movement from audio, reducing excessively exaggerated hand motion and improving naturalness compared to audio-only models (IA).

---

### Implications
- The omni-conditions training paradigm demonstrates that the data scarcity bottleneck in human animation is not fundamental but is an artifact of single-condition filtering; mixing condition strengths allows the field to exploit the same large-scale data strategies that drove progress in T2V and LLMs.
- A unified model handling audio-driven, pose-driven, and combined driving across all body proportions and image styles substantially lowers the barrier for real-world deployment, replacing the current ecosystem of narrow, scenario-specific models.
- The finding that weaker conditions (text) improve stronger-condition performance (lip-sync, gesture quality) when data is scaled suggests a general principle for multimodal generative training: condition hierarchy and training ratio scheduling may be more important than raw data volume for specialised generation tasks.
- The reference image conditioning approach — reusing the denoising backbone with modified RoPE rather than a parallel reference network — provides a parameter-efficient blueprint for appearance conditioning that scales with model size, relevant to both video

## Key Claims

1. Existing end-to-end audio-driven human animation methods struggle to scale up as large general video generation models, limiting their potential in real applications.
2. Most existing end-to-end audio-driven models are limited to facial or portrait images captured from a front-facing perspective with a static background.
3. After rigorous data cleaning for audio-conditioned human animation, less than 10% of the raw data is retained by recent state-of-the-art methods.
4. Incorporating multiple conditioning signals beyond audio (such as text and pose) during training can significantly reduce data wastage in human animation model training.
5. OmniHuman is the first solution capable of audio-driven human video generation on input images with any body proportions and image styles, with auxiliary pose driving support.
6. Scaling effects in human animation have not been effectively investigated prior to OmniHuman.
7. Existing human animation methods typically focus on limited-scale datasets generally less than a thousand hours and 2B parameters.
8. OmniHuman's omni-conditions training follows Principle 1: tasks with stronger conditioning can leverage weaker conditioned tasks and their data to scale up training.
9. OmniHuman's omni-conditions training follows Principle 2: the stronger the conditioning signal, the lower its training ratio should be.
10. OmniHuman uses a minimalist design principle for condition injection, aiming to minimize modality-specific parameters so that multimodal interactions are modeled within the shared MMDiT backbone.

## Capabilities

- Single unified DiT-based model generates realistic audio-driven human animation supporting arbitrary body proportions (face close-up, portrait, half-body, full-body), aspect ratios, and image styles — first model to achieve this
- Multi-condition human video generation from a single unified model supporting audio, pose, and text as interchangeable or combined driving signals at inference time
- Omni-conditions training strategy enabling data-scalable human animation by routing otherwise-discarded video through weaker conditioning branches (text), recovering large-scale motion priors from data that previously failed lipsync filtering
- Significantly improved hand/gesture quality and naturalness in audio-driven full-body animation, with hand keypoint variance (HKV) of 47.561 vs 24.733 for prior SOTA CyberHost — nearly 2x motion richness improvement
- Cross-style human animation supporting stylized, cartoon, anime, and non-human characters with anthropomorphic motion generation driven by audio

## Limitations

- Audio-driven animation still produces uncoordinated or overly expressive body movements due to fundamental weak correlation between audio signal and full-body pose
- Object interaction generation is unrealistic when reference image differs significantly from training distribution
- High CFG scale required for synthesis stability introduces overfitting to audio variations, trading expressiveness for coherence
- Human animation training requires discarding over 90% of raw video data due to strict lipsync accuracy and stability filtering — direct dataset scaling is highly cost-ineffective
- Human animation models have not demonstrated scaling law behavior — unlike LLMs, VLMs, and text-to-image models, increasing data/compute does not yield predictable performance gains in this domain
- Training at this scale requires 400 A100 GPUs running approximately 10 days per training phase — compute cost that prevents academic replication and limits iteration speed for the research community
- System depends entirely on proprietary in-house 18.7K-hour training dataset — results are non-reproducible and dependent on data access unavailable to the broader research community
- Only 13% of training data qualifies for audio and pose conditioning — the vast majority of video footage cannot directly train the core audio-driven animation task even in this expanded framework
- Audio conditioning provides virtually no signal about background motion, camera movement, or lighting changes — these must be handled by other conditions or simply left uncontrolled
- Prior existing methods are all limited to specific body proportions (portrait or half-body) with fixed input sizes — general body proportion handling was a longstanding unsolved problem before this work
- Introducing pose conditioning too early in training degrades overall generation quality — training order sensitivity creates a fragile training recipe that is likely to fail if not carefully tuned

## Bottlenecks

- Strict audio-lipsync filtering discards over 90% of raw video data, making dataset scaling for human animation prohibitively inefficient — unlike LLMs or image models, human animation cannot simply train on more data
- Human animation has not achieved scaling law behavior — systematic improvement via scaled compute and data is not demonstrated, unlike LLMs, VLMs, and T2I/T2V models where scaling recipes are well-understood
- Weak audio-to-full-body-motion correlation creates fundamental ambiguity in audio-driven gesture generation — audio encodes phonemes and prosody but provides almost no information about body kinematics

## Breakthroughs

- Omni-conditions training demonstrates first successful data scaling for human animation — mixing weak (text) and strong (audio, pose) conditioning signals enables leveraging of previously-discarded video data, producing the first single model handling arbitrary body proportions and image styles

## Themes

- [[themes/creative_content_generation|creative_content_generation]]
- [[themes/generative_media|generative_media]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/diffusion-transformer-dit|Diffusion Transformer (DiT)]]
- [[entities/fid|FID]]
- [[entities/fvd|FVD]]
