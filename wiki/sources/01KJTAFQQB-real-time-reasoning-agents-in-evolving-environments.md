---
type: source
title: Real-Time Reasoning Agents in Evolving Environments
source_id: 01KJTAFQQB35FY9EWY7BEV6QZ3
source_type: paper
authors:
- Yule Wen
- Yixin Ye
- Yanzhe Zhang
- Diyi Yang
- Hao Zhu
published_at: '2025-11-07 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- chain_of_thought
- evaluation_and_benchmarks
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 16
tags: []
---
# Real-Time Reasoning Agents in Evolving Environments

**Authors:** Yule Wen, Yixin Ye, Yanzhe Zhang, Diyi Yang, Hao Zhu
**Published:** 2025-11-07 00:00:00
**Type:** paper

## Analysis

# Real-Time Reasoning Agents in Evolving Environments
2025-11-07 · paper · Yule Wen, Yixin Ye, Yanzhe Zhang, Diyi Yang, Hao Zhu
https://arxiv.org/pdf/2511.04898

---

### Motivation & Prior Limitations
The dominant assumption in LLM-based agent research — that environments only change in response to agent actions — fails to capture the reality of dynamic worlds that evolve in parallel with agent computation, leaving timely decision-making as an unaddressed open problem.
- Despite substantial work on improving agent planning with LLM reasoning (ReAct, ToT, etc.), none of these approaches accounts for the environment continuing to change while the agent is still thinking, meaning their planning gains are irrelevant when time pressure is real.
  - "Most existing work assume that the environments only change when the agents issue an action, ignoring the dynamic nature of the world, which evolves in parallel to the agent's computation."
- The two natural deployment paradigms each have a fundamental flaw: planning agents cannot easily react to changes in the environment, and reactive agents with bounded computation fail to make strategic decisions — yet no prior work directly confronts this tradeoff under real-time constraints.
- Prior dual-system approaches (Christakopoulou et al. 2024, Liu et al. 2024, Zhang et al. 2025) either run two systems fully independently or require one to complete before the other can access its outputs, failing to exploit intermediate reasoning state.

---

### Proposed Approach
The paper contributes two interlinked artifacts: the **Real-Time Reasoning Gym** benchmark and the **AgileThinker** architecture, together establishing a framework for evaluating and improving agents that must reason under temporal pressure.

**Real-Time Reasoning Gym** formalizes a new decision-making problem where the environment steps forward at a fixed rate regardless of agent reasoning completion; if no action is produced within the time window T_E, a default action is applied — simulating a world that does not wait for the agent.
- Three games operationalize distinct dynamic challenges: Freeway (hazard avoidance with moving cars), Snake (seizing transient opportunities as food appears and disappears), and Overcooked (coordinating with an independently acting partner).
- Each game has a controllable cognitive load factor (minimum steps S in Freeway, obstacle count N in Snake, counter length L in Overcooked) and a controllable time pressure dimension, enabling systematic 2D evaluation.
- The gym is reproducible via simulation to eliminate hardware noise, which is critical for comparing agent reasoning budgets fairly.

**AgileThinker** addresses the speed-accuracy tradeoff by running two LLM threads in parallel: a planning thread performing extended reasoning over a frozen game state snapshot, and a reactive thread that must produce decisions within environmental update time.
- The key architectural novelty is that the reactive thread can reference *partial* reasoning traces from the still-running planning thread, enabling informed fast decisions without waiting for planning to complete — a departure from prior dual-system methods where inter-system access is gated on completion.
- DeepSeek V3 (non-reasoning) and R1 (reasoning, with transparent chain-of-thought required for trace sharing) are used as primary models; budget forcing is evaluated for reactive agents and code-as-a-policy for planning agents.

---

### Results & Capabilities
AgileThinker consistently outperforms single-paradigm agents (reactive-only or planning-only) as both cognitive load and time pressure increase, with scores averaged across all three games showing a clear advantage that grows with task difficulty.
- The advantage holds across both open-source (DeepSeek V3/R1) and proprietary model families, suggesting the architecture generalizes beyond a specific model.
- The performance gains observed in simulation are confirmed to transfer to real-world wall-clock time experiments, validating that the gym's token-budget simulation is a faithful proxy for actual latency constraints.
- State-of-the-art models in isolation (pure reactive or pure planning) struggle with the joint requirement of logical correctness and timeliness, establishing that neither paradigm alone is sufficient.

---

