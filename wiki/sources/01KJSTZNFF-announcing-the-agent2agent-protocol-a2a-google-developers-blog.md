---
type: source
title: Announcing the Agent2Agent Protocol (A2A)- Google Developers Blog
source_id: 01KJSTZNFF8H4ZJWZXYCNZ3BXY
source_type: article
authors: []
published_at: '2025-04-09 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- multi_agent_coordination
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Announcing the Agent2Agent Protocol (A2A)- Google Developers Blog

**Authors:** 
**Published:** 2025-04-09 00:00:00
**Type:** article

## Analysis

# Announcing the Agent2Agent Protocol (A2A)- Google Developers Blog
2025-04-09 · article
https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/

---

## Briefing

**Google has launched A2A (Agent2Agent), an open protocol enabling AI agents from different vendors and frameworks to discover each other, exchange tasks, and coordinate actions across enterprise systems — addressing the fundamental interoperability gap that currently limits multi-agent productivity gains to single-vendor silos. With 50+ partners spanning major enterprise software platforms (Salesforce, SAP, ServiceNow, Workday) and consulting firms (McKinsey, Deloitte, Accenture, PwC), A2A represents a serious industry-level push to establish a universal agent communication standard. The economic and structural implication is significant: if successful, A2A commoditizes agent orchestration logic and shifts competitive value toward specialized agent capabilities, accelerating SaaS disruption by making cross-system workflow automation vendor-agnostic.**

### Key Takeaways
1. **Agent interoperability unlocks compound productivity** — Single-agent automation is limited; the real productivity multiplier requires agents to hand off, coordinate, and negotiate across system boundaries, which A2A is explicitly designed to enable.
2. **A2A is a complement to MCP, not a replacement** — Anthropic's Model Context Protocol provides tools and context to individual agents; A2A operates at the inter-agent communication layer, meaning these standards are composable.
3. **"Agent Card" enables dynamic capability discovery** — Agents advertise capabilities in JSON format, allowing client agents to identify the best available remote agent for a given task without pre-hardcoded integration.
4. **Long-running tasks are a first-class design concern** — The protocol explicitly supports tasks that span hours or days, including human-in-the-loop checkpoints with real-time status notifications — not just synchronous request/response.
5. **Built on boring infrastructure intentionally** — HTTP, SSE, and JSON-RPC were chosen over novel transport layers to minimize integration friction with existing enterprise IT stacks.
6. **Modality-agnostic from launch** — A2A supports audio and video streaming alongside text, signaling that enterprise agentic workflows are expected to involve richer interaction types than current LLM interfaces suggest.
7. **Enterprise-grade security as a baseline** — Authentication and authorization are designed to match OpenAPI schemes at launch, a deliberate signal to enterprise buyers who require compliance and auditability.
8. **The partner list encodes a platform land-grab** — Salesforce, SAP, ServiceNow, Workday, and Intuit all signed on at launch, meaning A2A may become the default inter-agent bus across the dominant ERP/CRM/HCM landscape.
9. **Consulting firms as distribution vector** — The inclusion of Accenture, BCG, Deloitte, McKinsey, PwC, TCS, Wipro, and others signals that A2A adoption will be pushed through enterprise transformation engagements, not just developer adoption.
10. **SaaS disruption framing is explicit in partner quotes** — Multiple partners describe A2A as enabling "breaking down silos," "cross-platform agents," and replacing "disconnected capabilities" — language that implies existing software integration layers (iPaaS, middleware) are being targeted.
11. **Agent-to-agent commerce as emergent pattern** — Supertab's quote specifically mentions agents paying for and charging for services, hinting at an economic layer where agents transact autonomously — a structural shift beyond task automation.
12. **Production readiness is pending** — The protocol launched as a draft specification; a production-ready version is targeted for later in 2025, meaning the partner ecosystem is committing to a work-in-progress standard.

---

### Protocol Architecture: How A2A Actually Works

- **The fundamental abstraction is a client/remote agent pair with a task lifecycle.** The client agent formulates and communicates tasks; the remote agent executes them and returns artifacts — creating a clean separation between orchestration and execution.
  - This mirrors HTTP's client/server model at the agent layer, which is likely intentional for developer familiarity and tooling reuse.
  - The "artifact" abstraction formalizes task outputs as structured, transferable objects rather than raw text responses.

- **Capability discovery via "Agent Card"** allows agents to dynamically discover what other agents can do without pre-built integrations.
  - Agent Cards are JSON-formatted advertisements of capabilities, consumable by client agents at runtime.
  - This enables a marketplace-like dynamic where the best available agent for a task can be selected on-the-fly, rather than requiring hardcoded routing logic.

