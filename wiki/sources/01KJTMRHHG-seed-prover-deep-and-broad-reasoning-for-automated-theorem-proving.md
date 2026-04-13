---
type: source
title: 'Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving'
source_id: 01KJTMRHHGEJAPYKFBPHVV6MCE
source_type: paper
authors:
- Luoxin Chen
- Jinming Gu
- Liankai Huang
- Wenhao Huang
- Zhicheng Jiang
- Allan Jie
- Xiaoran Jin
- Xing Jin
- Chenggang Li
- Kaijing Ma
- Cheng Ren
- Jiawei Shen
- Wenlei Shi
- Tong Sun
- He Sun
- Jiahui Wang
- Siran Wang
- Zhihong Wang
- Chenrui Wei
- Shufa Wei
- Yonghui Wu
- Yuchen Wu
- Yihang Xia
- Huajian Xin
- Fan Yang
- Huaiyuan Ying
- Hongyi Yuan
- Zheng Yuan
- Tianyang Zhan
- Chi Zhang
- Yue Zhang
- Ge Zhang
- Tianyun Zhao
- Jianqiu Zhao
- Yichi Zhou
- Thomas Hanwen Zhu
published_at: '2025-07-31 00:00:00'
theme_ids:
- chain_of_thought
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving

Seed-Prover is a large language model specialized in formal theorem proving in Lean 4, developed to address the gap between LLMs' natural language mathematical reasoning and machine-verified proof generation. The system introduces lemma-style whole-proof generation — where intermediate lemmas from different inference paths accumulate in a shared pool and are recombined across attempts — alongside a three-tiered test-time compute strategy that scales from iterative refinement to days-long conjecture search. Paired with Seed-Geometry, a neuro-symbolic geometry engine with a C++-rewritten reasoning backend, the combined system proved 5 out of 6 IMO 2025 problems with full Lean verification, surpassing all prior automated theorem proving results and matching frontier natural-language AI performance on competition mathematics.

**Authors:** Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu, Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan, Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, Thomas Hanwen Zhu
**Published:** 2025-07-31
**Type:** Paper
**Source:** https://arxiv.org/pdf/2507.23726

---

## Background and Motivation

The central difficulty in applying LLMs to formal theorem proving is the absence of reliable supervision signals. LLMs have achieved strong results on natural language mathematics benchmarks (MATH, AIME) via [[themes/reinforcement_learning|reinforcement learning]], but natural language proofs offer no automatable correctness signal — each step requires careful manual or automated verification, making RL reward computation noisy or impossible at scale. Formal proof assistants like Lean 4 solve this: the compiler provides exact binary feedback on proof validity. The challenge shifts to generating proofs the compiler accepts.

Prior work split into two architecturally constrained families:

- **Step-level provers** interact with the Lean environment line-by-line, enabling tight compiler feedback but requiring special scaffolding and operating at too fine a granularity for strategic [[themes/reasoning_and_planning|high-level reasoning]].
- **Whole-proof generators** produce complete proofs in a single pass, supporting [[themes/chain_of_thought|chain-of-thought]] reasoning but lacking iterative compiler interaction — capping their ability to recover from partial failures.

Neither family scaled to IMO-level difficulty. Additionally, prior whole-proof models trained only on formal statements as RL prompts, missing the diversity of hints — natural language proofs, failed attempts, compiler error messages — that would make them robust at inference time. A further domain gap: Lean's lack of native geometry support meant olympiad geometry problems required a separate reasoning substrate entirely.

---

## Approach

### Lemma-Style Whole-Proof Generation

Seed-Prover's most significant architectural departure from prior work is requiring the model to generate named intermediate `lemma` blocks before the main `theorem`. Each lemma is independently compilable, enabling:

- Clear identification of what has been proved versus what remains open
- A **shared lemma pool** per problem that stores all lemmas across inference runs, indexed by name, formal statement, proof difficulty, and dependency relations
- Cross-trajectory knowledge reuse: lemmas from failed attempts in one inference run become available context for subsequent attempts

Unlike Draft-Sketch-Prove, which presupposes the model can outline a full solution path, lemma-style proving allows modular progress — the system can accumulate useful intermediate facts even when the main theorem remains out of reach.

### Training: Multi-Task RL with VAPO

Seed-Prover is trained with multi-stage, multi-task [[themes/rl_for_llm_reasoning|RL using VAPO]] over a diverse prompt distribution that randomly includes:

