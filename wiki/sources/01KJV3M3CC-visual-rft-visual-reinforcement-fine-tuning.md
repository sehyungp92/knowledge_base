---
type: source
title: 'Visual-RFT: Visual Reinforcement Fine-Tuning'
source_id: 01KJV3M3CCRCTJ0M3XV0TM1W6Y
source_type: paper
authors:
- Ziyu Liu
- Zeyi Sun
- Yuhang Zang
- Xiaoyi Dong
- Yuhang Cao
- Haodong Duan
- Dahua Lin
- Jiaqi Wang
published_at: '2025-03-03 00:00:00'
theme_ids:
- multimodal_models
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 15
tags: []
---
# Visual-RFT: Visual Reinforcement Fine-Tuning

**Authors:** Ziyu Liu, Zeyi Sun, Yuhang Zang, Xiaoyi Dong, Yuhang Cao, Haodong Duan, Dahua Lin, Jiaqi Wang
**Published:** 2025-03-03 00:00:00
**Type:** paper

## Analysis

# Visual-RFT: Visual Reinforcement Fine-Tuning
2025-03-03 · paper · Ziyu Liu, Zeyi Sun, Yuhang Zang, Xiaoyi Dong, Yuhang Cao et al. (8 total)
https://arxiv.org/pdf/2503.01785

---

### Motivation & Prior Limitations
- Supervised Fine-Tuning (SFT) for Large Vision-Language Models (LVLMs) is data-hungry, requiring large amounts of high-quality curated data to imitate ground-truth answers, making it poorly suited for domain-specific tasks where labeled data is scarce.
  - In the one-shot fine-grained classification setting (~100 samples), SFT actually *dropped* accuracy by 4.3% relative to the baseline, demonstrating active harm from data-starved SFT.
- Reinforcement Fine-Tuning (RFT) as demonstrated by DeepSeek-R1 and OpenAI o1 had been confined almost exclusively to language-only tasks with clear objective answers (mathematics, code), because those domains make reward verification straightforward.
  - The challenge of defining verifiable, rule-based rewards for visual perception tasks (e.g., object detection, grounding) had not been systematically addressed, leaving the multimodal domain largely unexplored.
- Separate reward models trained on preference data (RLHF-style) introduce additional complexity and data requirements, and are less scalable than rule-based verifiable rewards in low-data regimes.

---

### Proposed Approach
- Visual-RFT extends Reinforcement Fine-Tuning to multimodal visual perception tasks by designing task-specific, rule-based verifiable reward functions that can score LVLM outputs without a separate reward model.
  - Unlike SFT, which optimizes via imitation of ground-truth labels, Visual-RFT samples multiple reasoning trajectories per input and updates the policy (via Group Relative Policy Optimization, GRPO) based on reward scores derived from rule-defined correctness criteria.
  - For object detection, the key reward design is an Intersection over Union (IoU) reward that directly scores predicted bounding boxes against ground truth; for classification tasks, an exact-match classification reward is used. This shifts the training bottleneck from data scaling to reward function engineering.
- The model generates responses containing explicit reasoning tokens (in `<think>...</think>` tags) followed by structured final answers, enabling the model to develop chain-of-thought visual reasoning as a byproduct of the reward-optimization process.
  - The base model used is Qwen2-VL-2B, a relatively small LVLM, demonstrating that the paradigm is accessible without frontier-scale compute.
- The training paradigm is applied across four distinct task types: fine-grained few-shot image classification, few-shot object detection, open-vocabulary object detection, and reasoning grounding — demonstrating reward-function generality across perception modalities.

---

### Results & Capabilities
- In one-shot fine-grained image classification (~100 training samples), Visual-RFT improves accuracy by 24.3% over the baseline, while SFT degrades by 4.3%, demonstrating a stark data-efficiency advantage in the extreme low-data regime.
  - In 4-shot classification, Visual-RFT achieves improvements ranging from +4.2% (Pets37) to +38.5% (Aircraft) across five fine-grained datasets, outperforming the SFT baseline across all categories.
- In few-shot object detection on COCO, Visual-RFT exceeds the SFT baseline by 21.9 mAP on the two-shot setting; on LVIS (a long-tail detection benchmark), it exceeds SFT by 15.4 mAP.
  - These gains are notable because LVIS contains rare and long-tail categories, suggesting Visual-RFT's reward-driven exploration generalizes better to novel concepts than label imitation.
- On open-vocabulary (OV) object detection benchmarks (COCO and LVIS), Visual-RFT outperforms SFT across multiple per-category evaluations, including semantically diverse and unusual categories (e.g., "casserole," "suger bowl," "handsaw").
- On reasoning grounding (LISA benchmark), Visual-RFT achieves higher mIoU and gIoU on both validation and test splits compared to SFT, demonstrating that the approach also strengthens spatially-grounded language understanding that requires multi-step reasoning.
  - The reasoning traces show the model performing explicit multi-step visual inference (e.g., identifying a Pokémon by its moveset to locate the correct bounding box), a qualitatively new capability not present in SFT-trained models.

---

