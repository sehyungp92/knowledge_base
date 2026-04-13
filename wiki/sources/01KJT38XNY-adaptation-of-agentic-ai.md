---
type: source
title: Adaptation of Agentic AI
source_id: 01KJT38XNYEF97W3QWXNTN27WC
source_type: paper
authors:
- Pengcheng Jiang
- Jiacheng Lin
- Zhiyi Shi
- Zifeng Wang
- Luxi He
- Yichen Wu
- Ming Zhong
- Peiyang Song
- Qizheng Zhang
- Heng Wang
- Xueqiang Xu
- Hanwen Xu
- Pengrui Han
- Dylan Zhang
- Jiashuo Sun
- Chaoqi Yang
- Kun Qian
- Tian Wang
- Changran Hu
- Manling Li
- Quanzheng Li
- Hao Peng
- Sheng Wang
- Jingbo Shang
- Chao Zhang
- Jiaxuan You
- Liyuan Liu
- Pan Lu
- Yu Zhang
- Heng Ji
- Yejin Choi
- Dawn Song
- Jimeng Sun
- Jiawei Han
published_at: '2025-12-18 00:00:00'
theme_ids:
- agent_systems
- finetuning_and_distillation
- in_context_and_meta_learning
- multi_agent_coordination
- post_training_methods
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Adaptation of Agentic AI

> A comprehensive survey and unifying framework for understanding how agentic AI systems are adapted to overcome their limitations. The paper introduces a four-paradigm taxonomy — A1, A2, T1, T2 — organized by what is optimized (agent parameters vs. external tools) and where the supervision signal originates. Its central contribution is demonstrating that the T2 "symbiotic inversion" paradigm, which trains lightweight peripheral subagents against a frozen foundation model rather than retraining the core, achieves comparable or superior performance to full agent retraining at ~70x lower data cost — reframing the foundation model from optimization target to stable supervisor.

**Authors:** Pengcheng Jiang, Jiacheng Lin, Zhiyi Shi, Zifeng Wang, Luxi He, Yichen Wu, Ming Zhong, Peiyang Song, Qizheng Zhang, Heng Wang, Xueqiang Xu, Hanwen Xu, Pengrui Han, Dylan Zhang, Jiashuo Sun, Chaoqi Yang, Kun Qian, Tian Wang, Changran Hu, Manling Li, Quanzheng Li, Hao Peng, Sheng Wang, Jingbo Shang, Chao Zhang, Jiaxuan You, Liyuan Liu, Pan Lu, Yu Zhang, Heng Ji, Yejin Choi, Dawn Song, Jimeng Sun, Jiawei Han
**Published:** 2025-12-18
**Type:** Paper
**Source:** https://arxiv.org/pdf/2512.16301

---

## Motivation

The rapid expansion of agentic AI research produced a fragmented landscape of adaptation methods — fine-tuning, tool learning, retrieval adaptation, subagent training — discussed in isolation with no unified framework for understanding their trade-offs, guiding principles, or structural relationships. Existing surveys on agent architectures and multi-agent coordination did not center on *how* components are modified to overcome limitations, leaving practitioners without principled guidance for choosing or switching adaptation strategies.

Meanwhile, the failure modes motivating adaptation are well-documented: unreliable tool use, limited long-horizon planning, domain-specific reasoning gaps, robustness failures in real-world environments, and poor generalization to unexplored settings. No single adaptation recipe addresses all of these, and the field's terminology obscures deep structural relationships between methods that share surface similarities but differ in fundamental ways.

---

## The Four-Paradigm Taxonomy

The paper introduces two orthogonal axes — *what is optimized* and *where supervision originates* — yielding four non-overlapping paradigms. Crucially, the paradigms are not mutually exclusive: state-of-the-art systems like DeepResearch combine T1 retrievers, T2 search agents, and A1 reasoning agents in cascaded pipelines.

### A1 — Tool Execution Signaled Agent Adaptation

The agent's parameters are updated using verifiable outcomes produced by external tool execution as the reward signal: code sandbox pass rates, retrieval recall scores, SQL execution correctness, or formal proof checker verdicts. This directly optimizes tool-use mechanics with causal, environment-grounded feedback.

**Representative systems:**
- DeepRetrieval — trains query reformulation as an MDP with retrieval metrics as reward, achieving 65.1% recall vs. prior SOTA of 24.7% (roughly 3x improvement) on literature search
- R1-Code-Interpreter — multi-stage curriculum RL for code execution, reaching 72.4% accuracy on 37 code tasks
- [[entities/alphaproof|AlphaProof]] (Nature 2025) — RL from Lean 4 proof verifier feedback for competition-level formal theorem proving

