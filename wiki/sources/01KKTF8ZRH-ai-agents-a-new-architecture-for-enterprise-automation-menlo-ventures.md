---
type: source
title: 'AI Agents: A New Architecture for Enterprise Automation | Menlo Ventures'
source_id: 01KKTF8ZRHYSZCCYXGX832KWWW
source_type: article
authors: []
published_at: '2024-09-26 00:00:00'
theme_ids:
- agent_systems
- knowledge_and_memory
- retrieval_augmented_generation
- startup_and_investment
- tool_use_and_agent_protocols
- vc_and_startup_ecosystem
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AI Agents: A New Architecture for Enterprise Automation | Menlo Ventures

**Authors:** 
**Published:** 2024-09-26 00:00:00
**Type:** article

## Analysis

# AI Agents: A New Architecture for Enterprise Automation | Menlo Ventures
2024-09-26 · article
https://menlovc.com/perspective/ai-agents-a-new-architecture-for-enterprise-automation/

---

## Briefing

**Menlo Ventures argues that the AI application stack is undergoing a structural shift from static RAG pipelines to dynamic agentic systems, defined by placing LLMs in the control flow rather than treating them as passive tools. The key architectural insight is that "agentic-ness" is a spectrum — from decisioning agents routing through fixed DAGs, to agents-on-rails operating within procedural guardrails, to the still-unrealized general AI agent — and that the agent-on-rails design is where leading enterprise companies are converging today.**

### Key Takeaways
1. **The defining criterion for agency is control flow, not tool use** — an application becomes agentic only when the LLM dynamically decides which actions to take, not when it merely calls predefined functions with pre-coded logic.
2. **RAG is not agentic** — despite using reasoning and external memory, RAG pipelines have pre-determined logic flows written in code, making them sophisticated retrieval tools rather than agents.
3. **Tool use is a half-step, not a full step** — function calling empowers LLMs to act on external systems but logical control flows remain pre-defined, placing it between RAG and true agency.
4. **Agents-on-rails is the pragmatic enterprise sweet spot** — leading companies (Sierra, Decagon, Factory AI, Sema4) are converging on this architecture as a "happy medium between autonomy and control," using natural language rulebooks instead of hard-coded logic.
5. **The agents-on-rails architecture demands a new infrastructure stack** — durable execution, episodic/working/long-term memory management, multi-agent orchestration, and guardrails are all required, representing significant new infrastructure opportunity.
6. **General AI agents remain commercially unattainable** — the for-loop "holy grail" architecture, where the LLM subsumes all structured scaffolding, does not yet work reliably in production despite rapid research progress since BabyAGI/AutoGPT in 2023.
7. **LATS is the research frontier for general agents** — Language Agent Tree Search adapts Monte Carlo Tree Search (the AlphaGo technique) to allow agents to explore trajectories, prioritize reward, and backtrack, representing the most sophisticated current design.
8. **Enterprise AI workflows are replacing human labor armies** — companies like Anterior (health plan claims), Norm AI (regulatory compliance), and Sema4 (financial back office) are automating processes that previously required large human teams.
9. **Four building blocks define full agentic capability** — reasoning over unstructured data, external memory (domain-specific + context), execution via tools, and planning via sub-task decomposition must all combine for full autonomy.
10. **Production RAG is far more complex than the basic diagram** — real deployments involve tens to hundreds of retrieval steps, parallel prompt chains for different task types, and multi-step synthesis, not a single retrieve-and-generate loop.

---

### The Four Building Blocks of Agent Capability

- **Reasoning** is the foundation: LLMs encode a partial world model in pre-trained weights that provides general knowledge and basic logic without additional scaffolding.
  - Anthropic and OpenAI models are "already incredibly effective at this out of the box."
  - This is the component least requiring additional engineering — it is the baseline assumption.

- **External memory** addresses the context limitation of LLMs: agents need domain-specific knowledge and bounded problem context that cannot fit in a context window.
  - Implemented predominantly via vector databases (e.g., Pinecone) storing embedded document chunks.
  - Distinct from the LLM's parametric knowledge — external memory is dynamic and domain-specific.

- **Execution** is the action surface: agents use tools (pre-written code components) to interact with external systems and enhance problem-solving.
  - Generalized tool primitives are emerging: web browsing (Browserbase, Tiny Fish), code interpretation (E2B), authentication/authorization (Anon), CRM/ERP connectors.
  - Early platforms mostly provide custom, application-specific toolboxes; generalized tools represent the infrastructure layer emerging around agents.

- **Planning** is what separates agents from chatbots: decomposing complex problems into sub-tasks, reflecting on progress, and re-adjusting.
  - Contrasted explicitly with "single-threaded sequence of next-token predictions" — the essay-writing metaphor illustrates why next-token generation alone cannot handle complex multi-step tasks.
  - This human-like iterative loop is the cognitive architecture primitive that enables autonomous task completion.

---

### The Spectrum of Agent Architectures

- **RAG (non-agentic baseline):** Standard architecture for most modern AI apps today, using reasoning and external memory but with fully pre-determined logic flows in code.
  - Process: ingest → chunk → embed → store → retrieve semantically relevant chunks → construct metaprompt → LLM synthesizes answer.
  - **Production RAG is far more complex:** tens to hundreds of retrieval steps; parallel prompt chains for different sub-tasks; multi-step synthesis of intermediate outputs.
  - Example: Eve (legal research copilot) breaks a Title VII query into parallel prompt chains for employer background, employment history, case law, supporting evidence, then synthesizes a final memo.
  - The LLM is a "tool" in RAG — passive, called by application code, not in control.

