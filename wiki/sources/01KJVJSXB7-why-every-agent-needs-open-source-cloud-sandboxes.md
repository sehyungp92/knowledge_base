---
type: source
title: Why Every Agent needs Open Source Cloud Sandboxes
source_id: 01KJVJSXB77C96F4QVMJ33JV6Y
source_type: video
authors: []
published_at: '2025-04-24 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why Every Agent Needs Open Source Cloud Sandboxes

> An interview-style deep dive into E2B's evolution from AI agent hosting platform to general-purpose cloud sandbox infrastructure, tracing the company's product pivots, the explosive 375x growth in sandbox usage over 2024–2025, and the broader emergence of an LLM Operating System layer that enables agents to act as capable professionals with a persistent, stateful dev environment.

**Authors:** E2B (Vasek Mlejnsky)
**Published:** 2025-04-24
**Type:** video

---

## Expert Analysis

### Building an Agent Cloud

E2B launched as an AI agent cloud with a core hypothesis: code generation agents would need a persistent execution environment the way developers need a laptop. The initial product bundled hosting, monitoring, and a code execution sandbox — one early demo had an agent pulling GitHub repositories, working on code, and submitting PRs entirely inside the sandbox. This proved the sandbox's utility and scalability, but the go-to-market messaging proved difficult.

The company eventually found traction by narrowing to **code interpretation** — specifically AI-driven data analysis and visualization running inside a headless Jupyter-style notebook environment. The key insight was that the model doesn't need to manage how the program state is kept alive; the sandbox handles that. Jupyter itself turned out to be the wrong technical substrate at scale, but the abstraction it represented was correct.

### The Shift to General-Purpose Agent Runtime

By the end of 2024 into 2025, E2B's use cases had expanded dramatically: reinforcement fine-tuning (RFT), computer use, and deep research agents (notably Manus) all became significant consumers. The framing shifted accordingly — the sandbox is not a code interpreter but a **code runtime for LLMs**, analogous to a dev box.

The versatility mirrors how a human uses a laptop: create files, run scripts, download and transform data, browse the web via BrowserUse, generate Excel sheets, write small apps. The agent leveraging this environment is a capable professional — developer, accountant, researcher — and the sandbox simply gives it the tools to perform its job more effectively. This analogy carries real technical weight: the sandbox provides the stateful, isolated environment that makes complex multi-step agent tasks tractable.

### Growth Metrics

The scale of adoption is striking:

- **March 2024:** ~40,000 sandboxes/month
- **March 2025:** ~15 million sandboxes/month — roughly **375x growth in one year**

The growth curve notably steepened following the release of Claude Sonnet 3.7, suggesting a tight coupling between frontier model capability jumps and demand for execution infrastructure. This points to a broader dynamic: for the first time, **infrastructure is lagging applications** rather than leading them. In 2024, agents couldn't fully exploit the sandbox; by early 2025, LLMs were demanding more than the infrastructure could readily offer.

---

## Landscape Contributions

### Capabilities

**Scalable cloud sandbox execution** has reached [[themes/agent_systems|production scale]] for agentic workloads. E2B's numbers confirm that sandboxed code execution is not an experimental curiosity — it is a production primitive consumed at millions-of-invocations-per-month scale. See: [[themes/agent_systems|Agent Systems]].

**RL training infrastructure via sandboxes** has become a viable alternative to GPU clusters for the code evaluation step. Hugging Face's Open R1 project ran thousands of E2B sandboxes per training step to parallelize code generation reward evaluation, avoiding expensive GPU compute for verification. This is a meaningful capability unlock for open-source model development. See: [[themes/ai_business_and_economics|AI Business and Economics]].

**Agent framework ecosystem maturity** is further evidenced here: LangChain at ~20 million downloads/month, alongside Mastra, Composio, and Stagehand, establishes that standardized agent development patterns now exist at scale — contrary to the common developer perception that these frameworks are niche.

### Limitations

**Model version inconsistency** is a production-grade problem. The same code that successfully ran a complex agentic task one month may fail to replicate it after a model version update — not because the code changed, but because the model's behavior shifted. This creates a reproducibility crisis for production agentic systems and erodes deployment confidence. *(severity: significant, trajectory: unclear)*

**Gap between aspirational and actual agent capability** persists. Developers conceive of tasks agents should be able to handle, build toward them, and encounter that models simply aren't ready. This gap has been closing but remains a primary limiter on enterprise adoption. *(severity: significant, trajectory: improving)*

