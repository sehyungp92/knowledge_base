---
type: source
title: Context Engineering for Agents - Lance Martin, LangChain
source_id: 01KJVJY5T807HD28DPP1BPKRQY
source_type: video
authors: []
published_at: '2025-09-11 00:00:00'
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- software_engineering_agents
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Context Engineering for Agents — Lance Martin, LangChain

> A comprehensive walkthrough of context engineering as the central craft of agent development, covering token cost management, context offloading and compression, retrieval strategy diversity across code agents, and the tradeoffs of multi-agent architectures. Grounded in Lance Martin's experience building Open Deep Research, with comparisons across Claude Code, Windsurf, Devin, and Manus implementations.

**Authors:** Lance Martin (LangChain)
**Published:** 2025-09-11
**Type:** Video

---

## Core Thesis

[[themes/context_engineering|Context Engineering]] is the craft of feeding an LLM just the right information at the right time. It emerged as a term because it named a common experience practitioners were already struggling with: prompt engineering is merely a subset. When moving from chat models to agents, the primary input shifts from a human message to a continuous stream of tool call outputs accumulating across dozens or hundreds of steps — and naively handling that stream breaks agents in multiple ways.

A typical Manus task runs ~50 tool calls. Anthropic reports that a typical production agent (likely referring to [[entities/claude-code|Claude Code]]) can involve hundreds. A naive deep research loop can hit 500,000 tokens per run — $1–2 per inference — before hitting the context window limit and triggering degraded performance. This is not a theoretical concern; it is the primary engineering challenge of production agent deployment.

---

## The Anatomy of Context Failure

### Context Rot

Performance degrades with context length through several compounding mechanisms:

- **Context window saturation** — naive accumulation of tool feedback in message history exhausts the window
- **Context rot** — a distinct phenomenon where LLM performance degrades with length, independent of cost or caching
- **Increased susceptibility to irrelevant information** — longer context amplifies the influence of off-topic content on outputs
- **Hallucination propagation** — a hallucinated output gets written into message history and poisons all subsequent reasoning; the agent continues building on a false premise it cannot escape

Crucially, automatic context caching solves latency and cost but does not solve context rot. If 100,000 tokens are still in the window, performance loss persists regardless of whether those tokens are cached.

> *"There's all these weird and idiosyncratic failure modes as context gets longer."*

---

## Context Management Techniques

### Offloading

Rather than returning full tool call outputs to the message history, save them to an external file system or agent runtime state object. The agent receives only a compressed summary and fetches the full content on demand. This significantly reduces per-step token cost.

The summarization step is non-trivial. The prompt must target **high recall** — capturing every key bullet point so the agent can determine whether it needs the full content — while compressing aggressively. Generic summarization fails here. [[entities/devin|Devin (Cognition)]] uses a fine-tuned model specifically for the compaction step in coding workflows.

The quality gap is stark: automated compaction performs marginally better than no compression, while curated manual compression achieves approximately 2× better quality. Manual work is expensive and does not scale, making this a live [[themes/context_engineering|bottleneck]] for production agent systems.

### Retrieval

Code agents have converged on radically different retrieval strategies, with no emerging consensus:

| Agent | Approach |
|---|---|
| **Windsurf** | Semantic chunking at code boundaries → vector embedding → similarity search → knowledge graph → re-ranking |
| **Claude Code** | No indexing; purely agentic retrieval using grep and file tools |
| **Cline** | No code indexing; agentic search only |

[[entities/claude-code|Claude Code]]'s approach — using a simple `lm.txt` markdown index with good descriptions plus grep-based file lookup — outperformed Cursor on documentation-based coding benchmarks at time of testing. This challenges the assumption that retrieval sophistication correlates with retrieval quality.

The fragmentation of retrieval approaches represents a [[themes/tool_use_and_agent_protocols|standardization bottleneck]]: incompatible strategies across implementations make it difficult to evaluate what actually works and why.

### Isolation

When sub-agents operate independently on a shared task, they make implicit local decisions that can conflict when outputs are merged. This is the central argument [[entities/cognition|Cognition/Devin]] makes against multi-agent architectures for coding: each sub-agent's choices propagate through its output, and reconciling conflicting code changes at integration time is harder than doing the task in a single agent context.

---

