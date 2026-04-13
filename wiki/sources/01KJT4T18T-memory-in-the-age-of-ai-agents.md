---
type: source
title: Memory in the Age of AI Agents
source_id: 01KJT4T18TQM48KKNN118XKXQH
source_type: paper
authors:
- Yuyang Hu
- Shichun Liu
- Yanwei Yue
- Guibin Zhang
- Boyang Liu
- Fangyi Zhu
- Jiahang Lin
- Honglin Guo
- Shihan Dou
- Zhiheng Xi
- Senjie Jin
- Jiejun Tan
- Yanbin Yin
- Jiongnan Liu
- Zeyu Zhang
- Zhongxiang Sun
- Yutao Zhu
- Hao Sun
- Boci Peng
- Zhenrong Cheng
- Xuanbo Fan
- Jiaxin Guo
- Xinlei Yu
- Zhenhong Zhou
- Zewen Hu
- Jiahao Huo
- Junhao Wang
- Yuwei Niu
- Yu Wang
- Zhenfei Yin
- Xiaobin Hu
- Yue Liao
- Qiankun Li
- Kun Wang
- Wangchunshu Zhou
- Yixin Liu
- Dawei Cheng
- Qi Zhang
- Tao Gui
- Shirui Pan
- Yan Zhang
- Philip Torr
- Zhicheng Dou
- Ji-Rong Wen
- Xuanjing Huang
- Yu-Gang Jiang
- Shuicheng Yan
published_at: '2025-12-15 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- context_engineering
- knowledge_and_memory
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Memory in the Age of AI Agents

This survey establishes a unified conceptual foundation for the fragmented field of agent memory research, proposing a three-axis taxonomy (Forms, Functions, Dynamics) that supersedes the inadequate long-term/short-term dichotomy. Beyond classification, it maps the trajectory from hand-crafted heuristic pipelines toward fully learnable, RL-driven memory architectures, catalogues over 300 representative works and 25+ benchmarks, and articulates a set of blocking open problems — from the stability-plasticity dilemma to shared multi-agent memory coordination — that collectively define the frontier of agentic AI capability.

**Authors:** Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu et al. (47 total)
**Published:** 2025-12-15
**Type:** Survey paper
**Source:** https://arxiv.org/pdf/2512.13564

---

## Why This Survey Matters

The agent memory field had grown explosively without conceptual coherence — papers claiming to study "agent memory" differed drastically in implementation, objectives, and evaluation, while loose terminology (declarative, episodic, semantic, parametric) obscured rather than clarified. The survey's core contribution is not a new system but a shared language and a structural map that lets the field see itself clearly for the first time.

A crucial boundary-drawing exercise distinguishes agent memory from three adjacent constructs:

- **LLM memory** — KV-cache management, architectural recurrence (Mamba, RWKV), context-window design: these are *intrinsic architectural modifications* excluded from agent memory scope
- **RAG** — external, task-specific knowledge retrieval without cross-session persistence or self-evolution
- **Context engineering** — inference-time resource optimisation within a fixed window, not long-horizon knowledge accumulation

Agent memory is what survives between tasks, evolves from experience, and enables the transformation of a stateless LLM into an agent with a continuous history. The survey's central claim: **memory is the primitive that makes agents agents**.

---

## The Three-Axis Taxonomy

### Forms: What Carries Memory

**Token-level memory** (dominant in practice) stores explicit discrete units, subdivided by topology:
- *Flat (1D)* — independent memory entries without relational structure; coherence depends entirely on retrieval quality; redundancy accumulates as memory grows
- *Planar (2D)* — graph or tree structures encoding relational dependencies; enables multi-hop reasoning but imposes prohibitive construction and search costs for practical deployment
- *Hierarchical (3D)* — pyramid or multi-layer graph structures supporting vertical abstraction and cross-layer queries; optimal layout design remains unsolved

**Parametric memory** encodes knowledge directly into model weights via:
- *Internal fine-tuning* — most suitable for role-playing and stable domain knowledge, but requires costly retraining and is prone to catastrophic forgetting
- *External adapter/LoRA modules* — modular knowledge injection without modifying base weights; ELDER advances this with adaptive routing across multiple LoRA modules; integration effectiveness depends on unresolved alignment between external adapter parameters and base model representations

