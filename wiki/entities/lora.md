---
type: entity
title: LoRA
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- alignment_and_safety
- alignment_methods
- benchmark_design
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- knowledge_and_memory
- medical_and_biology_ai
- model_architecture
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
- representation_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- scientific_and_medical_ai
- spatial_and_3d_intelligence
- test_time_learning
- transformer_alternatives
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 13
sources_since_update: 0
update_count: 1
influence_score: 0.01485816250079864
staleness: 0.0
status: active
tags: []
---
# LoRA

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

Low-Rank Adaptation. A gradient-based fine-tuning technique that decomposes weight updates into low-rank matrices (M ≈ M_0 + AB^T) to reduce memory and computational costs. EGGROLL is the ES analog of LoRA.

## Key Findings

1. OpenVLA training used data mixture weights from Octo, which heuristically down-weights less diverse datasets and up-weights datasets with larger task and scene diversity. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
2. Existing learned robot policies lack robustness to scene distractors or novel objects and struggle to execute unseen task instructions. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
3. Fine-tuned OpenVLA outperforms Diffusion Policy by 20.4% on multi-task environments involving multiple objects and language grounding. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
4. OpenVLA discretizes each robot action dimension into 256 bins using quantile-based bounds (1st to 99th percentile) rather than min-max bounds. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
5. Fine-tuning the vision encoder during VLA training is crucial for performance, in contrast to VLM training where freezing the encoder is typically preferred. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
6. OpenVLA can be fine-tuned on consumer-grade GPUs via low-rank adaptation (LoRA) and served efficiently via quantization without a hit to downstream task success rate. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
7. OpenVLA uses next-token prediction with cross-entropy loss evaluated only on predicted action tokens, not on image or text tokens. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
8. OpenVLA is a 7B-parameter open-source vision-language-action model trained on 970k real-world robot demonstrations from the Open X-Embodiment dataset. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
9. Existing VLAs are largely closed and inaccessible to the public, with limited visibility into model architecture, training procedures, and data mixture. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
10. The largest robot manipulation datasets contain only 100K to 1M examples, creating an imbalance with Internet-scale vision-language pretraining data. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
11. The Prismatic VLM backbone outperformed LLaVA by approximately 10% absolute success rate on both simple single-object tasks and multi-object language grounding tasks. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
12. The fused SigLIP-DinoV2 visual encoder improves spatial reasoning compared to single-encoder approaches, which is particularly beneficial for robot control. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
13. OpenVLA achieves best results with a fixed learning rate of 2e-5 and no learning rate warmup. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
14. OpenVLA outperforms the closed RT-2-X (55B parameters) by 16.5% absolute task success rate across 29 tasks and multiple robot embodiments, while using 7x fewer parameters. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
15. OpenVLA uses a two-part visual encoder that concatenates pretrained DINOv2 and SigLIP features channel-wise to capture both spatial and semantic information. (from "OpenVLA: An Open-Source Vision-Language-Action Model")

## Capabilities

- Reasoning agents can autonomously decompose a task into multi-step search plans, execute iterative information-gathering actions, branch exploration dynamically, and synthesise a final result — withou (maturity: demo)
- Language Agent Tree Search (LATS): adapts Monte Carlo Tree Search to language agents, enabling multi-trajectory exploration, high-reward path prioritization, feedback incorporation, and backtracking (maturity: research_only)
- TTT using leave-one-out in-context tasks with per-task LoRA adapters surpasses standard few-shot prompting on BIG-Bench Hard by 7.3 percentage points (50.5% → 57.8%) in the 10-shot setting. (maturity: research_only)
- TTT with LoRA adapters enables parameter-efficient test-time adaptation using only a small number of in-context demonstration pairs, without requiring full model fine-tuning. (maturity: research_only)
- Sparse autoencoders (SAEs) applied to a genomic foundation model (Evo 2) to discover and visualize interpretable biological features in model internals, with interactive tooling for exploration (maturity: research_only)

## Known Limitations

- RLHF bypassed core RL capabilities — value functions, exploration, world models, temporal abstraction — making current systems structurally incapable of deep autonomous learning (severity: significant, trajectory: improving)
- Principled real-world exploration methods that discover behaviours radically different from human priors do not yet exist in a practical form (severity: significant, trajectory: improving)
- The approach involves limited exploration of critical design choices: latent generative structure, chunk size, MC sampling strategy, and warmstart model choice are all under-explored, meaning the repo (severity: minor, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