### A2 — Agent Output Signaled Agent Adaptation

The agent is optimized using evaluations of its own final outputs — answer correctness, reasoning quality, preference scores — after potentially incorporating tool results mid-trajectory. This learns holistic tool-use *strategy* rather than individual tool mechanics, including both SFT and RLVR variants.

**Representative systems:**
- DeepSeek-R1 — the foundational RLVR paradigm for math and code, establishing that RL can develop reasoning capabilities beyond SFT baselines without supervised reasoning-step annotations
- Search-R1 — trains agents to decide when and how to search via GRPO, without supervised reasoning-step data; up to 24% improvement over strong RAG baselines with emergent self-correction
- ReSearch — 9–22% absolute gains over iterative RAG on multi-hop QA

**Critical limitation:** A2 requires approximately 170,000 training examples to co-adapt internal knowledge, reasoning, and tool-use policy simultaneously — an entangled high-dimensional optimization. A2-adapted agents also overfit to training distributions: Search-R1 scores 71.8% on out-of-distribution medical QA compared to 76.6% for the T2-trained s3 system.

### T1 — Agent-Agnostic Tool Adaptation

The core agent is frozen and pre-trained tools — vision models (CLIP, SAM), speech models (Whisper), dense retrievers (DPR, ColBERT), scientific simulators (AlphaFold2), and "graduated" A1/A2-trained agents like DeepRetrieval — are deployed as plug-and-play modules without co-adaptation to the specific agent. Closed-source API models (GPT, Claude, Gemini) can consume these tools without any co-training.

**Tradeoff:** T1 tools trained on broad distributions generalize well across agents and tasks, but cannot internalize deep tool mechanics or update internal representations — the frozen foundation model's reasoning capacity places an architectural ceiling on what tool improvements can achieve.

### T2 — Agent Supervised Tool Adaptation

The core agent is frozen and lightweight peripheral tools — retrievers, planners, memory modules, subagents — are trained using the frozen agent's outputs as the supervision signal. The key conceptual inversion is that the expensive foundation model becomes a *stable supervision source* rather than the optimization target.

**Representative systems:**
- **s3** — a 7B searcher trained via Gain Beyond RAG reward from a frozen generator; achieves 58.9% average accuracy using only 2,400 training samples (~70x less data and ~33x faster than Search-R1), with *better* out-of-distribution generalization on medical QA (76.6% vs. 71.8%)
- **AgentFlow** — trains only a lightweight 7B planner to orchestrate frozen Qwen2.5-7B specialists via trajectory-level rewards; achieves 33.1% on GAIA, surpassing GPT-4 (~200B parameters), plus 57.3% on search-intensive tasks (+14.9% over AutoGen)
- **Memento** — trains a Q-function case-retrieval policy for a frozen GPT-4.1 planner; achieves 87.88% on GAIA validation (ranked 1st) and 95.0% on SimpleQA using only binary task success signals
- **SWE-Grep** — RL-trained subagent for fast parallel code search that conserves the primary agent's context window and shields it from context pollution

---

## Key Results

| Comparison | A2 (Search-R1) | T2 (s3) |
|---|---|---|
| Training examples | ~170,000 | ~2,400 |
| Training time | Baseline | ~33x faster |
| Average QA accuracy | 71.8% (medical OOD) | 76.6% (medical OOD) |

The explanation is structural: the T2 tool only needs to learn a narrow procedural skill (search policy) since the frozen generator already handles domain knowledge and reasoning. This decoupling of skill acquisition from general reasoning enables modular capability extension without backbone destabilization.

---

## Capabilities

The survey documents a broad set of demonstrated capabilities across paradigms. See the [[themes/post_training_methods|post-training methods]] and [[themes/tool_use_and_agent_protocols|tool use and agent protocols]] themes for related context.

**RLVR generalization (A1/A2):** RLVR has been demonstrated across math, coding, SQL, OCR, recommendation, and domain-specific tasks — establishing it as a broadly applicable paradigm rather than a domain-specific trick. Notable extensions include olmOCR 2 (binary unit tests as reward for document parsing), Rec-R1 (NDCG/Recall as reward for recommendation), and EHRMind (clinical reasoning, though requiring SFT warm-up first).

