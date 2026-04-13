---
type: source
title: New tools for building agents
source_id: 01KKTEN0B4Q29ZX9RV0BPVG9HT
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- knowledge_and_memory
- multi_agent_coordination
- retrieval_augmented_generation
- software_engineering_agents
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# New tools for building agents

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# New tools for building agents
article
https://openai.com/index/new-tools-for-building-agents/

---

## Briefing

**OpenAI is consolidating its agent development story around a new Responses API and open-source Agents SDK, signaling a platform shift away from the fragmented Chat Completions + Assistants API model toward a unified, tool-integrated primitive. This matters because it lowers the production deployment barrier for agents — the bottleneck has not been model capability but orchestration complexity, observability gaps, and integration overhead.**

### Key Takeaways
1. **Responses API supersedes Assistants API** — OpenAI plans to formally deprecate the Assistants API by mid-2026, with Responses API as the designated successor for all agentic development.
2. **Built-in RAG without configuration** — The file search tool includes query optimization and custom reranking out of the box, allowing production RAG pipelines with minimal setup code.
3. **Computer use is now an API primitive** — CUA (Computer-Using Agent) achieves 38.1% on OSWorld, 58.1% on WebArena, 87% on WebVoyager — capable for web tasks, still unreliable for OS-level automation.
4. **Web search scores 90% on SimpleQA** — The same model powering ChatGPT search is now available in the API, with inline source citations for downstream transparency.
5. **Agents SDK replaces Swarm** — The new open-source SDK formalizes handoffs, guardrails, and tracing as first-class primitives, replacing the experimental Swarm framework.
6. **Multi-provider compatibility** — The Agents SDK works with any Chat Completions-compatible endpoint, not just OpenAI models, making it a genuine orchestration layer rather than a lock-in play.
7. **Observability is built-in, not bolted on** — Tracing and execution visualization are integrated into the SDK, addressing a recurring pain point in production agent deployments.
8. **Vector Store API now has a direct search endpoint** — Developers can query vector stores outside the Responses API context, enabling use in third-party pipelines.
9. **CUA performance gap on OS tasks is explicitly acknowledged** — OpenAI flags 38.1% OSWorld performance as insufficient for reliable OS automation, recommending human oversight — a rare explicit reliability caveat in a product launch.
10. **Safety mitigations are developer-side responsibilities** — Prompt injection guards, confirmation prompts, and environment isolation are provided as tools, not enforced — risk ownership sits with developers.
11. **Enterprise RAG with permission-aware retrieval** — Navan and Box examples show dedicated vector stores per user group enabling role-based, permission-respecting knowledge retrieval at enterprise scale.

---

### The Responses API: A New Unified Primitive for Agentic Development

- The Responses API is positioned as a **superset of Chat Completions** — same performance, same pricing model, but with added support for built-in tools and multi-turn model calls within a single API invocation.
  - Developers using Chat Completions without built-in tools are not required to migrate; the API remains fully supported with new model releases.
  - For new integrations, OpenAI explicitly recommends starting with Responses API over Chat Completions.
- Key usability improvements over prior APIs include a **unified item-based design, simpler polymorphism, intuitive streaming events**, and SDK helpers like `response.output_text` for direct text access.
- The Assistants API is entering a deprecation path — feature parity work is underway (including Thread-like objects and Code Interpreter), after which formal deprecation will be announced with a mid-2026 sunset target.
  - A migration guide preserving all data will be provided when deprecation is formally announced.
  - Until then, new models will continue to be delivered to the Assistants API.
- The API enables **single-call multi-tool, multi-turn orchestration**, reducing the need for custom loop logic that previously required extensive prompt iteration.
- Tokens and tools are billed at standard rates — **no additional API fee** for the Responses API itself.

---

### Web Search Tool: Real-Time Retrieval with Citations

- Web search is available as a native tool in the Responses API for `gpt-4o` and `gpt-4o-mini`, and also exposed directly via `gpt-4o-search-preview` and `gpt-4o-mini-search-preview` in Chat Completions.
- **Benchmark performance:** GPT-4o search preview scores 90% on SimpleQA; GPT-4o mini search preview scores 88% — both represent state-of-the-art factual accuracy for short-answer retrieval tasks.
- The tool can be **paired with other tools or function calls**, enabling compound agents that blend live web data with file search or computer use.
- Responses include **inline citations with links** to source articles, enabling transparency and attribution in downstream user interfaces.
  - Content owners can opt in to appearing in API search results, creating a publisher participation model.
