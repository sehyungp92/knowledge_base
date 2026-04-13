---
type: source
title: 'MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon
  Agents'
source_id: 01KJTNJCZNRC73ZRS71693XZBS
source_type: paper
authors:
- Zijian Zhou
- Ao Qu
- Zhaoxuan Wu
- Sunghwan Kim
- Alok Prakash
- Daniela Rus
- Jinhua Zhao
- Bryan Kian Hsiang Low
- Paul Pu Liang
published_at: '2025-06-18 00:00:00'
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
# MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents

**Authors:** Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, Paul Pu Liang
**Published:** 2025-06-18 00:00:00
**Type:** paper

## Analysis

# MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents
2025-06-18 00:00:00 · paper · Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash et al. (9 total)
https://arxiv.org/pdf/2506.15841

---

### Motivation & Prior Limitations
Full-context prompting — appending all past turns unconditionally — is the dominant memory strategy for multi-turn LLM agents, but it creates three compounding failure modes at scale that prior work has not resolved end-to-end.
- Memory and compute grow unboundedly with context length: Transformer KV-cache memory scales O(N) and attention compute scales O(N²), causing significant GPU memory waste when reserving headroom for long trajectories.
- Models fail to generalize beyond training-horizon lengths: contexts exceeding training distribution become out-of-distribution inputs, degrading reasoning reliability on longer tasks even when relevant information is technically present.
- Redundant context actively harms reasoning: accumulated irrelevant observations dilute attention and degrade performance even before OOD length is reached, as documented in multiple prior studies.
- Existing external-memory alternatives (retrieval modules, summarizers) are trained separately from the agent policy, creating a disconnect between memory and reasoning that cannot be optimized end-to-end, while also adding engineering overhead.
- RL-trained agent systems (e.g., Search-R1, DeepResearcher) that do train policies end-to-end leave memory management entirely unsolved, allowing prompt length to grow without bound during rollouts.
- Public benchmarks for long-horizon training are structurally insufficient: HotpotQA, Bamboogle, and 2wiki are labeled "multi-hop" but typically require only two information-seeking steps, providing inadequate signal for genuine long-horizon memory behavior.

---

### Proposed Approach
MEM1 (Memory-Efficient Mechanism via learning 1-step integrated reasoning and consolidation) is an end-to-end RL framework that trains a language agent to maintain a compact, bounded internal state across arbitrarily long multi-turn horizons by treating memory consolidation as an inseparable part of inference-time reasoning.

- At each turn, the agent generates a new `<IS>` (internal state) element that fuses prior memory with new observations, then prunes all tokens from the previous turn — retaining at most two `<IS>` elements, two `<query>` elements, and one `<info>` element in context at any time, resulting in near-constant peak token usage regardless of horizon length.
  - This differs fundamentally from external-memory approaches: no separate summarizer or retrieval module is introduced; the consolidation is learned entirely within the model's own generation process via a shared representational space.
  - The key design insight is that inference-time chain-of-thought reasoning already functions as working memory — MEM1 exploits this by forcing the `<IS>` token to carry both reasoning and memory roles simultaneously.
- Training uses PPO (Proximal Policy Optimization) with verifiable task-success rewards; memory efficiency is never explicitly rewarded but emerges as a learned behavior because tasks require retaining information across pruned contexts.
  - Starting from the Qwen2.5-7B Base model (not instruction-tuned) consistently outperformed SFT and instruction-tuned initialization, indicating RL from base is superior for this capability.
- Because the rollout context is dynamically updated rather than static, standard policy-gradient trajectory assumptions are violated; MEM1 resolves this with a masked trajectory approach that stitches multi-turn segments into a unified trajectory and applies a 2D attention mask restricting each token's attention to only the memory retained at its generation time, ensuring valid log-probability ratios for PPO updates.
- To produce training environments with sufficient horizon complexity, MEM1 introduces multi-objective task augmentation: existing single-hop and two-hop QA datasets (HotpotQA, Natural Questions) are composed into N-question sequential tasks, scaling compositional depth arbitrarily without requiring new data collection.

