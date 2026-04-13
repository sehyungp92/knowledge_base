---
type: source
title: Meta-RL Induces Exploration in Language Agents
source_id: 01KJT4G8AARF15E8ZTQ0N589QB
source_type: paper
authors:
- Yulun Jiang
- Liangze Jiang
- Damien Teney
- Michael Moor
- Maria Brbic
published_at: '2025-12-18 00:00:00'
theme_ids:
- agent_systems
- in_context_and_meta_learning
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Meta-RL Induces Exploration in Language Agents

**Authors:** Yulun Jiang, Liangze Jiang, Damien Teney, Michael Moor, Maria Brbic
**Published:** 2025-12-18 00:00:00
**Type:** paper

## Analysis

# Meta-RL Induces Exploration in Language Agents
2025-12-18 · paper · Yulun Jiang, Liangze Jiang, Damien Teney, Michael Moor, Maria Brbic
https://arxiv.org/pdf/2512.16848

---

### Motivation & Prior Limitations
Standard RL-trained LLM agents learn a fixed policy during training and fail to actively explore or adapt their behavior to novel tasks at test time, causing poor performance on tasks requiring trial-and-error discovery.
- RL agents optimize a single-episode objective where rollouts are independent, providing no structural incentive to gather information early and exploit it later — the explore-then-exploit balance is not learned.
  - Krishnamurthy et al. (2024) specifically documented that LLM agents do not robustly engage in exploration without substantial interventions.
  - Nie et al. (2024) showed RL-trained agents struggle to adapt at test time even across bandit tasks designed to test in-context adaptation.
- Prior works addressing exploration either target single-turn non-agentic reasoning (Setlur et al., 2025; Qu et al., 2025) or rely on offline data (Tajwar et al., 2025; Gandhi et al., 2024), limiting them to imitation of pre-collected strategies rather than active, online exploration in interactive environments.
- Multi-turn agentic tasks have sparse success signals delivered only at episode end, making credit assignment for exploratory actions across attempts structurally difficult under standard RL.

---

### Proposed Approach
LAMER (LLM Agent with Meta-RL) applies a Meta-RL framework to LLM agent training via two components: a cross-episode training scheme that treats multiple sequential attempts at a task as a single trial, and in-context policy adaptation through self-reflection between episodes.

- The cross-episode training framework defines a discounted return G_t^(n) that spans across episodes within a trial, adding a trajectory-level discount factor γ_traj on top of the within-episode discount γ_step, so that the Meta-RL objective J(θ) incentivizes the agent to maximize long-term reward across the full trial rather than a single episode.
  - γ_traj controls the exploration-exploitation trade-off: larger values weight long-horizon cross-episode return and push the agent to explore early; smaller values bias toward immediate exploitation.
  - Unlike standard RL where rollouts are sampled independently for advantage estimation, Meta-RL episodes are conditioned sequentially — each episode's policy π_θ^(n) is updated via the accumulated inter-episode memory H^(n) from all prior episodes and reflections in the trial.
  - The objective is compatible with standard policy gradient optimizers including PPO, GRPO, and GiGPO, requiring no algorithmic changes beyond modified credit assignment.

- In-context policy adaptation uses self-reflection as the inner loop of Meta-RL: after each episode, the agent is prompted to generate a textual reflection summarizing what happened and how to adjust strategy, which is prepended to the context for the next episode.
  - This is structurally equivalent to an in-context RL algorithm — the LLM's parameters serve as meta-parameters (outer loop) while the growing reflection-augmented context serves as the adaptation state (inner loop), naturally leveraging LLMs' in-context learning capability without gradient updates at test time.
  - The reflection step itself is trained with RL reward from the subsequent episode, so the agent learns to generate reflections that actually improve downstream performance rather than generic self-critique.
  - Memory content H^(n) can be truncated via a configurable buffer to manage context length; the default retains full history and all reflections.

- LAMER is, to the authors' knowledge, the first application of a Meta-RL framework specifically to LLM agent training, extending prior in-context Meta-RL work (Duan et al., 2016; Wang et al., 2016 with RNN history-dependent policies) to the language model setting.

---

### Results & Capabilities
LAMER trained on Qwen3-4B achieves consistent performance gains over RL baselines across all four evaluated environments, with 11%, 14%, and 19% absolute performance gains on Sokoban, MineSweeper, and Webshop respectively at test time when the agent is allowed to adapt across episodes.

- LAMER also outperforms prompting baselines (e.g., ReAct, Reflexion) across all environments, demonstrating that the Meta-RL training instills capabilities beyond what zero-shot or few-shot prompting achieves.
- The Meta-RL trained model produces more diverse trajectories than RL-trained models: on MineSweeper, trajectory entropy under LAMER is measurably higher while simultaneously achieving better success rates, demonstrating a favorable exploration-exploitation frontier rather than a simple tradeoff.
  - RL training collapses trajectory diversity as training progresses (standard mode-seeking behavior), whereas LAMER retains diversity closer to the base model's distribution while raising performance — empirically visible in Figure 1 of the paper.
