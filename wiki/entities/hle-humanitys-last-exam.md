---
type: entity
title: HLE (Humanity's Last Exam)
entity_type: dataset
theme_ids:
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 9.391091307518157e-05
staleness: 0.0
status: active
tags: []
---
# HLE (Humanity's Last Exam)

> Humanity's Last Exam (HLE) is a benchmark designed to probe the outer limits of frontier model capability, requiring specialized graduate-level domain knowledge across multiple disciplines. It has emerged as a key reference point for distinguishing genuine expert-level reasoning from pattern-matched competence, and current model scores — clustered between 14% and 21% — suggest the field remains far from saturating it.

**Type:** dataset
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/alignment_and_safety|Alignment and Safety]], [[themes/alignment_methods|Alignment Methods]], [[themes/benchmark_design|Benchmark Design]], [[themes/chain_of_thought|Chain of Thought]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/finetuning_and_distillation|Finetuning and Distillation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/hallucination_and_reliability|Hallucination and Reliability]], [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/scaling_laws|Scaling Laws]], [[themes/software_engineering_agents|Software Engineering Agents]]

---

## Overview

HLE was conceived as a deliberate counterweight to benchmarks that frontier models had already saturated. Where [[themes/mathematical_and_formal_reasoning|mathematical reasoning]] benchmarks like AIME24 probe pure deductive ability using high school mathematics — problems solvable, in principle, with no specialist background — HLE requires deep, cross-domain graduate-level knowledge that cannot be reconstructed from first principles alone. The distinction matters: AIME24 tests whether a model can reason; HLE tests whether a model *knows things* that only genuine experts know, and can apply that knowledge in novel combinations.

This design choice makes HLE one of the more honest difficulty gradients in current evaluation. It is not a collection of tricky reformulations of solved problems; it is an attempt to locate the genuine frontier of model knowledge, where memorisation fails and cross-domain synthesis is unavoidable.

---

## Performance Landscape

Scores on HLE remain strikingly low across all frontier models, which is precisely the point. As of mid-2025 assessments, the spread clusters between roughly 14% and 21%, with Gemini 2.5 Pro at approximately 21.1%, o3 at 20.0%, and models like GLM-4.5 — which performs competitively on agentic and coding benchmarks — trailing at 14.4%. The 6–10 point gap between top and mid-tier performers on HLE is disproportionately large relative to gaps on other benchmarks, suggesting that HLE is capturing a dimension of capability that does not improve uniformly with general scaling or post-training.

This performance cliff is significant. GLM-4.5, which achieves the highest average tool-calling success rate (90.6%), outperforms o3 on agentic TAU-bench tasks, and ranks third overall across a broad twelve-benchmark suite, still sits well below top performers on HLE. The implication is that agentic competence — the ability to use tools, plan multi-step actions, and produce verifiable outputs — is partially orthogonal to the kind of deep domain knowledge HLE measures. Models can become excellent engineers and agents while remaining weak on genuinely hard, knowledge-intensive reasoning.

---

## Key Findings

The evidence linking HLE to broader model evaluations points to a structural limitation in current training pipelines. Post-training methods optimised for verifiable, execution-based tasks (software engineering, tool use, information-seeking QA) improve agentic scores but appear to provide limited lift on HLE. This is consistent with the benchmark's design: there is no external feedback signal when a model is wrong about graduate-level organic chemistry or topology — only the answer itself reveals correctness, which makes RL-based post-training harder to apply directly.

From the GLM-4.5 technical report, HLE emerges as the clearest marker of the gap between surface-level frontier performance and genuine expert knowledge depth. The trajectory is labelled *improving* — scores are not static — but the improvement rate is slow relative to gains on coding and agentic tasks, reinforcing the view that HLE is measuring something the current training paradigm does not optimise well.

---

## Known Limitations and Open Questions

HLE itself has a structural tension worth noting: a benchmark requiring graduate-level specialist knowledge inevitably has a finite and potentially narrow coverage of domains. Whether it samples cross-domain reasoning *representatively* — or whether high scorers are partly benefiting from better coverage of the specific domains HLE happens to include — remains an open methodological question.

More broadly, HLE surfaces a bottleneck in [[themes/evaluation_and_benchmarks|evaluation design]]: as models improve at measurable, verifiable tasks, the remaining hard problems tend to be those with limited ground truth signal during training. HLE's low scores may reflect not just a knowledge gap but a *feedback gap* — the training loop cannot easily reward correct expert-level reasoning the way it rewards passing unit tests or solving competition math.

From a [[themes/hallucination_and_reliability|reliability]] perspective, the low HLE scores also raise the question of calibration: do models that score 14–21% know what they don't know on the remaining 79–86%? Or are they hallucinating confidently in specialised domains? The sources referencing HLE in the context of hallucination research suggest this remains an active concern.

---

## Relationships

HLE sits in direct contrast to AIME24 and similar competition-math benchmarks, which models now solve at high rates and which no longer discriminate well between frontier systems. It is increasingly cited alongside [[themes/scaling_laws|scaling law]] discussions as evidence that capability gains are domain-uneven: scaling and post-training compound effectively on structured, verifiable tasks while providing diminishing returns on open-ended knowledge depth.

The benchmark is referenced across sources including Why Language Models Hallucinate, Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?, and the GLM-4.5 technical report, suggesting it has become a stable reference point across both capability and reliability research.

## Limitations and Open Questions

## Sources
