---
type: entity
title: Stability-Plasticity Dilemma
entity_type: theory
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- multi_agent_coordination
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0034769861652100293
staleness: 0.0
status: active
tags: []
---
# Stability-Plasticity Dilemma

**Type:** theory
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vision_language_models|vision_language_models]]

## Overview

The fundamental tension in learning systems between maintaining stable existing knowledge (stability) and acquiring new information (plasticity). Catastrophic forgetting arises when plasticity dominates. MEMRL addresses this by decoupling frozen LLM reasoning from updatable memory.

## Key Findings

1. PAM assumes that previous task data is not available when learning a new task and that task identity is not available at inference time. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
2. PAM achieves an average accuracy of 49.89 ± 1.66 on the CoIN benchmark, compared to 43.36 ± 8.18 for sequential fine-tuning. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
3. PAM uses PaliGemma as its base VLM with LoRA rank of 32 and alignment percentage of 50%. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
4. The T2 approach (s3) achieves 58.9% average accuracy with only 2,400 training samples by training a lightweight 7B searcher subagent using frozen-generator feedback. (from "Adaptation of Agentic AI")
5. DeepSeek-R1 demonstrated that reinforcement learning with verifiable reward can effectively enhance the reasoning capabilities of large agents (from "Adaptation of Agentic AI")
6. PAM periodically re-initializes LoRA weights that become sign-misaligned with the important weights of the global LoRA during new task training. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
7. Three dominant forms of agent memory exist: token-level, parametric, and latent memory. (from "Memory in the Age of AI Agents")
8. Agent memory can be classified by function into factual memory (recording knowledge from interactions), experiential memory (enhancing problem-solving via task execution), and working memory (managing (from "Memory in the Age of AI Agents")
9. Memory dynamics are formalized through three conceptual operators: formation (transforming artifacts into memory candidates), evolution (integrating and consolidating candidates), and retrieval (const (from "Memory in the Age of AI Agents")
10. MEMRL is a non-parametric approach that enables agent self-evolution via reinforcement learning on episodic memory without modifying model weights. (from "MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory")
11. Token-level memory stores information as persistent, discrete, externally accessible units including text tokens, visual tokens, and audio frames. (from "Memory in the Age of AI Agents")
12. TextGrad improves GPT-4o's zero-shot code accuracy on LEETCODE-HARD from 26% to 36%, raises MMLU-Physics performance from 91.2% to 95.1%, and enhances the multi-tool agent CHAMELEON by 7.7% (from "Adaptation of Agentic AI")
13. Applying post-training alignment (TIES) to the penultimate task prior to merging results in a 7.44% reduction in accuracy. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
14. PAM uses element-wise averaging to merge a temporary task-specific LoRA with a global evolving LoRA after each new task. (from "Continual Learning in Vision-Language Models via Aligned Model Merging")
15. The T2 paradigm represents a conceptual inversion: rather than adapting the agent to use tools better, it adapts tools to better serve a fixed frozen agent, reframing the foundation model from optimiz (from "Adaptation of Agentic AI")

## Relationships

## Limitations and Open Questions

## Sources
