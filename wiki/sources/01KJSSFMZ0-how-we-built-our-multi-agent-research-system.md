---
type: source
title: How we built our multi-agent research system
source_id: 01KJSSFMZ0912J92PBT3Y9R709
source_type: article
authors: []
published_at: None
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_systems
- evaluation_and_benchmarks
- knowledge_and_memory
- multi_agent_coordination
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How we built our multi-agent research system

Anthropic's engineering account of building and deploying a production multi-agent research system — where Claude Opus 4 orchestrates parallel Claude Sonnet 4 subagents — outperforms single-agent Opus 4 by 90.2% on internal evaluations. The piece is unusual in its candor: it quantifies *why* the system works (token volume explains 80% of performance variance), catalogs the failure modes encountered, and describes the engineering decisions made to close the gap between prototype and production.

**Authors:** Anthropic Engineering
**Published:** None
**Type:** article

---

## Expert Analysis

**The central insight is architectural, not algorithmic.** Multi-agent systems outperform single agents primarily because they spend more tokens — distributed across separate context windows — rather than because they reason differently. Token usage alone explains 80% of variance in the [[themes/evaluation_and_benchmarks|BrowseComp evaluation]], with tool call count and model choice as secondary factors. The architecture's primary job is to make it economically and computationally feasible to spend enough tokens on a task.

This reframing has an uncomfortable implication: **performance is fundamentally compute-bound.** Gains are bought, not engineered. The flip side is that model upgrades are unusually high-leverage within this architecture — moving from Claude Sonnet 3.7 to Sonnet 4 yields a larger gain than doubling the token budget on the older model.

---

## Architecture

The system uses an **orchestrator-worker pattern**: a lead agent (Claude Opus 4) analyzes the query, develops a strategy using extended thinking as a planning scratchpad, and spawns parallel subagents (Claude Sonnet 4) to explore different facets simultaneously.

**Subagents as compression engines.** Each subagent operates in its own context window, independently filling it with search results and intermediate reasoning, then compresses its findings before returning them to the lead. This is not merely a parallelism trick — it directly addresses the root constraint that a single context window limits how much information can be simultaneously reasoned over. Separate contexts also prevent one search direction from contaminating another.

**Contrast with static RAG.** Traditional retrieval augmented generation uses static chunk retrieval against an input query. This system uses multi-step adaptive search: each subagent dynamically reformulates queries based on what it finds, allowing investigations to branch in response to evidence rather than following a predetermined path.

**Parallelism at two levels.** The lead agent spawns 3–5 subagents simultaneously rather than sequentially. Within each subagent, 3+ tools are called in parallel. This combination cut research time by up to 90% for complex queries, transforming hours of work into minutes.

---

## Why Research Tasks Fit This Pattern

Research is inherently path-dependent: discoveries during investigation redirect subsequent search directions, requiring dynamic replanning that fixed pipelines cannot accommodate. The process is also **breadth-first** — many independent leads must be pursued simultaneously to avoid sequential bottlenecks.

The board members example is instructive: identifying all board members of all IT S&P 500 companies requires decomposing into hundreds of parallel lookup tasks. A single agent fails through sequential slowness; multi-agent decomposition succeeds through parallel execution.

This also explains why **most coding tasks are a poor fit** for multi-agent systems. Code changes are typically sequential and interdependent — one function must exist before another can call it. The parallelizable surface area is smaller, and real-time coordination between agents (which LLMs currently cannot do well) becomes necessary rather than optional. See [[themes/agent_systems|agent systems]] for the broader landscape.

---

## Capabilities Demonstrated

| Capability | Maturity |
|---|---|
| Orchestrator-worker research with 90.2% improvement over single-agent | `narrow_production` |
| Parallel subagent + parallel tool calling (up to 90% time reduction) | `narrow_production` |
| Dynamic multi-step adaptive search (vs. static RAG) | `narrow_production` |
| Extended thinking as orchestrator planning scratchpad | `narrow_production` |
| LLM-as-judge evaluation scaling to hundreds of free-form outputs | `narrow_production` |
| Long-horizon conversation management with summarization checkpoints | `narrow_production` |
| Self-improving tool description agent (40% task time reduction) | `demo` |
| Subagent filesystem artifact pattern for lightweight coordinator references | `demo` |

The **self-improving tool agent** is particularly notable as a distinct capability class: given a flawed MCP tool, it attempts to use the tool, identifies failure modes, and rewrites the tool description to steer future agents away from the same failures. This is prompt engineering automated and applied reflexively — an agent improving the interface conditions for subsequent agents.

---

## Limitations and Failure Modes

### Structural Limitations

**Token cost is the binding constraint on adoption.** Multi-agent systems consume ~15× more tokens than chat and ~4× more than single-agent interactions. This restricts economic viability to high-value tasks where output quality justifies the cost. Routine or medium-value research tasks remain inaccessible. See [[themes/multi_agent_coordination|multi-agent coordination]] for context.

