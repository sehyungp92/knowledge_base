---
type: source
title: Scaling Agent Learning via Experience Synthesis
source_id: 01KJTASF4SBPM26WZ8N0H3B4FM
source_type: paper
authors:
- Zhaorun Chen
- Zhuokai Zhao
- Kai Zhang
- Bo Liu
- Qi Qi
- Yifan Wu
- Tarun Kalluri
- Sara Cao
- Yuanhao Xiong
- Haibo Tong
- Huaxiu Yao
- Hengduo Li
- Jiacheng Zhu
- Xian Li
- Dawn Song
- Bo Li
- Jason Weston
- Dat Huynh
published_at: '2025-11-05 00:00:00'
theme_ids:
- agent_systems
- computer_use_and_gui_agents
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Scaling Agent Learning via Experience Synthesis

DreamGym introduces a unified synthetic training framework that replaces costly real-environment rollouts with a reasoning-based experience model operating in abstract textual state space, enabling scalable online RL for LLM agents — including in environments that are entirely RL-unready. By synthesising diverse interaction experiences, generating curriculum tasks, and enabling sim-to-real transfer, the framework makes RL-based agent training practical across web navigation and embodied control benchmarks while reducing training cost to one-third to one-fifth of real-environment baselines.

**Authors:** Zhaorun Chen, Zhuokai Zhao, Kai Zhang, Bo Liu, Qi Qi, Yifan Wu, Tarun Kalluri, Sara Cao, Yuanhao Xiong, Haibo Tong, Huaxiu Yao, Hengduo Li, Jiacheng Zhu, Xian Li, Dawn Song, Bo Li, Jason Weston, Dat Huynh
**Published:** 2025-11-05
**Type:** paper
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]]

---

## Motivation

Real-environment RL for LLM agents is blocked by four compounding barriers that together make scalable training infeasible:

1. **Rollout cost.** Long interaction sequences, high per-step compute, and sparse rewards make large-scale online RL prohibitively expensive. Environments like WebArena lack scalable data collection and reliable reset mechanisms, and incur irreversible side effects — deleting items on live websites — making them entirely RL-unready.
2. **Task diversity.** Most environments offer a static, limited set of task instructions. Effective RL requires broad coverage, but validating new task feasibility demands costly human expertise.
3. **Reward unreliability.** Dynamic web environments produce noisy, sparse, or factually incorrect reward signals, causing training instability and collapse in multi-step tasks.
4. **Infrastructure heterogeneity.** RL-ready environments rely on heavyweight backends (Docker, virtual machines), making large-batch sampling engineering-intensive independent of algorithmic concerns.

Prior synthetic environment work addressed some of these problems but introduced others: pixel-space dynamics models (WebDreamer, Dreamer) are data-hungry and costly; UI-Simulator requires substantial expert engineering per environment and is limited to SFT trajectory variations; scripted oracle approaches produce static, non-adaptive data.

The central insight DreamGym builds on is that **agent training does not require perfectly realistic environments — only interaction data that is sufficiently diverse, informative, and causally grounded.**

---

## Approach

DreamGym has three interlocking components:

### Reasoning Experience Model (M_exp)

The core of DreamGym is an LLM trained via SFT on offline trajectory data that simulates environment dynamics in **abstract textual state space** — for web tasks, clean element listings rather than raw HTML. Given a current action, full interaction history, task instruction, and top-*k* semantically similar demonstrations retrieved from a replay buffer, M_exp produces next states and reward signals through explicit chain-of-thought reasoning.

The joint SFT objective trains M_exp to both generate faithful reasoning traces explaining action consequences *and* leverage those traces for consistent state prediction. This causal grounding is critical: ablations show that removing reasoning degrades state coherence and increases hallucination across multi-step rollouts.

Unlike pixel-space world models, operating in meta-representational space makes training sample-efficient (competitive with 10K offline steps) and token-efficient — irrelevant dimensions are discarded before any learning occurs.

### Experience Replay Buffer

The replay buffer is seeded with offline real-world trajectory data and continuously enriched with freshly generated synthetic transitions. Retrieval is by cosine similarity of a semantic encoder over state-action pairs, providing diverse yet relevant demonstrations that reduce hallucination and improve factuality. Critically, the buffer requires this seed data — **DreamGym cannot cold-start from zero real interactions**, though in practice public benchmark datasets (WebArena, ALFWorld offline splits) serve as a sufficient bootstrap.

### Curriculum Task Generator

M_exp doubles as a task generator. It selects seed tasks by a **group-based reward entropy criterion** — tasks where the agent's rollout outcomes show non-zero variance (both successes and failures) — and generates progressively harder variations. A hyperparameter λ bounds the proportion of synthetic tasks per iteration, preserving original task distribution coverage while directing exploration toward the policy's current capability boundary.

### Sim-to-Real (S2R) Transfer

A transfer variant trains the policy entirely in DreamGym, then applies a small-scale real-environment RL phase. State-space consistency between synthetic and real observations is maintained via a rule-based mapping or lightweight fine-tuned adapter model. The synthetic pretraining serves as warm-start initialisation, substantially reducing the real data required.

---

## Results

| Setting | Model | DreamGym | Baseline | Notes |
|---|---|---|---|---|
| WebArena (non-RL-ready) | Llama-3.2-3B | 14.5% | ~0% | Only viable RL approach; >30% over all baselines |
| WebShop (RL-ready) | Llama-3.1-8B | 63.9% | GRPO 65.0% | Zero real interactions used |
| ALFWorld (RL-ready) | Qwen-2.5-7B | 71.0% | GRPO 79.8% | Zero real interactions used |
| ALFWorld S2R | Llama-3.1-8B | 75.9% | GRPO 70.9% | 5K real vs. 80K real for baseline |

