---
type: entity
title: Gemma 3
entity_type: entity
theme_ids:
- generative_media
- long_context_and_attention
- model_architecture
- multimodal_models
- policy_optimization
- pretraining_and_scaling
- pretraining_data
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
- unified_multimodal_models
- video_and_world_models
- vision_language_action_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 8.857527757317327e-05
staleness: 0.0
status: active
tags: []
---
# Gemma 3

> Gemma 3 is Google DeepMind's family of open decoder-only language models — spanning sizes from 270M to 4B+ parameters — that serves as the parameter initialization source for T5Gemma 2. Its significance in recent research lies less in direct deployment and more in its role as a foundation: the T5Gemma adaptation recipe transforms Gemma 3's decoder-only checkpoints into encoder-decoder architectures capable of multimodal and long-context processing, with post-training results that consistently surpass the Gemma 3 baseline despite only lightweight finetuning.

**Type:** entity
**Themes:** [[themes/model_architecture|model_architecture]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/multimodal_models|multimodal_models]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/unified_multimodal_models|unified_multimodal_models]]

## Overview

Gemma 3 is a family of decoder-only transformer models from Google DeepMind, covering text-only variants at 270M and 1B parameters, and multimodal variants at larger scales (4B+). The smaller text-only models have limited context windows, but this has not prevented their use as initialisation points for architecturally more capable successors.

The primary research significance documented in the knowledge base concerns Gemma 3's role in the T5Gemma 2 work, which adapts Gemma 3 decoder-only checkpoints into encoder-decoder models using the UL2 pretraining objective. This adaptation is non-trivial: the decoder must be restructured to include a cross-attention mechanism alongside its self-attention layers, and the architectural gap between the two must be carefully managed. The introduction of *merged attention* — which unifies decoder self-attention and cross-attention into a single module with shared parameters — explicitly serves to narrow the structural distance between the T5Gemma 2 decoder and the Gemma 3 decoder, making parameter initialisation from the original checkpoint cleaner and more effective.

## Architecture as a Constraint and Enabler

Gemma 3's decoder-only design imposes certain constraints on the adaptation process. Because the 270M and 1B variants are text-only and context-limited, T5Gemma 2 must genuinely *extend* them rather than merely fine-tune them — the multimodal and long-context capabilities are emergent properties of the encoder-decoder architecture, not transfers from the base model. This is evidenced by the finding that T5Gemma 2, even when built from these constrained base models, successfully gains multimodal capability and achieves long-context performance up to 128K context length despite pretraining on sequences of only 16K tokens.

This pattern has a notable implication: the encoder-decoder architecture confers structural advantages — bidirectional encoder attention for input understanding, cross-attention for attending to high-level representations, and a dedicated pathway for visual tokens — that a decoder-only model cannot access regardless of scale. Gemma 3 is, in this framing, a strong initialisation rather than a ceiling.

## Post-Training Comparisons

A recurring finding is that T5Gemma 2, after post-training via distillation (no reinforcement learning), generally surpasses its Gemma 3 counterparts on benchmark performance. This holds across the model size range, and the gap is attributed not to more data or stronger training signals but to the encoder-decoder architecture's structural advantages for reasoning over long inputs. Tying all word embeddings across encoder and decoder — reducing embedding parameters by ~10.5% with negligible quality cost — is one design choice that reflects the redundancy already present in Gemma 3's original embedding space.

## Open Questions and Limitations

The evidence here is almost entirely mediated through the T5Gemma 2 lens, so direct analysis of Gemma 3's standalone capabilities, limitations, or failure modes is not well-represented in the knowledge base. Key open questions include:

- **How much of the post-training gap is architectural vs. training recipe?** T5Gemma 2 uses a specialised UL2 multi-task objective; it is unclear how much of the advantage over Gemma 3 comes from the encoder-decoder structure versus the pretraining curriculum.
- **Do the adaptation findings generalise beyond Gemma 3?** The T5Gemma 2 paper frames the recipe as generalising across modalities, but it remains anchored to the Gemma 3 checkpoint family. Whether other decoder-only families (e.g., Llama-class models) would benefit equivalently is not addressed.
- **Robustness of the text-only base for multimodal adaptation.** The 270M and 1B Gemma 3 models are text-only, yet multimodal capability is recovered post-adaptation. It is not documented whether the quality gap relative to adaptation from natively multimodal base models is significant.

## Relationships

Gemma 3 is the direct predecessor and parameter source for T5Gemma 2, which extends it into a multimodal encoder-decoder model. EmbeddingGemma further leverages T5Gemma 2 checkpoints (themselves derived from Gemma 3) for state-of-the-art text retrieval. The architectural choices made in adapting Gemma 3 — merged attention, RoPE base frequency tuning, embedding tying — reflect broader tensions explored across [[themes/model_architecture|model_architecture]] and [[themes/long_context_and_attention|long_context_and_attention]] themes. The use of a frozen 400M SigLIP encoder alongside Gemma 3-derived decoder weights connects to developments in [[themes/multimodal_models|multimodal_models]] and [[themes/unified_multimodal_models|unified_multimodal_models]].

## Key Findings

## Limitations and Open Questions

## Sources
