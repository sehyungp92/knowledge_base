---
type: source
title: 'Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents'
source_id: 01KJTRC2KSAF7MX3E03Z20FA3X
source_type: paper
authors:
- Jenny Zhang
- Shengran Hu
- Cong Lu
- Robert Lange
- Jeff Clune
published_at: '2025-05-29 00:00:00'
theme_ids:
- agent_evaluation
- agent_self_evolution
- agent_systems
- evaluation_and_benchmarks
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents

**Authors:** Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, Jeff Clune
**Published:** 2025-05-29 00:00:00
**Type:** paper

## Analysis

# Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents
2025-05-29 · paper · Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, Jeff Clune
https://arxiv.org/pdf/2505.22954

---

### Motivation & Prior Limitations
- Most AI systems are constrained by fixed, human-designed architectures that cannot autonomously rewrite their own source code, meaning each advancement in AI still depends heavily on human intervention to design better algorithms, prompts, and workflows.
  - Meta-learning approaches can automate algorithm discovery but are limited to first-order improvements and require humans to pre-define the search space, capping the ceiling of what can be discovered.
  - The theoretical Gödel Machine (Schmidhuber, 2007) proposed a provably self-improving AI, but requiring formal proofs that a modification is beneficial is practically impossible — the actual impact of any change (e.g., adding a code-search tool) depends heavily on model training and task context in ways that resist formal verification.
- Prior FM-based meta-learning systems such as ADAS (Hu et al., 2025) use a fixed, handcrafted meta-agent to modify downstream agents, meaning the meta-agent itself never improves and gains taper off as its fixed capabilities become the bottleneck.
- Concurrent work by Robeyns et al. (2025) has a single agent recursively modifying its own codebase, but without an open-ended exploration archive it greedily follows the best-performing path and risks stagnation in local optima.

---

### Proposed Approach
- The Darwin Gödel Machine (DGM) is a self-referential, self-improving system that replaces formal proofs of improvement with empirical validation: a coding agent iteratively modifies its own Python codebase, and each modification is tested on a coding benchmark to determine whether it is retained.
  - Unlike ADAS, there is no fixed meta-agent — the same agent that solves downstream coding tasks also performs self-modification, so improvements in coding ability directly translate into improved self-modification capability, enabling a self-accelerating loop.
  - Unlike greedy hill-climbing (Robeyns et al., 2025), the DGM maintains a growing archive of all generated agents (initialized from a single base agent) and selects parents for self-modification roughly proportional to performance score and the number of children with codebase-editing functionality, enabling open-ended exploration across many parallel paths.
- The open-ended exploration mechanism is explicitly inspired by Darwinian evolution and quality-diversity research: archived agents serve as stepping stones, including suboptimal ones, allowing the system to escape deceptive local optima and explore diverse implementation strategies for the same target functionality.
- Self-modification is operationalized as a coding task: a selected parent agent analyzes its own benchmark evaluation logs, proposes the next feature to implement, and then edits its own repository to produce a child agent; only children that compile and retain basic codebase-editing functionality are added to the archive.
- The current DGM focuses on improving agent design (tools, prompts, workflows) with frozen pretrained foundation models, explicitly deferring self-modification of training scripts or the foundation model weights themselves as future work.

---

### Results & Capabilities
- The DGM automatically improves coding performance from 20.0% to 50.0% on SWE-bench Verified and from 14.2% to 30.7% on the full Polyglot benchmark over 80 iterations, discovering improvements to both tools and FM-utilization workflows without any human guidance.
  - Specific tool improvements discovered include more granular file viewing (by line range) and more precise file editing (via string replacement instead of whole-file replacement), multiple patch generation attempts with FM-based ranking of solutions, and history-aware patch generation that considers prior attempts.
- Both self-improvement and open-ended exploration are necessary: the DGM outperforms a baseline without self-improvement (DGM w/o self-improve, which replicates ADAS and whose gains taper off quickly) and a baseline without open-ended exploration (DGM w/o open-ended exploration, which greedily follows the latest version and cannot recover from poorly-performing modifications).
- The DGM-discovered agents match or exceed handcrafted open-source baselines: the best SWE-bench agent is comparable to the checked open-source SoTA, and the best Polyglot agent substantially surpasses Aider — a representative coding agent developed and refined by human experts over more than a year.
- Improvements transfer across foundation models, benchmarks, and programming languages: the SWE-bench agent (discovered using Claude 3.5 Sonnet) achieves 59.0% with Claude 3.7 Sonnet and 33.0% with o3-mini (versus 19.0% and 23.0% for the base agent respectively); zero-shot cross-benchmark transfer shows the SWE-bench agent reaching 28.9% on Polyglot (baseline 14.2%) and vice versa, indicating genuine general skill acquisition rather than benchmark overfitting.
- The open-ended archive enables recovery from deceptive performance dips: at iterations 4 and 56 on SWE-bench the agent score temporarily fell below its parent, yet the archive preserved those branches and subsequent exploration along those paths eventually produced agents outperforming all predecessors.

---

