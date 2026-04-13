---
type: source
title: 'Mixture of States: Routing Token-Level Dynamics for Multimodal Generation'
source_id: 01KJT8TG9RW6XR51A552X9NM5B
source_type: paper
authors:
- Haozhe Liu
- Ding Liu
- Mingchen Zhuge
- Zijian Zhou
- Tian Xie
- Sen He
- Yukang Yang
- Shuming Liu
- Yuren Cong
- Jiadong Guo
- Hongyu Xu
- Ke Xu
- Kam-Woh Ng
- Juan C. Pérez
- Juan-Manuel~Pérez-Rúa
- Tao Xiang
- Wei Liu
- Shikun Liu
- Jürgen Schmidhuber
published_at: '2025-11-15 00:00:00'
theme_ids:
- adaptive_computation
- generative_media
- image_generation_models
- model_architecture
- multimodal_models
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Mixture of States: Routing Token-Level Dynamics for Multimodal Generation

**Authors:** Haozhe Liu, Ding Liu, Mingchen Zhuge, Zijian Zhou, Tian Xie, Sen He, Yukang Yang, Shuming Liu, Yuren Cong, Jiadong Guo, Hongyu Xu, Ke Xu, Kam-Woh Ng, Juan C. Pérez, Juan-Manuel~Pérez-Rúa, Tao Xiang, Wei Liu, Shikun Liu, Jürgen Schmidhuber
**Published:** 2025-11-15 00:00:00
**Type:** paper

## Analysis

# Mixture of States: Routing Token-Level Dynamics for Multimodal Generation
2025-11-15 · paper · Haozhe Liu, Ding Liu, Mingchen Zhuge, Zijian Zhou, Tian Xie et al. (19 total)
https://arxiv.org/pdf/2511.12207

---

### Motivation & Prior Limitations
- Prior multimodal fusion methods rely on fixed, hand-crafted cross-modal interaction schemes that fail to exploit the full representational richness of text encoders and ignore the dynamic nature of the diffusion process.
  - Cross-attention methods (e.g., Stable Diffusion) provide only the final-layer text embedding to the visual branch, discarding all intermediate layer representations from the text encoder.
  - Self-attention methods (e.g., Flux, SD3) concatenate text and visual tokens into a unified sequence, achieving richer fusion but at quadratic computational cost with combined sequence length.
  - Mixture-of-Transformers (MoT) designs (e.g., Bagel, LMFusion) enable finer-grained layer-wise interactions but impose a hard architectural constraint: both text and visual towers must have identical depths and hidden dimensions, enforcing rigid one-to-one block correspondence.
- All dominant approaches encode text once and provide a static conditional signal to the diffusion model, creating a fundamental "information mismatch" with the dynamic, timestep-varying nature of the denoising process.
  - Ablations confirm that routing using only the static prompt embedding is strictly worse than conditioning on the full dynamic state (prompt + noised latent + timestep), yielding higher FID and lower CLIP scores.
- Fixed layer selection — whether always using the final text layer (cross-attention) or symmetric layer pairing (MoT) — is experimentally suboptimal, with no evidence that diffusion models consume language features in a layer-aligned manner.

---

### Proposed Approach
- MoS (Mixture of States) introduces a learnable, token-wise router that creates sparse, dynamic connections between any layer of a frozen understanding tower and any layer of a trainable generation tower, adapting both to the current input and to the denoising timestep.
  - Unlike MoT's global attention-based sharing (which requires symmetric towers), MoS uses hidden states — full layer-level activations — as the unit of inter-model transfer, making it compatible with asymmetric transformers of arbitrary depth and width.
  - The router takes as input the text prompt embedding, the noised image latent $z_t$, and the sinusoidal timestep embedding, and outputs a per-token logit matrix $W \in \mathbb{R}^{m \times n}$ (understanding layers × generation layers), independently for each context token.
  - Sparse top-$k$ selection is applied column-wise (per generation block) with softmax reweighting; an $\epsilon$-greedy strategy during training randomly substitutes top-$k$ selections with random layer picks at probability $\epsilon$ to prevent routing collapse into local optima.
- The dual-tower architecture freezes the understanding tower (e.g., PLM-8B or InternVL-14B) throughout training, so only the generation tower and the lightweight 100M-parameter router are optimized from scratch.
  - This staged training avoids throughput bottlenecks and competing learning objectives inherent in joint multi-task training, and allows the frozen understanding tower to serve both image generation (text-only context) and image editing (text + reference image context) without modification.
  - MoS-Image is trained across four progressive stages: 512px pre-training, 1024px scaling, aesthetic fine-tuning on 10M high-quality samples, and 2K super-resolution tuning — totaling approximately 3,000 A100-days.

