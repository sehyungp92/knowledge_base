---
type: source
title: Equipping agents for the real world with Agent Skills \ Anthropic | Claude
source_id: 01KJS276S89V12MY2AXQ1DWBE5
source_type: article
authors: []
published_at: '2025-10-16 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- software_engineering_agents
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Equipping agents for the real world with Agent Skills \ Anthropic | Claude

**Authors:** 
**Published:** 2025-10-16 00:00:00
**Type:** article

## Analysis

# Equipping agents for the real world with Agent Skills \ Anthropic | Claude
2025-10-16 · article
https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

## Briefing

**Anthropic introduces Agent Skills — a filesystem-based, progressively disclosed packaging format that lets any user or developer transform a general-purpose Claude agent into a specialized one by bundling instructions and executable code into a folder. The core design insight is that context can be loaded lazily in layers, making the total bundled knowledge effectively unbounded despite finite context windows, and that deterministic code execution should be delegated to scripts rather than token generation.**

### Key Takeaways
1. **Skills are directories, not APIs** — The entire format is a folder with a `SKILL.md` entry point; no special runtime or infrastructure is required beyond Claude's existing filesystem and code-execution tools.
2. **Progressive disclosure eliminates context window limits** — Only skill metadata (name + description) is pre-loaded at startup; the body and linked files are fetched lazily, making bundled context "effectively unbounded."
3. **The skill name/description is the routing signal** — Claude uses these two fields alone to decide whether to trigger a skill; poorly written metadata is the primary failure mode for under- or mis-triggered skills.
4. **Code in skills is preferable to LLM inference for deterministic operations** — Sorting via token generation is explicitly cited as far more expensive than a script; skills package pre-written executables Claude can run without loading them into context.
5. **Skills replace the fragmented custom-agent model** — Rather than building a bespoke agent per use case, organizations encode procedural knowledge once as a composable skill and attach it to any general-purpose agent.
6. **The PDF skill illustrates splitting context by scenario** — Form-filling instructions live in `forms.md` (loaded only when needed), keeping the core `SKILL.md` lean while still supporting deep functionality.
7. **Skills were published as an open standard in December 2025** — Two months after launch, Anthropic standardized the format for cross-platform portability, signaling intent beyond Anthropic's own products.
8. **Malicious skills are a real attack surface** — Skills can inject instructions to exfiltrate data or exploit the execution environment; auditing bundled code and external network calls is the recommended mitigation.
9. **Self-reflective iteration is the recommended authoring workflow** — Asking Claude what went wrong when using a skill surfaces what context it actually needed, rather than the author guessing upfront.
10. **Autonomous skill authoring is the stated long-term goal** — Anthropic explicitly plans for agents to create, edit, and evaluate their own skills, codifying discovered behavioral patterns into reusable capabilities.
11. **Skills and MCP are complementary, not competing** — Skills teach procedural workflows *using* MCP-connected external tools, not a replacement for the protocol layer.

---

### What Agent Skills Are and Why They Exist

- **The core problem** is that general-purpose agents lack procedural knowledge and organizational context required for real work — model capability is necessary but not sufficient.
  - Claude Code can accomplish complex cross-domain tasks but has no native mechanism to carry domain-specific expertise across deployments.
  - The existing solution — building custom agents per use case — is fragmented, hard to share, and doesn't scale across an organization.
- **Agent Skills** solve this by packaging expertise into composable, portable folders: "organized folders of instructions, scripts, and resources that agents can discover and load dynamically."
  - The analogy used is an onboarding guide for a new hire: structured, reusable, transferable knowledge rather than bespoke engineering.
- **The format is intentionally minimal**: a directory containing at minimum a `SKILL.md` file with YAML frontmatter specifying `name` and `description`.
  - Simplicity is a design goal — it lowers the barrier for non-engineers to contribute skills, and makes the format auditable.

---

### The Progressive Disclosure Architecture

- **Three layers of context depth**, each loaded only when needed:
  - **Layer 1 — Metadata in system prompt**: At startup, only `name` and `description` for every installed skill are loaded. This is enough for Claude to route to the right skill.
  - **Layer 2 — Full SKILL.md body**: When Claude judges a skill relevant to the current task, it reads the full `SKILL.md` into context.
  - **Layer 3+ — Linked files**: For larger skills, `SKILL.md` references additional files (e.g., `reference.md`, `forms.md`) that Claude fetches only in the specific sub-scenarios that require them.
- **Consequence: context bundled per skill is effectively unbounded**, because Claude never needs to load the entirety of a skill's directory at once.
  - This sidesteps context window constraints without requiring chunking, retrieval systems, or vector search — the agent navigates the file structure itself.
