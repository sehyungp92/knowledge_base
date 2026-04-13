---
type: source
title: Thinking, Searching, and Acting
source_id: 01KJS34J20X9DH54QG8V2YV7W1
source_type: article
authors: []
published_at: '2025-09-22 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinking, Searching, and Acting

**Authors:** 
**Published:** 2025-09-22 00:00:00
**Type:** article

## Analysis

# Thinking, Searching, and Acting
2025-09-22 · article
https://www.interconnects.ai/p/thinking-searching-and-acting

---

## Briefing

**Modern reasoning models are not merely smarter chatbots — they represent a durable new infrastructure class defined by three co-equal primitives: Thinking (inference-time compute via reasoning traces), Searching (retrieval from non-parametric stores), and Acting (code execution and real-world manipulation). Inference-time scaling was the catalytic step-change that made all three viable simultaneously, and the industry is now in the early infrastructure-building phase of a transition that will last far longer than the static-weights era it replaced.**

### Key Takeaways
1. **Three primitives define the reasoning model era** — Thinking, Searching, and Acting are not features but structural pillars; all frontier AI systems of the coming years will embody all three.
2. **Convergence happened fast** — OpenAI's o3 unified all three primitives within just 3-6 months of o1-preview's September 2024 release, far faster than the broader industry adapted.
3. **Hallucinations are a different problem now** — With search, hallucinations shift from generating false content to retrieving missing context, requiring entirely different study and mitigation approaches.
4. **Inference-time scaling was the unlock** — Reasoning traces were not just a capability upgrade; they were the step-change event that made search and tool use far more functional, catalyzing all three primitives.
5. **Tool quality now rivals model quality** — Improving the tools embedded with a reasoning model is arguably more tractable than improving the model itself, though it demands substantial engineering.
6. **Open vs. closed models face a structural asymmetry** — Closed models control one unified inference stack; open models must generalize across many search products and deployment contexts, making MCP-style standardization critical.
7. **Reasoning model cost increases were a one-time step, not a trend** — The widely-cited 1000x cost increase reflected a singular moment of industry-wide adoption, not a compounding trajectory; hardware improvements (Blackwell) will normalize costs.
8. **Standard tokenomics are broken for tool-augmented inference** — Hidden costs like search index queries and idle GPU time waiting for tool results dwarf the token-count concerns that dominate public discussion.
9. **Parameter scaling has hit diminishing returns** — GPT-4.5's non-frontier status and Gemini Ultra's non-release both signal the same inflection point; reasoning token scaling will follow the same curve.
10. **The future cost pressure is on agents, not base models** — As base model inference gets cheaper, the rising costs will be parallel-inference agent products like Claude Code and OpenAI's rumored Pro offerings.
11. **Diffusion LMs cannot replace transformers for reasoning** — Parallel token generation precludes sequential tool integration, making transformer-based architectures structurally superior for the thinking-searching-acting paradigm.
12. **The infrastructure layer matters more than the weights** — Modern AI systems depend on the quality of the entire inference stack far more than on optimal training runs for model weights alone.

---

### The Three Primitives of Reasoning Models

- **Thinking** refers to the extended reasoning traces that enable inference-time scaling, not a direct analog to human cognition.
  - The terminology (Chain of Thought, "Thinking models") is human-inspired but the actual mechanism is fundamentally different from human reasoning.
  - Thinking traces are the foundational primitive that made the other two primitives functional — without them, search and acting integration remained limited.

- **Searching** addresses the core structural tension in language models: weights are static but the world is dynamic.
  - Search is access to non-parametric knowledge stores designed specifically for the model, queried at inference time.
  - Search can be argued to be a form of execution itself, but because the information retrieved is uniquely imperative, it warrants its own category separate from code execution.

- **Acting** allows models to manipulate the physical or digital world, overcoming the nondeterminism of their core.
  - Code execution is the current primary form; real robotics represents the long-term trajectory.
  - Most executable environments for acting will be built on top of infrastructure developed for coding agents specifically.
  - **All future tools accessible to language models will be subsets of either code or search** — no fundamentally new primitive category is anticipated.

- These three primitives are expected to define AI infrastructure for years to come, outlasting the static-weights paradigm that produced and preceded ChatGPT.

---

### A Spectrum of Reasoning Models, Not a Single Profile

- The long-reasoning traces and tool use can be crafted to fit different profiles, yielding a spectrum rather than one dominant style.
  - **Aggressive end (OpenAI o3, GPT-5 Thinking "Research Goblin", xAI Grok 4):** Described as "a dog determined to chase their goal indefinitely," burning substantial compute to maximize search depth and reasoning length.
  - **Softer end (Claude 4):** Applies a much softer touch — less adept at search, but almost always returns a faster answer; represents a different but valid trade-off.

