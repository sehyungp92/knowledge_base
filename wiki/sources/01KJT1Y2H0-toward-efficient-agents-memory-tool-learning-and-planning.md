---
type: source
title: 'Toward Efficient Agents: Memory, Tool learning, and Planning'
source_id: 01KJT1Y2H0E1TNW0DK3V51VCSW
source_type: paper
authors:
- Xiaofang Yang
- Lijun Li
- Heng Zhou
- Tong Zhu
- Xiaoye Qu
- Yuchen Fan
- Qianshan Wei
- Rui Ye
- Li Kang
- Yiran Qin
- Zhiqiang Kou
- Daizong Liu
- Qi Li
- Ning Ding
- Siheng Chen
- Jing Shao
published_at: '2026-01-20 00:00:00'
theme_ids:
- agent_evaluation
- agent_memory_systems
- agent_systems
- evaluation_and_benchmarks
- knowledge_and_memory
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Toward Efficient Agents: Memory, Tool Learning, and Planning

This survey reframes LLM-based agent efficiency as a Pareto optimization problem — maximizing task success under fixed cost, or minimizing cost at comparable effectiveness — and provides the first comprehensive taxonomy across three modular components: efficient memory management, efficient tool learning, and efficient planning. Unlike prior efficiency literature focused on model compression for single-turn LLM inference, this work addresses the compounding resource costs unique to multi-step agentic execution, where token consumption, tool invocations, memory accesses, and retries all independently contribute to prohibitive real-world deployment costs.

**Authors:** Xiaofang Yang, Lijun Li, Heng Zhou, Tong Zhu, Xiaoye Qu, Yuchen Fan, Qianshan Wei, Rui Ye, Li Kang, Yiran Qin, Zhiqiang Kou, Daizong Liu, Qi Li, Ning Ding, Siheng Chen, Jing Shao
**Published:** 2026-01-20
**Type:** Paper
**Source:** https://arxiv.org/pdf/2601.14192

---

## Why Agent Efficiency Is a Distinct Problem

Pure LLM inference costs are dominated by token generation. Agentic systems face a fundamentally different cost structure formalized as:

> `Cost_agent ≈ α·N_tok + I_tool·Cost_tool + I_mem·Cost_mem + I_retry·Cost_retry`

Each recursive step's output becomes the next step's input, creating **compounding token accumulation** that scales super-linearly with task length. A single deep-research task may invoke a search API 600 times. Model compression alone — the dominant approach in efficient LLM literature — cannot address tool invocation frequency, memory access overhead, or retry rates.

This compounding cost structure makes long-horizon agent deployment economically infeasible without dedicated efficiency optimization at the system level, not just the model level. The survey is the first to treat these three overhead sources jointly under a POMDP-augmented formal agent model with an explicit tool interface and memory component.

---

## Efficient Memory

### The Core Tension

An LLM's context window is finite; potentially relevant interaction history is effectively unbounded. Naively appending raw history degrades performance before hard limits are reached — the "lost in the middle" phenomenon means burying relevant information in long sequences hurts accuracy independently of computational cost. Any memory system must trade off between compression ratio and information fidelity, and **no principled method currently exists for finding the optimal balance**.

### Working Memory: Compression Strategies

Two convergent principles emerge across methods:

**Sequential rewriting** keeps prompt size roughly constant across long-horizon tasks. MemAgent overwrites a summarized memory state per chunk; [[entities/mem1|MEM1]] uses reinforcement learning to maintain a fixed-length internal state tagged as `<IS></IS>` that replaces itself at each step, enabling sequential long-input processing without context growth.

**Latent KV-cache compression** (Activation Beacon, MemoRAG, MemoryLLM, M+) compresses long histories into fixed-size neural states, avoiding proportional growth in attention cost. Titans takes this further — a test-time trainable neural memory module that writes only when prediction error is high, combining selective online learning with memory efficiency.

> *Maturity: research only.* These approaches demonstrate strong in-lab results but remain unvalidated in production agentic deployments.

### External Memory: Graph and Hierarchical Structures

