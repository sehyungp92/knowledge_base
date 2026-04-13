---
type: source
title: Agent Workflow Memory
source_id: 01KJV8HGEPZYBJ5JXYBKCNJR3W
source_type: paper
authors:
- Zora Zhiruo Wang
- Jiayuan Mao
- Daniel Fried
- Graham Neubig
published_at: '2024-09-11 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- knowledge_and_memory
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agent Workflow Memory

This paper introduces AWM, a system that induces reusable sub-routine workflows from agent trajectories and injects them into agent memory to guide future web navigation — operating in both offline (from annotated examples) and supervision-free online modes. By abstracting example-specific values out of successful trajectories, AWM enables cross-task procedural transfer that outperforms both retrieval-based baselines and human-expert-written workflow libraries, achieving 35.5% task success on WebArena and demonstrating that capable agents can bootstrap their own curriculum from test-time experience alone.

**Authors:** Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, Graham Neubig
**Published:** 2024-09-11
**Type:** paper
**Source:** https://arxiv.org/pdf/2409.07429

---

## Expert Analysis

### Motivation & Prior Limitations

LM-based web agents treat each task in isolation. They integrate a fixed set of examples via training or in-context learning, which biases them toward action sequences similar to those examples and degrades when contexts shift. Crucially, **agents accumulate no learning across the task stream** — as test examples mount, baseline performance stays flat.

Prior attempts at structured memory have significant drawbacks:
- **Synapse** retrieves full concrete trajectories, but these entangle example-specific contexts and generalize poorly
- **SteP** achieves strong results (33.0% SR on WebArena) but requires 14 manually-written, domain-specific workflows with heavy human supervision — an approach that doesn't scale

The central gap: no mechanism existed for continual, supervision-free adaptation from accumulated experience.

### Proposed Approach

AWM introduces an **induction module** `I` that prompts an LM to extract common sub-routines from past experiences at sub-task granularity. Rather than storing "buy dry cat food on Amazon," it stores "search for a product on Amazon" — abstracting away example-specific values to produce portable workflows.

Each workflow comprises:
1. A textual description of the goal
2. A sequence of steps, each containing: environment state description, agent reasoning, and an executable program action

**Offline mode** inducting from annotated examples; **online mode** processing test queries as a stream — after each attempt, a neural evaluator judges success, and successful trajectories are immediately inducted into memory for subsequent queries.

AWM also explores expanding the agent's action space with induced workflows as callable high-level functions (**AWMAS**), though adoption is low in practice.

### Results

| Setting | Benchmark | AWM SR | Baseline SR | Relative Gain |
|---|---|---|---|---|
| Online (GPT-4) | WebArena | 35.5% | 23.5% (BrowserGym) | +51.1% |
| Offline (GPT-4) | Mind2Web cross-task (step) | 45.1% | 36.2% (MindAct) | +24.6% |
| Online | Mind2Web cross-domain (step) | 35.5% | 18.6% (MindAct) | +91.0% |

Additional efficiency gains: AWM reduces mean steps per task from 7.9 (BrowserGym) to 5.9, and from 46.7 (AutoEval) to 5.9.

AWM also **outperforms SteP** — 14 hand-crafted, expert-written WebArena workflows — by 7.6% relative increase in overall success rate, without any human-written procedures.

**Generalization strengthens as distribution gaps widen.** On Mind2Web cross-domain splits, AWMonline leads MindAct by 16.9 absolute points vs. 7.4 points on cross-task and 3.8 on cross-website — because the online mode avoids train-test domain mismatch entirely.

**Rapid learning curve.** Most essential workflows are acquired within the first ~40 examples. After that, the agent enters a stable inference phase.

**Compositional hierarchy.** A "Find a place by its name" workflow induced early becomes a reusable prefix for "Get the zip code of a place" — accumulating complexity hierarchically without re-induction from scratch.

---

## Capabilities

| Capability | Maturity | Evidence |
|---|---|---|
| Workflow induction from trajectories for 51.1% relative WebArena improvement | demo | WebArena: 35.5% vs. 23.5% baseline |
| Supervision-free online workflow induction from self-generated trajectories | demo | Online AWM outperforms human-written SteP workflows |
| Outperforming human-expert-written workflow libraries automatically | demo | +7.6% relative over SteP (14 expert workflows) |
| Cross-distribution generalization with widening margins | demo | 16.9pt lead on cross-domain splits |
| Near-plateau learning from ~40 example interactions | demo | Fast early-learning curve on WebArena |
| Hierarchical workflow composition | demo | "get zip code" built atop "find place by name" |

---

## Limitations & Open Questions