### Implications
This work reframes the evaluation of LLM reasoning capability: benchmark performance on static problems is not predictive of performance in environments that evolve during inference, meaning the field's standard evaluation regime systematically overestimates agent readiness for deployment.
- The gym provides a concrete, reproducible testbed for studying test-time compute allocation under temporal constraints — a dimension entirely absent from existing reasoning benchmarks — which could redirect test-time compute research toward latency-aware scaling.
- The partial-trace-sharing mechanism in AgileThinker suggests a general architectural principle: slow deliberative reasoning need not complete before fast reactive systems can benefit from it, which has implications for any agent architecture combining System 1/System 2 components.
- Requiring transparent reasoning trajectories (a prerequisite for AgileThinker's trace sharing) creates a concrete downstream use case for open reasoning models like DeepSeek R1, linking interpretability to architectural capability rather than treating it as a standalone property.

---

### Remaining Limitations & Next Steps
The paper evaluates only within a single model family (DeepSeek V3/R1) for primary experiments, with proprietary model results deferred to an appendix, limiting direct quantitative comparison across the model landscape.
- Proprietary model results are noted to show "similar performance trends" but are not presented in the main body, making it difficult to assess whether the magnitude of AgileThinker's gains is consistent.
- The three games, while diverse in their dynamic ch

## Key Claims

1. Most existing LLM-based agent work assumes that environments only change when agents issue an action, ignoring the dynamic nature of the world that evolves in parallel to the agent's computation.
2. Real-Time Reasoning Gym is the first environment designed for language agents to reason in dynamic environments.
3. Even state-of-the-art language models struggle with making logical and timely judgments under both reactive and planning paradigms in real-time environments.
4. AgileThinker runs two LLMs in two parallel threads: a planning thread that performs extended reasoning over frozen game states and a reactive thread that outputs timely decisions within environmental 
5. In AgileThinker, the reactive thread can reference partial reasoning traces from the ongoing planning process, enabling informed real-time decisions without waiting for complete analysis.
6. AgileThinker consistently outperforms agents engaging only one reasoning paradigm as task difficulty and time pressure rise.
7. In Real-Time Reasoning Gym, the environment steps forward at a fixed rate even when the agent has not finished thinking, and if no action is produced in time, a default action is applied.
8. Prior dual-system methods either have two systems operating independently or require one system to wait for the other to complete before accessing its outputs, unlike AgileThinker.
9. Planning agents performing extended reasoning cannot easily react to changes in the environment, while reactive agents with bounded computation fail to make strategic decisions.
10. AgileThinker's performance advantage over single-paradigm methods is confirmed to translate to real-world scenarios through wall-clock time experiments.

## Capabilities

- AgileThinker dual-paradigm architecture runs planning and reactive LLM threads in parallel, with the reactive thread accessing partial planning traces mid-computation for informed real-time decisions without waiting for complete analysis
- Real-Time Reasoning Gym provides a reproducible simulation environment where the environment state updates at a fixed rate independent of agent reasoning completion, enabling controlled evaluation of agent performance under orthogonally varied time pressure and cognitive load

## Limitations

- State-of-the-art LLMs fail to make both logical and timely judgments in dynamic real-time environments — neither the reactive nor planning paradigm alone is sufficient
- Planning agents fail to react to rapid environmental changes because extended reasoning computation exceeds the environment update rate, causing the agent to act on stale observations
- Reactive agents with bounded computation budgets fail at strategic long-term decision making, sacrificing reasoning quality for response speed
- Existing AI agent evaluation frameworks assume turn-based environments where the world pauses while the agent reasons — creating a fundamental validity gap between benchmark performance and real-world deployability
- AgileThinker requires models with accessible intermediate reasoning traces — models with opaque chain-of-thought outputs cannot serve as the planning thread since the reactive thread reads partial traces mid-computation
- AgileThinker's dual-thread architecture doubles inference compute by running two simultaneous LLM instances, creating substantial resource overhead for real-time deployment at scale
- Real-time reasoning evaluation is confined to simulated game environments — hardware-level noise (variable inference latency, OS scheduling jitter) is explicitly excluded, limiting external validity
- Prior dual-system agent approaches either operate fully independently (no information sharing) or require one system to wait for the other to finish — neither can share partial intermediate reasoning state across concurrent threads

## Bottlenecks

- LLM agents face a fundamental tension between reasoning depth and response latency in dynamic real-time environments — no single compute budget satisfies both requirements, blocking reliable deployment in any scenario where the world evolves faster than reasoning completes
- The field's reliance on turn-based evaluation environments has created an evaluation-deployment gap — years of agent planning research has been optimized against a fundamentally unrealistic assumption, with no established methodology for measuring real-time agent capability

## Breakthroughs

- AgileThinker demonstrates that running planning and reactive LLM reasoning in asynchronous parallel threads — with the reactive thread reading partial planning traces mid-computation — consistently outperforms both single-paradigm approaches in dynamic real-time environments, and outperforms prior d

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/budget-forcing|Budget Forcing]]
