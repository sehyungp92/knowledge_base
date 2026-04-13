---
type: source
title: 'ARE: Scaling Up Agent Environments and Evaluations'
source_id: 01KJTH9GV7B64HFXS5ZWTJ5KE7
source_type: paper
authors:
- Romain Froger
- Pierre Andrews
- Matteo Bettini
- Amar Budhiraja
- Ricardo Silveira Cabral
- Virginie Do
- Emilien Garreau
- Jean-Baptiste Gaya
- Hugo Laurençon
- Maxime Lecanu
- Kunal Malkan
- Dheeraj Mekala
- Pierre Ménard
- Gerard Moreno-Torres Bertran
- Ulyana Piterbarg
- Mikhail Plekhanov
- Mathieu Rita
- Andrey Rusakov
- Vladislav Vorotilov
- Mengjue Wang
- Ian Yu
- Amine Benhalloum
- Grégoire Mialon
- Thomas Scialom
published_at: '2025-09-21 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- benchmark_design
- evaluation_and_benchmarks
- multi_agent_coordination
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ARE: Scaling Up Agent Environments and Evaluations

**Authors:** Romain Froger, Pierre Andrews, Matteo Bettini, Amar Budhiraja, Ricardo Silveira Cabral, Virginie Do, Emilien Garreau, Jean-Baptiste Gaya, Hugo Laurençon, Maxime Lecanu, Kunal Malkan, Dheeraj Mekala, Pierre Ménard, Gerard Moreno-Torres Bertran, Ulyana Piterbarg, Mikhail Plekhanov, Mathieu Rita, Andrey Rusakov, Vladislav Vorotilov, Mengjue Wang, Ian Yu, Amine Benhalloum, Grégoire Mialon, Thomas Scialom
**Published:** 2025-09-21 00:00:00
**Type:** paper

## Analysis

# ARE: Scaling Up Agent Environments and Evaluations
2025-09-21 · paper · Romain Froger, Pierre Andrews, Matteo Bettini, Amar Budhiraja, Ricardo Silveira Cabral et al. (24 total)
https://arxiv.org/pdf/2509.17158

---

### Motivation & Prior Limitations
Existing agent benchmarks and environments are tightly coupled to narrow sets of tasks and capabilities, causing them to saturate quickly with model progress and requiring frequent rewriting of boilerplate code when moving to new environments.
- The web is an appealing evaluation substrate for search tasks but its constant evolution makes reproducibility difficult, particularly for write operations and complex multi-turn behaviors.
- Most benchmarks model agent interaction as sequential and paused — frameworks like τ-bench and SWE-bench freeze the environment while the agent works, eliminating valuable real-world capabilities such as asynchronous user communication and adaptation to concurrent events.
- As of late 2025, few open-source, flexible libraries exist for developing and studying practical LLM agents at scale, creating a structural gap between model development and real-world deployment.
- Reinforcement learning from verifiable rewards (RLVR) is emerging as a scalable path toward continuous model improvement, but its effectiveness is bounded by the controllability, diversity, and realism of available training environments.

---

### Proposed Approach
ARE (Meta Agents Research Environments) is a research platform built around five core abstractions — Apps, Environments, Events, Notifications, and Scenarios — that enable scalable creation of diverse, time-driven, asynchronous agent environments without rewriting boilerplate code.
- Unlike prior frameworks, ARE treats time and asynchrony as first-class primitives: the environment runs continuously and independently of the agent, with the world state updating via scheduled and random events (e.g., a friend replying to a sent message) while the agent is deliberating.
- Apps are stateful API interfaces implemented as Python classes whose methods are automatically converted into tool descriptions; tools are classified as `read` or `write` via decorators and scoped by role (agent, user, env), enabling fine-grained verification and RL reward computation.
- Event scheduling uses Directed Acyclic Graphs (DAGs) supporting parallel branches, conditional execution, and validation milestones, allowing complex multi-event dependencies and deterministic replay for reproducible evaluation.
- A configurable Notification System with three verbosity levels (low/medium/high) controls selective agent observability, enabling research into proactivity — agents can either wait for notifications or poll the environment independently.
- ARE supports MCP (Model Context Protocol) integration, allowing real external applications to be connected so that model development, evaluation, and production deployment operate in a consistent interface.
- Built on ARE, Gaia2 is a benchmark of 1,120 verifiable, annotated scenarios in a Mobile environment (email, messaging, calendar, etc.) that targets agent adaptability, ambiguity handling, noise tolerance, temporal reasoning, and multi-agent collaboration — capabilities absent from prior benchmarks.
- Gaia2's verification compares agent write actions against pre-scheduled Oracle actions, evaluating each argument via soft (LLM judge) or hard (exact-match) comparison depending on type, making it directly suitable for RL training.

