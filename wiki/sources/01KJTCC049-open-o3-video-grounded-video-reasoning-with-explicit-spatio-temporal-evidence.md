---
type: source
title: 'Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence'
source_id: 01KJTCC049V0BDGGG66CNH20YT
source_type: paper
authors:
- Jiahao Meng
- Xiangtai Li
- Haochen Wang
- Yue Tan
- Tao Zhang
- Lingdong Kong
- Yunhai Tong
- Anran Wang
- Zhiyang Teng
- Yujing Wang
- Zhuochen Wang
published_at: '2025-10-23 00:00:00'
theme_ids:
- chain_of_thought
- generative_media
- multimodal_models
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence

**Authors:** Jiahao Meng, Xiangtai Li, Haochen Wang, Yue Tan, Tao Zhang, Lingdong Kong, Yunhai Tong, Anran Wang, Zhiyang Teng, Yujing Wang, Zhuochen Wang
**Published:** 2025-10-23 00:00:00
**Type:** paper

## Analysis

# Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence
2025-10-23 · paper · Jiahao Meng, Xiangtai Li, Haochen Wang, Yue Tan, Tao Zhang et al. (11 total)
https://arxiv.org/pdf/2510.20579

---

### Motivation & Prior Limitations
Prior video reasoning models generate textual rationales but cannot indicate *when* or *where* in a video the supporting evidence appears, making their outputs unverifiable and disconnected from visual content.
- Models such as Video-R1 and VideoRFT rely entirely on text-only chain-of-thought outputs, providing no timestamps or bounding boxes to ground their conclusions in the video stream.
  - This creates a transparency and reliability problem: the model may arrive at the correct answer for wrong or hallucinated reasons, with no mechanism for external verification.
- Existing datasets are structurally misaligned with joint spatio-temporal supervision: temporal grounding corpora supply time spans but lack object regions, while spatial/frame-level caption corpora provide bounding boxes on isolated frames without timestamps, and neither typically includes chain-of-thought reasoning traces.
  - This data gap makes it impossible to compute verifiable RL rewards for synchronized spatio-temporal alignment, blocking training of models that localize objects in both time and space simultaneously.
- Image-centric "thinking with images" paradigms (e.g., OpenAI-o3, DeepEyes) cannot transfer directly to video because video adds temporal consistency, motion, occlusions, camera changes, and the requirement to pinpoint *when* events occur alongside *where* objects are.
- A critical training instability — spatial collapse — arises when reinforcement learning is naively applied: spatial rewards are conditioned on accurate temporal predictions, so early temporal imprecision produces near-zero spatial rewards, stalling localization learning entirely.

---

### Proposed Approach
Open-o3 Video is a non-agent, single-model framework that embeds explicit spatio-temporal evidence (timestamped key frames and localized bounding boxes) directly into the chain-of-thought reasoning trace, producing outputs in a structured `<think>…<obj><box><t>…</think><answer>` format.
- Unlike agent-based approaches such as VITAL, which rely on external tool pipelines for visual operations, Open-o3 Video emits timestamped crops and bounding boxes as inline evidence within a single model forward pass.
- Two complementary training datasets were curated: STGR-CoT-30k for supervised fine-tuning (SFT) and STGR-RL-36k for reinforcement learning (RL), combining existing temporal-only and spatial-only resources with 5.9k newly annotated spatio-temporal samples generated via a three-stage pipeline (Gemini 2.5 Pro annotation → bounding box filtering via Qwen2.5-VL-7B verification → self-consistency checking).
- Training proceeds in two stages: cold-start SFT on STGR-CoT-30k to establish structured grounded output formats, followed by reinforcement learning using Group Sequence Policy Optimization (GSPO), which computes importance ratios and clipping at the sequence level rather than the token level, providing more stable long-horizon optimization than GRPO.
- The reward function combines an accuracy term (task-specific: exact match for MCQ, ROUGE for free-form QA, visual IoU for spatial grounding, temporal IoU for temporal grounding), a thinking reward, and a format reward. The thinking reward incorporates two novel mechanisms: (1) *adaptive temporal proximity*, which uses a Gaussian proximity function with a large σ early in training that gradually tightens, providing dense initial gradients while enforcing precision later; and (2) *temporal gating*, which conditions spatial reward computation on whether the predicted timestamp falls within a threshold τ of ground truth, preventing incorrectly timed but visually salient objects from being rewarded.

