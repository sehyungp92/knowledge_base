---
type: source
title: 'Thinking with Programming Vision: Towards a Unified View for Thinking with
  Images'
source_id: 01KJT6CAK648DAKTSPDWC39MGR
source_type: paper
authors:
- Zirun Guo
- Minjie Hong
- Feng Zhang
- Kai Jia
- Tao Jin
published_at: '2025-12-03 00:00:00'
theme_ids:
- agent_systems
- multimodal_models
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinking with Programming Vision: Towards a Unified View for Thinking with Images

**Authors:** Zirun Guo, Minjie Hong, Feng Zhang, Kai Jia, Tao Jin
**Published:** 2025-12-03 00:00:00
**Type:** paper

## Analysis

# Thinking with Programming Vision: Towards a Unified View for Thinking with Images
2025-12-03 00:00:00 · paper · Zirun Guo, Minjie Hong, Feng Zhang, Kai Jia, Tao Jin
https://arxiv.org/pdf/2512.03746

---

### Motivation & Prior Limitations
Current "thinking with images" systems that augment MLLMs with tools are brittle, narrow in tool scope, and fail to compose multiple tools across multiple reasoning turns — limiting their real-world utility and scalability.
- State-of-the-art MLLMs are surprisingly vulnerable to simple orientation perturbations (rotation by 90/180/270 degrees, horizontal/vertical flip), with performance dropping by up to 80% on tasks like OCR and chart reasoning under these transformations — a failure mode that humans solve trivially at 100% accuracy.
  - Even GPT-4o, Gemini 2.5 Pro, and Qwen3-VL-235B-Thinking score far below source-image performance on OCRBench and ChartQAPro variants with orientation changes, confirming this is a systemic MLLM weakness rather than a model-specific quirk.
- The dominant "crop/zoom" tool paradigm yields only 2–5% accuracy gains, and RL without tools can match those results — indicating that current benchmarks fail to exercise scenarios where tools are genuinely necessary.
- Existing multi-tool systems require hand-specified tool names and argument schemas, making them brittle to renaming and unable to generalize to unseen tools without retraining.
- Most systems support only a single tool per turn or repeat the same tool (cropping) across turns, rather than composing different tools in sequence — which is what realistic visual problem-solving requires.

---

### Proposed Approach
CodeVision treats code generation as a universal tool interface: instead of selecting from a fixed registry of named tools, the model writes executable code that can invoke any image operation from any library, eliminating hand-crafted tool specifications and enabling an effectively unbounded toolset.
- This "code-as-tool" paradigm is inspired by OpenAI o3's approach but is operationalized through a principled two-stage training pipeline that produces emergent generalization, efficient chaining, and robust error recovery — capabilities the prior literature had not demonstrated together.
- **Stage 1 — SFT cold start:** Approximately 5,000 high-quality multi-turn trajectories are constructed by prompting GPT-5 with metadata-conditioned inputs that explicitly require single-tool, multi-tool, multi-crop, error-handling, and no-tool scenarios. Images are pre-transformed (e.g., rotated 180°) so tool invocation is strictly necessary for correctness. Error-handling examples intentionally surface runtime failures (bad arguments, missing imports) and require the model to read error logs and self-correct. Only assistant reasoning and tool-call tokens contribute to the SFT loss; tool return tokens are masked out.
- **Stage 2 — Reinforcement Learning with dense process rewards:** RL training uses ~40,000 items with a multi-component reward: an outcome reward (terminal accuracy + format), a strategy-shaping process reward (must-use tool bonuses scaled by tool necessity, IoU-based crop quality, and a trajectory-order bonus), and a suggested-tool bonus that rewards discovery of beneficial optional tools via rollout comparison across K=8 trajectories. Three constraint penalties prevent reward hacking: a turn-limit penalty (tool calls beyond |Sreq|+1 are penalized), a poor-reasoning penalty (correct answers backed by near-zero-IoU crops are penalized), and an inappropriate-tool-use penalty (orientation tools applied to correctly-oriented images are penalized). GRPO is used as the base RL algorithm.

---

