---
type: source
title: 'Climbing the Ladder of Reasoning: What LLMs Can-and Still Can''t-Solve after
  SFT?'
source_id: 01KJTZV5JKJ2RY94DF8SBNVQG7
source_type: paper
authors:
- Yiyou Sun
- Georgia Zhou
- Haoyue Bai
- Hao Wang
- Dacheng Li
- Nouha Dziri
- Dawn Song
published_at: '2025-04-16 00:00:00'
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- scaling_laws
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?

**Authors:** Yiyou Sun, Georgia Zhou, Haoyue Bai, Hao Wang, Dacheng Li, Nouha Dziri, Dawn Song
**Published:** 2025-04-16 00:00:00
**Type:** paper

## Analysis

# Climbing the Ladder of Reasoning: What LLMs Can-and Still Can't-Solve after SFT?
2025-04-16 · paper · Yiyou Sun, Georgia Zhou, Haoyue Bai, Hao Wang, Dacheng Li et al. (7 total)
https://arxiv.org/pdf/2504.11741

---

### Motivation & Prior Limitations
Recent small-scale SFT approaches (LIMO, s1) achieved impressive benchmark scores on mathematical reasoning, but the specific capabilities enhanced — and limitations that persist — were poorly understood, leaving an incomplete picture of what SFT actually buys.
- Small-scale SFT models like LIMO-32B and S1.1-32B can outperform o1-preview on MATH500 (89% vs 81.4%), yet aggregate scores mask which problem types remain fundamentally unsolvable and why.
  - Prior work (Muennighoff et al., 2025; Ye et al., 2025) suggested ~1K carefully curated samples are sufficient and better, but this claim was not validated against a difficulty-stratified benchmark.
- Standard benchmarks like MATH500 and GSM8K are saturated by strong chain-of-thought models, making them uninformative for probing the frontier of reasoning capability.
  - AIME2024 was chosen as the primary evaluation surface because it spans a genuine difficulty gradient from high-school-level to competition problems requiring unconventional insight, while avoiding confounds from graduate-level domain knowledge (unlike HLE).

---

### Proposed Approach
The paper conducts a systematic empirical analysis of how reasoning capabilities evolve through SFT by discovering and exploiting a ladder-like difficulty structure in AIME24 questions, categorizing all 30 problems into four tiers (Easy, Medium, Hard, Extremely Hard) based on averaged accuracy across six diverse models, then running controlled ablations to identify the minimal conditions for tier-to-tier advancement.
- Six models spanning three capability classes were evaluated — base model (Qwen2.5-32B-Instruct), small-scale SFT (S1.1-32B, LIMO-32B), and large-scale post-training or tool-augmented (R1, QwQ-32B, STILL3-32B) — each attempting every question 8 times to compute avg@8 and cov@8 metrics, enabling separation of potential from stability.
- SFT ablations independently varied four dimensions: math category (algebra, calculus, geometry, combinatorics, etc.), dataset size (50 to 20K trajectories), CoT trajectory length (short/normal/long), and trajectory style (DeepSeek-R1 vs. Gemini-flash), all using Qwen2.5-32B-Instruct as the fixed base model.
- For Exh-level questions, the authors used targeted probing — hints, subproblem decomposition, suggestive prompts — with R1 as the ceiling model, to identify qualitative failure modes rather than quantitative scaling trends.
- Trajectory similarity between SFT variants and DeepSeek-R1 was measured by summarizing full CoT traces with GPT-4o-mini and scoring similarity on a 0–5 scale, revealing whether different training data leads to genuinely different problem-solving strategies.

---

### Results & Capabilities
Progression from Easy to Medium tier requires only ~500–1K R1-style CoT trajectories in any math category, yielding a sharp improvement from ~10% to ~90% average accuracy on Medium problems, independent of whether the trajectories cover algebra, geometry, combinatorics, or other domains.
- The critical configuration is at least 500 long, randomly selected R1-style trajectories; short trajectories or Gemini-style trajectories fail to reach the ~90% passline, establishing that R1's extended chain-of-thought with self-reflection is the active ingredient, not subject-matter coverage.
- Despite being trained on diverse math categories, SFT models adopt nearly identical problem-solving strategies to each other and to DeepSeek-R1 on Medium-level problems: ~50% of trajectories rated "almost identical" and ~50% "mostly similar," suggesting SFT instills a generic reasoning style rather than domain-specific skill transfer.

