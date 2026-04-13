---
type: source
title: 'CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models'
source_id: 01KJV26GZXW1B6ARRSK37D98ZD
source_type: paper
authors:
- Qingqing Zhao
- Yao Lu
- Moo Jin Kim
- Zipeng Fu
- Zhuoyang Zhang
- Yecheng Wu
- Zhaoshuo Li
- Qianli Ma
- Song Han
- Chelsea Finn
- Ankur Handa
- Ming-Yu Liu
- Donglai Xiang
- Gordon Wetzstein
- Tsung-Yi Lin
published_at: '2025-03-27 00:00:00'
theme_ids:
- chain_of_thought
- generative_media
- reasoning_and_planning
- robotics_and_embodied_ai
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models

**Authors:** Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, Tsung-Yi Lin
**Published:** 2025-03-27 00:00:00
**Type:** paper

## Analysis

# CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models
2025-03-27 · paper · Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang et al. (15 total)
https://arxiv.org/pdf/2503.22020

---

### Motivation & Prior Limitations
- Current vision-language-action (VLA) models primarily learn direct input–output mappings from observations to actions, lacking the intermediate reasoning steps that are crucial for complex manipulation tasks.
  - Existing VLAs inherit strong visual and language understanding from pretrained VLMs but do not leverage the step-by-step reasoning capabilities that have been shown to significantly improve LLM performance on complex tasks.
  - Without intermediate reasoning, prior VLAs exhibit failure modes such as overfitting to visual cues while disregarding language instructions — for example, executing the wrong task when initial states appear visually similar across different LIBERO-Spatial tasks.
- Prior approaches to incorporating intermediate representations into robotics (language descriptions, keypoints, bounding boxes) capture abstracted states but typically require additional pre-processing pipelines and do not exploit the natural availability of future-frame information within robot demonstration datasets.
- Existing VLAs are trained exclusively on action-annotated robot demonstrations, leaving abundant unlabeled video data (e.g., EPIC-KITCHENS, Something-Something V2) unexploited for improving visual understanding and reasoning.

---

### Proposed Approach
- CoT-VLA introduces visual chain-of-thought (CoT) reasoning into VLAs by predicting a subgoal image — a future pixel-space representation of the desired robot state — as an explicit intermediate reasoning step before generating a short action sequence to achieve that goal.
  - Unlike prior CoT-in-robotics work that uses abstract intermediate representations (bounding boxes, keypoints, text plans), CoT-VLA uses full subgoal images sampled from within existing demonstration videos, requiring no additional annotations or preprocessing pipelines.
  - The model operates in two sequential phases: first sampling a subgoal image $\hat{s}_{t+n}$ conditioned on the current observation and language instruction, then sampling an action chunk $\{\hat{a}_t, \ldots, \hat{a}_{t+m}\}$ conditioned on the current observation, instruction, and generated subgoal.
- The system is built on VILA-U, a 7B unified multimodal foundation model capable of both understanding and generating image and text tokens via autoregressive next-token prediction with residual quantization.
  - The subgoal generation step is trained on both robot demonstrations (Open X-Embodiment) and action-less video datasets (EPIC-KITCHENS-100, Something-Something V2), enabling the model to learn visual dynamics and instruction following from far more data than robot demonstrations alone provide.
- CoT-VLA employs a hybrid attention mechanism: causal (autoregressive) attention for text and image token generation, and full attention for action token prediction, allowing all action dimensions across a chunk to interact with each other simultaneously.
  - Action tokens are discretized into 256 bins per dimension, repurposing the 256 least-frequently-used text vocabulary tokens, following OpenVLA; an action chunk size of 10 is used throughout.

---

### Results & Capabilities
- On the LIBERO simulation benchmark, CoT-VLA-7B achieves an average success rate of 81.1%, outperforming OpenVLA fine-tuned (76.5%), Octo fine-tuned (75.1%), and Diffusion Policy (72.4%) across all four task suites (Spatial, Object, Goal, Long).
  - The largest margin appears on LIBERO-Long (69.0% vs. 53.7% for OpenVLA), which requires the longest-horizon sequential task execution, suggesting visual CoT reasoning is especially beneficial for temporally extended tasks.
- On real-world Bridge-V2 experiments with a 6-DoF WidowX arm, CoT-VLA achieves competitive or superior performance to baselines across four generalization categories: 65% visual, 60% motion, 50% semantic, and 70% language grounding, compared to OpenVLA's 75%, 45%, 40%, and 75% respectively.
  - CoT-VLA outperforms SUSIE — a two-stage diffusion-based goal-conditioned approach that generates higher visual quality goal images — on motion (60% vs. 10%) and semantic (50% vs. 20%) generalization, despite SUSIE's superior image generation quality.
- On Franka-Tabletop real-robot experiments with only 10–150 demonstrations per task, CoT-VLA achieves the highest average performance across 6 tasks (3 single-instruction, 3 multi-instruction), with a 17% improvement over the prior state-of-the-art VLA reported by the authors.
- Ablation studies confirm additive contributions from each architectural component: action chunking alone improves over single-action prediction, hybrid attention further improves on top of chunking, and visual CoT reasoning provides the largest additional gain on both LIBERO-Spatial and LIBERO-Goal.
- Pretraining on OpenX augmented with action-less video data yields a 46.7% relative improvement (53.7% → 78.8%) over directly fine-tuning the base VILA-U model on Franka-Tabletop demonstrations.
- A ground-truth goal image substitution experiment shows that using ground-truth rather than generated subgoal images improves absolute success rate by 40% on two out-of-distribution long-horizon tasks, directly quantifying the performance headroom available from better visual reasoning.

