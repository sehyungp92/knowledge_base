---
type: source
title: Towards General Agentic Intelligence via Environment Scaling
source_id: 01KJTJ3WVG8VE0SK2CPCWGV9K0
source_type: paper
authors:
- Runnan Fang
- Shihao Cai
- Baixuan Li
- Jialong Wu
- Guangyu Li
- Wenbiao Yin
- Xinyu Wang
- Xiaobin Wang
- Liangcai Su
- Zhen Zhang
- Shibin Wu
- Zhengwei Tao
- Yong Jiang
- Pengjun Xie
- Fei Huang
- Jingren Zhou
published_at: '2025-09-16 00:00:00'
theme_ids:
- agent_systems
- finetuning_and_distillation
- post_training_methods
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Towards General Agentic Intelligence via Environment Scaling

**Authors:** Runnan Fang, Shihao Cai, Baixuan Li, Jialong Wu, Guangyu Li, Wenbiao Yin, Xinyu Wang, Xiaobin Wang, Liangcai Su, Zhen Zhang, Shibin Wu, Zhengwei Tao, Yong Jiang, Pengjun Xie, Fei Huang, Jingren Zhou
**Published:** 2025-09-16 00:00:00
**Type:** paper

## Analysis

# Towards General Agentic Intelligence via Environment Scaling
2025-09-16 · paper · Runnan Fang, Shihao Cai, Baixuan Li, Jialong Wu, Guangyu Li et al. (16 total)
https://arxiv.org/pdf/2509.13311v1

---

### Motivation & Prior Limitations
- The scarcity of agentic data — multi-turn trajectories of agents interacting with environments via explicit tool calls — is the fundamental bottleneck constraining progress toward general function-calling intelligence, because agents must acquire these capabilities through direct environmental interaction rather than passive corpus learning.
  - Reverse-paradigm approaches (generating user queries to match observed function calls) produce trajectories with limited realism; forward-paradigm simulated agent–human interplay approaches lack naturalness and, critically, lack automated environment construction, making large-scale deployment require manual intervention.
- Real-world API environments are too costly and unstable for large-scale agentic data generation and RL training, while LLM-simulated environments suffer from hallucination and inconsistent response variability, making neither approach viable for scalable, verifiable trajectory collection.
- The breadth of function-calling competence is tightly coupled to the diversity of training environments, yet no prior work had proposed a principled, automated method for constructing and scaling heterogeneous tool-use environments across thousands of domains without human involvement.

---

### Proposed Approach
- AgentScaler introduces a two-stage pipeline: (i) automated, scalable construction of fully simulated, database-grounded tool-use environments, and (ii) a two-phase agent fine-tuning strategy that first builds general tool-usage foundations before domain-specific specialization.
  - Environment construction begins by collecting over 30,000 APIs from ToolBench, API-Gen, and internal sources, then building a tool dependency graph where edges encode compositional compatibility via cosine similarity of parameter embeddings; Louvain community detection partitions this graph into over 1,000 coherent tool domains, each assigned a database schema.
  - Each tool is materialized as executable Python code performing read/write operations on its domain's database schema, enabling two-granularity verifiability: database-level state consistency checks and exact-match validation of tool call sequences — eliminating the need for human verification at scale.
  - Agentic tasks are constructed by sampling logically coherent tool sequences via directed walks on the domain tool graph, initializing diverse database states, grounding tool executions on the live database, and running simulated human–agent interplay; trajectories are filtered through a three-stage funnel (validity control → environment state alignment → function-calling exact match), with error-containing trajectories retained if they still achieve the goal, improving model robustness.
- The training objective masks tool responses and human instructions from the loss, propagating gradients only through agent-generated tool calls and natural-language responses, ensuring the model learns to condition on environmental feedback without being supervised on it.
- Stage 1 trains on broad, general-domain data to develop versatile function-calling and user-response integration skills; Stage 2 fine-tunes on vertical domain scenarios to achieve contextually aligned, accurate tool selection and parameterization — a curriculum that mirrors general-to-specialist skill acquisition.

