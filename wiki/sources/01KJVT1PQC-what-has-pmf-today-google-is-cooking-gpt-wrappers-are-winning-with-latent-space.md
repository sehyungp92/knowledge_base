---
type: source
title: What has PMF Today, Google is Cooking & GPT Wrappers are Winning | With Latent
  Space
source_id: 01KJVT1PQCFK94WXDZC2D03YXD
source_type: video
authors: []
published_at: '2025-03-28 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- frontier_lab_competition
- startup_and_investment
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# What has PMF Today, Google is Cooking & GPT Wrappers are Winning | With Latent Space

A retrospective and forward-looking analysis from the Latent Space podcast examining the past year of AI surprises — the rise of inference-time scaling, the failure of incumbents to capture the AI builder market, the shifting consensus on "GPT wrappers," and candid takes on what's overhyped versus underhyped heading into 2025.

**Authors:** Latent Space (swyx, Alessio)
**Published:** 2025-03-28
**Type:** video

---

## AI Surprises of the Past Year

### The Inference-Time Scaling Shift

The emergence of reasoning models was among the most notable surprises of the period — particularly striking because it arrived just as pre-training scaling was publicly declared to be exhausted. The timing was "suspiciously neat": OpenAI's o1/Strawberry had reportedly been in development for approximately two years before release, meaning the labs knew pre-training was winding down while quietly working on the next paradigm. The result was a [[themes/frontier_lab_competition|frontier lab]] narrative whiplash: from "scaling is dead" to "inference-time is the new scaling law" almost overnight.

This represents a genuine [[themes/agent_systems|agentic systems]] breakthrough — inference-time compute scaling is now the dominant paradigm, shifting the bottleneck from training to reasoning depth at inference time.

### Open Source's Plateau in Enterprise

Despite widespread developer enthusiasm, open-source model adoption in enterprise environments has stalled — and is declining. [[entities/braintrust|Braintrust]] estimated open-source usage in enterprise at approximately **5% and falling**. The diagnosis: enterprises are still in *use-case discovery mode*, defaulting to the most capable available model to find what works. By the time a use case is identified, a new generation of models arrives and the discovery cycle restarts. Licenses have had negligible impact on this dynamic.

The narrative around open source catching up to closed models also deserves scrutiny. The more precise framing is that [[entities/deepseek|DeepSeek]] specifically caught up — and there is evidence DeepSeek may stop open-sourcing future models. Beyond DeepSeek and Llama, most "open source" activity is distillation from DeepSeek, which is an order of magnitude cheaper than original research. Even DeepSeek's breakthrough was excellent execution of known techniques rather than fundamental novelty.

> *"It's always an order of magnitude cheaper to replicate what's already been done than to create something fundamentally new."*

### The GPT Wrapper Reversal

The [[themes/ai_market_dynamics|market consensus]] has inverted sharply. The industry moved from dismissing "GPT wrappers" to treating application-layer AI products as the only interesting category. Aravind Srinivas of [[entities/perplexity|Perplexity]] now proudly claims the wrapper label. [[entities/cursor|Cursor]] reached a ~$10B valuation. The defensibility thesis has shifted entirely: competitive advantage comes from the thousand small UX decisions, velocity, and network effects — not proprietary model weights or data moats.

The implication for early-stage companies: worrying about differentiation before product-market fit is premature. Build something people want first.

---

## Who Missed the AI Builder Wave

### Low-Code Incumbents

One of the more structurally interesting failures: low-code/no-code platforms — Zapier, Airtable, [[entities/retool|Retool]], Notion — had every structural advantage to capture the AI builder market: distribution, reach, fast-follow capability, and existing user bases. They didn't.

The diagnosis is that incumbents optimized their existing baselines with AI (e.g., Notion AI for writing documents) rather than rebuilding from scratch. New entrants like Bolt and Lovable, unburdened by prior product commitments, built AI-native tools and reportedly grew from $0 to $20M ARR in approximately three months.

> *"They should have the DNA. They already have the reach. They already have the distribution."*

This is a recurring [[themes/vertical_ai_and_saas_disruption|SaaS disruption]] pattern: incumbents protect their core and miss the adjacent architectural shift.

### Apple Intelligence

Apple was widely seen as prime-positioned for consumer AI — the most natural owner of personal assistants given hardware integration and on-device privacy. The execution failed across multiple dimensions, including the BBC hallucination incident (a notification falsely reporting a person had shot himself). The Apple Intelligence rollout is cited as a significant product-market fit failure despite structural advantages.

The one underappreciated Apple asset: **Private Cloud Compute (PCC)**, which could prove significant for bringing on-device security guarantees to cloud-based LLM inference. This remains underappreciated relative to the headline product failures.

