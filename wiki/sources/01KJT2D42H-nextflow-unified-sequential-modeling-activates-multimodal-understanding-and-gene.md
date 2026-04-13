---
type: source
title: 'NextFlow: Unified Sequential Modeling Activates Multimodal Understanding and
  Generation'
source_id: 01KJT2D42HR0GBX4E9N2KF3RMZ
source_type: paper
authors:
- Huichao Zhang
- Liao Qu
- Yiheng Liu
- Hang Chen
- Yangyang Song
- Yongsheng Dong
- Shikun Sun
- Xian Li
- Xu Wang
- Yi Jiang
- Hu Ye
- Bo Chen
- Yiming Gao
- Peng Liu
- Akide Liu
- Zhipeng Yang
- Qili Deng
- Linjie Xing
- Jiyang Liu
- Zhao Wang
- Yang Zhou
- Mingcong Liu
- Yi Zhang
- Qian He
- Xiwei Hu
- Zhongqi Qi
- Jie Shao
- Zhiye Fu
- Shuai Wang
- Fangmin Chen
- Xuezhi Chai
- Zhihua Wu
- Yitong Wang
- Zehuan Yuan
- Daniel K. Du
- Xinglong Wu
published_at: '2026-01-05 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# NextFlow: Unified Sequential Modeling Activates Multimodal Understanding and Generation

**Authors:** Huichao Zhang, Liao Qu, Yiheng Liu, Hang Chen, Yangyang Song, Yongsheng Dong, Shikun Sun, Xian Li, Xu Wang, Yi Jiang, Hu Ye, Bo Chen, Yiming Gao, Peng Liu, Akide Liu, Zhipeng Yang, Qili Deng, Linjie Xing, Jiyang Liu, Zhao Wang, Yang Zhou, Mingcong Liu, Yi Zhang, Qian He, Xiwei Hu, Zhongqi Qi, Jie Shao, Zhiye Fu, Shuai Wang, Fangmin Chen, Xuezhi Chai, Zhihua Wu, Yitong Wang, Zehuan Yuan, Daniel K. Du, Xinglong Wu
**Published:** 2026-01-05 00:00:00
**Type:** paper

## Analysis

# NextFlow: Unified Sequential Modeling Activates Multimodal Understanding and Generation
2026-01-05 · paper · Huichao Zhang, Liao Qu, Yiheng Liu, Hang Chen, Yangyang Song et al. (36 total)
https://arxiv.org/pdf/2601.02204

---

### Motivation & Prior Limitations
- The dominant paradigms for text reasoning (LLMs) and visual generation (diffusion models) remain largely separated, creating a fundamental architectural friction: diffusion models achieve pixel-level fidelity but lack logical reasoning and in-context learning, while traditional multimodal LLMs are restricted to perception with no generative capability.
  - AR-diffusion hybrids like Transfusion and Bagel showed early promise but rely on two different representations, imposing re-encoding overhead for interleaved tasks and potentially constraining deep multimodal integration.

- Pure autoregressive models (Chameleon, EMU3, EMU3.5) face a prohibitive efficiency bottleneck from raster-scan next-token prediction: visual token sequence length grows quadratically with resolution, making generation of a single 1024×1024 image take over 10 minutes — orders of magnitude slower than diffusion counterparts and impractical for interactive use.
  - This bottleneck is inherent to the paradigm, not an implementation artifact, since text's strictly sequential nature does not apply to the spatially hierarchical structure of images.

- Reconstruction-oriented VQ tokenizers used in prior pure-AR models optimize for pixel-level fidelity but produce discrete codes with low semantic density, creating a semantic gap that fundamentally limits multimodal understanding and alignment with the textual latent space.
  - This means prior unified AR models sacrifice comprehension quality to achieve generation capability, making the trade-off structurally unfavorable versus specialist models.

---

### Proposed Approach
- NextFlow is a unified decoder-only autoregressive transformer trained on 6 trillion interleaved text-image discrete tokens that resolves the modality mismatch by applying different prediction paradigms per modality: next-token prediction for text and next-scale prediction for visual generation.
  - Unlike raster-scan methods that flatten image tokens into a 1D sequence, next-scale prediction generates images hierarchically from coarse structural layouts to fine-grained details, exploiting the inherent spatial hierarchy of visual data.
  - This departs from prior pure-AR work and removes the need for a separate diffusion component, maintaining a single unified representation throughout.

