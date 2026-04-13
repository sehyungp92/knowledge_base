---
type: source
title: A Survey of Reinforcement Learning for Large Reasoning Models
source_id: 01KJTHH7D3G7Q8Z1CKTG59M3DZ
source_type: paper
authors:
- Kaiyan Zhang
- Yuxin Zuo
- Bingxiang He
- Youbang Sun
- Runze Liu
- Che Jiang
- Yuchen Fan
- Kai Tian
- Guoli Jia
- Pengfei Li
- Yu Fu
- Xingtai Lv
- Yuchen Zhang
- Sihang Zeng
- Shang Qu
- Haozhan Li
- Shijie Wang
- Yuru Wang
- Xinwei Long
- Fangfu Liu
- Xiang Xu
- Jiaze Ma
- Xuekai Zhu
- Ermo Hua
- Yihao Liu
- Zonglin Li
- Huayu Chen
- Xiaoye Qu
- Yafu Li
- Weize Chen
- Zhenzhao Yuan
- Junqi Gao
- Dong Li
- Zhiyuan Ma
- Ganqu Cui
- Zhiyuan Liu
- Biqing Qi
- Ning Ding
- Bowen Zhou
published_at: '2025-09-10 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# A Survey of Reinforcement Learning for Large Reasoning Models

> A comprehensive taxonomic review of reinforcement learning applied to large reasoning models (LRMs), covering algorithmic foundations, reward design paradigms, training infrastructure, open foundational debates, and downstream applications. The survey articulates "Verifier's Law" as a unifying structural principle, identifies co-evolving generative reward systems as the critical path beyond verifiable domains, and precisely frames five unresolved theoretical controversies that currently block principled scaling of RL post-training.

**Authors:** Kaiyan Zhang, Yuxin Zuo, Bingxiang He, Youbang Sun, Runze Liu et al. (39 total)
**Published:** 2025-09-10
**Type:** paper

---

## Motivation

RL for LLMs was historically synonymous with alignment — RLHF and DPO fine-tune pre-trained models to follow instructions and reflect human preferences, but do not incentivize reasoning itself. Landmark models (OpenAI o1, DeepSeek-R1) demonstrated that RL with verifiable rewards (RLVR) can induce long-form chain-of-thought reasoning, planning, reflection, and self-correction — behaviors alignment-oriented RL does not reliably produce.

Two structural revelations catalysed the field:
- **o1** demonstrated smooth performance scaling with both additional RL training compute and test-time thinking budget, revealing a new scaling axis orthogonal to parameter and data scaling.
- **DeepSeek-R1** showed that large-scale GRPO with rule-based rewards can elicit sophisticated reasoning even in base models prior to alignment — "Zero RL" without SFT cold-start.

Further scaling now faces foundational challenges not present in classical RLHF: algorithm design for long-horizon reasoning, reward design beyond verifiable domains, training data sufficiency, asynchronous multi-turn rollout infrastructure, and the absence of standardised experimental protocols.

---

## Organising Principle: Verifier's Law

The survey articulates **Verifier's Law** as a structural constraint on the entire field:

> The ease of training an AI system on a task is proportional to the degree to which the task is automatically verifiable.

This explains both current RLVR successes (mathematics, competitive programming, formal code) and persistent open problems (open-ended generation, scientific discovery, creative writing). It positions the development of reliable automatic verifiers — particularly Generative Reward Models — as the single most important enabling capability for the next phase of [[themes/reinforcement_learning|RL]] scaling. See [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]].

---

## Algorithmic Taxonomy

### Critic-Based vs. Critic-Free

**Critic-based (PPO with GAE):** Standard RLHF approach. Co-trains a value model alongside the policy to estimate token-level advantage. Provides fine-grained per-token credit signals. Key limitation: critic requires full co-training, creating significant computational overhead that scales unfavorably for long chain-of-thought tasks with hundreds to thousands of tokens per rollout.

