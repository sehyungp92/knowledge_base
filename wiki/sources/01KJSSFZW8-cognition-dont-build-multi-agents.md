---
type: source
title: Cognition | Don’t Build Multi-Agents
source_id: 01KJSSFZW8ZFXBYS7AHT81Z0PN
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- multi_agent_coordination
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Cognition | Don’t Build Multi-Agents

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Cognition | Don't Build Multi-Agents
article
https://cognition.ai/blog/dont-build-multi-agents#principles-of-context-engineering

---

## Briefing

**Parallel multi-agent systems are architecturally broken in 2025: the root cause is that agents cannot share context thoroughly enough to make consistent implicit decisions, and the solution is to default to single-threaded linear agents until the field solves cross-agent context-passing.** The author (from Cognition, builders of Devin) argues from production experience that two inviolable principles — share full traces, and prevent conflicting implicit decisions — rule out most multi-agent designs today, and that real-world examples like Claude Code validate this conservative approach.

### Key Takeaways
1. **Parallel multi-agent systems are fragile by design** — Subagents decomposed from a parent task lack the multi-turn conversation history and tool-call context needed to interpret their subtask correctly, leading to compounding miscommunication.
2. **Sharing the original task is insufficient** — Even with full task context, parallel subagents cannot see each other's actions and therefore make conflicting implicit decisions that produce inconsistent outputs.
3. **Actions embed hidden assumptions** — Every agent action encodes an implicit choice; when parallel agents make conflicting implicit choices, the final result degrades in ways that are hard to predict or debug.
4. **Two principles should be treated as near-inviolable** — Share full agent traces (not just messages), and ensure no two agents make conflicting implicit decisions; architectures violating these should be ruled out by default.
5. **Single-threaded linear agents are the reliable baseline** — Continuous context eliminates inter-agent conflicts and handles most real-world tasks well, at the cost of eventual context window overflow for very long tasks.
6. **Context compression is the key extension for long-horizon tasks** — A dedicated model (potentially fine-tuned) that distills action history into key decisions can extend effective trace length; Cognition does this in production for Devin.
7. **Claude Code deliberately avoids parallel subagents** — Its subagents only answer questions (never write code), run sequentially, and exist solely to keep investigative work out of the main agent's context window — a purposefully simple design.
8. **The edit apply model pattern failed for the same reason** — Splitting decision-making (large model) from application (small model) created an inter-agent context gap; slight ambiguities caused incorrect edits, and unified single-model editing is now preferred.
9. **Multi-agent "dialogue" is not yet reliable** — Agents cannot engage in the kind of efficient, high-bandwidth knowledge exchange humans use to resolve conflicts; the communication overhead and context loss makes multi-agent collaboration worse than a single agent.
10. **Cross-agent context-passing is an unsolved problem with no dedicated research effort** — The author sees no one directly working on it and believes it will emerge as a byproduct of improving single-agent human communication rather than as a direct research target.

---

### Why Parallel Multi-Agent Systems Fail

- The intuition behind parallel multi-agent decomposition is sound — real tasks have parallel components — but the execution is structurally broken given current agent capabilities.
  - Example: Decomposing "build a Flappy Bird clone" into parallel subagents results in one agent producing Super Mario Bros-style graphics and another producing a non-game-asset bird with wrong movement physics.
  - The final integration agent then inherits two layers of miscommunication with no way to reconcile them.
- **Real-world tasks contain many layers of nuance** that are all potential sites of miscommunication — the toy example is representative, not contrived.
- A naive fix — copying the original task description to all subagents — is insufficient in production systems.
  - Production conversations are multi-turn; the task breakdown itself required tool calls.
  - Any detail in those tool call results or intermediate messages could change how the subtask should be interpreted.
  - The subagent has no access to this history if only the final task message is forwarded.

### The Two Inviolable Principles

- **Principle 1: Share full agent traces, not just individual messages.**
  - Subagents must see the complete history of the parent agent — all tool calls, all intermediate messages, all decisions — not just their subtask description.
  - Without this, subagents will systematically misinterpret intent.
- **Principle 2: Actions carry implicit decisions; conflicting implicit decisions produce bad results.**
  - Even with Principle 1 satisfied (full context from parent), parallel subagents still cannot see each other's actions.
  - When subagent 1 chooses a visual style and subagent 2 independently chooses a different one, neither is wrong given their local information — but the combined output is inconsistent.
  - These conflicting implicit decisions are invisible before the fact and painful to resolve after.
