---
type: source
title: 'Pricing in the AI Era: From Inputs to Outcomes, with Paid CEO Manny Medina'
source_id: 01KJVSP7HTV1W80HD21RED09GC
source_type: video
authors: []
published_at: '2025-04-22 00:00:00'
theme_ids:
- ai_business_and_economics
- ai_pricing_and_business_models
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Pricing in the AI Era: From Inputs to Outcomes, with Paid CEO Manny Medina

A practitioner-level analysis of what is working in AI applications as of early 2025, with particular focus on which market niches are gaining traction, which are not yet ready, and how AI companies should think about pricing models. Manny Medina, CEO of Paid (an AI pricing infrastructure company), draws on direct observation of early-stage AI app companies to argue that narrow specialization and value-aligned pricing are the two defining success factors of this moment.

**Authors:** Manny Medina
**Published:** 2025-04-22
**Type:** Video

---

## The Hedgehog Principle: Narrow Beats Broad

The clearest pattern across commercially successful AI apps is extreme specialization. Rather than building broad platforms, winning companies identify a single, well-bounded problem and become the best solution for that one thing. Medina frames this as the hedgehog strategy: one big idea, executed deeply.

The characteristics of problems that fit this mold:

- **High aggregate volume** — the problem seems small but occurs at massive scale
- **No existing software solution** — typically handled manually or via BPO
- **Clear labor displacement** — the AI does something a human was doing, not something a human couldn't do

Concrete examples:

- **Quandri** — insurance policy renewals
- **Owl** — insurance claims data review
- **HappyRobot** — phone-based freight negotiation between brokers and truckers (up to 2,000 simultaneous agents)
- **XBOW** — continuous automated penetration testing, providing a capability that previously didn't exist at this scale

The pentesting case is instructive: XBOW didn't just automate an existing workflow — it made continuous pentesting tractable for the first time, replacing periodic agency engagements with always-on coverage. This is a capability expansion, not just a labor substitution.

> "if you take up a very narrow problem and then you hedgehog into it and you become the best at that one thing that is printing money right now"

---

## What Isn't Working Yet

Medina is careful to distinguish "not working" from "not working *yet*." Two categories of products show why breadth is the enemy of traction:

**AI SDRs** — the category is too loosely defined. Different buyers mean different things by "AI SDR," creating fragmented demand and pricing confusion. Companies in this space struggle to land clear value propositions.

**AI executive assistants** — highly desirable in theory, but current products break down under real-world complexity. Handling multiple time zones, multiple business lines, and ambiguous scheduling constraints remains beyond current capability. Products like Fixer work well only in narrow, repetitive configurations (e.g., a real estate broker with a fixed routine).

> "I have three time zones that I work through... like getting that to work out just right doesn't quite work for me"

These aren't product failures — they are timing failures. The underlying need is real; the systems aren't yet reliable enough for the full scope of the problem.

See also: [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]] for the broader pattern of vertical focus as a competitive moat.

---

## Market Transformation: Who Gets Disrupted First

### The High-Paying Jobs Hypothesis — and Its Limits

A common view holds that AI will first attack the highest-paying jobs because that's where the economic incentive is greatest. Medina contests this. The competitive dynamics cut against it: high-paying markets attract every major AI lab and well-funded startup simultaneously, making it nearly impossible for individual companies to establish dominance.

### The BPO Replacement Thesis

A more durable pattern is AI targeting **labor pools that nobody else wants to manage**: high-turnover roles, hard-to-backfill positions, and tasks currently outsourced to BPOs. The presence of a BPO is a reliable signal that a task is ripe for agent replacement.

> "the companies that are doing really well are addressing pools of labor that are either disappearing because of retirement or are typically handled by BPOs"

The economics of BPO replacement are favorable: the upper bound on pricing is the BPO contract cost; the lower bound is the AI company's margin. The customer comparison is clear, and pricing power follows.

### The Two-Mode Model

Both hypotheses have merit in different contexts:

| Mode | Target Market | AI Role | Examples |
|---|---|---|---|
| Co-pilot | Higher-paying, creative work | Augments expert | Harvey (legal), Open Evidence (medicine) |
| Autopilot | Lower-paying, repetitive work | Replaces labor | HappyRobot, Quandri, XBOW |

The co-pilot market is real but structurally harder. Value is difficult to demonstrate and differentiate — one legal AI copilot looks like another to a buyer. The path through this is vertical depth (a legal AI specializing purely in patent law), which loops back to the hedgehog principle.