- Pricing: $30/1K queries for GPT-4o search, $25/1K queries for GPT-4o mini search.
- Real-world use cases from early testing: shopping assistants, research agents, travel booking agents — any application requiring timely, non-static information.
- **Hebbia** uses web search to serve asset managers and legal practices, combining real-time search with internal datasets to deliver context-specific market intelligence outperforming existing benchmarks.

---

### File Search Tool: Production RAG Without Extra Tuning

- The improved file search tool supports **multiple file types, query optimization, metadata filtering, and custom reranking** — the full stack of a production RAG pipeline exposed as a single tool call.
  - This directly addresses the configuration overhead that has historically made RAG pipelines expensive to maintain.
- **Navan's deployment** is the clearest example of the tool's production posture: dedicated vector stores per user group enable role-aware, permission-respecti

## Key Claims

1. OpenAI launched a Responses API that combines the simplicity of Chat Completions API with the tool-use capabilities of the Assistants API for building agents
2. The Responses API supports built-in tools including web search, file search, and computer use
3. OpenAI plans to deprecate the Assistants API with a target sunset date in mid-2026 once feature parity with the Responses API is achieved
4. The Responses API is a superset of Chat Completions with the same performance, and OpenAI recommends it for new integrations
5. GPT-4o with web search scores 90% on SimpleQA benchmark for factual question answering
6. GPT-4o mini with web search scores 88% on SimpleQA benchmark for factual question answering
7. The Computer-Using Agent (CUA) model achieves 38.1% success on OSWorld benchmark for full computer use tasks
8. The CUA model achieves 58.1% on WebArena benchmark for web-based agent tasks
9. The CUA model achieves 87% on WebVoyager benchmark for web-based interactions
10. The CUA model is not yet highly reliable for automating tasks on operating systems, with only 38.1% performance on OSWorld, and human oversight is recommended

## Capabilities

- Web search tool in API achieving 90% on SimpleQA (GPT-4o search preview) and 88% (GPT-4o mini search preview), with inline citations and source links, available in Responses API and Chat Completions API
- Computer-Using Agent (CUA) achieving 38.1% on OSWorld, 58.1% on WebArena, and 87% on WebVoyager — available via API for automating browser workflows and OS-level tasks
- Built-in file search tool with query optimization, metadata filtering, and custom reranking enabling zero-config RAG pipelines over large document collections
- Unified Responses API combining Chat Completions simplicity with multi-tool, multi-turn agent capabilities in a single API call
- Open-source Agents SDK for orchestrating multi-agent workflows with handoffs, guardrails, and integrated tracing — production deployable in hours to days
- Integrated agent observability with execution trace visualization for debugging and optimizing multi-step agent workflows

## Limitations

- Computer use on full OS environments is unreliable — 38.1% OSWorld success rate means ~62% task failure; human oversight explicitly required
- Substantial performance cliff between web-based and full OS computer use — 87% WebVoyager vs 38.1% OSWorld reveals models are far more reliable in structured browser environments than general OS contexts
- Computer use tool susceptible to prompt injection attacks even after mitigations — adversarial content in the environment can hijack agent actions
- Production agent deployment requires extensive prompt iteration and custom orchestration logic — existing API primitives were insufficient, confirming a systemic developer experience gap
- Assistants API design was fundamentally inadequate for agent use cases — its planned deprecation reveals a prior API generation that failed developer needs at scale
- Agents SDK limited to Python at launch — no Node.js support, cutting off the large JS/TS developer community from the native SDK
- No disclosure of latency, reliability SLAs, or cost structure for multi-turn agent workflows running many sequential model calls — real-world economics of production agents remain opaque
- No discussion of agent reliability, failure recovery, or graceful degradation in long-horizon tasks — documentation focuses entirely on happy-path workflows
- Computer use tool access gated to usage tiers 3-5 — the most capable agent tool is not broadly accessible, signaling safety and reliability concerns that limit real-world adoption

## Bottlenecks

- Computer use reliability for full OS automation is blocking autonomous enterprise deployment — 38.1% OSWorld success necessitates human oversight, preventing unattended operation
- Absence of unified agent development infrastructure (API + orchestration + observability) was blocking production agent deployment — partially resolved by today's launch but ecosystem still maturing

## Breakthroughs

- Computer-Using Agent (CUA) model achieves new state-of-the-art on OSWorld (38.1%), WebArena (58.1%), and WebVoyager (87%), and is made available to developers via API for the first time
- Unified Responses API introduces a new paradigm for agent development: multi-tool, multi-turn workflows expressed as a single API primitive, replacing the fragmented Chat Completions + Assistants API architecture

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/prompt-injection|Prompt Injection]]
- [[entities/webarena|WebArena]]