**Graph-based memory** (Zep, AriGraph, Mem0g) incrementally builds relational memory from agent interactions with time-aware validity tracking. Compression efficiency comes from merging repeated content about the same entity into a single node, avoiding unbounded prompt growth. This enables efficient multi-hop evidence traversal but introduces retrieval latency and noise absent in working memory.

**Hierarchical multi-tier systems** (MemGPT, MemoryOS, MemOS) implement OS-style virtual memory paging — partitioning context into system instructions, writable working context, and a FIFO message buffer with external retrieval for overflow. Policy-driven promotion/demotion across tiers mirrors operating system memory management.

> *Maturity: demo.* These systems have been demonstrated end-to-end but not yet at scale.

### Memory Management Policies

A second convergent principle: **hybrid management** outperforms either extreme. Rule-based triggers (FIFO eviction, forgetting curves) handle routine capacity control cheaply; LLM calls are reserved for semantically sensitive decisions (merge-or-add, conflict resolution). This avoids the constant LLM overhead of purely adaptive management while avoiding the accuracy drops of purely static rules.

However, both extremes have documented failure modes:
- **Forgetting-curve management** (A-MEM) effectively controls size and reduces retrieval time but causes **substantial task performance drops** — a striking result for a technique borrowed from cognitive science.
- **LLM-based management** requires extra LLM calls per interaction, increasing financial costs and response latency proportionally with interaction frequency.

**Memory-R1** takes a different approach: RL-trained agents learn optimal CRUD policies (ADD, UPDATE, DELETE, NOOP) over external memory stores, replacing heuristics or expensive per-step LLM calls with a trained lightweight management policy. This represents the survey's clearest breakthrough in memory — demonstrating that management policy itself can be learned rather than hand-engineered or delegated to expensive LLM calls.

### Multi-Agent Memory

Duplicating interaction histories across individual agent prompts (early CAMEL-style systems) is prohibitively expensive. **LatentMAS** reduces inter-agent communication overhead by having agents exchange compact hidden states (layer-wise KV caches) rather than full token histories. The tension between shared memory (consistency risk from concurrent writes, noisy retrieval under high agent counts) and local memory (redundancy, staleness) remains an open architectural problem.

---

## Efficient Tool Learning

### Tool Selection

Three paradigms with distinct efficiency profiles:

| Paradigm | Approach | Efficiency | Generalization |
|---|---|---|---|
| External retriever | Semantic search over tool descriptions | High overhead, scales | Generalizes to new tools |
| Multi-label classification (MLC) | Trained classifier | Fast, low-cost | Requires full retraining for new tools |
| Vocabulary-based (ToolGen, ToolkenGPT) | Tools as special tokens | Next-token speed | **Fails on unseen tools** |

MLC cannot handle growing or changing tool sets — any addition requires full model retraining, making it impractical for dynamic ecosystems. Vocabulary-based methods suffer from inaccurate invocation timing and poor generalization to post-training tools. External retrievers generalize but at retrieval latency cost. **No selection paradigm currently solves all three constraints simultaneously.**

### Tool Calling

**Parallel execution** (LLMCompiler, LLM-Tool Compiler) dispatches independent tool calls concurrently rather than sequentially, achieving measurable reductions in latency and cost for multi-tool tasks. This is the most production-mature capability in the survey.

**Cost-aware calling** (BTP — Budget-Constrained Tool Learning with Planning) formulates tool invocation as a knapsack optimization, pre-computing optimal tool budgets via dynamic programming to enforce hard budget constraints as a forward pass. Tree search-based tool planning (LATS, CATS) is theoretically sound but **computationally prohibitive** — exhaustive branch exploration for optimal tool call sequences requires traversing exponentially large action spaces.

### Tool-Integrated Reasoning

The dominant convergent principle across tool learning methods: **RL reward shaping to penalize redundant invocations** (OTC-PO, ToolOrchestra, AutoTIR, SWiRL). The field has shifted from "maximize tool use for accuracy" to "minimize unnecessary interactions" — a fundamental reorientation of what good tool use means.

---

## Efficient Planning

### Single-Agent Inference-Time Strategies

