---
type: source
title: 'TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them'
source_id: 01KJTGJW0TDBGPXG88VM32C8PP
source_type: paper
authors:
- Yidong Wang
- Yunze Song
- Tingyuan Zhu
- Xuanwang Zhang
- Zhuohao Yu
- Hao Chen
- Chiyu Song
- Qiufeng Wang
- Cunxiang Wang
- Zhen Wu
- Xinyu Dai
- Yue Zhang
- Wei Ye
- Shikun Zhang
published_at: '2025-09-25 00:00:00'
theme_ids:
- alignment_and_safety
- benchmark_design
- evaluation_and_benchmarks
- hallucination_and_reliability
- reinforcement_learning
- reward_modeling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them

**Authors:** Yidong Wang, Yunze Song, Tingyuan Zhu, Xuanwang Zhang, Zhuohao Yu, Hao Chen, Chiyu Song, Qiufeng Wang, Cunxiang Wang, Zhen Wu, Xinyu Dai, Yue Zhang, Wei Ye, Shikun Zhang
**Published:** 2025-09-25 00:00:00
**Type:** paper

## Analysis

# TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them
2025-09-25 · paper · Yidong Wang, Yunze Song, Tingyuan Zhu, Xuanwang Zhang, Zhuohao Yu et al. (14 total)
https://arxiv.org/pdf/2509.21117

---

### Motivation & Prior Limitations
LLM-as-a-judge frameworks, while scalable alternatives to human evaluation, contain two fundamental and previously unaddressed inconsistencies that undermine their reliability as evaluation tools.
- The first inconsistency, Score-Comparison Inconsistency, occurs when a response with a lower absolute score nonetheless "wins" in direct pairwise comparison against a higher-scored response — a direct violation of the assumption that scores and pairwise preferences are interchangeable.
  - Measured as a Conflict Ratio (CR), this occurs in 23.32% of pairs with Llama-3.1-70B under a standard 5-point scoring protocol, meaning nearly one in four score-to-pairwise comparisons is self-contradictory.
  - The root cause is information loss in coarse discrete rating systems: a 5-point scale compresses distinct response quality distributions into identical integer scores, destroying the entropy that differentiates them.
- The second inconsistency, Pairwise Transitivity Inconsistency, arises when pairwise judgments form irrational preference cycles (A > B > C > A) or equivalence contradictions (A = B = C ≠ A), violating basic rational preference axioms.
  - Non-Transitivity Ratio (NTR at k=5) reaches 15.22% with Llama-3.1-70B baseline and as high as 54.69% with Llama-3.2-3B, making pairwise rankings unreliable for ranking multiple models simultaneously.
  - Analysis shows the majority of transitivity violations (84.6% for Llama-3.1-8B) originate from inequality inconsistency — contradictions arising from ambiguous tie judgments — rather than circular cycles.
- Prior work addressing pairwise inconsistencies relied on continual training or complex mathematical modeling, which risks compromising model generalizability and does not resolve the score-comparison conflict. No prior work had systematically exposed both inconsistency types as a unified structural weakness.

---

### Proposed Approach
TrustJudge is a training-free probabilistic evaluation framework that addresses both inconsistencies by preserving judgment entropy rather than discarding it through discretization.
- For Score-Comparison Inconsistency, TrustJudge employs distribution-sensitive scoring: the judge LLM is prompted to score on a finer-grained scale (e.g., 100-point instead of 5-point), its output logits over all candidate scores are passed through a softmax to yield a valid probability distribution, and the final score is computed as the expected value scaled back to the original range.
  - This differs from G-Eval's probability summation approach, which sums probabilities without softmax normalization and can violate the constraint that probabilities sum to 1 because non-score tokens also influence the output; TrustJudge ensures a properly normalized distribution.
  - Theorem 3.1 formalizes the guarantee: discrete scoring can assign identical scores to responses with distinct underlying distributions and different conditional entropies, while distribution-sensitive scoring provably distinguishes them.
