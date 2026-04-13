---
type: source
title: 'Generative Verifiers: Reward Modeling as Next-Token Prediction'
source_id: 01KJV7NM6AWC5CXT3SRS8DRN77
source_type: paper
authors:
- Lunjun Zhang
- Arian Hosseini
- Hritik Bansal
- Mehran Kazemi
- Aviral Kumar
- Rishabh Agarwal
published_at: '2024-08-27 00:00:00'
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Generative Verifiers: Reward Modeling as Next-Token Prediction

This paper challenges the architectural assumption that reward modeling requires a separate discriminative head, demonstrating that recasting verification as next-token prediction ("Is the answer correct? Yes/No") unlocks chain-of-thought reasoning, inference-time compute scaling, and strong out-of-distribution generalization for verifiers. The resulting GenRM and GenRM-CoT frameworks consistently outperform discriminative reward models, DPO verifiers, and LLM-as-a-Judge across algorithmic and mathematical reasoning benchmarks, with a 6.4x sample efficiency advantage on easy-to-hard generalization from grade-school to competition math.

**Authors:** Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, Rishabh Agarwal
**Published:** 2024-08-27
**Type:** paper

---

## Expert Analysis

### Motivation and Prior Limitations

Standard LLM-based verifiers are trained as discriminative classifiers that assign numerical scores to candidate solutions, which fundamentally discards the generative capabilities that pretrained LLMs are built around. Discriminative reward models use a binary cross-entropy loss over a special `[cls]` token logit, producing a scalar score that bypasses the model's generative capacity entirely, making it impossible to employ chain-of-thought reasoning or scale inference-time compute during verification.

The failure mode is concrete: a discriminative RM scored a plausible but incorrect GSM8K solution at 0.999 confidence, failing to detect that "each" was ignored in a bundle pricing problem; it similarly scored an incorrect MATH solution at 0.827 despite a clearly wrong algebraic simplification. [[themes/reward_modeling|LLM-as-a-Judge]], while generative, consistently underperforms trained verifiers on reasoning tasks because it lacks task-specific fine-tuning (achieving only ~5% Best-of-32 on algorithmic tasks versus 45.3% for GenRM-CoT). DPO-based verifiers attempt to unify policy and reward modeling but exhibit erroneous extrapolation and representation degradation without additional stabilization techniques.

### The GenRM Approach

GenRM recasts verification as next-token prediction by training a verifier to output a `Yes` or `No` token in response to the prompt "Is the answer correct (Yes/No)?", using the standard SFT cross-entropy loss rather than a discriminative classification head. The score at inference is simply `p_θ(Yes | x, y, I)`, the probability of the `Yes` token, which keeps the model fully generative and integrates naturally with instruction tuning.

**GenRM-CoT** extends this by prepending a chain-of-thought rationale before the final Yes/No token, trained with the prompt "Let's verify step by step." Rationales are generated synthetically using Gemini 1.0 Pro with *reference guidance* (providing a correct solution alongside the candidate during generation), then filtered by verification correctness. Reference guidance is crucial: without it, synthetic rationale quality degrades to ~50% accuracy (chance level), since the model has insufficient signal to reason about correctness. With it, Best-of-N on GSM8K improves from 87.8% to 91.7% for Gemma-7B verifiers.

**Majority voting** over K sampled CoT rationales scales inference-time compute: `r_MajV@K = (1/K) Σ p_θ(Yes | x, y, ICoT, v^(i)_CoT, I)`, averaging correctness probabilities to marginalize over reasoning path variance. This provides a direct mechanism for [[themes/test_time_compute_scaling|test-time compute allocation]] in [[themes/reward_modeling|reward modeling]], an advantage fundamentally unavailable to discriminative verifiers.

**Unified generation-verification training** is achieved via a single loss `L_GenRM = L_SFT(D_verify) + λ L_SFT(D_correct)`, jointly training the model to generate correct solutions and to verify candidate solutions. Teaching a model to critique solutions deepens its understanding of how to produce them.

---

## Key Claims

