---
type: source
title: 'MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End
  Reinforcement Learning'
source_id: 01KJTBCNKDWMC8R13R057EH052
source_type: paper
authors:
- Qianhao Yuan
- Jie Lou
- Zichao Li
- Jiawei Chen
- Yaojie Lu
- Hongyu Lin
- Le Sun
- Debing Zhang
- Xianpei Han
published_at: '2025-11-04 00:00:00'
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning

**Authors:** Qianhao Yuan, Jie Lou, Zichao Li, Jiawei Chen, Yaojie Lu, Hongyu Lin, Le Sun, Debing Zhang, Xianpei Han
**Published:** 2025-11-04 00:00:00
**Type:** paper

## Analysis

# MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning
2025-11-04 · paper · Qianhao Yuan, Jie Lou, Zichao Li, Jiawei Chen, Yaojie Lu et al. (9 total)
https://arxiv.org/pdf/2511.02805

---

### Motivation & Prior Limitations
The dominant ReAct paradigm for search agents concatenates the entire interaction history into the LLM context at every turn, causing context length to grow nearly linearly with interaction depth, which drives computational cost up quadratically due to the O(n²) complexity of attention.
- Retrieved search passages introduce substantial noise into the growing context, compounding performance degradation as turn count increases.
- Prior work (Liu et al. 2023; Hsieh et al. 2024; Wu et al. 2024) shows LLMs exhibit large accuracy drops as context length grows and fail to reliably use information from long contexts, making unbounded context growth a hard scalability wall for multi-step retrieval agents.
- Using only the current turn sidesteps the cost problem but discards intermediate reasoning and retrieved facts, creating an accuracy cliff — neither design point is acceptable for complex knowledge-acquisition tasks.

---

### Proposed Approach
MemSearcher replaces the ever-growing interaction history with a bounded, iteratively rewritten natural-language memory object, keeping per-turn context length stable regardless of how many search rounds are executed.
- At each turn the LLM receives exactly two inputs — the original user question and the current memory (capped at a predefined token budget) — rather than the full trajectory; after each observation is returned, the same LLM also acts as a memory manager, rewriting memory to incorporate new findings while discarding irrelevant content.
- This dual role (reasoning/acting + memory management) is learned jointly end-to-end via a new training algorithm called **multi-context GRPO**, which extends vanilla GRPO to handle trajectories composed of multiple conversations operating under different context states: trajectory-level reward advantages are propagated back to every constituent conversation, and each conversation is then treated as an independent optimization target, enabling stable gradient estimation across the non-i.i.d. conversation segments that MemSearcher produces.
- Unlike SFT-based approaches (which require costly curated trajectories), multi-context GRPO trains purely from self-generated rollouts, jointly optimizing reasoning quality, search query formulation, and memory compression without separate training stages.

---

### Results & Capabilities
MemSearcher trained on Qwen2.5-3B-Instruct achieves an average relative improvement of +11% across seven public knowledge-acquisition benchmarks versus strong baselines, while the 7B variant achieves +12%, both trained on the identical dataset used by Search-R1.
- The 3B MemSearcher outperforms 7B ReAct-based baselines, indicating that context efficiency gains translate directly into accuracy gains rather than merely reducing cost.
- Context token counts remain nearly constant across interaction turns for MemSearcher agents, whereas ReAct-based agents show a near-linear growth in token counts — demonstrating that the memory compression mechanism successfully enforces the bounded-context invariant in practice.
- The efficiency benefit is multiplicative: lower per-turn token counts reduce both GPU memory pressure and the quadratic attention cost per turn, making longer multi-step reasoning chains tractable on smaller hardware.

---

### Implications
MemSearcher establishes that memory management is a learnable, RL-trainable skill rather than a hand-engineered heuristic, suggesting that compact working memory is a viable substitute for full context retention in agentic RAG pipelines.
- The multi-context GRPO algorithm generalises beyond search agents to any workflow where a single task decomposes into a sequence of conversations under shifting contexts, pointing toward a broader family of RL algorithms for stateful agents.
- The result that a 3B model with good context hygiene outperforms a 7B model with naive context growth has direct implications for deployment economics: capability can be recovered through architectural discipline rather than parameter scaling alone.
- For the memory-and-context theme, this work suggests that the long-context bottleneck in multi-turn reasoning agents may be addressable not by extending context windows but by training models to compress selectively — a different solution trajectory than current long-context pretraining investments.

---

