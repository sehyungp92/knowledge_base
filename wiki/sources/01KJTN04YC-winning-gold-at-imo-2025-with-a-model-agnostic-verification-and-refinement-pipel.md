---
type: source
title: Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement
  Pipeline
source_id: 01KJTN04YCTMRTN22442JC56F3
source_type: paper
authors:
- Yichen Huang
- Lin F. Yang
published_at: '2025-07-21 00:00:00'
theme_ids:
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
# Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline

**Authors:** Yichen Huang, Lin F. Yang
**Published:** 2025-07-21 00:00:00
**Type:** paper

## Analysis

# Winning Gold at IMO 2025 with a Model-Agnostic Verification-and-Refinement Pipeline
2025-07-21 00:00:00 · paper · Yichen Huang, Lin F. Yang
https://arxiv.org/pdf/2507.15855

---

### Motivation & Prior Limitations
LLMs capable of solving grade-school and AIME-level mathematics still fail badly at Olympiad-level proof generation, where logical rigor and novelty are required rather than pattern retrieval. Even with best-of-32 post-selection at inference time, state-of-the-art models achieved only 31.6% (Gemini 2.5 Pro), 21.4% (Grok-4), and 38.1% (GPT-5) on IMO 2025 problems.
- Single-pass generation is fundamentally limited by finite reasoning budgets: Gemini 2.5 Pro's maximum of 32,768 thinking tokens is routinely exhausted before a complete IMO proof is produced, leaving the model unable to finish its own argument in one query.
- IMO problems are specifically selected for novelty, ruling out the pattern-matching and training-data retrieval strategies that inflate AIME performance; models must produce original multi-step reasoning and logically sound proofs rather than adapted solutions.
- The prior leading result (AlphaProof/AlphaGeometry 2, silver medal at IMO 2024) relied on formal language (Lean) verification, producing machine-verified but human-unreadable proofs and requiring specialized domain solvers, leaving the natural-language proof generation problem unsolved.
- High-quality verifier feedback is a known bottleneck for self-correction methods in general, making it unclear whether iterative refinement could be made reliable enough for extreme-rigor settings like the IMO.

---

### Proposed Approach
The paper presents a model-agnostic, prompt-engineered verification-and-refinement pipeline that wraps any capable LLM in a structured loop of generation, self-improvement, verification, bug-report review, and correction — entirely in natural language, without formal proof tools or domain-specific solvers.
- Unlike AlphaProof's Lean-based approach, the pipeline produces human-readable mathematical proofs compatible with standard mathematical communication and enabling human-AI collaboration; it is also model-agnostic, demonstrated across Gemini 2.5 Pro, Grok-4, and GPT-5 without architecture changes.
- The solver prompt (Step 1) explicitly prioritizes rigor over answer-finding and requires the model to report partial results honestly rather than fabricate plausible-looking but flawed completions; Step 2 injects a second reasoning budget via a self-improvement pass, directly addressing the token-budget exhaustion problem.
- The verifier (Step 3) performs step-by-step analysis and classifies issues into two types: critical errors (logical fallacies or factual mistakes that invalidate the proof chain) and justification gaps (incomplete arguments that may still have a correct conclusion). The distinction allows downstream correction steps to triage severity.
- An optional bug-report review step (Step 4) filters false positives from the verifier before correction, analogous to peer review — authors (the solver) can contest referee (verifier) judgments, improving presentation even when the verifier errs.
- Acceptance requires passing five consecutive independent verifier runs, providing statistical robustness against the verifier's own occasional errors; the full pipeline can run instances in parallel or serially to increase the probability of finding a correct solution.

---

### Results & Capabilities
The pipeline solved 5 out of 6 IMO 2025 problems (≈85.7%) with each of three base models, representing a 2–4× improvement over those models' baseline best-of-32 accuracies and demonstrating consistent performance independent of which base model is used.
- Baseline best-of-32 accuracies were 31.6% (Gemini 2.5 Pro), 21.4% (Grok-4), and 38.1% (GPT-5); the pipeline raised all three to the same ≈85.7%, isolating the pipeline's contribution from model-specific capability differences.
- IMO 2025 was used as the evaluation benchmark precisely because Gemini 2.5 Pro and Grok-4 were released before the competition, making it a clean, contamination-free testbed; GPT-5 (released after) still shows a comparable lift that cannot be explained by contamination alone, since contamination would affect both the baseline and pipeline evaluations equally.
- Independent third-party validation on the IMC 2025 (university-level mathematics, broader knowledge base than IMO) showed the pipeline with Gemini 2.5 Pro achieving 94.5% accuracy, ranking #3 among 434 human participants, versus 57.7% (rank #92) for the base model alone — on a dataset released after the pipeline's public code, ruling out contamination.
- General hints (e.g., "use induction," "use analytic geometry") improved efficiency on Problems 1 and 2 in early experiments but were not necessary for correctness; hint-free solutions were subsequently obtained for all five solved problems, confirming the pipeline's capability without problem-specific guidance.

---

### Implications
The results establish that strong base models already possess latent mathematical reasoning capability sufficient for gold-medal IMO performance, and that inference-time methodology — not only model scaling — is a primary lever for converting that capability into rigorous proofs. This reframes the path toward advanced AI reasoning as a two-dimensional problem: base model capability and inference-time pipeline design are complementary, not substitutes.
- The model-agnostic nature of the pipeline means improvements carry forward automatically as base models improve, and any future frontier model can be plugged in without redesigning the methodology.
- The natural-language output paradigm, as opposed to formal verification, makes the pipeline's proofs directly accessible to mathematicians for critique and extension, enabling a practical human-AI collaboration mode that Lean-based systems do not support.
- The structured verifier design — separating critical errors from justificati

