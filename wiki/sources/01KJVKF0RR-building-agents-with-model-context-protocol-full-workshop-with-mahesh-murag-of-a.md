---
type: source
title: Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag
  of Anthropic
source_id: 01KJVKF0RR0DNTM8BYJ411JGK1
source_type: video
authors: []
published_at: '2025-03-01 00:00:00'
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Building Agents with Model Context Protocol — Full Workshop with Mahesh Murag of Anthropic

This workshop provides a comprehensive technical and conceptual introduction to the Model Context Protocol (MCP), covering its origins, architecture, core primitives, and emerging patterns for multi-agent systems. Mahesh Murag situates MCP as a standardization layer analogous to LSP for IDEs, explains the three interface types (tools, resources, prompts) and their distinct control models, and demonstrates patterns including sampling, hierarchical tool grouping, and agent composability — while candidly surfacing the protocol's unresolved challenges around tool discovery, authentication, and error handling.

**Authors:** Mahesh Murag (Anthropic)
**Published:** 2025-03-01
**Type:** video

---

## Why MCP Exists

The core premise is deceptively simple: *models are only as good as the context provided to them.* A year before this talk, most AI applications were chatbots where users manually copy-pasted context from external systems. The industry shift toward agents with active hooks into data and tools made the absence of a shared standard acutely felt.

The result was an **N×M fragmentation problem**: every combination of AI client and external tool or data source required a bespoke integration with custom prompt logic, custom tool invocation patterns, and custom access federation. Teams inside the same company would build incompatible versions of the same thing.

MCP is positioned as the resolution — a standardization layer for AI applications analogous to two predecessors:
- **APIs** standardized how web front-ends interact with back-end services
- **Language Server Protocol (LSP)** standardized how IDEs interact with language-specific tooling (build Go LSP once; every LSP-compatible IDE gets Go support for free)
- **MCP** standardizes how AI applications interact with external systems

---

## Architecture and Primitives

MCP defines a client-server architecture with three primary interface types, each with a distinct **control model**:

### Tools — Model-Controlled
Tools are the most developed primitive. The LLM within the client application autonomously decides when to invoke them. This makes tools appropriate for actions the model should be able to trigger on its own judgment — API calls, computations, searches, writes. See [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]].

### Resources — Application-Controlled
Resources are data exposed by the server (images, text files, JSON) that the *client application* decides how and when to surface to the model. This is a meaningful distinction: the application, not the model, controls resource consumption. Resources also support **subscription-based notifications** — clients can subscribe to a resource and receive updates whenever it changes, enabling reactive agent patterns.

### Prompts — User-Controlled
Prompts are predefined templates for common interactions that the *user* (not the model, not the application) chooses to invoke. In IDE contexts these manifest as slash commands (e.g., `/summarize-pr`). The control boundary here is intentional: prompts represent reusable workflows the user has explicitly opted into, not autonomous model decisions.

---

## Value Across the Ecosystem

The standardization argument holds differently for each stakeholder:

- **Application developers**: Once MCP-compatible, connect to any server with zero additional work
- **Tool/API providers**: Build one MCP server; get adoption across all compatible AI clients (Claude Desktop, Cursor, Windsurf, Zed, Goose)
- **End users**: More context-rich, personalized agents that can act in the real world
- **Enterprises**: Clean separation of concerns between teams — one team owns the vector DB MCP server; all other teams consuming it don't need to rebuild the integration. This is analogous to the microservices model applied to AI context infrastructure.

---

## Adoption Snapshot (as of early 2025)

- ~1,100 community-built MCP servers published as open source
- Integration across major IDEs: Cursor, Windsurf, Zed
- LangGraph released MCP adapters the week of this talk, allowing LangGraph agents to connect to MCP servers without modifying underlying agent logic
- Cline (30k GitHub stars) ships an MCP auto-generator: LLM-based tooling that creates MCP servers on-the-fly for APIs without pre-built servers

---

## Capabilities

**Multi-agent orchestration via MCP** is in broad production: agents compose access to multiple servers in sequence and parallel for complex multi-step tasks (web search + fetch + synthesis demonstrated live).

**Sampling** — a capability Murag explicitly flags as *the most underutilized MCP feature* — allows an MCP server to request completions (LLM inference) from the client, rather than hosting its own model. This enables distributed intelligence: servers can reason and act without independently managing model infrastructure.

**Logical composability** is architecturally notable: the client/server separation is *logical, not physical*. Any application or agent can simultaneously be both a client (calling downstream servers) and a server (exposing capabilities upstream). This enables hierarchical agent architectures where orchestrators delegate to sub-agents, which delegate further. See [[themes/agent_systems|Agent Systems]].

---

## Limitations and Open Questions

This section deserves emphasis — the protocol's maturity gaps are as informative as its capabilities.

### Tool Discovery at Scale (significant, improving)
Models handle approximately 50–100 tools in context reliably; Claude extends this to a couple hundred. Beyond that, naive enumeration overflows context or degrades performance. The emerging but not-yet-standardized approach is **RAG over tools**: fuzzy/keyword search over a tool library to dynamically surface relevant subsets. **Hierarchical tool grouping** (finance-read, finance-write, etc.) offers another handle. Neither is a solved pattern.

> *"beyond that I think the question becomes how do you search through or expose tools in the right way without overwhelming the context"*

### Authentication and Security (significant, trajectory unclear)
Authentication mechanisms for MCP are explicitly deferred. How agents securely access sensitive tools and data sources — credential management, scoping, revocation — remains unspecified. This is a meaningful gap for production enterprise deployments.

### Cross-Cutting Concern Ownership (minor, improving)
No consensus exists on whether retry logic, authentication, logging, and error handling belong on the client or server side. Murag's personal view is that most should live server-side, but this is opinion, not specification. Until this is settled, production-grade deployment patterns remain idiosyncratic.

### Multi-Layer Error Handling (significant, trajectory unclear)
Hierarchical agent composability introduces compounding failure modes. There is no standard pattern for detecting, propagating, or recovering from errors in multi-layer MCP agent chains. The current advice — treat it like complex hierarchical software systems generally — is acknowledged as incomplete.

### Server Versioning (minor, improving)
Best practices for MCP server versioning and backward compatibility are still emerging. Breaking changes in server APIs can silently break agent workflows with no standard mitigation.

### MCP vs. Agent Frameworks (significant, improving)
The boundary between MCP (context/tool integration layer) and agent frameworks (orchestration/loop logic) is still being defined. MCP does not replace frameworks like LangGraph or AutoGen — it complements them. But the exact division of responsibility is being worked out in real time, as evidenced by LangGraph only just shipping MCP adapters.

---

## Connections

- [[themes/context_engineering|Context Engineering]]: MCP is fundamentally a context delivery mechanism — the protocol is the infrastructure for the principle that model quality is bounded by context quality
- [[themes/knowledge_and_memory|Knowledge and Memory]]: Resources with subscription notifications begin to address stateful context and reactive memory patterns for agents
- [[themes/agent_systems|Agent Systems]]: The logical composability of MCP clients/servers is a structural primitive for hierarchical multi-agent architectures
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]: MCP is the standardization attempt for the tool-use layer; the tool discovery bottleneck links directly to broader unsolved problems in dynamic tool selection

## Key Concepts

- [[entities/mcp-server|MCP server]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
