---
type: source
title: 'Agent models: Internalizing Chain-of-Action Generation into Reasoning models'
source_id: 01KJV3DVFC97VTBMSKRB726WDH
source_type: paper
authors:
- Yuxiang Zhang
- Yuqi Yang
- Jiangming Shu
- Xinyan Wen
- Jitao Sang
published_at: '2025-03-09 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agent models: Internalizing Chain-of-Action Generation into Reasoning models

**Authors:** Yuxiang Zhang, Yuqi Yang, Jiangming Shu, Xinyan Wen, Jitao Sang
**Published:** 2025-03-09 00:00:00
**Type:** paper

## Analysis

# Agent models: Internalizing Chain-of-Action Generation into Reasoning models
2025-03-09 · paper · Yuxiang Zhang, Yuqi Yang, Jiangming Shu, Xinyan Wen, Jitao Sang
https://arxiv.org/pdf/2503.06580

---

### Motivation & Prior Limitations
Traditional agentic workflows (e.g., ReAct, Reflexion) rely on external prompts and scripted pipelines to manage tool usage and environmental interaction, making tool invocation a "passive" behavior driven by preset workflows rather than internalized model capability.
- Reasoning models like DeepSeek-R1 and o1 excel at Chain-of-Thought (CoT) generation but cannot autonomously decide when and how to invoke external tools; the switching between thought and action is triggered by the surrounding prompt context rather than by the model's own learned behavior.
  - R1-Distill-Qwen-7B in zero-shot (model-only) achieves only 11.8% average EM on open-domain QA, and even with ReAct prompting, performance drops further to 15.2% average EM — demonstrating that workflow-based augmentation does not effectively leverage reasoning model capabilities.
- Fine-tuning reasoning models for action execution risks catastrophic forgetting of CoT generation ability, and online RL with real tool calls incurs high cost, low efficiency, and instability due to dynamic environments.
  - Web search interactions during training impose latency and non-stationarity; the dynamic internet makes environment responses inconsistent across training steps, complicating policy gradient estimation.

---

### Proposed Approach
The paper introduces **Large Agent Models (LAMs)** — a conceptual framing for reasoning models that internalize Chain-of-Action (CoA) generation — and proposes **AutoCoA**, a multi-stage SFT+RL training framework to achieve this internalization end-to-end.
- AutoCoA addresses the reasoning-action balance challenge by mixing pure CoT data (without tool usage) throughout all training stages, preventing the model from forgetting reasoning capabilities and forcing it to learn context-dependent tool triggering.
  - Three SFT sub-stages progressively inject capability: (1) **CoT+A** uses contrastive learning on paired trajectories that diverge at a specific prefix — one with an `<action>` token leading to correct answers, one without — training the model when to trigger actions via a combined contrastive + auxiliary SFT loss; (2) **CoT+CoA with observation mask** trains full reasoning-action trajectories while masking environment response tokens from the loss, teaching how to formulate action types and parameters; (3) **CoT+CoA without observation mask** adds prediction of environment responses alongside action generation, equipping the model with an implicit internal world model.
