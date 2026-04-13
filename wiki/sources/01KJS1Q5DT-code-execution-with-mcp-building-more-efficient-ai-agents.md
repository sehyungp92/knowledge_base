---
type: source
title: 'Code execution with MCP: building more efficient AI agents'
source_id: 01KJS1Q5DTBCF1SJ89YTNVEBQH
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Code execution with MCP: building more efficient AI agents

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Code execution with MCP: building more efficient AI agents
article
https://www.anthropic.com/engineering/code-execution-with-mcp

---

## Briefing

**As MCP adoption scales to thousands of tools per agent, the dominant cost is not inference on user requests but token overhead from tool definitions and intermediate results passing through context — a problem solved by treating MCP servers as code APIs rather than direct tool calls, achieving up to 98.7% token reduction. This reframes agent architecture: instead of context-window management being an LLM problem, it becomes a software engineering problem with known solutions (filesystems, filtering, code execution), and agents that write and execute code become fundamentally more capable than those that merely call tools.**

### Key Takeaways
1. **Tool definition bloat is a scaling crisis** — Agents connected to thousands of MCP servers must process hundreds of thousands of tokens just to read tool descriptions before handling any user request, making the protocol's own success a bottleneck.
2. **Intermediate results double token costs** — Every result returned by an MCP tool call passes through the model context; a 2-hour meeting transcript flowing through twice adds ~50,000 tokens, and large documents can exceed context limits entirely, breaking workflows.
3. **Code execution achieves 98.7% token reduction** — Materializing MCP tools as typed TypeScript files in a directory tree and letting agents write code to call them reduces token usage from 150,000 to ~2,000 tokens in a representative Google Drive → Salesforce task.
4. **Filesystem navigation is an underutilized LLM strength** — Models are proficient at exploring directory trees, making the filesystem an effective lazy-loading registry that requires zero upfront context cost.
5. **Execution environment as a data filter** — Agents can fetch 10,000-row spreadsheets, filter to 5 relevant rows in code, and return only the result to the model — the difference between bloating and preserving context is just a `.filter()` call.
6. **Conditional logic in code eliminates round-trip latency** — Expressing `if/while/try` in executable code rather than chaining model decisions through the agent loop reduces "time to first token" for branching logic.
7. **Intermediate results become private by default** — With code execution, data only enters the model context when explicitly logged or returned; this inverts the default: context exposure becomes opt-in rather than unavoidable.
8. **PII can flow between external systems without ever touching the model** — The MCP client can tokenize sensitive fields before the model sees them and untokenize when passing to downstream tools, enabling deterministic data-flow security rules.
9. **Agents can self-accumulate reusable skills** — Working code saved to a `./skills/` directory with a `SKILL.md` becomes a structured, importable capability; over time agents build their own higher-order toolboxes.
10. **The problems are software engineering problems in disguise** — Context management, tool composition, and state persistence feel novel in agent framing but have decades of solved patterns in software engineering; code execution is the bridge.
11. **Cloudflare independently validated the approach** — Their independently-published "Code Mode" findings corroborate the core insight, suggesting this is a convergent architectural conclusion across teams.
12. **Code execution has real operational costs** — Sandboxing, resource limits, and monitoring for agent-generated code add infrastructure overhead that direct tool calls avoid; the tradeoff must be deliberately weighed.

---

### The MCP Scaling Problem: Two Token Traps

- **Trap 1: Tool definition overload.** Most MCP clients load all tool definitions directly into context at startup using a verbose natural-language format.
  - A single tool definition (e.g., `gdrive.getDocument` with parameters, types, return types) occupies substantial context space.
  - Agents connected to dozens of MCP servers with hundreds of tools each face hundreds of thousands of tokens of overhead before the model reads the first user message.
  - This is a structural problem that worsens linearly as MCP adoption grows and servers proliferate.

- **Trap 2: Intermediate result amplification.** When agents call MCP tools directly, every returned value enters the model context — and often re-enters it.
  - Example: fetch a meeting transcript from Google Drive → transcript enters context; write it to Salesforce → model must reproduce the full transcript again in the tool call arguments.
  - **A 2-hour sales meeting transcript could consume 50,000 additional tokens in a single two-step workflow.**
  - For large documents, this isn't just expensive — it's a hard failure: context limits are exceeded and the workflow breaks.
  - There is also an accuracy dimension: models are more likely to make errors when repeatedly copying large data structures between tool calls.

---

### The Solution Architecture: MCP Servers as Code APIs

