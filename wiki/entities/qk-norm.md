---
type: entity
title: QK-Norm
entity_type: method
theme_ids:
- adaptive_computation
- agent_systems
- ai_market_dynamics
- code_and_software_ai
- code_generation
- finetuning_and_distillation
- frontier_lab_competition
- generative_media
- image_generation_models
- long_context_and_attention
- model_architecture
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- software_engineering_agents
- test_time_compute_scaling
- unified_multimodal_models
- video_and_world_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0010748530739423698
staleness: 0.0
status: active
tags: []
---
# QK-Norm

QK-Norm is a normalization technique applied to query and key vectors within attention mechanisms, designed to stabilize attention logit magnitudes during training. It has become a standard stabilization tool in large-scale transformer training — most notably adopted by Gemma 2 and carried forward into T5Gemma 2 — but its apparent simplicity belies an important constraint: its portability across attention architectures is not guaranteed, exposing a deeper tension between training stability solutions and novel efficiency-oriented attention designs.

**Type:** method
**Themes:** [[themes/model_architecture|Model Architecture]], [[themes/long_context_and_attention|Long Context & Attention]], [[themes/pretraining_and_scaling|Pretraining & Scaling]], [[themes/finetuning_and_distillation|Finetuning & Distillation]], [[themes/multimodal_models|Multimodal Models]], [[themes/unified_multimodal_models|Unified Multimodal Models]]

---

## Overview

At its core, QK-Norm applies layer normalization (or a similar normalization operation) to the query and key projections before computing attention scores. This constrains the scale of the dot-product logits, preventing attention entropy collapse or explosion — a known failure mode in deep transformers trained at scale, where unnormalized attention weights can saturate or diffuse catastrophically.

The technique was adopted by Gemma 2 as part of its architecture, and T5Gemma 2 inherits it through its initialization from pretrained Gemma 3 decoder-only checkpoints. In the T5Gemma 2 context, QK-Norm operates within a hybrid local/global attention design where RoPE base frequencies are set to 10k and 1M for local and global attention layers respectively — an environment where logit stability is especially important given the extreme frequency differences across attention types. The broader T5Gemma 2 architecture also employs merged attention (unifying decoder self-attention and cross-attention into a single module with shared parameters), tying all word embeddings to reduce redundancy, and using a frozen 400M SigLIP encoder for vision. QK-Norm sits within this carefully engineered stack as a stability primitive that enables the rest of the architecture to function reliably through adaptation from decoder-only to encoder-decoder form.

---

## Key Findings

QK-Norm's role in T5Gemma 2 is best understood against the background of what the T5Gemma 2 paper demonstrates about adaptation stability. Adapting a pretrained decoder-only Gemma 3 model into an encoder-decoder via UL2 is a parameter-efficient operation, and the quality of that initialization depends heavily on how closely the decoder architecture in the adapted model mirrors the original. Merged attention is explicitly described as narrowing the architectural gap to ease parameter initialization from the Gemma 3 checkpoint — and QK-Norm, inherited through this process, is part of the stable operational baseline that the adapted model preserves rather than discards.

The broader context suggests QK-Norm is a low-cost, high-reliability technique: embedding tying eliminates ~10.5% of parameters with essentially no quality drop, and merged attention saves 6.5% of parameters at a cost of only ~0.3 average quality points. These ablations collectively paint a picture of an architecture where stability primitives like QK-Norm are retained because the marginal cost of removing them outweighs any simplification benefit.

Notably, T5Gemma 2 pretraining on ~2T tokens with 16K sequence lengths, followed by post-training that surpasses Gemma 3 counterparts despite only lightweight finetuning (distillation-free UL2), suggests that the inherited architectural features — including QK-Norm — are sufficient for the training regime without needing significant modification.

---

## Known Limitations

The critical limitation of QK-Norm is its **incompatibility with Multi-head Latent Attention (MLA)**, the attention variant used in DeepSeek models and increasingly explored for its KV-cache efficiency gains. MLA compresses key-value pairs through low-rank projections, decoupling the key structure from the standard per-head layout that QK-Norm assumes. This means QK-Norm cannot be straightforwardly applied in MLA contexts, and alternative stabilization approaches must be engineered per-architecture rather than ported wholesale.

This is classified as a **minor** limitation in severity — training instability can often be addressed through other means (learning rate schedules, gradient clipping, architectural alternatives) — but its trajectory is **unclear**. As MLA-style architectures gain traction for KV-cache efficiency at inference time, the absence of a portable equivalent to QK-Norm for these designs represents a subtle but real engineering burden. Each new attention variant that departs from the standard multi-head structure must rediscover or reinvent stability mechanisms from scratch, fragmenting what might otherwise be a shared toolkit.

This tension reflects a broader pattern in attention architecture research: the techniques developed for training stability (QK-Norm, RoPE, grouped-query attention) were largely co-evolved with standard multi-head attention, and as the field moves toward efficiency-oriented variants (MLA, linear attention, sparse attention), the portability of these primitives becomes an open question rather than an assumption.

---

## Relationships

QK-Norm is most directly associated with [[themes/long_context_and_attention|Long Context & Attention]] research and [[themes/model_architecture|Model Architecture]] decisions. Its use in T5Gemma 2 connects it to [[themes/multimodal_models|Multimodal Models]] and [[themes/finetuning_and_distillation|Finetuning & Distillation]] through the encoder-decoder adaptation pipeline. Its incompatibility with MLA places it in tension with efficiency-driven architecture work appearing in models from GLM-4.5, Qwen3, and others exploring compressed attention representations. The technique also appears contextually in Emerging Properties in Unified Multimodal Pretraining and the Qwen3 Technical Report as part of the broader landscape of stabilization choices made at scale.

## Limitations and Open Questions

## Sources
