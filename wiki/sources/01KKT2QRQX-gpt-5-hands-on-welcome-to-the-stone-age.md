---
type: source
title: 'GPT-5 Hands-On: Welcome to the Stone Age'
source_id: 01KKT2QRQX3681G2XAPPVCEHKY
source_type: article
authors: []
published_at: '2025-08-07 00:00:00'
theme_ids:
- ai_market_dynamics
- code_and_software_ai
- code_generation
- frontier_lab_competition
- interpretability
- model_behavior_analysis
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GPT-5 Hands-On: Welcome to the Stone Age

**Authors:** 
**Published:** 2025-08-07 00:00:00
**Type:** article

## Analysis

# GPT-5 Hands-On: Welcome to the Stone Age
2025-08-07 · article
https://www.latent.space/p/gpt-5-review

---

## Briefing

**GPT-5 represents a qualitative shift in LLM capability — not by being uniformly smarter, but by thinking natively through tools in a way that makes it the best coding model in the world while being worse at writing than its predecessors. The author frames this as an "AI Stone Age" milestone: the defining criterion for AGI-level intelligence is integrated tool use, not narrow benchmark performance, and GPT-5 is the first model to cross that threshold convincingly.**

### Key Takeaways
1. **GPT-5 is the best coding model in the world** — the author estimates it moved software engineering automation from ~65% to ~72% complete, calling it the biggest leap since GPT-3.5 Sonnet.
2. **GPT-5 thinks through tools, it doesn't just call them** — analogous to how Deep Research taught o3 to conduct iterative research rather than make a single web search call, GPT-5 applies this same integrated reasoning to any tool.
3. **One-shotting complex tasks is a step-change** — GPT-5 solved nested dependency conflicts with Vercel AI SDK v5 + Zod 4 in a single pass after both o3+Cursor and Claude Opus 4 failed entirely.
4. **Parallel tool calling is qualitatively different here** — prior models were technically capable but rarely correct; knowing which tasks to parallelize vs. serialize requires genuine intelligence, and GPT-5 demonstrates this reliably.
5. **GPT-5's output is closer to production-ready, not just prototype-quality** — unlike Claude Opus 4 (builds from scratch, no DB) it leverages standard frameworks (create-next-app) and includes a SQLite database by default.
6. **GPT-5 is worse at writing than GPT-4.5 and possibly GPT-4o** — business writing produces "LinkedIn-slop" style output; GPT-4.5 and DeepSeek R1 remain superior for tone-matching and personal writing.
7. **The model is highly instructable and literal but personality-free** — where Claude models have distinct personalities, GPT-5 simply executes; this is a feature for agentic tasks, a limitation for creative work.
8. **Optimal tool design for GPT-5 means natural language interfaces, not structured APIs** — tools should accept free-text descriptions and act as sub-agents, exploiting OpenAI's new free-form function calling support.
9. **Prompting GPT-5 requires an "agent compass" not a context dump** — provide project purpose, key files, organization, domain terms, and success criteria rather than pre-loading dense context.
10. **When GPT-5 gets stuck, Socratic questioning outperforms correction** — asking "what does that failure tell you?" is more effective than "that's wrong."
11. **The AGI frame has shifted from benchmark performance to tool-integrated cognition** — the author argues humans became intelligent by externalizing capabilities into tools, and GPT-5 marks the first LLM to exhibit this property at scale.
12. **Non-developers will miss the significance for months** — GPT-5's value requires integration into products; raw API/chat access does not expose its core differentiation.

---

### The AGI Reframe: Tool Use as the Intelligence Threshold

- The author explicitly rejects narrow benchmark performance (chess, theorem-proving, digit recitation) as the appropriate metric for AGI.
  - The Stone Age analogy: human intelligence is defined by tool use — we externalized short-term memory into writing, trading internal capability for external leverage.
  - Chimpanzees have better short-term memory than humans precisely because we offloaded that to writing systems.
- **The claim is that GPT-5 "thinks with tools, not just uses them"** — a qualitative shift from tool-calling as function invocation to tool-calling as a mode of reasoning.
  - Deep Research is the first demonstration of this pattern: o3 was taught to conduct research iteratively, not to call a search API and respond.
  - GPT-5 extends this pattern to all tools it has access to.
- This framing explains why GPT-5's writing regression doesn't undermine the AGI thesis — **a human who uses tools well isn't assessed by raw memorization; the relevant capability is the integrated system.**

---

### GPT-5 vs. Competitors: Coding Benchmark Comparison

- **Dependency conflict resolution (Vercel AI SDK v5 + Zod 4):**
  - o3 + Cursor: failed.
  - Claude Code + Opus 4: failed (ended with "Here are some things to try" — the author glosses this as "giving up").
  - GPT-5: one-shotted it.
  - GPT-5's approach: ran `yarn why` systematically across directories, took notes between runs, paused to reason when anomalies appeared, then made precise multi-file edits.
  - Contrast with Claude Opus 4: guessed a solution, ran tool calls, encountered failures, tried more things — trial-and-error without an investigative phase.

