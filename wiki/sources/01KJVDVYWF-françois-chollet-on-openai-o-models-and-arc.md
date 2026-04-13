---
type: source
title: François Chollet on OpenAI o-models and ARC
source_id: 01KJVDVYWFCKN89G9QS87E4ST5
source_type: video
authors: []
published_at: '2025-01-09 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- model_architecture
- reasoning_and_planning
- representation_learning
- search_and_tree_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# François Chollet on OpenAI o-models and ARC

> A wide-ranging technical post-mortem of the 2024 ARC Prize competition that reframes the results as evidence for a paradigm shift: System 2 reasoning cannot emerge from scale alone, and the surprising parity between compute-restricted and frontier-model submissions reveals that ideas — not raw compute — are the binding constraint on generalisation.

**Authors:** François Chollet
**Published:** 2025-01-09
**Type:** video

---

## Overview

Chollet uses the 2024 ARC Prize as a lens for diagnosing the broader state of AI reasoning. The competition produced two striking empirical findings: (1) a compute-restricted submission running on a P100 GPU for 12 hours (~$10) matched frontier-model submissions spending up to $10,000 in API credits at roughly 55% on the private test set; and (2) an ensemble of all 2024 submissions reached 81%, approaching the 85% human-level threshold — while individual humans solve 97–99% of tasks. These facts structure the rest of the analysis: compute is a multiplier for ideas, not a substitute for them.

The source covers two winning families of approaches — **program synthesis** (deep-learning-guided code generation and iterative debugging) and **test-time training** (transductive LLM fine-tuning on demonstration pairs) — and argues they are complementary rather than competing, because they solve fundamentally different task types.

---

## The 2024 ARC Competition: Key Results

| Metric | Score |
|---|---|
| Single best submission (2024, private test) | ~55% |
| Ensemble of all 2024 submissions | ~81% |
| Human performance | ~97–99% |
| Human-level threshold (ARC Prize definition) | 85% |
| Single best submission (2020, Kaggle) | ~20% |
| Ensemble of all 2020 submissions | ~49% |

The 2020 ensemble reaching 49% is itself diagnostic: it means roughly half the private test set was brute-forceable even then, pointing to a partial flaw in benchmark difficulty distribution. The gap between 49% (2020 ensemble) and 81% (2024 ensemble) represents genuine progress; the gap between 81% and 97%+ represents the remaining hard problem.

The compute-parity finding is the competition's most theoretically significant result. Compute budget spanned four orders of magnitude across submissions, yet scores clustered around the same value. This falsifies the hypothesis that frontier models have a privileged path to ARC via sheer inference-time compute — see [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]].

---

## Two Families of Approaches

### Program Synthesis (Induction)

Deep-learning-guided program synthesis uses LLMs to generate candidate programs and iteratively debug them against demonstration pairs. The goal is induction: find a program that maps inputs to outputs, then apply it to the test input. A less-explored variant uses building blocks from a DSL rather than free-form code.

**Strengths:** Algorithmic and discrete tasks; no performance drop between public and semi-private eval sets; solutions are verifiable by execution.

**Weaknesses:** Perceptual tasks with fuzzy, continuous decision boundaries resist symbolic encoding — writing a program to recognise a handwritten 'A' is a famously hard problem that neural networks handle trivially. Brute-force enumeration can in principle solve ARC at human level, but would cost hundreds of millions of dollars.

### Test-Time Training / Transduction

Transductive approaches use the demonstration pairs directly as fine-tuning signal: a base model pre-trained on ARC tasks is adapted at inference time to each new task via gradient descent on its weights. Without this test-time adaptation, LLM transduction is stuck below ~10% accuracy. With it, performance jumps into the 50–55% range.

**Strengths:** Perceptual tasks; flexible knowledge recombination via gradient descent in weight space; strong generalisation lift from small fine-tuning signal.

**Weaknesses:** Systematic overfitting to public evaluation sets — top solutions showed 10+ percentage point drops on semi-private eval, revealing learned spurious features. Program synthesis solutions showed no equivalent drop.

A more speculative variant performs gradient descent not in weight space but in a **learned latent program embedding space**, seeking a smooth intermediate between discrete search and full TTT. This approach can find solutions within latent space but lacks execution feedback — decoded programs cannot be verified without running them.

---

## Theoretical Framing: What ARC Tests

Chollet distinguishes two modes of reasoning:

- **Pattern memorisation and re-application** — what LLMs do well; fetching and reusing patterns seen during training.
- **Adapting to novelty by recombining cognitive building blocks** — what ARC requires; constructing new procedures from known primitives for problems never seen before.

The distinction maps onto the induction/transduction divide. Transduction via TTT approximates the second mode by allowing weight updates, but Chollet is explicit that gradient descent on weights is not how humans do it: humans recombine knowledge compositionally and symbolically, not via parameter optimisation — see [[themes/reasoning_and_planning|Reasoning and Planning]].

The claim that System 2 reasoning cannot emerge from pre-training scale is treated as settled by the competition results. The question has shifted to *how* to add it: test-time search, program synthesis, TTT, or some hybrid.

---

## Capabilities

