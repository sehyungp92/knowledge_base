---
type: source
title: 'RIP to RPA: The Rise of Intelligent Automation | Andreessen Horowitz'
source_id: 01KJT0E4FTAR5KBJ97VSVHR5SY
source_type: article
authors: []
published_at: '2024-11-13 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# RIP to RPA: The Rise of Intelligent Automation | Andreessen Horowitz

**Authors:** 
**Published:** 2024-11-13 00:00:00
**Type:** article

## Analysis

# RIP to RPA: The Rise of Intelligent Automation | Andreessen Horowitz
2024-11-13 · article
https://a16z.com/rip-to-rpa-the-rise-of-intelligent-automation/

---

## Briefing

**LLM-powered agents can now fulfill the original promise of RPA — automating internal operations work that was too analog, bespoke, or process-variable for legacy automation — opening a $250B+ greenfield market where no software incumbents exist and the people themselves were the product.** The key strategic insight is that intelligent automation startups should target narrow, revenue-generating entry workflows in specific verticals, avoiding the system-of-record position initially to sidestep legacy displacement battles while earning rights to upstream data and downstream workflows.

### Key Takeaways
1. **Internal ops work is the underappreciated AI opportunity** — While external professional services (legal, accounting) get headlines, the "internal stitching" of organizations — data entry, document extraction, information transfer — represents an equally large and largely unaddressed automation surface.
2. **Legacy RPA failed because it mimicked, not understood** — UiPath and peers built bots that replicated exact keystrokes, which broke on any process variation and required expensive consultants, limiting deployment to large enterprises only.
3. **LLMs shift automation from deterministic scripts to goal-directed agents** — Instead of encoding every step, agents are prompted with an end goal and given tools, making them adaptable to variable inputs and process changes that would have broken legacy RPA.
4. **The addressable market spans 8M+ roles and $250B in BPO spend** — The Bureau of Labor Statistics counts over 8 million operations/information clerk roles in the US, and the broader BPO market is ~$250B — both directly in scope for intelligent automation displacement.
5. **No system-of-record incumbents means true greenfield** — Unlike sales (Salesforce) or HR (Workday), operations roles never developed software systems of record, so there is no incumbent to bolt AI onto; the entire category is open to startups.
6. **Anthropic's computer use capability is a foundational infrastructure unlock** — The ability for models to interact directly with existing software GUIs means agents can operate in legacy environments without requiring API integrations that often don't exist.
7. **Vertical specificity is a competitive moat, not a constraint** — Operational agents need narrow domain context and deep integrations to meet accuracy thresholds customers require; generic horizontal agents are insufficient for production-grade workflows.
8. **Start with revenue-generating entry workflows, not systems of record** — The winning formula is automating the first step of a revenue workflow (referral intake, order entry, load tracking) to become mission-critical while avoiding rip-and-replace friction.
9. **Horizontal enabling layers are being commoditized in real-time** — Every intelligent automation company independently building unstructured data parsing creates demand for shared infrastructure; Reducto and Extend are competing to own this layer.
10. **The strategic wedge earns rights to the full data flow** — By automating the start of a workflow, startups capture upstream data and position themselves to expand into all downstream steps, not just the initial task.

---

### Why Legacy RPA Failed: The Technology Wasn't Ready

- Traditional RPA companies like UiPath (founded 2005, IPO 2021) promised the "fully automated enterprise" but were fundamentally limited by their technological approach.
  - Their bots worked by observing human navigation of a process and then replicating the exact keystrokes and clicks — deterministic mimicry rather than understanding.
  - **This approach had a critical fragility: any deviation from the expected process caused failures.** If a UI changed, a form field moved, or a new data format appeared, the bot broke.
  - Implementation required expensive specialist consultants, creating a high cost barrier that confined RPA to large enterprises capable of absorbing the overhead.
- The result was that RPA delivered value in narrow, rigidly defined, unchanging workflows — a small fraction of actual operations work — while the rest remained manual.
- The underlying problem was not the concept of automation but the technology: pre-LLM systems could not generalize, reason about intent, or adapt to variation.

### What LLMs Change: From Scripts to Goal-Directed Agents

- **LLMs enable a fundamentally different automation paradigm: prompt with a goal, not a script.**
  - Rather than encoding "click button A, then type in field B, then submit," an agent receives "book an appointment for this customer" or "transfer this data from document to database" and determines the execution path itself.
  - This goal-directed approach means the agent can handle varied data formats, unexpected UI states, and process changes without breaking.
- Agents are equipped with tooling and context that enables real action-taking — not just text generation but interactions with software systems, web interfaces, and data sources.
- Anthropic's computer use capability is cited as a concrete infrastructure enabler: models can now interact with existing software GUIs, removing the hard dependency on API availability.
  - This is significant because most operations workflows lack APIs — they run over fax, phone, spreadsheet, and paper forms.