---

### Results & Capabilities
- AgentScaler-30B-A3B achieves state-of-the-art performance among open-source models under 1T parameters across all three benchmarks (τ-bench, τ2-Bench, ACEBench-en), reaching parity with trillion-parameter open-source models such as Kimi-K2-1T-A32B and approaching closed-source systems on most sub-tasks.
  - On τ2-Bench, AgentScaler-30B-A3B scores 70.2 (Retail), 60.0 (Airline), 55.3 (Telecom) versus the Qwen3-Thinking-30B-A3B baseline of 58.8, 58.0, and 26.3 respectively; on ACEBench-en Overall it scores 75.7 versus the backbone's 67.2.
- AgentScaler-4B achieves performance comparable to 30B-parameter open-source models, scoring 64.3 on τ-bench Retail and 54.0 on Airline, demonstrating that agentic capabilities can be effectively concentrated in compact models suitable for resource-constrained or latency-sensitive deployment.
- Two-stage training is validated by ablation on ACEBench-en: both Stage 1 and Stage 2 independently improve over the base Qwen3-Thinking-30B-A3B, with Stage 2 providing additional gains specifically on the Agent subset, confirming that general foundation learning and domain specialization are complementary and non-redundant.
- Strong out-of-distribution generalization is demonstrated on ACEBench-zh, an OOD evaluation relative to the English training setup: AgentScaler-30B-A3B achieves 81.5 Overall (+7.3 over its backbone), and the 4B model's Agent subset score jumps from 6.7 to 38.4 (+31.7), indicating that the synthetic data pipeline induces transferable rather than superficial capabilities.
- The pass^k metric on τ2-Bench confirms greater stability than the Qwen3-Thinking-30B-A3B baseline across all k settings, though a clear downward trend as k increases reveals that consistency under repeated independent trials remains a fundamental unsolved challenge for all current LLMs.

---

### Implications
- Automated environment scaling via tool graph construction and programmatic database materialization decouples agentic data generation from human intervention and real API costs, suggesting that the diversity and quality of training environments — not just model scale — may be the primary lever for advancing general function-calling intelligence.
- The finding that a 30B MoE model trained with this pipeline matches trillion-parameter models on agentic benchmarks has direct implications for the efficient-deployment trajectory of AI agents:

## Key Claims

1. Progress in LLM function-calling is fundamentally constrained by the scarcity of agentic data — trajectories generated by autonomous agents interacting with environments via tool calls.
2. The breadth of an agent's function-calling competence is closely tied to the diversity of environments in which it is trained.
3. The reverse paradigm for synthetic agentic data generation — generating user queries to match observed function calls — produces trajectories with limited realism.
4. The forward paradigm for synthetic agentic data generation — constructing trajectories top-down from user intent via human-agent interplay — produces trajectories that lack naturalness and is not scal
5. The AI community is transitioning from the era of raw corpora and human-curated data to an emerging era of experience-based training for language agents.
6. The AgentScaler framework collected more than 30,000 APIs from ToolBench, API-Gen, and an internal tool repository after rigorous filtering.
7. Tool dependency graph construction uses cosine similarity of parameter vector representations, with edges inserted between tool pairs exceeding a predefined threshold, followed by Louvain community de
8. The environment construction pipeline yielded over 1,000 distinct tool domains.
9. Programmatic materialization of tool schemas into executable Python code, when applied to τ-bench domains, produces database structures with high consistency to τ-bench's official implementations.
10. Agentic task construction uses a three-stage funnel-based trajectory filtering consisting of validity control, environment state alignment, and function calling exact match.

## Capabilities

