---
type: source
title: 'Large Language Monkeys: Scaling Inference Compute with Repeated Sampling'
source_id: 01KJV5MK13QFXGWZX2B14E1256
source_type: paper
authors:
- Bradley Brown
- Jordan Juravsky
- Ryan Ehrlich
- Ronald Clark
- Quoc V. Le
- Christopher Ré
- Azalia Mirhoseini
published_at: '2024-07-31 00:00:00'
theme_ids:
- code_and_software_ai
- code_generation
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Large Language Monkeys: Scaling Inference Compute with Repeated Sampling

Repeated sampling — independently generating many candidate solutions and selecting via automatic verification — is a simple, training-free mechanism that yields consistent, predictable coverage gains across four orders of magnitude in sample budgets, multiple model families, and diverse task types. The paper establishes empirical inference-time scaling laws analogous to training scaling laws, demonstrates that open-source models with large sample budgets can exceed the single-sample performance of frontier closed models at lower cost, and identifies verification quality (not generation coverage) as the binding constraint for realising the full value of inference-time compute.

**Authors:** Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, Azalia Mirhoseini
**Published:** 2024-07-31
**Type:** paper

---

## Core Contribution

The paper argues that inference compute is a neglected but viable second scaling axis alongside training compute. At the time of publication, [[themes/scaling_laws|training scaling laws]] had been extensively characterised and used to guide investment decisions, but no analogous framework existed for inference-time scaling through repeated sampling. Meanwhile, the single-sample SWE-bench Lite SOTA — achieved by a mixture of GPT-4o and Claude 3.5 Sonnet — sat at 43%, leaving headroom that stronger models alone had not closed.

The proposed framework decouples the problem cleanly into two orthogonal sub-problems:

- **Coverage** — can *any* sample solve the problem? Measured via the unbiased pass@k estimator.
- **Precision** — can a verifier reliably identify the correct sample from the set?

This decomposition lets each axis be studied and improved independently, and immediately clarifies where the real bottleneck lies.

---

## Inference-Time Scaling Laws

Coverage as a function of sample count k follows an **exponentiated power law**:

> c ≈ exp(ak^b)

where a and b are fitted per model-task pair. In log space, this is often approximately linear — coverage vs. log(k) traces a near-straight line across most model-task combinations, with mean fit error as low as 0.003 ± 0.003 for Llama-3-8B-Instruct on MATH.

This holds across:
- Four orders of magnitude in sample count (1 to 10,000)
- Model sizes from 70M (Pythia) to 70B (Llama-3)
- Model families: Llama-3, Gemma, Pythia
- Tasks: GSM8K, MATH, MiniF2F-MATH, CodeContests, SWE-bench Lite

A structurally important finding about within-family scaling: **coverage curves share the same slope but differ only by a horizontal offset in log-sample space**. A stronger model is not a different scaling regime — it is a multiplicative shift in the sample budget required to achieve equivalent coverage. This implies that training scaling and inference scaling may be partially substitutable along a common axis, with implications for how compute should be allocated across training vs. inference.

---

## Empirical Results

**SWE-bench Lite (software engineering):** DeepSeek-Coder-V2-Instruct with Moatless Tools improves from 15.9% (1 sample) to **56% (250 samples)**, exceeding the single-sample SOTA of 43% by 13 percentage points — surpassing the best mixed closed-source system at the time.

**Cost efficiency:** Sampling five times from DeepSeek-Coder-V2-Instruct (~$10.80 total) solves 29.62% of SWE-bench Lite issues — more than single samples from GPT-4o (24%, ~$39) or Claude 3.5 Sonnet (26.7%, ~$51) at 3–5× lower cost. This restructures the cost-capability tradeoff and reduces dependence on closed, expensive APIs.

**CodeContests:** Gemma-2B coverage increases over **300×**, from 0.02% (pass@1) to 7.1% (pass@10k). Pythia-160M on MATH increases from 0.27% to 57% over the same range.

**Optimal model size is task-dependent:** At fixed FLOP budgets, Llama-3-8B-Instruct dominates on MATH and GSM8K at all budgets, while the 70B model is more efficient on CodeContests. No universal compute-optimal size rule exists across task types.

---

## The Verification Bottleneck

The most consequential finding is the divergence between coverage and selection precision at scale.

For MATH with Llama-3-8B-Instruct:
- Coverage grows from **82.9% → 98.44%** as samples increase from 100 to 10,000
- Majority voting and reward model accuracy grow from **40.50% → 41.41%** over the same range

Verification **plateaus at approximately 100 samples** and then stagnates while the pool of correct solutions continues to expand. The gap between what the model *can* solve and what the system *retrieves* widens monotonically with scale.

Crucially, this is not a signal absence problem. Human evaluation of 105 Llama-3-8B-Instruct chains-of-thought on GSM8K finds **over 90% are logically faithful** — even for problems where correct answers appear in fewer than 10% of attempts. The signal is there; current verifiers cannot exploit it.

