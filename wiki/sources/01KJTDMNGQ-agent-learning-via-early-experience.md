---
type: source
title: Agent Learning via Early Experience
source_id: 01KJTDMNGQVQ0YVR8YHW0NNJ54
source_type: paper
authors:
- Kai Zhang
- Xiangchao Chen
- Bo Liu
- Tianci Xue
- Zeyi Liao
- Zhihan Liu
- Xiyao Wang
- Yuting Ning
- Zhaorun Chen
- Xiaohan Fu
- Jian Xie
- Yuxuan Sun
- Boyu Gou
- Qi Qi
- Zihang Meng
- Jianwei Yang
- Ning Zhang
- Xian Li
- Ashish Shah
- Dat Huynh
- Hengduo Li
- Zi Yang
- Sara Cao
- Lawrence Jang
- Shuyan Zhou
- Jiacheng Zhu
- Huan Sun
- Jason Weston
- Yu Su
- Yifan Wu
published_at: '2025-10-09 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- finetuning_and_distillation
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Agent Learning via Early Experience

**Authors:** Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao, Zhihan Liu, Xiyao Wang, Yuting Ning, Zhaorun Chen, Xiaohan Fu, Jian Xie, Yuxuan Sun, Boyu Gou, Qi Qi, Zihang Meng, Jianwei Yang, Ning Zhang, Xian Li, Ashish Shah, Dat Huynh, Hengduo Li, Zi Yang, Sara Cao, Lawrence Jang, Shuyan Zhou, Jiacheng Zhu, Huan Sun, Jason Weston, Yu Su, Yifan Wu
**Published:** 2025-10-09 00:00:00
**Type:** paper

## Analysis

# Agent Learning via Early Experience
2025-10-09 · paper · Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao et al. (30 total)
https://arxiv.org/pdf/2510.08558

---

### Motivation & Prior Limitations
- Most language agents are trained via supervised fine-tuning (SFT) on expert demonstrations, which is reward-free but fundamentally limited in scalability and generalization because demonstrations capture only a narrow range of scenarios and expose the agent to limited environment diversity.
  - Distribution shift is an inherent failure mode: during deployment, the agent's policy inevitably deviates from the expert distribution, encountering states never seen in training where errors compound with no recovery mechanism.
  - Scaling high-quality human demonstrations is expensive and unsustainable; synthetic demonstrations from stronger models offer only incremental gains because the underlying supervision signal remains static.
- Reinforcement learning — the natural alternative — remains impractical for most real-world language agent environments due to two structural barriers: many environments lack verifiable reward signals (e.g., web forms where submission success is unconfirmed), and multi-turn tool-use tasks involve long interaction sequences with delayed or ambiguous outcomes, making credit assignment unstable and training inefficient.
  - Current RL applications to language agents are exploratory and brittle, often relying on approximate rewards from teacher models, hand-tuned reward functions, or carefully curated training recipes; standard RL infrastructure (simulators, reset mechanisms, scalable evaluation) is largely absent for real-world agent environments.
- No practical paradigm existed between static imitation learning and fully reward-driven RL that could leverage an agent's own interaction experience as a scalable, reward-free supervision source.

---

### Proposed Approach
- The paper introduces **early experience**, a training paradigm in which an agent proposes alternative actions at each expert state, executes them in the environment, and uses the resulting future states as direct supervision signals — without any external reward function.
  - The key insight is that future states encode implicit feedback about action quality through environment responses (error messages, DOM changes, tool outputs, task progression), making reward signals unnecessary for learning from consequences.
  - For each expert state $s_i$, $K$ alternative actions are sampled from the current policy and executed, producing a rollout dataset $D_{\text{rollout}} = \{(s_i, a_i^j, s_i^j)\}$ of state–action–nextstate triples that is typically an order of magnitude larger than the expert dataset.
