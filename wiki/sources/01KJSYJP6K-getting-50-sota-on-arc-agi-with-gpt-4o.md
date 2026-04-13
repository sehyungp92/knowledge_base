---
type: source
title: Getting 50% (SoTA) on ARC-AGI with GPT-4o
source_id: 01KJSYJP6K4TS7AZZPP5NJ28W6
source_type: article
authors: []
published_at: '2024-06-17 00:00:00'
theme_ids:
- benchmark_design
- code_and_software_ai
- code_generation
- evaluation_and_benchmarks
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Getting 50% (SoTA) on ARC-AGI with GPT-4o

**Authors:** 
**Published:** 2024-06-17 00:00:00
**Type:** article

## Analysis

# Getting 50% (SoTA) on ARC-AGI with GPT-4o
2024-06-17 · article
https://redwoodresearch.substack.com/p/getting-50-sota-on-arc-agi-with-gpt

---

## Briefing

**By generating ~8,000 Python program candidates per ARC-AGI problem and selecting among them by correctness on training examples, GPT-4o achieves 50% on the public test set — a 16-point improvement over prior SoTA — demonstrating that test-time compute scaling via program synthesis is a powerful inference strategy for visual reasoning benchmarks. The result directly challenges Chollet's claim that LLMs cannot do in-context learning, while also revealing that ARC-AGI may be more vulnerable to brute-force elicitation than its designers intended.**

### Key Takeaways
1. **Test-time sampling scales as a clean log-linear law** — Each doubling of samples from the best prompt yields ~3% additional accuracy, meaning 50% requires ~8,000 samples and reaching 70% would require ~2 million.
2. **Better prompting multiplies the value of samples by orders of magnitude** — Reaching 50% with the weakest prompt (V0) alone would require 1.5 million samples; better representations and prompts achieve the same result with ~8,000.
3. **A one-step revision step contributes ~13% absolute accuracy** — Showing GPT-4o the diff between its program's actual output and the expected output, then asking for a revision, fixes ~20% of remaining wrong answers and is far more efficient than equivalent sampling.
4. **Program selection is itself a form of learning** — Best-of-N over LLM-generated programs only works because the distribution of generated programs is already highly concentrated near the correct solution; random Python programs would fail completely.
5. **GPT-4o's vision is a severe bottleneck, not its reasoning** — The model totally fails to extract colors from grids larger than 12×12; removing this limitation alone would substantially close the gap to human performance.
6. **Custom ASCII representations substitute for broken vision** — Providing connected-component lists, spreadsheet-style coordinate notation, normalized shape views, and input-output color diffs compensates for the model's inability to reliably read raw grid images.
7. **ARC-AGI train and test sets are not IID** — The test set is qualitatively harder and somewhat different in character, making iteration on train set performance a poor proxy for test set gains.
8. **Chollet's "LLMs can't learn at runtime" claim is falsified by this result** — One of three propositions must be rejected; the author argues the most defensible conclusion is that LLMs do perform some genuine in-context learning, just far less competently than humans.
9. **ARC-AGI is not a good TAI benchmark** — Strong vision is not necessary for transformative AI, and vision improvements have outsized effects on ARC-AGI scores; purely text-based problem variants would be a better proxy.
10. **Prior SoTA used 1000x less compute** — The comparison is not apples-to-apples; the scaling potential of prior approaches under similar compute budgets is unknown.
11. **The revision step creates a multiplicative interaction with sampling** — Revision's ~20% fix rate applies to the residual after sampling, so its absolute contribution is larger at lower base accuracy and smaller at higher base accuracy.
12. **Benchmark contamination is unlikely but unverifiable** — The author considers dataset contamination an implausible explanation for GPT-4o's performance, but acknowledges it as a formal caveat.

---

### The Core Method: Program Synthesis via Massive Sampling

- The fundamental approach is to treat ARC-AGI as a program synthesis task: prompt GPT-4o to write a Python function implementing the grid transformation, generate ~8,000 such functions per problem, and select among those that pass all training examples.
  - This mirrors AlphaCode's strategy of generating millions of completions and aggregating over them, applied to a visual reasoning benchmark rather than competitive programming.
  - The selection criterion is purely correctness on the provided input-output examples (typically 3 per problem); no learned scoring model is used.
  - Final submission is the top-3 outputs by majority vote over programs that pass the examples, falling back to Hamming-distance-weighted voting when fewer than 3 distinct correct outputs exist.

- **The approach required approximately 6 days of engineering effort** beyond the core sampling idea, including constructing few-shot prompts, building better text representations, iterating on the training set, and implementing revision.

- The method is ineligible for the official ARC-AGI prize and main leaderboard due to use of a closed-source model and excessive runtime compute.

---

### Test-Time Compute Scaling Laws

- **Performance scales log-linearly with sample count**, yielding approximately 3% additional accuracy per doubling of samples when using the best prompt variant (V2).
  - This is a clean empirical scaling law over the range tested, though the linear-in-log fit cannot hold indefinitely as it would eventually predict >100% accuracy.
  - The author notes that a log(1 - accuracy) fit would have better asymptotic properties but fits slightly worse in the relevant regime.

- The compute budget used here is extreme but not at the frontier: AlphaCode uses up to 1 million samples per problem; the author uses ~8,000.
  - **Reaching 70% (estimated typical MTurk human test-set performance) would require ~2 million samples with the current method.**
  - Reaching 70% using only V0 (the weakest prompt) would require ~32,000 samples on the train set.

