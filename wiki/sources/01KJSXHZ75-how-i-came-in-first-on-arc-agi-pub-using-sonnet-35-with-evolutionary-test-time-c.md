---
type: source
title: How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time
  Compute
source_id: 01KJSXHZ75N7PG1RDV2K94ZYTM
source_type: article
authors: []
published_at: '2024-12-06 00:00:00'
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- interpretability
- model_behavior_analysis
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute

**Authors:** 
**Published:** 2024-12-06 00:00:00
**Type:** article

## Analysis

# How I came in first on ARC-AGI-Pub using Sonnet 3.5 with Evolutionary Test-time Compute
2024-12-06 · article
https://jeremyberman.substack.com/p/how-i-got-a-record-536-on-arc-agi

---

## Briefing

**By applying evolutionary algorithm principles to test-time compute — iteratively generating, evaluating, and refining Python transform functions across multiple generations — the author achieved 53.6% on ARC-AGI-Pub with Claude Sonnet 3.5, a 10+ percentage point jump over the prior record. The result is practically significant because it demonstrates that LLMs can partially compensate for their generalization deficit through structured search, but theoretically significant because it exposes the hard ceiling: LLMs reason inductively, not deductively, and the verifier problem may make test-time compute alone insufficient for AGI.**

### Key Takeaways
1. **Evolutionary test-time compute achieved 53.6% on ARC-AGI-Pub** — a 10+ point improvement over the prior record of 43% (Ryan Greenblatt), using Claude Sonnet 3.5 with up to 500 generated functions and 31 dynamic prompts per challenge.
2. **Generating executable Python functions, not output grids, is the key architectural choice** — functions can be run against example pairs to score fitness; raw grids cannot be verified without ground truth.
3. **Depth beats breadth: 4-generation deep search outperforms single-generation shallow search** — on 60 training challenges at equal LLM call budgets (200 calls each), deep achieved 75% vs. shallow's 70%, with 42% of deep's solutions coming only in generations 2–4.
4. **The "pooling" prompt combines multiple parent functions to address local maxima** — when different functions each solve different example cases but none solves all, pooled prompts provide more diverse genetic material; but pooling has cost-accuracy tradeoffs and isn't always superior.
5. **LLMs use induction, not deduction — CoT prompting is mimicry, not reasoning** — LLMs produce "convincing impressions of deduction" because correct-sounding tokens are more likely to be logically correct, but the process is inherently probabilistic and systemically riddled with hallucinations.
6. **The verifier problem is the fundamental obstacle to test-time compute AGI** — ARC is tractable because candidate solutions can be checked against examples; for open-ended tasks, a trustworthy verifier would itself need to be capable of deduction, potentially requiring AGI to verify AGI.
7. **Model diversity would likely improve performance further** — different frontier models (o1, GPT-4o, Gemini 1.5 Pro) each solve different challenges more efficiently; diverse "brains" expand solution space coverage.
8. **Chain-of-thought prompt wording matters little; the example in the prompt matters a lot** — for frontier models, surface variation in CoT instructions produces negligible accuracy differences, but the choice of in-context example (especially whether it matches the transformation type) has measurable impact.
9. **Fine-tuning on ~10,000 correct CoT solutions may be sufficient to solve ARC** — if all core knowledge needed is present in the training/eval sets, a fine-tuned model could internalize the reasoning patterns without needing in-context examples at all.
10. **JEPA-style concept-space optimization may be required for genuine deductive capability** — training LLMs to predict in feature space rather than token space could align the optimization objective with concept manipulation, which is what deduction actually requires.
11. **ARC-AGI is significant precisely because it isolates generalization from memorization** — 400 of the 500 challenges are not publicly available, making retrieval-based approaches ineffective and directly measuring novel rule induction.
12. **The generation depth hyperparameter is analogous to learning rate** — too few generations per challenge yields insufficient refinement; too many with too few attempts per generation causes overfitting to parent solutions and narrow search.

---

### What ARC-AGI Measures and Why It Matters

- ARC-AGI is designed as an intelligence test for abstract pattern recognition, structurally similar to an IQ test, presenting novel input/output grid transformations the solver has never seen.
  - The benchmark is notable for its stark human-AI gap: humans achieve ~85% accuracy on 400 challenges; the best LLMs achieved only ~18% before this work.
  - **The gap is not about task difficulty but about generalization** — the puzzles are simple enough that humans solve them intuitively, yet hard enough that billion-parameter models trained on internet-scale data fail systematically.
- ARC-AGI-Pub is the internet-accessible leaderboard variant, allowing use of any public LLM API under constraints: 12 hours of compute on a Kaggle notebook and $10,000 for API costs to complete 500 challenges.
  - 400 of the 500 challenges do not exist on the internet, making retrieval or memorization-based approaches ineffective.
  - Public leaderboard submissions are not eligible for prize money; only private (offline) submissions are.
- The author frames ARC as the most important benchmark currently available because it directly tests the capability LLMs most fundamentally lack: reasoning about things they were not trained on.

---

### The Evolutionary Test-Time Compute Architecture

- The core idea: treat the LLM as an evolution engine that generates Python transform functions, scores them against provided example pairs, selects the fittest, and breeds the next generation via revision prompts.
  - **Python functions are the unit of evolution, not output grids** — because functions are executable, they can be scored automatically by running them on example inputs and comparing outputs; grids have no equivalent verification mechanism.
  - Fitness scoring is two-tiered: primary score is the number of complete example grids solved perfectly; secondary score counts correct individual cells in imperfect solutions.