- **Implicit World Modeling (IWM)** uses rollout data to train the policy on next-state prediction as an auxiliary objective: the same model parameters predict $s_i^j$ given $(s_i, a_i^j)$ via standard next-token prediction loss, internalizing environment dynamics without a separate simulator module.
  - This is implemented as a two-stage pipeline: one epoch of the world modeling objective to internalize coarse transition dynamics, followed by standard imitation learning fine-tuning on $D_{\text{expert}}$ within the same total training budget.
  - Unlike classical model-based RL, there is no standalone simulator or explicit planning step; dynamics are embedded directly into the policy, functioning as a lightweight mid-training warm-up rather than a planning module.
- **Self-Reflection (SR)** uses rollout data to generate chain-of-thought rationales that explain why the expert action is preferable to each sampled alternative, grounded in the observed state transitions, then trains the policy to jointly predict these rationales and the expert action.
  - A language model is prompted with the expert action's resulting state and each alternative's resulting state, generating contrastive natural language reasoning; only rationales grounded in actual observed outcomes are used, distinguishing this from STaR-style ungrounded rationale generation.
  - Reflection data is mixed with the expert dataset for joint training, preserving original chain-of-thought reasoning in expert trajectories wherever present.

---

### Results & Capabilities
- Early experience consistently outperforms imitation learning baselines across all eight environments (ALFWorld, ScienceWorld, TravelPlanner, BFCLv3, Tau-Bench, SearchQA, WebShop, WebArena-Lite) and all three model families (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B).
  - SR yields the largest absolute gains on reasoning-heavy, constraint-satisfaction tasks: TravelPlanner +12.8–15.0 pp, ScienceWorld +13.3 pp (Llama-3.1-8B), BFCLv3 +8.0 pp (3B model); IWM excels on environments with consistent, predictable dynamics: WebShop +11.3–18.4 pp.
  - Even in the most challenging open-action-space settings where absolute performance is low, improvements are reliable: WebArena-Lite +1.2–3.6 pp, SearchQA +0.6–3.3 pp.
- Early experience substantially improves out-of-domain generalization, with OOD gains meeting or exceeding in-domain gains in several benchmarks (e.g., ALFWorld Llama-3.1-8B OOD +14.8 pp for IWM; SearchQA OOD +2.2–4.2 pp).
  - IWM generalizes best when environment dynamics are stable across distributions; SR generalizes best when distribution shifts alter tool availability, argument types, or retrieval conditions.
- Early experience serves as a superior initialization for downstream RL: starting GRPO from IWM or SR checkpoints consistently achieves higher post-RL performance ceilings than starting from imitation-only checkpoints, with the advantage maintained or amplified after identical RL training steps.
  - Starting GRPO directly from the raw pretrained model (no supervised stage) performs worst across all tasks and shows unstable training dynamics, confirming the necessity of a strong initialization.
- Early experience is data-efficient: on WebShop, using only 1/8 of exper

## Key Claims

1. Most current language agents rely on supervised fine-tuning on expert data, which is challenging to scale and generalizes poorly.
2. The fundamental limitation of imitation learning for agents stems from expert demonstrations capturing only a narrow range of scenarios and exposing the agent to limited environment diversity.
3. Applying reinforcement learning to real-world language agents remains highly challenging because many environments lack verifiable or dense reward signals.
4. Tasks in multi-turn tool-use environments involve long interaction sequences with delayed or ambiguous outcomes, making credit assignment and training inefficient and unstable.
5. SFT agents do not observe the outcomes of their own actions during training, restricting their ability to learn from failure, refine decision-making, or generalize to unseen situations.
6. Scaling high-quality human demonstrations for SFT is expensive and difficult to sustain.
7. Distribution shift occurs because the agent's learned policy inevitably deviates from the expert policy during deployment, leading to states not covered in training data where errors compound.
8. In imitation learning, agents never observe what happens when they take non-expert actions, limiting their ability to recover from errors or reason about why certain actions fail.
9. The early experience paradigm enables agents to learn from future states generated by their own actions as a reward-free and scalable source of supervision.
10. Implicit world modeling trains the policy to predict its own future states, internalizing coarse environment dynamics without a standalone simulator.

## Capabilities