---

### Results & Capabilities
No frontier model dominates across the full intelligence spectrum on Gaia2: stronger reasoning comes at the cost of efficiency, and at equal cost, some models outperform others, but all budget scaling curves plateau with a simple ReAct-like scaffold.
- Models evaluated include GPT-5 (at minimal/low/high budget tiers), Claude-4 Sonnet, Gemini 2.5-Pro, Grok-4, Kimi-K2, Llama-4 Maverick, and Qwen3 235B; none achieves dominance across the cost-capability tradeoff space.
- The budget scaling curves — plotting P{scenario_result = True ∧ scenario_cost < max_budget} against max budget — all plateau before saturation, indicating that standard scaffolds and current models miss key ingredients for sustained progress on agentic tasks.
- ARE's simulation acceleration (switching from real-time to event-to-event queue processing when `wait` tools are invoked) allows scenarios that would take hours in real time to complete in minutes, making long-horizon evaluation practical.
- ARE's abstraction layer successfully integrates existing benchmarks (e.g., τ-bench) alongside newly created ones, demonstrating extensibility as a platform property rather than a per-benchmark effort.

---

### Implications
The shift from sequential to asynchronous evaluation exposes an entirely new class of failure modes — invisible in static benchmarks — related to temporal adaptation, proactivity, and response to concurrent events, which will need to become core model capabilities for practically useful agents.
- ARE's verifiable-reward structure positions it as a direct RL training substrate, not just an evaluation harness; high-quality SFT trace generation is also supported, making it a dual-use infrastructure for both data generation and evaluation.
- The plateau of budget scaling curves across all tested frontier models suggests that scale alone is insufficient and points toward the need for new agent architectures and adaptive compute strategies rather than simply larger models or more inference budget.
- By removing the need for environment and runtime boilerplate, ARE lowers the barrier for the community to continuously extend Gaia2 to new domains, potentially decoupling benchmark creation velocity from the rate at which existing benchmarks saturate.
- In the authors' framing of AI's "second half," progress increasingly depends on defining meaningful tasks and robust evaluations rather than on raw scaling — ARE and Gaia2 are positioned as infrastru

## Key Claims

1. Reinforcement learning from verifiable rewards (RLVR) has emerged as a more scalable alternative to reliance on reward models in settings like reasoning, coding, and agent tool use.
2. Model improvement through experience and deployment in production are bounded by the controllability, diversity, and realism of available environments.
3. The web is a constantly evolving environment, making reproducibility for evaluation and study of complex behaviors challenging, particularly for write operations.
4. Existing agent environments saturate quickly with model progress, requiring frequent rewriting of boilerplate code to move to new environments and tasks.
5. As of December 2025, there are few open-source and flexible libraries for developing and studying practical LLM agents.
6. Most existing agent environments reflect idealized models of agent interaction that do not map to real-world deployment conditions, such as pausing the environment while the agent is working.
7. Sequential agent environments give away valuable real-world capabilities such as asynchronous communication with users and adaptation to new events.
8. ARE supports a shift from sequential to asynchronous interaction between an agent and its environment, unlocking new tasks and capabilities including handling time.
9. ARE supports connection of real apps through Model Context Protocol (MCP) integration, enabling consistency between model development, evaluation, and production deployment.
10. ARE enables generation of high-quality supervised fine-tuning (SFT) traces in addition to supporting RL.

