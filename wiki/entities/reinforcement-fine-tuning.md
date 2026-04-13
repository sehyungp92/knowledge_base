---
type: entity
title: Reinforcement Fine-Tuning
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- computer_use_and_gui_agents
- model_commoditization_and_open_source
- multi_agent_coordination
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00220604649968116
staleness: 0.0
status: active
tags: []
---
# Reinforcement Fine-Tuning

> Reinforcement Fine-Tuning (RFT) is a model adaptation technique introduced by OpenAI that uses task-grader pairs to steer a model's chain-of-thought reasoning toward domain-specific patterns. Unlike traditional fine-tuning on static datasets, RFT enables developers to define tasks and automated graders, letting the model discover optimal reasoning and tool-calling paths for specific domains — making it a key enabler of vertical AI specialization and the commoditization of task-specific expert systems.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Reinforcement Fine-Tuning is one of OpenAI's agent development tools, described in Inside OpenAI's New Agent Development Tools. The core mechanic is the definition of a task-grader pair: developers supply a task description and an automated grading function that scores model outputs, and the training loop reinforces reasoning trajectories that score well. This is distinct from supervised fine-tuning (which requires labeled ground-truth completions) because the grader only needs to evaluate outcomes, not prescribe paths. The result is a model that internalises domain-specific heuristics — including which tools to call, in what order, and under what conditions — through exploration rather than imitation.

The significance of RFT extends beyond technique. It is an ingredient in the broader shift toward vertical AI: foundation models are strong generalists, but domains like law, medicine, and finance require precise, reliable behaviour under specialised constraints. RFT offers a route to that specialisation that is cheaper and more accessible than training from scratch, potentially democratising the creation of domain-expert agents at the startup level.

## Key Findings

### RFT as Infrastructure for Vertical AI Startups

The most concrete case study available for RFT's implications is Deal Velocity, Not Billable Hours: How Crosby Uses AI to Redefine Legal Contracting. Crosby is an AI-first law firm focused entirely on automating contract negotiations — NDAs, MSAs, and DPAs — billing per document rather than by the billable hour. Their core value proposition is *deal velocity*: reducing Total Turnaround Time (TTA), defined as time-in to time-out across all back-and-forths for a contract. They also track a secondary metric called HURT (Human Review Time) as a proxy for how much human attention the system still demands.

This operational structure maps directly onto what RFT enables. Contract negotiation is precisely the kind of domain where task-grader pairs are natural: the task is negotiating an acceptable contract, and the grader can evaluate whether the output satisfies a playbook, passes legal review, or reduces the number of negotiation rounds. Crosby's paralegal-level routing agent — responsible for classifying and directing incoming work from customers — is an early expression of what an RFT-trained orchestration layer might look like in production.

### The Grader-as-Domain-Expert Insight

A non-obvious implication of RFT is that it shifts the bottleneck from *labelled data* to *grader design*. Writing a grader requires domain expertise, but it is far less expensive than labelling thousands of expert completions. For legal work specifically, this matters because legal services are what economists call a *credence good* — consumers can only assess quality after the fact, and even then require an expert to confirm it. This makes labelled datasets inherently expensive and slow to accumulate. A grader that approximates the expert's judgement (checking against a legal playbook, flagging non-standard clauses, or measuring round-trip reduction) sidesteps much of that cost.

Crosby's staggered lawyer-engineer seating arrangement — physically alternating desks to maximise feedback cycles — is an organisational reflection of this: the grader (and the domain judgement behind it) must be continuously co-developed between legal and technical staff, not handed off once and forgotten.

### Liability and the Trust Gap

One open question RFT raises in high-stakes verticals is where liability lands when an RFT-trained agent makes a consequential error. Crosby's answer is unambiguous: they take malpractice insurance and accept full liability for all work performed, viewing this as foundational to the business model. This is notable because it suggests that the technical capability of RFT is not, by itself, sufficient to unlock a market — trust infrastructure (liability acceptance, professional credentials, auditability) must accompany the model. The question of whether RFT makes model behaviour auditable enough to satisfy that bar in regulated domains remains open.

### Scope and Current Limitations

The sources do not yet describe how RFT generalises beyond relatively structured domains. Legal contract review has well-defined evaluation criteria and bounded action spaces (accept, reject, redline, escalate). How RFT performs in domains where graders are harder to specify — open-ended research, strategy, or creative work — is not addressed. Similarly, the cost and complexity of grader design at scale, and whether the resulting models degrade gracefully outside their training distribution, are not characterised in the available evidence.

## Relationships

RFT is introduced as part of OpenAI's broader agent tooling ecosystem (alongside tool use primitives and orchestration APIs), situating it within [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]] and [[themes/agent_systems|agent_systems]]. Its primary strategic implication is as an accelerant for [[themes/vertical_ai_and_saas_disruption|vertical AI disruption]]: it lowers the barrier for startups to build domain-expert agents that compete with established professional services, as Crosby illustrates in legal contracting. This connects directly to [[themes/startup_formation_and_gtm|startup_formation_and_gtm]] — RFT-capable startups can define defensible moats around proprietary graders and domain-specific training data rather than model weights alone.

The technique also intersects [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]]: if RFT is accessible via API, it accelerates the commoditization dynamic by allowing any developer to create a specialist model on top of a general foundation, further compressing the advantage of incumbents who relied on proprietary training data. The 2024 landscape review in 2024 Year in Review frames this as part of the broader four-wars dynamic in AI — and RFT is one mechanism through which the application layer increasingly captures value that was previously retained at the model layer.

## Limitations and Open Questions

## Sources