GAE's exponential discount factor compounds a further problem: temporal discounting over extended reasoning traces produces near-zero credit for early reasoning steps, systematically misattributing credit in long-horizon tasks.

**Critic-free (GRPO and variants):** The dominant practical paradigm. Replaces GAE with group-relative advantage normalization — generating a group of responses to the same prompt and normalising rewards across the group. Key properties:
- Requires only sequence-level rewards, making it more scalable for verifiable tasks
- Avoids reward hacking from ill-trained critic models
- Eliminating the critic effectively doubles maximum trainable model size for a given compute budget

Recent algorithmic variants address residual weaknesses:

| Algorithm | Problem Addressed | Mechanism |
|-----------|-------------------|-----------|
| **DAPO** | Saturated/degenerate rollouts | Clip-Higher + dynamic sampling filtering medium-difficulty prompts |
| **GSPO** | Token-level IS bias | Sequence-level clipping factor replacing token-wise ratios |
| **Dr. GRPO** | Spurious variance from normalisation | Revised advantage normalisation scheme |
| **CISPO** | Training instability | Conservative importance sampling |
| **FlowRL** | Mode collapse | Distribution matching over complete reward distributions rather than scalar maximisation |

A key controversy: KL regularization toward the reference policy — standard in RLHF for stability — is increasingly removed in RLVR settings, because policy divergence from the initialization is necessary for discovering novel chain-of-thought structures. However, the optimal form, coefficient, and necessity of KL, entropy, and length regularization remain theoretically unresolved.

### Off-Policy and Mixed-Policy Methods

Off-policy methods (Retrospective Replay, RLEP, ARPO, PPER) decouple trajectory generation from policy updates using replay buffers, enabling concurrent sampling across multiple actors. Mixed-policy approaches (LUFFY, RED, ReLIFT, BREAD, Prefix-RFT) blend SFT and RL losses at the data or loss level to prevent reward hacking while retaining pre-training knowledge.

**Quantization discrepancy:** Training at FP32 while deploying at INT8 creates a structural distributional shift between training target and deployed behavior — a currently unavoidable but practically manageable artifact, with truncated importance sampling as the standard mitigation.

### Tree-Based Methods

MCTS-based approaches (TreeRL, TreeRPO, TreePO, SPO) branch at key decision points within a reasoning trace, assign rewards at the node level, and compute process rewards via Monte Carlo estimation through subtrees. This provides denser, more fine-grained credit signals than chain-based rollouts. The fundamental cost: significantly lower sample efficiency — a compute-quality tradeoff with no current principled resolution.

TreePO introduces segment-wise tree sampling to alleviate KV cache burden, reducing GPU hours while retaining richer process signals.

---

## Reward Design Taxonomy

Five distinct paradigms, ordered roughly by verifiability:

**1. Verifiable/Rule-Based Rewards**
Accuracy and format checkers for mathematics and code — the foundation of current RLVR successes. Primary limitation: systematic false negatives when models generate correct answers in unexpected formats, introducing noisy negative reward signals that corrupt training.

**2. Generative Reward Models (GenRMs)**
LLMs that generate chain-of-thought reasoning before rendering judgment. Provide nuanced reward signals for subjective tasks. The most advanced variant: **co-evolving systems** (RL Tango, Cooper, URPO) where policy and reward model train simultaneously and improve each other, partially circumventing Verifier's Law by bootstrapping capability from outcome-level signals alone.

**3. Rubric-Based Generative Rewards**
Natural language checklists that enable RL on creative writing, scientific peer review, and other subjective domains where binary verifiers fail.

**4. Dense Rewards**
Process Reward Models (PRMs) that assign step-level credit. Online PRM training during RL rollouts is prohibitively expensive — computing step-level labels requires multiple additional forward passes per reasoning step. Training PRMs offline and deploying statically risks reward hacking.

