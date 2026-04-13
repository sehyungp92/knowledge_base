---
type: source
title: Kimi-VL Technical Report
source_id: 01KJTPMJBF37SDX28VSNECG0AW
source_type: paper
authors:
- Kimi Team
- Angang Du
- Bohong Yin
- Bowei Xing
- Bowen Qu
- Bowen Wang
- Cheng Chen
- Chenlin Zhang
- Chenzhuang Du
- Chu Wei
- Congcong Wang
- Dehao Zhang
- Dikang Du
- Dongliang Wang
- Enming Yuan
- Enzhe Lu
- Fang Li
- Flood Sung
- Guangda Wei
- Guokun Lai
- Han Zhu
- Hao Ding
- Hao Hu
- Hao Yang
- Hao Zhang
- Haoning Wu
- Haotian Yao
- Haoyu Lu
- Heng Wang
- Hongcheng Gao
- Huabin Zheng
- Jiaming Li
- Jianlin Su
- Jianzhou Wang
- Jiaqi Deng
- Jiezhong Qiu
- Jin Xie
- Jinhong Wang
- Jingyuan Liu
- Junjie Yan
- Kun Ouyang
- Liang Chen
- Lin Sui
- Longhui Yu
- Mengfan Dong
- Mengnan Dong
- Nuo Xu
- Pengyu Cheng
- Qizheng Gu
- Runjie Zhou
- Shaowei Liu
- Sihan Cao
- Tao Yu
- Tianhui Song
- Tongtong Bai
- Wei Song
- Weiran He
- Weixiao Huang
- Weixin Xu
- Xiaokun Yuan
- Xingcheng Yao
- Xingzhe Wu
- Xinhao Li
- Xinxing Zu
- Xinyu Zhou
- Xinyuan Wang
- Y. Charles
- Yan Zhong
- Yang Li
- Yangyang Hu
- Yanru Chen
- Yejie Wang
- Yibo Liu
- Yibo Miao
- Yidao Qin
- Yimin Chen
- Yiping Bao
- Yiqin Wang
- Yongsheng Kang
- Yuanxin Liu
- Yuhao Dong
- Yulun Du
- Yuxin Wu
- Yuzhi Wang
- Yuzi Yan
- Zaida Zhou
- Zhaowei Li
- Zhejun Jiang
- Zheng Zhang
- Zhilin Yang
- Zhiqi Huang
- Zihao Huang
- Zijia Zhao
- Ziwei Chen
- Zongyu Lin
published_at: '2025-04-10 00:00:00'
theme_ids:
- adaptive_computation
- long_context_and_attention
- model_architecture
- multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Kimi-VL Technical Report

Kimi-VL is an efficient open-source [[themes/multimodal_models|Multimodal]] [[themes/model_architecture|Mixture-of-Experts]] vision-language model from Moonshot AI that integrates native-resolution visual encoding, 128K long-context processing, and RL-trained long chain-of-thought reasoning into a single ~3B activated parameter family — a combination previously absent from the open-source ecosystem. The report documents training methodology, architectural innovations (MoonViT, Muon optimizer, 4D parallelism), and benchmark results across 24 multimodal tasks, including SOTA open-source performance on computer-use agents, OCR, long video, and long document understanding.

**Authors:** Kimi Team et al. (95 total)
**Published:** 2025-04-10
**Type:** Paper
**Themes:** [[themes/adaptive_computation|Adaptive Computation]] · [[themes/long_context_and_attention|Long Context & Attention]] · [[themes/model_architecture|Model Architecture]] · [[themes/multimodal_models|Multimodal Models]] · [[themes/vision_language_models|Vision-Language Models]]

---

## Motivation

Open-source VLMs have lagged significantly behind language-only counterparts on two fronts: architectural efficiency and advanced reasoning. Dense-architecture models like Qwen2.5-VL and Gemma-3 offer no long chain-of-thought support; MoE-based VLMs like DeepSeek-VL2 and Aria addressed efficiency but introduced their own constraints — a 4K context ceiling, weak fine-grained visual tasks, and fixed-size vision encoders incapable of handling variable-aspect-ratio or ultra-high-resolution inputs.

The core gap: no open-source VLM had simultaneously achieved MoE structural efficiency, native-resolution visual encoding, 128K context, and RL-trained reasoning in a single unified family.

---

## Architecture

### MoonViT — Native-Resolution Vision Encoder

MoonViT is a 400M-parameter vision encoder initialized from SigLIP-SO-400M and purpose-built to eliminate sub-image splitting. Images are divided into patches, flattened, and packed into 1D sequences using NaViT-style packing — fully compatible with FlashAttention and variable-length sequence attention. This handles arbitrary resolutions and aspect ratios without tiling artifacts.

Positional encoding combines two mechanisms:
- **Interpolated SigLIP absolute positional embeddings** — preserves pre-trained spatial priors but degrades at high resolution
- **2D RoPE** across height and width dimensions — compensates for the breakdown of interpolated fixed embeddings, maintaining fine-grained spatial encoding at scale

In Kimi-VL-A3B-Thinking-2506, MoonViT is further trained to encode up to **3.2 million pixels per image** — 4× the original limit.

