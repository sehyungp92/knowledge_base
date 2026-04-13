---
type: source
title: 'Universal Deep Research: Bring Your Own Model and Strategy'
source_id: 01KJTM33JCSNTRYDT4JYQWBZE9
source_type: paper
authors:
- Peter Belcak
- Pavlo Molchanov
published_at: '2025-08-29 00:00:00'
theme_ids:
- agent_systems
- context_engineering
- knowledge_and_memory
- retrieval_augmented_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Universal Deep Research: Bring Your Own Model and Strategy

**Authors:** Peter Belcak, Pavlo Molchanov
**Published:** 2025-08-29 00:00:00
**Type:** paper

## Analysis

# Universal Deep Research: Bring Your Own Model and Strategy
2025-08-29 00:00:00 · paper · Peter Belcak, Pavlo Molchanov
https://arxiv.org/pdf/2509.00244

---

### Motivation & Prior Limitations
- Existing deep research tools (DRTs) hard-code both their research strategy and their choice of underlying language model, leaving users with no meaningful control over the research process beyond writing the prompt itself.
  - Consumer tools like Gemini, Perplexity, and OpenAI Deep Research all follow fixed iterative web-crawling strategies with no user-configurable logic; enterprise tools like SambaNova and NVIDIA AI-Q use fixed multi-step pipelines with no interchangeable model support.
- The rigidity of existing DRTs creates three distinct problems: users cannot enforce resource hierarchies or manage search costs (P1), specialized high-value industries cannot create domain-specific research strategies without bespoke agentic development (P2), and the best available models cannot be freely paired with the best available DRT (P3).
- The gap between consumer and enterprise DRTs exists partly because enterprise research requires specialized, controllable strategies that current consumer tools structurally cannot support.

---

### Proposed Approach
- Universal Deep Research (UDR) is a generalist agentic system that accepts both a user-defined natural language research strategy and a research prompt as inputs, converting the strategy into executable code that orchestrates the research process without requiring any model fine-tuning.
  - Unlike prior DRTs where the LLM acts as the orchestrating agent, UDR relegates the LLM to a callable utility for localized reasoning tasks (summarization, extraction, ranking); all control flow is handled by generated CPU-executable code, not by live LLM reasoning.
  - The strategy compiler converts the natural language strategy into a single callable Python generator function, with each strategy step explicitly annotated by comments in the generated code — a design choice found to prevent the model from skipping steps, taking shortcuts, or imposing spurious constraints.
- Intermediate state is stored as named variables in the code execution environment rather than in a growing LLM context window, enabling full research workflows to complete within a context of approximately 8,000 tokens regardless of workflow complexity.
- Code execution runs in a sandboxed isolated environment (e.g., Piston) to prevent prompt injection and code-based exploits from affecting the host system, which the authors identify as a strict deployment requirement.
- The system is model-agnostic by design: any sufficiently capable general-purpose language model can serve as the underlying LLM without modification or fine-tuning.

---

### Results & Capabilities
- UDR successfully executes custom research workflows using three example strategies of varying depth — minimal, expansive, and intensive — demonstrating that the architecture generalizes across different research approaches without strategy-specific training.
  - The authors report that generating the full strategy as a single end-to-end code pass was significantly more reliable than earlier approaches (prompting a reasoning model directly, or generating isolated code fragments per step), which exhibited failure modes including step skipping, out-of-sequence LLM invocations, and spurious constraint injection.
- The 8k-token context ceiling for full workflow execution is presented as a qualitative efficiency result: by storing state in code variables rather than the LLM context, the system avoids the context-window scaling problem that typically afflicts long agentic workflows.
- A demonstration user interface was developed and is publicly released alongside the code, providing strategy editing, real-time progress notifications via structured yield streams, mid-execution stop-and-report capability, and Markdown report rendering.

---

### Implications
- UDR demonstrates that deep research capability is separable from any particular model, meaning DRT quality and model quality can evolve and compete independently — a structural shift that could commoditize the research-agent layer and intensify competition at the model layer.
- The architecture generalizes the notion of "programming agent behavior in natural language": users define control flow, tool use, and decision logic through prose strategies that are compiled to deterministic code, suggesting a broader design pattern applicable beyond research to any structured agentic workflow.
- For high-value professional domains (finance, legal, healthcare, real estate, government), UDR removes the current barrier that forces organizations to commission bespoke agentic systems for specialized document research, potentially democratizing access to automation in these sectors.
- The authors explicitly recommend that future systems expose user control over LLM "thinking" or reasoning processes (R2) and explore automatic conversion of large sets of user prompts into deterministically controlled agents (R3), pointing toward a research agenda around user-programmable agency.

---

### Remaining Limitations & Next Steps
- The faithfulness of UDR's execution to the user's intended strategy depends on the quality of code generated by the underlying language model; semantic drift or hallucinated logic can still occur with ambiguous or underspecified strategies, and the system provides no automated validation of strategy coherence or correctness.
  - The authors explicitly note this as a limitation tied to LLM code generation quality, and their mitigation (comment-code structure enforcement) reduces but does not eliminate the problem.
