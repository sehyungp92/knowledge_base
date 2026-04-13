---
type: source
title: 'Memp: Exploring Agent Procedural Memory'
source_id: 01KJTMCJY1VR7XBK30K79RA9A4
source_type: paper
authors:
- Runnan Fang
- Yuan Liang
- Xiaobin Wang
- Jialong Wu
- Shuofei Qiao
- Pengjun Xie
- Fei Huang
- Huajun Chen
- Ningyu Zhang
published_at: '2025-08-08 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Memp: Exploring Agent Procedural Memory

**Authors:** Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, Ningyu Zhang
**Published:** 2025-08-08 00:00:00
**Type:** paper

## Analysis

# Memp: Exploring Agent Procedural Memory
2025-08-08 00:00:00 · paper · Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao et al. (9 total)
https://arxiv.org/pdf/2508.06433

---

### Motivation & Prior Limitations
- LLM-based agents lack robust procedural memory, forcing them to restart complex multi-step tasks from scratch every time despite recurring structural similarities across tasks, leading to redundant exploration, high token consumption, and vulnerability to mid-task disruptions.
  - Existing frameworks like LangGraph, AutoGPT, Memory Bank, and Soar provide coarse memory abstractions (buffers, rule chunks, production systems) but leave the lifecycle optimization of procedural skills — how they are built, indexed, patched, and pruned — largely unexamined.
  - Procedural knowledge in contemporary agents is either hand-crafted as brittle prompt templates or implicitly entangled in expensive-to-update model parameters, with no reliable way to measure how efficiently an agent grows its procedural skills or to ensure new experiences improve rather than harm performance.
- Prior work on learning from experience (Voyager, AWM, AutoManual) uses procedural memory in limited ways but lacks systematic analysis of how to construct, retrieve, and update such memory across trajectories, and existing update strategies are predominantly simple "merge" appends with no error-correction or deprecation logic.

---

### Proposed Approach
- Memp is a task-agnostic framework that treats procedural memory as a first-class optimization object, systematically studying strategies across three lifecycle phases: Build, Retrieval, and Update.
  - **Build:** Three memory formats are explored — verbatim Trajectory storage, high-level Script abstraction distilled by the model, and Proceduralization (combining both). Proceduralization integrates concrete step-by-step examples with abstract script-like guidance, outperforming either format alone.
  - **Retrieval:** Memory entries are indexed with task-derived keys, and retrieval is performed via cosine similarity over vector embeddings. Three key strategies are compared: random sampling, query-vector matching (Query), and keyword-averaged similarity (AveFact), with AveFact performing best by focusing retrieval on core task features.
  - **Update:** Three online update mechanisms are introduced beyond the naive append baseline — Validation (retaining only successful trajectories), Adjustment (revising erroneous memories in-place using reflexion when a retrieved memory leads to failure), and Vanilla (unconditional append). The Adjustment/reflexion-based mechanism substantially outperforms the others by embedding error correction into the update loop.
- The memory library is modeled formally as an MDP-grounded structure with an explicit update function supporting add, delete, and modify operations, allowing the memory to evolve continuously with task experience rather than accumulating stale or contradictory entries.

---

### Results & Capabilities
- Proceduralization (combined trajectory + script) consistently outperforms no-memory baselines across all three backbone models on both benchmarks, with GPT-4o achieving 79.94% commonsense constraint score on TravelPlanner (vs. 71.93% without memory) and 87.14%/77.86% dev/test success on ALFWorld (vs. 39.28%/42.14%), while reducing steps from 17.84 to 14.62 and 23.76 to 15.01 respectively.
  - Similar gains hold for Claude-3.5-sonnet and Qwen2.5-72B, confirming the finding generalizes beyond proprietary models.
- The reflexion-based Adjustment update strategy delivers the largest improvements over time, surpassing the second-best strategy by +0.7 reward points and achieving a 14-step reduction by the final task group, demonstrating that continual error-correcting memory update drives near-linear mastery.
- Procedural memory built from GPT-4o transfers effectively to Qwen2.5-14B-Instruct, raising the smaller model's task completion rate by ~5% and reducing average steps by 1.6 on TravelPlanner, confirming that distilled procedural knowledge can be ported across models with minimal overhead.
  - This cross-model transfer suggests a practical workflow: use a strong model to build a high-quality offline memory library, then deploy it to cheaper or smaller models at inference time.
- Scaling the number of retrieved memories improves agent performance up to a plateau (~10–12 retrieved memories for GPT-4o on ALFWorld), after which excessive retrieval degrades performance by overloading context length with less precise memories.
- Compared to ReAct, Expel, and AWM baselines on ALFWorld with GPT-4o, Memp achieves the highest dev and test success rates while requiring the fewest steps, confirming the advantage of systematic procedural memory over ad hoc or partial memory approaches.

---

