---
type: source
title: Process Reinforcement through Implicit Rewards
source_id: 01KJV4KX85J6NJAA4F3RAMSYRT
source_type: paper
authors:
- Ganqu Cui
- Lifan Yuan
- Zefan Wang
- Hanbin Wang
- Yuchen Zhang
- Jiacheng Chen
- Wendi Li
- Bingxiang He
- Yuchen Fan
- Tianyu Yu
- Qixin Xu
- Weize Chen
- Jiarui Yuan
- Huayu Chen
- Kaiyan Zhang
- Xingtai Lv
- Shuo Wang
- Yuan Yao
- Xu Han
- Hao Peng
- Yu Cheng
- Zhiyuan Liu
- Maosong Sun
- Bowen Zhou
- Ning Ding
published_at: '2025-02-03 00:00:00'
theme_ids:
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Process Reinforcement through Implicit Rewards

**Authors:** Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Yuchen Zhang, Jiacheng Chen, Wendi Li, Bingxiang He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen, Jiarui Yuan, Huayu Chen, Kaiyan Zhang, Xingtai Lv, Shuo Wang, Yuan Yao, Xu Han, Hao Peng, Yu Cheng, Zhiyuan Liu, Maosong Sun, Bowen Zhou, Ning Ding
**Published:** 2025-02-03 00:00:00
**Type:** paper

## Analysis

# Process Reinforcement through Implicit Rewards
2025-02-03 · paper · Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Yuchen Zhang et al. (25 total)
https://arxiv.org/pdf/2502.01456

---

### Motivation & Prior Limitations
- Dense process rewards are theoretically superior to sparse outcome rewards for RL training of LLMs — addressing training efficiency, credit assignment, and spurious solutions — but their practical use in online RL has remained largely unrealized due to three compounding challenges.
  - **C1 — Annotation ambiguity and cost:** Step-level labels are difficult to define because reasoning steps are not naturally delimited, token-level annotation is prohibitively expensive, and the absolute correctness of intermediate steps is semantically ambiguous (some incorrect steps can positively contribute by pruning search branches).
  - **C2 — Online PRM updates are unscalable:** Preventing reward hacking requires updating the reward model online alongside the policy, but existing PRMs (e.g., Lightman et al., 2023) require nuanced step-level annotation on the latest policy rollouts, making this infeasible at RL training scale.
  - **C3 — Explicit reward modeling overhead:** Training a PRM requires extensive annotated data and a separate dedicated training stage, adding substantial development cost before RL can even begin. DeepSeek-AI (2025) independently identifies this as the reason it avoided PRMs in large-scale RL.
- Value models, sometimes proposed as a proxy for dense signal, do not effectively resolve reward sparsity due to their own training challenges and add computational overhead without commensurate benefit, as confirmed empirically by prior work (Shao et al., 2024; Ahmadian et al., 2024).
- Sparse outcome-reward RL (e.g., GRPO, RLOO, PPO with verifiable rewards) has been the dominant paradigm in recent frontier models (DeepSeek-R1, Kimi), leaving dense-reward RL for LLMs an open and underexplored problem.

---

### Proposed Approach
- PRIME (Process Reinforcement through IMplicit rEwards) introduces a scalable online RL framework that derives token-level dense process rewards from an Implicit PRM trained exclusively on outcome labels, eliminating all three prior challenges simultaneously.
  - The Implicit PRM represents reward as $r_\phi(y) := \beta \log \frac{\pi_\phi(y)}{\pi_\text{ref}(y)}$, which allows it to be trained with a standard binary cross-entropy loss on outcome labels (correct/incorrect) rather than step-level annotations. At inference, token-level process rewards are computed as the log-ratio of the policy LM over the reference LM at each token: $r_\phi(y_t) := \beta \log \frac{\pi_\phi(y_t|y_{<t})}{\pi_\text{ref}(y_t|y_{<t})}$.
  - Because the Implicit PRM is itself a causal language model trained on outcome labels already collected during policy rollout, it can be updated online at no additional data-collection cost — directly resolving C1 and C2.