## Capabilities

- Asynchronous, time-driven agent simulation platform (ARE) enabling environments where time passes independently of agent actions, unlocking evaluation of temporal reasoning, proactivity, and dynamic event adaptation in a controlled reproducible setting
- Accelerated long-horizon simulation via event-queue switching: scenarios spanning hours of simulated real-world time can execute in minutes by switching from real-time to event-to-event loop when the agent issues a wait call
- Composable benchmark creation platform with event DAG scheduling, role-scoped tool taxonomy, and RL-compatible verification logic — enabling rapid community development of new agent benchmarks without boilerplate environment rewriting
- Multi-agent collaborative and temporal scenario evaluation in a dense realistic smartphone-mimicking environment — 1,120 verifiable annotated scenarios spanning email, messaging, calendar apps with built-in asynchronous verification

## Limitations

- Budget scaling curves plateau for all evaluated frontier models on agentic tasks — increasing inference budget beyond a threshold yields no further performance gain with standard ReAct-like scaffolds
- No frontier model dominates across the capability-efficiency spectrum — every evaluated system (GPT-5, Claude-4 Sonnet, Gemini 2.5-Pro, Grok-4, Kimi-K2, Llama-4 Maverick, Qwen3 235B) trades off reasoning quality against efficiency with no Pareto-dominant approach
- Current AI agents cannot handle temporal constraints, asynchronous event streams, or proactive time-sensitive actions — capabilities treated as requirements for real-world deployment but effectively absent from current trained models
- Sequential evaluation paradigms (τ-bench, SWE-bench) systematically mask real-world agent requirements — pausing the environment during agent deliberation eliminates asynchronous communication, dynamic state changes, and time-sensitive adaptation from evaluation signal
- Multi-agent and temporal reasoning scenarios require architectural innovation beyond scaling training — current scaling approaches are insufficient for the coordination and temporal-constraint challenges these tasks demand
- Agent benchmark environments saturate quickly with model progress, requiring constant rewriting of boilerplate code — current evaluation infrastructure cannot scale with frontier capability advances
- Web-based agent evaluation creates fundamental reproducibility problems — the constantly-evolving web makes consistent evaluation and study of complex behaviours (especially write operations) unreliable
- Today's frontier models are far from solving Gaia2 — tasks simple for humans but requiring handling of ambiguity, noise, dynamic environments, inter-agent collaboration, and temporal constraints remain out of reach for current systems
- Implicit: Reasoning-intensive frontier models exhibit a cost-quality cliff in agentic settings — at equal budget, high-reasoning models sometimes underperform more efficient alternatives because their per-step cost leaves fewer steps available
- Implicit: Agent progress in AI's 'second half' is bottlenecked by availability of meaningful tasks and robust evaluations — without improved evaluation infrastructure, capability advances cannot be reliably guided or measured via RLVR

## Bottlenecks

- Budget scaling ceiling on agentic tasks — all frontier models evaluated with standard ReAct-like scaffolds hit performance plateaus regardless of increased inference budget, blocking sustained improvement through test-time compute scaling for agents
- Absence of open-source, flexible evaluation and training infrastructure for asynchronous agent capabilities — no established platform exists for creating environments where time passes during agent deliberation, blocking development and measurement of temporally-aware, proactive agents

## Breakthroughs

- ARE platform introduces asynchronous, event-driven agent evaluation and training: the first open-source framework to fully decouple agent execution from environment time, enabling evaluation of temporal reasoning, proactive behaviour, and dynamic event adaptation at scale

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/appworld|AppWorld]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/reinforcement-learning-from-verifiable-rewards-rlvr|Reinforcement Learning from Verifiable Rewards (RLVR)]]
- [[entities/τ-bench|τ-Bench]]