### Language Decoder — Moonlight MoE

The language decoder is the Moonlight MoE model: **2.8B activated / 16B total parameters**, architecturally similar to DeepSeek-V3. It is initialized from an intermediate checkpoint after 5.2T tokens of pure text pre-training with an 8K context window, then further trained on 2.3T multimodal tokens.

### MLP Projector

A two-layer MLP bridges MoonViT and the language decoder. It applies **2×2 pixel shuffle downsampling** to compress spatial features before projecting to LLM embedding dimensionality — reducing token count for common-resolution images while preserving fidelity for high-resolution inputs.

---

## Training

### Pre-training (4 stages, 4.4T tokens total)

| Stage | Tokens | Purpose |
|---|---|---|
| ViT Training | 2T + 0.1T | Standalone CoCa-style SigLIP + caption pre-training; OCR capability emergence observed during OCR data scaling |
| Joint Pre-training | 1.4T | Progressive multimodal data ratio increase |
| Joint Cooldown | 0.6T | High-quality synthetic QA pairs for math, code, knowledge — yields significant downstream reasoning gains |
| Joint Long-context Activation | ~0.3T | Two sub-stages, each 4× context extension; RoPE base reset from 50K → 800K; 8K → 128K; 25%/75% long/short data mix including multimodal long data |

A key empirical finding: synthetic data (QA pairs for math, knowledge, code) incorporated during cooldown yields significant performance improvements, but **synthetic caption data must be strictly limited** to mitigate hallucination risk from insufficient real-world grounding.

### Post-training — Kimi-VL-Thinking

Two additional stages produce the reasoning variant:
1. **Long-CoT SFT** on rejection-sampled reasoning trajectories generated by Kimi k1.5
2. **Online RL** using policy mirror descent with binary correctness reward, plus a **length penalty** to suppress overthinking (redundant chains without accuracy gain)

RL training uses curriculum and prioritized sampling based on per-instance difficulty and success rate.

### Infrastructure

- **Muon optimizer** (enhanced with weight decay and per-parameter update scaling) applied uniformly to all parameters — vision encoder, projector, and language model
- **4D parallelism**: Data Parallelism + Expert Parallelism + Pipeline Parallelism + Context Parallelism, combined with ZeRO-1 and selective activation recomputation
- Result: ~60% higher training throughput than a comparable 7B dense VLM

---

## Capabilities

### Reasoning
- Kimi-VL-Thinking achieves **36.8% on MathVision** (+15.4% over base), **70.9% on MathVista**, with clear test-time scaling: MathVision rises from 18.7% at 1K thinking tokens to 36.8% at 16K
- Kimi-VL-Thinking-2506 pushes further: **56.9% MathVision** (+20.1%), **80.1% MathVista**, **64.0% MMMU**, **65.2% VideoMMMU** — matching 30B-scale dense VLMs on reasoning benchmarks with ~3B activated parameters
- Output token efficiency also improves in 2506: ~20% reduction in average output length (e.g., MathVision: 5.8K → 4.4K tokens) while improving accuracy — demonstrating that efficiency and quality can co-improve with continued RL training

### Long-Context Understanding
- **LongVideoBench: 64.5%** (vs. Qwen2.5-VL-7B: 56.0%)
- **MMLongBench-Doc: 42.1%** (2506 variant — first open-source model matching GPT-4o)
- Near-perfect NIAH recall up to 65K tokens; 87–92% at 65K–128K range