- **The PDF skill is the worked example**:
  - `SKILL.md` is lean: it describes PDF capabilities and references two additional files.
  - `forms.md` contains form-filling instructions and is fetched only when the task involves forms — "the skill author is able to keep the core of the skill lean, trusting that Claude will read forms.md only when filling out a form."
  - A Python script for extracting form fields is bundled and executed by Claude without loading the script or the PDF into context.

---

### Code Execution as a First-Class Skill Component

- Skills can include executable scripts that Claude runs as tools at its discretion, not just markdown instructions.
  - **The PDF skill's Python script** extracts all form fields from a PDF deterministically — Claude invokes it rather than 

## Key Claims

1. Agent Skills are organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks.
2. At its simplest, a skill is a directory that contains a SKILL.md file with YAML frontmatter specifying name and description metadata.
3. At startup, the agent pre-loads the name and description of every installed skill into its system prompt.
4. The skill metadata serves as the first level of progressive disclosure, providing enough information for Claude to know when each skill should be used without loading all of it into context.
5. If Claude thinks a skill is relevant to the current task, it will load the skill by reading its full SKILL.md into context as the second level of detail.
6. Skills can bundle additional files within the skill directory referenced by name from SKILL.md, forming a third (and beyond) level of progressive disclosure that Claude navigates only as needed.
7. Progressive disclosure makes the amount of context that can be bundled into a skill effectively unbounded.
8. Skills can include pre-written code that Claude executes as tools at its discretion, without loading the script or its inputs into context.
9. Sorting a list via token generation is far more expensive than simply running a sorting algorithm, illustrating why code execution is preferable to LLM-native approaches for certain operations.
10. Code execution within skills provides deterministic reliability that LLM token generation cannot, making workflows consistent and repeatable.

## Capabilities

- General-purpose agents can dynamically discover and load domain-specific skill packages at runtime using progressive disclosure — loading only metadata at startup, full SKILL.md when relevant, and linked sub-files only as needed, keeping the active context lean while making deep expertise accessible
- Skill directories can bundle effectively unbounded domain knowledge because progressive disclosure allows agents to navigate file hierarchies on demand — the practical limit on bundled knowledge is decoupled from the context window size
- Skills can package executable code as deterministic tools — agents run pre-written scripts rather than attempting to replicate deterministic operations via token generation, enabling consistent, repeatable workflows without loading code or large inputs into context
- Claude can fill out PDF forms and manipulate PDF documents directly via an agent skill that bundles Python scripts for form-field extraction and structured instructions for form-filling workflows
- Agent Skills work cross-platform across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform — a single skill directory is portable across all supported environments

## Limitations

- Claude cannot directly manipulate PDFs (e.g., fill out forms) at the base model level — understanding PDFs is possible but programmatic manipulation requires external tooling
- LLM token generation is computationally expensive and unreliable for deterministic operations (sorting, arithmetic, structured extraction) that are trivially solved by traditional code — the mismatch between probabilistic generation and deterministic requirements is structural
- Skills must currently be authored, curated, and maintained by humans — agents cannot yet autonomously create, edit, or evaluate skills from their own successful task patterns
- Agents using skills exhibit unexpected execution trajectories and overreliance on certain contexts — skill behavior in real-world scenarios is difficult to predict and requires iterative human observation to correct
- No automated security vetting mechanism exists for skill packages from untrusted sources — malicious skills can introduce environment vulnerabilities, exfiltrate data, or trigger unintended agent actions, requiring full manual human audit before use
- The context window size constraint is the fundamental architectural driver behind the entire progressive disclosure design — without filesystem access and dynamic file loading, all skill knowledge would need to fit in context, making comprehensive domain coverage impossible at scale
- Skills require careful prompt engineering of the name and description fields — the agent's decision to trigger a skill is entirely dependent on these brief metadata strings matching the task at hand, creating a fragile dependency on accurate labeling

## Bottlenecks

- Human bottleneck in agent skill authorship — skills must be written, tested, and iterated by domain experts, limiting the rate at which specialized agent capabilities can be developed and distributed; the inability of agents to self-author skills caps the scalability of the ecosystem
- Absence of automated skill security infrastructure blocks safe open distribution of community-authored agent skills — trust currently depends on source reputation and manual human code review rather than technical verification, creating a security ceiling on ecosystem openness

## Breakthroughs

- Progressive disclosure architecture for agent skill packaging decouples domain knowledge capacity from context window size — by organizing expertise as a navigable file hierarchy rather than a flat context payload, general-purpose agents can carry effectively unbounded domain-specific knowledge with

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/software_engineering_agents|software_engineering_agents]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/claude-code|Claude Code]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