- PRIME initializes both the policy model and the Implicit PRM from the same SFT (or base) model checkpoint, bypassing the need for a dedicated reward model training phase entirely (resolving C3) and alleviating distribution shift between the PRM and the current policy.
  - Experiments show this initialization strategy outperforms using a separately trained PRM (EurusPRM trained on 500K additional samples), because the shared initialization keeps the PRM tightly coupled to the policy's rollout distribution.
- Advantages are computed by summing two RLOO (leave-one-out) returns computed separately: one from discounted implicit process rewards and one from sparse outcome rewards, preventing numerical instability from directly mixing reward magnitudes.
  - An online prompt filtering step retains only prompts in a mid-difficulty accuracy range, stabilizing the training distribution for both policy and PRM updates and substantially reducing gradient variance.
- PRIME is algorithm-agnostic: it modifies only the advantage estimation function and is compatible with REINFORCE, RLOO, GRPO, and PPO without changing the clipped surrogate loss.

---

### Results & Capabilities
- Starting from Qwen2.5-Math-7B-Base with a lightweight SFT warmup, PRIME achieves a 15.1% average improvement across seven reasoning benchmarks over the SFT model, with over 20% improvement on AMC and AIME 2024 competition benchmarks.
- Compared to RLOO with sparse outcome rewards only, PRIME achieves **2.5× sample efficiency** (reaching the same training reward in 40% of the gradient steps) and a **6.9% absolute performance improvement** on challenging math problems at the same training budget, at the cost of only 24% additional wall-clock time per step.
  - The net training-time efficiency advantage is approximately 2× even accounting for the PRM update overhead, as shown in Table 2 (PRIME: 680s/step vs. RLOO: 531s/step, but requiring 2.5× fewer steps).
- The resulting model, **Eurus-2-7B-PRIME**, surpasses Qwen2.5-Math-7B-Instruct on seven reasoning benchmarks while using only 10% of its training data, and achieves 26.7% pass@1 on AIME 2024 — exceeding GPT-4o (9.3%), Llama-3.1-70B-Instruct (20.0%), and Qwen2.5-Math-7B-Instruct (13.3%).
- Online PRM update is empirically essential: an offline (frozen) PRM starts with high accuracy but degrades over training due to distribution shift, while the online PRM's classification accuracy increases monotonically, directly preventing reward hacking.
- Using the Implicit PRM as a **reward model** (computing returns) substantially outperforms using it as a **value model** (computing baselines), and both explicit value models (linear-head PPO) and implicit value baselines underperform the reward-model formulation — confirming that PRMs are fundamentally better suited than value models for dense supervision in LLM RL.
- PRIME consistently improves training efficiency and final performance when applied to REINFORCE, GRPO, and PPO in addition to RLOO, validating its claim as a general plug-in.
- Scaling experime

## Key Claims

1. Dense process rewards are more effective than sparse outcome rewards for inference-time scaling of LLMs on complex multi-step reasoning tasks
2. The potential of dense rewards to address training efficiency and credit assignment in RL for LLMs remains largely unrealized
3. PRIME enables online PRM updates using only policy rollouts and outcome labels through implicit process rewards, without requiring dedicated reward model training
4. PRIME achieves a 15.1% average improvement across key reasoning benchmarks over the SFT model starting from Qwen2.5-Math-7B-Base
5. Eurus-2-7B-PRIME surpasses Qwen2.5-Math-7B-Instruct on seven reasoning benchmarks using only 10% of its training data
6. Industry-leading models primarily depend on verifiable outcome rewards and have not yet demonstrated meaningful progress with dense rewards
7. Optimizing toward a static reward model eventually leads to overoptimization or reward hacking due to distribution shift
8. PRIME achieves 2.5x sample efficiency gain and 6.9% performance improvement compared to RL using outcome rewards only
9. Sparse outcome rewards encourage spurious solutions with incorrect processes but correct answers and reduce sample efficiency
10. Value models cannot effectively solve the reward sparsity issue despite adding computational overhead

## Capabilities

