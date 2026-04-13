---
type: source
title: Multi-Agent Collaboration via Evolving Orchestration
source_id: 01KJTCTNJHDZHQFAWFM2JDEDJK
source_type: paper
authors:
- Yufan Dang
- Chen Qian
- Xueheng Luo
- Jingru Fan
- Zihao Xie
- Ruijie Shi
- Weize Chen
- Cheng Yang
- Xiaoyin Che
- Ye Tian
- Xuantang Xiong
- Lei Han
- Zhiyuan Liu
- Maosong Sun
published_at: '2025-05-26 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Multi-Agent Collaboration via Evolving Orchestration

**Authors:** Yufan Dang, Chen Qian, Xueheng Luo, Jingru Fan, Zihao Xie, Ruijie Shi, Weize Chen, Cheng Yang, Xiaoyin Che, Ye Tian, Xuantang Xiong, Lei Han, Zhiyuan Liu, Maosong Sun
**Published:** 2025-05-26 00:00:00
**Type:** paper

## Analysis

# Multi-Agent Collaboration via Evolving Orchestration
2025-05-26 · paper · Yufan Dang, Chen Qian, Xueheng Luo, Jingru Fan, Zihao Xie et al. (14 total)
https://arxiv.org/pdf/2505.19591

---

### Motivation & Prior Limitations
Static organizational structures in existing multi-agent systems cannot adapt as task complexity and agent count grow, producing coordination overhead that degrades performance and wastes compute.
- Prior work (MacNet, EvoAgent, GPT-Swarm) relied on predefined or statically generated agent topologies — directed acyclic graphs, chains, trees — that lock in collaboration structure before reasoning begins, preventing feedback and iterative refinement.
  - MacNet with 50-node mesh structures required up to 10 hours to develop software of only a few hundred lines, illustrating that static large-scale MAS does not scale gracefully.
- When agents autonomously select collaborators without centralized coordination, the combinatorial topology search space is intractable, so prior methods constrained themselves to canonical graph shapes (chains, trees, DAGs) that miss richer interaction patterns.
- Performance gains from agent collaboration in non-learnable systems came at the cost of increased token consumption, creating an accuracy–efficiency trade-off that prior work did not resolve.

---

### Proposed Approach
The paper introduces Puppeteer, a puppeteer-style multi-agent framework where a single centralized orchestrator — a learnable policy — dynamically selects which agent to activate at each reasoning step, treating the full collaboration as a sequential Markov decision process optimized via reinforcement learning.

- The orchestrator serializes what would otherwise be an intractable topology search: rather than searching over all possible directed graphs, it "unfolds" collaboration into a time-ordered sequence of agent activations, which can be "folded back" into a directed graph post-hoc (agents as nodes, activation order as edges), covering chains, trees, and cyclic graph topologies without enumerating them.
  - This differs from MacNet (static DAG) and EvoAgent (evolutionary search over fixed structures) by making topology an emergent property of sequential decisions rather than a design choice.
  - The Markov property of the state transition (`P(a_{t+1} | S_{t+1}, τ)`) enables gradient-based policy optimization via REINFORCE without needing to model long-range dependencies explicitly.

- The reward function jointly optimizes solution quality and computational efficiency: at the terminal step the reward combines correctness `r ∈ {0,1}` (or quality `r ∈ [0,1]` for open tasks) with a cumulative cost penalty `λ · C_T`, where per-step cost `C_t = F · log(1 + t/φ)` grows logarithmically with step count, incentivizing early termination and agent pruning.
  - The trade-off weight `λ` is tunable: higher `λ` sacrifices some accuracy for greater token savings; setting `λ = 0` degenerates the system toward a traditional large-scale collaborative framework with maximum performance but no efficiency pressure.

- Agents are defined as triples `(model, reasoning_pattern, tool_set)`, with reasoning patterns including task decomposition, reflection, refinement, critique, modification, summarization, and termination, plus external tools (WebViewer, WikiSearch, BingSearch, Code Interpreter, File Reader), making the agent space heterogeneous and modular.

---

### Results & Capabilities
Puppeteer in its evolved phase consistently achieves the best average performance across all four evaluated datasets in both the Titan (large-model) and Mimas (small-model) subspaces, while simultaneously reducing token consumption over the course of RL training.

- In the Titan subspace, evolved Puppeteer reaches an average score of 0.7731 across GSM-Hard, MMLU-Pro, SRDD, and CommonGen-Hard, up from 0.6893 at initialization — a gain of ~12% — outperforming all baselines including AFlow (0.6899) and Self-Refine (0.6157) using the same base models.
- In the Mimas subspace, evolved Puppeteer reaches 0.6324 average versus initialized 0.6273, while Puppeteer-Mono (single model, Llama-3.1-8B) improves more substantially from 0.5068 to 0.6147, confirming that RL-driven evolution benefits both heterogeneous and homogeneous agent pools.
- Token consumption decreases monotonically across training in nearly all settings, demonstrating that performance and efficiency improve simultaneously — not at each other's expense — which is a direct contradiction of the trade-off observed in static MAS literature.

- Structural analysis reveals two emergent phenomena as the orchestrator evolves: **compaction** (graph density rises from avg. 1.08 to 1.45) and **cyclicality** (cycle count per graph increases, with length-2 cycles growing from avg. 1.17 to 1.40), shifting the topology from diffuse exploratory chains to tightly coupled cyclic subnetworks centered on a small cohort of "hub" agents.
  - In the Titan subspace, the number of active agents per task decreases over training (earlier termination), while in Mimas it stays stable (weak agents require longer chains), with efficiency gains in Mimas coming instead from preferential selection of lower-cost agents.

