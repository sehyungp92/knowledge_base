---
type: source
title: 'MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent'
source_id: 01KJTNTHTPSNR70SSEDMC3Y2CZ
source_type: paper
authors:
- Hongli Yu
- Tinghong Chen
- Jiangtao Feng
- Jiangjie Chen
- Weinan Dai
- Qiying Yu
- Ya-Qin Zhang
- Wei-Ying Ma
- Jingjing Liu
- Mingxuan Wang
- Hao Zhou
published_at: '2025-07-03 00:00:00'
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

**Authors:** Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, Hao Zhou
**Published:** 2025-07-03 00:00:00
**Type:** paper

## Analysis

# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent
2025-07-03 00:00:00 · paper · Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai et al. (11 total)
https://arxiv.org/pdf/2507.02259

---

### Motivation & Prior Limitations
Existing long-context LLM approaches fail to simultaneously achieve unbounded input length, lossless performance extrapolation, and linear computational complexity — no prior method satisfies all three requirements.
- Length extrapolation methods (NTK, PI, YaRN, DCA) modify positional embeddings and extend context via continued pretraining, but suffer performance degradation and O(n²) attention cost at extreme lengths.
- Sparse and linear attention mechanisms (SSMs, RNNs, sliding-window attention) achieve O(N) complexity but require training from scratch, with linear attention facing parallel training difficulties and sparse attention relying on human-defined heuristics rather than learned patterns.
- Context compression approaches condense information at the token or memory-plugin level but struggle with extrapolation and require additional modules that disrupt standard generation, harming compatibility and parallelization.
- Multi-turn RL agent training (Search-R1, Agent-R1, RAGEN, GiGPO) handles tool-use trajectories by concatenating or sliding-window over interleaved observations and replies, making these methods inapplicable to more general agent workflows with context-independent conversations.

---

### Proposed Approach
MemAgent introduces an RL-trained agent workflow in which an LLM processes arbitrarily long documents by reading fixed-size chunks sequentially and overwriting a fixed-length memory token buffer after each chunk, enabling O(N) end-to-end inference without any architectural modification to the base model.
- The memory is a plain token sequence inside the standard context window, so positional embeddings are never rescaled or patched; the same attention layout applies throughout, allowing latent length-extrapolation capability to emerge naturally from RL training rather than architectural surgery.
- The overwrite strategy is deliberately simple: after reading each chunk the model replaces the entire previous memory with an updated one, keeping memory length constant and thus total compute per chunk O(1); the agent is rewarded for retaining answer-critical information and discarding distractors.
- Inference decomposes into a Context-Processing module (iterative chunk reading with memory updates, using a structured prompt template) and an Answer-Generation module (final answer produced from memory + question only), with no long raw text ever present at answer time.
- Training is handled by Multi-Conv DAPO, a novel extension of the DAPO/GRPO RL algorithm that treats each context-independent conversation in a multi-conversation rollout as a separate optimization target, distributing group-normalized advantages (computed from the final answer conversation) uniformly across all associated conversations; the loss is extended from (group, token) to (group, conversation, token) dimensionality, following DrGRPO's no-std-normalization design.
- This multi-conversation formulation contrasts with prior multi-turn RL approaches that apply attention masking over concatenated tool-response trajectories — a technique that does not generalize to independent-context workflows.

---

### Results & Capabilities
RL-MemAgent achieves near-lossless extrapolation from an 8K training context to documents up to 3.5 million tokens on RULER-HotpotQA, with performance loss under 5%, while all baseline long-context models exhibit substantial degradation at extreme lengths.
- RL-MemAgent-14B and RL-MemAgent-7B maintain consistent accuracy from 7K through 3.5M tokens on RULER-HotpotQA, outperforming QwenLong-L1-32B, Qwen2.5-Instruct-14B-1M, and DeepSeek-Distill-Qwen variants (7B/14B/32B) which all degrade significantly at lengths beyond their training window.
- The model achieves 95%+ accuracy on the 512K RULER benchmark despite being trained on 32K-token documents with only an 8K context window (1024-token memory, 5000-token document chunks).
- Computational cost scales strictly linearly with input length because the context window size is fixed (memory length never grows), making MemAgent practical for book-length or agent-session-length inputs.

---

### Implications
MemAgent demonstrates that end-to-end RL optimization — rather than architectural modification or continued pretraining — is a viable and potentially superior path to long-context capability, suggesting that the bottleneck of extreme-length processing may be a training objective problem as much as an architectural one.
- The result that an 8K-context model generalizes to 3.5M-token tasks implies that the critical skill being learned is selective compression, not positional encoding range — reframing the long-context problem in terms of memory management policy rather than attention span.
- For the RLHF/reward modeling and RL-for-LLM communities, Multi-Conv DAPO establishes a general framework for optimizing agent workflows with context-independent conversations, potentially enabling RL training of more complex agentic pipelines beyond long-document QA.
- For the transformer alternatives community, MemAgent shows that a standard transformer with fixed context can match or exceed recurrent/SSM architectures on long-range tasks when given a learned memory policy — challenging the assumption that architectural recurrence is necessary for linear-complexity long-context processing.
- Practically, the approach converts any moderately-capable LLM into an efficient long-context reasoner with minimal engineering overhead, lowering the barrier to deploying strong long-context agents without specialized hardware or model redesign.