- **Core reframe:** instead of exposing MCP servers as tool definitions in context, materialize them as typed code files on a filesystem that the agent explores.
  - Each MCP server becomes a directory; each tool becomes a `.ts` file with typed input/output interfaces wrapping a `callMCPTool()` primitive.
  - The file tree is generated once from connected MCP servers and becomes the stable registry the agent navigates.

- **How agent tool discovery works:**
  - Agent lists `./servers/` to find available servers (e.g., `google-drive`, `salesforce`).
  - Agent reads only the specific tool files it needs (e.g., `getDocument.ts`) to understand the interface.
  - No other tool definitions enter context — the rest of the thousands of tools remain as unread files.

- **Concrete token impact on the Google Drive → Salesforce example:**
  - Direct MCP tool call approach: ~150,000 tokens (all definitions upfront + intermediate res

## Key Claims

1. MCP is an open standard for connecting AI agents to external systems, launched in November 2024.
2. Most MCP clients load all tool definitions upfront directly into context, which causes agents connected to thousands of tools to process hundreds of thousands of tokens before reading a single user re
3. When agents directly call MCP tools, intermediate results must pass through the model context, causing large data (e.g., a full meeting transcript) to be loaded into context multiple times.
4. Large intermediate results passed through the model context can exceed context window limits entirely, breaking the workflow.
5. Models are more likely to make mistakes when copying large data structures between tool calls through the context window.
6. Presenting MCP servers as code APIs on a filesystem rather than as direct tool calls reduces token usage from 150,000 tokens to 2,000 tokens — a 98.7% reduction.
7. Cloudflare published similar findings about code execution with MCP, referring to the approach as 'Code Mode.'
8. LLMs are adept at navigating filesystems, making it effective to present tool definitions as files that agents discover on demand.
9. A search_tools capability with configurable detail levels (name only, name and description, or full definition with schemas) allows agents to conserve context while finding relevant tools efficiently.
10. With code execution, agents can filter and transform large datasets in the execution environment before returning results to the model, reducing what the model sees from 10,000 rows to just a few rele

## Capabilities

- MCP provides a universal protocol for agent-tool integration: developers implement it once and gain access to an ecosystem of thousands of community-built integrations, with SDKs available for all major programming languages
- Code execution with MCP ('Code Mode') enables agents to treat tool servers as importable code APIs, discovering and loading tool definitions on demand via filesystem navigation rather than loading all upfront, reducing token usage by up to 98.7%
- Agents can filter and transform large datasets (e.g., 10,000-row spreadsheets) within a code execution environment before results enter the model context, enabling arbitrarily large data sources to be processed without context blowup
- Privacy-preserving agent operations via MCP-layer PII tokenization: sensitive data (emails, phone numbers, names) flows between services through deterministic code pipelines without ever entering the model's context
- Agents can build and persist reusable skill libraries from successfully completed tasks, saving working code implementations to a structured skills folder that future executions auto-discover and reuse

## Limitations

- Loading all MCP tool definitions upfront into context requires hundreds of thousands of tokens; agents connected to thousands of tools must process this overhead before reading a single user request
- Intermediate tool results must pass through the model context in standard architectures, causing large documents to be duplicated across multiple tool calls — a 2-hour transcript could add ~50,000 tokens per pass
- Documents large enough to exceed the context window limit cause complete workflow failure rather than graceful degradation — the entire multi-step task breaks
- Model accuracy degrades when copying large data structures between tool calls; larger documents increase transcription error rates in tool arguments
- Code execution with MCP requires a secure sandboxed execution environment with resource limits and monitoring — infrastructure that direct tool-calling avoids entirely, adding significant operational overhead
- Control flow (loops, conditionals, retries) in standard agent-loop architectures requires a full model inference round-trip for each branching decision, incurring time-to-first-token latency for operations a deterministic runtime could execute instantly
- Standard MCP clients have no search or progressive disclosure mechanism — the default behaviour loads all connected tool schemas upfront, a design limitation that worsens linearly as the ecosystem of available MCP servers grows

## Bottlenecks

- Token consumption scales linearly with number of connected MCP tools under standard client architectures, creating a practical ceiling on how many tools an agent can access simultaneously before costs and latency become prohibitive
- Absence of standardised, production-ready secure execution environments for agent-generated code blocks broad adoption of code-execution-based MCP patterns despite their demonstrated token efficiency advantages

## Breakthroughs

- MCP has become the de-facto universal standard for connecting AI agents to external tools and data, replacing fragmented custom per-integration adapters with a single implement-once protocol backed by thousands of community servers
- Code execution with MCP enables agents to treat tool servers as importable code rather than direct tool calls, achieving ~99% token reduction for large tool ecosystems while enabling privacy-preserving data pipelines and richer programmatic control flow

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/mcp-server|MCP server]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
