---
type: entity
title: ARC-AGI-1
entity_type: dataset
theme_ids:
- adaptive_computation
- agent_memory_systems
- ai_market_dynamics
- benchmark_design
- continual_learning
- evaluation_and_benchmarks
- frontier_lab_competition
- knowledge_and_memory
- latent_reasoning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- search_and_tree_reasoning
- test_time_compute_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00023965937942658564
staleness: 0.0
status: active
tags: []
---
# ARC-AGI-1

> ARC-AGI-1 is the original Abstraction and Reasoning Corpus benchmark, introduced by François Chollet in 2019, designed to resist pattern-memorization by requiring genuine program synthesis and visual analogy. For four years it served as AI's hardest public reasoning gauntlet; by 2024–2025 it became a story of sudden saturation — and a lesson in the gap between benchmark passage and actual intelligence.

**Type:** dataset
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/benchmark_design|Benchmark Design]], [[themes/continual_learning|Continual Learning]], [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/latent_reasoning|Latent Reasoning]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/search_and_tree_reasoning|Search and Tree Reasoning]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/test_time_learning|Test-Time Learning]], [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Overview

ARC-AGI-1 consists of visual grid-transformation puzzles that humans can solve intuitively but that proved nearly impenetrable to deep learning for years. The benchmark is split into a Public Training set, a Public Evaluation set (400 tasks), and a Semi-Private Evaluation set used for official scoring. Its defining property is that each puzzle type appears only in that puzzle — there is no statistical shortcut through memorization of task formats.

Progress was glacial through the transformer era: GPT-3 scored 0% in 2020, and GPT-4o reached only 5% in 2024 — four years of frontier scaling for a 5-point gain. That trajectory collapsed entirely with the arrival of OpenAI o3.

---

## Key Findings

### The o3 Discontinuity

o3 scored 75.7% on the Semi-Private Evaluation set at the high-efficiency ($10k) compute limit, and 87.5% at a 172x higher compute configuration. On the Public Eval set, the high-efficiency run (6 samples per task) reached 82.8%; the low-efficiency run (1,024 samples per task) reached 91.5%. This was not a incremental improvement — it was a phase transition after years of near-zero progress.

Critically, ARC Prize disclosed that o3 was trained on 75% of the Public Training set, raising legitimate contamination questions. The benchmark's semi-private eval exists precisely to guard against this, but training proximity to test-adjacent data is now a design pressure every future benchmark must explicitly address.

### Compute Cost as a First-Class Metric

The o3 results forced a methodological update: efficiency (compute cost per task) is now a required reporting metric alongside raw score. The economic gap is stark — a human can solve an ARC-AGI task for roughly $5, while o3 in low-efficiency mode costs approximately $1,900 per task on the Public Eval set ($760k total for 400 tasks). High-efficiency o3 brings this to ~$167 per task — still 33× human cost, and without the human's near-zero energy overhead. This frames ARC-AGI-1 performance not as a capability binary but as a cost-capability frontier.

### Saturation from Below

Simultaneously, the benchmark is being closed from the other direction: a large ensemble of low-compute Kaggle solutions now scores 81% on the private eval, without any frontier-scale models. This dual pressure — frontier compute from above, ensemble methods from below — signals that ARC-AGI-1 has largely served its discriminative purpose and is now saturating.

### Memory and Test-Time Learning Approaches

ArcMemo demonstrates a different attack surface: lifelong LLM memory that accumulates reusable reasoning patterns across tasks. ArcMemo-PS improved the official score from 55.17 to 59.33 (+7.5% relative gain over a no-memory baseline), and with two retries reached an Oracle@2 score of 70.83. This approach is notable because it achieves competitive performance through accumulated experience rather than brute-force compute scaling — closer in spirit to what ARC-AGI-1 was designed to reward.

### Small Models and Structural Reasoning

HRM (Hierarchical Reasoning Model) reached 32% on the Semi-Private Evaluation set — impressive given its small parameter count — by relying on structural inductive biases rather than scale. Notably, HRM receives only the input and a `puzzle_id` at inference time, with no few-shot context from other input-output examples of the same task. This makes its performance a cleaner test of learned compositional reasoning. However, HRM scored only 2% on ARC-AGI-2, suggesting its inductive biases are specifically tuned to ARC-AGI-1's distribution.

---

## Limitations and Open Questions

The most important claim about ARC-AGI-1 comes from ARC Prize itself: passing the benchmark does not equate to AGI. o3 still fails on tasks that are trivially easy for humans, indicating fundamental asymmetries that the aggregate score obscures. A benchmark that can be saturated by a large Kaggle ensemble at low compute, or by a frontier model trained on adjacent data, is no longer measuring what it was designed to measure.

The successor ARC-AGI-2 was released to address this — and HRM's 2% on that set illustrates just how different the two distributions are. The lesson from ARC-AGI-1's trajectory is that benchmark design must anticipate both the memorization axis (training contamination) and the compute axis (brute-force sampling); neither raw score nor single-configuration testing is sufficient.

---

## Relationships

- Superseded by **ARC-AGI-2**, which proved resistant to the methods that saturated ARC-AGI-1.
- Directly evaluated: o3 ARC-AGI results, ArcMemo, HRM analysis.
- Thematically central to [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] (o3's sampling strategy), [[themes/test_time_learning|Test-Time Learning]] (ArcMemo's memory accumulation), and [[themes/benchmark_design|Benchmark Design]] (saturation dynamics and the move to ARC-AGI-2).

## Sources
