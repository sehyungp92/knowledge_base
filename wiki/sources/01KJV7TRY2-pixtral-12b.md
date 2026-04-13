---
type: source
title: Pixtral 12B
source_id: 01KJV7TRY28HAYF81PCXPPZCAW
source_type: paper
authors:
- Pravesh Agrawal
- Szymon Antoniak
- Emma Bou Hanna
- Baptiste Bout
- Devendra Chaplot
- Jessica Chudnovsky
- Diogo Costa
- Baudouin De Monicault
- Saurabh Garg
- Theophile Gervet
- Soham Ghosh
- Amélie Héliou
- Paul Jacob
- Albert Q. Jiang
- Kartik Khandelwal
- Timothée Lacroix
- Guillaume Lample
- Diego Las Casas
- Thibaut Lavril
- Teven Le Scao
- Andy Lo
- William Marshall
- Louis Martin
- Arthur Mensch
- Pavankumar Muddireddy
- Valera Nemychnikova
- Marie Pellat
- Patrick Von Platen
- Nikhil Raghuraman
- Baptiste Rozière
- Alexandre Sablayrolles
- Lucile Saulnier
- Romain Sauvestre
- Wendy Shang
- Roman Soletskyi
- Lawrence Stewart
- Pierre Stock
- Joachim Studnia
- Sandeep Subramanian
- Sagar Vaze
- Thomas Wang
- Sophia Yang
published_at: '2024-10-09 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- model_architecture
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Pixtral 12B

Pixtral 12B introduces a 12-billion-parameter vision-language model that resolves a longstanding tradeoff in open-source multimodal models: achieving strong multimodal performance without degrading text-only reasoning. Its central architectural contribution is Pixtral-ViT, a 400M-parameter vision encoder trained from scratch using RoPE-2D positional encodings, enabling native processing of arbitrary image resolutions and aspect ratios — eliminating the fixed-resolution tiling workarounds that constrained prior VLMs. The paper also exposes a systemic reliability problem in multimodal evaluation and proposes concrete remedies, including standardized prompt specifications, flexible parsing, and MM-MT-Bench, a new multi-turn instruction-following benchmark that correlates strongly with human preference rankings.

**Authors:** Pravesh Agrawal, Szymon Antoniak, Emma Bou Hanna, Baptiste Bout, Devendra Chaplot, Jessica Chudnovsky et al. (42 total)
**Published:** 2024-10-09
**Type:** paper
**Themes:** [[themes/multimodal_models|Multimodal Models]] · [[themes/vision_language_models|Vision-Language Models]] · [[themes/model_architecture|Model Architecture]] · [[themes/evaluation_and_benchmarks|Evaluation & Benchmarks]] · [[themes/benchmark_design|Benchmark Design]]

---

## Motivation

Prior open-source multimodal models at the 7–12B scale exhibit a consistent tradeoff: gains in vision capability come at measurable cost to text-only performance. Models like Llama-3.2 11B and Qwen2-VL 7B show degraded scores on MATH and HumanEval relative to their base language models. Pixtral 12B directly targets this tradeoff, framing it as an architectural problem rather than a fundamental constraint.

A second motivation is architectural. Standard vision encoders — optimized for ImageNet at 224×224 or 336×336 pixels — require images to be decomposed into fixed-size square tiles when used in multimodal LLMs. Learned absolute position embeddings must then be interpolated for novel resolutions, reliably degrading performance. This limits fidelity for documents, charts, and high-resolution inputs where geometry and aspect ratio carry semantic meaning.

A third motivation is evaluative. The paper finds that multimodal benchmark scores are highly sensitive to prompt specification and scoring conventions. Small format changes dramatically shift rankings for leading closed-source models, and exact-match metrics systematically underecount correct answers that differ only in surface form (e.g., `6.0` vs `6`). Cross-paper comparisons are, as a result, unreliable.

---

## Architecture

### Vision Encoder: Pixtral-ViT

Pixtral-ViT is a 400M-parameter vision transformer trained from scratch — not adapted from an ImageNet-optimized encoder. This design choice is explicit: the encoder is optimized for multimodal language modeling tasks (OCR, chart reasoning, document understanding) rather than image classification.

Four key changes distinguish it from standard ViT architectures:

**RoPE-2D positional encodings.** Learned absolute embeddings are replaced with 2D rotary position encodings that encode row and column positions independently across feature dimensions. The implementation satisfies the *relative* property: inner products between two patch representations depend only on their relative positional offset in height and width, not absolute position. This allows the encoder to generalize to arbitrary resolutions without interpolation.

**[IMAGE BREAK] and [IMAGE END] tokens.** Inserted between image rows and at image boundaries respectively, these tokens help the decoder distinguish between images with identical patch counts but different aspect ratios — a disambiguation problem that RoPE-2D alone does not fully resolve.

**Gated feedforward network.** Standard FFN layers in the attention block are replaced with gating in the hidden layer.

**Sequence packing with block-diagonal attention masks.** Multiple images are flattened and concatenated along the sequence dimension in a single forward pass. Block-diagonal attention masks prevent attention leakage between images, improving training and inference efficiency.

### Multimodal Decoder

The decoder is Mistral Nemo 12B (frozen), connected to Pixtral-ViT via a two-layer fully connected network with GeLU activations. Standard causal self-attention with RoPE-1D is applied uniformly to both image and text tokens across a 128K-token context window, enabling arbitrary multi-image, multi-turn conversations.

