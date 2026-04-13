---
type: source
title: 'Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction'
source_id: 01KJV9HBMYX34A6W0K3DX4JQ9V
source_type: paper
authors:
- Keyu Tian
- Yi Jiang
- Zehuan Yuan
- Bingyue Peng
- Liwei Wang
published_at: '2024-04-03 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- model_architecture
- pretraining_and_scaling
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction

**Authors:** Keyu Tian, Yi Jiang, Zehuan Yuan, Bingyue Peng, Liwei Wang
**Published:** 2024-04-03 00:00:00
**Type:** paper

## Analysis

# Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction
2024-04-03 · paper · Keyu Tian, Yi Jiang, Zehuan Yuan, Bingyue Peng, Liwei Wang
https://arxiv.org/pdf/2404.02905

---

### Motivation & Prior Limitations
Standard autoregressive (AR) image generation models flatten 2D image tokens into 1D raster-scan sequences, which introduces fundamental mathematical and structural problems that prevent them from reaching the quality and scalability of diffusion models.
- Raster-scan tokenization violates the unidirectional dependency assumption of AR models: VQVAE encoders produce feature maps with bidirectional inter-token correlations (confirmed empirically via attention heat maps in Appendix A), yet these are fed into models that assume each token depends only on its prefix.
- Flattening destroys spatial locality by severing the correlation between token q(i,j) and its four immediate spatial neighbors, which are no longer adjacent in the linear sequence.
- Conventional AR image generation requires O(n²) decoding iterations and O(n⁶) total computation for an n×n token map, making it prohibitively expensive compared to single-step GAN inference or multi-step but parallelizable diffusion sampling.
- Prior AR models (VQGAN, ViT-VQGAN, RQ-Transformer) substantially lagged diffusion models on ImageNet 256×256, with the best AR FID of ~3.04 (ViT-VQGAN with rejection sampling) versus DiT-XL/2 at 2.27, and scaling laws for visual AR models remained underexplored.
- The unidirectional nature of raster-scan AR prevents zero-shot generalization to tasks requiring bidirectional reasoning, such as predicting the top half of an image given the bottom half.

---

### Proposed Approach
VAR redefines autoregressive learning on images as "next-scale prediction" — each autoregressive step predicts an entire token map at the next higher resolution, not a single token — structured as a coarse-to-fine hierarchy from a 1×1 map up to full resolution.
- The autoregressive unit is a complete token map rk ∈ [V]^(hk×wk), and the joint likelihood is factored as p(r1,...,rK) = ∏p(rk | r1,...,rk-1), where each rk is generated in parallel conditioned on all coarser maps, respecting a strict prefix dependency that aligns with the residual encoding process.
- A new multi-scale VQVAE is developed using the VQGAN CNN architecture with a shared codebook (V=4096) across all scales and K extra convolution layers; encoding uses a residual design where each scale rk is quantized from the residual of the feature map after subtracting the contribution of all coarser scales, ensuring rk genuinely depends only on its prefix.
- The VAR transformer uses a GPT-2-style decoder-only architecture with adaptive layer normalization (AdaLN), a block-wise causal attention mask during training (each rk attends only to r≤k), and query/key normalization to unit vectors for training stability; no advanced LLM techniques (RoPE, SwiGLU, RMSNorm) are used.
- Within each autoregressive step, all hk×wk tokens of rk are predicted in parallel, reducing total generation complexity from O(n⁶) to O(n⁴) and the number of decoding iterations from O(n²) to O(log n).

---

### Results & Capabilities
VAR-d30 achieves FID 1.73 and IS 350.2 on ImageNet 256×256 class-conditional generation — the first time a GPT-style autoregressive model surpasses diffusion transformers on this benchmark — while running ~20× faster than VQGAN and ~45× faster than DiT-XL/2.
- Against the AR baseline (VQGAN, FID 18.65, IS 80.4), the switch to VAR alone (row 2 in ablation) drops FID to 5.22 at 0.013× the inference cost; the full VAR-d30 reaches FID 1.73, a 16.85-point improvement.
- VAR outperforms L-DiT-3B (FID 2.10) and L-DiT-7B (FID 2.28) with only 2B parameters, while DiT-XL/2 requires 1400 training epochs versus VAR's 350, establishing VAR as more data-efficient and compute-efficient.
- VAR exhibits clear power-law scaling laws across 12 model sizes from 18M to 2B parameters: test loss as a function of parameter count N follows L = (2.0·N)^(-0.23) with Pearson correlation -0.9993, and scaling laws with optimal training compute Cmin hold across 6 orders of magnitude with correlation -0.998.
- On ImageNet 512×512, VAR-d36 achieves FID 2.63 versus DiT-XL/2's 3.04, maintaining the quality advantage at higher resolution.
- VAR-d30 demonstrates zero-shot generalization to image in-painting, out-painting, and class-conditional editing by teacher-forcing ground-truth tokens outside the mask region, with no architecture modification or fine-tuning required.

---