### Implications
- Procedural memory as an explicit, updatable, first-class component represents a concrete path toward self-improving agents — ones that accumulate task-solving competence across episodes rather than remaining stateless, which is directly relevant to long-horizon personal assistant and autonomous agent scenarios where task repetition is the norm.
- The demonstrated cross-model transferability of procedural memory has significant practical implications for continual learning and deployment economics: expensive frontier model inference can be used to build high-quality memory libraries that then bootstrap cheaper models, effectively decoupling knowledge acquisition from knowledge utilization.
- The reflexion-based update mechanism shows that error-correction embedded in memory management — not just task-level reflection — is a lever for compounding improvement, suggesting that future agent architectures for continual learning should treat memory maintenance as an active optimization loop rather than passive storage.
- For retrieval-augmented generation systems, the finding that semantic key construction (query-vector o

## Key Claims

1. LLM-based agents suffer from brittle procedural memory that is manually engineered or entangled in static parameters
2. Combining full retrieved trajectories with high-level script abstractions (Proceduralization) yields optimal procedural memory performance
3. Procedural memory reduces agent step count by approximately 50% on similar tasks
4. Semantic retrieval strategies (query-based and AveFact) substantially outperform random sampling for procedural memory retrieval
5. Reflection-based (Adjustment) memory update is the most effective update strategy, surpassing the second-best strategy by +0.7 points and achieving a 14-step reduction by the final task group
6. All memory update strategies improve agent performance monotonically as more task groups are completed sequentially
7. Procedural memory built from a stronger model (GPT-4o) can be transferred to a weaker model (Qwen2.5-14B), improving task completion rate by 5% and reducing average steps by 1.6 on TravelPlanner
8. Procedural memory transfer from strong to weak models yields gains on both success rate and trajectory length on ALFWorld
9. Retrieving too many procedural memories degrades agent performance due to increased context length and introduction of less accurate memories
10. Agent performance improves steadily then plateaus as number of retrieved procedural memories increases, showing an optimal retrieval count exists

## Capabilities

- LLM agents equipped with distilled procedural memory (combining step-by-step trajectories and high-level script abstractions) achieve ~50% higher task success rates and ~50% fewer execution steps on long-horizon tasks, demonstrated across GPT-4o, Claude-3.5-sonnet, and Qwen2.5-72B on TravelPlanner a
- Procedural memory built from a stronger model (GPT-4o) can be transferred intact to a substantially smaller model (Qwen2.5-14B, ~10x smaller), yielding +5% task completion rate and -1.6 average steps on TravelPlanner without any parameter updates to the weaker model
- Reflexion-based procedural memory update — combining a failed execution trajectory with its original memory entry to produce a corrected version — is the most effective online memory update strategy, outperforming simple append by +0.7 reward points and -14 steps by final task group
- Scaling retrieved procedural memory count improves agent performance monotonically up to a plateau; peak performance reached at ~10-15 retrieved memories, with performance declining beyond that threshold due to context saturation

## Limitations

- Memp's procedural memory retrieval is restricted to vector cosine-similarity search with manually crafted keys; BM25 and other classical precision-retrieval methods have not been incorporated, leaving an acknowledged accuracy gap
- The entire framework depends on explicit, benchmark-supplied binary reward signals for memory update gating; it cannot determine task success in real-world deployments where rewards are sparse, absent, or require human or LLM judgment
- Retrieving too many procedural memories beyond an optimal ceiling degrades agent performance — a hard performance cliff caused by context window saturation and introduction of low-relevance memories that interfere with reasoning
- Script-format memory generalizes better to out-of-distribution test tasks while trajectory-format memory excels on tasks similar to training episodes — no single memory representation dominates both regimes, requiring practitioners to choose based on unknown deployment assumptions
- All evaluations are conducted only on TravelPlanner (structured planning) and ALFWorld (simulated household tasks) — both are controlled benchmark environments with known reward functions; real-world generalizability is entirely untested
- Memory update is evaluated only in sequential (one-task-at-a-time) execution regimes; performance in parallel multi-agent pipelines or asynchronous environments where multiple agents share and update a memory store simultaneously is entirely unexplored
- Current LLM agent procedural knowledge is either hand-crafted as static prompt templates or implicitly encoded in frozen model parameters — neither form is updateable without expensive retraining or manual engineering
- Long-horizon agentic tasks demand dozens of steps and large token budgets; unpredictable external events (network failures, UI changes, schema shifts) can derail execution mid-task, and current agents have no recovery mechanism — forcing full restart
- Learning from experience methods in LLM agents face persistent low sample efficiency, poor cross-task generalization, and catastrophic forgetting when incorporating new experiences — acknowledged as standing field-level limitations
- Memory management in multi-turn agent interactions 'remains underexplored' — no established methodology exists for reliably learning and utilizing memory across distinct task trajectories; the Memp system itself acknowledges this as the primary motivation gap
- High token consumption during long-horizon task execution imposes significant cost even with procedural memory; memory reduces but does not eliminate redundant exploration, and each task still requires substantial context buildup

## Bottlenecks

- Absence of automated real-world reward signals prevents self-improving agent memory systems from operating outside benchmark environments — production deployment requires either human labelling of task success or a reliable LLM-as-judge mechanism that does not yet exist at sufficient reliability
- Vector-only retrieval in procedural memory systems leaves precision gains from exact-match and hybrid retrieval (BM25, keyword overlap) unrealised — cosine similarity captures semantic proximity but fails on precise procedural step matching
- Context window finite capacity imposes a hard ceiling on the number of useful procedural memories that can be injected per inference call — beyond ~10-15 retrieved memories performance degrades, blocking further scaling of experience-based agent improvement without architectural innovations in memor

## Breakthroughs

- Procedural memory distilled from a frontier model (GPT-4o) functions as a transferable, model-agnostic artifact — a ~10x smaller model (Qwen2.5-14B) that ingests this memory achieves measurable task performance gains without any weight updates, establishing memory as decoupled from model parameters

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/expel|ExpeL]]
- [[entities/react|ReAct]]
- [[entities/voyager|Voyager]]
