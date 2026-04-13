---
type: source
title: 'Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory'
source_id: 01KJT71V4QQ718BPYTKC0WR9D4
source_type: paper
authors:
- Tianxin Wei
- Noveen Sachdeva
- Benjamin Coleman
- Zhankui He
- Yuanchen Bei
- Xuying Ning
- Mengting Ai
- Yunzhe Li
- Jingrui He
- Ed H. Chi
- Chi Wang
- Shuo Chen
- Fernando Pereira
- Wang-Cheng Kang
- Derek Zhiyuan Cheng
published_at: '2025-11-25 00:00:00'
theme_ids:
- agent_evaluation
- agent_memory_systems
- evaluation_and_benchmarks
- knowledge_and_memory
- post_training_methods
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory

**Authors:** Tianxin Wei, Noveen Sachdeva, Benjamin Coleman, Zhankui He, Yuanchen Bei, Xuying Ning, Mengting Ai, Yunzhe Li, Jingrui He, Ed H. Chi, Chi Wang, Shuo Chen, Fernando Pereira, Wang-Cheng Kang, Derek Zhiyuan Cheng
**Published:** 2025-11-25 00:00:00
**Type:** paper

## Analysis

# Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory
2025-11-25 · paper · Tianxin Wei, Noveen Sachdeva, Benjamin Coleman, Zhankui He, Yuanchen Bei et al. (15 total)
https://arxiv.org/pdf/2511.20857

---

### Motivation & Prior Limitations
Existing LLM memory systems are fundamentally static: they retrieve past dialogue context to answer queries but do not abstract reusable reasoning strategies from accumulated experience, meaning agents remember *what was said* but not *what was learned*.
- Prior benchmarks such as StreamBench evaluate sequential learning but measure only factual retention without reasoning or trajectory reuse; LifelongBench studies retention across environments but does not model memory structure or updates.
- The critical gap is the absence of a unified framework that evaluates how different memory methods *retrieve, integrate, and evolve* historical strategies under realistic streaming conditions — LLMs repeatedly solve similar problems without leveraging prior solution patterns, wasting accumulated experience.
- Real-world deployments (interactive assistants, embodied agents) require handling continuous task streams, yet current systems provide no mechanism for test-time evolution — the ability to retrieve, integrate, and update memory continuously during deployment rather than relying on static pre-trained weights.

---

### Proposed Approach
The paper introduces Evo-Memory, a streaming benchmark and evaluation framework that restructures conventional static datasets into sequential task streams, forcing agents to search, adapt, and evolve memory after each interaction rather than performing one-off retrieval.
- The formal abstraction unifies all memory mechanisms under a single iterative tuple (F, U, R, C) — base LLM, update pipeline, retrieval module, and context constructor — with a canonical search→synthesis→evolve loop: retrieve relevant memory R(M_t, x_t), synthesize a working context C̃_t, produce output ŷ_t, then update M_t+1 = U(M_t, m_t).
- ExpRAG is provided as a simple retrieval-augmented baseline that encodes each task experience as a structured text entry and performs top-k similarity retrieval at inference time, instantiating in-context learning from prior task outcomes without iterative refinement.
- ReMem is the primary proposed method, extending ReAct-style agents with an explicit third action type — *Refine* — creating a Think→Act→Refine loop where the agent can actively prune noisy memories, reorganize stored experiences, and evolve its knowledge state mid-task rather than treating memory as passive context; this is formalized as a Markov decision process where the state encapsulates current input, memory state, and ongoing reasoning traces.
- Ten representative memory modules (retrieval-based, workflow, hierarchical, adaptive) are unified under the same evaluation protocol across 10 diverse datasets spanning factual knowledge, mathematics (AIME-24/25), graduate-level reasoning (GPQA-Diamond), tool use (ToolBench), and embodied goal-oriented interaction (AlfWorld, BabyAI, ScienceWorld, PDDL, Jericho).

---

