---
type: theme
title: Tool Use & Agent Protocols
theme_id: tool_use_and_agent_protocols
level: 2
parent_theme: agent_systems
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 68
sources_since_update: 0
update_count: 1
velocity: 0.505
staleness: 0.0
status: active
tags: []
---
# Tool Use & Agent Protocols

> Tool use and agent protocols have crossed from infrastructure-building into architectural reckoning. Through 2024 and early 2025, the field consolidated around reliable multi-turn agentic execution — 90%+ tool-calling success rates, unified APIs, deep research in minutes rather than weeks. GPT-5's tool-integrated reasoning then broke the underlying paradigm: tools are no longer discrete interruptions to reasoning but woven into the thinking process itself, rendering the atomic function-call architecture the ecosystem standardized around incompatible with how advanced agents actually operate. The resolution horizon is 1–2 years, with security architecture lagging even further behind the integration surface MCP has created.

**Parent:** [[themes/agent_systems|Agent Systems]]

---

## Current State

The trajectory of tool use and agent protocols divides cleanly into two eras: consolidation, then paradigm invalidation.

Through 2024 and into early 2025, the dominant motion was consolidation. LLMs advanced from single-shot function calls to reliable multi-turn, multi-step agentic execution — correctly determining parallel versus sequential tool dispatch, achieving 90.6% tool-calling success rates across standardized benchmarks, and compressing deep research workflows from weeks to minutes in broad production. The Unified Responses API replaced the fragmented Chat Completions + Assistants architecture; the Assistants API's planned deprecation was a tacit admission that an entire API generation had failed developer needs. These were real gains. But gains within a paradigm: tools as discrete interruptions to reasoning, retrieval pipelines as developer-specified scaffolding, control flows hard-coded at build time.

GPT-5's tool-integrated reasoning broke that paradigm. Tools are no longer post-hoc function calls; they are woven into the thinking process itself — the model iterates, branches, and synthesizes mid-chain using tool outputs. The breakthrough converts a capability story into a bottleneck story. The atomic API-style tool design the ecosystem standardized around is architecturally incompatible with how advanced reasoning agents actually operate. Benchmark performance confirms the models are ahead of the infrastructure designed to deploy them: 70.6 on Tau2-retail, 65.8 on Tau2-telecom, outperforming Claude Sonnet 4 and GPT-4.1 on multi-turn tasks.

The security trajectory is the underappreciated counterweight. MCP creates a universal integration layer without commensurate authentication and access controls — a worsening architectural vulnerability. As autonomous commerce agents move from demo maturity toward payment execution on behalf of users, this gap shifts from theoretical to consequential. The field has not yet produced MCP-era security frameworks to match the scale of integration it has enabled.

Momentum is building in tool-integrated reasoning and multi-domain autonomous orchestration; it is stalling in security architecture and the transition to open-ended tool API design.

---

## Capabilities

**Broad production:**
- Deep research agents (ChatGPT, Perplexity) generate tailored competitive and industry syntheses from public data in minutes, compressing workflows that previously took weeks.
- Reasoning models agentically use and combine all tools within ChatGPT — web search, Python code execution, visual analysis, and file operations — within a single reasoning trace.
- Web search tool in API achieving 90% on SimpleQA (GPT-4o search preview) and 88% (GPT-4o mini search preview), with inline source citations grounding time-sensitive queries.
- Unified Responses API combining Chat Completions simplicity with multi-tool, multi-turn agent capabilities in a single API surface, replacing the fragmented prior architecture.
- Agent systems extend capabilities through simple CLI tool definitions that agents learn to call dynamically, with automatic discovery.

**Narrow production:**
- Multi-step agentic tool use in constrained customer service domains: 70.6 Tau2-retail, 56.5 Tau2-airline, 65.8 Tau2-telecom.
- Tool-integrated reasoning: the model uses tools as part of the thinking process itself — iterating, planning, and exploring mid-tool-chain.
- Reliable parallel tool calling: correctly determining which tools can run in parallel versus sequentially and executing accordingly.
- LLMs invoke tool use and API calls in the digital world, with capabilities increasingly built on execution feedback loops.
- Highest tool-calling success rate among frontier models at 90.6%, outperforming Claude Sonnet 4 (89.5%) and Kimi-K2 (86.2%).
- Multi-step agentic tool use with multi-turn dialogue, achieving 66.1 on Tau2-bench and 76.5 on ACEBench (En).
- Tool use and function calling enabling LLMs to invoke web browsing, code interpretation, authentication, and enterprise system integrations.
- Agents autonomously discover unavailable tools, compose multi-step tool chains (ffmpeg, header detection, API calls), and fall back gracefully.

