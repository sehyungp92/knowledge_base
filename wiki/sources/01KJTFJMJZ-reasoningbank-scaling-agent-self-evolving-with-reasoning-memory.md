---
type: source
title: 'ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory'
source_id: 01KJTFJMJZ6T6SH5T8ZHCCY81H
source_type: paper
authors:
- Siru Ouyang
- Jun Yan
- I-Hung Hsu
- Yanfei Chen
- Ke Jiang
- Zifeng Wang
- Rujun Han
- Long T. Le
- Samira Daruki
- Xiangru Tang
- Vishy Tirumalashetty
- George Lee
- Mahsan Rofouei
- Hangfei Lin
- Jiawei Han
- Chen-Yu Lee
- Tomas Pfister
published_at: '2025-09-29 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory

**Authors:** Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki, Xiangru Tang, Vishy Tirumalashetty, George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, Tomas Pfister
**Published:** 2025-09-29 00:00:00
**Type:** paper

## Analysis

# ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory
2025-09-29 · paper · Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang et al. (17 total)
https://arxiv.org/pdf/2509.25140

---

### Motivation & Prior Limitations
LLM agents deployed in persistent, long-running roles encounter continuous streams of tasks but fail to learn from accumulated interaction history, forcing them to repeat past errors and discard valuable cross-task insights.
- Existing memory approaches store raw trajectories or only successful routines (workflows/procedures), leaving two fundamental gaps: inability to distill transferable reasoning patterns, and near-complete neglect of failure signal as a learning source.
  - Trajectory-based memory (e.g., Synapse) retains verbose, noisy interaction logs that are difficult to generalize from; workflow-based memory (e.g., AWM) mines only success paths, which degrades on cross-domain transfer settings where AWM actually hurts performance relative to no memory.
- Test-time scaling has been applied to multi-turn agentic settings, but no prior work considers the role of agent memory in scaling — meaning additional compute generates more trajectories without extracting structured lessons, limiting the return on inference investment.
- The test-time learning paradigm imposes a hard constraint: no ground-truth labels are available at inference time, so any self-improvement mechanism must rely entirely on self-verification and past trajectories.

---

### Proposed Approach
ReasoningBank is a memory framework that distills generalizable reasoning strategies from both successful and failed agent trajectories into structured, human-interpretable memory items, retrieved and updated continuously at test time.
- Each memory item has three fields — a title (concise identifier), a description (one-sentence summary), and content (distilled reasoning steps, decision rationales, operational insights) — abstracting away low-level execution details while preserving transferable patterns.
  - This differs from trajectory memory (raw logs) and workflow memory (action templates) by operating at the level of strategic reasoning principles rather than execution sequences or success-only procedures.
  - Outcome labels are produced by an LLM-as-a-judge without ground-truth access; successful trajectories contribute validated strategies while failed ones contribute counterfactual signals and pitfalls used as guardrails.
- The integration cycle is a closed loop: (i) embedding-based retrieval of top-k relevant memory items injected into the agent's system prompt before acting, (ii) post-task memory extraction from the completed trajectory, and (iii) additive consolidation back into the bank — deliberately kept simple to isolate the contribution of the memory content itself.
- Memory-aware Test-Time Scaling (MaTTS) extends ReasoningBank by scaling experience depth rather than breadth: for each task, additional compute generates multiple trajectories (parallel) or iterative self-refinements (sequential), then self-contrast or self-refinement intermediate notes are used as contrastive signals to synthesize higher-quality memory items.
  - Parallel MaTTS uses self-contrast across k trajectories to identify consistent patterns and filter spurious solutions; sequential MaTTS uses self-refinement steps and their intermediate reasoning notes as additional memory signal, not just the final output.
  - The synergy is bidirectional: better memory steers scaled exploration toward promising paths, and diverse rollouts from scaling produce richer contrastive signals for memory curation — a positive feedback loop framed as a new scaling dimension distinct from compute scaling alone.

---