**Efficient tool orchestration (T1):** HuggingGPT demonstrated that frozen LLMs can orchestrate 1000+ specialized ML models from a hub using natural language; SciToolAgent scales to 500+ scientific domain tools with 94% accuracy via graph-based organization, a 15–20% improvement over prompt-based approaches; MCP + Code Execution mode reduces agent context window usage by over 98% while maintaining full tool compositionality.

**Multi-turn adaptive search:** Compact 350M–1.2B parameter models can perform multi-turn adaptive search with iterative query refinement, pivoting, and backtracking through structured think-search cycles — with explicit reasoning in `<think>` tags separated from structured tool calls in `<tool_call>` tags.

**Formal theorem proving:** Neural agents trained via RL from Lean 4 proof verifier feedback can generate valid multi-step proofs for competition-level mathematics, with AlphaProof's publication in Nature 2025 marking mainstream scientific recognition of this capability.

**Self-improvement mechanisms:** Multiple mechanisms for inference-time and training-time self-improvement have been demonstrated, including Test-Time Self-Improvement (TT-SI), textual gradient descent (TextGrad), and MCTS-based iterative self-correction (Agent-R).

---

## Limitations and Open Challenges

This source is unusually explicit about limitations, cataloguing them across paradigms. See the [[themes/agent_systems|agent systems]] theme for broader context on agentic failure modes.

### Structural Limitations by Paradigm

**Agent-centric (A1/A2):**
- High computational cost — training billion-parameter models via RL creates large cost asymmetry vs. tool adaptation
- Catastrophic forgetting — updating weights for one task degrades previously learned behaviors; mitigated but not structurally eliminated by on-policy RL
- Overfitting to training distributions — A2-adapted agents learn task shortcuts that fail on out-of-distribution inputs
- Entangled optimization — A2 must simultaneously co-adapt internal knowledge, reasoning, and tool-use policy, requiring massive training data

**Tool-centric (T1/T2):**
- Architectural ceiling — tool improvements cannot compensate for failures rooted in the frozen agent's reasoning capacity
- T2 ecosystem lock-in — subagents trained to serve one foundation model may not transfer to other agents without retraining
- A2-style final-output supervision is insufficient for teaching tool-use — the model can improve final-answer likelihood without ever invoking tools

### Fundamental Open Problems

**Continual adaptation** is explicitly flagged as blocking: no agentic paradigm maintains performance across dynamic, shifting environments. Formal libraries (MATHLIB) and community-maintained formalization projects grow continuously, invalidating policies trained on static premise sets. Real-world deployments involve non-stationary task distributions where isolated one-off adaptation is insufficient.

**Reward hacking** in open-ended RL loops blocks deployment of self-improving agents in real-world environments. Safe adaptation with open-ended reward signals is described as theoretically unsolved, with on-policy RL and outcome-driven tool tuning introducing emergent dynamic threat vectors — reward hacking, autonomous risk-taking, adversarial co-evolution — without established mitigation frameworks.

**Credit assignment in co-adaptive systems** is described as theoretically intractable: when a joint agent-tool system fails, it is fundamentally ambiguous whether failure originated in the agent's reasoning or the tools' outputs. This blocks joint agent-tool co-adaptation frameworks.

**Red Queen dynamics** in co-adaptive learning: when both agent and tool parameters are updated simultaneously, no pacemaker mechanisms or convergence guarantees exist to prevent oscillation without improvement or collapse into degenerate policies.

**RLVR applicability** is implicitly restricted to verifiable output domains — tasks where correctness can be evaluated via deterministic signals. Open-ended, creative, and subjective tasks are excluded, blocking R1-paradigm reasoning improvement for the majority of real-world applications. Furthermore, pure RLVR exploration fails in specialist domains without SFT grounding first (demonstrated in EHRMind for clinical reasoning).

**No standardized benchmarks** across paradigms: each of A1/A2/T1/T2 is evaluated on different tasks and metrics, making cumulative community progress measurement impossible and systematic comparison between paradigms infeasible.

**GPU cluster dependency** blocks on-device and personalized agent adaptation — current RL fine-tuning workflows are infeasible on mobile, edge, or low-power hardware.

---

## Bottlenecks

The paper identifies several critical bottlenecks relevant to the trajectory of [[themes/agent_systems|agentic AI]] development:

