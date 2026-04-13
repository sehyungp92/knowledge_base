---
type: theme
title: Software Engineering Agents
theme_id: software_engineering_agents
level: 2
parent_theme: agent_systems
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 53
sources_since_update: 0
update_count: 1
velocity: 0.473
staleness: 0.0
status: active
tags: []
---
# Software Engineering Agents

> Software engineering agents have moved decisively past the question of whether they can code and into a race over how cheaply, reliably, and autonomously they can operate at scale — with the frontier now defined less by benchmark scores than by production economics and simulation fidelity. The arc from IDE assistant to autonomous engineer has accelerated through multiple inflection points, culminating in AlphaEvolve's deployment on Google's live infrastructure in mid-2025, while open-source models have compressed the capability moat of proprietary labs faster than anticipated, and the central bottleneck has shifted from model intelligence to training infrastructure and interaction paradigm design.

**Parent:** [[themes/agent_systems|Agent Systems]]

---

## Current State

Software engineering agents have moved decisively past the question of whether they can code and into a race over how cheaply, reliably, and autonomously they can operate at scale — with the frontier now defined less by benchmark scores than by production economics and simulation fidelity.

The arc from IDE assistant to autonomous engineer accelerated through several inflection points. Cursor-paradigm integration established the baseline: direct codebase access, diff-based editing, error-aware iteration. The next shift was ownership of execution surfaces — agents managing full DocuSign workflows, owning DevOps on-call rotations, and autonomously resolving incidents without escalation. By mid-2025, Google's AlphaEvolve crossed the most meaningful threshold yet: a coding agent running in production, recovering 0.7% of fleet-wide compute and cutting Gemini training time by 1% through self-discovered scheduling heuristics and kernel rewrites. This wasn't a demo — it was infrastructure impact at mission-critical scale, and it redefined what "coding agent" means from assistant to autonomous engineer operating on live systems.

The benchmark frontier has compressed dramatically. SWE-bench Verified scores that seemed aspirational in early 2025 are now table stakes: o3 achieves SOTA without custom scaffolds (signaling general reasoning sufficiency), Claude 4 Sonnet scores 35.5% on the harder terminal-based SWE-Terminal-Bench, and Kimi K2's September 2025 release (65.8% SWE-bench Verified, #1 open-source) demonstrated that frontier-grade agentic performance is now achievable in open weights. The open-source parity story is compressing the capability moat of proprietary labs faster than anticipated. Yet the 36% of real-world engineering tasks that remain unsolvable even with 100-iteration budgets indicates the frontier is not yet close to general autonomous engineering.

The central bottleneck has crystallized around training infrastructure rather than model intelligence: synthetic simulation environments cannot replicate real-world tool execution complexity, forcing expensive hybrid real-sandbox pipelines that constrain the scale of agentic RL training. A secondary bottleneck has emerged around prompting paradigm shift — GPT-5-class models degrade significantly when prompted as models rather than agents, indicating that the entire interaction paradigm must evolve toward compass-style orientation. Meanwhile, CUDA kernel optimization work remains technically impressive but economically constrained ($4–5 per kernel, 1.5-hour wall clock, evaluation limited to MNIST-scale kernels) — the attention-scale and sparse-operation cases that dominate real training costs remain untested.

Watch for whether hybrid real-sandbox infrastructure closes the simulation fidelity gap within 12–18 months (this is the unlock for cheaply scalable agentic RL), whether CUDA kernel optimization generalizes to transformer-scale complexity, and whether the open-source agentic capability race accelerates enterprise deployment by making self-hosted, near-frontier coding agents economically viable — which would structurally threaten the per-token revenue model of closed-weights lab products.

---

## Capabilities

Capabilities span a wide maturity spectrum, from production-proven engineering automation to early-stage research demonstrations.