- **Test-time training unlocks transductive generalisation.** Without TTT, LLM transduction scores below 10%; with TTT, it reaches 55%+. The demonstration pairs provide sufficient signal to recombine latent knowledge for novel tasks. (maturity: [[themes/model_architecture|research only]])
- **Latent program space gradient descent.** One approach learns a smooth embedding space of programs and performs gradient descent within it at test time — a middle ground between discrete search and weight-space TTT. (maturity: research only)
- **Ensemble complementarity.** Program induction and transductive methods solve substantially different task subsets; combining them reaches 81%, well above either alone. (maturity: research only)

---

## Limitations and Open Problems

### Architectural Limitations

- **Transformers cannot perform basic compositional operations** (copying, counting) reliably even with large data and long training. This is treated as an in-principle architectural constraint, not a data or scale issue. (severity: blocking)
- **Language models are finite-state automata** and lack compositional generalisation in principle — they cannot dynamically recombine knowledge in unbounded ways. See [[themes/model_architecture|Model Architecture]].

### Synthesis and Search Limitations

- **Brute-force program enumeration is computationally intractable** at human-level performance; achieving it would require hundreds of millions of dollars. The 2020 competition demonstrated this ceiling.
- **Programs are poor data structures for perception.** Perceptual tasks with fuzzy decision boundaries resist symbolic formalisation; the two method families solve complementary but non-overlapping task types. (severity: significant, trajectory: stable)
- **Latent program spaces lack execution feedback.** Gradient descent in latent space provides no correctness guarantee; solutions cannot be verified without decoding and executing the program. The ability to decode and run programs is identified as a critical missing capability. (severity: significant)
- **Heterogeneous program manifolds degrade optimisation.** Smooth, convex latent structure is necessary for gradient-descent-guided test-time search, but real program manifolds may have multiple disconnected modes. (severity: significant)

### Data and Evaluation Limitations

- **Synthetic ARC task generation collapses distribution diversity.** LLM-generated synthetic tasks remix limited conceptual primitives from the small training set; models trained on synthetic data severely overfit. (severity: significant)
- **Test-time compute confounds evaluation.** Performance scales logarithmically with compute budget; leaderboard rankings are meaningless without compute normalisation. No current benchmarking standard enforces this. (severity: significant, trajectory: improving — the compute-restricted track is a direct response)
- **Transductive solutions overfit to public eval.** Top TTT-based submissions score 10+ points lower on the semi-private set, indicating public eval contamination in learned features.

### Architecture Search as Bottleneck

- **Automated architecture search cannot identify structural priors for novel task classes.** Designing architectures that bake in inductive biases appropriate to unknown problem types requires understanding the problem — a circularity that makes the search problem at least as hard as the original task. (horizon: 3–5 years) See [[themes/model_architecture|Model Architecture]].

---

## Bottlenecks

| Bottleneck | What It Blocks | Horizon |
|---|---|---|
| Verification gap in latent program spaces | Scalable test-time adaptation via latent-space optimisation | 1–2 years |
| Synthetic data distribution collapse | Scaling program synthesis via data augmentation | 1–2 years |
| Evaluation unfairness from compute variance | Comparable reasoning system benchmarking | Months |
| Automated architecture search circularity | Autonomous compositional generalisation without human engineering | 3–5 years |

---

## Cross-Theme Implications

The program synthesis / transduction complementarity is more than a competition finding — it is a structural claim about [[themes/reasoning_and_planning|reasoning]]. Perceptual and algorithmic cognition are not on a spectrum; they require different computational substrates. This has implications for:

- [[themes/benchmark_design|Benchmark Design]]: ARC's task distribution inadvertently tests both modes, which is why no single approach dominates. Future benchmarks should track task-type coverage explicitly.
- [[themes/search_and_tree_reasoning|Search and Tree Reasoning]]: The failure of brute-force enumeration at tractable compute levels motivates learned heuristics and DL-guided search, not simply faster search.
- [[themes/representation_learning|Representation Learning]]: The latent program space approach depends on learning smooth, semantically meaningful embeddings of programs — a hard open problem in representation learning.
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]: The claim that LLMs are finite-state automata without compositional generalisation sets a hard ceiling on formal reasoning via pure next-token prediction.

---

## Key Claims Summary

1. System 2 reasoning will not emerge from pre-training scale; it must be explicitly engineered. *(claim 6)*
2. Compute is a multiplier for ideas — a $10 submission matched a $10,000 submission at 55%. *(claim 12)*
3. Transduction without test-time training is stuck below 10%; TTT unlocks ~55%. *(claim 3, 4)*
4. Program synthesis and transduction solve disjoint task subsets; ensemble reaches 81%. *(claim 14)*
5. Transformers cannot do basic compositional operations in principle. *(limitation: blocking)*
6. Transductive top solutions overfit to public eval by 10+ points. *(claim 13)*
7. Programming from input-output pairs will become a widespread non-technical paradigm. *(claim 5)*
8. Humans solve 97–99% of ARC tasks; the 85% threshold remains unbreached by any single system. *(claim 11)*

## Key Concepts

- [[entities/system-1-system-2-reasoning|System 1 / System 2 Reasoning]]
- [[entities/system-2-reasoning|System 2 Reasoning]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/test-time-training|Test-Time Training]]
