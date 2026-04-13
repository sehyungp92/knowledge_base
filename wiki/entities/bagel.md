---
type: entity
title: Bagel
entity_type: entity
theme_ids:
- chain_of_thought
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0010834075747538795
staleness: 0.0
status: active
tags: []
---
# Bagel

> Bagel (also stylized BAGEL) is an open-source unified multimodal foundation model with 7B active parameters (14B total), built on a Mixture-of-Transformers architecture initialized from Qwen2.5. It serves as the base model for ThinkMorph and represents a significant contribution to the field of joint image understanding and generation, pretrained on large-scale interleaved visual-text data to provide raw visual manipulation capabilities.

**Type:** entity
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/multimodal_models|multimodal_models]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/pretraining_data|pretraining_data]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/unified_multimodal_models|unified_multimodal_models]], [[themes/video_and_world_models|video_and_world_models]], [[themes/vision_language_models|vision_language_models]]

## Overview

BAGEL (Scalable Generative Cognitive Model) is an open-source multimodal foundation model designed for both visual understanding and generation within a single unified architecture. With 7B active parameters out of 14B total, it employs a Mixture-of-Transformers design initialized from the Qwen2.5 LLM backbone, trained on large-scale interleaved visual-text corpora. Its architecture is deliberately structured to support joint reasoning over image and text streams — a prerequisite for the kind of interleaved chain-of-thought that [[themes/unified_multimodal_models|unified multimodal]] fine-tuning approaches like ThinkMorph depend on.

Bagel-7B occupies a specific and important niche: it is a *base* model — strong on raw visual manipulation capabilities, but not yet directed toward structured reasoning. This makes it an instructive reference point for measuring what [[themes/post_training_methods|post-training]] can achieve, and equally, what the base pretraining alone cannot.

## Key Findings

The most revealing picture of Bagel-7B emerges from the ThinkMorph fine-tuning study (see ThinkMorph: Emergent Properties in Multimodal Interleaved Chain-of-Thought Reasoning). ThinkMorph, fine-tuned on approximately 24K interleaved reasoning traces built on top of Bagel, achieves an average gain of **20.74% over Bagel-7B across nine diverse tasks** in the full benchmark comparison. The gains are not uniform — they are concentrated precisely in vision-centric tasks where the base model struggles most acutely. On Spatial Navigation, Bagel-7B nearly fails outright at 0.83%, while interleaved reasoning lifts the fine-tuned model to 86.67% — a 85.84-point swing that signals the base model's pretraining, however strong, does not automatically confer structured spatial reasoning. Jigsaw Assembly tells a similar story, with a 38.75% in-domain improvement over the base.

These results frame Bagel-7B's limitation clearly: **raw visual pretraining provides a capable substrate, but not a reasoning architecture**. The visual manipulation capabilities are present; the ability to direct them through structured intermediate steps is not. This is consistent with the broader pattern in [[themes/pretraining_and_scaling|pretraining and scaling]] research — scale and data diversity build capability headroom, but task-aligned fine-tuning is still required to surface it.

Across a broader nine-task benchmark sweep, ThinkMorph's average 34.74% improvement over the base on vision-centric benchmarks quantifies this gap. Notably, ThinkMorph (7B) built on Bagel surpasses Qwen2.5-VL-72B — a model more than 10x larger — by 34% on VSP and 10.67% on BLINK-J. This efficiency gain is partly attributable to the quality of Bagel's foundation: a weaker base would not permit such gains from small-data fine-tuning alone.

From the Emerging Properties in Unified Multimodal Pretraining paper, the architectural specifics confirm BAGEL as a deliberate design choice rather than an ad-hoc combination: the Mixture-of-Transformers structure enables parameter efficiency (7B active from 14B total) while maintaining the interleaved processing capability essential for downstream interleaved [[themes/chain_of_thought|chain-of-thought]] training.

## Limitations and Open Questions

The ThinkMorph benchmark results, while flattering to Bagel as a foundation, also expose its ceiling without fine-tuning. The near-zero performance on spatial navigation tasks suggests that certain [[themes/reasoning_and_planning|spatial reasoning]] capabilities are not emergent from pretraining alone — they require explicit training signal. This raises the question of whether Bagel's pretraining data adequately covers the kinds of structured visual tasks needed for genuine multimodal reasoning, or whether such capabilities are fundamentally post-training phenomena regardless of base model quality.

There is also an efficiency question latent in the architecture: the 14B total / 7B active parameter split implies that roughly half the model capacity is inactive at any given forward pass. Whether this MoT design distributes specialization effectively across visual and language modalities — or whether it introduces load imbalance that limits ceiling performance — is not directly addressed in the available sources.

Finally, Bagel-7B's role across multiple concurrent research lines (ThinkMorph, OmniGen2, Show-o2) positions it as a shared experimental substrate. This makes it harder to disentangle which performance characteristics belong to BAGEL itself versus the specific fine-tuning and data curation choices layered on top.

## Relationships

- **ThinkMorph** — the primary downstream fine-tune of Bagel-7B; ThinkMorph's gains over Bagel serve as the main empirical window into the base model's capabilities and gaps
- [[themes/unified_multimodal_models|Unified Multimodal Models]] — Bagel sits at the frontier of joint understanding-and-generation architectures, distinct from decode-only or encode-only multimodal designs
- [[themes/post_training_methods|Post-Training Methods]] — Bagel's trajectory illustrates the leverage that small-scale, high-quality fine-tuning can exert over a strong pretrained base
- [[themes/pretraining_and_scaling|Pretraining and Scaling]] — the Mixture-of-Transformers architecture and large-scale interleaved pretraining regime are central to what Bagel can and cannot do out of the box
- **Qwen2.5** — the LLM backbone from which BAGEL's transformer weights are initialized, creating a lineage dependency on the quality of that underlying language model

## Sources
