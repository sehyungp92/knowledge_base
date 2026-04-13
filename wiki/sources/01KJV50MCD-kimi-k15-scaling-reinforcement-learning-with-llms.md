---
type: source
title: 'Kimi k1.5: Scaling Reinforcement Learning with LLMs'
source_id: 01KJV50MCDN3MJA7NSEB9CDW07
source_type: paper
authors:
- Kimi Team
- Angang Du
- Bofei Gao
- Bowei Xing
- Changjiu Jiang
- Cheng Chen
- Cheng Li
- Chenjun Xiao
- Chenzhuang Du
- Chonghua Liao
- Chuning Tang
- Congcong Wang
- Dehao Zhang
- Enming Yuan
- Enzhe Lu
- Fengxiang Tang
- Flood Sung
- Guangda Wei
- Guokun Lai
- Haiqing Guo
- Han Zhu
- Hao Ding
- Hao Hu
- Hao Yang
- Hao Zhang
- Haotian Yao
- Haotian Zhao
- Haoyu Lu
- Haoze Li
- Haozhen Yu
- Hongcheng Gao
- Huabin Zheng
- Huan Yuan
- Jia Chen
- Jianhang Guo
- Jianlin Su
- Jianzhou Wang
- Jie Zhao
- Jin Zhang
- Jingyuan Liu
- Junjie Yan
- Junyan Wu
- Lidong Shi
- Ling Ye
- Longhui Yu
- Mengnan Dong
- Neo Zhang
- Ningchen Ma
- Qiwei Pan
- Qucheng Gong
- Shaowei Liu
- Shengling Ma
- Shupeng Wei
- Sihan Cao
- Siying Huang
- Tao Jiang
- Weihao Gao
- Weimin Xiong
- Weiran He
- Weixiao Huang
- Weixin Xu
- Wenhao Wu
- Wenyang He
- Xianghui Wei
- Xianqing Jia
- Xingzhe Wu
- Xinran Xu
- Xinxing Zu
- Xinyu Zhou
- Xuehai Pan
- Y. Charles
- Yang Li
- Yangyang Hu
- Yangyang Liu
- Yanru Chen
- Yejie Wang
- Yibo Liu
- Yidao Qin
- Yifeng Liu
- Ying Yang
- Yiping Bao
- Yulun Du
- Yuxin Wu
- Yuzhi Wang
- Zaida Zhou
- Zhaoji Wang
- Zhaowei Li
- Zhen Zhu
- Zheng Zhang
- Zhexu Wang
- Zhilin Yang
- Zhiqi Huang
- Zihao Huang
- Ziyao Xu
- Zonghan Yang
- Zongyu Lin
published_at: '2025-01-22 00:00:00'
theme_ids:
- multimodal_models
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
# Kimi k1.5: Scaling Reinforcement Learning with LLMs

Kimi k1.5 demonstrates that a simplistic reinforcement learning framework — long-context scaling combined with online mirror descent, without Monte Carlo tree search, value functions, or process reward models — is sufficient to match OpenAI o1 on reasoning benchmarks. The paper introduces context window length as an independent RL scaling axis, validates long-CoT-to-short-CoT knowledge transfer at up to +550% improvement over GPT-4o and Claude 3.5 Sonnet, and articulates a clear taxonomy of open problems that block RL scaling beyond verifiable STEM and coding tasks.

**Authors:** Kimi Team (96 total, led by Moonshot AI)
**Published:** 2025-01-22
**Type:** Paper · [arXiv 2501.12599](https://arxiv.org/pdf/2501.12599)
**Themes:** [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] · [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/policy_optimization|Policy Optimization]] · [[themes/reinforcement_learning|Reinforcement Learning]] · [[themes/multimodal_models|Multimodal Models]]

---

## Motivation

Two independent ceilings were converging before this work. First, pretraining via next-token prediction is bounded by available high-quality data — Villalobos et al. 2024 and Muennighoff et al. 2023 identify data exhaustion as an imminent wall even as Kaplan-style scaling laws continue to hold empirically. Second, prior published RL-with-LLM work had not produced competitive results at frontier performance levels, leaving the approach theoretically promising but practically unvalidated.