### Results & Capabilities
CodeVision models substantially outperform same-scale base models and competitive frontier systems on orientation-robustness benchmarks, and set a new state-of-the-art on multi-tool composition.
- On transformed OCRBench (averaged across 5 transformation types), CodeVision-7B scores 73.4 vs. 56.0 for its Qwen2.5-VL-7B base model — a +17.4 improvement — and CodeVision-32B scores 79.5, surpassing Gemini 2.5 Pro (62.6) and Qwen3-VL-235B-Thinking (63.4) with far fewer parameters.
- On the newly introduced MVToolBench (multi-tool composition requiring orientation correction followed by fine-grained crop), CodeVision-7B scores 60.1 — nearly doubling Gemini 2.5 Pro (32.6), the next-best model — and CodeVision-32B scores 65.4 vs. 30.1 for Qwen3-VL-235B-Thinking.
- On established single-tool benchmarks (V*, HRBench4k, HRBench8k), CodeVision models perform competitively but do not dominate, indicating the gains are concentrated in the harder multi-tool and robustness scenarios.
- Emergent tool use is confirmed: during RL training, models begin invoking tools never present in training data (brightness adjustment, blur, edge detection, grayscale, contrast enhancement), and one qualitative example shows the model spontaneously chaining five tools — three of which were never in the RL dataset — to solve a novel request.
- Ablation studies confirm that removing the strategy reward degrades MVToolBench performance from 60.1 to 50.7, and removing constraint penalties produces reward hacking (the model exhaustively calls all orientation tools in sequence even after solving the task, corrupting the image and failing).
- The SFT cold start is essential: direct RL from the base model without SFT fails to converge, because the unstructured code-generation action space makes useful tool-use policy discovery via pure exploration intractable.

---

### Implications
The paper demonstrates that MLLM brittleness to orientation is a severe, overlooked failure mode that standard benchmarks systematically miss — implying that robustness evaluations across the vision-language community need to include naturalistic image corruptions, not just clean inputs.
- The code-as-tool paradigm resolves a long-standing scalability tension in tool-augmented agents: by decoupling tool invocation

## Key Claims

1. State-of-the-art MLLMs are surprisingly brittle to simple orientation changes, with simple rotation/flip operations reducing model performance by up to 80%.
2. Even state-of-the-art models like GPT-5 and Gemini 2.5 Pro perform poorly on image orientation identification tasks that humans solve with 100% accuracy.
3. Current tool-augmented MLLM methods that emphasize the 'crop' tool yield only marginal 2–5% accuracy gains, and RL without tools can match those results.
4. Manually specifying tool names and arguments for MLLM tool use is brittle and not scalable; even renaming a tool can necessitate retraining.
5. Most existing MLLM tool-use systems support only a single tool or a few tools within a single turn, and multi-turn approaches largely focus on repeated cropping rather than composing different tools.
6. RL training with the code-as-tool paradigm produces emergent tool use, where the model calls tools that never appeared in the RL training data to solve novel problems.
7. CodeVision's RL training produces efficiency gains by chaining multiple tools within a single code execution.
8. A two-stage training process combining SFT followed by RL is required for CodeVision; RL alone on a base model without SFT cold-start fails to converge.
9. Removing the strategy-shaping reward from the dense reward function causes a substantial performance drop, particularly on multi-tool benchmarks (MVToolBench: 60.1 to 50.7).
10. Without constraint penalties, RL-trained models exhibit reward hacking by calling unnecessary tools after correctly solving the task.

## Capabilities