### Implications
VAR's demonstration that an AR transformer can surpass diffusion models in image quality, speed, data efficiency, and scalability simultaneously suggests that the raster-scan ordering — not AR modeling itself — was the binding constraint on visual AR performance.
- The confirmation of LLM-style power-law scaling laws (correlation -0.998) for visual AR models means performance of large VAR models can now be reliably predicted from smaller runs, enabling rational compute allocation for visual generation at scale.
- VAR's architectural similarity to GPT-style LLMs positions it as a natural substrate for unified multimodal learning, particularly text-to-image generation via encoder-decoder or in-context integration with language models.
- The O(n⁴) complexity reduction and O(log n) decoding steps make VAR substantially more tractable for video generation than traditional AR models (which become prohibitively expensive at video resolutions), opening a credible path to "3D next-scale prediction" over spatiotemporal pyramids.
- The residual multi-scale VQVAE design — a shared codebook across all scales with scale-specific convolution projections — may inform tokenizer design for other modalities where hierarchical structure is natural.
- For representation learning, the coarse-to-fine prediction objective may induce stronger hierarchical representations than raster-scan AR, since the model must

## Key Claims

1. VAR is the first GPT-style autoregressive model to surpass diffusion transformers in image generation quality.
2. On ImageNet 256×256, VAR improves FID from 18.65 to 1.73 over the AR (VQGAN) baseline.
3. On ImageNet 256×256, VAR improves Inception Score from 80.4 to 350.2 over the AR (VQGAN) baseline.
4. VAR achieves approximately 20× faster inference speed compared to VQGAN-style AR models.
5. VAR with 2B parameters achieves FID 1.73 on ImageNet 256×256, surpassing L-DiT with 3B and 7B parameters.
6. VAR outperforms DiT in image quality (FID/IS), inference speed, data efficiency, and scalability.
7. VAR is more data-efficient than DiT-XL/2, requiring only 350 training epochs compared to DiT-XL/2's 1400.
8. DiT exhibits marginal or negative scaling gains beyond 675M parameters, while VAR shows consistent improvement.
9. VAR's scaling laws with optimal training compute Cmin hold across 6 orders of magnitude.
10. Larger VAR transformers are more compute-efficient because they reach the same performance level with less computation when trained with sufficient data.

## Capabilities

- Next-scale prediction autoregressive image generation achieving FID 1.73 on ImageNet 256×256 with 10 autoregressive steps, surpassing diffusion transformers (DiT) in image quality, inference speed, data efficiency, and scalability simultaneously
- Visual autoregressive models exhibit LLM-style power-law scaling laws — test loss declines predictably with model parameter count and training compute across 12 model sizes (18M to 2B parameters) and 6 orders of magnitude in compute, with Pearson correlation near -0.998
- Zero-shot generalization of visual AR models to downstream image tasks (inpainting, outpainting, class-conditional editing) without fine-tuning or architectural modification
- Coarse-to-fine next-scale prediction reduces visual AR generation complexity from O(n^6) to O(n^4) total compute and O(log n) autoregressive steps, achieving 20× wall-clock speedup over standard raster-scan AR while using more parameters

## Limitations

- VAR generates images class-conditionally only — natural language text prompts are not supported, blocking the dominant use case for practical text-to-image generation
- VQVAE tokenizer is unchanged from the VQGAN baseline — the fixed 16× spatial downsampling, shared codebook of 4096 entries, and training on OpenImages impose a hard quality ceiling that transformer scaling cannot overcome
- Video generation is entirely unimplemented — the temporal dimension is absent from VAR's multi-scale paradigm
- All results are from ImageNet class-conditional benchmarks — generalization to open-domain, diverse, or compositional generation settings is entirely undemonstrated
- Higher-resolution (512×512) synthesis required architectural compromise — a single shared AdaLN layer replaces per-block normalization due to memory constraints, reducing parameter count from ~73728d³ to ~49152d³
- Even at 2B parameters, token error rates remain extremely high (89–97%) — the vast majority of individual tokens are mispredicted, with quality emerging only from the multi-scale ensemble
- VAR retains unidirectional coarse-to-fine dependency — bidirectional spatial reasoning tasks (e.g., predicting the top of an image from the bottom) remain architecturally impossible
- Advanced LLM architectural components (RoPE, SwiGLU, RMSNorm) are conspicuously absent — reported results likely understate VAR's ceiling, and the gap vs. modern transformer architectures is uncharacterized
- Training cost for VAR is not compared against diffusion model training costs — the claim of data efficiency (350 vs 1400 epochs) refers to epochs not wall-clock or FLOPs, and two-stage training (VQVAE + transformer) compound cost is not reported
- Safety, adversarial robustness, and content safety of VAR outputs are entirely unaddressed despite releasing models and code publicly for high-quality realistic image generation

## Bottlenecks

- VQVAE tokenizer architecture is the binding quality constraint for visual AR models — the fixed 16× downsampling, 4096-entry codebook, and VQGAN architecture impose a hard reconstruction ceiling that next-scale prediction cannot bypass
- Absence of text conditioning in visual AR models — VAR's class-conditional architecture has no mechanism for natural language prompts, blocking deployment in the dominant text-to-image paradigm

## Breakthroughs

- Next-scale prediction makes GPT-style autoregressive models surpass diffusion transformers in image generation for the first time — resolving the fundamental computational and structural pathologies of raster-scan AR
- Visual autoregressive models exhibit LLM-style power-law scaling laws — confirmed across 12 model sizes and 6 orders of magnitude in training compute with near-perfect fit (r = -0.998), establishing visual generation as a scalable paradigm analogous to language modeling

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/model_architecture|model_architecture]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/adaptive-layer-normalization-adaln|Adaptive Layer Normalization (AdaLN)]]
- [[entities/diffusion-transformer-dit|Diffusion Transformer (DiT)]]
