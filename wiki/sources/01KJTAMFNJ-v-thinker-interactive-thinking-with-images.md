---
type: source
title: 'V-Thinker: Interactive Thinking with Images'
source_id: 01KJTAMFNJXJ21H8RH9D3SBE5S
source_type: paper
authors:
- Runqi Qiao
- Qiuna Tan
- Minghan Yang
- Guanting Dong
- Peiqing Yang
- Shiqiang Lang
- Enhui Wan
- Xiaowan Wang
- Yida Xu
- Lan Yang
- Chong Sun
- Chen Li
- Jing Lyu
- Honggang Zhang
published_at: '2025-11-06 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- multimodal_models
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# V-Thinker: Interactive Thinking with Images

**Authors:** Runqi Qiao, Qiuna Tan, Minghan Yang, Guanting Dong, Peiqing Yang, Shiqiang Lang, Enhui Wan, Xiaowan Wang, Yida Xu, Lan Yang, Chong Sun, Chen Li, Jing Lyu, Honggang Zhang
**Published:** 2025-11-06 00:00:00
**Type:** paper

## Analysis

# V-Thinker: Interactive Thinking with Images
2025-11-06 · paper · Runqi Qiao, Qiuna Tan, Minghan Yang, Guanting Dong, Peiqing Yang et al. (14 total)
https://arxiv.org/pdf/2511.04460

---

### Motivation & Prior Limitations

- Current Large Multimodal Models (LMMs) produce lengthy, coherent chain-of-thought reasoning but remain detached from visual grounding, relying on linguistic priors rather than genuine visual perception, which leads to hallucinations.
  - Models like GPT-4o and Qwen2.5-VL score as low as 8.8% on instruction-guided visual interaction tasks (VTBench), despite strong general visual reasoning performance — revealing a fundamental gap between language-driven reasoning and perceptual grounding.

- The emerging "Thinking with Images" paradigm (pioneered by OpenAI o3) is constrained by narrow visual tool spaces and task-specific workflow designs that limit generalization.
  - Works such as DeepEyes and Thyme rely on a limited set of visual operations (e.g., cropping) and require precise spatial localization; DeepSketcher and similar approaches are tightly coupled to specific task types (e.g., geometric auxiliary lines only).
  - Approaches relying on "Image2Code" pipelines for image editing struggle to accurately depict spatial relationships between visual elements and may introduce extra noise.

- Traditional vision-centric reasoning datasets are built on manually defined tasks where models act as solvers, constraining diversity, scalability, and the spatial-logical alignment required for interactive reasoning.
  - Distillation-based synthesis methods are limited by the seed images they start from and cannot create genuinely novel visual reasoning scenarios.

---

### Proposed Approach

- V-Thinker is a general-purpose multimodal reasoning assistant that formalizes reasoning as a code-driven visual interaction process: at each step, the model generates a textual thought and, when necessary, a Python code segment that modifies the current image, with a sandboxed executor feeding the updated visual state back into the reasoning chain (the "think–edit loop").
  - This differs from prior work by expanding the visual tool space to arbitrary Python-renderable operations rather than a fixed set of crops or rotations, and by eliminating the coupling between tool design and task type.

- The **Data Evolution Flywheel** is a three-stage automated pipeline for synthesizing the V-Interaction-400K dataset that shifts models from "solvers" to "creators" via knowledge-driven generation.
  - **Diversity (Knowledge-driven Evolution):** Starting from an initial knowledge system K₀ (derived from We-Math 2.0) and a curated tool set T₀, a strong generator (GPT-5) iteratively co-evolves both sets — sampling knowledge concept combinations to generate QA pairs and predict new tools, and vice versa. Novel elements are filtered, merged, and normalized via BGE-based hierarchical clustering, growing to ~50× seed size after five iterations without saturation.
  - **Quality (Coordinated Calibration):** A checker module verifies answer correctness, rendered image validity, and coherence of intermediate visual states; a repairer reconstructs questions from valid visual states when the textual answer is wrong, looping until consistency is achieved.
  - **Difficulty (Progressive Expansion):** Two complementary strategies — parallel extension (independent auxiliary constructions providing additional observations) and sequential extension (new constructions dependent on prior results) — escalate reasoning chain complexity up to three steps deep.

