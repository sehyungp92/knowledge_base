---
type: source
title: 'MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic
  Memory'
source_id: 01KJT28Q4KZZW7MKAEXCVXK7C0
source_type: paper
authors:
- Shengtao Zhang
- Jiaqian Wang
- Ruiwen Zhou
- Junwei Liao
- Yuchen Feng
- Zhuo Li
- Yujie Zheng
- Weinan Zhang
- Ying Wen
- Zhiyu Li
- Feiyu Xiong
- Yutao Qi
- Bo Tang
- Muning Wen
published_at: '2026-01-06 00:00:00'
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- knowledge_and_memory
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory

**Authors:** Shengtao Zhang, Jiaqian Wang, Ruiwen Zhou, Junwei Liao, Yuchen Feng, Zhuo Li, Yujie Zheng, Weinan Zhang, Ying Wen, Zhiyu Li, Feiyu Xiong, Yutao Qi, Bo Tang, Muning Wen
**Published:** 2026-01-06 00:00:00
**Type:** paper

## Analysis

# MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory
2026-01-06 · paper · Shengtao Zhang, Jiaqian Wang, Ruiwen Zhou, Junwei Liao, Yuchen Feng et al. (14 total)
https://arxiv.org/pdf/2601.03192

---

### Motivation & Prior Limitations
- Fine-tuning enables agents to internalize experience but is computationally expensive and causes catastrophic forgetting, making it unsuitable for post-deployment continuous improvement.
  - Weight-update methods (RLHF, DPO, rule-based RL) place all learning in model parameters, incurring online update costs and risking forgetting previously mastered tasks.
- Existing RAG and memory-based methods provide a non-parametric alternative but rely on passive semantic similarity matching, which cannot distinguish high-utility memories from semantically similar but functionally useless noise.
  - Standard cosine-similarity retrieval assumes "similar implies useful," but agentic tasks involve environment-specific routines that generalize poorly; the retrieval policy has no mechanism to learn from environmental feedback about which memories actually led to successful outcomes.
- No prior method achieves Runtime Continuous Learning — post-deployment self-improvement without backbone weight modification — while simultaneously solving the noise-filtering problem inherent to semantic retrieval.
  - Recent memory-augmented agents (MemP, Mem0, Reflexion) improve memory organization or add reflection, but the selection problem — identifying which experiences to reuse based on outcome utility — remains unaddressed without training additional parametric modules.

---

### Proposed Approach
- MEMRL decouples stable reasoning (frozen LLM) from plastic episodic memory, formalizing the interaction as a Memory-augmented Markov Decision Process (M-MDP) and applying non-parametric reinforcement learning directly to the memory retrieval policy rather than to model weights.
  - Unlike all prior parametric RL approaches to LLM improvement, MEMRL optimizes µ(m|s, M) — the retrieval policy — leaving the backbone entirely frozen, so the "learning" happens exclusively as updates to Q-values stored alongside memory entries.
  - Memory is structured as Intent-Experience-Utility triplets (z, e, Q), where Q_i approximates the expected return of applying experience e_i to intents similar to z_i, transforming retrieval from a passive lookup into a value-based decision.
- Two-Phase Retrieval separates semantic recall from value-aware selection: Phase A filters a candidate pool C(s) via cosine similarity above a sparsity threshold δ; Phase B re-ranks using a composite score `(1−λ)·sim + λ·Q` with z-score normalization, where λ = 0.5 is the empirically optimal balance.
  - This two-phase design explicitly targets "distractor" memories — those with high semantic similarity but low historical utility — which pure RAG systems cannot distinguish.
- Q-values are updated at runtime via a Monte Carlo-style rule (Q_new ← Q_old + α(r − Q_old)), treating each task interaction as a one-step MDP terminal; after each trajectory, an LLM summarizes the experience and writes a new triplet (z, e_new, Q_init) into the memory bank, enabling continual expansion without weight changes.
  - The authors prove under a frozen inference policy and stationary task distribution that Q-value estimates are unbiased and variance-bounded, converging to the true expected return; the system is further shown to converge via a Generalized EM framing where retrieval ranking is the E-step and utility update is the M-step, guaranteeing monotonic improvement.

