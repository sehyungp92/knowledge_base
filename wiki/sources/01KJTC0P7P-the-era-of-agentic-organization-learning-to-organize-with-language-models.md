---
type: source
title: 'The Era of Agentic Organization: Learning to Organize with Language Models'
source_id: 01KJTC0P7PEXCP05K0TGKSPE6Y
source_type: paper
authors:
- Zewen Chi
- Li Dong
- Qingxiu Dong
- Yaru Hao
- Xun Wu
- Shaohan Huang
- Furu Wei
published_at: '2025-10-30 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Era of Agentic Organization: Learning to Organize with Language Models

**Authors:** Zewen Chi, Li Dong, Qingxiu Dong, Yaru Hao, Xun Wu, Shaohan Huang, Furu Wei
**Published:** 2025-10-30 00:00:00
**Type:** paper

## Analysis

# The Era of Agentic Organization: Learning to Organize with Language Models
2025-10-30 · paper · Zewen Chi, Li Dong, Qingxiu Dong, Yaru Hao, Xun Wu et al. (7 total)
https://arxiv.org/pdf/2510.26658

---

### Motivation & Prior Limitations
- Sequential thinking in LLMs is fundamentally bottlenecked by serial decoding, leaving substantial parallelism potential untapped when problems contain conditionally independent sub-problems.
  - Sequential decoding produces a single chain-of-thought trajectory; the entire reasoning budget is consumed along one path even when branches could be explored concurrently.
- Parallel thinking approaches (e.g., sampling multiple independent traces and aggregating via majority vote) improve accuracy but at significant latency cost, bounded by the slowest trace plus aggregation overhead.
  - Parallel methods are limited not only by the slowest thinking trace but also by extra delay incurred during final aggregation; they effectively multiply latency rather than reduce it.
- Existing parallel and multi-agent reasoning systems rely on manually designed, fixed workflows that cannot adapt to the diverse structural requirements of different queries — some tasks benefit from divide-and-conquer, others from step-by-step reasoning, and no single predetermined topology handles both well.
  - APR demonstrates parallel reasoning by imitating DFS/BFS execution traces, but this limits applicability to open-ended tasks where no universal algorithmic procedure exists.
- Learning an effective agentic organization policy — rather than hand-engineering it — remains an open problem, as designing optimal thinking structures for every query class is intractable.

---

### Proposed Approach
- The paper introduces AsyncThink (Asynchronous Thinking), a reasoning paradigm in which a single LLM simultaneously plays two roles — an **organizer** that dynamically structures execution via Fork/Join action tags, and **workers** that execute assigned sub-queries concurrently and return results — all expressed entirely in text within the model's autoregressive decoding loop.
  - Unlike parallel thinking, which dispatches the same original query to multiple independent agents, AsyncThink's organizer decomposes problems into *diverse* sub-queries, assigns them selectively, and merges intermediate results before deciding whether to fork further — enabling adaptive, multi-stage divide-and-merge reasoning.
  - The Fork-Join action tags are plain text tokens, requiring no architectural modification to the underlying LLM; this means the execution graph is produced by the model's own generation process rather than an external scheduler.
- Training proceeds in two stages: (1) **Cold-start format SFT**, where GPT-4o-synthesized organizer-worker traces (with randomly sampled thinking topologies to prevent collapse to a single structure) teach the model the syntax of Fork/Join actions; and (2) **Reinforcement learning** with a composite reward covering answer accuracy, format compliance, and a **thinking concurrency reward** (η = mean active workers / capacity, clipped at threshold τ to prevent reward hacking).
  - The concurrency reward specifically incentivizes the model to distribute thinking across workers rather than deferring all parallelism to the end, and ablations confirm it is critical for latency reduction.
  - Policy optimization extends GRPO to the non-sequential episode structure: the organizer trace and all worker traces are treated as a single unit for advantage computation, with worker-returned text masked from the organizer loss so the model is only trained on tokens it actually generated.
- Critical-path latency — the minimum sequential depth required given the Fork-Join DAG, computed via dynamic programming — is used as the primary efficiency metric, abstracting away hardware and implementation details and enabling fair comparison across methods.

---

### Results & Capabilities
- On **math reasoning** (AIME-24 and AMC-23), AsyncThink matches the accuracy of the best baseline (Parallel-Thinking-L2K: 38.7% on AIME-24, 72.8% on AMC-23) while achieving 28% lower critical-path latency (1,468 vs. ~2,048 tokens), and slightly exceeds it on AMC-23 (73.3%).
  - Workers are each restricted to 512-token responses per sub-query — far shorter than the 2K traces used by baselines — yet collective accuracy remains competitive, indicating that organized short fragments can substitute for long monolithic traces.
- On **multi-solution countdown** (MCD), AsyncThink substantially outperforms both sequential (70.5% all-correct) and parallel thinking (68.6% all-correct) baselines, achieving 89.0% strict all-correct accuracy, demonstrating stronger multi-solution coverage and reliability.
- AsyncThink generalizes its learned organization policy **zero-shot to unseen tasks**: a model trained only on countdown data achieves 89.4% accuracy on 4×4 Sudoku versus 84.2% for parallel thinking, with substantially lower latency (2,853 vs. 3,694 tokens), despite receiving no Sudoku-specific training.
  - This cross-task transfer suggests AsyncThink learns a domain-general decomposition strategy rather than task-specific heuristics.