1. Generative verifiers trained with next-token prediction outperform discriminative RMs, DPO verifiers, and LLM-as-a-Judge on reasoning tasks under Best-of-N evaluation.
2. GenRM-CoT improves Best-of-N performance from 28% to 44.6% on MATH and from 37.9% to 53.5% on MMLU abstract algebra in easy-to-hard generalization settings, without any in-distribution training on those harder tasks.
3. On GSM8K, a Gemma2-9B GenRM-CoT verifier applied to Gemini 1.0 Pro solutions achieves 93.4% problems solved (Best-of-16), surpassing GPT-4 and Gemini 1.5 Pro.
4. GenRM-CoT demonstrates 6.4x better sample efficiency than discriminative verifiers on MATH (easy-to-hard generalization).
5. On algorithmic tasks, Best-of-32 accuracy improves from 5% (discriminative RM) to 45.3% (GenRM-CoT), nearly matching oracle verifier performance.
6. Majority voting over multiple sampled CoT rationales improves verification accuracy and scales favorably across model sizes (2B, 7B, 9B); greedy decoding performance is matched within ~2 majority votes.
7. Unified generation-verification training improves both tasks simultaneously: incorporating CoT verification data into a generator's training mix improves the generator's own solution generation.
8. Reference guidance during synthetic rationale generation is critical; unguided generation yields ~50% verification accuracy (chance level).
9. Adding excessive solution generation data to the joint training mix degrades verification performance, indicating a saturation point requiring careful hyperparameter tuning.
10. Discriminative RMs fail to detect subtle reasoning errors that CoT verifiers reliably catch, such as misinterpreting "each" in a bundle pricing problem or applying an incorrect algebraic simplification.

---

## Capabilities

**CoT-based verification achieves state-of-the-art Best-of-N performance on math reasoning** (maturity: demo). GenRM-CoT achieves 93.4% on GSM8K Best-of-16, up from 73% with discriminative RMs, and 45.3% on algorithmic Best-of-32, up from 5%. The framework nearly matches oracle verifier ceilings on algorithmic tasks.

**Explicit step-by-step error diagnosis** (maturity: demo). Chain-of-thought verifiers trained via next-token prediction detect subtle multi-step reasoning errors that discriminative reward models systematically miss, including errors requiring correct interpretation of natural language quantifiers.

**Inference-time scaling for verification** (maturity: demo). Generative verifiers scale favorably with both model size (2B to 9B) and inference-time compute (1 to 32 majority votes), consistently outperforming discriminative counterparts at all scales tested. See [[themes/test_time_compute_scaling|test-time compute scaling]].

**Out-of-distribution generalization from easy to hard math** (maturity: demo). Verifiers trained only on grade-school math (GSM8K) generalize to competition-level problems, achieving 44.6% on MATH500 versus 28% for discriminative RM, and 53.5% on MMLU abstract algebra versus 37.9%. The CoT verifier appears to develop more transferable representations of mathematical correctness than scalar classifiers.

**Scalable synthetic training data via reference-guided rationale generation** (maturity: demo). Reference-guided grading with a capable model (Gemini 1.0 Pro) produces sufficient synthetic rationale quality to train CoT verifiers that identify subtle math reasoning errors, without requiring human annotators. Increasing the number of synthetic rationales per training solution further improves performance via an ensembling effect.

---

## Limitations and Open Questions

**32x inference compute cost at best performance** (severity: significant, trajectory: improving). Achieving top GenRM-CoT verification performance requires 32 majority votes, multiplying verification compute cost by 32x compared to a single discriminative RM forward pass. This directly blocks cost-effective deployment in high-throughput Best-of-N pipelines. The trajectory is improving as majority voting requirements may decrease with better base models and training data.

**Synthetic rationale quality degrades to chance without reference guidance** (severity: significant, trajectory: improving). Naive synthetic rationale generation without providing a correct reference solution yields approximately 50% verification accuracy. The approach is fundamentally broken in this configuration, which means reference-guided generation (requiring access to ground-truth solutions) is a hard dependency for the training pipeline.