- The tokenizer adopts a dual-codebook architecture (building on TokenFlow) that simultaneously learns semantic and pixel-level features via a shared-mapping mechanism, with quantization jointly constrained by both reconstruction fidelity and semantic consistency.
  - Unlike standard VQ-VAE trained on pixel reconstruction alone, this approach ensures discrete tokens encapsulate both high-level concepts (distilled from a semantic teacher) and fine-grained visual detail.
  - The semantic encoder is upgraded from siglip-so400m to siglip2-so400m-naflex to enable variable resolution and aspect ratio processing, allowing training at native resolutions without fixed input ratio constraints.

- NextFlow introduces a prefix-tuning strategy for Group Reward Policy Optimization (GRPO) that concentrates reinforcement learning updates on the coarse-scale "prefixes" that determine global image structure, stabilizing RL training across multi-scale generation.
  - This is a novel adaptation of RL fine-tuning for hierarchical autoregressive generation, addressing the instabilities that arise when applying standard RLHF techniques to next-scale prediction.

- An optional diffusion decoder can be attached post-hoc to refine the discrete autoregressive output for scenarios demanding hyper-realistic detail, without altering the unified base architecture or its reasoning capabilities.

---

### Results & Capabilities
- NextFlow generates 1024×1024 images in approximately 5 seconds, compared to over 10 minutes for raster-scan AR models at equivalent resolution, representing an orders-of-magnitude speedup within the pure autoregressive paradigm.
  - This is achieved with 6× fewer FLOPs during inference compared to MMDiT-based diffusion models at 1024² resolution, demonstrating a favorable compute-quality trade-off.

- The 7B parameter model achieves state-of-the-art performance among unified models on text-to-image benchmarks and rivals specialized diffusion baselines in visual quality without requiring a hybrid architecture.
  - On image editing, NextFlow outperforms specialized editing models, evaluated on the EditCanvas benchmark spanning local edits (object color, position, material, motion, outfit, size, inpainting, removal, rotation), global edits (color adjustment, background, lighting, modality conversion), style edits (real-to-unreal, unreal-to-real), text edits, and view edits.

- The unified architecture natively enables a broad set of multimodal capabilities beyond text-to-image: image editing, interleaved content generation, video generation, Chain-of-Thought reasoning to refine prompts before generation, and zero-shot image editing via in-context learning.
  - These capabilities emerge from the single shared discrete representation rather than requiring task-specific modules, suggesting the unified token space supports genuine cross-modal reasoning transfer.

---

### Implications
- NextFlow provides direct empirical evidence that a pure autoregressive architecture can match specialized diffusion models in visual quality without sacrificing the reasoning and in-context learning capabilities inherent to LLMs, challenging the prevailing assumption that hybrid AR-diffusion architectures are necessary for competitive unified models.

- The next-scale prediction paradigm, applied within a decoder-only transformer at 6T-token scale, suggests that the efficiency barrier of pu

## Key Claims

1. NextFlow is a unified decoder-only autoregressive transformer trained on 6 trillion interleaved text-image discrete tokens
2. NextFlow retains next-token prediction for text generation but adopts next-scale prediction for visual generation, departing from raster-scan methods
3. NextFlow generates 1024×1024 images in just 5 seconds, which is orders of magnitude faster than comparable autoregressive models
4. NextFlow achieves state-of-the-art performance among unified models and rivals specialized diffusion baselines in visual quality
5. Generating a single 1024×1024 image via raster-scan autoregression can take over 10 minutes, making pure AR models significantly slower than diffusion models
6. The sequence length of flattened visual tokens grows quadratically with image resolution, creating prohibitive computational cost for high-resolution AR generation
7. Reconstruction-oriented VQ tokenizers used in pure AR models optimize for pixel-level fidelity but the resulting discrete codes often lack high-level semantic density, limiting multimodal understandin
8. AR-Diffusion hybrid architectures impose re-encoding overheads for interleaved tasks and may fundamentally constrain deep multimodal integration due to relying on two different representations
9. NextFlow requires 6× fewer FLOPs during inference compared to MMDiT-based diffusion models at 1024×1024 resolution
10. NextFlow's 7B parameter model achieves competitive performance on text-to-image benchmarks and outperforms specialized models in image editing