- Online process reward model (PRM) training using only outcome labels — no stepwise annotations required — enabling scalable dense-reward RL for LLM reasoning without dedicated reward model training phase
- Dense implicit process rewards achieve 2.5× sample efficiency gain and 6.9% performance improvement over outcome-only RL on competitive math benchmarks
- 7B parameter model trained with PRIME (Eurus-2-7B-PRIME) achieves 26.7% pass@1 on AIME 2024 and surpasses GPT-4o, Llama-3.1-70B-Instruct, and Qwen2.5-Math-7B-Instruct using only 10% of Qwen-Math's training data
- SFT model self-initialization as implicit PRM outperforms a dedicated PRM trained on 500K additional samples, eliminating the need for a separate reward model training phase
- PRIME dense-reward framework is a drop-in plug-in compatible with RLOO, REINFORCE, GRPO, and PPO — consistently boosting both efficiency and performance regardless of policy update algorithm
- Online prompt filtering during RL training (retaining prompts within a median-difficulty accuracy range) substantially reduces training variance without external data curation

## Limitations

- Dense-reward RL with PRIME is restricted to tasks with rule-based verifiable outcome labels (math exact match, code pass rate) — no demonstrated applicability to open-ended, creative, or agentic tasks
- Offline (static) PRMs are progressively overoptimized during RL training due to distribution shift — PRM accuracy degrades monotonically as the policy diverges from the reward model's training distribution
- Value models (including Implicit PRM used as value function) fail to effectively mitigate reward sparsity — they do not improve over REINFORCE baseline and introduce additional computation overhead
- Acquiring high-quality stepwise process labels for training standard PRMs is prohibitively expensive — either requiring human annotation pipelines or ~10× more rollouts per step than outcome-level sampling
- Sparse outcome rewards incentivise spurious solutions: models learn to produce incorrect reasoning processes that still arrive at correct answers, masking process-level failures from the training signal
- PRIME adds 24% wall-clock overhead per training step compared to outcome-only RLOO, requiring PRM forward pass and update in addition to policy update
- PRIME requires an SFT warmup stage before RL training — end-to-end training directly from a base model is possible but the standard protocol still begins with supervised finetuning
- PRIME validated only at 7B parameter scale — no experiments at larger model sizes; scalability to 70B+ frontier scale remains undemonstrated
- Defining the absolute correctness of intermediate reasoning steps as dense rewards is inherently ambiguous — incorrect intermediate steps can positively contribute to finding the correct answer by pruning search branches
- Current industry-leading RL systems (DeepSeek-R1, Kimi k1.5) rely exclusively on outcome rewards and have not demonstrated meaningful progress with dense process rewards — the industry consensus has not yet validated dense rewards at the largest scales
- Training data approaching exhaustion signals a fundamental constraint on supervised learning scaling — the authors frame this as the motivating context for moving to RL-based experience generation

## Bottlenecks

- Stepwise process label collection for PRM training is prohibitively expensive, blocking scalable dense-reward RL — human annotation pipelines or Monte Carlo estimation methods requiring 10× more rollouts per step are both unscalable in online RL
- Offline static reward models are inherently vulnerable to reward hacking as the policy distribution diverges during training — online RM updates are necessary but were previously bottlenecked by annotation cost
- Sparse outcome-only rewards cause severe credit assignment problems in multi-step reasoning RL — the policy receives no signal about which intermediate steps were productive, reducing sample efficiency and encouraging spurious solutions

## Breakthroughs

- PRIME demonstrates that dense token-level process rewards for RL can be derived implicitly from outcome labels alone — eliminating the need for stepwise annotations that previously made online PRM training infeasible

## Themes

- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/amc|AMC]]
- [[entities/credit-assignment|Credit Assignment]]
- [[entities/grpo|GRPO]]
- [[entities/generalized-advantage-estimation|Generalized Advantage Estimation]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/ppo|PPO]]
- [[entities/prime|PRIME]]
- [[entities/rloo|RLOO]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/sample-efficiency|Sample Efficiency]]
- [[entities/verl|verl]]