**In narrow production use:**
- IDE-integrated AI coding assistants with direct codebase access, diff-based editing, and error-aware iteration (Cursor paradigm) represent the established baseline.
- Iterative self-correcting debugging — identifying what a failed attempt reveals, reasoning about it, and making targeted corrections — and robust recovery from tool call failures enable longer-horizon autonomous operation.
- Coding agents can reason across codebases, tickets, telemetry, and architectural graphs, learning from patterns of failure across time. AI DevOps on-call agents autonomously resolve software incidents, reduce mean time to repair (MTTR), and triage technical alerts without escalation.
- AI agents complete end-to-end contract workflows (DocuSign) from short natural language prompts, owning the full execution surface. Runtime-configurable agents adapt business rule changes (thresholds, allow-lists, YAML policies) without redeployment. Reusable implementation scaffolding (custom adapters, monitoring dashboards, migration scripts, ingestion kits) compounds across deployments.
- Best AI systems reliably manage ~100 sequential steps at 99% per-step accuracy, equivalent to a day or two of focused human work. Horizon length for software and coding agents has been doubling every 7 months (METR research).
- LLMs can refactor entire multi-language codebases across thousands of lines in a single prompt, including architectural changes. One-shot resolution of complex nested dependency conflicts across large codebases, succeeding where frontier models (o3, etc.) fail.
- o3 sets new SOTA on SWE-bench Verified without a custom model-specific scaffold, and on Codeforces and MMMU, making 20%+ improvements a threshold signal of general reasoning sufficiency.
- Open-source MoE LLMs achieving frontier agentic performance: Kimi K2 (32B activated / 1T total params) at 65.8% SWE-bench Verified single-attempt; a separate MoE (355B total, 32B active) unifying reasoning, coding, and agentic capabilities, with SWE-Terminal-Bench leading score of 37.5% — outperforming o3 (30.2%), GPT-4.1 (30.3%), Claude 4 Sonnet (35.5%), and Gemini.
- Evolutionary coding agent discovers and deploys production-grade infrastructure optimizations autonomously: 0.7% Google fleet-wide compute recovery and 1% Gemini training time reduction (AlphaEvolve). AI agents directly optimize compiler-generated IRs of production ML kernels despite IR opacity.

**Research / demo stage:**
- LLM-driven evolutionary pipeline for CUDA kernel optimization achieves up to 12.52x speedup over PyTorch native and 24.8x over reference code. Automatic CUDA operation fusion via LLM agents combining multiple discrete operations into single optimized kernels. LLM-based soft verification of CUDA kernel correctness (compilation, memory access, numerical) achieving up to 82% accuracy. Discovered CUDA kernels generalize across GPU architectures (H100, RTX 4090, A6000).
- AI coding agent evolves entire multi-function, multi-language codebases of hundreds of lines (vs. prior systems limited to single functions).
- Major labs training agents inside simulated versions of the top 150 websites and every major system of record.
- Codex CLI: open-source lightweight coding agent for terminal use, combining o3/o4-mini reasoning with local codebase access.

---

## Limitations

**Compounding error at horizon (blocking, improving):** Per-step error rates compound ruthlessly — at 99% per-step accuracy, a 100-step task succeeds only ~37% of the time. This is the primary ceiling on long-horizon autonomous operation and directly explains why 36% of real-world engineering tasks remain unsolvable even with 100-iteration budgets.

**Simulation fidelity (significant, improving):** Synthetic simulation environments cannot replicate real-world tool execution complexity, forcing expensive hybrid real-sandbox pipelines. This constrains the scale of agentic RL training — the central bottleneck to cheaply scalable agentic improvement.

**Prompting paradigm mismatch (significant, stable):** Prompting GPT-5-class models as models rather than agents degrades output quality significantly. The entire interaction paradigm must evolve toward compass-style orientation — a structural shift, not a parameter tweak.

**Context and architecture dependency (significant, stable):** Removing context from prompts substantially degrades performance — the system depends heavily on rich context injection. Removing full-file evolution (restricting to single-function evolution as in FunSearch) significantly degrades performance. Performance degrades significantly when SOTA frontier LLMs are replaced with smaller base models — the system is tightly coupled to frontier model capability.

**Human scaffolding requirements (significant, stable):** AlphaEvolve requires a human-provided initial program (even if rudimentary) and evaluation function — it is not fully autonomous problem discovery. Agents operating in shadow enterprise processes (undocumented SOPs, desktop procedures, unofficial workarounds) cannot learn from or replicate those workflows. AI tools currently handle discrete tasks in isolation but cannot autonomously manage complex, multi-step enterprise workflows end-to-end without structured process scaffolding.

**Kernel optimization economics (significant, improving):** API cost accumulates to $4–5 per kernel optimization task. The pipeline requires 4 GPU devices and ~1.5 hours of wall-clock time per kernel. Evaluation is limited to small, well-understood kernel types (MNIST-scale convolutions, linear layers, simple activations) — the attention-scale and sparse-operation cases that dominate real training costs remain untested.

