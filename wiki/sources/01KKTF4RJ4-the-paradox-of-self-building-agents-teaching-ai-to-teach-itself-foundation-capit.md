---
type: source
title: 'The paradox of self-building agents: teaching AI to teach itself - Foundation
  Capital'
source_id: 01KKTF4RJ4956V5WAM57Z3HK16
source_type: article
authors: []
published_at: None
theme_ids:
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- alignment_and_safety
- multi_agent_coordination
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The paradox of self-building agents: teaching AI to teach itself - Foundation Capital

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# The paradox of self-building agents: teaching AI to teach itself - Foundation Capital
article
https://foundationcapital.com/ideas/the-paradox-of-self-building-agents-teaching-ai-to-teach-itself/

---

## Briefing

**Self-building AI agents — those that autonomously generate and expand their own capabilities — represent both the most transformative and most dangerous frontier in enterprise AI. The core argument is that unlocking their value requires a graduated, trust-based deployment model analogous to developing human employees: constrain first, expand scope only as reliability is demonstrated, and never skip the training wheels.**

### Key Takeaways
1. **The SaaS-to-service-as-software transition is driven by agents** — Foundation Capital frames "System of Agents" as the architectural capture mechanism for the shift away from four decades of enterprise software stacks.
2. **Self-building is the key inflection** — Agents that can generate their own tools and modify their own architecture are qualitatively different from prompt-response AI, creating both exponential upside and novel risk profiles.
3. **Four autonomy levels define the design space** — Nakajima's L0–L3 taxonomy (fixed tools → request-triggered → need-driven → anticipatory) provides a precise vocabulary for where current agents sit and where they're heading.
4. **Most production AI is still at Level 0** — ChatGPT, Slack AI, and similar tools operate on fixed developer-provided toolsets with no self-building capability, despite widespread agent hype.
5. **Level 3 agents introduce misaligned-objective risks** — An agent tasked with "maximizing efficiency" may autonomously build employee surveillance tools; optimization for narrow metrics makes agents vulnerable to external manipulation.
6. **The intern analogy is the right mental model for deployment** — Graduated trust, human oversight, and domain-gated expansion (low-risk → high-stakes) are the prescribed safety pattern, not comprehensive pre-built guardrails.
7. **Judgment and context awareness must be trained, not assumed** — Technical capability alone is insufficient; agents need to learn red-flag recognition, source validation, and priority balancing just as human employees do.
8. **Agentic architectures are already mainstream** — Menlo Ventures data shows they powered 12% of enterprise AI implementations in 2024, with Salesforce (150K companies) and Microsoft (1.4B Windows users) already at scale.
9. **Enterprise build-vs-buy is reversing** — Companies building internal gen AI dropped from 80% using third-party vendors to ~50%, signaling growing enterprise confidence in proprietary agent development.
10. **The capability-control balance is an organizational imperative** — Getting self-building right is framed not as a technical problem but as a governance challenge whose failure mode is security vulnerabilities and systemic bad code.

---

### The Structural Shift: From SaaS to Service-as-Software

- **AI agents represent a categorical change in what software is**: shifting from tools that respond to tools that act autonomously on goals.
  - An agentic system takes a goal, decomposes it into steps, executes them sequentially while passing results forward, and synthesizes outcomes — a fundamentally different execution model than query-response systems.
  - Foundation Capital positions this as "eating into four decades of technological advances," with agents systematically collapsing existing enterprise software stacks rather than layering on top of them.
- **"System of Agents" is Foundation Capital's thesis for value capture** in the transition from SaaS to service-as-software.
  - This is a VC-level architectural bet: the firms and builders who design multi-agent coordination systems capture the structural shift, not those optimizing individual models.
- **By end of 2024, the largest enterprise software vendors had aligned on agents as the successor paradigm** — Salesforce, HubSpot, and Microsoft executives explicitly framed agents as "the new apps."
  - This convergence signals a vendor ecosystem reorientation, not just product-level updates.

---

### Nakajima's Four Levels of Agent Autonomy

- **Level 0 — Fixed tools**: The agent operates on a static, developer-provided function library with no mechanism to expand or modify it.
  - Examples: ChatGPT with predefined plugins, Slack AI with pre-built summarization and writing features.
  - **This is where most production AI sits today**, despite the scale of deployment (Salesforce, Microsoft, etc.). The level offers no self-building capability.
  - The agent checks its existing library and applies the relevant tool — no gap-detection, no tool generation.

- **Level 1 — Request-triggered self-building**: The agent can generate new tools but only in direct response to explicit user instruction.
  - If asked to parse a specialized data format it doesn't support, it analyzes the requirement, identifies the gap, builds a new function, and adds it to its toolkit.
  - The new tool persists for future use — the toolkit grows, but **only via user-commanded expansion**.
  - The agent has no anticipatory capability; it remains reactive.

