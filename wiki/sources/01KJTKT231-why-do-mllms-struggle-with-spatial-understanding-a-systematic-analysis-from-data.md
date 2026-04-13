---
type: source
title: Why Do MLLMs Struggle with Spatial Understanding? A Systematic Analysis from
  Data to Architecture
source_id: 01KJTKT231S15HXEVDVGGYJ5PW
source_type: paper
authors:
- Wanyue Zhang
- Yibin Huang
- Yangbin Xu
- JingJing Huang
- Helu Zhi
- Shuo Ren
- Wang Xu
- Jiajun Zhang
published_at: '2025-09-02 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- multimodal_models
- robotics_and_embodied_ai
- spatial_and_3d_intelligence
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Why Do MLLMs Struggle with Spatial Understanding? A Systematic Analysis from Data to Architecture

**Authors:** Wanyue Zhang, Yibin Huang, Yangbin Xu, JingJing Huang, Helu Zhi, Shuo Ren, Wang Xu, Jiajun Zhang
**Published:** 2025-09-02 00:00:00
**Type:** paper

## Analysis

# Why Do MLLMs Struggle with Spatial Understanding? A Systematic Analysis from Data to Architecture
2025-09-02 00:00:00 · paper · Wanyue Zhang, Yibin Huang, Yangbin Xu, JingJing Huang, Helu Zhi et al. (8 total)
https://arxiv.org/pdf/2509.02359v1

---

### Motivation & Prior Limitations
- Existing studies confirm that MLLMs struggle with spatial understanding, yet prior analyses are fragmented — typically restricted to isolated scenarios (single-view only, or video only) — leaving no comprehensive, cross-scenario diagnosis of why these failures occur.
  - Models like LLaVA-OV-7B and Qwen2.5-VL-7B approach human-level performance on single-view spatial tasks, but exhibit large gaps on multi-view and video-based scenarios (Figure 1), indicating the failure is not uniform and scenario-specific mechanisms are at play.
  - Prior mechanistic analyses (e.g., Chen et al. 2025 on attention alignment, Yang et al. 2025 on cognitive maps) are narrow in task coverage and do not distinguish whether the bottleneck is data insufficiency or architectural constraint.
- There is no high-quality benchmark tailored for multi-view spatial understanding, leaving a critical evaluation gap for tasks requiring integration of spatial cues across different viewpoints.

---

