---
type: source
title: 'LLaVA-CoT: Let Vision Language Models Reason Step-by-Step'
source_id: 01KJV6G030GM66QCNBBZCETGSN
source_type: paper
authors:
- Guowei Xu
- Peng Jin
- Ziang Wu
- Hao Li
- Yibing Song
- Lichao Sun
- Li Yuan
published_at: '2024-11-15 00:00:00'
theme_ids:
- chain_of_thought
- multimodal_models
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# LLaVA-CoT: Let Vision Language Models Reason Step-by-Step

LLaVA-CoT introduces a structured four-stage reasoning framework for Vision-Language Models — Summary, Caption, Reasoning, Conclusion — trained via supervised fine-tuning on a purpose-built 100k dataset annotated by GPT-4o, paired with a novel Stage-Wise Retracing Search (SWIRES) algorithm at inference time. The work demonstrates that an 11B model trained with structured reasoning can outperform 90B-scale open-source models and mid-tier closed-source systems on multimodal reasoning benchmarks, and that structured CoT with stage-level retracing breaks the test-time scaling plateau that afflicts best-of-N and standard beam search.

**Authors:** Guowei Xu, Peng Jin, Ziang Wu, Hao Li, Yibing Song, Lichao Sun, Li Yuan
**Published:** 2024-11-15
**Type:** paper
**Themes:** [[themes/chain_of_thought|Chain of Thought]] · [[themes/multimodal_models|Multimodal Models]] · [[themes/post_training_methods|Post-Training Methods]] · [[themes/reasoning_and_planning|Reasoning & Planning]] · [[themes/synthetic_data_generation|Synthetic Data Generation]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]] · [[themes/vision_language_models|Vision-Language Models]]

---

## Motivation

Existing VLMs operate in a **direct-prediction paradigm**: they generate brief answers immediately without organising the problem or tracking their reasoning stage. Even when [[themes/chain_of_thought|chain-of-thought prompting]] is applied, VLMs routinely produce errors and hallucinations — not because CoT is absent, but because it is neither *systematic* (no multistage structure) nor *structured* (no explicit tracking of which stage the model is in).

The failure mode is token-level: once an erroneous conclusion is introduced, the autoregressive generation process propagates that error through all subsequent tokens. The model then attempts to justify the flawed conclusion post-hoc rather than correct it. This is an inherent property of token-by-token generation without a mechanism for upstream error correction.

Test-time scaling approaches available prior to this work — majority voting, best-of-N, and beam search — are misaligned with the semantic structure of visual QA. Standard beam search applies search after a fixed number of tokens or sentences, not at semantically meaningful stage boundaries, and has no way to repair errors introduced in earlier reasoning steps.

---

## Approach

### Structured Four-Stage Reasoning

LLaVA-CoT enforces reasoning through four sequential stages, delimited by XML-style tags and executed autonomously in a single inference pass:

1. **Summary** — outlines the problem
2. **Caption** — extracts relevant visual information from the image
3. **Reasoning** — conducts step-by-step logical analysis
4. **Conclusion** — synthesises the final answer

The first three stages are internal; only the Conclusion is surfaced to the user. Critically, all stages are initiated at the model's discretion — no external prompting or intervention is required at inference time. This distinguishes the approach from standard CoT prompting, which provides a reasoning trajectory as a prompt prefix.

Ablations confirm that the structured tags themselves — not merely the additional training data — are the primary driver of performance gains. Removing the tags while keeping the same data yields a significant performance drop (avg 60.9 vs. 62.4); training on the original unstructured Q&A pairs without reasoning annotations performs worse still (avg 59.0).

### LLaVA-CoT-100k Dataset

No [[themes/multimodal_models|multimodal model]] capable of producing structured reasoning natively existed at the time of dataset construction. The authors used **GPT-4o to generate each reasoning stage separately** for 99k image-QA pairs drawn from 10 existing VQA datasets spanning general-purpose and science-targeted domains (ShareGPT4V, ChartQA, A-OKVQA, AI2D, GeoQA+, ScienceQA, DocVQA, PISC, CLEVR, CLEVR-Math). This bootstrapping approach — leveraging a capable closed-source model to create [[themes/synthetic_data_generation|synthetic training data]] for a smaller open model — is the only viable path given the absence of structured reasoning annotations in any existing VQA dataset.

The base model is Llama-3.2-11B-Vision-Instruct, fine-tuned with full-parameter SFT on 8×H100 GPUs.

### SWIRES: Stage-Wise Retracing Search

SWIRES extends stage-wise beam search with a **retracing mechanism** that enables upstream error correction:

- At each reasoning stage, M candidate responses are generated and scored by a reward model (InternLM-XComposer2.5-Reward)
- If all candidates fall below a predefined quality threshold at the current stage, SWIRES **retraces to the previous stage** to regenerate it, rather than proceeding with a flawed foundation
- Retracing begins from the Caption stage — the Summary stage empirically produces high-quality outputs reliably and is excluded

This contrasts with standard stage-wise beam search, which can only optimise within a stage given a (potentially flawed) prior stage output. The retracing mechanism directly addresses the core failure mode of token-by-token generation propagating upstream errors downstream.

---

## Results

### Base Performance (no test-time scaling)

LLaVA-CoT (11B) achieves **62.4 average** across six benchmarks (MMStar, MMBench, MMVet, MathVista, AI2D, HallusionBench), a +5.8% improvement over its Llama-3.2-11B base model (56.6) using only 100k training samples.

Performance gains are concentrated in **reasoning-intensive skills**:

| Skill | Improvement over base |
|---|---|
| Math | +18.8 |
| Science & Technology | +12.0 |
| Logical Reasoning | +7.2 |
| Instance Reasoning | +5.6 |
| Coarse Perception | +2.8 |
| Fine-Grain Perception | +0.4 |