- UDR currently offers no mid-execution interactivity beyond a full stop: users cannot provide feedback, redirect the research, or trigger dynamic branching during an active workflow, which limits adaptability for exploratory or open-ended research tasks.
  - All decision

## Key Claims

1. Each deep research agent introduced so far is hard-coded to carry out a particular research strategy using a fixed choice of tools.
2. UDR wraps around any language model and enables users to create custom deep research strategies without any additional training or finetuning.
3. Deep research tools are among the most impactful and most commonly encountered agentic systems today.
4. Gemini, Perplexity, and OpenAI Deep Research tools transform user prompts into a research plan and analyze the web by browsing autonomously through iterative search.
5. Grok 3 DeepSearch employs a two-tier crawling architecture where a distributed network of crawler bots continuously indexes the web and an on-demand agent performs targeted searches at query time.
6. Enterprise-focused DRTs employ considerably more specialized approaches than consumer-facing ones because their source space is limited to internal document databases rather than the entire web.
7. ERP AI Deep Research uses a Graph-Based AI Architecture that represents enterprise data through knowledge graphs accessed via Graph Neural Networks, forgoing the traditional document/page notion of so
8. Existing DRTs restrict user ability to enforce a hierarchy of preferred resources, automate cross-validation against reputable sources, and control search expenses.
9. Existing DRTs do not allow users to create specialized document research strategies, leaving high-value industries such as finance, legal, healthcare, and real estate to rely on costly bespoke agentic
10. Models used in existing DRTs are not interchangeable, preventing users from pairing the most capable model with the best research agent.

## Capabilities

- Commercial deep research tools (Gemini, Perplexity, OpenAI Deep Research, Grok 3 DeepSearch) can autonomously browse the web iteratively, cross-validate sources, and produce structured research reports
- Enterprise-focused deep research tools can follow structured multi-step document research pipelines with section-level planning, specialized sub-agents, and citation-grounded Markdown reports
- Natural language research strategies can be compiled into deterministic executable agent code by a language model without any fine-tuning, enabling model-agnostic customisable deep research
- Code-based agent orchestration (separating control logic from LLM reasoning) can execute full complex research workflows within an 8k token context window by storing intermediate state in code variables
- Graph Neural Network-based enterprise data research using knowledge graphs can replace traditional document/page traversal for organisations with graph-structured internal data

## Limitations

- LLM code generation faithfulness to user-defined strategies degrades with ambiguity: semantic drift, hallucinated logic, skipped steps, and spurious constraints are observed failure modes
- LLMs given free rein over agentic orchestration systematically skip steps, take shortcuts, and impose unsolicited constraints — reliable execution requires heavy structural scaffolding to override this tendency
- Agent orchestration using LLMs is orders of magnitude more expensive than CPU-executable code orchestration; existing DRTs incur unnecessary GPU costs by using LLMs to control the full research process
- No mid-execution user intervention or dynamic branching based on real-time feedback is possible in current agent research workflows; all decision logic must be encoded upfront, blocking adaptability in exploratory tasks
- Designing sophisticated research strategies that handle the full complexity of real user queries is cognitively demanding, limiting adoption of customisable agent systems even among appreciative users
- Current DRTs do not validate whether user-specified agent strategies produce coherent or meaningful workflows; poorly designed strategies silently yield incomplete or absent reports
- Sandboxed code execution is a strict deployment requirement for any agent system executing user-defined code beyond a fully trusted audience — this constraint blocks frictionless broad consumer deployment
- Existing DRTs do not allow interchangeable models — users cannot pair the most capable available model with a preferred deep research framework, creating artificial capability ceilings
- Current DRT tools do not support asynchronous tool use, preventing parallel execution of search and retrieval operations that would reduce latency in research workflows
- The functionality gap between consumer and enterprise DRTs is structurally enforced by the inability to customise resource hierarchies, automate cross-validation, and control per-search costs within consumer tools
- Specialised document research strategies required by high-value industries (finance, legal, healthcare) cannot be created within existing DRTs, leaving large professional research workloads to bespoke expensive agentic solutions

## Bottlenecks

- Hard-coded research strategies in all existing DRTs block enterprise customisation, industry-specific workflows, and best-of-breed model-framework pairings — requiring costly bespoke agentic solutions for professional use
- LLM-as-orchestrator architecture in DRTs incurs orders-of-magnitude higher GPU inference costs than necessary, as orchestration logic that could run on CPU is executed through expensive LLM calls
- User cognitive load for specifying complex agent behaviours in natural language is a practical adoption bottleneck for customisable agentic systems — even technically appreciative users struggle to create robust strategies

## Breakthroughs

- Code-as-orchestrator architecture demonstrates that complex multi-step research agent workflows can execute entirely within an 8k token context window by storing state in code variables rather than the LLM context

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/prompt-injection|Prompt Injection]]
