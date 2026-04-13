---
type: source
title: 'AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through
  Multi-Turn Reinforcement Learning'
source_id: 01KJTK494KTKNRTXJDVJ25RESE
source_type: paper
authors:
- Zhiheng Xi
- Jixuan Huang
- Chenyang Liao
- Baodai Huang
- Honglin Guo
- Jiaqi Liu
- Rui Zheng
- Junjie Ye
- Jiazheng Zhang
- Wenxiang Chen
- Wei He
- Yiwen Ding
- Guanyu Li
- Zehui Chen
- Zhengyin Du
- Xuesong Yao
- Yufei Xu
- Jiecao Chen
- Tao Gui
- Zuxuan Wu
- Qi Zhang
- Xuanjing Huang
- Yu-Gang Jiang
published_at: '2025-09-10 00:00:00'
theme_ids:
- agent_systems
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning

**Authors:** Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo, Jiaqi Liu, Rui Zheng, Junjie Ye, Jiazheng Zhang, Wenxiang Chen, Wei He, Yiwen Ding, Guanyu Li, Zehui Chen, Zhengyin Du, Xuesong Yao, Yufei Xu, Jiecao Chen, Tao Gui, Zuxuan Wu, Qi Zhang, Xuanjing Huang, Yu-Gang Jiang
**Published:** 2025-09-10 00:00:00
**Type:** paper

## Analysis

# AgentGym-RL: Training LLM Agents for Long-Horizon Decision Making through Multi-Turn Reinforcement Learning
2025-09-10 · paper · Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo et al. (23 total)
https://arxiv.org/pdf/2509.08755

---

### Motivation & Prior Limitations
The community lacked a unified, end-to-end, interactive multi-turn RL framework proven effective across diverse real-world environments for training LLM agents without requiring supervised fine-tuning (SFT) as a preliminary step.
- Most RL-for-LLM work (including DeepSeek-R1) is restricted to single-turn, static tasks where models do not engage in multi-turn interaction with complex environments, making learned behaviors fundamentally inadequate for sequential decision-making.
- Recent efforts extending RL to multi-turn agents are limited in task complexity and environment diversity, and frequently encounter optimization instability — particularly around the exploration-exploitation trade-off at long horizons.
  - Starting with a large number of interaction turns leads the model into redundant reasoning and unproductive actions, causing training collapse; starting with too few constrains exploration and imposes a performance ceiling.
- Existing alternatives — prompting-based agents with self-reflection, and imitation learning from expert trajectories — either depend on powerful proprietary models without training the underlying model, or are expensive, hard to scale, and prevent self-improvement through environmental interaction.

---

