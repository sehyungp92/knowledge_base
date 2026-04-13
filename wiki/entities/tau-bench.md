---
type: entity
title: tau-bench
entity_type: dataset
theme_ids:
- adaptive_computation
- agent_self_evolution
- agent_systems
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- model_architecture
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000635675669079043
staleness: 0.0
status: active
tags: []
---
# tau-bench

tau-bench is a benchmark for agentic task completion that departs from conventional automated evaluation by placing a simulated user inside the evaluation loop. Rather than assessing whether an agent can complete tasks autonomously, tau-bench measures whether an agent can successfully navigate multi-turn interactions with a synthetic human — making it one of the closer proxies available for real-world deployment conditions where tasks unfold through dialogue rather than isolated execution.

**Type:** dataset
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/software_engineering_agents|Software Engineering Agents]]

## Overview

The core design insight of tau-bench is that realistic agentic evaluation cannot be fully decoupled from the user. Tasks in domains like retail customer service or airline booking are inherently interactive — the agent must elicit information, handle ambiguous requests, and coordinate across multiple turns to reach a goal. By simulating this interaction rather than flattening it into a static task description, tau-bench surfaces failure modes that autonomous benchmarks miss: the ability to manage conversation state, recover from misunderstandings, and adapt to shifting user intent.

The benchmark is structured around two primary domains: **Retail** and **Airline**, each with a distinct interaction graph and task distribution. As of mid-2025, frontier models cluster in a meaningful performance range — GLM-4.5 scores 70.1% overall, with 79.7 on Retail and 60.4 on Airline, matching Claude Sonnet 4 on both sub-tasks. This clustering suggests tau-bench is genuinely discriminative at the current frontier, with the Airline domain posing a harder challenge even for the strongest systems.

## Key Findings

Performance on tau-bench has emerged as a key signal for agentic capability in the 2025 model generation. GLM-4.5 — an open-source MoE model with 355B total and 32B activated parameters — achieves parity with Claude Sonnet 4 on both Retail (79.7) and Airline (60.4), and leads all compared models on BFCL v3 function calling (77.8%). This is notable given GLM-4.5 has roughly half the parameters of DeepSeek-R1 and one-third those of Kimi K2. The result situates tau-bench as a benchmark where architecture and post-training choices — rather than raw scale — appear to be the decisive variables.

The post-training methods underlying GLM-4.5's agentic performance are instructive: a two-stage pipeline separating Expert Training (domain-specialized models for reasoning, agent behavior, and general chat) from Unified Training via self-distillation, combined with a difficulty-based curriculum for RL that switches from moderate to extremely difficult problems to push past performance ceilings. This suggests that tau-bench scores are sensitive to how well post-training aligns a model to the specific dynamics of multi-turn, tool-augmented interaction.

From the Agent Learning via Early Experience perspective, a structural limitation of SFT-trained agents is directly relevant to tau-bench performance: such agents do not observe the outcomes of their own actions during training, preventing them from learning to recover from failed sub-steps — exactly the kind of recovery that interactive benchmarks like tau-bench demand.

## Known Limitations and Open Questions

The most significant methodological concern is the **user simulator dependency**. Retail evaluations in tau-bench require a high-quality instruction-following model — specifically GPT-4.1 — as the synthetic user. This creates an evaluation artifact: scores reflect the joint capability of the agent and the quality of the simulated user, not the agent alone. A weaker simulator would generate different trajectories and likely different scores, making cross-run comparisons fragile unless simulator identity is held fixed. This also introduces a dependency on a proprietary model that may change over time, raising reproducibility concerns.

A second open question is **coverage and generalization**. Tau-bench's retail and airline domains are narrow relative to the space of real-world agentic tasks. High performance in these domains does not straightforwardly imply robustness to novel domains, tool APIs with different failure modes, or users whose behavior falls outside the simulator's distribution. The benchmark's human-in-the-loop design is its strength, but its fixed domain set is a ceiling on what it can tell us about general agentic capability.

## Relationships

- Closely associated with GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models, which reports detailed sub-task scores and uses tau-bench as a primary agentic evaluation axis
- Contextually linked to Agent Learning via Early Experience, which identifies why SFT agents structurally underperform on interactive benchmarks
- Referenced alongside The Second Half in the context of evaluating whether models can handle the interactive, ambiguous second half of tasks that purely autonomous benchmarks omit
- Sits in the same evaluation tier as SWE-bench Verified and BFCL v3 as a multi-dimensional assessment of frontier agentic systems

## Limitations and Open Questions

## Sources