Hard-level performance follows a logarithmic scaling law with dataset size, plateauing at approximately 65% avg@8 accuracy around 10K–20K trajectories, with models using RL (QwQ-32B) or external tools (STILL3) exceeding this ceiling.
- The root cause of Hard-level failure is compounding instability across multiple sequential hidden steps: overall accuracy approximates the product of per-step success rates, so a 5-step problem with 87.5% per-step accuracy yields ~52% end-to-end accuracy.
- Computational substeps (e.g., evaluating a Cayley-Menger determinant for a tetrahedron volume) are a distinct failure mode: LIMO-32B achieves 0% on this substep while QwQ-32B achieves 100%, and fixing this single substep fully determines overall problem accuracy (Table 1b).
- Careful curation of a 1K SFT dataset using semantic similarity to Hard-level test questions yields only a 5% gain over a randomly sampled dataset of the same size (33.6% vs. 28.4%), while simply doubling to 2K random trajectories yields a larger 7% gain, falsifying the hypothesis that curation quality substitutes for scale.

Exh-level questions achieve 0% accuracy across all SFT variants regardless of dataset size, with only QwQ-32B (3.1%) and STILL3 (25%) making any progress, and human expert performance remaining the unclosed gap.
- Small-scale SFT models show comparable coverage potential to R1 (cov@8×4 reaching 90 for geometry-trained models), indicating the 32B model has latent capacity for the same problems — the gap is instability, not missing knowledge.
- Performance across all math categories evaluated at 1K trajectories falls within a narrow band of 55±4% avg@8×4, with dissimilar and similar curated datasets differing by only ~6% (49.6% vs. 56.0%), reinforcing that category and curation choices have marginal effect relative to scale.

---

### Implications
The ladder structure implies that different capability tiers require qualitatively different interventions: Easy→Medium is a style-adoption problem solvable with minimal SFT, Medium→Hard is a stability and scale problem addressable with more data but subject to 

## Key Claims

1. Progression from Easy to Medium tier on AIME24 requires adopting an R1 reasoning style with minimal SFT of approximately 500-1K instances, regardless of the specific math category trained on.
2. Exh-level questions are not addressed by scaling SFT dataset size; all SFT models across all dataset sizes achieve 0% accuracy on Exh-level questions.
3. Small-scale SFT models have comparable coverage potential to DeepSeek-R1 (same number of solvable questions given multiple attempts), but significantly lower average accuracy due to instability.
4. Careful curation of small-scale SFT datasets yields only marginal performance gains (~1%) compared to randomly selected datasets of the same size, making scaling dataset size more effective than curat
5. SFT across all math categories produces models with performance within a narrow range of 55±4% on AIME24, showing that math category of training data has minimal impact.
6. Models fine-tuned via SFT on diverse math categories converge to similar problem-solving strategies, with approximately 50% of trajectories rated as 'almost identical' to DeepSeek-R1's strategies.
7. Using Gemini-style CoT trajectories instead of R1-style trajectories for SFT results in lower accuracy on Medium-level questions, failing to reach the ~90% passline.
8. Reinforcement learning and external computational tools (e.g., Python) allow models to surpass the ~65% Hard-level accuracy ceiling that SFT alone cannot exceed.
9. Hard-level question failures are primarily caused by multi-step reasoning instability, where success rates across sequential subquestions multiply, causing overall accuracy to decline with the number 
10. LLMs exhibit rigid, fixed problem-solving strategies (e.g., coordinate systems for geometry, inclusion-exclusion for combinatorics) that cause failure on Exh-level problems requiring unconventional ap

## Capabilities