### Proposed Approach
The paper introduces AgentGym-RL, a modular, decoupled RL framework for multi-turn interactive decision-making that cleanly separates Environment, Agent, and Training components into plug-and-play modules, and trains agents from scratch using only environment reward signals across five distinct scenario types.
- The framework models agentic tasks as a Partially Observable Markov Decision Process (POMDP) and supports four mainstream on-policy RL algorithms — PPO, GRPO, REINFORCE++, and RLOO — alongside SFT, DPO, and rejection sampling (AgentEvol) for comparison.
  - A standardized server-client architecture with unified HTTP protocols enables parallel rollout across isolated environment instances, with engineering fixes addressing memory leaks (TextCraft's recursive crafting_tree, SciWorld's clock mechanism) and concurrency failures (SciWorld initialization, WebArena's single-browser-per-process bottleneck).
- The core methodological contribution is ScalingInter-RL, a progressive interaction-horizon curriculum that begins training with a short maximum turn budget (emphasizing exploitation of foundational skills on simple tasks) and monotonically increases the horizon according to schedule {h₁ < h₂ < ··· < hₙ} with increment δh every Δ training steps.
  - This staged scaling draws explicit analogy to inference-compute scaling in reasoning models (o1, DeepSeek-R1), but operates on external agent-environment interactions rather than internal chain-of-thought length — and does not prescribe how the agent allocates additional compute, letting it learn planning, reflection, and strategic backtracking organically.
  - Unlike TTI (which uses rejection sampling to teach agents to allocate compute for thinking in web navigation), ScalingInter-RL uses on-policy RL and scales interactions directly, making the agent responsible for its own compute allocation strategy.
- GRPO is identified as superior to REINFORCE++ for multi-turn agentic tasks: by normalizing rewards within groups of sampled actions per state and applying PPO-style clipping, GRPO provides more stable, lower-variance gradient estimates better suited to the sparse-reward, long-horizon credit assignment problem.

---

### Results & Capabilities
A Qwen2.5-7B model trained with AgentGym-RL + ScalingInter-RL achieves an average improvement of 33.65 points over the base model across five tasks, matching or surpassing commercial closed-source models including OpenAI o3 and Gemini-2.5-Pro.
- On WebArena (web navigation), ScalingInter-7B achieves 26.00% overall, surpassing GPT-4o (16.00%) and matching DeepSeek-R1-0528 (28.00%) and Gemini-2.5-Pro (28.00%), with ScalingInter-7B achieving 33.33% in Shopping — matching the best any model achieves in that subcategory.
- On Deep Search, ScalingInter-7B reaches 38.25% overall, surpassing GPT-4o (26.75%) and Gemini-2.5-Pro (36.50%), and tying OpenAI o3 on TriviaQA (70.00%) and achieving highest overall on NQ (52.00%) — without explicit long-chain-of-thought reasoning.
- On SciWorld (scientific tasks), ScalingInter-7B sets a new state-of-the-art at 57.00, substantially exceeding the next-best model OpenAI o3 (41.50); AgentGym-RL boosted the base model from 1.50 to 50.50 — a gain of nearly 50 points — demonstrating that structured RL training is particularly effective in environments with clear causal feedback.
- On BabyAI (embodied navigation), ScalingInter-7B achieves 96.67% overall, outperforming OpenAI o3 (94.44%) and GPT-4o (86.67%), with perfect scores on GoTo, ActionObjDoor, and SynthLoc subtasks.
- Post-training and test-time compute scaling outperform model size scaling: the 7B ScalingInter-RL model (58.6% average) surpasses Llama3.1-70B (~47%) and Qwen2.5-72B (~43%), which have nearly 10× more parameters.
- Test-time interaction scaling is validated independently: all models show clear accuracy gains as maximum interaction turns increase at inference, and Pass@K performance improves with parallel sampling — with the RL-trained model maintaining a lead over baselines at every sampling budget (e.g., 5.5% improvement on Deep Search and 7.05% on SciWorld at K=64).
- GRPO consistently outperforms REINFORCE++ across all tasks, with GRPO-3B exceeding REINFORCE++-7B on TextCraft (75 vs. 73) and BabyAI (93.33 vs. 84.44), indicating algorithmic choice is more impactful than model scale in these settings.

---

### Implications
AgentGym-RL provides empirical evidence 

## Key Claims

1. The community lacks a unified, end-to-end, interactive multi-turn RL framework proven effective across a wide range of real-world scenarios for training LLM agents without SFT as a preliminary step.
2. Most existing RL studies for LLMs are restricted to single-turn tasks where models are not required to engage in multi-turn interaction with complex environments.
3. AgentGym-RL achieves an average improvement of 33.65 points over the base Qwen-2.5-7B model, matching or outperforming larger commercial closed-source models such as OpenAI-o3 and Gemini-2.5-Pro.
4. Beginning RL training with a large number of interaction turns leads to redundant reasoning, unproductive actions, training collapse, and degraded performance.
5. Constraining interaction turns to remain consistently small narrows exploration and limits the agent's ability to master diverse patterns.
6. ScalingInter-RL delivers more than a 10% improvement on WebArena over baseline RL, bringing performance close to that of closed-source commercial models.
7. ScalingInter-RL surpasses the base model by 30 points on the TextCraft benchmark, achieving state-of-the-art results.
8. Using a large maximum interaction turn (e.g., 10) achieves higher performance early in training but rapidly collapses as training progresses, compared to shorter-turn settings (e.g., 5).
9. Post-training and test-time compute show higher scaling potential than increasing model parameter count.
10. A 7B model trained with ScalingInter-RL achieves ~58.6% average success rate, outperforming Llama3.1-70B (~47%) and Qwen2.5-72B (~43%) which have nearly ten times the parameters.

## Capabilities

- Multi-turn reinforcement learning can train LLM agents for long-horizon decision-making entirely from scratch — without any supervised fine-tuning prerequisite — achieving performance matching or exceeding commercial frontier models like OpenAI o3 and Gemini-2.5-Pro across diverse agentic benchmarks
- Progressive interaction horizon scaling (ScalingInter-RL) enables stable long-horizon RL optimization by starting with short interaction budgets to build foundational skills, then gradually expanding the horizon — preventing the training collapse seen with fixed large horizons and outperforming fixe
- Post-training RL and test-time compute scaling yields higher efficiency gains for agentic tasks than raw model parameter scaling — a 7B RL-trained model (58.6%) substantially outperforms 70B and 72B untuned models (~47%, ~43%)
- Test-time sequential interaction scaling produces clear performance gains in RL-trained agents — allocating more environment interaction turns at inference time allows agents to explore more thoroughly and reach better outcomes
- GRPO substantially outperforms REINFORCE++ for multi-turn agentic RL training — the algorithmic advantage exceeds the benefit of doubling model scale from 3B to 7B, attributed to relative action advantage estimation that stabilises gradients under sparse, long-trajectory rewards

## Limitations

- Complex multi-step chemical simulation and mixing is completely intractable for all current LLMs — every model tested (including GPT-4o, OpenAI o3, Gemini-2.5-Pro, and RL-trained 7B models) scored zero on the Chem-Mix subtask
- Fixed large interaction horizons during RL training cause catastrophic collapse — starting with long interaction budgets before foundational skills are established leads to redundant reasoning, unproductive actions, and irreversible training instability
- RL performance gains are highly environment-structure dependent — RL delivers dramatic improvements in structured rule-based environments (TextCraft: +77pts, SciWorld: +49pts) but only moderate gains in open-ended real-world environments (WebArena, Deep Search)
- RL-trained agents do not generalise to novel environments and unfamiliar tools — training produces in-domain specialists with strong within-domain performance but unknown transfer to out-of-distribution settings
- RL-trained agents develop over-interaction patterns in web navigation — redundant clicking, unnecessary hovering, and excessive scrolling impede task completion even after successfully locating the correct page, revealing a gap between state-reaching and efficient action selection
- RL-trained agents substitute parametric recall for experimental procedure in scientific tasks — facing interaction failures, agents report known facts instead of executing systematic debugging, and terminate exploration prematurely rather than completing full comparative analyses
- All experiments are confined to text-based digital simulated environments — the entire framework avoids real-world physical grounding, actual hardware deployment, and sensory-rich inputs, with authors explicitly flagging this as an open challenge
- Multi-agent coordination and collective intelligence are entirely absent from the framework — all training and evaluation is single-agent, leaving emergent cooperation, competitive dynamics, and role specialisation unaddressed
- Persistent performance gap on complex structured-repository interaction tasks (GitLab/Reddit) — RL-trained 7B models trail OpenAI o3 (34%) and o4-mini (36%) by a margin concentrated in tasks requiring multi-hop reasoning over code repositories and community forums
- REINFORCE++ produces high-variance gradient estimates in long-trajectory agentic tasks — full-episode Monte Carlo returns are sensitive to stochastic successes and failures across many turns, causing unstable learning under sparse multi-turn rewards
- Maximum compositional planning depth remains a near-universal failure mode — Depth-4 tasks in TextCraft score zero for nearly all models (including GPT-4o, Qwen3-235B, DeepSeek-R1), indicating a hard ceiling on compositional planning in current LLMs
- Shorter fixed interaction horizons produce a performance ceiling — constraining agents to too few turns limits exploration breadth and causes diminishing returns in later training stages, revealing a fundamental tension between stability and capability

## Bottlenecks

- Multi-turn agent RL training is blocked by engineering fragility in simulation environments — memory leaks, broken parallel instantiation, missing full-reset interfaces, and single-threaded browser architectures require substantial per-environment engineering before large-scale RL training is feasib
- Complex multi-step scientific simulation is a blocking unsolved bottleneck — LLMs universally fail tasks requiring procedural chemical or physical state simulation, regardless of scale, reasoning training, or RL fine-tuning
- RL agent generalisation is blocked by in-domain specialisation — training in one set of environments produces specialists that cannot transfer policies to novel environments, tools, or task distributions without retraining

## Breakthroughs

- End-to-end multi-turn RL training from scratch — without SFT prerequisite — closes the open/closed source performance gap on diverse agentic benchmarks, with 7B models matching or exceeding GPT-4o, Gemini-2.5-Pro, and OpenAI o3
- Post-training RL compute is empirically established as a more impactful scaling axis than parameter count for agentic intelligence — 7B RL-trained model surpasses 70B+ untuned models by a substantial margin across five agentic benchmarks

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/reinforce|REINFORCE++]]
- [[entities/rloo|RLOO]]
- [[entities/sciworld|SciWorld]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/webarena|WebArena]]
- [[entities/verl|verl]]
