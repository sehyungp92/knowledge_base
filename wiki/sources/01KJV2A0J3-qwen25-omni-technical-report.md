---
type: source
title: Qwen2.5-Omni Technical Report
source_id: 01KJV2A0J3CM8E8P7ZM79RR57V
source_type: paper
authors:
- Jin Xu
- Zhifang Guo
- Jinzheng He
- Hangrui Hu
- Ting He
- Shuai Bai
- Keqin Chen
- Jialin Wang
- Yang Fan
- Kai Dang
- Bin Zhang
- Xiong Wang
- Yunfei Chu
- Junyang Lin
published_at: '2025-03-26 00:00:00'
theme_ids:
- audio_and_speech_models
- finetuning_and_distillation
- model_architecture
- multimodal_models
- post_training_methods
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Qwen2.5-Omni Technical Report

**Authors:** Jin Xu, Zhifang Guo, Jinzheng He, Hangrui Hu, Ting He, Shuai Bai, Keqin Chen, Jialin Wang, Yang Fan, Kai Dang, Bin Zhang, Xiong Wang, Yunfei Chu, Junyang Lin
**Published:** 2025-03-26 00:00:00
**Type:** paper

## Analysis

# Qwen2.5-Omni Technical Report
2025-03-26 · paper · Jin Xu, Zhifang Guo, Jinzheng He, Hangrui Hu, Ting He et al. (14 total)
https://arxiv.org/pdf/2503.20215

---

### Motivation & Prior Limitations

- Prior multimodal models handled understanding and generation across modalities in fragmented or pipeline-based ways, failing to unify text, audio, image, and video perception with simultaneous streaming text and speech output in a single end-to-end system.
  - Language-Audio-Language Models (LALMs) and Language-Visual-Language Models (LVLMs) each extended LLMs into one additional modality, but no single model efficiently unified all modalities for both input and output.
  - Existing omni-models suffered from temporal misalignment between audio and video streams, with no principled mechanism to synchronize their positional representations within a shared attention context.

- Concurrent generation of text and speech outputs in prior systems caused cross-modal interference during training, with text and speech token supervision conflicting when naively combined.
  - This interference degraded both modality outputs and prevented true end-to-end joint training of the understanding and speaking components.

- Streaming multimodal inference imposed prohibitive initial packet latency due to the sequential nature of full-sequence encoding for audio and visual inputs, making real-time interaction impractical.
  - Full-attention audio/visual encoders could not be chunked for prefilling without architectural modification, blocking efficient streaming deployment.

- Speech instruction-following quality in prior audio-language models degraded severely compared to text-instruction baselines: Qwen2-Audio scored 33.2 on MMLU when using speech instructions, versus 69.3 for Qwen2-7B using text, a 36-point gap that rendered voice interaction unreliable for complex reasoning tasks.

---

### Proposed Approach

- Qwen2.5-Omni introduces a Thinker-Talker architecture that separates reasoning (text generation) from speaking (speech token generation) while keeping both components jointly trained end-to-end in a single model.
  - Thinker is a standard Transformer decoder that processes multimodal inputs and generates text and high-level hidden representations; Talker is a dual-track autoregressive Transformer decoder that receives Thinker's hidden states directly and autoregressively generates discrete speech tokens in parallel with text.
  - Talker receives both the high-dimensional representations (for prosodic/tonal context before full text completion) and the sampled discrete text tokens (to resolve phonetic ambiguity, since semantically similar representations may correspond to phonetically distinct words), enabling natural streaming speech with appropriate prosody and emotion.
  - This design is inspired by human neurobiology, where distinct organs produce different output signals coordinated by shared neural systems.

- TMRoPE (Time-aligned Multimodal RoPE) is a novel positional embedding that decomposes rotary position encodings into temporal, height, and width components and assigns absolute temporal positions aligned to 40ms intervals across both audio and video streams.
  - For video-with-audio inputs, a time-interleaving method segments representations into 2-second chunks, placing visual tokens first and audio tokens second within each chunk, then interleaving across time — ensuring audio and video share a coherent temporal axis within the shared attention mechanism.
  - For text and image-only inputs, TMRoPE reduces to standard 1D-RoPE and M-RoPE respectively, maintaining backward compatibility with Qwen2.5-VL's vision encoder.