**Adaptive budgeting** via fast/slow system switching (SwiftSage) routes simpler sub-problems to cheap fast models and escalates only genuinely complex steps. **Structured search** (MCTS/A* variants: LATS, CATS) prunes planning trajectories rather than exhaustively exploring. **Task decomposition** (ReWOO, Alita) separates planning from execution, pre-generating tool call plans without interleaving reasoning, reducing total steps.

### Learning-Based Planning Evolution

Policy optimization via RL (QLASS, ETO) and skill memory accumulation (VOYAGER, GAP) migrate computation from expensive online search to offline learning or structured retrieval — achieving complex goals within strict resource constraints by amortizing planning cost across tasks.

### Multi-Agent Planning Efficiency

The most striking efficiency finding in planning: MAS communication overhead can be reduced from **O(N²) to O(N)** through structured topologies (Chain-of-Agents, MacNet, DAG-based ordering). Beyond topology, **distillation** of multi-agent interaction graphs into single-student models (MAGDI, D&R) retains collective reasoning quality while reverting to single-agent inference cost — the efficiency of one model, the reasoning of many.

Protocol compression (pseudocode rather than natural language inter-agent messages) reduces communication volume without losing coordination fidelity.

---

## Open Problems and Limitations

### Fundamental Unsolved Problems

**The compression-performance trade-off** has no principled solution. Experiments (LightMem) demonstrate a clear monotonic relationship: excessive compression degrades accuracy, mild compression preserves accuracy at higher cost. The optimal compression rate is task-dependent, domain-dependent, and currently found only by search or heuristic.

**The online-offline memory update dilemma** is a fundamental architectural tension. Real-time adaptation requires high-latency LLM calls; low-latency offline-only updates produce slow adaptation to new information. No architecture currently achieves both simultaneously — an unsolved requirement for production long-running agents.

**Tool generalization** to unseen tools remains unsolved for efficient paradigms. The efficiency-generalization frontier cannot currently be reached: the fastest selection methods (vocabulary-based, MLC) fail on new tools; the most generalizable (retrieval) carries overhead that undermines the efficiency motivation.

### Benchmark Gap

Agent efficiency benchmarks are sparse and non-standardized. The survey itself is motivated by this absence — effectiveness-focused benchmarks (SWEBench, GAIA) do not measure cost-performance Pareto frontiers. Without standardized efficiency evaluation, systematic research progress and fair method comparison are blocked. The survey identifies this as the most immediately addressable bottleneck (months horizon vs. 1-2 years for architectural problems).

### Structural Cost Issues

- **Expanding working memory** causes computational growth (textual) or increased memory footprint (latent) — no approach avoids the fundamental cost of long-horizon context maintenance, only shifting the cost profile
- **LLM-based retrieval** incurs substantial token and latency overhead, making it unusable as a general-purpose retrieval mechanism
- **Shared MAS memory** is prone to inconsistency from concurrent writes — noisy and costly to retrieve without consolidation and access control

---

## Connections

**Themes:** [[themes/agent_memory_systems|Agent Memory Systems]] · [[themes/agent_systems|Agent Systems]] · [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]] · [[themes/knowledge_and_memory|Knowledge and Memory]] · [[themes/agent_evaluation|Agent Evaluation]] · [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]

**Key entities:** [[entities/mem1|MEM1]] · Titans · MemGPT · [[entities/memory-r1|Memory-R1]] · LLMCompiler · LatentMAS

**Related open problems:** The compression-performance trade-off documented here connects directly to debates about [[themes/knowledge_and_memory|retrieval-augmented generation]] — the question of what to keep in context vs. externalize is the same underlying problem in a different architectural frame. The O(N²) → O(N) communication finding in MAS has direct implications for [[themes/agent_systems|multi-agent system]] scaling discussions.

## Key Concepts

- [[entities/a-mem|A-MEM]]
- [[entities/expel|ExpeL]]
- [[entities/lightmem|LightMem]]
- [[entities/mem1|MEM1]]
- [[entities/mem0|Mem0]]
- [[entities/memos|MemOS]]
- [[entities/memory-r1|Memory-R1]]
- [[entities/memorybank|MemoryBank]]
- [[entities/readagent|ReadAgent]]
- [[entities/zep|Zep]]
