---
type: entity
title: LLaDA
entity_type: entity
theme_ids:
- adaptive_computation
- code_and_software_ai
- code_generation
- generative_media
- image_generation_models
- model_architecture
- multimodal_models
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- test_time_compute_scaling
- transformer_alternatives
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00022653232233355185
staleness: 0.0
status: active
tags: []
---
# LLaDA

> LLaDA (Large Language Diffusion with mAsking) is an open-source 8B masked diffusion language model that represents the current state of the art among diffusion LMs. It formulates text generation as iterative masked token prediction rather than autoregressive next-token prediction, achieving competitive generation quality but at substantially higher computational cost than autoregressive models. LLaDA has become an important reference point in the emerging literature on applying reinforcement learning to diffusion language models, surfacing fundamental incompatibilities between AR-era training algorithms and the structural properties of diffusion inference.

**Type:** entity
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/code_and_software_ai|code_and_software_ai]], [[themes/code_generation|code_generation]], [[themes/generative_media|generative_media]], [[themes/image_generation_models|image_generation_models]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/unified_multimodal_models|unified_multimodal_models]]

## Overview

LLaDA is an 8B masked diffusion language model trained to predict masked tokens rather than generate them autoregressively. Its generative process works by starting from a fully masked sequence and iteratively unmasking tokens over multiple denoising steps, with the model predicting all masked positions simultaneously at each step. Best generation quality is achieved when decoding one token per forward pass, which preserves fidelity but collapses the parallelism advantage that diffusion models nominally offer over autoregressive generation. This tension between quality and throughput is a defining characteristic of the current generation of diffusion LMs, and LLaDA exemplifies both what has been achieved and where the ceiling currently sits.

LLaDA also serves as a baseline and foil in work on adapting RL fine-tuning to diffusion models. Because it is open-source and well-characterised, subsequent systems such as MMaDA directly benchmark against it and diagnose its limitations as motivation for new approaches.

## Key Findings

### The RL Adaptation Problem

The most technically significant finding associated with LLaDA in recent literature concerns the cost of applying on-policy reinforcement learning to diffusion models. LLaDA's approach uses Monte Carlo sampling over 128 mask ratios per training step to estimate the policy gradient, because the non-autoregressive structure of diffusion inference means that standard token-level log-likelihood decomposition via chain rule does not apply. The sequence-level likelihood must instead be approximated by averaging over masked token predictions at many different noise levels, and 128 samples is the working number in LLaDA's implementation. This is computationally expensive relative to autoregressive GRPO, which can compute token-level log-probabilities in a single forward pass.

This cost is not incidental; it reflects a deep structural mismatch. Adapting autoregressive RL algorithms like GRPO to diffusion models faces three identified challenges: local masking dependency (token-level log-likelihoods are only locally valid given the current mask, not across the full sequence), mask ratio sensitivity (gradient estimates vary substantially depending on what fraction of tokens are masked), and non-autoregressive sequence-level likelihoods (the chain rule factorisation that makes AR log-probabilities tractable does not hold). LLaDA's Monte Carlo approach addresses these by brute-force sampling, while subsequent work like MMaDA's UniGRPO addresses them by sampling mask ratios uniformly and averaging rather than accumulating token probabilities.

The d1 approach, an alternative to LLaDA's strategy, fixes the mask ratio and randomises question masking instead. This reduces computational cost but introduces its own problems: lower noise diversity and a failure to reflect the multi-step denoising structure of diffusion models. Neither LLaDA's expensive sampling nor d1's fixed-ratio shortcut is fully satisfactory, which frames the problem as genuinely open.

### Competitive Standing

LLaDA represents the current SOTA among diffusion LMs but does not match the speed-quality profile of autoregressive models. This gap is important context for evaluating claims about diffusion LMs as successors to AR approaches. Systems built on LLaDA's architecture, such as MMaDA, demonstrate that the framework can be extended to multimodal settings (text, image, and reasoning in a unified masked-token-prediction objective), but the fundamental throughput limitation of best-quality-at-one-token-per-forward remains unresolved.

In textual reasoning benchmarks, MMaDA-8B (built on a similar architectural foundation) surpasses LLaMA-3-7B and Qwen2-7B, suggesting that diffusion LMs at this scale are not categorically weaker at reasoning tasks. However, these comparisons are on benchmarks where quality matters and throughput is not the primary metric, so the competitive picture depends heavily on what is being measured.

## Relationships

LLaDA is directly compared against and built upon in MMaDA: Multimodal Large Diffusion Language Models, which extends the masked diffusion framework to unified multimodal generation and introduces UniGRPO as a computationally efficient alternative to LLaDA's Monte Carlo RL approach. The d1 system represents a contrasting design choice for RL adaptation. In the code generation domain, DiffuCoder investigates masked diffusion models specifically for code, where the structured, locally coherent nature of programs may interact differently with the iterative unmasking process. TiDAR explores a hybrid approach that thinks in diffusion but generates autoregressively, motivated in part by the throughput limitations that LLaDA exemplifies.

Thematically, LLaDA sits at the intersection of [[themes/transformer_alternatives|transformer alternatives]] and [[themes/policy_optimization|policy optimization]], since its primary interest in the current literature is less about architecture per se and more about what it reveals regarding the difficulty of applying standard RL fine-tuning pipelines to non-autoregressive generation.

## Open Questions

The core unresolved question is whether the quality-throughput gap between diffusion LMs and autoregressive models can be closed, or whether the best-quality-at-one-token-per-forward result reflects a fundamental property of masked diffusion inference. A related question is whether the RL adaptation challenges (mask ratio sensitivity, local masking dependency, sequence-level likelihood approximation) have clean solutions or whether they impose a permanent overhead cost on diffusion LM fine-tuning. LLaDA's role in the literature is largely to make these questions concrete and measurable.

## Limitations and Open Questions

## Sources
