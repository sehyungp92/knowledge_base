---
type: source
title: 'GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models'
source_id: 01KJTMGSTSRJEV5VTV93WVW7P9
source_type: paper
authors:
- GLM-4. 5 Team
- ':'
- Aohan Zeng
- Xin Lv
- Qinkai Zheng
- Zhenyu Hou
- Bin Chen
- Chengxing Xie
- Cunxiang Wang
- Da Yin
- Hao Zeng
- Jiajie Zhang
- Kedong Wang
- Lucen Zhong
- Mingdao Liu
- Rui Lu
- Shulin Cao
- Xiaohan Zhang
- Xuancheng Huang
- Yao Wei
- Yean Cheng
- Yifan An
- Yilin Niu
- Yuanhao Wen
- Yushi Bai
- Zhengxiao Du
- Zihan Wang
- Zilin Zhu
- Bohan Zhang
- Bosi Wen
- Bowen Wu
- Bowen Xu
- Can Huang
- Casey Zhao
- Changpeng Cai
- Chao Yu
- Chen Li
- Chendi Ge
- Chenghua Huang
- Chenhui Zhang
- Chenxi Xu
- Chenzheng Zhu
- Chuang Li
- Congfeng Yin
- Daoyan Lin
- Dayong Yang
- Dazhi Jiang
- Ding Ai
- Erle Zhu
- Fei Wang
- Gengzheng Pan
- Guo Wang
- Hailong Sun
- Haitao Li
- Haiyang Li
- Haiyi Hu
- Hanyu Zhang
- Hao Peng
- Hao Tai
- Haoke Zhang
- Haoran Wang
- Haoyu Yang
- He Liu
- He Zhao
- Hongwei Liu
- Hongxi Yan
- Huan Liu
- Huilong Chen
- Ji Li
- Jiajing Zhao
- Jiamin Ren
- Jian Jiao
- Jiani Zhao
- Jianyang Yan
- Jiaqi Wang
- Jiayi Gui
- Jiayue Zhao
- Jie Liu
- Jijie Li
- Jing Li
- Jing Lu
- Jingsen Wang
- Jingwei Yuan
- Jingxuan Li
- Jingzhao Du
- Jinhua Du
- Jinxin Liu
- Junkai Zhi
- Junli Gao
- Ke Wang
- Lekang Yang
- Liang Xu
- Lin Fan
- Lindong Wu
- Lintao Ding
- Lu Wang
- Man Zhang
- Minghao Li
- Minghuan Xu
- Mingming Zhao
- Mingshu Zhai
- Pengfan Du
- Qian Dong
- Shangde Lei
- Shangqing Tu
- Shangtong Yang
- Shaoyou Lu
- Shijie Li
- Shuang Li
- Shuang-Li
- Shuxun Yang
- Sibo Yi
- Tianshu Yu
- Wei Tian
- Weihan Wang
- Wenbo Yu
- Weng Lam Tam
- Wenjie Liang
- Wentao Liu
- Xiao Wang
- Xiaohan Jia
- Xiaotao Gu
- Xiaoying Ling
- Xin Wang
- Xing Fan
- Xingru Pan
- Xinyuan Zhang
- Xinze Zhang
- Xiuqing Fu
- Xunkai Zhang
- Yabo Xu
- Yandong Wu
- Yida Lu
- Yidong Wang
- Yilin Zhou
- Yiming Pan
- Ying Zhang
- Yingli Wang
- Yingru Li
- Yinpei Su
- Yipeng Geng
- Yitong Zhu
- Yongkun Yang
- Yuhang Li
- Yuhao Wu
- Yujiang Li
- Yunan Liu
- Yunqing Wang
- Yuntao Li
- Yuxuan Zhang
- Zezhen Liu
- Zhen Yang
- Zhengda Zhou
- Zhongpei Qiao
- Zhuoer Feng
- Zhuorui Liu
- Zichen Zhang
- Zihan Wang
- Zijun Yao
- Zikang Wang
- Ziqiang Liu
- Ziwei Chai
- Zixuan Li
- Zuodong Zhao
- Wenguang Chen
- Jidong Zhai
- Bin Xu
- Minlie Huang
- Hongning Wang
- Juanzi Li
- Yuxiao Dong
- Jie Tang
published_at: '2025-08-08 00:00:00'
theme_ids:
- adaptive_computation
- agent_systems
- model_architecture
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models

