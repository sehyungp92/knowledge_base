---
type: source
title: 'Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future
  Frontiers'
source_id: 01KJTNW0W4JFNXBS89R7JDZG5G
source_type: paper
authors:
- Zhaochen Su
- Peng Xia
- Hangyu Guo
- Zhenhua Liu
- Yan Ma
- Xiaoye Qu
- Jiaqi Liu
- Yanshu Li
- Kaide Zeng
- Zhengyuan Yang
- Linjie Li
- Yu Cheng
- Heng Ji
- Junxian He
- Yi R. Fung
published_at: '2025-06-30 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- multimodal_models
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers

This survey systematizes a paradigm shift in multimodal AI from treating vision as a static, once-encoded input ("thinking *about* images") to using visual information as a dynamic, manipulable cognitive workspace ("thinking *with* images") — introducing a three-stage framework of increasing cognitive autonomy and arguing that visual manipulation and generation must become first-class reasoning operations rather than perceptual preprocessing.

**Authors:** Zhaochen Su, Peng Xia, Hangyu Guo, Zhenhua Liu, Yan Ma, Xiaoye Qu, Jiaqi Liu, Yanshu Li, Kaide Zeng, Zhengyuan Yang, Linjie Li, Yu Cheng, Heng Ji, Junxian He, Yi R. Fung
**Published:** 2025-06-30
**Type:** Survey paper
**Source:** https://arxiv.org/pdf/2506.23918

---

## The Core Critique: Why Text-Centric Reasoning Fails

The dominant paradigm for [[themes/multimodal_models|multimodal models]] performs a single visual encoding pass, then reasons entirely in text. This one-time encoding collapses relational visual structure into a fixed feature vector, creating a **critical information bottleneck** that causes cognitive brittleness on any task requiring iterative visual engagement.

The survey's motivating failure case is telling: a model misreads "160 calories" on a nutrition label as "60" because it cannot re-examine the image after initial encoding. This is not a perceptual failure — it is a *cognitive architecture* failure.

The underlying pathology is a **fundamental semantic gap**: high-dimensional continuous visual information cannot be faithfully encoded in discrete tokens. For text, this gap is narrow; for vision, it is theoretically intractable. [[themes/vision_language_models|Vision-language models]] built on text-centric [[themes/chain_of_thought|chain-of-thought]] reasoning inherit this structural limitation regardless of how strong the visual encoder is.

---

## The Proposed Framework: Three Stages of Cognitive Autonomy

The paper defines "thinking with images" formally as a reasoning process where intermediate steps $z_t$ are sampled from the union of *textual outputs* and *intermediate visual artifacts*, conditioned on an evolving multimodal state history — in contrast to standard VLMs where visual features act as a fixed initial condition.

This is organized into a **three-stage framework**, explicitly presented as non-linear cognitive strategies (the "how") rather than a strict developmental progression:

### Stage 1 — Tool-Driven Visual Exploration
The model orchestrates a fixed inventory of external visual modules (OCR, zoom, object detection, segmentation, depth estimation) as intermediate reasoning steps. Its role is planner rather than executor. Using [[themes/reinforcement_learning|reinforcement learning]], models can discover effective tool policies from as few as 20–1,000 examples — and RL generalizes better than [[themes/finetuning_and_distillation|SFT]] for this orchestration task.

**Current capability level:** Narrow production — tool-driven pipelines are deployed in constrained settings, but long-tail reliability is insufficient for unconstrained use.

**Ceiling:** The approach is fundamentally bounded by the predefined toolbox. No model can construct a visual analysis not anticipated by the tool designer. Error propagation is also catastrophic: a single incorrect intermediate image (e.g., zooming to the wrong region) establishes a false perceptual ground truth that poisons all subsequent reasoning.

### Stage 2 — Programmatic Visual Manipulation
The model generates executable Python code to construct *custom* visual operations — drawing auxiliary lines, filtering image regions, computing spatial properties, applying computer vision algorithms on demand. Systems like VisProg and ViperGPT achieve strong zero-shot performance by treating generated code as a transparent, verifiable intermediate representation.

**Key insight:** SFT on code-derived data (execution traces, image-code pairs) functions as implicit neuro-symbolic learning — the compositional, hierarchical structure of code provides an inductive bias that shapes more structured reasoning pathways in the neural model. [[themes/rl_for_llm_reasoning|RL for reasoning]] can further optimize code generation by training on execution feedback and task-oriented rewards.

**Current capability level:** Demo — strong results on benchmark tasks, not yet reliably generalizable to arbitrary real-world queries.

### Stage 3 — Intrinsic Visual Imagination
The model generates new images as native intermediate reasoning steps within a closed cognitive loop, requiring no external tools or APIs. Unified architectures (Chameleon, BAGEL, BLIP3-o, GoT-R1, Janus-Pro) make this possible by integrating visual generation and language reasoning within a single model.

**Demonstrated result:** Visual Planning (VPRL) navigates complex environments by reasoning through *sequences of generated images with no text*, outperforming language-based chain-of-thought on spatial navigation tasks — the first evidence that visual simulation may be a *superior* cognitive substrate to verbal description for certain problem types.

**Current capability level:** Research only — the architectural integration exists, but coherent multi-step visual imagination at production quality does not.

---

## The Unified Visual Thinker: Proposed Architecture

The survey proposes a conceptual target architecture with three components:

**Metacognitive Controller** — routes incoming tasks based on assessed complexity. Straightforward tasks go directly to low-cost interpretation; complex tasks activate the Visual Cognitive Workspace. This controller is the crucial missing piece: no current architecture implements learned task-complexity routing.

