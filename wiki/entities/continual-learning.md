---
type: entity
title: Continual learning
entity_type: method
theme_ids:
- agent_self_evolution
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- computer_use_and_gui_agents
- continual_learning
- finetuning_and_distillation
- frontier_lab_competition
- hallucination_and_reliability
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reinforcement_learning
- rl_for_llm_reasoning
- scaling_laws
- software_engineering_agents
- transformer_alternatives
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0025552185067138937
staleness: 0.0
status: active
tags: []
---
# Continual learning

> Continual learning is the capacity for an AI model to acquire and retain new knowledge from ongoing experience without forgetting what it previously learned. It represents one of the most significant gaps between current AI systems and biological intelligence, and its absence is a defining constraint on how deployed agents can adapt, personalize, and remain useful over time.

**Type:** method
**Themes:** [[themes/continual_learning|Continual Learning]], [[themes/model_architecture|Model Architecture]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]], [[themes/agent_self_evolution|Agent Self-Evolution]], [[themes/agent_systems|Agent Systems]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/transformer_alternatives|Transformer Alternatives]], [[themes/alignment_and_safety|Alignment & Safety]], [[themes/hallucination_and_reliability|Hallucination & Reliability]], [[themes/scaling_laws|Scaling Laws]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/computer_use_and_gui_agents|Computer Use & GUI Agents]], [[themes/vertical_ai_and_saas_disruption|Vertical AI & SaaS Disruption]], [[themes/ai_business_and_economics|AI Business & Economics]], [[themes/ai_governance|AI Governance]], [[themes/ai_market_dynamics|AI Market Dynamics]]

## Overview

Current AI systems are stateless learners. As Andrej Karpathy has noted, agents cannot persistently retain new information told to them in deployment: "They don't have continual learning. You can't just tell them something and they'll remember it." This is not a minor inconvenience but a structural limitation on what deployed AI can do. Every conversation begins from the same frozen weights. The model cannot accumulate domain expertise from the users it serves, cannot update its beliefs when corrected, and cannot carry forward lessons learned from previous errors.

Continual learning is the proposed remedy: a mechanism by which models update from ongoing deployment experience in a self-directed way, analogous to how a specialist's expertise deepens through practice rather than through repeated retraining from scratch. The ambition is not just memory augmentation (storing facts externally and retrieving them) but genuine weight-level adaptation that does not degrade prior knowledge.

## Research Progress

Several research frameworks have made recent inroads. The **Hope** framework combines a self-modifying sequence model with a Continuum Memory System (CMS), demonstrating improved performance on language modeling, knowledge incorporation, and few-shot generalization. The CMS component specifically targets class-incremental text classification, outperforming established baselines including EWC, InCA, and vanilla in-context learning on standard benchmarks (CLINC, Banking, DBpedia) using Llama-3 base models.

The **Nested Learning** framework offers a more conceptually ambitious reframing: pretraining, in-context learning, and continual learning are not separate mechanisms but instances of the same underlying process, learning to compress and reuse context at different levels of timescale. This unification suggests that the boundary between "training" and "inference" is less fundamental than commonly assumed, and that continual adaptation may be a natural extension of capabilities already latent in large models.

Despite these advances, all current results remain at the `research_only` maturity level. Demonstrations are on controlled benchmarks, not open-ended real-world deployment.

## Architectural Constraints

The challenge of continual learning is inseparable from architectural choices in how models process and store information. The Transformer's KV cache scales with sequence length, making long-context deployment on edge devices memory-prohibitive and ruling out naive approaches where context length serves as a proxy for memory. Hybrid architectures like Zamba (Mamba + attention) were partly motivated by this constraint: Mamba's fixed-size hidden state means memory does not grow with sequence length, theoretically enabling arbitrarily long sequences at constant memory cost. In principle, a recurrent hidden state is a natural home for continually updated knowledge. In practice, the hidden state is discarded between sessions, and training the state to persist useful information across non-stationary distributions remains unsolved.

The optimizer state is another under-recognized casualty. In continual learning settings, the momentum accumulated during pretraining encodes knowledge about the loss landscape geometry. When training is resumed without recovering this momentum, the model loses that geometry and must relearn it, compounding the catastrophic forgetting problem. Standard momentum acts as a low-pass filter over gradient updates and cannot selectively retrieve historically relevant gradient subspace information needed for stable adaptation.

## Open Questions and Limitations

The core unsolved problem is catastrophic forgetting: gradient updates that improve performance on new data tend to overwrite weights that supported performance on old data. Existing approaches beyond in-context learning are either computationally expensive, require external memory components, lack generalization, or fail to suppress forgetting reliably. There is no current method that achieves the full combination of: lightweight, parameter-efficient, generalizing well across distribution shifts, and preserving prior knowledge without replay.

Hope's benchmark results are also limited in scope. The evaluations focus on specific empirically-studied task types, and generalization to arbitrary non-stationary streams or real-world deployment conditions remains unverified. This is a persistent gap between academic continual learning benchmarks and the conditions under which deployed AI systems actually operate.

There is also a credit assignment problem adjacent to this space: process-based supervision in reinforcement learning raises the question of how to assign partial credit to intermediate steps in an automated way. As Karpathy noted, "If you're doing process supervision, how do you assign in an automatable way, a partial credit assignment? It's not obvious how you do it." Continual learning under RL raises an even sharper version of this problem since the reward signal itself may shift as the deployment environment changes.

Adversarial fragility in RL reward models compounds this further. LLM judges used as reward functions are vulnerable to adversarial examples that yield maximum reward for nonsensical outputs, meaning that a system that continually fine-tunes against such a signal could silently degrade.

## Connections and Implications

Continual learning is a prerequisite for several high-value downstream capabilities. Personalized agents that adapt to user style and preferences, enterprise systems that absorb proprietary domain knowledge through use rather than through expensive fine-tuning runs, and autonomous agents that improve their task-specific skills over long deployment horizons all depend on solving this problem. Without it, the gap between AI as a static tool and AI as a genuinely adaptive collaborator remains unbridged.

The relationship to [[themes/agent_self_evolution|agent self-evolution]] is direct: an agent that can learn from its own deployment trajectory is the minimal version of a self-improving system, and it is notable that we do not yet have even this. The relationship to [[themes/transformer_alternatives|transformer alternatives]] is structural: recurrent architectures like Mamba have properties (fixed-size state, no positional encodings in Zamba's implementation) that make them plausible hosts for continual state updates in ways that KV-cache-based Transformers are not. The relationship to [[themes/finetuning_and_distillation|finetuning and distillation]] is methodological: continual learning can be understood as an extreme of continual fine-tuning, and the pathologies that afflict catastrophic forgetting in fine-tuning are the same ones that block continual learning at deployment time.

## Sources

- Andrej Karpathy — "We're summoning ghosts, not building animals"
- Training Zamba: A Hybrid Model Master Class with Zyphra's Quentin Anthony
- Thoughts on AI Progress (Dec 2025)
- Why I don't think AGI is right around the corner
- Ilya Sutskever – We're moving from the age of scaling to the age of research

## Key Findings

## Limitations and Open Questions

## Relationships
