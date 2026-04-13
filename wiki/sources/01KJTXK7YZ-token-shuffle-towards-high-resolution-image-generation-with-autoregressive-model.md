---
type: source
title: 'Token-Shuffle: Towards High-Resolution Image Generation with Autoregressive
  Models'
source_id: 01KJTXK7YZ20KP3N0AWEKT84NH
source_type: paper
authors:
- Xu Ma
- Peize Sun
- Haoyu Ma
- Hao Tang
- Chih-Yao Ma
- Jialiang Wang
- Kunpeng Li
- Xiaoliang Dai
- Yujun Shi
- Xuan Ju
- Yushi Hu
- Artsiom Sanakoyeu
- Felix Juefei-Xu
- Ji Hou
- Junjiao Tian
- Tao Xu
- Tingbo Hou
- Yen-Cheng Liu
- Zecheng He
- Zijian He
- Matt Feiszli
- Peizhao Zhang
- Peter Vajda
- Sam Tsai
- Yun Fu
published_at: '2025-04-24 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- long_context_and_attention
- model_architecture
- multimodal_models
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Token-Shuffle: Towards High-Resolution Image Generation with Autoregressive Models

**Authors:** Xu Ma, Peize Sun, Haoyu Ma, Hao Tang, Chih-Yao Ma, Jialiang Wang, Kunpeng Li, Xiaoliang Dai, Yujun Shi, Xuan Ju, Yushi Hu, Artsiom Sanakoyeu, Felix Juefei-Xu, Ji Hou, Junjiao Tian, Tao Xu, Tingbo Hou, Yen-Cheng Liu, Zecheng He, Zijian He, Matt Feiszli, Peizhao Zhang, Peter Vajda, Sam Tsai, Yun Fu
**Published:** 2025-04-24 00:00:00
**Type:** paper

## Analysis

# Token-Shuffle: Towards High-Resolution Image Generation with Autoregressive Models
2025-04-24 · paper · Xu Ma, Peize Sun, Haoyu Ma, Hao Tang, Chih-Yao Ma et al. (25 total)
https://arxiv.org/pdf/2504.17789

---

### Motivation & Prior Limitations
- Autoregressive (AR) models operating on discrete visual tokens face a quadratic scaling wall with image resolution, making high-resolution generation prohibitively expensive or practically infeasible within the next-token prediction paradigm.
  - A 1024×1024 image requires ~4K visual tokens with a standard 16× downsampling VQGAN tokenizer; scaling to 2048×2048 multiplies this to ~16K tokens, making both training and inference impractical given Transformer's O(n²) attention complexity.
  - Prior AR text-to-image MLLMs such as LlamaGen, Chameleon, and EMU3 were therefore limited to low- or medium-resolution outputs, ceding quality and resolution to diffusion-based models.
- The standard practice of directly appending a VQGAN codebook (typically 256-dimensional vectors) to the LLM vocabulary (3072–4096 dimensions) introduces severe dimensional redundancy in visual token representations that prior work ignored entirely.
  - An empirical study with squeeze-and-expand MLP layers shows that visual vocabulary rank can be compressed by up to 8× with only minimal increase in pretraining loss, confirming this redundancy is exploitable.
- Existing efficient Transformer methods (linear attention, state-space models, long-context optimizations) either require architectural modifications that abandon off-the-shelf LLMs or are optimized for language without leveraging image-specific spatial structure.

---

### Proposed Approach
- Token-Shuffle introduces a plug-and-play pair of operations — token-shuffle and token-unshuffle — that exploit visual vocabulary dimensional redundancy to merge spatially local visual tokens along the channel dimension before Transformer computation and recover them afterward, reducing visual token count by s² for a window size s without discarding information.
  - Unlike aggressive compression or learned resampling schemes (e.g., the Re-sampler in SEED-X), Token-Shuffle preserves all fine-grained spatial information by fusing it into higher-dimensional channel representations, then disentangling it post-Transformer rather than permanently discarding tokens.
  - Concretely, a shared MLP compresses each visual token's dimension from d to d/s², then s×s neighboring tokens are channel-concatenated into a single token, reducing sequence length from n to n/s²; Token-Unshuffle reverses this with a symmetric MLP after the Transformer blocks. Residual MLP blocks are added to both operations, and n=2 MLP blocks per operation is found sufficient.
  - The method is architecture-agnostic (demonstrated on LLaMA 2.7B), requires no additional pretrained text encoder, and preserves the standard causal autoregressive next-token-prediction framework — the model predicts a fused token representing a local s×s window of visual tokens simultaneously.
