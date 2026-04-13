---
type: entity
title: FlashAttention
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_for_scientific_discovery
- alignment_and_safety
- finetuning_and_distillation
- hallucination_and_reliability
- in_context_and_meta_learning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- scientific_and_medical_ai
- software_engineering_agents
- transformer_alternatives
- vision_language_action_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.00599730430232057
staleness: 0.0
status: active
tags: []
---
# FlashAttention

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vision_language_action_models|vision_language_action_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

IO-aware attention kernel implementation reducing memory requirements of quadratic attention; proposed as an architectural mitigation for the quadratic memory/compute complexity that makes very long context attention infeasible.

## Key Findings

1. Fine-tuning the vision encoder during VLA training is crucial for performance, in contrast to VLM training where freezing the encoder is typically preferred. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
2. Existing learned robot policies lack robustness to scene distractors or novel objects and struggle to execute unseen task instructions. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
3. Existing VLAs are largely closed and inaccessible to the public, with limited visibility into model architecture, training procedures, and data mixture. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
4. The fused SigLIP-DinoV2 visual encoder improves spatial reasoning compared to single-encoder approaches, which is particularly beneficial for robot control. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
5. OpenVLA outperforms the closed RT-2-X (55B parameters) by 16.5% absolute task success rate across 29 tasks and multiple robot embodiments, while using 7x fewer parameters. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
6. OpenVLA can be fine-tuned on consumer-grade GPUs via low-rank adaptation (LoRA) and served efficiently via quantization without a hit to downstream task success rate. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
7. OpenVLA is a 7B-parameter open-source vision-language-action model trained on 970k real-world robot demonstrations from the Open X-Embodiment dataset. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
8. OpenVLA uses next-token prediction with cross-entropy loss evaluated only on predicted action tokens, not on image or text tokens. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
9. Fine-tuned OpenVLA outperforms Diffusion Policy by 20.4% on multi-task environments involving multiple objects and language grounding. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
10. The Prismatic VLM backbone outperformed LLaVA by approximately 10% absolute success rate on both simple single-object tasks and multi-object language grounding tasks. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
11. OpenVLA achieves best results with a fixed learning rate of 2e-5 and no learning rate warmup. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
12. OpenVLA training used data mixture weights from Octo, which heuristically down-weights less diverse datasets and up-weights datasets with larger task and scene diversity. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
13. The largest robot manipulation datasets contain only 100K to 1M examples, creating an imbalance with Internet-scale vision-language pretraining data. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
14. OpenVLA discretizes each robot action dimension into 256 bins using quantile-based bounds (1st to 99th percentile) rather than min-max bounds. (from "OpenVLA: An Open-Source Vision-Language-Action Model")
15. OpenVLA uses a two-part visual encoder that concatenates pretrained DINOv2 and SigLIP features channel-wise to capture both spatial and semantic information. (from "OpenVLA: An Open-Source Vision-Language-Action Model")

## Capabilities

- Evolutionary coding agent discovers and deploys production-grade infrastructure optimizations autonomously: 0.7% Google fleet-wide compute recovery from scheduling heuristics, 23% kernel speedup for G (maturity: narrow_production)
- AI agent can directly optimize compiler-generated intermediate representations (IRs) of production ML kernels, despite IRs being designed for debugging not editing — achieving 32% speedup on FlashAtte (maturity: narrow_production)

## Known Limitations

- Reliance on cuBLAS Sgemm for GEMM operations rather than custom tiled kernels or FlashAttention-style fused memory-efficient implementations means the approach does not exploit modern memory-bandwidth (severity: minor, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
