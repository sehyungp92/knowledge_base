---
type: entity
title: MCP server
entity_type: entity
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 9.174691388043185e-05
staleness: 0.0
status: active
tags: []
---
# MCP Server

> An MCP server is an implementation of the Model Context Protocol — an open standard launched by Anthropic in November 2024 — that exposes tools, data, and capabilities to AI agents. MCP servers have seen rapid adoption as a connective layer between agents and external systems, but how agents interact with them turns out to have dramatic consequences for context efficiency, latency, and security.

**Type:** entity
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/context_engineering|Context Engineering]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

---

## Overview

MCP servers sit at the boundary between AI agents and external systems — databases, APIs, filesystems, execution environments — providing a standardised interface through which agents can discover and invoke capabilities. In practice, an agent may connect to dozens of MCP servers simultaneously, each exposing its own set of tool definitions. The protocol was designed to be open and composable, and its adoption since late 2024 has been broad enough that the design choices made at the client-server boundary now carry significant engineering weight.

---

## The Context Overhead Problem

The dominant pattern for MCP tool discovery is to load all tool definitions upfront into the model's context. This is straightforward to implement but does not scale. An agent connected to many servers may encounter hundreds of thousands of tokens of tool definitions before reading a single character of user input. The cost is not just financial — it compresses the effective working context available for reasoning, retrieval, and intermediate results.

The alternative is lazy, on-demand tool discovery. Presenting MCP servers as code APIs on a filesystem — rather than injecting their full schemas into context — reduces token usage from roughly 150,000 tokens to around 2,000 tokens, a ~98.7% reduction. This approach, independently validated by Cloudflare under the name "Code Mode," exposes the server as an importable interface rather than a pre-loaded catalogue. A complementary mechanism is a `search_tools` capability with configurable detail levels: name only, name with description, or full schema with parameters. This lets agents fetch only what they need for the current task, preserving context budget for more consequential content.

---

## Intermediate Results and State

When agents chain MCP tool calls directly, every intermediate result passes through the model context. A two-hour sales call transcript flowing through context twice is not a degenerate case — it is representative of real workflows involving documents, datasets, and logs. Beyond token cost, sufficiently large intermediates can exceed context window limits entirely and break the workflow.

Code execution with MCP addresses this structurally. When an agent writes code that runs in an execution environment, intermediate results stay there by default; only explicitly logged or returned values re-enter the model's context. For large datasets — say, a 10,000-row spreadsheet — the agent can filter and transform in the execution environment, returning only the rows relevant to the current query. State can be persisted across operations by writing to files in a filesystem-accessible execution environment, enabling resumable workflows without burdening context.

Writing control flow logic (loops, conditionals, error handling) in code rather than via sequential tool calls also reduces "time to first token" latency: the execution environment evaluates the conditional tree rather than the model waiting on each tool response before deciding the next action.

---

## Skill Accumulation

One underexplored implication of code execution with MCP is that agents can accrete capabilities over time. When an agent produces a useful function, saving it alongside a `SKILL.md` descriptor creates a structured, referenceable skill. Future agent invocations can discover and reuse these functions, building a higher-level toolbox from prior work. This is a form of externalised procedural memory — the agent's competence grows with use, without modifying the underlying MCP server or model weights.

---

## Security: PII and Data Flow Control

MCP clients sit in a position to intercept data flowing between external systems and the model. This creates a natural enforcement point for PII tokenization: the client replaces sensitive fields (emails, phone numbers, names) with deterministic tokens before they reach the model, then untokenizes them when passing data to downstream MCP tool calls. The model never sees raw PII, but the workflow proceeds normally. More broadly, this allows deterministic security rules about which data can flow to which systems — a meaningful capability for regulated or sensitive deployments where probabilistic model-level filtering is insufficient.

---

## Open Questions and Limitations

The efficiency gains from code execution with MCP are real, but they shift complexity: agents must now write correct, safe code in an execution environment rather than composing pre-validated tool calls. Error handling, sandboxing, and code generation reliability become load-bearing concerns.

The skill accumulation pattern is promising but immature. There is no established mechanism for skill versioning, conflict resolution, or deprecation — the toolbox can grow stale or contradictory without active curation.

The PII tokenization approach depends on deterministic identification of sensitive fields, which is itself an unsolved problem for unstructured text. It also assumes the MCP client is a trusted intermediary, which may not hold in multi-tenant or adversarial settings.

More fundamentally, as the note from Code execution with MCP: building more efficient AI agents observes, the underlying problems — context management, tool composition, state persistence — are not novel. They are software engineering problems with known solutions, now appearing in a new interface layer. The implication is that MCP server design will converge toward patterns already established in distributed systems and API design, rather than requiring fundamentally new approaches.

---

## Related Entities

- [[themes/context_engineering|Context Engineering]] — tool definition loading is a primary driver of context waste
- [[themes/agent_systems|Agent Systems]] — MCP servers are the primary integration surface for multi-tool agents
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]] — MCP is the protocol substrate
- Code execution with MCP: building more efficient AI agents — primary source for efficiency findings
- What Is MCP, and Why Is Everyone Talking About It? — contextual overview
- Building Agents with Model Context Protocol — workshop covering broader MCP agent patterns

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