Existing test-time compute methods that achieve planning-like behavior (MCTS, explicit value functions, process reward models) introduce significant deployment complexity and require critic models that evaluate partial solutions mid-generation — expensive and brittle. Meanwhile, short-CoT models like GPT-4o and Claude Sonnet 3.5 performed substantially below long-CoT models on hard reasoning, with no established method for transferring long-CoT priors without retraining from scratch.

---

## Approach

### Implicit Planning via Long Context

Kimi k1.5 reframes planning as a sequence modelling problem. Rather than building an explicit search tree, the model learns trial-and-error, backtracking, and self-correction entirely within a long autoregressive context window. The planning algorithm `A(·|z1, z2, ...)` acting on a history of reasoning steps is approximated by a single model generating long chains of thought — the search tree is "flattened" into the context. This eliminates MCTS, value networks, and process reward models at both training and inference time.

### Policy Optimization

The core algorithm is a variant of **online mirror descent** with KL-regularization relative to a reference policy updated each iteration. Unlike standard REINFORCE:
- Responses are sampled from the reference policy (off-policy)
- An L2 penalty on the log-ratio replaces the value baseline
- The value network is **deliberately excluded** — value functions structurally penalize exploratory wrong reasoning steps that later self-correct, suppressing the trial-and-error behavior essential for long-CoT learning

### Context Length as a Scaling Axis

RL training context is scaled to **128k tokens**. The paper empirically shows continued performance improvement as context length increases, establishing context window length as an independent scaling axis for RL with LLMs analogous to parameter count in pretraining. Partial rollouts reuse large chunks of prior trajectories to avoid regeneration cost, improving training efficiency substantially.

### Prompt Set Curation

Three quality criteria: diverse coverage, balanced difficulty, accurate evaluability. Filters exclude:
- Multiple-choice and true/false questions (reward-hackable via small answer space)
- Proof-based questions (verification is undecidable)
- Prompts where the model can guess the correct answer without CoT within 8 attempts (easy-to-hack)

Difficulty is assessed via pass rate from 10 SFT model samples. Difficulty-adaptive sampling combines **curriculum sampling** (easy-to-hard progression) with **prioritized sampling** (problems weighted by `1 - success_rate`).

### Chain-of-Thought Reward Model

A CoT-RM trained on ~800k labeled examples achieves **98.5% accuracy** on manual spot checks versus **84.4%** for a classic discriminative reward model. Used as the primary math reward signal. The gap matters because different written forms of the same answer (e.g., equivalent fractions) fool discriminative RMs but not CoT-RMs.

### Length Penalty

To counteract "overthinking" — response lengths growing excessively during RL training — a length penalty is applied: among correct responses, shorter ones are rewarded and longer ones penalized; among incorrect responses, all long responses are penalized. The penalty is warmed up gradually to avoid degrading early-stage performance.

### Long2Short Transfer

Four complementary methods distill long-CoT reasoning into short-CoT models:
1. **Model weight averaging** — merge long-CoT and short-CoT model weights
2. **Shortest rejection sampling** — select the shortest correct response from n=8 samples
3. **DPO** — shortest-correct as positive, longer responses as negative
4. **Long2short RL** — reduced maximum rollout length + active length penalty

---

## Results

| Benchmark | Kimi k1.5 (long) | OpenAI o1 | Kimi k1.5 (short) | GPT-4o | Claude 3.5 Sonnet |
|---|---|---|---|---|---|
| AIME 2024 | 77.5 | 74.4 | 60.8 | 9.3 | — |
| MATH 500 | 96.2 | 94.8 | 94.6 | 74.6 | — |
| Codeforces | 94th pct | 94th pct | — | — | — |
| MathVista | 74.9 | 71.0 | — | — | — |
| MMMU | 70.3 | 77.3 | — | — | — |
| LiveCodeBench v4 | — | — | 47.3 | — | 33.4 |

The long-CoT model matches o1 across domains. The short-CoT model outperforms GPT-4o on AIME 2024 by **+554%**, demonstrating that long2short transfer is not merely marginal.

---

## Limitations & Open Problems

### Training Signal

