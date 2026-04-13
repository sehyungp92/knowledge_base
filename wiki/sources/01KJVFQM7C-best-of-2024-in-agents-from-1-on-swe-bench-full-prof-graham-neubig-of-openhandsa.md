---
type: source
title: 'Best of 2024 in Agents (from #1 on SWE-Bench Full, Prof. Graham Neubig of
  OpenHands/AllHands)'
source_id: 01KJVFQM7CTX1HV5BZRMW72TH9
source_type: video
authors: []
published_at: '2024-12-25 00:00:00'
theme_ids:
- agent_evaluation
- agent_systems
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Best of 2024 in Agents (from #1 on SWE-Bench Full, Prof. Graham Neubig of OpenHands/AllHands)

Prof. Graham Neubig's end-of-year retrospective from the OpenHands project distills hard-won lessons from building and deploying the #1-ranked system on SWE-Bench Full. Rather than celebrating benchmark scores, Neubig interrogates the gap between leaderboard performance and real-world utility, identifies eight design considerations for agent systems, and anticipates where the field is heading in 2025 — with particular attention to the limitations that remain stubbornly unsolved.

**Authors:** Graham Neubig
**Published:** 2024-12-25
**Type:** Video

---

## Agent-Compute Interface

OpenHands' central architectural bet is **CodeAct**: rather than exposing a fixed menu of granular API tools, the agent is given the ability to write and execute arbitrary Python code. This means instead of issuing twenty sequential tool calls, the agent can compose a program that orchestrates them all at once, execute it, observe the output, and fix errors inline. The agent is given only five or six tools — bash execution, Jupyter cell execution, file editing with browse/overwrite, global search-and-replace, and web browsing — but gains access to the full Python ecosystem (requests, PDF parsers, visualization libraries, GitHub API wrappers) through that code execution surface.

This design choice turns out to be load-bearing. Agents can `git clone` repositories, run data pipelines, call REST APIs, and automate GitHub workflows without any special-casing. The limitation is that scaling to new domains still requires **manual microagent engineering**: trigger detection and custom prompt instructions must be hand-crafted for each new tool or context, with no automated mechanism for capability extension.

---

## Human-Agent Interface

Neubig is candid that no one has solved this problem well. The guiding principles he offers:

- Present the user with what the agent is doing in plain English at each action step
- Meet the user where they already work — but only to a point

OpenHands offers three surfaces: a chat UI, a GitHub plugin for tagging and resolving issues directly from PRs, and a remote runtime API for launching headless fleets of agents. The right interface is use-case dependent, and the field has not converged on a general answer.

A critical and underappreciated failure mode sits here: **agents cannot reliably recognize when to ask for help**. They ask when they don't need it (interrupting unnecessarily) and stay silent when they should escalate (proceeding confidently toward the wrong solution). This is a core blocker for any interactive human-in-the-loop workflow.

---

## Choosing a Language Model

For agentic use, Neubig identifies four required properties:

1. **Instruction following** — determines what applications are even possible
2. **Tool use and coding ability** — determines how well the agent uses its interface
3. **Environment understanding** — e.g., parsing web pages via vision or text
4. **Error awareness and recovery** — the ability to recognize failure and try something different

Claude was "head and shoulders above the rest" across these dimensions when evaluated within OpenHands. The sharpest contrast was on error recovery: GPT-4o gets stuck in repetitive loops, issuing the same failing action repeatedly. Claude instead attempts alternative strategies. This difference is not minor — error recovery ability is what separates agents that make progress from agents that spin.

Open-source models (Llama 3.1 405B) lag meaningfully behind frontier models on these combined properties, making model portability a live bottleneck.

---

## Planning

Two axes structure the planning design space:

- **Curated vs. generated**: For GitHub issue resolution, OpenHands uses a curated workflow (reproduce → fail tests → fix → pass tests). For more open-ended tasks, the model generates its own plan. Both approaches are valid and depend on whether the task structure is predictable.
- **Explicit vs. implicit structure**: Explicit multi-agent systems break the plan into subagents with defined roles. Neubig's preference, however, is **single-agent with strong instruction following**, because it preserves the flexibility to deviate from the plan when the situation demands it. A rigid multi-agent pipeline can't adapt when reality doesn't match the plan.

**Information gathering is the most common failure mode.** The single biggest source of agent errors is attempting to solve a task before gathering sufficient information. Mitigating this requires explicit prompt scaffolding — essentially instructing the agent to gather information first — but this instruction is not automatically learned or applied. It must be manually engineered into the system prompt.

---

## Web Agents and Interaction Modalities

Three modalities for web interaction, ranked by effectiveness:

1. **API-based** — most accurate; APIs are structured and predictable
2. **Accessibility tree / HTML** — middle ground; HTML is too large to use directly but accessibility trees (designed for screen readers) are a practical intermediate
3. **Screenshot + pixel clicking** — least effective; models frequently misclick, sometimes landing on ads or unrelated elements

Neubig's work on API-based web agents shows a significant accuracy gap between API and browser interfaces. Markdown conversion of web content offers a more concise representation than HTML but still requires preprocessing overhead.

---

## Memory and Self-Improvement

**Agent Workflow Memory** is OpenHands' approach to self-improvement: after successful task completions, the workflows are extracted and injected back into the agent's prompt for future similar tasks. This achieved a **22.5% improvement on WebArena after 40 examples**.

The approach works for web tasks but runs into a hard wall for code: **RAG from natural language to code does not work well**. This limits the scalability of memory-augmented approaches for software engineering agents. Infinite context is not a practical substitute. The gap between the conceptual appeal of self-improvement and its current practical limitations is significant.

---

## Benchmarks: The Gap Between Scores and Reality

This is where Neubig is most blunt. OpenHands reports 53–55% on SWE-Bench Verified. His estimate of real-world performance on his own repositories: **30–40%**.

The inflation has a structural cause: SWE-Bench tests popular open-source repositories whose issues and code are present in LLM training data. The benchmarks are not measuring out-of-distribution generalization.

The historical pattern is now playing out again:
- 2023: benchmarks were too easy → built WebArena and SWE-Bench
- 2024: agents were too weak → built better agents
- 2025 (predicted): current benchmarks will saturate → need harder benchmarks

WebArena is already flagged as too easy — its tasks take a skilled human about two minutes. No existing benchmark tests the combined versatility of agents across both coding and web navigation simultaneously.

With interactive feedback, agents can solve 80–90% of tasks without the user opening an IDE. Autonomously, the number is 30–40%. The 40–60 point gap is the measure of how far agents remain from reliable independent operation.

---

## Open Questions and Limitations

| Limitation | Severity | Trajectory |
|---|---|---|
| Real-world performance gap vs. benchmark scores (contamination) | Significant | Stable |
| Agents fail to gather sufficient info before acting | Significant | Improving |
| Agents don't know when to ask for help | Significant | Unclear |
| Screenshot-based clicking is unreliable | Significant | Stable |
| RAG from language to code is ineffective | Significant | Unclear |
| World infrastructure not designed for agents | Significant | Worsening |
| Microagent scaling requires manual engineering | Significant | Stable |
| Benchmark saturation reducing measurement signal | Significant | Worsening |

The infrastructure gap deserves particular attention: most APIs lack fine-grained authentication tokens, most websites have no agent-compatible interface, and building one requires deliberate design choices that the current web was not built to support. Neubig frames this as a decades-long transition — the world will need to be prepared for agents, not just the agents prepared for the world.

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/software_engineering_agents|Software Engineering Agents]]
- [[themes/computer_use_and_gui_agents|Computer Use and GUI Agents]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/agent_evaluation|Agent Evaluation]]

## Key Concepts

- [[entities/agent-workflow-memory|Agent Workflow Memory]]
- [[entities/bagel|Bagel]]
- [[entities/webarena|WebArena]]
