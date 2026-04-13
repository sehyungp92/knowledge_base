---
type: entity
title: Test-Time Training
entity_type: method
theme_ids:
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_market_dynamics
- benchmark_design
- computer_use_and_gui_agents
- continual_learning
- evaluation_and_benchmarks
- frontier_lab_competition
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- scaling_laws
- search_and_tree_reasoning
- test_time_compute_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.003173189804818694
staleness: 0.0
status: active
tags: []
---
# Test-Time Training

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/representation_learning|representation_learning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

A form of TTA where the model adjusts some of its parameters based on examples in the test task using gradient descent, enabling in-context adaptation beyond static retrieval.

## Key Findings

1. ARC-AGI measures generalization on novel tasks rather than skill at tasks that can be prepared for in advance. (from "ARC Prize 2024: Technical Report")
2. A Mechanical Turk study found 99% of public evaluation tasks were solved by at least one worker, with 10 workers assigned to each task. (from "ARC Prize 2024: Technical Report")
3. A human can solve ARC-AGI tasks for approximately $5 per task, while o3-preview requires approximately $27 per task in low-compute mode. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
4. The ARC-AGI benchmark remains unbeaten as of December 5, 2024, five years after its creation. (from "ARC Prize 2024: Technical Report")
5. ARC-AGI-1 is now saturating — a large ensemble of low-compute Kaggle solutions can score 81% on the private eval. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
6. ARC-AGI-1 consists of 1,000 tasks split into four subsets: 400 public training tasks, 400 public evaluation tasks, 100 semi-private evaluation tasks, and 100 private evaluation tasks. (from "ARC Prize 2024: Technical Report")
7. o3 scored 82.8% on the Public Eval set at high-efficiency and 91.5% at low-efficiency. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
8. ARC-AGI-1 took 4 years to progress from 0% with GPT-3 in 2020 to only 5% with GPT-4o in 2024. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
9. o3 scored 75.7% on the ARC-AGI-1 Semi-Private Evaluation set at the high-efficiency ($10k) compute limit. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
10. OpenAI trained the o3 tested by ARC Prize on 75% of the Public Training set. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
11. Efficiency (compute cost) is now a required metric when reporting performance on ARC-AGI, not just raw score. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
12. The high-efficiency configuration used 6 samples per task; the low-efficiency configuration used 1024 samples, representing approximately 172x more compute. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
13. o3 still fails on some very easy tasks, indicating fundamental differences with human intelligence, and the author does not consider o3 to be AGI. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
14. A high-compute (172x) o3 configuration scored 87.5% on the Semi-Private Evaluation set. (from "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub")
15. In the first Kaggle ARC-AGI competition (2020), no deep-learning based approach scored above 1%. (from "ARC Prize 2024: Technical Report")

## Capabilities

- Test-time training (TTT) with an 8B LLM ensembled with program synthesis achieves 61.9% on ARC public validation, matching average human performance of 60.2% — the first neural-driven system to reach  (maturity: research_only)

## Relationships

## Limitations and Open Questions

## Sources