**Benchmark and capability gaps (significant, mixed):** SWE-bench Verified 64.2% leaves ~36% of real-world software engineering tasks unsolved. Kimi K2 lags Claude Sonnet 4 and Claude Opus 4 on SWE-bench Verified agentic coding (65.8% vs 72.7%/72.5%) and Terminal-Bench. GLM-4.5 underperforms Claude-4-Sonnet on holistic agentic coding despite leading on tool-calling success rate — winning on a proxy metric does not translate cleanly to end-to-end task completion.

**Verification and safety gaps (significant, unclear):** LLM numerical correctness verifier achieves only 73% accuracy — roughly one in four numerical correctness judgments is wrong. No discussion of safety, security, or adversarial robustness of LLM-generated CUDA kernels deployed in production — a silent gap with significant production risk.

**One-shot degradation (significant, stable):** One-shot prompting for complete software projects yields significant performance degradation vs. agentic frameworks; model capability alone is insufficient without multi-step scaffolding.

**Ecosystem gaps (minor, improving):** Agents SDK limited to Python at launch — no Node.js support, cutting off the large JS/TS developer community. Contributions from non-programmers to agent systems require heavy revision and filtering, despite enabling first-time participation.

---

## Bottlenecks

**Simulation fidelity gap for agentic RL training** (active, 1–2 year horizon): Synthetic tool execution environments cannot fully replicate real-world complexity — filesystem state, network variability, concurrent process interaction, version-specific API behavior. This forces investment in expensive real execution sandboxes to achieve authentic feedback signals, directly blocking fully synthetic, cheaply scalable agentic RL training pipelines. Until this closes, the cost of improving agents via RL on realistic software engineering tasks remains high, throttling the rate of capability improvement.

**Sequential LLM sampling dependency in CUDA kernel translation** (active, 1–2 year horizon): Each refinement step in the kernel optimization pipeline must wait for compilation and GPU result feedback before the next LLM call — the pipeline cannot be parallelized across refinement iterations. This blocks scalable automated kernel optimization across large codebases and diverse kernel types, limiting the economic viability of LLM-driven kernel optimization at production scale.

---

## Breakthroughs

**Multi-thousand-line codebase refactoring in a single prompt** (major): LLMs can refactor entire multi-thousand-line codebases across different programming languages in a single prompt, including architectural changes. Prior belief: code generation was limited to individual functions or files; large-scale refactoring required human architectural planning and step-by-step guidance. This redrew the boundary of what constitutes a "coding task" vs. a "software engineering project."

**Moore's Law-like agent horizon scaling** (notable): Empirical discovery that AI agent horizon length has been doubling every 7 months (METR research group) — establishing a consistent scaling law for long-horizon task reliability. Prior belief: progress was perceived as erratic and hard to extrapolate. This provides an actionable extrapolation framework for anticipating when autonomous engineering becomes viable for specific task durations.

**AlphaEvolve: production infrastructure impact** (notable): LLM-guided evolutionary coding agent deployed in production at Google, recovering 0.7% of fleet-wide compute and reducing Gemini training time by 1% through self-discovered scheduling heuristics and kernel rewrites. Prior belief: mission-critical infrastructure optimization required months of dedicated expert engineering; AI approaches offered worse interpretability-performance tradeoffs than expert systems. This is the clearest evidence yet that autonomous coding agents can operate on live, mission-critical systems — not just development environments.

**Open-source model reaches near-frontier agentic performance** (notable): Kimi K2 ranks #1 open-source and #5 overall on LMSYS Arena at launch (September 2025), achieving 65.8% on SWE-bench Verified. Prior belief: open-source models lagged significantly behind proprietary frontier models on agentic and software engineering benchmarks, with the gap considered large enough to limit viability of open-weight deployment in production agentic applications. The implication is structural: enterprises can now self-host near-frontier coding agents, threatening the per-token revenue model of closed-weights API products.

---

## Anticipations

- **Simulation fidelity gap closure (12–18 months):** Whether hybrid real-sandbox infrastructure closes the simulation gap is the unlock for cheaply scalable agentic RL. If it closes, expect a step-change in the rate of agentic RL capability improvement.
- **CUDA kernel optimization generalization:** Whether the demonstrated speedups on MNIST-scale kernels transfer to transformer-scale attention and sparse operations — the cases that dominate real training costs — is the key question for economic viability of LLM-driven kernel optimization.
- **Open-source agentic capability race:** Whether open-weights parity accelerates enterprise deployment of self-hosted coding agents, structurally undermining per-token API pricing for coding agent products.
- **Prompting paradigm shift:** As GPT-5-class and successor models require agent-oriented interaction patterns, expect widespread migration of production pipelines away from model-style prompting toward compass-style orientation — with significant breakage for teams that don't adapt.
- **Tool-calling reliability as primary differentiator:** As raw reasoning capability approaches sufficiency for many SE tasks, tool-calling success rate (90.6% for GLM-4.5 vs 77.1% for Qwen3-Coder) is emerging as the key differentiator — implying BFCL-v3-style function-calling benchmarks should be weighted heavily in model selection.

