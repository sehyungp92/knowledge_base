---
type: source
title: 'RIP to RPA: How AI Makes Operations Work'
source_id: 01KJVV469S2T4WJESN0K6D3NAD
source_type: video
authors: []
published_at: '2024-12-20 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- computer_use_and_gui_agents
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# RIP to RPA: How AI Makes Operations Work

A venture capital perspective on why AI agents are replacing Robotic Process Automation (RPA) in back-office workflows. Using healthcare referral management as a case study, the source argues that LLMs unlock automation of the "long tail" of edge cases that made RPA brittle — and that this opens a TAM far larger than existing software incumbents suggest, because the real competition is labor budgets, not software budgets.

**Authors:** (Unsourced — VC podcast/video)
**Published:** 2024-12-20
**Type:** video

---

## What RPA Was and Why It Failed

Robotic Process Automation automated manual business tasks — data entry, invoice processing, referral management — by recording and replaying human clicks. The approach was fundamentally deterministic: a bot would be programmed by an implementation consultant who sat beside a worker and mapped every click into a script.

This worked on the routine case but shattered on variation. A misspelled name, a website that moved its sign-in box, an unexpected form field — any deviation broke the process. The practical result was a persistent 80/20 failure: RPA handled ~80% of task volume reliably but the remaining 20% still required a human to intervene. For full-cycle automation, that residual failure rate was blocking.

> "RPA is often very good for doing like 80% of the task but then like 20% of the time that it fails it's still a manual person who has to come in."

This is a [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]] story at its root: the reason legacy industries have large labor budgets alongside small software budgets is precisely because no prior software could handle the long tail of edge cases embedded in real workflows.

---

## The LLM Unlock

[[themes/agent_systems|AI Agent Systems]] based on LLMs change the failure mode. Rather than deterministic click-replay, agents can:

- Parse unstructured inputs (faxes, voice calls, PDFs, variable form layouts)
- Collect contextual information intelligently and determine the best action
- Handle variation through reasoning rather than brittle rule-matching

The source frames this as replacing the entire RPA category rather than incrementally improving it — hence the title.

> "With AI and LLMs now, because they're able to process such unstructured data and they're able to intelligently collect context and then figure out what the best course of action is, the next generation of actually automating these back office tasks should be the intelligent AI agents instead."

The enabling infrastructure comes from large labs rather than automation startups themselves. Specifically cited: [[entities/anthropic|Anthropic]]'s Computer Use (a browser agent capable of semantically understanding and interacting with any desktop environment) and OpenAI's forthcoming "Operator" product. Intelligent automation startups are expected to build on top of these capabilities rather than conducting fundamental research.

---

## Case Study: Tenor and Healthcare Referral Management

The concrete example is Tenor, a portfolio company automating healthcare referral management — the process by which a primary physician refers a patient to a specialist.

**The pre-automation workflow:**
1. Physician writes referral on paper, faxes it to specialist
2. Front-desk administrator receives fax, manually reads it
3. Administrator inputs data into the specialist's system
4. Administrator checks insurance policies and prior patient history
5. Administrator decides whether to accept the referral

This workflow had enough complexity — unstructured fax inputs, insurance verification, cross-system data entry, judgment calls — that RPA couldn't reliably handle it. It required a human administrator throughout.

**Tenor's solution:**
- Drag-and-drop UI that feels self-serve to the healthcare practice
- Significant engineering complexity hidden under the hood: system integrations, insurance verification, data extraction
- No implementation consultant required — practices configure their own automation flows
- End-to-end automation of the referral lifecycle

This illustrates the [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]] thesis in production: the value isn't just that the agent can click, it's that it can reason about what to do given messy, real-world inputs.

---

## Capabilities

| Capability | Maturity | Evidence |
|---|---|---|
| Browser/desktop agents with semantic understanding of UI environments | Demo | Anthropic Computer Use announcement |
| Domain-specific workflow automation (healthcare referral end-to-end) | Narrow production | Tenor deployment |
| Unstructured data extraction from documents, audio, faxes | Narrow production | "Almost every intelligent automation path starts with some messy unstructured data" |
| Voice order processing with intelligent parsing and system integration | Demo | Voice-to-system order capture use case |

