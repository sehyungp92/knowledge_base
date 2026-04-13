---
type: entity
title: Tennr
entity_type: entity
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- multi_agent_coordination
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00014674842275512904
staleness: 0.0
status: active
tags: []
---
# Tennr

> Tennr is a healthcare intelligent automation startup that uses LLMs to extract unstructured data from PDFs and faxes and write it into EHR systems, automating the referral management workflow. It represents a new generation of "intelligent automation" that succeeds where traditional RPA failed — by handling the messy, unstructured information flows that previously required human clerks or expensive BPO outsourcing.

**Type:** entity
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Tennr automates healthcare referral management — a workflow historically burdened by unstructured data arriving via fax and PDF, requiring manual extraction and re-entry into electronic health record (EHR) systems. By applying LLMs to this ingestion and transcription problem, Tennr collapses what was previously a human-intensive, error-prone process into an automated pipeline.

## Key Findings

Tennr sits at the intersection of two converging narratives: the failure of legacy RPA and the rise of intelligent automation as its successor.

**The RPA context.** Traditional robotic process automation, typified by companies like UiPath (founded 2005, IPO 2021), promised enterprise-wide automation but consistently underdelivered. RPA bots mimicked exact human keystrokes and clicks — making them brittle against any process variation or non-rigid workflow. Implementations required expensive consultants, limiting adoption to large enterprises. The core failure was structural: RPA assumed structured, deterministic processes, but real enterprise workflows are saturated with unstructured inputs. Healthcare referrals — arriving as handwritten faxes and scanned PDFs — are precisely the kind of workflow that defeated traditional RPA entirely.

**What Tennr does differently.** Rather than scripting keystrokes, Tennr uses LLMs to interpret unstructured inputs and extract semantically meaningful data before writing it into downstream systems of record. This mirrors a broader pattern in intelligent automation, where companies like Vooma (trucking price quoting from unstructured email) and Happyrobot (AI voice assistants for load status) are applying the same approach to other verticals. The key architectural shift is that the intelligence lives in the language model rather than in brittle procedural scripts.

**Market framing.** The addressable opportunity is substantial: over 8 million operations and information clerk roles in the US handle exactly this kind of data entry and transfer work, and the broader BPO market sits at approximately $250 billion. Tennr's vertical focus on healthcare referrals is a deliberate go-to-market choice — healthcare is a domain where fax usage has persisted anomalously long, creating a concentrated and high-value automation target.

**Business model implications.** Tennr's positioning aligns with the "service as software" paradigm described by Foundation Capital: rather than selling a tool that customers must operate themselves, the vendor takes responsibility for outcomes. This shifts pricing leverage from seat-based SaaS toward outcome- or volume-based models, and reframes the competitive comparison from other software vendors to the BPO and staffing costs being displaced.

**Systems of record dynamics.** Healthcare EHRs are archetypal Systems of Record — designed since the 1980s for data storage, not intelligent processing. Tennr does not displace these systems; it acts as an intelligent intake layer that feeds them, occupying a position analogous to what Foundation Capital terms a System of Intelligence sitting between unstructured inputs and structured records. As AI capabilities like Anthropic's computer use mature, such layers could become even more powerful — capable of navigating arbitrary software interfaces rather than relying on structured API integrations.

## Open Questions

The core limitation is validation: LLM extraction from handwritten or low-quality faxes introduces error risk in a high-stakes medical context. It is not clear from available sources how Tennr handles confidence thresholds, human-in-the-loop review, or liability for extraction errors. A second open question is defensibility — the technical moat of "apply LLMs to unstructured healthcare documents" is thin, and the durable advantage likely lies in EHR integration depth, training data from processed referrals, and workflow trust built with healthcare providers over time. Whether vertical focus creates sufficient lock-in against better-resourced horizontal automation platforms remains unresolved.

## Relationships

- **Vooma** — parallel pattern in trucking (unstructured email → TMS entry); both are post-RPA intelligent automation plays in document-heavy verticals
- **Happyrobot** — adjacent healthcare/logistics automation using voice rather than document processing
- **UiPath** — predecessor generation; Tennr's existence implicitly argues for RPA's failure mode
- RIP to RPA: The Rise of Intelligent Automation — primary source; frames Tennr as a representative case of the new automation paradigm
- AI leads a service as software paradigm shift — business model context for outcome-based pricing
- How Systems of Agents will collapse the enterprise stack — structural context on Systems of Record and the enterprise software stack Tennr operates within

## Limitations and Open Questions

## Sources
