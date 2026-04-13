---
type: source
title: 'MindJourney: Test-Time Scaling with World Models for Spatial Reasoning'
source_id: 01KJTNMPQ6X586C0PCRSY62TC5
source_type: paper
authors:
- Yuncong Yang
- Jiageng Liu
- Zheyuan Zhang
- Siyuan Zhou
- Reuben Tan
- Jianwei Yang
- Yilun Du
- Chuang Gan
published_at: '2025-07-16 00:00:00'
theme_ids:
- generative_media
- reasoning_and_planning
- robotics_and_embodied_ai
- spatial_and_3d_intelligence
- test_time_compute_scaling
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# MindJourney: Test-Time Scaling with World Models for Spatial Reasoning

**Authors:** Yuncong Yang, Jiageng Liu, Zheyuan Zhang, Siyuan Zhou, Reuben Tan, Jianwei Yang, Yilun Du, Chuang Gan
**Published:** 2025-07-16 00:00:00
**Type:** paper

## Analysis

# MindJourney: Test-Time Scaling with World Models for Spatial Reasoning
2025-07-16 00:00:00 · paper · Yuncong Yang, Jiageng Liu, Zheyuan Zhang, Siyuan Zhou, Reuben Tan et al. (8 total)
https://arxiv.org/pdf/2507.12508

---

### Motivation & Prior Limitations
- State-of-the-art VLMs perceive 2D images but lack an internal model of 3D dynamics, causing them to fail on tasks as simple as anticipating how a scene looks after an egocentric motion (perspective-shift questions).
  - Benchmarks SpatialRGPT, SAT, COMFORT, and SPAR all document that frontier VLMs underperform on spatial understanding requiring imagination of egocentric movement consequences.
  - GPT-4o scores 60.3% average on SAT-Real — well below what humans achieve on equivalent perspective-shift tasks — illustrating the concrete capability gap.
- Existing test-time scaling approaches for reasoning (best-of-n, guided decoding, MCTS-style tree search) are text-centric and provide no geometry-aware evidence; they cannot compensate for a missing 3D world model because they operate entirely in token space.
- RL-fine-tuned reasoning models such as OpenAI o1 improve chain-of-thought at test time but still score only 74.6% on SAT-Real, indicating that self-reflection alone cannot substitute for grounded 3D simulation.

---

### Proposed Approach
- MindJourney is a training-free, plug-and-play test-time scaling framework that couples a frozen VLM with a controllable video-diffusion world model, enabling the VLM to iteratively explore an imagined 3D scene before answering a spatial question.
  - Unlike prior TTS methods that scale over text chains, MindJourney scales over physically grounded egocentric rollouts: the world model takes a single RGB frame plus a camera-pose trajectory and synthesises a coherent egocentric video, effectively turning a still image into an explorable 3D environment.
  - The action space is a small discrete set {move-forward d, turn-left θ, turn-right θ}; each action is mapped to a relative SE(3) camera-pose transformation, and the video-diffusion model is conditioned on the resulting pose sequence to generate frame-accurate egocentric clips.
- The core search procedure, Spatial Beam Search, alternates question-agnostic trajectory expansion with question-aware VLM pruning across up to n = 3 steps.
  - At each step, every beam node is expanded by up to k = 3 consecutive repetitions of each primitive action (producing ≤3k candidates per node), all rendered in one batched world-model call; the search VLM scores each candidate on two axes — exploration utility (s_exp) and answer helpfulness (s_help) — and the top-B by s_exp advance to the next beam while the top-H by s_help are cached in an evidence buffer.
  - After the search terminates, the QA VLM receives the original image plus the buffered multi-view observations and their natural-language trajectory descriptions to produce the final answer; no gradient updates or fine-tuning occur at any stage.
- The authors also train their own world model, Search World Model (SWM), built on Wan2.2-TI2V-5B and trained on a mix of Habitat 2.0 synthetic navigation data (for geometric precision), RealEstate-10K, and DL3DV-10K (for visual diversity), specifically calibrated to the primitive action space used by MindJourney.

