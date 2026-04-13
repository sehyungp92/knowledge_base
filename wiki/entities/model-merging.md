---
type: entity
title: Model Merging
entity_type: method
theme_ids:
- alignment_and_safety
- alignment_methods
- continual_learning
- finetuning_and_distillation
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0007421143317469628
staleness: 0.0
status: active
tags: []
---
# Model Merging

> Model merging is a family of techniques for combining the parameters of multiple fine-tuned models into a single unified model, typically through weighted averaging or more sophisticated aggregation strategies. It has emerged as a practical approach to multi-task learning, continual learning, and post-training alignment, offering a way to consolidate specialized capabilities without the computational cost of joint training or the catastrophic forgetting risk of sequential fine-tuning.

**Type:** method
**Themes:** [[themes/alignment_and_safety|Alignment and Safety]], [[themes/alignment_methods|Alignment Methods]], [[themes/continual_learning|Continual Learning]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/multimodal_models|Multimodal Models]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/vision_language_models|Vision-Language Models]]

## Overview

Model merging combines the weights of models trained on different tasks or objectives, typically starting from the same base checkpoint, to produce a single model that inherits capabilities from each branch. The most straightforward variant is parameter averaging, but the field has developed more targeted methods that selectively aggregate parameters aligned across tasks. Its appeal is practical: it avoids storing and serving multiple specialized models, sidesteps the data-availability constraints of joint training, and can be applied post hoc to already-trained checkpoints.

## Key Findings

### Model Merging in the Post-Training Stack

Model merging has found a concrete role in the post-training pipelines of frontier systems. Kimi k1.5 explicitly employs model merging as a component of its RL-based post-training recipe, using it to improve training efficiency and stabilize the resulting policy. Notably, the Kimi k1.5 system excludes a value network from its RL training, and model merging contributes to compensating for this design choice by consolidating capabilities across training stages. The downstream results are strong: Kimi k1.5 short-CoT reaches 94.6 on MATH500 (versus 78.3 for Claude 3.5 Sonnet and 74.6 for GPT-4o), 60.8 on AIME 2024 (outperforming GPT-4o's 9.3 and Claude 3.5 Sonnet's 16 by up to 550%), and 47.3 on LiveCodeBench v4. The long-CoT variant pushes further: 96.2 on MATH500, 77.5 on AIME, 62.5 on LiveCodeBench v5, and 74.9 on MathVista, matching or exceeding OpenAI o1 across all of these.

These results do not isolate model merging's specific contribution; they reflect the full system. But their inclusion of merging in the recipe signals that the technique is no longer niche, it is part of how competitive post-training pipelines are assembled. As noted in discussions around LLM post-training (see Everything You Wanted to Know About LLM Post-Training), model merging sits alongside SFT, RL, and distillation as a recognized tool for shaping model behavior after pretraining.

### Continual Learning in Vision-Language Models

A more targeted application comes from Continual Learning in Vision-Language Models via Aligned Model Merging, which introduces PAM (Parameter-Aligned Merging) as a solution to a specific and difficult constraint: learning new tasks without access to previous task data, and without knowing task identity at inference time. This is the hardest continual learning setting, and sequential fine-tuning performs poorly under it, achieving 43.36 ± 8.18 average accuracy on the CoIN benchmark with high variance. PAM reaches 49.89 ± 1.66, a meaningful gain with substantially reduced variance, suggesting that merging provides both better performance and more stable generalization.

The alignment step in PAM is the key contribution. Rather than naively averaging checkpoints, PAM aligns the parameter spaces of task-specific models before merging, reducing destructive interference between specialized weights. The constraints it operates under are worth emphasizing: no replay, no task labels at test time. These are realistic deployment conditions that many continual learning methods quietly relax. The benchmark improvement, while not dramatic in absolute terms, is achieved in a genuinely harder setting.

## Limitations and Open Questions

Model merging carries several underexplored tensions. First, its benefits are most reliable when merged models share a base checkpoint and were fine-tuned on sufficiently distinct tasks; when tasks overlap or interfere, merging can degrade performance on all of them. Second, the technique is largely black-box in its effects: it is difficult to predict in advance which capabilities will be preserved, which will be diluted, and which will interact unexpectedly. Third, in the context of RL-based post-training (as in Kimi k1.5), merging is embedded in a complex pipeline where its individual contribution cannot easily be isolated from other design choices such as reward shaping, context length scaling, or the removal of the value network.

The continual learning framing surfaces a deeper open question: whether merging can scale to long task sequences. PAM demonstrates gains at the scale of the CoIN benchmark, but it is unclear how parameter alignment holds up as the number of sequentially learned tasks grows and the merged parameter space becomes increasingly crowded. Catastrophic interference may simply be deferred rather than solved.

## Relationships

Model merging is closely related to [[themes/finetuning_and_distillation|finetuning and distillation]] as a post-training technique, and to [[themes/continual_learning|continual learning]] as a strategy for task-incremental adaptation without replay. Its use in RL pipelines (as in Kimi k1.5) connects it to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] and [[themes/post_training_methods|post-training methods]] more broadly. In the vision-language setting, PAM links merging directly to [[themes/vision_language_models|vision-language models]] and multimodal continual learning. The broader question of how to consolidate specialized models without degrading alignment connects to [[themes/alignment_methods|alignment methods]] and [[themes/alignment_and_safety|alignment and safety]].

## Sources
