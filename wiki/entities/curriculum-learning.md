---
type: entity
title: Curriculum Learning
entity_type: method
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- code_and_software_ai
- code_generation
- frontier_lab_competition
- multi_agent_coordination
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- robotics_and_embodied_ai
- robot_learning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.001080116716740621
staleness: 0.0
status: active
tags: []
---
# Curriculum Learning

Curriculum learning is a training strategy that structures the acquisition of complex skills by decomposing them into staged sub-tasks — simpler precursors that scaffold toward a harder target objective. Its significance in modern RL lies in making otherwise intractable policies learnable: tasks that fail entirely when attempted from scratch become achievable when approached through a well-ordered sequence of intermediate challenges.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/robotics_and_embodied_ai|Robotics & Embodied AI]], [[themes/robot_learning|Robot Learning]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/scaling_laws|Scaling Laws]]

---

## Overview

Curriculum learning addresses a core failure mode in reinforcement learning: the sparse-reward cold-start problem, where an agent cannot stumble upon task-completing behavior often enough to learn anything meaningful. Rather than presenting the full difficulty from the outset, a curriculum sequences the learning problem so that earlier stages produce a policy that meaningfully initializes the harder one.

The canonical demonstration in recent literature comes from the EUREKA system applied to dexterous pen spinning with a simulated Shadow Hand. Pen spinning is a continuous, high-dimensional manipulation task requiring coordinated finger control that direct RL training — even with EUREKA-generated rewards — completely fails to learn. The curriculum solution is two-stage: first train a policy on random pen re-orientation (a simpler, more densely rewarded precursor), then fine-tune that policy on the full spinning objective using an EUREKA-generated reward. This staged approach yields a policy that spins the pen successfully for many consecutive cycles, a result that neither stage achieves in isolation.

---

## Role Within EUREKA

Curriculum learning is not intrinsic to EUREKA's reward generation mechanism — it is an add-on that extends the system's reach to tasks that remain out of scope even for automated reward design alone. EUREKA's core loop generates executable reward functions from raw environment source code, refines them through in-context evolutionary search (iterating over the best reward from each prior round), and uses *reward reflection* — textual summaries of reward component values and task fitness at training checkpoints — to guide targeted mutation. This loop outperforms expert human-engineered rewards on 83% of tasks across 29 RL environments, with an average normalized improvement of 52%, and matches or exceeds human-level performance on all Isaac tasks and 15 of 20 Dexterity tasks.

But pen spinning sits outside the reach of reward design alone. Curriculum learning fills the gap: the re-orientation policy provides a warm-start that collapses the exploration problem for the spinning stage. The combination — EUREKA rewards plus curriculum — achieves what neither achieves separately. Removing reward reflection from the EUREKA loop degrades average normalized score by 28.6% on Isaac tasks, with larger drops on higher-dimensional tasks; by analogy, the curriculum stage similarly acts as a structural scaffold whose removal causes complete collapse rather than mere degradation.

---

## Relationship to Pretraining and Imitation

Curriculum learning shares a structural logic with imitation-based pretraining: both use an easier or more abundant signal to initialize a model before exposing it to the harder target objective. In pretraining, random weights are adapted to imitate large volumes of human-generated data, creating a starting point for downstream fine-tuning. In curriculum RL, a policy trained on a simpler reward landscape is adapted to a harder one. The key difference is the domain of the prior signal — demonstrations versus a structured sub-task — but the underlying principle of staged initialization is the same. After training concludes in either regime, weights are frozen; all downstream behavior flows from the fixed checkpoint with no further adaptation during deployment.

---

## Limitations and Open Questions

The central limitation of curriculum learning is **curriculum design itself**. The pen-spinning example works because a natural sub-task (re-orientation) exists that shares structure with the full task (spinning) while being independently learnable. This relationship is not always obvious or even well-defined. For tasks without a clear hierarchical decomposition, identifying the right staging remains a manual, expert-dependent process — the same bottleneck that afflicts reward design more broadly. The survey underlying EUREKA found that 92% of RL researchers and practitioners rely on manual trial-and-error reward design, and 89% consider their designed rewards sub-optimal; curriculum design faces the same human bottleneck.

It is also unclear how curriculum learning interacts with EUREKA's evolutionary search when the curriculum itself is part of the optimization target. EUREKA's experiments fix the curriculum structure (re-orientation → spinning) and search over rewards within that structure. Whether automated curriculum discovery — learning the sequence of sub-tasks jointly with the rewards — is tractable with LLM-based code generation is an open question. The gradient-free in-context RLHF mechanism EUREKA enables (steering reward generation via human textual feedback without model weight updates) points toward one direction: human feedback could in principle guide curriculum construction, though this has not been demonstrated.

Finally, curriculum learning's sample efficiency benefits come with a cost: total training is multi-stage, and each stage requires its own reward and policy. For the pen-spinning case this is manageable, but for tasks requiring many curriculum stages, the engineering overhead compounds quickly.

---

## Relationships

- **Eureka: Human-Level Reward Design via Coding Large Language Models** — primary source; curriculum learning appears as the enabling mechanism for pen spinning, the hardest task in the EUREKA benchmark suite.
- **Gemini 2.0 and the evolution of agentic AI | Oriol Vinyals** — provides context on pretraining as a structurally analogous staged initialization regime.
- **[[themes/reward_modeling|Reward Modeling]]** — curriculum learning is downstream of reward design; a well-specified intermediate reward is required for each curriculum stage.
- **[[themes/robotics_and_embodied_ai|Robotics & Embodied AI]]** — dexterous manipulation is the domain where curriculum learning is most visibly necessary; sparse reward problems are most severe in high-dimensional continuous control.
- **[[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]** — staged training (easier problems before harder ones) is an active area of application for reasoning model training, where curriculum learning principles apply to problem difficulty ordering rather than task decomposition.

## Key Findings

## Sources
