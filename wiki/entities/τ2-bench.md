---
type: entity
title: τ2-bench
entity_type: dataset
theme_ids:
- agent_systems
- finetuning_and_distillation
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reinforcement_learning
- software_engineering_agents
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0003341620231636353
staleness: 0.0
status: active
tags: []
---
# τ2-bench

> τ2-bench is a benchmark designed to evaluate agentic systems on constraint-satisfaction tasks requiring collaboration in dual-control environments, where an agent must coordinate actions across interdependent decision spaces. It has emerged as a key evaluation surface for frontier tool-use and multi-agent systems, with recent results showing that smaller, efficiently-trained models can surpass much larger ones — raising questions about what the benchmark actually measures and whether score improvements track general agentic capability.

**Type:** dataset
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

τ2-bench targets a class of agentic tasks that go beyond single-turn tool invocation: agents must satisfy constraints and collaborate within dual-control setups, where decisions in one part of the environment affect what is feasible in another. This structure makes it a more demanding evaluation than flat tool-use benchmarks, probing whether a model can reason about action legality and sequencing under mutual constraints across a multi-turn trajectory.

The benchmark has become a standard point of comparison for systems that combine multi-turn reasoning with tool orchestration. Its dual-control framing makes it particularly sensitive to whether an agent plans ahead or greedily acts — a distinction that separates reactive tool-calling from genuine agentic behaviour.

## Key Findings

The most striking result on τ2-bench comes from ToolOrchestra, where Orchestrator-8B achieves **80.2%**, compared to GPT-5's 77.7%, Claude Opus 4.1's 76.8%, and Qwen3-235B-A22B's 75.6%. This is not a marginal gap — Orchestrator-8B outperforms models orders of magnitude larger while using roughly 30% of GPT-5's compute cost. The result is consistent with ToolOrchestra's performance on FRAMES (76.3% vs. GPT-5's 74.0%) and HLE (37.1% vs. GPT-5's 35.1%), suggesting a systematic efficiency advantage rather than benchmark-specific overfitting.

ToolOrchestra achieves this through end-to-end reinforcement learning over a multi-turn reasoning–action–observation loop (up to 50 turns), with reward signals balancing correctness, resource efficiency, and alignment with user preferences. Crucially, the system is trained on synthetically generated multi-turn tool-use trajectories via the ToolScale dataset — thousands of verifiable examples across 10 domains — which provides the dense supervision signal RL requires without relying on human demonstrations. The agentic task is formalized as an MDP incorporating user action preferences, costs, latency, and correctness reward, making τ2-bench's constraint-satisfaction structure a natural fit for the training objective.

From Nex-N1, τ2-bench serves as an evaluation target for systems trained across hierarchically structured agent graphs — from single ReAct agents to multi-layer multi-agent systems with up to 34 nodes. NexAU's recursive, fractal architecture, where sub-agents are exposed to parent agents as typed tools with defined input schemas, provides a natural decomposition for the dual-control problems τ2-bench poses. The AgentScaler work, which constructs training environments from over 30,000 APIs across 1,000+ tool domains, similarly treats τ2-bench as an out-of-distribution generalization test for agents trained at environment scale.

## Limitations and Open Questions

The fact that Orchestrator-8B — an 8B-parameter model trained specifically on synthetic multi-turn tool-use data — tops the τ2-bench leaderboard raises a structural question: does the benchmark's constraint-satisfaction framing reward genuine generalisation, or does it reward fine-tuning on sufficiently similar synthetic trajectories? The ToolOrchestra training pipeline is purpose-built for exactly the kind of multi-turn tool-use the benchmark evaluates, and the synthetic data is generated to be *verifiable* — meaning the reward signal is well-shaped for τ2-bench's task class. Score improvements may thus reflect optimisation against the benchmark's implicit structure rather than a broader capability advance.

The dual-control framing also leaves open what "collaboration" means operationally: whether the benchmark involves two distinct agents coordinating, a single agent managing two interacting action spaces, or something else is not made explicit in the claims available. This ambiguity matters for interpreting results across systems with very different architectures — a single orchestrator versus a recursive multi-agent hierarchy may solve the benchmark's tasks via fundamentally different mechanisms.

Finally, all three source papers treat τ2-bench as one point in a multi-benchmark evaluation suite rather than as a primary design target. Its role as a *differentiator* — where systems with strong general tool-use training tend to score well — suggests it captures something real, but its coverage of the full space of agentic constraint satisfaction remains unclear.

## Relationships

τ2-bench is most directly associated with the ToolOrchestra system (ToolOrchestra), which currently holds the highest reported score. It appears alongside FRAMES and HLE as part of a standard evaluation trio for tool-use agents, where FRAMES tests multi-hop retrieval and HLE tests hard reasoning — together probing complementary aspects of agentic intelligence. Systems from Nex-N1 and AgentScaler treat it as a downstream generalisation target, connecting it to the broader agenda of scaling environment diversity during training to produce agents that transfer across task classes.

## Sources