- A complementary CFG scheduler (half-linear by default) is introduced to address an artifact unique to AR generation: early unconditional logits are fixed by the two system tokens, causing small errors that accumulate autoregressively, which the scheduler suppresses by ramping CFG scale from 1 to the target value over the first half of the visual token sequence.
- Training follows a three-stage curriculum: 512×512 without Token-Shuffle (50B tokens), then 1024×1024 with Token-Shuffle (2TB tokens), then 2048×2048 fine-tuning (~300B tokens) with z-loss added to stabilize gradient behavior at very high resolution.

---

### Results & Capabilities
- Token-Shuffle (2.7B, s=2) achieves a VQAScore of 0.77 on GenAI-Bench hard prompts, outperforming the prior best pure AR model LlamaGen by 0.18 and the diffusion baseline LDM by 0.15, and matching DALL-E 3 (0.70) with superior hard-prompt performance.
  - On "basic" prompts the model scores 0.88, matching DALL-E 3 (0.89) and exceeding all other AR models including EMU3 (0.78) and Lumina-mGPT-7B (0.84).
- On GenEval the 2.7B model achieves an overall score of 0.62, competitive with SD3 (0.62) and EMU3 (0.66) at similar or smaller parameter count, and outperforming prior AR-only baselines including LlamaGen (0.32) and Chameleon (0.39).
- For the first time, an autoregressive model is demonstrated generating coherent 2048×2048 images, a resolution that was previously impractical under next-token prediction due to the 16K token requirement.
  - With s=2, Token-Shuffle reduces training FLOPs and token count by ~4× (saving ~75% of visual tokens), and inference time scales roughly linearly with token count due to KV-cache, enabling 1024×1024 generation at roughly the same cost as a baseline 512×512 model.
- Large-scale human evaluation confirms Token-Shuffle outperforms LlamaGen and Lumina-mGPT on text alignment, visual flaws, and visual appearance, and achieves comparable or superior visual appearance and text alignment versus LDM.

---