Collaborative workflow moats — historically durable in SaaS — are under pressure from vibe coding and accelerated development cycles, making it easier for competitors to replicate embedded workflows than it once was.

---

## Pricing Models: Four That Are Working

Medina identifies four pricing structures demonstrating commercial success in AI applications, with a clear directional argument about where companies should aim.

### 1. Activity-Based Pricing

Charging per token, credit, or discrete action. Easiest to sell because it's transparent and maps directly to usage. But:

> "if you don't move out of that bottom one which is easy to sell, you'll get competed out"

Activity-based pricing commoditizes AI companies. As models become cheaper, per-unit pricing erodes margins. It also anchors the conversation to inputs rather than value.

### 2. Workflow-Based Pricing

Charging for a complete sequence of activities — a full document review, a complete policy renewal, an end-to-end freight booking. This moves pricing toward value by bundling activities into meaningful units of work, and allows pricing to flex with complexity (e.g., longer documents cost more).

This is where most mature AI companies should be operating today.

### 3. Outcome-Based Pricing

Charging when a specific, measurable result is achieved (e.g., a meeting booked, a policy renewed, a vulnerability found). Medina's preferred structure is a hybrid: **base fee + outcome bonus**, which preserves revenue predictability while opening a value-alignment conversation with the buyer.

> "charge instead of charging per outcome, get an outcome bonus"

The outcome bonus framing is strategically important: it's easier to get a customer to agree to a bonus for results than to shift entirely to pure outcome pricing, which requires both parties to define and measure outcomes precisely.

### 4. Per-Agent Pricing

Pricing AI agents as headcount — an annual fee per agent, analogous to a fully-loaded employee cost. For AI SDR agents, the comparison is explicit: ~$20,000/agent/year versus $70,000–$90,000 for a human SDR.

The strategic advantage of per-agent pricing is **budget routing**: it moves the purchase out of the RevOps/tools budget and into the HR/headcount budget, which is typically larger and governed by different buyers.

> "You're not in the RevOps purview in terms of like where my budget is coming from. You're in the headcount side of the house"

---

## Limitations and Open Questions

### Cascading Hallucinations in Agentic Chains

The most technically acute limitation: a hallucination at step one of a multi-step agentic workflow corrupts all downstream steps. Long agentic chains have no error recovery from early misclassification or bad extraction. This is a **blocking constraint** for complex autonomous workflows.

> "if you have a hallucination at the very beginning of that chain, you're screwed"

Current workaround: keep chains short, validate at boundaries, and design workflows to catch errors before they propagate. Not yet a solved problem. See: AI Reasoning and Planning.

### Margin Opacity in Agent Systems

AI companies typically cannot attribute costs to specific customers or agents. LLM tokens pass through orchestration frameworks that aggregate costs, making per-customer margin calculation impossible without significant instrumentation.

> "You don't know what customer is profitable to you, what customer is negatively impacting your margins"

This is acute for multi-modal agents, where costs extend beyond inference: phone minutes, TTS, speech recognition, and avatar hosting compound in ways that are not yet predictable at pricing time.

### Inference Cost Trajectory for Reasoning Models

Input token costs have dropped dramatically, but inference-time compute for reasoning-heavy models may be going the other direction. For agents that require deep reasoning, the cost curve may worsen before it improves — a concern for companies that have priced on assumptions of continued deflation.

### The 'Vibe Revenue' Problem

Most AI agent deployments in 2025 are still in trial or mandate-driven adoption phases. Companies bought AI tools because they had to, not because they renewed based on demonstrated value. True renewal viability — whether these deployments stick when the mandate pressure fades — is unknown.

> "every company in the planet got an AI mandate... They bought it and they bought it"

This creates a hidden risk in ARR figures: revenue that looks like product-market fit may be mandate-driven spend that doesn't renew.

---

## Connections

- [[themes/ai_business_and_economics|AI Business and Economics]] — pricing models, margin structure, unit economics
- [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]] — the four pricing modes in detail
- [[themes/startup_and_investment|Startup and Investment]] — what investors and founders should look for in AI app companies
- [[themes/startup_formation_and_gtm|Startup Formation and GTM]] — BPO targeting as a GTM signal; hedgehog strategy for early traction
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]] — how narrow AI apps undercut and replace existing SaaS and BPO vendors

## Key Concepts

- [[entities/harvey|Harvey]]
- [[entities/outcome-based-pricing|Outcome-Based Pricing]]
- [[entities/perplexity|Perplexity]]
- [[entities/sierra|Sierra]]
- [[entities/vibe-coding|Vibe Coding]]
