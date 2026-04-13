---
type: entity
title: policy entropy
entity_type: metric
theme_ids:
- agent_systems
- mathematical_and_formal_reasoning
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 2.123373729235599e-05
staleness: 0.0
status: active
tags: []
---
# policy entropy

Policy entropy measures the diversity of a policy's output distribution during reinforcement learning training — essentially, how spread out or concentrated a model's probability mass is across possible next tokens. In the context of RL for LLM reasoning, it has emerged as one of the most diagnostic signals for training health: a policy exploring meaningfully maintains moderate entropy, while one that has locked in on a narrow set of behaviors collapses toward zero. Its significance extends beyond a monitoring metric; entropy dynamics now appear to fundamentally govern the ceiling of what RL training can achieve.

**Type:** metric
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/policy_optimization|policy_optimization]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Overview

Policy entropy quantifies, at each training step, how uncertain or explorative a language model policy is when generating outputs. High entropy means the policy spreads probability across many tokens; low entropy means it has converged on near-deterministic behavior. During RL training for reasoning tasks, this quantity evolves rapidly and non-trivially — and its trajectory is now understood to be tightly coupled with downstream performance outcomes.

The core finding from The Entropy Mechanism of Reinforcement Learning for Reasoning Language Models is stark: without any entropy intervention, policy entropy collapses sharply to near zero within just a few training steps. The mechanism is self-reinforcing — once a policy becomes highly certain, it loses the ability to discover alternative solution paths, and training stalls. Critically, the relationship between entropy and downstream validation accuracy is not linear but exponential: performance follows the law R = −a·exp(H) + b, meaning that as entropy decays, performance improvements become exponentially harder to sustain.

This theoretical characterization finds direct empirical support in JustRL. There, a stable entropy oscillation in the range of 1.2–1.4 throughout training is associated with healthy learning dynamics and state-of-the-art results on mathematical reasoning benchmarks at the 1.5B scale — 54.9% and 64.3% average accuracy across nine benchmarks, and AIME 2024 performance climbing from 28% to 58% over 4,000 training steps. The entropy band is not incidental: it is presented as a key indicator that the policy is still exploring rather than exploiting a narrow solution pattern.

## Entropy Collapse as a Failure Mode

The most practically important insight is that many common training interventions inadvertently destroy the entropy range necessary for learning. JustRL's ablations make this concrete. Adding an explicit overlong penalty — a seemingly reasonable technique to discourage verbose outputs — collapses entropy to 0.5–0.6, roughly half the healthy range, and caps AIME 2024 performance at 50% versus the 55% baseline. When both an overlong penalty and a more robust verifier are added simultaneously, performance degrades further, plateauing at 45% — a 10 percentage point loss. The entropy collapse in both cases is the common cause: the policy stops exploring and settles into a compressed behavioral mode.

What makes this finding counterintuitive is that the length compression it was designed to prevent happens organically anyway. Without any explicit penalty, response length naturally converges from ~8,000 tokens to 4,000–5,000 tokens by step 1,000 and maintains that range. The lesson is that interventions perceived as helpful hygiene can impose hidden costs by interfering with the exploration dynamics that entropy tracks.

## Entropy as a Design Constraint

JustRL's approach treats entropy stability not as an outcome to engineer directly but as a constraint that other design choices must respect. The single non-default technique employed — asymmetric clipping (`clip higher`, with ratio [0.8, 1.28]) — is framed as a baseline practice for stability in long-horizon RL rather than an entropy-specific intervention. The training setup (GRPO with binary outcome rewards, a lightweight rule-based verifier from DAPO, single-stage fixed hyperparameters) is deliberately minimal, and the entropy behavior that results appears to be an emergent property of avoiding over-specified reward shaping.

This contrasts with approaches like DeepScaleR, which uses a three-stage curriculum with progressively increasing context lengths (8K→16K→24K), and BroRL, which achieves competitive results by scaling rollouts to 512 per example — at 4.9× the compute cost of JustRL-DeepSeek. Entropy stability, in JustRL's framing, is what allows a simple single-stage recipe to match or exceed the performance of more elaborate pipelines without exhaustive exploration via brute-force sampling.

## Open Questions and Limitations

Despite its diagnostic power, policy entropy as studied here leaves substantial questions unresolved. JustRL cannot isolate which specific components of its recipe — hyperparameters, verifier design, training data — are most responsible for the healthy entropy trajectory it observes. The causal direction is unclear: does the training setup produce good entropy behavior and therefore good performance, or is the entropy merely a correlate of other factors that are doing the real work?

The scope of established findings is also narrow. All results are on mathematical reasoning at the 1.5B parameter scale. Whether the exponential relationship between entropy and performance holds for coding, general QA, or agentic tasks is unknown. Whether the 1.2–1.4 oscillation range is specific to this scale and task distribution, or reflects a more general principle, is unexplored. JustRL also acknowledges it has not tested whether its approach maintains its advantages at longer training horizons, leaving open the question of whether entropy management becomes harder or requires additional techniques as training extends.

The exponential law R = −a·exp(H) + b is empirically derived; its theoretical grounding — why this functional form and not another — is not yet established. This matters because extrapolation beyond the observed entropy range is unreliable without a mechanistic account of why entropy collapse produces the performance ceiling it does.

## Relationships

Policy entropy is closely linked to [[entities/grpo|GRPO]] as the optimization algorithm within which its dynamics are most studied, and to clip higher as a stabilization technique that appears to preserve healthy entropy ranges. It is implicated in the behavior of overlong penalty interventions, which the evidence now suggests should be approached with caution given their entropy-collapsing effects. The exponential performance law connects it to broader questions about [[themes/scaling_laws|scaling laws]] for RL training and [[themes/test_time_compute_scaling|test-time compute scaling]] — particularly whether entropy can be managed as a resource analogous to tokens or compute. The findings from JustRL and The Entropy Mechanism together form the primary empirical and theoretical basis for current understanding of this entity.

## Key Findings

## Limitations and Open Questions

## Sources
