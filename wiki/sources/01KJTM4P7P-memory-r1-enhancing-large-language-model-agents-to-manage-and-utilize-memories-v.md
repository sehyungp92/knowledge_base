---
type: source
title: 'Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories
  via Reinforcement Learning'
source_id: 01KJTM4P7PSZ9TQ1WJX19JC1TM
source_type: paper
authors:
- Sikuan Yan
- Xiufeng Yang
- Zuchao Huang
- Ercong Nie
- Zifeng Ding
- Zonggen Li
- Xiaowen Ma
- Jinhe Bi
- Kristian Kersting
- Jeff Z. Pan
- Hinrich Schütze
- Volker Tresp
- Yunpu Ma
published_at: '2025-08-27 00:00:00'
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning

**Authors:** Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Jinhe Bi, Kristian Kersting, Jeff Z. Pan, Hinrich Schütze, Volker Tresp, Yunpu Ma
**Published:** 2025-08-27 00:00:00
**Type:** paper

## Analysis

# Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning
2025-08-27 00:00:00 · paper · Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding et al. (13 total)
https://arxiv.org/pdf/2508.19828

---

### Motivation & Prior Limitations
LLMs are fundamentally stateless, bounded by finite context windows that cause them to forget information across long conversations or multi-session tasks, preventing long-horizon reasoning.
- Existing memory-augmented pipelines rely on static, heuristic-driven RAG: retrieved memories are passed to the LLM without filtering or prioritization, causing the model to reason over both relevant and irrelevant content and become prone to distraction.
  - Liu et al. (2023) document the "lost in the middle" effect where too many retrieved entries degrade performance; heuristics can also return too few entries, omitting crucial context.
- Memory management — deciding what to store, update, or discard — is unsolved in learned systems: prior work (Mem0, MemGPT) applies CRUD-style operations but selects them via in-context instructions with no learning signal tied to correctness.
  - A concrete failure mode: a vanilla system shown "I adopted a dog named Buddy" then "I adopted another dog named Scout" issues DELETE+ADD, overwriting the original fact, instead of issuing a single UPDATE to consolidate.
- Supervised fine-tuning is impractical for memory operation labeling because annotating every ADD/UPDATE/DELETE/NOOP decision at scale requires prohibitive human effort.

---

### Proposed Approach
Memory-R1 is a reinforcement learning framework that trains two specialized agents — a Memory Manager and an Answer Agent — to actively manage and use an external memory bank, replacing heuristic pipelines with learned, outcome-driven policies.

- The **Memory Manager** is modeled as a policy πθ that takes newly extracted dialogue information and the current memory bank as input and outputs one of {ADD, UPDATE, DELETE, NOOP} along with updated memory content; it is rewarded by whether the resulting memory state enables the Answer Agent to answer downstream questions correctly (exact-match reward).
  - This outcome-driven reward requires no manual operation labels and propagates through the frozen Answer Agent to teach the manager which operations yield useful memory states.

- The **Answer Agent** applies a Memory Distillation policy: it receives 60 candidate memories retrieved via similarity-based RAG, filters them to the most relevant subset, and generates an answer; it is fine-tuned independently with exact-match reward.
  - Memory distillation is learned rather than heuristic, allowing the agent to acquire a filtering behavior that mirrors how humans retrieve broadly but integrate selectively.

- Both agents are fine-tuned with either PPO (Proximal Policy Optimization) or GRPO (Group Relative Policy Optimization); GRPO avoids an explicit value function by sampling G candidate actions per state and computing group-relative advantages, making it more stable under sparse rewards.
  - The two agents are trained separately (Memory Manager first, Answer Agent second with frozen manager) to avoid compounding instability under sparse reward signals.

- The operator set {ADD, UPDATE, DELETE, NOOP} is adopted from Mem0 (Chhikara et al., 2025) as a minimal yet expressive framework for memory dynamics; Memory-R1's novel contribution is learning when to apply these operators via RL rather than selecting them from in-context instructions.

---

### Results & Capabilities
Memory-R1-GRPO with LLaMA-3.1-8B-Instruct sets a new state of the art on LoCoMo, improving over the strongest prior baseline (MemoryOS) by 28.5% in F1, 34.0% in BLEU-1, and 30.2% in LLM-as-a-Judge, using only 152 training QA pairs.
- Memory-R1-GRPO with Qwen-2.5-7B-Instruct similarly outperforms MemoryOS by 24.5% (F1), 24.1% (BLEU-1), and 20.0% (LLM-as-a-Judge).
- Memory-R1 outperforms Memory-SFT — a supervised fine-tuning variant trained on GPT-5-generated operation trajectories using the same architecture and data — demonstrating that outcome-driven RL surpasses behavioral cloning from a powerful teacher model.

The framework scales consistently across model sizes: tested on Qwen-2.5 at 3B, 7B, and 14B, both PPO and GRPO variants outperform base models at every scale, showing that RL-based memory training is not capacity-dependent.

Memory-R1 generalizes zero-shot to two out-of-distribution benchmarks (MSC and LongMemEval) despite training exclusively on LoCoMo, with consistent gains across single-hop, multi-hop, open-domain, and temporal question types.

Ablation studies confirm that each component contributes independently: removing the RL-fine-tuned Memory Manager under PPO drops F1 from 41.0 to 34.5, BLEU-1 from 32.9 to 28.1, and J from 57.5 to 49.0; removing the RL-fine-tuned Answer Agent reduces F1 from 41.0 to 32.5 (PPO) and from 45.0 to 33.0 (GRPO).

Answer Agent gains compound with memory quality: pairing the GRPO-trained Answer Agent with a stronger GPT-4o-mini Memory Manager yields F1 gains of +19.72 versus +10.10 with the LLaMA-3.1-8B manager, showing that a better upstream memory state amplifies downstream answer quality.

