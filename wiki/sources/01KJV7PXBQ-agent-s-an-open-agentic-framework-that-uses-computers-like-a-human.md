---
type: source
title: 'Agent S: An Open Agentic Framework that Uses Computers Like a Human'
source_id: 01KJV7PXBQFTHEVGHDCGE868Q0
source_type: paper
authors:
- Saaket Agashe
- Jiuzhou Han
- Shuyu Gan
- Jiachen Yang
- Ang Li
- Xin Eric Wang
published_at: '2024-10-10 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- computer_use_and_gui_agents
- knowledge_and_memory
- multi_agent_coordination
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agent S: An Open Agentic Framework that Uses Computers Like a Human

Agent S introduces experience-augmented hierarchical planning for GUI agents, combining a Manager-Worker architecture with retrieval-based memory (web knowledge, narrative summaries, episodic traces) and a language-centric Agent-Computer Interface to nearly double the prior state-of-the-art on OSWorld — from 11.21% to 20.58% success rate — without any model fine-tuning, while systematically exposing the gap between benchmark progress and production-ready computer use.

**Authors:** Saaket Agashe, Jiuzhou Han, Shuyu Gan, Jiachen Yang, Ang Li, Xin Eric Wang
**Published:** 2024-10-10
**Type:** paper

## Expert Analysis

### Motivation & Prior Limitations

GUI agents based on MLLMs face three structural problems that flat, single-level architectures cannot overcome:

**Knowledge staleness.** Desktop applications and websites change constantly; agents without live external knowledge are locked to their pre-training distribution and fail on updated interfaces.

**Planning depth.** Complex desktop tasks require long-horizon, multi-step planning with interdependent actions. The best prior result on OSWorld (GPT-4o with accessibility tree + screenshot) achieved only 11.21%, directly attributable to the absence of structured subtask decomposition.

**Grounding.** MLLMs lack an internal coordinate system and cannot reliably pinpoint specific UI elements from visual input. Prior Set-of-Mark approaches augmented images with accessibility tree data, but grounding errors remained the dominant failure mode.

These problems compound: an agent that plans well but grounds poorly fails; one that grounds well but has no memory of prior experience fails on novel applications.

---

### Proposed Architecture

**Hierarchical Manager-Worker planning.** The Manager decomposes each task into a topologically sorted subtask queue. Workers execute subtasks one at a time, drawing on a separate memory store keyed by (task, subtask, context) tuples. A Trajectory Reflector module monitors Worker execution and issues corrective advice when repetitive or diverging behaviour is detected.

The Manager fuses two retrieval sources via an Experience Context Fusion submodule:
- *Online Web Knowledge* — retrieved via Perplexica search at planning time, supplying up-to-date application-specific domain knowledge.
- *Narrative Memory* — abstractive, action-free task summaries from prior experience, encoding high-level strategy without raw trajectory noise.

**Self-supervised continual memory.** Memory is bootstrapped by running the agent on synthetically generated tasks during an offline exploration phase, then updated continuously during inference. A Self-Evaluator module assesses completed trajectories and writes summarised strategy descriptions rather than raw action logs. Ablation confirms this is strictly superior to storing full trajectories (26.15% vs. 18.46% on testsub). Crucially, self-supervised exploration contributes more than continual update: removing exploration drops performance to 15.38%, while removing only continual update drops to 23.18%.

**Language-centric Agent-Computer Interface (ACI).** Rather than augmenting screenshots with accessibility tree overlays (prior approach), Agent S reverses the direction: the accessibility tree is augmented with OCR-extracted text blocks matched via IOU, producing uniquely tagged elements suitable for language-addressed grounding. A bounded discrete action space (`click(element_id)`, `type()`, `drag_and_drop()`, etc.) enforces one action per timestep, providing immediate environmental feedback and preventing multi-action safety failures. Screenshots remain in the input for detecting salient visual state — popups, button state changes, action outcome verification — where the tree is insufficient.

---

### Results

| Setting | Overall | OS | Office | Daily | Professional | Workflow |
|---|---|---|---|---|---|---|
| GPT-4o baseline | 11.21% | — | — | — | — | — |
| Agent S (GPT-4o) | **20.58%** | 45.83% | 13.00% | 27.06% | 36.73% | 10.53% |
| Agent S (Claude-3.5-Sonnet) | 20.48% | — | — | 30.46% | 32.65% | — |

On WindowsAgentArena, Agent S (GPT-4o) improves from 13.3% (NAVI baseline) to **18.2%** without any explicit Windows adaptation — demonstrating cross-OS transfer. Gains concentrate in "Windows System" (+16.6pp) and "Coding" (+20.1pp); "Web Browser" and "Office" show no improvement or regression.

Ablation on the 65-task testsub isolates component contributions:

| Configuration | testsub |
|---|---|
| Full Agent S | 26.15% |
| ACI-only | 12.31% |
| w/o Web Knowledge | 16.80% |
| w/o Hierarchical Planning | 20.00% |
| w/o Self-supervised Exploration | 15.38% |
| w/o Continual Memory Update | 23.18% |
| Raw trajectories (no Self-Evaluator) | 18.46% |

Web knowledge removal is the largest single-component drop (9.35pp), confirming that live domain knowledge — not learned memory alone — is the primary driver of gains on knowledge-intensive tasks.

