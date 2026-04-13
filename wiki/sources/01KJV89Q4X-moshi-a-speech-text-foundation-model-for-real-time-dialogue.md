---
type: source
title: 'Moshi: a speech-text foundation model for real-time dialogue'
source_id: 01KJV89Q4XJ3GHGFF55XY78V0D
source_type: paper
authors:
- Alexandre Défossez
- Laurent Mazaré
- Manu Orsini
- Amélie Royer
- Patrick Pérez
- Hervé Jégou
- Edouard Grave
- Neil Zeghidour
published_at: '2024-09-17 00:00:00'
theme_ids:
- audio_and_speech_models
- multimodal_models
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Moshi: a speech-text foundation model for real-time dialogue

Moshi (Défossez et al., 2024) is the first real-time full-duplex spoken large language model, achieving 160ms theoretical and 200ms practical latency by reframing dialogue as a joint speech-to-speech generation problem. It eliminates text as an obligatory intermediate modality, instead jointly modeling two parallel audio streams (model and user) through a hierarchical RQ-Transformer architecture, a causal streaming audio codec (Mimi), and an Inner Monologue mechanism that preserves text-quality reasoning while generating audio in real time.

**Authors:** Alexandre Défossez, Laurent Mazaré, Manu Orsini, Amélie Royer, Patrick Pérez, Hervé Jégou, Edouard Grave, Neil Zeghidour
**Published:** 2024-09-17
**Type:** paper

---

## Motivation

Prior spoken dialogue systems were structurally broken for natural conversation on two axes.

**Latency.** Cascaded pipelines — VAD → ASR → LLM → TTS — compound per-stage delays into several seconds between turns. Natural human response time averages ~230ms across languages. No cascade can approach this.

**Dialogue structure.** All prior systems modeled conversation as a sequence of discrete, non-overlapping speaker turns. This is architecturally incompatible with interruptions, backchanneling ("OK", "I see"), and overlapping speech — which accounts for 10–20% of spoken time in real conversations. The only prior full-duplex attempt (dGSLM) was an offline proof-of-concept lacking text LLM knowledge, modeling only semantic tokens, with no real-time capability.

**Information bottleneck.** Using text as an intermediate modality discards paralinguistic information — emotion, accent, prosody, non-speech sounds — that carries meaning. Speech-only models avoid this but acquire negligible factual knowledge, since structured facts are encoded in text corpora, not audio.

---

## Architecture

### Mimi: causal streaming audio codec

Mimi operates at 12.5Hz and 1.1kbps using 8 RVQ quantizers (codebook size 2048). Its key design decision is a **split RVQ**: a single semantic VQ (first level, distilled from non-causal WavLM via cosine distance loss) runs in parallel with a 7-level acoustic RVQ. Outputs are summed.

This resolves a fundamental conflict: forcing semantic discriminability and acoustic reconstruction through a single residual chain degrades both. The split allows each objective to operate independently. Results: ABX score 6.5% (near ceiling), MUSHRA 81.0.

A secondary finding with significant implications: **adversarial-only training** (removing mel-spectrogram reconstruction loss entirely) dramatically improves perceived quality — MUSHRA 81.0 vs. 58.8 with combined losses. Standard objective metrics (VisQOL) rated the adversarial-only model *worse* (1.84 vs. 3.33), revealing that automated metrics are not reliable proxies for perceptual quality when training objectives change.

Mimi is fully causal with an 80ms frame stride, supporting streaming encoding and decoding.

### RQ-Transformer

The core model is a hierarchical two-level transformer:

- **Temporal Transformer**: 7B parameters, initialized from Helium (a 7B text LLM trained on 2.1T tokens), operates at 12.5Hz frame rate across time
- **Depth Transformer**: 1024-dim, 6 layers, conditions on the temporal representation and autoregressively predicts all 8 RVQ codebook levels within a single timestep using per-codebook (depthwise) linear layers

An **acoustic delay** of 1–2 steps between semantic (first codebook) and acoustic tokens reduces conditional dependencies within a timestep, letting the weaker Depth Transformer approximate the joint distribution more accurately.

### Inner Monologue

At each timestep, the Depth Transformer predicts the following token hierarchy: `text token → semantic token → 7 acoustic tokens`. Text tokens are time-aligned using Whisper word-level timestamps and mapped to the 12.5Hz framerate; ~65% of positions are PAD tokens in conversational English.

The effect is substantial. Without Inner Monologue: NLL 3.65, transcript length 602 chars. With Inner Monologue: NLL 2.77, transcript length 1920 chars. On spoken QA (Web Questions), the gap is 9.2% → 26.6% — a near-tripling of accuracy at the cost of one additional token per timestep (17 vs. 16).

A secondary property: by adjusting a single text-audio delay hyperparameter at inference time, the same trained model operates as:
- Streaming ASR (text generated after audio)
- Streaming TTS (audio generated after text)
- Real-time dialogue (simultaneous)

No architecture, loss, or training data changes required.

### Multi-stream modeling

Two audio token sequences — Moshi and user — are concatenated into the joint RQ-Transformer sequence. During inference, Moshi samples its own stream while treating the user stream as conditioning input. No explicit turn segmentation is used; the model can generate during user speech (producing silence or speech) and process user audio during its own generation.

Training proceeds in four stages:
1. Single-stream unsupervised audio pretraining (7M hours)
2. Simulated multi-stream from diarized single-channel audio
3. Fine-tuning on 2000 hours of Fisher dual-channel telephone conversations
4. Instruction fine-tuning on 20k+ hours of synthetic speech generated by a custom multi-stream TTS conditioned on a single voice actor