- The author argues these principles are **so fundamental and so rarely worth violating** that they should be a hard architectural filter: any design that cannot satisfy them should be ruled out by default.
  - This is not as constraining as it sounds — a wide design space remains within these constraints.

### The Recommended Architecture: Single-Threaded Linear Agent

- The simplest compliant architecture is a fully sequential agent with one continuous context window.
  - Context is never split; every action has access to the full history; no implicit decisions can conflict.
  - This architecture handles most real-world tasks well in practice.
- The limitation is context window overflow for very long, complex tasks with many subparts.
- For teams willing to invest in solving long-horizon reliability, **context co

## Key Claims

1. Parallel multi-agent architectures where tasks are divided among subagents are fundamentally fragile due to context miscommunication.
2. Providing subagents with only a subtask description — without full conversation and tool-call history — leads to misinterpretation of the original intent.
3. Even when subagents share the original task context, parallel subagents still produce inconsistent outputs because they cannot see each other's actions and therefore make conflicting implicit assumpti
4. Every agent action carries implicit decisions, and when parallel agents make conflicting implicit decisions, the resulting system output degrades.
5. Sharing full agent traces — not just individual messages — is a necessary condition for reliable multi-component agent systems.
6. A single-threaded linear agent maintains continuous context and is the simplest reliable architecture, though it faces context window overflow for very large tasks.
7. A dedicated context compression model that summarizes agent history into key details and decisions can extend effective context length for long-horizon tasks.
8. Cognition has fine-tuned a smaller model for context compression in their Devin agent system.
9. As of June 2025, Claude Code never performs work in parallel with its subtask agents; subtask agents only answer questions rather than write code.
10. Claude Code uses subagents specifically to offload investigative work so it does not occupy the main agent's context window, thereby extending the effective trace length.

## Capabilities

- Dedicated context compression models can distil long agent action histories into key details, decisions, and events, enabling agents to operate effectively beyond normal context window limits on extended tasks
- Software agents can spawn read-only investigative subagents restricted to answering well-defined questions, isolating token-heavy investigation traces from the main agent context without risking conflicting code actions
- Frontier coding models can handle both code edit decision-making and application in a single model action, replacing the prior fragile two-model pipeline where a large model generated markdown instructions and a small model applied them

## Limitations

- Parallel subagent architectures produce inconsistent outputs because subagents cannot observe each other's actions and therefore make conflicting implicit decisions, with no mechanism to reconcile diverged assumptions
- Multi-agent collaborative systems in 2025 are fragile at the production level — decision-making is too dispersed and context cannot be shared thoroughly enough between agents to achieve reliability comparable to single-agent architectures
- No active research effort in the field is dedicated to solving the cross-agent context-passing problem, meaning the key bottleneck to reliable multi-agent parallelism is entirely unaddressed
- Single-threaded agents hit context window overflow on very large, long-duration tasks with many subparts, requiring significant architectural investment in context compression to extend task length
- Context compression for long-running agents is difficult to engineer correctly, requires significant domain-specific investment, and may require fine-tuning a smaller model — there is no general-purpose automated solution
- Claude Code's subagent architecture is intentionally constrained to prevent parallelism — subagents cannot write code because they lack the full task context, meaning agentic coding gains context isolation but not throughput
- Agents cannot efficiently communicate implicit knowledge to peer agents the way humans can — AI-to-AI collaborative discourse produces no better reliability than a single agent, despite the intuitive appeal of multi-agent consensus
- In multi-turn agentic production systems, subtask context is extremely difficult to propagate correctly — tool calls, intermediate decisions, and implicit assumptions accumulate nuanced dependencies that cannot be captured by passing only the original task prompt
- The two-model edit apply pipeline (2024) was faulty — small apply models frequently misinterpreted large model markdown instructions and made incorrect edits due to slight ambiguities, revealing a fragility in chained-model architectures

## Bottlenecks

- The cross-agent context-passing problem is unsolved and actively unaddressed — agents cannot efficiently share the full implicit reasoning context needed for reliable parallel collaboration, blocking genuine multi-agent parallelism in production
- Context compression for long-running agents requires domain-specific engineering investment with no general-purpose solution, capping the practical autonomous task duration before context overflow or critical information loss

## Breakthroughs

- Frontier coding models shifted from requiring a dedicated two-model 'edit apply' pipeline to handling both edit reasoning and application in a single model action, collapsing a fragile multi-model coordination layer

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/claude-code|Claude Code]]
- [[entities/context-engineering|Context engineering]]
- [[entities/devin|Devin]]