---

### Results & Capabilities
- MindJourney delivers an average 7.7% accuracy gain on SAT-Real and 8.0% on SAT-Synthesized across all four tested VLM backends, with the largest single boost exceeding 10 percentage points (GPT-4o on SAT-Real: 60.3% → 70.6%).
  - GPT-4.1 augmented with MindJourney (SWM) reaches 80.6% on SAT-Real, surpassing vanilla o1 (74.6%) without any RL fine-tuning.
  - o1 augmented with MindJourney (SWM) sets a new state of the art at 84.7% on SAT-Real, demonstrating that world-model-driven TTS and RL-based TTS are complementary rather than competing.
- Gains are consistent across all five SAT task categories (ego movement, object movement, action consequence, goal aiming, perspective shifts) and across both synthetic and real image splits, confirming model-agnostic generality.
  - The framework improves performance with two entirely distinct world models (SWM and Stable-Virtual-Camera), ruling out world-model-specific artefacts as the source of gains.
- Ablation studies show that accuracy scales with search depth when the world model's training distribution matches the test scenes, and that the VLM pruning threshold is critical: a lenient threshold (γ = 4) allows low-quality views into the evidence buffer and degrades accuracy, especially on real images where generation fidelity is lower.

---

### Implications
- MindJourney establishes a new axis for test-time compute scaling — over imagined physical observations rather than over text tokens — suggesting that controllable video world models are viable reasoning substrates for spatially grounded tasks, not just content-generation tools.
- The result that world-model TTS outperforms and additively combines with RL-based TTS (o1) implies that the two methods encode largely orthogonal information: RL inductive bias cannot substitute for a physically consistent imaginary workspace, and vice versa; future reasoning systems may benefit from stacking both.
- The plug-and-play, training-free design means any future improvement to video-diffusion world models (longer roll-out consistency, query conditioning, multi-view fusion) would directly and transparently propagate to improved spatial reasoning without retraining the VLM, creating a modular improvement path for embodied AI.
- The framework points toward a general principle for multimodality: VLMs can compensate for missing sensory modalities (here, 3D dynamics) at inference time by delegating to specialist generative models rather than requiring end-to-end retraining on multi-modal corpora.

---

### Remaining Limitations & Next Steps
- The pipeline assumes a single reference image; when a spatial-reasoning query supplies multiple images,

## Key Claims

1. State-of-the-art VLMs struggle with spatial reasoning tasks that require imagining the consequences of egocentric movements, despite performing well on visual recognition and simple spatial problems.
2. VLMs perceive 2D images but lack an internal model of 3D dynamics, which limits their usefulness for embodied agents operating in 3D space.
3. MindJourney achieves an average 7.7% performance boost on the SAT benchmark without any fine-tuning of the VLM.
4. MindJourney is model-agnostic, improving performance across four different VLM backends (GPT-4o, GPT-4.1, InternVL3-14B, o1) and with two distinct world models (SWM and SVC).
5. Controllable video diffusion models function as world models by taking a single RGB frame plus a pose trajectory and synthesizing coherent egocentric video that faithfully follows specified motion.
6. MindJourney outperforms RL-fine-tuned test-time scaling models (OpenAI o1) on the SAT benchmark when using a plain VLM augmented with world-model search.
7. World-model-driven test-time scaling and RL-based test-time scaling provide largely orthogonal information, such that combining them yields the best results.
8. GPT-4o augmented with MindJourney achieves a performance boost of over 10 percentage points on SAT-Real, the largest single-model gain observed.
9. GPT-4.1 augmented with MindJourney surpasses vanilla OpenAI o1 on both SAT-Real and SAT-Synthesized.
10. MindJourney improves mean accuracy by 8.0% on average on SAT-Synthesized across all evaluated VLMs.

## Capabilities