These limitations are treated as the most informative signal in this work:

**Blocking — production deployment:**
- **Task-level success remains critically low.** Even with AWM+GPT-4, agents fail to complete over 95% of multi-step Mind2Web tasks (4.8% task SR). WebArena SOTA of 35.5% means ~64.5% failure rate — far below production reliability thresholds.
- **Stateless isolation is the default.** Without explicit memory mechanisms, LM agents accumulate nothing across the task stream. AWM addresses this, but only within the evaluated setup.

**Significant — architectural fragility:**
- **Workflow rigidity.** Pre-determined action sequences cannot adapt to dynamic intermediate environment states. If an airport pop-up appears mid-workflow that wasn't in the induction trajectory, the agent executes the workflow step regardless — breaking execution silently.
- **Action deviation failures.** Agents struggle to identify when to *deviate* from workflow guidelines, sometimes executing prescribed actions even when the current state makes them inappropriate. This slightly reduces action F1 scores versus MindAct on some splits.
- **Error propagation in online mode.** False-positive trajectory evaluations by the LM evaluator cause incorrect workflows to be stored and reused — actively degrading downstream performance. The evaluator's reliability is a single point of failure.
- **Resistance to new action types.** Despite AWMAS making induced workflows callable actions, agents invoke them in only 18.5% of tasks — suggesting current LMs have strong priors against using recently-added action types, independent of their utility.
- **HTML grounding degrades performance.** Adding HTML observations to workflow steps substantially increases context length and degrades agent performance, despite HTML containing potentially useful UI grounding. Relevance-filtered HTML misses all correct elements 47% of the time.
- **Offline induction fails on distribution shift.** When training and test examples on the same website cover different intents (e.g., "buy items" vs. "find careers" on Amazon), offline workflows fail to transfer.
- **Flat, unstructured workflow context.** All induced workflows are incorporated into the context window at inference time. As workflow libraries grow, relevance-based selection will degrade — no indexing or hierarchical retrieval is implemented.

**Absent from evaluation:**
- **Security and adversarial robustness** are entirely unaddressed — no evaluation of prompt injection via web content, workflow poisoning, or manipulation of the LM evaluator to corrupt the workflow library.

---

## Landscape Contributions

### Bottlenecks Identified

**Production deployment of web automation agents** — end-to-end task completion rates (35.5% WebArena, ~5% task-level Mind2Web) remain below the threshold for reliable deployment in real-world digital workflows. Horizon: 1–2 years.

**Reliable macro-action execution via workflows** — workflow rigidity blocks scalable action space expansion via learned routines; real-time state access and dynamic execution loops are needed. Horizon: 1–2 years.

**Domain-aligned training data** — annotated examples are unavailable for most web domains, limiting offline induction and forcing reliance on noisier online self-supervision. Horizon: 1–2 years.

### Breakthrough

**Supervision-free workflow induction surpassing human-expert baselines** — AWM online autonomously builds a workflow library from test-time trajectories that outperforms SteP's 14 hand-crafted expert workflows. This demonstrates that domain-expert knowledge is not a prerequisite for high web navigation performance at this scale — a notable shift in assumptions about the role of human curation in agent capability.

---

## Implications

**Procedural abstraction over episodic retrieval.** AWM demonstrates that abstracting reusable sub-routines from trajectories outperforms retrieving full concrete examples. Future agent architectures should prioritize procedural workflow memory over episodic example banks.

**Self-bootstrapping curriculum as a deployment paradigm.** Supervision-free online AWM shows that capable agents can build their own curriculum from test-time experience alone — pointing toward continual self-improvement loops as a viable alternative to curated training pipelines.

**Convergence with hierarchical RL and program synthesis.** The compositional workflow hierarchy — simpler routines as building blocks for complex ones — mirrors core ideas in hierarchical reinforcement learning and program synthesis, suggesting a convergence point for these fields with LM-based agent design.

**Fragility of the evaluator-as-teacher loop.** Error propagation via false-positive evaluation is a fundamental vulnerability in any self-supervised agent improvement loop. The quality of the evaluator sets a ceiling on the quality of the learned curriculum.

---

## Related Themes

- [[themes/agent_memory_systems|Agent Memory Systems]]
- [[themes/agent_self_evolution|Agent Self-Evolution]]
- [[themes/agent_systems|Agent Systems]]
- [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]
- [[themes/knowledge_and_memory|Knowledge & Memory]]

## Key Concepts

- [[entities/agent-workflow-memory|Agent Workflow Memory]]
- [[entities/mind2web|Mind2Web]]
- [[entities/task-success-rate|Task Success Rate]]
- [[entities/webarena|WebArena]]
