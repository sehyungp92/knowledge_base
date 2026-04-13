---
type: source
title: 'Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in
  Small Multimodal Models'
source_id: 01KJT7H2D2R5QXPSK8970Q1X7A
source_type: paper
authors:
- Mark Endo
- Serena Yeung-Levy
published_at: '2025-11-21 00:00:00'
theme_ids:
- finetuning_and_distillation
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- scaling_laws
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 12
tags: []
---
# Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models

**Authors:** Mark Endo, Serena Yeung-Levy
**Published:** 2025-11-21 00:00:00
**Type:** paper

## Analysis

# Downscaling Intelligence: Exploring Perception and Reasoning Bottlenecks in Small Multimodal Models
2025-11-21 · paper · Mark Endo, Serena Yeung-Levy
https://arxiv.org/pdf/2511.17487

---

### Motivation & Prior Limitations
- The practical demand for on-device, efficient multimodal models has produced many small VLMs, but the consequences of LLM downscaling for multimodal capability remain poorly understood, with no systematic characterization of which abilities degrade most and why.
  - Prior works yield inconsistent findings: some report that scaling LLM size has little effect on perception, while others find perception-heavy tasks such as OCR and Chart VQA are highly sensitive to model size.
  - Existing failure analyses of VLMs focus predominantly on large, powerful models, leaving the failure modes introduced specifically by LLM downscaling largely unexplored.
- A general finding from prior work is that even state-of-the-art multimodal models perform near-randomly on perceptual tasks humans solve quickly, and that VLMs often fail to adequately utilize visual information produced by the vision encoder — yet these failure modes have not been characterized as a function of LLM scale.

---

### Proposed Approach
- The paper first conducts a controlled downscaling study using Qwen3 LLMs at four sizes (0.6B, 1.7B, 4B, 8B) paired with a fixed SigLIP vision encoder and 2-layer MLP connector, trained on 574K single-image and 309K multi-image instruction tuning examples, to isolate how LLM size affects performance across diverse visual tasks.
  - A decoupled perception–reasoning framework is applied to separately measure how LLM downscaling impacts each component, distinguishing fundamental perceptual degradation from weakened reasoning.
- To address the discovered perception bottleneck, the paper proposes **visual extraction tuning**: a training paradigm in which the model explicitly learns to produce structured, instruction-relevant visual descriptions before answering, unifying diverse perception skills across task types.
  - This is then combined with step-by-step reasoning over the extracted visual details in a two-stage pipeline called **EXTRACT+THINK**, which requires no additional visual supervision for the reasoning stage.
  - The approach differs from prior two-stage baselines like PrismCaptioner by being substantially more parameter- and data-efficient rather than relying on larger dedicated captioning modules.

---

### Results & Capabilities
- LLM downscaling disproportionately degrades visual capabilities rather than abilities inherited from the base LLM: tasks relying on general knowledge are largely unaffected, whereas visually-demanding tasks (e.g., Perceptual Similarity, Multi-Image VQA, Grounding) show the steepest drops.
  - This asymmetry holds consistently across the 0.6B–8B parameter range studied.
- Isolating LLM downscaling's effect on perception alone still produces severe performance drops, often matching or exceeding the drops observed when isolating its effect on reasoning, establishing perception as a co-equal bottleneck with reasoning in small multimodal models.
- EXTRACT+THINK's smaller variant surpasses the two-stage PrismCaptioner baseline across a wide range of tasks using a perception module roughly 12× smaller and a reasoning module 41× smaller.
- The approach improves over LLaVA-OneVision-0.5B while using 95% fewer visual training samples, demonstrating extreme data efficiency.

---

### Implications
- The finding that perception — not just reasoning — degrades sharply under LLM downscaling reframes the design target for efficient multimodal models: improving small-model visual extraction may matter as much as, or more than, improving their reasoning chains.
- Visual extraction tuning suggests that explicitly disentangling perception from reasoning during training is a viable and highly parameter-efficient strategy for recovering visual capability lost to LLM downscaling, with implications for how instruction tuning curricula should be designed for small VLMs.
- The systematic characterization offered here lays groundwork for future scaling-law research specifically targeting the downscaling regime, which has received far less study than upscaling.

---

### Remaining Limitations & Next Steps
- The source text is truncated before section 3.2's full results and before any explicit limitations section, so the paper's own stated caveats cannot be fully enumerated from the available text.
- The study is confined to a single architectural family (Qwen3 + SigLIP + 2-layer MLP), so generalizability of the downscaling findings to other LLM backbones, vision encoders, or connector designs is not established.
- The controlled training setting uses a fixed, curated data mixture (574K + 309K examples); whether the perception bottleneck characterization holds under different data regimes, pretraining approaches, or at larger small-model scales (e.g., 3B) is not addressed.
- The hypothesis that the perception bottleneck arises from the difficulty of acquiring diverse visual extraction skills during instruction tuning is stated as a hypothesis, not empirically verified through ablations visible in the provided text.