---

## Capabilities

- **Native variable-resolution vision encoding.** Pixtral-ViT processes images at their natural resolution and aspect ratio without tiling or interpolation, removing a longstanding architectural constraint in VLMs. [[themes/vision_language_models|Vision-Language Models]]
- **No modality-performance tradeoff.** Pixtral 12B maintains competitive scores on MATH and HumanEval while outperforming similarly sized multimodal models — the first open-source model at this scale to demonstrate this.
- **Flexible per-image token budget.** Images can be processed at low resolution for latency-constrained settings or high resolution for fine-grained tasks without retraining.
- **Multi-image, multi-turn context.** Any number of images can be processed within the 128K context window via the causal decoder architecture.
- **Scale efficiency.** Pixtral 12B outperforms Llama-3.2 90B on multimodal benchmarks while being approximately 7× smaller, and surpasses Claude-3 Haiku and Gemini-1.5 Flash 8B.

---

## Limitations & Open Questions

### Evaluation reliability
- **Prompt sensitivity.** Benchmark rankings are highly sensitive to prompt specification. Small format changes dramatically alter scores for leading closed-source models, making cross-paper comparisons misleading. *(severity: significant, trajectory: improving)*
- **Short-form benchmark bias.** Existing multimodal benchmarks predominantly measure single-image, multiple-choice or short-form QA, systematically failing to capture multi-turn, long-form, open-ended assistant settings. *(severity: significant, trajectory: improving)*
- **Exact-match scoring.** Standard metrics underecount correct answers that differ only in surface format, artificially depressing reported performance. *(severity: significant, trajectory: improving)*
- **Upward publication bias.** Under-specified default prompts systematically inflate the reported figures of models that have been carefully tuned to those prompts, creating asymmetric baseline comparisons. *(severity: significant, trajectory: stable)*

### Architectural limitations inherited
- **Fixed-resolution encoders.** The paper's framing highlights how ImageNet-optimized encoders lose spatial context and aspect ratio fidelity — a limitation Pixtral-ViT addresses, but one that remains present in most deployed VLMs. *(severity: significant, trajectory: improving)*
- **Absolute positional embeddings.** Standard ViTs must interpolate embeddings for unseen resolutions, reliably degrading out-of-distribution performance. RoPE-2D resolves this for Pixtral-ViT specifically. *(severity: significant, trajectory: improving)*

### Evaluation coverage gaps in this paper
- **MM-MT-Bench scale.** The benchmark covers only 92 manually curated conversations, too small for statistically robust evaluation across long-tail tasks or domain-specific use cases. *(severity: minor, trajectory: unclear)*
- **No hallucination or calibration evaluation.** The paper is entirely benchmark-performance-focused. Hallucination rates, factual grounding, adversarial robustness, and failure modes are not characterized. *(severity: significant, trajectory: unclear)*

---

## Bottlenecks Addressed

**Evaluation standardization.** The absence of standardized multimodal evaluation protocols — varying prompt specifications and scoring conventions — blocks fair model-to-model comparison and reliable measurement of capability improvements over time. The paper directly addresses this with explicit prompt specifications, flexible parsing, and open-sourced evaluation code. *(horizon: months)*

**Real-world benchmark validity.** Benchmarks optimized for automated exact-match scoring fail to measure assistant utility in practical settings, blocking reliable model selection for deployment. MM-MT-Bench proposes a scalable LLM-judged alternative with demonstrated validity via 0.91 Pearson correlation with LMSys human-preference ELO. *(horizon: 1–2 years)*

---

## Breakthroughs

**RoPE-2D in a from-scratch vision encoder** removes the fixed-resolution constraint that has required tiling workarounds in VLMs since their inception. The relative-position property enables clean generalization to arbitrary resolutions without interpolation degradation. This is likely to influence future vision encoder designs. *(significance: notable)*

**Architectural efficiency at scale.** Surpassing a 90B-parameter model with a 12B-parameter model via architectural improvements — rather than scale — demonstrates that the quality-size tradeoff in multimodal models is not fundamental. *(significance: notable)*

---

## Evaluation Methodology Contributions

The paper's evaluation contributions are arguably as significant as its architectural ones:

- **"Explicit" prompts** fully specify required output format, eliminating ambiguity that artificially disadvantages models not tuned to a particular benchmark's implicit conventions.
- **Flexible parsing** accepts semantically equivalent but format-variant answers, correcting systematic undercounting by exact-match metrics.
- **MM-MT-Bench** provides 92 multi-turn conversations across five categories (charts, tables, PDF pages, diagrams, miscellaneous), scored by LLM judge on correctness and completeness (1–10 scale). Its 0.91 Pearson correlation with LMSys Vision ELO validates LLM-judged multi-turn evaluation as a scalable proxy for human preference — with implications for [[themes/benchmark_design|benchmark design]] broadly.

---

## Connections

- The variable-resolution encoding architecture connects to broader work on [[themes/model_architecture|model architecture]] for spatial and document understanding tasks.
- The evaluation reliability findings feed directly into ongoing debates in [[themes/evaluation_and_benchmarks|evaluation methodology]] — the prompt sensitivity result is a general finding that extends beyond VLMs.
- The efficiency result (12B > 90B) reinforces a trend in [[themes/multimodal_models|multimodal models]] where architectural innovations increasingly decouple capability from parameter count.
