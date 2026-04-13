---
type: source
title: 'Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation
  and Agentic RL'
source_id: 01KJTMK79EGQTSBGMN1B215EKM
source_type: paper
authors:
- Weizhen Li
- Jianbo Lin
- Zhuosong Jiang
- Jingyi Cao
- Xinpeng Liu
- Jiayu Zhang
- Zhenqiang Huang
- Qianben Chen
- Weichen Sun
- Qiexiang Wang
- Hongxuan Lu
- Tianrui Qin
- Chenghao Zhu
- Yi Yao
- Shuying Fan
- Xiaowan Li
- Tiannan Wang
- Pai Liu
- King Zhu
- He Zhu
- Dingfeng Shi
- Piaohong Wang
- Yeyi Guan
- Xiangru Tang
- Minghao Liu
- Yuchen Eleanor Jiang
- Jian Yang
- Jiaheng Liu
- Ge Zhang
- Wangchunshu Zhou
published_at: '2025-08-06 00:00:00'
theme_ids:
- agent_systems
- finetuning_and_distillation
- multi_agent_coordination
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL

Chain-of-Agents (CoA) proposes collapsing multi-agent system collaboration into a single model's decoding process, eliminating the coordination overhead and training opacity of conventional MAS while preserving collaborative problem-solving patterns. By distilling trajectories from a state-of-the-art open-source multi-agent system (OAgents) and fine-tuning with agentic RL (DAPO), the resulting Agent Foundation Models (AFMs) achieve new SOTA among same-size models across ~20 agent benchmarks — with 84.6% fewer tokens than the teacher system — while remaining fully open-sourced.

**Authors:** Weizhen Li, Jianbo Lin, Zhuosong Jiang, Jingyi Cao, Xinpeng Liu, et al. (30 total)
**Published:** 2025-08-06
**Type:** Paper
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]

---

## Motivation

Three interlocking failures motivate this work:

**Multi-agent systems (MAS) cannot learn.** Current MAS are built on manual prompt and workflow engineering. LLM backbones inside agent frameworks are static — they cannot receive gradient signal across agent boundaries and cannot improve via data-centric training on agentic tasks. Coordination cost scales quadratically with agent count, fundamentally constraining deployment.

**Tool-Integrated Reasoning (TIR) cannot collaborate.** TIR models (Search-R1, WebThinker, WebDancer) are end-to-end trainable but locked into a linear ReAct-style think-action-observation loop. They lack mechanisms for synergistic multi-tool coordination and bidirectional tool dependencies, and suffer from reward sparsity in multi-step sequences.

**Neither paradigm supports the other.** MAS has collaboration but not trainability; TIR has trainability but not collaboration. CoA is designed to merge both properties in a single model.

---

## The Chain-of-Agents Paradigm

CoA reformulates multi-agent collaboration as a structured decoding process within one model. Rather than routing tasks across separate agent processes, the model maintains a persistent reasoning state $S_t$ and samples from a role distribution at each step — dynamically activating:

- **Role-playing agents:** Thinking, Plan, Reflection, Verification
- **Tool agents:** Search, Crawl, Code Generate

This eliminates inter-agent message passing entirely. Because the full trajectory lives within one model, end-to-end gradient optimisation becomes tractable. Unlike TIR's rigid pipeline, CoA supports adaptive orchestration — including bidirectional tool dependencies and multi-strategy search patterns that TIR cannot represent.

The paradigm generalises: CoA "supports almost any multi-agent system by flexibly defining multiple agents corresponding to different tools and roles."

---

## Training Pipeline

### Stage 1: Multi-Agent Distillation (SFT)

OAgents — the state-of-the-art open-source MAS — is used as a teacher system. Successful agentic trajectories are recorded (agent activation, reasoning state, output at each step) and converted into CoA-formatted SFT data.

A four-stage progressive quality filter ensures training signal quality:
1. **Complexity filter:** trajectories with fewer than 5 agent-tool interactions excluded
2. **Correctness filter:** incorrect answers, redundant tool inputs, instruction violations removed
3. **Reflection filter:** trajectories lacking reflection mechanisms excluded
4. **Error-correction upsampling:** trajectories demonstrating error recovery upweighted

Observation tokens are masked during SFT to prevent environmental noise from entering the loss, establishing a stable cold start for RL. *Note: this success-bias in training data means models may underlearn robust error recovery from failure states.*

### Stage 2: Agentic RL (DAPO)

Following SFT, DAPO reinforcement learning further refines the policy on verifiable tasks:
- **Code/math tasks:** reward = answer correctness × format compliance
- **Web agent tasks:** binary LLM-as-Judge reward (Qwen-2.5-72B evaluator)

RL training filters to challenging queries (pass rate ≤ 0.3) to concentrate compute where tool-based reasoning adds genuine value. Queries with pass rate > 0.3 are excluded — meaning models may underperform when parametric knowledge and tool use need to be combined.

---

## Results

### Web & General Reasoning

| Benchmark | AFM-32B | Prior Best (same size) | GPT-4.1-based MAS |
|---|---|---|---|
| GAIA (text-only) | **55.3%** | WebSailor 46.6% | OAgents 58.3%, OWL 55.8% |
| WebWalker | **63.0%** | WebShaper 51.4% | — |
| BrowseComp | **11.1%** | — | — |
| HLE (text-only) | **18.0%** | WebThinker-RL w/ QwQ-32B: 15.8% | — |

### Mathematical Reasoning

