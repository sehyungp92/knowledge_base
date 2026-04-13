---
type: entity
title: context compaction
entity_type: method
theme_ids:
- agent_systems
- ai_software_engineering
- code_and_software_ai
- code_generation
- context_engineering
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- reasoning_and_planning
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00038921501732360776
staleness: 0.0
status: active
tags: []
---
Created `wiki/entities/context-compaction.md`. Here's what the page covers:

**Overview** — frames compaction as the operationally dominant approach to context budget management in agent systems, and situates it as a symptomatic rather than structural solution.

**Key Findings (synthesized, not listed):**
- *Simplicity won in practice* — Claude Code tried rewriting tool calls, truncation, and hybrid strategies before settling on model summarization. Consistent with the project's "thinnest wrapper" philosophy.
- *Context engineering as upstream frame* — LangChain's framing positions compaction as one of several context management strategies (alongside retrieval and structured memory), helping characterize where it fits and where it doesn't.
- *RLMs as structural alternative* — the 91.3% vs 0.0% result on BrowseComp-Plus illustrates how much compaction leaves on the table vs. lossless on-demand access via REPL; but RLMs trade summarization bias for retrieval bias.
- *Cost dimension* — the $6/user/day figure grounds compaction as an economic decision, not just an architectural one.

**Limitations** — invisible loss to the model, underspecified compaction threshold, early-context dependency penalty, and compounding drift in persistent agents.

**Relationships** — connected to agentic RAG, RLMs, context engineering theme, and all three source pages.

## Overview

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