On WebArena — the hardest case, with no reward signals, no reset mechanisms, and no RL infrastructure — DreamGym is the **only approach that achieves non-trivial performance**, making the environment tractable for the first time. Training cost across settings is reduced to approximately one-third to one-fifth of real-environment RL, with notably smoother training curves attributed to dense curriculum feedback and lightweight abstract state serving.

---

## Capabilities

- **LLM reasoning world models** can simulate environment dynamics in abstract textual state space with sufficient fidelity for RL training, producing causally grounded state transitions and reward signals via chain-of-thought — no pixel-space reconstruction required. *(maturity: research only)*
- **Zero-real-data RL training** of LLM agents using only synthetic rollouts achieves performance parity with GRPO and PPO trained on 80K real interactions on web navigation and embodied control benchmarks. *(maturity: research only)*
- **Synthetic pretraining as RL warm-start** yields >40% performance improvement over training from scratch while using <10% of external real-world data. *(maturity: research only)*
- **Reward-entropy curriculum generation** automatically identifies and produces increasingly difficult task variations calibrated to the agent's current capability boundary, without human labelling. *(maturity: research only)*
- **Non-RL-ready environment training** is now viable — success rates exceeding 13% on WebArena where real-environment RL yields near-zero results. *(maturity: research only)*

---

## Limitations & Open Questions

### Significant Limitations

**No cross-domain transfer.** Policies trained on web-based environments (WebShop, WebArena) cannot transfer to embodied control (ALFWorld), and vice versa. When domain gap becomes too large — different meta-representations, action spaces, and causal structures — synthetic pretraining provides no benefit. This is a fundamental constraint on the ambition of building universal synthetic RL frameworks.

**Text-only environments.** The abstract textual state space design is restricted to environments where observations can be rendered as structured text. Pixel-space inputs, continuous sensor streams, raw visual observations, and real-world robotics are outside scope. This excludes a large fraction of practically important agent deployment contexts.

**Manual sim-to-real alignment.** State-space consistency between synthetic and real environments requires either a manually designed rule-based mapping or an additional fine-tuned adapter — alignment is not automatic. This is a non-trivial engineering requirement that partially recreates the infrastructure complexity DreamGym aims to eliminate.

**Sparse binary rewards only.** DreamGym uses outcome-based rewards (0/1 at final step only). No dense intermediate reward generation is demonstrated. Long-horizon credit assignment remains dependent on terminal outcomes, which may limit applicability to tasks requiring fine-grained step-level feedback.

**Performance gaps on specific model-benchmark pairs.** DreamGym GRPO achieves 40.5% vs. traditional GRPO's 47.0% on ALFWorld with the 3B model — a ~15% relative gap. Synthetic training is not uniformly competitive at smaller model scales.

**Hallucination in state predictions.** Without trajectory history, causal coherence breaks across multi-step interactions; without reasoning, states become factually inconsistent. The framework mitigates but does not eliminate hallucination in the experience model.

### Scope Gaps

**Evaluation coverage is narrow.** Results cover only web navigation (WebShop, WebArena) and text-based embodied control (ALFWorld). Coding agents, mathematical reasoning, tool-use chaining, and real robotics are untested — generalisation claims across agent types remain unvalidated.

**Bootstrap dependency.** The replay buffer must be seeded with offline real-world trajectory data. While public benchmark datasets suffice in practice, truly cold-start deployment in novel environments is not demonstrated.

---

## Bottlenecks Addressed

**Online RL for production web agents** — [[themes/reinforcement_learning|RL]] self-improvement for agents deployed in real web environments is blocked by the systemic absence of scalable reset mechanisms, verifiable reward signals, and safe exploration infrastructure. DreamGym directly addresses this bottleneck for the training phase, but deployment-time RL remains unresolved. *(horizon: 1–2 years)*

**Cross-domain generalisation in synthetic RL** — abstract state spaces learned for one environment class do not transfer to structurally different ones. Universal synthetic RL frameworks without domain-specific engineering remain an open problem. *(horizon: 1–2 years)*

---

## Breakthrough Assessment

DreamGym's most significant contribution is demonstrating that **a reasoning-based LLM world model can fully substitute real-environment rollouts for RL agent training** — achieving parity with GRPO/PPO on 80K real interactions using zero real data, and delivering the first viable RL training results on WebArena (>30% over all baselines). This shifts the prior assumption that online RL for LLM agents necessarily requires live environment access.

The result is *notable* rather than *transformative* because: (a) the abstract textual state space design restricts the approach to text-representable environments; (b) cross-domain transfer fails completely at large domain gaps; (c) evaluation scope is limited to two environment families. Whether this approach generalises to the environments where agent RL matters most — code execution, real-world tool use, continuous control — remains to be demonstrated.

---

## Connections

- Extends prior [[themes/synthetic_data_generation|synthetic data]] work (WebDreamer, WebEvolver) from SFT trajectory generation to full online RL training
- Related to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] via GRPO and PPO training dynamics for language model agents
- Complements [[themes/computer_use_and_gui_agents|GUI agent]] work on WebArena and WebShop by providing a training pathway where real-environment interaction was previously infeasible
- Connects to [[themes/post_training_methods|post-training methods]] literature on curriculum learning and sim-to-real transfer for policy optimisation

## Key Concepts

- [[entities/alfworld|ALFWorld]]
- [[entities/generalized-advantage-estimation|Generalized Advantage Estimation]]
- [[entities/markov-decision-process|Markov Decision Process]]
- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/webarena|WebArena]]
- [[entities/webshop|WebShop]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