---

## Cross-Theme Implications

**→ [[themes/frontier_lab_competition|Frontier Lab Competition]]:** GLM-4.5 (Zhipu AI, China) achieving 64.2% on SWE-bench Verified and 90.6% tool-calling success — competitive with or exceeding Claude 4 Sonnet and GPT-4.1 — signals that frontier software engineering agent capability is no longer a US-lab exclusive, intensifying global competition in the most commercially valuable AI application domain.

**→ [[themes/ai_pricing_and_business_models|AI Pricing and Business Models]]:** Open-weights GLM-4.5 at frontier agentic coding performance creates direct pricing pressure on Claude Code and similar API-gated products. Enterprises can now run comparable agentic coding pipelines on self-hosted infrastructure, threatening the usage-based revenue model of labs whose moat was closed-weights capability advantage. This accelerates the shift toward outcome-based or platform-level pricing. Separately, mature SE agents lower the barrier to building personal AI infrastructure to hours of work — compressing the product formation cycle and implying vertical AI products may increasingly be assembled by individual developers rather than funded teams, disrupting traditional SaaS formation economics.

**→ [[themes/reasoning_and_planning|Reasoning and Planning]]:** Strong software engineering capability appears to generalize into broader multi-step problem-solving — the agent's ability to decompose unknown file-handling problems (unknown extension → header inspection → tool selection → fallback strategy) maps directly from debugging and refactoring skills. SE agent benchmarks may therefore underestimate general reasoning capability.

**→ [[themes/benchmark_design|Benchmark Design]]:** The introduction of SWE-Bench Multilingual as an evaluation axis signals that English-only benchmarks are insufficient for assessing real-world SE agent capability, driving demand for multilingual and cross-ecosystem evaluation frameworks. SWE-Terminal-Bench is emerging as a harder, more discriminating axis than SWE-bench Verified.

**→ [[themes/agent_systems|Agent Systems]] (internal):** Several cross-cutting dynamics reinforce each other within SE agents:
- Open-sourcing frontier-class agentic MoE models (Kimi K2) dramatically lowers the barrier to building capable SE agents — teams no longer require proprietary API access.
- Achieving SOTA on SWE-bench *without* custom scaffolds signals that general reasoning is becoming sufficient for repository-level SE — shifting the bottleneck from model capability to task grounding, tool integration, and long-horizon state management.
- Tool-calling success rate is emerging as a primary differentiator independent of raw reasoning ability.
- Native zero-shot tool understanding reduces engineering overhead for building SE agents, shifting complexity from orchestration code to model capability.
- Built-in computer use and file search as first-class API tools reduce integration burden for coding agent developers.
- Hybrid thinking/non-thinking mode architecture — extended reasoning applied selectively to complex sub-tasks — lifts SE agent performance; GLM-4.5's SWE-Terminal-Bench score of 37.5% (vs o3's 30.2%) implies future agent scaffolds should route subtasks to thinking mode dynamically.
- Multi-agent orchestration primitives enable SE pipelines that decompose complex repository-level tasks (planning, implementation, testing, review) across specialized sub-agents.
- Self-building agents at Levels 1–3 effectively merge agent self-evolution with automated software engineering, blurring the boundary between agent orchestration and code generation.
- RLVR training (originally validated on math/formal reasoning) appears to generalize effectively to open-ended, multi-step tool-use scenarios — implying RLVR is a general mechanism for improving agentic reliability, not a domain-specific one.
- The removal of labeled golden data requirements for RL reward functions directly unblocks RL fine-tuning for SE agents where ground-truth correctness oracles are expensive or incomplete.
- Code interpretation as a standardized tool primitive (e.g., E2B) moves code execution from a custom-built capability to a plug-in service, reducing the marginal cost of building coding agents.
- Claude Code establishing market leadership in consumer coding has made SE agent capability a primary axis of frontier lab competition, incentivizing accelerated investment in coding-specific agent capabilities across all major labs.

**→ Robotics (analog):** If world models can replace hand-coded physics simulators for robotics, an analogous shift may occur for software agents: learned environment models could substitute for expensive real execution environments in code testing, reducing the need for sandbox infrastructure.