## Key Claims

1. A model-agnostic verification-and-refinement pipeline equipped with any of Gemini 2.5 Pro, Grok-4, or GPT-5 correctly solved 5 out of 6 IMO 2025 problems (~85.7% accuracy).
2. The baseline accuracies of leading LLMs on IMO 2025, using best-of-32 candidate selection, were only 31.6% (Gemini 2.5 Pro), 21.4% (Grok-4), and 38.1% (GPT-5).
3. State-of-the-art LLMs struggle to generate sound, rigorous proofs for Olympiad-level problems, often committing logical fallacies or using superficial heuristics.
4. GSM8K and MATH benchmarks, testing grade-school and high-school mathematics, have been largely solved by leading LLMs.
5. Formal language proofs (e.g., Lean) guarantee correctness but sacrifice human readability, making them inaccessible to most mathematicians.
6. Gemini 2.5 Pro's maximum thinking budget of 32,768 tokens is insufficient to solve a typical IMO problem in a single pass.
7. The self-improvement step (Step 2) effectively injects an additional reasoning budget and consistently produces noticeably improved outputs.
8. The verifier seldom misses critical errors; when it does, running it a few more times will very likely catch them.
9. The verifier may incorrectly flag trivial statements as justification gaps, but this does not significantly harm the overall pipeline's robustness.
10. A solution is accepted only if it passes verification five consecutive times without any issues.

## Capabilities

- Model-agnostic verification-and-refinement pipeline achieves 85.7% accuracy (5/6 problems) on IMO 2025 using any of Gemini 2.5 Pro, Grok-4, or GPT-5 — a dramatic improvement over single-pass best-of-32 baselines of 21–38%
- Natural language (human-readable) proof generation at Olympiad level — producing rigorous proofs legible to mathematicians without requiring formal verification languages like Lean
- Verification-and-refinement pipeline achieves 94.5% accuracy on IMC 2025 undergraduate mathematics, ranking #3 among 434 human participants — demonstrating generalisation beyond pre-university Olympiad scope
- Iterative verifier-guided self-improvement loop as an effective test-time compute strategy: decomposing reasoning across multiple budgeted steps recovers capability that single-pass generation loses to context/compute limits

## Limitations

- Maximum per-query reasoning budget (e.g. 32,768 thinking tokens for Gemini 2.5 Pro) is insufficient to solve a typical IMO problem in a single pass — even trivial sub-proofs consume thousands of tokens, exhausting the budget before the problem is resolved
- Complex combinatorial reasoning remains a consistent failure mode across all three frontier models even within the verification-and-refinement framework — Problem 6 (combinatorial tiling) was unsolved by Gemini 2.5 Pro, Grok-4, and GPT-5
- Single-pass solution quality for Olympiad-level problems is extremely low — models almost always produce flawed or incomplete solutions without the pipeline, making the pipeline a necessary rather than optional enhancement
- More powerful model variants (Gemini 2.5 Pro Deep Think, Grok-4 Heavy, GPT-5 Pro) are not accessible via API, preventing their integration into automated verification pipelines — a hard engineering gate on near-term capability extension
- Web search cannot be disabled for the most powerful model variants (Gemini 2.5 Pro Deep Think, Grok-4 Heavy, GPT-5 Pro), preventing fair evaluation on any benchmark problem whose solution exists online — creating an unresolvable evaluation contamination risk for published competition problems
- Current pipeline operates in a single-model paradigm where the same LLM acts as both solver and verifier — systematic reasoning errors that afflict the model will appear in both roles, reducing the independence of verification
- LLM verifier produces false positives (reporting errors that are not real issues, particularly for minor justification gaps at or near trivial statements) and false negatives (occasionally missing genuine errors) — no quantitative characterisation of error rates provided
- AIME 2025 is partially contaminated — 8 out of 30 problems had close analogs in online sources prior to the competition — reducing its validity as a test of genuine novel mathematical reasoning for models trained on internet data
- Reasoning budget control is absent or coarse-grained for Grok-4 and GPT-5 — Grok-4 does not allow any adjustment of reasoning effort, and GPT-5 only supports categorical settings — preventing fine-grained compute allocation in the pipeline

## Bottlenecks

- Finite per-query reasoning budget is insufficient for single-pass generation of complete, rigorous proofs for hard mathematical problems — the constraint forces pipeline decomposition as a workaround rather than a fundamental solution
- Generating high-quality verifier feedback for self-correction is a known bottleneck for iterative refinement — without a carefully designed verifier that distinguishes critical errors from justification gaps, self-improvement loops fail to converge on rigorously correct proofs
- Complex combinatorial reasoning — particularly spatial tiling and constraint-satisfaction proofs — remains unsolvable by current models even with a verification-and-refinement pipeline, indicating a structural gap beyond what iterative self-correction can address

## Breakthroughs

- A model-agnostic, prompt-only verification-and-refinement pipeline achieves 85.7% accuracy (5/6 problems) on IMO 2025 in natural language — without formal verification languages, without model fine-tuning, and consistently across three independent frontier models

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/alphaproof|AlphaProof]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gpt-5|GPT-5]]
- [[entities/gsm8k|GSM8K]]
- [[entities/gemini-25-pro|Gemini 2.5 Pro]]
- [[entities/math-dataset|MATH Dataset]]