### Implications
- Visual-RFT establishes that verifiable reward functions can be defined for visual perception tasks, breaking the assumption that RFT is limited to domains with symbolic, easily-checkable outputs (math, code) and opening a path for RL-based fine-tuning across the full multimodal task space.
- The paradigm shift from data scaling to reward function design has significant implications for sample efficiency in vision-language models: high-performance domain adaptation may become feasible with tens to hundreds of examples rather than thousands, democratizing specialization of LVLMs for rare or proprietary domains.
- The emergence of structured chain-of-thought reasoning as a byproduct of reward optimization (rather than explicit supervision) suggests that RLHF/RFT-style training may be a more reliable mechanism for instilling visual reasoning than supervised imitation of reasoning traces, with implications for multimodal safety and alignment research.
- For RLHF and reward modeling, the success of rule-based IoU and classification rewards over learned reward models in the low-data regime suggests that reward model training may be avoidable in structured perception tasks, reducing alignment overhead and preference data requirements.
- The results on open-vocabulary and few-shot detection suggest that reward-driven exploration improves generalization to novel concepts, which has direct implications for the sample efficiency and learning dynamics of multimodal foundation models in continual learning settings.

---

### Remaining Limitations & Next Steps
-

## Key Claims

1. R1-style reinforcement learning models have demonstrated success in language models but their application in multi-modal domains remains under-explored.
2. Verifiable rewards—where reward scores are determined by pre-defined rules rather than a separate reward model trained on preference data—are a key direction for reproducing OpenAI o1.
3. RFT was conventionally applied only to mathematical and code generation tasks because those domains have clear, objective final answers that make rewards straightforward to verify.
4. SFT (Supervised Fine-Tuning) relies on large amounts of curated training data because it directly imitates ground-truth answers.
5. RFT is more data-efficient than SFT because it evaluates model responses and adjusts based on correctness, enabling trial-and-error learning.
6. Visual-RFT generates multiple responses (trajectories) containing reasoning tokens and final answers for each input, then applies task-specific verifiable reward functions to guide policy optimization
7. Visual-RFT uses an Intersection over Union (IoU) reward function for the object detection task.
8. Visual-RFT improves accuracy by 24.3% over the baseline in one-shot fine-grained image classification using approximately 100 samples, while SFT decreases accuracy by 4.3% in the same setting.
9. Visual-RFT exceeds the baseline by 21.9 mAP on COCO two-shot object detection and by 15.4 mAP on LVIS few-shot object detection.
10. Visual-RFT shifts the training paradigm from data scaling (as in SFT) to the strategic design of verifiable reward functions tailored to specific multi-modal tasks.

## Capabilities

- Reinforcement fine-tuning (RFT) with verifiable rewards applied to Large Vision-Language Models for visual perception tasks including few-shot object detection, fine-grained classification, reasoning grounding, and open-vocabulary detection — achieving 24.3% accuracy gain in one-shot classification 
- Task-specific verifiable reward functions for visual spatial tasks: IoU (Intersection over Union) reward enables RL policy optimisation for object detection without a separate trained reward model
- Data-efficient fine-tuning of VLMs via RL using only 10–1000 domain-specific samples, outperforming SFT which degrades in extremely low-data regimes
- Chain-of-thought reasoning traces embedded within VLM responses for visual grounding tasks — model reasons through spatial and semantic relationships before producing structured bounding box outputs

## Limitations

- Verifiable reward design for visual tasks requires bespoke per-task engineering — different reward functions must be manually designed for each perception task type (classification vs. detection vs. grounding), preventing general-purpose applicability
- Visual-RFT is fundamentally restricted to tasks with structured, verifiable outputs — open-ended visual tasks (image captioning, open-domain VQA, scene description) cannot benefit because no rule-based reward function can be defined
- All experiments conducted exclusively on Qwen2-VL-2B (a 2B parameter model) — no evidence that Visual-RFT benefits hold or scale with larger models (7B, 32B, 70B+)
- No analysis of how Visual-RFT performance scales with increasing training data — experiments are confined to the extremely low-data regime (10–1000 samples), leaving the data-scaling behaviour and potential ceiling unknown
- SFT degrades significantly in visual few-shot regimes — standard supervised fine-tuning on small labeled datasets causes accuracy to drop below the baseline, indicating SFT overfits with insufficient data
- Implicit assumption that reward verifiability is achievable for the task — the Visual-RFT paradigm does not address how to construct verifiable rewards for tasks where ground truth is ambiguous or requires human judgement (e.g., aesthetic image quality, semantic scene understanding)
- No evaluation of inference-time cost or training compute requirements — the paper omits analysis of GPU-hours, training time relative to SFT, or inference latency, making practical deployment cost opaque

## Bottlenecks

- Absence of generalised, automatically derivable verifiable reward functions for the full range of visual tasks blocks broad application of RL fine-tuning to VLMs beyond the narrow set of tasks with structured spatial/categorical outputs
- RL fine-tuning for visual tasks has been unexplored in multimodal domains — the field has concentrated RL with verifiable rewards on language-only tasks, leaving VLMs without the infrastructure and reward function libraries that text models benefit from

## Breakthroughs

- Demonstration that RL with verifiable rewards (R1/GRPO-style RFT) extends beyond language tasks to visual perception — enabling data-efficient fine-tuning of VLMs for object detection, classification, and grounding with only 10–1000 examples

## Themes

- [[themes/multimodal_models|multimodal_models]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
