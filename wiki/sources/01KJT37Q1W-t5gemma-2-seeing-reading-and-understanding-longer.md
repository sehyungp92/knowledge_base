---
type: source
title: 'T5Gemma 2: Seeing, Reading, and Understanding Longer'
source_id: 01KJT37Q1W003X4GBB8WPM45H4
source_type: paper
authors:
- Biao Zhang
- Paul Suganthan
- Gaël Liu
- Ilya Philippov
- Sahil Dua
- Ben Hora
- Kat Black
- Gus Martins
- Omar Sanseviero
- Shreya Pathak
- Cassidy Hardin
- Francesco Visin
- Jiageng Zhang
- Kathleen Kenealy
- Qin Yin
- Xiaodan Song
- Olivier Lacombe
- Armand Joulin
- Tris Warkentin
- Adam Roberts
published_at: '2025-12-16 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- multimodal_models
- pretraining_and_scaling
- pretraining_data
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# T5Gemma 2: Seeing, Reading, and Understanding Longer

**Authors:** Biao Zhang, Paul Suganthan, Gaël Liu, Ilya Philippov, Sahil Dua, Ben Hora, Kat Black, Gus Martins, Omar Sanseviero, Shreya Pathak, Cassidy Hardin, Francesco Visin, Jiageng Zhang, Kathleen Kenealy, Qin Yin, Xiaodan Song, Olivier Lacombe, Armand Joulin, Tris Warkentin, Adam Roberts
**Published:** 2025-12-16 00:00:00
**Type:** paper

## Analysis

# T5Gemma 2: Seeing, Reading, and Understanding Longer
2025-12-16 · paper · Biao Zhang, Paul Suganthan, Gaël Liu, Ilya Philippov, Sahil Dua et al. (20 total)
https://arxiv.org/pdf/2512.14856

---

### Motivation & Prior Limitations
Encoder-decoder LLMs had fallen significantly behind decoder-only models in capability breadth, operating exclusively on text with limited context length — a substantial gap given that modern applications demand joint vision, multilingual, and long-context understanding.
- Prior encoder-decoder models (including the first-generation T5Gemma) were text-only, meaning the entire encoder-decoder revival trend was blind to images and constrained to short sequences, even as decoder-only LLMs scaled to 128K+ context windows.
  - T5Gemma demonstrated competitive text performance but provided no multimodal capability and no systematic approach to long-context; the paper characterizes this as "the vast majority of these models (if not all) are blind."
- The conventional encoder-decoder design carries architectural overhead: separate word embeddings for encoder and decoder add disproportionate parameter cost at small scales, and the split between decoder self-attention and cross-attention sub-layers increases both parameter count and initialization complexity when adapting from decoder-only checkpoints.

---

### Proposed Approach
T5Gemma 2 extends the T5Gemma adaptation recipe — initializing both encoder and decoder from a pretrained decoder-only Gemma 3 checkpoint and then adapting with the UL2 denoising objective — into multimodal and long-context regimes, while introducing two architectural efficiency innovations.
- The adaptation generalizes across modalities by incorporating the frozen 400M SigLIP vision encoder from Gemma 3, which maps each image to 256 embedding tokens fed exclusively to the encoder; the encoder's bidirectional self-attention gives all tokens full mutual visibility, and cross-attention then exposes those representations to the decoder, creating a structural separation between perception and generation not present in decoder-only models.
- **Tied word embeddings** share encoder input, decoder input, and decoder output/softmax embeddings as a single matrix, reducing embedding parameters by 10.5% with negligible quality loss (~0.1 points), motivated by the observation that separate embeddings are highly redundant at small scales.
- **Merged attention** eliminates the separate cross-attention sub-layer in the decoder by concatenating encoder outputs H with decoder inputs X to form a joint key/value sequence, computing a single attention operation over [X; H] with appropriate causal masking. This saves 6.5% of total parameters with only ~0.3 point quality cost, and critically narrows the architectural difference between the T5Gemma 2 decoder and the Gemma 3 decoder, easing parameter initialization.
- For long-context, positional interpolation is applied with RoPE base frequencies of 10k for local attention layers and 1M for global attention layers (ratio 5:1 local:global), allowing 128K inference despite pretraining only on sequences up to 16K tokens.
- Pretraining uses five UL2 denoising tasks with varied span lengths and corruption rates (mixing ratio 1:1:1:1:4, with a prefix-LM variant for vision data), trained on ~2T tokens across three model sizes: 270M-270M, 1B-1B, and 4B-4B (encoder-decoder parameter counts).