### Proposed Approach
- The paper presents a two-axis systematic analysis of spatial understanding — data-centric (scaling experiments) and architecture-centric (positional encoding ablations) — across three scenarios: single-view, multi-view, and video, using multiple MLLM families (cascaded and native).
  - For multi-view evaluation, the authors introduce MulSeT (Multi-view Spatial Understanding Tasks), a simulation-based benchmark built from AI2THOR with 38.2k QA pairs across 5,000+ unique 3D scenes, comprising three progressively difficult subtasks: Occlusion Restoration (semantic correspondence across views), Distance Comparison (intuitive spatial perception), and Azimuth Transfer (viewpoint-conditioned spatial imagination).
  - The architecture-centric analysis uses three ablation strategies — Mask (zero out a PE dimension), Shuffle (randomly permute positional indices), and Constant Value (assign all positions a single reference token's value) — applied independently to the visual encoder (VE) and language model (LLM) across models with different PE configurations (2D-RoPE in Qwen2.5-VL's VE, learnable PEs in LLaVA-OV and Mono-InternVL's VE, M-RoPE vs. 1D-RoPE in LLMs).
  - For solution exploration, the paper evaluates reasoning injection via four prompt variants (implicit vs. explicit × stepwise vs. multi-view consistency), finding that implicit multi-view consistency prompting consistently outperforms standard stepwise CoT across all three MulSeT tasks.

---

### Results & Capabilities
- Data scaling yields rapidly diminishing returns for spatial understanding: performance saturates quickly and the performance ceiling remains low, especially for tasks requiring spatial imagination, indicating data volume alone is insufficient.
  - On Occlusion Restoration (semantic matching), performance improves from 54.8 to ~79.6 over 1k–10k training samples, with gains concentrated in early data increments and near-zero marginal gain after 3k samples.
  - On Azimuth Transfer (spatial imagination), the performance ceiling is substantially lower (~45), and gains become noisy and sometimes negative after 3k samples, demonstrating that abstract spatial reasoning is not learnable from more data of the same kind.
  - Model size scaling exhibits the same pattern of diminishing returns: fine-tuning Qwen2.5-VL from 3B to 72B on 10k samples yields base scores of 27.7→38.6 but fine-tuning increments of 14.3→6.0, confirming that larger models improve the baseline but not the fine-tuning benefit for spatial tasks.
- The visual encoder's positional encoding is the dominant bottleneck for spatial understanding, contributing far more than the LLM's positional encoding across both cascaded and native MLLM architectures.
  - Shuffling the VE's height-width RoPE dimensions (Shuffle-VE-hw) causes catastrophic degradation on single-view spatial tasks: What'sUp drops from 86.65 to 8.99 for Qwen2.5-VL-7B and from 98.66 to 12.31 for LLaVA-OV-7B, while equivalent shuffling of LLM positional indices (Shuffle-LLM-xy, text tokens only) causes minimal degradation (~2–6 points).
  - Cascaded models (LLaVA-OV) are more reliant on the VE's positional encoding than native models (Mono-InternVL), but this relationship inverts for non-spatial tasks (VG attribute recognition), suggesting native end-to-end training enables more distributed spatial-semantic fusion.
  - Setting all visual token positions in the LLM to the last token's value (Const-LLM-Last) causes disproportionate performance loss compared to using the first token's value, attributed to Qwen2.5-VL's training convention of appending a global thumbnail after local patches, making the final token's positional context architecturally significant.
- Implicit multi-view consistency prompting outperforms explicit Chain-of-Thought on all MulSeT subtasks, with explicit CoT causing substantial degradation on perceptually grounded tasks.
  - Explicit Stepwise CoT reduces Distance Comparison from 43.41 to 34.41 (−9.0 points) and Azimuth Transfer from 27.25 to 23.00 (−4.25), while Implicit Multi-view yields gains of +1.85 and +1.90 on Occlusion Restoration and Azimuth Transfer respectively.
  - Attention visualization reveals that explicit reasoning diffuses the model's attention away from task-relevant objects (e.g., attending to the bike itself rather than nearby objects when asked which is closest), whereas implicit prompting preserves focused, discriminative attention patterns.

---

### Implications
- The finding that data scaling hits a low ceiling for spatial imagination tasks (Azimuth Transfer) suggests that current MLLM training paradigms — which treat spatial understanding as a learnable pattern — are architecturally mismatch

## Key Claims

1. MLLMs achieve human-level performance on single-view spatial tasks but show a significant gap in multi-view and video-based scenarios
2. Merely scaling up training data is insufficient to significantly improve MLLM spatial understanding, especially for tasks requiring spatial imagination
3. Spatial understanding in MLLMs relies more heavily on positional encoding within the visual encoder than within the language model
4. Performance gains from training data scale saturate quickly and the performance ceiling is relatively low for spatial understanding tasks
5. For spatial reasoning tasks, larger models start from a higher baseline but show diminishing returns from fine-tuning as model size increases
6. Disabling the visual encoder's RoPE leads to catastrophic performance decline, establishing 2D positional signals as the primary foundation for spatial understanding
7. Cascaded MLLMs demonstrate stronger reliance on visual encoder positional information for spatial tasks compared to natively integrated MLLMs
8. Setting all visual token positions to the last token's position incurs greater performance penalty than using the first token's position, due to global image thumbnail appended after local patches in 
9. Explicit reasoning causes more diffused attention maps compared to implicit reasoning, leading the model to focus on the wrong objects
10. Multi-view consistency prompting consistently outperforms traditional stepwise prompting across all three multi-view spatial understanding tasks

## Capabilities

- MLLMs achieve near human-level performance on single-view spatial understanding tasks (object relations, spatial attribute questions on datasets like What'sUp and COCO-QA)
- Implicit multi-view consistency prompting improves MLLM spatial reasoning on multi-view tasks without fine-tuning, by directing cross-view object comparison before answering
- LoRA fine-tuning on synthetic spatial data yields measurable multi-view spatial gains for semantically-grounded tasks like occlusion restoration (54.8 → ~79 with 3k samples)

## Limitations

- MLLMs show a large performance gap versus humans on multi-view spatial tasks — models score 34–43% versus human 57–86% on occlusion restoration, distance comparison, and azimuth transfer
- Spatial understanding performance saturates rapidly with training data and hits a low ceiling — especially for tasks requiring spatial imagination (azimuth transfer plateaus ~45% after 4k samples, human ~51%)
- Visual encoder positional encoding is nearly irreplaceable for spatial understanding — shuffling it (Shuffle-VE-hw) causes catastrophic collapse from 86.65% to 8.99% on What'sUp and from 43.75% to 35.11% on multi-view distance comparison
- LLM positional encoding contributes minimally to spatial understanding — shuffling or masking it (Shuffle-LLM-xy) causes near-zero impact on single-view spatial tasks and small impact on multi-view, meaning the language reasoning pathway cannot compensate for spatial perception failures
- Explicit chain-of-thought reasoning substantially degrades spatial task performance — Explicit Stepwise CoT drops distance comparison by 9 points and azimuth transfer by 4.25 points compared to vanilla
- Larger MLLM parameter counts show sharply diminishing returns from spatial fine-tuning — 3B gains +14.3 points, but 32B and 72B gain only +6.1 and +6.0 points respectively from the same 10k-sample spatial fine-tuning
- Abstract spatial imagination tasks (azimuth transfer — egocentric viewpoint-conditioned direction reasoning) have a hard performance ceiling barely reachable even with extensive fine-tuning, indicating a capability the current paradigm cannot acquire
- Video-based spatial understanding also plateaus at low levels (~44–48%) with training data scaling from 10k to 90k samples, with most gains concentrated in the first 10k samples
- Benchmark evaluation is conducted entirely in simulated indoor environments (AI2THOR), leaving real-world spatial understanding performance unvalidated
- Experiments use only small-to-mid models (2B–7B, with limited 32B/72B ablations); findings about architectural bottlenecks may not generalize to frontier-scale models (GPT-4o, Gemini 1.5 Pro) which are not tested
- Cascaded MLLMs (LLaVA-OneVision) show stronger dependence on visual encoder positional encoding for spatial tasks than native/monolithic models (Mono-InternVL), but native models' different PE characteristics are not yet understood or exploitable

## Bottlenecks

- Visual encoder positional encoding design is the primary architectural bottleneck for MLLM spatial understanding — current 2D-RoPE and learnable PE schemes are insufficient for multi-view and abstract spatial reasoning, and the LLM cannot compensate
- Spatial training data provides rapidly diminishing returns for abstract spatial tasks — the learning paradigm cannot acquire spatial imagination from 2D image data alone, creating a ceiling that cannot be lifted by scale

## Breakthroughs

- Systematic empirical proof that MLLM spatial understanding failures are primarily architectural (visual encoder positional encoding design) rather than a data scaling problem — reframes the research agenda for spatial reasoning improvement

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/llava-onevision|LLaVA-OneVision]]
- [[entities/lora|LoRA]]
- [[entities/m-rope|M-RoPE]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
