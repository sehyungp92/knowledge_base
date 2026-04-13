---
type: source
title: 'Context Engineering for AI Agents: Lessons from Building Manus'
source_id: 01KJS48D4HARDHAAK6D1NZ9847
source_type: article
authors: []
published_at: None
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- in_context_and_meta_learning
- knowledge_and_memory
- post_training_methods
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Context Engineering for AI Agents: Lessons from Building Manus

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Context Engineering for AI Agents: Lessons from Building Manus
article
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

---

## Briefing

**Context engineering — the deliberate shaping of what goes into an LLM's context window — is the core discipline of production agentic systems, more impactful than model choice or prompt tricks alone. The Manus team argues that betting on in-context learning over fine-tuning enables rapid iteration, and that six specific engineering patterns (KV-cache optimization, masked action spaces, file-system memory, attention manipulation via recitation, error preservation, and diversity injection) collectively determine agent reliability and cost at scale. This matters because it shifts the framing from "which model is best" to "how do you engineer the environment the model operates in."**

### Key Takeaways
1. **Bet on in-context learning over fine-tuning** — Fine-tuning locks you into week-long iteration cycles; context engineering lets you ship improvements in hours and keeps the product model-agnostic as the frontier advances.
2. **KV-cache hit rate is the single most important production metric** — With Claude Sonnet, cached tokens cost $0.30/MTok vs. $3.00/MTok uncached — a 10x difference that compounds at Manus's ~100:1 input-to-output token ratio.
3. **Stable, append-only context prefixes are essential for cache efficiency** — Even a single token change (e.g., a per-second timestamp) invalidates the entire downstream cache, silently destroying cost and latency.
4. **Mask tool logits instead of removing tools dynamically** — Removing tools mid-iteration breaks the KV-cache and confuses the model when prior observations reference undefined tools; logit masking preserves the definition space while constraining selection.
5. **The file system is the correct solution to context length limits** — Unlike truncation or compression, file-based externalization is fully restorable; the agent learns to write and retrieve from files as structured external memory.
6. **Recitation of goals into the recent context window counteracts "lost-in-the-middle" drift** — Manus's todo.md update pattern is a deliberate attention manipulation mechanism, not cosmetic behavior.
7. **Leaving errors in the context is more effective than hiding them** — Failed actions and stack traces shift the model's prior away from repeating mistakes; error recovery is a key indicator of genuine agentic capability.
8. **Uniform context patterns cause behavioral drift via implicit few-shot mimicry** — When action-observation pairs are too homogeneous, the model imitates the pattern even when it's no longer optimal; structured variation breaks this.
9. **Response prefill enables action space control without tool redefinition** — Three modes (auto, required, specified) let you constrain what the model calls by prefilling the assistant turn, not by modifying tool schemas.
10. **SSMs with file-based memory could be a viable path to efficient agentic architectures** — If state space models could master external file memory to compensate for their lack of full attention, they might combine SSM speed with Transformer-level agentic capability.
11. **"Stochastic Graduate Descent" is the honest characterization of agent architecture search** — Four full framework rewrites at Manus reflect that context engineering is empirical, not principled; convergence comes from iteration, not theory.

---

### The Strategic Case for In-Context Learning Over Fine-Tuning

- The Manus team faced a foundational build decision: train an end-to-end agentic model on open-source foundations, or build on top of frontier models via in-context learning.
  - Historical experience with BERT-era fine-tuning meant weeks-per-iteration cycles even for small models — a fatal feedback loop for pre-PMF products.
  - The author's prior startup trained models from scratch for open information extraction and semantic search, only to be made irrelevant overnight by GPT-3 and Flan-T5.
  - **The lesson: betting on proprietary fine-tuned models is betting against the tide of model progress.**
- Choosing context engineering decouples product improvement velocity from model retraining cycles.
  - Improvements ship in hours, not weeks.
  - The product remains orthogonal to underlying models — as the author puts it, "if model progress is the rising tide, we want Manus to be the boat, not the pillar stuck to the seabed."
- Context engineering is nonetheless non-trivial and empirical — Manus rebuilt its agent framework four times.
  - The team calls their process "Stochastic Graduate Descent": architecture searching, prompt fiddling, and empirical guesswork.
  - This post represents local optima found through that process, not universal truths.

---

### KV-Cache Optimization: The Economics of Production Agents

- **KV-cache hit rate is the single most important metric for production-stage AI agents**, directly affecting both latency (TTFT) and inference cost.
- The agent loop creates a highly skewed prefill-to-decode ratio.
  - Each iteration appends action + observation to a growing context; outputs (structured function calls) remain short.
  - Manus's average input-to-output token ratio is approximately **100:1** — far beyond typical chatbot ratios.
  - This makes the per-token economics of caching extremely consequential at scale.
- **Claude Sonnet pricing illustrates the stakes**: cached input tokens cost $0.30/MTok; uncached cost $3.00/MTok — a **10x difference**.
- Key practices for maximizing KV-cache hit rate:
  - **Keep prompt prefixes stable.** LLM autoregression means a single differing token invalidates the cache from that point forward.
    - Common failure: including a timestamp precise to the second at the start of the system prompt. The model can tell you the time, but the cache hit rate collapses.
  - **Make context append-only.** Never modify prior actions or observations retroactively.
    - Seri