- Ablation studies confirm that all three components are necessary: removing RL drops MCD accuracy to ~0% (the model cannot use the thinking mechanism correctly); removing format SFT causes the model to fork but maintain only minimum concurrency (η = 1/c); removing the concurrency reward raises latency by ~38% on MCD and ~32% on AMC-23 while also reducing accuracy.
- Training dynamics reveal that RL first drives accuracy up while latency spikes to the token budget ceiling, then the model self-organizes to increase concurrency and bring latency back down — the number of Fork operations per query increases monotonically, showing progressive learning to distribute rather than serialize thinking.

---

### Implications
- AsyncThink demonstrates that **organization policy for multi-agent reasoni

## Key Claims

1. AsyncThink achieves 28% lower inference latency compared to parallel thinking while improving accuracy on mathematical reasoning.
2. AsyncThink generalizes its learned asynchronous thinking capabilities to unseen tasks without additional training.
3. Current parallel thinking approaches are limited not only by the slowest thinking trace but also by the additional delay incurred during the final aggregation process.
4. Parallel thinking methods rely on manually designed, fixed workflows that cannot accommodate the diverse requirements of different queries.
5. The AsyncThink thinking protocol operates entirely at the input-output surface of LLMs and does not require any modification to the underlying neural network architectures.
6. Sequential thinking and parallel thinking are special cases of the AsyncThink framework: sequential thinking arises when no Fork actions are taken, and parallel thinking arises when the organizer repe
7. In AsyncThink, the organizer and worker roles share the same LLM backbone and both perform autoregressive text decoding, distinguished only by the set of actions each can take.
8. AsyncThink uses a two-stage training procedure: cold-start format fine-tuning followed by reinforcement learning.
9. GPT-4o predominantly produces organizer traces following only two distinct thinking topologies during cold-start data synthesis, which limits model plasticity during training.
10. After cold-start format fine-tuning, the model can emit valid organizer actions but has not yet learned to produce correct answers with asynchronous thinking.

## Capabilities

- LLMs can be trained via RL to self-organize their internal reasoning into dynamically concurrent Fork-Join execution structures, enabling adaptive multi-worker thinking without architectural modification
- Asynchronous thinking via learned Fork-Join protocol achieves 28% lower critical-path latency than parallel thinking while matching or exceeding its accuracy on AIME-24 and AMC-23 math reasoning benchmarks
- A single LLM simultaneously playing organizer and worker roles via text-format action tags (Fork/Join) achieves concurrent multi-agent thinking with zero modifications to underlying neural network architecture
- AsyncThink generalizes learned asynchronous thinking zero-shot to unseen task types — a model trained only on countdown problems achieves 89.4% on 4×4 Sudoku, outperforming parallel thinking (84.2%) with lower latency
- GRPO extended to handle non-sequential multi-role episodes: organizer and worker traces treated as a single unit for reward computation, with worker-returned segments masked from organizer loss
- Short, organized 512-token thinking fragments coordinated via learned asynchronous policy can collectively match the reasoning quality of 2K-token monolithic sequential traces, suggesting thinking length is substitutable by thinking structure

## Limitations

- Worker-organizer communication and synchronization overhead consumes a substantial portion of the latency budget — 512-token per-worker limits yield ~1.5K overall critical-path latency, meaning coordination cost alone exceeds individual worker compute
- Without cold-start format fine-tuning, RL training fails to discover effective asynchronous thinking — models collapse to minimal concurrency (η = 1/c), performing Forks but never actually parallelizing
- Leverage reward (rewarding Fork operations following a Join) induces training instability and mode collapse to near-sequential thinking with interleaved Forks and Joins
- Scaling laws for agentic organization are entirely unknown — the paper acknowledges no understanding of how accuracy-latency trade-offs evolve as agent pool capacity grows from a few to hundreds or thousands of workers
- Cold-start data synthesis requires GPT-4o to detect conditionally independent thinking fragments — creating a bootstrapping dependency on a stronger external model that may not generalize to novel task structures
- GPT-4o training data synthesis produces only two distinct thinking topologies (interleaved vs. batch Fork-Join), limiting exploration diversity and requiring random structure injection to prevent mode collapse during RL
- Evaluation confined to three narrow structured tasks (countdown arithmetic, AIME/AMC math, Sudoku) with no validation on NLP, code generation, open-ended reasoning, or real-world multi-step workflows
- Parallel thinking approaches remain limited by slowest-trace latency plus aggregation overhead when using fixed, manually designed workflows — adaptive policy is only achievable through the full two-stage RL training pipeline
- Recursive agentic organization (workers promoting to sub-organizers for hierarchical decomposition) is entirely absent from the current system, blocking application to deeply nested multi-level problems

## Bottlenecks

- Scaling laws of agentic organization are unmapped — how accuracy, latency, and coordination overhead evolve as agent pool grows beyond c=4 to hundreds or thousands of workers is an open empirical question blocking production deployment
- Reward design for agentic organization training is unstable — concurrency rewards are gameable, leverage rewards cause mode collapse, and no principled reward formulation exists that stably incentivises both parallelism and reasoning quality simultaneously
- Bootstrapping asynchronous thinking training requires a stronger teacher model (GPT-4o) to identify decomposable sub-queries — no self-sufficient data generation pipeline exists for domains where task decomposability is not obvious

## Breakthroughs

- Reinforcement learning can train a single LLM to self-discover and optimize its own concurrent thinking structure via Fork-Join actions, achieving a better accuracy-latency frontier than both sequential and manually-designed parallel thinking

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/deepscaler-dataset|DeepScaleR Dataset]]
