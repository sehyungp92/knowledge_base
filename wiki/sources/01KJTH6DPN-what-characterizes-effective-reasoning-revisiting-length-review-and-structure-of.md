---
type: source
title: What Characterizes Effective Reasoning? Revisiting Length, Review, and Structure
  of CoT
source_id: 01KJTH6DPN4HFBVYMA8Y3FZ9A8
source_type: paper
authors:
- Yunzhen Feng
- Julia Kempe
- Cheng Zhang
- Parag Jain
- Anthony Hartshorn
published_at: '2025-09-23 00:00:00'
theme_ids:
- chain_of_thought
- interpretability
- model_behavior_analysis
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# What Characterizes Effective Reasoning? Revisiting Length, Review, and Structure of CoT

**Authors:** Yunzhen Feng, Julia Kempe, Cheng Zhang, Parag Jain, Anthony Hartshorn
**Published:** 2025-09-23 00:00:00
**Type:** paper

## Analysis

# What Characterizes Effective Reasoning? Revisiting Length, Review, and Structure of CoT
2025-09-23 · paper · Yunzhen Feng, Julia Kempe, Cheng Zhang, Parag Jain, Anthony Hartshorn
https://arxiv.org/pdf/2509.19284

---

### Motivation & Prior Limitations
The prevailing "longer-is-better" narrative for chain-of-thought reasoning lacks systematic empirical grounding, and conflicting findings across studies create real confusion about what drives reasoning performance at test time.
- The S1 paper (Muennighoff et al., 2025) and follow-up work showed that appending `wait` tokens to increase generation length and encourage review behaviors improves reasoning, leading to widespread assumptions that more test-time compute via length is generically beneficial.
  - However, subsequent studies (Wu et al., 2025b; Hassid et al., 2025; Ghosal et al., 2025; Marjanović et al., 2025) reported that shorter thoughts outperform longer ones, and that continued `wait` insertion induces oscillatory performance degradation.
- Existing evaluations are typically conducted on small model sets, leaving open whether different LRMs exhibit consistent behaviors, and no study had systematically separated the effects of length, review behavior, and underlying reasoning structure across a diverse model population.
- Token-level metrics such as total length and review ratio conflate verbosity with process quality, providing no insight into the structural properties — such as failed exploratory branches — that may drive accuracy.

---

### Proposed Approach
The paper introduces a reasoning-graph extraction method to move beyond token-level CoT metrics and identifies the Failed-Step Fraction (FSF) — the fraction of reasoning steps in abandoned branches — as the key structural predictor of correctness.
- Each CoT is converted into Graphviz format by prompting Claude 3.7 Sonnet (thinking disabled), which directly elicits graph structure rather than relying on multi-round scaffolding (as in Jiang et al., 2025) or sentence-level embeddings (Minegishi et al., 2025); the Claude-produced graphs compiled without error in 100% of cases.
- Review behaviors are measured using Llama 4 Maverick as an LLM judge to label each reasoning chunk as either `progress` (advances the active reasoning frontier) or `review` (reads, checks, restates, or rewinds without advancing), achieving 90% agreement with human labels; Review Ratio is then the character-fraction of review content per trace.
- The study evaluates ten LRMs — including Claude 3.7 Sonnet Thinking, Grok 3 mini, Deepseek R1, Qwen 3 variants (235B/32B/8B), and GPT oss variants (120B/20B) — generating 16 traces per question on HARP (300 subsampled math problems across 6 difficulty levels) and GPQA-Diamond (198 scientific reasoning problems), using conditional correlation analysis with question fixed effects to remove confounding from question-level difficulty.
- Causality is probed via two interventions: (1) test-time reranking of 64 candidate generations per problem by each metric on AIME 2025 and GPQA-Diamond, and (2) controlled CoT editing that removes identified failed branches from incorrect traces, followed by 8-continuation generations to measure accuracy change.

---

### Results & Capabilities
Contrary to the S1 narrative, shorter CoTs and lower review ratios are negatively correlated with accuracy, and FSF is the single strongest and most consistent predictor of correctness across all ten models on both math and scientific reasoning.
- Conditional correlation analysis (controlling for question-level confounders) shows that shorter CoT length correlates with higher accuracy across virtually all models on both HARP and GPQA-Diamond; Review Ratio is similarly negatively associated with accuracy for most models, with Claude 3.7 as a notable exception on math tasks.
- FSF achieves significant negative correlation with accuracy across every one of the ten models on both datasets, showing stronger and more consistent effects than either Length or Review Ratio; the correlation is especially pronounced for harder questions (HARP Levels 4–6), where the effect is most cleanly isolated because easy questions allow multiple viable solution paths.
- FSF-based test-time reranking of 64 candidates on AIME 2025 yields gains of roughly 5–13% over random selection across tested models, consistently outperforming Length- and Review Ratio-based selection; on GPQA-Diamond, FSF again produces significant gains for every model, with gains generally smaller (1–3%) reflecting the lower variance of the scientific reasoning task.
- Removing failed branches from incorrect HARP traces increases accuracy by 8–14% for both Deepseek R1 and GPT oss 120B: at the first failed branch, accuracy rises from ~21% to ~29% (Deepseek R1) and from ~28% to ~36% (GPT oss 120B); providing a concise summary of the removed branch instead of deletion also improves accuracy but less so, indicating that models do not fully "unsee" past failed attempts even after backtracking.
- The depth at which the first failed step occurs shows little to no correlation with correctness, implying it is the presence and extent of failed branching — not its position — that harms performance.

