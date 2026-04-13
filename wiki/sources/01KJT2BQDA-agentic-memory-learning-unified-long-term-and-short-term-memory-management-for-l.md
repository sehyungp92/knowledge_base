---
type: source
title: 'Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management
  for Large Language Model Agents'
source_id: 01KJT2BQDAZRR1WQEM8WCGD2Y8
source_type: paper
authors:
- Yi Yu
- Liuyi Yao
- Yuexiang Xie
- Qingquan Tan
- Jiaqi Feng
- Yaliang Li
- Libing Wu
published_at: '2026-01-05 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents

**Authors:** Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, Libing Wu
**Published:** 2026-01-05 00:00:00
**Type:** paper

## Analysis

# Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents
2026-01-05 · paper · Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng et al. (7 total)
https://arxiv.org/pdf/2601.01885

---

### Motivation & Prior Limitations
LLM agents operating on long-horizon tasks are fundamentally constrained by finite context windows, making memory management critical — yet existing methods treat long-term memory (LTM) and short-term memory (STM) as independent, loosely coupled components optimized in isolation and combined ad hoc.
- STM management via RAG (e.g., MainRAG, ReSum) relies on predefined retrieval schedules or periodic summarization heuristics, which risks overlooking infrequent but critical details or introducing irrelevant noise, and does not prevent context explosion in long-horizon settings.
- LTM systems (LangMem, A-Mem, Mem0, Zep) are split between trigger-based approaches using fixed memory operations at predefined moments and agent-based approaches using auxiliary expert LLMs as memory managers — both depend on handcrafted rules or external models, increasing system complexity and limiting adaptability.
- End-to-end RL optimization of memory is blocked by three compounding challenges: (C1) functional heterogeneity between LTM and STM, (C2) training paradigm mismatch between the two memory types and the fragmented/discontinuous experience structure produced by memory operations, and (C3) the deployment cost of relying on auxiliary expert LLMs for memory control.

---

### Proposed Approach
AgeMem (Agentic Memory) is a unified framework that integrates both LTM and STM management directly into the agent's policy as tool-based actions, replacing external heuristic pipelines with a single end-to-end learnable mechanism.
- The agent is given six explicit tools — ADD, UPDATE, DELETE (targeting LTM) and RETRIEVE, SUMMARY, FILTER (targeting STM) — and autonomously decides when and how to invoke each, rather than relying on a separate memory manager or scheduler.
- Training uses a three-stage progressive RL strategy: Stage 1 trains LTM construction from casual context; Stage 2 resets STM and trains proactive STM filtering under semantic distractors while retaining the constructed LTM; Stage 3 requires coordinated retrieval and reasoning from both memory systems to answer a query. This staged-but-continuous trajectory structure forces the agent to learn proper LTM storage and retrieval rather than exploiting residual context.
- To handle sparse and discontinuous rewards across stages, the paper introduces step-wise GRPO: terminal task rewards are group-normalized into advantages and broadcast uniformly to all preceding steps in the trajectory, enabling long-range credit assignment from final task outcome back to early-stage memory decisions. The composite reward R(τ) combines Rtask (LLM-judged answer correctness), Rcontext (compression efficiency, preventive actions, information preservation), and Rmemory (storage quality, maintenance, semantic relevance of retrieved memories), plus penalty terms for context overflow and turn-limit violations.

---

### Results & Capabilities
AgeMem achieves the highest average performance across all five long-horizon benchmarks (ALFWorld, SciWorld, PDDL, BabyAI, HotpotQA) on both tested backbones, with average scores of 41.96% on Qwen2.5-7B-Instruct and 54.31% on Qwen3-4B-Instruct.
- Relative to a no-memory baseline, AgeMem improves by 49.59% and 23.52% respectively; compared to the best individual baselines (Mem0, A-Mem), gains are 4.82 and 8.57 percentage points on average. RL training alone over AgeMem-noRL contributes approximately 8.5–8.7 percentage points of improvement.
- Memory quality (MQ), measured by LLM-judged relevance between stored memories and ground-truth facts on HotpotQA, reaches 0.533 (Qwen2.5-7B) and 0.605 (Qwen3-4B), outperforming all baselines including the best competitor Mem0 (0.527 / 0.543), demonstrating that unified management promotes more selective, higher-quality knowledge storage.
- Learned STM tools reduce average prompt token usage compared to RAG-based STM: 3.1% reduction on Qwen2.5-7B (2,117 vs. 2,186 tokens) and 5.1% on Qwen3-4B (2,191 vs. 2,310 tokens), while maintaining or improving task performance — validating that adaptive context control achieves a better efficiency-retention tradeoff than static retrieval.
- RL fine-tuning shifts tool usage toward more proactive and balanced memory management: ADD operations nearly double on Qwen2.5-7B (0.92→1.64), UPDATE and DELETE operations emerge from near-zero, and FILTER calls increase substantially (0.02→0.31), indicating that RL teaches qualitatively different memory behavior rather than merely amplifying existing patterns.
- Ablation confirms that all three components (LTM, STM, RL) contribute additively: on SciWorld, +LT alone gives +14.2%, adding RL gives +18.7%, and adding STM tools gives +21.7% over the no-memory baseline. The full reward function converges faster and achieves higher final performance (J=0.544, MQ=0.533) than an answer-only reward variant (J=0.509, MQ=0.479).

