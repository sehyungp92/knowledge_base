---
type: entity
title: Rejection Sampling
entity_type: method
theme_ids:
- alignment_and_safety
- chain_of_thought
- finetuning_and_distillation
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00046266919908421556
staleness: 0.0
status: active
tags: []
---
```markdown
# Rejection Sampling

> Rejection sampling is a data quality technique central to post-training pipelines for LLMs, where candidate reasoning trajectories or outputs are generated en masse and filtered by outcome correctness — keeping only those that satisfy ground truth labels or rule-based rewards. Its simplicity makes it a foundational baseline for synthetic data generation, but evidence increasingly shows it is outpaced by process-level verification methods that evaluate intermediate reasoning steps rather than just final answers.

**Type:** method
**Themes:** [[themes/alignment_and_safety|Alignment & Safety]], [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/search_and_tree_reasoning|Search & Tree Reasoning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Overview

Rejection sampling, in the context of LLM post-training, refers to the practice of generating multiple candidate outputs from a policy model and retaining only those judged correct by some external verifier — typically ground truth answer matching for math, or a trained reward model for more open-ended domains. The retained outputs form a high-quality SFT dataset, allowing iterative self-improvement without requiring online RL.

The method is attractive precisely because of its simplicity: no critic model, no value estimation, no rollout infrastructure. A single pass through a generator and a binary filter is enough to build a training corpus. This has made rejection sampling a default component in pipelines like DeepSeek-R1, where a dedicated rejection sampling fine-tuning (RS-FT) stage precedes RL training — the model first learns from its own correct rollouts before being shaped by reward signal. The O1 Replication Journey Part 2 similarly used distillation combined with rejection-filtered traces as a surprisingly powerful baseline, raising questions about how much of apparent RL gains are actually attributable to data selection rather than policy gradient update mechanics.

The core limitation is structural: rejection sampling is an outcome filter. It can tell you whether a trajectory ended correctly but says nothing about the quality of the path taken to get there. A model can stumble into a correct answer through flawed intermediate steps, and rejection sampling will preserve that trajectory alongside genuinely sound ones — diluting the quality signal in the training data.

---

## The Outcome vs. Process Gap

The most direct evidence for this limitation comes from rStar-Math, which frames rejection sampling as its primary SFT baseline and systematically demonstrates that step-by-step verified trajectories generated via MCTS substantially outperform it. The mechanism is concrete: rStar-Math's Monte Carlo Tree Search evaluates each reasoning step independently, scoring terminal nodes as +1 (correct) or −1 (incorrect) and backpropagating Q-values through intermediate steps. A Process Preference Model (PPM) trained on these preference pairs then provides dense, step-level reward signal — a fundamentally different information structure than the binary outcome signal rejection sampling uses.

The result is not marginal. Fine-tuning on MCTS-verified trajectories significantly outperforms fine-tuning on rejection-sampled data across all benchmarks tested. On MATH, rStar-Math improves Qwen2.5-Math-7B from 58.8% to 90.0%, surpassing o1-preview by 4.5% — a gap attributable in part to the richer supervision signal the process-level method provides. Critically, the PPM-augmented MCTS approach with a 7B reward model also outperforms naive Best-of-N rejection sampling that uses a 10× larger 72B reward model, suggesting the architectural difference — process-level vs. outcome-level — matters more than scale.

The rStar-Math pipeline does incorporate a form of rejection sampling at a finer granularity: its code-augmented CoT synthesis retains only steps where the generated Python code executes successfully, filtering erroneous intermediate steps. This is closer in spirit to process-level filtering than classical trajectory-level rejection sampling, and it illustrates how the distinction between outcome and process filtering is not binary but a spectrum.

---

## Role in Broader Post-Training Pipelines

Rejection sampling occupies a specific ecological niche in the post-training stack. It is most valuable at the beginning of iterative self-improvement cycles, when a model lacks a reliable reward model and RL infrastructure is unavailable or premature. Generating many rollouts and filtering by correctness bootstraps a curriculum without requiring anything beyond a verifiable task signal.

In DeepSeek-R1's multi-stage pipeline, rejection sampling fine-tuning serves as a bridge between cold-start SFT (on human-curated long-CoT data) and full RL training. The RS-FT stage stabilises the policy before RL is applied, reducing variance and improving sample efficiency in the subsequent RL phase. This positioning — rejection sampling as warm-up, RL as refinement — has become a recurring structural pattern in math reasoning pipelines.

At test time, rejection sampling manifests as Best-of-N inference: generating N candidate solutions and selecting the best by reward model score or majority vote. s1 treats this as a baseline for test-time compute scaling, finding that budget forcing — forcing the model to think longer before outputting an answer — achieves better scaling behaviour and provides 100% controllability over compute expenditure, outperforming sampling-based selection on AIME24. The implication is that test-time rejection sampling is bottlenecked by diversity: N independent samples from the same policy eventually saturate in quality, while extended thinking accesses a qualitatively different compute regime.

---

## Capabilities

- Scalable synthetic data generation for SFT without online RL infrastructure: generate rollouts, filter by correctness, iterate across self-evolution rounds (as demonstrated in rStar-Math's four-round self-improvement loop covering 90.25% of 747k math problems by round 4) (maturity: established)
- Best-of-N test-time inference: sample N completions, rank by outcome-level reward or majority vote (maturity: established)
- Bootstrap stage in multi-phase post-training: stabilises policy before RL, as used in DeepSeek-R1's RS-FT stage (maturity: established)

---

## Limitations & Open Questions

The central open question is the **process supervision gap**: outcome-level rejection sampling demonstrably produces weaker training signal than step-level process verification for complex multi-step reasoning. The rStar-Math evidence is clear, but the cost difference is also substantial — MCTS-based process verification requires significantly more compute per trajectory. At what dataset scale or task complexity does the quality improvement justify the compute overhead? This remains unresolved.

A subtler issue is **correct-but-wrong-reason contamination**: models that learn from outcome-filtered data may develop brittle heuristics that generalise poorly when the answer format changes, even if benchmark accuracy looks strong. Rejection sampling cannot distinguish a trajectory that is correct for the right reasons from one that is correct by shortcut.

Finally, **diversity saturation** in Best-of-N settings — where additional samples yield diminishing returns — suggests that the method is inherently limited as a test-time scaling strategy compared to search-based or extended-thinking approaches.

---

## Relationships

Rejection sampling is closely related to Process Reward Models — the move from outcome to process supervision directly addresses rejection sampling's core limitation. It is a component of [[entities/self-play|Self-Play]] and iterative self-improvement loops, where it bootstraps early rounds before stronger supervision is available. It contrasts with Monte Carlo Tree Search-based data generation, which provides the process-level signal rejection sampling lacks. In the test-time compute domain, it competes with Best-of-N Search, Beam Search, and budget forcing as strategies for allocating additional inference compute.

Sources: rStar-Math, DeepSeek-R1, s1, O1 Replication Journey Part 2
```

## Key Findings

## Limitations and Open Questions

## Sources
