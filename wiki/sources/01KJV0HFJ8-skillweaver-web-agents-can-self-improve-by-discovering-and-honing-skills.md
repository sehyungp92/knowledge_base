---
type: source
title: 'SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills'
source_id: 01KJV0HFJ8JQFQQYJF6MAH6BHW
source_type: paper
authors:
- Boyuan Zheng
- Michael Y. Fatemi
- Xiaolong Jin
- Zora Zhiruo Wang
- Apurva Gandhi
- Yueqi Song
- Yu Gu
- Jayanth Srinivasa
- Gaowen Liu
- Graham Neubig
- Yu Su
published_at: '2025-04-09 00:00:00'
theme_ids:
- agent_evaluation
- agent_self_evolution
- agent_systems
- computer_use_and_gui_agents
- evaluation_and_benchmarks
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills

**Authors:** Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, Yu Su
**Published:** 2025-04-09 00:00:00
**Type:** paper

## Analysis

# SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills
2025-04-09 · paper · Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi et al. (11 total)
https://arxiv.org/pdf/2504.07079

---

### Motivation & Prior Limitations
Web agents based on LLMs struggle to generalize to novel websites and out-of-distribution task types because they lack the capacity to explicitly abstract reusable procedural knowledge from experience.
- Trajectory-based self-improvement methods (e.g., WebGUM, ETO, PAE) store skills implicitly as action sequences used for in-context learning or fine-tuning, which creates heavy training demands, risks catastrophic forgetting, and generates memory-intensive artifacts (~0.3 GB per trajectory in Mind2Web) that are impractical to transfer between agents.
- Natural-language workflow methods (Agent Workflow Memory, ICAL) improve abstraction but cannot be formally verified or precisely composed into new workflows, and both require either online access to test queries or high-quality annotated demonstrations — leaving autonomous, unsupervised exploration unaddressed.
- Existing agents trained on large-scale trajectory datasets tend to overfit to specific website structures and task distributions, reducing their ability to handle previously unseen environments effectively.

---

### Proposed Approach
SkillWeaver is a three-stage, skill-centric framework that enables web agents to autonomously self-improve by exploring website environments and distilling successful trajectories into reusable Python APIs backed by Playwright browser automation code.
- Unlike trajectory-based or natural-language workflow methods, SkillWeaver represents skills as executable Python functions with typed signatures, docstrings with usage logs, and prerequisite-state documentation, enabling formal unit testing, static analysis, precise composition, and lightweight transfer between agents without retraining.
- **Stage I — Skill Proposal**: An LLM acting as an automatic curriculum observes screenshots, accessibility trees, URLs, and HTML to propose novel, reusable skills in three categories: procedural tasks (multi-step workflows), navigational tasks (conceptual mapping of site structure), and information-seeking tasks (scraping APIs for enumeration). The LLM is explicitly prompted to avoid duplicating existing skills in the library, and a curriculum progression from simple to compositional skills governs the ordering.
- **Stage II — Skill Synthesis**: The base agent executes proposed tasks repeatedly; an LLM-based reward model evaluates success using the task description, full action trajectory with screenshots, and environmental feedback. Successful trajectories are converted into parameterized Python functions via LLM code generation, followed by static analysis to catch common generation errors before acceptance.
- **Stage III — Skill Honing**: Synthesized APIs are validated through automated unit testing — APIs with no required parameters are executed directly; APIs with parameters use LLM-generated test cases — and debugged iteratively using environment feedback and reward model signals to ensure reliability at inference time.
- The exploration loop runs for 160 iterations per website with GPT-4o; during inference, an API selection module filters relevant and precondition-satisfying APIs from the growing library before presenting them to the agent.

---

### Results & Capabilities
SkillWeaver achieves a 31.8% relative improvement in average success rate on the WebArena benchmark (12.3% baseline → 22.6% with GPT-4o, then +32% further with skills to 29.8%) and a 39.8% relative improvement on real-world live websites evaluated via Online-Mind2Web.
- The improvement is consistent across all five WebArena domains (Gitlab +25%, Map +23%, Shopping +38%, CMS +38%, Reddit +33%), and across four real-world live websites (Drug +34%, Flight +151%, Cooking +20%), with no site showing a regression.
- Weaker agents (GPT-4o-mini backbone) benefit even more dramatically from APIs synthesized by the stronger GPT-4o agent: success rates improve 40–133% across WebArena sites, with a GPT-4o-mini + Skills configuration outperforming the GPT-4o baseline without skills on Map, Shopping, and Reddit — demonstrating effective knowledge distillation through plug-and-play API transfer with no additional training.
- Synthesized APIs are competitive with human-crafted APIs from official documentation on low- and medium-API-support websites (Reddit, Shopping) and outperform the no-API baseline by comparable margins, validating the quality of autonomous exploration; on high-API-support sites (GitLab, Maps), human APIs retain an advantage.
- An emergent compositional behavior appears after sufficient iterations: the pipeline begins synthesizing higher-order APIs that call multiple simpler APIs in sequence (e.g., closing an overlay then applying two search filters), indicating increasing hierarchical abstraction without explicit compositional supervision.
- SkillWeaver outperforms AutoEval (inference-time LLM-guided exploration) on average across WebArena and matches or exceeds SteP (human-written domain-specific workflows) on CMS and Map environments.

---