- The evolutiona

## Key Claims

1. The author achieved 53.6% accuracy on ARC-AGI-Pub using Claude Sonnet 3.5, setting a new public record.
2. The previous state-of-the-art on ARC-AGI-Pub was 43%, achieved by Ryan Greenblatt.
3. Humans achieve approximately 85% accuracy on ARC challenges, while the best LLMs achieve only 18%.
4. The Evolutionary Test-time Compute method generates up to 500 Python transform functions using 31 dynamic prompts per ARC challenge.
5. The method generates Python functions rather than output grids directly because functions can be executed and verified for correctness whereas grids cannot.
6. A deep 4-generation architecture achieves higher accuracy than a shallow single-generation approach with the same total number of LLM calls.
7. 42% of the Deep architecture's solutions came from generations 2–4, demonstrating the value of iterative refinement over single-generation generation.
8. Fitness evaluation for ARC transform functions uses a two-tier scoring: primary score is the number of fully correct example grids, secondary score is the number of correct individual cells for non-pe
9. The evolutionary approach can get stuck at local maxima when top-performing parents all share the same partial solution pattern, missing diverse solutions from other lineages.
10. Pooling multiple parent functions into a single revision prompt helps address the local maxima problem by ensuring at least one solution for each example case is represented.

## Capabilities

- Evolutionary test-time compute using LLM-generated Python transform functions achieves 53.6% on ARC-AGI-Pub public leaderboard — improving over previous 43% SOTA by combining multi-generation evolutionary refinement with execution-based fitness evaluation
- LLM-generated executable Python functions as intermediate representation enables verifiable fitness scoring during test-time evolutionary search — functions can be run against ARC example pairs to produce objective correctness scores, enabling Darwinian selection
- Multi-generation evolutionary refinement of LLM-generated solutions yields measurable improvement over single-generation search — 75% vs 70% accuracy (45/60 vs 42/60 training challenges) with 42% of Deep solutions emerging only in generations 2–4
- Pooled multi-parent evolutionary prompting addresses local-maxima problem by combining functions that each solve different example cases into a single revision prompt, ensuring diverse genetic material from the full solution frontier

## Limitations

- LLMs are fundamentally incapable of deductive reasoning — they use induction (pattern extrapolation from training) rather than logical necessity, producing systemic hallucinations and false statements in reasoning chains, not merely occasional errors
- Test-time compute evolutionary search cannot generalize beyond tasks with easily verifiable ground truth — for open-ended reasoning (argument validity, logical soundness), there is no fitness function, so the evolutionary selection mechanism collapses
- Humans achieve 85% on ARC-AGI while the best unaided LLMs achieve only 18% — a ~4.7x gap — demonstrating a fundamental generalization deficit on novel abstract pattern recognition tasks
- Evolutionary test-time compute is prohibitively expensive at scale — the ARC-AGI-Pub challenge consumed up to $10,000 in API costs for 500 challenges (~$20 per challenge), generating up to 500 functions each, making this approach inaccessible without large API budgets
- LLM attention degrades with longer contexts — pooled multi-parent prompts that combine several function solutions are less efficiently processed than shorter single-parent prompts, limiting the diversity benefits of pooling
- Evolutionary search is susceptible to local maxima — when multiple examples must all be solved, selection pressure systematically discards functions that solve rare sub-problems in favor of functions solving common ones, permanently losing exploration of those solution regions
- Token-prediction training objective misaligns LLM optimization with concept-level reasoning — any conceptual understanding models develop is incidental to the surface-level token accuracy objective, preventing direct optimization for deductive capability
- One-shot prompting consistently outperforms two- and three-shot prompting for ARC reasoning tasks — LLMs lose focus with additional examples rather than benefiting from broader context, indicating that attention concentration matters more than example diversity in few-shot ICL
- Evolutionary architecture depth must be carefully calibrated — too few generations (too shallow) misses refinement opportunities, while too many generations (too deep) causes overfitting to parent solutions and collapse of solution diversity
- Chain-of-thought prompt wording has negligible impact on LLM reasoning quality — changing reasoning instructions, step structures, or tag formats does not meaningfully alter accuracy, suggesting CoT elicits a fixed capability rather than teaching new reasoning
- Limited experimental budget severely constrained architecture optimization — the 4-generation limit and specific branching factors were chosen for cost reasons rather than optimality, leaving the evolutionary architecture potentially far from its performance ceiling

## Bottlenecks

- Absence of verifiable fitness functions for open-ended tasks blocks test-time compute and evolutionary approaches from scaling beyond structured domains — for general language and reasoning tasks, output correctness cannot be evaluated without human judgement or an equivalently capable AI verifier
- Inductive-only LLM architecture blocks development of genuine deductive reasoning — without a fundamentally different training objective or architecture that optimizes at the concept level rather than token level, models cannot develop the logical necessity required for robust generalization

## Breakthroughs

- Evolutionary test-time compute with executable Python code generation achieves 53.6% on ARC-AGI-Pub — a 10.6 percentage point (25% relative) improvement over the prior 43% SOTA — by combining multi-generation LLM evolution, execution-based fitness evaluation, and pooled multi-parent diversity

## Themes

- [[themes/benchmark_design|benchmark_design]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/interpretability|interpretability]]
- [[themes/model_behavior_analysis|model_behavior_analysis]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/evolutionary-test-time-compute|Evolutionary Test-Time Compute]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