- The **Visual Progressive Training Curriculum** is a two-stage framework: first, Perception Alignment via supervised fine-tuning on the V-Perception-40K dataset (synthesized across element relations, element count, and knowledge concepts, with tasks spanning surface-level, semantic-level, and integrated reasoning); second, Interactive Reasoning Alignment via cold-start SFT on V-Interaction-400K followed by RL using GRPO.
  - The RL reward function combines accuracy (Racc), formatting (Rformat, λ=0.5), and tool usage (Rtool, λ=0.3), where the tool usage reward is gated on correct answers to prevent reward hacking through spurious tool calls.
  - RL training data includes open-source visual reasoning samples (We-Math 2.0, MMK12, ThinkLite) plus targeted samples from V-Interaction-400K where the base model answers incorrectly on the original image but correctly on the edited version — directly incentivizing visual interaction as a reasoning strategy.

- **VTBench** is an expert-verified benchmark of 1,500 QA pairs (500 per task type) across Perception, Instruction-Guided Interaction, and Interactive Reasoning dimensions, sourced from 9 open-source benchmarks and validated by five-expert majority voting, with LMM-as-judge evaluation for visual outputs.

---

### Results & Capabilities

- V-Thinker-7B achieves an average VTBench score of 30.2%, outperforming its base model Qwen2.5-VL-7B (17.7%) by +12.5% overall, with particularly strong gains in Instruction-Guided Interaction (+22.8%, from 8.8% to 31.6%).
  - V-Thinker-7B also outperforms GPT-4o (25.0%) and InternVL3-78B (25.4%) on VTBench despite being a 7B model, demonstrating that the interactive reasoning training paradigm is highly efficient relative to scale.

- On general reasoning benchmarks without specific in-domain data, V-Thinker-7B improves over its base model on MathVision (+6.3%, 29.3%), We-Math (+1.1%, 62.8%), and VisuLogic (+0.6%, 26.6%), validating that the interactive reasoning paradigm generalizes beyond interactive tasks.

- Ablation study confirms that all three curriculum stages are necessary: removing RL training causes over 6% performance drop on MathVision and We-Math; removing perception alignment SFT also causes notable degradation, confirming that fine-grained perceptual grounding is a prerequisite for effective interactive reasoning.

- The Data Evolution Flywheel produces a knowledge syst

## Key Claims

1. OpenAI's o3 model was the first to actively interact with images during reasoning via visual tools such as cropping and rotation, shifting the paradigm from vision-assisted reasoning to vision-centric
2. Progress in the 'Thinking with Images' paradigm remains constrained by narrow visual tool spaces and task-specific workflow designs.
3. Heavy reliance on 'Image2Code' pipelines for image editing struggles to accurately depict spatial relationships between visual elements and may introduce extra noise.
4. Traditional vision-centric reasoning data synthesis paradigms limit diversity and scalability because they rely on manually defined tasks where models act as solvers.
5. GPT-5 can directly generate Python code to render high-quality original images along with corresponding auxiliary line diagrams and reasoning trajectories.
6. Knowledge concepts serve as condensed representations of reasoning semantics and can replace seed samples as references for diverse data synthesis.
7. V-Thinker treats reasoning as a code-driven visual interaction process where at each step the model generates a textual thought and, when necessary, executable code that modifies the current image.
8. The Data Evolution Flywheel synthesizes interactive reasoning data across three dimensions—diversity, quality, and difficulty—through a three-stage process yielding the V-Interaction-400K dataset.
9. Knowledge-driven evolution uses a co-evolutionary loop between a knowledge system K and tool set T, where each is used to generate data predicting new elements for the other, with BGE-based hierarchic
10. Progressive Expansion uses parallel extension (new auxiliary constructions independent of existing ones) and sequential extension (new constructions dependent on prior results) to escalate reasoning c

## Capabilities

