---
type: source
title: 'Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification'
source_id: 01KJV3X90H49CTVN35T1QDQR8V
source_type: paper
authors:
- Eric Zhao
- Pranjal Awasthi
- Sreenivas Gollapudi
published_at: '2025-02-03 00:00:00'
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
# Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification

> A systematic study of sampling-based search as a test-time compute strategy, demonstrating that a minimalist pipeline of random sampling plus self-verification (Verification@k) outperforms o1-Preview on mathematical reasoning benchmarks — while characterizing the scaling laws, failure modes, and algorithmic principles that govern when and why it works.

**Authors:** Eric Zhao, Pranjal Awasthi, Sreenivas Gollapudi
**Published:** 2025-02-03
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

Self-consistency (majority voting) saturates quickly as a [[themes/test_time_compute_scaling|test-time compute]] strategy: it converges on the most probable response rather than the correct one, and cannot recover rare but valid solutions in the long tail of response distributions. On AIME, Consistency@50 achieves the same accuracy as Consistency@10,000 — hard saturation that no amount of additional sampling can overcome.

The verification capability of frontier models is also alarmingly weak out-of-the-box. GPT-4o and Claude 3.5 Sonnet identify wrong responses as wrong only ~31% and ~22.5% of the time respectively — barely above random chance (20%). Models systematically struggle to localize hallucinations without being told where to look.

A further structural problem: post-training techniques such as RLHF explicitly optimize for Pass@1, which may degrade Pass@k and thereby suppress the diversity that inference-time search depends on. The authors argue Pass@k, not Pass@1, should be the key performance metric for search applications — and that current training objectives work against this.

---

### The Verification@k Algorithm

The paper proposes a minimalist sampling-based search algorithm. Given a query, it:

1. Generates $k_\text{inf}$ candidate responses via parallel sampling at temperature 1.5
2. Scores each candidate with $k_\text{verif} = 50$ self-verification attempts, rewriting each response into a **theorem-lemma-proof** structure before scanning for errors
3. Resolves ties via round-robin pairwise comparison tournaments ($k_\text{tie} = 100$ matchups) when top candidates score within 5% of each other

The entire pipeline operates via blackbox natural-language queries to the same language model — no custom-trained [[themes/reward_modeling|reward models]], no symbolic verifiers, no access to ground-truth answers.

Two key verification principles underpin the design:

- **Comparative verification.** Providing the verifier with other candidate responses lets it localize disagreements and thus errors. Ablations confirm that removing tie-breaking comparisons accounts for most of Verification@200's gains over Consistency@200 on MATH and LiveBench Math.
- **Output-style rewriting.** [[themes/chain_of_thought|Chain-of-thought]] format is effective for *generating* responses but structurally harder to verify than formal mathematical prose. Rewriting into theorem-lemma-proof format before evaluation reduces false negatives from 12% to 7% on AIME.

Splitting verification across separate conversation threads sharply degrades performance — verification requires holistic context and cannot be decomposed into independent per-segment checks without severe miscalibration.

---

### Implicit Scaling

The paper's most counterintuitive finding: sampling more candidate responses *improves* per-candidate verification accuracy, rather than degrading it. This is called **implicit scaling**.

The mechanism: larger candidate pools contain higher-quality (more rigorous, more verifiable) correct responses — not merely more correct responses. Well-written, formally structured responses are easier to verify than poorly written ones. Scaling $k_\text{inf}$ therefore widens the pool of verifiable candidates simultaneously with improving Pass@k, violating the naive expectation of an accuracy-recall tradeoff.

This has a compounding implication: stronger base models, which produce more rigorous reasoning, will see amplified gains from sampling-based search — better generation directly amplifies verification accuracy in a virtuous cycle.

---

### Results

