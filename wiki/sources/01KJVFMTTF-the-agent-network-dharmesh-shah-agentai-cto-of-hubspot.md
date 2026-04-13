---
type: source
title: The Agent Network — Dharmesh Shah, Agent.ai + CTO of HubSpot
source_id: 01KJVFMTTF4CBT71368ZPGYCBY
source_type: video
authors: []
published_at: '2025-03-28 00:00:00'
theme_ids:
- agent_systems
- ai_business_and_economics
- code_and_software_ai
- code_generation
- software_engineering_agents
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Agent Network — Dharmesh Shah, Agent.ai + CTO of HubSpot

> Dharmesh Shah, co-founder of HubSpot and founder of agent.ai, surveys the current state of AI agents through the lens of a practitioner operating a live platform with 1.3 million users. The source is unusually grounded: claims about model routing, tool limits, eval adoption, and memory gaps are backed by production data rather than speculation. It maps both the genuine progress (MCP adoption, autoregressive image editing, cost-reduction via model routing) and the structural ceilings (agent discovery, async UX, attribution, cross-agent memory) that define where the field actually is versus where it is assumed to be.

**Authors:** Dharmesh Shah
**Published:** 2025-03-28
**Type:** video

---

## What Agents Actually Are

Shah opens with a deliberately broad definition: an agent is AI-powered software that accomplishes a goal. But the useful work is in the classification axes that follow — autonomous vs. non-autonomous, deterministic vs. non-deterministic workflow, synchronous vs. asynchronous execution, chat vs. workflow interaction modes. These axes are not academic; they determine what you can build reliably today.

The failure of first-generation frameworks like BabyAGI and AutoGPT is instructive here. They were not wrong about the destination — they were wrong about the models they were running on. Those frameworks assumed reasoning and execution planning capability that simply did not exist. The lesson is that agent architecture is downstream of model capability, and premature abstraction built on insufficient models produces fragile systems rather than general intelligence.

What has changed to make agents viable now:
- Better, more reliable models
- Improved tool use and standardized tool interoperability ([[themes/agent_systems|agent_systems]])
- entities/mcp as an emerging standard
- Cheaper and faster inference
- RL fine-tuning progress
- Model diversity reducing single-model performance basin lock-in

---

## The Minimal Agent and the Network Primitive

A minimum viable agent must use AI to achieve its goals — otherwise it is just software. This sounds obvious but has a structural implication: if tools are just atomic agents, then tool use *is already* multi-agent composition. A network of agents that know about each other via something like MCP, decompose a problem, and delegate accordingly is not a future architecture — it is a re-description of what LLM tool use already is.

This framing points toward a unifying primitive: a single abstraction (the agent) that composes into arbitrary networks, raising the level of abstraction incrementally. The elegance of reducing everything to one composable primitive — rather than maintaining separate concepts for tools, workflows, and agents — is both intellectually satisfying and practically significant for platform design.

Agent.ai operationalizes this directly: every agent on the platform automatically receives a callable REST API and is exposed as an MCP server entry. Agents become Lego blocks discoverable by other agents, with thousands of pre-built capabilities available as building blocks without manual API development by the original author.

---

## Image Generation: The Autoregressive Inflection

A significant portion of the conversation concerns an inflection point in image generation that is easy to miss if you are focused on language models. The core claim: diffusion-based image editing is *architecturally* incapable of coherent targeted editing. If you run a diffusion model twice from similar prompts, you get entirely different images — you cannot "go back that way." Precise element-level modification is blocked at the architectural level, not the capability level.

Autoregressive image generation (next-token prediction extended to image tokens) overcomes this ceiling. entities/gemini-flash-experimental enables persistent image editing — modifying specific elements while maintaining coherence — a capability diffusion approaches cannot provide structurally. The rumored trajectory at Meta (image generation in Llama 3 blocked by legal review; Mustafa Suleyman moving to Google Gemini reportedly bringing an autoregressive approach) suggests this paradigm shift is happening at multiple frontier labs simultaneously.

**Current limitation:** First-generation autoregressive image editing models lack spatial precision. They can semantically replace elements but cannot accurately size or position replacements to fit existing image geometry. The O→donut replacement example is telling: it works semantically but fails geometrically. This is the remaining gap between "credible threat to Photoshop/Canva" and actual displacement of those tools. See [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]].

