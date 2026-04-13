---
type: entity
title: Agent Workflow Memory
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- knowledge_and_memory
- post_training_methods
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.000648289073364033
staleness: 0.0
status: active
tags: []
---
# Agent Workflow Memory

Agent Workflow Memory (AWM) is a memory-augmented agent architecture that encodes procedural knowledge as reusable, structured workflows — sequences of environment observations, reasoning steps, and executable actions — allowing agents to generalize task strategies across novel web navigation scenarios without re-learning from scratch. It represents a significant shift from instance-level memory (storing raw trajectories) toward abstracted, transferable procedure memory, and has become a key reference point in evaluating how well agents can self-improve through accumulated experience.

**Type:** method
**Themes:** [[themes/agent_evaluation|Agent Evaluation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]], [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]], [[themes/knowledge_and_memory|Knowledge & Memory]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/test_time_learning|Test-Time Learning]], [[themes/tool_use_and_agent_protocols|Tool Use & Agent Protocols]]

## Overview

AWM addresses a fundamental inefficiency in agentic systems: agents repeatedly rediscover the same strategies for recurring task types because they carry no persistent procedural knowledge between episodes. The solution is to induce *workflows* — structured memory items each containing a goal description and an ordered sequence of steps, where every step records the environment state, agent reasoning, and the action taken. These workflows are retrieved at test time to guide behavior on new tasks sharing the same procedural structure.

AWM can operate in two modes. In its offline setting, workflows are induced from annotated training trajectories. More significantly, its online mode requires no annotated examples at all: it iteratively induces workflows from self-generated experience using only test queries, running in a fully supervision-free loop. This makes AWM applicable in settings where labeled data is unavailable — a practically important property for real-world deployment.

## Performance and Empirical Grounding

AWM's results on standard web navigation benchmarks established it as a strong baseline for procedural memory approaches. On WebArena, it achieves a 35.5% total success rate, surpassing the BrowserGym baseline by 12.0 absolute points (a 51.1% relative increase). On Mind2Web, it improves relative success rate by 24.6%. Beyond raw success rate, AWM is notably more efficient: it uses approximately 2.0 fewer steps per example compared to BrowserGym (5.9 vs. 7.9 steps), suggesting that retrieving reusable workflows shortcuts the exploratory behavior that inflates step counts in baseline agents.

Generalization under distribution shift is where AWM's design shows its clearest advantage. In cross-task, cross-website, and cross-domain evaluations — where training and test task distributions diverge — online AWM surpasses baselines by 8.9 to 14.0 absolute points. This robustness is not incidental: abstracting procedures away from specific instance details is precisely what enables transfer when surface conditions change.

On workflow induction method, LM-based and rule-based approaches perform nearly identically in success rate (35.5% vs. 35.6% on WebArena), but LM-based induction is more efficient (5.9 vs. 6.3 steps), suggesting the two are interchangeable for accuracy while LM-based edges ahead in operational cost.

## Relationship to Successor Work

AWM's position in the literature is partly defined by where it sits in a progression toward richer memory architectures. ReasoningBank extends the AWM framework by structuring memory items along three components — a title (concise identifier), a description (one-sentence summary), and content (distilled reasoning steps and insights) — and by incorporating both successful and failed experiences into memory construction without requiring ground-truth labels. ReasoningBank's closed-loop process (retrieval → construction → consolidation) represents a more principled form of the self-improvement loop AWM pioneered.

The performance gap is instructive: ReasoningBank improves overall WebArena success rate by +8.3, +7.2, and +4.6 points over memory-free agents across three backbone LLMs, and critically, it also amplifies the returns from test-time compute scaling. Without memory, Best-of-N scaling improves success rate only modestly (39.0 to 40.6 at k=3); with ReasoningBank, the same scaling budget yields 49.7 to 52.4. AWM provides moderate amplification in this regime, positioning it between weaker baselines (Synapse) and the more capable ReasoningBank. This gradient reveals an important structural insight: the quality of procedural memory determines how much test-time compute can be usefully spent.

ReasoningBank also extends to coding agents, improving SWE-Bench-Verified resolve rates from 34.2% to 38.8% (Gemini-2.5-flash) and 54.0% to 57.4% (Gemini-2.5-pro) over no-memory baselines while reducing interaction steps — a domain where AWM was not evaluated, leaving open questions about its generalizability beyond web navigation.

## Limitations and Open Questions

AWM's empirical evaluations are concentrated in web navigation (Mind2Web, WebArena), and its extension to other agentic domains — software engineering, tool-use pipelines, multi-modal environments — remains underexplored relative to newer approaches. The supervision-free online mode is compelling in principle, but the quality of self-generated trajectories bounds the quality of induced workflows; when the base agent fails frequently, the bootstrapping loop may reinforce poor strategies.

The near-equivalence of LM-based and rule-based induction also raises a question: if structured rule extraction matches learned induction in accuracy, what is the marginal value of the language model's generalization capacity in the induction step specifically? This suggests that the bottleneck may lie in *retrieval* — knowing which workflow to apply — rather than induction quality.

Finally, AWM's position relative to the [[themes/test_time_compute_scaling|test-time compute scaling]] frontier is now somewhat circumscribed: as ReasoningBank demonstrates, higher-quality memory is not just additive but multiplicative with compute scaling. AWM's moderate amplification effect suggests its memory representation, while effective, may not capture the reasoning-level abstractions that most benefit from being re-used across diverse tasks.

## Source Connections

- Agent Workflow Memory — primary source for AWM architecture, benchmarks, and workflow induction comparisons
- ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory — extends and benchmarks against AWM; provides the compute-scaling amplification analysis
- Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory — situates AWM within a broader evaluation framework for test-time learning agents
- SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills — parallel line of work on skill-based self-improvement in web agents
- Best of 2024 in Agents — contextualizes AWM within the broader landscape of 2024 agent advances

## Key Findings

## Relationships

## Sources
