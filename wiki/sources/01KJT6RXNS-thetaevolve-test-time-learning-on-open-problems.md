---
type: source
title: 'ThetaEvolve: Test-time Learning on Open Problems'
source_id: 01KJT6RXNSQ8HZXA9JFP31EPRD
source_type: paper
authors:
- Yiping Wang
- Shao-Rong Su
- Zhiyuan Zeng
- Eva Xu
- Liliang Ren
- Xinyu Yang
- Zeyi Huang
- Xuehai He
- Luyao Ma
- Baolin Peng
- Hao Cheng
- Pengcheng He
- Weizhu Chen
- Shuohang Wang
- Simon Shaolei Du
- Yelong Shen
published_at: '2025-11-28 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 14
tags: []
---
# ThetaEvolve: Test-time Learning on Open Problems

**Authors:** Yiping Wang, Shao-Rong Su, Zhiyuan Zeng, Eva Xu, Liliang Ren, Xinyu Yang, Zeyi Huang, Xuehai He, Luyao Ma, Baolin Peng, Hao Cheng, Pengcheng He, Weizhu Chen, Shuohang Wang, Simon Shaolei Du, Yelong Shen
**Published:** 2025-11-28 00:00:00
**Type:** paper

## Analysis

# ThetaEvolve: Test-time Learning on Open Problems
2025-11-28 · paper · Yiping Wang, Shao-Rong Su, Zhiyuan Zeng, Eva Xu, Liliang Ren et al. (16 total)
https://arxiv.org/pdf/2511.23473

---

### Motivation & Prior Limitations
AlphaEvolve demonstrated that LLMs can evolve programs to improve bounds on open mathematical problems, but its design imposes significant resource and learning constraints that limit accessibility and adaptability. AlphaEvolve is closed-source and relies on ensembles of multiple frontier LLMs (Gemini-2.0-Flash/Pro), making it expensive and inaccessible to the broader research community. More fundamentally, AlphaEvolve is a pure inference system — the models do not update their weights based on experience, meaning they cannot internalize evolving strategies and must rediscover effective approaches from scratch each time.

---

### Proposed Approach
ThetaEvolve is an open-source framework that extends AlphaEvolve by combining in-context learning with Reinforcement Learning (RL) applied at test time, enabling a single model to continuously learn from its own evolutionary experience during optimization. Unlike AlphaEvolve's multi-model ensemble, ThetaEvolve operates with a single LLM, reducing resource requirements while maintaining competitive performance. Key technical components include a large program database for enhanced exploration, batch sampling for higher throughput, lazy penalties to discourage stagnant repetitive outputs, and optional reward shaping to produce stable RL training signals.

---

### Results & Capabilities
ThetaEvolve using DeepSeek-R1-0528-Qwen3-8B (an 8B open-source model) achieves new best-known bounds on both benchmark tasks, surpassing AlphaEvolve and ShinkaEvolve: a circle packing (CP) score of 2.63598308 vs. ShinkaEvolve's 2.63598283 and AlphaEvolve's 2.63586276, and a first autocorrelation inequality (FACI) score of 1.503133 vs. AlphaEvolve's 1.503164. The circle-packing program discovered by ThetaEvolve solves the problem in just 3 seconds, compared to approximately 75 seconds for ShinkaEvolve's program, representing a 25x improvement in runtime efficiency. Across two models and four open tasks, ThetaEvolve with test-time RL consistently outperforms inference-only baselines, and RL-trained checkpoints show faster progress and better final performance on both the trained task and previously unseen tasks, demonstrating generalization of learned evolving capabilities.

---

### Implications
ThetaEvolve demonstrates that small open-source models (8B parameters) can match or surpass closed frontier ensembles on genuine open mathematical problems when equipped with test-time learning, substantially lowering the resource bar for AI-assisted mathematical discovery. The finding that RL-trained checkpoints transfer to unseen tasks suggests that "evolving capability" is a learnable, generalizable skill rather than task-specific memorization, which has broad implications for how RL at test time might be used to bootstrap mathematical and scientific reasoning in smaller models. By releasing the framework publicly, ThetaEvolve enables the research community to independently pursue program-evolution approaches to open problems without reliance on proprietary frontier API access.

---

### Remaining Limitations & Next Steps
The source text is a truncated preprint excerpt, and explicit limitation sections are not present in the available text. The evaluation is restricted to a narrow set of benchmark tasks (circle packing and first autocorrelation inequality) explicitly drawn from AlphaEvolve's benchmark suite, leaving open the question of how broadly the approach generalizes to other classes of open problems. The system still requires sufficient compute for test-time RL training, and the comparison baseline (ShinkaEvolve) uses an ensemble of much larger frontier models, making raw compute parity difficult to assess. The extent to which the learned evolving capabilities transfer across fundamentally different mathematical domains beyond the four tasks tested remains an open question.