- All multimodal encoders are modified to support block-wise streaming attention: the audio encoder operates in 2-second blocks (rather than full-sequence attention), and the vision encoder uses flash attention with 2×2 token merging via MLP, enabling chunked prefilling compatible with modern inference frameworks.

- Speech token decoding uses a sliding-window DiT (Diffusion Transformer) with Flow-Matching that limits the receptive field to 4 blocks (2 lookback, 1 lookahead) to convert discrete tokens to mel-spectrograms in a streaming chunk-by-chunk fashion, followed by a modified BigVGAN for waveform reconstruction, minimizing initial audio output latency.

- The Talker undergoes a three-stage post-training process: (1) in-context learning for speech continuation via next-token prediction on multimodal dialogue data, (2) DPO optimization using WER and punctuation pause error rate as reward signals to improve generation stability and reduce hallucinations, and (3) multi-speaker instruction fine-tuning with timbre disentanglement to improve naturalness and controllability.

- Pre-training proceeds in three stages: frozen LLM with encoder-only training on image-text and audio-text pairs, then full parameter training on 800B image/video tokens + 300B audio tokens + 100B video-with-audio tokens across mixed multimodal tasks, then long-sequence extension to 32k tokens for long audio and video comprehension.

---

### Results & Capabilities

- On multimodal understanding benchmarks, Qwen2.5-Omni achieves state-of-the-art performance on OmniBench, scoring 56.13% average across speech, sound event, and music categories — surpassing Gemini-1.5-Pro (42.91%), Baichuan-Omni-1.5 (42.9%), and MiniCPM-o (40.5%) by substantial margins.
  - The music subset score of 52.83% and sound event score of 60.00% are particularly notable given that prior omni models largely underperformed on non-speech audio categories.

- Speech instruction-following narrows the gap to text-based performance to near-parity: Qwen2.5-Omni scores 65.6 on MMLU and 85.4 on GSM8K with speech instructions, versus 69.3 and 82.3 for Qwen2-7B with text instructions — compared to Qwen2-Audio's 33.2 and 18.4 on the same benchmarks with speech input.