---

## Contradictions

- **Tool-calling success vs. end-to-end task completion:** GLM-4.5 leads on tool-calling success rate (90.6%) yet underperforms Claude-4-Sonnet on holistic agentic coding. This contradicts the intuition that tool reliability is the primary differentiator — high proxy-metric performance does not straightforwardly translate to end-to-end task completion, suggesting that tool-calling benchmarks and holistic task benchmarks are measuring partially independent capabilities.
- **Open-source parity claim vs. persistent gap:** Kimi K2 is positioned as near-frontier open-source, yet lags Claude Sonnet 4 and Claude Opus 4 on SWE-bench Verified (65.8% vs 72.7%/72.5%) and Terminal-Bench. "Near-frontier" conceals a meaningful absolute gap on the hardest tasks — the marketing claim and the benchmark delta tell different stories about practical deployment viability.
- **Benchmark sufficiency vs. real-world gap:** o3 achieving SOTA on SWE-bench Verified without custom scaffolds signals general reasoning sufficiency for benchmark tasks — yet 36% of real-world software engineering tasks remain unsolvable with 100-iteration budgets. The benchmark is not representative of the hardest real-world cases, creating a gap between "benchmark solved" and "production ready."
- **Kernel optimization speedups vs. evaluation scope:** 12.52x speedups over PyTorch native are striking, but the entire evaluation is limited to MNIST-scale convolutions and linear layers. The result cannot be extrapolated to transformer-scale attention operations without direct evidence — the speedup claim and the scope of evidence are mismatched.

---

## Research Opportunities

- **Simulation environment fidelity:** Building hybrid real-sandbox training infrastructure that closes the fidelity gap for agentic RL without the cost of fully real execution environments. The 1–2 year horizon on this bottleneck suggests near-term tractability.
- **Transformer-scale CUDA kernel optimization:** Extending the LLM-driven evolutionary kernel optimization pipeline to attention mechanisms and sparse operations — the cases that dominate real training costs — to determine whether demonstrated speedups transfer.
- **Parallelizing refinement pipelines:** Breaking the sequential LLM sampling dependency in kernel translation by developing compilation-aware parallelization strategies or learned surrogate feedback models.
- **Agent-oriented interaction paradigms:** Designing prompting frameworks, training objectives, and scaffolding architectures explicitly for compass-style agent orientation, rather than retrofitting model-oriented patterns.
- **Shadow process discovery:** Methods for agents to discover, surface, and encode undocumented SOPs, desktop procedures, and unofficial workarounds — the dark matter of enterprise process knowledge.
- **Holistic vs. proxy metric alignment:** Understanding why tool-calling success rate and holistic agentic coding performance diverge, and designing evaluation frameworks that better predict end-to-end task completion.
- **RL reward functions without golden data:** Extending the removal of labeled golden data requirements for RL fine-tuning to more complex SE tasks beyond unit-test-verifiable code — opening RL improvement to the long tail of engineering tasks.
- **Multilingual SE agent evaluation:** Building robust multilingual coding benchmarks analogous to SWE-bench Verified across major programming ecosystems to close the English-codebase evaluation bias.
- **Safety and adversarial robustness of LLM-generated kernels:** Characterizing the security surface of LLM-generated CUDA kernels deployed in production — a conspicuously absent research area given the production deployment precedent set by AlphaEvolve.