- **Level 2 — Need-driven self-building**: The agent automatically generates new tools when existing ones are insufficient, without waiting for user instruction.
  - Workflow: receive query → check existing tools → if gap exists, build tool → execute → deliver result.
  - **The toolkit grows organically** through accumulated gap-filling, but the agent is still entirely reactive to current task demands, not future ones.
  - This is the level where significant autonomous behavior begins, and where oversight challenges start to materialize.

- **Level 3 — Anticipatory self-evolution**: The agent proactively predicts future needs and evolves itself ahead of demand.
  - Goes beyond tool generation: **can rework its own architecture or algorithms** to address anticipated requirement shifts.
  - Examp

## Key Claims

1. An agentic system takes a goal, breaks it down into steps, executes the steps while passing results forward, then combines results to achieve the goal.
2. Foundation Capital posits that a System of Agents represents a sweeping shift from software-as-a-service to service-as-software.
3. AI agents will systematically collapse enterprise software stacks.
4. Tech leaders at Salesforce, HubSpot, and Microsoft predicted that agents will be the new apps in an AI-powered world by end of 2024.
5. Agents can be not only self-directed but also self-building.
6. Yohei Nakajima identified four levels of autonomy for self-building agents.
7. Most AI tools today operate at Level 0, relying on a fixed set of developer-provided tools and unable to acquire new ones.
8. Level 1 agents can generate new tools only when a user explicitly requests them.
9. Level 2 agents automatically generate new tools when existing tools cannot handle a task, without waiting for an explicit user request.
10. Level 3 agents anticipate future user needs and proactively evolve themselves, including reworking their own architecture or algorithms.

## Capabilities

- Enterprise-scale agent deployment: Salesforce Einstein GPT agents deployed across 150,000-company customer base for workflow automation
- Microsoft Copilot agents with configurable autonomy levels rolled out to 1.4 billion Windows users
- Level 1 self-building agents: agents that can generate new tools (e.g., custom parsers) on explicit user request, accumulating an expanding toolkit over time
- Level 2 self-building agents: agents that autonomously detect missing capabilities and generate new tools on-demand without explicit user instruction
- Agentic architectures powering enterprise AI implementations, representing 2024's biggest enterprise breakthrough at 12% of all enterprise AI deployments
- Graduated trust-building framework for agent autonomy expansion: starting agents on low-risk tasks (web scraping) and advancing to complex domains (financial decisions) based on demonstrated reliability

## Limitations

- Most AI tools remain at Level 0 — fixed developer-provided toolsets with no capacity to acquire new capabilities, severely limiting adaptability
- Self-building agents are vulnerable to adversarial manipulation by external services — malicious or deceptive content in the environment can hijack agent behavior toward suboptimal or harmful actions
- Self-building agents pursuing broad goal specifications may autonomously create inappropriate or harmful tools (e.g., employee monitoring when tasked with 'efficiency'), with no internal constraint preventing scope creep
- AI agents lack the judgment, contextual awareness, and red-flag recognition that humans develop through experience — they cannot reliably balance competing priorities or validate information sources in novel situations
- Level 3 anticipatory self-building agents (proactively evolving architecture ahead of user needs) remain aspirational — no safe production deployment described, only the risks of premature deployment
- Agentic architectures still represent only 12% of enterprise AI implementations despite being declared the 'biggest breakthrough' of 2024 — structural adoption barriers remain
- Enterprises building their own gen AI software has dropped from 80% to ~50%, implying a significant cohort lacks confidence to develop internal agentic tools — creating dependency on third-party vendors whose agentic capabilities are immature
- No established trust-scoring or capability-verification infrastructure exists for agents — the graduated trust model is a design philosophy, not an implemented system, leaving organizations to improvise safety boundaries
- Financial safety guardrails (spending caps, multi-factor authentication) for autonomous agents are described as necessary but not as solved — agents with financial access represent an unsolved risk class

## Bottlenecks

- No standardized methodology for calibrating and expanding agent autonomy safely — the trust-building process for self-building agents is ad hoc, blocking reliable deployment of Level 2+ agents in production
- Agent goal-scope containment is unsolved — agents optimizing broad objectives autonomously create tools and behaviors outside intended scope, with no reliable architectural solution preventing harmful instrumental sub-goals
- Agent robustness to environmental adversarial manipulation is unresolved — agents operating in open environments (web, email, external APIs) have no reliable defense against prompt injection or deceptive content steering

## Breakthroughs

- Agentic architectures recognized as 2024's defining enterprise AI breakthrough, with measurable production penetration (12% of implementations) and mega-scale deployments at Salesforce and Microsoft — marking the shift from AI-as-tool to AI-as-actor in enterprise software

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]