**Latent memory** carries information implicitly in KV caches, hidden states, or continuous embeddings:
- High compression ratios; suitable for multimodal, on-device, or privacy-sensitive settings
- Fundamentally opaque — latent memory vectors cannot be read, debugged, or manually verified; structurally unsuitable for high-stakes domains requiring transparency
- Errors and drift accumulate across multiple read-write cycles

### Functions: Why Agents Need Memory

**Factual memory** handles user- and environment-facing declarative knowledge — maintaining consistency, coherence, and adaptability across sessions. This is the most mature category, supported by nearly all production frameworks.

**Experiential memory** encodes procedural knowledge at three abstraction levels:
- *Case-based* — raw trajectory replay; high informational fidelity and verifiable imitation evidence, but retrieval efficiency and context window consumption scale poorly
- *Strategy-based* — editable, auditable, composable high-level workflow guidelines; reduces dependence on lengthy trajectory replay; AWM demonstrates reusable workflow induction on Mind2Web and WebArena, improving success rates while reducing steps. Key distinction: strategies are structural guidelines, not executable actions — necessitating the third level
- *Skill-based* — executable functions, APIs, MCP libraries; the execution substrate of modern agents. The primary bottleneck has shifted from tool invocation to **tool retrieval**: exponential API library growth means standard IR methods fail to capture functional tool semantics

**Working memory** manages the active within-episode context:
- *Input condensation* — hard (LLMLingua: token perplexity-based selection, risks severing syntactic dependencies) vs. soft (Gist, ICAE, AutoCompressors: latent compression, requires additional training, obscures fine-grained details)
- *State consolidation* — semantic summarization; serial update nature causes progressive information forgetting; compression introduces irreducible resolution loss
- *Hierarchical folding* — decomposes trajectories by subgoals, maintaining fine-grained traces only while a subtask is active, folding completed sub-trajectories into concise summaries; Context-Folding and AgentFold make this a learnable policy via RL
- *Cognitive planning* — structured plan and scene graph substrates (SayPlan with 3D scene graphs) as readable/writable working memory for embodied agents

Critically: **current LLMs do not exhibit human-like working memory characteristics**. The standard context window is a passive, read-only buffer with no explicit mechanisms to select, sustain, or transform its contents dynamically.

### Dynamics: How Memory Operates

**Formation** encompasses: semantic summarization, knowledge distillation, structured construction (KG extraction), latent encoding, and parametric internalization. Each carries distinct trade-offs between fidelity, cost, and deployability.

**Evolution** covers three operations:
- *Consolidation* — merging new information with existing memory; risks information smoothing where outlier events are lost
- *Updating* — conflict resolution for contradictory information; the stability-plasticity dilemma is theoretically unresolved: no principled mechanism distinguishes genuine knowledge updates from noise
- *Forgetting* — LRU/LFU/time-decay heuristics systematically eliminate long-tail knowledge; LLM-driven importance assessment (TiM, MemTool) enables "conscious forgetting" based on task relevance and semantic cues, but remains research-stage

**Retrieval** is decomposed into:
- *Timing and intent* — autonomous retrieval triggering via fast-slow thinking (ComoRAG, PRIME): agents self-evaluate initial response adequacy before triggering deeper retrieval; intent-driven systems (AgentRR) fail in open-ended settings where feedback is sparse
- *Query construction* — LLM-driven decomposition and rewriting substantially improve retrieval quality; query construction quality has been systematically underweighted relative to architecture design
- *Retrieval strategies* — lexical (BM25: fails on semantic variation), dense semantic (semantic drift, forced top-K introduce noise), graph-based (multi-hop reasoning, long-range dependencies), hybrid, temporal (Zep, MemoTime with explicit time constraints), hierarchical coarse-to-fine (H-MEM)
- *Post-retrieval* — re-ranking, RL-optimized score aggregation (learn-to-memorize: learns optimal weights over recency, importance, relevance without hyperparameter tuning), aggregation

---

## Trajectory: From Heuristics to RL-Driven Memory

The survey maps a clear developmental arc:

| Stage | Representative Systems | Characteristic |
|-------|----------------------|----------------|
| RL-free heuristic | MemGPT, Mem0 | Rule-based pipelines, manual engineering |
| RL-assisted components | RMM (retrieval reranking), Mem-α (update policy), MemAgent/MEM1 (working memory) | RL optimizes individual memory operations |
| Projected fully RL-driven | (future work) | Memory architectures learned end-to-end |

Key breakthroughs driving this trajectory:

