---
type: source
title: Multi-Agent Tool-Integrated Policy Optimization
source_id: 01KJTEKYPYV766863NYBAZYYCN
source_type: paper
authors:
- Zhanfeng Mo
- Xingxuan Li
- Yuntao Chen
- Lidong Bing
published_at: '2025-10-06 00:00:00'
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
# Multi-Agent Tool-Integrated Policy Optimization

**Authors:** Zhanfeng Mo, Xingxuan Li, Yuntao Chen, Lidong Bing
**Published:** 2025-10-06 00:00:00
**Type:** paper

## Analysis

# Multi-Agent Tool-Integrated Policy Optimization
2025-10-06 · paper · Zhanfeng Mo, Xingxuan Li, Yuntao Chen, Lidong Bing
https://arxiv.org/pdf/2510.04678

---

### Motivation & Prior Limitations
Single-agent tool-integrated planning (TIP) frameworks suffer from two compounding failure modes that become critical in complex, multi-hop research tasks: context window saturation from verbose tool responses and reasoning degradation from noisy, out-of-distribution tool outputs.
- Iterative multi-turn interactions with search and scraping tools rapidly fill a single agent's context, making long-horizon reasoning chains prohibitive under typical LLM context limits.
- Tool responses (web scraping, search APIs) are structurally noisy and deviate significantly from LLM generation distributions, inducing cascading planning errors and degraded subsequent actions.
- While multi-agent planner/worker frameworks exist as inference-time solutions via prompt engineering, no principled reinforcement learning training methodology existed for such architectures prior to this work.
- Deploying separate models per agent role introduces infrastructure challenges: uneven workloads, higher memory consumption, and incompatibility with standard single-model RL frameworks like veRL or GRPO.

---

### Proposed Approach
MATPO (Multi-Agent Tool-Integrated Policy Optimization) encodes multiple agent roles — planner and worker — within a **single LLM instance**, differentiated only by distinct system prompts, and derives a principled policy gradient objective that performs credit assignment across both planner and worker rollouts jointly.
- Unlike prior multi-agent setups requiring separate model deployments (multi-agent-multi-model), MATPO operates in a "multi-agent-in-one-model" configuration using a single rollout engine, maintaining full compatibility with off-the-shelf RL frameworks such as veRL.
- The MATPO objective extends GRPO by normalizing advantages across G×(T+1) rollouts — one planner rollout plus T worker rollouts per query — rather than GRPO's G worker rollouts, so that the final verifiable accuracy reward propagates credit back through both planner decisions and worker subtask executions.
  - Worker agents receive no independent reward signal; their gradient contribution is inherited from the planner's end-to-end accuracy reward, with advantages broadcast from the planner rollout to all associated worker rollouts.
  - The policy gradient derivation shows that ∇θ log Pθ(τ) decomposes cleanly into a sum over planner token log-probabilities and worker token log-probabilities, with tool response tokens masked out throughout (∇θPTool = 0), making the credit assignment mathematically grounded rather than heuristic.
- Implementation nests worker rollout functions asynchronously inside the outer planner rollout, then concatenates planner and worker data into an augmented training batch for a single forward/backward pass on πθ.
- A "user query recapping" technique embeds the original user query into the worker agent's system prompt, providing explicit goal alignment between delegated subtasks and the top-level query.
- A final-summary mechanism forces each worker to produce a structured answer block at rollout end, providing the planner with a clean, distilled interface rather than raw tool-interleaved trajectories.

---

### Results & Capabilities
MATPO consistently outperforms single-agent GRPO across all three evaluation benchmarks — GAIA-text, WebWalkerQA, and FRAMES — achieving an average relative improvement of **18.38%**.
- On GAIA-text, MATPO reaches 42.60% vs. 32.16% for single-agent GRPO; on WebWalkerQA, 33.00% vs. 30.14%; on FRAMES, 63.64% vs. 56.22%.
- MATPO exhibits more stable training dynamics: single-agent GRPO shows performance collapse after step 120 on GAIA-text and FRAMES, while MATPO continues improving — attributed to the worker's ability to launch additional browsing subtasks when primary search returns noisy or incomplete results.
- Ablation studies confirm that the worker final-summary mechanism is a necessary component: removing it degrades performance substantially, as raw worker outputs containing `<think>` blocks and terminal tool-call blocks actively distract planner reasoning.
- User query recapping in the worker system prompt produces a substantial performance gain, suggesting that subtask context alone (without the original query) is insufficient for stable worker behavior during RL training.
- Blocking benchmark-adjacent URLs (e.g., HuggingFace) from the search API has only mild effect on measured accuracy, indicating the risk of reward hacking via direct retrieval of ground-truth answers is low but non-zero.
- All experiments use Qwen3-14B-base as the base model, trained on a filtered subset of MuSiQue (multi-hop QA), and evaluated zero-shot on held-out benchmarks; 128 A800 GPUs were required for training.

---

### Implications
MATPO establishes that a single LLM can be trained end-to-end to occupy multiple agent roles simultaneously, opening a path toward memory-efficient multi-agent RL that does not require separate model deployments or bespoke multi-model infrastructure.
- The principled credit assignment derivation — showing that the GRPO policy gradient extends naturally to hierarchical planner/worker rollouts — provides a theoretical foundation for scaling multi-agent RL beyond two-role systems.
- The result that a single model improves by being exposed to *both* planner and worker experience during RL training suggests that role diversity in training trajectories may function as a form of curriculum or perspective augmentation, with implications for how future agentic post-training pipelines are designed.
- For the reinforcement learning with verifiable rewards (RLVR) line of research, MATPO demonstrates that context management and noise isolation are training-time concerns, not just inference-time engineering choices — multi-agent decomposition actively improves gradien