---

### Results & Capabilities
On the V-STAR benchmark — specifically designed to evaluate joint spatio-temporal grounding — Open-o3 Video achieves state-of-the-art results, surpassing both proprietary and open-source baselines.
- Compared to the Qwen2.5-VL-7B baseline, Open-o3 Video improves mAM by +14.4% and mLGM by +24.2%, and outperforms GPT-4o and Gemini-2-Flash on overall V-STAR metrics despite being a 7B open-source model.
- On general video understanding benchmarks, the model achieves consistent gains over Qwen2.5-VL-7B: +1.2% on VideoMME overall (+4.1% on long videos), +1.4% on WorldSense (+3.1% on recognition), +1.1% on VideoMMMU (+3.3% on perception), and +4.5 mIoU on TVGBench temporal grounding.
- Ablations confirm that the combination of SFT and GSPO-based RL is synergistic and superior to either alone: SFT+RL(GSPO) reaches 33.7% mAM / 46.6% mLGM versus 28.5/37.1 for pure SFT and 30.4/40.7 for pure RL, with GSPO further outperforming GRPO by +0.9% mAM and +1.3% mLGM.
- Removing adaptive temporal proximity degrades performance by −0.7% mAM / −1.4% mLGM; removing temporal gating causes larger drops of −1.4% mAM / −1.7% mLGM, confirming that gating is the more critical of the two mechanisms.
- The grounded evidence traces enable *confidence-aware voting* at test time, outperforming naive majority voting by +1.2% on WorldSense and +1.0% on VideoMMMU, demonstrating that spatio-temporal evidence provides a reliable self-verification signal for inference-time scaling.

---

### Implications
Grounding reasoning traces in timestamped frames and bounding boxes transforms video QA from an opaque text prediction task into a verifiable, evidence-linked inference process — directly relevant to trust, interpretability, and downstream use of video reasoning models in high-stakes applications.
- The cold-start + RL training recipe with adaptive reward shaping (progressive temporal proximity + gating) establishes a generalizable template for any multimodal task where one localization dimension (temporal) must be learned before another (spatial) can b

## Key Claims

1. Most video reasoning models only generate textual reasoning traces without indicating when and where key evidence appears in the video.
2. Extending evidence-centered image reasoning to video is substantially more difficult than for images because it requires coherent localization across both time and space simultaneously.
3. Previous attempts to incorporate explicit reasoning in video have been limited to textual rationales or coarse temporal-only grounding, failing to achieve fine-grained spatio-temporal precision.
4. The absence of high-quality datasets providing joint spatio-temporal supervision and the difficulty of training precise simultaneous temporal and spatial localization are the two interconnected obstac
5. A spatial collapse issue occurs during RL training when spatial grounding rewards are conditioned on correct temporal identification: imprecise temporal predictions in early stages lead to near-zero s
6. Open-o3 Video achieves state-of-the-art performance on V-STAR, improving mAM by +14.4% and mLGM by +24.2% over the Qwen2.5-VL-7B baseline.
7. Open-o3 Video surpasses closed-source commercial models GPT-4o and Gemini-2-Flash on the V-STAR spatio-temporal reasoning benchmark.
8. Open-o3 Video achieves a +27.5 percentage point improvement in QA accuracy (the 'What' dimension) over Qwen2.5-VL-7B on V-STAR.
9. Grounded evidence traces from Open-o3 Video enable confidence-aware voting at test time, which surpasses majority voting by +1.2% on WorldSense and +1.0% on VideoMMMU.
10. Reinforcement learning outperforms pure supervised fine-tuning for spatio-temporal grounding, with +2.1% mAM and +4.6% mLGM improvements.

## Capabilities