- Language agents can improve task performance across diverse environments (embodied navigation, web navigation, multi-turn tool use, long-horizon planning) using reward-free 'early experience' — self-generated interaction data from the agent's own actions without external reward signals
- Language agent policies can internalize environment transition dynamics via implicit world modeling — predicting next states from self-generated rollouts without a standalone simulator module, grounding the policy in operating context and improving robustness to distribution shift
- Self-reflection training — contrasting own suboptimal actions against expert actions using observed next-state differences — improves multi-step reasoning and constraint satisfaction, with largest gains on long-horizon planning (+12.8 to +15.0%) and scientific reasoning (+13.3%)
- Early experience warm-starts consistently yield higher post-RL performance ceilings than pure imitation learning warm-starts under identical GRPO training — the advantage persists or amplifies after RL across WebShop, ALFWorld, and SearchQA
- Early experience training achieves comparable or superior agent performance with only 1/8 to 1/2 of expert demonstrations required by pure imitation learning — on WebShop, 1/8 expert data with early experience surpasses imitation learning trained on the full dataset

## Limitations

- Current early experience approaches are limited to short-horizon interaction traces; credit assignment across long-horizon task sequences without explicit reward signals remains an open algorithmic challenge
- Most real-world language agent environments lack verifiable or dense reward signals — websites don't expose ground-truth feedback, and multi-turn tool-use tasks have long sequences with delayed or ambiguous outcomes, blocking direct RL application
- RL training for language agents requires approximate rewards from teacher models or carefully curated reward functions and hand-tuned training recipes to maintain stability — scalable RL with ground-truth rewards alone is not yet mature
- RL infrastructure for real-world language agent environments is critically underdeveloped — most environments lack reliable simulators, standard reset mechanisms, and scalable evaluation platforms, making large-scale RL training costly and brittle
- Self-reflection training performance is non-monotonic at large branching factors K — comparing many alternative actions reduces contrastive signal quality when some alternatives also lead to success, and current models have limited capacity to reason over many outcomes simultaneously
- Early experience gains are smallest on open action space environments — WebArena-Lite shows only +1.2 to +3.6% success rate improvement versus +12.8 to +15.0% for closed environments — indicating a performance cliff in highly combinatorial, fine-grained web interaction settings
- Rollout data generation requires an order of magnitude more data than expert demonstrations — the K alternative actions per expert state create substantial compute, storage, and processing overhead that may be prohibitive for large-scale or real-time deployment
- Full-parameter fine-tuning at frontier model scale (70B+) is computationally infeasible with current experimental setup — all main results use 3B-8B models, and 70B results are limited to parameter-efficient LoRA with constrained update steps
- Self-generated rationales without actual environment execution (STaR-style) frequently hallucinate tools or facts and can degrade agent performance — grounding in real observed state transitions is essential; purely imagined self-reflection is ineffective or harmful
- Extended chain-of-thought at inference time collapses into invalid or off-policy actions in models fine-tuned only on expert demonstrations — SFT on action-only trajectories suppresses the model's prior reasoning capabilities, causing long reasoning chains to drift
- No evaluation of online or continual deployment where interaction data is collected organically from live environments — all experiments use offline training pipelines with pre-collected rollouts, leaving the core deployment scenario (continuous self-improvement) unvalidated

## Bottlenecks

- Long-horizon credit assignment without explicit reward signals for language agents is algorithmically unresolved — no principled method exists to propagate learning signals across extended multi-step interaction sequences in reward-free environments, blocking early experience from scaling to complex
- Absence of reliable simulators, standard reset mechanisms, and scalable evaluation platforms for real-world language agent environments blocks large-scale RL training — the infrastructure prerequisite for the 'era of experience' does not yet exist for most practical commercial domains

## Breakthroughs

- Early experience paradigm enables reward-free learning from self-generated interaction data as a practical and scalable bridge between imitation learning and RL for language agents — agents improve from their own exploratory actions without human demonstrations or reward signals, with gains that per

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/era-of-experience|Era of Experience]]
- [[entities/llama-31-8b|Llama-3.1-8B]]
- [[entities/markov-decision-process|Markov Decision Process]]
- [[entities/webshop|WebShop]]
- [[entities/tau-bench|tau-bench]]
