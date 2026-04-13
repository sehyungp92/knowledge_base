---
type: entity
title: Benchmark
entity_type: entity
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_for_scientific_discovery
- reasoning_and_planning
- scientific_and_medical_ai
- search_and_tree_reasoning
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0010841263713572932
staleness: 0.0
status: active
tags: []
---
# Benchmark

> Benchmark is a prominent early-stage venture capital firm operating a small, flat, equal-carry partnership model with a deliberate focus on Series A investments in enterprise software and consumer technology. Its philosophy of concentrated conviction, proactive founder engagement, and deliberate avoidance of foundation model bets distinguishes it from most of its peers at a moment when the majority of top-tier venture is flooding capital into AI infrastructure.

**Type:** entity
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/startup_and_investment|Startup and Investment]], [[themes/startup_formation_and_gtm|Startup Formation and GTM]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]], [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

---

## Overview

Benchmark operates with a partnership that has remained deliberately small and structurally flat — equal carry shared across partners including Bill Gurley, Peter Fenton, Mitch Lasky, Matt Cohler, Eric Vishria, Sarah Tavel, Miles Grimshaw, and Victor Lazarte. This structural choice is itself a thesis: that concentrated ownership of fewer, higher-conviction bets outperforms the spray-and-pray or platform-heavy models that have come to dominate large multi-stage funds.

The firm's investment philosophy extends to how its partners relate to founders. Miles Grimshaw articulates the distinction between being "founder friendly" — which he treats as a form of cheerleading — and "founder respect," which means sharing hard truths even when uncomfortable. Similarly, Grimshaw reframes the "first call" investor identity (being the person founders call first) as a reactive posture, preferring instead "first to call" — proactively initiating contact rather than waiting to be sought out. Shopify's leadership is cited as an exemplar of the truth-seeking disposition Benchmark values in founders: the ability to reverse major decisions quickly, without ego capture or desire to appear correct.

Benchmark's portfolio includes consumer fintech (Monzo, which at time of recording held accounts representing roughly one-tenth of the British population), collaboration infrastructure (Figma, characterised not as design software but as the "nexus of collaboration for digital products"), and hard tech AI plays such as Quilter.

---

## The Foundation Model Non-Bet

One of Benchmark's most publicly stated positions — articulated by Eric Vishria — is the deliberate choice not to invest in any foundation model companies. The rationale reflects a structural view of capital dynamics rather than a capability scepticism: foundation model companies are consuming enormous capital to build what Vishria characterises as some of the most rapidly depreciating assets in venture capital history. The competitive moat of a foundation model erodes as peers close the capability gap, and the capital intensity required to stay at frontier makes the return profile structurally unattractive for a Series A-focused fund that prizes capital efficiency.

This is not a general AI scepticism. Benchmark's investment in Quilter through Vishria illustrates the opposite view — that AI applied to constrained hard-tech domains, where the problem is well-defined, the incumbent tooling is genuinely brittle, and the proprietary data advantage is defensible, represents a more durable opportunity.

---

## Hard Tech AI: The Quilter Thesis

The Quilter investment (circuit board design via reinforcement learning) is a useful window into Benchmark's framework for evaluating AI applications. Several conditions made Quilter legible as an investment:

- **Supervised learning was structurally insufficient.** Publicly available circuit board data is too sparse to train a supervised model at meaningful scale; the best designs are locked inside Apple, Google, and SpaceX repositories and will never be released. This scarcity closes off the most obvious commodity AI path.
- **Reinforcement learning opens a ceiling.** Without the data ceiling of supervised learning, RL-based approaches have the opportunity to exceed human performance rather than merely approximate it — a qualitatively different investment thesis.
- **The problem is "AI and done," not co-pilot.** Quilter is framed as a case where the AI replaces the workflow rather than assisting it. Circuit board layout is deterministic enough and its quality measurable enough that full automation is the correct frame, not augmentation.
- **The founder's background closed the data gap differently.** Sergiy Nesterenko's experience designing boards at SpaceX gave him domain knowledge and network access that partially substituted for public data availability.

This cluster of conditions — data moat, RL headroom, full automation framing, founder-specific advantage — appears to represent Benchmark's template for distinguishing genuine hard-tech AI opportunities from co-pilot wrappers.

---

## Relationships

Benchmark's portfolio and partner perspectives surface across three sources: Behind The Scenes of Benchmark's Boldest Bets, Miles Grimshaw: The 5 Pillars of Venture Capital & Why Co-Pilot is an Incumbent Strategy | E1061, and Investing in AI for Hard Tech, with Eric Vishria of Benchmark and Sergiy Nesterenko of Quilter.

Notable related entities include **Quilter** (portfolio company, hard-tech AI for PCB design), **Figma** (portfolio company, collaboration infrastructure), **Monzo** (portfolio company, consumer fintech), and **Shopify** (cited as a case study in founder truth-seeking culture). The foundation model non-bet positions Benchmark in implicit contrast to funds that have made large commitments to **OpenAI**, **Anthropic**, and **Google DeepMind**.

The firm's structural philosophy — small partnership, equal carry, Series A concentration — connects thematically to broader debates in [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]] about platform funds versus conviction funds, and the tension between access-driven and judgment-driven venture models.

---

## Open Questions

The Benchmark framework raises several unresolved tensions worth tracking:

- **Where is the line between co-pilot and AI-and-done?** The Quilter classification rests on the assumption that circuit board design is automatable without ongoing human judgment. As more domains are evaluated, the criteria for that classification remain underspecified.
- **Does the foundation model non-bet age well?** The depreciation-of-assets argument is structurally sound today, but if one or two foundation model companies achieve durable platform lock-in (via distribution, not capability), the analysis inverts. The position deserves revisiting as the competitive dynamics consolidate.
- **How does the "first to call" posture scale?** Proactive sourcing is a time and attention resource. As the firm's portfolio and reputation grow, the friction of maintaining genuine proactivity — rather than replying to inbound — increases. Whether the equal-carry flat structure supports this sustainably at scale is an open question.

## Key Findings

## Limitations and Open Questions

## Sources