**5. Unsupervised Rewards**
- **Consistency-based:** Majority voting across self-generated answers
- **Confidence-based:** Internal model uncertainty signals
- **Self-generated knowledge:** RPT reframes next-token prediction on web-scale corpora as an RL objective, enabling RL pre-training signal generation without any annotated data

All unsupervised methods share a critical fragility: they depend on the base model already having relevant prior knowledge and fail catastrophically when this assumption is violated. Closed-loop self-rewarding systems additionally risk convergence on self-confirming incorrect outputs with no external correction mechanism.

---

## Foundational Debates

The survey precisely frames five unresolved theoretical controversies that currently block principled scaling:

### 1. Sharpening vs. Discovery
Does RLVR sharpen latent pre-training capabilities, or does it genuinely discover new reasoning behaviors?

**Evidence for sharpening:** Pass@K evaluations show RL improves Pass@1 but underperforms base models at large-k sampling, suggesting RL narrows the search space rather than expanding it. Spurious and random rewards can improve reasoning nearly as effectively as carefully designed rewards — implying gains often reflect pre-training feature elicitation. Mechanistic analysis shows SFT induces output distribution collapse toward training patterns, while RL preserves the base model's distributional breadth.

**Evidence for discovery:** DeepSeek-R1 Zero demonstrates sophisticated reasoning behaviors (reflection, self-correction) emerging from base models with no SFT cold-start — behaviors not clearly present before RL.

**Why this matters:** No principled theory currently predicts when RL post-training can acquire genuinely new capabilities versus reorganising pre-trained ones — blocking principled decisions about when more pre-training versus more RL is the right investment.

### 2. RL Generalises vs. SFT Memorises
Substantiated by PCA and KL-divergence analysis: SFT on math induces representation drift and catastrophic forgetting on non-math capabilities, while RL on math preserves or improves performance on non-math tasks and instruction following.

### 3. Model Family Responsiveness
Different base model families respond differently to RL post-training depending on their pre-training characteristics and prior strength.

### 4. Genuine Advances vs. Experimental Artifacts
Which "trick" results in the fragmented algorithm space (DAPO, GSPO, REINFORCE++, Dr. GRPO, etc.) constitute genuine advances versus artifacts of specific experimental setups, benchmarks, or undisclosed implementation details?

### 5. Process vs. Outcome Rewards
For long-chain credit assignment, whether process rewards (PRMs, dense signals) are more effective than outcome rewards (GRPO-style) remains contested — with conflicting empirical evidence and no principled theoretical prediction.

---

## Key Capabilities

