---
type: entity
title: Multi-Agent Architecture
entity_type: method
theme_ids:
- agent_systems
- ai_market_dynamics
- computer_use_and_gui_agents
- model_commoditization_and_open_source
- multi_agent_coordination
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0005165330445195074
staleness: 0.0
status: active
tags: []
---
# Multi-Agent Architecture

Multi-agent architecture is a system design pattern in which complex tasks are decomposed across multiple specialized agents, each operating with focused context and bounded responsibilities. Analogous to multi-processor computing, the pattern reduces what practitioners call "prompt blast radius" — the cascading failures that occur when a single overloaded agent loses coherence — while improving debuggability and enabling finer control over context window consumption. Its rapid adoption across commercial AI products in 2024–2025 marks one of the clearest structural shifts in how LLM-based systems are actually built.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]]

## Overview

Multi-agent architecture addresses a fundamental constraint of LLM deployment: context windows fill up fast, and a single agent trying to handle planning, knowledge retrieval, and execution simultaneously degrades in coherence before the task is done. The solution is decomposition — separate agents for separate cognitive roles, with strict handoff protocols between them.

The pattern exists on a spectrum. At the simpler end, circa 2024, most agentic products were deterministic workflow graphs with fewer than twelve tools and explicit step-by-step orchestration — essentially scripted pipelines wearing an LLM interface. By 2025, the frontier shifted toward chain-of-thought tool calling, where the model reasons dynamically about which tools to invoke, self-corrects mid-task, and backtracks autonomously when a path fails. Products like OpenAI's Deep Research exemplify this shift: the model retrieves information, reconsiders what it found, and reorients — all without a fixed execution graph.

## Key Findings

### Structural decomposition as context management

The core engineering insight behind multi-agent systems is that context length is a finite, expensive resource, and the best way to manage it is never to mix concerns that don't need to share context. Manus — the Chinese general-purpose agent that attracted significant attention in early 2025 — implements this directly: a **knowledge agent**, a **planner agent**, and an **executor agent** operate in distinct contexts, and users only ever communicate with the executor. The knowledge and planner agents remain invisible to the user interaction surface, not because of UX simplicity, but as a deliberate strategy to prevent user conversation history from polluting the planning and retrieval contexts. This is a concrete answer to what the source identifies as "one of the biggest problems" in LLM-based agents: context window exhaustion.

Session isolation reinforces this — each Manus session runs in a completely isolated sandbox, preventing cross-user context bleed and providing a clean failure boundary. See Before you call Manus AI Agent, a GPT Wrapper!.

### The CodeAct execution layer

Manus's executor agent is built on a modified version of the **CodeAct** framework, in which agent actions are expressed as computer programs rather than natural language instructions or JSON function calls. The motivation is well-grounded: LLMs are strong code generators, and code is a more precise, composable, and verifiable medium for expressing complex multi-step actions than prose. CodeAct also integrates naturally with tool use — Manus has access to 29 tools available to the LLM, including browser emulation via `browser-use`. The combination of programmatic action expression, browser access, and sandboxed execution represents the current practical ceiling for general-purpose agent capability.

### Infrastructure-level validation from OpenAI

OpenAI's release of the **Agents SDK** is a significant signal: it was built because developers were already constructing multi-agent "swarms" in production to solve real business problems, and the SDK was backward-fitted to what the ecosystem had independently converged on. This pattern — community practice preceding official tooling — suggests multi-agent architecture is not a speculative design philosophy but an empirical finding from practitioners hitting the limits of single-agent systems. See Inside OpenAI's New Agent Development Tools.

## Limitations and Open Questions

Despite its practical momentum, multi-agent architecture introduces coordination overhead that single-agent systems avoid. Handoffs between agents create latency, require serialization of intermediate state, and introduce new failure modes: an executor agent that doesn't know what the planner decided, or a planner that can't access what the knowledge agent retrieved, can produce incoherent behavior that's harder to diagnose than a single-agent failure.

The Manus analysis also reveals a persistent tension: the system is architecturally sophisticated (multi-agent, CodeAct, 29 tools, isolated sandboxes) but is ultimately a wrapper on top of Claude. This raises an open question about where durable value accrues in the stack — in model capability, in orchestration architecture, or in the quality of tool integration. As the underlying models improve at long-context reasoning and self-correction, some of the coordination complexity that multi-agent systems exist to manage may collapse back into single, more capable agents. Whether the pattern is a permanent architectural fixture or a workaround for current model limitations is not yet settled.

The 2024→2025 transition from deterministic workflows to autonomous chain-of-thought tool use also introduces reliability regressions: deterministic pipelines are auditable and predictable; autonomous backtracking is not. The field has not converged on evaluation frameworks robust enough to characterize when autonomous agent behavior is safe to deploy without human-in-the-loop oversight.

## Related Entities

- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]] — the tool access layer that multi-agent systems depend on
- [[themes/software_engineering_agents|Software Engineering Agents]] — the domain where multi-agent decomposition is most mature
- [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]] — browser-use and sandbox execution as instantiations of this pattern
- [[themes/model_commoditization_and_open_source|Model Commoditization]] — relevant to whether orchestration layers like multi-agent systems become the primary differentiation as base models commoditize

## Relationships

## Sources