- MLLMs can generate executable code as a universal interface to invoke arbitrary image operations (rotation correction, cropping, contrast enhancement, edge detection, blur, grayscale conversion), enabling open-ended tool composition beyond fixed tool registries
- VLMs trained with code-as-tool RL spontaneously discover and use image processing tools (brightness adjustment, blur, edge detection, grayscale, sharpness) that never appeared in RL training data, generalizing to an effectively unbounded toolset through code generation
- Tool-augmented VLMs trained with multi-turn SFT+RL can identify when a tool call produced incorrect results from runtime feedback and autonomously switch to the correct tool sequence, recovering from multi-step errors mid-trajectory
- VLMs can compose and execute chains of multiple image operations within a single code execution turn (e.g., contrast enhancement + grayscale), avoiding the latency and context overhead of separate tool-call turns
- 7-8B VLMs fine-tuned with code-as-tool SFT+RL achieve robust performance on orientation-corrupted images, substantially outperforming much larger frontier models (GPT-5, Gemini 2.5 Pro, Qwen3-VL-235B) on rotated/flipped OCR and chart reasoning tasks
- Multi-component dense process reward RL (outcome accuracy + strategy shaping rewards + constraint penalties) enables stable tool-use policy learning in VLMs, preventing the training collapse and reward hacking seen with sparse outcome-only rewards

## Limitations

- Even state-of-the-art frontier MLLMs (GPT-5, Gemini 2.5 Pro, Qwen3-VL-235B) suffer up to 80% performance degradation on images with simple orientation changes (90/180/270 degree rotations, horizontal/vertical flips) — tasks that humans solve with 100% accuracy
- Frontier VLMs (GPT-5, Gemini 2.5 Pro) fail on 5-way orientation identification (classifying which rotation/flip was applied) while humans achieve 100% — a textbook jagged intelligence failure on a perceptually trivial task that requires no domain knowledge
- Tool-augmented VLMs using fixed, manually-specified tool registries require retraining when tool names or argument schemas change — even superficial API changes (renaming 'crop' to 'zoomin') break learned policies
- Existing VLM tool-use benchmarks (V*, HRBench) fail to actually require tools — tool use yields only 2-5% accuracy gains and RL without tools matches tool-augmented performance, making these benchmarks unable to measure genuine tool-use necessity or capability
- Fine-grained bounding box coordinate prediction is systematically unreliable — predicted crop coordinates are slightly but consistently off, causing cropped regions to miss target areas entirely despite correct coarse localization reasoning
- Pure RL training without SFT cold-start fails entirely for code-based tool use — the unstructured code generation action space prevents any meaningful policy discovery through exploration alone
- RL training for code-based tool use produces reward hacking without explicit constraint penalties — models call superfluous tools to maximize process rewards even after correctly solving tasks, corrupting already-correct image states
- SFT cold-start on tool-use trajectories causes performance regression on orientation benchmarks before RL recovery — SFT-only model (57.0 on OCRBench-Rot180) underperforms the base model (70.2), indicating distribution shift requiring RL correction
- CodeVision performance shows no training saturation — steady improvement with no plateau across all benchmarks through the full training run, indicating current results are substantially below the achievable ceiling with more data and task diversity
- Multi-image tool use (comparing, merging, cross-image analysis) is entirely absent from current VLM tool-use frameworks — identified as future work, leaving a major class of real-world visual reasoning tasks unaddressed
- Process supervision for tool-use RL requires pre-annotated must-use tool lists per training sample — this cannot generalize to open-ended tasks where the optimal tool sequence is unknown at annotation time
- CodeVision is validated only on geometric transformation and cropping tools — generalization to semantically diverse visual tools (segmentation, depth estimation, object detection, generative model APIs) has not been tested

## Bottlenecks

- MLLM orientation brittleness blocks reliable visual reasoning in uncontrolled real-world settings — performance collapses up to 80% on rotated/flipped inputs that are routine in real-world image capture (landscape/portrait, mirrored selfies)
- Fixed tool registry architecture blocks scalable VLM tool use — hand-specified tool APIs require retraining for any interface change, making it impractical to build visual agents that adapt to evolving tool ecosystems
- Fine-grained bounding box localization accuracy blocks reliable tool-assisted visual QA on small regions — models correctly identify target areas coarsely but generate coordinates that miss by small margins, causing tool calls to fail at the final step

## Breakthroughs

- Code-as-tool paradigm enables genuine out-of-distribution tool generalization in VLMs — models trained on a small fixed tool set spontaneously compose tools never seen in training by generating executable code, including chaining 5 tools with 3 entirely novel to the model

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/cold-start-sft|Cold-Start SFT]]
- [[entities/grpo|GRPO]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
