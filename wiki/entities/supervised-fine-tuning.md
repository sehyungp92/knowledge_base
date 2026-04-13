---
type: entity
title: Supervised Fine-Tuning
entity_type: method
theme_ids:
- agent_systems
- ai_market_dynamics
- alignment_and_safety
- alignment_methods
- benchmark_design
- chain_of_thought
- context_engineering
- continual_learning
- evaluation_and_benchmarks
- finetuning_and_distillation
- frontier_lab_competition
- in_context_and_meta_learning
- knowledge_and_memory
- medical_and_biology_ai
- multi_agent_coordination
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scientific_and_medical_ai
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- synthetic_data_generation
- tool_use_and_agent_protocols
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
influence_score: 0.00848011472333666
staleness: 0.0
status: active
tags: []
---
# Supervised Fine-Tuning

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/alignment_methods|alignment_methods]], [[themes/benchmark_design|benchmark_design]], [[themes/chain_of_thought|chain_of_thought]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]], [[themes/vision_language_models|vision_language_models]]

## Overview

A training stage (as in InstructGPT ~2022) where LLMs are fine-tuned on curated instruction-following examples. Considered a 'thin/short' stage computationally compared to RLVR.

## Key Findings

1. AMIE was evaluated against 19 board-certified PCPs with a median post-residency experience of 6 years (IQR 3.5–11.5 years) (from "2025-5-6")
2. The mechanistic account of why larger KL shifts on the new task disrupt prior knowledge remains unknown (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")
3. The codebase and specific prompts for multimodal AMIE are not being open-sourced due to safety implications associated with unmonitored deployment of AI systems in medical contexts. (from "2025-5-6")
4. The OSCE study used 105 scenarios across three modality types (35 skin photos, 35 ECGs, 35 clinical documents), evaluated by 18 specialist physicians with each consultation reviewed by 3 independent s (from "2025-5-6")
5. Off-policy RL algorithms were not studied, leaving their forgetting behavior relative to on-policy methods an open question (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")
6. Forward KL divergence (R²=0.96) outperforms all alternative metrics as a predictor of forgetting, including reverse KL (0.93), Total Variation (0.80), L2 distributional distance (0.56), and weight-cha (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")
7. RL experiments used GRPO with only a binary success reward and no explicit KL regularization term (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")
8. AMIE remains a research system not intended for clinical use and requires further real-world validation before clinical translation. (from "2025-5-6")
9. The KL-forgetting link's behavior at frontier-scale models and in more diverse generative domains remains unknown (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")
10. AMIE implements a three-phase state-aware dialogue framework: (1) History Taking, (2) Diagnosis & Management, and (3) Answer Follow-up Questions, with automatic phase transitions driven by intermediat (from "2025-5-6")
11. The author coined the term 'vibe coding' in a tweet and was surprised by how widely it spread. (from "2025 LLM Year in Review")
12. The T2 paradigm represents a conceptual inversion: rather than adapting the agent to use tools better, it adapts tools to better serve a fixed frozen agent, reframing the foundation model from optimiz (from "Adaptation of Agentic AI")
13. The dominant multimodal reasoning paradigm ('Thinking about Images') treats the visual modality as a static, initial context while conducting all reasoning exclusively in the textual domain. (from "Thinking with Images for Multimodal Reasoning: Foundations, Methods, and Future Frontiers")
14. The T2 approach (s3) achieves 58.9% average accuracy with only 2,400 training samples by training a lightweight 7B searcher subagent using frozen-generator feedback. (from "Adaptation of Agentic AI")
15. Sparse weight updates attributed to RL were an artifact of bfloat16 numerical precision, not a fundamental property of on-policy training (from "RL's Razor: Why Online Reinforcement Learning Forgets Less")

## Known Limitations

- Domain-specific supervised fine-tuning of foundation models for medical tasks causes catastrophic forgetting, degrading performance on other critical consultation aspects (e.g., management plan approp (severity: significant, trajectory: stable)
- Supervised fine-tuning (SFT) on small domain-specific medical datasets degrades conversational quality and management plan appropriateness, particularly for dermatology and ECG tasks — making SFT coun (severity: significant, trajectory: stable)

## Relationships

## Limitations and Open Questions

## Sources
