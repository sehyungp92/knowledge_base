---
type: source
title: On the “ARC-AGI” $1 Million Reasoning Challenge
source_id: 01KJSY403HJYVESWF8XD2CQ8HT
source_type: article
authors: []
published_at: '2024-08-06 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- in_context_and_meta_learning
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# On the “ARC-AGI” $1 Million Reasoning Challenge

**Authors:** 
**Published:** 2024-08-06 00:00:00
**Type:** article

## Analysis

# On the "ARC-AGI" $1 Million Reasoning Challenge
2024-08-06 · article
https://aiguide.substack.com/p/on-the-arc-agi-1-million-reasoning

---

## Briefing

**ARC-AGI exposes a fundamental gap between current AI systems and human-like abstraction: while humans solve ~84% of tasks, the best AI methods reach only 43% — and even that progress is driven largely by brute-force computation rather than genuine few-shot reasoning. The $1M prize risk accelerating Goodhart's Law, where methods optimized to hit the 85% target may wholly bypass the benchmark's original purpose of measuring core-knowledge-grounded abstraction.**

### Key Takeaways
1. **ARC tests few-shot abstraction, not pattern interpolation** — Each task requires inferring an abstract transformation rule from only 3 demonstrations and applying it to a new grid, specifically targeting capabilities current LLMs largely lack.
2. **Human performance benchmark is ~84%, AI SoTA is 43%** — A large gap persists even after years of competition, with the MindsAI team holding first place at 43% on the private evaluation set as of writing.
3. **Greenblatt's 51% was on the public set, not the private one** — The widely circulated claim of a new SoTA was a confusion between public and private evaluation sets, and the method violated competition rules (internet access, time limits).
4. **Generate-test-revise with ~8,000 LLM calls per task** — Greenblatt's method generates 5,000 programs, selects 12 most promising, generates 3,000 more revisions, then majority-votes — raising serious questions about whether this constitutes abstraction at all.
5. **MindsAI's key innovation is test-time task augmentation ("active inference")** — Fine-tuning the LLM on augmented versions of each specific test task transforms a 3-shot problem into a many-shot one, which is a qualitatively different and more tractable problem.
6. **Data scarcity is a fundamental obstacle** — Only 400 training tasks exist; MindsAI's solution is synthetic task generation to augment fine-tuning, but the quality and generalization of these synthetic tasks remains unverified.
7. **Score improvements are largely compute-driven, not conceptual** — Both leading methods improve primarily by scaling up sampling and fine-tuning, not by implementing better reasoning mechanisms.
8. **Goodhart's Law is already activating** — As ARC becomes a $500K target, methods are being engineered specifically to hit the score rather than to instantiate the abstract reasoning capacities the benchmark was designed to measure.
9. **The chess analogy frames the core concern** — Good human chess players use abstraction to minimize search; current AI chess (and ARC) solutions invert this, substituting brute-force search for understanding — progress on ARC via search does not imply progress on abstraction.
10. **Dynamic evaluation sets could mitigate overfitting** — The author suggests continually rotating the 100-task private evaluation set to prevent methods from being tuned to a fixed target.
11. **ARC's 85% threshold is weakly motivated** — The grand prize threshold derives from the 84% human estimate from a single 2021 MTurk study on the easier training set, likely an overestimate for the harder evaluation sets.

---

### What ARC Is and Why It Matters

- ARC (Abstraction and Reasoning Corpus), created by François Chollet, is a benchmark of analogy puzzles requiring **few-shot abstraction over grid transformations**.
  - Each task presents 3 demonstration input-output grid pairs; the solver must infer the abstract transformation rule and apply it to a new test input.
  - The corpus spans 1,000 tasks: 400 in the public training set, 400 in the public evaluation set, and 200 in a never-revealed private evaluation set.
  - The benchmark deliberately targets **core knowledge concepts** and human-like generalization — capabilities the author argues are largely absent in current AI systems.
- The private evaluation set (or a 100-task subset) is used exclusively for scoring competition submissions and is never published, preserving its integrity as a holdout.
- ARC tasks are intentionally resistant to statistical pattern matching because the training distribution is small and the abstract rules are combinatorially diverse.

---

### The Human Performance Baseline and Its Weaknesses

- The commonly cited human benchmark of **~84%** comes from a single 2021 NYU study using Amazon Mechanical Turk workers on 40 randomly selected tasks from the training set.
  - The author explicitly notes this is **likely an overestimate**: the sample was drawn from the easier training set, not the harder evaluation set, and MTurk workers are a self-selected population.
  - Chollet's original claim that "a typical human can solve most of the ARC evaluation set without previous training" has never been formally tested to the author's knowledge.
- The 85% grand prize threshold was set in reference to the 84% human estimate, but the basis is fragile given the methodological limitations of that study.
  - The ARC Prize website describes the threshold as "high enough to consider ARC-AGI as solved, but low enough to acknowledge it is imperfect" — a somewhat circular justification.

---

### Competition History and the Evolution of SoTA

- In the **2020 Kaggle competition**, the winning method scored 21% on 100 tasks from the private evaluation set; the top-two ensemble reached 31%.
  - By comparison, vanilla LLMs (no special prompting) scored roughly 10% even on the easier training set.