- **Task management is stateful and lifecycle-aware.** Tasks can be completed immediately or tracked over extended periods, with agents maintaining synchronization on status throughout.
  - Long-running tasks receive real-time feedback, notifications, and state updates — addressing a gap in current LLM APIs which are fundamentally stateless.
  - This is architecturally significant for enterprise workflows where processes like background checks, procurement approvals, or regulatory submissions cannot complete in a single API call.

- **The "parts" model in messages enables UX negotiation.** Each message contains "parts" — fully formed content pieces with explicit content types — allowing agents to negotiate output format based on the user's UI capabilities.
  - Supported negotiation targets include iframes, video, web forms, and other rich UI elements.
  - **This is a meaningful departure from current agent interfaces**, which typically force all output through text regardless of richer possibilities.

- **Collaboration primitives include context passing, replies, artifact sharing, and user instruction forwardin

## Key Claims

1. A2A allows AI agents to communicate with each other, securely exchange information, and coordinate actions across enterprise platforms, regardless of the underlying vendor or framework.
2. A2A is designed to complement Anthropic's Model Context Protocol (MCP), which provides tools and context to agents, rather than replace it.
3. A2A is built on existing web standards including HTTP, SSE, and JSON-RPC to ease integration with existing enterprise IT stacks.
4. A2A supports enterprise-grade authentication and authorization with parity to OpenAPI's authentication schemes.
5. A2A supports long-running tasks ranging from quick tasks to deep research taking hours or days, with real-time feedback and state updates throughout.
6. A2A supports multiple modalities beyond text, including audio and video streaming.
7. A2A uses an 'Agent Card' in JSON format for capability discovery, allowing client agents to identify the best remote agent for a task.
8. A2A defines a 'task' object with a full lifecycle; tasks can complete immediately or persist as long-running jobs with ongoing status synchronization between agents.
9. A2A enables user experience negotiation between agents, allowing client and remote agents to agree on content formats including iframes, video, and web forms.
10. Enterprises are currently building and deploying autonomous agents to automate processes such as ordering hardware, aiding customer service, and assisting in supply chain planning.

## Capabilities

- AI agents can advertise their capabilities via a structured 'Agent Card' JSON format, allowing client agents to dynamically discover the best remote agent for a task at runtime across vendor boundaries
- Cross-vendor AI agents can exchange structured task objects with full lifecycle tracking — creation, in-progress updates, completion, and artifact delivery — regardless of the underlying framework or vendor
- Multi-agent systems can coordinate long-running tasks spanning hours or days with real-time notifications and state updates pushed to human operators throughout execution
- Agent-to-agent communication channels can carry multi-modal content — including audio and video streaming — not just text, enabling richer inter-agent collaboration pipelines
- Standardized user experience negotiation between client and remote agents allows dynamic format selection (iframes, video, web forms) based on the user's actual UI capabilities, enabling richer agent-mediated interfaces

## Limitations

- A2A provides a communication channel between agents but does not solve shared memory, shared tools, or shared context — agents collaborating via A2A remain fundamentally isolated cognitive units
- The A2A protocol is still a draft specification; a production-ready version is not expected until later in 2025, meaning enterprise deployments cannot yet rely on a stable, finalized standard
- Long-running cross-agent tasks still implicitly require humans in the loop — full autonomous multi-day agent collaboration without human supervision is not demonstrated or claimed
- No security model is specified for preventing adversarial agent impersonation, prompt injection via crafted Agent Cards, or malicious task hijacking between agents — the conspicuous absence of adversarial threat modeling is a major gap for enterprise deployments
- Cross-agent data access remains siloed — A2A provides message routing but does not give agents access to each other's underlying data stores, meaning the fundamental enterprise data fragmentation problem is unresolved
- Actual interoperability quality depends entirely on per-vendor A2A implementation fidelity — a shared protocol specification does not guarantee that 50+ partner implementations are semantically compatible or reliably interoperable in practice
- No mention of pricing, token cost, or latency implications of adding an A2A routing layer to multi-agent pipelines — the overhead of cross-vendor agent coordination via a protocol layer is uncharacterized

## Bottlenecks

- Cross-vendor agent interoperability has had no open standard — agents from different frameworks (LangChain, SAP, Salesforce, ServiceNow) cannot coordinate tasks without expensive bespoke integrations, blocking compound multi-agent enterprise automation
- Adoption critical mass is required before A2A delivers on its interoperability promise — a standard with 50 launch partners is not yet a standard that is broadly implemented, tested, and stable across the ecosystem

## Breakthroughs

- Google launched A2A — the first open, broadly-backed industry protocol for agent-to-agent communication — with 50+ major technology and services partners at launch, establishing a coordination layer that makes cross-vendor multi-agent systems architecturally tractable for enterprises

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/multi-agent-system|Multi-Agent System]]
