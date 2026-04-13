---
type: source
title: 'MMaDA: Multimodal Large Diffusion Language Models'
source_id: 01KJTTRBRJ1C584K4HRGNNFF68
source_type: paper
authors:
- Ling Yang
- Ye Tian
- Bowen Li
- Xinchen Zhang
- Ke Shen
- Yunhai Tong
- Mengdi Wang
published_at: '2025-05-21 00:00:00'
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- policy_optimization
- reinforcement_learning
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# MMaDA: Multimodal Large Diffusion Language Models

**Authors:** Ling Yang, Ye Tian, Bowen Li, Xinchen Zhang, Ke Shen, Yunhai Tong, Mengdi Wang
**Published:** 2025-05-21 00:00:00
**Type:** paper

## Analysis

# MMaDA: Multimodal Large Diffusion Language Models
2025-05-21 · paper · Ling Yang, Ye Tian, Bowen Li, Xinchen Zhang, Ke Shen et al. (7 total)
https://arxiv.org/pdf/2505.15809

---

### Motivation & Prior Limitations
Existing unified multimodal foundation models overwhelmingly rely on autoregressive (AR) architectures or hybrid AR+diffusion designs, leaving diffusion-only models critically underexplored as general-purpose reasoners and leaving a systematic gap in post-training methodology for non-autoregressive settings.
- Hybrid architectures like Show-o and Transfusion combine autoregressive text modeling with diffusion-based image generation in a single model, but do so using separate objectives per modality, which introduces architectural complexity and prevents a shared probabilistic formulation that could enable genuine cross-modal synergy.
- No prior unified model — including Emu3, Janus, Show-o, SEED-X, or DreamLLM — supports reasoning (chain-of-thought) during both understanding and generation tasks simultaneously; all existing unified models have reasoning capability checked as absent in the paper's comparative table.
- Post-training strategies (instruction tuning, reinforcement learning, chain-of-thought finetuning) had not been systematically explored for unified diffusion architectures, leaving diffusion models lagging in complex reasoning benchmarks despite their structural advantages for parallel generation.
- Adapting GRPO-style RL from autoregressive LLMs to diffusion models is non-trivial: token-level log-likelihoods are only valid within masked regions, mask ratio sensitivity affects policy distribution estimation, and the absence of an AR chain rule makes sequence-level likelihood accumulation intractable.

---

### Proposed Approach
MMaDA introduces a three-stage unified diffusion foundation model that applies a single discrete diffusion (masked token prediction) objective to both text and image modalities, then enhances it through cross-modal chain-of-thought finetuning and a novel diffusion-native RL algorithm.

**Unified Diffusion Architecture (Stage 1):** Both text and image tokens are discretized — text via the LLaDA tokenizer and images via MAGVIT-v2 (512×512 → 1024 discrete tokens with codebook size 8192, downsampling factor f=16) — and trained under a single masked token prediction loss `L_unify`, which computes cross-entropy only over masked positions sampled at uniform timesteps. This eliminates modality-specific components entirely, unlike Show-o and Transfusion which maintain separate AR and diffusion objectives.

**Mixed Long-CoT Finetuning (Stage 2):** A compact but diverse dataset of long chain-of-thought trajectories is curated across three tasks (textual reasoning, multimodal reasoning, world-knowledge-aware text-to-image generation). A task-agnostic unified CoT format `<special_token><reasoning_process><special_token><result>` is applied across all modalities, enabling cold-start initialization for the RL stage and direct knowledge transfer between reasoning and generation branches. Data quality is enforced using state-of-the-art VLMs as verifiers to filter shallow or inaccurate reasoning; GPT-4.1 synthesizes factual item-description pairs for world-knowledge image generation.

**UniGRPO (Stage 3):** A policy-gradient RL algorithm designed specifically for diffusion models addresses three failure modes of naïve AR GRPO adaptation. A structured noising strategy samples a uniform random starting mask ratio per response and generates uniformly spaced denoising timesteps for subsequent iterations, approximating Monte Carlo averaging over the diffusion process more stably and cheaply than LLaDA's 128-sample Monte Carlo or d1's fixed-ratio approach. Sequence-level log-likelihood is approximated by averaging per-token log-probs over masked positions. The final objective integrates clipped surrogate rewards and KL divergence regularization. Diversified reward modeling tailors rewards per task branch: textual reasoning uses correctness (2.0) and format rewards (0.5); multimodal reasoning adds a CLIP reward (0.1 × CLIP score); image generation uses CLIP and ImageReward signals (both scaled by 0.1).

