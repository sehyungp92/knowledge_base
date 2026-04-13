---
type: entity
title: Entropy Collapse
entity_type: theory
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.00010214484356539525
staleness: 0.0
status: active
tags: []
---
# Entropy Collapse

Entropy collapse is a failure mode in reinforcement learning training of language models where the policy's token-level entropy decreases rapidly toward zero, causing sampled rollouts to become near-identical and exploration to effectively cease. Identified as a critical pathology in naive PPO and GRPO implementations, it represents one of the key structural reasons why RL training for reasoning can stall or regress — and has motivated a wave of mitigation strategies that have become central to post-training methodology.

**Type:** theory
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

When a policy collapses in entropy, it loses the diversity of outputs necessary for RL to function: without varied rollouts, the advantage signal becomes degenerate, gradient updates shrink toward zero, and the model effectively stops learning. This is not merely a theoretical concern — ablation experiments show that removing the `clip-higher` technique causes entropy to collapse to 0.03, versus 0.34 for a baseline RL run and 0.17 for entropy-based advantage shaping (from Reasoning with Exploration: An Entropy Perspective). The collapse is fast and severe enough to functionally halt training.

The significance of this failure mode is sharpened by a counterintuitive finding from Reinforcement learning with random rewards actually works with Qwen 2.5: when reward is *never* assigned in GRPO, the policy gradient is exactly zero and no learning occurs at all — a kind of entropy collapse induced not by over-optimization but by reward absence. Yet the same paper demonstrates that nearly any reward signal, no matter how semantically vacuous, can drive substantial MATH-500 improvements in Qwen 2.5 Math 7B: format rewards (+19.8), majority vote rewards (+23.2), even rewarding only incorrect answers (+21.2) and purely random rewards (+15.8). These results suggest that much of what RL training accomplishes may be less about reward semantics and more about maintaining gradient flow — keeping entropy alive long enough for the policy to reorganize latent structure it already possessed.

## Key Findings

The primary technical response to entropy collapse examined in the literature is **entropy-based advantage shaping**, introduced in Reasoning with Exploration: An Entropy Perspective. The method adds a clipped, gradient-detached entropy term $H^{\text{detach}}_t$ to the advantage function. The detachment is architecturally important: because the entropy term is removed from the computation graph during backpropagation, it adjusts the *magnitude* of updates without introducing any additional entropy gradient component. This makes it fundamentally orthogonal to entropy regularization — it does not add a new optimization objective, only rescales the existing one. The clipping further ensures the entropy term cannot dominate or reverse the sign of the original advantage, preserving the original optimization direction.

The practical payoff is meaningful. On AIME 2025 — a benchmark released after the training data cutoff of the base models, limiting overfitting concerns — entropy-based advantage with PPO achieves Pass@256 of 56.7%, versus 43.3% for the PPO baseline and 50.0% for the base model itself. This last comparison is particularly notable: vanilla PPO *underperforms* the base model on this hardest benchmark, while entropy shaping breaks through the ceiling. The method requires a single line of code added to existing RLVR pipelines, lowering the barrier to adoption substantially.

Prolonged RL work (e.g., ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models) provides complementary context: training Nemotron-Research-Reasoning-Qwen-1.5B on 136K diverse verifiable problems across math, code, STEM, logic puzzles, and instruction following required approximately 16K GPU hours on 32× H100-80GB GPUs. At this training scale and duration, entropy management becomes a sustained engineering challenge rather than a single intervention.

## Limitations and Open Questions

The random rewards result poses a fundamental interpretive challenge. If rewarding incorrect answers (+21.2) nearly matches ground-truth RLVR (+24.6), it is unclear how much credit reward signal deserves versus structural effects — entropy maintenance, output formatting regularization, or activation of latent capabilities through continued gradient flow. The literature does not yet resolve whether entropy collapse mitigation methods are surfacing genuinely new reasoning behaviors or simply preventing self-sabotage of existing ones.

Entropy-based advantage shaping has been validated primarily on mathematical benchmarks with verifiable rewards. Its behavior in open-ended domains, where reward signals are noisier and the relationship between entropy and exploration is less direct, remains an open question. The interaction with reward hacking — where maintained entropy might increase the surface area for policy exploitation of reward model flaws — is also underexplored.

The `clip-higher` ablation result (entropy 0.03 without it) suggests that entropy collapse sensitivity varies significantly with implementation details, but systematic characterization of which training configurations are most vulnerable is lacking. Similarly, the relationship between entropy collapse and the composition of skills during RL (see From $f(x)$ and $g(x)$ to $f(g(x))$: LLMs Learn New Skills in RL by Composing Old Ones) — where models appear to recombine existing capabilities — implies that diversity in the rollout distribution may matter not just for gradient health but for the *topology* of what can be discovered.

## Relationships

Entropy collapse is mechanistically related to **advantage degeneracy** in GRPO: when all rollouts are identical, group-relative advantages collapse to zero and training halts. It connects upstream to **reward signal quality** — as the random rewards experiments demonstrate, even malformed reward signals can prevent collapse — and downstream to **test-time compute scaling**, since a collapsed policy cannot benefit from pass@k or majority voting strategies that depend on output diversity. The failure mode is also relevant to **distillation and fine-tuning** pipelines that initialize from strong base models and risk rapid entropy loss when the reward landscape is narrow or the KL penalty is weak.

## Sources