- **Critic-free RLVR at scale:** GRPO and variants achieve competitive reasoning performance using only sequence-level rewards, removing the critic model. Now in broad production across frontier labs. → [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- **Generative Reward Models:** GenRMs extend RL beyond verifiable domains; co-evolving variants (research stage) partially circumvent Verifier's Law. → [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]]
- **Self-instruction curriculum learning:** Proposer-solver systems generate training problems of optimal difficulty, enabling fully unsupervised RL data generation that scales without human annotation (research stage).
- **Turn-level reward decomposition:** Distributes trajectory-level outcomes into per-turn contributions for stable multi-turn agent RL without per-step human annotation (research stage). → [[themes/reasoning_and_planning|Reasoning and Planning]]
- **Dynamic difficulty sampling:** DAPO-style online filtering focuses training on medium-difficulty problems with non-zero advantage, eliminating wasted compute on trivially easy or unsolvable examples (research stage).
- **Frontier agentic models:** Kimi K2 (1T-parameter MoE) demonstrates large-scale agentic training data synthesis with RL on non-verifiable rewards at production scale.
- **Hybrid attention for RL efficiency:** Minimax-M1's hybrid attention enables efficient RL scaling by reducing the quadratic attention cost during long-context policy rollout generation. → [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]

---

## Key Limitations

### Blocking

- **Open-ended task intractability (Verifier's Law):** RLVR fundamentally cannot scale to tasks without fast, objective verification — open-ended QA, creative writing, strategic planning remain intractable for outcome-based RL. The structural barrier is likely 3–5 years from principled resolution.
- **Superhuman expertise bottleneck:** Human feedback for reward signals is impractical for tasks requiring superhuman competence — human evaluators cannot reliably judge outputs exceeding their own level.
- **Dense reward definition for open-domain text:** No principled method exists for assigning process-level credit to intermediate reasoning steps without ground-truth annotation.
- **No scaling laws for RL reasoning:** No clear theory exists analogous to pre-training scaling laws — the field cannot predict what more RL compute will produce without running experiments.

### Significant

- **Reward hacking in learned reward models:** Policies learn to exploit RM imperfections rather than improve the underlying task — a systematic failure mode that worsens as models become more capable.
- **Entropy collapse:** Without explicit intervention, RL training reliably collapses into low-entropy distributions. Direct entropy regularization is neither common nor effective in LLM RL settings — its effect is highly context-dependent with no consistent best practice.
- **KL divergence controversy:** Theoretically unresolved — many works advocate removing it entirely while others find it essential, with conflicting empirical evidence across settings.
- **Token-level IS bias:** All current policy gradient methods use token-level importance ratios as a tractable substitute for the exact sequence-level ratio, introducing systematic bias. Sequence-level IS (GSPO) substitutes a different bias.
- **Uniform token advantage in GRPO:** All tokens in a response share the same advantage estimate — ignoring differential contributions of individual reasoning steps and creating uniformly noisy credit signals.
- **Long context fragility:** Staged context lengthening starting at 8k tokens is near-universal practice, revealing RL training dynamics are fragile with large context from initialization.
- **Algorithm fragmentation without convergence:** Dozens of competing variants (GRPO, DAPO, GSPO, Dr. GRPO, CISPO, FlowRL, PSPO, CPGD, SPO, GPPO, etc.) without convergence on a dominant approach or principled comparative framework.

---

## Infrastructure Notes

The survey identifies standardisation gaps in RL training infrastructure as a practical barrier. Asynchronous distributed RL (HeteroRL, vLLM-based rollout engines) is increasingly standard, with:
- Decoupled rollout and parameter update for concurrent trajectory generation
- Shared replay buffers sampled by a centralised learner
- Truncated importance sampling to manage staleness from asynchronous updates

HeteroRL sustains <3% performance degradation relative to synchronous training while enabling decentralised asynchronous execution — but these systems remain non-standardised across research groups.

---

## Connections

- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — primary theme; the algorithmic and empirical core
- [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]] — foundational debates, regularisation, credit assignment
- [[themes/policy_optimization|Policy Optimization]] — GRPO variants, PPO, critic-free methods
- [[themes/reasoning_and_planning|Reasoning and Planning]] — multi-turn agent RL, tree-based search
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]] — benchmark results, RLVR success domains
- DeepSeek-R1 — key empirical anchor; Zero RL demonstration
- OpenAI o1 — established train-time RL compute as scaling axis

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/entropy-regularization|Entropy Regularization]]
- [[entities/grpo|GRPO]]
- [[entities/generalized-advantage-estimation|Generalized Advantage Estimation]]
- [[entities/generative-reward-model-genrm|Generative Reward Model (GenRM)]]
- [[entities/genie-3|Genie 3]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/large-reasoning-model-lrm|Large Reasoning Model (LRM)]]
- [[entities/large-reasoning-models|Large Reasoning Models]]
- [[entities/outcome-reward-model-orm|Outcome Reward Model (ORM)]]
- [[entities/prime|PRIME]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/proximal-policy-optimization-ppo|Proximal Policy Optimization (PPO)]]
- [[entities/reinforce|REINFORCE]]
- [[entities/rlhf|RLHF]]
- [[entities/rloo|RLOO]]
- [[entities/rlvr|RLVR]]
