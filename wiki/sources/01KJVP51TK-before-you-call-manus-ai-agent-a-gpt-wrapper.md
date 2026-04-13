---
type: source
title: Before you call Manus AI Agent, a GPT Wrapper!
source_id: 01KJVP51TK37X7T8GTJWH108QE
source_type: video
authors: []
published_at: '2025-03-10 00:00:00'
theme_ids:
- agent_systems
- ai_market_dynamics
- computer_use_and_gui_agents
- model_commoditization_and_open_source
- multi_agent_coordination
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
---

# Before you call Manus AI Agent, a GPT Wrapper!

Manus is a production autonomous agent built on Claude 3.5 Sonnet and a suite of fine-tuned auxiliary models, revealing that sophisticated agentic behavior emerges less from novel model architectures than from careful systems engineering: a CodeAct-based execution loop, sandbox isolation per session, and a multi-agent topology that deliberately gates user interaction to a single executor agent in order to manage context window exhaustion. The source demystifies Manus as a "Claude wrapper" while simultaneously demonstrating why that framing undersells the architectural insight the system embodies.

**Authors:** (not specified)
**Published:** 2025-03-10
**Type:** video

---

## Expert Analysis

Manus is best understood as the combination of OpenAI's Deep Research and Operator, but running within an isolated Ubuntu-like virtual sandbox. For each session, it spins up a fresh compute environment, executes tasks autonomously, and returns deliverables ranging from interactive webpages to PDF travel itineraries to Three.js games written zero-shot.

**The CodeAct framework.** Rather than expressing agent actions as text or JSON, Manus uses a modified version of the CodeAct framework, where LLM outputs take the form of computer programs that are then executed. The rationale is grounded in training distribution alignment: LLMs are extensively trained on code, and computer programs are unusually precise at specifying objectives. This approach also compresses context significantly, since a program can express multi-step operations that would otherwise require lengthy text exchanges. Coding is not the goal; it is the most natural representational medium for agentic planning given what LLMs are good at.

**Multi-agent isolation as a context management strategy.** Manus operates with at least three internal agents: a knowledge agent, a planner agent, and an executor agent. Crucially, users only ever communicate with the executor, which itself has no visibility into the knowledge or planner components. This compartmentalization is not incidental; it is a deliberate architectural choice to prevent context window saturation. The fundamental bottleneck in multi-agent LLM systems is that reasoning pipelines burn through token budgets extremely quickly. By exposing only the executor layer to the user, Manus keeps the interaction context narrow while the broader planning machinery operates upstream and out of scope.

**Model composition and the fine-tuning layer.** The system runs Claude 3.5 Sonnet as its primary model, not Claude 3.7, because development began before the newer model existed. Alongside Sonnet, Manus deploys what appear to be Qwen fine-tunes as auxiliary models for specialized subtasks. This reveals a pattern that is becoming standard in production agents: no single base model suffices, and the gap between a capable foundation model and a well-behaved agent requires targeted post-training.

**The alignment framing.** One of the source's most consequential observations is that agentic capability may be less a foundational model problem than an alignment problem. The comparison drawn is between GPT-3 and InstructGPT: the underlying capability was present, but the behavior required explicit shaping. Open-source base models trained on chatbot-style interaction are implicitly rewarded for producing complete responses immediately, regardless of task complexity. A modest investment in post-training on agentic trajectories, potentially including online RL in an agent-appropriate environment, may be sufficient to unlock substantially more capable agent behavior without changing the underlying model. This is a significant implication for the open-source ecosystem: replicating Manus-level performance may be more tractable than a "DeepSeek moment" comparison would suggest.

**Jailbreak caveats.** System prompts obtained by jailbreaking Manus may be hallucinations rather than genuine internal prompts. Manus publicly acknowledges using Browser Use and CodeAct, but adversarially extracted tool descriptions cannot be trusted as ground truth.

---

## Key Claims

1. Manus is built on Claude 3.5 Sonnet as its primary underlying LLM, not a custom-trained model.
2. The system has access to approximately 29 tools available to the LLM.
3. Manus uses the Browser Use library to emulate a browser within LLM agent sessions.
4. Each session runs in an isolated sandbox, completely separate from other user sessions; users can enter the sandbox directly via the Manus interface.
5. Manus uses a modified version of the CodeAct framework, where agent actions are expressed and executed as computer programs rather than text or JSON.
6. LLM-generated programs compress context and enable precise task specification, making code a universal medium for agent action rather than an end goal.
7. A multi-agent architecture separates knowledge, planner, and executor agents; users only communicate with the executor, which is unaware of the other agents' internals.
8. This multi-agent isolation is a deliberate strategy to manage context window exhaustion, one of the core bottlenecks in LLM-based agent systems.
9. Manus uses Qwen fine-tunes as auxiliary models alongside Claude 3.5 Sonnet.
10. Prompts obtained by jailbreaking Manus may be hallucinations, not actual system prompts.
11. Agentic capability is plausibly more an alignment problem than a foundational capability gap; targeted post-training on agentic trajectories may be sufficient to dramatically improve open-source agent behavior.
12. An online RL fine-tuning approach in an appropriate agent environment may be a promising path toward capable open-source agents.

---

## Capabilities

**Autonomous multi-step task execution via tool use** (maturity: narrow_production). Agents with 20+ tool integrations combining file access, browser automation, and sandboxed code execution can complete complex, multi-stage tasks zero-shot, including game development, trip planning, and design work.
> *"Manis is nothing but a cloud rapper so it's got clouds on it with 29 tools these are the tools that the llm has got access to"*