---

### Results & Capabilities
MMaDA-8B achieves state-of-the-art or competitive performance across all three task categories simultaneously, demonstrating that a single discrete diffusion model can match or exceed specialized and hybrid baselines.

**Multimodal Understanding:** MMaDA scores 86.1 on POPE, 1410.7 on MME, 67.6 on Flickr30k, 76.7 on VQAv2, 61.3 on GQA, and 68.5 on MMBench — outperforming all tested unified models (Show-o, SEED-X, DreamLLM, Emu3, Janus) on most benchmarks and matching or exceeding understanding-only models like LLaVA-v1.5 (85.9 POPE, 1510.7 MME).

**Text-to-Image Generation:** MMaDA achieves the highest CLIP Score (32.46) and ImageReward (1.15) among both generation-only models (SDXL: 32.12, 1.13) and all unified models. On the WISE Cultural benchmark for world knowledge-aware generation, MMaDA scores 0.67, substantially outperforming Janus (0.16), Show-o (0.28), and SDXL (0.43), attributed to its joint training on text-based reasoning which other image models lack. On GenEval, MMaDA reaches an overall score of 0.63, compared to 0.61 for Janus and 0.55 for SDXL, with particular strength in counting (0.61 vs. 0.30 for Janus).

**Textual Reasoning:** MMaDA-8B scores 68.4 on MMLU, 57.4 on ARC-C, 73.4 on GSM8K, and 36.0 on MATH500 — consistently outperforming the diffusion baseline LLaDA-8B (65.9, 47.9, 70.7, 27.3) and comparable to or exceeding LLaMA-3-8B (64.5, 53.1, 53.1, 15.1), though not matching Qwen2-7B (70.3, 60.6, 80.2, 43.5).

**Qualitative reasoning capability:** MMaDA correctly solves geometry problems that other unified models (Show-o, Emu3, Janus Pro 7B) answer incorrectly by executing genuine chain-of-thought reasoning (e.g., angle CFE = 50° via exterior angle theorem, versus all competitors answering 60°), and it produces

## Key Claims

1. Existing unified multimodal foundation models predominantly focus on model architecture design and pretraining strategies, leaving a critical gap in post-training methodologies for non-autoregressive 
2. MMaDA-8B surpasses LLaMA-3-7B and Qwen2-7B in textual reasoning
3. MMaDA outperforms Show-o and SEED-X in multimodal understanding
4. MMaDA excels over SDXL and Janus in text-to-image generation
5. MMaDA uses discrete tokenization for both text and image modalities, enabling a single unified masked-token-prediction modeling objective
6. Image tokenization based on MAGVIT-v2 converts a 512×512 pixel image into a sequence of 1024 discrete tokens using a downsampling factor of 16 and a codebook size of 8192
7. MMaDA formulates both image and text generation as a mask token prediction problem, predicting all masked tokens simultaneously under a unified cross-entropy loss
8. Enhanced textual reasoning capabilities from CoT training directly improve the realism of generated images by aligning semantic logic with visual synthesis
9. Adapting autoregressive GRPO to diffusion models faces three critical challenges: local masking dependency, mask ratio sensitivity, and non-autoregressive sequence-level likelihoods
10. LLaDA employs Monte Carlo sampling over 128 mask ratios for on-policy RL, incurring high computational costs

## Capabilities

- Unified 8B discrete diffusion foundation model performing textual reasoning, multimodal understanding, and text-to-image generation within a single modality-agnostic architecture — first such model to support chain-of-thought reasoning across all three modalities simultaneously
- World knowledge-aware text-to-image generation via explicit chain-of-thought reasoning prior to image synthesis, enabling factually grounded images for culturally specific or knowledge-intensive prompts — WISE Cultural benchmark 0.67 vs next-best 0.43 (SDXL)
- UniGRPO: computationally efficient policy-gradient RL for non-autoregressive diffusion foundation models, using structured uniformly-random masking and averaged masked token log-likelihoods to approximate sequence-level likelihoods without Monte Carlo sampling
- Diffusion LMs can generate coherent image outputs with as few as 15 denoising steps and text/multimodal outputs with 256 steps (quarter of maximum), with only marginal quality degradation — CLIP Score 31.7 at 15 steps vs 32.8 at 1024 steps
- Inpainting and span completion across text sequences, visual question answering completions, and image inpainting — all without additional fine-tuning — by formulating all as masked token prediction inherent in the diffusion training objective
- Measurable cross-modal synergy in joint diffusion training: all three performance metrics (text generation, multimodal understanding, image generation) improve simultaneously during Stage 2 joint fine-tuning, with textual reasoning gains transferring directly to image generation factual accuracy

