---
type: entity
title: KV Cache
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- ai_market_dynamics
- chain_of_thought
- compute_and_hardware
- context_engineering
- continual_learning
- finetuning_and_distillation
- in_context_and_meta_learning
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- model_architecture
- model_commoditization_and_open_source
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 11
sources_since_update: 0
update_count: 1
influence_score: 0.008312102786737222
staleness: 0.0
status: active
tags: []
---
# KV Cache

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/compute_and_hardware|compute_and_hardware]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

The key-value cache used in the attention mechanism of transformer models during inference to avoid recomputing attention for already-processed tokens.

## Key Findings

1. LatentMAS reduces output token usage by 70.8%-83.7% compared to text-based MAS (from "Latent Collaboration in Multi-Agent Systems")
2. LatentMAS latent working memory is defined as layer-wise KV caches from all transformer layers, capturing both input context and newly generated latent thoughts — unlike prior cache-sharing methods th (from "Latent Collaboration in Multi-Agent Systems")
3. Cross-agent information transfer in LatentMAS is performed by layer-wise KV cache concatenation, so each successive agent's generation is conditioned on both the predecessor's working memory and its o (from "Latent Collaboration in Multi-Agent Systems")
4. Existing LLM-based multi-agent systems depend on text-based mediation for both reasoning and communication between agents (from "Latent Collaboration in Multi-Agent Systems")
5. LatentMAS transfers working memory as KV caches rather than raw hidden states to avoid redundant recomputation by successive agents (from "Latent Collaboration in Multi-Agent Systems")
6. Under the Linear Representation Hypothesis, expressing m latent thoughts losslessly via text requires at least Ω(dh·m / log|V|) tokens, making latent generation O(dh/log|V|) times more efficient (from "Latent Collaboration in Multi-Agent Systems")
7. In LatentMAS, reasoning unfolds by auto-regressively appending last-layer hidden representations as next-step input embeddings, replacing standard token decoding entirely (from "Latent Collaboration in Multi-Agent Systems")
8. LatentMAS is architecture-agnostic and can be applied to sequential, hierarchical, or other MAS designs without modification (from "Latent Collaboration in Multi-Agent Systems")
9. Latent expressiveness scales linearly with hidden dimension dh, meaning larger models inherently have greater latent reasoning capacity (from "Latent Collaboration in Multi-Agent Systems")
10. The alignment matrix Wa is computed once per run and reused across all inference steps, making its computational overhead negligible (from "Latent Collaboration in Multi-Agent Systems")
11. LatentMAS provides 4x-4.3x faster end-to-end inference than text-based MAS (from "Latent Collaboration in Multi-Agent Systems")
12. LatentMAS is a training-free framework that enables pure latent collaboration among LLM agents through continuous latent space communication (from "Latent Collaboration in Multi-Agent Systems")
13. LatentMAS achieves up to 14.6% higher accuracy than baselines across 9 benchmarks without any additional training (from "Latent Collaboration in Multi-Agent Systems")
14. Natural language serves as the lingua franca in existing LLM-based MAS, carrying agents' internal thoughts and enabling cross-agent communication (from "Latent Collaboration in Multi-Agent Systems")
15. Latent working memory transfer guarantees information fidelity equivalent to explicit input exchange — agent outputs conditioned on latent working memory are equivalent to outputs obtained by directly (from "Latent Collaboration in Multi-Agent Systems")

## Relationships

## Limitations and Open Questions

## Sources
