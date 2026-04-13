---
type: source
title: 'DeepSeek-OCR: Contexts Optical Compression'
source_id: 01KKT3SS8QNPF4DKKA749J3TFR
source_type: paper
authors: []
published_at: '2025-10-17 00:00:00'
theme_ids:
- adaptive_computation
- long_context_and_attention
- model_architecture
- multimodal_models
- post_training_methods
- synthetic_data_generation
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# DeepSeek-OCR: Contexts Optical Compression

> DeepSeek-OCR reframes document OCR as a vision-text compression problem, treating the vision encoder as a lossy compressor of textual information and the LM decoder as the decompressor. By introducing a novel serial encoder architecture (DeepEncoder) and a token-efficient MoE decoder, the system demonstrates near-lossless text recovery at 10× compression, challenging whether visual tokens can substitute for digital text in LLM context windows — and establishing a new paradigm for efficient document understanding at production scale.

**Authors:** DeepSeek AI
**Published:** 2025-10-17
**Type:** paper

---

## Motivation

[[themes/long_context_and_attention|Long Context & Attention]] processing in LLMs scales quadratically with sequence length, making document-heavy workloads prohibitively expensive. Yet no prior work had systematically investigated using the visual modality as a compression medium for text. The question motivating this paper — *how many vision tokens are minimally required to decode N text tokens from a document image?* — had never been addressed end-to-end.

Prior approaches carried distinct architectural deficits that prevented their use as efficient text compressors:

- **Dual-tower** (e.g., Vary): dual image preprocessing complicates deployment and pipeline parallelism
- **Tile-based** (e.g., InternVL2.0): low native encoder resolution (~512×512) causes fragmentation into 6,000–7,000 vision tokens per page
- **Adaptive-resolution** (e.g., Qwen2-VL via NaViT): massive activation memory at high resolution, risking GPU overflow

State-of-the-art pipeline systems like MinerU2.0 consumed 6,000+ vision tokens per page; even the most efficient prior end-to-end model (GOT-OCR2.0) required 256 tokens per page.

---

## Architecture

### DeepEncoder (~380M parameters)

The central architectural contribution is a serial encoder that chains two components through a 16× convolutional compressor:

1. **SAM-base** (80M params, patch size 16, window attention): processes a 1024×1024 input into 4,096 patch tokens at low activation memory cost
2. **16× convolutional compressor**: two convolutional layers (kernel 3, stride 2, padding 1, channels 256→1024) reduce 4,096 tokens to 256
3. **CLIP-large** (300M params, global attention): operates on the compressed 256-token sequence, avoiding the memory cost of dense attention over 4,096 tokens

This design keeps activation memory tractable by deferring global attention until after compression — the key insight that prior architectures missed. DeepEncoder operates at native resolutions of 512–1,280px, with tile counts limited to 2–9 in Gundam mode to prevent fragmentation.

Six resolution modes enable a single model to probe different compression regimes:

| Mode | Vision Tokens | Approx. Compression Range |
|------|-------------|--------------------------|
| Tiny | 64 | ~20× |
| Small | 100 | ~7.5–12.6× |
| Base | 256 | — |
| Large | 400 | — |
| Gundam | ~100n+256 | variable |
| Gundam-M | ~256n+400 | variable |

Dynamic positional encoding interpolation enables all modes in a single model.

### Decoder: DeepSeek-3B-MoE

The decoder uses [[entities/deepseek|DeepSeek]]'s MoE architecture: 3B total parameters, ~570M activated via 6 routed experts + 2 shared experts out of 64 routed. This achieves ~3B expressive capacity at ~500M inference cost — matched deliberately to the compression paradigm's efficiency goals.

### Training Pipeline

Two-stage training:
1. **DeepEncoder pretraining**: independent next-token prediction with a compact LM on OCR 1.0/2.0 data plus 100M LAION samples
2. **End-to-end joint training**: SAM+compressor frozen (vision tokenizer), CLIP unfrozen (input embedding), MoE decoder trained jointly; 20 nodes × 8×A100-40G with PP=4

Training data breakdown (8,192-token sequence length):
- 70% OCR: 30M PDF pages (~100 languages), 20M natural scene samples, 10M synthetic HTML-table charts, 5M chemical formulas (SMILES), 1M geometry figures
- 20% general vision data
- 10% text-only data

---

## Results

### Compression-Accuracy Trade-off (Fox Benchmark)

The central empirical finding establishes that the 10× compression ratio is a meaningful threshold:

| Compression Ratio | OCR Precision |
|------------------|--------------|
| 9–10× | **96%+** |
| 10–12× | ~90% |
| ~20× (64 tokens) | ~60% |

Near-lossless recovery holds below 10×; degradation above this is attributed to layout complexity in longer documents and model capacity limits.

### OmniDocBench (Edit Distance, lower is better)

| Model | Vision Tokens | English (overall) |
|-------|-------------|------------------|
| MinerU2.0 | ~6,790 | 0.133 |
| DeepSeek-OCR (Gundam, ~795 tokens) | ~795 | **0.127** |
| DeepSeek-OCR (Large, 400 tokens) | 400 | 0.138 |
| Qwen2.5-VL-72B | ~4,000+ | 0.214 |
| InternVL3-78B | ~4,000+ | 0.218 |
| GOT-OCR2.0 | 256 | 0.287 |
| DeepSeek-OCR (Small, 100 tokens) | 100 | **0.221** |