### Results & Capabilities
ReasoningBank consistently outperforms memory-free agents and both Synapse (trajectory memory) and AWM (workflow memory) baselines across web browsing and software engineering benchmarks with three different backbone LLMs (Gemini-2.5-flash, Gemini-2.5-pro, Claude-3.7-sonnet).
- On WebArena (684 tasks across Shopping, Admin, GitLab, Reddit, Multi domains), ReasoningBank improves overall success rate by +8.3, +7.2, and +4.6 percentage points over no-memory baselines for the three backbones respectively, while simultaneously reducing average interaction steps by up to 1.6 steps versus other memory baselines.
  - The Multi-domain subset, which requires cross-website memory transfer, yields +4.6 SR gain averaged over the strongest baseline; AWM fails entirely in this setting, dropping below no-memory performance.
- On SWE-Bench-Verified, ReasoningBank achieves 38.8% resolve rate with Gemini-2.5-flash (+4.6 over no-memory) and 57.4% with Gemini-2.5-pro (+3.4), saving 2.8 and 1.3 interaction steps respectively.
- MaTTS with parallel scaling (k=5) on WebArena-Shopping raises success rate from 49.7 to 55.1; sequential scaling reaches 54.5, representing a 34.2% relative improvement cited in the paper relative to weaker baselines.
  - Scaling without memory (MaTTS w/o memory) fluctuates between 39.0 and 42.2 with parallel scaling — gains are smaller and inconsistent — demonstrating that compute scaling alone is insufficient and requires high-quality memory to be effective.
  - Pass@1 results (measuring average trajectory quality after memory curation) show that scaling actually degrades performance for weaker memories: Synapse drops from 40.6 to 40.1 and AWM drops from 44.4 to 41.2, while ReasoningBank is the only method that improves Pass@1 under scaling (49.7 → 50.8), confirming the asymmetric synergy.
- Efficiency analysis separating successful from failed instances shows that step reductions are most pronounced on successful trajectories — up to 2.1 fewer steps (26.9% relative reduction on Shopping) — indicating that ReasoningBank shortens the path to correct solutions rather than merely truncating failed attempts.
- Memory items in ReasoningBank exhibit emergent complexity over time, evolving fr

## Key Claims

1. LLM agents deployed in persistent roles fail to learn from accumulated interaction history, forcing them to repeat past errors and discard valuable insights.
2. Existing agent memory approaches are limited to storing raw trajectories or successful task routines and cannot distill higher-level, transferable reasoning patterns.
3. ReasoningBank distills generalizable reasoning strategies from both successful and failed agent experiences without requiring ground-truth labels.
4. ReasoningBank uses a three-step closed-loop process: memory retrieval, memory construction, and memory consolidation.
5. ReasoningBank uses embedding-based similarity search to retrieve the top-k relevant memory items for a given query context.
6. An LLM-as-a-judge approach is used to label trajectory outcomes as success or failure without access to ground-truth labels during test time.
7. Memory items in ReasoningBank are structured as three components: a title (concise identifier), a description (one-sentence summary), and content (distilled reasoning steps and insights).
8. MaTTS introduces a synergy between memory quality and test-time scaling: better memory steers exploration toward more promising paths, and richer exploration forges stronger memories.
9. MaTTS parallel scaling uses self-contrast across multiple trajectories to identify consistent reasoning patterns and filter spurious solutions for more reliable memory curation.
10. MaTTS sequential scaling applies self-refinement iteratively within a single trajectory and uses intermediate refinement notes as additional memory signals.

## Capabilities

- LLM agents can distill generalizable reasoning strategies from both successful and failed past experiences without ground-truth labels, using LLM-as-a-judge self-evaluation — achieving up to 34.2% relative improvement and 16% fewer interaction steps on web browsing and software engineering benchmark
- Memory and test-time compute scaling form a synergistic positive feedback loop: higher-quality memory steers test-time exploration toward more promising trajectories, while diverse exploration generates richer contrastive signals for better memory curation — parallel TTS SR grows from 49.7% to 55.1%
- Agent memory items exhibit emergent strategy evolution over time — progressively advancing from procedural execution rules to adaptive self-reflections, to systematic checks, to compositional multi-step reasoning strategies, resembling RL learning dynamics without any weight updates
- Contrastive signals from multiple parallel trajectories on the same task can be leveraged via self-contrast to curate more reliable, generalizable agent memory — comparing across diverse rollouts filters spurious solutions and reinforces consistent reasoning patterns
- Intermediate reasoning notes generated during sequential self-refinement provide memory signals beyond the final answer — capturing reasoning attempts, mid-course corrections, and partial insights that may not appear in the final solution trajectory