- The RL stage uses **GRPO (Group Relative Policy Optimization)** with exact-match and format-adherence rewards, proceeding in two sub-stages: first training exclusively in a simulated environment (using the model's own internal world model to generate observations), then fine-tuning on real environment interactions.
  - The simulated RL stage allows extensive, low-cost rollouts to explore diverse CoA strategies; only a limited fraction of real tool calls (1/6 of total RL steps) is needed to adapt to real-world dynamics, with the internal world model bootstrapping convergence.
- Inference is formalized as a POMDP where the policy generates one of three token types at each step — `<think>` (CoT), `<action>` (CoA with tool type and parameters), or `<answer>` — with the environment response appended to the trajectory as context for subsequent steps.
  - This is structurally distinct from ReAct, where tool invocation is triggered by prompt templates; here the model has been end-to-end trained with task completion as the explicit optimization objective, considering both preceding and subsequent context.

---

### Results & Capabilities
AutoCoA-trained agent models substantially outperform both model-only baselines and ReAct-based agentic workflows across all six evaluated QA benchmarks (NQ, TriviaQA, HotpotQA, 2WikiMultihopQA, MuSiQue, Bamboogle).
- The best overall configuration (SFT-stage1&2 + RL-stage2) achieves 33.9% average EM and 38.5% average LLM accuracy, compared to 15.2% EM / 18.5% LLM for R1-Distill-Qwen-7B with ReAct — more than doubling task completion on the same base model.
  - On multi-hop benchmarks where long-horizon reasoning is critical, gains are especially pronounced: HotpotQA improves from 15.1% EM (ReAct) to 35.6% EM; 2WikiMultihopQA improves from 21.3% EM (ReAct) to 48.4% EM.
- Separating CoA training into explicit when-to-act (stage1) and how-to-act (stage2) sub-stages consistently outperforms using stage2 alone: SFT-stage1&2 reaches 32.0% EM vs. 29.5% EM for SFT-stage2 only.
- The internal world model approach (SFT-stage1&2&3 + RL-stage1&2 at 83% simulated / 17% real interactions) achieves 33.4% average EM, compared to 33.9% EM for full real-environment RL — demonstrating near-parity with dramatically reduced real tool calls.
- Long-horizon task analysis shows that after CoA learning, agent models maintain high success rates even at 5 sequential actions, while the initial policy with ReAct workflow shows monotonically declining success rates as action count increases.

---

### Implications
The work operationalizes a conceptually important paradigm shift: just as CoT prompting was superseded by reasoning models that internalize multi-step deliberation, agentic workflows built on ReAct-style prompting are likely to be superseded by models that internalize tool invocation as a learned behavior — with qualitatively better long-horizon coherence.
- The staged SFT→simulated RL→real RL curriculum provides a practical training recipe that substantially reduces real environment interaction costs, which has direct implications for training agents that use expensive APIs, physical robots, or live production systems.
- The internal world model mechanism — where the model predicts its own tool 

## Key Claims

1. Traditional agentic workflows rely on external prompts to manage interactions with tools and the environment, which limits the autonomy of reasoning models.
2. AutoCoA-trained agent models significantly outperform ReAct-based workflows in task completion, especially in tasks requiring long-term reasoning and multi-step actions.
3. OpenAI's Deep Research and Operator are believed to use end-to-end fine-tuned models that actively decide when and how to use tools, rather than merely orchestrating existing LLMs with agentic workflo
4. In agentic workflows, switching between thought and action is 'passive' behavior triggered by preset workflows, whereas in agent models the switching is based on the model's inherent, 'active' learned
5. The model behind OpenAI's Deep Research has undergone end-to-end fine-tuning on the basis of reasoning models for tool usage, considering not only preceding but also subsequent context, with task comp
6. The shift from agentic workflows to agent models that internalize Chain-of-Action generation is expected to gradually replace static and scripted workflows.
7. Agent model inference can be formalized as a partially observable Markov decision process (POMDP) where the state comprises initial environment state, task context, and the generated sequence so far.
8. Fine-tuning reasoning models to enhance action execution capabilities risks the model forgetting its Chain-of-Thought generation ability.
9. Interacting with the external environment through tool invocations during training results in high training costs, low efficiency, and risks due to dynamic environmental changes causing instability.
10. Deep Research's agent model is built by end-to-end reinforcement fine-tuning atop the flagship reasoning model o3, with web search as the main action.

## Capabilities

- Reasoning models can internalize Chain-of-Action (CoA) generation via SFT+RL training (AutoCoA), enabling autonomous decisions on when and how to invoke external tools without relying on external prompts or scripted agentic workflows
- AutoCoA-trained 7B agent models substantially outperform ReAct-based agentic workflows on open-domain QA, averaging 33.9% EM vs 15.2% EM for the same reasoning base model with ReAct — a 2x+ improvement
- AutoCoA agent models maintain high task success rates as the number of required sequential actions increases to 5+, whereas ReAct-based workflows show consistently declining success rates with more actions
- Reasoning models can be trained to simulate environment feedback internally (implicit world model from SFT stage 3), enabling RL training primarily in a simulated sandbox and reducing real-environment interaction to just ~1/6 of total RL training steps while achieving comparable performance
- Contrastive learning on paired reasoning trajectories (with vs. without tool invocation at the same prefix) teaches models to autonomously determine when internal knowledge is insufficient and external tool use is required

## Limitations

- AutoCoA has only been validated on small-scale (7B) models using a single tool type (web search) and one task domain (open-domain QA); scalability to larger models, diverse tools, and open-ended tasks is entirely unverified
- Fine-tuning reasoning models to add action generation capabilities risks catastrophic forgetting of Chain-of-Thought generation ability — a fundamental challenge requiring careful multi-stage training and data mixing to mitigate
- RL training for agent models with real external environment calls (web search APIs) is expensive, slow, and unstable — API latency, rate limits, and dynamic environment state cause training instability and high costs, blocking scalable end-to-end agent training
- The internal world model's simulation fidelity is insufficient — switching from simulated to real environment interaction still improves performance, confirming the world model cannot fully substitute for real feedback
- AutoCoA's RL reward is restricted to exact-match ground truth — this constrains the framework to closed-form tasks with verifiable outputs and completely blocks application to open-ended tasks (writing, analysis, research summarization) without a different reward mechanism
- Reasoning models paired with ReAct workflows perform worse than plain base models with ReAct (15.2 vs 19.6 average EM) — suggesting chain-of-thought reasoning capability interferes with or is fundamentally incompatible with externally scripted tool invocation
- Direct RL application without SFT initialization yields only marginal gains ('constrained by the initial policy's baseline capacity'), indicating RL alone cannot bootstrap agentic tool-use capabilities from a reasoning model
- Agent models still fail on harder multi-hop tasks: best AutoCoA performance on MuSiQue (4-hop) is only 12.6% EM, exposing a performance cliff on tasks requiring deep compositional multi-step reasoning and information integration
- Knowledge research agents (like Deep Research) are limited to open-domain web data with shallow expert analysis and cannot perform deep domain-specific consulting in law, medicine, or science without proprietary data fine-tuning
- No security or adversarial robustness discussion for agent models interacting with live web environments — prompt injection from hostile web pages is a conspicuously absent concern given the threat model of web-browsing agents
- Current GUI interfaces (web pages, apps) designed for human interaction are inefficient for agent operation; no agent-native protocol exists yet for tool, memory, and agent-to-agent interaction at the OS level
- Transformer token-based sequential representations are architecturally ill-suited for an Agent OS requiring unified multimodal I/O representations and a general agent instruction set — a structural limitation for long-term agent ecosystem development
- Multi-stage AutoCoA training pipeline requires five sequential training substages with separately curated datasets, implying high engineering overhead and data infrastructure requirements that may limit adoption outside well-resourced labs

## Bottlenecks

- End-to-end RL training for agent models requires real environment tool calls (web search, APIs) that are expensive, slow, and unstable due to latency and dynamic state — blocking scalable training of Large Agent Models via online RL
- World model fidelity for agent RL simulation is insufficient — learned internal environment simulators cannot faithfully replicate real tool responses, preventing full substitution of simulated for real training interactions
- Exact-match verifiable reward signals constrain agent RL to closed-form tasks, blocking AutoCoA-style training from extending to open-ended agentic tasks (research synthesis, domain analysis, creative) where no ground truth string exists

## Breakthroughs

- AutoCoA demonstrates that end-to-end SFT+RL training can internalize Chain-of-Action generation into reasoning models — establishing a training recipe that fundamentally shifts agent capability from prompt-scripted tool use to learned autonomous tool invocation

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/bamboogle|Bamboogle]]
- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/exact-match-em|Exact Match (EM)]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/musique|MuSiQue]]
- [[entities/react|ReAct]]
- [[entities/triviaqa|TriviaQA]]
- [[entities/verl|verl]]
