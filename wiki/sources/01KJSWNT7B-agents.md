---
type: source
title: Agents
source_id: 01KJSWNT7BDCEJNTQJWZ050N89
source_type: article
authors: []
published_at: '2025-01-07 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- evaluation_and_benchmarks
- reasoning_and_planning
- search_and_tree_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agents

> A comprehensive technical treatment of foundation model agents that establishes a formal definition grounded in classical AI, catalogs the tool inventory design space, and identifies compound error accumulation as the central engineering challenge — while remaining candid that reliable planning remains an open theoretical and empirical problem.

**Authors:** Chip Huyen
**Published:** 2025-01-07
**Type:** article
**Source:** https://huyenchip.com/2025/01/07/agents

---

## Expert Analysis

**Foundation model agents are now practically viable — defined by their environment, tool inventory, and planning capability — but their power comes with compounding failure modes that require systematic evaluation. The shift from static LLMs to agentic systems is not a new paradigm but an extension of long-established patterns (chain-of-thought, self-critique, structured outputs), now made economically meaningful by model capability crossing a threshold. The real bottleneck is reliable planning, not tools.**

The key reframe this source offers is definitional clarity: an agent is *anything that perceives its environment and acts upon it* — the Russell & Norvig (1995) definition applies directly to FM agents. This means [[themes/agent_systems|agent systems]] already surround us. RAG systems are agents. ChatGPT with web search is an agent. The SWE-agent built on GPT-4 that navigates repositories, searches files, and edits lines is an agent. The term is not a marketing upgrade — it carries structural implications for how failure modes propagate.

---

## What an Agent Actually Is

An agent is formally characterized by two things: the **environment** it operates in and the **action set** (tool inventory) available to it. These are mutually constraining — a tool is only meaningful relative to an environment, and an environment only accessible via corresponding tools. The AI model is the *brain* that perceives state, sequences actions, and determines completion; it is not merely a response generator.

This definition has an immediate practical consequence: agents require more powerful models than non-agentic use cases for two structural reasons:

1. **Compound error accumulation** — mistakes multiply across steps
2. **Higher stakes** — write-capable agents act on the world; failures have real consequences

The compound error problem is the central quantitative argument of the source. At 95% per-step accuracy — a high bar — a 10-step task succeeds only ~60% of the time. A 100-step task succeeds only ~0.6% of the time. This is not a soft concern; it is a hard mathematical constraint on what agentic systems can reliably accomplish today. See [[themes/reasoning_and_planning|reasoning and planning]] for the broader context of this bottleneck.

---

## The Tool Inventory

Tools serve three distinct functions:

### Knowledge Augmentation
Prevents model staleness and extends perception beyond training data. Includes text/image retrievers, SQL executors, web browsers, internal search APIs, email readers, and social media APIs. Web browsing is an umbrella term covering browsers, search APIs, news APIs, GitHub APIs — each with different coverage, reliability, and adversarial exposure.

**Critical limitation:** Internet-connected agents are exposed to adversarial manipulation via malicious content on the public web. API selection requires deliberate curation, not permissive access.

### Capability Extension
Addresses inherent model weaknesses directly rather than through training. Calculators, calendars, timezone converters, translators, and code interpreters provide reliable performance on tasks models structurally fail at — arithmetic being the canonical example (a model that cannot divide 199,999 by 292 reliably can be trivially fixed with a calculator).

Code interpreters are the highest-leverage capability extension, enabling agents to act as coding assistants, data analysts, and research assistants that write, execute, and analyze in a single loop. The cost: **automated code execution introduces code injection attack surface** that is not yet adequately secured for broad deployment.

### Write Actions
The qualitative risk escalation. Read-only tools extend perception; write tools — email APIs, banking APIs, database mutations — enable automation of entire workflows but demand human approval gates. The asymmetry matters: a read error produces a wrong answer; a write error acts on the world.

### Tool Inventory Design Tradeoffs

**Granularity tradeoff:** High-level natural-language plans are easier to generate and more robust to API changes but require a translation module. Exact function-name plans are easier to execute but brittle — any API rename requires retraining or re-prompting. A hierarchical approach (high-level plan first, then subtask expansion) can partially circumvent this.

**Size tradeoff:** More tools enable more capabilities, but tool selection reliability degrades as inventory grows. [[themes/tool_use_and_agent_protocols|Tool use]] at scale (Gorilla attempted 1,645 APIs via prompting) hits a hard context ceiling — tool descriptions alone may exhaust available context. Different models also exhibit different tool preferences; GPT-4 selects broader tool sets while ChatGPT favors image captioning — no single model reliably selects optimal tools across domains.

**Finetuning brittleness:** Finetuned agent models become version-locked to specific API signatures. Any tool rename or parameter change requires full retraining — making production deployment of finetuned agents on evolving software environments a significant maintenance bottleneck.

---

## Planning

Planning is the hardest problem in [[themes/agent_systems|agent systems]] and the one with the least resolved theoretical status.

### The Open Question

Yann LeCun flatly argues autoregressive LLMs cannot plan (2023). The counterargument — that backtracking can be simulated through revision, and that LLMs may have internalized sufficient world model structure to predict action outcomes — is plausible but unproven. **The source treats this as genuinely open.** This is the most important epistemic flag in the document.

### What Chain-of-Thought Alone Cannot Do

Chain-of-thought generates action sequences without modeling outcome states. A plan is syntactically valid if it lists plausible actions; it is semantically valid only if each action's post-state enables the next action. CoT does not verify this. The result is plans that look coherent but are logically broken — a limitation documented in [[themes/reasoning_and_planning|reasoning and planning]] research.