**Demo maturity:**
- Reasoning agents autonomously decompose tasks into multi-step search plans, executing iterative information-gathering loops.
- Fully autonomous multi-domain orchestration: single agent executing 17 tool calls spanning search, calendar, Gmail, flights, and more.
- AI agent payment and commerce protocols enabling autonomous purchasing on behalf of users.

---

## Limitations

**Blocking / worsening:**
- Standardized agent protocols (MCP) increase attack surface dramatically by creating a universal integration layer without commensurate authentication and access controls. This is an architectural vulnerability that worsens as adoption grows, not an improving one. *(severity: blocking, trajectory: worsening)*

**Significant / improving:**
- Production agent deployment requires extensive prompt iteration and custom orchestration logic — existing API primitives do not abstract enough of the complexity for reliable multi-step execution without bespoke engineering. *(severity: significant)*
- Assistants API design was fundamentally inadequate for agent use cases — its planned deprecation reveals a prior API generation that failed, a costly ecosystem lesson. *(severity: significant)*
- Current RAG and tool-use applications have fully pre-determined control flows hard-coded by developers — the LLM cannot restructure the pipeline in response to what it discovers at runtime. *(severity: significant)*
- Agents on rails require pre-built, code-defined tool libraries — agents cannot dynamically discover or create new tools outside of research demonstrations. *(severity: significant)*
- Excessive token generation on hard reasoning tasks or unclear tool definitions leads to truncated outputs or incomplete tool executions. *(severity: significant)*
- Performance degradation when tool use is enabled: certain tasks that perform well in plain completion mode regress when tools are introduced. *(severity: significant)*
- GPT-5's capabilities only manifest effectively when given high-quality, open-ended tools — atomic API-style tool design creates a controlled-conditions ceiling on what the model can actually do in production. *(severity: significant, trajectory: stable)*

**Significant / unclear:**
- No disclosure of latency, reliability SLAs, or cost structure for multi-turn agent workflows running many sequential model calls — a conspicuous absence that complicates enterprise planning. *(severity: significant, trajectory: unclear)*

**Minor / improving:**
- o3-pro launches without full tool support, temporarily making the most compute-intensive variant also the most capability-constrained for agentic use cases. *(severity: minor)*
- MCP features absent from web and mobile app at launch: agentic integrations unavailable to consumer product users initially. *(severity: minor)*

---

## Bottlenecks

**Atomic API tool design incompatibility** *(horizon: 1–2 years, status: active)*
The current atomic API-style tool design paradigm is architecturally incompatible with how advanced reasoning agents like GPT-5 actually work. GPT-5 demonstrated that tool-integrated reasoning — where tools are woven into mid-chain thinking rather than dispatched as discrete interruptions — requires open-ended query interfaces, not function signatures. Companies must rebuild their tool APIs as open-ended query languages. This blocks deployment of agent-native products at scale and has no near-term resolution; the ecosystem-wide migration required makes this a 1–2 year horizon.

**Agent development infrastructure gap** *(horizon: months, status: active)*
The absence of unified agent development infrastructure (API + orchestration + observability) was blocking rapid production deployment of reliable multi-step agents by enterprise developers without bespoke engineering. The Responses API and Agents SDK partially address this, but the bottleneck remains active as observability and reliability SLA tooling lags.

**Structured protocols vs. model-native tool calling** *(horizon: 1–2 years, status: active)*
A fundamental architectural mismatch exists between structured tool protocols (MCPs) and model-native tool calling (CLIs). No consensus has emerged on which abstraction layer is canonical, blocking efficient tool integration for context-constrained agents that need composable tool chains.

---

## Breakthroughs

**GPT-5 tool-integrated reasoning** *(significance: major)*
GPT-5 demonstrated that tools are no longer discrete function calls that interrupt reasoning — they are integral steps within the reasoning process. The model iterates, branches, and synthesizes using tool outputs mid-chain. This overturned the prior assumption that LLMs use tools by emitting function calls, receiving results, and reasoning about them afterward. Tools were external appendages; they are now internal reasoning operations.

**First reasoning models with full agentic tool access** *(significance: major)*
o3 and o4-mini unified extended chain-of-thought reasoning with web search, Python execution, and file analysis in single deployed models. Previously, reasoning models (o-series) and tool-using assistant models (GPT-series) were separate capability tracks — deep multi-step reasoning and broad agentic tool use could not be combined. This integration removes a hard architectural partition that had structured the field.