| Benchmark | Consistency@200 | Verification@200 | o1-Preview |
|---|---|---|---|
| AIME 2024 | 26.7% (4/15) | 53.3% (8/15) | 46.7% (7/15) |
| MATH | — | 467/500 | 428/500 |
| LiveBench Math | — | 135/200 | 131/200 |
| LiveBench Reasoning | — | 97/140 | 95/140 |

Verification@200 doubles Consistency@200 accuracy on AIME and surpasses o1-Preview on all four benchmarks — using Gemini v1.5 Pro, a model *not* explicitly trained for [[themes/reasoning_and_planning|reasoning search]], outperforming a model specifically trained to leverage internal test-time compute.

On AIME, performance follows a **power-law scaling trend** as $k_\text{inf}$ increases; Consistency@k plateaus. The AIME Problem 11 example is illustrative: 124 of 200 responses reach the wrong answer "1"; the single response reaching the correct answer "601" receives 98% verification confidence versus ≤36% for all "1" responses — Consistency fails, Verification succeeds.

A hybrid **Pro+Flash** configuration (Pro generates candidates, Flash verifies) reduces per-question cost from ~$200 to ~$12 while matching or exceeding Pro-only Consistency@200 — equivalent in compute cost to roughly Consistency@500.

---

### Verification Benchmark

A new verification benchmark reveals the depth of the out-of-box verification deficit:

| Model | Identifies wrong responses as wrong |
|---|---|
| o1-Preview | 68.8% (scoring), 84.5% (comparison) |
| GPT-4o | ~31% |
| Claude 3.5 Sonnet | ~22.5% |
| Random baseline | ~20% |

The "Flawed" category — responses that reach the correct final answer through flawed reasoning — is particularly difficult: GPT-4o succeeds 22.2% of the time, Claude 3.5 Sonnet 33.3%, near or below random.

---

## Key Claims

1. **Implicit scaling exists:** Sampling more candidates improves self-verification accuracy because larger pools contain higher-quality, more verifiable correct responses.
2. **CoT is generation-optimal, not verification-optimal:** Chain-of-thought format is harder to verify than structured theorem-lemma-proof format; rewriting before verification improves accuracy.
3. **Comparative verification localizes errors:** Providing the verifier with other candidate responses produces strong signals about error location and hallucinations.
4. **Verification@200 surpasses o1-Preview** on AIME (8/15 vs 7/15), MATH, LiveBench Math, and LiveBench Reasoning.
5. **Consistency@k saturates hard:** Consistency@50 equals Consistency@10,000 on AIME; additional sampling cannot overcome this ceiling.
6. **Verification@k follows power-law scaling** on AIME even as Consistency@k plateaus.
7. **Performance has not saturated** at 200 samples — trends indicate further gains remain available.
8. **Pass@1 optimization (RLHF) may harm search** by reducing output diversity and Pass@k.

---

## Capabilities

- **Minimalist sampling-based search** (Verification@200) elevates Gemini v1.5 Pro above o1-Preview on four [[themes/mathematical_and_formal_reasoning|mathematical reasoning]] benchmarks using only random sampling and natural-language self-verification — no specialized training required. *(narrow production)*
- **Implicit scaling** — a virtuous cycle where more samples produce more verifiable candidates, improving verification accuracy simultaneously with recall. *(research only)*
- **Comparative verification** localizes errors by leveraging candidate disagreements, enabling reliable tie-breaking. *(demo)*
- **Output-style rewriting** into theorem-lemma-proof format reduces verification false negative rate from 12% to 7% on AIME. *(demo)*
- **Sustained power-law compute scaling** on hard benchmarks, contrasting with the hard ceiling of consistency-based methods. *(research only)*
- **Long-tail recovery** — can identify the 1-in-200 correct response even when 124 of 200 responses agree on the wrong answer. *(demo)*
- **Hybrid cost reduction** (Pro+Flash) achieves competitive performance at ~$12/question versus ~$200 for full Pro pipeline. *(demo)*

---

## Limitations & Open Questions