| Bottleneck | Horizon | Status |
|---|---|---|
| Joint agent-tool co-adaptation (no unified A+T framework) | 1–2 years | Open |
| Continual adaptation in non-stationary environments | 1–2 years | Open |
| No standardized evaluation benchmarks for adaptation paradigms | 1–2 years | Open |
| GPU cluster dependency blocking on-device adaptation | 1–2 years | Open |
| RLVR restricted to verifiable domains | 1–2 years | Open |
| Hybrid architecture combining reasoning depth + modular efficiency | 1–2 years | Emerging |
| Catastrophic forgetting blocking cumulative skill acquisition | 3–5 years | Open |
| Reward hacking blocking safe self-improvement | 3–5 years | Open |
| Credit assignment in co-adaptive systems | 3–5 years | Open |
| Red Queen dynamics in co-adaptive learning | 3–5 years | Open |

---

## Breakthroughs Documented

**T2 symbiotic inversion** is identified as a conceptual breakthrough: reframing the foundation model from optimization target to stable supervisor enables a ~70x reduction in training data requirements and ~33x faster training, representing a phase change in the economics of capable agentic systems. This paves the way for federated agentic systems that evolve continuously without destabilizing the backbone.

**RLVR paradigm** (DeepSeek-R1, Nature 2025): RL with verifiable rewards can develop reasoning capabilities beyond SFT/DPO baselines without supervised reasoning-step annotations, establishing a scalable annotation-free pathway for improving agent reasoning across verifiable domains.

**AlphaProof** (Nature 2025): RL-trained neural agents achieving competition-level formal theorem proving via proof assistant verifier feedback, marking mainstream scientific recognition of RL-based mathematical reasoning.

**MCP + Code Execution**: over 98% reduction in context window usage while maintaining full tool compositionality, effectively decoupling tool ecosystem size from inference cost.

**TextGrad**: textual gradient descent enables end-to-end optimization of compound AI systems through natural-language critiques alone, without parameter access or scalar rewards.

---

## Forward-Looking Positions

The paper's central forward-looking claim is that the next generation of intelligent systems will be defined not by a single monolithic model but by the principled orchestration of stable reasoning cores supported by specialized and adaptive tools. The hybrid architecture combining reasoning depth of agent-centric adaptation with modular efficiency of tool-centric adaptation does not yet exist as a realized system — it is described only as a design direction.

Three fundamental challenges must be addressed: **continual adaptation** to maintain performance in dynamic streams, **safe adaptation** to mitigate reward hacking and emergent threat vectors, and **efficient adaptation** to enable deployment in resource-constrained environments.

The survey implicitly raises a structural question it does not resolve: if T2 is dramatically more data-efficient than A2 for equivalent capability, and if the frozen backbone places an architectural ceiling on T2, then the critical unanswered question is *when and how* to decide which components warrant the expense of A1/A2 retraining vs. T2 peripheral adaptation — a question that requires the unified co-adaptation framework the paper identifies as missing.

---

## Related Themes

- [[themes/agent_systems|Agent Systems]] — core subject; agentic architectures, failure modes, deployment challenges
- [[themes/post_training_methods|Post-Training Methods]] — RLVR, SFT, DPO, the DeepSeek-R1 paradigm
- [[themes/finetuning_and_distillation|Finetuning and Distillation]] — parameter-efficient methods (LoRA), catastrophic forgetting
- [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]] — MCP, tool orchestration, CodeAct, HuggingGPT
- [[themes/multi_agent_coordination|Multi-Agent Coordination]] — AgentFlow, subagent training, federated agentic systems
- [[themes/in_context_and_meta_learning|In-Context and Meta-Learning]] — TextGrad, test-time self-improvement, inference-time adaptation

## Key Concepts

- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/codeact|CodeAct]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/lora-low-rank-adaptation|LoRA (Low-Rank Adaptation)]]
- [[entities/low-rank-adaptation|Low-Rank Adaptation]]
- [[entities/model-context-protocol-mcp|Model Context Protocol (MCP)]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/rlvr-reinforcement-learning-with-verifiable-rewards|RLVR (Reinforcement Learning with Verifiable Rewards)]]
- [[entities/react|ReAct]]
- [[entities/retool|ReTool]]
- [[entities/reflexion|Reflexion]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/score|SCoRe]]
- [[entities/self-refine|Self-Refine]]
- [[entities/stability-plasticity-dilemma|Stability-Plasticity Dilemma]]
- [[entities/supervised-fine-tuning|Supervised Fine-Tuning]]