## Capabilities

- Unified decoder-only autoregressive transformer performing multimodal understanding, image generation, image editing, interleaved content generation, and video generation in a single architecture without separate encoders
- High-resolution 1024×1024 image generation in 5 seconds via next-scale prediction in an autoregressive model — orders of magnitude faster than raster-scan AR approaches
- Unified AR model achieving 6× fewer inference FLOPs than MMDiT-based diffusion models at 1024×1024 resolution while matching visual quality
- Broad image editing in a unified AR model spanning local object edits (color, material, position, size, removal, addition), global edits (color, background, lighting, modality), style transfers, and camera view changes
- Chain-of-Thought reasoning applied to image generation — the model reasons over prompts before generating, improving generation quality through explicit deliberation
- In-context learning for zero-shot image editing — providing example edits as context enables novel editing operations without fine-tuning
- Dual-codebook tokenizer simultaneously achieving high-fidelity pixel reconstruction and semantically rich discrete representations, decoupling semantic and pixel-level features within a unified token space
- Interleaved text-image generation from a single unified autoregressive decoder without separate generation pathways or re-encoding overhead

## Limitations

- Pure discrete autoregressive tokens are insufficient for top-tier visual fidelity — an optional diffusion decoder is required to achieve 'hyper-realistic detail', revealing a quality ceiling for AR-only generation
- Multi-scale (next-scale) AR generation introduces training instabilities that require a specially designed, non-trivial training recipe to resolve
- RL training over autoregressive visual generation is unstable without special architectural interventions — standard GRPO cannot be applied directly to multi-scale generation
- Video generation capabilities are claimed but receive no evaluation, benchmark results, or qualitative examples in the paper — the actual quality and limitations are entirely unknown
- Unified AR model only 'rivals' specialized diffusion models in visual quality — it does not surpass them — indicating a persistent quality gap between unified and specialized architectures
- Training NextFlow requires 6 trillion tokens of interleaved text-image data — a massive data and compute requirement inaccessible to most researchers and organisations
- Standard VQ tokenizers used in prior pure-AR models (Chameleon, EMU3) produce discrete codes with low semantic density that fundamentally limit multimodal understanding performance
- AR-Diffusion hybrid architectures (Transfusion, Bagel) impose re-encoding overhead for interleaved tasks because they maintain two separate representations, constraining deep multimodal integration
- Raster-scan autoregressive generation scales quadratically with resolution — generating 1024×1024 images takes over 10 minutes — making prior pure-AR unified models impractical for interactive use
- The model's multimodal understanding performance on tasks requiring complex spatial reasoning, counting, or fine-grained localization is not benchmarked against frontier VLMs — results may not generalize beyond visual QA

## Bottlenecks

- Raster-scan next-token prediction for visual generation scales quadratically with resolution, blocking practical deployment of pure autoregressive unified multimodal models at interactive speeds
- Semantic-pixel representational gap in VQ tokenizers prevents unified AR models from achieving both high-quality visual generation and strong multimodal understanding in a single token space
- Training instabilities in hierarchical multi-scale generation prevent straightforward application of RL alignment techniques (GRPO/PPO) to unified visual generation models
- Discrete quantization ceiling in pure AR generation — the quality achievable without a continuous diffusion refinement stage remains below specialized diffusion model quality, constraining AR-only architectures

## Breakthroughs

- Next-scale prediction applied to unified autoregressive models reduces 1024×1024 image generation from 10+ minutes to 5 seconds — making pure AR unified models competitive with diffusion on inference speed
- A unified decoder-only autoregressive model outperforms specialized image editing models while rivaling top-tier diffusion models in generation quality — demonstrating that the quality-specialization tradeoff in multimodal AI is not fundamental

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]
- [[themes/video_and_world_models|video_and_world_models]]
- [[themes/vision_language_models|vision_language_models]]

## Key Concepts

- [[entities/bagel|Bagel]]
- [[entities/vq-vae|VQ-VAE]]