This reframes the research priority: the bottleneck to realising inference-time scaling is **not** making models solve problems more often. It is making verifiers reliably find the rare correct solution among many incorrect ones.

Repeated sampling is also **fundamentally inapplicable to open-ended tasks** (creative writing, general reasoning) where automatic verifiers do not exist, and where majority voting and reward model limitations are immediately binding rather than emerging at large k.

---

## Limitations and Open Problems

**Diversity mechanism is narrow.** All sample diversity derives from temperature-based stochasticity. No higher-level diversity mechanisms (varied prompting strategies, decomposition scaffolds, search-based exploration) are used, potentially limiting coverage gains on hard problems requiring qualitatively different solution approaches rather than surface-level variation.

**Attempts are fully independent.** Models cannot learn from or iterate on previous failed attempts. Access to execution feedback from earlier samples — analogous to multi-turn refinement — could substantially improve efficiency, but is currently unimplemented.

**Minimum capability prerequisite.** Pythia models achieve **zero coverage on CodeContests even with 10,000 samples**, revealing that repeated sampling provides no benefit below a minimum domain-competence threshold. The technique amplifies latent capability; it cannot create capability that does not exist.

**Benchmark reliability issues.** 11.3% of SWE-bench Lite problems have flaky test suites that produce inconsistent results on identical candidate solutions — occasionally misclassifying gold-standard solutions as incorrect. On CodeContests, 35 of 122 Python problems (28.7%) have correct solutions that fail the test suite due to multiple valid outputs not being handled or malformed test cases, creating systematic false negatives.

**Scaling law imprecision.** Inference-time scaling laws are less precise than training scaling laws. Coverage curves on some tasks (e.g., MiniF2F-MATH for Llama-3-8B-Instruct) do not fit the exponentiated power law model well. The laws provide directional guidance, not exact predictions.

---

## Connections and Implications

This work sits at the intersection of several active themes:

- **[[themes/test_time_compute_scaling|Test-time compute scaling]]:** Establishes the empirical foundation for treating inference compute as a principled scaling axis, complementing concurrent work on chain-of-thought budgeting, tree search, and process reward models.
- **[[themes/scaling_laws|Scaling laws]]:** Extends the scaling law paradigm from training to inference, with the horizontal-offset finding suggesting partial substitutability between training and inference compute.
- **[[themes/code_and_software_ai|Code and software AI]] / [[themes/code_generation|Code generation]]:** The SWE-bench Lite results have immediate practical relevance — parallelising cheap agentic attempts and selecting via unit tests is a deployable pattern for software agent systems.
- **[[themes/reasoning_and_planning|Reasoning and planning]]:** The verification plateau finding suggests that reasoning quality in individual samples is not the binding constraint — the ability to *evaluate* reasoning quality is.

The bottleneck identification has an immediate structural implication: research investment in inference-time scaling should flow toward **verifier quality and generality**, not toward improving pass@1. Reward models that can score open-ended reasoning, learned verifiers that generalise across domains, and process-level verification that exploits faithful chain-of-thought are the natural next steps.

For practical deployment, the cost-efficiency results suggest a concrete pattern: for any task with automatic verification (code execution, unit tests, formal proof checkers, mathematical solvers), consider replacing a single expensive frontier model call with many cheaper model calls, especially when the task admits parallelisation.

---

## Key Claims

1. Coverage scales with sample count over four orders of magnitude, consistently across model families and task types.
2. The coverage-vs-samples relationship follows an exponentiated power law c ≈ exp(ak^b), constituting inference-time scaling laws.
3. Within a model family, coverage curves share slope but differ by horizontal offset in log-sample space — model capability is a multiplicative shift in sample budget, not a change in scaling rate.
4. DeepSeek-Coder-V2-Instruct reaches 56% on SWE-bench Lite with 250 samples, exceeding the single-sample SOTA of 43%.
5. Five samples from DeepSeek-Coder-V2-Instruct outperforms single samples from GPT-4o and Claude 3.5 Sonnet at 3–5× lower cost.
6. Majority voting and reward model selection plateau at ~100 samples while coverage continues to grow — a widening gap at scale.
7. Over 90% of Llama-3-8B-Instruct chains-of-thought on GSM8K are logically faithful, even on hard problems — the verification gap is not a signal absence problem.
8. Pythia models achieve zero coverage on CodeContests at 10,000 samples, confirming that minimum baseline domain capability is a prerequisite.
9. Optimal model size for inference-time FLOP efficiency is task-dependent: 8B dominates on MATH/GSM8K; 70B dominates on CodeContests.
10. 11.3% of SWE-bench Lite problems have flaky test suites; 28.7% of CodeContests Python problems have false-negative test failures.

## Key Concepts

- [[entities/codecontests|CodeContests]]
- [[entities/gsm8k|GSM8K]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/passk|pass@k]]
- [[entities/passk-metric|pass@k metric]]