- Topology hyperparameters (chain depth D, exploration width W) exhibit a non-monotonic relationship with accuracy: the default W4D2 setting achieves the best accuracy–efficiency trade-off, and increasing either depth or width introduces redundancy and performance degradation.

---

### Implications
Treating multi-agent collaboration as a sequential MDP and learning the orchestration policy via RL establishes a principled pathway for making MAS topology itself an optimizable variable, which could substantially reduce the manual engineering burden of designing agent workflows.

- The emergence of compact cyclic topologies as the optimal learned structure suggests that iterative self-referential reasoning (mutual verification, recursive critique) is not merely a desig

## Key Claims

1. Monolithic LLMs restrict scalability and efficiency in complex problem-solving
2. Most existing multi-agent approaches rely on static organizational structures that struggle to adapt as task complexity and agent numbers grow
3. Mesh-structured multi-agent systems with 50 nodes can require up to 10 hours to develop software comprising only a few hundred lines of code
4. Prior multi-agent approaches where each agent autonomously selects collaborators incur coordination overhead and poor scalability as agents increase or change
5. The Puppeteer framework uses a centralized orchestrator trained via reinforcement learning to adaptively sequence and prioritize agents
6. Multi-agent collaboration is formalized as a sequential decision process governed by a centralized policy that selects agents based on the Markov property
7. Serializing the collaborative reasoning process avoids exhaustive topological search by unfolding the graph into a reasoning sequence guided by topological traversal
8. REINFORCE is used as the underlying policy optimization framework for the orchestrator
9. The reward function jointly accounts for solution quality and computational efficiency via a tunable weighting factor lambda
10. Step-wise cost is defined based on FLOPs or token-level metrics at each reasoning step

## Capabilities

- RL-trained centralized orchestrator (Puppeteer) dynamically sequences agent activations in multi-agent systems, achieving superior task performance while simultaneously reducing token consumption — breaking the assumed performance-vs-efficiency tradeoff
- RL reward shaping with a combined accuracy-efficiency objective enables dynamic agent pruning — the orchestrator learns to suppress low-contributing agents and trigger early termination, reducing active agent count and token usage during inference
- Multi-agent systems with heterogeneous model pools (diverse vendors and scales) consistently outperform homogeneous single-model multi-agent systems on both closed- and open-domain tasks under RL-trained orchestration
- RL-driven multi-agent orchestration naturally produces graph-structured topologies with cycles and cross-branch connections — enabling recursive critique, mutual verification, and sustained internal debate that chain or tree structures cannot support

## Limitations

- Efficiency gains from RL-trained orchestration are model-capacity-dependent and collapse for small model pools: the Mimas (7B–14B) subspace shows no reduction in orchestrated agent count — only lower-cost agent substitution — because weak models cannot safely terminate reasoning early without qualit
- Topology hyperparameters (chain depth, exploration width) exhibit a non-monotonic relationship with performance — increasing depth or width beyond the default (W4D2) causes redundancy, higher computational cost, and performance degradation rather than improvement
- Static multi-agent systems with mesh topologies at scale (50 nodes) require up to 10 hours to develop software of only a few hundred lines of code — making large-scale collaborative agent deployment computationally infeasible without dynamic pruning
- All experiments use fixed, short episode length (maximum 4 reasoning steps) and small parallel exploration budgets (up to 3) — the framework's behaviour on long-horizon tasks requiring many sequential agent activations is not characterised
- Open-ended task quality rewards (r ∈ [0,1]) rely on LLM-as-judge evaluation for metrics like grammar, relevance, and logical consistency — creating a dependency on an evaluator whose own calibration and reliability are not validated in the paper
- The orchestrator is trained via REINFORCE — a high-variance policy gradient estimator — with episode-level (terminal) rewards, providing no step-level credit assignment across individual agent activations within a trajectory
- The agent pool A is enumerated upfront as fixed combinations of model, reasoning pattern, and tool set — there is no mechanism for the system to incorporate new models or tools without redefining the agent space and retraining the orchestrator
- The framework assumes a single-source, single-sink graph configuration — tasks requiring multiple independent outputs or parallel sub-goals with separate sinks are not supported by the formalism
- Performance validation is entirely benchmark-confined (GSM-Hard, MMLU-Pro, SRDD, CommonGen-Hard) — there is no evaluation on real-world deployment scenarios, novel task distributions outside training benchmarks, or long-horizon autonomous operation

## Bottlenecks

- Scaling laws of agentic organization remain empirically unmapped — this paper provides evidence that topology density and cycle counts evolve predictably under RL, but does not characterise how accuracy, latency, and coordination overhead scale as agent pool size grows beyond the experimental range
- Open-ended task verifiers for RL training of multi-agent orchestrators remain unreliable — the Puppeteer system requires r ∈ [0,1] quality scores for open-ended outputs, but these are delegated to LLM judges whose consistency under adversarial agent outputs is unknown
- Credit assignment in multi-step agent selection RL remains unresolved — REINFORCE with terminal rewards cannot attribute which specific agent activation in a long trajectory caused success or failure, limiting the orchestrator's learning efficiency

## Breakthroughs

- RL-trained centralized orchestration breaks the performance-efficiency tradeoff in multi-agent LLM systems — prior work documented that performance gains via multi-agent collaboration necessarily come with increased token consumption, but Puppeteer achieves simultaneous improvement in both metrics

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]

## Key Concepts

- [[entities/bradley-terry-model|Bradley-Terry model]]
- [[entities/reinforce|REINFORCE]]
- [[entities/self-refine|Self-Refine]]
