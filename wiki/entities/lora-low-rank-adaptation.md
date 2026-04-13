---
type: entity
title: LoRA (Low-Rank Adaptation)
entity_type: method
theme_ids:
- agent_systems
- benchmark_design
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- in_context_and_meta_learning
- interpretability
- mechanistic_interpretability
- model_architecture
- multi_agent_coordination
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- test_time_learning
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0027730319329089385
staleness: 0.0
status: active
tags: []
---
# LoRA (Low-Rank Adaptation)

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/benchmark_design|benchmark_design]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/interpretability|interpretability]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/representation_learning|representation_learning]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vision_language_models|vision_language_models]]

## Overview

A parameter-efficient fine-tuning technique that adapts large models by updating only low-rank weight matrices, significantly reducing memory and compute requirements. Empirically shown to perform equivalently to full fine-tuning even at small ranks in RL tasks.

## Key Findings

1. TTT on in-context examples surpasses standard few-shot prompting on BIG-Bench Hard (BBH) in the 10-shot setting by 7.3 percentage points (50.5% to 57.8%) (from "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning")
2. TTT with an 8B-parameter LM achieves 61.9% accuracy on ARC when ensembled with program-synthesis methods, matching average human performance of 60.2% (from "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning")
3. TTT improves the fine-tuned base model on ARC from 18.3% to 47.1% on the full public validation set (from "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning")
4. PAM achieves an average accuracy of 49.89 ± 1.66 on the CoIN benchmark, compared to 43.36 ± 8.18 for sequential fine-tuning. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
5. PAM assumes that previous task data is not available when learning a new task and that task identity is not available at inference time. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
6. On average, 29.41% of parameters across all layers are misaligned between the global LoRA module and the most recent LoRA module when using TIES post-training alignment. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
7. PAM periodically re-initializes LoRA weights that become sign-misaligned with the important weights of the global LoRA during new task training. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
8. PAM uses element-wise averaging to merge a temporary task-specific LoRA with a global evolving LoRA after each new task. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
9. TextGrad improves GPT-4o's zero-shot code accuracy on LEETCODE-HARD from 26% to 36%, raises MMLU-Physics performance from 91.2% to 95.1%, and enhances the multi-tool agent CHAMELEON by 7.7% (from "Adaptation of Agentic AI")
10. DeepSeek-R1 demonstrated that reinforcement learning with verifiable reward can effectively enhance the reasoning capabilities of large agents (from "Adaptation of Agentic AI")
11. PAM uses PaliGemma as its base VLM with LoRA rank of 32 and alignment percentage of 50%. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
12. The T2 approach (s3) achieves 58.9% average accuracy with only 2,400 training samples by training a lightweight 7B searcher subagent using frozen-generator feedback. (from "Adaptation of Agentic AI")
13. Over 1100 models — including 500 Mistral-7B LoRAs, 500 Vision Transformers, and 50 LLaMA-8B models — show universal subspaces capturing majority variance in just a few principal directions. (from "The Universal Weight Subspace Hypothesis")
14. The T2 paradigm represents a conceptual inversion: rather than adapting the agent to use tools better, it adapts tools to better serve a fixed frozen agent, reframing the foundation model from optimiz (from "Adaptation of Agentic AI")
15. Applying post-training alignment (TIES) to the penultimate task prior to merging results in a 7.44% reduction in accuracy. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")

## Relationships

## Limitations and Open Questions

## Sources
