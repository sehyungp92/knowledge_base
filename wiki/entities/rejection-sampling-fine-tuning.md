---
type: entity
title: Rejection Sampling Fine-Tuning
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- chain_of_thought
- context_engineering
- finetuning_and_distillation
- knowledge_and_memory
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0007759607377496395
staleness: 0.0
status: active
tags: []
---
# Rejection Sampling Fine-Tuning

> Rejection sampling fine-tuning (RFT) is a supervised learning technique that bootstraps high-quality training signal from a model's own outputs by generating many candidate responses, filtering to those that meet a correctness criterion, and fine-tuning on the survivors. As a post-training method, it occupies a pivotal position in multi-stage pipelines — warming up a model with structured reasoning behaviors before more expensive reinforcement learning stages — and has become a standard component in state-of-the-art reasoning model recipes, most notably in the DeepSeek-R1 lineage and the IterResearch training framework.

**Type:** method
**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_systems|Agent Systems]], [[themes/chain_of_thought|Chain of Thought]], [[themes/context_engineering|Context Engineering]], [[themes/finetuning_and_distillation|Fine-Tuning and Distillation]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

Rejection sampling fine-tuning sits at the intersection of supervised learning and reinforcement learning: it uses a reward signal (typically answer correctness) to filter generated rollouts, then converts the survivors into a conventional SFT dataset. This makes it considerably cheaper than full RL while still allowing the training distribution to shift toward higher-quality outputs.

The technique's role has evolved from a standalone fine-tuning trick into a structural stage in multi-phase pipelines. In DeepSeek-R1, the full training sequence is: cold-start SFT → first RL stage → rejection sampling + SFT → second RL stage. The intermediate RFT stage serves to stabilise the model after an initial RL pass — consolidating emergent reasoning behaviors into more readable, consistent chain-of-thought patterns before the final RL stage refines them further. In IterResearch, RFT is positioned as stage 1, tasked specifically with instilling the iterative deep-research paradigm into the model before RL is applied. In both cases, the common logic is the same: RFT is a low-variance way to seed a model with a target behavioral prior, reducing the exploration burden that pure RL must overcome.

## Role in Reasoning Pipeline Development

The contrast with DeepSeek-R1-Zero is instructive. DeepSeek-R1-Zero deliberately bypasses conventional SFT before RL, operating on the hypothesis that human-defined reasoning patterns may constrain model exploration. The result is remarkable — pass@1 on AIME 2024 jumps from 15.6% to 77.9% through RL alone, and self-consistency decoding over 16 samples pushes this to 86.7%, surpassing average human competitor performance. This demonstrates that reasoning capabilities can be incentivized via pure RL without any supervised warm-up. However, DeepSeek-R1-Zero also exhibits well-documented failure modes: poor readability, language mixing (blending English and Chinese within a single chain-of-thought), and structural output degradation. These are precisely the pathologies that rejection sampling fine-tuning is used to remediate in the full DeepSeek-R1 pipeline.

This positions RFT as a *readability and stability* intervention as much as a *capability* one. The RL stages do the heavy lifting on reasoning performance; the RFT stage in between enforces stylistic consistency and format compliance — qualities that pure reward-maximization tends to neglect because they are hard to score automatically.

## Relationship to RL and Distillation

RFT occupies an interesting middle ground: it is supervised learning in mechanism but RL-adjacent in spirit, because the training examples are self-generated and filtered by outcome. This means it inherits some of the distributional advantages of on-policy RL (the model trains on its own outputs at its current capability level) while avoiding the high variance and instability of policy gradient methods.

In the IterResearch framework, where the goal is long-horizon agentic research tasks, RFT's role as a curriculum primer is especially important. IterResearch achieves a 14.5 percentage point average improvement over existing open-source deep-research agents across six benchmarks, and also functions as a prompting strategy improving frontier models by up to 19.2pp over ReAct on long-horizon tasks — even without training. The fact that the iterative paradigm transfers as a zero-shot prompting strategy suggests that RFT is teaching the model a robust behavioral schema, not just memorizing trajectories.

## Limitations and Open Questions

Several open questions surround RFT's role in reasoning pipelines:

**Coverage bias.** Rejection sampling is only as good as the model's ability to generate at least one correct response. For very hard problems where the base model's pass rate is near zero, the filter produces nothing — meaning the hardest, highest-value training signal is precisely what RFT cannot capture. This creates a capability ceiling that RL must eventually push through.

**Reward sparsity does not go away.** RFT filters on correctness but doesn't explain *why* a response was correct. The resulting SFT dataset can encode spurious reasoning steps that happened to co-occur with correct answers. Whether this introduces systematic biases in the model's chain-of-thought is an open question.

**Prompt sensitivity.** DeepSeek-R1's sensitivity to prompting — few-shot examples consistently degrade performance, making zero-shot prompting the recommended mode — may be a downstream artifact of RFT training dynamics. Training on self-generated rollouts produced under specific prompt conditions may reduce the model's robustness to distributional shift at inference time.

**Structural capability limits.** Even after RFT and multiple RL stages, DeepSeek-R1's structural output capabilities remain suboptimal relative to other models, and it cannot leverage external tools such as search engines or calculators. This suggests that RFT, while effective at instilling reasoning schemas, does not fully solve the problem of grounding those schemas in external action spaces — a gap particularly relevant for agentic applications like IterResearch.

**Interaction with scale.** DeepSeek-V3-Base, the foundation for DeepSeek-R1, has 671 billion total parameters with 37 billion activated per token, pre-trained on 14.8 trillion tokens. It is unclear how much of the RFT intervention's effectiveness is intrinsic to the method versus a product of the base model's already strong priors — raising the question of whether RFT remains necessary or sufficient at different capability levels.

## Relationships

Rejection sampling fine-tuning is structurally related to [[entities/grpo|GRPO]] (the RL algorithm used in DeepSeek-R1-Zero), which rewards final-answer correctness without constraining the reasoning process. The two methods are complementary: GRPO explores and expands, RFT consolidates and regularises. It is also adjacent to distillation methods — when a stronger teacher model is used to generate the rollouts, RFT becomes essentially knowledge distillation filtered by correctness. The [[themes/test_time_compute_scaling|test-time compute scaling]] connection is direct: RFT-trained models tend to produce the extended chain-of-thought structures that make majority voting and self-consistency techniques effective, linking training-time filtering decisions to inference-time sampling strategies.

## Key Findings

## Sources