**Agents autonomously discover and compose novel tool chains** *(significance: notable)*
Agents demonstrated spontaneous tool discovery and composition without explicit tool registration — finding ffmpeg, detecting opus audio headers, locating API keys, and falling back from local Whisper to remote OpenAI API. This challenges the assumption that tool use requires pre-declared schemas and implies that agent protocols may need to accommodate dynamically discovered toolchains.

**Unified Responses API** *(significance: notable)*
The Responses API introduced a new paradigm for agent development: multi-tool, multi-turn workflows expressed as a single unified primitive. Prior to this, agent development required composing incompatible APIs (Chat Completions for simplicity, Assistants API for tool use) with custom orchestration glue. The Assistants API's simultaneous deprecation marked the close of a failed API generation.

---

## Anticipations

- Developer tooling ecosystems begin reorienting around query-language-style tool interfaces rather than function signatures — the transition from atomic tool design to open-ended query APIs.
- A high-profile agentic security incident forces reactive hardening before proactive MCP-era security frameworks emerge, stress-testing both the integration surface and the commerce agent layer simultaneously.
- Autonomous commerce agents crossing from demo to production maturity, at which point the MCP security gap shifts from architectural concern to active liability.
- Benchmark suites measuring function-calling fidelity (BFCL-v3) gain weight in model selection for agentic pipelines as tool-calling reliability emerges as a primary differentiator independent of raw reasoning.

---

## Cross-Theme Implications

**→ [[themes/multi_agent_coordination|Multi-Agent Coordination]]**
A standardized SDK designed for both single-agent and multi-agent workflow orchestration removes the need for custom coordination logic, lowering the complexity barrier and accelerating experimentation with hierarchical and peer-to-peer architectures. Separately, standardized tool APIs and authentication infrastructure create the shared protocol surface that agent-to-agent delegation requires — agents can hand off subtasks to specialized peers only when tool interfaces are stable enough to serve as coordination contracts.

**→ [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]**
Built-in file search with query optimization, metadata filtering, and custom reranking commoditizes core RAG infrastructure. Developers can now instantiate production-grade RAG pipelines in a few lines of code, raising the baseline expectation for quality and reducing the moat of specialized RAG middleware.

**→ [[themes/software_engineering_agents|Software Engineering Agents]]**
Tool-calling success rate (90.6% for GLM-4.5 vs. 77.1% for Qwen3-Coder) is emerging as a primary differentiator in SE agent performance, independent of raw reasoning ability — reliability of tool-use infrastructure, not model intelligence alone, is a key bottleneck. Native zero-shot tool understanding reduces engineering overhead, shifting complexity from orchestration code to model capability. Built-in computer use and file search as first-class API tools further reduce integration burden for coding agent developers.

**→ [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]]**
Agents with dynamic tool-use capabilities can integrate with arbitrary APIs and legacy systems on-the-fly, removing the need for pre-built connector libraries — directly threatening Zapier's and iPaaS providers' moat. Commoditizing web search, file search, and computer use as platform-level primitives accelerates time-to-market for vertical AI companies and increases disruption pressure on incumbents. Deterministic code execution within agent skills simultaneously provides the reliability tier that LLM-native approaches lack, undercutting the repeatability justification for maintaining vertical SaaS subscriptions.

**→ [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]**
Commoditization of tool-use primitives (web browsing, code interpretation, CRM/ERP connectors) directly enables GUI agents — once these building blocks are standardized infrastructure, computer-use agents become an assembly problem rather than a research problem.

**→ [[themes/hallucination_and_reliability|Hallucination & Reliability]]**
Web search with inline source citations provides a systematic grounding mechanism for time-sensitive queries, directly attacking a core hallucination failure mode. The measurable accuracy improvement (90% SimpleQA for GPT-4o search) establishes web search as a reliability primitive, shifting the reliability burden from model internals to retrieval architecture.

**→ [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]]**
Near-perfect AIME performance with a Python interpreter shows that tool-augmented reasoning effectively closes the gap on competition mathematics benchmarks. Formal reasoning benchmarks must now explicitly control for tool access to remain meaningful signals of unaided capability.

**→ [[themes/ai_pricing_and_business_models|AI Pricing & Business Models]]**
Per-query pricing for search tools ($25–30/1K queries) layered on top of token costs establishes a new pricing architecture where action costs must be modeled separately from inference costs, creating pressure toward outcome-based and usage-metered pricing models.