- LAMER demonstrates superior test-time scaling: when evaluated under pass@k (sampling k attempts and taking the best), the Meta-RL trained model shows better scaling curves than the RL baseline, meaning increased test-time compute is more efficiently utilized.
  - The paper explicitly matches training compute budgets between RL and Meta-RL baselines to make this comparison fair, isolating the benefit of the meta-learning objective rather than compute.
- LAMER generalizes better to harder and out-of-distribution tasks than RL-trained agents, including tasks with larger boards (MineSweeper), more complex objectives (Sokoban), and previously unseen environment configurations, suggesting the learned exploration strategy is transferable rather than task-memorized.
- Results also hold on Llama3.1-8B-Instruct as a base model, indicating the framework is not specific to Qwen3-4B architecture.

---

### Implications
Meta-RL provides a principled 

## Key Claims

1. RL-trained LLM agents often struggle in tasks that require active exploration and fail to efficiently adapt from trial-and-error experiences.
2. LAMER achieves 11% absolute performance gain on Sokoban over the RL baseline.
3. LAMER achieves 14% absolute performance gain on MineSweeper over the RL baseline.
4. LAMER achieves 19% absolute performance gain on Webshop over the RL baseline.
5. LAMER demonstrates better generalization to more challenging or previously unseen tasks compared to RL-trained agents.
6. LLM agents do not robustly engage in exploration without substantial interventions.
7. Prior works on inducing exploration in LLMs either focus on single-turn non-agentic reasoning or rely on offline data, limiting them to imitation rather than active exploration.
8. LAMER is the first application of a Meta-RL framework to LLM agent training.
9. Meta-RL training produces more diverse samples while simultaneously achieving higher performance, reaching a better balance between exploration and exploitation than standard RL.
10. Standard RL agents learn a fixed policy during training and struggle to actively explore and adapt their behavior to tasks at test time.

## Capabilities

- Meta-RL framework (LAMER) trains LLM agents to actively explore novel environments and adapt in-context at test time, achieving 11–19% absolute performance gains over standard RL baselines on agentic benchmarks (Sokoban, MineSweeper, Webshop)
- Cross-episode RL training with trajectory-level discount factors (γ_traj) induces principled exploration-exploitation balance in LLM agents — early episodes explore, later episodes exploit accumulated knowledge
- In-context policy adaptation via trained self-reflection allows LLM agents to update their strategy between episodes without any gradient updates — the reflection step is explicitly trained with downstream episode rewards
- Meta-RL training produces superior test-time scaling (pass@k) compared to standard RL training — the diversity-preserving property of Meta-RL translates into better compute scaling at inference
- Meta-RL trained LLM agents generalise to harder and out-of-distribution tasks better than standard RL agents — the learned exploration strategy transfers across task distributions

## Limitations

- Standard RL-trained LLM agents learn fixed policies during training and cannot actively adapt their exploration strategy when encountering novel tasks at test time
- LLM agents do not robustly engage in exploration without substantial external interventions — unlike humans, they tend toward premature convergence on suboptimal strategies
- Multi-turn agentic environments have sparse success signals that arrive only at episode end, making credit assignment for individual exploratory actions difficult
- Prior approaches to inducing exploration in LLM agents are limited to imitation from offline data rather than active, online exploration — bounding the quality of learned exploration to what was already demonstrated
- LAMER experiments are conducted exclusively in text-modal simulated benchmark environments; performance in visual, multimodal, or real-world deployment settings is entirely unvalidated
- Inter-episode memory (H^(n)) accumulates full trajectory history and reflections across episodes, causing context length to grow linearly with episode count — requiring explicit truncation that may discard relevant experience
- LAMER evaluation uses only Qwen3-4B (and one ablation on Llama3.1-8B) — scaling behaviour with frontier-scale models (70B+, 400B+) is unknown and may not hold
- The multi-episode training scheme requires resetting to the same initial state across episodes within a trial — an assumption that is unrealistic in open-world or non-resettable real-world tasks
- Meta-RL training is computationally more expensive than standard RL due to sequential multi-episode rollout generation (episodes conditioned on preceding rollouts rather than independently sampled)
- The γ_traj hyperparameter controlling exploration-exploitation trade-off requires per-environment tuning — the optimal value is task-dependent and no automatic selection method is proposed
- Reasoning work in LLMs has been concentrated on single-turn math and coding problems; multi-turn agentic environments with per-action environment feedback remain systematically understudied

## Bottlenecks

- RL-trained LLM agents lack principled exploration mechanisms for multi-turn long-horizon tasks — they converge to fixed policies and fail to gather new information when encountering novel environments
- Multi-episode RL training for agentic tasks requires resettable, episodic environments — the lack of such environments for real-world tasks blocks direct application of Meta-RL beyond controlled benchmarks

## Breakthroughs

- First application of Meta-RL to LLM agent training — LAMER introduces cross-episode RL with in-context policy adaptation, enabling LLM agents to learn principled exploration strategies rather than converging to fixed test-time policies

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/in_context_and_meta_learning|in_context_and_meta_learning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/grpo|GRPO]]
- [[entities/ppo|PPO]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/webshop|WebShop]]
- [[entities/test-time-compute|test-time compute]]