## Key Claims

1. AlphaEvolve relies on ensembles of frontier LLMs to achieve new bounds on open problems.
2. AlphaEvolve is a pure inference system in which models cannot internalize the evolving strategies they produce.
3. AlphaEvolve is a closed-source system.
4. ThetaEvolve is the first evolving framework to enable a small open-source model to achieve new best-known bounds on the open problems (circle packing and first autocorrelation inequality) mentioned in
5. ThetaEvolve with RL at test-time consistently outperforms inference-only baselines across two models and four open tasks.
6. RL-trained checkpoints in ThetaEvolve demonstrate faster progress and better final performance on both the trained target task and other unseen tasks, indicating the model learns generalizable evolvin
7. ThetaEvolve uses lazy penalties to discourage stagnant outputs.
8. ThetaEvolve uses optional reward shaping for stable training signals.
9. ThetaEvolve uses a large program database for enhanced exploration.
10. ThetaEvolve achieved a circle packing (CP) score of 2.63598308, surpassing AlphaEvolve (2.63586276) and ShinkaEvolve (2.63598283).

## Capabilities

- Test-time reinforcement learning enables a small open-source 8B model (DeepSeek-R1-0528-Qwen3-8B) to achieve new best-known bounds on open mathematical optimization problems, surpassing results from ensembles of frontier models like Gemini-2.0-Flash/Pro
- RL at test time enables models to learn genuinely transferable 'evolving capabilities' — RL-trained checkpoints show faster progress and better final performance on both trained tasks and previously unseen tasks
- Program evolution for mathematical discovery can be performed with a single LLM (rather than frontier model ensembles), using a large program database, batch sampling, lazy penalties, and optional reward shaping to achieve competitive or superior results
- Test-time program evolution can produce solutions with dramatically improved execution efficiency — the circle-packing program discovered by ThetaEvolve runs in 3 seconds vs ~75 seconds for a comparable frontier-model-based system
- Hybrid in-context learning and RL scaling at test time consistently outperforms inference-only program evolution baselines across multiple open optimization tasks

## Limitations

- AlphaEvolve is closed-source, blocking the research community from building on or auditing the system that first achieved new mathematical bounds via LLM-driven program evolution
- Pure inference-time program evolution systems (like AlphaEvolve) cannot allow models to internalize or retain the strategies they discover — each run starts from scratch without accumulated learning
- Frontier model ensembles are required by systems like AlphaEvolve to achieve competitive mathematical bounds, creating a high compute and cost barrier that limits accessibility and reproducibility
- Program evolution systems are susceptible to output stagnation — models repeatedly produce similar or identical programs — requiring explicit penalty mechanisms (lazy penalties) to maintain exploration
- RL training at test time is unstable without reward shaping, suggesting the raw reward signal from mathematical optimization problems is too sparse or noisy to train reliably on its own
- Evaluation is narrowly scoped to two specific open mathematical problems (circle packing and first autocorrelation inequality) and four tasks total, limiting generalisation claims
- The paper is a preprint and has not undergone peer review; all results should be treated as preliminary until independently validated
- The 'small model' used (DeepSeek-R1-0528-Qwen3-8B) is still an 8-billion parameter model, and the compute/time cost of running RL at test time over a large program database is not characterised in the abstract — resource requirements for practical use remain unclear

## Bottlenecks

- Mathematical discovery via program evolution has been gated behind closed-source frontier model ensembles, blocking independent researchers from reproducing, extending, or auditing the approach
- Inference-only program evolution cannot produce persistent learning — models must rediscover effective strategies from scratch on every run, wasting accumulated experience
- RL training instability in sparse mathematical reward settings limits how reliably test-time learning can be applied across diverse problem types without careful reward engineering

## Breakthroughs

- A single small open-source 8B model, trained with test-time RL, achieves new best-known bounds on open mathematical optimisation problems — surpassing results from systems using ensembles of frontier models (Gemini-2.0-Flash/Pro) and matching or beating Claude-sonnet-4/o4-mini ensembles
- Test-time RL enables models to genuinely internalise and accumulate 'evolving capabilities' — RL-trained checkpoints transfer faster progress and better final performance to previously unseen tasks, not just the training task

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_learning|test_time_learning]]
