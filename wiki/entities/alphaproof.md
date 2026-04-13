---
type: entity
title: AlphaProof
entity_type: entity
theme_ids:
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- compute_and_hardware
- evaluation_and_benchmarks
- frontier_lab_competition
- mathematical_and_formal_reasoning
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- scientific_and_medical_ai
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.0018278105378370065
staleness: 0.0
status: active
tags: []
---
# AlphaProof

> AlphaProof is Google DeepMind's system for formal mathematical theorem proving, notable for achieving silver medal performance at the International Mathematics Olympiad (IMO) through reinforcement learning over a formal proof environment. It represents a landmark result in AI mathematical reasoning, generating roughly 100 million proofs during training and demonstrating that RL-driven interaction with a formal verifier can push machine reasoning to the level of elite human competitors.

**Type:** entity
**Themes:** [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/scaling_laws|Scaling Laws]], [[themes/compute_and_hardware|Compute and Hardware]], [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/alignment_methods|Alignment Methods]], [[themes/reward_modeling|Reward Modeling]], [[themes/agent_systems|Agent Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/ai_governance|AI Governance]]

## Overview

AlphaProof operates in the domain of *formal* mathematical reasoning: rather than producing natural-language arguments that could contain hidden errors, it generates proofs in Lean, a proof assistant whose verifier either accepts or rejects a proof with complete certainty. This formalism is both AlphaProof's greatest strength and its most significant constraint. The guaranteed-correct output has no analogue in informal AI math systems, but formal proofs are largely unreadable by working mathematicians and require all problems to be translated into Lean first, a laborious bottleneck that limits real-world deployment.

The system's core training loop is reinforcement learning over the formal environment. By interacting with a Lean verifier at massive scale (generating on the order of 100 million proof attempts), AlphaProof develops strategies that go well beyond pattern-matching, ultimately achieving performance in the silver-medal tier at IMO. This placed it alongside AlphaGeometry 2, DeepMind's companion system for Euclidean geometry, in a combined result that cleared four of six IMO 2025 problems.

## What AlphaProof Reveals About the State of AI Math Reasoning

AlphaProof's results are best understood in contrast to what informal LLM-based pipelines can and cannot do. Contemporary evaluation on IMO 2025 shows that the strongest base models (Gemini 2.5 Pro, Grok-4, GPT-5), when prompted directly, achieved baseline accuracies of only 31.6%, 21.4%, and 38.1% respectively using best-of-32 sampling. A verification-and-refinement pipeline built around the same models raised all three to roughly 85.7% accuracy (5 of 6 problems), as shown in Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline. The implication is stark: *raw model capability is not the limiting factor*. The path from latent mathematical reasoning to rigorous, verified proof requires architectural choices about iteration, verification, and compute allocation at inference time, not just a stronger base model.

This surfaces a deeper tension. Informal pipelines close much of the gap between raw and verified performance by using one LLM to both generate and verify, but this single-model paradigm is a known limitation: a model with consistent blind spots will produce systematically invalid verifications alongside systematically invalid proofs. AlphaProof sidesteps this by outsourcing verification to a sound external oracle (Lean), but at the cost of expressiveness and accessibility.

The persistent failure of all systems (including AlphaProof-style pipelines) on IMO 2025 Problem 6 deserves particular attention. The problem involves complex combinatorial reasoning, and no pipeline built on Gemini 2.5 Pro, Grok-4, or GPT-5 solved it. This is not a scaling artifact; it reflects a structural gap in how current models handle certain combinatorial search problems, pointing to an open bottleneck at the intersection of [[themes/search_and_tree_reasoning|search and tree reasoning]] and [[themes/mathematical_and_formal_reasoning|formal reasoning]].

## Compute and Inference Constraints

One underappreciated constraint surfaced by work around AlphaProof-adjacent systems is the raw insufficiency of current inference budgets for hard reasoning. Gemini 2.5 Pro's maximum thinking budget of 32,768 tokens is demonstrably not enough to solve a typical IMO problem in a single pass, which is why iterative refinement pipelines produce such large gains: they effectively extend the computation available per problem across multiple calls. This is a concrete instance of [[themes/test_time_compute_scaling|test-time compute scaling]] in action, where the bottleneck is not model quality but per-problem compute allocation.

AlphaProof's training-time compute profile is even more extreme. Generating 100 million proofs implies a training investment that few actors can replicate, placing the system squarely in the [[themes/compute_and_hardware|compute-intensive]] regime and raising questions about how its results generalize beyond the specific formal proving setup.

## Significance and Open Questions

The IMO benchmark has unusual external validity among AI math benchmarks. Of the 34 Fields medalists awarded since 1990, 11 were prior IMO gold medalists, including Terence Tao, Maryam Mirzakhani, and Grigori Perelman; an IMO gold medalist is roughly 50 times more likely to win a Fields Medal than a typical mathematician. This gives AlphaProof's performance a claim to significance that saturated benchmarks like MATH or MMLU cannot make.

Concurrent systems are closing in from different directions. Seed-Prover proves 121 of 155 past IMO problems (78.1% overall) entirely within a broad formal reasoning framework, and Seed-Geometry outperforms AlphaGeometry 2 on IMO-AG-50 (43 vs. 42 problems). These results suggest the formal theorem proving frontier is becoming genuinely competitive, with multiple organizations now capable of IMO-caliber performance.

The central open questions are: whether the formal-proof requirement can be relaxed without sacrificing verifiability; whether the combinatorial reasoning gap identified on Problem 6 reflects a fundamental limitation or a solvable engineering problem; and whether the training compute required for AlphaProof-level RL over formal systems can be made tractable enough to extend beyond mathematical olympiad domains into broader scientific reasoning.

## Relationships

AlphaProof was developed by Google DeepMind alongside AlphaGeometry 2, and both systems contributed to the combined IMO 2025 performance. It is architecturally downstream of [[themes/reinforcement_learning|RL]] advances and the broader [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] paradigm. Its benchmark significance connects to ongoing debates in [[themes/evaluation_and_benchmarks|evaluation and benchmarks]] about what constitutes meaningful AI capability measurement. The verification-and-refinement pipelines that followed (as documented in Winning Gold at IMO 2025) represent a complementary informal approach that achieves comparable IMO performance without formal proof generation, raising the question of whether AlphaProof's formalism constraint is a feature or a limitation going forward.

## Key Findings

## Limitations and Open Questions

## Sources