**Scope limited to math and algorithmic string tasks** (severity: significant, trajectory: unclear). The framework is only demonstrated on math and algorithmic string manipulation tasks. Coding, alignment, text-to-image generation, and open-ended generation are explicitly listed as future work with no experimental evidence. Generalization across task types is an open question.

**Human verification rationale generation becomes infeasible at frontier capability levels** (severity: significant, trajectory: worsening). As LLMs surpass human reasoning abilities, generating high-quality human verification rationales becomes increasingly difficult, creating an escalating data bottleneck for verifier training on the hardest problems.

**Individual CoT rationales are unreliable; reliability requires voting** (severity: minor, trajectory: improving). Individual verification rationales frequently contain their own reasoning errors. Verification reliability depends on majority voting across many samples rather than any single rationale being trustworthy, which links back to the compute cost concern.

**No process-level (step-by-step) supervision** (severity: significant, trajectory: improving). GenRM operates at the outcome level, verifying full solutions. It does not provide fine-grained intermediate error localization that process reward models (PRM) offer. Combining GenRM with process-level supervision is identified as a promising direction. See [[themes/reinforcement_learning|reinforcement learning]] and [[themes/reasoning_and_planning|reasoning and planning]].

**Generator-verifier separation untested** (severity: minor, trajectory: unclear). All experiments use a fixed, separate generator (Gemini 1.0 Pro) distinct from the Gemma verifier models. Performance when generator and verifier are the same model, or from different capability tiers, remains uninvestigated.

**Positive transfer degrades with noisy synthetic rationales** (severity: significant, trajectory: improving). The mutual benefit of unified generation-verification training is substantially weaker when using synthetic (potentially erroneous) rationales. The improvement is larger on algorithmic tasks using ground-truth verification data than on GSM8K with synthetic rationales.

---

## Landscape Significance

### A Reconceptualization of Verification

The central contribution is architectural: GenRM demonstrates that the boundary between "generator" and "verifier" in RLHF and Best-of-N pipelines is an artifact of discriminative design choices rather than a principled distinction. Verification is a natural extension of next-token prediction, not a separate task requiring a separate head. This reframing has immediate implications for how [[themes/reward_modeling|reward models]] are trained and how [[themes/test_time_compute_scaling|inference-time compute]] is allocated.

The easy-to-hard generalization result is particularly significant as a signal about what discriminative versus generative representations learn. A scalar classifier trained on GSM8K learns to predict "correct" for the distribution it saw. A CoT verifier trained on GSM8K learns to reason about mathematical correctness in a way that transfers to competition mathematics. This suggests that chain-of-thought reasoning during verification is not just a compute mechanism but a representational one: it forces the model to articulate *why* a solution is correct or incorrect, which generalizes across difficulty levels.

### Connection to Scaling Debates

GenRM provides an important data point in the [[themes/test_time_compute_scaling|test-time compute scaling]] literature: compute scaling applies to *verification*, not just generation. The majority voting mechanism over CoT rationales is structurally analogous to repeated sampling in generation (Best-of-N), but applied at the verification stage. This suggests a two-dimensional compute scaling space for reasoning pipelines: scale candidates generated, and scale verification compute per candidate.

### Bottlenecks This Raises

Two binding constraints emerge from this work:

1. **Synthetic rationale quality** is the current gating factor for scalable generative verifier training. Reference guidance is necessary but requires access to ground-truth solutions, which limits applicability to tasks with clear correctness criteria. Extending to open-ended domains requires either human rationales (expensive and increasingly infeasible) or a capable enough teacher model that can ground-truth verify without reference solutions.

2. **Verification compute cost** at 32 votes makes GenRM-CoT impractical as a drop-in improvement over discriminative RMs in high-throughput pipelines. The question of how to achieve GenRM-CoT-level accuracy with fewer votes (through better training data, larger base models, or distillation) is an open engineering challenge.

---

## Themes

- [[themes/reward_modeling|Reward Modeling]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]

## Key Concepts

- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/gsm8k|GSM8K]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/math500|MATH500]]
- [[entities/mmlu|MMLU]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