### Results & Capabilities
ReMem achieves the strongest and most consistent performance across both single-turn and multi-turn settings on Gemini-2.5 and Claude 3.7 backbones, with particularly large gains in multi-turn embodied environments where long-horizon experience reuse matters most.
- On multi-turn benchmarks under Claude 3.7 Sonnet, ReMem reaches 0.92/0.96 success/progress on AlfWorld and 0.83/0.95 on PDDL, compared to the History baseline's 0.50/0.73 and 0.65/0.85 respectively — roughly doubling success rate on AlfWorld.
- On single-turn reasoning under Gemini-2.5 Flash, ReMem achieves 0.65 average exact match and 0.85/0.71 API accuracy on ToolBench, with improvements that are moderate but consistent across datasets and model families.
- Step efficiency improves dramatically: ReMem reduces average steps to task completion from 22.6 to 11.5 on AlfWorld, with ExpRAG and ExpRecent also showing strong efficiency gains despite their simplicity, suggesting that even lightweight test-time evolution meaningfully focuses reasoning.
- Performance gain from ReMem correlates strongly with within-dataset task similarity (Pearson r = 0.717 on Gemini-2.5 Flash, r = 0.563 on Claude 3.7 Sonnet), meaning recurring structural patterns in tasks are the primary driver of memory reuse benefit — high-similarity environments like PDDL and AlfWorld gain most, while diverse sets like AIME-25 or GPQA show limited transfer.
- When both successful and failed experiences are stored (RQ4), baseline methods suffer clear performance drops from retrieval noise, while ReMem remains robust by actively refining stored experiences — demonstrating that selective utilization and memory pruning are critical for stable adaptation under imperfect experience streams.
- Smaller models benefit disproportionately from self-evolving memory, suggesting test-time refinement is a practical path to enhancing lighter LLMs without parameter updates.
- ExpRAG, despite its simplicity, outperforms several more architecturally complex methods (MemOS, LangMem, AWM, DC variants), establishing experience retrieval as an underexplored but effective baseline.

---

### Implications
The distinction between *conversational recall* and *experience reuse* formalizes a capability gap that current evaluations systematically ignore, and Evo-Memory's streaming reformulation of static benchmarks provides a reusable template for injecting this dimension into future agent evaluations across any task domain.
- The strong correlation between intra-dataset task similarity and memory improvement implies that the structure of deployment environments — not just memory architecture — is a primary determinant of whether test-time learning is viable, which has direct consequences for how agentic systems should be designed and deployed.
- ReMem's Think→Act→Refine loop represents a minima

## Key Claims

1. Existing LLM memory systems remain largely static, retrieving information passively rather than evolving through use, and current evaluations test context recall but not experience reuse.
2. Conversational recall retrieves prior facts whereas experience reuse abstracts reasoning strategies for future tasks — these are fundamentally distinct capabilities.
3. No prior unified framework exists for evaluating how different memory methods retrieve, integrate, and evolve historical strategies in realistic streaming scenarios.
4. ReMem achieves success/progress rates of 0.92/0.96 on BabyAI and 0.95/0.62 on ScienceWorld under the Claude 3.7 Sonnet backbone.
5. Performance gains from self-evolving memory are notably larger in multi-turn settings than single-turn settings, indicating continual adaptation becomes increasingly valuable as task horizons lengthen
6. Smaller LLMs benefit particularly from self-evolving memory, suggesting test-time refinement is a practical path to enhancing lighter models.
7. ExpRAG, a simple retrieval-based baseline, outperforms several more complex memory architectures, indicating that explicit task-level experience reuse is underexplored.
8. ReMem's performance improvement strongly correlates with within-dataset task similarity (Pearson r=0.717 on Gemini 2.5 Flash, r=0.563 on Claude 3.7 Sonnet).
9. Tasks with higher embedding cluster ratios (higher intra-dataset structural similarity) yield larger memory reuse gains, while diverse low-similarity datasets like AIME-25 or GPQA show smaller gains.
10. ReMem reduces the average steps required to complete Alf World tasks from 22.6 to 11.5, demonstrating that continual refinement improves reasoning efficiency in addition to accuracy.

## Capabilities