**The paradigm convergence:** Diffusion was the image paradigm; autoregressive was the language paradigm. These two worlds are now colliding in image generation, with entities/playground-ai building Photoshop-like composition UIs on top of what may be autoregressive backends. The convergence of paradigms across modalities is a structural signal worth tracking.

---

## Knowledge Graphs as AI-Native Knowledge Stores

Shah is bullish on knowledge graphs as a representation layer, and the reasoning is worth unpacking carefully rather than treating it as generic graph enthusiasm.

The progression of data stores — index DBs → key-value stores → relational → document → vector → graph — is not just historical context. Each store embeds assumptions about what relationships matter. Relational databases assume tabular structure and foreign key relationships. Vector stores assume that semantic proximity in embedding space captures what you need. Graphs assume that the *traversal structure itself* is the knowledge.

For LLMs and RAG pipelines specifically, two properties make graphs interesting:
1. **Discoverability and observability** — unlike embeddings, graph nodes and edges are human-readable and auditable. A PageRank-style traversal can rank nodes in ways that surface importance without black-box similarity scores.
2. **Chunking loss** — vector RAG loses relational and structural context during chunking. Top-k semantic retrieval returns fragments that miss cross-document relationships and hierarchical structure. Graph RAG preserves this at the cost of construction complexity.

**Traction areas:** Conversation memory and document RAG are where knowledge graphs are gaining adoption in 2025. Both use cases share a property: the relationship *between* pieces of information matters as much as the content of any single piece.

**The adoption trap:** Knowledge graph RAG only demonstrates clear advantage at large deployment scale. Small-scale evals systematically underestimate it. This creates a validation dead zone: you cannot cheaply demonstrate value, so most teams stay on simpler vector pipelines. The evaluation cost barrier is a genuine structural blocker — not a capability gap. See [[themes/agent_systems|agent_systems]].

**The complexity failure mode:** Teams that go hard into knowledge graphs tend to produce graphs that are too complex to navigate, defeating the purpose. Curation discipline is not optional — it is load-bearing.

Note: relational databases can technically represent graphs via join tables, but you likely lose the traversal efficiency that makes graph retrieval useful in practice. A social graph represented in MySQL is not a social graph in the relevant sense.

---

## Production Data from Agent.ai

The agent.ai platform numbers provide empirical grounding for several claims that are usually speculative:

| Metric | Value |
|--------|-------|
| Users | 1.3 million |
| Agent builders | 3,000 |
| Published agents | ~1,000 |
| Human quality ratings | Tens of thousands |
| Average agent rating | 4.1 / 5.0 |

**Model routing finding:** Runtime routing to smaller, cheaper models produces orders-of-magnitude inference cost reduction with no measurable change in human-rated output quality — validated across production interactions. The catch: users do not trust this. They consistently select the largest frontier model (GPT-4.5, etc.) regardless of task complexity. User trust, not model capability, is the binding constraint on inference cost optimization. See [[themes/ai_business_and_economics|AI Business and Economics]].

**Tool count finding:** LLMs degrade dramatically above ~15-20 tools. Exposing hundreds of community-built agents directly to a single LLM is architecturally impossible. The practical solution — latent-space based tool/agent retrieval (RAG for agents) — provides a semantic routing layer, but this introduces its own engineering complexity.

**Evals finding:** Everyone acknowledges evals are critical. Almost no one actually implements them. Agent platforms accumulate human ratings as a side effect of use, which functions as a practical alternative — but this signal is coarse and delayed relative to what systematic evals would provide.

---

## Structural Gaps: Where the Field Actually Is

Shah identifies a cluster of gaps that are not incremental improvements but structural absences in current agent infrastructure:

**Agent discovery:** No standardized registry exists for agents to advertise capabilities or be found by other agents. Multi-agent collaboration currently requires pre-built point-to-point integrations. Anthropic is reportedly working on a registry; others are building directories. Until this exists, "multi-agent systems" mostly means manually wired pipelines, not emergent composition. (Horizon: months)