These capabilities position [[themes/agent_systems|agent systems]] as genuinely production-ready in narrow, well-scoped domains — not merely theoretical.

---

## Limitations and Open Questions

Several constraints bound the current state of intelligent automation:

**Technical limitations:**
- **Edge case handling** is still imperfect — hallucinations in LLMs remain a significant deployment concern, and the source doesn't fully resolve how agents handle adversarial or truly novel inputs (severity: significant, trajectory: improving)
- **Browser agents are not yet fully reliable at scale** — additional engineering is required to move from demo to production-scale deployment (severity: significant, trajectory: improving)
- **Scope must be narrow to start** — intelligent automation currently works best constrained to one specific, repeated, industry-specific workflow; broad multi-flow, multi-industry automation is not yet viable (severity: significant, trajectory: improving)

> "There's still tech that needs to be done to make a browser agent fully work at scale."

**Adoption limitations:**
- **Customer knowledge gap** — buyers don't yet understand what agents can and cannot do, creating friction in sales and deployment (severity: minor, trajectory: improving)
- **On-premises and legacy industry adoption** will be slow — organizational change management and technical integration are harder in less tech-savvy environments (severity: minor, trajectory: improving)
- **Hidden integration complexity** — despite self-serve UIs, each deployment requires deep integration with industry-specific systems, constraining how quickly vendors can expand to new verticals (severity: minor, trajectory: stable)

The 80/20 failure problem of RPA hasn't been fully solved — it's been substantially improved. The open question is whether hallucination rates and edge-case failures in LLM-based systems can be brought low enough for workflows where errors have real consequences (healthcare decisions, financial transactions).

---

## Bottlenecks

Three bottlenecks are identified as currently blocking the full promise of intelligent automation:

1. **Edge case reliability** — Full end-to-end automation of complex, variable workflows still requires ~20% human fallback. Resolving this requires both better models and better system design around uncertainty. Horizon: 1–2 years.

2. **Browser/computer use agents at scale** — Current browser agents work in demos and constrained settings but aren't yet production-ready for high-volume, multi-environment deployment. Horizon: 1–2 years.

3. **Industry-specific integration depth** — Each new vertical requires significant engineering investment in system integrations, data formats, and business context — blocking rapid horizontal scaling. Horizon: 1–2 years.

---

## Market Framing: Labor Budgets, Not Software Budgets

A recurring analytical point concerns how to size the opportunity. The conventional approach — comparing intelligent automation startups to legacy software incumbents in a given industry — systematically underestimates the TAM.

> "I think it's actually like a false comparison to look at the historical software incumbent and say that's the market size."

The actual competition is labor. Many legacy industries have large labor budgets allocated to tasks that existing software couldn't automate. Intelligent automation directly displaces that labor spend. This reframing is central to the [[themes/ai_business_and_economics|AI Business & Economics]] thesis for vertical automation.

Especially attractive: **revenue-generating flows** where the customer was previously capacity-constrained by the manual process. Automating these flows doesn't just reduce cost — it removes a ceiling on the customer's revenue, making ROI immediate and compelling.

---

## Go-to-Market Pattern

The recommended [[themes/startup_formation_and_gtm|startup GTM]] approach:

1. **Start with one workflow** — pick the most-repeated, highest-pain, most-measurable flow in a specific industry
2. **Nail it completely** — integrate deeply into all relevant systems, build around the specific constraints of that workflow
3. **Expand from the wedge** — once trust and integration are established, move into adjacent flows and deepen the automation footprint

This contrasts with attempting broad multi-flow automation from day one, which the source argues fails because the constraints are too diffuse to engineer around reliably.

---

## Trajectory

The 5–10 year view: continued deepening as customers become more comfortable with agents, as browser agent infrastructure matures from large labs, and as vertical vendors expand from narrow wedge workflows to broader core business processes. The bottleneck is trust and technical reliability, not fundamental capability — the source positions the underlying LLM and computer use capabilities as already sufficient for narrow production use.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business & Economics]]
- [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]
- [[themes/startup_and_investment|Startup & Investment]]
- [[themes/startup_formation_and_gtm|Startup Formation & GTM]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]

## Key Concepts

- [[entities/computer-use|Computer Use]]
- [[entities/openai-operator|OpenAI Operator]]
- [[entities/operator|Operator]]