GLM-4.5 is a 355B-parameter (32B activated) open-source Mixture-of-Experts model from Zhipu AI that achieves top-3 global ranking simultaneously across agentic, reasoning, and coding tasks — the first open-source model to do so. The paper documents a full-stack training methodology including architectural innovations, a two-stage post-training regime separating expert specialization from unification via self-distillation, and several RL training insights that overturn prior best practices (notably, multi-stage progressive RL is shown to be actively harmful). The work is as much a training methodology report as a model release.

**Authors:** GLM-4.5 Team (172 total, led by Aohan Zeng, Xin Lv, Qinkai Zheng, et al.)
**Published:** 2025-08-08
**Type:** Paper
**Source:** https://arxiv.org/pdf/2508.06471

---

## Motivation

Prior to GLM-4.5, no single open-source model had achieved competitive performance across all three of the ARC capability axes — agentic task completion, mathematical/scientific reasoning, and software engineering. Closed-source leaders like OpenAI o3 and Claude Sonnet 4 dominated individual domains, while open-source alternatives either specialized narrowly or required substantially more parameters without commensurate gains. Existing MoE models like DeepSeek-V3 (671B total) and Kimi K2 (1043B total) pointed to poor parameter efficiency. Meanwhile, several RL training practices that had become standard — multi-stage progressive output-length scaling, sequence-mean loss for code, uniform difficulty sampling — were never rigorously challenged.

---

## Architecture

GLM-4.5 adopts a **deeper-rather-than-wider** MoE design philosophy, motivated by empirical findings that depth improves reasoning capacity more than width:

