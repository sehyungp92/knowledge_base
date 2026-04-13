---
type: source
title: In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
source_id: 01KJTE6RW1ANJJ0VM4QECDVQ75
source_type: paper
authors:
- Zhuofeng Li
- Haoxiang Zhang
- Seungju Han
- Sheng Liu
- Jianwen Xie
- Yu Zhang
- Yejin Choi
- James Zou
- Pan Lu
published_at: '2025-10-07 00:00:00'
theme_ids:
- agent_systems
- multi_agent_coordination
- policy_optimization
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# In-the-Flow Agentic System Optimization for Effective Planning and Tool Use

**Authors:** Zhuofeng Li, Haoxiang Zhang, Seungju Han, Sheng Liu, Jianwen Xie, Yu Zhang, Yejin Choi, James Zou, Pan Lu
**Published:** 2025-10-07 00:00:00
**Type:** paper

## Analysis

# In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
2025-10-07 · paper · Zhuofeng Li, Haoxiang Zhang, Seungju Han, Sheng Liu, Jianwen Xie et al. (9 total)
https://arxiv.org/pdf/2510.05592

---

### Motivation & Prior Limitations
Outcome-driven reinforcement learning has advanced LLM reasoning, but prevailing tool-augmented approaches train a single monolithic policy that interleaves thoughts and tool calls under full context, creating fundamental scaling and generalization problems.
- Training a single policy over multi-turn, full-context trajectories becomes increasingly unstable as horizon length grows, tool diversity increases, and environments shift dynamically with tool feedback.
  - Cited instability is documented across multiple concurrent works (Wang et al., 2025c; Mai et al., 2025; Moonshot AI, 2025; Xue et al., 2025).
- Inference-time generalization of monolithic TIR models remains brittle when faced with unseen tasks or novel tool configurations.
  - Early TIR systems supported only a single tool type; even multi-tool extensions that encode tool metadata into prompts do not resolve the underlying policy-collapse risk at long horizons.

Agentic systems decompose work across specialized modules and can address long-horizon, multi-tool problems, but almost all remain training-free, relying on handcrafted orchestration logic or static prompting heuristics that cannot reliably adapt to evolving tool outputs or recover from early mistakes.
- The few systems that do employ training use supervised fine-tuning or preference optimization applied offline, decoupling training from the live dynamics of multi-turn interaction and preventing modules from learning from downstream successes or failures.
  - This creates a structural gap: agentic systems are flexible but static; trainable TIR models are adaptive but monolithic and fragile at scale.

The long-horizon credit assignment problem is the core unsolved challenge: sparse, trajectory-level rewards must propagate back through many interleaved turns where module outputs, tool observations, and memory states shift continuously.

---

### Proposed Approach
AGENTFLOW is a trainable, in-the-flow agentic framework that coordinates four specialized modules — Action Planner (P), Tool Executor (E), Execution Verifier (V), and Solution Generator (G) — through a shared evolving memory (M) and a toolset (K), with the planner trained on-policy directly inside the live multi-turn loop rather than offline.
- Unlike prior agentic systems, only the planner is trained; the other three modules remain frozen, keeping the training surface tractable while still allowing adaptive coordination.
- The system is formalized as a multi-turn Markov Decision Process: at each turn t, the planner samples an action (sub-goal, tool selection, context retrieval) conditioned on the query, the toolset, and the current memory state M_t; the executor invokes the tool; the verifier produces a binary validation signal; and the memory is updated deterministically via a structured, bounded memory-update function f_mem that records process information, turn index, time, and error signals.
  - The bounded, structured memory design is a deliberate architectural choice: it prevents unbounded context growth (a scaling failure mode in monolithic TIR), enables transparent state tracking, and ensures the planner always operates on a clean, controllable representation of accumulated evidence rather than raw full-context token sequences.

Flow-based Group Refined Policy Optimization (Flow-GRPO) is an on-policy algorithm purpose-built for sparse-reward credit assignment in this multi-module setting, converting the multi-turn RL problem into a sequence of tractable single-turn policy updates.
- Rather than attempting to estimate brittle intermediate rewards at each turn, Flow-GRPO broadcasts a single, verifiable trajectory-level final-outcome reward to every turn in the rollout, so each planner decision receives a reward signal aligned with global success.
- Group-normalized advantages (following the GRPO lineage from Shao et al., 2024) stabilize training by normalizing reward signals across sampled trajectory groups, preventing high-variance gradient estimates that would otherwise destabilize learning over long horizons.
- Rollouts are generated "in the flow" — meaning they capture the full trajectory of states, actions, and tool events produced by the live agentic system, including verifier signals and memory updates — so the planner is always trained on the distribution of states it will actually encounter at inference time.

---

### Results & Capabilities
AGENTFLOW with a 7B-scale Qwen2.5-7B-Instruct backbone (planner trained via Flow-GRPO, other modules frozen) achieves average accuracy gains of 14.9% on knowledge-intensive search tasks, 14.0% on broader agentic tasks, 14.5% on mathematical reasoning, and 4.1% on scientific reasoning across ten benchmarks, outperforming all evaluated 7B-scale baselines.
- Baselines span diverse categories: base LLMs (Qwen2.5-7B), tool-integrated RL models (Search-R1, TIR, ToRL, ReSearch), and training-free agentic systems (AutoGen) — all at 7B scale.
- The system surpasses GPT-4o (~200B parameters) across all four task domains, representing a greater-than-20x parameter efficiency advantage on the evaluated benchmarks.

Flow-GRPO training provides the decisive margin: AGENTFLOW without Flow-GRPO (using only the modular architecture with frozen or SFT-tuned planner) substantially underperforms the trained variant, with per-benchmark gaps of 10–20+ percentage points on representative tasks (2Wiki, HotpotQA, GAIA, AIME24, GameOf24, GPQA).
- This comparison directly validates the "in-the-flow optimization is crucial" claim and rules out the modular architecture alone as the source of gains.

