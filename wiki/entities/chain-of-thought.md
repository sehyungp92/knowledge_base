---
type: entity
title: Chain-of-Thought
entity_type: method
theme_ids:
- adaptive_computation
- agent_self_evolution
- agent_systems
- ai_for_scientific_discovery
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- in_context_and_meta_learning
- knowledge_and_memory
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- multi_agent_coordination
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- scaling_laws
- scientific_and_medical_ai
- search_and_tree_reasoning
- software_engineering_agents
- test_time_compute_scaling
- test_time_learning
- tool_use_and_agent_protocols
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 12
sources_since_update: 0
update_count: 1
influence_score: 0.008319290562251645
staleness: 0.0
status: active
tags: []
---
# Chain-of-Thought

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/agent_self_evolution|agent_self_evolution]], [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/scaling_laws|scaling_laws]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

An extended reasoning trace produced by a language model before giving a final answer. In o1, the chain of thought is hidden and trained via RL.

## Key Findings

1. VeriFree bypasses answer verification and instead uses RL to directly maximize the probability of generating the reference answer. (from "Reinforcing General Reasoning without Verifiers")
2. ProRL training ran on 4 nodes of 8x NVIDIA H100-80GB GPUs for approximately 16K GPU hours (from "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models")
3. HRM with 27M parameters and ~1000 training examples achieves 40.3% accuracy on ARC-AGI-1, surpassing o3-mini-high (34.5%) and Claude 3.7 8K context (21.2%). (from "Hierarchical Reasoning Model")
4. HRM executes sequential reasoning tasks in a single forward pass without explicit supervision of the intermediate process. (from "Hierarchical Reasoning Model")
5. In RLVR, a rule-based program assigns a reward of 1 if the final answer is correct and 0 otherwise. (from "Reinforcing General Reasoning without Verifiers")
6. HRM operates without pre-training or CoT data, using only input-output pairs and randomly initialized weights. (from "Hierarchical Reasoning Model")
7. Nemotron-Research-Reasoning-Qwen-1.5B was trained on a diverse, verifiable dataset of 136K problems across five domains (from "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models")
8. HRM features two coupled recurrent modules: a high-level module for abstract deliberate reasoning and a low-level module for fast detailed computations, inspired by hierarchical processing in the brai (from "Hierarchical Reasoning Model")
9. RLVR methodology is limited to tasks where rule-based answer verification is possible and does not naturally extend to real-world domains such as chemistry, healthcare, engineering, law, biology, busi (from "Reinforcing General Reasoning without Verifiers")
10. LLMs have five fundamental limitations that persist even under scaling: hallucination, context compression, reasoning degradation, retrieval fragility, and multimodal misalignment. (from "On the Fundamental Limits of LLMs at Scale")
11. In VeriFree, the likelihood of the reference answer conditioned on the question and generated reasoning trace serves both as a reward signal for policy gradients and as a weighting term for supervised (from "Reinforcing General Reasoning without Verifiers")
12. In R1-Zero-style RL, the model is trained using GRPO, a simplified variant of PPO. (from "Reinforcing General Reasoning without Verifiers")
13. TRM with self-attention and 7M parameters outperforms HRM with 27M parameters on all tested benchmarks, achieving 85.3% vs 74.5% on Maze-Hard, 44.6% vs 40.3% on ARC-AGI-1, and 7.8% vs 5.0% on ARC-AGI- (from "Less is More: Recursive Reasoning with Tiny Networks")
14. For any computably enumerable set of LLMs, there exists a computable ground-truth function such that every model hallucinates on at least one input, making hallucination-free LLMs mathematically impos (from "On the Fundamental Limits of LLMs at Scale")
15. TextGrad improves GPT-4o's zero-shot code accuracy on LEETCODE-HARD from 26% to 36%, raises MMLU-Physics performance from 91.2% to 95.1%, and enhances the multi-tool agent CHAMELEON by 7.7% (from "Adaptation of Agentic AI")

## Capabilities

- LLMs can reason through chain-of-thought, functioning as universal computers by appending tokens into their own context to execute arbitrary algorithms before outputting a final result (maturity: broad_production)
- Large Reasoning Models (LRMs) with extended chain-of-thought demonstrate superior performance over standard LLMs on medium-complexity planning and reasoning tasks, showing measurable advantage when co (maturity: narrow_production)
- Reasoning-enhanced VLA with trajectory chain-of-thought significantly improves out-of-distribution performance requiring simultaneous instruction, visual, and action generalization (maturity: demo)
- Latent thought models can perform chain-of-thought reasoning in a latent space Z (rather than the observed text space X), and this consistently outperforms raw-text-space CoT at inference time on math (maturity: research_only)
- Multimodal LLMs can reason about physical common sense (space, time, fundamental physics) from video input using long chain-of-thought, achieving scores competitive with or exceeding OpenAI o1 on stru (maturity: demo)

## Known Limitations

- No extended thinking / chain-of-thought reasoning: Kimi K2 is explicitly a 'reflex-grade model without long thinking', lacking the test-time compute scaling that thinking models provide (severity: significant, trajectory: improving)
- Quality of reasoning traces (thinking process) is not measured — only final answer accuracy — leaving the validity of chain-of-thought supervision signal empirically unverified (severity: minor, trajectory: unclear)
- TTT applied to chain-of-thought reasoning traces is explicitly left unexplored, leaving open whether TTT could compound gains from intermediate reasoning steps. (severity: minor, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
