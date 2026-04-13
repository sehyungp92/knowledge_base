---
type: entity
title: CoT-Pass@k
entity_type: metric
theme_ids:
- alignment_and_safety
- chain_of_thought
- hallucination_and_reliability
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- policy_optimization
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000916291647773556
staleness: 0.0
status: active
tags: []
---
# CoT-Pass@k

CoT-Pass@k is a verifiable reward metric for evaluating language model reasoning that extends the standard Pass@k benchmark by requiring correctness in both the final answer *and* the intermediate chain-of-thought steps. Where Pass@k measures only whether a correct answer appears in k sampled completions, CoT-Pass@k exposes whether the model actually reasoned its way there — making it a sharper diagnostic for distinguishing genuine reasoning improvement from surface-level answer matching. This distinction has become significant in the analysis of RLVR (Reinforcement Learning with Verifiable Rewards) training dynamics, where answer-only metrics can mask a narrowing of the underlying reasoning distribution.

**Type:** metric
**Themes:** [[themes/alignment_and_safety|Alignment & Safety]], [[themes/chain_of_thought|Chain of Thought]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/long_context_and_attention|Long Context & Attention]], [[themes/mathematical_and_formal_reasoning|Mathematical & Formal Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/policy_optimization|Policy Optimization]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/reasoning_and_planning|Reasoning & Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/rl_theory_and_dynamics|RL Theory & Dynamics]], [[themes/scaling_laws|Scaling Laws]]

---

## Overview

CoT-Pass@k operationalises a deceptively simple idea: a model that arrives at the right answer through flawed reasoning is not improving in the way that matters. By demanding chain-of-thought correctness alongside final-answer correctness, it functions as a stricter filter that penalises lucky or shortcut solutions. This makes it particularly valuable in regimes where the evaluation signal might otherwise reward outcome without process — a concern central to RLVR, where reward shaping directly influences the training distribution.

The metric gains force precisely because Pass@k and CoT-Pass@k can diverge. RLVR-trained models frequently outperform base models at low k on Pass@k, suggesting reliable answer production. But the underlying mechanism — support shrinkage — means RLVR progressively concentrates probability mass on already-supported solution paths while reducing the diversity of reasoning traces. A metric that inspects only outcomes is blind to this compression.

---

## The RLVR Context: Precision vs. Coverage

The most substantive findings around CoT-Pass@k emerge from work on RLVR's fundamental dynamics (see The Invisible Leash). RLVR training achieves very high support retention rates (SRR ≈ 0.93–0.99): the vast majority of solutions the RLVR model can produce were already present in the base model's distribution. Genuine discovery — solutions the base model could not have generated — remains rare, with new discovery rates (NDR) at or below 0.04. The apparent gains on standard benchmarks reflect *amplification of existing capacity*, not acquisition of new reasoning strategies.

This matters acutely when k is large. On AIME2024, the base model achieves pass@8192 = 93.3% while a ProRL-1.5B model achieves only 83.3%. At high sampling budgets, the base model's broader solution coverage dominates. RLVR trades tail coverage for precision: it makes the model more reliable at producing a correct answer on the first few attempts, but it simultaneously shrinks the space of reachable solutions. CoT-Pass@k captures the quality of individual reasoning chains and therefore remains sensitive to this trade-off even when aggregate Pass@k numbers look flat or improving.

Support shrinkage is asymmetric and consistent: ProRL-1.5B-v2 loses 175 completions while gaining only 48 (ratio ≈ 3.6:1). Similar shrinkage patterns appear across Nemotron-7B and Skywork-OR1-7B at ratios of roughly 2:1 to 3:1. The entropy-reward trade-off this creates — reliably enhanced precision, progressively narrowed exploration — is not domain-specific. It appears across mathematics, logical reasoning, factual QA, and code generation.

One further signal: RLVR training increases perplexity on diverse external reasoning traces. On AIME2024, perplexity on Claude Sonnet traces rises from 8.76 (base) to 14.91 after ProRL training. The model becomes less able to assign probability to reasoning styles it was not reinforced on — a form of reasoning monoculture that answer-only metrics would not detect.

---

## Theoretical Bounds and Limitations of Any Correctness Metric

CoT-Pass@k presupposes that intermediate reasoning steps can be verified — that there is a ground truth against which chain-of-thought can be checked. This requirement has non-trivial scope limits. Work on the fundamental limits of LLMs (see On the Fundamental Limits of LLMs at Scale) establishes that hallucination is not a correctable engineering deficit but a computability-theoretic inevitability: for any computably enumerable set of LLMs, there exists a computable ground-truth function such that every model hallucinates on at least one input. Worse, the failure set is infinite — each model hallucinates on *infinitely many* inputs, not rare edge cases.

This result is independent of architecture, training procedure, or prompt engineering — it holds for transformers, RNNs, and state-space models alike. Undecidable problems such as the Halting Problem force any computable LLM to hallucinate on infinitely many inputs, because a finite failure set would imply a computable decider. The theoretical impossibility results, bounded performance theorems, and capacity-aware diagnostics presented in that work characterise precisely where scaling helps, saturates, and fails across the five identified fundamental limitations: hallucination, context compression, reasoning degradation, retrieval fragility, and multimodal misalignment.

The implication for CoT-Pass@k is subtle but important: the metric assumes verifiable ground truth for intermediate steps, yet the hardest reasoning tasks — those where CoT-Pass@k would be most valuable — are precisely those where ground truth is most difficult to specify or check. For formal mathematics or code with test suites, verification is tractable. For open-ended reasoning, scientific inference, or problems with undecidable structure, the verifiability assumption breaks down and CoT-Pass@k becomes inapplicable or unreliable.

---

## Open Questions

The central unresolved tension is whether the support-shrinkage dynamic RLVR induces can be corrected without sacrificing the precision gains that make RLVR useful in the first place. CoT-Pass@k provides a diagnostic but not a remedy. Several questions remain open:

- Can RLVR be modified to maintain diversity over reasoning strategies while still reinforcing correctness? Entropy regularisation approaches exist but their interaction with the verifiable-reward signal is not well characterised.
- Does CoT-Pass@k have a natural extension to tasks where intermediate step verification is soft rather than binary — e.g., where reasoning quality is graded rather than pass/fail?
- The perplexity-on-external-traces finding suggests RLVR models become less able to generalise across reasoning styles. Whether this represents a fundamental trade-off or a training-procedure artefact is not yet settled.
- At very high k, base models dominate. This suggests there is a sampling-budget threshold below which RLVR is strictly beneficial and above which it is not. CoT-Pass@k could in principle trace this threshold more precisely than answer-only metrics, but this has not been systematically studied.

The metric is most powerful as a complement to Pass@k rather than a replacement: together, they triangulate whether a model is improving in output distribution, reasoning process, or both — distinctions that matter for understanding what RLVR is actually doing to models during training.

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
