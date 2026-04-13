---
type: source
title: Context Engineering
source_id: 01KJSRXVCS2SJ4D8V19KSE9DBS
source_type: article
authors: []
published_at: '2025-07-02 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- knowledge_and_memory
- multi_agent_coordination
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Context Engineering

**Authors:** 
**Published:** 2025-07-02 00:00:00
**Type:** article

## Analysis

# Context Engineering
2025-07-02 · article
https://blog.langchain.com/context-engineering-for-agents/

---

## Briefing

**Context engineering — the deliberate management of what enters an LLM's context window at each agent step — is emerging as the primary engineering discipline for production agent systems, not prompt engineering or model selection. As agents run longer and accumulate tool feedback across hundreds of turns, naive context handling causes hallucination propagation, performance degradation, and runaway cost; the four strategies of write, select, compress, and isolate constitute the practitioner's toolkit for managing this.**

### Key Takeaways
1. **Context engineering is #1 for agent builders** — Cognition explicitly identified it as "effectively the #1 job of engineers building AI agents," reflecting how central it has become relative to model selection or architecture.
2. **Long context actively degrades performance** — Longer context causes four failure modes: context poisoning (hallucinations persisting), context distraction (overwhelmed training signal), context confusion (superfluous influence), and context clash (internal contradictions).
3. **Scratchpads extend working memory beyond the window** — Anthropic's multi-agent researcher uses explicit plan-saving to memory before the context hits 200k tokens, because truncation would destroy the agent's working plan.
4. **Memory selection is an unsolved reliability problem** — Simon Willison's example of ChatGPT unexpectedly injecting location into an image request shows that semantic memory retrieval can violate user expectations and create a sense of lost ownership over the context window.
5. **RAG over tool descriptions triples selection accuracy** — When agents have large tool sets with overlapping descriptions, applying RAG to tool selection (not just knowledge) improves accuracy approximately 3-fold per recent papers.
6. **Code agents are the most demanding RAG environment** — Windsurf found that embedding search alone becomes unreliable at codebase scale; production-grade retrieval requires AST-aware chunking, knowledge graph retrieval, grep/file search, and a re-ranking step in combination.
7. **Multi-agent isolation outperforms single-agent on complex tasks** — Anthropic's multi-agent researcher demonstrated that many agents with isolated context windows beat a single long-context agent because each subagent's window is allocated to a narrow, focused sub-task.
8. **Multi-agent multiplies token consumption dramatically** — Anthropic reported up to 15× more tokens for agentic workflows compared to chat, making token management a cost and latency constraint, not just a capability one.
9. **Code agents sandbox context into the environment** — HuggingFace's CodeAgent architecture outputs code rather than JSON tool calls; the code runs in a sandbox and only selected return values re-enter the LLM context, keeping token-heavy objects (images, audio) out of the window.
10. **Compression timing matters as much as compression method** — Claude Code's auto-compact triggers at 95% context usage; Cognition inserts summarization at agent-agent boundaries; targeted post-processing of heavy tool calls is a third insertion point — each serves a different need.
11. **Fine-tuned summarization models are production-grade infrastructure** — Cognition uses a fine-tuned model specifically for trajectory summarization, underscoring that off-the-shelf LLM summarization may not reliably capture critical events and decisions.
12. **Runtime state objects are an underutilized isolation primitive** — Agent state schemas can segregate tool outputs into non-LLM-exposed fields, providing sandboxing-equivalent isolation without a separate execution environment.

---

### The Operating System Analogy for LLM Context

- **Andrej Karpathy's framing positions the LLM as a CPU and the context window as RAM** — context engineering is therefore analogous to what an operating system does to manage what fits in working memory at any moment.
  - This framing is consequential: it implies that context engineering is a systems-level discipline, not a prompting trick, and should be designed into agent architecture from the start.
  - The three types of context being managed are instructions (prompts, few-shot examples, tool descriptions, memories), knowledge (facts, retrieved information), and tool feedback (results from tool calls).
- Context engineering as a discipline emerges precisely because agents, unlike single-turn chat, accumulate context across many steps — creating compounding pressure on a fixed-size window.

---

### Write Strategies: Externalizing Context

- **Scratchpads let agents persist information outside the context window during a task session**, functioning as explicit working memory overflow.
  - Implementation options include: (a) a tool call that writes to a file, or (b) a field in the agent's runtime state object that persists across steps.
  - Anthropic's multi-agent researcher is the canonical example: the LeadResearcher writes its plan to memory at the outset specifically because exceeding 200k tokens causes truncation that would destroy the plan.
  - The key value is that scratchpad content is agent-controlled — the agent decides when to write and what to preserve, rather than relying on the context window's implicit retention.