---

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KKTE8FZZ-untitled-article|Untitled Article]]: New capability: MoE LLM (355B total, 32B active parameters) unifying reasoning, coding, and agen
- **2026-04-08** — [[sources/01KKT3N28G-ai-leads-a-service-as-software-paradigm-shift-foundation-capital|AI leads a service as software paradigm shift - Foundation Capital]]: New capability: AI DevOps on-call agents can autonomously resolve software incidents, reduce mea
- **2026-04-08** — [[sources/01KKTEN0B4-new-tools-for-building-agents|New tools for building agents]]: Limitation identified: Agents SDK limited to Python at launch — no Node.js support, cutting off the lar
- **2026-04-08** — [[sources/01KJRZT83B-2025-the-year-in-llms|2025: The year in LLMs]]: OpenAI initiated the reasoning/inference-scaling/RLVR revolution in September 2024 with o1 and o1-mi
- **2026-04-08** — [[sources/01KKTE8J95-kimi-k2-open-agentic-intelligence|Kimi K2: Open Agentic Intelligence]]: New capability: Open-source MoE LLM (32B activated / 1T total params) achieving 65.8% SWE-bench 
- **2026-04-08** — [[sources/01KKT5MA2X-towards-robust-agentic-cuda-kernel|Towards Robust Agentic CUDA Kernel]]: New capability: LLM-driven evolutionary pipeline for CUDA kernel optimization achieves up to 12.
- **2026-04-08** — [[sources/01KJS1WVEB-interleaved-thinking-unlocks-reliable-minimax-m2-agentic-capability|Interleaved Thinking Unlocks Reliable MiniMax-M2 Agentic Capability]]: The model carries forward plans, hypotheses, constraints, and intermediate conclusions across turns,
- **2026-04-08** — [[sources/01KJSSFZW8-cognition-dont-build-multi-agents|Cognition | Don’t Build Multi-Agents]]: As of June 2025, Claude Code never performs work in parallel with its subtask agents; subtask agents
- **2026-04-08** — [[sources/01KJSTNBZM-ai-horseless-carriages-koomendev|AI Horseless Carriages | koomen.dev]]: Allowing users to write and edit their own system prompts produces better, personalized AI outputs c
- **2026-04-08** — [[sources/01KJSX4F4C-building-effective-ai-agents|Building Effective AI Agents]]: The Model Context Protocol allows developers to integrate with a growing ecosystem of third-party to
- **2026-04-08** — [[sources/01KKT3D2HY-the-46t-services-as-software-opportunity-lessons-from-the-first-year-foundation-|The $4.6T Services-as-Software opportunity: Lessons from the first year - Foundation Capital]]: New capability: Runtime-configurable AI agents that adapt business rule changes (thresholds, all
- **2026-04-08** — Wiki page created. Theme has 53 sources.
- **2026-02-12** — [[sources/01KM251Q7Y-openclaw-the-viral-ai-agent-that-broke-the-internet-peter-steinberger-lex-fridma|OpenClaw: The Viral AI Agent that Broke the Internet - Peter Steinberger | Lex Fridman Podcast #491 [8:55-27:04, 2:34:58-2:46:17]]]: Breakthrough: LLMs can refactor entire multi-thousand-line codebases across different programm
- **2026-02-11** — [[sources/01KJRZT83A-gemini-deep-think-redefining-the-future-of-scientific-research|Gemini Deep Think: Redefining the Future of Scientific Research]]: A research paper (LeeSeo26) demonstrated human-AI collaboration in proving bounds on systems of inte
- **2025-12-21** — [[sources/01KJT3Z974-toward-training-superintelligent-software-agents-through-self-play-swe-rl|Toward Training Superintelligent Software Agents through Self-Play SWE-RL]]: The bug-injection agent is responsible for discovering how to run tests, creating test parsers, and 
- **2025-12-19** — [[sources/01KJS0J2A8-2025-llm-year-in-review|2025 LLM Year in Review]]: The author coined the term 'vibe coding' in a tweet and was surprised by how widely it spread.
- **2025-12-04** — [[sources/01KJT62ZGZ-nex-n1-agentic-models-trained-via-a-unified-ecosystem-for-large-scale-environmen|Nex-N1: Agentic Models Trained via a Unified Ecosystem for Large-Scale Environment Construction]]: In NexAU, a sub-agent is exposed to its parent as simply a tool with a defined input schema, and the
- **2025-11-19** — [[sources/01KJVK5SZY-self-improving-ai-agents-architecting-llm-memory-with-ace-voyager-and-claude-ski|Self-Improving AI Agents: Architecting LLM Memory with ACE, Voyager, and Claude Skills [AIA Nov 7]]]: The ACE (Agentic Context Engineering) framework divides labor across three roles: a generator that p
- **2025-11-04** — [[sources/01KJTBFGVH-training-proactive-and-personalized-llm-agents|Training Proactive and Personalized LLM Agents]]: The proactivity reward adds +0.05 if all queries are low-effort, penalizes -0.1 per medium-effort qu
- **2025-10-17** — [[sources/01KJVDZXXQ-andrej-karpathy-were-summoning-ghosts-not-building-animals|Andrej Karpathy — “We’re summoning ghosts, not building animals”]]: Current AI agents lack continual learning: they cannot persistently retain new information told to t
- **2025-10-16** — [[sources/01KJS276S8-equipping-agents-for-the-real-world-with-agent-skills-anthropic-claude|Equipping agents for the real world with Agent Skills \ Anthropic | Claude]]: Asking Claude to self-reflect on what went wrong when using a skill is a recommended approach for it
- **2025-09-30** — [[sources/01KJTFFNZY-cwm-an-open-weights-llm-for-research-on-code-generation-with-world-models|CWM: An Open-Weights LLM for Research on Code Generation with World Models]]: CWM achieves 68.6% on LiveCodeBench-v5.
- **2025-09-11** — [[sources/01KJVJY5T8-context-engineering-for-agents-lance-martin-langchain|Context Engineering for Agents - Lance Martin, LangChain]]: Context engineering is defined as the challenge of feeding an LM just the right context for the next
- **2025-09-11** — [[sources/01KKT42HFY-kimi-k2-open-agentic-intelligence|KIMI K2: OPEN AGENTIC INTELLIGENCE]]: Breakthrough: Open-source model reaches near-frontier agentic performance: Kimi K2 ranks #1 op
- **2025-09-02** — [[sources/01KJVTHEDF-deal-velocity-not-billable-hours-how-crosby-uses-ai-to-redefine-legal-contractin|Deal Velocity, Not Billable Hours: How Crosby Uses AI to Redefine Legal Contracting]]: Crosby physically staggers lawyer and engineer desks alternately to maximize collaboration and feedb
- **2025-08-27** — [[sources/01KJSZ6JB0-roadmap-developer-tooling-for-software-30|Roadmap: Developer Tooling for Software 3.0]]: Significant work remains before widespread enterprise AI adoption is possible, with critical gaps ar
- **2025-08-19** — [[sources/01KJVK1H1A-long-live-context-engineering-with-jeff-huber-of-chroma|Long Live Context Engineering - with Jeff Huber of Chroma]]: Context engineering is the job of figuring out what should be in the context window at any given LLM
- **2025-08-08** — [[sources/01KJTMGSTS-glm-45-agentic-reasoning-and-coding-arc-foundation-models|GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models]]: GLM-4.5 achieves 89.87 on SafetyBench, competitive with Kimi K2 (90.48) and GPT-4.1 (89.71), with ro
- **2025-08-02** — [[sources/01KJVSCDAD-state-of-startups-and-ai-2025-sarah-guo-conviction|State of Startups and AI 2025 - Sarah Guo, Conviction]]: GPT-4 dropped from $30 per million tokens to $2 per million tokens in approximately 18 months.
- **2025-07-14** — [[sources/01KJSRWREB-kimi-k2-and-when-deepseek-moments-become-normal|Kimi K2 and when "DeepSeek Moments" become normal]]: OpenAI delayed its forthcoming open-weight model to run additional safety tests and review high-risk
- **2025-06-27** — [[sources/01KJTP7WMB-the-automated-llm-speedrunning-benchmark-reproducing-nanogpt-improvements|The Automated LLM Speedrunning Benchmark: Reproducing NanoGPT Improvements]]: The NanoGPT Speedrun community effort reduced GPT-2 training time from 45 minutes to below 3 minutes
- **2025-06-19** — [[sources/01KJVH03BZ-scaling-test-time-compute-to-multi-agent-civilizations-noam-brown-openai|Scaling Test Time Compute to Multi-Agent Civilizations — Noam Brown, OpenAI]]: Superhuman poker AIs have been built for no-limit Texas Hold'em
- **2025-06-19** — [[sources/01KJVGFHX6-andrej-karpathy-software-is-changing-again|Andrej Karpathy: Software Is Changing (Again)]]: Software 1.0 is traditional code written by humans for computers; Software 2.0 is neural network wei
- **2025-06-17** — [[sources/01KKT490MT-alphaevolve-a-coding-agent-for-scientific-and|AlphaEvolve: A coding agent for scientific and]]: Breakthrough: LLM-guided evolutionary coding agent deployed in production at Google, recoverin
- **2025-05-29** — [[sources/01KJSZPWHN-roadmap-ai-systems-of-action|Roadmap: AI systems of action]]: The two deepest moats for incumbent SoR vendors are high upfront implementation costs and housing cu
- **2025-05-29** — [[sources/01KJTRC2KS-darwin-godel-machine-open-ended-evolution-of-self-improving-agents|Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents]]: All DGM agent execution and self-modification processes are conducted within isolated sandboxed envi
- **2025-05-07** — [[sources/01KJVK34BD-claude-code-anthropics-cli-agent|Claude Code: Anthropic's CLI Agent]]: Claude Code is Claude running in the terminal with access to bash commands and all files in the curr
- **2025-04-24** — [[sources/01KJTXQNR0-paper2code-automating-code-generation-from-scientific-papers-in-machine-learning|Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning]]: PaperCoder's planning stage transforms unstructured paper text into four structured implementation a
- **2025-04-10** — [[sources/01KJVFZ54E-new-in-nature-google-agents-beat-human-doctors-make-scientific-discoveries-with-|New in Nature: Google Agents Beat Human Doctors, Make Scientific Discoveries – With Vivek and Anil]]: Co-scientist's top hypothesis for the mechanism of bacterial drug resistance exactly matched an expe
- **2025-04-10** — [[sources/01KJV0GSYV-the-ai-scientist-v2-workshop-level-automated-scientific-discovery-via-agentic-tr|The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search]]: AI Scientist-v2 lacks the detailed methodological rigor and in-depth analysis required for acceptanc
- **2025-03-28** — [[sources/01KJVFMTTF-the-agent-network-dharmesh-shah-agentai-cto-of-hubspot|The Agent Network — Dharmesh Shah, Agent.ai + CTO of HubSpot]]: Agent.ai has 1.3 million users, with 3,000 people having built agents and approximately 1,000 agents
- **2025-03-25** — [[sources/01KJVFH11E-inside-openais-new-agent-development-tools|Inside OpenAI's New Agent Development Tools]]: OpenAI released the Agents SDK to support multi-agent swarm architectures because developers were al
- **2025-03-08** — [[sources/01KJVBPHHT-towards-conversational-ai-for-disease-management|Towards Conversational AI for Disease Management]]: RxQA is a multiple-choice medication reasoning benchmark derived from two national drug formularies 
- **2025-02-25** — [[sources/01KJVNYSCT-no-priors-ep-103-with-vevo-therapeutics-and-the-arc-institute|No Priors Ep. 103 | With Vevo Therapeutics and the Arc Institute]]: Tahoe 100 contains 100 million single cell data points.
- **2025-02-25** — [[sources/01KJV3W9QT-swe-rl-advancing-llm-reasoning-via-reinforcement-learning-on-open-software-evolu|SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution]]: The base Llama-3.3-70B-Instruct model produces correctly formatted code edits only 12.2% of the time
- **2025-02-19** — [[sources/01KJVJJDA3-david-luan-deepseeks-significance-whats-next-for-agents-lessons-from-openai|David Luan: DeepSeek’s Significance, What’s Next for Agents & Lessons from OpenAI]]: Reducing the cost of intelligence does not reduce consumption of intelligence; cheaper intelligence 
- **2025-01-01** — [[sources/01KJVT1PHD-2024-year-in-review-the-big-scaling-debate-the-four-wars-of-ai-top-themes-and-th|2024 Year in Review: The Big Scaling Debate, the Four Wars of AI, Top Themes and the Rise of Agents]]: O1 (also known as Strawberry and QStar) was released in September 2024.
- **2024-12-25** — [[sources/01KJVFQM7C-best-of-2024-in-agents-from-1-on-swe-bench-full-prof-graham-neubig-of-openhandsa|Best of 2024 in Agents (from #1 on SWE-Bench Full, Prof. Graham Neubig of OpenHands/AllHands)]]: Open Hands provides agents with the ability to call arbitrary Python code rather than a fixed set of
- **2024-11-13** — [[sources/01KJT0E4FT-rip-to-rpa-the-rise-of-intelligent-automation-andreessen-horowitz|RIP to RPA: The Rise of Intelligent Automation | Andreessen Horowitz]]: UiPath was founded in 2005 and conducted its IPO in 2021
- **2024-10-09** — [[sources/01KJT0NENF-generative-ais-act-o1|Generative AI’s Act o1]]: The o1 paper establishes a new scaling law: the more inference-time compute given to the model, the 
- **2024-10-02** — [[sources/01KJVGWEGP-openais-noam-brown-ilge-akkaya-and-hunter-lightman-on-o1-and-teaching-llms-to-re|OpenAI's Noam Brown, Ilge Akkaya and Hunter Lightman on o1 and Teaching LLMs to Reason Better]]: O1 is OpenAI's first major foray into general inference-time compute and reasoning.
- **2024-08-12** — [[sources/01KJV8RNT6-the-ai-scientist-towards-fully-automated-open-ended-scientific-discovery|The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery]]: The AI Scientist can produce a full research paper at a cost of less than $15 per paper.
- **2024-06-27** — [[sources/01KJVSF4MB-10-people-ai-billion-dollar-company|10 People + AI = Billion Dollar Company?]]: SWE-bench is a dataset of GitHub issues taken from real programming problems, representative of real
