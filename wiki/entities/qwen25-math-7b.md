---
type: entity
title: Qwen2.5-Math-7B
entity_type: entity
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
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 7.040085176313672e-05
staleness: 0.0
status: active
tags: []
---
# Qwen2.5-Math-7B

> Qwen2.5-Math-7B is a 7-billion parameter math-specialized language model from Alibaba's Qwen family that has become a prominent experimental subject for post-training methods pushing small model capabilities toward frontier-level mathematical reasoning. Its baseline performance of 12.9 on AIME 2024 makes it a useful benchmark anchor — modest enough that improvements are dramatic and measurable, yet capable enough to serve as a meaningful base for advanced techniques.

**Type:** entity
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]]

## Overview

Qwen2.5-Math-7B sits at the intersection of two competing post-training philosophies: compute-intensive search-and-synthesis pipelines and lightweight reinforcement learning at test time. It has been used as the base model in both rStar-Math and TTRL, making it one of the most heavily studied substrates for understanding how much headroom small models actually have on hard mathematical tasks.

The model's baseline — 12.9 on AIME 2024, 58.8% on MATH — is deliberately framed as a floor in both papers, with results showing that the ceiling is far higher than the base suggests. Whether through MCTS-guided self-evolution or majority-vote reinforcement learning, the gains are large enough to challenge the assumption that scale is the primary lever for competition-level math.

## Key Findings

### rStar-Math: Scaling Up with Self-Evolved Deep Thinking

The rStar-Math system treats Qwen2.5-Math-7B as a policy model that co-evolves with a Process Preference Model (PPM) through four iterative rounds of MCTS-augmented data generation and fine-tuning. The results are striking: MATH benchmark performance rises from 58.8% to 90.0%, surpassing o1-preview by 4.5 percentage points, and the model solves an average of 8 out of 15 AIME 2024 problems (53.3%) — placing it in the top 20% of high school math competitors.

The mechanism is a tightly coupled feedback loop. MCTS generates step-by-step reasoning trajectories, terminal nodes are scored ±1 for correctness, and Q-values backpropagate through the tree to intermediate steps. Rather than using raw Q-values as direct reward labels (which risks label noise), rStar-Math constructs preference pairs and trains the PPM with a pairwise ranking loss. The PPM head is a scalar-value head with tanh activation clamping outputs to [−1, 1], initialized from the policy model itself — a design choice that keeps the two models architecturally coupled and reduces initialization overhead.

A key detail is the code-augmented chain-of-thought synthesis: trajectories are only retained when the accompanying Python code executes successfully, filtering out steps that contain correct-sounding but erroneous reasoning. This verification step is what gives the training data its quality edge over GPT-4 distillation baselines (NuminaMath-CoT, MetaMath) and simple rejection sampling. The four-round self-evolution eventually covers 90.25% of 747k training problems, with PPM-augmented MCTS in round 3 raising Olympiad-level coverage from 56.04% to 62.16%. By round 2, the system already surpasses GPT-4o on MATH (86.6% vs 76.6%).

Notably, a 7B PPM is sufficient to outperform Qwen's own Best-of-N baselines that rely on a 72B reward model — a 10× parameter advantage that the PPM approach erases through better step-level signal.

### TTRL: Reinforcement Learning Without Ground Truth Labels

TTRL takes a philosophically different route. Instead of building elaborate training pipelines, it applies reinforcement learning directly at test time using majority voting as a proxy label: given N candidate outputs, the most frequent answer is treated as the estimated ground truth, and any output matching it receives a positive reward signal.

Applied to Qwen2.5-Math-7B, this produces a 211% improvement on AIME 2024 alone (12.9 → 40.2), with an average gain of 76% across AIME 2024, AMC, MATH-500, and GPQA. The significance here is methodological: TTRL requires no curated labels, no teacher model, no reward model training — only the model's own output distribution and a consistency heuristic. This makes it deployable in settings where ground truth is unavailable, though the majority voting proxy is an imperfect signal that can reinforce confidently wrong answers when the model is systematically biased.

## Limitations and Open Questions

The rStar-Math gains depend heavily on infrastructure: MCTS at scale is compute-intensive, and the four-round self-evolution requires iterative training runs that are far from lightweight. The 90% problem coverage after four rounds still leaves a 10% gap concentrated on the hardest Olympiad problems — a gap that may be structurally resistant to further self-evolution without qualitative changes to the search or reward signal.

TTRL's majority voting proxy is an elegant approximation but not a principled one. On distribution shifts or highly ambiguous tasks, the majority may converge on wrong answers, and TTRL would reinforce that error. The 76% average gain also obscures variance: GPQA is a different domain from math olympiad problems, and it's unclear how far the method generalizes beyond tasks with verifiable, discrete answers.

A deeper open question is what these results reveal about the model's pre-training. Both methods extract large gains without architectural changes, suggesting that Qwen2.5-Math-7B's weights already encode substantial mathematical capability that standard inference fails to surface. Whether this is a property of the Qwen pre-training data, the math-specialization fine-tuning, or a more general phenomenon of 7B models is not yet disentangled.

## Relationships

Qwen2.5-Math-7B shares its base architecture lineage with Qwen2-Math-7B and Qwen2.5-Math-1.5B, both also used in rStar-Math experiments. It is closely related to **PPM** (Process Preference Model), which is initialized from and co-trained with the policy model. Its performance trajectory connects it to broader themes of [[themes/test_time_compute_scaling|test-time compute scaling]] (rStar-Math's MCTS) and [[themes/test_time_learning|test-time learning]] (TTRL's online RL), two approaches that are formally distinct but both challenge the assumption that inference-time behavior is fixed by training. The AIME 2024 benchmark serves as a shared evaluation anchor connecting it to other frontier math reasoning efforts, including OpenAI o1, which both papers use as a comparison point.

## Sources
