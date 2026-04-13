---
type: entity
title: Reinforcement Learning from Verifiable Rewards
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- context_engineering
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- knowledge_and_memory
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- scaling_laws
- software_engineering_agents
- spatial_and_3d_intelligence
- synthetic_data_generation
- test_time_compute_scaling
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0021952373511875947
staleness: 0.0
status: active
tags: []
---
# Reinforcement Learning from Verifiable Rewards

> Reinforcement Learning from Verifiable Rewards (RLVR) is a post-training paradigm that optimizes language and multimodal models against objective, automatically checkable reward signals — such as math answer correctness or code execution results — rather than human preference judgments. By removing the human rater from the reward loop, RLVR enables longer and more stable optimization runs, and has been credited with the spontaneous emergence of extended reasoning strategies in frontier models. It became a defining technique of the 2024–2025 post-training era, underpinning the reasoning capabilities of models like DeepSeek-R1 and, more recently, extending into embodied and game-playing agents.

**Type:** method
**Themes:** [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/context_engineering|context_engineering]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/generative_media|generative_media]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/scaling_laws|scaling_laws]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/spatial_and_3d_intelligence|spatial_and_3d_intelligence]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

RLVR distinguishes itself from RLHF by the nature of its reward signal. Where RLHF depends on a trained reward model acting as a proxy for human judgment — a proxy that can be gamed and that degrades over long optimization — RLVR binds the reward to ground truth: a math answer either matches the reference or it doesn't; code either passes the test suite or it doesn't. This non-gameability is what makes extended RL runs viable, and those extended runs are where emergent reasoning behaviors — self-checking, backtracking, extended chain-of-thought — appear to arise.

The paradigm's influence extends well beyond text-domain puzzles. SIMA 2 applies RLVR after supervised finetuning in a game-playing setting, where curated tasks are defined as tuples of initial game state, text instruction, and a verifiable completion criterion. This structural equivalence — a game task checked by a rule engine maps cleanly onto a math problem checked by a symbolic verifier — has allowed the RLVR recipe to travel from language-only reasoning models into fully embodied, visually grounded agents.

## The SIMA 2 Case: RLVR in Embodied AI

The most detailed picture available of RLVR applied to an embodied agent comes from SIMA 2, Google DeepMind's generalist game-playing model. The system's training proceeds in stages: first, supervised finetuning on a mixture of human gameplay annotated with synthetically generated reasoning traces and dialogue ("bridge data"), and only then online RLVR against verifiable game task rewards.

Critically, RLVR training is explicitly restricted to training environments and withheld from held-out environments such as ASKA and MineDojo. This is a deliberate methodological choice: it preserves the held-out set as a clean generalization test, but it also reveals a structural limitation — the verifiable reward signal is only available where someone has built the verification infrastructure. Generalization to new environments, including photorealistic worlds generated on-the-fly by Genie 3, is achieved not through RL but through the breadth of the supervised stage.

The SIMA 2 architecture also illustrates how RLVR composes with other components. Three foundation models operate together: a task setter (generating tasks), the agent itself, and a reward model that evaluates task completion. A world model (Genie 3) provides the environment. This decomposition — generator, learner, judge — is itself a template for open-ended self-improvement: by having Gemini generate tasks and provide rewards, SIMA 2 can autonomously acquire new skills in new environments from scratch, without human-curated curricula for each new domain.

## Broader Significance and Market Dynamics

The accessibility of RLVR relative to RLHF has had significant competitive consequences. Because verifiable reward functions for math and code require no proprietary human preference data, RLVR lowered the barrier for labs — most prominently DeepSeek — to achieve frontier reasoning capabilities at dramatically reduced cost. This is discussed directly in David Luan on DeepSeek's Significance and Julian Schrittwieser on Scaling RL, where the technique is presented as a key reason DeepSeek's results were both surprising in their quality and reproducible without massive compute.

Nathan Lambert's account in Everything You Wanted to Know About LLM Post-Training situates RLVR within the broader post-training landscape: it occupies a particular niche — domains with unambiguous ground truth — and does not straightforwardly generalize to open-ended tasks like writing or instruction-following where correctness is inherently contestable.

## Limitations and Open Questions

The method's core strength is also its core constraint: **it only works where verification is cheap and unambiguous**. Math, code, formal logic, and rule-bound game tasks all satisfy this criterion. But large swaths of valuable capability — nuanced reasoning about social situations, creative writing quality, scientific hypothesis generation — do not. This is not a solvable engineering problem within the current RLVR framing; it is a definitional boundary.

Within verifiable domains, several tensions remain unresolved:

- **Reward scope vs. exploration scope.** SIMA 2's RL training is confined to environments where verification infrastructure exists. Every new environment requires either building a verifier or relying on a foundation model to act as one — and foundation model reward signals reintroduce the reliability questions that make RLHF fragile.
- **Capability preservation.** SIMA 2 found it necessary to maintain a mixture of gameplay and non-gameplay Gemini pretraining data throughout finetuning. Optimizing hard on verifiable game rewards without this mixture degraded base capabilities like vision understanding and general reasoning — a form of catastrophic forgetting that suggests RLVR pressure is not narrowly targeted.
- **Aggregation under majority voting.** The Majority is not always right examines a related failure mode: using outcome-verified majority voting to aggregate RL-trained solutions can systematically favor confident-but-wrong consensus answers over correct minority solutions, suggesting that even in verifiable settings the training signal can mislead at the level of selection strategy.
- **Emergent reasoning: how and why.** The emergence of chain-of-thought and self-correction strategies from RLVR optimization is empirically documented but mechanistically underexplained. Whether these behaviors reflect genuine internalization of reasoning or surface-level pattern exploitation that will break under distribution shift remains an open question across the field.

## Relationships

RLVR is the primary engine behind the [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] wave, and is closely coupled to [[themes/test_time_compute_scaling|test-time compute scaling]] — the extended reasoning chains it enables are what models spend compute on at inference time. It intersects [[themes/agent_self_evolution|agent self-evolution]] through the open-ended self-improvement loop demonstrated by SIMA 2, where the reward function itself is generated by another model rather than hardcoded.

It sits in tension with [[themes/reward_modeling|reward modeling]]: RLVR emerged partly as a response to reward model hacking in RLHF, but as it expands into less structured domains it faces pressure to reintroduce learned reward models — at which point the distinction between the two paradigms begins to blur.

Key source connections: SIMA 2, 2025 LLM Year in Review, The Majority is not always right, Julian Schrittwieser on Scaling RL, David Luan on DeepSeek's Significance, Nathan Lambert on LLM Post-Training.

## Key Findings

## Sources