- Automated pipeline constructs 1,000+ heterogeneous agent training environments from 30,000+ real-world APIs using tool dependency graph clustering (Louvain community detection) and programmatic database materialization — no manual intervention required
- 30B MoE open-source agent (AgentScaler-30B-A3B) achieves function-calling performance on par with trillion-parameter open-source models and approaches closed-source frontier models across τ-bench, τ2-Bench, and ACEBench
- Two-phase SFT strategy — broad foundation training across general domains, then domain-specific specialization — substantially outperforms single-stage training on agentic benchmarks, with Stage 2 multi-step training further boosting complex agent task scores
- Database-grounded trajectory generation enables automated rule-based filtering of agentic training data at two complementary granularities: environment state consistency and exact tool-sequence matching — no human evaluation required
- Compact 4B-parameter agent trained on English synthetic function-calling data generalizes out-of-distribution to Chinese language tasks, surging from 6.7 to 38.4 on the Agent subset and gaining 21.7 overall points on ACEBench-zh without Chinese-specific training

## Limitations

- Task accuracy for agentic models drops sharply as the number of tool calls in a trajectory increases — tasks requiring extended tool chains (>8 calls) approach zero accuracy, making complex multi-step workflows practically unsolvable
- Current LLMs show significant consistency instability — performance degrades substantially across repeated independent trials of the same task (pass^k metric collapses with increasing k), indicating correctness is probabilistic rather than robust
- Specialized tool-calling models (xLAM-2 series) achieve near-zero performance on multi-turn Agent tasks (0%, 5%, 38.4% for 8B/32B/70B) despite reasonable single-turn scores, revealing a fundamental gap between single-call proficiency and multi-turn agentic planning
- The AgentScaler framework relies entirely on supervised fine-tuning — RL integration with the simulated environment, though explicitly recognized as theoretically ideal, has not been implemented, leaving significant potential gains unrealized
- Framework validated only at ≤30B parameter scale — generalization and scalability to 200B+ or trillion-parameter models is untested and unknown
- Closed-source frontier LLMs (GPT-o3, Gemini-2.5-Pro, Claude Sonnet 4) maintain a persistent performance advantage over open-source models on agentic benchmarks — the gap attributable to industrial-scale training pipelines and proprietary optimization strategies not accessible to open-source approach
- Real-world API environments are impractical for large-scale agent training — frequent MCP service calls create prohibitive cost, latency, and reliability challenges, blocking online RL training
- LLM-simulated tool environments suffer from hallucination and response inconsistency — generated tool responses are plausible but not reliably correct or state-consistent, making them unreliable training signal sources
- Simulated forward agent-human interplay trajectories lack naturalness compared to real human-agent interactions, creating a potential distribution gap that may limit generalization to real-world deployment contexts
- Domain specialization training (Stage 2) causes capability regression on out-of-domain task categories — AgentScaler-4B loses 15.3 points on the Special subset of ACEBench-zh vs. its base model, indicating partial catastrophic forgetting during specialization

## Bottlenecks

- Long-horizon agentic task accuracy degrades sharply and reliably with tool call chain length — tasks requiring >8 sequential tool invocations remain practically unsolvable for all current models including state-of-the-art, blocking deployment on complex real-world workflows
- Agentic training data scarcity — collecting diverse, high-quality trajectories of agents interacting with environments via tool calls is fundamentally constrained by the cost and complexity of environment construction across domains
- Real-world API environments are too costly and unstable for online RL training — MCP service call costs and reliability issues prevent RL training loops from running at the scale and speed needed, keeping agent RL confined to offline SFT

## Breakthroughs

- Principled automated construction of 1,000+ verifiable, executable agent training environments from 30,000+ real-world APIs using tool dependency graph clustering and programmatic database materialization — fully eliminating manual environment engineering

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/qwen3|Qwen3]]
- [[entities/passk-metric|pass^k metric]]
- [[entities/τ-bench|τ-Bench]]
- [[entities/τ2-bench|τ2-bench]]
