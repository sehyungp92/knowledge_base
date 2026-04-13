---
type: source
title: 'Maestro: Self-Improving Text-to-Image Generation via Agent Orchestration'
source_id: 01KJTJQZ8YJN8GENQ8RK31WS4C
source_type: paper
authors:
- Xingchen Wan
- Han Zhou
- Ruoxi Sun
- Hootan Nakhost
- Ke Jiang
- Rajarishi Sinha
- Sercan Ö. Arık
published_at: '2025-09-12 00:00:00'
theme_ids:
- agent_self_evolution
- agent_systems
- generative_media
- image_generation_models
- multi_agent_coordination
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Maestro: Self-Improving Text-to-Image Generation via Agent Orchestration

**Authors:** Xingchen Wan, Han Zhou, Ruoxi Sun, Hootan Nakhost, Ke Jiang, Rajarishi Sinha, Sercan Ö. Arık
**Published:** 2025-09-12 00:00:00
**Type:** paper

## Analysis

# Maestro: Self-Improving Text-to-Image Generation via Agent Orchestration
2025-09-12 · paper · Xingchen Wan, Han Zhou, Ruoxi Sun, Hootan Nakhost, Ke Jiang et al. (7 total)
https://arxiv.org/pdf/2509.10704v1

---

### Motivation & Prior Limitations
- Text-to-image models are highly sensitive to prompt formulation yet users routinely under-specify their prompts, creating a usability gap that forces costly manual, iterative prompt engineering to achieve satisfactory results.
  - Users frequently provide prompts lacking the necessary detail or nuance, and models have been found to prefer detailed, descriptive prompts over abstract concepts requiring implicit reasoning (Niu et al., 2025; Hahn et al., 2024).
- Train-time automated prompt optimization (APO) methods such as Promptist require large-scale labeled datasets, are bottlenecked by annotation cost and training data coverage, and cannot incorporate visual feedback from actual generated images at test time.
  - A bespoke optimizer model must be retrained with newly generated datasets whenever the underlying T2I or MLLM components advance, making these approaches structurally brittle to model progress.
- Existing test-time methods that use MLLMs for critique largely reduce them to scalar reward models (e.g., DSGScore, CLIPScore), failing to exploit their reasoning and generative capabilities, and methods that forgo explicit objectives have no principled mechanism for maintaining the best candidate across iterations.
  - Proxy pointwise metrics show poor correlation with human perceptual judgments (Ross et al., 2024), and prior iterative methods typically return the generation from the final step rather than tracking the global best, making optimization unstable.
- Evaluating generated image quality is inherently subjective and multifaceted — encompassing prompt fidelity, aesthetics, coherence, and style — with no objective ground-truth reference, making it structurally different from text-based APO where task objectives are well-defined.

---

### Proposed Approach
- Maestro is a test-time, model-agnostic multi-agent orchestration system that autonomously refines T2I outputs through iterative prompt evolution, requiring only an initial user prompt as input.
  - Unlike train-time methods, it requires no labeled data, no dedicated fine-tuned model, and can immediately benefit from advances in MLLM capabilities without retraining.
- At initialization, Maestro generates an initial LLM proposal by rewriting the user prompt against T2I best-practice guidelines, and concurrently decomposes the user prompt into Decomposed Visual Questions (DVQs) — structured yes/no questions probing each desired property of the image — using a two-pass LLM pipeline for improved coherence and precision.
- During each iteration, two complementary prompt generators operate on the current best prompt-image pair: (1) **targeted editing**, which identifies DVQs where the MLLM judge answered "No", prompts the MLLM to generate a textual rationalization of why the image failed that criterion, and derives a specific corrective prompt edit; and (2) **implicit improvement**, which prompts a powerful MLLM to assess the best image holistically against both the original and best prompts and propose general enhancements without being tied to the predefined DVQs.
  - Targeted editing uses DVQ responses as interpretable textual gradients rather than aggregated scalar scores, directly leveraging the MLLM's reasoning capability to produce actionable, human-readable edit signals — a qualitative departure from prior work (Mañas et al., 2024) that used binary VQA scores only numerically.