---

### Results & Capabilities
MEM1-7B achieves 3.5× better performance and 3.7× lower memory usage than Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task, while using only 27.1% of peak tokens and 29.3% of total inference time of that 14B baseline.

- On multi-objective QA scaling (2 → 16 objectives), MEM1's peak token usage remains nearly constant (6.40×10² at 2-obj, 10.4×10² at 16-obj), while all baselines scale near-linearly and several collapse to near-zero performance at high objective counts (Search-R1 EM drops to 0.009 at 16-obj; DeepResearcher drops to 0.071).
- On single-objective Wiki-RAG tasks, MEM1-QA (trained only on 2-objective compositions) achieves the highest EM score (0.405) among 7B-class models and comparable F1 to Qwen2.5-14B-Instruct (0.471 vs. 0.534), while using the fewest peak tokens (5.63×10²) and lowest dependency (0.76×10⁵).
- MEM1 zero-shot transfers to an unseen Online Web-QA environment, matching or exceeding DeepResearcher (which was specifically trained on that task) in both EM (0.397 vs. 0.372) and F1 (0.485 vs. 0.492), while using 56% fewer peak tokens.
- On WebShop navigation, MEM1-WebShop (7B) achieves an average final reward of 70.87 — matching AgentLM-13B (70.80, twice the parameters) — while using 2.8× fewer peak tokens, 1.9× lower dependency, and running 1.5× faster.
- Behavioral analysis reveals emergent capabilities not explicitly trained for: concurrent multi-question tracking with separate memory slots per objective, dynamic focus-shifting when one question stalls, self-verification with query correction, subgoal decomposition before search, and query re-scoping upon retrieval failure.
- SFT trained on GPT-4o-curated trajectories using the same rollout format substantially underperforms RL (0.302 EM vs. 0.405 EM 

## Key Claims

1. Most LLM systems rely on full-context prompting, appending all past turns regardless of relevance, leading to unbounded memory growth, increased computational costs, and degraded reasoning performance
2. MEM1-7B improves task performance by 3.5× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task.
3. MEM1-7B reduces memory usage by 3.7× compared to Qwen2.5-14B-Instruct on a 16-objective multi-hop QA task.
4. MEM1 generalizes beyond the training horizon, performing well on tasks with more objectives than seen during training.
5. Transformer-based LLMs incur O(N²) compute cost, or O(N) with Key-Value caching, and O(N) memory usage as context length N increases.
6. Long contexts cause context length to exceed training distribution, causing models to struggle with managing and reasoning over such unfamiliar long-horizon inputs.
7. Accumulation of irrelevant or redundant content in the context dilutes the model's attention, reducing its ability to reason effectively even when relevant information is present.
8. Recent progress in long-context modeling largely targets static inputs and does not address multi-turn interaction with external environments.
9. External memory modules such as summarizers or retrievers are typically trained separately and cannot be optimized end-to-end with the agent's policy.
10. Existing RL approaches for training LLM agents still rely on accumulating the full interaction history as memory, leaving memory management during training an underexplored area.

## Capabilities

- LLM agents trained end-to-end via RL can learn to maintain near-constant memory usage across arbitrarily long multi-turn horizons by consolidating reasoning and memory into a shared internal state — achieving 3.5× performance improvement while reducing memory 3.7× vs a 14B baseline
- RL training can induce memory-efficient agent behavior implicitly — without any explicit reward signal for memory efficiency — through verifiable task-completion rewards alone
- Existing single-objective QA datasets can be composed into arbitrarily complex multi-objective long-horizon training environments by interleaving questions into composite queries, enabling scalable agent training without new data collection
- Memory-efficient agents trained with RL on internal-retrieval tasks generalise zero-shot to unseen open-web search environments with improved efficiency and comparable accuracy
- A 7B RL-trained agent with constant memory outperforms a 14B instruction-tuned model on long-horizon multi-objective tasks, while using only 27% of peak tokens and 29% of inference time
- Emergent agentic behaviours — including self-verification, query decomposition, iterative search refinement, focus-shifting between stalled objectives, and query re-scoping on failure — arise from RL training on multi-objective tasks without explicit supervision for these behaviours
- A 7B RL-trained agent with constant-memory consolidation outperforms GPT-4o on web navigation (WebShop) tasks, even when GPT-4o uses truncation or external memory augmentation

## Limitations

- MEM1's RL training paradigm requires environments with well-defined, verifiable rewards; it cannot currently be applied to open-ended tasks where reward signals are ambiguous, sparse, delayed, or implicit
- Publicly available datasets for training long-horizon multi-turn interactive agents are extremely limited; existing multi-hop benchmarks (HotpotQA, Bamboogle, 2wiki) typically require only two reasoning steps and are not structured for memory-intensive multi-turn interaction
- Standard LLM agents with full-context prompting fail on interactions that exceed their training context distribution; context lengths beyond training horizon are out-of-distribution and degrade reasoning performance
- Baseline RL agents (Search-R1, DeepResearcher) completely collapse on tasks requiring 8–16 sequential objectives, with performance dropping to near-zero while context grows linearly — revealing a hard practical ceiling for full-context accumulation approaches
- External memory modules (RAG summarisers, vector retrievers) used in LLM agents are trained separately from agent policy and cannot be optimised end-to-end, creating a disconnect between memory retrieval and reasoning objectives
- Full-context prompting in multi-turn agents incurs O(N²) compute cost or O(N) with KV caching, with O(N) memory growth — making long-horizon deployment increasingly expensive and requiring large pre-reserved GPU memory
- Supervised fine-tuning on curated expert trajectories significantly underperforms RL training for long-horizon memory-consolidating agents, demonstrating that imitation learning cannot adequately teach memory management
- Existing RL approaches for training tool-using agents leave memory management entirely unsolved — all current RL agent training methods allow context to grow unboundedly, treating memory as outside the learned policy
- MEM1's dynamic context pruning disrupts the linearity assumption of standard policy gradient algorithms (PPO, REINFORCE++), requiring non-trivial masked trajectory reconstruction to compute valid token-level advantages
- MEM1 requires explicit meta-information injection (remaining turns budget hint) to avoid premature termination — revealing that agents cannot reliably self-track progress through long horizons without external scaffolding
- MEM1 initially underperforms larger instruction-tuned models (14B) at lower objective counts; efficiency and accuracy gains only materialise at longer horizons where context overload hurts baselines
- A-MEM (external vector memory) achieves high accuracy at 16 objectives but incurs 10× greater inference latency than MEM1, revealing that retrieval-augmented memory management trades speed for recall at long horizons

## Bottlenecks

- Absence of training environments and datasets supporting long-horizon multi-turn agent interaction — existing multi-hop benchmarks cover only 2 reasoning steps and lack the compositional complexity needed to train agents on realistic memory-intensive tasks
- Designing reward mechanisms for open-ended agentic tasks with ambiguous or noisy outcomes blocks application of RL-based memory consolidation training beyond narrow verifiable domains (QA, math, web navigation)
- Linear context accumulation in standard RL-trained agents imposes a hard practical ceiling on long-horizon performance: as task length grows, peak token usage scales linearly and models eventually collapse, regardless of model size

## Breakthroughs

- MEM1 demonstrates that end-to-end RL training can teach LLM agents to consolidate memory as an emergent part of their reasoning policy — achieving near-constant memory usage across arbitrarily long horizons without separate memory modules, architectural changes, or explicit memory rewards

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/a-mem|A-MEM]]
- [[entities/exact-match-em|Exact Match (EM)]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/mem1|MEM1]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/webshop|WebShop]]