- **Full-stack web app one-shot (Is It Worse Or Just Me? — Cursor + SQLite DB):**
  - o3: gave a plan only; when prompted to implement, produced scaffolding but not a working app; required 3+ follow-ups; 10x slower.
  - Claude Opus 4: immediately built something, but from scratch (no frameworks), no database — good prototype, not production-ready.
  - Claude Opus 4.1: attempted full-stack with SQLite (more ambitious), but encountered build errors requiring multiple back-and-forths.
  - GPT-5: one-shotted the full-stack app including SQLite, using create-next-app, with correct project naming (`IsItWorseOrJustMe` vs o3's generic `my-app`).

- **Mac OS 9 website (pure HTML/CSS/JS, no libraries):**
  - GPT-5 one-shotted the entire UI including a paint application.
  - Paint app included: pen, pencil, eraser, color picker, thickness control — all functional.
  - Added icon drag-and-drop with localStorage persistence without being asked.
  - Author has never read the code; reports everything works.

- **Complex Clickhouse query:**
  - o3 struggled; GPT-5 one-shotted it.

- **Self-referential debugging (swyx anecdote):**
  - GPT-5 debugged 3 layers of nested ab

## Key Claims

1. GPT-5 is the best coding model in the world as of its release.
2. GPT-5 is worse at writing than GPT-4.5 and possibly GPT-4o.
3. GPT-5 successfully one-shotted resolving complex nested dependency conflicts with Vercel's AI SDK v5 and Zod 4, which o3 and Claude Opus 4 failed to solve.
4. Claude Opus 4 approached the dependency conflict problem by guessing and running trial-and-error tool calls, ultimately ending with suggestions rather than a solution.
5. GPT-5 used a systematic investigative approach to solve dependency conflicts, using yarn why commands and taking notes between runs before editing files.
6. GPT-5 can debug multiple layers of nested abstractions in a codebase, including migrating an old AI SDK version to support GPT-5 itself.
7. GPT-5 one-shotted a Mac OS 9 themed personal website in pure HTML/CSS/JS including a functional paint app with pen/pencil/eraser tools, color picker, and thickness control.
8. GPT-5 autonomously implemented localStorage persistence for icon positions and file saving without being explicitly prompted for it.
9. With the same prompt, o3 in Cursor only provided a plan rather than implementing the application, requiring multiple follow-up interactions and spending 10x more time than GPT-5.
10. Claude Opus 4 produced a prototype from scratch without using standard frameworks or a database, making it a good one-shot prototype but less production-ready than GPT-5's output.

## Capabilities

- One-shot resolution of complex nested dependency conflicts across large codebases, succeeding where frontier models (o3, Claude Opus 4) failed entirely
- One-shot generation of production-ready full-stack web applications, including proper framework scaffolding and database integration, without requiring follow-up prompts
- Tool-integrated reasoning: model uses tools as part of the thinking process (iterating, planning, exploring mid-tool-chain) rather than as discrete post-reasoning function calls
- Reliable parallel tool calling in practice: correctly determining which tools can run in parallel vs. sequentially and executing them concurrently
- Robust recovery from tool call failures during agentic loops, enabling longer-horizon autonomous operation
- Iterative self-correcting debugging: identifying what a failed attempt reveals, reasoning about it, and making targeted multi-file edits to converge on a solution

## Limitations

- GPT-5 is significantly worse at natural language writing quality than GPT-4.5 and GPT-4o, producing 'LinkedIn-slop' style responses that don't preserve user tone
- GPT-5 has no persistent memory across sessions; must be fully re-onboarded to codebase, code standards, and domain context on every invocation
- GPT-5's capabilities only manifest effectively when given the right high-quality, open-ended tools — atomic API-style tools underutilize the model and produce subpar results
- Prompting GPT-5 as a model rather than an agent degrades output quality significantly — the entire prompting paradigm must shift toward compass-style orientation rather than context pre-loading
- Non-developers cannot access GPT-5's capabilities without product integrations — the model's value is gated behind appropriate tooling and UI abstractions that don't yet exist at scale
- Software engineering automation is estimated at only ~72% complete even with GPT-5 — a hard ceiling on full automation remains, and the rate of progress per model generation is slowing
- Models are increasingly 'spiky' with capability tradeoffs — no single model dominates all tasks, forcing developers to maintain multi-model workflows or accept capability gaps
- Claude Opus 4.1 encountered build errors requiring multiple follow-ups on full-stack one-shot tasks, suggesting frontier models outside GPT-5 still struggle with end-to-end production code correctness
- GPT-5 is extremely literal and lacks the autonomous judgment to push back or add useful unsolicited improvements — where Claude models have 'minds of their own', GPT-5 just executes instructions verbatim

## Bottlenecks

- Current atomic API-style tool design paradigm is incompatible with how advanced reasoning agents like GPT-5 actually work, blocking effective deployment of agent-native products
- Product integration lag: GPT-5's agentic capabilities require purpose-built product wrappers before non-developers can access the value, delaying broad consumer adoption by months
- Remaining ~28% of software engineering tasks are blocking full automation; each model generation captures diminishing returns on this metric

## Breakthroughs

- GPT-5 demonstrates tool-integrated reasoning: tools are no longer discrete function calls that interrupt reasoning, but part of the thinking process itself — enabling iterative, exploratory, mid-chain reasoning with tool outputs
- GPT-5 achieves reliable one-shot production-ready code generation on tasks that previously required multiple frontier models working in series or failed entirely — resolving a class of complex dependency and integration problems in a single pass

## Themes

- [[themes/ai_market_dynamics|ai_market_dynamics]]
- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/frontier_lab_competition|frontier_lab_competition]]
- [[themes/interpretability|interpretability]]
- [[themes/model_behavior_analysis|model_behavior_analysis]]

## Key Concepts

- [[entities/claude-opus-41|Claude Opus 4.1]]
- [[entities/cursor|Cursor]]
- [[entities/deep-research|Deep Research]]
- [[entities/gpt-45|GPT-4.5]]
- [[entities/gpt-5|GPT-5]]
- [[entities/vibe-coding|Vibe Coding]]
- [[entities/o3|o3]]