---

### Results & Capabilities
- MoS-L (5B learnable parameters, 14B frozen understanding tower) achieves state-of-the-art results on text-to-image generation benchmarks, matching or surpassing Qwen-Image (20B parameters) despite being 4× smaller.
  - MoS-L scores GenEval 0.90, DPG 87.01, WISE 0.54, oneIG 0.52, outperforming Bagel (14B, MoT) on all reported metrics and nearly matching Qwen-Image (20B, self-attention) which scores 0.87 / 88.32 / 0.62 / 0.54.
- MoS-L achieves state-of-the-art on instruction-based image editing benchmarks, scoring GEdit 7.86 and ImgEdit 4.33, surpassing Qwen-Image (7.56 / 4.27) and Bagel (6.52 / 3.20) despite the substantially smaller learnable parameter count.
- The router contributes only 0.008 seconds per inference iteration on a single A100 GPU, making its computational overhead negligible relative to the generation tower.
  - End-to-end latency for 1024×1024 generation is 6.53s (MoS-S) and 8.38s (MoS-L), compared to 25.05s for Qwen-Image and 40.21s for Bagel on identical hardware.
- Ablations confirm that each design principle independently contributes to performance: token-specific routing beats sample-wise (FID 20.17 vs. 21.66), full dynamic conditioning beats static prompt-only (FID 20.15 vs. 21.12), and MoS consistently outperforms MoT at all training checkpoints on both GenEval and DPG.
- When paired with self-CoT reasoning from the understanding tower, MoS-L's WISE score improves from 0.54 to 0.65 without any additional training, demonstrating that the frozen understanding capacity enhances generation quality through better textual grounding.

---

### Implications
- MoS demonstrates that adaptive, sparse routing of inter-model hidden states is a viable and more compute-efficient alternative to scaling model size, suggesting that architectural design quality can substitute for raw parameter count in multimodal diffusion systems.
- By removing the symmetric-tower constraint of MoT, MoS opens the design space to pairing heterogeneous pretrained models (e.g., large VLMs as frozen understanding towers with smaller diffusion transformers), enabling modular reuse of existing foundation models without joint retraining.
- The principle of extending dynamic computation (previously applied intra-model in MoE, MoD, MoR) to inter-model routing establishes a concep

## Key Claims

1. MoS 5B parameter model matches or surpasses a 20B parameter model (4x larger), demonstrating exceptional computational efficiency
2. Prior cross-attention and self-attention multimodal fusion methods typically provide only the final text encoder block's embedding to the visual branch, limiting cross-modal information richness
3. Static text conditioning creates an 'information mismatch' with the dynamic nature of the denoising process because the text encoder provides only a single fixed representation
4. MoT (Mixture of Transformers) requires identical hidden dimensions and a strict one-to-one block correspondence across modalities, making it incompatible with asymmetric transformer architectures
5. Self-attention multimodal fusion has prohibitive computational cost, scaling quadratically with the combined text and visual sequence length
6. Routing conditioned on the full dynamic state (prompt, noised latent, and timestep) outperforms routing conditioned only on the static prompt on both FID and CLIP metrics
7. Token-specific routing prediction (each token defines its own routing matrix) outperforms sample-wise prediction (single global routing matrix for the entire prompt)
8. MoS adaptive layer selection significantly outperforms hand-crafted static routing on both FID (17.77 vs 21.51) and CLIP (22.91 vs 22.04) metrics
9. MoS significantly outperforms a 5B-parameter cross-attention baseline on GenEval (0.79 vs 0.74) and DPG (85.61 vs 83.40) benchmarks under identical data and parameter budget
10. MoS consistently outperforms MoT across all training steps on both GenEval and DPG benchmarks under identical parameters, data, and compute

## Capabilities