- On audio understanding, Qwen2.5-Omni achieves state-of-the-art on MMAU (65.6

## Key Claims

1. Qwen2.5-Omni is an end-to-end multimodal model that can perceive text, images, audio, and video while simultaneously generating text and natural speech responses in a streaming manner.
2. Both audio and visual encoders in Qwen2.5-Omni use a block-wise processing approach to enable streaming of multimodal information inputs.
3. TMRoPE (Time-aligned Multimodal RoPE) is a novel position embedding approach that synchronizes timestamps of video inputs with audio by organizing audio and video in an interleaved manner.
4. The Talker component is a dual-track autoregressive model that directly uses hidden representations from the Thinker to produce audio tokens.
5. A sliding-window DiT is used for decoding audio tokens in streaming, restricting the receptive field to reduce initial packet delay.
6. Qwen2.5-Omni's image and audio capabilities are comparable to Qwen2.5-VL and superior to Qwen2-Audio respectively, at similar model sizes.
7. Qwen2.5-Omni achieves state-of-the-art performance on OmniBench and AV-Odyssey Bench multimodal benchmarks.
8. Qwen2.5-Omni's end-to-end speech instruction following performance is comparable to its text-input performance on MMLU and GSM8K benchmarks.
9. Qwen2.5-Omni achieves 1.42%, 2.33%, and 6.54% WER on seed-tts-eval test-zh, test-en, and test-hard sets respectively, outperforming MaskGCT and CosyVoice 2.
10. Qwen2.5-Omni's streaming Talker outperforms most existing streaming and non-streaming alternatives in robustness and naturalness of speech generation.

## Capabilities

- End-to-end unified 7B multimodal model simultaneously perceiving text, audio, images, and video while streaming both text and natural speech responses in real time, achieving state-of-the-art on OmniBench (56.13% avg vs Gemini-1.5-Pro 42.91%)
- Speech instruction following in a unified 7B omni-model achieves near-parity with text input on complex reasoning benchmarks: GSM8K 85.4% (speech) vs 82.3% (text), MMLU 65.6% vs 69.3%
- Streaming speech generation with near-human naturalness (NMOS 4.46–4.62 vs human baseline 4.51) via Thinker-Talker architecture and sliding-window DiT codec, outperforming most existing streaming and non-streaming TTS systems on robustness and naturalness
- TMRoPE (Time-aligned Multimodal RoPE) positional embedding synchronizes audio and video temporal streams by interleaving representations in 2-second chunks with absolute temporal IDs (one ID per 40ms), enabling coherent joint audio-video understanding
- Block-wise streaming processing of multimodal encoders enables real-time prefilling for audio (2-second blocks) and video inputs without full-sequence buffering, supporting chunked-prefill inference patterns
- Unified 7B multimodal model trained on 800B image/video + 300B audio tokens achieves image understanding comparable to the dedicated Qwen2.5-VL-7B (DocVQA: 95.2, ChartQA: 85.3) and surpasses GPT-4o-mini on most image benchmarks

## Limitations

- Multimodal training imposes a measurable text capability tax — Qwen2.5-Omni-7B underperforms the equivalent pure-text Qwen2.5-7B on MMLU-Pro (47.0 vs 56.3), GPQA (30.8 vs 36.4), and LiveBench (29.6 vs 35.9), falling between two generations of text-only models
- Speech instruction following still significantly lags text on complex instruction benchmarks — IFEval: 41.7% (speech) vs 53.3% (text), CEval: 61.1% vs 78.4%, Math401: 62.2% vs 75.5% — suggesting residual information loss in the speech-to-understanding pathway
- Output modalities are limited to text and speech — the model cannot generate images, video, or music despite ingesting all four modalities as input
- Pretraining data noise and pronunciation errors cause speech generation hallucinations, requiring an additional RL stabilization stage to mitigate — revealing that stable speech generation cannot be achieved through pretraining alone
- Speaker similarity in zero-shot TTS lags behind dedicated TTS systems — Qwen2.5-Omni achieves 0.641 speaker similarity on test-en vs Seed-TTS's 0.766, a 16% relative gap that persists even after RL optimization
- Video OCR and audio-video collaborative understanding are identified as critical unsolved challenges with no adequate benchmarks or training datasets, leaving a systematic gap in evaluation and improvement
- Block-wise audio processing (2-second chunks with no cross-block attention) constrains fine-grained temporal reasoning that requires context spanning block boundaries — a deliberate latency/quality tradeoff with unknown performance impact on long-form audio tasks
- Speech generation evaluation methodology is entirely TTS-centric (WER, speaker similarity, NMOS) with no metrics for interactive latency, turn-taking naturalness, emotional appropriateness, or conversational coherence
- Full replication and iteration requires training on 800B image/video tokens, 300B audio tokens, and 100B video-audio tokens — making the training cost inaccessible to most researchers and creating a significant compute moat
- Stable and natural speech generation requires a three-stage Talker training pipeline (ICL pretraining → DPO stabilization → speaker fine-tuning), preventing direct end-to-end training and adding significant engineering complexity

## Bottlenecks

- No adequate evaluation benchmarks or research datasets exist for video OCR and audio-video collaborative understanding, blocking systematic measurement and improvement of joint modality reasoning in omni-models
- The speech-text instruction following gap persists as a structural bottleneck in end-to-end omni-models — even with large-scale unified training, speech inputs yield meaningfully lower performance on complex structured tasks (IFEval: 41.7% speech vs 53.3% text), limiting voice-native AI in technical

## Breakthroughs

- Thinker-Talker architecture enables a single end-to-end model to concurrently generate streaming text and natural speech by having the Talker consume high-level hidden representations directly from the Thinker — preserving emotional and semantic context that cascaded STT→LLM→TTS pipelines discard — 
- End-to-end unified training nearly closes the speech-text instruction following gap for complex reasoning tasks — GSM8K: 85.4% (speech input) vs 82.3% (text input), compared to Qwen2-Audio's 18.4% on the same task — demonstrating that the modality gap is an artifact of architecture and training stra

## Themes

- [[themes/audio_and_speech_models|audio_and_speech_models]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/model_architecture|model_architecture]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/m-rope|M-RoPE]]
- [[entities/mmlu|MMLU]]
- [[entities/qwen25-vl|Qwen2.5-VL]]