### Implications
SkillWeaver demonstrates a viable path to non-parametric, continual self-improvement for web agents — agents can accumulate structured procedural knowledge indefinitely without weight updates, sidstepping catastrophic forgetting and the data-pipeline costs of fine-tuning approaches.
- The API-as-skill representation decouples skill acquisition from agent architecture: a library synthesized by a strong frontier model can be redistributed to and immediately exploited by weaker or cheaper models, suggesting a marketplace or open-source ecosystem model for web agent capabilities analogous to software libraries.
- The three-stage pipeline (propose → practice → hone) generalizes the Voyager framework from open-ended game env

## Key Claims

1. SKILLWEAVER achieves a 31.8% relative success rate improvement on WebArena benchmark
2. SKILLWEAVER achieves a 39.8% relative success rate improvement on real-world websites
3. APIs synthesized by strong agents can enhance weaker agents by up to 54.3% on WebArena
4. Trajectory-based self-improvement approaches struggle to explicitly abstract reusable procedural knowledge, resulting in heavy training demands and limited generalization
5. Continuously updating models with new trajectories introduces catastrophic forgetting and sensitivity to website changes
6. Natural language-based reusable routines pose challenges for formal verification and precise composition into new workflows
7. SKILLWEAVER's exploration process requires no annotated data and enables agents to gather experiences through autonomous environment exploration
8. Weaker agents (GPT-4o-mini) see even more dramatic improvements from synthesized APIs, ranging from 40% to 133% on WebArena
9. GPT-4o-mini with synthesized APIs achieves better average success rate than baseline GPT-4o on Map, Shopping, and Reddit websites
10. Synthesized APIs are comparable in quality to human-crafted APIs on websites with low and medium API support

## Capabilities

- Web agents can autonomously self-improve through iterative environment exploration — proposing novel skills, synthesizing them as executable Python/Playwright APIs, and testing/debugging — all without human supervision, labeled demonstrations, or model weight updates
- Compositional skills emerge spontaneously from iterative web agent exploration — after sufficient iterations, agents begin generating higher-order APIs that internally chain simpler previously-synthesized APIs without being explicitly instructed to do so
- APIs synthesized by a stronger web agent (GPT-4o) function as plug-and-play modules enabling a weaker agent (GPT-4o-mini) to match or exceed the stronger agent's unaided performance — up to 133% relative improvement and cross-model capability parity without retraining

## Limitations

- LLMs including GPT-4o are insufficiently robust at API calling — they fail both to identify the correct API from a library and to generate correct parameter values, undermining skill-augmented agents even when the underlying skills are well-specified
- Web agent skill synthesis is implicitly constrained to short-horizon, single-API-call tasks — complex multi-step workflows requiring long-range planning and backtracing cannot be reliably synthesized, capping the complexity ceiling of the approach
- Skill synthesis requires full per-website exploration from scratch with no cross-website transfer of synthesis strategies — 160 LLM-driven iterations of overhead are required before any performance gain is available on a new site
- Partially observable web environments — where critical information only surfaces during mid-interaction (dynamic product results, context-dependent pages) — cause performance cliffs that synthesized APIs cannot mitigate
- Visual reasoning and environment understanding failures at final task steps are not resolved by API augmentation — agents guided correctly to the penultimate state by APIs still fail the last-mile steps requiring real-time visual grounding
- Trajectory-based model fine-tuning approaches exhibit catastrophic forgetting and sensitivity to website structural changes — skills become stale whenever website UIs are updated
- Synthesized APIs underperform human-crafted APIs on websites with high structured API support (GitLab, Maps) — the autonomous synthesis gap widens when rich programmatic documentation is available but inaccessible to the exploration agent
- Real-world evaluation was implicitly restricted to 4 out of 136 websites due to exploration cost — results may not generalise to the long tail of websites with fewer tasks or non-Playwright-compatible UIs
- Web interaction trajectory storage is prohibitively expensive for large-scale knowledge sharing — multimodal trajectories (screenshots + HTML) consume ~0.3 GB per trajectory, making trajectory-based skill transfer impractical compared to code-based APIs
- Natural language-based routine representations (prior work) cannot be formally verified or precisely composed — only code-based representations provide the execution semantics needed for unit testing and compositional guarantees

## Bottlenecks

- Web agent generalisation to novel websites is blocked by the absence of cross-site skill transfer — current synthesis approaches require full per-website exploration, making deployment to the long tail of websites economically and computationally prohibitive
- LLM parameter generation precision for API calls forms a last-mile bottleneck in skill-augmented web agents — agents correctly identify the right API but produce semantically incorrect argument values, creating failures that are invisible without ground-truth oracle checking

## Breakthroughs

- Web agents achieve substantial self-improvement (31.8–39.8% on benchmarks) through fully non-parametric skill synthesis — building executable API libraries via autonomous exploration with no weight updates, no human annotations, and no pre-defined task queries
- Procedural web knowledge distils non-parametrically from stronger to weaker models via executable APIs — GPT-4o-synthesised skills boost GPT-4o-mini by up to 133%, enabling the weaker model to match or exceed the stronger model's unaided performance with no gradient updates

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/agent-workflow-memory|Agent Workflow Memory]]
- [[entities/codeact|CodeAct]]
- [[entities/skill-library|Skill Library]]
- [[entities/skillweaver|SkillWeaver]]
- [[entities/webarena|WebArena]]
