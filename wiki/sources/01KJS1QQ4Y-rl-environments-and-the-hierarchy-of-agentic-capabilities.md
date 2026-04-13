---
type: source
title: RL Environments and the Hierarchy of Agentic Capabilities
source_id: 01KJS1QQ4YJK5XJV2G84HF569C
source_type: article
authors: []
published_at: None
theme_ids:
- agent_evaluation
- agent_systems
- evaluation_and_benchmarks
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# RL Environments and the Hierarchy of Agentic Capabilities

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# RL Environments and the Hierarchy of Agentic Capabilities
article
https://surgehq.ai/blog/rl-envs-real-world

---

## Briefing

**Nine AI models were evaluated on 150 real-world customer support tasks inside a realistic RL environment (Corecraft, Inc.), revealing that even the top performers — GPT-5 and Claude Sonnet 4.5 — fail over 40% of tasks. The authors propose the Hierarchy of Agentic Capabilities as a diagnostic framework, arguing that common sense reasoning is the final and least-understood barrier separating current models from human-level agents, and that 2025 is the year agents became coherent enough to even begin studying that barrier.**

### Key Takeaways
1. **Top models still fail 40%+ of tasks** — GPT-5 and Claude Sonnet 4.5 lead by a wide margin but both fail more than 4 in 10 tasks in a realistic customer support environment, making economic deployment highly dependent on task type and failure tolerance.
2. **A natural capability hierarchy emerges from failure analysis** — Models' failures cluster predictably around four levels: basic tool use & planning, adaptability, groundedness, and common sense reasoning — suggesting a developmental sequence for agentic training.
3. **Tool use failures are definitional, not incidental** — Models that can't reliably map prompt information to correct tool arguments, or follow MCP schemas, aren't agents; they're chatbots with tool access — GPT-4o, Mistral Medium, and Nova 1 Pro all exhibited this.
4. **Adaptability means updating the plan when reality pushes back** — Gemini 2.5 and Qwen3 models showed correct initial plans but failed to replan when tool calls returned empty or unexpected results, instead treating null results as ground truth.
5. **Groundedness failures are the subtlest and most dangerous** — Kimi K2 Turbo searched the wrong year despite it being stated in the system prompt; Claude hallucinated an email address mid-task; both are failure modes that can slip undetected into final outputs.
6. **Common sense reasoning is the gap between GPT-5 and human-level** — GPT-5's failures at this tier weren't tool or planning errors but inferences that a human would make trivially: recognizing that "the package showed up a few hours ago" means a return, not a cancellation.
7. **RL environments should be grown, not designed top-down** — Effective training environments are populated by domain experts drawing on real experience, not engineered abstractly — Corecraft, Inc. was built by "Surgers" with customer support expertise.
8. **Customer support is a strategically chosen evaluation domain** — It spans the full difficulty range from single-tool lookups to multi-system reasoning, making it a strong proxy for general-purpose agentic competence rather than a narrow benchmark.
9. **2025 is the year agents became coherent enough to study** — The year's significance is not that general-purpose agents were achieved, but that models now act reliably enough that their common sense reasoning failures can be isolated and analyzed for the first time.
10. **The hierarchy is diagnostic, not strictly sequential** — Capabilities overlap and co-develop; the framework's value is identifying where foundational work is still needed, not enforcing a linear training path.
11. **Strong adaptability partially compensates for groundedness failures** — Claude's ability to self-correct after hallucinating an email address demonstrates that meta-cognitive recovery is itself a measurable capability worth tracking.
12. **Common sense reasoning may be emergent, not trainable** — Whether it decomposes into identifiable subskills or arises from large-scale real-world training is an open question that will define the next stage of AI development.

---

### The Corecraft RL Environment: Design and Rationale

- Corecraft, Inc. is a simulated online retailer of high-performance PC parts and custom builds, serving as the evaluation world for agentic benchmarking.
  - The world model is the company itself; entities include customers, orders, support tickets, products, and all operational records.
  - The agent role evaluated is customer support — handling tasks from simple product lookups and policy questions to multi-step operational workflows requiring cross-system reasoning.
- Task difficulty spans a wide range by design, from trivially simple ("How many refunds were there in July 2025?") to complex multi-constraint reasoning ("compatibility warnings during final review... suggest the cheapest way to fix it").
  - This breadth is intentional: a role that spans difficulty levels is a better testbed for foundational agentic capabilities than one that is uniformly hard or easy.
- **RL environments are grown, not engineered.** Rather than designing the world top-down, domain-expert contributors ("Surgers") populate the environment with realistic entities and tasks based on their own professional experience.
  - This grounds the environment in real worker experience, not abstract simulation.
  - The result is an environment shaped by the same kinds of people the agent is meant to work alongside — a form of ecological validity that purely synthetic benchmarks lack.
- The evaluation covered 150 tasks across nine AI models, with a December 2025 update adding results for newly released models on the same task set.

### Benchmark Results and Model Positioning

