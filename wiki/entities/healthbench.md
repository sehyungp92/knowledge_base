---
type: entity
title: HealthBench
entity_type: dataset
theme_ids:
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- hallucination_and_reliability
- medical_and_biology_ai
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scientific_and_medical_ai
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00025376636378822914
staleness: 0.0
status: active
tags: []
---
# HealthBench

HealthBench is OpenAI's open-source benchmark for evaluating large language model performance on healthcare guidance tasks, distinguished by its scale, physician-validated rubrics, and emphasis on realistic, open-ended conversational evaluation. Released in 2025, it represents a significant methodological shift away from multiple-choice medical exams toward nuanced, multi-turn assessments that better reflect real-world clinical communication — and has rapidly become a reference point for tracking frontier model progress in medical AI.

**Type:** dataset
**Themes:** [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/policy_optimization|policy_optimization]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

HealthBench comprises 5,000 multi-turn conversations between models and users (patients or healthcare professionals), evaluated against 48,562 unique rubric criteria developed by 262 physicians across 26 specialties and 60 countries. Rubrics span seven health themes — including emergency referrals, context-seeking, global health, and health data tasks — and five behavioral axes: accuracy, completeness, communication quality, instruction following, and context-awareness. This design directly addresses three structural failures of prior health benchmarks: reliance on multiple-choice exams that don't reflect real-world impact, absence of validation against genuine expert medical opinion, and benchmark saturation that leaves no headroom for model improvement.

The benchmark is accompanied by HealthBench Hard, a curated subset of 1,000 particularly difficult examples on which the current top frontier model scores only 32%, preserving meaningful room for future development.

## Methodology and Grading

A key design choice is the use of model-based grading: GPT-4.1 acts as the automated rubric grader in place of human physicians for each evaluation run. This is validated by showing that model-physician agreement is statistically comparable to physician-physician agreement, both ranging from 55–75% on consensus criteria. GPT-4.1 as grader exceeds the average physician macro-F1 score in five out of seven themes, placing it in the upper half of physicians for six themes — a strong empirical basis for automated grading at scale. Measurement reliability is high: repeated runs yield a standard deviation of approximately 0.002 across scores ranging from 0.16 to 0.60.

This grading approach has made HealthBench attractive as an evaluation target in RL and reward modeling research. Papers on rubric-as-reward methods (see Rubrics as Rewards and Direct Reasoning Optimization) cite HealthBench specifically as a non-verifiable domain where rubric-based reward signals can replace ground-truth verification — extending RL training beyond domains with checkable answers.

## Model Performance Trends

HealthBench captures a striking two-year arc of progress: GPT-3.5 Turbo scored 16%, GPT-4o scored 32%, and o3 reached 60% on the main benchmark, with model error rates on consensus criteria falling by over 4× from GPT-3.5 through GPT-4.1. Smaller models have improved particularly sharply — GPT-4.1 nano outperforms GPT-4o while being 25× cheaper, illustrating how efficiency gains at the small-model tier are catching up to prior large-model baselines.

Among non-OpenAI models, Grok 3 and Gemini 2.5 Pro performed strongly; Claude 3.7 Sonnet and Llama 4 Maverick lagged markedly behind. This cross-model spread makes HealthBench useful as a comparative lens on the broader frontier, not just an internal OpenAI metric.

A structurally important finding: recent LLMs outperform unassisted physicians on HealthBench. Physicians could improve model responses from September 2024 models but not April 2025 models — a threshold that marks a qualitative shift in the human-AI relationship in clinical communication contexts.

## What Models Still Struggle With

Performance is systematically uneven across axes. Models score lower on completeness and context-awareness than on accuracy, communication quality, or instruction following — a pattern that suggests models are better at saying correct things than at knowing what to ask for or what to leave unsaid. Theme-level variation reinforces this: emergency referrals and expertise-tailored communication score highest, while context-seeking, health data tasks, and global health score lowest. The global health gap is notable, as it may reflect training data skew toward high-income, English-language clinical settings.

## Known Limitations

The benchmark carries several significant constraints that temper its authority as a measure of real-world clinical utility.

Most fundamentally, HealthBench evaluates single model responses to conversations — not multi-step clinical workflows or longitudinal patient interactions. The benchmark cannot measure whether AI actually improves patient health outcomes in deployment, which is the outcome that ultimately matters. This gap between benchmark score and real-world impact is not unique to HealthBench, but it is especially consequential in healthcare, where the cost of errors is high and clinical workflows are inherently iterative.

The majority of HealthBench conversations are synthetically generated rather than drawn from real patient-LLM interactions. Distribution mismatch between synthetic and real-world prompts may cause benchmark scores to overestimate or mischaracterize performance in actual deployment — a concern that is particularly acute for rare or high-stakes clinical presentations that are hard to synthesize realistically.

Even with these caveats, the ceiling problem on HealthBench Hard (32% top score) indicates that a large fraction of complex, real-world health queries remain unsolved by current frontier models — a blocking limitation for deployment in high-acuity settings, even as mainstream HealthBench scores continue to improve rapidly.

## Relationships

HealthBench is produced and described in HealthBench: Evaluating Large Language Models. It appears as an evaluation target in rubric-reward and RL research, including Rubrics as Rewards and Direct Reasoning Optimization, where it anchors claims about extending RL training to non-verifiable domains. It connects thematically to [[themes/benchmark_design|benchmark design]] debates about the limits of multiple-choice evaluation, to [[themes/reward_modeling|reward modeling]] work that repurposes rubrics as training signal, and to [[themes/medical_and_biology_ai|medical and biology AI]] more broadly as one of the few benchmarks with genuine expert validation at scale.

## Key Findings

## Limitations and Open Questions

## Sources