### Remaining Limitations & Next Steps
The evaluation is restricted to knowledge-acquisition benchmarks where the answer can be verified as correct or incorrect, and the paper does not evaluate on tasks requiring multi-hop reasoning over structured data, long-document QA, or open-ended generation, leaving the generality of the memory management approach undemonstrated.
- The memory token budget is a predefined hyperparameter; the paper does not analyze sensitivity to this budget or how to set it optimally for tasks with varying information density.
- All experiments use Qwen2.5-Instruct base models; it is unclear whether the approach transfers to other model families or to models without strong instruction-following priors, since the memory-writing behavior may depend on instruction tuning quality.
- The paper is under review and explicitly notes the code and models are forthcoming, meaning reproducibility and external validation are not yet possible.
- An implicit limitation is that the LLM acting as its own memory manager creates a single point of failure: if the model misidentifies relevant information during a memory update, that error is irreversible within the trajectory, whereas ReAct at least retains the raw observation for potential re-use.

## Key Claims

1. ReAct-based search agents produce continuously growing LLM contexts because they concatenate all previous thoughts, actions, and observations at each turn.
2. The token count in ReAct-based search agents increases nearly linearly with the number of interaction turns.
3. The computational cost of ReAct-based search agents increases quadratically with the number of interaction turns because LLM computational complexity scales as O(n²) with token count.
4. LLMs do not reliably make use of information from long contexts.
5. LLMs exhibit large performance drops as context length increases.
6. LLMs show a significant accuracy drop on memorizing information across sustained multi-turn interactions.
7. In search agent contexts, retrieved passages often include substantial noise and information irrelevant to the user's question, further constraining the performance and scalability of ReAct-based agen
8. MemSearcher maintains nearly constant token counts in context across multi-turn interactions, unlike ReAct which grows linearly.
9. MemSearcher trained on Qwen2.5-3B-Instruct achieves +11% relative average improvement over strong baselines on seven public benchmarks.
10. MemSearcher trained on Qwen2.5-7B-Instruct achieves +12% relative average improvement over strong baselines on seven public benchmarks.

## Capabilities

- LLMs trained via end-to-end RL (multi-context GRPO) can jointly reason, issue search queries, and iteratively maintain a compact memory across multi-turn interactions — stabilising context length while improving accuracy over ReAct baselines
- Multi-context GRPO enables end-to-end RL training for agents whose trajectories span multiple conversations under different contexts — propagating trajectory-level advantages across all sub-conversations and treating each as an independent optimisation target
- A 3B-parameter search agent trained with memory-efficient RL can outperform 7B-parameter baselines on knowledge-acquisition benchmarks, demonstrating that memory management quality can substitute for raw parameter scale
- Multi-turn search agents can maintain nearly constant context token counts across arbitrary interaction turns by replacing full history concatenation with iteratively compressed natural-language memory

## Limitations

- Standard LLMs are not optimised for memory management roles and cannot reliably perform MemSearcher-style selective compression without explicit RL fine-tuning
- ReAct-based search agents incur quadratic computational cost growth with interaction turns because LLM computational complexity scales as O(n²) with token count, making long-horizon tasks prohibitively expensive
- LLMs do not reliably make use of information positioned in long contexts — performance degrades as context grows even when the relevant information is present
- LLMs show significant accuracy drops on memorising and utilising information across sustained multi-turn interactions, independently of context length effects
- Search engine observations are noisy and contain substantial irrelevant passages, which when concatenated into the context further degrades the performance and scalability of ReAct-style agents
- MemSearcher memory is bounded by a predefined maximum token length, creating a hard information capacity constraint — if accumulated essential information exceeds the cap, earlier relevant content will be discarded
- MemSearcher is evaluated exclusively on knowledge-acquisition benchmarks requiring factual lookup and reasoning — generalisability to tasks with different memory profiles (procedural tasks, long planning horizons, multi-party state) is undemonstrated
- MemSearcher requires RL training from scratch on each base model — there is no demonstrated transfer of trained memory management behaviour across model families or sizes without retraining
- Vanilla GRPO cannot handle multi-conversation trajectories — each MemSearcher trajectory spans multiple sub-conversations under different contexts, which breaks the standard single-trajectory advantage computation
- SFT-based alternatives to RL training for MemSearcher-style agents require costly, carefully curated high-quality trajectories that are difficult to obtain at scale — limiting the accessibility of this approach without RL
- The paper is under review and results have not been independently replicated — all quantitative gains (+11%, +12%) are preliminary and subject to revision

## Bottlenecks

- Standard multi-turn search agents using full history concatenation face quadratic computational scaling with interaction depth, blocking practical deployment on long-horizon reasoning tasks
- Standard RL algorithms (GRPO and variants) are designed for single-context trajectories and cannot natively optimise agents whose full trajectory spans multiple sub-conversations under different contexts

## Breakthroughs

- Multi-context GRPO enables a single end-to-end RL training loop to jointly optimise reasoning, tool-use search strategies, and memory management — previously believed to require separate training objectives or heuristic design

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/qwen25-3b-instruct|Qwen2.5-3B-Instruct]]
- [[entities/qwen25-7b-instruct|Qwen2.5-7B-Instruct]]
- [[entities/react|ReAct]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