**Visual Cognitive Workspace** — the active reasoning environment, containing a feedback loop that allows the system to review and iteratively build upon its own generated visual thoughts. The process is flexible — the system can emit a final answer at any point if a satisfactory solution is reached, without completing a full reasoning cycle.

**Action & Output Interface** — produces diverse output types: textual answers, edited images, diagrams, or executable command sequences for robotic agents.

The central principle is not peak capability but **dynamic appropriateness**: a Stage 3-capable model should still invoke a simple Stage 1 measurement tool when that is more efficient, routing to complex visual simulation only when genuinely required.

---

## Limitations and Open Problems

This survey is unusually candid about the severity of unsolved challenges. The most critical:

### Compute as a Structural Barrier
Visual reasoning chains are **orders of magnitude more expensive** than textual reasoning. A single intermediate image requires thousands of visual patches with intensive computation; multi-step chains compound this cost multiplicatively. Generating photorealistic images at every reasoning step — as current Stage 3 approaches do — is likely unnecessary (human cognition relies on sketchy, abstract mental imagery) but no learned policy yet knows when to use cheaper representations. This is currently a **blocking bottleneck** for practical deployment.

### Error Propagation Is Catastrophic
Unlike text, where a reasoning error can often be self-corrected downstream, a wrong intermediate image establishes a false perceptual ground truth. There is no established mechanism for detecting or recovering from visual errors mid-chain. The entire reasoning loop is also **vulnerable to adversarial attack** at every intermediate step — not just inputs and outputs — with no established defences and no existing safety work for this expanded attack surface.

### The Modular Architecture Divide
Most current systems separate the vision encoder from the language decoder, forcing translation of spatial information into sequential format. This indirect loop loses fine-grained spatial relationships and prevents the tight perception-action feedback required for genuine visual cognition. Unified autoregressive architectures close this gap architecturally but have not yet demonstrated the benefits reliably.

### Missing Metacognition
No current architecture implements a learned meta-policy for strategy selection — models cannot assess whether to use tool orchestration, code generation, or intrinsic imagination for a given task. Cross-task visual strategy generalization is unsolved: models trained with one reasoning mode fail to transfer to others.

### Benchmark Inadequacy
Current benchmarks only assess final answer correctness. A model that reaches the right answer via a shortcut, an implausible visual chain, or lucky perceptual misreadings is indistinguishable from one with genuine visual reasoning. **No process-oriented evaluation framework exists** for intermediate visual reasoning quality — making it impossible to reliably measure whether "thinking with images" is actually happening or whether training and scaling are producing better-calibrated shortcuts.

### Unaddressed Dimensions
- **Temporal reasoning:** all current approaches are validated on static 2D images; *Thinking with Video* and *Thinking with Audio* are entirely future work
- **Abstract visual representations:** models operate at the pixel level; higher-level structural, semantic, or causal representations are not yet developed
- **3D embodied environments:** extension beyond 2D is unaddressed
- **Safety and trustworthiness:** listed as a future direction with no existing work
- **Human-AI collaborative visual reasoning:** no standard interface or interaction paradigm exists

---

## Connections to Broader Themes

The paradigm shift described here connects directly to several active research fronts:

**[[themes/reasoning_and_planning|Reasoning and planning]]:** The survey argues that genuine planning in visually grounded environments requires visual simulation as a native cognitive operation — purely verbal planning over visual domains hits a fundamental ceiling. The physical simulation bottleneck links directly to limitations in embodied agent planning.

**[[themes/post_training_methods|Post-training methods]] and [[themes/rl_for_llm_reasoning|RL for LLM reasoning]]:** The finding that RL generalizes better than SFT for tool orchestration — and that complex reasoning patterns appear to be latent in pre-trained models rather than trained in — echoes findings from the textual reasoning literature. Curiosity-driven RL rewards are required to elicit visual exploration behaviors that otherwise remain dormant.

**[[themes/finetuning_and_distillation|Finetuning and distillation]]:** Code-bootstrapped training data generation (CoSyn and related approaches) represents a significant technique: text-only LLMs generate code that renders synthetic images, providing perfectly aligned multimodal supervision without human annotation. This positions code as a privileged intermediate representation for multimodal training.

**[[themes/chain_of_thought|Chain of thought]]:** The survey directly challenges the assumption that chain-of-thought must be textual. Visual scratchpads — intermediate images with auxiliary annotations — represent a fundamentally different, potentially superior reasoning substrate for spatial and geometric problems, with the added benefit of being human-interpretable and verifiable in ways that implicit neural representations are not.

---

## Significance and Status

The paper's primary contribution is **taxonomic and conceptual**: it provides the first systematic organization of an emerging paradigm rather than reporting original empirical results. Its value is in making the paradigm shift legible, identifying where the field actually is (Stages 1 and 2, with Stage 3 beginning to emerge in research settings), and mapping the gap between current capability and genuine visual cognition.

The clearest finding from the surveyed literature is that **the paradigm shift is real but incomplete**: vision-as-static-input is a provably inferior architectural choice, unified architectures that internalize visual imagination exist, and RL-based approaches have demonstrated superior generalization over SFT for visual reasoning — but the efficiency, reliability, safety, and generalization challenges mean that "thinking with images" remains a research direction rather than a deployed capability outside narrow constrained domains.

The survey's honest conclusion: *"The journey towards true visual cognition is still in its early stages."*

---

## Related Themes

- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/finetuning_and_distillation|Finetuning and Distillation]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/vision_language_models|Vision-Language Models]]

## Key Concepts

- [[entities/bagel|Bagel]]
- [[entities/set-of-mark-prompting|Set-of-Mark Prompting]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
- [[entities/world-model|World Model]]
- [[entities/verl|veRL]]
