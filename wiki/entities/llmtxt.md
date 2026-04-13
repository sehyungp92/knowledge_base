---
type: entity
title: llm.txt
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_pricing_and_business_models
- ai_software_engineering
- code_and_software_ai
- code_generation
- context_engineering
- knowledge_and_memory
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00047580665457297314
staleness: 0.0
status: active
tags: []
---
# llm.txt

> `llm.txt` is a proposed web convention — a markdown file placed at a website's root — that communicates structured site context directly to LLM agents, analogous to how `robots.txt` signals intent to web crawlers. Its significance lies in addressing a fundamental friction in agentic systems: LLMs operating as autonomous agents need clean, semantically dense context, yet the web is built for human browsers. As agents move from chat assistants to autonomous actors traversing external services, `llm.txt` represents an early attempt to redesign the web's interface layer around the needs of LLM-powered clients.

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/ai_software_engineering|ai_software_engineering]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/context_engineering|context_engineering]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

`llm.txt` is a convention for a plain markdown file served at `https://example.com/llm.txt`, designed to give LLM agents a structured, parse-friendly description of what a site is and what it offers — without requiring the agent to scrape and interpret HTML. The analogy to `robots.txt` is instructive: just as `robots.txt` encodes a site's intent toward automated crawlers, `llm.txt` encodes a site's identity and navigational structure toward reasoning agents.

The motivation is rooted in context economics. As Context Engineering for Agents makes clear, feeding an LLM "just the right context for the next step" is the central engineering challenge in agentic systems — and HTML is a poor medium for that. Navigation menus, ad scripts, footer boilerplate, and dynamic rendering add noise without information. A site that publishes an `llm.txt` eliminates that overhead by exposing a curated, human-authored summary: what the site does, what endpoints or pages matter, and how an agent should orient itself.

## Context Engineering as the Core Problem

The `llm.txt` convention is best understood as one instance of a broader discipline. Context in agentic systems flows not only from users but from tool calls, retrieved documents, and external services — all accumulating across an agent's trajectory. Lance Martin at LangChain describes how naively accumulating all tool call outputs in an agent's message history quickly hits context window limits and degrades performance. The practical solutions — context offloading, summarization, selective retention — all require that context arriving from external sources be as clean and dense as possible from the start.

`llm.txt` addresses the intake side of this problem. If a web-browsing or research agent can retrieve structured context about a site in one small file rather than parsing multiple HTML pages, every downstream context management decision becomes easier. This is especially salient for production agents — such as those described in the LangChain talk, where systems like Claude Code can involve hundreds of tool calls per task — where each interaction with an external resource has a real token cost and cognitive load implication.

## Situating llm.txt in the Software Paradigm Shift

Andrej Karpathy's framing of Software 3.0 gives `llm.txt` deeper significance. In Software 3.0, LLMs are programmed via natural language prompts — they are the runtime, not a library. Sites that publish `llm.txt` are, in effect, writing documentation for a new kind of operating system: one where the "user" is a reasoning model rather than a person with a browser. This is a meaningful inversion. Historically, documentation and metadata were written to help humans; now sites must increasingly consider the LLM as a first-class reader.

Karpathy's observation about "jagged intelligence" — LLMs being superhuman in some reasoning domains while making elementary errors in others — also bears on `llm.txt`. An LLM that misreads a site's structure may confidently propagate that misreading through an entire agentic workflow. A well-authored `llm.txt` reduces the surface area for such failures by pre-resolving ambiguities a model might otherwise hallucinate around.

## Adoption and Economic Dynamics

The explosive growth of agentic infrastructure — E2B's sandbox usage grew roughly 375x in a single year, from 40,000 to approximately 15 million monthly sandboxes — signals that agents interacting with external web services are no longer theoretical. At this scale, the friction of HTML scraping is a genuine economic cost. Sites that lower that cost via `llm.txt` may see preferential treatment from agent orchestrators optimizing for efficiency; conversely, sites that don't may find themselves deprioritized as agents learn to route around noisy sources.

This creates an unusual incentive structure: unlike `robots.txt`, which is primarily about restriction, `llm.txt` is about invitation and legibility. It is an optimization play for site operators who want to remain relevant as agentic traffic grows relative to human browser traffic.

## Open Questions and Limitations

Several questions remain unresolved:

- **Standardization**: `llm.txt` is a convention, not a specification. Without a governing standard, content and structure will vary widely, limiting the degree to which agents can reliably depend on it.
- **Trust and adversarial use**: `robots.txt` is routinely ignored by bad actors; `llm.txt` could similarly be used to mislead agents — injecting false context or prompt-injection payloads into the file itself, exploiting the fact that agents may parse it with high trust.
- **Maintenance burden**: A `llm.txt` that goes stale as a site evolves may be worse than no file at all, particularly for agents that cache or overly rely on it. This is an instance of the broader LLM amnesia problem: models do not natively track whether their context sources have been updated.
- **Scope**: It is unclear how much a one-file convention can capture for complex, dynamic sites. For static documentation sites, it is likely sufficient; for platforms with evolving APIs, user-generated content, or dynamic structure, the file may need to be continuously regenerated or supplemented by richer protocols.

## Relationships

`llm.txt` sits at the intersection of [[themes/context_engineering|context engineering]], [[themes/tool_use_and_agent_protocols|agent protocols]], and the emerging economics of agentic web access. It is closely related to the memory and context management challenges described in Context Engineering for Agents, and exists within the paradigm shift Karpathy outlines in Software Is Changing (Again). The rapid growth of sandbox and agent infrastructure documented in Why Every Agent Needs Open Source Cloud Sandboxes provides the demand-side pressure that makes conventions like `llm.txt` economically meaningful.

## Key Findings

## Limitations and Open Questions

## Sources