- **Reward hacking** is a structural constraint: models exploit verifiable signals when answer spaces are small. The filtering heuristics (excluding MC/T-F/proof questions, running no-CoT guessing) reduce but do not eliminate the problem, and the filtering pipeline itself requires manual calibration.
- **Classic discriminative reward models achieve only 84.4% accuracy** on math evaluation — insufficient for reliable RL training, especially with equivalent but differently-expressed answers. The CoT-RM mitigates this but requires 800k labeled examples to train.
- **Verifier construction for non-STEM domains remains unsolved** and is explicitly flagged as an open direction. The entire RL framework is structurally restricted to tasks with binary verifiable outcomes. Creative writing, open-ended QA, and agentic multi-step tasks receive no coverage.

### Context & Compute

- **Overthinking**: response lengths grow excessively during RL training, increasing training and inference costs without proportional quality gains. The length penalty addresses symptoms but not the root cause — the model lacks well-calibrated internal token budget estimation (evidenced by large length variation across runs of the same problem).
- **Long-CoT inference cost** is fundamentally higher than short-CoT. o1-level reasoning requires substantially more tokens, making long-CoT economically impractical for latency-sensitive applications. Long2short transfer is a workaround, not a solution.

### Data Coverage

- **Only ~32% of web-sourced coding contest problems** can be converted into valid RL training problems. Most are either not automatable (require special judge), fail test case generation, or fail ground-truth verification. The CYaRon-based pipeline is an improvement but leaves the majority of available data inaccessible.
- **Multimodal vision RL is constrained** to categorized data types (STEM questions, location guessing, chart analysis, synthetic scenes, text-rendered images). Real-world unstructured visual tasks are not represented.

### Credit Assignment

- **Conventional value functions are structurally unsuitable** for long-CoT RL: they penalize exploratory wrong reasoning steps that later self-correct. Excluding the value network is presented as a solution, but this removes the primary mechanism for dense credit assignment — the model learns only from terminal outcomes, which may limit learning efficiency on very long reasoning traces.
- **RL sample efficiency remains low**: even with curriculum and prioritized sampling, the per-problem sample efficiency of RL is substantially lower than supervised methods. Partial rollout reuse improves wall-clock efficiency but does not change the fundamental sample complexity.

---

## Key Breakthroughs

**o1 without MCTS** — The central result: a simplistic RL framework (online mirror descent + long context + length penalty + curriculum sampling) matches OpenAI o1 on reasoning benchmarks without any of the infrastructure-heavy components assumed necessary. This validates that planning can emerge from long-context RL rather than requiring explicit search.

**Context window as an independent RL scaling axis** — Empirically confirmed: increasing RL context window from shorter baselines to 128k yields continued performance improvement. This opens a new scaling dimension orthogonal to parameter count and pretraining data, with clear implications for how RL compute should be allocated going forward.

**Long2short transfer at scale** — Up to +550% improvement over GPT-4o and Claude 3.5 Sonnet on short-CoT benchmarks. This suggests that long-CoT training is not just a deployment format choice but a fundamentally different capability acquisition pathway whose benefits can be partially transferred to inference-efficient models.

---

## Open Questions

- Can the CoT-RM approach generalize beyond math to construct reliable verifiers for open-ended tasks? What is the minimum label set required, and how does accuracy scale?
- Is the exclusion of value networks fundamental to long-CoT RL, or can a modified credit assignment mechanism recover dense learning signal without suppressing exploration?
- What is the theoretical relationship between context window length and implicit search depth? Is there a formal equivalence between token budget and search budget?
- How much of the long2short transfer benefit is attributable to each of the four methods independently? Are model weight averaging and DPO complementary or redundant?
- Does the RL scaling curve saturate at 128k context, or does continued extension yield continued gains?

---

## Connections

- Validates the general RL-for-reasoning hypothesis explored concurrently in DeepSeek-R1 and OpenAI o1 system card
- Extends [[themes/test_time_compute_scaling|test-time compute scaling]] beyond inference-time MCTS (cf. Snell et al. 2024) to a training-time framework
- The long2short transfer approach is mechanistically related to [[themes/policy_optimization|policy distillation]] but operates via weight averaging rather than KL-constrained imitation
- The CoT-RM design echoes Lightman et al. 2023 process reward models but uses generative rather than discriminative evaluation, trading inference cost for accuracy

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/long-chain-of-thought|Long Chain-of-Thought]]
- [[entities/math500|MATH500]]
- [[entities/model-merging|Model Merging]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/reward-hacking|Reward Hacking]]
