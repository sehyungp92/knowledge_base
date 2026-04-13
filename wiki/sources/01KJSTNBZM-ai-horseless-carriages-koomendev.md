---
type: source
title: AI Horseless Carriages | koomen.dev
source_id: 01KJSTNBZM074JN96NWY1MRDDZ
source_type: article
authors: []
published_at: None
theme_ids:
- agent_systems
- ai_business_and_economics
- software_engineering_agents
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AI Horseless Carriages | koomen.dev

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# AI Horseless Carriages | koomen.dev
article
https://koomen.dev/essays/horseless-carriages/

---

## Briefing

**Most AI applications are "horseless carriages" — they graft AI onto interfaces designed for human labor rather than redesigning interfaces around AI's actual strengths, producing products that are worse than doing the task manually. The core failure is that developers retain control of the System Prompt when the user should own it, because LLM agents acting on a user's behalf must be taught by that user, not by a committee of product managers. The killer app of AI is not generation but automation: teaching agents to handle mundane work so users never have to touch it.**

### Key Takeaways
1. **The horseless carriage failure mode** — AI apps that add AI to existing interfaces instead of redesigning for AI produce products that feel worse than doing the work manually, not because the models are weak but because the design constrains them.
2. **Gmail's Gemini integration as canonical bad design** — The draft-writing feature produced output longer than the prompt that requested it, meaning users spent more time asking for help than the task required; the model is capable, the design is broken.
3. **System Prompt ownership is the central design error** — Developers default to owning the System Prompt because "that's how software has always worked," but when an agent acts on your behalf, you must be able to define how it behaves in the general case.
4. **User-editable System Prompts produce dramatically better results** — A "Pete System Prompt" teaching the model to write like the author produced a perfect draft instantly; the same improvement applies to every future draft, compounding the value.
5. **LLMs are great at reading and transforming text, not generating it** — For users who want concise output, generative AI is nearly useless because any email "written in your voice" will be about as long as the prompt describing it.
6. **The real AI killer app is automation of mundane work** — An email-reading agent that categorizes, prioritizes, auto-archives, drafts replies, and triggers notifications represents what AI-native software should actually do.
7. **Most AI apps should be agent builders, not agents** — Developers should provide domain-specific UIs, templates, and prompt-writing tools that help users bootstrap and iterate on their own agents rather than shipping one-size-fits-all behavior.
8. **Tools are the correct security layer for agents** — Enforcing agent boundaries via code-defined tools is far more robust than trying to secure System Prompts from User Prompts in text; prompt injection is a symptom of broken abstractions.
9. **The developer role shifts to infrastructure, not behavior** — Developers build the UI for agent construction, the tool integrations, the feedback loops for iteration, and the templates — not the logic that defines how the agent behaves for a specific user.
10. **Domain expertise is context-specific, invalidating one-size-fits-all agents** — YC's accounting team uses YC-specific conventions, fund structures, and software mix; a generic accounting agent is as useless as an accountant who knows nothing about YC, which is why finance still runs on Excel.
11. **Prompt-writing will democratize without developers** — Writing System Prompts is surprisingly intuitive and provides instantaneous feedback unlike teaching a human; the barrier to users owning their own agent behavior is lower than most developers assume.
12. **AI-native software has a clear design principle** — It should maximize user leverage in a specific domain and minimize time spent on that domain's mundane work, not replicate existing interfaces with an AI button added.

---

### The Horseless Carriage Analogy: Why First-Generation AI Apps Are Broken

- The author identifies a consistent pattern: AI applications feel useless not because the underlying models are weak, but because the product design unnecessarily constrains what the models can do.
  - The historical parallel is the 1803 Steam Carriage, which borrowed the wooden frame, seats, and layout of horse-drawn carriages despite being powered by a completely different mechanism — the brokenness was invisible at the time and obvious in retrospect.
  - **The "old world thinking" is swapping the horse for an engine without redesigning the vehicle** — in AI terms, adding AI features to interfaces designed for human labor rather than interfaces designed to automate that labor.
- The author distinguishes between using AI to build software (empowering, feels like a power tool) versus using software built with AI (often tacked-on, counter-productive, useless).
  - This distinction suggests the primary value of current LLMs may be in the development loop rather than the end-user product, at least until design patterns catch up.
