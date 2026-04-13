---
type: entity
title: Qwen3
entity_type: entity
theme_ids:
- adaptive_computation
- agent_memory_systems
- agent_systems
- chain_of_thought
- finetuning_and_distillation
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 10
sources_since_update: 0
update_count: 1
influence_score: 0.0028535172467747355
staleness: 0.0
status: active
tags: []
---
# Qwen3

**Type:** entity
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vision_language_models|vision_language_models]]

## Overview

A family of language models from Qwen, used in this paper across sizes 0.6B, 1.7B, 4B, and 8B to study SDPO's scaling properties. Qwen3-8B is the primary model for LCBv6 experiments.

## Key Findings

1. LatentMAS transfers working memory as KV caches rather than raw hidden states to avoid redundant recomputation by successive agents (from "Latent Collaboration in Multi-Agent Systems")
2. LatentMAS latent working memory is defined as layer-wise KV caches from all transformer layers, capturing both input context and newly generated latent thoughts — unlike prior cache-sharing methods th (from "Latent Collaboration in Multi-Agent Systems")
3. In LatentMAS, reasoning unfolds by auto-regressively appending last-layer hidden representations as next-step input embeddings, replacing standard token decoding entirely (from "Latent Collaboration in Multi-Agent Systems")
4. Cross-agent information transfer in LatentMAS is performed by layer-wise KV cache concatenation, so each successive agent's generation is conditioned on both the predecessor's working memory and its o (from "Latent Collaboration in Multi-Agent Systems")
5. Existing LLM-based multi-agent systems depend on text-based mediation for both reasoning and communication between agents (from "Latent Collaboration in Multi-Agent Systems")
6. Under the Linear Representation Hypothesis, expressing m latent thoughts losslessly via text requires at least Ω(dh·m / log|V|) tokens, making latent generation O(dh/log|V|) times more efficient (from "Latent Collaboration in Multi-Agent Systems")
7. LatentMAS achieves up to 14.6% higher accuracy than baselines across 9 benchmarks without any additional training (from "Latent Collaboration in Multi-Agent Systems")
8. LatentMAS provides 4x-4.3x faster end-to-end inference than text-based MAS (from "Latent Collaboration in Multi-Agent Systems")
9. The alignment matrix Wa is computed once per run and reused across all inference steps, making its computational overhead negligible (from "Latent Collaboration in Multi-Agent Systems")
10. Latent expressiveness scales linearly with hidden dimension dh, meaning larger models inherently have greater latent reasoning capacity (from "Latent Collaboration in Multi-Agent Systems")
11. LatentMAS is architecture-agnostic and can be applied to sequential, hierarchical, or other MAS designs without modification (from "Latent Collaboration in Multi-Agent Systems")
12. LatentMAS is a training-free framework that enables pure latent collaboration among LLM agents through continuous latent space communication (from "Latent Collaboration in Multi-Agent Systems")
13. LatentMAS reduces output token usage by 70.8%-83.7% compared to text-based MAS (from "Latent Collaboration in Multi-Agent Systems")
14. Natural language serves as the lingua franca in existing LLM-based MAS, carrying agents' internal thoughts and enabling cross-agent communication (from "Latent Collaboration in Multi-Agent Systems")
15. Latent working memory transfer guarantees information fidelity equivalent to explicit input exchange — agent outputs conditioned on latent working memory are equivalent to outputs obtained by directly (from "Latent Collaboration in Multi-Agent Systems")

## Capabilities

- Highest tool calling success rate among frontier models at 90.6%, outperforming Claude-4-Sonnet (89.5%), Kimi-K2 (86.2%), and Qwen3-Coder (77.1%) across 52 standardized agentic coding tasks (maturity: narrow_production)
- LLM-driven evolutionary pipeline for CUDA kernel optimization achieves up to 12.52x speedup over PyTorch native and 24.87x over torch.compile (MNIST CrossEntropy forward on H100), consistently outperf (maturity: demo)

## Known Limitations

- Baseline frontier models (Claude, o3, Kevin-32B, Qwen3-32B) frequently fail to produce valid kernels at all — many benchmark cells are empty dashes — revealing that single-pass LLM CUDA generation is  (severity: significant, trajectory: improving)

## Relationships

## Limitations and Open Questions

## Sources