## Key Claims

1. LLM downscaling disproportionately affects visual capabilities rather than abilities inherited from the base LLM.
2. Isolating the effect of LLM downscaling on perception alone still results in severe performance drops, often matching or exceeding the drops observed when isolating reasoning.
3. Tasks most affected by LLM downscaling are those that emphasize visual processing, not those that rely heavily on the base LLM.
4. Tasks that rely more heavily on the base LLM, such as general or knowledge tasks, are largely unaffected by LLM downscaling.
5. Perception is a critical bottleneck in small multimodal models alongside reasoning.
6. Visual extraction tuning is a training paradigm in which the model explicitly learns to extract the visual details relevant to each instruction.
7. EXTRACT+THINK improves over LLaVA-OneVision-0.5B while using 95% fewer visual training samples.
8. Prior works have inconsistent findings on whether LLM size affects perception in multimodal models, with some finding little effect and others finding perception-heavy tasks are highly sensitive to mo
9. Even the best-performing multimodal models perform near-randomly on perceptual tasks that humans can solve quickly.
10. The perception bottleneck in small multimodal models arises from the model needing to acquire diverse skills to extract relevant visual information across instruction-tuning tasks.

## Capabilities

- Visual extraction tuning trains small VLMs to explicitly extract instruction-relevant visual details consistently across tasks, separating perception from reasoning in a two-stage pipeline
- EXTRACT+THINK achieves competitive small VLM performance with a perception module ~12× smaller and reasoning module ~41× smaller than the PrismCaptioner baseline, demonstrating extreme parameter efficiency
- Small VLMs can be trained to exceed LLaVA-OneVision-0.5B performance using 95% fewer visual training samples when visual extraction tuning is applied from scratch

## Limitations

- LLM downscaling disproportionately degrades visual and perceptual capabilities in multimodal models, far more than general language or knowledge-based capabilities
- Perception degradation in small VLMs is as severe as or worse than reasoning degradation — perception alone (isolated from reasoning) drops sharply under LLM downscaling, contradicting the assumption that reasoning is the primary bottleneck
- State-of-the-art multimodal models perform near-randomly on perceptual tasks that humans solve quickly — a performance cliff that is not purely a function of model size
- VLMs have fundamental deficiencies in visual spatial planning — not just accuracy degradation but a categorical inability to reason about spatial relationships
- Visual information from vision encoders is systematically underutilized by the language model backbone, with failures attributed to limited exposure to relevant visual data — suggesting a structural coupling problem rather than just a data problem
- VLMs broadly struggle with visual reasoning puzzles requiring strong pattern recognition and abstract reasoning — a systematic failure class not resolved by scaling
- Failure modes of small VLMs — especially concerning visual perception — remain poorly understood, with prior findings inconsistent across works: some find LLM scaling has little effect on perception, others find strong sensitivity for tasks like OCR and Chart VQA
- Prior VLM failure mode research focuses on large models — techniques and mitigations developed for frontier-scale VLMs do not systematically transfer to the small-model regime
- Instruction tuning across diverse visual task types creates an excessive skill acquisition burden on small LLM backbones — the diversity of visual interpretation required across tasks cannot be compressed into small parameter budgets
- On-device small VLMs are practically limited as general visual assistants due to disproportionate perceptual degradation — the widely anticipated use case of capable on-device VLMs remains unrealized for visually demanding tasks

## Bottlenecks

- Perception is a critical, underappreciated bottleneck in small multimodal models — LLM downscaling impairs visual perception as severely as reasoning, blocking deployment of capable small VLMs for visually demanding on-device tasks
- The MLP projector architecture coupling vision encoders to LLM token spaces creates a systematic visual information utilization gap — vision encoder representations are inadequately surfaced to the LLM, and this gap widens dramatically as LLM capacity shrinks

## Breakthroughs

- First principled decoupling of perception vs. reasoning degradation in small VLMs, establishing that perception (not just reasoning) is a critical — and often dominant — bottleneck when LLM capacity is reduced
- EXTRACT+THINK achieves a new efficiency frontier for small VLMs: competitive performance with a 12× smaller perception module and 41× smaller reasoning module than the prior state-of-the-art two-stage baseline, with 95% fewer visual training samples

## Themes

- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/llava-onevision|LLaVA-OneVision]]
- [[entities/qwen3|Qwen3]]
- [[entities/siglip|SigLIP]]