- For Pairwise Transitivity Inconsistency, TrustJudge offers two likelihood-aware aggregation strategies to resolve ambiguous tie judgments without retraining.
  - Option A (PPL-based): given two responses Rx and Ry, the framework computes the perplexity of both presentation orderings under the judge model and selects the ordering with lower perplexity as the decisive signal; Proposition 3.2 proves this produces a lower-entropy decision signal than the near-uniform distribution typical of ambiguous cases.
  - Option B (likelihood-aware aggregation): for each possible outcome k ∈ {win, lose, tie}, the framework aggregates preference probabilities from both orderings (m[k] = p_order1[k] + p_order2[−k]) and selects the outcome with maximum aggregated probability, simultaneously reducing position bias.
- A tolerance hyperparameter δ ≥ 0 allows users to tune tie sensitivity — declaring a pair tied when the score difference, PPL gap, or probability margin falls within δ — without any retraining.

---

### Results & Capabilities
TrustJudge achieves substantial, simultaneous reductions in both inconsistency types while maintaining or improving evaluation accuracy, across diverse model families and scales without additional training.
- Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Score-Comparison inconsistency (CR) from 23.32% to 14.89% (an 8.43 percentage point absolute reduction) and Pairwise Transitivity inconsistency (NTR k=5) from 15.22% to 4.40% (a 10.82 percentage point absolute reduction).
  - For smaller models, gains are more dramatic: Llama-3.2-3B NTR k=5 drops from 54.69% to 17.76% — a 36.93 percentage point reduction.
- Evaluation accuracy improves alongside consistency: exact match rates increase by 1.19%–6.85% across model sizes compared to baseline, with the largest gains for smaller models (6.85% for Llama-3.2-3B).
  - Win rates against baseline and G-Eval approaches range from 45.41% to 65.11%, with the 100-point scoring variant outperforming the 5-point variant uniformly.
- Ablation results confirm that likelihood-aware aggregation is the stronger pairwise strategy, reducing NTR k=4 to as low as 1.94% for Llama-3.1-70B and 2.83% for GPT-4o; PPL-based aggregation offers a simpler implementation with substantial but slightly lower gains.
- Generalization experiments across 12 model variants spanning Qwen2.5 (7B–32B), Gemma-2 (2B–27B), Llama-3, and GPT families confirm architecture-agnostic improvement; notably, model size does not monotonically predict inconsistency — Gemma-2-9B shows lower inconsistency than Gemma-2-27B under baseline conditions.
- TrustJudge's 100-point softmax scoring also improves downstream preference optimization: DPO training on preferences sele

## Key Claims

1. LLM-as-a-judge frameworks suffer from Score-Comparison Inconsistency, where lower-rated responses outperform higher-scored ones in pairwise comparisons.
2. LLM-as-a-judge frameworks suffer from Pairwise Transitivity Inconsistency, manifested as circular preference chains (A > B > C > A) and equivalence contradictions (A = B = C ≠ A).
3. Score-comparison inconsistency primarily stems from information loss in discrete integer scoring systems, where coarse-grained scales compress nuanced quality differences into identical scores.
4. Most pairwise transitivity inconsistencies originate from ambiguous tie judgments (equivalence contradictions) rather than from circular inconsistencies.
5. Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Score-Comparison Inconsistency by 8.43% (from 23.32% to 14.89%).
6. Using Llama-3.1-70B-Instruct as judge, TrustJudge reduces Pairwise Transitivity Inconsistency by 10.82% (from 15.22% to 4.40%).
7. TrustJudge improves pairwise exact match rates by 1.19%–6.85% across different model sizes, with the largest gains for smaller models.
8. TrustJudge achieves these improvements without requiring additional model training or human annotations.
9. Llama-3.2-3B shows the most substantial improvement under TrustJudge, with NTRk=5 decreasing from 54.69% to 17.76%.
10. Increasing scoring granularity from 5 to 100 points consistently reduces Score-Comparison Conflict Ratios across all tested judge models.