### Implications
- The DGM demonstrates that the self-referential self-improvement loop — where gains on the evaluation task directly enhance the system's capacity to improve itself — is empirically achievable with current LLMs, moving the field from theoretical proposals (Gödel Machine) to working systems.
- By matching or exceeding human-engineered open-source SoTA agents automatically, the DGM hints that labor-intensive manual agent engineering (prompt tuning, workflow design, tool selection) could increasingly be automated, compressing the development cycle for

## Key Claims

1. The Darwin Gödel Machine (DGM) automatically improves its coding performance on SWE-bench from 20.0% to 50.0% over 80 iterations of self-modification.
2. The DGM improves coding performance on the Polyglot benchmark from 14.2% to 30.7% on the full benchmark.
3. Most current AI systems are constrained by fixed, human-designed architectures and cannot autonomously rewrite their own source code to self-improve.
4. Formally proving that self-modifications to an AI system are net beneficial is impossible in practice without restrictive assumptions.
5. The DGM uses empirical benchmark validation rather than formal proofs to determine if self-modifications are beneficial, analogous to biological natural selection.
6. The DGM maintains a growing archive of all generated agent variants, enabling open-ended exploration by branching from any previously discovered agent rather than only the most recent.
7. Self-improvement (the meta-agent updating itself) is essential for sustained performance gains; without it, improvements taper off quickly.
8. Open-ended exploration with an archive is essential for sustained performance gains; without it, a poorly performing self-modification makes subsequent improvements harder to achieve.
9. The DGM automatically discovered improvements to both tools (e.g., granular file viewing by lines, string-replacement editing) and workflows (e.g., multi-attempt solving with FM-based ranking of solut
10. The DGM-discovered agent's performance is comparable to that of the checked, open-source, human-designed state-of-the-art on SWE-bench.

## Capabilities

- AI coding agents can autonomously modify their own source code iteratively to improve their own capabilities, validated empirically via benchmark performance without formal proofs
- Open-ended evolutionary search over an archive of self-modified agents discovers diverse stepping stones that enable later breakthroughs not reachable by hill-climbing on the current best agent
- Self-discovered agent improvements (tools, workflows, context management) transfer across different foundation models, benchmarks, and programming languages without reoptimization
- Automated meta-learning can autonomously discover specific coding agent improvements — granular file viewing, string-replacement editing, multi-attempt patch generation with ranking, context summarisation — comparable to human-expert-engineered solutions

## Limitations

- DGM is fundamentally capability-bounded by its frozen foundation model — it can improve agent design (tools, prompts, workflows) but cannot retrain the underlying FM weights, blocking deeper recursive self-improvement
- The open-ended exploration process itself (archive maintenance, parent selection strategy) is fixed and cannot be self-modified, preventing true recursive meta-self-improvement
- A single DGM run takes approximately 2 weeks and incurs significant API costs, making iterative experimentation prohibitively expensive for most researchers and blocking rapid iteration
- Self-improvement is confined entirely to the coding domain; the system cannot improve itself in other AI application areas (computer vision, creative writing, robotics)
- DGM still falls short of closed-source state-of-the-art SWE-bench solutions built by teams of expert engineers, and it is unknown whether longer runs would close this gap
- Benchmark-based empirical validation is a limited proxy: if benchmarks do not capture safety and robustness, the self-improvement loop can amplify misalignment over successive generations
- Iterative self-modification produces increasingly complex and uninterpretable agent code, making human oversight progressively harder as successive generations accumulate changes
- Formal proofs that self-modifications are net beneficial are impossible in practice, leaving the system reliant on finite empirical heuristics that cannot anticipate all downstream effects
- Without open-ended exploration (hill-climbing only on most recent agent), a single bad mutation breaks the lineage — there is no recovery mechanism from deceptive local optima or destructive modifications
- Fixed meta-agent approaches to automated agent design hit a rapid performance plateau — gains taper off after early iterations without self-referential improvement of the meta-agent itself
- The assumption that coding benchmark performance reliably reflects self-improvement capability is unvalidated outside the coding domain and may not hold for general AI self-improvement
- SWE-bench likely being included in frontier FM training sets introduces contamination that may inflate base performance and confound self-improvement gain attribution
- Self-modifications optimised solely for benchmark performance can inadvertently introduce security vulnerabilities or misaligned behaviours not captured by the evaluation metric

## Bottlenecks

- Self-improving AI systems cannot yet improve their own foundation model weights — only the agent scaffolding around frozen FMs — blocking the next level of recursive self-improvement
- Automated agent self-improvement search requires prohibitive per-run compute (2-week wall-clock, large API costs), blocking rapid iteration and broad research access
- No benchmark fully captures safety, robustness, and alignment properties needed to safely validate self-modifications — benchmark proxies risk amplifying misalignment through the self-improvement loop

## Breakthroughs

- First practical self-referential self-improving AI system that replaces the Gödel Machine's impossible formal-proof requirement with empirical benchmark validation, achieving open-source state-of-the-art coding performance autonomously from 20% to 50% on SWE-bench

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/aider|Aider]]
- [[entities/constitutional-ai|Constitutional AI]]
