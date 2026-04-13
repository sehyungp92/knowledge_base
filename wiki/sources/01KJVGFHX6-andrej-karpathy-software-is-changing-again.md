---
type: source
title: 'Andrej Karpathy: Software Is Changing (Again)'
source_id: 01KJVGFHX6QP2QMDYB093S055Y
source_type: video
authors: []
published_at: '2025-06-19 00:00:00'
theme_ids:
- agent_systems
- ai_software_engineering
- code_and_software_ai
- code_generation
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Andrej Karpathy: Software Is Changing (Again)

> Karpathy argues that software is undergoing its second fundamental paradigm shift in rapid succession — from human-written code (1.0) to learned neural network weights (2.0) to LLM-programmable natural language systems (3.0) — and draws extended analogies between LLMs and utilities, semiconductor fabs, and operating systems to characterize where the industry sits developmentally, concluding that we are in a ~1960s computing era whose personal computing revolution has not yet arrived.

**Authors:** Andrej Karpathy
**Published:** 2025-06-19
**Type:** video

---

## Software Paradigm Shifts

Karpathy's central thesis is that software has undergone two rapid, fundamental shifts after ~70 years of relative stability:

- **Software 1.0** — traditional human-written code; instructions explicitly authored for computers.
- **Software 2.0** — neural network weights produced by optimizing over datasets. The programmer's job shifts from writing logic to curating data and tuning optimizers. [[entities/hugging-face|Hugging Face]] is the GitHub equivalent of this paradigm — a repository for weights rather than code.
- **Software 3.0** — LLMs programmable via natural language. Prompts *are* programs. Anyone who speaks English can now write software.

The succession is not merely additive — each paradigm *eats* the prior. At Tesla Autopilot, growing neural network capability caused C++ code to be actively deleted as functionality migrated into weights. The same dynamic is now playing out with 3.0 consuming capabilities previously handled by both 1.0 and 2.0.

**Practical implication**: developers entering the field now must be fluent in all three paradigms and fluidly decide whether a given functionality is best expressed as written code, a trained model, or a prompt.

---

## LLMs as Infrastructure: Three Analogies

### Utilities
LLM labs spend significant capex to train models (building the grid), then serve intelligence via metered per-token APIs (paying for watts). Users demand low latency, high uptime, and consistent quality — identical expectations to electrical infrastructure. The significance: when state-of-the-art LLMs go down, it constitutes an *intelligence brownout* affecting global productivity. Tools like OpenRouter function as transfer switches between providers, analogous to grid/solar switching.

### Semiconductor Fabs
Frontier model training requires enormous capex, deep R&D, and proprietary secrets — structurally similar to chip fabrication. Companies training on proprietary hardware (Google/TPUs) resemble Intel's integrated model; those relying on NVIDIA GPUs resemble the fabless model. The analogy is imperfect: software is more malleable and less defensible than silicon.

### Operating Systems (strongest analogy)
The OS framing is Karpathy's primary lens:
- A few closed-source providers ([[entities/openai|OpenAI]], Gemini, [[entities/anthropic|Anthropic]]) parallel Windows/macOS
- The [[entities/meta-llama|Llama ecosystem]] approximates an open-source Linux
- The LLM functions as a CPU; the context window serves as RAM; the model orchestrates computation and memory

Critically, *no general GUI has been invented yet*. Interacting with ChatGPT via text is equivalent to using an operating system through the terminal. The GUI revolution — which made computing accessible to billions — has no LLM analogue.

---

## The 1960s Computing Era Hypothesis

The current moment maps to 1960s computing: compute is expensive, models are centralized in the cloud, and users access shared resources via time-sharing. The personal computing revolution for LLMs has not happened because **it is not yet economical**.

Mac Minis show early potential for local inference (memory-bound at batch size one, favorable for LLM workloads), but the economics remain marginal. The shape of the personal LLM era is unclear.

One inversion from historical precedent: **LLMs diffused to consumers first**, not governments or corporations. Unlike electricity, cryptography, and the internet — which were government/enterprise technologies before consumer adoption — LLMs were immediately available to everyone, with consumers asking how to boil an egg while governments lagged adoption. This inverted diffusion pattern has no clear historical precedent.

---

## Psychology of LLMs: Cognitive Profile

LLMs are stochastic simulations of people — autoregressive transformers trained on vast human-generated text, producing emergent human-like psychology. The cognitive profile is characterized by extreme asymmetry:

**Superpowers:**
- Encyclopedic memory far exceeding any single human
- Superhuman performance on certain problem-solving domains

**Significant deficits** (see Limitations section below):
- Hallucination and poor self-knowledge
- Jagged intelligence: making errors no human would make (claiming 9.11 > 9.9; miscounting letters in "strawberry") while excelling at graduate-level problems
- Anterograde amnesia: weights are fixed, context windows reset between sessions, no native accumulation of organizational expertise over time

The amnesia limitation is particularly consequential for agentic deployment. A human colleague who joins an organization gradually learns its context, culture, and workflows. LLMs do not do this natively — it remains unsolved in R&D.

---

## Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| Natural language as programming interface | broad_production | Prompts are programs; no CS training required |
| Vibe coding (non-programmer app creation) | broad_production | Karpathy built a Swift app without knowing Swift |
| Partial autonomy / tunable human-AI loops | broad_production | Tap completion → chunk replacement → full file → autonomous run |
| LLM-friendly software infrastructure (lm.txt, MCP) | narrow_production | Vercel, Stripe as early examples |

The democratization of programming is the headline breakthrough: what required 5–10 years of specialized training now requires fluency in natural language. See [[themes/code_generation|code generation]] and [[themes/ai_software_engineering|AI software engineering]].

---

## Limitations

### Cognitive and Reliability
- **Hallucination** — frequent generation of plausible but false information; weak internal self-knowledge. *(severity: significant, trajectory: improving)*
- **Jagged intelligence** — wildly inconsistent performance profile; superhuman on some axes, pre-school errors on others. *(severity: significant, trajectory: unclear)*
- **Anterograde amnesia** — no persistent memory or continual learning; context resets between sessions; explicit memory management required. *(severity: significant, trajectory: stable)*

### Security
- **Prompt injection vulnerability** — LLMs are gullible; susceptible to adversarial prompt injection and potential data leakage through training conditioning. *(severity: significant, trajectory: unclear)*

### Agentic Deployment
- **Infrastructure designed for humans** — APIs, documentation, and UI controls assume human interaction; must be entirely rebuilt for agents. *(severity: blocking, trajectory: improving)*
- **Verification bottleneck** — autonomous execution remains unreliable; human verification is mandatory; larger diffs compound error probability. *(severity: blocking, trajectory: stable)*
- **No native action mechanisms** — agents cannot act on real systems without explicit API wrappers or curl-equivalent tooling. *(severity: blocking, trajectory: improving)*
- **Demo-to-deployment gap** — systems that appear capable on simple demos reliably fail on complex autonomous tasks (the 2013 self-driving anecdote: a perfect first demo that misrepresented a decade-long deployment gap). *(severity: blocking, trajectory: stable)*

### Economics
- **Vision model inference costs** — token consumption for vision-heavy applications makes consumer unit economics structurally unsustainable; Karpathy's Menu.app lost significant money. *(severity: blocking, trajectory: worsening)*
- **Integration overhead dominates** — authentication, payments, DevOps, domain setup, and deployment entirely outweigh AI code generation effort for real products; vibe coding solves the easy part. *(severity: significant, trajectory: worsening)*

---

## Bottlenecks

- **Agent-software interface** — no standard patterns for agents to reliably interact with real software systems; all existing infrastructure must change. *(horizon: months)*
- **Consumer AI economics** — vision-heavy and agentic consumer apps are structurally uneconomical at current inference costs. *(horizon: 1–2 years)*
- **Autonomous multi-step execution** — agents lack reliable planning, error recovery, and action sequencing; human oversight remains mandatory. *(horizon: 1–2 years)*
- **DevOps / deployment abstraction** — infrastructure tooling (auth, payments, monitoring) remains largely manual and dominates engineering effort over AI-assisted code generation. *(horizon: months)*
- **Prompt injection resilience** — security properties of LLMs in agentic/enterprise contexts are neither well-characterized nor reliably preventable. *(horizon: 1–2 years)*

---

## Key Breakthroughs

1. **Natural language as universal programming interface** — paradigm-shifting democratization; removes the 5–10 year specialization barrier entirely.
2. **Software 3.0** — LLMs constitute a third, genuinely new computing paradigm beyond code and learned weights.
3. **Partial autonomy loops** — tunable human-AI collaboration is now the reliable operational model for production AI contribution.
4. **Inverted technology diffusion** — consumer-first adoption of LLMs represents a historically unprecedented reversal of how transformative technologies spread.

---

## Connections and Open Questions

Karpathy's OS analogy implies that the **platform wars are already underway** — the consolidation into a few dominant closed-source providers with one open-source challenger maps directly onto the Windows/macOS/Linux history. The critical open question is whether the LLM equivalent of the GUI arrives — and what form it takes — before the platform landscape freezes.

The 1960s computing analogy raises an uncomfortable implication: if we are genuinely in the mainframe era, the most consequential work is not building applications but building the infrastructure that will make personal LLM compute economical. Yet almost all current investment is in applications.

The inverted diffusion pattern is underexplored. Consumer-first adoption means the primary use cases being optimized for (boiling eggs, coding assistants, creative tasks) are not the high-leverage institutional applications that drove ROI in every prior technology wave. This may mean the organizational and institutional productivity gains from LLMs are structurally delayed compared to consumer utility.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_software_engineering|AI Software Engineering]]
- [[themes/code_and_software_ai|Code and Software AI]]
- [[themes/code_generation|Code Generation]]
- [[themes/software_engineering_agents|Software Engineering Agents]]

## Key Concepts

- [[entities/cursor|Cursor]]
- [[entities/jagged-intelligence|Jagged Intelligence]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/perplexity|Perplexity]]
- [[entities/prompt-injection|Prompt Injection]]
- [[entities/vibe-coding|Vibe Coding]]
- [[entities/llmtxt|llm.txt]]