**Cross-agent memory:** Users must re-explain context, preferences, and knowledge to every new agent they interact with. No shared memory layer exists across independently developed agents. Shah describes this as his current primary focus at agent.ai. The privacy-aware selective memory sharing problem is non-trivial — shared memory for a *team* of people and agents, not just a single user, adds another dimension of complexity. (Horizon: 1-2 years)

**Async UX primitives:** Agent interaction remains locked to synchronous chatbot request-response patterns. Real-world task delegation is inherently asynchronous — you don't stand over a colleague's shoulder while they complete a task. The product primitives and UX models for agents that work in the background and report back do not yet exist at the platform level. Shah characterizes current agent UIs as "HTML 1.0" — dropdowns, checkboxes, text inputs. (Horizon: months)

**Attribution:** Connecting specific AI actions to business outcomes in multi-step workflows is fundamentally unsolved. Without traceable causal chains, results-based AI pricing is impossible to implement honestly. Platform incentives actively work against attribution transparency, since platforms benefit from overclaiming contribution. Shah calls this "sad" — important, widely recognized as unsolvable in practice, and structurally suppressed by incentive misalignment. (Horizon: 3-5 years)

**Persistent digital workers:** Agents that function as genuine team members — with persistent identity, continuity, discoverability, and delegatable authority — do not yet exist in any commercially meaningful deployment. The "digital coworker" framing is aspirational. What exists today is stateless task executors.

---

## Vibe Coding and the Complexity Risk

The vibe coding discussion surfaces a structural tension in [[themes/code_generation|code generation]] and [[themes/software_engineering_agents|software engineering agents]]:

**The under-engineering argument:** As refactoring becomes cheap, the case for deliberate under-engineering weakens. The cost of "we'll fix it later" drops toward zero if AI can restructure code on demand.

**The over-engineering risk:** If the cost of adding a feature approaches zero, teams lose the forcing function that prevents feature bloat. Engineering-hour constraints historically served as a natural prioritization filter. Remove that filter and you get promiscuous feature addition that bloats products without improving them.

**The self-regulation absence:** AI code generation tools do not model the downstream cost of architectural complexity. They add features and abstraction layers without understanding what happens at scale. The models do whatever is locally coherent without global architectural discipline.

The question Shah leaves open: will AI eventually develop the capacity to determine appropriate abstraction levels autonomously, or will this remain a human judgment call that AI execution makes easier to skip?

---

## Personal Knowledge Infrastructure

Several observations cluster around the gap between what Google/Gmail *could* do with AI and what it actually offers:

- A personal vector store built from email archives enables high-quality retrieval of past answers to recurring questions — effective enough that Shah describes it as "shockingly good."
- Gmail does not offer semantic search over email history despite Google's demonstrated AI capabilities. This is characterized as a notable product gap — "they're Google" — likely driven by privacy architecture constraints rather than capability gaps.
- Video transcript extraction remains a commonly used "novel" primitive on agent platforms, which implies that composable personal agent tooling is still inaccessible to ordinary users.
- The slide-extraction use case (extract structured knowledge from YouTube conference talks) is identified as a clear unmet demand where the underlying technology exists but has not been productized.

These gaps collectively suggest that the distance between "AI capability exists" and "AI capability is accessible as personal infrastructure" remains large — and is a distinct category of problem from AI capability development itself.

---

## Open Questions

- Will autoregressive image generation fully displace diffusion, or will hybrid approaches emerge for different use cases?
- Can knowledge graph RAG be made evaluable at small scale, or does its value proposition inherently require production-scale deployment to measure?
- What is the correct trust model for shared cross-agent memory — who controls what agents can see about a user, and who is liable when shared context produces harmful outputs?
- Will async agent UX require fundamentally new interaction paradigms, or will existing notification/task management patterns (like email threads or project management tools) be adapted?
- If attribution of AI value is structurally suppressed by platform incentive misalignment, can third-party attribution infrastructure emerge and survive commercial pressure?

---

## Related Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_business_and_economics|AI Business and Economics]]
- [[themes/code_and_software_ai|Code and Software AI]]
- [[themes/code_generation|Code Generation]]
- [[themes/software_engineering_agents|Software Engineering Agents]]
- [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Key Concepts

- [[entities/dspy|DSPy]]
- [[entities/diffusion-models|Diffusion Models]]
- [[entities/mem0|Mem0]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/vibe-coding|Vibe Coding]]
