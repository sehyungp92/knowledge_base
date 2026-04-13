---
type: entity
title: MATH Dataset
entity_type: dataset
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0010131250490655944
staleness: 0.0
status: active
tags: []
---
# MATH Dataset

The MATH Dataset is a benchmark of 500 high-school competition mathematics problems that has become a central evaluation standard for LLM mathematical reasoning. Its significance lies not merely in measuring raw accuracy, but in serving as a proving ground for the core training and inference techniques that have come to define modern reasoning systems — reinforcement learning from verifiable rewards, chain-of-thought supervision, test-time compute scaling, and self-correction. Where early models scored near zero on competition-level mathematics, MATH now functions as a gateway benchmark: a model must convincingly clear it before stronger evaluations (AIME, USAMO, IMO) are even considered meaningful.

**Type:** dataset
**Themes:** [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scaling_laws|Scaling Laws]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Overview

MATH consists of competition-style problems drawn from AMC, AIME, and other high-school olympiad tracks, covering seven subject areas (algebra, geometry, number theory, counting, probability, intermediate algebra, precalculus) at five difficulty levels. Problems are formatted with structured solution steps, making them tractable for supervised fine-tuning and reward modeling alike. Its difficulty profile — hard enough to differentiate models, not so hard as to be noise — makes it the canonical benchmark for the mathematical reasoning research cycle.

## Role in the Research Landscape

### As a Training Target

MATH's verifiable answer format makes it ideal for reinforcement learning from outcome rewards: a model either reaches the correct final answer or it doesn't, and this binary signal can be computed automatically without a learned reward model. This property has made it the primary training corpus for [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] approaches. INTUITOR, for instance, replaces even this external reward with self-certainty scores computed within GRPO's advantage function, demonstrating that MATH-style problems can sustain RL training loops with no supervision signal at all beyond self-consistency — a shift toward fully unsupervised reinforcement learning for mathematical reasoning (from Learning to Reason without External Rewards).

[[themes/post_training_methods|Post-training methods]] that leverage MATH go beyond simple outcome supervision. SCoRe, trained via reinforcement learning to self-correct, achieves a 15.6% absolute improvement in self-correction performance on MATH relative to the Gemini 1.5 Flash base model, with overall accuracy at second attempt (Accuracy@t2) rising by 23.0% (from Training Language Models to Self-Correct via Reinforcement Learning). This result is notable because it demonstrates that the capacity for self-correction is not inherent to instruction-tuned models — it must be explicitly cultivated, and MATH provides the structured signal to do so.

Credit assignment within these RL loops remains a key challenge. VinePPO targets this directly, refining how advantage estimates propagate across multi-step reasoning chains on MATH — recognizing that a wrong final answer may contain a largely correct reasoning trajectory that naive outcome rewards will discount entirely (from VinePPO: Refining Credit Assignment in RL Training of LLMs).

### As a Ceiling Benchmark — and Its Replacement

MATH now sits below the ceiling of frontier models. Work on [[themes/test_time_compute_scaling|test-time compute scaling]] uses MATH to study how inference-time search, majority voting, and best-of-N selection interact with model capability — but the benchmark's relevance to the leading edge is shrinking. Scaling Test-Time Compute treats MATH primarily as a calibration surface: a place to validate techniques before applying them at harder problem distributions where models still fail meaningfully.

The shift toward IMO-level evaluation is explicit in recent literature. Leading LLMs now score at or above human competition levels on most MATH problems, but their baseline accuracies on IMO 2025 problems — 31.6% (Gemini 2.5 Pro), 21.4% (Grok-4), 38.1% (GPT-5) using best-of-32 selection — reveal the gap that remains at the frontier (from Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline). MATH problems can be solved by a model with a modest reasoning budget; a typical IMO problem exhausts Gemini 2.5 Pro's 32,768-token thinking budget without resolution.

## Limitations and Open Questions

The core limitation of MATH as an evaluation surface is its solvability by current models — it can no longer distinguish the strongest systems from each other. High scores on MATH do not transfer cleanly to harder problem classes. Models that achieve near-perfect MATH accuracy still commit logical fallacies on Olympiad-level proofs, relying on superficial pattern-matching and heuristics rather than the step-by-step deductive reasoning that competition mathematics demands (from Winning Gold at IMO 2025). This gap between benchmark performance and genuine mathematical competence is MATH's most important limitation: it measures something real, but the ceiling is already in sight.

A second open question concerns what MATH-trained models actually learn. The benchmark's competition-problem format rewards correct final answers, but the solution paths that RL-trained models develop are not guaranteed to be valid mathematical arguments. VinePPO's focus on credit assignment is motivated precisely by this concern — if an incorrect final answer can arise from a mostly-correct reasoning chain, then outcome-only supervision on MATH may systematically degrade the quality of intermediate steps even as it improves aggregate accuracy. Whether MATH training instills genuine reasoning or sophisticated pattern completion remains unresolved.

A further limitation is the benchmark's coverage: combinatorial reasoning problems of the type that appear in IMO Problem 6 — the one that consistently defeated all three frontier models in the 2025 pipeline — are underrepresented in MATH's difficulty profile. MATH thus provides little signal about the specific reasoning failure modes that remain at the frontier.

## Relationships

MATH sits at the intersection of [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] and [[themes/mathematical_and_formal_reasoning|mathematical & formal reasoning]], functioning as the shared training and evaluation surface across both. It is closely related to harder successors — AIME, USAMO, IMO — which pick up where MATH's difficulty ceiling leaves off. The benchmark connects to [[themes/reward_modeling|reward modeling]] through its verifiable answer structure, to [[themes/test_time_compute_scaling|test-time compute scaling]] through best-of-N and search evaluations, and to [[themes/chain_of_thought|chain of thought]] through the solution-step supervision it enables.

## Key Findings

## Sources