**Verification capability is near-random out-of-the-box.** Frontier models barely exceed random chance at identifying incorrect responses without specialized prompting. This is the primary bottleneck blocking efficient deployment — every verification gain in this paper requires multi-sample averaging and careful prompt engineering to overcome fundamental LLM recall deficits. The authors suggest instruction tuning on verification tasks as low-hanging fruit; the trajectory is improving but the baseline is alarming.

**Cost is prohibitive at scale.** Full Verification@200 costs $200–$650 per reasoning question at public API pricing (200 samples × 50 verifications × ~13K tokens ≈ 130M output tokens). This restricts deployment to narrow high-stakes applications and forces research evaluation on tiny test sets — AIME results are based on n=15, raising statistical reliability concerns.

**RLHF creates structural tension with search.** [[themes/reinforcement_learning|Reinforcement learning]] from human feedback optimizes Pass@1, which may systematically reduce the output diversity that sampling-based search requires. The paper identifies this as a significant open problem: current post-training practice and effective inference-time scaling may be in direct conflict.

**CoT and verification are mismatched formats.** The dominant generation paradigm produces outputs that are structurally harder to verify. This creates a format-level bottleneck that the rewriting step only partially addresses — it adds compute and may not generalize to all domains.

**Verification degrades on certain task types.** LiveBench Olympiad sees -9% relative degradation versus Consistency, revealing task-format incompatibilities the paper does not fully resolve. The pipeline is not universally beneficial.

**Flawed reasoning is invisible to verifiers.** Models cannot reliably flag responses that reach the correct answer through incorrect reasoning — the hardest and most important verification failure mode for ensuring genuine understanding rather than lucky answers.

**Decomposed verification fails.** Verification cannot be split into independent per-segment checks; it requires holistic context. This limits architectural options for cost reduction.

**Performance has not saturated.** Achieving maximum benefit from sampling-based search requires compute that grows without a known ceiling on current benchmarks — practical deployments are always operating sub-optimally.

---

## Landscape Connections

### Bottlenecks Addressed or Characterized

- **LLM self-verification accuracy** — characterized as near-random, with a concrete path to improvement via instruction tuning. Blocks efficient sampling-based search deployment and reliable [[themes/reinforcement_learning|RL reward generation]].
- **Per-query inference cost** — $200+ per question blocks broad adoption; the Pro+Flash hybrid reduces this to ~$12 but the underlying compute demand remains a 1–2 year horizon problem.
- **Pass@1 vs Pass@k training tension** — RLHF-trained models may be structurally worse search targets; inference-aware training objectives are identified as a needed research direction.

### Breakthroughs

- **Sampling-based search surpasses trained reasoning models** — a minimalist pipeline with no specialized training beats o1-Preview, establishing a strong reproducible baseline any non-trivial inference method must exceed.
- **Implicit scaling discovery** — overturns the naive accuracy-recall tradeoff intuition and suggests that better base models will see compounding search gains, not merely additive ones.

### Implications for Adjacent Themes

- **[[themes/reward_modeling|Reward modeling]]:** Poor out-of-box verification undermines RL pipelines that rely on self-verification for reward signals; improving verification capability is prerequisite to effective self-play and data flywheeling.
- **[[themes/reinforcement_learning|Reinforcement learning]]:** The Pass@1 vs Pass@k tension implies RL training may be actively reducing the diversity needed for inference-time search — a structural problem for the dominant post-training paradigm.
- **[[themes/chain_of_thought|Chain-of-thought]]:** CoT's dominance as a generation format creates a systematic verification bottleneck; structured outputs may be preferable in search-heavy deployments even if they sacrifice some generation quality.
- **[[themes/test_time_compute_scaling|Test-time compute scaling]]:** Verification@k establishes a concrete power-law baseline against which speculative decoding, tree search, and process reward models should be compared.

---

## Themes

- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Key Concepts

- [[entities/livebench|LiveBench]]
- [[entities/self-verification|Self-Verification]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
- [[entities/passk|pass@k]]