- A 7B VLM trained via SFT+GSPO can produce reasoning traces with explicit timestamps and bounding boxes, grounding answers in concrete spatio-temporal evidence from video — achieving state-of-the-art on V-STAR (+14.4% mAM, +24.2% mLGM over Qwen2.5-VL-7B) and surpassing GPT-4o on spatio-temporal groun
- Confidence-aware voting using grounded spatio-temporal evidence as a self-verification signal outperforms naive majority voting at test time, enabling evidence-aware test-time scaling for video reasoning (+1.2% on WorldSense, +1.0% on VideoMMMU)
- Adaptive temporal proximity reward scheduling combined with temporal gating enables stable joint spatio-temporal RL training: loose temporal constraints early provide dense rewards, tightening progressively while spatial rewards are only computed when temporal predictions meet a threshold
- GSPO (Group Sequence Policy Optimization) provides more stable RL training than GRPO for long-horizon video reasoning with composite rewards by operating at the sequence level, eliminating high-variance token-wise corrections (+0.9% mAM, +1.3% mLGM, +2.9% Chain1 tIoU over GRPO)
- Cold-start SFT on 30k grounded reasoning traces followed by GSPO-based RL provides strongly synergistic gains for video spatio-temporal grounding (33.7% mAM) over either pure SFT (28.5%) or pure RL (30.4%) alone

## Limitations

- Video reasoning models are limited to processing a small fixed number of frames (16 per video with resolution capped at 128×28×28), creating a hard ceiling on temporal resolution that makes fine-grained localization in long or fast-paced videos structurally impossible with the current approach
- Joint spatio-temporal RL training suffers a spatial collapse failure mode: when temporal predictions are imprecise early in training, spatial rewards collapse to near-zero, stalling localization learning entirely — requiring specialized curriculum mechanisms to overcome
- Despite achieving state-of-the-art, spatial grounding (visual IoU) remains extremely weak in absolute terms — 6.0% on Chain2 (what-where-when ordering) and 25.4% on Chain1 even for the best model — revealing that fine-grained object localization in dynamic video is far from solved
- Spatial grounding improvements on Chain2 (what-where-when) are substantially smaller than Chain1 (what-when-where) — 3.5% vs 8.4% gain — indicating the model is brittle to reasoning chain ordering and has not learned robust spatio-temporal integration
- The data annotation pipeline for joint spatio-temporal reasoning data requires heavy external model involvement (Gemini 2.5 Pro API) plus multi-stage filtering, making large-scale dataset construction expensive and not self-contained — only 5.9k new samples could be produced
- Existing video datasets entirely lack unified spatio-temporal supervision: temporal-only datasets provide time spans without object regions; spatial datasets provide boxes on isolated frames without timestamps; almost none include reasoning chains linking both to answers
- Long video understanding, while improved, remains substantially below short-clip performance — 54.9% on VideoMME Long vs 63.6% overall — revealing that temporal reasoning over extended durations hits architectural limits with 16-frame subsampling
- The framework has not been tested on real-world video with adversarial conditions (motion blur, severe occlusion, rapid camera pans) — all evaluation is on curated benchmark datasets, with the paper explicitly acknowledging these challenges remain open
- Inference cost of generating grounded reasoning traces is not analyzed anywhere in the paper — no discussion of latency, token count increase, or computational overhead vs. standard video QA models, making production viability assessment impossible
- The cold-start SFT phase is essential for stable RL — without it RL training fails to converge — meaning the two-stage pipeline is not simplifiable to pure RL from a base model and requires a large supervised corpus as a prerequisite
- The approach does not extend to audio modality, leaving cross-modal reasoning across text, time, space, and audio as explicitly unresolved future work

## Bottlenecks

- The absence of training datasets providing unified spatio-temporal supervision — where temporal keyframes, spatial bounding boxes, and reasoning chains are jointly annotated — blocks training of video models that ground reasoning in verifiable visual evidence
- The spatial collapse problem in joint spatio-temporal RL — where cascaded reward dependency causes near-zero spatial rewards when temporal predictions are imprecise — blocks stable end-to-end RL training for any task requiring multi-level grounding hierarchies

## Breakthroughs

- Open-o3 Video demonstrates that a single non-agent 7B VLM can be trained via SFT+GSPO to produce joint spatio-temporal evidence (timestamps + bounding boxes) embedded in its chain-of-thought, achieving state-of-the-art and surpassing GPT-4o on spatio-temporal grounding without external tool pipeline
- Adaptive temporal proximity + temporal gating resolve the spatial collapse problem in joint spatio-temporal RL training, providing a general curriculum mechanism for stable optimization of hierarchically dependent composite reward signals

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/generative_media|generative_media]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/video_and_world_models|video_and_world_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/cold-start-initialization|Cold-Start Initialization]]
- [[entities/qwen25-vl-7b|Qwen2.5-VL-7B]]