Qualitative analysis reveals that the trained planner learns three concrete behavioral improvements: higher-quality sub-goal decomposition and

## Key Claims

1. Most agentic systems remain training-free or rely on offline training decoupled from the live dynamics of multi-turn interaction.
2. AGENTFLOW with a 7B-scale backbone outperforms top-performing baselines with average accuracy gains of 14.9% on search tasks.
3. AGENTFLOW with a 7B-scale backbone surpasses GPT-4o (~200B parameters) across all reasoning domains.
4. In-the-flow optimization with Flow-GRPO produces improved planning, enhanced tool-calling reliability, and positive scaling with model size and reasoning turns.
5. Outcome-driven reinforcement learning has driven recent advances in reasoning capabilities of large language models.
6. Monolithic multi-turn full-context training becomes increasingly unstable as horizons lengthen, tool diversity grows, and environments shift with tool feedback.
7. Inference-time generalization of monolithic tool-integrated reasoning models remains brittle to unseen tasks or tools.
8. Agentic systems are typically training-free, relying on handcrafted logic or prompting heuristics, which prevents them from reliably adapting to evolving tool outputs or recovering from early mistakes
9. Off-policy supervised fine-tuning or preference optimization approaches for agentic system modules are decoupled from live dynamics and learn poorly from downstream successes or failures.
10. Flow-GRPO converts multi-turn reinforcement learning into a series of tractable single-turn policy updates by broadcasting a single verifiable final-outcome reward to every turn.

## Capabilities

- A 7B-parameter trainable agentic system (AgentFlow) with in-the-flow RL optimization achieves average accuracy gains of 14.9% on search, 14.0% on agentic, 14.5% on mathematical, and 4.1% on scientific reasoning benchmarks over top baselines, surpassing GPT-4o (~200B parameters) across all tested dom
- Flow-GRPO enables stable on-policy RL training of a planner module within a live multi-turn agentic loop by broadcasting a single verifiable trajectory-level outcome reward to every turn, converting multi-turn optimization into a sequence of tractable single-turn policy updates
- A four-module agentic system (planner, executor, verifier, generator) coordinated via a shared evolving structured memory achieves bounded context growth while enabling transparent state tracking across multi-turn tool-augmented reasoning
- In-the-flow RL optimization of only the planner module within an otherwise frozen multi-module agentic system produces increased rewards and condensed responses with higher training efficiency compared to traditional monolithic tool-integrated RL methods

## Limitations

- Monolithic tool-integrated reasoning models that train a single policy under full multi-turn context become increasingly unstable as horizon length grows, tool diversity increases, and environments shift with tool feedback
- Inference-time generalization of monolithic tool-integrated reasoning models remains brittle to unseen tasks or tools not encountered during training
- Handcrafted logic and static prompting in training-free agentic systems cannot reliably capture when and how modules should collaborate, adapt to evolving tool outputs, or recover from early mistakes — robust coordination structurally requires training
- Off-policy SFT and preference optimization for agentic modules are decoupled from live dynamics and learn poorly from downstream successes or failures — a structurally inferior alternative to on-policy in-the-flow training
- AgentFlow trains only the planner module; executor, verifier, and generator remain frozen — the full pipeline is not jointly optimized, potentially capping the performance ceiling achievable through end-to-end training
- Flow-GRPO requires a verifiable, binary trajectory-level outcome reward signal — the method is inapplicable to open-ended generative tasks where outcomes cannot be automatically verified
- All evaluations are conducted exclusively on standard reasoning benchmarks — no real-world deployment evaluation, production latency measurements, or cost-per-task analysis is provided, making operational viability unknown
- No per-turn latency or total inference cost is reported — it is unclear whether the four-module architecture with inter-module communication reduces or increases end-to-end compute overhead relative to monolithic approaches despite claimed training efficiency
- All experiments use Qwen2.5-7B as the backbone — whether AgentFlow's architectural and training gains transfer to other model families (Llama, Mistral, etc.) is not demonstrated, raising questions about generality
- The verifier module produces only a binary verification signal (pass/fail) — fine-grained error diagnosis and targeted recovery within a turn are not captured, potentially limiting the system's ability to recover from partially-correct tool executions

## Bottlenecks

- Long-horizon credit assignment in multi-turn agentic RL — sparse trajectory-level outcomes must be attributed across many sequential planner decisions without intermediate rewards, making stable on-policy policy gradient updates on agentic loops intractable with existing methods
- Multi-turn training instability under growing tool diversity and horizon length — standard policy gradient methods become increasingly unstable as tool libraries expand and trajectories lengthen, blocking reliable training of monolithic or partially-modular agents
- Absence of scalable in-the-flow RL training frameworks — most agentic systems remain frozen because no established method exists to align module-level decisions with global trajectory outcomes in live multi-turn settings

## Breakthroughs

- Flow-GRPO: in-the-flow on-policy RL training of a planner within a live multi-turn agentic system, achieved by broadcasting a single verifiable trajectory-level outcome reward uniformly to every turn and using group-normalized advantages for stability — converting intractable multi-turn RL into trac
- A 7B-parameter modular agentic system trained with in-the-flow RL surpasses GPT-4o (~200B parameters) across all tested reasoning domains — demonstrating that architecture and training method can substitute for a 28× parameter count advantage

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/bamboogle|Bamboogle]]
- [[entities/gaia|GAIA]]
- [[entities/gpqa|GPQA]]
- [[entities/game-of-24|Game of 24]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/musique|MuSiQue]]
- [[entities/tool-integrated-reasoning|Tool-Integrated Reasoning]]