- **Long-term memory enables cross-session persistence**, going beyond scratchpads (which are session-scoped) to carry agent knowledge across separate interactions.
  - The Reflexion paper introduced self-generated reflection after each agent turn, with those reflections reused in future turns — one of the earliest operationalizations of agent memory.
  - Generative Agents synthesized memories periodically from collections of past feedback, creating a more structured long-term record.
  - **ChatGPT, Cursor, and Windsurf all implemented auto-generated long-term memories** that learn from user-agent interac

## Key Claims

1. Context engineering is the art and science of filling the context window with just the right information at each step of an agent's trajectory.
2. LLMs function analogously to a CPU, with the context window serving as RAM — the model's working memory — with limited capacity.
3. Context engineering applies across instructions (prompts, memories, few-shot examples, tool descriptions), knowledge (facts, memories), and tools (feedback from tool calls).
4. Long-running agentic tasks with accumulating tool call feedback cause agents to utilize a large number of tokens, which can exceed context window size, balloon cost and latency, or degrade agent perfo
5. Longer context can cause performance problems via context poisoning (hallucinations entering context), context distraction (context overwhelming training), context confusion (superfluous context influ
6. Context engineering is considered the #1 job of engineers building AI agents.
7. Anthropic states that agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies.
8. Anthropic's multi-agent researcher saves its plan to an external memory (scratchpad) at the start because context windows exceeding 200,000 tokens are truncated.
9. Scratchpads can be implemented either as tool calls that write to a file, or as fields in a runtime state object that persists during the session.
10. Reflexion introduced the idea of reflection following each agent turn, with self-generated memories reused across subsequent turns.

## Capabilities

- Production software agents (Claude Code) automatically compress context via recursive/hierarchical summarisation when approaching context window limits (95% threshold), maintaining agent continuity across extended sessions
- RAG applied to tool descriptions improves tool selection accuracy by approximately 3-fold in agents operating over large tool collections
- Multi-agent architectures with isolated per-agent context windows outperform single-agent systems on complex research tasks, with each subagent's context allocated to a narrower subtask in parallel
- Automatic cross-session long-term memory generation and retrieval is in broad production use across major AI products, persisting user-specific facts, instructions, and episodic memories across sessions
- Code agents can isolate token-heavy objects (images, audio, large data) from LLM context by executing tool calls in a sandbox and selectively returning only the required output values

## Limitations

- Long-running agents accumulate tool-call feedback that exceeds context window capacity, causing cost/latency inflation and performance degradation — a fundamental constraint on agentic task length
- Hallucinations that enter the agent context window ('context poisoning') propagate forward and corrupt subsequent agent decisions throughout the rest of a trajectory
- Superfluous or contradictory context degrades model performance even when the context window is not full — irrelevant tokens distract attention and contradictions stall reasoning
- Embedding-based retrieval becomes unreliable as a retrieval heuristic as codebase size grows, requiring hybrid pipelines combining grep, knowledge-graph retrieval, and re-ranking
- Agents provided with too many tools experience confusion from overlapping tool descriptions, degrading task performance
- Long-term memory retrieval is unreliable and can inject unexpected, unintended context — users lose predictability over what appears in their agent context window
- Multi-agent systems consume up to 15× more tokens than single-turn chat, making multi-agent architectures prohibitively expensive for many production use cases despite their performance advantages
- High-fidelity summarisation at agent-to-agent handoff boundaries requires fine-tuned models — general-purpose LLM summarisation misses critical decisions and state transitions needed for agent continuity
- Context engineering for agents requires significant bespoke manual engineering per application — no general-purpose automated solution exists, and it is currently 'the #1 job of engineers building AI agents'
- Agents spanning hundreds of turns accumulate context that requires multi-agent scratchpads and persistent plans to avoid truncation — context window limits constrain how long a plan can stay in working memory

## Bottlenecks

- Lack of automated general-purpose context management blocks reliable deployment of long-running agents — engineers must hand-engineer write/select/compress/isolate strategies per application with no standard tooling
- Embedding-based retrieval degrades for large-scale code corpora, requiring complex hybrid pipelines (semantic search + AST parsing + knowledge graphs + re-ranking) that add latency and engineering burden
- Multi-agent token overhead (up to 15× vs chat) makes multi-agent architectures cost-prohibitive for mainstream and consumer deployment despite their demonstrated performance advantages on complex tasks

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]

## Key Concepts

- [[entities/context-engineering|Context engineering]]
- [[entities/generative-agents|Generative Agents]]
- [[entities/reflexion|Reflexion]]