**RL-trained working memory** (MEM1 via PPO, MemAgent via GRPO): LLMs trained to internalize multi-turn history compression as first-class capabilities rather than relying on external pipelines. This is the first demonstrated case of LLMs genuinely learning *when and how* to manage their own context.

**Mem-α**: formulates memory updating as a policy-learning problem, enabling meta-learning of update decisions (when, how, whether to update) — achieving dynamic stability-freshness trade-offs without hand-engineered rules.

**Darwin Gödel Machine**: safe empirically-validated self-rewriting of agent executable code, producing self-referential and progressively expanding skill sets. This breaks the assumption that an agent's capabilities are fixed at deployment — the agent becomes its own software engineer.

**Evolutionary case-to-skill compilation** (G-Memory, Memp): automatic compilation of frequently successful trajectories into executable skills, autonomously managing the case→strategy→skill transition without human supervision.

**MemEvolve**: joint meta-evolution of agent knowledge *and the memory architecture itself* — the memory management framework becomes learnable and adaptive, not just its contents.

**Memory-augmented test-time scaling** (2025 emergence): distilling reusable tools and strategies from accumulated experience links persistent memory accumulation to inference-time compute scaling — a convergence of two previously distinct research directions.

---

## Open Problems and Blocking Limitations

The survey is unusually candid about what remains unsolved. Limitations are not peripheral — they define the research agenda.

### Blocking Constraints

**LLM statelessness** is the root constraint: context windows alone are insufficient for long-horizon persistent intelligent behaviour. Every other memory problem is downstream of this fundamental architectural gap. [[themes/context_engineering|Context Engineering]] approaches address only the inference-time symptom.

**The stability-plasticity dilemma** is theoretically unresolved. No principled mechanism distinguishes genuine knowledge updates from noise. Online updates that adapt rapidly overwrite stable long-term knowledge; conservative updates accumulate stale information. This blocks reliable long-term autonomous operation.

**Catastrophic forgetting** in parametric internalization prevents continuous online learning. Every new memory injection risks degrading existing knowledge — making parametric memory unsuitable for agents that must accumulate experience over time.

**Silent hallucination from retrieval miscalibration**: agents that overestimate parametric knowledge and skip retrieval produce hallucinated outputs with no error signal. This is a systemic failure mode in any autonomous retrieval-augmented system.

**Trustworthy memory** does not exist as an engineering artifact. Memory systems have no established defences against poisoning attacks, no privacy preservation mechanisms, no version control, no auditability. The survey characterises this as a foundational requirement for any production deployment — yet no paper in the surveyed corpus addresses it.

### Structural Gaps

**Shared multi-agent memory** is architecturally unsolved. Current multi-agent systems operate with isolated memories; no mechanism handles consistency, conflict resolution, access control, or privacy across agents sharing a common substrate. This blocks collaborative agent collectives. See [[themes/agent_systems|Agent Systems]].

**No principled memory architecture selection framework**: practitioners choose between token-level, parametric, and latent memory — and among subtypes — based entirely on intuition and empirical trial. No automated framework exists.

**Flat memory's compositional ceiling**: flat (1D) architectures lack explicit relational organisation; as memory grows, redundancy accumulates and retrieval degrades. But the alternative — graph and hierarchical memory — imposes prohibitive construction and search costs that block practical deployment.

**Generative retrieval scalability wall**: generative retrieval (superior in generation-retrieval integration) requires full retraining when the corpus evolves, making it architecturally incompatible with dynamic agent memory. See [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]].

**Offline consolidation gap**: all current agent memory systems operate exclusively online. No mechanism exists to decouple from live interaction and perform offline memory reorganisation, schema distillation, or active forgetting — blocking the resolution of the stability-plasticity dilemma.