The near-zero gain in perceptual tasks confirms that structured CoT training targets reasoning rather than perceptual capability — an important scope limitation for applications where perception is the bottleneck.

### With SWIRES Test-Time Scaling

LLaVA-CoT with SWIRES reaches **65.5–66.3 average** across benchmarks, competitive with or exceeding:

- Gemini-1.5-Pro (avg 63.6)
- GPT-4o-mini (avg 63.8)
- Llama-3.2-90B-Vision-Instruct (avg 62.3)
- VILA-1.5-40B (avg 56.9)

An 11B model with structured reasoning training and test-time scaling surpasses a 90B-parameter open-source model — an 8× parameter efficiency advantage on reasoning benchmarks.

### Scaling Behaviour

SWIRES demonstrates superior [[themes/test_time_compute_scaling|test-time compute scaling]] compared to both stage-wise beam search and best-of-N:

- Both alternatives **plateau around 10,000 seconds**; best-of-N shows a slight accuracy *decline* beyond that point
- SWIRES **continues to improve** beyond 10,000 seconds, reaching 62.5 on MMStar at 15,000 seconds versus 61.2 for stage-wise beam search and 60.5 for best-of-N

The plateau of prior methods is attributed to operating at granularities misaligned with semantic structure — they cannot repair errors from upstream stages.

---

## Limitations & Open Questions

### Structural Limitations

**Reward model dependency.** SWIRES is not self-contained — it requires an external reward model at inference time to score candidate responses at each stage. The quality ceiling of test-time scaling is directly determined by reward model precision, and whatever biases or blind spots that model has are inherited by the overall system. This is a binding constraint on how far SWIRES-style scaling can go.

**Wall-clock cost.** SWIRES scaling experiments run up to 15,000 seconds (~4 hours) per evaluation on a single A800 node. The approach is demonstrably impractical for latency-sensitive applications in its current form. Whether the efficiency frontier can be pushed substantially is unclear.

**Local optima in stage-wise beam search.** Selecting the highest-scoring response at each individual stage does not guarantee globally optimal reasoning paths. Errors in stage selection propagate and may be amplified by subsequent stages. SWIRES partially addresses this through retracing, but the retracing depth is limited.

### Scope Limitations

**Reasoning-only gains.** Structured CoT training does not improve perceptual tasks. Applications where perceptual limitations are the binding constraint will not benefit from this approach.

**Multiple-choice evaluation only.** All six benchmarks use multiple-choice or structured-answer formats. Open-ended generation quality of structured reasoning is unassessed — applicability to unconstrained real-world tasks is unvalidated.

**Single architecture.** The approach is demonstrated on Llama-3.2-11B-Vision-Instruct only. Generalisation to other VLM architectures is unvalidated.

### Training Data Limitations

**GPT-4o quality ceiling.** The LLaVA-CoT-100k dataset is entirely bootstrapped from GPT-4o-generated annotations. The trained model is bounded by GPT-4o's reasoning quality — it cannot learn reasoning patterns that GPT-4o cannot produce. This is an inherent ceiling of [[themes/synthetic_data_generation|teacher-model distillation]] approaches.

**No RL training.** The paper explicitly identifies reinforcement learning for multimodal reasoning as unexplored future work. The current approach relies entirely on supervised fine-tuning; there is no mechanism for the model to discover reasoning strategies beyond what GPT-4o demonstrates. The absence of RL is the binding constraint on capabilities exceeding the teacher model's quality ceiling.

**Compute access barrier.** Full-parameter fine-tuning of an 11B model on 8×H100 GPUs is not accessible to most researchers, even though the dataset and weights are released.

---

## Key Bottlenecks Identified

**Structured reasoning training data scarcity.** No existing VQA datasets contain multi-stage reasoning annotations. Every approach in this space must either generate synthetic data (inheriting teacher model ceilings) or build annotation pipelines from scratch. This bottleneck is partially addressed by LLaVA-CoT-100k but not resolved — the field still lacks natively structured reasoning data with human-verified quality.

**Reward model precision as the scaling ceiling.** SWIRES-style test-time scaling for [[themes/vision_language_models|VLMs]] is bounded by how accurately the reward model can judge stage-level output quality. Reliable VLM test-time scaling — including self-improvement without external verification — requires reward models that are substantially more capable and calibrated than what exists currently.

**Absence of RL for multimodal reasoning.** SFT on teacher-generated data has a provable quality ceiling. Until reinforcement learning methods are successfully applied to multimodal reasoning — analogous to what RLHF and RLAIF did for text reasoning — VLM reasoning capabilities will remain bounded by frontier closed-source model quality.

---

## Significance

LLaVA-CoT is notable for two contributions to [[themes/reasoning_and_planning|reasoning research]]:

1. **Structured format as a training target** — demonstrating that explicitly tagging reasoning stages as a supervised training objective (not just a prompt format) produces substantially better reasoning than unstructured CoT prompting. The structured tags encode a cognitive architecture that the model learns to follow autonomously.

2. **Stage-level retracing as a scaling mechanism** — identifying that the plateau in VLM test-time scaling is attributable to the inability to correct upstream stage errors, and that introducing a retracing mechanism at stage boundaries (rather than token or sentence boundaries) breaks this plateau.

The broader implication is that the granularity at which test-time search operates matters for [[themes/test_time_compute_scaling|test-time compute scaling]]: semantically meaningful stage boundaries outperform arbitrary token/sentence boundaries, and the ability to revise upstream stages is necessary (not just sufficient) for continued scaling gains.

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/mmbench|MMBench]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/scienceqa|ScienceQA]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/vlmevalkit|VLMEvalKit]]