## Key Claims

1. KV-cache hit rate is the single most important metric for a production-stage AI agent, directly affecting both latency and cost.
2. In agentic systems, the input-to-output token ratio is highly skewed compared to chatbots; in Manus the average ratio is approximately 100:1.
3. With Claude Sonnet, cached input tokens cost 0.30 USD/MTok versus 3 USD/MTok for uncached tokens, a 10x cost difference.
4. Including a timestamp precise to the second at the beginning of a system prompt destroys KV-cache hit rate due to LLM autoregressive nature.
5. Non-deterministic JSON serialization (e.g., unstable key ordering) can silently break KV-cache in agent contexts.
6. Dynamically adding or removing tools mid-iteration degrades agent performance by invalidating KV-cache and causing model confusion about undefined tool references.
7. Masking token logits during decoding to constrain action selection is more effective than removing tools from the context.
8. Consistent action name prefixes (e.g., browser_, shell_) enable easy group-level tool constraint enforcement during decoding without stateful logits processors.
9. Even with 128K+ token context windows, real-world agentic tasks regularly exceed context limits and suffer performance degradation at long contexts.
10. Irreversible context compression carries fundamental risk because it is impossible to reliably predict which observation will become critical many steps later.

## Capabilities

- KV-cache optimization for production AI agents achieves 10x inference cost reduction — cached tokens cost $0.30/MTok vs $3/MTok uncached on Claude Sonnet
- Context-aware state machine with token logit masking constrains agent action selection to valid tool subsets without modifying tool definitions or breaking KV-cache
- File system as restorable external agent memory: agents write and read files on demand, enabling context compression without permanent information loss — URLs and file paths serve as pointers to dropped content
- Goal-alignment maintenance across 50+ tool call sequences via continuous todo recitation — injecting objectives into recent context to combat lost-in-the-middle drift without architectural changes
- Error recovery via failure context preservation: leaving failed actions and stack traces in agent context shifts model priors away from repeated mistakes, improving multi-step task reliability in production
- Context diversity injection — structured variation in action/observation serialization templates and phrasing — breaks repetitive pattern mimicry in long-running batch agent tasks

## Limitations

- Context windows of 128K+ tokens are insufficient for real-world agentic scenarios: observations from web pages and PDFs trivially exceed limits, and performance degrades before the hard limit is reached
- KV-cache is invalidated by single-token prefix changes — including timestamps in system prompts — causing 10x cost regressions that are silent and easy to introduce inadvertently
- Non-deterministic JSON serialization (unstable key ordering) silently breaks KV-cache and causes hidden latency and cost regressions in production agent systems
- Tool count explosion from MCP adoption degrades agent reliability: exposing hundreds of user-configured tools to an agent increases wrong-action selection and path inefficiency
- Dynamic tool loading/removal mid-iteration breaks KV-cache and causes model confusion when action history references tools no longer in the context, leading to schema violations and hallucinated actions
- Long agentic loops (~50 tool calls) cause goal drift — models forget earlier objectives in long contexts and drift off-topic even when technically within context window limits
- Agent self-few-shotting: repetitive action-observation pairs in uniform context cause models to mirror observed patterns even when the pattern is suboptimal, producing drift, overgeneralization, and hallucination in batch tasks
- Long context inputs remain expensive even with prefix caching: every token must still be transmitted and prefilled per iteration, so linear context growth creates unavoidable cost scaling
- 100:1 input-to-output token ratio in production agents creates severe TTFT latency and cost pressure — fundamentally different from chatbot workloads and creating a distinct inference serving challenge
- Any irreversible context compression is fundamentally risky in multi-step agents because relevance of any prior observation to future steps cannot be predicted at compression time
- SSMs cannot handle long-range backward dependencies, preventing direct adoption as agentic LLMs despite superior speed and efficiency — they would require file-based memory externalisation to compensate
- Error recovery as an agentic capability is systematically absent from academic benchmarks, which evaluate only task success under ideal conditions — creating a blind spot in capability assessment
- Context engineering for production agents is empirically intractable — no principled design method exists, requiring repeated architectural rewrites and manual 'Stochastic Graduate Descent'

## Bottlenecks

- Context management for long-horizon production agents is unsolved at scale: 50+ tool-call tasks face compounding costs from linear context growth, KV-cache sensitivity to any prefix mutation, and the fundamental impossibility of safe irreversible compression
- MCP-driven tool proliferation has no principled solution: user-configurable ecosystems expose hundreds of tools to agents, but no approach maintains selection accuracy at that scale without static masking workarounds that themselves introduce constraints
- No principled methodology for context engineering: optimal agent context design can only be found through exhaustive empirical search, creating 4+ framework rebuild cycles even for expert practitioners

## Breakthroughs

- Context engineering validated as a production discipline matching model-level improvements: a systematic set of principles (KV-cache optimization, state-machine masking, file-system memory, attention recitation, error preservation, diversity injection) enables stable multi-step agents at millions-of

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/in_context_and_meta_learning|in_context_and_meta_learning]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/context-engineering|Context Engineering]]