- The ReMem action-think-memory-refine pipeline achieves 0.92/0.96 success/progress on Alf World and 0.73/0.83 on BabyAI with Claude 3.7 Sonnet, representing a 5x improvement over no-memory baseline in embodied multi-turn environments through active memory reasoning rather than passive retrieval.
- Simple experience retrieval (ExpRAG) — storing structured past task experiences and retrieving top-k similar ones as in-context examples — consistently outperforms several more complex adaptive memory systems (MemOS, LangMem, AWM) across both single-turn and multi-turn settings.
- Self-evolving memory with active refinement reduces task completion steps by ~50% in embodied environments: ReMem reduces average steps from 22.6 to 11.5 on Alf World, demonstrating that continual memory reorganisation improves reasoning efficiency, not just accuracy.
- Smaller LLMs benefit proportionally more from self-evolving memory than larger models, establishing test-time memory refinement as a practical path to enhancing lighter model capabilities without retraining.
- Self-evolving memory agents (ReMem) maintain stable performance across task difficulty transitions (Easy→Hard and Hard→Easy), reaching 0.94/0.97 success/progress in Hard→Easy settings, while baseline methods degrade significantly under distribution shift.

## Limitations

- Current LLM agents can recall past conversational facts but cannot abstract and reuse reasoning strategies from past interactions for future similar problems — they remember what was said, not what was learned.
- Self-evolving memory provides near-zero benefit for semantically diverse task streams: ReMem improvement correlates at r=0.717 with within-dataset task similarity, collapsing on heterogeneous benchmarks like GPQA and AIME-25 where tasks share little structural overlap.
- Naive memory accumulation without failure filtering degrades agent performance: storing both successful and failed task experiences introduces retrieval noise that hurts subsequent reasoning in baseline memory systems.
- Self-evolving memory provides negligible improvement for novel mathematical olympiad problems (AIME): Claude 3.7 Sonnet with ReMem scores 0.13/0.13 on AIME-24/25 vs 0.17/0.13 baseline, indicating that experience reuse is structurally incapable of helping with genuinely novel mathematical problems.
- Several state-of-the-art adaptive memory systems (MemOS, LangMem) are architecturally incompatible with embodied multi-turn environments, limiting benchmark coverage and indicating significant architectural constraints on generalizability across task types.
- Task sequence ordering substantially impacts self-evolving memory effectiveness: easy→hard vs hard→easy transitions produce different performance trajectories, meaning real-world deployment order of arbitrary tasks cannot guarantee the empirical gains observed in structured benchmarks.
- Procedural knowledge memory systems (Dynamic Cheatsheet, AWM) generalize poorly across domains — they perform well in structured mathematical settings but show limited flexibility for scientific reasoning and tool use, indicating brittleness in procedural abstraction.
- Self-evolving memory benefits are minimal for single-turn tasks and scale dramatically with interaction horizon — single-turn settings show only moderate improvements while embodied multi-turn tasks see 5x gains, suggesting memory evolution requires accumulated interaction depth to provide value.
- No unified evaluation framework for self-evolving memory existed before this work — the field lacked standardised benchmarks for measuring whether LLMs accumulate and reuse experience, preventing systematic comparison across memory designs.

## Bottlenecks

- No principled mechanism exists to learn from failure experiences without degrading agent memory quality — naive accumulation of failed experiences introduces retrieval noise that hurts future performance, and current systems require manual or heuristic filtering.
- Self-evolving memory effectiveness is fundamentally gated by inter-task semantic similarity — when deployed on heterogeneous real-world task streams, experience retrieval degrades because past experiences are structurally dissimilar to novel inputs, making retrieval ineffective or actively harmful.

## Breakthroughs

- Active memory reasoning integrated into the agent action loop (ReMem's think-act-refine pipeline) achieves 5x improvement in embodied agent success rates, establishing that treating memory as an active reasoning target — not passive context — is a qualitatively different and substantially more effec

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/agent-workflow-memory|Agent Workflow Memory]]
- [[entities/dynamic-cheatsheet|Dynamic Cheatsheet]]
- [[entities/mem0|Mem0]]
- [[entities/memos|MemOS]]
- [[entities/react|ReAct]]
