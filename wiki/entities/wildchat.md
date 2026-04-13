---
type: entity
title: WildChat
entity_type: dataset
theme_ids:
- ai_governance
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- finetuning_and_distillation
- hallucination_and_reliability
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00027352340269466626
staleness: 0.0
status: active
tags: []
---
# WildChat

WildChat is a large-scale dataset of natural, real-world conversations between users and AI assistants, crowdsourced from users worldwide. Its significance lies in its dual role: as a source of authentic instruction data for post-training pipelines, and as a naturalistic safety evaluation benchmark that reflects the messy, uncurated distribution of actual user requests — making it a more ecologically valid test bed than synthetically constructed datasets.

**Type:** dataset
**Themes:** [[themes/ai_governance|AI Governance]], [[themes/alignment_and_safety|Alignment & Safety]], [[themes/alignment_methods|Alignment Methods]], [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]]

---

## Overview

WildChat is a crowdsourced collection of real user–assistant interactions, distinguished from curated or synthetic instruction datasets by its organic, unfiltered character. The dataset skews heavily toward everyday use: roughly 75.5% of conversations cover daily assistance, advice, and analysis — the long tail of what people actually ask AI systems to do. This distributional realism makes it valuable both as a training signal and as a diagnostic lens.

In the context of Tulu 3, WildChat serves as the primary source of instructions for the Reinforcement Learning from Crowd Feedback (RLCF) stage, feeding a preference tuning pipeline built around on-policy data generation. The Tulu 3 recipe uses WildChat prompts to sample completions from Tulu 3-SFT and other models, then derives preference labels through pairwise comparisons — grounding the DPO stage in realistic user intent rather than curated demonstrations. This is notable given the broader opacity in the field: as of November 2024, no model in the top 50 of the LMSYS ChatBot Arena had released its post-training data, making WildChat-backed open recipes unusually transparent.

In the context of Deliberative Alignment, WildChat functions as a naturalistic safety benchmark. The key result is that o1 maintains a 98% safe completion rate on WildChat without external safety filters — a result attributed to deliberative alignment, where the model explicitly retrieves and applies relevant policy categories during chain-of-thought reasoning before generating a response. This stands in contrast to trained-reflex safety, which the paper argues degrades under distributional shift.

---

## Key Findings

WildChat's role across these sources illuminates a productive tension in post-training methodology. On one side, Tulu 3 treats it as instruction provenance — a way to anchor preference optimization in what real users want, complementing verifiable-reward RL (RLVR) which targets skills with objective correctness signals like mathematics. On the other side, Deliberative Alignment uses it as a probe for whether safety generalizes beyond red-teaming distributions: o1's 98% safe completion rate on WildChat, paired with a goodness@0.1 score of 0.88 on StrongREJECT, suggests that reasoning-mediated safety transfers better to naturalistic prompts than reward-model-based approaches.

The Deliberative Alignment results reveal a mechanistic detail worth flagging: the chain-of-thought is hidden from the reward model (GRM) during RL training, specifically to reduce optimization pressure on the CoT and thereby reduce the risk of encouraging deceptive reasoning chains. The policy retrieval accuracy numbers — 0.75 for hard refusals, 0.91 for safe completions, 0.54 for compliance — show that safety-trained models reference the correct policy category far more reliably than baselines (0.27, 0.21 across comparison conditions), and that this reasoning accuracy correlates with downstream safety behavior on WildChat.

---

## Limitations and Open Questions

WildChat's crowdsourced nature is simultaneously its strength and its weakness. Because it reflects actual user behavior, it captures realistic instruction distributions — but it also inherits whatever biases exist in the self-selected user population (language, geography, use case). How well WildChat represents the tail of adversarial or sensitive prompts compared to deliberate red-team datasets like StrongREJECT or XSTest remains an open question.

The 75.5% concentration in daily assistance/advice/analysis raises a coverage concern: WildChat may be underweighted in domains where safety and capability failures are most consequential (e.g., technical misuse, medical advice, politically sensitive content). A 98% safe completion rate on WildChat is a meaningful result, but it should be read alongside StrongREJECT and XSTest performance rather than in isolation.

There is also a methodological question about using WildChat simultaneously as training data (Tulu 3's RLCF stage) and as an evaluation surface: if models are trained on WildChat-derived preferences, their performance on WildChat as a benchmark is no longer a fully held-out measure. Tulu 3 and Deliberative Alignment use WildChat for different purposes and with different models, so contamination is not a direct concern across these specific papers — but it is a structural issue for the field as WildChat becomes more widely adopted.

---

## Relationships

WildChat is directly implicated in Tulu 3: Pushing Frontiers in Open Language Model Post-Training, where it anchors the instruction distribution for preference tuning, and in Deliberative Alignment: Reasoning Enables Safer Language Models, where it serves as a naturalistic safety evaluation surface. It connects to [[themes/post_training_methods|post-training methods]] through its role in DPO data generation, to [[themes/alignment_and_safety|alignment and safety]] through its use as a safety probe, and to [[themes/benchmark_design|benchmark design]] through the broader question of whether real-world conversation distributions are the right substrate for safety evaluation. The contrast between WildChat's organic coverage and red-team datasets like StrongREJECT is a recurring structural theme across both papers.

## Sources
