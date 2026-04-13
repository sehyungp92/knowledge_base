---
type: entity
title: Thinking Mode
entity_type: method
theme_ids:
- adaptive_computation
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012756447994697077
staleness: 0.0
status: active
tags: []
---
```markdown
# Thinking Mode

Thinking mode is an LLM inference paradigm in which a model emits explicit chain-of-thought reasoning traces — typically enclosed in `<think>` tags — before producing a final answer, trading additional token generation for improved accuracy on complex tasks. It sits at the intersection of test-time compute scaling and chain-of-thought prompting: the extended reasoning budget is consumed at inference rather than baked into weights, making it a flexible lever for capability without retraining. The paradigm has become a central axis along which frontier models differentiate, with some systems (Qwen3) shipping hybrid modes that switch between thinking and non-thinking on demand, and others (Kimi K2) explicitly declining it as architecturally out of scope.

**Type:** method
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/chain_of_thought|Chain of Thought]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/policy_optimization|Policy Optimization]], [[themes/post_training_methods|Post-Training Methods]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reward_modeling|Reward Modeling]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

In thinking mode, the model generates an extended internal monologue before committing to an answer. This trace is not merely cosmetic — it functions as a scratchpad where the model can decompose problems, backtrack on errors, verify intermediate steps, and synthesise partial results before final output. The contrast with non-thinking (or "reflex") mode is sharp: non-thinking models answer immediately from pattern recognition, while thinking models spend tokens to reason. The difference in downstream accuracy on hard mathematical and competitive benchmarks can be substantial, though the picture is more nuanced at scale (see Limitations).

The rise of thinking mode has catalysed a secondary problem: how to aggregate multiple thinking-mode solutions. Standard majority voting degrades when correct answers appear in the minority, precisely because thinking-mode solutions are longer, more diverse, and less likely to cluster around a single surface form. "The Majority is not always right" directly addresses this failure mode with AggLM, a small aggregator trained via reinforcement learning from verifiable rewards to review, reconcile, and synthesise a final answer from a candidate set — achieving better results than majority voting over 16 solutions using only 8, and outperforming 72B reward-model selection baselines at 1.7B parameters.

## Key Findings

The AggLM work reveals several non-obvious structural properties of thinking-mode outputs. **Diversity is a feature, not a bug**: AggLM's advantage over majority voting is largest precisely when the candidate set is most diverse — when solutions are uncertain and minority-correct answers are most at risk of being suppressed. This directly validates a key limitation of majority voting in the thinking-mode regime: high-quality reasoning can produce heterogeneous answer forms that suppress correct minority answers through sheer surface variation.

**Token efficiency is a real advantage of aggregation over scaling the solution model.** The AggLM aggregator consumes roughly one-third the tokens per generation that the solution models do, meaning that achieving equivalent performance gains by simply generating more solutions from the base model would be substantially more expensive. This asymmetry has practical implications for deployment budgets: a small trained aggregator is a more compute-efficient lever than brute-force sampling.

**Reward-model selection is surprisingly fragile with thinking-mode inputs.** Best-of-N and weighted majority voting with AceMath (7B/72B) are frequently *inferior* to plain majority voting when aggregating thinking-mode solutions — a counterintuitive result suggesting that reward models trained primarily on non-thinking distributions may misread the longer, more exploratory trace format. This is an important warning for practitioners who assume that any reward model will improve over naive aggregation.

**Curriculum balance matters more than data volume.** Training AggLM on hard examples alone leads to suboptimal performance; including all easy examples adds only marginal lift over an untrained aggregator. The sweet spot — 5–50% easy examples relative to hard — is stable and teaches the model both to rescue minority-correct answers on hard problems and to correctly handle majority-correct answers on easy ones. More data from the solution model, rather than from a trained aggregator, does not close the performance gap, confirming that the gains are genuinely attributable to learning the aggregation skill rather than additional exposure to solved problems.

**Cross-distribution generalisation is strong but asymmetric.** AggLM-1.7B, trained exclusively on thinking-mode distributions, generalises effectively to non-thinking model solutions — remaining the top performer across datasets. It also transfers to stronger solution models (Qwen3-8B) not seen during training. The practical upshot is that a single small aggregator can serve as a drop-in component across a range of base models without per-model retraining.

## Capabilities

Recent production systems illustrate the breadth of what thinking mode unlocks:

- Qwen3 deploys a **hybrid thinking/non-thinking mode** in a single model, enabling extended reasoning for hard tasks and instant responses for simple queries without model switching. Its non-thinking mode already achieves state-of-the-art math performance among non-thinking models (AIME 2024 69.6 Avg@64, MATH-500 97.4%), while thinking mode pushes further on competition-level problems.
- The open-source MoE variant (32B active / 1T total) reaches 65.8% on SWE-bench Verified single-attempt agentic coding, rising to 71.6% with parallel test-time compute sampling — showing thinking mode combines naturally with parallel sampling strategies.
- AggLM-1.7B raises Qwen3-1.7B's AIME25 accuracy from 35% to 50%, exceeding majority voting at 45%, which demonstrates that thinking mode's benefit is amplifiable post-hoc by learned aggregation rather than requiring a stronger base model.

## Known Limitations

Two limitations cut against the most optimistic reading of thinking mode's advantages:

**Token-budget equivalence on standard benchmarks.** Under equivalent inference token budgets, thinking and non-thinking models converge to comparable pass@k performance on MATH-500. This is a significant qualifier: if the headline advantage of thinking mode is that it spends more tokens, then controlling for budget erodes that advantage on benchmarks where non-thinking models can simply sample more. The implication is that thinking mode's edge may be most durable on problems that genuinely require sequential, dependent reasoning steps — not problems where independent samples plus majority voting can substitute. Whether this holds on harder competition-level tasks (AIME, HMMT) remains an open question.

**Reward model mismatch.** As noted above, off-the-shelf reward models often underperform majority voting when scoring thinking-mode candidates. This is not a limitation of thinking mode per se, but it creates a practical gap: the reward-model infrastructure built for non-thinking systems does not transfer cleanly, and new aggregation-aware components (like AggLM) are needed to capture the value of the richer reasoning traces.

**Architectural exclusion.** Kimi K2 is explicitly a "reflex-grade model without long thinking," which signals that the MoE architecture and training objectives optimised for broad capability at scale are not trivially compatible with thinking mode. The fact that a 1T-parameter frontier model ships without thinking mode suggests there are still real architectural or training cost constraints limiting how broadly thinking mode can be deployed.

## Relationships

Thinking mode is the primary enabling condition for [[themes/test_time_compute_scaling|test-time compute scaling]] strategies — without extended reasoning traces, techniques like best-of-N sampling, sequential revision, and learned aggregation lack the rich intermediate signal they exploit. It is downstream of [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] post-training (models are trained to produce useful traces via GRPO or similar), and upstream of [[themes/reward_modeling|reward modeling]] challenges (reward models must adapt to trace-format inputs). The AggLM work from "The Majority is not always right" sits at the intersection of thinking mode, [[themes/policy_optimization|policy optimisation]], and [[themes/mathematical_and_formal_reasoning|mathematical reasoning]], using thinking-mode diversity as the raw material that aggregation learns to exploit. The hybrid deployment pattern in Qwen3 connects thinking mode to [[themes/adaptive_computation|adaptive computation]] — the mode itself becomes a runtime routing decision rather than a fixed model property.
```

## Limitations and Open Questions

## Sources