Key comparisons:
- **100 vision tokens** outperforms GOT-OCR2.0's 256 tokens (2.56× token reduction)
- **~800 vision tokens** outperforms MinerU2.0's ~6,790 tokens (~8.5× token reduction)
- **400 tokens** matches Qwen2.5-VL-72B and InternVL3-78B despite being orders of magnitude smaller

### Production Throughput

- Single A100-40G: **200,000+ pages/day** of LLM/VLM training data
- 20-node cluster (160×A100-40G): **33 million pages/day**

This throughput makes DeepSeek-OCR a practical [[themes/synthetic_data_generation|synthetic data generation]] engine for pretraining pipelines.

---

## Capabilities

- **Vision-text optical compression** at 96%+ precision up to 10× ratio — near-lossless text recovery from images (maturity: demo)
- **Token-efficient document OCR** beating prior art at dramatically lower token budgets across benchmarks (maturity: narrow production)
- **Deep parsing** of heterogeneous content — charts, chemical formulas (SMILES), geometric figures, natural images — via prompt-controlled output (maturity: demo)
- **Multilingual OCR** across ~100 languages for PDF documents, with layout and non-layout output modes (maturity: narrow production)
- **Large-scale data generation** at 33M pages/day for [[themes/synthetic_data_generation|synthetic data]] pipelines (maturity: narrow production)

---

## Limitations & Open Questions

**Performance cliffs above 10× compression.** Precision drops from ~97% to ~60% between the 10× and 20× thresholds. Dense document types (newspapers, ~4,000–5,000 text tokens/page) consistently require Gundam or Gundam-M mode; the 10× regime is not achievable for these formats.

**Natural scene language gap.** Scene OCR supports only Chinese and English; ~100 language coverage applies only to PDF documents. This leaves major real-world deployment gaps.

**Geometry parsing remains unsolved.** The paper explicitly describes geometry parsing as "extremely challenging with a long way to go" due to complex interdependencies between line segments.

**No SFT stage.** The model is not a chatbot — capabilities require completion-mode prompts. This limits usability without additional post-training investment.

**Optical context compression is unvalidated for LLM inference.** The most speculative proposal — using rendered images of dialogue history as a compressed memory layer — has not been tested with interleaved digital-optical pretraining, needle-in-a-haystack evaluation, or actual conversational context. The paper acknowledges this explicitly and flags it as future work. This is the most consequential [[themes/long_context_and_attention|long-context]] claim, and it remains a proof-of-concept only.

**Financial report anomaly.** Gundam mode shows edit distance 0.289 on financial reports versus 0.022 in Large mode — a severe regression unexplained by compression ratio alone, suggesting layout-specific failure modes under high token budgets.

**Benchmark underestimation.** Reported Fox benchmark figures are systematically below true performance due to output format mismatch with ground truth annotations.

**Gundam-M co-training constraint.** The highest-resolution mode requires separate continued training rather than co-training with other modes, due to load balancing issues — a practical limitation for unified model deployment.

---

## Broader Significance

### Optical Context Compression as a Paradigm

The paper's most speculative but architecturally interesting proposal: render LLM dialogue history as images, compressing older context into progressively downscaled visual representations. This would implement a multi-level, biologically-inspired context decay — older contexts consuming exponentially fewer tokens. If validated through end-to-end pretraining, this would represent a qualitatively new approach to the [[themes/long_context_and_attention|quadratic scaling bottleneck]] in LLMs.

The claim that "compact language models can effectively learn to decode compressed visual representations through OCR-style training" suggests that this compression capability may be acquirable through pretraining design alone, not requiring architectural changes to the LLM itself. The implication for larger models is direct: existing frontier LLMs "could readily acquire similar capabilities through appropriate pretraining design."

### Encoder Architecture Findings

The DeepEncoder design implicitly resolves a previously uncharacterised design space gap: no existing open-source [[themes/vision_language_models|VLM]] encoder simultaneously supports high resolution, low activation memory, minimal output tokens, and multi-resolution flexibility. The serial window-then-global architecture with interposed convolutional compression is the key design primitive — it sequences the expensive operations rather than compounding them.

### Data Generation at Scale

The production throughput figures (33M pages/day) position DeepSeek-OCR as a strategic infrastructure component for [[themes/synthetic_data_generation|pretraining data pipelines]]. The compression efficiency directly enables training data generation at costs that tile-based or adaptive-resolution approaches cannot match.

---

## Related Themes

- [[themes/model_architecture|Model Architecture]] — DeepEncoder's serial window/global attention design
- [[themes/vision_language_models|Vision-Language Models]] — encoder architecture trade-offs and token efficiency
- [[themes/long_context_and_attention|Long Context & Attention]] — optical compression as alternative to architectural long-context solutions
- [[themes/multimodal_models|Multimodal Models]] — visual modality as a compression medium for text
- [[themes/adaptive_computation|Adaptive Computation]] — dynamic resolution modes with variable token budgets
- [[themes/synthetic_data_generation|Synthetic Data Generation]] — high-throughput OCR for pretraining pipelines
- [[themes/post_training_methods|Post-Training Methods]] — absence of SFT stage and its implications for deployment
