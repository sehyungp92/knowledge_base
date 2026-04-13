---
type: theme
title: Audio & Speech Models
theme_id: audio_and_speech_models
level: 2
parent_theme: multimodal_models
child_themes: []
created: '2026-04-08'
updated: '2026-04-08'
source_count: 8
sources_since_update: 0
update_count: 1
velocity: 0.0
staleness: 0.0
status: active
tags: []
---
# Audio & Speech Models

> Audio and speech models have undergone a quiet paradigm shift — one driven less by architectural innovation than by a belated reckoning with data quality and scale. Voice AI has crossed practical thresholds for research deployment, but the deeper story is structural: the field spent years optimizing models against inadequate datasets, mistaking data starvation for architectural limitation. The emergence of internet-scale cinematic training pipelines has exposed a scaling gap analogous to GPT-2→GPT-3, suggesting audio is one of the last major modalities where the scaling thesis was untested — and is now being confirmed.

**Parent:** [[themes/multimodal_models|multimodal_models]]

## Current State

For much of its recent history, audio generation research operated under a false ceiling. Models in the 300M–1.3B parameter range were trained on datasets like VGGSound (550 hours) and AudioSet (5K hours) — non-cinematic, small-scale corpora that systematically prevented models from learning professional production patterns. The field interpreted the resulting quality gap as an architectural problem and responded with architectural solutions. It was the wrong diagnosis.

The arrival of Movie Gen Audio — 13B parameters trained on internet-scale cinematic data — produced a qualitative capability jump that reframed the prior decade of work. Outperforming all baselines by 33–91% across synchronization, correctness, and overall quality metrics, it demonstrated that the bottleneck was never the model; it was the data. Synchronized diegetic and non-diegetic audio mixing, frame-by-frame visual-audio alignment, and DAC-VAE operating at 48kHz/25Hz represent capabilities the field had not seen before — not because they were architecturally out of reach, but because the training signal was too impoverished to learn them.

In parallel, the practical deployment frontier has moved. Voice AI models have crossed what might be called the uncanny valley for research applications — sounding natural and responding quickly enough to sustain meaningful interaction. Yet consumer voice assistants (Alexa, Siri) still command substantial adoption (32% and 25% of AI users for routine tasks respectively) despite significant quality gaps, a reminder that user inertia and ecosystem lock-in can decouple adoption from capability.

The emerging architectural direction — masked audio prediction enabling a single model to generate, extend, and infill — points toward consolidation: separate generation and editing systems may give way to unified models trained on a single objective.

## Capabilities

- **Voice naturalness for research deployment** (maturity: `narrow_production`): Voice AI models have crossed the uncanny valley for research applications — sounding natural and responding quickly enough to be useful in structured contexts. Deployment beyond controlled research settings remains limited.

## Limitations

- **Consumer adoption decoupled from quality** (severity: `significant`, trajectory: `improving`, type: `implicit_controlled_conditions`): Voice AI assistants (Alexa, Siri) maintain significant user adoption — 32% and 25% of AI users for routine tasks — despite quality gaps relative to newer models. This signals that adoption metrics are poor proxies for capability leadership; ecosystem inertia, distribution, and habit dominate. Improving trajectory reflects both rising model quality and slow erosion of legacy assistant share.

## Bottlenecks

- **Dataset quality and scale** (now partially resolved): The primary bottleneck in audio generation was not architecture but training data. VGGSound and AudioSet — the dominant benchmarks — are non-cinematic and undersized, preventing models from learning professional production patterns. Internet-scale cinematic data has begun to dissolve this bottleneck, but access to such data remains asymmetrically concentrated in large labs. The research community at large has not yet been able to replicate this data advantage.

## Breakthroughs

- **Movie Gen Audio and the scaling confirmation**: Movie Gen Audio (13B params, internet-scale cinematic data) vs. prior SOTA (300M–1.3B params, 550–5K hours) produces a qualitative capability jump the field had not seen before. Frame-by-frame visual-audio alignment (replacing temporal concatenation), DAC-VAE at 48kHz/25Hz, and masked audio prediction enabling unified generation, extension, and infilling from a single model — collectively outperforming all baselines by 33–91% across key metrics. This is early confirmation that scaling laws transfer to audio as they did to language and vision. See cross-theme implications from [[themes/multimodal_models|multimodal_models]].

## Anticipations

- **Masked audio prediction as the standard training objective** (confidence: 0.70, status: `open`): Masked audio prediction — enabling generate, extend, and infill from a single unified model — will become the standard training objective for video-conditioned audio models, displacing separate generation and editing systems. The architectural precedent from language (masked language modeling → GPT-style objectives → unified models) suggests this consolidation is likely; the question is pace and whether cinematic video-audio alignment specifically demands this approach.

## Cross-Theme Implications

- **From [[themes/multimodal_models|multimodal_models]]:** Movie Gen Audio's frame-by-frame visual-audio alignment (vs. temporal concatenation), DAC-VAE at 48kHz/25Hz, and masked audio prediction enabling infilling and bidirectional extension from a single model represent a step-change in synchronized video-to-audio generation — outperforming all baselines by 33–91% across sync, correctness, and overall quality metrics. The architectural choices are directly relevant to any multimodal system requiring tight temporal alignment between modalities.

