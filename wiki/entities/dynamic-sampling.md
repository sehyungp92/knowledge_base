---
type: entity
title: dynamic sampling
entity_type: method
theme_ids:
- chain_of_thought
- creative_content_generation
- finetuning_and_distillation
- generative_media
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0008934353184324623
staleness: 0.0
status: active
tags: []
---
# dynamic sampling

Dynamic sampling is an online data filtering technique used during reinforcement learning training of language models that selectively removes training examples based on rollout outcomes, retaining only problems of intermediate difficulty where the model shows genuine uncertainty. By discarding both trivially easy examples (where all rollouts succeed) and intractably hard ones (where none do), the method concentrates gradient signal on the productive learning margin, where exploration is meaningful and reward feedback is discriminative. The approach has gained traction as a lightweight but consequential component of RL post-training pipelines, most visibly in work like JustRL.

**Type:** method
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/creative_content_generation|creative_content_generation]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/generative_media|generative_media]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Dynamic sampling operates as an online filter applied per training batch: for each problem, the model generates a group of rollouts (e.g., 8), and the example is dropped from the update if all rollouts are correct (8/8) or all are incorrect (0/8). Only examples with mixed outcomes survive, producing a training signal that is neither saturated nor hopeless. For 1.5B-scale models, this filter typically removes roughly half of all candidate examples, meaning the effective training curriculum is substantially narrower than the raw data pool.

The intuition is clean and has antecedents in curriculum learning and adaptive difficulty scheduling: reward gradients are uninformative at the extremes. A problem every rollout solves produces no variance in outcome and thus no useful policy gradient; a problem no rollout ever solves produces equally flat signal. The productive zone is in between, and dynamic sampling mechanically enforces training within it.

In the context of JustRL, this filter is part of a deliberately minimal recipe. JustRL uses GRPO with binary outcome rewards, a lightweight rule-based verifier derived from DAPO (without symbolic math libraries), and asymmetric clipping ("clip higher," ratio [0.8, 1.28]) as its only non-default modification. Dynamic sampling sits alongside these choices as an unremarkable but load-bearing component, contributing to a training run that achieves 55% on AIME 2024 with 1.5B parameters across roughly 15 days on 32 A800-80GB GPUs. The framing in JustRL is notable: the authors treat dynamic sampling not as a clever trick but as part of the default baseline, consistent with the paper's broader argument that simplicity is underrated in RL post-training.

The interaction with other training choices is instructive. JustRL reports that adding an explicit overlong penalty causes entropy collapse (entropy dropping to 0.5–0.6 from a healthy 1.2–1.4 baseline) and caps AIME 2024 performance at 50% rather than 55%. Dynamic sampling, by contrast, preserves exploration by keeping the model in a regime where both success and failure are possible. The implicit lesson is that filtering for difficulty and penalizing length are not interchangeable tools for managing training stability; they operate on different mechanisms and can have opposing effects on the entropy profile.

## Relationship to Curriculum and Data Quality

Dynamic sampling can be understood as a form of implicit curriculum: rather than pre-sorting a dataset by difficulty, it adapts the training distribution at each step based on the model's current competence. This distinguishes it from static filtering approaches and gives it an online character. As training progresses and the model improves, problems that once had mixed outcomes may shift to all-correct, at which point they drop out of the training set. The curriculum self-adjusts without any explicit difficulty oracle.

This connects to the broader trend in RL for reasoning toward data quality over data quantity. Pipelines like DeepScaleR use staged context length expansion (8K to 16K to 24K) as a different axis of curriculum control; dynamic sampling operates on outcome variance rather than length. Both reflect a growing recognition that the distribution of training examples matters as much as their volume, and that naive dataset scaling without attention to difficulty distribution is wasteful or actively harmful.

## Limitations and Open Questions

The ~50% filter ratio observed at 1.5B scale is an empirical estimate and may not generalize cleanly to larger models or different task domains. JustRL explicitly acknowledges that its results are limited to mathematical reasoning at 1.5B scale, and that generalization to coding, general question answering, and larger model sizes remains unexplored. This is a significant gap: mathematical reasoning has a natural, well-behaved difficulty distribution, and the filter may behave very differently on domains where rollout variance has different structure.

A related open question is how dynamic sampling interacts with the choice of group size. The 8-rollout design is implicit in the 8/8 and 0/8 thresholds; smaller or larger groups would shift the filter's sensitivity. With fewer rollouts, more examples would survive (since achieving unanimity in either direction is harder), potentially admitting noisier signal. With more rollouts, the filter becomes more aggressive. This hyperparameter has not been systematically studied.

The ~50% filter ratio also raises a compute-efficiency concern. Half of all rollouts are effectively discarded, meaning the total compute budget for data generation is approximately double what feeds into gradient updates. Whether this is justified by training stability gains, or whether smarter problem selection upstream could achieve similar effects at lower cost, is an open question. In settings where rollout generation is expensive (e.g., long-horizon problems, tool-use tasks), the overhead may matter.

Finally, dynamic sampling assumes that the 8-rollout sample is representative of the model's true difficulty on a problem. For tasks with high variance per rollout (stochastic decoding, ambiguous reward functions), the observed pass rate in a small sample may not reliably classify a problem as easy, hard, or intermediate. Noise in the filter criterion could corrupt the curriculum in ways that are difficult to detect without per-problem difficulty tracking over training time.

## Related Entities

Dynamic sampling sits at the intersection of [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] and [[themes/post_training_methods|post-training methods]], with particular relevance to curriculum design in [[themes/mathematical_and_formal_reasoning|mathematical reasoning]] pipelines. Its interaction with entropy and exploration connects it to [[themes/rl_theory_and_dynamics|RL theory and dynamics]]. Methodologically, it shares structure with difficulty-aware sampling in [[themes/robotics_and_embodied_ai|robotics and embodied AI]], where environment curriculum design is a long-standing concern. The WMPO approach to robot learning illustrates a parallel challenge: when direct RL on the target domain is impractical (due to sample cost and safety constraints), the system must carefully manage what experiences are used for training, which is a distributional cousin of the problem dynamic sampling addresses in the language domain.

## Key Findings

## Relationships

## Sources