- **GPT-5 and Claude Sonnet 4.5 are in a distinct performance tier**, but both still fail over 40% of tasks — the gap between leading and trailing models is large, but the absolute performance ceiling remains well below human-level.
- GPT-4o, Mistral Medium, and Nova 1 Pro clustered at the bottom, struggling with basic tool use and planning — the most foundational tier.
- Gemini 2.5 Flash, Gemini 2.5 Pro, and Qwen3 Max were in the middle tier, demonstrating solid planning but failing on adaptability when plans encountered unexpected real-world friction.
- Kimi K2 Turbo was positioned above the Gemini/Qwen tier on plannin

## Key Claims

1. GPT-5 and Claude Sonnet 4.5 outperform all other evaluated models on agentic tasks, but still fail over 40% of tasks.
2. In 2025, AI model training and evaluation has shifted from rating individual responses to assessing multi-step tasks with tool use.
3. 2025 is characterized as 'the year of RL environments' for model post-training.
4. Effective RL environments for agent training require a coherent world model, a set of entities with relationships, and a tool system for agent interaction.
5. RL environments for agent training must be grounded in real worker experience rather than abstract simulations to be effective.
6. The Hierarchy of Agentic Capabilities identifies five progressive levels: basic tool use and goal formation, planning, adaptability, groundedness, and common-sense reasoning.
7. GPT-4o, Mistral Medium, and Nova 1 Pro exhibit failures at the basic tool use and planning level.
8. Nova 1 Pro failed to correctly map task information to tool arguments, passing obviously incorrect values such as a literal string 'gold' as a customer ID.
9. GPT-4o failed to execute a complete multi-step plan, forgetting to search for 'paid' and 'pending' orders after correctly identifying 'fulfilled' ones.
10. Mistral Medium failed basic MCP schema adherence by passing an array where a string argument was expected.

## Capabilities

- Frontier models (GPT-5, Claude Sonnet 4.5) can reliably decompose multi-step tasks into sequential tool call chains and execute them coherently in realistic RL environments
- Frontier agents (Claude Sonnet 4.5) can detect plan failure mid-execution and adaptively try alternative tool call strategies without human intervention — e.g. reformulating search parameters after empty results
- Expert-contributed RL environments grounded in real worker experience enable agentic model training and evaluation on realistic multi-step operational tasks
- Agentic models can orchestrate chains of heterogeneous MCP tools (searchCustomers, searchOrders, searchProducts, validateBuildCompatibility) to complete complex customer support and operational workflows

## Limitations

- Even the top frontier models (GPT-5, Claude Sonnet 4.5) fail more than 40% of realistic multi-step agent tasks in RL environments
- Weaker models (Nova 1 Pro, Mistral Medium, GPT-4o) fail to correctly map prompt information to tool arguments and violate MCP schema constraints even on simple tasks
- Mid-tier models (Gemini 2.5, Qwen3) fail to adapt when tool calls return unexpected or empty results, accepting failures as ground truth rather than investigating alternatives
- Models (Kimi K2 Turbo, Claude Sonnet 4.5) lose grounding on temporal context and entity identity over long tool call sequences — hallucinating dates, fabricating IDs, or producing internally inconsistent final responses
- Common sense reasoning — inferring unstated but contextually obvious conclusions from available evidence — remains a hard failure mode even for GPT-5, blocking human-level agent performance
- Subtle grounding errors in final responses are hard to detect and slip through into delivered answers — models may repeat items under wrong categories or produce internally incoherent outputs without self-correction
- Models select inefficient or incoherent plans even when better strategies are available — both GPT-5 and Claude iterated through 31 days of orders one day at a time rather than filtering by product category as the tools permitted
- Models fail to use task context to resolve lexical ambiguity in prompts — GPT-5 parsed 'my name under my account should be set to Sarah Kim' as an update instruction rather than an identity cue, ignoring task-coherence signals
- Evaluation is conducted in simulated RL environments rather than live production systems, leaving performance under genuine operational conditions — live data, consequential errors, adversarial users — unmeasured
- The nature of common sense reasoning is theoretically undefined — it is unknown whether it is a set of trainable subskills or an emergent property of scale — blocking targeted research and training investment
- Top models (GPT-5, Claude Sonnet 4.5) still exhibit occasional basic tool use and schema failures despite high overall capability, indicating reliability — not capability — is now the primary gap at the foundational layer

## Bottlenecks

- Common sense reasoning for agents is theoretically undefined — neither its structure nor its trainability is understood — blocking progress from capable-but-brittle to genuinely general-purpose agents
- Context grounding across long multi-step tool call sequences remains unreliable — models hallucinate IDs, misremember dates, and generate internally inconsistent responses — blocking safe production deployment
- Scarcity of real-world RL training environments grounded in authentic expert-contributed domain knowledge limits the quality of both agent training and evaluation

## Breakthroughs

- Frontier models (GPT-5, Claude Sonnet 4.5) have crossed a threshold of reliable agentic competence — sufficiently consistent in tool use, planning, adaptability, and groundedness that common sense reasoning is now the primary isolable bottleneck

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]