---

### Implications
These results shift the framing of test-time compute scaling from a quantity problem (generate more tokens) to a quality problem (manage failure propagation), suggesting that structure-aware selection and context management are more effective levers than indiscriminate length scaling.
- The causal experiments establish that failed branches actively bias subsequent reasoning rather than being passive markers of difficulty, which means any practical test-time strategy — whether beam search, best-of-N sampling, or speculative decoding — should account for how early failures corrupt later exploration.
- FSF can be estimated without access to ground-truth answers (Claude 3.7 extracts graphs from other models' CoTs and improves their accurac

## Key Claims

1. Naive CoT lengthening is associated with lower accuracy in large reasoning models.
2. Higher Review Ratio (fraction of review tokens in a CoT) is associated with lower accuracy across most large reasoning models.
3. Failed-Step Fraction (FSF) consistently outpredicts CoT length and Review Ratio as a predictor of correctness across models.
4. FSF is significantly negatively correlated with accuracy across all ten tested models on both math and scientific reasoning.
5. Removing failed reasoning branches from incorrect CoTs significantly improves accuracy on continuation generation.
6. Failed reasoning branches bias subsequent reasoning steps, meaning models do not fully 'unsee' earlier mistakes when backtracking.
7. FSF-based test-time selection from 64 candidate generations yields 5–13% accuracy gains over random selection on AIME 2025.
8. FSF-based reranking yields up to 12% accuracy improvement when the same model (Claude 3.7) both generates and estimates FSF.
9. FSF-based test-time selection produces significant accuracy gains for every model on GPQA-Diamond.
10. The correlation between CoT structural metrics and accuracy is stronger for harder questions.

## Capabilities

- Failed-Step Fraction (FSF)-based test-time selection — reranking among N candidate CoTs by fraction of steps in abandoned reasoning branches — yields 5–13% accuracy gains on AIME 2025 and consistent gains on GPQA-Diamond over random baseline, without access to ground-truth answers
- LLMs (Claude 3.7 Sonnet) can extract structured reasoning graphs from CoT traces in Graphviz format with 100% compilation success, enabling structural analysis of reasoning quality without multi-call scaffolding or embedding pipelines
- Targeted CoT editing — removing failed reasoning branches from incorrect traces — improves continuation accuracy by 8–14 percentage points on math reasoning tasks, providing a post-hoc intervention for boosting LRM performance

## Limitations

- LRMs do not fully 'unsee' earlier failed reasoning attempts after backtracking — the presence of failed branches biases subsequent exploration even when the model explicitly reviews and reverts, causing measurable accuracy degradation
- Naive CoT lengthening via 'wait' tokens and similar techniques is negatively correlated with accuracy at the per-question level — indiscriminate test-time compute scaling by extending generation length degrades rather than improves reasoning
- Higher review ratio (backtracking, verification, restating prior steps) is negatively correlated with accuracy for most LRMs — increased review behavior is a surface proxy for underlying reasoning difficulty, not a quality improvement mechanism
- Token-level reasoning metrics (length, review ratio) are unreliable proxies for CoT quality — they conflate verbosity with process quality and mask structural failure modes, making them poor guides for test-time scaling
- FSF estimation requires an auxiliary LLM call (Claude 3.7 Sonnet) to extract the reasoning graph — adding latency and compute cost per candidate, limiting practical deployment of FSF-based selection in low-latency or cost-sensitive settings
- FSF-accuracy correlations substantially weaken for easy questions — structural quality metrics provide no reliable signal on problems where models succeed along multiple trajectories, limiting utility to harder reasoning tasks
- How training shapes low-FSF reasoning behavior is unknown — the paper cannot explain whether low FSF is trainable, what training interventions would reduce failed branches, or how RLVR/SFT post-training affects structural CoT quality
- CoT faithfulness is assumed but not verified — findings rest on the assumption that CoT traces reflect actual model reasoning, but unfaithful CoTs would invalidate structural quality analysis
- FSF findings are restricted to math and scientific reasoning domains — generalisation to open-ended, creative, or agentic tasks is untested and likely requires different structural metrics
- LRMs currently have no mechanism to generate low-FSF CoTs directly — they can only be selected post-hoc from a candidate pool, requiring expensive multi-sample generation (64 samples in experiments) to realise FSF-based accuracy gains
- Model-specific review behavior creates cross-model inconsistency in FSF findings — Claude 3.7 Sonnet uniquely benefits from higher review ratio unlike all other tested models, suggesting structurally different CoT generation strategies across model families

## Bottlenecks

- LRMs cannot avoid generating failed reasoning branches during the forward pass — models produce exploratory failures that persistently bias subsequent reasoning, making quality control only possible post-hoc through candidate selection or editing
- No training methodology exists to induce low-FSF reasoning — the relationship between RLVR/SFT training dynamics and structural CoT quality (failed branch fraction) is entirely uncharacterised, blocking training-level interventions
- Structural CoT quality metrics like FSF require auxiliary LLM inference for graph extraction, creating a compute multiplier on top of the already expensive multi-sample test-time scaling pipeline

## Breakthroughs

- Failed-Step Fraction (FSF) established as a causally active structural predictor of CoT correctness — demonstrating that structural quality (fraction of failed reasoning branches) outpredicts surface metrics (length, review ratio) across all 10 tested LRMs, with causal confirmation via both selectio

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/interpretability|interpretability]]
- [[themes/model_behavior_analysis|model_behavior_analysis]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