- Multimodal models can perform interactive visual reasoning by autonomously generating Python code to modify images during reasoning (draw auxiliary lines, add annotations, crop, label regions) and use resulting visual feedback to guide subsequent reasoning steps — a 'think-edit loop'
- End-to-end reinforcement learning (GRPO) in a sandboxed code execution environment can train a 7B multimodal model to autonomously generate, execute, and iterate visual code during reasoning, improving both interactive (+12.5%) and general reasoning (+6.3% MathVision) performance
- LLMs (specifically GPT-5) can act as autonomous dataset creators for interactive visual reasoning — generating original images via Python rendering, spatial auxiliary constructions, and multi-step reasoning trajectories from scratch, rather than only solving predefined problems
- Automated co-evolutionary data synthesis flywheels can expand interactive reasoning datasets from small seeds to ~50× their initial size over 5 iterations, with non-saturating non-linear growth in both knowledge concepts and visual tool diversity

## Limitations

- Leading multimodal models fundamentally fail at fine-grained visual interaction tasks requiring spatial point localization — GPT-4o scores 12.6% and Qwen2.5-VL scores 8.8% on perception tasks in VTBench, revealing a massive gap between general visual QA ability and interactive spatial grounding
- Visual reasoning in current LMMs is decoupled from actual image content — models rely on linguistic priors rather than genuine visual perception, causing hallucinations on tasks that cannot be solved from language statistics alone
- Even V-Thinker's interactive reasoning improvement only weakly transfers to general reasoning — 12.5% improvement on VTBench but only 2.7% average improvement on standard benchmarks (MathVision +6.3%, We-Math +1.1%, VisuLogic +0.6%)
- Interactive visual reasoning accuracy remains well below human-level — V-Thinker achieves 40.4% and GPT-4o 36.4% on VTBench interactive reasoning tasks, indicating interactive visual cognition is far from solved even after targeted training
- Image-to-code pipelines for visual editing cannot accurately represent spatial relationships between elements and introduce noise — code-rendered geometry is an approximate proxy for precise pixel-level spatial truth
- Data evolution flywheel effectiveness is critically dependent on initial seed quality — low-diversity seeds result in substantially inferior knowledge expansion trajectories, creating a bootstrapping problem
- Training V-Thinker required 512 H20 GPUs (64 nodes × 8 GPUs) — the compute cost for interactive RL training with code execution sandboxes is prohibitive for most academic groups
- The paper provides no analysis of inference-time compute requirements or latency — interactive visual reasoning requires real-time sandboxed Python execution at inference, implying significant deployment overhead not acknowledged in the paper
- VTBench evaluation criteria are sensitive to prompt variations in LLM judges — results cannot be compared across differently-prompted evaluation setups, undermining benchmark reproducibility
- V-Thinker is only demonstrated at 7B scale — whether interactive RL training benefits compound, degrade, or transfer at larger model scales is entirely unexplored
- Prior interactive reasoning approaches (DeepEyes, Thyme, DeepSketcher) are tightly coupled to specific task types — their tool designs cannot generalize across diverse visual domains without task-specific re-engineering

## Bottlenecks

- Fine-grained spatial perception is a blocking constraint for interactive visual reasoning — models can recognize scene semantics but cannot reliably localize specific points, intersections, and geometric anchors required for code-driven image manipulation
- Absence of high-quality interactive visual reasoning training data — existing datasets use static problem-solving trajectories and lack the spatial precision and diverse tool interaction patterns needed for image-interactive thinking

## Breakthroughs

- End-to-end reinforcement learning successfully trains a 7B open multimodal model to perform general-purpose 'Interactive Thinking with Images' — autonomously generating, executing, and iterating visual code modifications during reasoning across diverse domains without task-specific engineering
- Knowledge-driven co-evolutionary data synthesis flywheel automates generation of 400K+ high-quality interactive visual reasoning samples from small seeds — shifting data creation from human annotation toward LLM-driven generation with non-saturating 50× scale-up over 5 iterations

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/vision_language_models|vision_language_models]]
