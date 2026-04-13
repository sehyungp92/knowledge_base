---
type: entity
title: long context
entity_type: method
theme_ids:
- agent_memory_systems
- agent_systems
- ai_business_and_economics
- computer_use_and_gui_agents
- context_engineering
- continual_learning
- finetuning_and_distillation
- knowledge_and_memory
- model_architecture
- post_training_methods
- pretraining_and_scaling
- scaling_laws
- transformer_alternatives
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00046101205854115414
staleness: 0.0
status: active
tags: []
---
# long context

Long context refers to the capability of language models to process very large amounts of information in a single pass — measured in tokens, the atomic units of text a model can attend to simultaneously. As of 2025, frontier models have reached 1M+ token context windows (Claude, Gemini) and 400K tokens (GPT-5), transforming how AI systems can be used for document analysis, agentic memory, and multi-step reasoning. The method sits at a crossroads of architecture, systems engineering, and product design: the ability to hold more context is simultaneously a capability unlock and an engineering bottleneck with sharp cost implications.

**Type:** method
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/computer_use_and_gui_agents|computer_use_and_gui_agents]], [[themes/context_engineering|context_engineering]], [[themes/continual_learning|continual_learning]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/scaling_laws|scaling_laws]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

## Overview

Long context is not a single technique but a design target that different architectures approach very differently — and those differences carry significant practical consequences.

For Transformers, the fundamental challenge is the KV cache: memory grows with sequence length, making dense Transformer deployment on edge devices prohibitive as context scales. Doubling attention heads to support longer sequences in MoE models creates an 83% inference FLOP increase at 128k sequence length, making naive attention head scaling untenable for production agentic applications. This is not a theoretical concern — it is an active constraint on what can be run where.

Mamba-based state space models offer a structurally different tradeoff. The fixed-size hidden state means memory does not grow with sequence length at all, theoretically enabling arbitrarily long sequences with constant memory cost. The Mamba 2 SSD algorithm deepened this by adding structure to the A matrix (which governs state transitions), enabling matrix multiplication operations that leverage GPU tensor cores for faster training and larger effective state sizes. In practice, the Zamba hybrid architecture (six Mamba blocks followed by one globally shared attention + MLP block, repeating with no positional encodings) was built precisely to capture attention's recall quality while keeping Mamba's memory profile — a pragmatic compromise that prioritises deployment viability over architectural purity.

But Mamba's theoretical advantage at long context has a hard engineering ceiling: sequence parallelism for Mamba blocks does not yet exist, which blocks million-token context training. Transformers have mature infrastructure for distributing sequence computation across GPUs; Mamba does not. The gap between "constant memory at inference" and "trainable at million-token context" is currently unbridged.

## The Systems Problem

One underappreciated dimension of long context is that expanding the window does not automatically unlock the use cases it seems to enable. As analysed in Contra Dwarkesh on Continual Learning, the behaviours often described as requiring continual learning — models that accumulate and act on growing contextual knowledge over time — are in fact a systems problem rather than a learning problem. The bottleneck is not that models cannot learn from long context; it is that current tools and interfaces are not set up to accumulate and present that context in the first place. Nobody is giving models the kind of persistent, structured context that would be needed to exhibit continual-learning-like behaviour. The context window exists; the pipelines to fill it usefully do not.

This shifts the locus of innovation. Making the window longer is the architecture problem. Making the window useful is the product and systems engineering problem — and that second problem is currently less well solved.

## Product and Economic Implications

From a product perspective, long context is a capability that grows more valuable as models get cheaper, faster, and smarter — processing a 1M token document costs real money today but may be trivial within a few years. Josh Woodward at Google Labs frames the broader principle: products must be aligned with the trajectory of AI improving, not dependent on AI staying expensive or slow. Long context is a paradigm case — it is expensive now, which means products built around cheap long-context inference are correctly positioned for the curve. Conversely, products that assume long context will always be scarce or slow are misaligned with the trend.

Computer use and GUI agents, which require maintaining state across many steps and screen observations, are one concrete downstream beneficiary. Google Mariner demonstrates both the promise and the present gap: driving a browser via an AI model is now possible in principle, but accuracy and latency are not yet at the threshold for widespread deployment. Long context is a necessary but not sufficient ingredient.

## Open Questions

The central open question is whether constant-memory architectures like Mamba can be trained at million-token context lengths once sequence parallelism is solved — or whether hybrid approaches will always require some attention component to maintain recall quality. A second structural question is whether the product-level infrastructure for accumulating and managing context will develop at the same pace as raw window size. The window expanding without the tools to fill it intelligently is a context engineering problem that remains largely unsolved.

## Relationships

Closely related to [[themes/transformer_alternatives|transformer alternatives]], where Mamba and hybrid architectures like Zamba are the primary contenders. Intersects with [[themes/agent_memory_systems|agent memory systems]] because long context is one implementation strategy for memory — alternatives include retrieval, external stores, and fine-tuning. Connects to [[themes/continual_learning|continual learning]] via the Dwarkesh framing: what looks like a learning limitation is often a context accumulation failure. Relevant to [[themes/ai_business_and_economics|AI business and economics]] because inference cost at long context is a significant factor in which use cases are economically viable and when.

## Key Findings

## Limitations and Open Questions

## Sources