## Multi-Agent Architecture: When It Works and When It Doesn't

The tension between [[entities/cognition|Cognition]]'s "don't do sub-agents" position and [[entities/anthropic|Anthropic]]'s "multi-agents work really well" position resolves around a specific distinction:

**Read-only parallelization works.** When sub-agents only gather context — no writes, no shared state — outputs can be merged safely. [[entities/anthropic|Anthropic]]'s deep research system exemplifies this: parallelized sub-agents collect research, a single final step does all writing. Claude Code now supports sub-agents, reflecting confidence in this model for appropriate task types.

**Write-heavy coordination does not.** If sub-agents each write a component of a shared solution, their implicit decisions must be reconciled — and [[themes/agent_systems|agent-to-agent communication]] is still early. The integration problem compounds with task complexity. Coding tasks are the hard case; deep research tasks are the easy case.

> *"Use multi-agent in cases where there's very clear and easy parallelization of tasks... with deep research, it's really only reading."*

---

## Memory and Automatic Retrieval

[[themes/knowledge_and_memory|Automatic memory]] systems introduce their own failure modes. When a system decides autonomously when to write and retrieve memories — as ChatGPT does in production — it can inject unintended context into unrelated outputs (e.g., location data appearing in generated images). The decision of when to write memories is non-trivial and poorly solved.

Ambient agents with human-in-the-loop correction represent a more controlled alternative: user edits to tool calls or explicit feedback get incorporated into agent memory and standing instructions, enabling continuous learning without autonomous memory writes that might misfire.

---

## Open Questions

- **When does retrieval sophistication help?** Claude Code's simple agentic retrieval outperforms Windsurf's complex semantic pipeline in at least one benchmark. The conditions under which each approach wins are not well understood.
- **How much history should coding agents preserve?** Full history improves precision but increases cost. The precision-recall tradeoff for context compaction in long coding sessions has no established best practice.
- **Can multi-agent coordination for stateful tasks be solved?** The conflict resolution problem for sub-agents writing shared state remains open. Claude Code's sub-agent support suggests Anthropic believes it can be managed, but the engineering details are not public.
- **What is the right unit of compression?** Summarization preserves semantics but loses structure. Structured extraction preserves key facts but loses narrative. Neither approach dominates across task types.

---

## Landscape Contributions

### Capabilities

- **Context offloading** enables cost-effective long-horizon agents by externalizing tool outputs and fetching on demand — directly addressing the $1–2/run cost problem of naive loops ([[themes/context_engineering|context_engineering]])
- **Agentic retrieval without indexing** (Claude Code's grep-based approach) achieves production-grade code understanding without the engineering overhead of vector stores ([[themes/software_engineering_agents|software_engineering_agents]])
- **Parallelized read-only sub-agents** with centralized write effectively scale context collection for deep research tasks ([[themes/agent_systems|agent_systems]])
- **MCP servers with embedded prompts and resources** allow project-specific tool configuration without polluting the main agent context ([[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]])
- **Human-in-the-loop memory integration** enables ambient agents to improve from user corrections without autonomous write decisions ([[themes/knowledge_and_memory|knowledge_and_memory]])

### Limitations

| Limitation | Severity | Trajectory |
|---|---|---|
| Context rot — performance degrades with length independent of caching | Significant | Stable |
| Hallucination propagation through message history | Significant | Unclear |
| Automated compression quality ≈ no compression; manual is 2× better but expensive | Significant | Stable |
| Multi-agent coordination for stateful write tasks | Significant | Improving |
| No consensus on retrieval strategy for code agents | Significant | Stable |
| Autonomous memory retrieval fails by injecting unintended context | Significant | Stable |
| Naive agentic loops: ~500k tokens, $1–2/run for deep research | Blocking | Improving |

---

## Related

- [[themes/agent_systems|Agent Systems]]
- [[themes/context_engineering|Context Engineering]]
- [[themes/knowledge_and_memory|Knowledge and Memory]]
- [[themes/software_engineering_agents|Software Engineering Agents]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Key Concepts

- [[entities/bitter-lesson|Bitter Lesson]]
- [[entities/context-engineering|Context engineering]]
- [[entities/context-rot|Context rot]]
- [[entities/context-compaction|context compaction]]
- [[entities/llmtxt|llm.txt]]