- Natural language problem hints
- Previously proved or failed lemmas
- Lean compiler feedback
- Summaries of prior attempts

This trains the model to exploit all these signal types at inference time, not just bare formal statements. A formatting penalty during RL reinforces lemma-before-theorem output as a robust behavior rather than a prompted heuristic. A difficulty-aware curriculum progressively increases problem difficulty and max output length; problems with proof rate above 1/4 are excluded from RL training, since they provide no useful learning signal.

### Three-Tiered Test-Time Compute Scaling

A core contribution is a structured [[themes/test_time_compute_scaling|test-time compute]] hierarchy:

| Tier | Mechanism | Wall Time | Use Case |
|------|-----------|-----------|----------|
| **Light** | Up to 8–16 iterative refinement passes using Lean compiler feedback + self-summarization | 1–2 hours | Equivalent to Pass@64–256; fixes syntax errors, revises proof sketches mid-trajectory |
| **Medium** | Adds inner loop targeting difficult lemmas; feeds proven sub-lemmas back into outer loop | Hours–days | Proofs exceeding 1000 lines; IMO P5 |
| **Heavy** | Conjecture pool of ~5000 candidates; light inference to prove/disprove each; scored lemma pool fed into medium inference | Days | IMO P1, P3, P4 |

The **Conjecture Proposer** module underpins Heavy inference: rather than committing to a proof path, it broadly enumerates potentially useful properties (injectivity, monotonicity, periodicity, etc.) across parallel chains of thought, building a diverse conjecture pool scored by proof rate, semantic relevance (LLM judge), and proof length.

### Seed-Geometry

Because Lean lacks native geometry support, a companion neuro-symbolic system handles olympiad geometry:

- **C++-rewritten forward-chaining reasoning backend**: ~100× faster than the prior Python TongGeometry implementation
- **Extended DSL** with composite ruler-and-compass actions (isogonal conjugate, exsimilitude/insimilitude centers)
- **Policy-only LLM** for auxiliary construction proposals — value model experiments were abandoned after extensive search showed large estimation errors degraded overall performance
- **230 million unique geometry problems** generated synthetically by running the C++ engine on historical olympiad statistics for 7+ days, yielding ~38B tokens of training data

---

## Results

### IMO 2025

Seed-Prover and Seed-Geometry together proved **5 out of 6 IMO 2025 problems** with full Lean verification:

- **P2** (geometry): Seed-Geometry, solved in 2 seconds after human-provided formalization
- **P1, P3, P4** (algebra/number theory): Seed-Prover, Heavy inference setting (days of search)
- **P5**: Seed-Prover, Medium inference setting
- **P6**: Unsolved — a hard ceiling at the upper tail of competition difficulty
- **P1 note**: Proof completed after the competition deadline; the system could not reliably solve all hard problems within real competition time constraints

This surpasses AlphaProof's 3/6 at IMO 2024 and equals frontier natural-language AI performance (Gemini 5/6) while providing machine-verified correctness guarantees.

### Benchmark Performance

| Benchmark | Seed-Prover | Previous SOTA | Notes |
|-----------|-------------|---------------|-------|
| MiniF2F-valid | 100.0% | 90.6% | Saturated |
| MiniF2F-test | 99.6% | 92.2% | Near-saturated |
| PutnamBench | 331/657 (50.4%) | 86/657 (13.1%, Goedel-Prover-V2) | ~3.85× improvement |
| Past IMO (155 problems) | 121/155 (78.1%) | — | Including 27/44 hard P3/P6 |
| MiniCTX-v2 | 81.8% | 44.3% (o4-mini, Pass@8) | Contamination-free, real-world repos |
| CombiBench | 30/100 (30%) | 10% (DeepSeek-Prover-V2) | 3× improvement |
| IMO-AG-50 (geometry) | 43/50 | 42/50 (AlphaGeometry 2) | |
| IMO shortlist geometry 2000–2022 | 22/39 | 19/39 (AlphaGeometry 2) | |

The PutnamBench result is particularly significant: a ~3.85× improvement crossing the 50% threshold for undergraduate mathematics marks a qualitative capability jump for automated formal provers.

---

## Limitations and Open Questions

### Structural Blockers