- Early production evidence: Decagon has deployed automated customer support agents in live environments, demonstrating the technology is beyond proof-of-concept.

### The Market Opportunity: Analog Work That Software Never Reached

- **Despite decades of "software eating the world," vast amounts of business work remain analog**: phone calls, spreadsheets, fax lines, paper forms — the infrastructure of operations.
  - These workflows lack APIs or direct integrations, making them inaccessible to tra

## Key Claims

1. Substantial opportunity exists in productizing internal operations work within organizations, not just external professional services
2. Traditional RPA bots could not handle process changes or non-rigid workflows, causing frequent failures
3. Traditional RPA required expensive consultants, making it accessible only to large enterprises
4. UiPath was founded in 2005 and conducted its IPO in 2021
5. LLM-powered agents can be prompted with end goals rather than hard-coded deterministic steps, enabling true automation
6. AI agents will be more adaptable to data input variation and process changes than traditional RPA systems
7. There are over 8 million operations and information clerk roles in the US according to Bureau of Labor Statistics
8. The business process outsourcing (BPO) market represents approximately $250 billion
9. Operations roles lack established systems of record, leaving the intelligent automation market open to startups with no incumbent software to displace
10. Anthropic's computer use capability enables models to meaningfully interact with existing software

## Capabilities

- LLM-powered agents can be given high-level end goals (e.g., 'book an appointment', 'transfer data from document to database') and autonomously execute multi-step operations tasks without hard-coded deterministic steps, adapting to varied inputs and process changes
- LLMs can extract unstructured data from PDFs and faxes, run validations, and write structured data directly into electronic health record systems, automating healthcare referral management end-to-end
- AI-powered voice assistants can automate logistics load status checking and update tracking in trucking operations, replacing manual broker phone calls
- LLMs can ingest unstructured email data and automate price quoting and order entry into transportation management systems
- AI agents can provide automated customer support at production scale as a replacement for human operations headcount
- Horizontal AI services can parse unstructured data and output contextualized structured data as a reusable foundational component consumed by multiple intelligent automation pipelines

## Limitations

- Intelligent automation agents require vertical-specific domain context and deep system integrations to achieve the accuracy and consistency required for production — horizontal general-purpose agents cannot meet customer expectations across diverse industries
- Most back-office operations workflows lack APIs or direct integrations, forcing AI agents to use brittle bridging techniques (computer use, unstructured extraction) rather than clean programmatic access
- Production-ready intelligent automation is currently limited to very narrow, well-defined single workflows — broad multi-workflow or cross-department automation within a single organization remains undemonstrated
- Operations roles have no existing systems of record, so AI agents must extract and infer context from unstructured sources rather than querying authoritative structured data stores — introducing reliability and consistency risks
- Intelligent automation ecosystem is explicitly characterised as nascent with only 'early examples' in production — suggesting significant reliability, coverage, and edge-case gaps remain at time of writing
- Every intelligent automation company must independently rebuild the same foundational internal tooling (parsers, crawlers, write-back connectors) before addressing domain-specific logic — no mature shared infrastructure layer exists
- Previous RPA automation required expensive specialist consultants to implement, restricting it to large enterprises — current intelligent automation startups inherit the challenge of reducing implementation complexity enough to reach mid-market and SMB customers
- The source does not address accuracy, error-rate benchmarks, or failure mode analysis for any of the production intelligent automation deployments cited — the absence of these metrics is conspicuous given the critical nature of healthcare and logistics workflows

## Bottlenecks

- Absence of standard horizontal infrastructure components (unstructured data parsing, web crawlers, legacy system write-back) forces every intelligent automation company to rebuild the same foundational tooling, slowing ecosystem development and raising startup capital requirements
- Most legacy operational workflows run over phone, fax, spreadsheets, and paper with no APIs, forcing AI agents to rely on fragile bridging techniques (computer use, OCR, unstructured extraction) rather than reliable programmatic integrations

## Breakthroughs

- LLMs enable true end-goal-directed automation of business operations, replacing rigid keystroke-mimicry RPA with adaptive agents that handle process variation, unstructured inputs, and changing business conditions without re-scripting

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/startup_formation_and_gtm|startup_formation_and_gtm]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/business-process-outsourcing-bpo|Business Process Outsourcing (BPO)]]
- [[entities/computer-use|Computer Use]]
- [[entities/decagon|Decagon]]
- [[entities/robotic-process-automation-rpa|Robotic Process Automation (RPA)]]
- [[entities/tennr|Tennr]]