---

## Results

| Benchmark | Moshi (Inner Monologue) | Moshi (no IM) | Spectron | SpeechGPT |
|-----------|------------------------|----------------|----------|-----------|
| Web Questions | 26.6% | 9.2% | 6.1% | 6.5% |
| LlaMA Questions | 62.3% | 21.0% | 22.9% | 21.6% |
| Audio TriviaQA | 22.8% | 7.3% | — | 14.8% |

Moshi is the only streaming-compatible model in the comparison. Practical latency: 200ms.

---

## Capabilities

- **Real-time full-duplex dialogue** at 200ms practical latency — first demonstrated system to model two speaker streams jointly without turn boundaries, enabling overlap, interruption, and backchanneling (maturity: demo)
- **Inner Monologue** for streaming speech-text models: per-frame text prefix nearly triples spoken QA accuracy while remaining streaming-compatible (maturity: demo)
- **Unified ASR/TTS/dialogue** from a single model via a single delay hyperparameter — no architecture or training changes required (maturity: demo)
- **Mimi codec**: causal streaming tokenizer combining semantic and acoustic information at 12.5Hz/1.1kbps, MUSHRA 81.0, outperforming non-causal codecs at higher bitrates (maturity: demo)
- **Adversarial-only codec training**: dramatically superior perceptual quality vs. combined reconstruction+adversarial losses, counter to prevailing assumptions (maturity: research_only)

---

## Limitations and Open Questions

### Architectural limitations

**No text stream for the user.** Moshi processes the user's speech as audio tokens only — there is no text-side Inner Monologue for the user stream. The model cannot perform explicit language-model-level reasoning over what the user said.

**Context window: ~5 minutes.** At 12.5Hz × 8 codebooks, audio requires ~100 tokens/sec. Five minutes of two-stream dialogue requires 60,000 tokens. This is a hard ceiling on session length from the current architecture.

**Audio token compactness gap.** Audio is 25–33× less compact than text (100 tokens/sec vs. 3–4 tokens/sec for text). Efficient long-context audio language modeling at text-LLM scale remains intractable without specialized hierarchical architectures.

### Data limitations

**Full-duplex training data scarcity.** Only ~2000 hours of Fisher dual-channel telephone conversations (8kHz, requiring AudioSR upsampling) exist at scale. This is the primary bottleneck for production-quality real-time dialogue.

**Simulated multi-stream is unrealistic.** Diarized single-channel audio produces perfectly silent inactive speakers — no overlap, no cross-talk. Models trained on this cannot learn natural conversational dynamics.

**Synthetic instruction data only.** All instruction fine-tuning data (20k+ hours) is generated by Helium+TTS. Distribution mismatch with real spontaneous user speech is uncharacterized.

**Text instruct datasets are incompatible with speech.** URLs, bullet points, markdown, and long enumerations cannot be rendered naturally as speech. A new speech-native instruction dataset format is required.

### Evaluation limitations

**Objective audio quality metrics are unreliable.** VisQOL and MOSNet are severely decorrelated from human perceptual judgments when training objectives change. This blocks automated codec development and rapid iteration without expensive human evaluations.

### Scope limitations

**English-only.** The tokenizer targets English with 32,000 tokens. No multilingual capability is demonstrated or discussed.

**Latent diffusion is incompatible with streaming.** High-quality offline audio generation methods are architecturally excluded from real-time dialogue systems — a structural constraint that will affect the ceiling of audio quality achievable at real-time latency.

---

## Bottlenecks Addressed / Introduced

| Bottleneck | Status | Horizon |
|---|---|---|
| Dual-channel conversational recording scarcity | **Active** — limits full-duplex training to thousands of hours | 1–2 years |
| Audio token sequence compactness | **Active** — hierarchical RQ-Transformer is a partial mitigation | 1–2 years |
| Reliable objective audio quality metrics | **Active** — no automated proxy for perceptual quality at present | 1–2 years |
| Speech-native instruction-following data | **Active** — synthetic pipeline is a partial workaround | 1–2 years |

---

## Key Findings for the Landscape

1. **Full-duplex is achievable now** — at the cost of severe data constraints and a 5-minute context ceiling. The architectural path is clear; the bottleneck has shifted to data and long-context efficiency.

2. **Inner Monologue is a general technique** — predicting aligned text as a prefix to audio tokens within a streaming model solves the speech-only knowledge bottleneck without requiring a separate ASR stage. This pattern likely generalizes beyond dialogue.

3. **Text instruction datasets are a hidden incompatibility** — the entire existing instruction-tuning ecosystem (Open Hermes, etc.) is structurally incompatible with speech training. Speech-native instruction data is an underinvested area.

4. **Objective metrics cannot be trusted for codec evaluation** — VisQOL diverging from MUSHRA by 3× is a significant methodological hazard for the field. Any paper reporting only VisQOL for neural codec quality should be treated with caution.

5. **Paralinguistic information is still partially discarded** — while Moshi avoids the ASR bottleneck, the user stream remains audio-only (no user-side Inner Monologue), meaning higher-level reasoning over user prosody and emotion is not directly available to the LM.

---

## Related Themes

- [[themes/audio_and_speech_models|Audio and Speech Models]]
- [[themes/multimodal_models|Multimodal Models]]
- [[themes/unified_multimodal_models|Unified Multimodal Models]]

## Key Concepts

- [[entities/acoustic-tokens|Acoustic Tokens]]
- [[entities/semantic-tokens|Semantic Tokens]]