**→ [[themes/context_engineering|Context Engineering]]**
The Responses API's unified item-based design with streaming events and forthcoming stateful Thread-like objects introduces a platform-level context management model, pushing context engineering practices toward API-native state rather than application-managed context windows.

**→ [[themes/agent_evaluation|Agent Evaluation]]**
Models capable of zero-shot tool orchestration without workflow scaffolding require evaluation frameworks that test open-ended tool composition rather than templated tool-call sequences, driving evolution of agentic benchmarks.

**→ [[themes/startup_formation_and_gtm|Startup Formation & GTM]]**
Standardized platform primitives lower the technical barrier to building agent-based products but simultaneously raise the competitive floor. Startups that previously differentiated on integration complexity now face commoditization of their core infrastructure, forcing GTM strategy toward domain data, workflow depth, and distribution.

**→ [[themes/agent_systems|Agent Systems]]** *(self-referential pressure)*
Models that autonomously chain web search, code execution, image generation, and file analysis within a single reasoning trace reduce the architectural burden on multi-agent orchestration frameworks. Tasks previously requiring multi-agent pipelines become single-agent workloads, reshaping where agent system complexity is warranted.

---

## Contradictions

**Tool reliability vs. reasoning regression.** Models achieve 90.6% tool-calling success rates on benchmarks while simultaneously exhibiting performance degradation on tasks that perform well in plain completion mode when tools are introduced. High aggregate reliability coexists with specific regression failure modes that are not captured by aggregate metrics.

**Integration standardization vs. security regression.** MCP accelerates integration by creating a universal layer, but the universality of that layer is precisely what makes the security gap worsening rather than improving. The same property that makes MCP valuable (broad connectivity) makes its authentication gaps increasingly consequential as adoption grows.

**Agents ahead of infrastructure.** The field's most capable reasoning agents (GPT-5) are architecturally incompatible with the tool infrastructure designed to deploy them. The models outran the ecosystem — an inversion of the more common pattern where infrastructure precedes model capability.

**Dynamic discovery vs. static protocols.** Breakthroughs in spontaneous tool discovery (agents finding ffmpeg, detecting formats, locating API keys without declarations) contradict the protocol assumption that tool use requires pre-declared schemas. The research frontier and the standards layer are moving in opposite directions.

---

## Research Opportunities

- **Open-ended tool API design:** Redesign tool interfaces as query languages rather than function signatures, exposing richer intermediate state and feedback loops for mid-chain reasoning agents. The 1–2 year bottleneck on atomic API incompatibility is the most consequential near-term research target.
- **MCP-era security frameworks:** Develop authentication, authorization, and access control standards commensurate with the integration surface MCP has created — before a high-profile incident drives reactive rather than proactive hardening.
- **Dynamic tool registration protocols:** Extend agent protocol standards to support dynamically discovered toolchains — tool provenance tracking, runtime sandboxing, and capability registration without pre-declared schemas.
- **Tool-aware benchmarking:** Develop evaluation frameworks that explicitly control for tool access in formal reasoning benchmarks, and that test open-ended tool composition rather than templated call sequences. BFCL-v3 style function-calling fidelity metrics need to be incorporated into standard model selection criteria for agentic pipelines.
- **Latency and reliability SLAs for multi-turn agentic workflows:** The conspicuous absence of disclosed performance characteristics for long-horizon agent execution is a gap with direct enterprise adoption implications.
- **Commerce agent trust architecture:** As autonomous payment and purchasing agents approach production maturity, develop trust models, audit trails, and user-consent frameworks that make delegation to commerce agents safe at scale.

---

## Development Timeline

