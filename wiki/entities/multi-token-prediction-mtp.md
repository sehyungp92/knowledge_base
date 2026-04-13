---
type: entity
title: Multi-Token Prediction (MTP)
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- code_and_software_ai
- code_generation
- frontier_lab_competition
- model_architecture
- model_commoditization_and_open_source
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00010502196494091433
staleness: 0.0
status: active
tags: []
---
# Multi-Token Prediction (MTP)

> Multi-Token Prediction (MTP) is a training and inference technique in which a language model is trained to predict multiple future tokens simultaneously rather than one at a time. Implemented in GLM-4.5 as an auxiliary Mixture-of-Experts (MoE) layer, MTP serves a dual purpose: it enriches the training signal by forcing the model to plan ahead across a token sequence, and it enables speculative decoding at inference time — where draft tokens are generated in parallel and verified in bulk, substantially reducing latency without degrading output quality.

**Type:** method
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/model_architecture|Model Architecture]], [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/software_engineering_agents|Software Engineering Agents]]

---

## Overview

Multi-Token Prediction (MTP) addresses a structural inefficiency in standard autoregressive training: each forward pass produces a single token, meaning the model receives no direct supervisory signal about the coherence of longer spans it must eventually generate. By extending the prediction target to cover several tokens ahead, MTP encourages representations that encode local trajectory, not just next-token probability.

In GLM-4.5, MTP is realized as a dedicated additional MoE layer grafted onto the base model. This architectural choice keeps the primary model stream clean while giving the MTP head its own mixture of expert capacity — critical for a model that must generalise across agentic, reasoning, and coding registers simultaneously. At inference, the MTP head functions as a speculative decoder: it proposes candidate token sequences that the base model verifies in a single forward pass, compressing what would otherwise be several sequential decoding steps into one. The efficiency gain is especially significant for long agentic trajectories and code generation tasks, where the model must sustain coherent output over hundreds of tokens.

The technique has a direct lineage from DeepSeek-V3, which demonstrated that auxiliary prediction objectives — including MTP — could be applied at scale without destabilising training, contributing to a total training cost of approximately $5.576M for a frontier-class model when GPU-hours are priced at $2/hour. GLM-4.5's adoption of MTP is thus part of a broader trend of efficiency-focused architecture choices that allow parameter-efficient open-source models to approach or exceed the performance of larger proprietary systems.

---

## Role in GLM-4.5's Architecture and Performance

GLM-4.5 — a 355B total / 32B activated MoE model — is the primary publicly documented deployment of MTP. The model achieves results that contextualise the value of MTP's inference efficiency: 64.2% on SWE-bench Verified (surpassing GPT-4.1 at 48.6% and Gemini 2.5 Pro at 49.0%), 91.0% on AIME 24 (edging OpenAI o3's 90.3%), 70.1% on TAU-Bench, and 90.6% tool calling success on CC-Bench — the highest among evaluated baselines. It ranks 3rd overall and 2nd on agentic benchmarks while using roughly half the parameters of DeepSeek-R1 and one-third those of Kimi K2.

These numbers reflect a system where MTP-enabled speculative decoding is one of several interlocking efficiency mechanisms. The post-training regime — split into Expert Training (specialised models for reasoning, agent, and general chat) and Unified Training (integrating experts via self-distillation) — means the MTP layer must serve a model that has already been shaped by multi-domain specialisation. Similarly, a two-stage difficulty-based curriculum for reinforcement learning (moderate-difficulty problems followed by extremely-difficult ones) pushes the model past its performance ceiling in reasoning tasks; the throughput benefits of MTP-based decoding make such inference-heavy RL training more tractable.

Sources: GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models, DeepSeek-V3 Technical Report

---

## Limitations and Open Questions

Despite compelling benchmark results, several aspects of MTP remain underspecified in public reporting:

**Attribution of gains.** GLM-4.5's performance improvements arise from a confluence of factors — MoE architecture, multi-stage post-training, RL curriculum, and MTP. How much of the efficiency or quality gain is attributable specifically to MTP, versus the other components, is not disentangled in available evidence.

**Frontier reasoning headroom.** GLM-4.5 scores only 14.4% on Humanity's Last Exam, indicating substantial unresolved headroom in frontier scientific reasoning. Whether MTP's richer training signal helps or is neutral for this class of problem is unknown.

**Speculative decoding acceptance rates.** The practical inference speedup from speculative decoding is highly sensitive to how often the verifier accepts the drafter's proposals. This acceptance rate depends on domain, sequence length, and temperature — but no disaggregated data has been released.

**Safety and calibration effects.** GLM-4.5 scores 89.87 on SafetyBench, competitive but with measurable gaps in Unfairness and Bias (77.4%). Whether predicting multiple tokens ahead alters the model's tendency toward harmful completions — either by smoothing over refusal signals or by reinforcing them through longer-horizon planning — is an open question with no current evidence.

**Generalisability beyond MoE.** GLM-4.5 implements MTP as a specialised MoE layer. Whether MTP confers comparable benefits in dense architectures or alternative sparse designs is not established from the available sources.

---

## Connections

MTP sits at the intersection of several converging pressures in [[themes/model_architecture|model architecture]]: the push toward inference efficiency driven by [[themes/ai_market_dynamics|AI market dynamics]], the use of auxiliary objectives to improve [[themes/pretraining_and_scaling|pretraining signal]], and the demand from [[themes/software_engineering_agents|software engineering agents]] for sustained coherent generation over long horizons. Its role in speculative decoding links it to [[themes/adaptive_computation|adaptive computation]] — where the computational budget is allocated dynamically based on output difficulty. The technique's appearance in both DeepSeek-V3 and GLM-4.5 suggests it is consolidating as a standard component in the efficiency toolkit of [[themes/model_commoditization_and_open_source|open-source frontier models]].

## Key Findings

## Relationships

## Sources