## Capabilities

- LLM-as-a-judge frameworks provide scalable automated evaluation as a practical alternative to costly human assessment, achieving broad adoption across research and production contexts for both single-score and pairwise comparison protocols
- Distribution-sensitive probabilistic scoring for LLM judges: computing continuous expected scores from discrete rating probability distributions via softmax normalisation over expanded score sets, preserving full judgment entropy and reducing Score-Comparison inconsistency by 8.43%
- Likelihood-aware aggregation using bidirectional preference probabilities or perplexity-based tie-breaking to resolve pairwise transitivity violations in LLM-as-a-judge, achieving NTR reduction from 15.22% to 4.40% without requiring additional training or human annotations
- Using TrustJudge's probabilistic 100-point scoring as a reward signal for DPO preference optimisation, improving LC win rate by up to 16.21% over standard 5-point scoring baselines

## Limitations

- Discrete integer scoring systems in LLM-as-a-judge cause provable structural information loss: coarse-grained 5-point scales collapse genuinely different response quality distributions to the same integer score, producing 23.32% Score-Comparison inconsistency even in strong 70B models
- Pairwise LLM judge evaluations exhibit systematic non-transitive preference cycles and equivalence contradictions at a 15.22% base rate, violating foundational rational preference axioms required for consistent ranking
- Residual inconsistency persists after TrustJudge correction — 14.89% Score-Comparison and 4.40% Pairwise Transitivity violations remain — indicating an irreducible floor of judgment noise that output-aggregation methods cannot fully eliminate
- RL specialisation training on mathematical reasoning causes catastrophic forgetting of judging capability: DeepSeek-R1-Distill-Llama-8B exhibits 58.75% Score-Comparison inconsistency versus 29.73% for base Llama-3.1-8B — nearly double the inconsistency rate
- Small-scale LLM judges (3B parameters) are severely unreliable for automated evaluation: 36.65% Score-Comparison inconsistency and 54.69% Pairwise Transitivity inconsistency at baseline — majority of pairwise orderings are non-transitive
- G-Eval-style probability summation generates invalid non-normalised probability distributions because non-score tokens influence output logits — violating the probability axiom and producing biased scoring
- Ambiguous tie judgments are the primary structural driver of pairwise transitivity violations — the binary tie/no-tie decision in contexts of genuine quality ambiguity creates unstable equivalence classes that cannot satisfy transitivity
- Model scale is not a reliable predictor of judge consistency quality: 9B Gemma exhibits lower inconsistency than 27B Gemma, indicating architectural and training factors dominate scale effects for evaluation tasks
- Evaluation generalisation beyond general instruction-following benchmarks is undemonstrated — MT-Bench and ArenaHard cover writing, roleplay, and reasoning but not specialised domains such as code correctness, theorem proving, or safety assessment

## Bottlenecks

- Fundamental structural inconsistencies in LLM-as-a-judge frameworks — ~23% Score-Comparison and ~15% Pairwise Transitivity violations at baseline — undermine the reliability of automated evaluation as a replacement for human assessment, limiting its use in high-stakes research decisions and RLHF pip
- Coarse-grained discrete scoring causes irreversible information loss in LLM evaluation — multiple distinct response quality distributions collapse to the same integer score, preventing fine-grained quality discrimination needed for accurate ranking and reward modelling
- RL specialisation training catastrophically degrades LLM evaluation capability — reasoning-optimised models cannot serve dual roles as strong reasoners and reliable evaluators, creating a fundamental capability trade-off in model design

## Breakthroughs

- TrustJudge: first systematic formalisation and unified resolution of dual structural inconsistencies in LLM-as-a-judge frameworks — providing theoretical proofs of information loss in discrete scoring and a practical probabilistic correction that works at inference time across all model families wit

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]

## Key Concepts

- [[entities/arenahard|ArenaHard]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/mt-bench|MT-Bench]]
- [[entities/position-bias|Position Bias]]