**Human formalization remains mandatory.** Every problem must be translated into a correct Lean statement by human experts before the system can attempt a proof. For IMO 2025 fill-in-the-blank problems, this required determining the answer first and encoding it correctly — no automated pipeline exists for the natural language → formal statement step. This is the primary bottleneck blocking fully autonomous mathematical reasoning.

**Heavy inference is economically infeasible at scale.** Days of compute per problem confines the system to prestige competitions, not general mathematical research. The current system is only practically viable for a handful of high-stakes problems.

**One problem remains unsolved.** P6 of IMO 2025 is beyond the system under all inference settings. 34/155 past IMO problems (22%) remain unsolved even under maximum heavy inference — a hard capability ceiling at the olympiad level persists.

### Domain-Specific Gaps

**Combinatorics is disproportionately hard.** Seed-Prover proves 7/14 (50%) of past IMO combinatorics problems versus 72/85 (85%) of algebra and 42/55 (76%) of number theory problems, and achieves only 30% on CombiBench. Problems involving newly-defined combinatorial structures expose a fundamental gap: no breakthrough approach exists for formally proving problems where the underlying mathematical structures must be constructed from scratch. This bottleneck likely requires 3–5 years to resolve.

**Geometry is not a first-class Lean citizen.** Seed-Geometry's existence as a parallel system is itself a limitation — geometry requires a separate DSL, C++ engine, and training pipeline. Seed-Geometry is also restricted to proof-based geometry; computation-based problems (solvable by algebraic engines) are outside its scope, explaining why AlphaGeometry 2 solves some problems Seed-Geometry cannot.

### Formalization Difficulty Mismatch

Some problems trivial in natural language become disproportionately difficult in Lean. The hardest MiniF2F problems solved include AMC12A problems that are straightforward mathematically but require elaborate formal scaffolding (e.g., applying Vieta's formulas, counting roots). This creates artificial barriers unrelated to mathematical difficulty and means benchmark scores do not map cleanly onto mathematical capability.

### Architectural Design Decisions

**Value models are not viable for formal proof search.** Experiments showed that under extensive search, value model estimation errors degraded overall performance — the actor-critic design was abandoned in favor of a single policy. This is a notable negative result: the intuition that learned value functions would guide proof search more efficiently than policy-only methods does not hold at the scale of combinatorial proof search.

**One-shot auxiliary construction generation fails for geometry.** Generating full auxiliary construction sequences in a single pass is significantly inferior to step-by-step beam search. Whole-sequence geometry approaches are not a viable alternative.

---

## Significance and Connections

### A Parity Milestone

The 5/6 IMO 2025 result represents parity between formally-verified and natural-language AI provers — a threshold that seemed distant even a year prior. The significance is not just the score but the verification: every Lean proof is machine-checked, eliminating the evaluation ambiguity that plagues natural language mathematical reasoning assessments. This makes formal AI provers uniquely trustworthy for applications requiring correctness guarantees.

### Lemma Accumulation as a New Paradigm

The cross-trajectory lemma pool transforms [[themes/mathematical_and_formal_reasoning|formal theorem proving]] from independent sampling into knowledge accumulation. Proved intermediate facts from failed attempts become assets for future attempts, turning compute into a resource that compounds rather than simply scales linearly. This architectural insight is likely to propagate beyond Seed-Prover.

### Connection to Test-Time Compute Scaling

The three-tiered inference hierarchy is a concrete instantiation of [[themes/test_time_compute_scaling|test-time compute scaling]] for a domain with deterministic correctness feedback. Unlike natural language reasoning where scaling is evaluated through soft metrics, formal provers provide exact signals, making the scaling curves interpretable. The gap between Light (1–2 hours) and Heavy (days) demonstrates that current LLMs can be pushed to qualitatively harder problems through structured search — but only with architectural support (lemma pools, conjecture proposers) rather than raw sampling.

### Reinforcement Learning with Verified Feedback

Seed-Prover exemplifies the strongest case for [[themes/rl_for_llm_reasoning|RL for LLM reasoning]]: a domain with exact, automatable reward signals. The VAPO training setup — diverse prompt distribution, difficulty curriculum, formatting penalties — demonstrates that RL works best when the training distribution matches inference-time conditions, including the diversity of hints and feedback types the model will encounter.

---

## Themes

- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Key Concepts

- [[entities/alphaproof|AlphaProof]]
- [[entities/passk|pass@k]]
