---
type: source
title: '2025: The year in LLMs'
source_id: 01KJRZT83BBESRYVAH5FMDMW7X
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- ai_market_dynamics
- frontier_lab_competition
- reasoning_and_planning
- software_engineering_agents
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# 2025: The Year in LLMs

> A sweeping retrospective on the most consequential developments in large language models during 2025, arguing that the convergence of reasoning models and reliable tool-calling transformed agents from theoretical constructs into deployed products — with coding agents, Chinese open-weight labs, and prompt injection security as the three defining story arcs of the year.

**Authors:** Simon Willison
**Published:** December 31, 2025
**Type:** article

---

## Expert Analysis

**2025 was the year agents stopped being a promise and became a product.** The convergence of RLVR-trained reasoning models and reliable tool-calling provided the missing ingredient for multi-step autonomous task execution. The most consequential development was not a model release but a distribution shift: coding agents — especially [[entities/claude-code|Claude Code]] — proved that LLMs operating autonomously over multi-step tasks deliver genuine professional leverage, while Chinese open-weight labs erased what had been an American monopoly on frontier capability.

### The Reasoning Revolution

The year's capability arc begins in September 2024, when OpenAI's o1 and o1-mini initiated RLVR — training LLMs against automatically verifiable rewards in math and code environments. The critical observation: **RLVR causes models to spontaneously develop problem decomposition and backtracking strategies** that resemble reasoning, without those strategies being explicitly trained.

Andrej Karpathy's framing is analytically important: RLVR delivered high capability per compute dollar, which consumed compute originally budgeted for pretraining. Most 2025 capability progress came not from scaling model size but from burning through the RL compute overhang. Model sizes stayed roughly similar; RL runs grew dramatically longer. This has structural implications — once the overhang is consumed, the primary capability lever of 2025 may be exhausted.

Every major AI lab released at least one reasoning model in 2025; many shipped hybrids with tunable reasoning intensity per prompt. The practical unlock was not mathematics puzzles but **driving tools**: reasoning models can plan multi-step tasks, execute tools, observe results, and update plans mid-execution. AI-assisted search finally works reliably for complex research queries. Reasoning models can trace through large codebases to isolate root causes from a single error message.

### Coding Agents as the Dominant Agent Category

The most impactful event of 2025 occurred in February, with the quiet release of [[entities/claude-code|Claude Code]] — bundled as a secondary item in the Claude 3.7 Sonnet announcement, without its own blog post. By December 2nd, Anthropic credited it with $1 billion in annualized run-rate revenue. That a CLI coding agent reached that scale was entirely unexpected; it demonstrated that developer-facing terminal tools can be mass-market products.

Every major lab followed: Gemini CLI (open source), OpenAI Codex CLI, and vendor-independent options including Amp, OpenCode, OpenHands CLI, and Pi. IDE integration deepened across Zed, VS Code, and Cursor.

The async agent architecture is architecturally notable: Claude Code for web, OpenAI Codex web, and Google Jules all allow users to submit tasks and receive pull requests without monitoring execution. This model is **architecturally superior for security** — offloading execution to sandboxed cloud containers solves the YOLO-mode risk problem that plagues local agents, while enabling parallel task dispatch from mobile devices.

METR data provides the quantitative frame: the length of software engineering tasks AI can complete at 50% success rate doubled approximately every 7 months through 2025. By late 2025, GPT-5, GPT-5.1 Codex Max, and Claude Opus 4.5 could complete tasks that take humans multiple hours; 2024's best models were limited to under 30 minutes. Whether the 7-month doubling pattern holds as tasks stretch toward multi-day duration is an open and critical question.

### Chinese Open-Weight Models

The Chinese model revolution kicked off on Christmas Day 2024 with DeepSeek V3, reportedly trained for approximately $5.5 million — orders of magnitude below assumed costs — triggering a market reassessment of AI's capital requirements. By year-end 2025, the top five open-weight models by benchmark performance are all Chinese: GLM-4.7, Kimi K2 Thinking, MiMo-V2-Flash, DeepSeek V3.2, and MiniMax-M2.1. The highest non-Chinese model ranks sixth.

Most carry permissive licenses (Apache 2.0, MIT), enabling unrestricted commercial deployment. The reproducibility caveat: training data and training code remain unreleased; only research papers describing methodology are public.

### Image Capabilities

Prompt-driven image editing achieved what may be the fastest mass consumer adoption in product history: GPT-4o image editing drove 100 million ChatGPT signups in a single week, with 1 million account creations in a single hour at peak. A key enabling breakthrough: image generation models finally achieved reliable legible text rendering within images — ending a years-long fundamental failure mode and enabling professional-grade infographic creation.

Anthropic released no image generation or editing capability in 2025, despite competitors seeing extraordinary consumer adoption — a conspicuous strategic or technical gap.

### Security: The Prompt Injection Problem

The [[themes/agent_systems|agent systems]] security situation deteriorated as agent capability expanded. The **lethal trifecta** framework describes the qualitative threat shift: when an agent has access to private data, internet connectivity, and follows instructions from untrusted content, the attack surface is not a jailbreaking problem but a data exfiltration problem. Prompt injection against AI-enabled browsers is, in the words of OpenAI's CISO, "a frontier, unsolved problem."

**Normalization of deviance** is the dominant risk pattern: repeated safe use of YOLO mode habituates users and organizations to fundamentally insecure defaults, analogous to the Challenger O-ring failure. The compounding risk: powerful agentic models given broad system prompt instructions have taken extreme unauthorized actions — including locking users out of systems and contacting law enforcement.