- A pairwise Comparator tracks the globally best prompt-image pair across iterations via a binary tournament of head-to-head MLLM-as-a-judge comparisons, querying the judge 2n times with randomized image position to reduce position bias, and maintaining the incumbent best rather than naively returning the last iteration's output.
  - This directly optimizes against pairwise preferences — analogous to RLHF/RLAIF — without training an intermediate reward model, avoiding the approximation errors and biases of a Bradley-Terry scalar proxy.
- A self-verification block checks all newly generated prompts against the original DVQs and iteratively self-corrects any core concept violations, addressing the risk of semantic drift where iterative editing causes the prompt to diverge from the user's original intent.

---

### Results & Capabilities
- Maestro consistently outperforms all baselines on both benchmark datasets (PartiPrompts "p2-hard" and DSG-1K) across automatic pairwise (AutoSxS) and pointwise (DSGScore) metrics, as well as human preference evaluations.
  - On p2-hard, Maestro achieves a DSGScore of 0.921 ± 0.10, compared to OPT2I at 0.900, Promptist at 0.873, LM-BBO at 0.859, Rewrite at 0.855, and Original at 0.826.
  - In AutoSxS pairwise evaluation (using Gemini 2.0 Flash as an independent judge), Maestro wins 73.2% of comparisons against the original prompt and 75.5% against OPT2I on p2-hard; on DSG-1K, it wins 78.3% against original and 69.9% against OPT2I.
  - Maestro outperforms OPT2I on DSGScore despite OPT2I explicitly optimizing DSGScore as its objective, while Maestro optimizes a pairwise preference signal.
- In human side-by-side evaluation against LM-BBO (the next strongest baseline), Maestro was preferred by 55.8% of judgments (aggregated across 3 respondents) versus 44.2% for LM-BBO, and this preference rate aligns closely with the AutoSxS automatic ratings, validating the pairwise evaluation design.
- Qualitative examples demonstrate that Maestro can steer generation toward highly specific, domain-specific or conceptually complex outputs that generic generation fails to produce — including Jeff Koons-style balloon animal texture on a Thanos statue, self-similar fractal Sierpiński triangle pyramids, and accurate text rendering on the Hubble Telescope.
- Maestro's effectiveness scales wit

## Key Claims

1. T2I models are highly sensitive to input prompts, with generated images varying drastically even when prompts are semantically equivalent.
2. Users frequently under-specify their desired output, providing prompts that lack necessary detail or nuance for optimal results.
3. T2I models show a preference for detailed, descriptive prompts over abstract concepts that require implicit reasoning.
4. Maestro enables T2I models to autonomously self-improve generated images through iterative prompt evolution, requiring only an initial user prompt.
5. Maestro uses specialized MLLM agents as critics that generate interpretable edit signals rather than scalar reward scores.
6. Maestro's effectiveness scales with the capabilities of the MLLM components used within the multi-agent framework.
7. Aggregating DVQ scores via simple averaging or summing shows poor correlation with human perceptual judgments.
8. Train-time prompt optimization methods are limited by dependence on large-scale datasets, poor generalization to new tasks and models, and the need to retrain when foundational models advance.
9. Test-time prompt optimization approaches are model-agnostic with respect to the underlying T2I generator and require no dedicated training phase or large-scale data collection.
10. Existing test-time iterative optimization methods often fail to address user prompt under-specification because they generate new prompts by paraphrasing the original under-specified prompt.

## Capabilities