Learned memory distillation achieves higher accuracy than a reranker-based baseline while incurring lower median and tail inference latency, representing a more favorable accuracy–latency trade-off.

GRPO converges faster than PPO in early training (attributed to grouped return normalization providing stronger early guidance), but both reach comparable final reward levels.

---

### Implications
Memory-R1 establishes RL as a viable and data-efficient training paradigm for LLM memory management, suggesting that explicit supervision of individual memory operations is unnecessary — outcome-based rewards on downstream task correctness are sufficient to induce structured memory behavior.

The two-agent decomposition (manager + answer a

## Key Claims

1. LLMs are fundamentally stateless, constrained by limited context windows that hinder long-horizon reasoning
2. Most existing external memory pipelines for LLMs are static and heuristic-driven, lacking a learned mechanism for deciding what to store, update, or retrieve
3. Memory-R1 uses two specialized RL-trained agents: a Memory Manager that learns structured operations (ADD, UPDATE, DELETE, NOOP) and an Answer Agent that pre-selects and reasons over relevant memory e
4. Memory-R1 achieves strong performance with only 152 training QA pairs
5. RAG-based memory retrieval creates a fundamental challenge where heuristics may return too few entries (omitting context) or too many (flooding with irrelevant information and degrading performance)
6. Existing memory-augmented LLM systems rely on vanilla LLMs to choose memory operations from in-context instructions without any learning signal tied to correctness
7. The Memory Manager's reward is outcome-driven: operations are judged by their effect on downstream QA using exact-match, requiring no manual labels
8. Memory-R1 is trained only on LoCoMo and evaluated zero-shot on MSC and LongMemEval, demonstrating cross-task generalization
9. Memory-R1-GRPO on LLaMA-3.1-8B outperforms MemoryOS by 28.5% F1, 34.0% B1, and 30.2% J on LoCoMo
10. RL-based Memory-R1 outperforms Memory-SFT which uses GPT-5-generated trajectories for supervised fine-tuning, demonstrating the superiority of outcome-driven optimization over imitation

## Capabilities

- LLM agents can learn structured memory operations (ADD, UPDATE, DELETE, NOOP) through outcome-driven RL with only 152 training QA pairs, outperforming heuristic baselines and SFT approaches using GPT-5-generated trajectories
- RL-trained Answer Agent can distill 60 retrieved memory candidates to the most relevant entries, achieving higher accuracy and lower inference latency than reranker-based pipelines
- Memory-augmented RL agents trained on one multi-session dialogue benchmark generalize zero-shot to distinct benchmarks without retraining, across all question types
- Outcome-driven RL (PPO/GRPO) surpasses supervised fine-tuning with GPT-5-generated trajectories for teaching memory management to LLM agents, demonstrating that reward-driven learning beats teacher imitation for agentic memory tasks
- GRPO-trained memory management achieves consistent gains across 3B, 7B, and 14B model scales, demonstrating that RL-based memory learning is scale-agnostic within the 3B–14B range

## Limitations

- LLMs are fundamentally stateless — their memory is bounded by a finite context window, and any information outside that window is forgotten, preventing knowledge maintenance across long conversations or evolving tasks
- Vanilla LLM memory systems misinterpret incremental user updates as contradictions, issuing destructive DELETE+ADD operations instead of UPDATE, fragmenting memory state
- Heuristic RAG retrieval flooding: returning too many entries floods the model with irrelevant content and degrades performance; returning too few omits crucial context — no adaptive mechanism exists to calibrate retrieval count
- Memory Manager and Answer Agent must be trained separately due to instability under sparse rewards — end-to-end joint multi-agent RL training is currently infeasible
- Exact-match reward produces balanced lexical metrics but discourages semantically correct verbose answers; LLM-as-judge reward maximizes semantic quality but degrades lexical metrics — no single reward function simultaneously optimizes both
- Answer Agent performance is ceiling-bounded by Memory Manager quality — gains from better answer reasoning are nearly double when paired with a stronger memory manager, meaning weak memory management cannot be compensated by reasoning improvements
- Initial RAG retrieval stage remains entirely heuristic (similarity-based); only distillation from the retrieved set is learned — the upstream retrieval quality bottleneck is unaddressed by RL training
- Evaluation is restricted to text-only, dialogue-centric benchmarks; multimodal memory management (images, audio, video) is explicitly out of scope and introduces unknown challenges
- GRPO exhibits faster initial convergence than PPO for memory management tasks but both converge to comparable final rewards — early training signal distribution advantage does not translate to sustained superiority

## Bottlenecks

- Memory management in LLM agents remains predominantly heuristic-driven — no standard learned mechanism exists for deciding what to store, update, or discard in external memory banks, limiting long-horizon agent reliability
- End-to-end joint RL training of multiple coordinated agents (e.g., memory manager + answer agent) is blocked by training instability under sparse outcome rewards — staged independent training is required, preventing rich inter-agent coordination
- No unified reward function simultaneously optimizes lexical accuracy and semantic quality for open-ended language generation tasks — forces researchers to choose between metric families, preventing holistic optimization

## Breakthroughs

- Memory-R1 establishes the first RL framework for learnable memory management in LLM agents, achieving state-of-the-art multi-session dialogue performance with only 152 training examples and zero-shot cross-benchmark generalization

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/a-mem|A-MEM]]
- [[entities/bleu-1|BLEU-1]]
- [[entities/exact-match|Exact Match]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/locomo|LoCoMo]]
- [[entities/longmemeval|LongMemEval]]
- [[entities/mem0|Mem0]]
- [[entities/memory-r1|Memory-R1]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
