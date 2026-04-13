---
type: entity
title: ScienceQA
entity_type: dataset
theme_ids:
- agent_evaluation
- agent_systems
- chain_of_thought
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00273893236421815
staleness: 0.0
status: active
tags: []
---
# ScienceQA

**Type:** dataset
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

A science question answering benchmark used to evaluate agent performance. Chameleon (Lu et al., 2023) improves the best-published few-shot result by 11.37%.

## Key Findings

1. PAM assumes that previous task data is not available when learning a new task and that task identity is not available at inference time. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
2. LLaVA-CoT decomposes answer generation into four structured reasoning stages: summary, caption, reasoning, and conclusion (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
3. SWIRES retraces to a previous reasoning stage when all candidate responses at the current stage fall below a reward threshold (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
4. InternLM-XComposer2.5-Reward was used as the reward model to judge generation quality during test-time scaling experiments (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
5. With test-time scaling via SWIRES, LLaVA-CoT improves from 62.4% to 65.5% average across six benchmarks (from "LLaVA-CoT: Let Vision Language Models Reason Step-by-Step")
6. PAM achieves an average accuracy of 49.89 ± 1.66 on the CoIN benchmark, compared to 43.36 ± 8.18 for sequential fine-tuning. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
7. CLIP leverages contrastive pretraining for zero-shot reasoning via aligned embeddings between vision and language. (from "Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models")
8. PAM uses element-wise averaging to merge a temporary task-specific LoRA with a global evolving LoRA after each new task. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
9. Even commercial models like Gemini-1.5-Pro and GPT-4o achieve less than 20% average accuracy on the OmniMMI interactive streaming video benchmark. (from "Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models")
10. Chameleon improves the best-published few-shot result on ScienceQA by 11.37%. (from "Agents")
11. An agent is characterized by the environment it operates in and the set of actions it can perform. (from "Agents")
12. Chameleon improves accuracy on TabMWP (Tabular Math Word Problems) by 17%. (from "Agents")
13. PAM uses PaliGemma as its base VLM with LoRA rank of 32 and alignment percentage of 50%. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
14. Applying post-training alignment (TIES) to the penultimate task prior to merging results in a 7.44% reduction in accuracy. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
15. Early multimodal reasoning systems employed CNNs and LSTM networks within supervised learning frameworks, adopting modular designs that decomposed reasoning into separate components: representation, a (from "Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models")

## Relationships

## Limitations and Open Questions

## Sources
