---
type: source
title: 'Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning'
source_id: 01KJT89YD67D2HK0MSXTA33J7J
source_type: paper
authors:
- Mingyue Cheng
- Jie Ouyang
- Shuo Yu
- Ruiran Yan
- Yucong Luo
- Zirui Liu
- Daoyu Wang
- Qi Liu
- Enhong Chen
published_at: '2025-11-18 00:00:00'
theme_ids:
- agent_systems
- policy_optimization
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning

**Authors:** Mingyue Cheng, Jie Ouyang, Shuo Yu, Ruiran Yan, Yucong Luo, Zirui Liu, Daoyu Wang, Qi Liu, Enhong Chen
**Published:** 2025-11-18 00:00:00
**Type:** paper

## Analysis

# Agent-R1: Training Powerful LLM Agents with End-to-End Reinforcement Learning
2025-11-18 · paper · Mingyue Cheng, Jie Ouyang, Shuo Yu, Ruiran Yan, Yucong Luo et al. (9 total)
https://arxiv.org/pdf/2511.14460

---

### Motivation & Prior Limitations
- RL has proven effective for static LLM tasks (math, code generation) but its application to interactive, multi-turn LLM agents remains nascent and poorly defined, leaving a significant gap between what RL can theoretically offer agents and what exists in practice.
  - Existing single-turn RL frameworks do not account for the distinct challenges of agent settings: sequential multi-turn decision-making, stochastic environmental feedback from tool use, and the need for intermediate process rewards rather than purely sparse final rewards.
  - Multi-turn agent training specifically suffers from instability, complex reward signal design, and limited generalization — problems that existing frameworks were not designed to address.
- No principled, flexible, and extensible open training framework existed for RL-based LLM agents, forcing researchers to adapt mismatched single-turn infrastructure or build from scratch.
  - The field lacked even a systematic formal account of how core MDP components (state space, action space, transitions, reward) change when moving from static LLM generation to interactive agents.

---

### Proposed Approach
- The paper makes two contributions: a formal MDP extension that precisely characterizes LLM agents, and Agent-R1, a modular open-source training framework implementing that formulation for end-to-end RL training of multi-turn tool-using agents.
  - The MDP extension distinguishes static LLM states (current token sequence only) from agent states (full multi-turn history including environmental feedback), separates deterministic generative transitions (PG) from stochastic environmental transitions (PE) triggered by tool calls, and introduces a richer reward structure combining sparse final outcome rewards (rf) with dense intermediate process rewards (rp) for successful tool invocations.
- Agent-R1's core architectural innovation is the separation of responsibilities between a **Tool** module (atomic executor that returns raw outcomes) and a **ToolEnv** module (orchestrator that manages state transitions, computes rewards, and packages new state for the agent), built around abstract base classes (`BaseTool`, `BaseToolEnv`) for easy extension.
  - The `ToolEnv.step` method handles both standard generative transitions and the more complex stochastic transitions from tool interactions, parsing LLM outputs for tool call triggers, executing tools, computing rewards, and determining trajectory termination.
- Policy optimization uses two masking mechanisms: a **loss mask** that restricts gradient computation to agent-generated tokens (excluding prompt tokens and environmental feedback), and an **advantage mask** that aligns advantage estimates (computed via GAE incorporating both process and outcome rewards) specifically to agent action timesteps for accurate credit assignment.
  - This directly addresses the credit assignment problem in multi-turn trajectories where non-agent tokens (tool responses, prompts) would otherwise contaminate the gradient signal.

---

### Results & Capabilities
- All five RL algorithms trained with Agent-R1 substantially outperform both baselines on multi-hop QA: the weakest RL method (REINFORCE++, average EM 0.3300) exceeds Naive RAG (0.1328) by approximately 2.5× and Base Tool Call (0.0847) by nearly 4×.
  - GRPO achieved the best average Exact Match of 0.3877 across HotpotQA, 2WikiMultihopQA, and out-of-domain Musique; PPO (0.3719) and RLOO (0.3716) were close behind; PPO notably led on the harder out-of-domain Musique (0.1552).
- Ablation results confirm that both masking strategies are critical components, not optional refinements.
  - For PPO, disabling the advantage mask alone drops average EM from 0.3719 to 0.3136 (−0.0583); further disabling the loss mask drops it to 0.3022. For GRPO, disabling the loss mask drops average EM from 0.3877 to 0.3722.
- The framework validates that its modular design supports five distinct RL algorithms (PPO, GRPO, REINFORCE++, REINFORCE++Baseline, RLOO) without algorithmic modification, demonstrating genuine extensibility.

---

### Implications
- The formal MDP re-characterization of LLM agents provides a shared vocabulary for the nascent field of agentic RL, potentially reducing the conceptual ambiguity that has slowed systematic progress on applying RL to tool-using, multi-turn agents.
- The 2.5–4× improvement of RL-trained agents over RAG and naive tool-calling baselines on multi-hop QA suggests that end-to-end RL, rather than prompt engineering or retrieval augmentation alone, may be the necessary training paradigm for agents that must adaptively chain tool calls across multiple reasoning steps — with direct implications for how autonomous software agents and computer-use agents should be trained.
- The open-source, modular architecture of Agent-R1 (Tool/ToolEnv abstraction, support for multiple RL algorithms) lowers the barrier for RL agent research and may accelerate empirical exploration of reward shaping, process reward modeling, and environment design for agentic tasks.
- The explicit separation of agent-generated tokens from environmental feedback via action masking is a reusable design pattern applicable to any multi-turn RLHF or reward modeling setup where non-agent tokens pollute the training signal.

---