**Multimodal memory immaturity**: production systems are predominantly text-only. Multimodal memory integrating vision, audio, spatial, and temporal data remains confined to specialised research prototypes (KARMA's two-tier spatial system) with no generalisation path.

**Benchmark fragmentation**: incompatible evaluation protocols prevent systematic comparison. The survey compiles 25+ benchmarks (LoCoMo, LongMemEval, MemBench with 53k samples, MPR with 108k samples) but notes that most operate in simulated environments with controlled ground-truth — real-world generalisation under privacy constraints and adversarial inputs is unmeasured.

---

## Ecosystem Snapshot (2025)

**Production-adjacent frameworks**: MemGPT, Mem0, MemOS, Zep, LangMem, Cognee, and ~20 others. Most support factual memory via vector/graph stores. Zep advances the ecosystem with a three-layer temporal graph architecture (episodic subgraph, time-bounded semantic entity subgraph, community-level cluster subgraph).

**Convergence signal**: the Model Context Protocol (MCP) provides an open standard unifying how agents discover and use tools and data. Broad platform adoption indicates convergence toward a common interface layer for skill-based memory — the growing MCP ecosystem effectively externalises skill libraries across the entire agent ecosystem.

**RL integration frontier**: Memory-R1, MemAgent, RMM, MEM1, Mem-α demonstrate feasibility of RL-trained memory management. But no established training recipes, reward signal specifications, or benchmark suites exist for this paradigm — it remains a research direction, not a deployable technology.

---

## Connections

- [[themes/agent_memory_systems|Agent Memory Systems]] — the primary theme; this survey is the field's most comprehensive structural map to date
- [[themes/agent_self_evolution|Agent Self-Evolution]] — Darwin Gödel Machine and evolutionary case-to-skill compilation represent the memory frontier of self-improving agents
- [[themes/agent_systems|Agent Systems]] — shared memory coordination is a structural prerequisite for scaling multi-agent collectives
- [[themes/context_engineering|Context Engineering]] — adjacent but distinct: context engineering optimises the inference-time window; agent memory handles cross-session persistence and self-evolution
- [[themes/knowledge_and_memory|Knowledge and Memory]] — the taxonomy formalises the relationship between factual, experiential, and working memory functions, grounding prior informal distinctions
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]] — agentic RAG occupies the closest conceptual space to agent memory; the boundary is whether the store is persistent and self-evolving (memory) vs. external and task-specific (RAG)

---

## Key Claims

1. **Case-based memory** offers high informational fidelity and verifiable imitation evidence, but raw trajectory storage imposes retrieval efficiency and context window consumption challenges that scale poorly.
2. **Strategy-based memory** elevates experiences into editable, auditable, composable high-level knowledge — but strategies are structural guidelines, not executable actions, necessitating skill-based memory for callable capabilities.
3. **Agent Workflow Memory (AWM)** induces reusable workflows on Mind2Web and WebArena, using them as high-level scaffolds to guide subsequent generation, improving success rates and reducing steps.
4. **The API retrieval bottleneck**: exponential growth of API libraries has shifted the primary challenge from tool invocation to retrieval — standard IR methods fail to capture functional tool semantics.
5. **Context windows are passive buffers**: standard LLM context windows lack mechanisms to actively select, sustain, or transform their workspace; current models do not exhibit human-like working memory characteristics.
6. **History accumulation is blocking**: even with extended context windows, multi-turn history inevitably saturates attention budgets, increases latency, and induces goal drift — raw retention cannot scale.
7. **Query construction is systematically underweighted**: query quality has substantial impact on reasoning performance; prior research over-invested in architecture while neglecting the retrieval query.
8. **MCP as convergence layer**: the Model Context Protocol provides an open standard that unifies agent tool discovery and use, with broad platform support indicating convergence toward a common interface.
9. **Memory is a first-class primitive**: memory is what enables the transformation of static LLMs into adaptive agents — not an auxiliary storage module but the central architectural distinction between LLM and agent.
10. **The design of agent memory remains a central and open research problem** — expected to remain unsolved for the foreseeable future, and likely to play a decisive role in the development of robust, general, and enduring intelligence.

## Key Concepts

- [[entities/a-mem|A-MEM]]
- [[entities/bm25|BM25]]
- [[entities/context-engineering|Context engineering]]
- [[entities/expel|ExpeL]]
- [[entities/gaia|GAIA]]
- [[entities/generative-agents|Generative Agents]]
- [[entities/graphrag|GraphRAG]]
- [[entities/hipporag|HippoRAG]]
- [[entities/hyde|HyDE]]
- [[entities/lightmem|LightMem]]
- [[entities/locomo|LoCoMo]]
- [[entities/longbench|LongBench]]
- [[entities/longmemeval|LongMemEval]]
- [[entities/mem1|MEM1]]
- [[entities/mem0|Mem0]]
- [[entities/memos|MemOS]]
- [[entities/memory-r1|Memory-R1]]
- [[entities/memorybank|MemoryBank]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/prime|PRIME]]