### Implications
- Token-Shuffle demonstrates that the gap between AR and diffusion models in image generation quality is largely attributable to token count constraints rather than fundamental architectural inferiority, and that exploiting representational redundancy inherent in cross-modal vocabulary design is a viable path to closing it.
- The plug-and-play nature of the method means it can be applied to existing MLLM stacks (any LLaMA-family model with a VQGAN tokenizer) without modifying attention mechanisms, enabling the broader community to upgrade AR image generators without re-architecting from scratch.
- Unifying high-resolution image generation within the standard next-token prediction framework — without separate diffusion decoders or text encoders — strengthens the case for a single autoregressive model handling both language and vision tasks, which is a central design goal for real-world MLLM deployments (e.g., EMU3, Chamele

## Key Claims

1. Autoregressive models are often considered less competitive than diffusion-based models for image synthesis, with a primary limitation being the substantial number of image tokens required.
2. Visual vocabularies in MLLMs have inherent dimensional redundancy because low-dimensional visual codes from the visual encoder are directly mapped to high-dimensional language vocabularies.
3. Token-Shuffle reduces visual token count by a factor of s² (approximately 75% with shuffle window size s=2), achieving a ~4x reduction in training FLOPs.
4. Token-Shuffle is the first method to push autoregressive text-to-image generation to a resolution of 2048×2048.
5. Token-Shuffle's 2.7B model achieves a VQAScore of 0.77 on GenAI-Bench hard prompts, outperforming AR model LlamaGen by 0.18 and diffusion model LDM by 0.15.
6. Generating a 1024×1024 image requires 4K visual tokens with a downsample-16 tokenizer, and a 2048×2048 image requires 16K tokens, making the latter impractical for next-token prediction.
7. Visual vocabulary embedding dimension can be compressed by up to a factor of 8 without significantly impacting generation quality.
8. Typical VQGAN codebook vector dimensions are low (e.g., 256), but directly appending these to LLM vocabularies inflates dimensions to 3072, 4096, or higher, introducing dimensional redundancy.
9. Token-Shuffle requires no additional pretrained text-encoder and enables MLLMs to support high-resolution image synthesis in a unified next-token prediction framework.
10. Inference time for AR models with KV-cache scales roughly linearly with token number, so Token-Shuffle's token reduction directly translates to proportional inference speedup.

## Capabilities

- Autoregressive text-to-image generation at 2048×2048 resolution using Token-Shuffle token compression in a 2.7B MLLM, achieving 0.77 VQAScore on GenAI-bench hard prompts and outperforming diffusion models including LDM
- Channel-dimension token merging (Token-Shuffle) reduces visual token count by ~75% at shuffle window size 2, achieving ~4x reduction in training FLOPs with roughly linear inference scaling via KV-cache
- Unified MLLM performing high-resolution text-to-image generation under pure next-token prediction without a separate frozen text encoder, by exploiting dimensional redundancy in visual vocabulary embeddings
- Visual vocabulary dimension in MLLMs can be compressed up to 8x with minimal generation quality loss, demonstrating that low-dimensional visual codes mapped into high-dimensional LLM vocabulary spaces carry substantial redundancy

## Limitations

- AR image generation models produce significantly more visual flaws (incomplete bodies, extra limbs, logical inconsistencies) than diffusion models even with Token-Shuffle improvements
- Training AR image models at very high resolutions (2048×2048) is inherently unstable — loss and gradient values increase unexpectedly, requiring special stabilisation techniques (z-loss) that are not standard practice
- Token-Shuffle quality degrades visibly at larger shuffle window sizes — window size 4 introduces noticeable blurring, imposing a hard efficiency-fidelity tradeoff that cannot currently be closed with extended training alone
- Discrete visual token AR models are architecturally inferior in generation quality to continuous token approaches, and this gap is a fundamental property of vector quantisation information loss rather than a tuning issue
- Despite 4x token reduction via Token-Shuffle, 2048×2048 AR training still requires approximately 300B tokens across multi-stage training after 2TB at 1024×1024 — compute costs remain prohibitive outside large labs
- AR image models including Token-Shuffle have a substantial performance gap on compositional counting and fine-grained attribute binding — GenEval scores of 0.37 on counting and 0.39 on color attribution compared to 0.96 on single object generation
- Standard CFG implementation from diffusion models causes error accumulation in AR image generation — fixed unconditional first-token logits produce artifacts that compound sequentially through the entire token sequence
- Token-Shuffle model performance is highly sensitive to prompt format — VQAScore drops from 0.77 to 0.67 (13% degradation) when using original benchmark prompts vs Llama3-rewritten long prompts, revealing a training-inference distribution mismatch
- No absolute wall-clock inference time is reported for 2048×2048 generation — the paper discusses FLOPs and token counts but omits seconds-per-image comparisons against diffusion baselines, making practical deployment suitability unverifiable
- Token-Shuffle is validated exclusively on a 2.7B Llama model — no evidence of generalisability to other scales, non-Llama architectures, or video/3D modalities where the dimensional redundancy property may differ

## Bottlenecks

- Quadratic scaling of visual token count with image resolution remains a hard constraint for AR image generation — Token-Shuffle provides constant-factor relief but going beyond 2048×2048 would require 64K+ tokens which are impractical even with compression
- VQ-based visual tokenizers with fixed 16x downsampling and 256-dimensional codebooks impose a hard ceiling on reconstruction fidelity that is independent of AR model capacity — larger models cannot recover detail lost at tokenisation
- Training instability at high resolutions for AR image generation blocks reliable scaling of AR models above 1024×1024 without specialised stabilisation techniques that are not yet standardised

## Breakthroughs

- Token-Shuffle enables AR text-to-image generation at 2048×2048 resolution for the first time, by exploiting dimensional redundancy in MLLM visual vocabularies to reduce token count 4x — achieving parity with or superiority to diffusion models on text-alignment benchmarks with a 2.7B model

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/geneval|GenEval]]
- [[entities/llama|LLaMA]]
- [[entities/z-loss|z-loss]]
