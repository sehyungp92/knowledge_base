---
type: entity
title: Muon Optimizer
entity_type: method
theme_ids:
- adaptive_computation
- agent_evaluation
- agent_systems
- ai_for_scientific_discovery
- ai_market_dynamics
- benchmark_design
- code_and_software_ai
- code_generation
- continual_learning
- evaluation_and_benchmarks
- frontier_lab_competition
- in_context_and_meta_learning
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- model_commoditization_and_open_source
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- scientific_and_medical_ai
- software_engineering_agents
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.00639634338929243
staleness: 0.0
status: active
tags: []
---
# Muon Optimizer

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_evaluation|agent_evaluation]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/benchmark_design|benchmark_design]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vision_language_models|vision_language_models]]

## Overview

A relatively unproven optimizer used in Kimi K2's training, noted for its 'beautiful learning curve'.

## Key Findings

1. Atlas is the first parallelizable recurrent architecture that optimizes memory using an approximation of second-order information, giving it a locally optimal memory module. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
2. The online nature of memory updates in most recurrent models—where memory is optimized with respect to only the current input—leads to memorization of individual tokens without considering broader con (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
3. Polynomial kernels are motivated as approximators of Softmax attention: the exponential kernel in Transformers can be approximated by a Taylor series, and polynomial feature maps generalize this appro (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
4. Modern recurrent architectures can be unified as associative memory modules optimizing an internal objective termed 'attentional bias'. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
5. Polynomial feature map coefficients can be interpreted as input feature gates: setting a_i→0 excludes a feature map, and setting a_i→1 retains it, providing gating on the input rather than the memory. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
6. Atlas achieves +80% accuracy improvement over Titans on the BABILong benchmark at 10M context length. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
7. Most recent recurrent models use gradient descent relying on first-order information about token dynamics, which causes memory to converge to spurious local minima and learn less effective key-value m (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
8. The Omega rule formulation connects to global and local softmax attentions (Sliding Window Attention), enabling derivation of DeepTransformers as strict generalizations of Transformers. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
9. Transformers have quadratic memory and time complexity, which bounds their applicability to longer sequences. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
10. Atlas, built on the Omega rule and Muon optimizer, surpasses the performance of Transformers and recent linear recurrent models on language modeling, common-sense reasoning, recall-intensive, and long (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
11. Attention functions as an associative memory that computes direct pairwise token dependencies, causing at least N×d operations per token for output calculation. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
12. Matrix-valued memory with the delta update rule (ℓ2 attentional bias) has sub-linear capacity with respect to its number of parameters, storing at most O(d_k) linearly independent key-value pairs. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
13. The shortcomings of modern recurrent models arise from three disjoint design aspects: limited memory capacity, online nature of update, and less expressive management of fixed-size memory. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
14. Modern recurrent neural networks (long-term recurrent memory modules) struggle with long context understanding and extrapolation to longer sequences despite recent success in diverse downstream tasks. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")
15. DeepTransformers are strictly more powerful generalizations of the original Transformer architecture. (from "ATLAS: Learning to Optimally Memorize the Context at Test Time")

## Capabilities

- Multi-scale Momentum Muon (M3) optimizer with multiple momentum terms encoding multi-frequency gradient compression, extending the Muon optimizer family (maturity: research_only)

## Known Limitations

- Muon optimizer causes training instability (exploding attention logits) at scale — existing mitigations (logit soft-capping, query-key normalization) are inadequate, requiring new architectural interv (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