**Code-as-action agent execution** (maturity: narrow_production). LLM agents can generate and execute programs as their primary action modality, enabling precise task specification and significant context compression relative to text-and-JSON approaches.
> *"what if you can turn that into a computer program because llms can write computer programs and computer programs are really good with expressing what an objective task should be"*

**Browser automation via embedded emulation** (maturity: narrow_production). Browser Use enables LLM agents to interact with live web content within the agent loop, supporting research, information synthesis, and form interaction.
> *"it also uses browser use which is a way to emulate a browser within llm usage"*

**Isolated per-session sandboxing** (maturity: narrow_production). Each user session receives a fully isolated compute environment, preventing cross-session interference and enabling users to inspect the agent's working state directly.
> *"for each and every session it creates its own sandbox and every sandbox that it creates the session sandbox is completely isolated from other user sessions"*

**Multi-agent production deployment with separated planning and execution** (maturity: narrow_production). Knowledge, planning, and execution functions can be distributed across distinct agents while maintaining coherent task completion, with context budgets managed through deliberate inter-agent information gating.
> *"Manis has got a multi-agent implementation... you have got a knowledge agent you have got a planner agent and then you have got an executive agent"*

**Fine-tuned base LLMs as effective production agent foundations** (maturity: broad_production). Claude 3.5 Sonnet combined with task-specific fine-tunes is sufficient to power production-grade autonomous agents across diverse domains.
> *"currently Manis uses clae 3.5 on it... they were using a couple of auxiliary models probably powered by Quin fine tunes"*

---

## Limitations & Open Questions

**Context window saturation in multi-agent systems** (severity: significant, trajectory: improving). Multi-agent reasoning pipelines consume the token budget rapidly, requiring architectural workarounds such as restricting user interaction to a single executor rather than allowing open communication across agents. This limits the depth and visibility of planning hierarchies that users can access.
> *"one of the biggest problems that you have with using LMS as agent is that you very quickly end up filling the context window of an LM"*

**Auxiliary fine-tuning requirement** (severity: significant, trajectory: stable). Base LLMs alone do not achieve the behavioral profile needed for production agents. Specialized post-training or auxiliary fine-tuned models remain necessary, adding complexity and resource overhead to agent deployment.
> *"they were using a couple of auxiliary models probably powered by Quin fine tunes"*

**Model version lock-in during development** (severity: minor, trajectory: improving). Agents developed against a specific model generation can become locked to it as their architecture stabilizes before newer models are released, temporarily missing capability and efficiency gains.
> *"currently Manis uses clae 3.5 on it not the latest model Claude 3.7... the reason is because when they started building Manis at the time only clae 3.5 was available"*

**Adversarial hallucination of internal tool descriptions** (severity: significant, trajectory: unclear). Jailbreaking attempts that extract tool prompts or system instructions from agents may produce hallucinated outputs that are indistinguishable from genuine internals, making external auditing of agent configurations unreliable.
> *"any prompt that you get through manises jail breaking could be hallucination they acknowledge that they're using browser use"*

**Dependence on proprietary model APIs** (severity: minor, trajectory: unclear). High-performing production agents currently rely on proprietary LLM APIs rather than custom-trained or fully open models, limiting deployment independence and reproducibility for the open-source community.
> *"it's not black magic it's not something you know they've trained their own model this is not the Deep seek Moment"*

---

## Bottlenecks

**Context window saturation in multi-agent architectures.** Intermediate reasoning layers (knowledge agents, planners) consume token budgets at a rate that makes full context visibility across agents impractical at scale. Current mitigations rely on information gating rather than increased context capacity. This blocks scaling multi-agent systems to more complex planning hierarchies with full inter-agent transparency. (horizon: 1-2 years)
> *"one of the biggest problems that you have with using LMS as agent is that you very quickly end up filling the context window of an LM and one of the ways that they are avoiding this particular Pitfall is by saying that okay whenever you chat with Manis you're directly communicating or only communicating with the executor agent"*

**Fine-tuning and auxiliary model dependency.** Deploying a production agent requires post-training or auxiliary specialized models alongside the base LLM. This blocks simplified, plug-and-play agent deployment from a single base model and increases the overhead of replicating or adapting agent systems. (horizon: 1-2 years)
> *"they were using a couple of auxiliary models probably powered by Quin fine tunes"*

---

## Breakthroughs

**Multi-agent isolation as a context management solution.** Routing user interaction exclusively through an executor agent while keeping knowledge and planner agents upstream, with no direct user exposure to those layers, effectively resolves context window saturation in complex agent pipelines. This architectural pattern may be broadly applicable across multi-agent deployments. (significance: notable)
> *"one of the ways that they are avoiding this particular Pitfall is by saying that okay whenever you chat with Manis you're directly communicating or only communicating with the executor agent which itself does not know or does not have any details of the knowledge planner or other agents"*

**Agentic behavior as a post-training problem.** Demonstrating that capable agent behavior can emerge from relatively modest post-training on agentic trajectories, rather than requiring novel model architecture, positions open-source models as viable foundations for Manus-class agents. This shifts the research frontier from pretraining at scale to targeted alignment work.
> *"just a bit of post-training on agentic trajectories can make an immediate and dramatic difference"*

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/ai_market_dynamics|AI Market Dynamics]]
- [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]
- [[themes/model_commoditization_and_open_source|Model Commoditization & Open Source]]
- [[themes/multi_agent_coordination|Multi-Agent Coordination]]
- [[themes/tool_use_and_agent_protocols|Tool Use & Agent Protocols]]

## Key Concepts

- [[entities/claude-35-sonnet|Claude 3.5 Sonnet]]
- [[entities/codeact|CodeAct]]
- [[entities/multi-agent-architecture|Multi-Agent Architecture]]
- [[entities/post-training|Post-training]]