- **From [[themes/multimodal_models|multimodal_models]] (data bottleneck):** The bottleneck in audio generation was dataset quality and scale, not architecture. VGGSound and AudioSet are non-cinematic, small-scale datasets that systematically prevented audio models from learning professional production patterns. Internet-scale cinematic data unlocks synchronized diegetic/non-diegetic audio mixing — a qualitative capability the field had not seen before. This implies the audio research community has been solving the wrong problem: architectural innovation on inadequate data cannot substitute for proper data curation at scale.

- **From [[themes/multimodal_models|multimodal_models]] (scaling laws):** Audio generation models have been operating under a false ceiling: the field interpreted the quality gap as architectural limitation when it was actually severe data and compute starvation. Movie Gen Audio (13B params, internet-scale cinematic data) vs. prior SOTA (300M–1.3B params, 550–5K hours) produces a qualitative capability jump analogous to GPT-2→GPT-3. Scaling laws that held for language and video appear to transfer directly to audio — audio is one of the last major modalities where the scaling thesis was untested, and this is early confirmation that it holds.

## Contradictions

- **Adoption vs. capability**: Legacy voice assistants (Alexa, Siri) command substantial adoption despite lagging meaningfully behind current model quality. This contradicts any model of the world where adoption tracks capability — and implies that competitive dynamics in voice AI are governed more by distribution and habit than by technical leadership. Labs optimizing for benchmark performance without distribution advantages may find the market unreceptive.

- **Architectural focus vs. data deficit**: The field's longstanding emphasis on architectural innovation — while training on VGGSound and AudioSet — represents a systematic mismatch between intervention and bottleneck. The implication is uncomfortable: a significant portion of audio ML research from the past several years may have been measuring progress against a data ceiling rather than a true capability frontier.

## Research Opportunities

- **Open cinematic audio datasets**: The quality gains from internet-scale cinematic training are currently inaccessible to most researchers. Curating and releasing high-quality, cinematically diverse audio-video datasets at scale could unlock a wave of research that replicates or extends Movie Gen Audio's findings outside proprietary settings.

- **Scaling law characterization for audio**: If audio follows the same scaling curves as language and vision, the field would benefit from systematic compute-optimal training studies (Chinchilla-style) specific to audio modalities and audio-visual alignment tasks.

- **Unified generate/extend/infill architectures**: The anticipated convergence on masked audio prediction as a training objective is still open. Research establishing when and why unified objectives outperform specialized ones — and characterizing failure modes — would ground the anticipation in empirical evidence.

- **Consumer adoption friction**: Understanding why users remain with lower-quality voice assistants despite alternatives has direct implications for deployment strategy. This is as much a behavioral research question as a technical one.

## Development Timeline
<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->
- **2026-04-08** — [[sources/01KJSW6SGQ-crossing-the-uncanny-valley-of-conversational-voice|Crossing the uncanny valley of conversational voice]]: Three model sizes were trained: Tiny (1B backbone, 100M decoder), Small (3B backbone, 250M decoder),
- **2026-04-08** — Wiki page created. Theme has 8 sources.
- **2025-05-05** — [[sources/01KJTWJ62T-voila-voice-language-foundation-models-for-real-time-autonomous-interaction-and-|Voila: Voice-Language Foundation Models for Real-Time Autonomous Interaction and Voice Role-Play]]: Voila's voice tokenizer was trained on 100,000 hours of audio data.
- **2025-03-26** — [[sources/01KJV2A0J3-qwen25-omni-technical-report|Qwen2.5-Omni Technical Report]]: Both audio and visual encoders in Qwen2.5-Omni use a block-wise processing approach to enable stream
- **2025-03-18** — [[sources/01KJVVDA1F-why-ai-voice-feels-more-human-than-ever|Why AI Voice Feels More Human Than Ever]]: Latency has dropped dramatically: one year ago, 2–3 seconds was acceptable; now even 0.5–1 second of
- **2024-11-19** — [[sources/01KJVTRDK8-a-deep-dive-into-the-future-of-voice-in-ai|A Deep Dive into the Future of Voice in AI]]: Traditional voice mode used a speech-to-text step to convert audio to text, which was then sent into
- **2024-10-17** — [[sources/01KJV79X7A-movie-gen-a-cast-of-media-foundation-models|Movie Gen: A Cast of Media Foundation Models]]: Diffusion-style models were chosen over discrete token-based language models because their non-autor
- **2024-10-15** — [[sources/01KJT0GCSN-part-ii-multimodal-capabilities-unlock-new-opportunities-in-vertical-ai|Part II: Multimodal capabilities unlock new opportunities in Vertical AI]]: Speech-native models have substantially lower latency (under 500 milliseconds) than previous cascadi
- **2024-09-17** — [[sources/01KJV89Q4X-moshi-a-speech-text-foundation-model-for-real-time-dialogue|Moshi: a speech-text foundation model for real-time dialogue]]: Helium is a 7B-parameter autoregressive text language model pretrained on 2.1 trillion tokens of pub
