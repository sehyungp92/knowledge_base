---
type: source
title: Build the web for agents, not agents for the web
source_id: 01KJTQD302SP6FG6TY60GF5Q1E
source_type: paper
authors:
- Xing Han Lù
- Gaurav Kamath
- Marius Mosbach
- Siva Reddy
published_at: '2025-06-12 00:00:00'
theme_ids:
- agent_systems
- alignment_and_safety
- computer_use_and_gui_agents
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Build the web for agents, not agents for the web

**Authors:** Xing Han Lù, Gaurav Kamath, Marius Mosbach, Siva Reddy
**Published:** 2025-06-12 00:00:00
**Type:** paper

## Analysis

# Build the web for agents, not agents for the web
2025-06-12 · paper · Xing Han Lù, Gaurav Kamath, Marius Mosbach, Siva Reddy
https://arxiv.org/pdf/2506.10953

---

### Motivation & Prior Limitations
Current web agents are forced to interact with interfaces designed for human users, creating a fundamental mismatch between LLM capabilities and the interfaces they must navigate.
- Browser-based agents relying on DOM trees face extreme token inefficiency, with DOM trees potentially exceeding 1M tokens; deploying a GPT-4.1-based agent on a single 20-step task could cost roughly $40 under current approaches.
  - Screenshots address token cost but lose occluded information (e.g., collapsed dropdowns), while DOM-based representations include irrelevant server-side rendering artifacts that add no decision-relevant signal.
- API-based hybrid agents are constrained by developer-oriented API designs that lack stateful manipulation primitives (e.g., sorting a product list), require substantial developer refactoring to extend, and frequently rate-limit agent traffic.
  - Internal web APIs bypass safety guardrails like two-factor authentication when accessed directly, as they were designed to communicate strictly with browsers rather than autonomous agents.
- The proliferation of browser-based agents strains web infrastructure through repeated automated rendering, driving website operators toward increasingly aggressive CAPTCHA systems that harm accessibility for legitimate human users without reliably distinguishing malicious automation from assistive use.
- Existing agent frameworks define mutually incompatible action spaces: BrowserGym includes tab management and user-messaging actions, while the concurrent space from Qin et al. (2025) omits tab actions entirely and replaces user messaging with a user-intervention request action, making policy learning non-transferable across frameworks.
- Safety and privacy risks are severe: browser-integrated agents with access to stored passwords, credit card details, and personal accounts can cause unauthorized purchases, send harmful messages, or be manipulated via prompt-level, HTML-level, or vision-level adversarial attacks.

---

### Proposed Approach
This position paper advocates for a paradigm shift from building agents that adapt to human-facing interfaces to designing a new class of interfaces — Agentic Web Interfaces (AWIs) — purpose-built for the operational requirements of web agents.
- AWIs are proposed as a dedicated interaction layer distinct from both browser UIs (built for humans) and web APIs (built for developers), targeting the specific representational, computational, and safety needs of agentic systems.
  - Unlike MCP, which is a stateless JSON-RPC 2.0 protocol allowing per-server method variation, AWIs are stateful interfaces with standardized implementations across websites — analogous to how a JavaScript FileReader behaves identically across browsers.
  - AWIs and MCP are framed as complementary: an AWI can communicate with a web service through MCP, and an MCP server can access websites through AWIs, enabling MCP-compatible LLM assistants to navigate websites autonomously.
