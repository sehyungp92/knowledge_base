---
type: source
title: 'IterResearch: Rethinking Long-Horizon Agents with Interaction Scaling'
source_id: 01KJTA1YHZ0D5ZR15PZD6AHT49
source_type: paper
authors:
- Guoxin Chen
- Zile Qiao
- Xuanzhong Chen
- Donglei Yu
- Haotian Xu
- Wayne Xin Zhao
- Ruihua Song
- Wenbiao Yin
- Huifeng Yin
- Liwen Zhang
- Kuan Li
- Minpeng Liao
- Yong Jiang
- Pengjun Xie
- Fei Huang
- Jingren Zhou
published_at: '2025-11-10 00:00:00'
theme_ids:
- agent_memory_systems
- agent_systems
- context_engineering
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# IterResearch: Rethinking Long-Horizon Agents with Interaction Scaling

**Authors:** Guoxin Chen, Zile Qiao, Xuanzhong Chen, Donglei Yu, Haotian Xu, Wayne Xin Zhao, Ruihua Song, Wenbiao Yin, Huifeng Yin, Liwen Zhang, Kuan Li, Minpeng Liao, Yong Jiang, Pengjun Xie, Fei Huang, Jingren Zhou
**Published:** 2025-11-10 00:00:00
**Type:** paper

## Analysis

# IterResearch: Rethinking Long-Horizon Agents with Interaction Scaling
2025-11-10 · paper · Guoxin Chen, Zile Qiao, Xuanzhong Chen, Donglei Yu, Haotian Xu et al. (16 total)
https://arxiv.org/pdf/2511.07327

---