<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJS1QQ4Y-rl-environments-and-the-hierarchy-of-agentic-capabilities|RL Environments and the Hierarchy of Agentic Capabilities]]: Nova 1 Pro failed to correctly map task information to tool arguments, passing obviously incorrect v
- **2026-04-08** — [[sources/01KKTE8J95-kimi-k2-open-agentic-intelligence|Kimi K2: Open Agentic Intelligence]]: New capability: Multi-step agentic tool use with realistic multi-turn dialogue: 70.6 Tau2-retail
- **2026-04-08** — [[sources/01KJS1Q5DT-code-execution-with-mcp-building-more-efficient-ai-agents|Code execution with MCP: building more efficient AI agents]]: When agents directly call MCP tools, intermediate results must pass through the model context, causi
- **2026-04-08** — [[sources/01KJS1WVEB-interleaved-thinking-unlocks-reliable-minimax-m2-agentic-capability|Interleaved Thinking Unlocks Reliable MiniMax-M2 Agentic Capability]]: Interleaved thinking is important for both agentic and coding applications in MiniMax-M2.
- **2026-04-08** — [[sources/01KJS48D4H-context-engineering-for-ai-agents-lessons-from-building-manus|Context Engineering for AI Agents: Lessons from Building Manus]]: With Claude Sonnet, cached input tokens cost 0.30 USD/MTok versus 3 USD/MTok for uncached tokens, a 
- **2026-04-08** — [[sources/01KJSS5RHX-project-vend-can-claude-run-a-small-shop-and-why-does-that-matter|Project Vend: Can Claude run a small shop? (And why does that matter?)]]: Claude hallucinated a conversation with a nonexistent person named 'Sarah' at Andon Labs and then th
- **2026-04-08** — [[sources/01KJSVPQDA-the-think-tool-enabling-claude-to-stop-and-think|The "think" tool: Enabling Claude to stop and think]]: The 'think' tool creates dedicated space for structured thinking during complex tasks and is distinc
- **2026-04-08** — [[sources/01KJSX4F4C-building-effective-ai-agents|Building Effective AI Agents]]: Complexity in agentic systems should only be added when it demonstrably improves outcomes.
- **2026-04-08** — [[sources/01KJRZT83B-2025-the-year-in-llms|2025: The year in LLMs]]: OpenAI initiated the reasoning/inference-scaling/RLVR revolution in September 2024 with o1 and o1-mi
- **2026-04-08** — [[sources/01KKTEN0B4-new-tools-for-building-agents|New tools for building agents]]: Breakthrough: Unified Responses API introduces a new paradigm for agent development: multi-too
- **2026-04-08** — Wiki page created. Theme has 68 sources.
- **2026-02-14** — [[sources/01KJVPHM2Z-the-100x-ai-breakthrough-no-one-is-talking-about|The 100x AI Breakthrough No One is Talking About]]: Google DeepMind explicitly states that its results should not be interpreted as AI being able to con
- **2026-02-12** — [[sources/01KJVPDX06-the-rise-of-webmcp|The Rise of WebMCP]]: The Google Chrome team shipped an early preview of WebMCP.
- **2026-02-10** — [[sources/01KJVPCJJ3-how-openclaw-works-the-real-magic|How OpenClaw Works: The Real "Magic"]]: The heartbeat input fires every 30 minutes automatically.
- **2026-01-20** — [[sources/01KJT1Y2H0-toward-efficient-agents-memory-tool-learning-and-planning|Toward Efficient Agents: Memory, Tool learning, and Planning]]: Agent cost includes overhead from tools, memory, and retries in addition to token generation, unlike
- **2026-01-05** — [[sources/01KJT2BQDA-agentic-memory-learning-unified-long-term-and-short-term-memory-management-for-l|Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents]]: Adding LTM alone yields performance gains of +10.6%, +14.2%, and +7.4% on ALFWorld, SciWorld, and Ho
- **2025-12-31** — [[sources/01KJT2Q145-recursive-language-models|Recursive Language Models]]: RLMs treat arbitrarily long user prompts as part of the external environment rather than feeding the
- **2025-12-18** — [[sources/01KJT38XNY-adaptation-of-agentic-ai|Adaptation of Agentic AI]]: TextGrad improves GPT-4o's zero-shot code accuracy on LEETCODE-HARD from 26% to 36%, raises MMLU-Phy
- **2025-12-04** — [[sources/01KJT62ZGZ-nex-n1-agentic-models-trained-via-a-unified-ecosystem-for-large-scale-environmen|Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment Construction]]: NexGAP constructs over 200 agent frameworks and environments, with agent and sub-agent graphs rangin
- **2025-12-03** — [[sources/01KJT6CAK6-thinking-with-programming-vision-towards-a-unified-view-for-thinking-with-images|Thinking with Programming Vision: Towards a Unified View for Thinking with Images]]: CodeVision-7B achieves an average score of 73.4 on transformed OCRBench, a +17.4 improvement over it
- **2025-11-26** — [[sources/01KJT6ZBSZ-toolorchestra-elevating-intelligence-via-efficient-model-and-tool-orchestration|ToolOrchestra: Elevating Intelligence via Efficient Model and Tool Orchestration]]: Orchestrator-8B is 2.5x more computationally efficient than GPT-5 on the HLE benchmark.
- **2025-11-20** — [[sources/01KJT7RXXT-agent0-unleashing-self-evolving-agents-from-zero-data-via-tool-integrated-reason|Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning]]: Agent0 on Qwen3-8B-Base shows consistent iterative improvement: math score 55.1 (Iter 1) → 56.5 (Ite
- **2025-11-19** — [[sources/01KJVK5SZY-self-improving-ai-agents-architecting-llm-memory-with-ace-voyager-and-claude-ski|Self-Improving AI Agents: Architecting LLM Memory with ACE, Voyager, and Claude Skills [AIA Nov 7]]]: The ACE (Agentic Context Engineering) framework divides labor across three roles: a generator that p
- **2025-11-18** — [[sources/01KJT89YD6-agent-r1-training-powerful-llm-agents-with-end-to-end-reinforcement-learning|Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning]]: GRPO achieved the best overall RL performance (average EM 0.3877) on multi-hop QA, closely followed 
- **2025-11-13** — [[sources/01KJT9AAYD-agentevolver-towards-efficient-self-evolving-agent-system|AgentEvolver: Towards Efficient Self-Evolving Agent System]]: AgentEvolver's self-evolution process follows a three-stage training flow: from environments to task
- **2025-11-03** — [[sources/01KJTBNSX3-simulating-environments-with-reasoning-models-for-agent-training|Simulating Environments with Reasoning Models for Agent Training]]: An 8B model fine-tuned on Simia-simulated trajectories (based on Qwen3-8B) outperforms Qwen2.5-32B-I
- **2025-10-16** — [[sources/01KJS276S8-equipping-agents-for-the-real-world-with-agent-skills-anthropic-claude|Equipping agents for the real world with Agent Skills \ Anthropic | Claude]]: Agent Skills are supported across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Devel
- **2025-10-13** — [[sources/01KJTD9WCB-demystifying-reinforcement-learning-in-agentic-reasoning|Demystifying Reinforcement Learning in Agentic Reasoning]]: Overlong reward shaping applies zero penalty within a safe length budget, linear penalty approaching
- **2025-10-07** — [[sources/01KJTE6RW1-in-the-flow-agentic-system-optimization-for-effective-planning-and-tool-use|In-the-Flow Agentic System Optimization for Effective Planning and Tool Use]]: AGENTFLOW with a 7B-scale backbone outperforms top-performing baselines with average accuracy gains 
- **2025-10-06** — [[sources/01KJTEKYPY-multi-agent-tool-integrated-policy-optimization|Multi-Agent Tool-Integrated Policy Optimization]]: MATPO is derived from a principled credit assignment mechanism across planner and worker rollouts.
- **2025-09-30** — [[sources/01KJS2K6B1-chatgpt-the-agentic-app|ChatGPT: The Agentic App]]: ACP is significantly more complex than MCP, with defined functionalities including discoverability, 
- **2025-09-22** — [[sources/01KJS34J20-thinking-searching-and-acting|Thinking, Searching, and Acting]]: Modern reasoning models are built on three fundamental primitives: Thinking (reasoning traces enabli
- **2025-09-16** — [[sources/01KJTJ3WVG-towards-general-agentic-intelligence-via-environment-scaling|Towards General Agentic Intelligence via Environment Scaling]]: AgentScaler has only been validated up to the 30B parameter scale and has not been extended to model
- **2025-09-12** — [[sources/01KJTJNWNW-deepdive-advancing-deep-search-agents-with-knowledge-graphs-and-multi-turn-rl|DeepDive: Advancing Deep Search Agents with Knowledge Graphs and Multi-Turn RL]]: The DeepDive-32B SFT-only model scores 9.5% on BrowseComp; RL training raises it to 15.3%.
- **2025-09-11** — [[sources/01KJVJY5T8-context-engineering-for-agents-lance-martin-langchain|Context Engineering for Agents - Lance Martin, LangChain]]: Context engineering is defined as the challenge of feeding an LM just the right context for the next
- **2025-09-11** — [[sources/01KKT42HFY-kimi-k2-open-agentic-intelligence|KIMI K2: OPEN AGENTIC INTELLIGENCE]]: New capability: Multi-step agentic tool use with multi-turn dialogue, achieving 66.1 on Tau2-ben
- **2025-08-29** — [[sources/01KJTM33JC-universal-deep-research-bring-your-own-model-and-strategy|Universal Deep Research: Bring Your Own Model and Strategy]]: UDR wraps around any language model and enables users to create custom deep research strategies with
- **2025-08-28** — [[sources/01KJTM994W-rstar2-agent-agentic-reasoning-technical-report|rStar2-Agent: Agentic Reasoning Technical Report]]: rStar2-Agent-14B achieves 80.6% pass@1 on AIME24, surpassing DeepSeek-R1 (671B), o3-mini (medium), a
- **2025-08-27** — [[sources/01KJSZ6JB0-roadmap-developer-tooling-for-software-30|Roadmap: Developer Tooling for Software 3.0]]: GitHub Copilot previewed in June 2021, five months before ChatGPT sparked the broader AI revolution.
- **2025-06-12** — [[sources/01KJTQ65VX-videoexplorer-think-with-videos-for-agentic-long-video-understanding|VideoExplorer: Think With Videos For Agentic Long-Video Understanding]]: VideoExplorer introduces the principle of 'thinking with video', which treats reasoning as a dynamic
- **2025-06-12** — [[sources/01KJTQD302-build-the-web-for-agents-not-agents-for-the-web|Build the web for agents, not agents for the web]]: The paper introduces the Agentic Web Interface (AWI) as a new type of interface specifically designe
- **2025-04-24** — [[sources/01KJVJSXB7-why-every-agent-needs-open-source-cloud-sandboxes|Why Every Agent needs Open Source Cloud Sandboxes]]: E2B grew from 40,000 sandboxes per month in March 2024 to approximately 15 million sandboxes per mon
- **2025-04-19** — [[sources/01KJSTSTMC-openais-o3-over-optimization-is-back-and-weirder-than-ever|OpenAI's o3: Over-optimization is back and weirder than ever]]: Bob McGrew, former Chief Research Officer at OpenAI, stated that intelligence is no longer the prima
- **2025-04-15** — [[sources/01KJTZD9X5-retool-reinforcement-learning-for-strategic-tool-use-in-llms|ReTool: Reinforcement Learning for Strategic Tool Use in LLMs]]: ReTool sets the KL coefficient to 0.0 during RL training.
- **2025-04-09** — [[sources/01KJSTZNFF-announcing-the-agent2agent-protocol-a2a-google-developers-blog|Announcing the Agent2Agent Protocol (A2A)- Google Developers Blog]]: A2A is built on existing web standards including HTTP, SSE, and JSON-RPC to ease integration with ex
- **2025-04-09** — [[sources/01KJV0HFJ8-skillweaver-web-agents-can-self-improve-by-discovering-and-honing-skills|SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills]]: APIs synthesized by strong agents can enhance weaker agents by up to 54.3% on WebArena
- **2025-04-07** — [[sources/01KJV168T2-synthetic-data-generation-multi-step-rl-for-reasoning-tool-use|Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use]]: SWiRL does not require golden labels or human annotations, relying entirely on model-based judgments
- **2025-03-30** — [[sources/01KJV1PA03-torl-scaling-tool-integrated-rl|ToRL: Scaling Tool-Integrated RL]]: TORL-7B reaches 62.1% average accuracy across benchmarks, representing a 14.7% absolute improvement 
- **2025-03-25** — [[sources/01KJVFH11E-inside-openais-new-agent-development-tools|Inside OpenAI's New Agent Development Tools]]: OpenAI released the Agents SDK to support multi-agent swarm architectures because developers were al
- **2025-03-18** — [[sources/01KJSVWTEZ-14-what-is-mcp-and-why-is-everyone-suddenly-talking-about-it|🦸🏻#14: What Is MCP, and Why Is Everyone – Suddenly!– Talking About It?]]: Anthropic announced Model Context Protocol (MCP) in November 2024 as an open standard to bridge AI a
- **2025-03-10** — [[sources/01KJVP51TK-before-you-call-manus-ai-agent-a-gpt-wrapper|Before you call Manus AI Agent, a GPT Wrapper!]]: Users interacting with Manus only communicate with the executor agent, not the knowledge or planner 
- **2025-03-09** — [[sources/01KJV3DVFC-agent-models-internalizing-chain-of-action-generation-into-reasoning-models|Agent models: Internalizing Chain-of-Action Generation into Reasoning models]]: Traditional agentic workflows rely on external prompts to manage interactions with tools and the env
- **2025-03-06** — [[sources/01KJV3G6RY-start-self-taught-reasoner-with-tools|START: Self-taught Reasoner with Tools]]: START achieves 95.0% on AMC23, a +15.0% absolute improvement over QwQ-32B-Preview.
- **2025-03-02** — [[sources/01KJV3PQ9W-a-law-reasoning-benchmark-for-llm-with-tree-organized-structures-including-factu|A Law Reasoning Benchmark for LLM with Tree-Organized Structures including Factum Probandum, Evidence and Experiences]]: The crowd-sourced dataset contains 453 cases, 2,627 factum probandum, 14,578 pieces of evidence, and
- **2025-03-01** — [[sources/01KJVKF0RR-building-agents-with-model-context-protocol-full-workshop-with-mahesh-murag-of-a|Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag of Anthropic]]: MCP does not replace agent frameworks; it complements them by providing a standardized layer for bri
- **2025-02-07** — [[sources/01KJV4D04E-agentic-reasoning-a-streamlined-framework-for-enhancing-llm-reasoning-with-agent|Agentic Reasoning: A Streamlined Framework for Enhancing LLM Reasoning with Agentic Tools]]: The Mind-Map agent constructs a knowledge graph from the reasoning chain to store and structure real
- **2025-01-22** — [[sources/01KJTNEFKK-acebench-who-wins-the-match-point-in-tool-usage|ACEBench: Who Wins the Match Point in Tool Usage?]]: ACEBench covers 8 major domains and 68 sub-domains with a collection of 4,538 APIs in both Chinese a
- **2025-01-09** — [[sources/01KJV5B2QG-search-o1-agentic-search-enhanced-large-reasoning-models|Search-o1: Agentic Search-Enhanced Large Reasoning Models]]: Search-o1 integrates an agentic RAG mechanism and a Reason-in-Documents module into the LRM reasonin
- **2025-01-07** — [[sources/01KJSWNT7B-agents|Agents]]: Chameleon improves the best-published few-shot result on ScienceQA by 11.37%.
- **2024-12-06** — [[sources/01KJVKFYWV-anthropics-claude-computer-use-is-a-game-changer-yc-decoded|Anthropic’s Claude Computer Use Is A Game Changer | YC Decoded]]: Computer use is vulnerable to prompt injection attacks, where malicious instructions embedded in vis
- **2024-10-22** — [[sources/01KJSXQAC8-when-you-give-a-claude-a-mouse|When you give a Claude a mouse]]: Claude's computer use agent operated for nearly an hour without human interruption during the Paperc
- **2024-09-26** — [[sources/01KKTF8ZRH-ai-agents-a-new-architecture-for-enterprise-automation-menlo-ventures|AI Agents: A New Architecture for Enterprise Automation | Menlo Ventures]]: New capability: Tool use / function calling enabling LLMs to invoke web browsing, code interpret
- **2024-09-26** — [[sources/01KKTFEAY1-beyond-bots-how-ai-agents-are-driving-the-next-wave-of-enterprise-automation-men|Beyond Bots: How AI Agents Are Driving the Next Wave of Enterprise Automation | Menlo Ventures]]: AI agents sit as decision engines at the center of application control flow, unlike RPA bots with ha
- **2024-07-25** — [[sources/01KJSYGVN2-building-a-generative-ai-platform|Building A Generative AI Platform]]: RAG consists of two components: a generator (e.g. a language model) and a retriever.
- **2024-07-16** — [[sources/01KJVCP8BF-reflection-ais-misha-laskin-on-the-alphago-moment-for-llms-training-data|Reflection AI’s Misha Laskin on the AlphaGo Moment for LLMs | Training Data]]: Language models were not trained for agency; they were trained for chat interaction and predicting t
- **2024-02-01** — [[sources/01KJV9HBN6-executable-code-actions-elicit-better-llm-agents|Executable Code Actions Elicit Better LLM Agents]]: There is a large performance gap between open-source and closed-source LLMs on CodeAct tasks: the be
- **2023-09-18** — [[sources/01KJVR48TZ-miles-grimshaw-the-5-pillars-of-venture-capital-why-co-pilot-is-an-incumbent-str|Miles Grimshaw: The 5 Pillars of Venture Capital & Why Co-Pilot is an Incumbent Strategy | E1061]]: The speaker prefers the concept of 'founder respect' over 'founder friendly', arguing that true resp
- **2023-05-25** — [[sources/01KJVC2MPT-voyager-an-open-ended-embodied-agent-with-large-language-models|Voyager: An Open-Ended Embodied Agent with Large Language Models]]: VOYAGER interacts with GPT-4 via blackbox queries, bypassing the need for model parameter fine-tunin