- Dynamic token-wise sparse routing for multimodal diffusion fusion: a learnable router selects hidden states across all layers of a text/understanding tower adaptively per token, per denoising timestep, and per noised image latent — enabling asymmetric transformer coupling without fixed layer corresp
- 5B parameter text-to-image diffusion model matching or surpassing a 20B parameter SOTA model (Qwen-Image) across GenEval, DPG, WISE, and oneIG benchmarks via compute-efficient MoS routing
- Instruction-based image editing with SOTA performance at 5B parameters: MoS-Edit scores 7.86 GEdit and 4.33 ImgEdit, surpassing Bagel (14B MoT) and Qwen-Image (20B) on automated GPT-4o evaluation across object-level, scene-level, text, and hybrid editing tasks
- Asymmetric multimodal transformer fusion: MoS couples understanding and generation towers with different hidden dimensions, depths, and design principles — removing the symmetric one-to-one block correspondence requirement of prior MoT architectures
- Multi-stage progressive diffusion training achieving ~2× compute efficiency vs Stable Diffusion v1.5: full 1024×1024 → 2048×2048 text-to-image model trained in ~3,000 A100 days vs 6,250 for SD v1.5, by freezing the understanding tower and focusing compute on generation components
- Self-CoT reasoning chain injection into image generation: using the understanding tower to generate reasoning-based captions that guide the generation tower improves world knowledge grounding, raising WISE benchmark from 0.54 to 0.65 for MoS-L without retraining the generation tower

## Limitations

- MoS one-way routing (understanding → generation) has not been validated for early-fusion bidirectional settings — joint image understanding and generation training, as demonstrated by Bagel/Mogao with MoT, remains unaddressed by the current MoS design
- Static text encoding in prior cross-attention and self-attention diffusion models creates a fundamental 'information mismatch' with the dynamic denoising process — the same fixed text representation is forced to guide all timesteps despite the model's visual state evolving dramatically across them
- MoT (Mixture-of-Transformers) architecture requires identical hidden dimensions and strict one-to-one block correspondence across modalities, preventing use of asymmetric encoders or encoders with different scaling properties — a hard architectural constraint blocking flexible multimodal design
- Self-attention multimodal fusion scales quadratically with combined text+image sequence length, making it computationally prohibitive for high-resolution generation where sequence lengths are large
- No human preference alignment (RLHF, DPO, GRPO) applied to MoS models — current post-training relies solely on SFT, leaving known improvements from preference optimization unexploited
- Visual artifacts persist for very small generated objects — a known failure mode shared with other DiT and unified generative models, not resolved by the MoS architecture
- MoS requires a high-quality pretrained understanding tower (large VLM) as a prerequisite — success is conditioned on the availability of a capable frozen encoder, not on the MoS mechanism alone
- Massive pretraining data and compute requirements: Stage 1 alone requires O(100M) filtered samples and 1,400 A100-days, creating a high barrier to reproducing or adapting MoS outside well-resourced labs
- Scarcity of paired image-editing data limits editing capability development: MoS-Edit uses only O(1M) paired samples, two orders of magnitude less than pretraining data, constraining how well editing generalises
- Joint training of understanding and generation tasks creates throughput bottlenecks from mixed data batches and conflicting learning objectives — causing MoS to adopt staged training to sidestep the problem rather than solving joint training directly
- MoS router explainability is not analysed — the routing patterns learned are observable but their interpretation in terms of which semantic features are being routed and why is left entirely unexplored
- Fixed-layer text conditioning (using only the final encoder layer) is suboptimal but pervasive in cross-attention and self-attention models — no experimental support exists for the assumption that final-layer features best represent all aspects of a prompt across all diffusion timesteps

## Bottlenecks

- Symmetric architecture constraint in MoT-style multimodal diffusion models: requiring identical hidden dimensions and one-to-one block correspondence prevents leveraging best-in-class understanding and generation towers with different depths, dimensions, and scaling properties
- Static text conditioning in multimodal diffusion models: providing a single frozen text embedding to guide all denoising timesteps mismatches the dynamic, evolving nature of the diffusion process — blocking optimal instruction following and prompt adherence
- Bidirectional (early-fusion) extension of token-wise dynamic routing in diffusion models is unsolved: current MoS one-way design cannot support joint understanding and generation training, blocking a unified model that simultaneously improves both tasks
- Scarcity of high-quality paired image editing data (instruction, source image, target image triplets) creates a data ceiling that limits instruction-following quality in image editing models regardless of architecture improvements

## Breakthroughs

- MoS (Mixture of States) demonstrates that a 5B parameter multimodal diffusion model can match or surpass a 20B parameter SOTA model through a learnable token-wise sparse router, achieving 4× parameter efficiency — establishing dynamic inter-model routing as a scalable alternative to parameter scalin

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/model_architecture|model_architecture]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/clip-score|CLIP Score]]
- [[entities/geneval|GenEval]]