### Remaining Limitations & Next Steps
- Experiments are limited to a single task type (multi-hop QA with Wikipedia search) using a single small model (Qwen2.5-3B-Instruct), making it unclear whether the framework and results generalize to other agent domains such as code execution, computer use, or embodied environments.
  - The authors describe these experiments as "initial validation," explicitly framing the work as a technical report 

## Key Claims

1. The application of RL to developing LLMs as autonomous, interactive agents is comparatively nascent compared to its use in well-defined tasks like math and code.
2. The state space for an LLM Agent must retain multi-turn interaction history and environmental feedback, making it significantly more comprehensive than that of a static LLM.
3. LLM Agents can receive intermediate process rewards for successfully executing steps like tool invocation, providing more frequent feedback than the sparse terminal rewards used for static LLMs.
4. Agent-R1 uses a modular Tool/ToolEnv architecture where Tool encapsulates atomic action execution and ToolEnv manages state transitions and reward calculation.
5. Agent-R1 uses an Action Mask to distinguish agent-generated tokens from environmental feedback and prompt tokens, ensuring credit assignment is limited to the agent's actual decisions.
6. Advantage calculation in Agent-R1 incorporates both process rewards and outcome rewards alongside critic value estimates, and is aligned with the action mask to assign credit only to agent-generated a
7. All RL-trained agents substantially outperform both the Base Tool Call and Naive RAG baselines on multi-hop QA tasks, with even the weakest RL agent surpassing RAG by approximately 2.5x.
8. GRPO achieved the best overall RL performance (average EM 0.3877) on multi-hop QA, closely followed by PPO (0.3719) and RLOO (0.3716).
9. PPO excelled on the out-of-domain Musique dataset (EM 0.1552) compared to other RL methods, suggesting better generalization.
10. Adding a baseline to REINFORCE++ (REINFORCE++Baseline) improved average EM from 0.3300 to 0.3619, though it still underperformed GRPO and PPO.

## Capabilities

- LLM agents trained via end-to-end RL across multiple algorithms (PPO, GRPO, REINFORCE++, RLOO) achieve substantial improvements on multi-turn interactive tool-use tasks — weakest RL agent (REINFORCE++, avg EM 0.33) still outperforms RAG baseline by a factor of 2.5x
- Action masking (loss mask + advantage mask) enables precise credit assignment in multi-turn RL trajectories by restricting gradient computation and advantage alignment exclusively to agent-generated tokens, substantially improving policy learning over unmasked baselines
- Modular RL training framework (Agent-R1) with Tool/ToolEnv abstractions supports rapid integration of diverse environments, multiple RL algorithms, and flexible multi-turn rollout — enabling extensible end-to-end agent training without redesigning core infrastructure per task
- Extended MDP formulation for LLM agents formally captures multi-turn state history, stochastic environmental transitions from tool use, and dense process rewards — providing a principled theoretical substrate for RL agent training that differs fundamentally from static single-turn LLM RL

## Limitations

- Multi-turn RL agent training is explicitly prone to instability, complex reward signal design failure, and limited generalization — none of these challenges are resolved by this work
- All experimental validation uses a single 3B-parameter model (Qwen2.5-3B-Instruct) on one task type — results may not generalise to larger models or more complex agent scenarios, and no scaling analysis is provided
- Agent is tested with only a single tool (wikisearch) — multi-tool coordination, tool selection under diversity, and heterogeneous tool type handling are entirely absent from evaluation despite being core real-world agent challenges
- Despite the theoretical framework centring process (intermediate) rewards as a key differentiator for agent RL, experiments use exclusively sparse final outcome rewards — the richer reward structure has no empirical validation in this work
- Out-of-domain generalisation is severely degraded — RL-trained agents score 0.1485 on out-of-domain Musique vs 0.5741 in-domain on 2Wiki (GRPO), a greater than 75% performance cliff across all tested RL algorithms
- The work is explicitly characterised as 'initial validation' on a single narrow benchmark — no real-world agentic tasks (open-ended web browsing, code execution, long-horizon planning) are evaluated, so external validity is unestablished
- No ablation of process rewards vs. sparse rewards is performed despite process rewards being the theoretical centrepiece — whether intermediate reward signals actually improve multi-turn agent training remains empirically untested
- No adversarial robustness or prompt injection testing is performed — RL-trained agents that retrieve from external sources (Wikipedia) have no evaluated defences against manipulation through retrieved content
- Stochastic environmental transitions from tool use introduce training variance that standard RL variance-reduction techniques (baselines, GAE) were not designed to handle — the interaction between PE stochasticity and policy gradient estimation is unaddressed

## Bottlenecks

- Multi-turn credit assignment in RL agent training is broken without explicit action masking — standard advantage calculation contaminates policy gradients with environmental feedback and prompt tokens, causing systematic misattribution that substantially degrades learning
- Existing RL training infrastructure is structurally designed for single-turn rollouts and cannot support multi-turn agent training — rollout phases, trajectory storage, state transition handling, and reward attribution all require redesign
- Dense process reward design for multi-turn agent RL is unresolved — practitioners must fall back to sparse outcome rewards, providing insufficient gradient signal for long-horizon trajectories where the final answer depends on many intermediate retrieval and reasoning decisions

## Breakthroughs

- End-to-end RL training of multi-turn LLM agents with tool use substantially and consistently outperforms retrieval-augmented generation baselines — by 2.5x for the weakest RL method and 2.9x for the best (GRPO) — across multiple datasets and RL algorithms, providing empirical evidence that RL is a s

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/exact-match|Exact Match]]
- [[entities/grpo|GRPO]]
- [[entities/generalized-advantage-estimation|Generalized Advantage Estimation]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/musique|MuSiQue]]
- [[entities/ppo|PPO]]
- [[entities/qwen25-3b-instruct|Qwen2.5-3B-Instruct]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/rloo|RLOO]]
- [[entities/react|ReAct]]