- Six guiding principles for AWI design are proposed: standardized action spaces and interface structure; human-centric design preserving human agency and the ability to pause/redirect agent trajectories; safety through access control lists, guardrails, and adversarial robustness; optimal representations tailored to agent needs without superfluous DOM detail; efficient hosting that avoids increasing website computational load; and developer-friendly integration with existing web infrastructure.
- Concrete design suggestions include: unified high-level actions that compose primitive operations (analogous to BrowserGym's `goto`); bidirectional UI-AWI translation tools (via Playwright/Selenium) for compatibility with human-facing interfaces; Access Control Lists for agents with privacy-preserving password managers and explicit user confirmation for destructive actions; progressive information transfer that sends images at optimal resolution or as embeddings rather than full-resolution assets; and agentic task queues that cap concurrent agent connections and distribute traffic across time to preserve human user experience.
- The paper explicitly does not provide a prototype or implementation, framing AWI design as a collective, iterative effort requiring contributions from ML researchers, website developers, AI safety researchers, HCI practitioners, and end users.

---

### Results & Capabilities
This is a position paper with no empirical results; its contribution is conceptual and argumentative rather than experimental.
- The paper provides a cost estimate illustrating the severity of the DOM inefficiency problem: a 20-step task using a GPT-4.1 agent over a full DOM tree could cost approximately $40, assuming $2 per million input tokens, with costs scaling further for reasoning models.
- The paper maps six AWI design principles to specific ML research disciplines and design suggestions in a structured table, arguing that AWI adoption would produce downstream benefits across reinforcement learning (consistent reward signals and action spaces), generalization research (decoupling task knowledge from interface knowledge), planning (scalable sandbox episodes without human-user interference), NLP (optimal summarization and retrieval-augmented representations), and multimodality (purposefully processed media at agent-appropriate resolution).

---

### Implications
AWIs, if adopted, would represent a structural intervention in how the web accommodates autonomous agents — shifting the locus of adaptation from agents to the infrastructure they operate within.
- Standardized high-level action spaces across AWI-compliant websites would enable RL policy learning and generalization research to transfer across sites without interface-specific retraining, potentially unlocking a class

## Key Claims

1. Current web agent approaches face substantial challenges due to a fundamental mismatch between human-designed interfaces and LLM capabilities.
2. Web agent browser states are currently presented via screenshots, DOM trees, or a combination of both.
3. Screenshots fail to provide comprehensive webpage information because visually occluded elements such as collapsed dropdown menus are not captured.
4. DOM-based representations are extremely inefficient due to excessive structural tokens and supplementary attributes such as server-side identifiers.
5. DOM trees for web pages can exceed 1 million tokens in size.
6. Deploying a GPT-4.1-based web agent for a single 20-step task could cost approximately $40.
7. Existing mitigation strategies for DOM inefficiency do not generalize well across different websites and novel task scenarios.
8. As web agent capabilities have improved, CAPTCHA systems have become increasingly complex, creating accessibility barriers for legitimate human users.
9. Browser-based web agents with access to personal accounts and sensitive browser data may cause severe harm through unauthorized actions such as sending harmful messages or making unauthorized purchase
10. API-based agents are limited by the narrower range of actions offered by web APIs compared to webpage UIs.

## Capabilities

- Web agents can perform multi-step browser-based task execution using LLMs with screenshot, DOM tree, and accessibility tree representations, covering element selection, text input, URL navigation, and tab management
- Hybrid web agents combining API calls and browser UI interactions can alternate between modes to complete web navigation tasks, extending beyond pure browser or pure API approaches
- Specialized reward models can evaluate web agent task completion trajectories without requiring access to the underlying environment state or human-defined success rules

## Limitations

- Screenshot-based web agent representations miss visually occluded DOM content — elements in collapsed dropdowns or hidden menus are invisible to the agent
- DOM tree representations for web agents are token-inefficient, with trees potentially exceeding 1M tokens, making LLM-based agents computationally prohibitive at scale
- Deploying a GPT-4.1-based DOM-tree web agent costs approximately $40 for a single 20-step task — order-of-magnitude cost prohibitive for consumer-scale deployment
- DOM tree compression and filtering mitigations do not generalize well across different websites and novel task scenarios, leaving the core cost problem unresolved
- Web API action spaces available to agents are far narrower than browser UI action spaces, constraining what hybrid agents can accomplish autonomously
- Web APIs cannot directly manipulate stateful objects (e.g., sorting product lists), forcing hybrid agents to fall back to brittle browser UI interaction for state-dependent tasks
- Frequent API calls by web agents trigger rate limiting and request denials, degrading agent effectiveness for tasks requiring high API call frequency
- Browser-based web agents with access to user accounts can cause unauthorized actions — unauthorized purchases, harmful message sending — due to absence of adequate access controls
- Security guardrails (password prompts, two-factor authentication) can be bypassed when agents communicate directly with internal web APIs via elevated API keys
- Web agents are vulnerable to prompt-level, HTML-level, and vision-level adversarial attacks, with no robust defense mechanisms yet available for production deployment
- As web agent traffic scales, repeated page rendering by automation tools strains web infrastructure, causing performance degradation for human users — a worsening externality with no current structural solution
- CAPTCHA systems are escalating in complexity as a direct arms-race response to agent sophistication, creating accessibility barriers for legitimate human users with no principled resolution
- Computing reward signals for web agent RL training requires elaborate bespoke engineering per-task and per-environment, blocking scalable RL-based web agent training
- Action spaces for web agents are incompatible across frameworks (BrowserGym vs. concurrent action space proposals), preventing cross-framework policy learning and RL transfer
- Web agents trained on specific UI patterns generalize poorly to novel website designs — a UI framework rewrite leaves agents non-functional despite the task being identical
- MCP's stateless JSON-RPC 2.0 protocol cannot track website state between calls, requiring full re-querying for state-dependent actions and incurring substantial redundant bandwidth overhead
- MCP server implementations are not standardized in their method signatures and parameters — the same conceptual operation requires different inputs across different server implementations (GitHub vs GitLab), undermining composability
- Distinguishing malicious automation from beneficial human-in-the-loop web agent applications is unsolved at the access control and policy layer, leading to blunt defensive measures that harm legitimate use

## Bottlenecks

- Web interfaces are designed for humans — creating a fundamental representational mismatch that forces agents to choose between information-incomplete screenshots and token-prohibitive DOM trees, with no current representation that is both complete and efficient
- No standardized agent-facing web interface exists — each research group independently develops site-specific workarounds that become obsolete with UI redesigns, creating a fragmented and non-generalizing ecosystem
- Web agent RL training is blocked by per-environment reward engineering complexity and incompatible action spaces across frameworks, preventing scalable cross-framework policy learning for web tasks

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/skillweaver|SkillWeaver]]
- [[entities/webarena|WebArena]]