- The essay frames this as a transitional period analogous to the gap between the steam carriage and the automobile — the right design patterns haven't been discovered or adopted yet, and most current AI apps will look laughably wrong in retrospect.

---

### The Gmail/Gemini Case Study: A Perfect Failure

- Gmail shipped a feature allowing users to generate email drafts from scratch via a prompt input field powered by Gemini.
  - The output was wordy, overly formal, and tonally alien — "so un-Pete that if I actually sent it to Garry, he'd probably mistake it for some kind of phishing attack."
  - **The critical failure metric: the resulting email was shorter than the original prompt**, meaning the user spent more time asking for help than the task would have taken without AI.
- The author notes that millions of Gmail users have concluded from this experience that AI isn't smart enough to write good emails — **a false conclusion drawn from a design failure, not a model capability failure**.
  - Gemini is described as "an astonishingly powerful model that is more than capable of writing good emails"; the Gmail team de

## Key Claims

1. Most AI apps feel tacked-on and useless because they mimic old ways of building software that unnecessarily constrain the AI models they're built with.
2. Gmail's AI draft feature can cost users more time than writing the email themselves when the resulting draft is longer than the original prompt.
3. The limitation of Gmail's AI feature is app design, not model capability — Gemini is capable of writing good emails.
4. Allowing users to write and edit their own system prompts produces better, personalized AI outputs compared to developer-controlled one-size-fits-all system prompts.
5. As of April 2025, most AI apps do not intentionally expose their system prompts to users.
6. The traditional software industry model requires developers to act as middlemen between users and computers, translating desires into code behind one-size-fits-all interfaces.
7. With LLMs, users no longer need developer middlemen to tell computers what to do — they can write system prompts directly.
8. When an LLM agent acts on a user's behalf, the user should be allowed to teach it how to behave by editing the system prompt.
9. Domain-expert AI agents (e.g., accounting, legal) still require user-editable system prompts because expert knowledge is highly context-specific to the organization.
10. Much of finance still runs on Excel because it is a general tool that accommodates infinite specific use cases — a model for AI tool design.

## Capabilities

- LLMs can read, categorize, prioritize, auto-archive emails, and generate drafted replies automatically when operating on a user-authored system prompt
- System prompt personalization enables LLMs to write consistently in a specific individual's voice — producing output indistinguishable from the user's own style when given a well-crafted personal system prompt
- LLMs excel at reading and transforming text — categorization, summarization, prioritization, and reformatting tasks work reliably across domains
- AI agents with access to tools can autonomously perform compound personal workflow tasks — unsubscribing from mailing lists, scheduling appointments, paying bills — without user intervention

## Limitations

- Default LLM output without personalized system prompts is generic, overly formal, and fails to match individual user voice — producing 'AI Slop' unsuitable for personal communication
- LLMs are poor at generating short personal text from scratch — when the user wants brief output, the prompt specifying the desired output becomes as long or longer than writing it directly, making AI a net negative for this task class
- One-size-fits-all AI agents fail for context-specific domains — organizational and domain expertise is always highly contextual, making generic expert-authored system prompts insufficient for real-world use
- As of April 2025, most consumer AI apps do not expose or allow editing of system prompts, preventing user personalization and locking AI into lowest-common-denominator behavior
- Prompt overhead for AI assistance frequently exceeds the effort of the underlying task — users spend more time writing prompts than they would have spent doing the task themselves
- Prompt injection attacks are an unsolved architectural security concern — current systems attempt to enforce trust boundaries within a single flat text prompt, which is architecturally unsound and exploitable
- AI app integrations overwhelmingly mimic existing software design patterns rather than rethinking the interaction paradigm — most shipped AI features add negative or marginal value because they are constrained by legacy UX assumptions
- Millions of users are forming incorrect beliefs about AI capability (concluding 'AI isn't smart enough') from poorly designed AI apps, creating a perception gap that may slow adoption of better-designed systems

## Bottlenecks

- Developer-controlled system prompts prevent personalization of AI agents acting on behalf of individual users — the inherited software paradigm assigns control of agent behavior to developers rather than users, producing generic agents that fail to represent anyone specifically
- Horseless carriage design paradigm — software teams adding AI to existing products rather than designing AI-native products from the ground up — constrains the leverage AI can deliver and produces user experiences that underperform manual alternatives

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/ai_business_and_economics|ai_business_and_economics]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Key Concepts

- [[entities/prompt-injection|Prompt Injection]]