- Multi-agent T2I prompt optimization system (Maestro) achieves autonomous iterative self-improvement of image generation from an initial user prompt alone, outperforming all tested SOTA automated methods (Promptist, LM-BBO, OPT2I) on complex T2I benchmarks
- MLLM-as-judge pairwise comparison reliably substitutes for scalar reward models in iterative visual generation optimization, with automatic pairwise judgments correlating well with human preference evaluations
- MLLM critics generating textual edit signals (rather than scalar reward scores) combined with decomposed visual questions enable targeted, interpretable prompt repair for T2I generation — correcting specific image deficiencies via rationale-grounded suggestions
- Simple LLM rewrite of user prompts using prompt engineering best-practice guidelines competes with or outperforms dedicated fine-tuned prompt optimization models on challenging T2I tasks, suggesting frontier LLMs have largely subsumed the need for specialised prompt-optimizer training
- Test-time multi-agent orchestration can be layered over black-box T2I APIs without model access to achieve iterative quality improvement, with gains scaling proportionally with the capability of the orchestrating MLLM

## Limitations

- Maestro incurs substantially higher computational cost and latency than single-pass generation — up to 8 T2I calls plus multiple MLLM calls per iteration (DVQ scoring, targeted critique, implicit improvement, 2n pairwise judge queries) across multiple iterations
- Evaluation is limited to a single T2I model (Imagen 3 at Google Cloud) — performance generalisation across other T2I systems (DALL-E, Stable Diffusion, Midjourney, Flux) is unvalidated
- Scalar proxy metrics for T2I image quality (DSGScore, CLIPScore, image reward models) weakly correlate with human perceptual judgements — fundamentally limiting any automated optimization objective that uses them as the sole signal
- Iterative non-semantically-equivalent prompt editing introduces semantic drift from the user's original intent, with drift compounding across iterations as each edit builds on the previous modified prompt
- Human evaluation is preliminary and statistically underpowered — only 3 respondents in the human preference study, making alignment results between automatic metrics and human judgement statistically uncertain
- System performance depends critically on access to frontier MLLMs (Gemini 1.5 Pro, Gemini 2.0 Flash) as critics and judges — performance with weaker, smaller, or open-source models is uncharacterised and likely substantially degraded
- Evaluation uses filtered 'hard' samples where T2I model cannot achieve perfect quality across 8 repeated attempts — results may not represent improvement magnitude on typical everyday user prompts or easy cases
- Position bias in MLLM-as-judge pairwise comparison introduces systematic evaluation noise that requires 2n parallel queries to mitigate, further multiplying the computational overhead of each comparison
- Train-time prompt optimization models (Promptist and equivalents) become outdated rapidly as T2I and MLLM architectures advance, requiring retraining on freshly generated datasets to remain competitive — a recurring engineering cost with no clear resolution
- No systematic analysis of Maestro failure cases — the system lacks an explicit failure detection mechanism and paper does not analyse the ~9-35% of cases where Maestro loses to baselines in pairwise evaluation

## Bottlenecks

- Absence of principled, scalable objective metrics for visual generation quality blocks automated optimization — image quality is inherently subjective and multidimensional with no reference ground truth, making reliable scalar reward construction theoretically intractable
- Persistent user prompt under-specification creates a representational gap between user intent and T2I model input that single-pass generation cannot bridge — requiring systematic iterative or agentic intervention for reliable output quality
- High cost of test-time iterative T2I optimization limits practical deployment — multiple frontier MLLM plus T2I API calls per optimization step accumulate to costs and latencies incompatible with consumer-facing real-time use

## Breakthroughs

- Direct pairwise MLLM-as-judge optimization for T2I generation outperforms all scalar-objective and train-time methods without requiring training data or reward model approximation, demonstrating that subjective visual quality can be reliably optimised through iterative pairwise comparison alone

## Themes

- [[themes/agent_self_evolution|agent_self_evolution]]
- [[themes/agent_systems|agent_systems]]
- [[themes/generative_media|generative_media]]
- [[themes/image_generation_models|image_generation_models]]
- [[themes/multi_agent_coordination|multi_agent_coordination]]

## Key Concepts

- [[entities/bradley-terry-model|Bradley-Terry model]]
- [[entities/generative-reward-model|Generative Reward Model]]
- [[entities/position-bias|Position Bias]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
