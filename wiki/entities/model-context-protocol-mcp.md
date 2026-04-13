---
type: entity
title: Model Context Protocol (MCP)
entity_type: method
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- ai_pricing_and_business_models
- ai_software_engineering
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- computer_use_and_gui_agents
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- frontier_lab_competition
- knowledge_and_memory
- model_commoditization_and_open_source
- multi_agent_coordination
- pretraining_and_scaling
- reasoning_and_planning
- retrieval_augmented_generation
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- tool_use_and_agent_protocols
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 18
sources_since_update: 0
update_count: 1
influence_score: 0.02013647845382037
staleness: 0.0
status: active
tags: []
---
# Model Context Protocol (MCP)

**Type:** method
**Themes:** [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/ai_pricing_and_business_models|ai_pricing_and_business_models]], [[themes/ai_software_engineering|ai_software_engineering]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

An open standard introduced by Anthropic in November 2024 for integrating tool calls with LLMs. Uses web servers and JSON payloads. Saw rapid cross-lab adoption in 2025 before being donated to the Agentic AI Foundation in December 2025.

## Key Findings

1. When agents use code execution with MCP, intermediate results stay in the execution environment by default and never enter the model's context unless explicitly logged or returned. (from "Code execution with MCP: building more efficient AI agents")
2. With code execution, agents can filter and transform large datasets in the execution environment before returning results to the model, reducing what the model sees from 10,000 rows to just a few rele (from "Code execution with MCP: building more efficient AI agents")
3. Adding a SKILL.md file to saved agent functions creates a structured skill that models can reference, enabling agents to build an evolving toolbox of higher-level capabilities over time. (from "Code execution with MCP: building more efficient AI agents")
4. Code execution with filesystem access allows agents to maintain state across operations by writing intermediate results to files and resuming work from those files in later executions. (from "Code execution with MCP: building more efficient AI agents")
5. Writing control flow logic (loops, conditionals, error handling) in code rather than chaining individual MCP tool calls reduces 'time to first token' latency by delegating evaluation to the execution  (from "Code execution with MCP: building more efficient AI agents")
6. The problems of context management, tool composition, and state persistence in agents are novel in framing but have known solutions from established software engineering practices. (from "Code execution with MCP: building more efficient AI agents")
7. MCP clients can automatically tokenize PII before it reaches the model and untokenize it when passing to MCP tool calls, allowing sensitive data (emails, phone numbers, names) to flow between external (from "Code execution with MCP: building more efficient AI agents")
8. Presenting MCP servers as code APIs on a filesystem rather than as direct tool calls reduces token usage from 150,000 tokens to 2,000 tokens — a 98.7% reduction. (from "Code execution with MCP: building more efficient AI agents")
9. Most MCP clients load all tool definitions upfront directly into context, which causes agents connected to thousands of tools to process hundreds of thousands of tokens before reading a single user re (from "Code execution with MCP: building more efficient AI agents")
10. Large intermediate results passed through the model context can exceed context window limits entirely, breaking the workflow. (from "Code execution with MCP: building more efficient AI agents")
11. When agents directly call MCP tools, intermediate results must pass through the model context, causing large data (e.g., a full meeting transcript) to be loaded into context multiple times. (from "Code execution with MCP: building more efficient AI agents")
12. MCP is an open standard for connecting AI agents to external systems, launched in November 2024. (from "Code execution with MCP: building more efficient AI agents")
13. Cloudflare published similar findings about code execution with MCP, referring to the approach as 'Code Mode.' (from "Code execution with MCP: building more efficient AI agents")
14. A search_tools capability with configurable detail levels (name only, name and description, or full definition with schemas) allows agents to conserve context while finding relevant tools efficiently. (from "Code execution with MCP: building more efficient AI agents")
15. PII tokenization in the MCP client can be used to define deterministic security rules about where data can flow to and from. (from "Code execution with MCP: building more efficient AI agents")

## Relationships

## Limitations and Open Questions

## Sources