- **Early termination on reliably-solved problems could reduce cost by 25–35%** without changing accuracy, but was not implemented.

- The `n` parameter in the OpenAI API makes large-scale sampling cheaper by batching completions; the author uses n ≤ 128 (typically 16–32) due to API stability issues at n=128.

---

### The Revision Step: One-Round Debugging as

## Key Claims

1. GPT-4o achieves 50% accuracy on the ARC-AGI public test set by generating approximately 8,000 Python programs per problem and selecting based on correctness on training examples.
2. The prior state of the art on ARC-AGI (or a similarly difficult dataset) was 34% accuracy before this work.
3. On a held-out subset of the ARC-AGI train set where humans achieve 85% accuracy, the GPT-4o-based solution achieves 72% accuracy.
4. Test-time compute scaling on ARC-AGI follows an approximately linear relationship between accuracy and log base 2 of the number of samples, yielding approximately 3% improvement per doubling of sample
5. Without the revision step, reaching 50% accuracy on ARC-AGI would require approximately 100,000 samples from the best prompt variant (V2), compared to ~8,000 with revision.
6. The code revision step fixes approximately 20% of remaining incorrect solutions, contributing an absolute improvement of ~13% on the test set (from 37% to 50%).
7. Using the V0 prompt alone without revision would require approximately 43,000 samples to reach 37% accuracy, whereas V2 achieves this with 4,096 samples.
8. Reaching 70% accuracy on the ARC-AGI test set using the current method would require approximately 2^21 (around 2 million) samples.
9. GPT-4o's vision system fails to correctly extract cell colors from grids larger than 12x12 pixels, representing a major non-reasoning bottleneck for ARC-AGI performance.
10. GPT-4o's long-context performance degrades significantly after approximately 32k–40k tokens, limiting the use of longer few-shot prompts.

## Capabilities

- Parallel test-time sampling on ARC-AGI follows a clean log-linear scaling law: approximately 3% additional accuracy per doubling of sample count, confirmed across multiple prompt variants
- Iterative revision step — showing GPT-4o its program's actual output versus expected output and asking for a fix — repairs approximately 20% of remaining incorrect solutions, equivalent to roughly 13 percentage points of ARC-AGI test accuracy gain
- Feature engineering via multi-modal ASCII grid representations (connected components, spreadsheet notation, normalised shapes, input-output diffs) reduces the number of samples needed to reach a given accuracy threshold by approximately 15–250× compared to naive image-only prompting
- GPT-4o can generate syntactically plausible Python programs implementing spatial transformation rules from visual examples, enabling a non-trivial search distribution for program synthesis on novel abstract reasoning tasks

## Limitations

- GPT-4o vision completely fails to extract grid cell colours for images larger than approximately 12×12 pixels and is unreliable at 8×8 — a hard performance cliff that makes spatial/grid reasoning dependent on text representations as a workaround
- GPT-4o long-context quality degrades substantially after approximately 32k–40k tokens, preventing the use of richer few-shot prompts with more examples or more detailed representations
- GPT-4o instruction following breaks down in long-context settings — the model ignores explicit formatting instructions and produces shorter completions than specified, even with repeated instructions
- GPT-4o makes frequent elementary coding errors (off-by-one, boundary conditions) on geometric manipulation tasks, requiring thousands of samples to obtain even a handful of correct implementations
- Reaching 70% accuracy on ARC-AGI test via the best current sampling-based approach requires approximately 2 million samples — an exponential compute wall that makes human-level performance economically infeasible at scale under this paradigm
- Absence of flexible prefix caching in the OpenAI API forces all parallel sampling to share a static prefix, preventing efficient exploration of branching multi-round reasoning traces and substantially raising the cost of iterative revision strategies
- LLM in-context learning on novel abstract reasoning tasks is substantially weaker than human learning — while some useful adaptation occurs, the system still requires thousands of attempts to solve problems that take humans minutes
- ARC-AGI train and test sets are not IID — the test set is substantially harder and qualitatively different — making iterative prompt optimisation on training data a poor proxy for test performance and obscuring true generalisation signal
- ARC-AGI top-3 accuracy metric and broad within-set difficulty distribution mean aggregate performance numbers mask the gap between easy (near-solved) and hard (intractable) subsets, making headline numbers misleading for capability assessment
- The approach as described is ineligible for the ARC-AGI prize and primary leaderboard due to closed-source model use and runtime compute exceeding contest limits, leaving it unverifiable against the hidden private test set

## Bottlenecks

- LLM vision quality for fine-grained spatial/symbolic reasoning is a first-order bottleneck: GPT-4o cannot reliably perceive grid contents in images, forcing costly text-representation workarounds and blocking native visual reasoning on spatial tasks
- Absence of production-grade dynamic prefix caching in frontier model APIs blocks efficient multi-branch reasoning exploration, confining high-compute test-time strategies to flat parallel sampling rather than structured tree search or multi-round iterative debugging
- The log-linear scaling of parallel sampling creates an exponential cost wall approaching human performance: each percentage point of accuracy gain on ARC-AGI test requires approximately doubling total compute, making the last 15–35 percentage points to human level economically untenable under this p

## Breakthroughs

- GPT-4o achieves 50% accuracy on ARC-AGI public test set — surpassing prior SOTA of 34% — using generate-test-revise program synthesis with massive parallel sampling, demonstrating that LLMs perform genuine (if weak) test-time learning on novel abstract reasoning problems

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