### Motivation & Prior Limitations
- Deep-research agents that require sustained reasoning over external sources are fundamentally undermined by the dominant mono-contextual paradigm, which appends all retrieved information and intermediate steps to a single, continuously expanding context window.
  - **Context suffocation**: as the context fills with prior interactions, available space for model reasoning shrinks progressively, forcing increasingly constrained responses that degrade into premature or superficial conclusions.
  - **Noise contamination**: irrelevant web-search results and early exploration errors become permanently embedded in the context, creating cascading interference that dilutes reasoning quality for all subsequent steps.
  - Mono-contextual state size grows as O(t), making context overflow structurally inevitable and capping effective exploration at dozens of interactions — even increasing context window size does not resolve the underlying degradation (ablation shows mono-contextual agent with 64K context still trails IterResearch's 40K-context iterative agent by 12.6pp on average).

- Prior open-source deep-research agents (WebThinker, WebDancer, WebSailor, Asearcher, MiroThinker) all adopt the mono-contextual approach and exhibit significant performance gaps relative to proprietary systems such as OpenAI DeepResearch and Kimi-Researcher, particularly on long-horizon information-seeking tasks like BrowseComp.

---

### Proposed Approach
- IterResearch introduces an iterative deep-research paradigm modeled as a Markov Decision Process (MDP) with strategic workspace reconstruction, where each state contains only three components — the question, an evolving report serving as compressed memory, and the immediate context from the last interaction — keeping workspace size at O(1) regardless of trajectory length.
  - Unlike mono-contextual approaches that accumulate the full history, the transition function deliberately discards the historical trajectory at each round, preserving only synthesized knowledge in the evolving report; this enforces the Markov property and structurally prevents both context suffocation and noise propagation.
  - At each step, the agent generates a composite decision (Think, updated Report, Action), where the report update is produced naturally by the LLM as part of its structured output, leveraging the model's inherent compression and relevance-filtering capabilities without requiring explicit algorithmic summarization.

- To train the iterative paradigm, the authors develop Efficiency-Aware Policy Optimization (EAPO), which adapts geometric reward discounting so that agents reaching correct answers through fewer, more focused steps receive proportionally higher rewards than those that meander over many steps: r_t = γ^(T−t) · R_T with γ ∈ (0,1).
  - Because each trajectory naturally decomposes into independent per-round training samples (rather than one sample per trajectory as in mono-contextual RL), EAPO also employs adaptive downsampling — truncating the training corpus to the largest multiple of data-parallel size — preserving over 99% of samples while ensuring stable distributed training.
  - EAPO is implemented on top of Group Sequence Policy Optimization (GSPO) and trains a Qwen3-30B-A3B backbone through two stages: rejection sampling fine-tuning (RFT) to instill the iterative paradigm, followed by RL to sharpen search strategy and reasoning.

---

### Results & Capabilities
- IterResearch-30B-A3B achieves an average improvement of **+14.5 percentage points** over the best existing open-source agents across six benchmarks (HLE, BrowseComp, BrowseComp-zh, GAIA, Xbench-DeepSearch, SEAL-0), and surpasses OpenAI DeepResearch on HLE (28.8% vs. 26.6%) and BrowseComp-zh (45.2% vs. 42.9%) while remaining competitive on GAIA (72.8% vs. 67.4%) and BrowseComp (37.3% vs. 51.5%).
  - On the hardest information-seeking benchmarks (BrowseComp, BrowseComp-zh, SEAL-0), improvements over the next-best open-source agent (MiroThinker-32B) are +20.1pp, +15.8pp, and +18.9pp respectively — benchmarks where context accumulation is most destructive.

- The iterative paradigm unlocks **interaction scaling** as a previously infeasible axis of test-time compute: on BrowseComp (200-sample subset), performance rises from 3.5% at 2 maximum turns to 42.5% at 2048 maximum turns, operating throughout within a constant 40K token workspace.
  - Despite a budget of 2048 turns, the agent uses only 80.1 turns on average, with average turns growing sublinearly relative to the exponentially increasing budget — demonstrating adaptive termination rather than budget exhaustion, and suggesting the agent develops increasingly efficient search strategies.

- IterResearch functions as a **model-agnostic prompting strategy** without any training: replacing ReAct (mono-contextual) with the iterative paradigm improves o3 by +12.7pp on BrowseComp and DeepSeek-V3.1 by +19.2pp on BrowseComp, with consistent gains across all four evaluated benchmarks.
  - This zero-training transfer validates that the paradigm's benefits stem from a more effective cognitive structure for long-horizon reasoning, not from model-specific fine-tuning.

- A cross-paradigm knowledge transfer effect is observed: augmenting a mono-contextual agent's training data with trajectories generated by IterResearch (while holding total data volume constant) yields an average +5.4pp improvement across benchmarks, with gains up to +7.2pp on SEAL-0 and +6.7pp on HLE.
  - This indicates that the iterative paradigm induces superior exploration behaviors that produce higher-quality training signals partially transferable even to paradigmatically different agents.

- EAPO reduces average interactions by **5.7%** compared 

## Key Claims

1. The mono-contextual paradigm causes context suffocation as the context window fills with all prior interactions, forcing increasingly constrained responses that degrade into premature or superficial c
2. The mono-contextual paradigm causes noise contamination where irrelevant information from web searches and early exploration errors become permanently embedded in context, creating cascading interfere
3. IterResearch achieves an average improvement of 14.5 percentage points over existing open-source deep-research agents across six challenging benchmarks.
4. IterResearch as a prompting strategy improves frontier models by up to 19.2pp over the ReAct mono-contextual prompting paradigm on long-horizon tasks, without any training.
5. IterResearch maintains an O(1) constant workspace size regardless of trajectory length, enabling theoretically unbounded exploration steps.
6. Simply expanding the context window cannot resolve the fundamental workspace suffocation limitation of mono-contextual approaches.
7. Despite having access to 2048 maximum turns, IterResearch agents use only 80.1 turns on average, indicating adaptive termination once sufficient information is gathered.
8. IterResearch at 2048 interactions operates within a constant 40K token workspace, while mono-contextual agents at that interaction depth would face catastrophic context accumulation.
9. IterResearch (30B-A3B) surpasses OpenAI's DeepResearch on HLE and BrowseComp-zh benchmarks, achieving competitive or superior performance to frontier proprietary systems.
10. The perceived difficulty of long-horizon tasks may stem from insufficient exploration capacity rather than inherent task complexity.

## Capabilities

- Iterative deep-research paradigm (IterResearch) enables interaction scaling to 2048 turns with O(1) constant context size, achieving 42.5% on BrowseComp—up from 3.5% at 2 turns—while operating within a fixed 40K token workspace
- IterResearch applied as a zero-training prompting strategy improves frontier LLMs (o3, DeepSeek-V3.1) by up to 19.2pp over ReAct on long-horizon tasks, demonstrating model-agnostic benefits from iterative workspace reconstruction without any fine-tuning
- Open-source 30B MoE agent (IterResearch-30B-A3B) surpasses OpenAI DeepResearch on HLE (28.8% vs 26.6%) and BrowseComp-zh (45.2% vs 42.9%), closing the open-source to proprietary gap in autonomous deep research
- Cross-paradigm knowledge transfer: training data from iterative deep-research trajectories improves mono-contextual agents by 5.4pp average, demonstrating that superior exploration behaviours are distillable across architecturally incompatible paradigms
- MDP-inspired iterative workspace reconstruction maintains O(1) agent working memory across arbitrary exploration depths, replacing O(t) context accumulation with a periodically synthesised evolving report that acts as compressed long-term memory

## Limitations

- Mono-contextual deep-research agents suffer irreversible context suffocation: as the window fills with prior interactions, available reasoning space shrinks progressively, forcing premature or superficial conclusions
- Irrelevant information and early exploration errors become permanently embedded in mono-contextual agent context, creating cascading noise contamination that dilutes reasoning quality across the entire trajectory
- Deep-research RL training is limited to binary terminal-only reward (correct/incorrect final answer); no fine-grained feedback on individual search queries or intermediate reasoning steps is available
- Workspace reconstruction quality depends entirely on the LLM's inherent ability to synthesise and compress information into the evolving report — poor compression would cause permanent loss of critical information at each reconstruction step
- Expanding context windows cannot resolve mono-contextual degradation: a 64K context baseline still underperforms IterResearch (40K) by 12.6pp average, confirming a qualitative architectural ceiling independent of window size
- Per-interaction API and compute costs create a significant economic barrier for deep-research agents: agents using 80–130 average turns per query represent multiplicative cost increases over single-pass approaches
- Interaction scaling experiments were validated on a 200-sample subset of BrowseComp only; whether the same smooth scaling curve holds across other benchmarks and task types is unverified
- EAPO's geometric reward discounting only achieves 5.7% reduction in average interactions versus standard GSPO at comparable accuracy, suggesting minimal room for further efficiency gains through reward shaping alone
- The iterative paradigm achieves peak performance only after a two-stage training pipeline (RFT + RL); as a zero-shot prompting strategy, gains are real but smaller and may not match trained agent performance
- Variable sample counts per question in iterative RL training (each trajectory decomposes into multiple per-round samples) create distributed training instability requiring compensating engineering mechanisms

## Bottlenecks

- Linear O(t) context accumulation in mono-contextual deep-research agents imposes a hard ceiling on exploration depth: context suffocation and noise contamination cause performance degradation that no amount of context window expansion can resolve
- Absence of intermediate-step reward signals for deep research forces training on terminal-only binary rewards, severely limiting RL's ability to guide efficient exploration strategies across the long research trajectory
- Per-interaction inference and API costs create an economic deployment barrier for production deep-research agents that require dozens to over a hundred turns per query, limiting commercial viability

## Breakthroughs

- IterResearch demonstrates that interaction scaling — not context window scaling — is the correct axis for long-horizon deep-research performance: 42.5% on BrowseComp at 2048 interactions versus 3.5% at 2 interactions, all within a constant 40K token workspace
- Cross-paradigm knowledge transfer: iterative deep-research trajectories improve mono-contextual agents by 5.4pp average when used as training data, demonstrating that high-quality exploration behaviour is distillable across architecturally incompatible paradigms

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/agent_systems|agent_systems]]
- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]

## Key Concepts

- [[entities/gaia|GAIA]]
- [[entities/humanitys-last-exam|Humanity's Last Exam]]
- [[entities/rejection-sampling-fine-tuning|Rejection Sampling Fine-Tuning]]
