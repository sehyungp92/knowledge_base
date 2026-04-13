---
type: entity
title: Game of 24
entity_type: dataset
theme_ids:
- agent_memory_systems
- agent_systems
- chain_of_thought
- knowledge_and_memory
- mathematical_and_formal_reasoning
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- search_and_tree_reasoning
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00028695863162174083
staleness: 0.0
status: active
tags: []
---
# Game of 24

The Game of 24 is a classic combinatorial arithmetic puzzle in which a solver must combine four given numbers using basic arithmetic operations (+, −, ×, ÷) to produce exactly 24. Despite its apparent simplicity, it has become a meaningful stress-test for AI reasoning systems because it demands precise multi-step planning, search over operation orderings, and the ability to discover and reuse solution strategies — making it a recurring benchmark across research on tree search, test-time learning, and agentic optimization.

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

The Game of 24 occupies an interesting position in the AI benchmark landscape: it is tractable enough to be solved programmatically, yet hard enough that vanilla LLM inference fails badly. Its value as a benchmark lies precisely in this gap. A model that cannot reason structurally about search spaces will plateau well below human-level performance, while a model equipped with the right strategy — particularly a Python-based computational solution — can reach near-perfect accuracy. This property makes it an unusually clean signal for evaluating whether a system is genuinely learning and retaining useful problem-solving strategies, rather than pattern-matching on surface form.

## Key Findings

### Test-Time Learning Can Close the Gap Dramatically

The most striking result associated with the Game of 24 comes from Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory. GPT-4o's baseline success rate on the puzzle sits at roughly 10% — a figure consistent with the known fragility of direct LLM arithmetic reasoning. After the Dynamic Cheatsheet mechanism allowed the model to discover and persist a Python-based solution strategy across problem instances, accuracy jumped to 99%. This is not a marginal improvement; it is a near-complete transformation of capability through memory alone. Critically, Dynamic Cheatsheet achieves this without modifying model parameters and is compatible with black-box LLM APIs — meaning the gains are attributable entirely to structured test-time adaptation rather than any form of fine-tuning.

This result generalises beyond the Game of 24 itself. On AIME 2024, GPT-4o improved from 20% to 40% under DC-RS (the robust variant), while full-history appending actually *degraded* performance to 13.3% — a cautionary result showing that naive memory accumulation can hurt rather than help. Claude 3.5 Sonnet showed similarly large gains across AIME 2020–2024 (6.7% → 40.6%) and GPQA-Diamond (59.6% → 68.7%), and more than doubled its AIME 2024 score (23% → 50%) under DC-Cu. The Game of 24 acts as the clearest demonstration of the underlying mechanism: when the right strategy exists and can be written down, the model only needs to find it once.

### Tree Search as a Structural Alternative

Before test-time memory approaches, structured tree search offered another route to improving performance on compositional reasoning tasks. Language Agent Tree Search (LATS) applies Monte Carlo Tree Search to language model reasoning, using UCT (Upper Confidence bounds applied to Trees) to balance exploration and exploitation. The value function combines a self-generated LM score with a self-consistency score, weighted by a tunable hyperparameter λ. On coding benchmarks, LATS achieves 83.8% pass@1 on HumanEval with GPT-3.5 (versus 68.1% for Reflexion and 54.4% for ToT), 81.1% on MBPP, and 92.7% with GPT-4 — state-of-the-art at time of publication. On WebShop, it raises average score by 22.1 points over ReAct with GPT-3.5.

While the Game of 24 is not LATS's primary evaluation target, LATS represents the class of approaches that address the same structural problem: how to navigate a combinatorial search space that exceeds what greedy inference can handle. Tree search does this through explicit rollout and backpropagation; Dynamic Cheatsheet does it through strategy memoisation. Both reflect the view that the Game of 24's difficulty is fundamentally about search, not knowledge.

### Agentic Optimization Framing

AGENTFLOW treats the Game of 24 as part of a broader mathematical reasoning evaluation suite, where it achieves average accuracy gains of 14.5% on mathematical reasoning tasks over top-performing baselines using a 7B-scale backbone. AGENTFLOW's Flow-GRPO mechanism converts multi-turn RL into tractable single-turn policy updates by broadcasting a single verifiable final-outcome reward across every turn in a trajectory — a design motivated precisely by the difficulty of assigning credit in multi-step reasoning chains like those required by arithmetic puzzles.

## Limitations and Open Questions

The Game of 24 results raise a question about the nature of the capability being measured. The near-perfect performance of Dynamic Cheatsheet (10% → 99%) suggests that, for this puzzle, *strategy discovery* is the bottleneck — once a Python solver is in the cheatsheet, the puzzle is essentially reduced to code execution. This is a useful capability, but it may not generalise to domains where no single strategy dominates, or where the space of useful strategies is large and context-dependent. The AIME results are more informative in this respect, since no single program solves all problems, and the gains are correspondingly more modest.

The degradation observed with full-history appending (GPT-4o: 20% → 13.3% on AIME 2024) also signals a real limitation: unstructured memory accumulation can introduce noise that overwhelms useful signal. The Game of 24, being simple enough to yield a single reusable strategy, may actually *understate* this problem for harder benchmarks.

## Relationships

The Game of 24 is closely linked to the broader [[themes/test_time_learning|test-time learning]] research programme, where it serves as a canonical demonstration case alongside AIME and GPQA. It connects to [[themes/search_and_tree_reasoning|tree search]] approaches through LATS's treatment of compositional reasoning as a search problem. Its appearance in AGENTFLOW's evaluation suite ties it to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] and [[themes/policy_optimization|policy optimization]] research, particularly work on assigning credit across multi-step agentic trajectories. As a benchmark, it is notable for having an unusually clean success condition (exactly 24, no approximation), which makes it attractive for verifiable reward signals in RL training pipelines.

## Sources