---

### Implications
AgeMem establishes a proof-of-concept that unified, learnable memory policies trained end-to-end via RL can outperform modular, heuristic-driven architectures — suggesting that the sharp boundary between LTM and STM systems in agent design may be an artificial constraint that should be dissolved at the policy level.
- The step-wise GRPO mechanism addresses a fundamental training challenge (sparse, discontinuous rewards from memory operations) that is broadly applicable beyond this specific system — any RL-trained agent with heterogeneous tool-use steps could benefit from broadcasting terminal-step advantages across trajectory stages.
- For personal assistant and long-context agent applications, the result that adaptive memory management produces measurable token reduction without performance loss points toward a practi

## Key Claims

1. LLM agents face fundamental limitations in long-horizon reasoning due to finite context windows, making effective memory management critical.
2. RAG-based STM methods rely on predefined schedules or heuristic rules, potentially resulting in overlooked infrequent but critical details as well as unnecessary noise.
3. Trigger-based LTM executes fixed memory operations at predefined moments, offering limited flexibility.
4. Agent-based LTM approaches still depend on handcrafted rules or auxiliary expert models, limiting adaptability and increasing system complexity.
5. Standard RL assumes continuous trajectories with stable rewards, which conflicts with the inherently fragmented and discontinuous experiences produced by memory operations.
6. Many agent systems rely on an auxiliary expert LLM for memory control, significantly increasing inference cost and training complexity.
7. AgeMem uses a three-stage progressive RL strategy where the model first acquires LTM storage capabilities, then learns STM context management, and finally coordinates both memory types under full task
8. ReSum periodically compresses interaction histories into compact reasoning states but its summarization schedule remains predefined and aggressive compression risks discarding rare but crucial details
9. Existing RL-based systems generally treat memory as a static or external component, making them ill-suited for the discontinuous and fragmented trajectories associated with memory operations.
10. AgeMem's agent state at each step is composed of the conversation context (short-term memory), the long-term memory store, and the task specification.

## Capabilities

- LLM agents can learn to autonomously manage both long-term and short-term memory through RL-trained tool-based actions (ADD, UPDATE, DELETE, RETRIEVE, SUMMARY, FILTER), without relying on heuristics or separate auxiliary controllers
- Step-wise GRPO broadcasts terminal task rewards back to all preceding memory decisions across multi-stage discontinuous trajectories, enabling long-range credit assignment for memory operations in RL training
- Unified memory management with three-stage progressive RL achieves 49.59% and 23.52% relative gains over no-memory agents on long-horizon benchmarks across 7B and 4B model backbones, outperforming best heuristic baselines by 4.82–8.57 percentage points

## Limitations

- AgeMem exposes only a fixed set of 6 memory operations, limiting fine-grained control over memory granularity
- Evaluation is confined to five structured academic benchmarks with closed answer spaces; performance on open-ended real-world agentic tasks is entirely unstated
- All experiments are conducted exclusively on small open-source models (Qwen2.5-7B, Qwen3-4B); no validation on frontier or API-only models means scalability of the approach is unverified
- Standard RL training fails for memory-augmented agents because memory operations produce sparse, discontinuous rewards across multi-stage trajectories that violate continuous-trajectory assumptions
- RAG-based STM enhancement does not prevent context explosion in long-horizon settings; it only expands usable context by appending retrieved content without managing total context growth
- Learned STM tools achieve only 3.1–5.1% token reduction compared to RAG-based approaches, indicating the context efficiency gains from learned memory management are marginal at current task lengths
- LTM quality scores peak at 0.533–0.605 out of 1.0, meaning even the best unified memory system frequently stores irrelevant or low-quality memories
- Existing LTM systems (Mem0, A-Mem, LangMem) rely on predefined memory structures and heuristic update rules; as memory grows they suffer from increasing complexity and inability to adaptively prioritize or forget
- Predefined summarization schedules in STM compression systems (e.g., ReSum) risk discarding rare but critical details through aggressive compression triggered at the wrong time
- Systems using an auxiliary expert LLM as a dedicated memory controller incur substantially higher inference cost and training complexity than single-model solutions

## Bottlenecks

- Standard RL algorithms cannot be directly applied to memory-augmented agent training because memory operations produce fragmented, discontinuous trajectory experiences with sparse cross-stage rewards that violate continuous-trajectory assumptions
- LTM and STM are independently designed and optimized across the field, with no framework for coordinating their interplay — yielding fragmented memory construction and suboptimal long-horizon agent performance

## Breakthroughs

- First demonstration that unified long-term and short-term memory management for LLM agents can be learned end-to-end via reinforcement learning, replacing heuristic pipelines and auxiliary memory controllers with a single trained policy

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/a-mem|A-MEM]]
- [[entities/alfworld|ALFWorld]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/mem0|Mem0]]
- [[entities/sciworld|SciWorld]]
- [[entities/zep|Zep]]
