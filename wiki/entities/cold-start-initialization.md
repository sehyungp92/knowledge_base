---
type: entity
title: Cold-Start Initialization
entity_type: method
theme_ids:
- adaptive_computation
- chain_of_thought
- generative_media
- model_architecture
- multimodal_models
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- synthetic_data_generation
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0001340132806173129
staleness: 0.0
status: active
tags: []
---
# Cold-Start Initialization

> Cold-start initialization is a two-stage training strategy in which a base model is first fine-tuned with supervised learning on structured, grounded chain-of-thought data before reinforcement learning begins. By establishing a stable behavioral prior, it reduces reward sparsity during RL and prevents the model from needing to relearn basic formatting and reasoning skills under sparse reward signals — a technique that has proven especially important for multimodal and video reasoning systems.

**Type:** method
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/chain_of_thought|Chain of Thought]], [[themes/generative_media|Generative Media]], [[themes/model_architecture|Model Architecture]], [[themes/multimodal_models|Multimodal Models]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/video_and_world_models|Video and World Models]], [[themes/vision_language_models|Vision-Language Models]]

## Overview

Cold-start initialization addresses a fundamental instability in applying reinforcement learning to large language models: when reward signals are sparse or delayed, models trained from a raw base checkpoint struggle to establish coherent output formats and reasoning strategies before receiving meaningful gradient updates. The solution is to first supervise the model into a behavioral regime that already approximates the desired output structure, then apply RL to push past the ceiling that supervised data alone cannot reach.

The strategy is implemented by constructing a high-quality chain-of-thought dataset — often synthetic and constructed without human annotation — and fine-tuning the base model on it before any RL stage begins. In the Vision-R1 system, this cold-start dataset comprises 200K multimodal CoT samples with human-like cognitive processes, used to initialize the model before 10K multimodal math problems are used for RL training. The Open-o3 Video system applies the same principle to spatio-temporal video reasoning, combining SFT on the STGR dataset before training with a composite reward over accuracy, grounding quality, and format.

## Empirical Evidence for the Two-Stage Benefit

The ablation record from Vision-R1 is particularly clear. When RL is applied without cold-start initialization (Vision-R1-Zero), the model produces an average output length of 1285 tokens and achieves 50.7% accuracy on the MathVista benchmark. With cold-start initialization preceding RL, average output length rises to 2057 tokens and accuracy to 55.4% — a gap attributable not to more data or a stronger reward function, but purely to initialization quality. This suggests that the RL stage is doing qualitatively different work when it begins from a model that already generates coherent reasoning chains versus one that must simultaneously discover format and improve accuracy.

Cold-start data alone also carries substantial signal. The Vision-R1-CI variant, which uses only the cold-start SFT and no RL at all, improves a Llama-3.2-11B base from 48.6% to 62.7% on MathVista and from 8.4% to 27.1% on MathVerse. This indicates that much of the eventual performance gain is attributable to the quality of the CoT data rather than the RL stage itself — raising the question of where the marginal contribution of RL ends and the marginal contribution of better cold-start curation begins.

## Interaction with Reward Design

Cold-start initialization does not operate in isolation; its effectiveness is tightly coupled to the reward functions used in the subsequent RL stage. Vision-R1 uses a Hard Formatting Result Reward Function (HFRRF) that assigns reward=1 only when both format requirements and answer correctness are simultaneously satisfied, and reward=0 otherwise. This binary, joint reward would be nearly impossible to learn from a blank initialization — the joint satisfaction event would be extremely rare. Cold-start SFT ensures the model already satisfies format requirements with high probability, so the reward signal reduces to primarily accuracy, making the RL problem tractable.

Open-o3 Video's composite reward — combining an accuracy term, a thinking reward with temporal and spatial components, and a format reward — faces an analogous sparsity problem in the video domain. The thinking reward employs adaptive temporal proximity (large sigma early in training for dense signals, decreasing sigma later for stricter alignment) and temporal gating (spatial rewards only computed when temporal predictions are sufficiently close to ground truth), both of which are curriculum strategies that mirror the logic of cold-start at the reward level: begin with a signal that is achievable, then sharpen. That both approaches are used together in the same system suggests they are complementary rather than redundant.

## Connections to RL Stability

The theoretical motivation for cold-start connects to broader work on stabilizing RL with LLMs. Token-level policy gradient methods (e.g., GRPO) accumulate high-variance corrections across long sequences, and this variance is worst when the model is far from a coherent output distribution — exactly the regime of a raw base model at the start of RL. Open-o3 Video's adoption of GSPO, which operates at the sequence level rather than the token level to eliminate high-variance token-wise corrections, can be understood as addressing the same instability from the algorithmic side. Cold-start initialization addresses it from the data side. The two approaches converge on the same goal: reducing the effective exploration horizon the model must traverse before receiving a useful learning signal.

## Limitations and Open Questions

Several questions remain underexplored in the current evidence. First, the cold-start data quality ceiling: if the SFT dataset is itself limited — for instance, constructed by prompting a teacher model that already has systematic errors in a domain — cold-start initialization may entrench those errors rather than providing a neutral starting point for RL to correct. The Vision-R1 construction pipeline avoids human annotation but relies on automated filtering; the failure modes of that filtering are not characterized.

Second, the tradeoff between cold-start data scale and RL data scale is not well mapped. Vision-R1 uses 200K cold-start samples and 10K RL samples, but it is unclear whether reducing the cold-start set and expanding the RL set would reach the same endpoint or a different one. The optimal balance likely varies by domain difficulty and reward density.

Third, cold-start initialization as described assumes the cold-start data and RL reward are well-aligned — that the CoT format the SFT stage teaches is the same format that the reward function expects. Misalignment between SFT-induced behaviors and RL reward signals is a known failure mode in post-training, and it is not clear how much the method degrades when that alignment is imperfect.

Finally, all reported results come from systems that initialize from strong base models (Qwen2.5-VL, Llama-3.2) rather than weaker ones. It is an open question whether cold-start initialization is equally effective when the base model has weaker priors, or whether the technique fundamentally depends on a base that already has latent reasoning capacity to unlock.

## Sources

- Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models
- Open-o3 Video: Grounded Video Reasoning with Explicit Spatio-Temporal Evidence
- Stabilizing Reinforcement Learning with LLMs: Formulation and Practices

## Key Findings

## Relationships