AFM-RL-32B achieves **59.8% on AIME2025** — a 10.5% absolute improvement over prior best TIR method (ReTool-32B: 49.3%) — and 78.0% average across five math benchmarks, 3.6% above ReTool-32B.

### Code Generation

AFM-RL-32B achieves 47.9% on LiveCodeBench v5 and 32.7% on CodeContests, outperforming ReTool and ReVeal.

### Efficiency

84.6% reduction in token consumption vs OAgents (24,047 vs 156,400 average tokens per task), with fewer tool calls per task. Multi-agent distillation compresses collaborative reasoning without sacrificing quality.

### Test-Time Scaling

Pass@3 yields substantial additional gains over base Pass@1:

| Benchmark | Pass@1 | Pass@3 | Gain |
|---|---|---|---|
| GAIA | 55.3% | 69.9% | +14.6 |
| WebWalker | 63.0% | 78.7% | +15.7 |
| HLE | 18.0% | 33.2% | +15.2 |
| BrowseComp | 11.1% | 19.2% | +8.1 |

AFM's Pass@3 gains outpace all compared systems (WebDancer +10.6, WebSailor +9.9 on GAIA vs AFM +14.6).

### Small Model Efficiency

The 7B AFM matches or exceeds 32B TIR baselines — achieving 15.6% on HLE vs 15.8% for WebThinker-RL with a QwQ-32B backbone. SFT alone contributed 22.0% average accuracy gain for 7B; RL added a further 20.8% over SFT baseline.

---

## Limitations & Open Questions

**Hard capability ceilings remain.** A 12-point gap persists on GAIA between AFM-32B (55.3%) and proprietary-backbone full MAS (OAgents 66.7%, DeepResearch 67.4%). HLE performance of 18.0% means ~82% of expert-level multi-disciplinary problems remain unsolved. BrowseComp at 11.1% confirms that persistent, creative multi-strategy search for obscure verifiable facts is still far beyond reliable agentic reach.

**Tool format brittleness blocks zero-shot generalisation.** Code agent models successfully invoke unseen tools (Web Search, Visual Inspector) at inference given schema prompts. But web-agent models fail on tools requiring character-level format precision — parser errors and task abortions result from minor formatting deviations (e.g., missing triple backtick wrapping). Universal agentic deployment across heterogeneous tool ecosystems without per-tool fine-tuning remains unsolved.

**Bootstrapping requires the expensive system you're trying to replace.** CoA trajectory generation requires a functioning state-of-the-art MAS (OAgents) as teacher. The method cannot bootstrap from scratch — it inherits a dependency on exactly the infrastructure it aims to supersede.

**Hard inference caps.** A maximum of 12 tool calls per inference run artificially limits task complexity. Multi-step tasks requiring more sequential interactions cannot be completed end-to-end.

**Evaluation coverage gaps.** HLE and BrowseComp evaluations use text-only subsets, blocking measurement of true agentic capability on multi-modal expert tasks. High variance on small benchmarks (AIME24/25: 30 examples, AMC23: 40 examples) requires avg@16 sampling to attenuate noise, tripling effective inference cost.

**LLM-as-Judge reward introduces bias and latency.** Web agent RL training uses binary judgment from Qwen-2.5-72B because F1/EM metrics fail on open-ended tasks. This introduces judge model bias and overhead at every RL training step.

**Success-biased training data.** The four-stage quality filter removes failure trajectories systematically. Models may not learn robust recovery from the kinds of errors they will encounter in deployment.

---

## Breakthroughs

**Chain-of-Agents paradigm** — the first framework enabling a single end-to-end trainable model to fully simulate any multi-agent system, merging MAS collaboration patterns with TIR's gradient optimisability in one unified inference pass. This reframes the MAS/single-model distinction as architectural rather than fundamental.

**Multi-agent distillation** — a systematic method for transferring collaborative intelligence from MAS into single LLMs via trajectory extraction and progressive quality filtering. Establishes a general template for compressing expensive multi-agent inference into efficient single-model deployment.

---

## Structural Implications

The CoA result suggests that the apparent dichotomy between "a single model" and "a multi-agent system" may dissolve as training methods mature. If multi-agent collaboration can be fully captured in one model's decoding process with 84.6% fewer tokens, the primary justification for separate-process MAS narrows to cases where independent parallelism or fault isolation is required — not expressive power.

Multi-agent distillation also establishes a reusable pattern: use expensive systems to generate high-quality training data, then distill down. This connects to broader [[themes/finetuning_and_distillation|distillation]] trends where frontier-model outputs bootstrap capable smaller models — here extended to the agentic trajectory domain.

The persistent gap between same-size AFM and proprietary-backbone full MAS signals that backbone capability remains a binding constraint: collaborative reasoning patterns can be compressed and trained into an open model, but raw model scale and proprietary training still contribute substantial performance headroom.

---

## Related Work

- OAgents — teacher system for multi-agent distillation; AFM approaches but does not close the gap with OAgents on GAIA
- WebThinker, WebDancer, WebShaper, WebSailor — TIR baseline family; AFM outperforms all on WebWalker and GAIA
- ReTool, ReVeal — code-tool TIR baselines; AFM-RL-32B outperforms on AIME2025 by 10.5% absolute
- DAPO — RL algorithm used for agentic post-training; see [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- GAIA, BrowseComp, HLE, WebWalker — primary evaluation benchmarks; see [[themes/agent_systems|Agent Systems]] for benchmark landscape

## Key Concepts

- [[entities/codecontests|CodeContests]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/react|ReAct]]
- [[entities/tool-integrated-reasoning-tir|Tool-Integrated Reasoning (TIR)]]
