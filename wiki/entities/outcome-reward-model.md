---
type: entity
title: Outcome Reward Model
entity_type: method
theme_ids:
- agent_systems
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
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.0021700110985186094
staleness: 0.0
status: active
tags: []
---
# Outcome Reward Model

An Outcome Reward Model (ORM) is a reward signal that evaluates an entire reasoning chain by inspecting only the final answer: correct answer yields a positive signal, incorrect answer yields none. Its simplicity makes it cheap to train and deploy, but it is structurally blind to the quality of intermediate steps, which limits its effectiveness precisely where it matters most, on complex multi-step reasoning tasks. The contrast between ORM and its step-level counterpart, the Process Reward Model (PRM), has become a central empirical question in [[themes/post_training_methods|post-training methods]] and [[themes/rl_for_llm_reasoning|RL for LLM reasoning]].

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

An ORM assigns a single scalar confidence to a completed solution sequence based on whether the final answer is correct. Training requires only answer-level labels, which are cheap to obtain automatically from ground-truth datasets. The tradeoff is that the model receives no information about which reasoning steps contributed to or detracted from the correct answer. Every step in a correct solution is implicitly rewarded equally, and every step in an incorrect solution is equally punished, regardless of how far along the chain the error occurred.

This design choice has measurable consequences. Evidence from Math-Shepherd shows that vanilla PPO with ORM does improve model accuracy over the baseline, but consistently underperforms step-by-step PPO supervised by a PRM. The gap widens on harder benchmarks: PRM achieves a substantially larger advantage over ORM on MATH than on the simpler GSM8K, and the authors attribute this directly to the greater number of reasoning steps required by harder problems. With more steps, the ORM's inability to localize errors becomes increasingly costly.

## Empirical Position Relative to PRM

The comparative picture from Math-Shepherd is consistent across evaluation conditions. MATH-SHEPHERD as a verifier outperforms both self-consistency and ORM across all generator models tested on both datasets. PRM also exhibits superior data efficiency: it outperforms ORM by roughly 4% accuracy at as few as 10k training instances, suggesting a higher performance ceiling even before scale advantages appear.

The Hard Estimation (HE) and Soft Estimation (SE) labeling schemes illuminate why ORM-style thinking can fail. HE labels a step as correct if any one of N completion paths reaches the right answer; SE uses the frequency of correct completions. As N increases, SE progressively aligns with human-annotated distributions, while HE does not exhibit similar convergence. ORM is closer in spirit to HE: it treats correctness as binary and provides no probability-weighted signal about path quality. This distributional mismatch likely explains why ORM-trained verifiers are less reliable at test time.

One size asymmetry compounds ORM's limitations further. Experiments show that using a larger reward model to validate a smaller generator substantially boosts performance, but the reverse, a smaller reward model validating a larger generator, actively degrades it. Because ORM provides only terminal feedback, a mismatched or weaker ORM can silently approve reasoning chains that a step-aware model would have flagged earlier.

## Role in the Broader RL Pipeline

Despite its limitations relative to PRM, ORM is not obsolete. The Math-Shepherd results confirm that RL with ORM does meaningfully improve accuracy: step-by-step PPO with MATH-SHEPHERD pushes Mistral-7B from 77.9% to 84.1% on GSM8K and from 28.6% to 33.0% on MATH, and pairing a PRM verifier on top of that RL-trained model pushes further to 89.1% and 43.5% respectively. The key finding is that RL training and verification are complementary rather than redundant, and ORM-supervised RL still contributes to that compound gain even when PRM handles the verification pass.

ORM is also implicitly present across many systems documented in this library, including DeepSeek-R1, s1, and Scaling LLM Test-Time Compute, where outcome-based reward signals (rule-based correctness checks, answer matching) drive policy optimization. In those frameworks, ORM corresponds to the simplest and most scalable supervision signal available, one that requires no step annotation infrastructure at all.

## Limitations and Open Questions

The fundamental limitation of ORM is architectural: without step-level supervision, it cannot distinguish a lucky correct answer from a sound reasoning chain, or a near-miss incorrect answer from a catastrophically wrong one. This makes it a poor signal for [[themes/search_and_tree_reasoning|search and tree reasoning]] methods where intermediate node quality determines whether a branch is worth expanding.

The cost of constructing PRM training data via automated completion (as in Math-Shepherd's MCTS-inspired approach) is non-trivial in compute, though still far below human annotation. As that cost decreases with better infrastructure, the practical case for ORM as a substitute weakens. The remaining open question is whether there are task regimes, perhaps very short chains or highly constrained domains, where ORM's simplicity is sufficient and the step-level overhead is genuinely unnecessary. Current evidence suggests this threshold is lower than initially assumed.

## Key Findings

## Relationships

## Sources