### Planning Failure Taxonomy

The source provides a specific, measurable failure taxonomy — rare in the field:

| Failure Mode | Description |
|---|---|
| Invalid tool | Agent generates a non-existent tool name |
| Valid tool, wrong parameter count | Hallucinated arity |
| Valid tool, wrong parameter values | Correct tool, bad arguments |
| Goal failure | Plan does not achieve the stated objective |
| Constraint violation | Plan ignores budget, time, or scope constraints |
| False completion | Agent is convinced it succeeded when it has not |

False completion is particularly insidious — it is a reflection failure mode where the model's self-assessment is wrong. Constraint violations are systematic: agents plan for the goal while ignoring or misapplying stated constraints. Time as a constraint is the most overlooked dimension in current [[themes/evaluation_and_benchmarks|agent evaluation]].

### Decoupling Plan Generation from Execution

A structural mitigation: generate and validate a plan before executing it. This prevents "fruitless execution" where an agent burns time and API credits on a fundamentally broken plan. Generating multiple plans in parallel and selecting the best trades cost for speed — a latency optimization available when plans are cheap relative to execution.

---

## Reflection and Multi-Step Reasoning

[[themes/search_and_tree_reasoning|Reasoning patterns]] like ReAct and Reflexion — interleaving thought, action, and observation — substantially improve agent performance over pure chain-of-thought. ReAct-style loops have become the dominant production pattern for agent execution.

**The cost is real.** Reflection substantially increases token consumption and perceived latency. Each thought/observation cycle adds tokens that scale with step count. Both ReAct and Reflexion require many in-context examples to establish the structured format, consuming input budget that could otherwise hold task-relevant information. This is a direct, unavoidable performance/cost tradeoff at current context sizes.

---

## Multi-Agent Systems

The source makes a structural argument: most agentic workflows are inherently multi-agent. The moment you separate plan generation, plan validation, intent classification, and execution into components — which you should, for reliability — you have a multi-agent system. "An agent" and "a multi-agent system" are nearly synonymous in practice for non-trivial tasks.

Agents can also build new tools from existing ones. Voyager's skill manager accumulates coding skills as reusable functions; Chameleon's tool-transition analysis reveals which tools are productive sequences. This property — agents expanding their own capability inventory — has long-term implications for autonomous capability growth that the source flags but does not resolve.

---

## Capabilities Summary

| Capability | Maturity |
|---|---|
| Tool-augmented agents outperforming base models (Chameleon: +11.37% ScienceQA, +17% TabMWP) | narrow_production |
| Function calling / tool use across major model providers | broad_production |
| ReAct-style reasoning-action interleaving as production pattern | broad_production |
| Multi-agent decomposition of planning and execution | broad_production |
| Hierarchical planning (high-level → subtask expansion) | narrow_production |
| Parallel plan generation with evaluator selection | narrow_production |
| Dynamic tool/skill acquisition and reuse (Voyager) | research_only |
| Tool selection from very large catalogues (1,600+ APIs via prompting) | research_only |

---

## Limitations and Open Questions

### Blocking
- **Compound error at scale** — mathematical ceiling on reliable multi-step task completion at current per-step accuracy levels
- **Code injection** — automated code execution lacks adequate security for broad deployment
- **No evaluation methodology** — no established benchmark suite for systematically measuring planning failures, tool use errors, and goal achievement

### Significant
- **LLM planning capability is theoretically unresolved** — LeCun's objection is not answered, only countered
- **Function call hallucination** — invalid tool names, wrong parameter counts, incorrect parameter values are frequent
- **Parameter value guessing** — agents must infer values from incomplete context; ambiguous queries (time range, quantity) are routinely wrong
- **Tool selection degrades with inventory size** — no known solution beyond retrieval-based tool selection
- **False task completion** — agents incorrectly believe they have succeeded
- **Constraint violation** — budget, time, scope constraints are systematically ignored in plans
- **Context ceiling on tool descriptions** — large inventories may overflow available context
- **API version lock for finetuned models** — every tool update forces retraining
- **Economic cost-effectiveness** — high API credit consumption without demonstrated autonomous ROI in 2025
- **Web adversarial exposure** — internet-connected agents vulnerable to manipulation via malicious content
- **Pre-paradigmatic field** — no established theoretical frameworks for agent definition, development, or evaluation

### Acknowledged Gap
The source explicitly defers **memory** — how agents manage information exceeding context limits — to a future post, positioning it as the key missing component for long-horizon agents. This is the most important acknowledged gap.

---

## Bottlenecks

**Agent evaluation methodology** *(blocking, horizon: months)* — No systematic framework exists for measuring planning failures, tool use errors, and goal achievement across diverse task types. Without this, improvement is anecdotal. See [[themes/evaluation_and_benchmarks|evaluation and benchmarks]].

**LLM world model for outcome prediction** *(blocking, horizon: 1-2 years)* — LLM planners generate action sequences without simulating post-action states. Reliable multi-step planning in open-ended environments requires knowing not just available actions but the state each action produces.

**Finetuned agent API version lock** *(blocking, horizon: months)* — Every tool API update forces full retraining of finetuned agents. This makes production deployment in evolving software environments operationally impractical at current tooling.

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/agent_evaluation|Agent Evaluation]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/search_and_tree_reasoning|Search and Tree Reasoning]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Key Concepts

- [[entities/ai-agent|AI Agent]]
- [[entities/hierarchical-planning|Hierarchical Planning]]
- [[entities/multi-agent-system|Multi-Agent System]]
- [[entities/scienceqa|ScienceQA]]