### OCR & Document Understanding
- **InfoVQA: 83.2%** (surpassing GPT-4o's 80.7%)
- **OCRBench: 86.7%** (surpassing all compared models)
- Handles multilingual text, dense layouts, LaTeX math, financial tables, and handwritten text

### Computer-Use Agents
- **OSWorld: 8.22%** (vs. GPT-4o: 5.03%)
- **WindowsAgentArena: 10.4%** (vs. GPT-4o: 9.4%)
- **ScreenSpot-Pro: 34.5%** on 4K screen grounding

### Video Understanding
- **EgoSchema: 78.5%** (vs. GPT-4o: 72.2%)
- **VSI-Bench: 37.4%** (vs. GPT-4o: 34.0%)
- **MLVU-MCQ: 74.2%** (vs. GPT-4o: 64.6%)

---

## Limitations & Open Questions

### Performance Ceilings

**Autonomous GUI tasks remain below 10% success.** OSWorld at 8.22% means approximately 9 in 10 real-world computer tasks fail even at SOTA open-source performance. This blocks practical deployment of computer-use automation for non-trivial workflows requiring multi-step GUI navigation, state tracking, and error recovery. *(severity: blocking)*

**MMMU gap persists.** The base model scores 57.0% vs. GPT-4o's 69.1% — a 12-point gap on complex academic visual reasoning. The 2506 thinking variant reaches 64.0%, closing the gap substantially but not fully. *(severity: significant)*

**Long document understanding still trails proprietary.** MMLongBench-Doc at 35.1% (base) lags GPT-4o's 42.8% by 7+ points. Multi-page (100+) document reasoning remains challenging at sub-10B activated parameter scale — though 2506 closes this gap to parity. *(severity: significant)*

**ScreenSpot-Pro at 34.5%** means GUI element localization fails in approximately 2 of 3 cases on 4K professional displays. *(severity: significant)*

### Architectural Constraints

**NIAH recall degrades at maximum context.** Recall drops to 87.0% (text) and 91.7% (video) at 65K–131K token range despite explicit long-context training — reliability degrades precisely where it matters most for very long documents. *(severity: significant)*

**Interpolated absolute positional embeddings break at high resolution.** The need to replace SigLIP's absolute PEs with 2D RoPE reveals a fundamental limitation of transfer from pre-trained vision encoders — spatial encoding quality degrades predictably beyond the pre-training resolution. *(severity: significant)*

**Synthetic caption ceiling.** Synthetic caption data must be strictly constrained to avoid hallucination, creating a practical ceiling on data augmentation via synthesis for VLM pre-training. *(severity: significant)*

### Test-Time Scaling Saturation

**Task-dependent saturation.** MathVista saturates at ~4K thinking tokens (70.9%) with no further gain — extended reasoning does not uniformly benefit all task types. This is an important calibration signal for when long-CoT compute is being wasted. *(severity: significant)*

**Overthinking failure mode.** Long-CoT RL training induces redundant reasoning chains without accuracy gain. The length penalty is a symptomatic fix; the underlying tendency to over-generate remains a structural concern. *(severity: significant)*

### Reproducibility & Safety

**Infrastructure barrier.** Reproducing Kimi-VL requires 4D parallelism infrastructure, a custom distributed Muon optimizer, and cloud-scale storage — creating a substantial barrier for community researchers outside well-resourced labs. *(severity: significant)*

**No safety evaluation.** The report contains no discussion of adversarial robustness, jailbreak resistance, bias analysis, or safety evaluation — a conspicuous absence for a production-released VLM capable of autonomous computer use. *(severity: significant)*

**Deployment efficiency undisclosed.** Inference latency, throughput, and deployment cost metrics are absent, leaving the actual production efficiency of the MoE architecture (vs. dense equivalents) undisclosed.

---

## Landscape Significance

### Breakthroughs

**Efficient reasoning at scale.** RL-trained long-CoT on a ~3B activated MoE VLM achieves reasoning scores matching 30B-scale dense VLMs. This directly challenges the assumption that deep multimodal reasoning requires massive activated parameter counts — demonstrating that [[themes/adaptive_computation|architectural efficiency]] and reasoning depth are not in conflict.

**Native-resolution vision encoding.** MoonViT's 2D RoPE approach eliminates sub-image splitting and enables end-to-end processing up to 3.2M pixels at arbitrary aspect ratios in a single forward pass — a meaningful architectural step toward treating images as first-class continuous inputs rather than pre-processed tiles.

### Bottlenecks Addressed (Partially)

- [[themes/vision_language_models|Open-source VLM]] reasoning parity with proprietary models: substantially reduced but not closed (MMMU: 57% → 64% with thinking, vs. GPT-4o 69.1%)
- MoE VLM training accessibility: model weights released, but 4D parallelism infrastructure remains a practical barrier to community iteration
- [[themes/long_context_and_attention|Long-context]] multimodal understanding: 128K context with competitive NIAH performance established as feasible at efficient parameter scales

### Bottlenecks Remaining

- **Autonomous GUI task completion** below 10% blocks practical computer-use deployment (horizon: 1–2 years)
- **Efficient open-source VLMs matching frontier proprietary models** on complex academic reasoning without RL test-time compute (horizon: 1–2 years)
- **Broad community reproducibility** of MoE+native-resolution+RL-reasoning systems outside industrial labs (horizon: months)

---

## Key Claims

1. MoE VLM (2.8B activated / 16B total) outperforms dense VLMs with 2–4× more activated parameters on 19 of 24 benchmarks, including surpassing GPT-4o on OCR (InfoVQA), video understanding (EgoSchema, VSI-Bench), and computer-use (OSWorld).
2. Native-resolution processing via NaViT packing + 2D RoPE eliminates sub-image splitting artifacts while handling up to 3.2M pixels per image.
3. 4-stage pre-training (4.4T tokens) with joint long-context activation (8K → 128K) enables near-perfect multimodal NIAH recall up to 65K tokens.
4. RL-trained long-CoT produces clear test-time scaling on MathVision (18.7% → 36.8% across 1K–16K tokens) but saturates on simpler tasks (MathVista: 4K tokens sufficient).
5. Synthetic QA data in cooldown phase significantly improves math/knowledge/code reasoning; synthetic caption data must be strictly limited to avoid hallucination.
6. 4D parallelism yields ~60% higher training throughput than 7B dense VLM equivalents — but requires specialized infrastructure inaccessible to most community researchers.
7. Continued MoonViT training in 2506 variant recovers capabilities degraded by long-CoT RL (perception, video, OS-agent tasks) while simultaneously reducing output token length by ~20%.

## Key Concepts

- [[entities/flashattention|FlashAttention]]
- [[entities/muon-optimizer|Muon Optimizer]]
- [[entities/context-parallelism|context parallelism]]
