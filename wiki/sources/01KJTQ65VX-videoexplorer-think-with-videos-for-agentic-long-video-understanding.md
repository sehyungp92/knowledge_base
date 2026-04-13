---
type: source
title: 'VideoExplorer: Think With Videos For Agentic Long-Video Understanding'
source_id: 01KJTQ65VXMV31FEDTS7ZXS8VH
source_type: paper
authors:
- Huaying Yuan
- Zheng Liu
- Junjie Zhou
- Hongjin Qian
- Yan Shu
- Nicu Sebe
- Ji-Rong Wen
- Zhicheng Dou
published_at: '2025-06-12 00:00:00'
theme_ids:
- agent_systems
- long_context_and_attention
- model_architecture
- multimodal_models
- reasoning_and_planning
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# VideoExplorer: Think With Videos For Agentic Long-Video Understanding

**Authors:** Huaying Yuan, Zheng Liu, Junjie Zhou, Hongjin Qian, Yan Shu, Nicu Sebe, Ji-Rong Wen, Zhicheng Dou
**Published:** 2025-06-12 00:00:00
**Type:** paper

## Analysis

# VideoExplorer: Think With Videos For Agentic Long-Video Understanding
2025-06-12 · paper · Huaying Yuan, Zheng Liu, Junjie Zhou, Hongjin Qian, Yan Shu et al. (8 total)
https://arxiv.org/pdf/2506.10821

---

### Motivation & Prior Limitations
- Modern VLMs address long-video understanding (LVU) by heavily downsampling frames and applying single-pass reasoning, which sacrifices fine-grained temporal details and degrades accuracy on hour-long videos containing tens of thousands of raw frames.
  - A video compressed to fit context windows loses the fine-grained evidence needed for multi-hop reasoning — Gemini-1.5-pro and VideoAgent both fail on questions requiring locating NetApp and then tracing backward to the preceding company.
- Agentic retrieval-augmented frameworks (VideoAgent, VideoTree, VideoRAG) mitigate downsampling by preprocessing videos into task-agnostic textual representations (dense captions, object trajectories, audio transitions), but this introduces a different failure mode: task-agnostic preprocessing compresses rich visual signals into generic text, causing irreversible information loss.
  - These frameworks operate on a static, pre-built index (Dv = Γpreprocess(v)) constructed before any query is seen, making it impossible to adaptively perceive the raw video in response to task-specific information needs discovered mid-reasoning.
  - Preprocessing is computationally expensive, limiting practical scalability.
- Existing large reasoning models (Video-R1, and similar RL-trained video models) apply chain-of-thought reasoning but operate solely on statically downsampled frames, meaning the reasoning process itself cannot trigger new perceptual queries to gather missing evidence.

---

### Proposed Approach
- The paper introduces "thinking with video" — a paradigm treating reasoning as a dynamic, temporally grounded process where the model iteratively decides *what* to look for, *where* to look, and *at what temporal scale*, maintaining direct access to the raw video stream throughout reasoning rather than over a static pre-processed context.
  - Formally: Y = Θ(q | {Pt}), where Pt = Φperc(τt) and τt = Γground(qsub_t | v) — perception results are computed on-demand from raw video spans located by a temporal grounder in response to planner-generated sub-questions.
  - This contrasts with prior RAG frameworks where Dv is fixed before inference; here the retrieval index is queried dynamically and visual perception granularity adjusts per sub-task.
- VideoExplorer implements "thinking with video" through three coordinated components: (1) a planner that decomposes tasks into sequential sub-questions and coordinates the reasoning trajectory; (2) a decoupled temporal grounding agent that maps sub-queries to validated temporal spans via segmentation, embedding, retrieval, and VLM-based verification; and (3) a temporal-scalable video understanding module that adjusts frame sampling density based on whether the query requires fine-grained inspection or coarse holistic browsing.
  - The temporal grounder supports both text-only and multimodal queries, and uses VLMs as verifiers to discard irrelevant retrieved segments before passing evidence back to the planner — mitigating hallucination from noise.
  - Decoupling grounding from planning reduces the planner's cognitive load and prevents premature answering before sufficient evidence is gathered.
