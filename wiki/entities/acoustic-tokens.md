---
type: entity
title: Acoustic Tokens
entity_type: method
theme_ids:
- audio_and_speech_models
- model_architecture
- multimodal_models
- pretraining_and_scaling
- unified_multimodal_models
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 5.4337499936595064e-05
staleness: 0.0
status: active
tags: []
---
# Acoustic Tokens

> Acoustic tokens are discrete encodings of fine-grained acoustic details in speech — speaker identity, timbre, prosody — produced via Residual Vector Quantization (RVQ). They serve as the low-level complement to semantic speech tokens, enabling high-fidelity audio reconstruction in modern speech-language models. Their design sits at the intersection of neural audio coding and language modelling, and how they are parameterised has direct consequences for latency, bitrate, and the quality ceiling of real-time spoken dialogue systems.

**Type:** method
**Themes:** [[themes/audio_and_speech_models|audio_and_speech_models]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/unified_multimodal_models|unified_multimodal_models]]

## Overview

Description: Discrete encodings of fine-grained acoustic details in speech, typically produced via RVQ, that retain speaker-specific characteristics like speaker identity and timbre, enabling high-fidelity audio reconstruction.

## Key Findings

### Codec Design and Bitrate Trade-offs

The clearest concrete instantiation of acoustic tokens in the recent literature comes from **Mimi**, the neural audio codec at the heart of Moshi. Mimi uses 8 RVQ quantizers, each with a codebook size of 2048, operating at 12.5 frames per second — yielding a bitrate of 1.1 kbps. This is a deliberately aggressive compression: high enough fidelity to preserve speaker-specific characteristics, low enough bandwidth to be tractable for a language model to generate autoregressively in real time.

Critically, Mimi is fully causal and streaming-capable for both encoding and decoding, with an initial frame size and overall stride of 80ms. This causality constraint is non-trivial — it rules out many standard codec architectures that rely on look-ahead — and it directly sets the floor on theoretical latency. Moshi achieves 160ms theoretical latency (200ms in practice), with the 80ms codec stride being a hard lower bound that cannot be improved without redesigning the tokenizer.

### The Semantic/Acoustic Split

Acoustic tokens deliberately capture *what* makes a voice sound like itself, not *what is being said*. This is the key architectural division exploited by systems like Moshi: a small number of semantic tokens (often distilled from a self-supervised speech model) carry linguistic content, while the remaining RVQ residuals carry acoustic detail. The model can then be trained to generate semantic tokens first — keeping the language modelling task clean — and condition the acoustic token generation on them for reconstruction. This split has implications for how much of the token budget a language model must "spend" on acoustic fidelity versus meaning.

The CSM models from Crossing the Uncanny Valley instantiate a backbone/decoder architecture that reflects this split directly: the backbone (1B–8B parameters) handles the high-level sequence, while a lighter decoder (100M–300M parameters) generates the acoustic token stream. This asymmetry acknowledges that acoustic token generation, while voluminous, is a lower-complexity task than semantic reasoning.

### Scale of Training

The acoustic quality achievable from these tokens is partly a function of how much data the underlying codec and model are trained on. Moshi's pretraining used 7 million hours of audio. Voila's voice tokenizer was trained on 100,000 hours. These are not directly comparable — Moshi's figure covers the full model pretraining dataset, not just the codec — but they indicate the data scale required to produce robust acoustic representations that generalise across speakers, accents, and recording conditions. Voila extends this to multilingual settings, supporting six languages (English, Chinese, French, German, Japanese, Korean), which places additional demands on the acoustic token space to cover cross-lingual phonetic diversity.

## Limitations and Open Questions

The bitrate and frame-rate choices in acoustic tokenization involve hard trade-offs with no universally optimal solution. Lower bitrates ease the language modelling burden but risk losing fine-grained speaker characteristics or introducing artifacts. Higher frame rates improve temporal resolution but multiply the sequence length the model must generate, directly harming latency. The 12.5 Hz / 1.1 kbps operating point used by Mimi is one empirical choice, not a principled optimum.

The 80ms stride lower-bound on latency is a genuine architectural constraint — it cannot be removed without moving to sub-frame or asynchronous generation schemes, neither of which has been demonstrated at scale. Whether acoustic token sequence lengths can be substantially reduced without quality loss (e.g., via better codebook design or hierarchical tokenization) remains an open question.

It is also unclear how well acoustic token representations transfer across recording conditions, emotional register, or paralinguistic signals (laughter, breath, hesitation). Most evaluations focus on objective audio quality metrics or speaker similarity scores; robustness in naturalistic, noisy, or emotionally varied settings is underreported.

## Relationships

Acoustic tokens are closely coupled to Mimi (the specific codec that produces them in the Moshi system) and to [[entities/semantic-tokens|Semantic Tokens]], which handle the complementary linguistic content. The backbone/decoder architectural split seen in CSM models is a direct consequence of the different generative complexity of semantic versus acoustic tokens. Broader context is provided by Residual Vector Quantization, the underlying compression technique.

## Sources