## Key Claims

1. Tool responses are often noisy and their distribution deviates significantly from LLM generation distribution, disrupting reasoning and inducing cascading errors.
2. No existing methods support effective reinforcement learning post-training of tool-integrated multi-agent frameworks.
3. Existing multi-agent inference-time frameworks rely solely on prompt engineering and provide no training methodology for multi-agent tool-integrated planning.
4. MATPO enables planner and worker agent roles to be trained within a single LLM instance using role-specific prompts via reinforcement learning.
5. MATPO is derived from a principled credit assignment mechanism across planner and worker rollouts.
6. MATPO outperforms single-agent baselines by an average of 18.38% relative improvement across three benchmarks.
7. MATPO achieves 42.60% on GAIA-text, 33.00% on WebWalkerQA, and 63.64% on FRAMES, compared to 32.16%, 30.14%, and 56.22% for single-agent GRPO.
8. MATPO exhibits greater robustness to noisy tool outputs than single-agent GRPO.
9. Single-agent GRPO suffers catastrophic performance drops after step 120 on GAIA-text and FRAMES, while MATPO continues to improve.
10. A key challenge in multi-agent RL is credit assignment: worker agents address unverifiable subtasks, making it non-trivial to assess their contribution to the planner's final accuracy.

## Capabilities

- A single LLM trained with MATPO can play both planner and worker roles via role-specific system prompts, achieving an average 18.38% relative improvement over single-agent GRPO on deep research benchmarks (GAIA-text: 42.60%, WebWalkerQA: 33.00%, FRAMES: 63.64%).
- Principled credit assignment in multi-agent RL via reward broadcast — a single accuracy reward at the planner level can be propagated to worker rollouts through shared advantage normalization across G×(T+1) rollouts, enabling gradient flow through hierarchical agent structures where worker subtasks 
- Multi-agent planner/worker decomposition during RL training isolates noisy tool responses within worker local context, preventing context saturation and reasoning disruption in the planner and producing more stable training trajectories than single-agent approaches.
- Worker-agent final summary mechanism — instructing worker agents to produce a distilled answer before returning control to the planner — significantly improves multi-agent RL training stability and accuracy by providing clean inter-agent interfaces that filter raw tool outputs and thinking blocks.

## Limitations

- Single-agent TIP systems face fundamental context window saturation: lengthy tool responses and multi-turn interaction histories rapidly exhaust available context, preventing scalability to deeper reasoning chains.
- Noisy tool responses from web search and scraping disrupt LLM reasoning through distributional mismatch — their content distribution deviates significantly from the LLM's generation distribution, inducing cascading reasoning errors in single-agent settings.
- Multi-agent-multi-model RL training requires (K+1) LLM rollout engines, introduces uneven workload distribution across agents, substantially more token context, and higher memory consumption than single-agent alternatives — creating significant infrastructure barriers.
- MATPO training requires 128 A800 GPUs, indicating extremely high compute cost that makes this research inaccessible to most groups and impractical for rapid iteration.
- Single-agent GRPO training exhibits catastrophic performance collapse during extended training runs (after step 120 on GAIA-text and FRAMES), caused by unstable environmental feedback from noisy search APIs, making single-agent agentic RL fundamentally brittle for deep research tasks.
- Planner agents develop a systematic compliance bias when worker outputs are formatted as 'user messages' — they initially detect errors in worker responses but fail to maintain their objections, accepting incorrect search directions and compounding downstream errors.
- MATPO evaluation is restricted to a single model family (Qwen3-14B), a single task domain (web search/deep research), and a single topology (one planner + one worker), with no evidence of generalization to other model sizes, task types, or agent configurations.
- Agentic RL training with web search access is vulnerable to reward hacking: models can retrieve query-answer pairs directly from dataset hosting sites (e.g., HuggingFace) to trivially satisfy accuracy rewards without genuine reasoning.
- Context management at token limit is handled by naive recency-based truncation — removing the most recent messages — potentially discarding the most relevant recent tool evidence precisely when it matters most in long agentic rollouts.
- Scaling behavior of multi-agent-in-one-model RL beyond one planner + one worker is entirely unexplored — whether adding more specialized agent roles (coding, file-processing) degrades, maintains, or improves capability is unknown, blocking principled architecture design.
- The mechanism by which original user query recapping improves worker agent performance remains unexplained — authors hypothesize without mechanistic analysis, leaving this critical engineering decision on an empirical footing only.

## Bottlenecks

- Absence of training methodology for multi-agent tool-integrated planning — prior to MATPO, all multi-agent frameworks for complex reasoning tasks existed only as inference-time prompt engineering designs, with no RL post-training path.
- Planner compliance bias from inter-agent message format — framing worker outputs as 'user messages' makes planner agents systematically defer to incorrect worker responses, requiring alternative message construction formats to achieve reliable hierarchical error correction.
- Scaling laws for multi-agent-in-one-model RL are entirely unknown — no theoretical framework or empirical data exists to guide decisions about how many agent roles a single model can productively learn, or whether emergent capability improvements arise from role diversity.
- Agentic RL infrastructure is unoptimized for multi-agent multi-turn training — current implementations rely on workarounds (nested asynchronous rollout functions) that are inefficient, brittle, and inaccessible without large GPU clusters.

## Breakthroughs

- MATPO establishes the first principled end-to-end RL training framework for hierarchical multi-agent tool-integrated planning, enabling a single LLM to be trained simultaneously across planner and worker roles via a theoretically derived credit assignment mechanism.

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/musique|MuSiQue]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/verl|verl]]