---

## Key Claims

1. Agent S outperforms the OSWorld baseline by 9.37% absolute (83.6% relative improvement), establishing a new SOTA at time of publication.
2. Current MLLMs cannot directly ground and pinpoint specific elements in images — they lack an internal coordinate system — making grounding a fundamental architectural limitation, not merely an implementation gap.
3. Execution errors occur in **79.59%** of failed tasks; grounding errors in **53.06%** — these are the dominant failure modes even for the best configuration.
4. Removing web knowledge is the single largest performance drop in ablation, indicating live retrieval compensates for knowledge staleness more than any memory component.
5. Self-supervised exploration is more impactful than continual memory update; the bootstrapping quality of initial memory is critical.
6. Summarised trajectory experiences outperform full raw trajectories for planning retrieval.
7. The ACI alone (without hierarchical planning or retrieval) achieves only 12.31% — the interface improvement is necessary but insufficient without the planning and memory layers.
8. Agent efficiency (steps per task, wall-clock time) is completely unmeasured across all existing GUI agent work, leaving production suitability unassessed.

---

## Capabilities

- **Experience-augmented hierarchical planning** achieves 20.58% on OSWorld — nearly doubling prior SOTA — through coordinated retrieval of web knowledge, narrative memory, and episodic traces. *(maturity: demo)*
- **Self-supervised continual improvement** bootstraps memory on synthetic tasks and refines during inference without human feedback or ground truth labels. *(maturity: demo)*
- **Language-based ACI with OCR-augmented accessibility tree** enables more reliable UI element grounding by reversing the prior image-augmentation direction and assigning unique element IDs. *(maturity: demo)*
- **Cross-OS generalisation** without explicit adaptation — Ubuntu-trained agent outperforms native Windows baseline on WindowsAgentArena. *(maturity: demo)*
- **Hierarchical subtask decomposition with trajectory reflection** supports long-horizon multi-step desktop workflows more reliably than flat planning. *(maturity: demo)*

---

## Limitations & Open Questions

### Blocking

- **Absolute performance remains low.** Even with full Agent S, roughly 80% of real-world desktop tasks fail. Office tasks reach only 13%; multi-app Workflow tasks only 10.53% — the lowest category. The benchmark improvement is real but the gap to human-level usability is large.
- **Multi-app workflow coordination is a performance cliff.** Tasks requiring state synchronisation across multiple applications remain nearly intractable, suggesting the architecture needs cross-application context mechanisms not present in the current design.

### Significant

- **Grounding is a fundamental bottleneck.** MLLM inability to regress coordinates is architectural, not incidental. The ACI's tree-based tagging is a workaround, not a solution — it fails when accessibility trees are incomplete or malformed (common in native desktop apps). Grounding errors appear in over half of all failures.
- **Execution reliability.** Agents cannot reliably self-correct mid-execution. Repetitive actions, goal drift, and premature action combination appear in 79.59% of failures. Trajectory Reflector provides advice but cannot enforce corrections.
- **Planning errors in 34.69% of failures.** The Manager itself produces unsuitable subtask sequences, misleading context, or misaligned ordering — hierarchical planning is necessary but not yet reliable.
- **Cold-start bootstrapping overhead.** The self-supervised exploration phase is computationally expensive and critically important. Deploying to a new application domain requires a full exploration run, blocking rapid adaptation and limiting democratisation.
- **Self-evaluator noise.** Success/failure labelling without ground truth introduces silently compounding errors into memory: misclassified experiences degrade future retrieval quality in ways that are hard to detect or correct.
- **Unmeasured agent efficiency.** Steps per task and wall-clock time are acknowledged but not reported. Real-world deployments for latency-sensitive workflows cannot be evaluated against existing benchmarks.
- **Frontier model dependency.** All validation uses GPT-4o or Claude-3.5-Sonnet. Applicability to smaller open-source MLLMs is explicitly unresolved and left to future work.
- **Stateless discrete-time operation.** Agents respond in slow, discrete intervals and are stateless between steps — a fundamental constraint making them unsuitable for reactive or latency-sensitive tasks regardless of benchmark success.

---

## Landscape Context

### Bottlenecks Identified

**GUI agent inference efficiency** is completely unmeasured across the research literature. Optimising only for success rate while ignoring latency creates a Pareto-blind evaluation regime that cannot support production deployment decisions. Horizon: 1–2 years.

**Cold-start memory bootstrapping** requires extensive synthetic exploration per application domain — high initialisation overhead that blocks rapid domain adaptation and enterprise deployment at scale. Horizon: 1–2 years.

### Breakthrough

Experience-augmented hierarchical planning with retrieval-based memory achieves an **83.6% relative improvement** in GUI agent task completion on OSWorld without any model fine-tuning — establishing that architecture and retrieval can substitute for parameter updates in this domain, at least at current capability levels.

---

## Themes

- [[themes/agent_memory_systems|Agent Memory Systems]]
- [[themes/agent_systems|Agent Systems]]
- [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]]
- [[themes/knowledge_and_memory|Knowledge & Memory]]
- [[themes/multi_agent_coordination|Multi-Agent Coordination]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/vision_language_models|Vision-Language Models]]

## Key Concepts

- [[entities/set-of-mark-prompting|Set-of-Mark Prompting]]