---

## What Google Is Building

Google presents a split picture. The models are genuinely strong — Flash Thinking, native image generation, multimodal capabilities, YouTube summarization — but perception lags reality. The core friction is internal: Google Cloud vs. Vertex vs. AI Studio is a brand fragmentation problem, not a capability problem. The thesis is that Google's share will increase incrementally as they consolidate platforms and improve developer bridges (e.g., reasoning models are currently inaccessible in Cursor).

For developers specifically, the story is Google getting over itself organizationally rather than technically. Better bridges are the missing ingredient.

---

## Overhyped vs. Underhyped

### Overhyped: Agent Frameworks

[[themes/agent_systems|Agent frameworks]] are seen as overhyped because the underlying workloads are in too much flux to justify stable abstractions. LangChain executed well on velocity — shipping constantly to stay relevant — but the market may now want something to actually build on for multiple years. Mastra on the TypeScript side is gaining traction and represents a real opportunity, but the fundamental critique holds: it may simply be too early for frameworks.

The more useful analogy: we're in the jQuery era of agents. jQuery was valuable and widely adopted but preceded the React-equivalent higher-order abstraction. The field may need to wait for that React moment.

### Underhyped: MCP as Protocol

MCP (Model Context Protocol) reframes the right unit of abstraction: protocol rather than framework. Frameworks embed protocols; focusing on the protocol layer alone is more durable. The analogy is XMLHttpRequest — the thing that enabled AJAX, which enabled the popularity of JavaScript as a language. MCP as the current protocol leader may occupy a similarly foundational role.

### Underhyped: Vertical Foundation Models with Unique Data

While the general LLM agent space is dominated by well-resourced labs, there remains genuine opportunity in foundation models for domains with unique, proprietary datasets: robotics, biology, materials science. These differ structurally from "vertical LLMs" that merely fine-tune general models — the key is irreplaceable data with specific inductive structure.

Fine-tuning as a standalone service, however, is a [[themes/startup_and_investment|startup]] failure mode: the market has repeatedly shown it doesn't sustain as a business and must be wrapped in broader enterprise AI services.

### New Model Training Companies

A surprising number of new model training companies have re-emerged after the apparent die-off at the end of 2024. The skeptical view: test-time compute may eventually allow models to automate the next algorithmic breakthrough themselves, potentially obsoleting the rationale for new entrants. The more sympathetic view: labs are moving up the stack into product (Deep Research, Operator), creating downstream openings for vertical model specialists.

---

## Structural Tensions to Watch

**Anthropic ↔ Cursor:** Anthropic's move toward the application layer in coding (Claude Code, agentic coding) creates latent tension with Cursor, which currently relies heavily on Anthropic models. The likely resolution: Anthropic focuses on the outer-loop coding agent (between git commits, cloud-orchestrated), while Cursor retains the inner-loop IDE experience. Cursor will likely diversify model providers to reduce dependency.

**RL in non-verifiable domains:** RL-based agents have clear traction in verifiable domains (code, math, formal systems). The unresolved question is whether reward learning can be made tractable for law, sales, and other domains where correctness is subjective. This is a [[themes/agent_systems|fundamental bottleneck]] on agent autonomy expansion.

**Reliability scaling:** Moving from 90% to 99% reliability requires an order-of-magnitude compute increase; 99% to 99.9% requires another. This recurs every 2–3 years. The implication: high-reliability autonomous systems face a structural cost constraint that compounds, not eases, over time.

**Agent authentication:** No standardized mechanism exists for an agent to prove it acted on behalf of a user rather than the user acting directly. This is a blocking bottleneck for agent-driven automation of external systems at scale.

---

## Open Questions

- Will DeepSeek continue open-sourcing models, or does the cost-to-benefit analysis eventually flip?
- Can RL-based reward learning generalize beyond verifiable domains to law, sales, or creative judgment?
- Is there a "React moment" for agent frameworks, or does MCP-as-protocol make monolithic frameworks permanently obsolete?
- Will Google consolidate its fragmented developer platform before the perception gap closes — or does mindshare lag capability for long enough to matter?
- Can specialized foundation models in biology/robotics/materials sustain competitive advantage as general models continue improving?

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/frontier_lab_competition|Frontier Lab Competition]]
- [[themes/startup_and_investment|Startup and Investment]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/apple-intelligence|Apple Intelligence]]
- [[entities/cursor|Cursor]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/pre-training-scaling|Pre-training Scaling]]
- [[entities/pre-training-scaling|Pre-training scaling]]
- [[entities/sierra|Sierra]]