- SFT on 500–1K R1-style trajectories enables 32B base models to reach ~90% accuracy on Medium-level AIME24 math problems — up from ~10% base model performance — with no dependence on specific math category
- Large-scale post-trained models (DeepSeek-R1, QwQ-32B) achieve avg@8 of 75–79% on full AIME24, with QwQ reaching 70.8% on Hard-level questions
- RL-trained and tool-augmented models (QwQ-32B, STILL3-32B) can surpass the ~65% Hard-level accuracy ceiling that SFT-only scaling cannot exceed regardless of dataset size

## Limitations

- SFT-trained models plateau at approximately 65% accuracy on Hard-level AIME24 questions regardless of dataset scale; logarithmic returns flatten beyond ~20K examples and additional data yields negligible gains
- All SFT-trained models achieve 0% on Extremely Hard (Exh) AIME24 problems; even DeepSeek-R1 achieves only 9.4% and the best model (STILL3, tool-augmented) achieves only 25%, indicating a fundamental and qualitatively distinct capability gap
- LLMs exhibit rigid, homogeneous problem-solving strategies: models trained on diverse math domains converge to nearly identical approaches regardless of training distribution (~50% 'almost identical', ~50% 'mostly similar' trajectories vs DeepSeek-R1)
- LLMs have a fundamental deficiency in geometric intuition due to 1D sequential architecture; spatial reasoning straightforward to humans (e.g., applying rotational symmetry to enumerate cases) cannot be reliably learned from text trajectories
- Models fail Exh-level problems requiring extensive hierarchical substep exploration even with 32K token context windows — they rush to conclude with incorrect answers after long chains rather than maintaining systematic case-by-case exploration
- Overall accuracy on Hard-level problems degrades multiplicatively across reasoning steps: LIMO achieves only 12.5% on a full problem despite 87–100% on the first three subquestions, because each step's error compounds through the chain
- Small-scale SFT models fail computationally intensive arithmetic subproblems (e.g., Cayley-Menger determinant), achieving 0% on critical subquestions that large-scale RL models solve at 100% — arithmetic computation, not strategy selection, is often the actual bottleneck
- Careful curation of SFT datasets (including with explicit knowledge of test questions) yields only ~1% performance improvement over randomly selected datasets of equal size; scaling dataset volume is consistently more effective than curation quality
- SFT models adopt fixed canonical strategies for problem types (coordinate systems for geometry, inclusion-exclusion for combinatorics) and systematically fail when unconventional or simpler approaches are required — strategy rigidity causes failures even when the model 'knows' the underlying math
- Small-scale SFT models demonstrate severe reliability instability: despite having coverage potential comparable to DeepSeek-R1 (cov@8 ~90%), their avg@8 accuracy is >20% lower due to inability to reproduce correct solutions consistently
- The specific mechanisms by which RL training surpasses SFT on Hard-level mathematical reasoning are unknown; precise training data volumes and algorithmic details for QwQ-32B are not publicly available, preventing reproducibility or mechanistic understanding

## Bottlenecks

- SFT-only training hits a hard accuracy ceiling (~65%) for Hard-level mathematical reasoning — logarithmic scaling makes further progress with more data increasingly inefficient, and RL or tool integration is required to surpass this fundamental limit
- No training recipe — SFT, RL, or tool augmentation — reliably enables solution of Exh-level mathematical problems requiring unconventional out-of-the-box insights; this represents a hard frontier even for the strongest current models
- LLM geometric and spatial intuition is architecturally bottlenecked by 1D sequential token processing — acquiring the spatial representations needed for rotational symmetry, visual enumeration, and shape reasoning requires representational capacity beyond autoregressive text models

## Breakthroughs

- Systematic empirical characterisation of a discrete 'reasoning ladder' in LLM mathematical capability, revealing qualitatively distinct tiers (Easy → Medium → Hard → Exh) with different mechanisms, requirements, and ceilings at each transition

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/finetuning_and_distillation|finetuning_and_distillation]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/scaling_laws|scaling_laws]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-32b|DeepSeek-R1-Distill-Qwen-32B]]
- [[entities/hle-humanitys-last-exam|HLE (Humanity's Last Exam)]]
- [[entities/math500|MATH500]]
- [[entities/qwq-32b|QwQ-32B]]