- Training-free test-time scaling framework (MindJourney) coupling frozen VLMs with controllable video world models achieves 7.7% average accuracy improvement on the SAT spatial reasoning benchmark, with largest single gain over 10%, and is model-agnostic across GPT-4o, GPT-4.1, InternVL3-14B, and o1
- Controllable video diffusion models can serve as egocentric world models — given a single RGB frame and a camera pose trajectory, they synthesize coherent multi-frame egocentric video, enabling interactive 3D scene exploration from a still image
- World-model-driven test-time scaling surpasses RL-based test-time scaling (o1) on 3D spatial reasoning without any fine-tuning — plain GPT-4.1 + MindJourney (80.6%) exceeds vanilla o1 (74.6%) on SAT-Real; o1 + MindJourney achieves 84.7% state of the art
- Spatial Beam Search: a question-aware beam search over imagined 3D trajectories alternating between world-model rollout expansion and VLM-guided pruning to accumulate multi-view evidence for spatial reasoning
- World-model test-time scaling and RL-based test-time scaling are orthogonal and additive: combining both (o1 + MindJourney) consistently outperforms either alone, with gains non-redundant across both SAT splits

## Limitations

- State-of-the-art VLMs fundamentally lack an internal model of 3D dynamics — they perceive 2D images but cannot anticipate how a scene changes after egocentric motion, failing on even simple perspective-shift tasks that humans solve effortlessly
- Current world models exhibit a hard performance cliff when imagined trajectories stray far from the reference frame — geometric and photometric consistency degrades, feeding noisy evidence to the VLM and capping the benefits of deeper search (accuracy peaks at 2 steps then declines at step 3 on SAT-
- SWM world model trained predominantly on indoor synthetic Habitat data degrades on outdoor scenes — causing accuracy to peak at 2 search steps on SAT-Real and decline at step 3, while SAT-Synthesized (closer to training distribution) continues improving through step 3
- MindJourney is limited to a single reference view — when spatial reasoning queries supply multiple images, it cannot treat extra views as separate entry points for parallel world model exploration
- Controllable video world models are query-agnostic — they generate views without awareness of the downstream reasoning task, and can hallucinate views irrelevant or contradictory to what the question implicitly assumes
- The trajectory search space grows exponentially with horizon, requiring beam search approximation to remain tractable — full exhaustive search is computationally infeasible, and beam search itself discards potentially useful trajectories
- Lenient pruning thresholds allow low-quality world model views into the evidence buffer, diluting reasoning signal and degrading accuracy — the effect is amplified on real-world images where generation quality is intrinsically lower than on synthetic scenes
- Inference cost of combining world-model beam search with o1 is prohibitive — o1 could only be used as the QA VLM while GPT-4o handled the search phase; full o1 deployment at both stages is computationally intractable for benchmark evaluation
- SAT-Synthesized evaluation required subsampling to 500 of 4000 questions to keep o1 experiments tractable — implying that world-model TTS with strong reasoners is currently too costly for large-scale evaluation or production deployment

## Bottlenecks

- World model long-horizon geometric and photometric consistency is the fundamental bottleneck for deeper test-time search — both SWM and state-of-the-art SVC degrade when trajectories stray far from the reference frame, capping search depth at ~2-3 steps on real scenes
- Query-agnostic video world model generation blocks targeted and efficient spatial reasoning at test time — without conditioning on task semantics, world models waste compute generating irrelevant or contradictory views, requiring heavy VLM-based filtering as a workaround
- VLMs treating images as static 2D representations rather than interactive 3D worlds is a core architectural bottleneck blocking embodied reasoning — external world models partially compensate at test time but do not resolve the fundamental internal representation gap

## Breakthroughs

- First demonstration that world-model-driven test-time scaling provides a complementary, orthogonal axis to RL-based test-time compute — coupling a frozen VLM with a video world model for interactive 3D exploration surpasses RL-tuned o1 on spatial reasoning without any fine-tuning

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/video_and_world_models|video_and_world_models]]

## Key Concepts

- [[entities/test-time-scaling|Test-time Scaling]]
