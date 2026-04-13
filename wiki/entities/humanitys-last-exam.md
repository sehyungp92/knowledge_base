---
type: entity
title: Humanity's Last Exam
entity_type: dataset
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- ai_market_dynamics
- context_engineering
- frontier_lab_competition
- knowledge_and_memory
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- scientific_and_medical_ai
- software_engineering_agents
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.002675716169842819
staleness: 0.0
status: active
tags: []
---
# Humanity's Last Exam

> Humanity's Last Exam (HLE) is a highly challenging benchmark dataset designed to probe expert-level, cross-domain reasoning at the frontier of what current AI systems can achieve. Composed of questions drawn from advanced scientific and interdisciplinary domains, it serves as a stress test for models that otherwise appear capable on standard benchmarks — and the near-universal failure across all evaluated systems makes it one of the most diagnostic signals for genuine reasoning depth in the field.

**Type:** dataset
**Themes:** [[themes/adaptive_computation|Adaptive Computation]], [[themes/agent_memory_systems|Agent Memory Systems]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/context_engineering|Context Engineering]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/model_architecture|Model Architecture]], [[themes/model_commoditization_and_open_source|Model Commoditization and Open Source]], [[themes/multi_agent_coordination|Multi-Agent Coordination]], [[themes/policy_optimization|Policy Optimization]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/tool_use_and_agent_protocols|Tool Use and Agent Protocols]]

## Overview

Humanity's Last Exam functions as a ceiling benchmark — one where performance gaps between frontier models compress toward near-zero, and where even the best systems demonstrate that current architectures remain far from expert human capability. Unlike benchmarks that saturate quickly as models scale, HLE maintains genuine difficulty across the evaluation landscape, with top models including Gemini 2.5 Pro (21.1%), o3 (20.0%), and Grok 4 still failing on the vast majority of questions. The benchmark exists in at least two modalities; a text-only variant has elicited particularly bleak scores in the 3.7–7.1% range across all evaluated models, while multimodal variants allow slightly higher performance.

HLE has become a standard reporting benchmark for frontier open-source releases precisely because it does not lie — a model can score well on AIME or GPQA while hiding significant deficiencies in novel, interdisciplinary reasoning, and HLE surfaces those deficiencies immediately.

## Key Findings

The benchmark's value is best understood through the pattern of scores it generates across competing systems. GLM-4.5, a parameter-efficient open-source MoE model with 355B total and 32B activated parameters, achieves 14.4% on HLE — a result that reflects both genuine capability and a significant gap behind proprietary leaders. Notably, this score sits 6–10 points behind Gemini 2.5 Pro and o3, even as GLM-4.5 performs competitively or better on agentic and coding benchmarks, scoring 91.0% on AIME 24, 79.1% on GPQA, and 64.2% on SWE-bench Verified. The divergence between HLE scores and performance on structured reasoning benchmarks is itself a finding: models can be highly capable at decomposable, well-scoped problems while failing at the kind of open-ended, deeply cross-domain inference HLE demands.

Kimi K2 Thinking — a 1-trillion-parameter MoE model (32B active) post-trained with Quantization-Aware Training for INT4 inference — reportedly beats leading closed models on HLE, and this result is presented under INT4 precision matching production serving conditions. The framing of Kimi K2 as an HLE leader is notable given the INT4 precision caveat: INT4 quantization provides roughly a 2x generation speed improvement and is applied during post-training, meaning the benchmark results reflect quantized rather than full-precision performance. This matters for interpreting how much of the performance is attributable to the reasoning pipeline versus numerical precision.

Across the broader evaluation landscape documented in sources like MemRL and ToolOrchestra, HLE scores in the text-only setting cluster tightly between 3.7% and 7.1% — a range so narrow that it functions less as a ranking instrument and more as a collective demonstration of a shared capability ceiling. This uniformity is itself a structural signal: the benchmark is not differentiating well-resourced systems from less-resourced ones; it is revealing a shared architectural or training limitation.

## Known Limitations and Open Questions

The most significant limitation HLE surfaces is not a property of the benchmark itself but of the models it tests. A text-only HLE score in the 4–7% range constitutes near-total failure on expert-level interdisciplinary knowledge — and the fact that this holds across all evaluated models, regardless of scale or architecture, suggests the bottleneck is not easily addressed through standard scaling or RL fine-tuning approaches. The trajectory here is currently **unclear**: it is not obvious whether improved reasoning pipelines, longer context, or more RL-on-hard-problems (as in GLM-4.5's two-stage difficulty curriculum) will move the needle materially, or whether HLE is probing a qualitatively different capability that requires architectural change.

The **14.4% gap** between GLM-4.5's HLE score and that of leading closed models like Gemini 2.5 Pro (21.1%) is described as significant and improving, but it also reveals how far even competitive open-source models remain from mastery. That the gap exists against the backdrop of GLM-4.5 outperforming Claude Sonnet 4, o3, and GPT-4.1 on Terminal-Bench and achieving the best BFCL V3 score among evaluated baselines underscores the discontinuity between task-specific capability and general scientific reasoning depth.

An open structural question is whether HLE scores will ever saturate, and if so, what that would mean for the field. Unlike MMLU or GSM8K, HLE was designed with the explicit intention of remaining hard. If models approach 50%+ on HLE, that would constitute a qualitative shift in AI capability that would ripple across assessments of scientific and medical AI, knowledge representation, and the architecture of reasoning itself.

## Relationships

HLE is most frequently cited alongside [[themes/reasoning_and_planning|reasoning and planning]] benchmarks — AIME, GPQA, MATH — but its diagnostic value is orthogonal to those: models that excel on structured mathematical reasoning still fail catastrophically on HLE, making it a uniquely informative complement. Its connection to [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] is significant: the two-stage RL curriculum in GLM-4.5, which switches from moderate to extremely hard problems, is partially motivated by the need to push past the performance ceilings HLE exposes. Similarly, [[themes/test_time_compute_scaling|test-time compute scaling]] is implicated — Kimi K2 Thinking's interleaved reasoning architecture is designed in part to address exactly the multi-step, deeply inferential problems HLE contains.

The benchmark also functions as a proxy for the competitive standing of frontier labs in the [[themes/frontier_lab_competition|frontier lab competition]] narrative, with HLE scores increasingly used as headline figures in model releases to signal reasoning ambition.

## Limitations and Open Questions

## Sources
