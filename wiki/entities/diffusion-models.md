---
type: entity
title: Diffusion Models
entity_type: method
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- code_and_software_ai
- code_generation
- frontier_lab_competition
- medical_and_biology_ai
- model_architecture
- multimodal_models
- reasoning_and_planning
- representation_learning
- scientific_and_medical_ai
- software_engineering_agents
- startup_and_investment
- test_time_compute_scaling
- unified_multimodal_models
- vc_and_startup_ecosystem
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0018636447845053945
staleness: 0.0
status: active
tags: []
---
# Diffusion Models

> Diffusion models are a class of probabilistic generative methods that learn to reverse a gradual noising process, iteratively denoising random noise into high-fidelity outputs — most famously images, but increasingly video, audio, and structured data. They have become the dominant architecture for generative media and a critical component of multimodal AI systems, though their stochastic nature creates a fundamental tension between generation quality and precise controllability that remains one of the field's most consequential open problems.

**Type:** method
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_business_and_economics|AI Business and Economics]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/code_and_software_ai|Code and Software AI]], [[themes/code_generation|Code Generation]], [[themes/frontier_lab_competition|Frontier Lab Competition]], [[themes/medical_and_biology_ai|Medical and Biology AI]], [[themes/model_architecture|Model Architecture]], [[themes/multimodal_models|Multimodal Models]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/representation_learning|Representation Learning]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/startup_and_investment|Startup and Investment]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]], [[themes/unified_multimodal_models|Unified Multimodal Models]], [[themes/vc_and_startup_ecosystem|VC and Startup Ecosystem]], [[themes/vertical_ai_and_saas_disruption|Vertical AI and SaaS Disruption]]

## Overview

Diffusion models operate by learning the reverse of a Markov chain that progressively corrupts data with noise. At inference time, the model starts from pure Gaussian noise and iteratively predicts and removes noise across many steps, guided by a learned score function. This process — denoising diffusion probabilistic models (DDPMs), score-matching, and their flow-matching successors — produces outputs of remarkable fidelity and diversity but with a structural constraint: each generation is a unique stochastic trajectory through a high-dimensional space. Two generations from identical prompts will diverge.

This stochasticity is both the source of diffusion models' generative richness and their core limitation. **Editing is fundamentally hard.** To change one element of a generated image, you cannot simply modify it in place — re-generating with a slightly altered prompt produces an entirely different stochastic outcome. Techniques like SDEdit, prompt-to-prompt, and InstructPix2Pix attempt to workaround this by inverting the noise process or injecting edits at intermediate steps, but none fully resolve the tension: controllability and diversity trade off against each other by design.

The architecture has expanded rapidly beyond static images. Latent diffusion models (operating in a compressed latent space rather than pixel space) dramatically reduced compute costs and enabled video diffusion, 3D generation, and integration into multimodal pipelines. Conditioning mechanisms — CLIP embeddings, cross-attention over text tokens, classifier-free guidance — made text-to-image generation practical at scale and commercially viable.

## Key Findings

The claims associated with diffusion models in this library emerge primarily from discussions of the broader AI investment and product landscape, reflecting how diffusion-based generative capabilities have been absorbed into the commercial AI ecosystem rather than from technical analyses of the method itself. Several patterns are worth synthesising.

**Diffusion models arrived at the founding moment of the current AI wave.** The November 2022 period that saw Sarah Guo and Elad Gil's Conviction launch was the same moment that image generation via diffusion was becoming mainstream and ChatGPT was demonstrating that language generation had crossed a consumer viability threshold. These two generative paradigms — diffusion for media, autoregressive transformers for language — defined the commercial landscape that followed. Conviction's founding thesis was shaped by this convergence.

**The business models emerging from generative AI treat the stochasticity as a feature, not a bug.** The "Results as a Service" framing discussed in Dharmesh Shah's Agent Network talk — charging for outcomes rather than the act of generation — is well-suited to diffusion-based products. When each generation is unique, value lies in the output achieved, not the reproducible process. This reframes the editing limitation: rather than fixing a specific output, users iterate toward a satisfactory one.

**Integration into agent pipelines creates new friction points.** As agent systems like Agent.ai move toward composable tool networks exposed via MCP, diffusion-based generation becomes one callable capability among many. The non-determinism of diffusion is more manageable when the agent can evaluate and retry, but it conflicts with the deterministic control flows that agent architectures favour. The observation that deterministic agent designs were chosen partly because reasoning models didn't yet exist applies symmetrically to diffusion: agentic use of diffusion requires either tolerating stochasticity or adding evaluation loops that catch bad samples.

**Test-time compute scaling creates an architectural contrast.** OpenAI's o1 demonstrates that scaling compute at inference time via iterative reasoning steps dramatically improves performance on structured tasks like math and code. Diffusion models have their own form of test-time compute: more denoising steps, higher guidance weights, and techniques like DDIM inversion all trade compute for quality. But unlike reasoning models where more steps mean more deliberate thinking, more diffusion steps primarily improve sample fidelity rather than correctness — the model does not "reason" toward a better answer, it refines noise into signal. This is a fundamental architectural distinction with implications for where diffusion models will and won't be competitive.

**Scientific and medical applications face the verification problem acutely.** In biology and drug discovery contexts discussed across the library's sources, diffusion models for molecular generation (protein structure, small molecule design) face a compounded challenge: the stochastic output must be not just high-quality but biochemically valid and interpretable. The representation learning demands are higher, and the absence of a ground-truth check analogous to a math proof means evaluation is expensive and domain-specific.

## Limitations and Open Questions

The core limitation — **stochastic non-reproducibility** — cascades into several practical constraints:

- **Editing without re-generation** remains unsolved at production quality. Current approaches either sacrifice diversity (high consistency but less creative range) or precision (expressive but hard to target).
- **Compositional failures** persist: diffusion models struggle with attribute binding (the red cube and blue sphere problem), counting, and spatial relationships, especially under distribution shift.
- **Compute at inference** is still high relative to discriminative models, though latent diffusion has reduced this significantly. Real-time video diffusion at high resolution remains at the frontier of feasibility.
- **Unified multimodal generation** — a single model generating images, text, audio, and video — is an active research frontier but no architecture has yet dominated. Whether diffusion or autoregressive or hybrid flow-based approaches win this is genuinely open.

## Relationships

Diffusion models are architecturally adjacent to and increasingly integrated with [[themes/representation_learning|representation learning]] (CLIP, DINO, and learned perceptual spaces are central to conditioning and evaluation), [[themes/multimodal_models|multimodal models]] (as the generation backbone for visual modalities), and [[themes/unified_multimodal_models|unified multimodal models]] (where the question is whether a single model can handle both understanding and generation). The test-time compute contrast with [[themes/test_time_compute_scaling|reasoning-oriented scaling]] is a structurally important comparison: diffusion scales compute toward perceptual quality, not cognitive correctness.

In the [[themes/medical_and_biology_ai|medical and biology AI]] space, diffusion models underpin protein and molecular generation pipelines and are increasingly part of the scientific AI infrastructure discussed in sources like AI at the Intersection of Bio. In the investment landscape, diffusion model capabilities were a defining catalyst for the 2022–2023 generative AI investment wave documented in The Future of AI Investing.

## Sources
