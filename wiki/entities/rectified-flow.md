---
type: entity
title: Rectified Flow
entity_type: method
theme_ids:
- generative_media
- image_generation_models
- multimodal_models
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
- unified_multimodal_models
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00010583377176158955
staleness: 0.0
status: active
tags: []
---
# Rectified Flow

Rectified Flow is a flow-matching generative method that has emerged as a foundational technique for visual generation in unified multimodal systems. By learning straight-line trajectories between noise and data distributions, it offers a cleaner and more efficient alternative to traditional diffusion schedules. Its adoption across leading unified models, including BAGEL and JanusFlow, signals a field-wide consensus that flow-based generation is the preferred backbone for continuous visual synthesis within autoregressive multimodal architectures.

**Type:** method
**Themes:** [[themes/generative_media|Generative Media]], [[themes/image_generation_models|Image Generation Models]], [[themes/multimodal_models|Multimodal Models]], [[themes/post_training_methods|Post-Training Methods]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/pretraining_data|Pretraining Data]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/synthetic_data_generation|Synthetic Data Generation]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/unified_multimodal_models|Unified Multimodal Models]], [[themes/video_and_world_models|Video and World Models]], [[themes/vision_language_models|Vision Language Models]]

## Overview

Rectified Flow frames image generation as learning an ordinary differential equation that transports a Gaussian prior to the target data distribution along straight paths. This linearity reduces discretization error and makes the model amenable to fewer inference steps compared to score-based diffusion. In practice, it is paired with architectural stabilizers, particularly QK-Norm in each attention block, which is now described as common practice in image and video generation models. BAGEL's adoption of this combination reflects a broader convergence: high-capacity unified models are settling on flow-matching with attention normalization as a stable and scalable recipe.

The most detailed empirical case comes from JanusFlow, which directly integrates Rectified Flow into an autoregressive multimodal framework. The key design insight is that autoregression handles discrete semantic understanding while Rectified Flow handles continuous pixel-space generation, with decoupled visual encoders preventing the representational conflict that plagues earlier unified approaches. With only 1.3B parameters, JanusFlow achieves an MJHQ FID-30k of 9.51, a GenEval overall score of 0.63, and DPG-Bench of 80.09%, surpassing specialized generation models including SDv1.5 and SDXL and outperforming prior unified frameworks at comparable scale. Multimodal understanding is equally competitive, reaching 74.9 on MMBench, 70.5 on SeedBench, and 60.3 on GQA, exceeding LLaVA-v1.5 and Qwen-VL-Chat.

BAGEL scales this approach considerably further, with 7B active parameters (14B total) in a Mixture-of-Transformers architecture. Rectified Flow serves as the visual generation backbone, operating within a bottleneck-free design where shared self-attention spans both understanding and generation experts. The training regime is substantial: 2.5T tokens in pre-training and approximately 2.6T in continued training, with a relatively compact 72.7B-token supervised fine-tuning stage. BAGEL's architecture also uses QK-Norm throughout, reinforcing that flow-based generation at scale requires explicit attention stabilization.

## Key Findings

The evidence across sources points to Rectified Flow functioning well within diverse architectural contexts. JanusFlow demonstrates that a three-stage training curriculum (component adaptation, unified pre-training, supervised fine-tuning) is sufficient to make autoregression and flow-matching cooperate within a single 1.3B model. BAGEL's Mixture-of-Transformers variant shows the method scales to larger, sparser architectures without sacrificing generation quality: the MoT and MoE variants carry roughly twice the total parameters of a dense baseline, yet maintain identical FLOPs at both training and inference time. This parameter efficiency argument is significant, because it suggests Rectified Flow can serve as the generation head for architectures designed primarily around inference-time compute constraints.

BAGEL's video data pipeline, which distills a lightweight captioner from Qwen2.5-VL-7B to produce 45 million temporally grounded interleaved sequences, feeds Rectified Flow generation in a multimodal pretraining setting that spans static images, video, and text. This positions Rectified Flow not merely as an image generation technique but as a candidate for temporally continuous synthesis once interleaved video sequences are incorporated into training. OmniGen2 is cited as a further source context, suggesting the approach generalizes beyond JanusFlow and BAGEL, though the specific findings from that work are not fully represented in the current claims.

## Limitations and Open Questions

The claims in the corpus are predominantly benchmark performance results rather than ablations of the Rectified Flow component itself. It is therefore difficult to separate the contribution of flow-matching from the contributions of architectural choices (MoT, decoupled encoders, QK-Norm) or data pipeline decisions (interleaved video, high-quality SFT data). The degree to which Rectified Flow's straight-trajectory inductive bias is responsible for the observed gains, versus simply being a robust default that tolerates large-scale pretraining, remains unclear.

JanusFlow's results are limited to 1.3B parameters. It is an open question whether the autoregression-plus-flow-matching coupling degrades, becomes harder to train, or requires qualitatively different stabilization strategies at the 7B-to-70B scale range that defines frontier unified models. BAGEL addresses some of this, but does not publish ablations comparing Rectified Flow against alternatives at its scale.

The interplay between Rectified Flow and video generation is underexplored in the available claims. BAGEL constructs temporally grounded video data but the claims do not describe how well Rectified Flow handles temporal coherence, motion fidelity, or multi-frame consistency relative to dedicated video diffusion architectures. This gap is notable given that video is one of the declared use cases.

Finally, the training cost asymmetry between the massive pretraining stages (over 5T tokens combined for BAGEL) and the compact SFT stage (72.7B tokens) raises a question about the method's data efficiency: Rectified Flow generation quality may be highly sensitive to the scale of pretraining data, which would constrain its accessibility outside of well-resourced training runs.

## Relationships

Rectified Flow sits at the intersection of [[themes/generative_media|generative media]] and [[themes/unified_multimodal_models|unified multimodal models]], where the central tension is between discrete autoregressive modeling of semantics and continuous generative modeling of pixels. JanusFlow's explicit "harmonizing" framing treats this tension as the primary architectural problem. BAGEL's bottleneck-free shared attention design takes a different resolution: rather than keeping the two pathways separate, it allows long-context interaction across generation and understanding streams, with Rectified Flow serving as the generation-side output head.

The QK-Norm stabilization practice links Rectified Flow to broader conventions in [[themes/video_and_world_models|video and world models]], where attention instability at high resolutions and long contexts is a known problem. The adoption of NaViT-style native-resolution encoding in BAGEL (up to 980x980 with interpolated positional embeddings) further connects to [[themes/vision_language_models|vision language models]], where flexible input geometry is increasingly standard.

Sources: JanusFlow: Harmonizing Autoregression and Rectified Flow for Unified Multimodal Understanding and Generation, Emerging Properties in Unified Multimodal Pretraining, OmniGen2: Exploration to Advanced Multimodal Generation

## Sources