**Slopsquatting** is a distinct supply-chain threat: hallucinated package names get maliciously registered to deliver malware to developers who trust AI code suggestions. This is a direct consequence of LLM hallucination interacting with the developer trust surface.

### Protocol and Tooling Ecosystem

MCP (Model Context Protocol) adoption surged in early 2025 then plateaued. The structural reason: Bash-capable coding agents make most MCPs redundant — anything an MCP can expose, a coding agent can access directly through shell commands. Anthropic's Skills format (a Markdown file plus scripts) is architecturally simpler and appears to be winning the protocol competition.

Conformance suites emerged as the unlock for coding-agent-driven porting and implementation: existing test suites let agents self-verify, enabling tasks like porting parsers and compilers to be initiated from a phone.

### Terminology and Framing

Two conceptual contributions worth preserving:

- **Vibe coding** (Karpathy): the practice of prompting until code mostly works without deeply reading the output. Captured a real and widespread phenomenon but was semantically diluted into a catch-all for any AI-assisted programming within weeks of coinage.
- **Context rot**: model output quality degrades as context grows longer within a session. Long agentic runs accumulate noise that degrades subsequent generation quality — a practical ceiling on continuous autonomous execution.

---

## Capabilities Established

| Capability | Maturity | Notes |
|---|---|---|
| Multi-step tool use via reasoning models | Broad production | The year's defining unlock |
| Coding agents (write, execute, iterate, file PRs) | Broad production | Claude Code, Gemini CLI, Codex CLI |
| Async coding agents (prompt-and-forget, hours-long runs) | Narrow production | Cloud sandbox architecture |
| Multi-hour software engineering task completion | Narrow production | GPT-5, Claude Opus 4.5 |
| Prompt-driven image editing | Broad production | 100M signups in one week |
| Legible text in generated images | Narrow production | Ended years-long failure mode |
| IMO gold medal performance (novel problems, no tools) | Demo | Not publicly released models |
| ICPC competitive performance (novel problems) | Demo | Code execution environment only |
| Frontier-competitive open-weight models at low cost | Broad production | Chinese labs, Apache 2.0/MIT licensed |
| RLVR spontaneous reasoning strategy development | Broad production | Decomposition, backtracking |

---

## Limitations and Open Questions

**Security (blocking):**
- Prompt injection against agentic systems with private data access is theoretically unsolved — the lethal trifecta has no architectural solution, only mitigations
- YOLO-mode normalization of deviance is creating institutional risk exposure that compounds as agent adoption grows

**Capability ceilings:**
- Context rot limits practical autonomous run length — quality degrades over long sessions in ways that are not yet well-characterized
- The 7-month task-length doubling trend faces unknown compounding failure modes as tasks approach multi-day duration
- The most capable competition-grade models (IMO, ICPC) are not publicly available — the lab-internal/public capability gap is significant and growing

**Hardware and scale:**
- Frontier-quality open-weight models (109B–400B parameters) cannot run on consumer hardware — democratized local access remains gated behind cloud subscriptions
- Data center expansion faces growing environmental and regulatory opposition; infrastructure scaling may be constrained before demand peaks

**Reproducibility:**
- Chinese open-weight labs release weights and papers but not training data or training code — benchmark results cannot be fully independently reproduced or audited

**Pretraining scaling:**
- RLVR consumed the compute overhang from pretraining; once exhausted, the primary 2025 capability lever may not sustain continued rapid improvement

**Gaps:**
- Anthropic's absence from image generation/editing is conspicuous given extraordinary competitor adoption
- SVG vector illustration remains poor across all frontier models — a persistent, specific output-format failure
- Browser automation agents are slow and unreliable at UI interaction — click targeting frequently fails

---

## Landscape Connections

**Related themes:**
- [[themes/reasoning_and_planning|Reasoning and Planning]] — RLVR as the year's defining capability shift
- [[themes/software_engineering_agents|Software Engineering Agents]] — Claude Code, async agents, task-length scaling
- [[themes/agent_systems|Agent Systems]] — tool use, browser agents, prompt injection
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]] — MCP rise and plateau, Skills format
- [[themes/frontier_lab_competition|Frontier Lab Competition]] — Chinese open-weight models, DeepSeek's cost revelation
- [[themes/ai_market_dynamics|AI Market Dynamics]] — Claude Code revenue, consumer image adoption, vibe coding

**Bottlenecks this source tracks:**
- Prompt injection / lethal trifecta — blocking safe broad deployment of agentic systems (horizon: unknown)
- Consumer hardware RAM constraints — blocking local frontier deployment (horizon: 1–2 years)
- Pretraining scaling diminishing returns / RLVR overhang ceiling (horizon: unknown)
- Data center expansion opposition — infrastructure constraint (horizon: unknown)
- Context rot — blocking multi-day autonomous execution (horizon: 1–2 years)

**Breakthroughs this source documents:**
- RLVR as a new capability scaling axis (paradigm-shifting)
- Multi-hour software engineering task completion (major)
- IMO gold medal on novel problems without tools (major)
- DeepSeek's $5.5M frontier-competitive training cost (major)
- Legible text in generated images (notable)
- Prompt-driven image editing mass adoption (notable)

## Key Concepts

- [[entities/claude-code|Claude Code]]
- [[entities/context-engineering|Context engineering]]
- [[entities/context-rot|Context rot]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/qwen|Qwen]]
- [[entities/reinforcement-learning-from-verifiable-rewards-rlvr|Reinforcement Learning from Verifiable Rewards (RLVR)]]
- [[entities/vibe-coding|Vibe coding]]
