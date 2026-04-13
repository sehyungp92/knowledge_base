---
type: entity
title: Services as Software
entity_type: theory
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- frontier_lab_competition
- multi_agent_coordination
- reasoning_and_planning
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0003971035908013734
staleness: 0.0
status: active
tags: []
---
# Services as Software

Services as Software is a structural shift in how professional service firms are built, wherein AI enables a services business to systematically replace human labor with automated workflows — capturing the feedback loops and domain credibility of a traditional practice while approaching the unit economics and scalability of software. The concept has attracted significant attention in 2025–2026 as the first generation of AI-native firms moves from proof-of-concept to contracted revenue, with legal tech serving as the primary proving ground.

**Type:** theory
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business & Economics]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/ai_pricing_and_business_models|AI Pricing & Business Models]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/startup_and_investment|Startup & Investment]], [[themes/startup_formation_and_gtm|Startup Formation & GTM]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]

---

## Overview

The Services as Software thesis holds that the $4.6 trillion professional services market — legal, accounting, consulting, recruiting, and adjacent domains — is structurally vulnerable to firms that embed AI directly into service delivery rather than selling AI tooling to incumbents. The core claim is that a services company can use AI to systematically automate the human labor in its own workflows, compounding operational improvements through tight feedback loops (client → output → model evaluation → process refinement) while maintaining the trust, accountability, and domain legitimacy that pure software products struggle to establish. The result is a business that bills like a firm but scales like software.

This is distinct from simply automating a SaaS product or selling AI copilots to lawyers. The defining feature is that the firm *is* the service provider — it takes on liability, employs licensed professionals, and is judged by outcomes. AI reduces the marginal cost of each unit of work; it does not eliminate the professional relationship.

---

## Key Findings

### Crosby as the Canonical Case Study

The clearest documented instantiation of this model is Crosby, an AI-first law firm focused exclusively on contract automation. Crosby's thesis is explicit: "we can automate human negotiations." It targets a well-defined, high-volume wedge — NDAs, MSAs, and DPAs — with NDAs representing the simpler end of the complexity spectrum and serving as the entry point for customer acquisition.

Several design choices at Crosby are structurally significant:

**Liability as moat.** Crosby takes malpractice insurance and accepts full legal liability for all work performed. This is not incidental — it is treated as load-bearing to the business model. The willingness to accept liability signals confidence in output quality, closes the trust gap that pure AI products face, and creates a meaningful barrier to competition from firms unwilling to assume professional risk. Legal services are what economists call a *credence good*: quality is only assessable after consumption, and often requires an expert to confirm it. Taking liability is the credibility mechanism that makes the model viable.

**Pricing against the billable hour.** Crosby bills per document rather than per hour, a deliberate inversion of the incentive structure that governs most legal work. The billable hour rewards time spent; per-document billing rewards efficiency. This pricing model only makes commercial sense if AI can drive the marginal cost of document processing well below the market rate — which is the operational bet underlying the entire firm.

**Organizational design for feedback.** Crosby physically staggers lawyer and engineer desks in an alternating pattern (lawyer–engineer–lawyer–engineer) to maximize the density of collaboration and shorten feedback cycles between legal judgment and technical implementation. This is an organizational embodiment of the feedback loop thesis: the value of Services as Software is not just AI-generated output, but the continuous refinement of AI behavior through expert review.

**Internal metrics as leading indicators.** The firm runs on two primary metrics: **TTA (Total Turnaround Time)** — time-in to time-out across all back-and-forths for a contract — and **HURT (Human Review Time)** — the total human attention required to review and approve AI output. TTA is the customer value metric; HURT is the automation efficiency metric. Together they operationalize the core tension: delivering speed to clients while systematically reducing the human labor cost per contract. A declining HURT with stable or improving TTA is the signature of the model working.

**Agent infrastructure.** Crosby has built a paralegal-level routing agent responsible for triaging and distributing incoming customer work — directly analogous to how a human paralegal routes work in a traditional firm. This is the first layer of an agent hierarchy; the expectation is that the stack deepens over time as more workflow steps become automatable.

---

## Structural Dynamics and Market Context

The $4.6T Services-as-Software opportunity framing from Foundation Capital positions this not as a niche play but as a potential wholesale restructuring of the professional services sector. The argument is that software has historically been unable to fully displace services because services require judgment, context, and accountability — precisely the properties that capable foundation models are now beginning to provide.

Foundation Capital's 2026 outlook reinforces the trajectory: as reasoning models improve and agent frameworks mature, the cost curve for automated professional work continues to fall, expanding the set of task types that can be handled without per-unit human review.

The model connects directly to several adjacent dynamics:

- **[[themes/test_time_compute_scaling|Test-time compute scaling]]** is the enabling mechanism — longer reasoning chains allow AI to handle more complex contract clauses, edge cases, and negotiation scenarios that previously required senior attorney attention.
- **[[themes/multi_agent_coordination|Multi-agent coordination]]** is the architectural path — routing agents, drafting agents, review agents, and negotiation agents operating in sequence or in parallel over a single contract workflow.
- **[[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS disruption]]** is the competitive context — established legal SaaS platforms (contract lifecycle management, e-discovery, research tools) face displacement not just from better software but from firms that have internalized the AI and compete on outcomes rather than tooling.

---

## Open Questions and Limitations

Several tensions in the model remain unresolved in the current evidence base:

**Complexity ceiling.** Crosby's wedge — NDAs, MSAs, DPAs — is deliberately chosen for its relative standardization and volume. MSAs are already acknowledged as substantially more complex than NDAs. The degree to which the automation stack generalizes to higher-stakes, more adversarial, or more jurisdiction-specific contract types is not yet demonstrated. The HURT metric may not remain flat as complexity increases.

**Liability at scale.** Accepting malpractice liability is currently a competitive differentiator, but it becomes a tail-risk accumulation problem as volume scales. The insurance market for AI-assisted legal work is nascent; pricing may shift materially as the actuarial base develops.

**Feedback loop quality.** The model's compounding advantage depends on the quality of human feedback entering the system. If legal staff are primarily approving AI output rather than actively correcting it (a natural drift under time pressure), the feedback signal degrades and the HURT metric can decline without genuine quality improvement.

**Generalization across service verticals.** Legal contracts are unusually well-structured as a domain — they are text-heavy, have established norms, and produce discrete artifacts. It is an open question whether the Services as Software model carries the same unit economics in domains with more tacit judgment (strategic consulting, complex negotiations, clinical services).

**Incumbent response.** Large law firms and legal outsourcing providers have the client relationships, the regulatory standing, and increasingly the capital to build or acquire similar capabilities. The first-mover advantage of AI-native firms depends on how quickly the automation stack can be replicated once the model is proven.

---

## Relationships

The Services as Software concept is most directly evidenced by Crosby's contract automation model, with the broader investment thesis articulated in Foundation Capital's services-as-software analysis and their 2026 outlook. It sits at the intersection of [[themes/agent_systems|agent systems]] (the multi-layer agent stack replacing human workflow steps), [[themes/ai_pricing_and_business_models|AI pricing models]] (per-document vs. per-hour), and [[themes/vertical_ai_and_saas_disruption|vertical SaaS disruption]] (outcome-based firms competing with tooling vendors). The liability-as-moat pattern distinguishes it from software products and connects it to [[themes/startup_formation_and_gtm|GTM strategy]] questions about how AI-native firms establish trust in credence-good markets.

## Limitations and Open Questions

## Sources