## Limitations

- Current 8B scale is explicitly insufficient for peak performance — the authors acknowledge larger model sizes are needed, and text benchmarks confirm underperformance vs. specialist AR models (MATH: 36.0 vs Qwen2-7B's 43.5; TruthfulQA: 43.1 vs 54.2)
- Fixed-length non-autoregressive diffusion generation produces unnaturally short text responses; semi-autoregressive block decoding is required to produce detailed long-form outputs
- Naive lowest-confidence remasking on instruction-tuned diffusion LMs generates pathologically high EOS token frequency without block partitioning — a structural failure mode that requires workaround
- Standard autoregressive GRPO is fundamentally incompatible with diffusion models due to local masking dependency, mask ratio sensitivity, and absence of an AR chain rule for accumulating sequence-level log-likelihoods
- Pretraining alone (Stage 1) leaves the model dramatically weaker than baselines — GSM8K 17.4, MATH500 4.2, GeoQA 8.3 — indicating the discrete diffusion pretraining objective alone is insufficient to induce structured reasoning
- Monte Carlo sampling for on-policy diffusion RL (LLaDA approach) requires ~128 samples per gradient update, making it computationally prohibitive for practical RL training at scale
- Multimodal understanding still underperforms dedicated understanding-only models on complex reasoning benchmarks (MMMU: 30.2 vs LLaVA-v1.5's 35.4), despite outperforming other unified models
- Training is conducted exclusively on open-source data and limited task-specific tokens — an implicit constraint that caps performance ceiling relative to proprietary-data AR models
- Three-stage training requires 64 A100 (80GB) GPUs for 600K+ steps — a resource barrier that makes replication or scaling experiments inaccessible to most academic research groups
- Image generation spatial compositionality remains incomplete — position accuracy (0.37) and color attribute binding (0.37) on GenEval lag behind what would be expected from a model with strong reasoning capabilities
- Discrete image tokenization at f=16 downsampling caps generation resolution at 512×512 — higher-resolution generation is conspicuously absent from all experiments and benchmarks
- Fully random timestep selection in diffusion RL training causes reward instability and slower convergence compared to structured uniformly-spaced masking — indicating sensitivity to the masking schedule hyperparameter

## Bottlenecks

- Post-training methodology for non-autoregressive diffusion foundation models is systematically underdeveloped — the entire field has focused on architecture and pretraining, leaving RL alignment, preference learning, and CoT fine-tuning largely unexplored for diffusion-based unified models
- Discrete VQ tokenization at coarse spatial resolution (f=16, 512×512 maximum) is a hard ceiling on image quality and resolution for unified discrete diffusion models — increasing resolution scales token count quadratically, conflicting with the need for long CoT reasoning sequences

## Breakthroughs

- First demonstration that a discrete diffusion foundation model achieves competitive performance simultaneously on textual reasoning, multimodal understanding, and text-to-image generation — with chain-of-thought reasoning across all three modalities in a single unified architecture
- UniGRPO resolves the fundamental incompatibility between policy-gradient RL and non-autoregressive diffusion dynamics, enabling practical RL training without Monte Carlo sampling overhead

## Themes

- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/multimodal_models|multimodal_models]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/unified_multimodal_models|unified_multimodal_models]]

## Key Concepts

- [[entities/clip-score|CLIP Score]]
- [[entities/classifier-free-guidance|Classifier-Free Guidance]]
- [[entities/grpo|GRPO]]
- [[entities/gsm8k|GSM8K]]
- [[entities/geneval|GenEval]]
- [[entities/llada|LLaDA]]
- [[entities/show-o|Show-o]]