- The most similar follow-up to o3 on the search-forward approach was xAI's Grok 4; Claude 4 expresses its reasoning model nature in a "far more nuanced manner."

- The author's taxonomy for evaluating reasoning models across this spectrum involves four traits:
  - **Skills:** Core reasoning intelligence.
  - **Calibration:** The ability to not overthink — knowing when to stop.
  - **Strategy:** Choosing the right solution approach from available options.
  - **Abstraction:** Breaking complex problems into tractable subproblems.

---

### How Halluc

## Key Claims

1. Modern reasoning models are built on three fundamental primitives: Thinking (reasoning traces enabling inference-time scaling), Searching (access to non-parametric knowledge stores), and Acting (manip
2. The 'thoughts' of a reasoning model take a very different form than human thoughts that inspired the terminology like Chain of Thought or Thinking models.
3. Search addresses the fundamental limitation that model weights are static while the world is dynamic.
4. Acting via code execution allows language models to contact reality and overcome their nondeterministic core.
5. Most executable environments for acting will build on top of infrastructure developed for coding agents.
6. OpenAI's o1-preview was released on September 12, 2024.
7. Early criticism that reasoning models 'won't generalize' has turned out to be false.
8. With OpenAI's o3, the three primitives of reasoning models converged within only 3-6 months of o1's release.
9. OpenAI's o3 and xAI's Grok 4 aggressively pursue goals while burning substantial compute, whereas Claude 4 applies a softer approach and returns faster answers at the cost of being less adept at searc
10. The functional traits of next-generation reasoning models are: skills for reasoning intelligence, calibration to not overthink, strategy to choose the right solutions, and abstraction to break them do

## Capabilities

- Frontier reasoning models from multiple labs (o3, Grok 4, Claude 4) have converged on integrating Thinking (inference-time chain-of-thought), Searching (non-parametric retrieval), and Acting (tool execution/code) as a unified paradigm — within 3-6 months of o1's release
- Reasoning model behaviour can be tuned across a spectrum from compute-intensive deep search (o3, Grok 4) to faster softer-touch reasoning (Claude 4) by adjusting reasoning trace length and tool use intensity
- Search-integrated reasoning models achieve near-perfect verbatim content copying and solid referencing accuracy — hallucinations have shifted from false-fact confabulation to missing-context gaps

## Limitations

- Long-context understanding remains severely flawed even in search-augmented reasoning models — retrieval can locate content but models still fail to synthesize and reason across large retrieved contexts
- Diffusion language models cannot integrate tools (search, code execution) in the same way autoregressive models can, blocking their path to becoming full reasoning models despite efficiency advantages from parallel token generation
- Serial reasoning token scaling exhibits diminishing returns — sequential chain-of-thought length can no longer be the primary lever for reasoning quality improvement
- Open-weight models face a structural tool-integration disadvantage: trained with one search engine but deployed into a heterogeneous ecosystem, requiring generalization that closed models never need
- Standard tokenomics metrics are deeply misleading for tool-using reasoning models — search index costs, idle GPU time during tool execution, and inference variance from tool latency are invisible in per-token cost figures
- Idle GPU compute during tool execution represents an unaccounted and unoptimised cost inefficiency in reasoning model serving — GPUs sit idle waiting for external search or code execution results
- Agent-scale costs are projected to increase even as base model costs fall — parallel inference requirements for agentic workloads create a cost trajectory opposite to single-user model serving
- Reasoning model infrastructure for agents is in early days — robust deterministic computing and search primitives to fully enable thinking+searching+acting systems have not yet been built out
- Hallucinations in search-augmented models — now manifest as context gaps rather than false facts — require entirely different evaluation and mitigation strategies that are not yet established

## Bottlenecks

- Serial reasoning token scaling hitting diminishing returns blocks continued quality improvement via simple chain-of-thought lengthening — parallel inference is the emerging workaround but introduces cost and infrastructure challenges
- Open-weight model generalisation across heterogeneous tool ecosystems blocks open models from matching closed model reasoning quality on search-augmented and tool-using tasks
- Idle GPU compute during tool execution and unquantified non-token serving costs create opaque cost barriers for production agentic deployments — the industry lacks even accurate cost models for these workloads

## Breakthroughs

- Convergence of Thinking, Searching, and Acting into a unified reasoning model paradigm — multiple frontier labs integrated all three primitives within 3-6 months of o1's release, establishing a new durable infrastructure layer for AI
- Hallucination character transformation: search integration structurally changes hallucinations from confabulated false facts to missing-context gaps — a qualitatively different failure mode requiring different evaluation and mitigation

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain of Thought (CoT)]]
- [[entities/claude-4|Claude 4]]
- [[entities/claude-code|Claude Code]]
- [[entities/diffusion-language-model|Diffusion language model]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/openai-o3|OpenAI o3]]
- [[entities/sglang|SGLang]]
