---
type: entity
title: Eureka
entity_type: method
theme_ids:
- code_and_software_ai
- code_generation
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 9.700586014991e-05
staleness: 0.0
status: active
tags: []
---
# Eureka

Eureka is a large language model-based reward design system that automatically generates executable reward functions directly from environment source code, eliminating the need for human reward engineering in reinforcement learning. Developed by NVIDIA, it represents a significant step toward automating one of RL's most labor-intensive bottlenecks — reward shaping — by treating reward generation as a code synthesis problem and iteratively refining solutions using policy training feedback. Its successor, DrEureka, extends this approach to sim-to-real transfer by additionally automating domain randomization configuration.

**Type:** method
**Themes:** [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]], [[themes/robot_learning|robot_learning]], [[themes/vision_language_action_models|vision_language_action_models]]

## Overview

Eureka addresses a fundamental problem in applied RL: reward design is largely manual, expert-dependent, and acknowledged to be sub-optimal by its own practitioners. A survey cited in the original paper found that 92% of RL researchers and practitioners rely on manual trial-and-error, with 89% believing their resulting rewards are sub-optimal. Eureka's core insight is that LLMs, given raw environment source code as context, can generate syntactically valid and semantically meaningful reward functions in a zero-shot fashion — no task-specific prompts, reward templates, or few-shot examples required.

The algorithm runs an **in-context evolutionary search**: it samples 16 reward function candidates per iteration, trains policies on each, and uses *reward reflection* — a textual summary of individual reward component magnitudes and task fitness at training checkpoints — to identify what is and isn't working. The best-performing reward from each iteration is mutated in the next via an appended reflection-and-mutation prompt. This loop runs for 5 iterations across 5 independent random restarts, giving Eureka 400 policy evaluations per environment in the standard configuration.

## Key Findings

### Performance and Benchmarks

Eureka's headline result is that it outperforms expert human-engineered rewards on 83% of tasks across 29 RL environments, with an average normalized improvement of 52%. It exceeds or matches human-level performance on all Isaac tasks and 15 of 20 Dexterity tasks. The most striking demonstration is dexterous pen spinning with a simulated Shadow Hand — a task neither human-designed rewards nor naive LLM-generated rewards could solve — achieved by combining Eureka rewards with curriculum learning. These results position Eureka not merely as competitive with human reward design but as capable of discovering reward structures that humans consistently fail to find.

### The Reward Reflection Mechanism

A key architectural contribution is the reward reflection signal. Rather than relying on scalar training curves alone, Eureka generates natural language summaries that describe *which reward components* are contributing what magnitudes at various training stages, alongside a measure of task fitness. Ablations show this mechanism is load-bearing: removing it reduces average normalized score by 28.6% on Isaac tasks, with steeper degradation on higher-dimensional environments where diagnosing reward misspecification becomes harder. This positions reward reflection as a domain-general debugging scaffold for automated reward engineering.

### Gradient-Free RLHF

Eureka's architecture naturally supports a gradient-free form of RLHF: human textual feedback can be injected into the evolutionary loop to steer reward generation without any model weight updates. This is notable as a practical middle ground — human preferences shape the reward structure while the LLM remains frozen — but also raises questions about how consistently human feedback integrates with the automated reflection signal and whether the two can conflict.

### DrEureka: Extending to Sim-to-Real

DrEureka inherits Eureka's reward generation pipeline and augments it with automated domain randomization (DR) configuration, addressing the full sim-to-real problem from a single physics simulation. Using GPT-4 as its backbone and sampling 16 DR configurations in parallel (with real-world evaluation), DrEureka's policies outperform human-designed configurations on quadruped locomotion by 34% in forward velocity and 20% in distance traveled across varied real-world terrains. In dexterous manipulation, its best policy achieves nearly 300% more in-hand cube rotations than the human-developed baseline within a fixed period. The safety instruction augmentation is a practical addition — it constrains the reward and DR search toward configurations less likely to damage hardware or produce erratic behavior.

## Limitations and Open Questions

Several limitations are worth noting. Eureka's evaluation budget (400 policy runs per environment) is computationally heavy and assumes access to fast GPU-based simulation; the approach as described does not extend cleanly to real-world-only settings or slow simulators. The method also depends on the LLM's ability to parse and reason about raw environment source code, which scales poorly with code complexity or proprietary environments. The pen-spinning result, while impressive, required curriculum learning on top of Eureka rewards — suggesting the reward generation alone may be insufficient for the hardest manipulation tasks, and that the combination of automated reward design with other techniques is where the real capability lies.

The gradient-free RLHF mechanism is promising but underspecified: there is no systematic study of how human feedback interacts with the automated reflection signal across conflicting objectives, how many human interventions are needed to meaningfully steer outcomes, or how robust the mechanism is to imprecise human language.

DrEureka's safety instruction mechanism is described but not thoroughly characterized — it remains unclear how reliably LLM-generated safety constraints translate to physical safety margins, especially as tasks become more dynamic or contact-rich.

## Relationships

Eureka is directly related to Eureka: Human-Level Reward Design via Coding Large Language Models and DrEureka: Language Model Guided Sim-To-Real Transfer. It connects thematically to [[themes/reinforcement_learning|reinforcement_learning]] bottlenecks around reward specification and to [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]] work on dexterous manipulation and locomotion. The sim-to-real thread links it to broader efforts in [[themes/robot_learning|robot_learning]] on domain randomization and transfer. The use of LLMs as code generators positions it within [[themes/code_and_software_ai|code_and_software_ai]], and the reward reflection mechanism has conceptual overlap with self-critique patterns in [[themes/reinforcement_learning|reinforcement_learning from human feedback]]. Jim Fan's broader work on NVIDIA's embodied AI infrastructure provides additional context for where Eureka sits within the lab's long-term robotics research agenda.

## Sources