---

### Remaining Limitations & Next Steps
The evaluation is heavily centered on extractive QA tasks (RULER-HotpotQA), and it is not demonstrated whether

## Key Claims

1. Handling infinitely long documents with linear complexity without performance degradation during extrapolation remains the ultimate challenge in long-text processing, despite improvements by length ex
2. MemAgent can extrapolate from an 8K context trained on 32K text to a 3.5M token QA task with performance loss less than 5%.
3. MemAgent achieves 95%+ accuracy on the 512K RULER benchmark.
4. Length extrapolation methods suffer from performance degradation and slow processing speed due to O(n²) computational complexity when applied to extremely long text.
5. Linear attention mechanisms require training from scratch and face difficulties in parallel training, while sparse attention depends on human-defined patterns.
6. Context compression approaches struggle with extrapolation and disrupt the standard generation process by requiring additional modules, hindering compatibility and parallelization.
7. Models that employ long-context continual pretraining and extrapolation techniques fail to maintain consistent performance across increasing context lengths.
8. MemAgent's overwrite strategy keeps memory length fixed, so total compute per chunk is O(1) and end-to-end complexity is strictly linear in the number of chunks.
9. MemAgent represents memory as ordinary tokens inside the context window, leaving the core generation process of the base LLM unchanged.
10. MemAgent does not re-scale or patch positional embeddings, which unlocks latent length-extrapolation capability without any architectural modifications.

## Capabilities

- RL-trained memory agent (MemAgent) with 8K context window extrapolates to handle 4-million-token QA tasks with <5% performance loss and linear O(N) compute cost, trained only on 32K documents
- Fixed-length overwrite memory strategy achieves O(1) compute per chunk and strictly O(N) end-to-end complexity for arbitrarily long documents, requiring no positional embedding modification or architectural change to the base LLM
- Multi-conversation DAPO (Multi-conv DAPO) algorithm enables end-to-end RL optimization of agent workflows composed of multiple independent conversation contexts, treating each context segment as a separate optimization target with shared outcome reward
- RL-trained LLMs learn to selectively compress and overwrite a fixed memory buffer, retaining answer-critical facts and discarding distractors, achieving 95%+ accuracy on 512K RULER benchmark with 7B and 14B models

## Limitations

- All existing long-context approaches simultaneously fail on at least one of three requirements: unlimited length, no performance degradation, and linear compute complexity
- Even state-of-the-art long-context models with continual pretraining (QwenLong-L1-32B, DS-Distill variants up to 32B) show sharp performance degradation beyond ~512K tokens
- MemAgent's overwrite strategy causes permanent information loss — content not retained in the fixed-length memory is irrecoverably discarded; the model must learn to predict future relevance at compression time
- MemAgent evaluation is restricted entirely to QA tasks; performance on summarization, instruction following, multi-step agentic execution, and code tasks over long inputs is not demonstrated
- Sequential chunk-by-chunk processing creates inference latency proportional to document length — multiple memory update passes before final answer generation prevent parallel document processing
- Training multi-turn agentic RL with independent conversation contexts is largely unexplored territory; existing tools (trajectory concatenation, sliding window) lack flexibility and do not generalize to arbitrary agent workflows
- Linear attention and SSM architectures require training from scratch and face parallelism difficulties during training, while sparse attention depends on predefined heuristic patterns rather than learned dynamic sparsity
- Context compression methods that integrate external memory modules disrupt standard autoregressive generation, preventing parallelization and breaking compatibility with standard serving infrastructure
- MemAgent performance is validated primarily on RULER-HotpotQA, a retrieval-focused multi-hop benchmark; generalization to tasks requiring holistic integration of distributed meaning across the full document is undemonstrated

## Bottlenecks

- Infinite-length document processing with all three properties simultaneously — (1) no performance degradation, (2) linear compute complexity, (3) no architectural modification to the base LLM — remains unmet by all prior approaches before MemAgent
- End-to-end RL optimization of agent workflows composed of multiple independent conversation contexts — standard gradient algorithms assume a single trajectory and cannot natively handle workflows where each sub-task runs in an isolated context

## Breakthroughs

- MemAgent achieves near-lossless length extrapolation at 125x training scale: a model trained on 32K documents with 8K context attains <5% performance loss on 4M-token QA tasks with strictly linear compute — without any positional embedding modification
- Multi-conversation DAPO enables end-to-end RL optimization of agent workflows with independent context segments by treating each conversation as a separate optimization target sharing a single outcome reward — going beyond all prior concatenation and sliding-window approaches

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/linear-attention|Linear Attention]]
- [[entities/ppo|PPO]]
- [[entities/rlvr|RLVR]]
- [[entities/state-space-models|State Space Models]]