- Training follows a two-stage pipeline: Stage I is supervised fine-tuning (SFT) on expert reasoning trajectories (11.1k planner + 10.8k grounding trajectories) generated with difficulty-adaptive sampling, where hard cases are re-sampled based on first-round accuracy; Stage II is trajectory-level direct preference optimization (TDPO), which adapts DPO to multi-turn video reasoning by comparing entire reasoning trajectories (chosen vs. rejected) rather than individual responses, rewarding faithful multi-step exploration.
  - Difficulty-adaptive sampling deliberately over-represents challenging cases by re-sampling tasks where the model's first-round accuracy falls below a threshold, ensuring training data is not dominated by trivially solved examples.

---

### Results & Capabilities
- VideoExplorer with a 7B planner and 7B VLM achieves 50.6 on LVBench, 55.4 on MLVU, and 49.1 on MH-NIAH, averaging 51.7 — outperforming all baselines including GPT-4o (48.9/54.9 on LVBench/MLVU) and significantly exceeding the best competing agentic framework Ego-R1 (39.6/40.9/42.3).
  - At the 32B VLM scale, VideoExplorer reaches 51.4/58.6/53.4, averaging 54.5, maintaining its lead over all baselines.
- VideoExplorer achieves substantially higher temporal grounding accuracy than competing agentic frameworks: IoU@0.1 of 27.8 vs. 19.6 for Ego-R1, 16.7 for VideoAgent, and 14.5 for VideoRAG on LVBench, validating that reasoning-aware adaptive grounding is the key driver of QA accuracy gains.
- VideoExplorer uses dramatically fewer visual tokens than competing methods: ~19.6k tokens on LVBench vs. 122.2k for Ego-R1 and 23.0k for VideoAgent, while achieving higher accuracy — demonstrating that selective, on-demand temporal access is more efficient than processing all retrieved segments indiscriminately.
  - On MLVU, VideoExplorer uses ~20.5k visual tokens vs. 61.5k for VideoAgent and 98.3k for Ego-R1.
- Ablation results confirm each component's independent contribution: removing TDPO drops performance by 3.3% on MLVU and 2.1% on MH-NIAH; removing the decoupled temporal grounder drops 2.4% and 1.8%; removing difficulty-adaptive sampling drops 2.1% and 1.5%.

---

### Implications
- The "thinking with video" paradigm establishes a direct parallel to "thinking with images" (adaptive zoom/focus) and extends it to the temporal dimension, suggesting a general principle for multimodal reasoning: models should maintain on-demand access to raw perceptual streams rather than reasoning over lossy pre-processed representations.
- Decoupling the temporal grounding agent from the p

## Key Claims

1. Modern VLMs address long-video input length constraints by heavily downsampling frames and applying single-pass reasoning, which inevitably sacrifices fine-grained details and compromises reasoning ac
2. Agentic frameworks that preprocess video into task-agnostic textual representations (e.g., dense captions, object trajectories) lose rich visual information from original long videos, leading to sub-o
3. Task-agnostic preprocessing for agentic video reasoning is computationally heavy, limiting scalability in practice.
4. Existing large reasoning models for video understanding operate solely on static downsampled video frames, leading to significant information loss in long-video understanding.
5. VideoExplorer introduces the principle of 'thinking with video', which treats reasoning as a dynamic process of temporally grounded exploration, allowing the model to interact directly with the raw vi
6. VideoExplorer's temporal grounder decouples retrieval from the main reasoning chain, supporting both text-only and multimodal queries, and uses VLMs as verifiers to assess whether retrieved segments a
7. VideoExplorer dynamically adjusts frame sampling granularity: dense sampling for fine-grained queries on short segments, and coarse sampling for global tasks covering broader intervals.
8. VideoExplorer's training dataset uses difficulty-adaptive sampling, where tasks are uniformly sampled, hard cases are re-sampled based on first-round accuracy, and only trajectories with correct answe
9. VideoExplorer with a 7B planner and 7B VLM achieves 51.7% average accuracy across LVBench, MLVU, and MH-NIAH, outperforming all agentic baselines and matching GPT-4o on MLVU (55.4 vs 54.9).
10. VideoExplorer achieves an IoU@0.1 temporal grounding accuracy of 27.8 on LVBench, significantly outperforming VideoAgent (16.7), VideoRAG (14.5), and Ego-R1 (19.6).

## Capabilities