---

### Results & Capabilities
- MEMRL outperforms the strongest baseline (MemP) by an average of +3.8% Cumulative Success Rate (CSR) across all benchmarks in the Runtime Learning setting over 10 epochs.
  - Gains are largest in exploration-intensive environments: ALFWorld (+6.2% CSR) and OS tasks (+6.2% CSR), reflecting that value-based filtering is most beneficial when many semantically similar but functionally distinct strategies exist.
  - On the hard knowledge-frontier benchmark HLE, MEMRL achieves 0.606 CSR vs. MemP's 0.570, a +3.6% gain, demonstrating value beyond structured procedural tasks.
- In Transfer Learning (frozen memory bank evaluated on held-out tasks), MEMRL exceeds MemP by +2.8% average Success Rate, with the largest margin on ALFWorld (+5.8%) and OS tasks (+2.6%), confirming that Two-Phase Retrieval selects procedural patterns that generalize rather than overfitting to seen task structure.
- MEMRL achieves the lowest Forgetting Rate of 0.041 (vs. MemP's 0.051), with the Epoch Success Rate and CSR curves remaining synchronized — unlike MemP, which shows a widening divergence between the two curves indicating catastrophic forgetting of previously solved tasks.
  - Ablation shows that removing z-score normalization and similarity gating spikes the forgetting rate to 0.073, isolating strict filtering as the mechanism that prevents utility variance from destabilizing self-evolution.
- Learned Q-values exhibit a Pearson r = 0.861 correlation with empirical task success rate, rising from 21.5% success in the lowest Q-bin (0.2–0.3) to 88.1% in the highest (0.9–1.0), validating that the critic accurately ranks memories by functional utility rather than surface similarity.
  - Approximately 12% of memories in high-Q bins (0.9–1.0) are failure memories, suggesting Q-values capture strategically useful near-misses and transferable procedural lessons rather than simply replaying successes.
- Cross-task retrieval accounts for most of MEMRL's gains in structured environments: ablating to single-task reflection reduces OS performance by 9.0% and ALFWorld by 5.1%, confirming that horizontal transfer of successful policies across semantically similar historical tasks is the primary driver in high-intra-dataset-similarity benchmarks.

---

### Implications
- MEMRL establishes a viable path for Runtime Continuous Learning — agents that improve thro

## Key Claims

1. Fine-tuning internalizes experience by modifying weights but suffers from computational costs and catastrophic forgetting.
2. Existing RAG-based memory methods retrieve by semantic similarity rather than utility, preventing agents from leveraging runtime feedback to distinguish high-value strategies from noise.
3. MEMRL is a non-parametric approach that enables agent self-evolution via reinforcement learning on episodic memory without modifying model weights.
4. MEMRL formalizes the interaction between a frozen LLM and external memory as a Markov Decision Process (MDP), optimizing the retrieval policy rather than backbone model weights.
5. MEMRL outperforms state-of-the-art baselines by an average of +3.8% in Cumulative Success Rate across all evaluated benchmarks.
6. MEMRL achieves the most significant performance gains over baselines in exploration-intensive environments like ALFWorld and OS tasks (+6.2% CSR each).
7. The Q-value adapts the traditional value function Q(s,a) to the retrieval phase, defining Q(s,m) as the expected utility of the subsequent action augmented by memory m.
8. Standard RAG systems assume 'similar implies useful,' but agentic tasks often involve environment-specific routines that generalize poorly.
9. A Q-weighting factor λ=0.5 achieves the optimal trade-off between semantic relevance and value-based exploitation; deviating toward either extreme degrades performance.
10. Learned Q-values exhibit a strong positive correlation (Pearson r=0.861) with empirical task success rates, confirming the critic's predictive power for ranking memories by success likelihood.

## Capabilities

- Non-parametric runtime learning via RL on episodic memory allows frozen LLMs to self-evolve post-deployment: Q-values are updated from environmental feedback without any weight modifications, yielding continuous task performance improvements over successive epochs.
- Value-aware memory retrieval using learned Q-values achieves Pearson r=0.861 correlation with downstream task success, enabling retrieval policies that distinguish high-utility memories from semantically similar but functionally useless noise.
- Cross-task episodic memory transfer enables agents to retrieve and apply procedural lessons from semantically similar historical tasks to novel unseen tasks, achieving up to +5.8% over strong baselines on complex navigation benchmarks.
- Frozen-backbone agents can maintain a low forgetting rate (0.041) across deployment epochs through non-parametric Q-value memory management, outperforming heuristic memory methods (MemP: 0.051) that exhibit catastrophic forgetting under continued operation.

## Limitations

- Step-wise Monte Carlo Q-value updates introduce high variance in long-horizon trajectories where delayed rewards must be attributed to individual memory retrievals — the one-step simplification loses temporal credit structure.
- Credit assignment is ambiguous when multiple memory items are jointly retrieved and contribute to an outcome: the scalar reward cannot be decomposed across co-retrieved experiences, producing biased Q-value estimates.
- Cross-task generalization collapses when task semantic similarity is low: on HLE (internal similarity score 0.186), MemRL performs no better than single-task reflection, completely eliminating the cross-task memory advantage.
- Industrial deployment requires high task density and hierarchical task abstraction: in sparse or highly heterogeneous task environments, insufficient similar experiences accumulate, causing performance to drift toward simple reflection behaviour.
- Retrieval bandwidth is highly sensitive: performance follows an inverted-U curve with k1/k2 — sparse settings under-provide guidance while dense settings flood context with distractors — requiring per-domain hyperparameter search.
- Theoretical stability guarantees require a stationary task distribution and frozen inference policy — assumptions that break in dynamic deployment environments with concept drift, policy fine-tuning, or shifting user behaviour.
- Memory security for deployed agents is unresolved: the paper flags adversarial memory injection and poisoning as an open concern in future work but provides no mechanisms to prevent malicious corruption of the memory bank.
- Q-value weighting factor λ must be carefully balanced: pure semantic retrieval (λ=0) plateaus due to inability to filter distractors, while pure Q-value exploitation (λ=1) induces volatility and context detachment — neither extreme generalises reliably.
- Multi-agent memory sharing is not addressed: the framework assumes a single-agent memory bank with no mechanism for pooling, merging, or selectively sharing learned memories across agents in collaborative or federated deployments.

## Bottlenecks

- Credit assignment across jointly retrieved memory items blocks accurate Q-value estimation: when multiple experiences co-contribute to an outcome, Monte Carlo updates cannot decompose attribution, producing systematically biased utility estimates that degrade retrieval quality at scale.
- Dependence on inter-task semantic similarity for memory candidate recall means non-parametric runtime learning degrades to reflection-only behaviour in low-similarity domains, blocking generalisation to diverse open-ended task distributions that characterise real-world deployment.
- Long-horizon credit assignment for episodic memory updates: one-step Monte Carlo utility updates cannot propagate delayed rewards through multi-step trajectories, introducing variance that blocks stable runtime learning in complex agentic tasks with extended action horizons.

## Breakthroughs

- Non-parametric RL on episodic memory reconciles the stability-plasticity dilemma, enabling LLM agents to continuously self-improve post-deployment with no weight updates — achieving +3.8% average CSR gain and +6.2% in exploration-heavy environments over the strongest memory baselines.

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/bigcodebench|BigCodeBench]]
- [[entities/humanitys-last-exam|Humanity's Last Exam]]
- [[entities/mem0|Mem0]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/stability-plasticity-dilemma|Stability-Plasticity Dilemma]]