---

### Results & Capabilities
T5Gemma 2 matches or exceeds its Gemma 3 counterpart at pretraining across all five capability dimensions (reasoning, STEM/code, multilingual, multimodal, long-context), and consistently surpasses Gemma 3 after post-training despite applying only lightweight supervised finetuning without RL.
- On long-context benchmarks, T5Gemma 2 4B-4B scores 81.7 on RULER-32K and 57.6 on RULER-128K at pretraining, compared to Gemma 3 4B's 66.8 and 51.7 respectively — a consistent advantage maintained even though T5Gemma 2 was pretrained only on 16K sequences, which the authors attribute to the structural advantage of encoder bidirectionality and cross-attention for information retrieval.
  - T5Gemma (the text-only predecessor) scores near zero on RULER at both 32K and 128K (0.2 and 0.5), confirming that long-context capability in T5Gemma 2 comes from the architectural changes and positional interpolation, not simply from the encoder-decoder form.
- Multimodal adaptation succeeds even for models whose Gemma 3 base was text-only: T5Gemma 2 1B-1B achieves average multimodal pretraining scores of 49.8 (vs. Gemma 3 4B's 58.5) and long-context scores of 43.8 (vs. 50.7), despite being much smaller — suggesting the encoder-decoder architecture provides strong structural inductive bias for perception-heavy tasks.
- At post-training, T5Gemma 2 4B-4B reaches 75.0 on ChartQA, 75.2 on DocVQA, 78.3 on AI2D, 88.6 on GSM8K, and 76.8 on HumanEval — generally outperforming the post-trained Gemma 3 4B despite T5Gemma 2's post-training using only distillation (no RL, much less compute).
- UL2 training objective outperforms PrefixLM+KD for models up to 1B-1B; knowledge distillation (UL2+KD) provides marginal gains (~0.4 points at 1B-1B) but was dropped due to expensive data-loading overhead, with the authors concluding its benefit is highly dependent on teacher-student capacity matching.
- T5Gemma 2 checkpoints serve as the foundation for EmbeddingGemma (Vera et al., 2025), which achieves state-of-the-art performance on text retrieval benchmarks — demonstrating downstream transferability beyond generative tasks.

---

### Implications
The encoder-decoder architecture, long dismissed as architecturally outdated relative to decoder-only LLMs, demonstrates here that its structural decomposition — dedicated bidirectional encoder for input/vision processing, cross-attention for information bridging, autoregressive decoder for generation — provides a genuine inductive advantage for long-context retrieval and multimodal grounding that decoder-only m

## Key Claims

1. T5Gemma 2 adapts pretrained decoder-only Gemma 3 models into encoder-decoder models using the UL2 objective, extending the approach from text-only to multimodal.
2. The encoder-decoder architecture has a unique advantage for long-context modeling, enabling T5Gemma 2 to achieve consistently improved long-context performance up to 128K despite being pretrained on s
3. Tying all word embeddings across encoder and decoder reduces embedding parameters by approximately 10.5% with nearly no quality change.
4. Merged attention, which unifies decoder self-attention and cross-attention into a single module with shared parameters, saves 6.5% of total parameters at a cost of approximately 0.3 points average qua
5. Restricting cross-attention to only decoder layers with global self-attention (every 6 layers) causes a substantial quality drop of approximately 1.3 points on average, making it an unacceptable desig
6. T5Gemma 2 uses a 400M SigLIP encoder as the frozen vision encoder, converting images into 256 embedding tokens fed to the encoder.
7. T5Gemma 2 sets the RoPE base frequency to 10k for local attention layers and 1M for global attention layers to improve long-context modeling.
8. The UL2 training objective consistently outperforms PrefixLM+KD for models up to 1B-1B scale, while UL2+KD provides only marginal improvement over UL2 alone.
9. Text-only pretrained decoder-only models can be successfully adapted into multimodal encoder-decoder models via the T5Gemma adaptation recipe, enabling multimodal capability even when the base model h
10. T5Gemma 2 1B-1B achieves average multimodal and long-context results of 49.8 and 43.8 respectively at pretraining, lagging behind the larger Gemma 3 4B by only 8.7 and 6.9 points despite being much sm

## Capabilities

- Lightweight open encoder-decoder LLMs (270M–4B scale) handling 128K-token long-context inputs, multimodal vision-language, and multilingual tasks, via adaptation from pretrained decoder-only Gemma 3 models using UL2 objective
- Text-only decoder-only pretrained models can be efficiently adapted into multimodal encoder-decoder LLMs via UL2 pretraining with a frozen SigLIP vision encoder, achieving vision-language capabilities without multimodal pretraining from scratch
- Encoder-decoder foundation models (T5Gemma 2) serve as a retrieval embedding backbone achieving state-of-the-art performance on text retrieval benchmarks (EmbeddingGemma)
- Merged attention unifying decoder self-attention and cross-attention into a single joint module with shared parameters reduces total parameter count by 6.5% with only ~0.3 point average quality loss
- Tying all word embeddings (encoder input, decoder input, decoder output/softmax) across encoder and decoder reduces embedding parameters by ~50% (10.5% of total parameters) with negligible quality impact

## Limitations

- Long-context performance degrades sharply from 32K to 128K: Ruler scores roughly halve (e.g., 4B-4B: 81.7 → 57.6 pretraining, 83.1 → 39.5 post-training), despite models being prompted to handle 128K via positional interpolation
- Post-training (lightweight SFT) catastrophically damages long-context performance in smaller encoder-decoder models: T5Gemma 2 1B-1B Ruler 128K collapses from 35.1 (pretraining) to 6.4 (post-training)
- Published post-training results are an explicit lower bound — the models underwent minimal SFT with no RL finetuning, whereas the Gemma 3 counterpart used distillation from a stronger teacher plus full RL
- Dense cross-attention across all decoder layers adds non-negligible computational cost at autoregressive inference, yet restricting cross-attention to global layers only (1 per 6 layers) causes a ~1.3 point quality drop — no efficient sparse cross-attention scheme currently works without quality pen
- Vision input is encoded at a fixed 256 tokens per image regardless of resolution or content complexity, and the vision encoder is frozen during training — preventing adaptation to downstream task-specific visual detail requirements
- STEM and code reasoning is effectively non-functional at 270M–1B scale: MATH scores of 1.5%/4.5%, MBPP 5.6%/25.2%, GSM8K 1.7%/9.1% for 270M-270M and 1B-1B respectively in pretraining evaluation
- Encoder-decoder models lag decoder-only counterparts on open-domain factual retrieval (TriviaQA: 53.1 vs 65.7; NQ: 17.2 vs 20.2 at 4B-4B vs Gemma 3 4B), suggesting the architecture distributes knowledge storage less efficiently
- Prior generation encoder-decoder models (T5Gemma 2B-2B, 9B-9B) were entirely incapable of long-context tasks, scoring near 0.0 on Ruler 32K and 128K — demonstrating that the encoder-decoder class only recently gained this capability
- Inference latency, throughput, and memory footprint at 128K context are entirely unevaluated — all efficiency claims are based solely on parameter count reductions

## Bottlenecks

- Dense cross-attention across all decoder layers is computationally necessary for quality but creates a hard inference cost bottleneck at long contexts; sparse alternatives (global-layer-only cross-attention) cause ~1.3 point quality degradation with no current solution
- Encoder-decoder models lack RL post-training pipelines, data, and recipes equivalent to those developed for decoder-only models, systematically preventing them from realising their full instruction-following and reasoning potential

## Breakthroughs

- First capable long-context encoder-decoder LLMs (up to 128K tokens) demonstrated at practical parameter scales (270M–4B), resolving a near-total capability gap where all prior encoder-decoder models scored ~0 on long-context benchmarks
- The UL2-based decoder-to-encoder-decoder adaptation recipe generalises from text-only to full multimodal: text-only decoder-only pretrained models can be adapted to vision-language encoder-decoder models by grafting a frozen vision encoder, achieving competitive multimodal benchmarks at 1B-1B scale 

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/pretraining_data|pretraining_data]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/gemma-3|Gemma 3]]
- [[entities/grouped-query-attention|Grouped-Query Attention]]
- [[entities/qk-norm|QK-Norm]]
- [[entities/rope-rotary-position-embedding|RoPE (Rotary Position Embedding)]]
- [[entities/siglip|SigLIP]]