- Agentic long-video understanding via iterative raw-video temporal grounding — VideoExplorer decomposes complex queries into sub-questions, dynamically grounds relevant temporal spans on the raw video stream, and adapts perceptual granularity without relying on downsampled frames or preprocessed text
- State-of-the-art temporal grounding from raw long video at IoU@0.1 of 27.8 on LVBench — significantly outperforming prior agentic frameworks (Ego-R1: 19.6, VideoAgent: 16.7, VideoRAG: 14.5)
- Token-efficient long-video reasoning: VideoExplorer uses ~20.5k visual tokens on LVBench vs VideoAgent's 122.2k while achieving 50.6 vs 34.9 accuracy — roughly 6× fewer tokens with 45% better accuracy
- Multi-hop reasoning over hour-long video by iterative query decomposition and temporal evidence localization — correctly answering questions requiring tracing backward from one event to find what preceded it, where Gemini-1.5-Pro, VideoRAG, and VideoAgent all fail
- Trajectory-level direct preference optimization (TDPO) for multi-step video reasoning — evaluating complete reasoning trajectories including intermediate steps rather than individual responses, improving MLVU by 3.3% and MH-NIAH by 2.1% over SFT-only baseline
- Difficulty-adaptive synthetic trajectory generation for long-video reasoning: produces 11.1k planner trajectories and 10.8k grounding trajectories by uniformly sampling tasks, running VideoExplorer, and resampling hard cases based on first-round accuracy

## Limitations

- Hour-long video understanding remains a significant unsolved challenge — all current VLMs, including frontier models (GPT-4o, Gemini-1.5-Pro), struggle with temporal reasoning at multi-hour scale due to context window constraints
- Temporal grounding precision remains extremely low even for state-of-the-art methods — the best reported IoU@0.1 is 27.8, an extremely permissive threshold (any 10% overlap counts), implying precision at standard thresholds (IoU@0.5, IoU@0.7) would be far worse
- Brute-force frame downsampling by single-pass VLMs irreversibly sacrifices fine-grained temporal detail — information discarded during compression cannot be recovered at reasoning time
- Task-agnostic video preprocessing (dense captions, object trajectories, audio transitions) causes irreversible visual information loss — converting video to text before knowing the query cannot preserve task-relevant visual detail
- One-pass retrieval-augmented generation cannot support multi-hop reasoning over long video — a single retrieval step cannot chain evidence across temporally separated segments requiring intermediate inference
- VideoExplorer training dataset is extremely small (11.1k planner + 10.8k grounding trajectories) — generalization beyond benchmark-derived video domains and query distributions is uncharacterized
- Training exclusively on correct-answer trajectories creates a success-only bias — the model never observes reasoning recovery from errors, potentially reducing robustness to novel failure modes
- SFT initialization is fundamentally constrained by teacher-forced demonstrations — the planner learns to mimic expert traces but cannot discover reasoning strategies absent from the training set
- Wall-clock latency of iterative agentic video reasoning is not characterized — multiple rounds of temporal grounding, VLM verification, and segment summarization likely incur substantial real-world latency not captured by token-efficiency metrics
- Planner model size is the binding constraint for multi-hop reasoning quality — scaling the visual encoder from 7B to 32B yields minimal improvement on MH-NIAH with a 3B planner (39.9→40.7), while scaling the planner from 3B to 7B yields large gains (39.9→49.1 at 7B VLM)
- Evaluation limited to academic benchmarks with controlled video types and query formats — real-world deployment across diverse domains (live surveillance, technical tutorials, multi-speaker conferences) is entirely uncharacterized
- Absolute QA accuracy on long-video benchmarks remains modest — best VideoExplorer result is 54.5% average across LVBench/MLVU/MH-NIAH, with LVBench at 51.4% and MH-NIAH at 53.4%, well below human-level performance

## Bottlenecks

- Absence of high-quality multi-step reasoning trajectory datasets for long-video understanding — existing video QA datasets provide only final-answer labels, which are insufficient to train iterative planning and temporal grounding agents
- Temporal grounding precision is insufficient for reliable multi-hop video QA — state-of-the-art systems achieve only IoU@0.1 = 27.8, meaning most retrieved segments have less than 10% overlap with ground-truth intervals, causing cascading evidence errors

## Breakthroughs

- VideoExplorer demonstrates that 'thinking with video' — treating reasoning as dynamic temporal exploration of raw video rather than static frame compression or text-converted preprocessing — substantially outperforms all prior paradigms on long-video understanding benchmarks

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/qwen25-vl|Qwen2.5-VL]]