- **89 MoE layers** at 5120 hidden dimension (vs. DeepSeek-V3's 58 layers at 7168 hidden dim)
- **96 attention heads** for 5120 hidden dim — 2.5× more than comparable models. Counterintuitively, this does not improve training loss but consistently improves reasoning benchmark scores
- **MTP layer** implemented as an additional MoE layer for multi-token prediction, supporting speculative decoding at inference
- **QK-Norm** for attention logit stabilization
- **Loss-free balance routing** with sigmoid gates for MoE layers
- **Muon optimizer** for all parameters except embeddings, bias, and RMSNorm weights — shown to accelerate convergence and tolerate larger batch sizes

The architecture sits on the [[themes/model_architecture|model architecture]] Pareto frontier for SWE-bench performance vs. active parameter count, outperforming models with substantially more active parameters.

See also: [[themes/adaptive_computation|adaptive computation]] (MTP / speculative decoding angle)

---

## Training Pipeline

### Pre-training & Mid-training

Three-stage training on **23T tokens total**:

1. **General pre-training** — 15T tokens, 4K context
2. **Code/reasoning continual pre-training** — 7T tokens, up to 32K context; includes repo-level code with cross-file dependencies, GitHub PRs/issues/commits in diff format, and synthetic reasoning traces
3. **Long-context/agent mid-training** — 100B tokens, extended to 128K context; adds large-scale synthetic agentic trajectories

Data deduplication uses both MinHash and **SemDedup** (embedding-based) to catch template-generated similar pages that evade hash-based methods. Cosine decay outperforms WSD learning rate schedule on general benchmarks (SimpleQA, MMLU), with WSD causing underfitting in the stable training stage.

### Post-training: Two Stages

**Stage 1 — Expert Training:** Three specialist models are trained independently:
- *Reasoning Expert* — SFT cold-start → domain-specific reasoning RL
- *Agent Expert* — SFT cold-start → agentic RL
- *General Chat Expert* — SFT cold-start → general/RLHF/RLAIF RL

**Stage 2 — Unified Training:** Millions of samples generated from all three expert models are used in Overall SFT to train a single unified base model. This **self-distillation** approach produces a hybrid model supporting both thinking (long CoT) and non-thinking (direct response) modes — without requiring separate model deployments.

---

## Reasoning RL Innovations

### Two-Stage Difficulty Curriculum

Standard RL with uniform difficulty sampling stalls as the model saturates moderate-difficulty problems. GLM-4.5 uses a two-stage curriculum:

1. Train on moderate-difficulty problems until plateau
2. Switch to **extremely hard problems** (pass@8 = 0 but pass@512 > 0) — problems the model cannot solve greedily but can occasionally solve with many samples

This enables the model to consistently surpass its prior performance ceiling. See [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

### Single-Stage vs. Multi-Stage Output Length Scaling

> **Key finding overturning prior practice:** Multi-stage RL with progressively increasing output lengths causes **irreversible catastrophic forgetting** of long-context capabilities acquired during SFT. Even a final full-length RL stage cannot recover this loss.

Single-stage RL conducted directly at the target 64K output length outperforms the multi-stage approach. This is a significant methodological correction for the field.

### Dynamic Sampling Temperature

When rollout rewards stabilize (a sign of insufficient exploration), temperature is increased. A quality-control mechanism periodically evaluates on a held-out validation set to cap temperature at the maximum that does not cause >1% performance drop. This adds implementation complexity but prevents reward collapse.

### Token-Weighted Mean Loss for Code RL

Sequence-mean loss over code rollouts gives equal weight to long and short responses, creating a length bias and encouraging generation of trivial base-case solutions. **Token-weighted mean loss** provides finer-grained gradient signals, suppresses base-case generation, and achieves significantly faster convergence.

### Data Quality for Science RL

Expert-verified multiple-choice-only questions dramatically outperform mixed-quality or unverified data on GPQA-Diamond. This creates a hard scalability bottleneck: the science RL data pipeline cannot be industrialized without maintaining expert verification quality.

---

## Agentic RL Innovations

### Iterative Self-Distillation Loop

Rather than running RL to convergence in one pass, GLM-4.5 alternates:

```
RL training → generate superior SFT data from RL-trained model
→ re-SFT base model → further RL at higher difficulty
→ repeat
```

This progressively pushes performance beyond the RL plateau without requiring a fundamentally different RL algorithm. See [[themes/agent_systems|agent systems]], [[themes/reinforcement_learning|reinforcement learning]].

### Test-Time Compute Scaling via Interaction Turns

A key finding for [[themes/software_engineering_agents|software engineering agents]] and web agents: BrowseComp accuracy scales **smoothly on a log scale** with the number of environment interaction turns. This is the agentic analogue of token-length scaling in reasoning models — more thinking turns ↔ more interaction turns. The implication is that inference-time budget should be allocated to interaction depth, not just generation length.

### Outcome Supervision with Format Penalties

Agent traces that fail to produce correct tool call formats are halted immediately and receive zero reward. This outcome-plus-format approach provides clean supervision without step-level reward engineering.

### XML Function Call Templates

JSON function call templates impose character-escaping overhead on code-containing parameters, increasing token count and learning burden. GLM-4.5 introduces XML-tagged templates that encapsulate keys and values directly, substantially reducing escaping without compromising function call accuracy.

### End-to-End Multi-Turn Function Calling RL

Rather than step-wise RL with static predetermined decision flows, GLM-4.5 trains on **full trajectory reward** — the model generates the complete multi-step trajectory and is rewarded based on final task completion. LLM-simulated user agents enable multi-turn scenarios at training scale. This allows the model to develop dynamic planning and recovery strategies that step-wise RL cannot.

### Automated Agentic SFT Data Pipeline

Four-step pipeline for constructing agentic training data at scale:
1. Collect real-world agentic frameworks, APIs, and MCP servers
2. LLM-synthesize tasks grounded in collected tools
3. Generate trajectories with LLM user simulator
4. Multi-judge quality filtering

---

## General RL

Multi-source reward system combining:
- Rule-based feedback (verifiable tasks)
- Human preference annotations (RLHF)
- AI feedback (RLAIF)

**Pathology RL** specifically targets low-frequency failure modes (language mixing, repetition, formatting errors) using prompts curated to trigger these behaviors. Although these occur at <1% rate, they are sample-inefficient to fix through standard RL — a dedicated targeted dataset is necessary.

**SFT data quality** findings: removing the bottom 50% of prompts by response length improves math and science performance by 2–4% despite training on half the data. Applying response scaling (4 responses per hard prompt) adds a further 1–2% on top.

---

## Infrastructure: Slime Framework

GLM-4.5's RL training infrastructure supports both:
- **Colocated synchronous** training (for reasoning/math RL)
- **Disaggregated asynchronous** training (for agentic RL, where rollouts are long and latency-sensitive)

Rollout efficiency is identified as the **persistent throughput bottleneck** across all RL training. Mitigations include FP8 quantization for rollout generation (vs. BF16 for training) and specialized hardware scheduling. This infrastructure complexity is a barrier to reproduction.

---

## Performance

| Benchmark | GLM-4.5 | Notes |
|---|---|---|
| TAU-Bench | 70.1% | Agentic; 2nd among open-source |
| AIME 24 | 91.0% | Mathematical reasoning |
| SWE-bench Verified | 64.2% | Software engineering |
| GPQA-Diamond | — | Science reasoning |
| HLE | 14.4% | Best model (Grok 4): 23.9% |
| BrowseComp | 26.4% | o3 leads at 49.7% |
| SimpleQA | 26.4% | Gemini 2.5 Pro: 54.0% |
| Terminal-Bench | 37.5% | Best model (Claude Opus 4): 43.2% |

GLM-4.5 ranks **3rd overall** across all models evaluated and **2nd on agentic benchmarks**, with only half the parameters of DeepSeek-R1 and one-third those of Kimi K2.

---

## Limitations and Open Questions

### Fundamental Capability Gaps

**HLE (Humanity's Last Exam):** All frontier models score dramatically below human expert level. GLM-4.5 at 14.4%, best-in-class Grok 4 at 23.9%. Genuine expert-level reasoning across disciplines remains unsolved. See [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

**Web browsing agents:** A large discontinuity exists between o3 (49.7% BrowseComp) and the second tier (GLM-4.5: 26.4%, o4-mini-high: 28.3%). Web agent capability is not uniformly distributed — something in o3's training produces qualitatively different browsing behavior that the field does not yet understand.

**Terminal-Bench:** All frontier models perform poorly (best: Claude Opus 4 at 43.2%). Complex terminal environment task completion remains largely unsolved even at frontier scale.

**SimpleQA factual recall:** Wide variation across frontier models (GLM-4.5: 26.4%, Gemini 2.5 Pro: 54.0%) reveals that factual grounding is not a solved problem and is not correlated with overall model capability.

### Training Bottlenecks

**Rollout throughput:** Data generation during RL dominates wall-clock training time. Every RL technique described in this paper depends on fast, high-volume rollout generation. This is the core scaling bottleneck for both reasoning and agentic RL.

**Science RL data quality gate:** Only expert-verified multiple-choice questions produce effective training signal for science domains. Mixed-quality data significantly degrades outcomes. This hard quality requirement severely limits the scalability of science RL to new domains.

**Heterogeneous agentic framework diversity:** Each real-world agentic framework (OpenHands, BrowseComp harness, etc.) uses different rollout formats, reward structures, and environment interfaces. Scaling agentic RL across diverse deployment contexts requires significant integration engineering per framework.

### Context and Efficiency

**128K context insufficient for complex SWE tasks:** SWE-bench evaluation requires history truncation even at 128K — full context retention for long-horizon software engineering tasks exceeds current practical context limits.

**Token efficiency vs. task success tradeoff:** GLM-4.5 uses 695K tokens/interaction vs. Claude Sonnet 4's 2M, but still loses 50% of CC-Bench coding competitions. The relationship between token efficiency and task success is non-trivial and context-dependent.

### Safety

**Unfairness and Bias:** GLM-4.5 scores 77.4% on this safety dimension vs. 91–97% on all other safety categories. This is acknowledged as an ongoing focus area.

---

## Key Methodological Findings (Summary)

| Finding | Prior Practice | GLM-4.5 Finding |
|---|---|---|
| RL output length scaling | Multi-stage progressive | Single-stage at max length; multi-stage causes irreversible forgetting |
| Code RL loss | Sequence-mean | Token-weighted mean; faster convergence, less base-case collapse |
| Science RL data | Mixed-quality acceptable | Expert-verified only; mixed data significantly degrades outcomes |
| RL difficulty | Uniform sampling | Two-stage curriculum; hard problems unlock post-plateau gains |
| Agentic function calls | JSON templates | XML-tagged templates; lower escaping burden without accuracy cost |
| Agent RL | Step-wise reward | Full-trajectory reward; enables dynamic planning and recovery |
| Test-time scaling (agents) | Token length | Interaction turns; log-linear scaling with turn count |

---

## Connections

- [[themes/reinforcement_learning|Reinforcement Learning]] — Core training methodology; multiple RL innovations documented
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — Difficulty curriculum, output-length scaling, token-weighted loss
- [[themes/agent_systems|Agent Systems]] — Iterative self-distillation, end-to-end multi-turn RL, agentic SFT pipeline
- [[themes/software_engineering_agents|Software Engineering Agents]] — SWE-bench methodology, OpenHands integration, context truncation findings
- [[themes/model_architecture|Model Architecture]] — MoE depth-vs-width tradeoff, attention head scaling, MTP layer
- [[themes/adaptive_computation|Adaptive Computation]] — Test-time scaling via interaction turns; speculative decoding via MTP

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/humanitys-last-exam|Humanity's Last Exam]]
- [[entities/multi-token-prediction-mtp|Multi-Token Prediction (MTP)]]
- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/qk-norm|QK-Norm]]
- [[entities/tau-bench|tau-bench]]
