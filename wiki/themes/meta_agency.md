---
type: theme
title: Agency & Systems
theme_id: meta_agency
level: 0
parent_theme: ''
child_themes:
- agent_systems
- knowledge_and_memory
created: '2026-04-08'
updated: '2026-04-08'
source_count: 0
sources_since_update: 0
update_count: 1
velocity: 0.0
staleness: 0.0
status: active
tags: []
---
```markdown
# Agency & Systems

> Agency & Systems encompasses the evolving theory and practice of AI that acts autonomously in the world — planning multi-step tasks, maintaining persistent state, calling tools, coordinating with other agents, and recovering from failures. As of early 2026 this theme sits at the intersection of rapid empirical progress and deep unresolved questions: language models can orchestrate non-trivial workflows in constrained settings, but robust, general-purpose agency remains elusive. The trajectory points toward increasingly capable multi-agent architectures, with memory and context management emerging as the central engineering bottleneck.

**Sub-themes:** [[themes/agent_systems|agent_systems]], [[themes/knowledge_and_memory|knowledge_and_memory]]

## Current State

The discourse around AI agency has shifted from "can LLMs use tools?" — answered affirmatively by 2023 — toward harder questions about reliability, composability, and long-horizon coherence. Early demonstrations (ReAct, Toolformer, early AutoGPT-style loops) established that language models could interleave reasoning and action, but exposed sharp performance cliffs once task horizons exceeded a handful of steps or required error recovery.

By mid-2024 the field had settled on a rough taxonomy: single-agent loops with tool access, hierarchical orchestrator-subagent patterns, and peer multi-agent networks. Each trades off differently on latency, cost, coherence, and fault tolerance. Orchestrator-subagent designs gained practical traction — they map naturally onto software decomposition and allow specialised models per subtask — but introduced new failure modes around inter-agent communication fidelity and error propagation.

Memory architecture became a first-class research concern. The original context-window-as-working-memory assumption broke down at scale: contexts bloat, retrieval degrades, and critical state gets lost to compression. Hybrid approaches — episodic retrieval over vector stores, structured external memory, explicit state machines — are being stitched together pragmatically, but no principled unified solution has emerged.

The 2025–2026 period has seen heavy investment in agent frameworks (LangGraph, CrewAI, AutoGen iterations, Claude's native tool-use) and early enterprise deployments in constrained domains (code generation, data pipelines, customer support workflows). Reliability in production remains the open frontier: systems that work in demos fail in deployment due to distribution shift, unexpected tool states, and cascade failures across agent boundaries.

## Capabilities

- **Tool use and function calling** — mature; major frontier models reliably call structured APIs, parse responses, and continue reasoning. Failure modes are mostly prompt-engineering and schema-mismatch rather than fundamental.
- **Multi-step planning** — capable in bounded domains with clear success criteria and reversible actions; degrades sharply with ambiguity, irreversibility, or horizon >10–15 steps.
- **Orchestrator-subagent coordination** — demonstrated at scale in software engineering tasks (SWE-bench class); coordination overhead and error propagation remain engineering problems.
- **Retrieval-augmented memory** — vector-store retrieval integrated into agent loops is production-grade; the harder problem of *what to store, when, and how to surface it* is still heuristic-driven.
- **Self-correction and reflection** — models can critique their own outputs when prompted; closing the loop reliably (acting on the critique, not hallucinating corrections) is the unsolved part.

## Limitations

- **Long-horizon coherence** — performance degrades non-linearly with task length; compounding errors accumulate across steps without robust checkpointing or rollback.
- **Context window as a bottleneck** — even with large contexts, models lose track of distant state; summarisation introduces lossy compression; no lossless solution exists.
- **Error recovery** — agents frequently fail to detect they are stuck, retry the same failing action, or take irreversible actions without safeguards.
- **Trust and verification** — in multi-agent systems, agents cannot reliably verify the provenance or correctness of messages from peer agents, creating adversarial attack surfaces.
- **Grounding and world-state tracking** — agents operating in dynamic environments (file systems, APIs, databases) lose synchrony with actual world state; stale assumptions propagate downstream.
- **Cost and latency** — multi-agent chains multiply inference costs; real-time applications are bottlenecked by sequential reasoning steps.

## Bottlenecks

- **Memory architecture** — no principled solution for persistent, efficiently-retrievable agent memory that scales across sessions and tasks without manual engineering.
- **Reliable tool error handling** — agents lack robust mechanisms for detecting, classifying, and recovering from tool failures at runtime without human intervention.
- **Agent evaluation** — absence of agreed benchmarks for real-world, long-horizon agency makes it hard to measure progress or compare architectures objectively.
- **Formal agent specification** — there is no standard way to specify agent capabilities, expected behaviours, or failure modes, making composition and debugging ad hoc.
- **Human-in-the-loop integration** — knowing *when* to pause and ask a human (vs. proceeding autonomously) is unsolved; current systems either over-interrupt or under-interrupt.

## Breakthroughs

- **ReAct and chain-of-thought tool use** — demonstrating that interleaved reasoning and action in a single pass is possible and effective, unlocking the modern agent loop paradigm.
- **Code interpreter and sandboxed execution** — giving language models access to a Python runtime transformed them from text generators into genuine computational agents.
- **Function calling standardisation** — structured tool-call APIs (OpenAI, Anthropic, Gemini) gave the ecosystem a common interface, enabling a generation of framework tooling.
- **SWE-bench class results** — agent systems solving non-trivial software engineering tasks end-to-end marked a qualitative shift in what autonomous systems can accomplish in knowledge work.

## Anticipations

- Multi-agent systems with persistent, shared memory stores will become the default architecture for complex knowledge work automation.
- Agent evaluation benchmarks will converge around real-world task completion metrics rather than proxy academic benchmarks within the next 12–18 months.
- Formal verification methods will be adapted from software engineering to specify and test agent behaviour contracts.
- The "human-in-the-loop calibration" problem will be partially addressed by learned interruption policies trained on failure logs.

## Cross-Theme Implications

- **→ [[themes/knowledge_and_memory|Knowledge & Memory]]**: The memory bottleneck in agency is the same problem as long-term knowledge retention in language models; solutions in one domain transfer directly.
- **→ Reasoning & Planning**: Long-horizon agency requires planning capabilities that exceed what current autoregressive generation reliably provides; progress in reasoning directly unlocks more capable agents.
- **→ Safety & Alignment**: Autonomous agents amplify alignment concerns — a misspecified objective pursued over many steps causes more damage than a single bad output; agency and safety research are tightly coupled.
- **→ Infrastructure & Compute**: Multi-agent systems multiply inference costs; the economics of agency are bottlenecked by compute efficiency improvements.

## Contradictions

- Agents are simultaneously praised for reducing human toil and criticised for generating unpredictable failure modes that require *more* human oversight to manage safely — the automation paradox.
- The field asserts that larger context windows reduce the need for external memory, while empirical evidence shows retrieval-augmented systems outperform long-context models on tasks requiring precise recall across long documents.
- Framework proliferation (LangChain, LangGraph, CrewAI, AutoGen, Semantic Kernel, etc.) is driven by the claim that no framework adequately solves the problem — yet each new framework introduces its own abstractions that become the next layer to abstract over.

## Research Opportunities

- **Principled memory architectures** — a theoretical framework for what information agents should retain, at what granularity, and with what decay functions.
- **Agent failure taxonomies** — systematic classification of failure modes in deployed agent systems, enabling targeted mitigations rather than ad hoc patches.
- **Lightweight formal specification** — low-overhead ways to specify agent behaviour contracts that practitioners will actually use.
- **Adaptive interruption policies** — learned models for when agents should defer to humans, trained on rollout outcomes rather than hand-coded thresholds.
- **Multi-agent trust protocols** — cryptographic or structural mechanisms for agents to verify message provenance in multi-agent networks.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — Wiki page created. Theme has 0 sources.
```