**Synchronous execution creates a systemic bottleneck.** The lead agent waits for each subagent batch to complete before proceeding. This means the full system stalls on the slowest subagent. The lead cannot steer subagents mid-execution, subagents cannot coordinate with each other, and dynamic task reallocation during execution is impossible.

**Real-time inter-agent coordination is absent.** LLMs are not yet capable of dynamically delegating to, negotiating with, or redirecting other agents during live task execution. This is a hard capability gap, not a prompt engineering problem.

### Behavioral Failure Modes

**Effort miscalibration.** Without explicit effort-scaling rules embedded in prompts, agents spawn 50 subagents for trivial queries and under-resource complex ones. The system cannot intrinsically judge appropriate effort.

**Work duplication without detailed decomposition.** Without specific task descriptions for each subagent, agents duplicate each other's searches. The canonical example: one subagent investigated the 2021 automotive chip crisis while two others duplicated work on 2025 supply chains — effective division of labor requires the orchestrator to spell out independent investigation trajectories in detail.

**Source quality bias.** Early agents systematically preferred SEO-optimized content farms over authoritative sources like academic PDFs and expert blogs. Critically, **no automated evaluation detected this bias** — it was discovered only through manual human testing. This points to a deeper issue: [[themes/agent_evaluation|evaluation]] methods optimized for coverage and recall miss qualitative source selection failures.

**Search query over-specificity.** Agents default to overly long, specific queries that return few results. Broad-first search strategy must be explicitly instructed.

### Engineering Challenges

**Error compounding.** In agentic systems, minor issues cause large behavioral changes — a single step failure can redirect the entire agent trajectory into an entirely different path. This makes the prototype-to-production gap substantially wider than in traditional software engineering.

**Non-determinism makes debugging hard.** Identical prompts produce different execution traces, preventing reliable failure reproduction. Failures that users report cannot be consistently replicated.

**Emergent inter-agent behaviors.** Small changes to the orchestrator prompt unpredictably alter subagent behavior in ways not anticipated during design. Effective prompt engineering must define frameworks for collaboration (division of labor, effort budgets) rather than rigid rules — but predicting downstream behavioral effects of prompt changes remains intractable.

**Stateful agent evaluation.** Standard evaluation methods break for agents that mutate persistent state across multi-turn conversations: each action changes the environment for subsequent steps, making clean test isolation impossible. There is no principled solution to this yet.

---

## Open Problems

The four bottlenecks identified represent the frontier of current [[themes/multi_agent_coordination|multi-agent coordination]] research:

1. **Synchronous coordination** — no mechanism for lead agents to steer in-flight subagents or for subagents to coordinate with each other; architectures remain batched rather than continuous
2. **Token cost scaling** — 15× overhead relative to chat confines multi-agent deployment to high-value tasks; broad deployment requires order-of-magnitude efficiency improvements
3. **Stateful agent evaluation** — no standardized methodology for benchmarking agents that modify persistent state; the evaluation gap limits systematic improvement
4. **Real-time inter-agent delegation** — LLMs lack the coordination primitives for subagents to self-organize, merge findings, or reassign work without full orchestrator mediation

The source is explicit that these are engineering-horizon problems (months to 1–2 years), not research horizon — suggesting the team expects them to yield to standard engineering approaches rather than requiring fundamental capability advances.

---

## Key Claims

1. Multi-agent (Opus 4 lead + Sonnet 4 subagents) outperforms single-agent Opus 4 by **90.2%** on internal research evals.
2. Token usage alone explains **80% of performance variance** in BrowseComp; three factors (tokens, tool calls, model choice) explain **95%**.
3. **Upgrading model > doubling token budget** — Sonnet 3.7 → Sonnet 4 provides larger gain than 2× token budget on Sonnet 3.7.
4. Multi-agent systems consume **~15× more tokens** than chat interactions, ~4× more than single-agent.
5. Parallel tool calling cut research time by **up to 90%** for complex queries.
6. Self-improving tool description agent reduced task completion time by **40%**.
7. Most coding tasks involve fewer truly parallelizable subtasks than research — a poor fit for multi-agent architectures.
8. Human testers discovered source quality bias that **no automated evaluation detected**.
9. Extended thinking serves as a controllable planning scratchpad for the orchestrator before acting.
10. Without detailed task decomposition, subagents duplicate work rather than divide it.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]] — orchestrator-worker pattern, agent lifecycle, durable execution
- [[themes/multi_agent_coordination|Multi-Agent Coordination]] — parallelism, synchronization, emergent behaviors, coordination bottlenecks
- [[themes/agent_evaluation|Agent Evaluation]] — LLM-as-judge, human testing, stateful evaluation challenges
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]] — BrowseComp analysis, performance variance decomposition
- [[themes/agent_memory_systems|Agent Memory Systems]] — context window management, external memory, summarization checkpoints
- [[themes/knowledge_and_memory|Knowledge and Memory]] — subagent compression, artifact systems, handoff continuity