- **Tool Use (half-step):** Adds execution capability but logical flow remains pre-defined.
  - LLM selects a tool, crafts structured JSON inputs, triggers API executions.
  - Example: Omni's Calculations AI outputs Excel functions directly into spreadsheets, automating complex query generatio

## Key Claims

1. Generative AI apps have three core use cases with strong product-market fit today: search, synthesis, and generation.
2. Fully autonomous agents are defined by four elements: reasoning, external memory, execution, and planning.
3. Foundation models like Anthropic and OpenAI encode a partial world model into LLMs' pre-trained weights for general knowledge and basic logic.
4. Agents require external memory, often implemented via vector databases like Pinecone, to store domain-specific knowledge and bounded problem context.
5. Generalized agent tools emerging include web browsing, code interpretation, authentication/authorization, and connectors with enterprise systems like CRM and ERP.
6. Planning in agents involves breaking down work into smaller sub-tasks, reflecting on progress, and re-adjusting, rather than single-threaded next-token prediction.
7. RAG is not agentic because the logic flows are still pre-determined in code, even though it leverages reasoning and external memory.
8. Agents emerge when the LLM is placed in the control flow of the application and can dynamically decide which actions to take, which tools to use, and how to interpret inputs.
9. Menlo Ventures identifies three types of agents: decisioning agents, agents on rails, and general AI agents, varying in degrees of freedom.
10. Production AI apps have much more sophisticated flows with tens or hundreds of retrieval steps, often featuring prompt chains that execute in parallel.

## Capabilities

- RAG is the standard architecture for most modern AI applications, enabling enterprise search, legal research, and synthesis via multi-step prompt chains with parallel execution across tens to hundreds of retrieval steps
- Tool use / function calling enabling LLMs to invoke web browsing, code interpretation, authentication, and enterprise system connectors as pre-written actions triggered via structured JSON outputs
- Decisioning agents that traverse predefined directed-acyclic-graph decision trees using LLMs at each node to automate complex multi-conditional business workflows (e.g., clinical claims review, regulatory compliance, KYC)
- Agents on rails: semi-autonomous agents given high-level objectives and equipped with predefined tool libraries and natural-language SOPs, enabling end-to-end workflow automation in customer service, software development, and financial back-office
- Language Agent Tree Search (LATS): adapts Monte Carlo Tree Search to language agents, enabling multi-trajectory exploration, high-reward path prioritization, feedback incorporation, and backtracking
- LLMs encode partial world models in pretrained weights enabling general knowledge retrieval and basic logic reasoning out of the box without additional training

## Limitations

- Fully autonomous general AI agents — capable of dynamic reasoning, planning, and custom code generation to perform any action in external systems without predefined tools or rails — are not yet attainable
- Current RAG and tool-use applications have fully pre-determined control flows hard-coded by developers — the LLM cannot dynamically rewrite or adapt its own logic at runtime
- Even the most advanced production-grade agents (agents on rails) still require extensive manual setup: natural-language rulebooks, predefined tool libraries, guardrails, and explicit review checkpoints to prevent hallucination
- Complex agentic architectures require substantial additional data infrastructure — durable execution engines, episodic/working/long-term memory management, multi-agent orchestration, and guardrails — adding significant engineering complexity
- LLMs only possess a 'partial' world model — they lack complete or reliable knowledge for tasks requiring up-to-date, domain-specific, or deeply specialized understanding
- No discussion of security, adversarial robustness, or prompt injection risks for agents interacting with external systems (web, CRMs, ERPs) — a conspicuous absence given the described attack surface
- Production AI applications require tens to hundreds of LLM calls per user request, imposing unacknowledged latency and cost burdens not discussed in the article
- LATS and general agent architectures remain at the research/pioneering stage with no established broad commercial deployments, indicating reliability gaps for open-ended real-world tasks
- Agents on rails require pre-built, code-defined tool libraries — agents cannot dynamically discover or create new tools for unforeseen tasks, constraining the solution space to anticipated workflows

## Bottlenecks

- General AI agents blocked by inability of LLMs to reliably generate dynamic, safe, multi-step logic without structural scaffolding — the 'rails' cannot yet be removed
- Lack of standardized production infrastructure for agentic systems — durable execution, multi-tier memory management, multi-agent orchestration, and guardrails — requires every team to build bespoke stacks
- Hallucination and reliability gaps in LLMs force mandatory human review and guardrails in agentic pipelines, preventing truly autonomous unattended operation

## Breakthroughs

- Language Agent Tree Search (LATS) adapts Monte Carlo Tree Search from game-playing AI to language agents, enabling structured multi-trajectory exploration, backtracking, and reward-guided search over agent reasoning paths
- Architectural convergence on 'agents on rails' as a production-viable paradigm that balances autonomy with reliability — enabling enterprise deployment of semi-autonomous agents across customer service, software engineering, and financial workflows

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/startup_and_investment|startup_and_investment]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
- [[themes/vc_and_startup_ecosystem|vc_and_startup_ecosystem]]

## Key Concepts

- [[entities/autogpt|AutoGPT]]
- [[entities/cognition|Cognition]]