- Subsequent competitions pushed the private-set SoTA to **34%** (MindsAI team, 2023), where it stagnated until the $1M prize drew renewed attention in mid-2024.
- As of the article's writing, MindsAI holds first place at **43%** on the private evaluation set, having incrementally improved over several months.
  - The author attributes most of this improvement to increased compute — more samples generated and more fine-tuning data — rather than architectural or rea

## Key Claims

1. ARC addresses few-shot abstraction, analogy, and generalization — capabilities largely lacking in current AI systems.
2. The ARC corpus contains 1,000 tasks: 400 in the training set, 400 in the public evaluation set, and 200 in an unpublished private evaluation set.
3. Human performance on ARC tasks is approximately 84%, based on a 2021 NYU study using Amazon Mechanical Turk workers on 40 randomly selected training tasks.
4. The winning method in the 2020 Kaggle ARC competition scored approximately 21% on a 100-task subset of the private evaluation set.
5. An ensemble of the top two methods in the 2020 Kaggle competition scored 31% on the private evaluation subset.
6. Large language models without significant prompt engineering score approximately 10% on the ARC training set.
7. The state-of-the-art on the 100-task ARC private evaluation set reached 34% prior to the ARC Prize announcement in 2024.
8. The ARC Prize was announced in June 2024, offering a $500,000 grand prize for any program scoring 85% or higher on 100 tasks from the private evaluation set.
9. Competition entries are constrained to 12 hours of run time with no internet access.
10. The 85% grand prize threshold was chosen because it exceeds the estimated 84% human performance while acknowledging the benchmark's imperfections.

## Capabilities

- GPT-4o with generate-test-revise program synthesis (generating ~5,000 programs per task, selecting and revising top 12 candidates, majority voting) achieves ~51% on ARC public evaluation set
- LLM fine-tuned on synthetic ARC task augmentations combined with test-time augmentation ('active inference') — additional fine-tuning on augmented demonstrations at inference — achieves 43% on ARC private evaluation set, the competition SoTA as of mid-2024
- Automatic synthetic ARC task generation via geometric and semantic variations of training tasks enables fine-tuning on effectively larger ARC datasets despite the small official training corpus of 400 tasks

## Limitations

- LLMs without substantial prompt engineering score only ~10% on ARC tasks — far below human performance of ~84% — demonstrating a fundamental gap in few-shot abstract rule inference
- Best AI performance on ARC private evaluation set (~43%) remains ~41 percentage points below estimated human performance (~84%), with the gap persisting across multiple years of competition
- The highest-performing LLM-based ARC approach requires internet access and more than 12 hours of compute — it cannot operate within standard competition constraints, meaning its headline results (~51%) are not reproducible under fair evaluation conditions
- Current ARC-solving methods rely on brute-force program enumeration and search rather than direct abstract rule inference — they compensate for lack of abstraction via massive candidate sampling, which is computationally expensive and unlikely to generalise
- MindsAI's performance improvements from 34% to 43% appear driven primarily by scaling compute and synthetic training examples rather than algorithmic progress, raising questions about the ceiling of this approach
- Effective LLM-based ARC solving requires ~30,000-token prompts with extensive manual engineering: multiple grid representations, difference encodings, and handwritten step-by-step reasoning examples — the approach is not self-contained
- Greenblatt's reported scores of 71% (training) and 51% (public evaluation) are sampled from only 100 of 400 tasks with ±5% standard error — the author acknowledges results 'might be slightly overoptimistic'
- The ARC training set contains only 400 tasks — insufficient for fine-tuning large neural networks without synthetic augmentation, creating a hard data ceiling for supervised approaches
- Synthetic ARC task augmentation generates variations of existing training tasks but may not capture conceptual diversity — the distribution of synthetic tasks is bounded by the original 400-task distribution's abstract rule vocabulary
- ARC is vulnerable to Goodhart's Law — the $500k prize incentivises methods that overfit to the fixed 100-task private evaluation set rather than solving the underlying abstract reasoning capability the benchmark was designed to measure

## Bottlenecks

- AI systems cannot perform few-shot abstract rule inference directly — the gap between compute-intensive search-based methods (~43%) and human performance (~84%) on ARC reflects a fundamental absence of humanlike abstraction; progress requires brute-force scaling rather than a reasoning advance
- The ARC private evaluation set is a fixed 100-task corpus — as competition incentives scale to $500k, methods can increasingly overfit to this distribution, breaking ARC's validity as a measure of generalised abstract reasoning

## Breakthroughs

- LLM-based generate-test-revise with massive program sampling achieved ~51% on ARC public evaluation set in June 2024, jumping ~17 points above the then-public-evaluation SoTA and demonstrating that LLM-based methods could meaningfully engage with ARC — though at prohibitive compute cost and outside 

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/in_context_and_meta_learning|in_context_and_meta_learning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/abstraction-and-reasoning-corpus-arc|Abstraction and Reasoning Corpus (ARC)]]
- [[entities/alphaproof|AlphaProof]]
- [[entities/benchmark-saturation|Benchmark Saturation]]
- [[entities/goodharts-law|Goodhart's Law]]