## Limitations

- LLM agents deployed in persistent roles cannot learn from accumulated interaction history by default — each task is approached in isolation, causing agents to repeatedly rediscover known strategies and repeat past errors across a continuous stream of tasks
- Raw trajectory storage is too noisy and lengthy to serve as effective reusable memory — retrieving full interaction histories creates context pollution and poor signal-to-noise ratio when injected into future task contexts
- Test-time scaling without memory yields inconsistent and diminishing returns for multi-turn interactive agents — vanilla TTS sequential scaling provides little or no benefit as k increases, and parallel scaling fluctuates unpredictably between 39.0% and 42.2% SR
- Sequential self-refinement scaling saturates rapidly — once an agent either succeeds or fails decisively, further refinement iterations add minimal insight, and performance improvement plateaus well before parallel scaling does at the same k
- Memory mechanisms relying solely on successful trajectories are actively harmed by test-time scaling — Synapse drops from 40.6 to 40.1 Pass@1 and AWM drops from 44.4 to 41.2 when more diverse rollouts are added, as mixed-outcome trajectories introduce noise their architectures cannot process
- Self-evolving agent systems without ground truth are bounded by self-judging accuracy — if LLM-as-a-judge incorrectly labels trajectory outcomes, the memory system learns from wrong signals and may reinforce failure modes as strategies
- Cross-domain and multi-site web agent performance remains extremely low despite memory augmentation — Mind2Web cross-domain SR reaches only 1.6% with ReasoningBank (vs 1.0% baseline), and WebArena Multi-subset only 13.8%, exposing a hard generalization ceiling for externally-memorized strategies
- Memory efficiency gains are substantially asymmetric: ReasoningBank reduces steps by up to 2.1 on successful tasks but only 0.2–1.4 on failed ones, meaning failure episodes remain nearly as expensive to attempt as before memory augmentation
- MaTTS scaling experiments are confined to a single benchmark subset (WebArena-Shopping) — the scaling curves, optimal k values, and the parallel-vs-sequential crossover point may not generalize to domains with longer horizons, sparser rewards, or more diverse task structures such as SWE-Bench or cro
- Deliberate simplicity in memory retrieval and consolidation creates an acknowledged performance ceiling — simple addition-based consolidation without deduplication, pruning, or prioritization will degrade as the memory bank grows, a problem not studied in the paper
- Success-only workflow memory (AWM) fails to generalize to multi-site transfer tasks and is degraded — not merely unchanged — when failure trajectories are added, indicating existing procedural workflow designs are incompatible with contrastive learning signal

## Bottlenecks

- Self-judging accuracy is the hard ceiling for unsupervised agent self-evolution — without reliable outcome labeling from an external oracle, the quality of distilled memory is fundamentally bounded by how accurately an LLM can evaluate its own trajectory success or failure in ambiguous, open-ended d
- Memory quality is a prerequisite bottleneck for effective test-time scaling in interactive agents — weaker memory mechanisms are actively harmed by additional compute, making memory architecture a gating requirement that must be solved before TTS can be responsibly deployed in agentic settings
- Cross-domain and multi-site agent generalization remains a fundamental open bottleneck — even with memory-augmented agents achieving competitive per-domain performance, absolute cross-domain success rates below 2% (Mind2Web) indicate that strategy transfer across structurally diverse environments is

## Breakthroughs

- Memory-driven experience scaling is established as a new independent AI scaling dimension — an agent's accumulated experience, properly distilled, provides performance gains orthogonal to model size and test-time compute, with memory and TTS forming a measurable virtuous cycle rather than competing 
- Failure trajectory distillation reverses the prior consensus that only successful experiences are valuable for agent learning — incorporating failures yields a 3.2-point SR lift over success-only ReasoningBank, while success-only architectures (Synapse, AWM) either gain trivially or actively degrade

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/agent-workflow-memory|Agent Workflow Memory]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/mind2web|Mind2Web]]
- [[entities/react|ReAct]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/webarena|WebArena]]