**Computer use / GUI automation** remains experimental. Across the ecosystem, only [[entities/anthropic|Anthropic]] appears to be deploying computer use at scale (via Manus), and Linux-only platform support creates a critical gap for Windows-dominated enterprise environments. *(severity: significant, trajectory: improving)*

**No technical distinction between agent and user access** in infrastructure protocols like [[themes/tool_use_and_agent_protocols|MCP]]. There is no mechanism to apply differential rate limits, access controls, or resource allocation based on whether the caller is a human or an autonomous agent. This is not a product gap at E2B specifically — it is an ecosystem-wide absence. *(severity: significant, trajectory: stable)*

**Web interfaces remain human-optimized.** Agents visiting human-oriented websites create misaligned incentive structures — OpenAI's crawler reads ~250 pages per referred visitor; Anthropic's reads ~6,000 per referred visitor, compared to Google's historical 2:1 ratio. The economics of the web assume human traffic patterns, and agents break that assumption without any current infrastructure response. *(severity: significant, trajectory: stable)*

**Advanced infrastructure features are hard to market without demonstration.** Sandbox forking and checkpointing are highly valuable for Monte Carlo tree search in agents (each node = a snapshotted sandbox state, enabling parallel path exploration), but developers cannot easily imagine this need without direct exposure. General-purpose platforms face a chronic education burden. *(severity: minor, trajectory: improving)*

### Bottlenecks

**Agent/user distinction at the protocol layer** is the deepest structural gap identified here. Without this, secure and efficient resource governance for agent ecosystems is impossible — rate limiting, access control, billing, and abuse prevention all require knowing whether a caller is human or autonomous. Resolution horizon: 1–2 years. See: [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]].

**Human-optimized web interfaces** block efficient agentic information retrieval and automation. Until websites offer agent-appropriate APIs or access layers, agents must parse human-oriented interfaces — expensive, brittle, and misaligned with website operator incentives. Resolution horizon: 1–2 years.

**Model version inconsistency** blocks reliable production deployment. If the same task fails after a model update, agentic systems cannot be operated with production SLAs. This is partly a model provider responsibility, partly an eval infrastructure problem. Resolution horizon: 3–5 years.

### Breakthroughs

**Agent infrastructure at production scale** is now demonstrated fact, not thesis. The 40K → 15M sandbox trajectory over 12 months is the clearest empirical signal that agentic code execution infrastructure has crossed the production threshold. See: [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business and Economics]].

**Distributed sandbox RL training** represents a meaningful infrastructure innovation: using cheap isolated sandboxes for reward evaluation during code model training, rather than GPU clusters, changes the cost structure of open-source model development. The Open R1 demonstration is the proof case. See: [[themes/ai_business_and_economics|AI Business and Economics]].

---

## The LLMOS Layer

E2B positions itself alongside BrowserBase and Exa as part of an emerging **LLM Operating System (LLMOS)** category — infrastructure companies that don't embed LLMs in their products but enable others to augment agents with real-world execution capabilities. The spectrum within this category runs from browser emulation → virtual machines → custom sandboxed environments; E2B occupies the most general position.

The company's intended user is not an infrastructure or ML engineer. It is the **AI engineer** and the web developer building LLM-powered applications — reflected in the SDK download split: ~500K Python/month, ~250K JavaScript/month. Python dominates for data analysis and code interpretation use cases; JavaScript is preferred for agentic web applications.

The product roadmap is shifting from SDK-first to **API-first** — a structural move that anticipates LLMs directly controlling infrastructure rather than developers instrumenting it. This is consistent with the broader [[themes/tool_use_and_agent_protocols|agent protocol]] evolution: the LLM needs to be able to spin up, checkpoint, fork, and tear down sandboxes through a stable API surface, not just through SDK abstractions built for human developers.

The "Kubernetes for agents" analogy is instructive: technically correct as an aspiration, but the actual product imperative is dramatically better developer experience — the abstraction must be invisible enough that AI engineers treat sandbox execution as a primitive, not an infrastructure concern.

---

## Open Questions

- As model capability continues to improve, which parts of the sandbox abstraction will models outgrow, and which will they increasingly depend on?
- What does the right agent/user distinction mechanism look like at the protocol layer — who builds it, and at which stack layer does it live?
- Will the web respond to agent traffic by building agent-appropriate APIs, by aggressively blocking crawlers, or by something else entirely?
- At what point does sandbox forking and checkpointing for tree-search agents become a standard design pattern rather than an advanced feature requiring education?
- Does the infrastructure-lagging-applications dynamic persist, or does the LLMOS layer eventually get ahead of model capability again?

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]]
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Key Concepts

- [[entities/llmtxt|llm.txt]]