---

### Implications
- Visual chain-of-thought reasoning — using predicted future images as intermediate reasoning steps — establishes a new paradigm for VLA interpretability and performance, analogous to how text-based CoT transformed LLM reasoning, and suggests that "thinking visually" before acting is a tractable and scalable direction for robot learning.
- The ability to leverage action-less video datasets (e.g., EPIC-KITCHENS) for pretraining subgoal generation decouples visual reasoning improvement from the 

## Key Claims

1. CoT-VLA outperforms the state-of-the-art VLA model by 17% in real-world manipulation tasks.
2. CoT-VLA outperforms the state-of-the-art VLA model by 6% in simulation benchmarks.
3. CoT-VLA generates subgoal images as intermediate visual reasoning steps before generating action sequences, enabling the model to 'think visually' about how to accomplish a task before acting.
4. CoT-VLA leverages action-less datasets like EPIC-KITCHEN-100 to enhance subgoal image generation ability during training.
5. CoT-VLA uses a hybrid attention mechanism combining causal attention for text and image generation with full attention for action token prediction.
6. CoT-VLA uses action chunking, predicting sequences of actions rather than a single action at each timestep, with a chunk size of 10.
7. CoT-VLA is built on VILA-U, a 7B parameter unified multimodal foundation model capable of understanding and generating text and image tokens.
8. VILA-U encodes images into 16×16×4 discrete tokens using residual quantization with a residual depth of 4, operating at 256×256 resolution.
9. CoT-VLA discretizes each continuous action dimension into 256 bins using the 256 least frequently used tokens in the text tokenizer's vocabulary.
10. CoT-VLA is pretrained on a subset of the Open X-Embodiment dataset with third-person camera views and single-arm end-effector control (7-DoF), augmented with EPIC-KITCHENS and Something-Something V2 a

## Capabilities

- 7B VLA (CoT-VLA) generating pixel-space subgoal images as explicit visual chain-of-thought intermediate reasoning steps before action sequence generation, outperforming prior SOTA by 17% in real-world manipulation and 6% in simulation
- VLA training leveraging action-less human activity video datasets (EPIC-KITCHENS, Something-Something V2) via visual CoT subgoal pretraining, without requiring any action annotations — unlocking abundant non-robot video as training signal
- Hybrid attention VLA architecture combining causal attention for image/text generation with full attention for parallel action token prediction, improving over standard autoregressive action prediction
- VLA achieving 46.7% relative improvement on novel robot setups (53.7% → 78.8%) through two-stage pretraining, enabling adaptation with only 10–150 task demonstrations

## Limitations

- Visual CoT inference introduces 7x latency overhead — generating 256 image tokens before action tokens creates a fundamental real-time control barrier that action chunking only partially mitigates
- Out-of-distribution subgoal generation degrades to near-random performance — on novel tasks CoT-VLA with generated goals achieves only 20%/0% vs 60%/40% with ground-truth goals, a 40% absolute gap revealing that visual imagination is the binding constraint
- Autoregressive image generation produces substantially lower-quality subgoal images than diffusion-based approaches — SUSIE achieves visually superior goal images despite lower task success rates
- Action chunking causes grasping failures and removes high-frequency closed-loop feedback — discontinuous transitions between 10-step chunks prevent corrective reactions mid-chunk
- Current compute constraints prevent generalisation of visual reasoning to entirely new tasks — the approach cannot reliably generate accurate subgoals for task-object combinations absent from pretraining
- Fixed 256×256 image resolution across the entire system constrains fine-grained manipulation — no evidence the system can handle precision tasks requiring spatial detail beyond what low-resolution encoding captures
- Entire evaluation confined to stationary tabletop single-arm setups — no testing on mobile manipulation, multi-arm tasks, dynamic environments, or outside controlled laboratory conditions
- Vision tower frozen throughout training prevents visual representation adaptation to robot-specific domains — any robot-specific visual features that differ from internet pretraining distribution cannot be learned
- Bridge-V2 evaluations use only 10 trials per category — sample size too small to establish statistical reliability of cross-method comparisons, yet results are presented as definitive rankings

## Bottlenecks

- Autoregressive intermediate image generation creates prohibitive inference latency (7x slowdown) for real-time robot control — generating subgoal images before every action chunk is the primary throughput bottleneck in visual CoT VLAs
- Subgoal image generation quality is the binding ceiling on VLA task performance — the demonstrated 40% success gap between generated vs ground-truth goals shows that visual imagination fidelity directly constrains what manipulation tasks can be attempted

## Breakthroughs

- Visual chain-of-thought via pixel-space subgoal generation — integrating subgoal image prediction as an explicit intermediate reasoning step into end-to-end VLAs — demonstrated as effective for closed-loop robot manipulation with a 17% real-world improvement over direct action prediction VLAs
- Action-less human activity video datasets demonstrated as effective pretraining signal for robot manipulation policy visual reasoning via the visual CoT framework — no action annotation required

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/generative_media|generative_media]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/video_and_world_models|video_and_world_models]]
- [[themes/vision_language_action_models|vision_language_action_models]]

## Key Concepts

- [[entities/action-chunking|Action Chunking]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/diffusion-policy|Diffusion Policy]]
- [[entities/libero-benchmark|LIBERO Benchmark]]
- [[entities/open-x-embodiment-dataset|Open X-Embodiment Dataset]]
