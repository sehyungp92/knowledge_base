---
type: source
title: 'Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision'
source_id: 01KJTHM1GBEV1R8PR5KXYWG07Z
source_type: paper
authors:
- Dulhan Jayalath
- Shashwat Goel
- Thomas Foster
- Parag Jain
- Suchin Gururangan
- Cheng Zhang
- Anirudh Goyal
- Alan Schelten
published_at: '2025-09-17 00:00:00'
theme_ids:
- medical_and_biology_ai
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scientific_and_medical_ai
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 12
tags: []
---
# Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision

**Authors:** Dulhan Jayalath, Shashwat Goel, Thomas Foster, Parag Jain, Suchin Gururangan, Cheng Zhang, Anirudh Goyal, Alan Schelten
**Published:** 2025-09-17 00:00:00
**Type:** paper

## Analysis

# Compute as Teacher: Turning Inference Compute Into Reference-Free Supervision
2026-02-03 · paper · Dulhan Jayalath, Shashwat Goel, Thomas Foster, Parag Jain, Suchin Gururangan et al. (8 total)
https://arxiv.org/pdf/2509.14234v1

---

### Motivation & Prior Limitations
Post-training large language models in non-verifiable domains — where outputs are qualitative and no ground truth exists — has remained an unsolved supervision problem, blocking RL-based improvement outside narrow formal domains.
- Programmatic verifiers for RL rewards only work in domains like math and code where formal correctness is computable, leaving qualitative domains such as clinical guidance, freeform dialogue, and creative writing without usable training signal.
  - The two incumbent alternatives each fail in distinct ways: human annotation pipelines are expensive and hard to scale, while judge-only LLM feedback suffers from known issues with inconsistency, verbosity bias, and reward hacking.
- Even in non-verifiable settings where expert annotations exist (e.g., physician-labeled healthcare data), acquiring them at scale is a significant bottleneck, motivating a framework that can match or exceed annotation quality without requiring it.

---

### Proposed Approach
Compute as Teacher (CaT) recycles inference-time compute — parallel rollouts already needed for sampling — directly into training supervision, closing the label-free RL gap in non-verifiable domains without additional annotation infrastructure.
- The framework has two sequential components: (1) **reference estimation**, which aggregates G parallel rollouts for a query into a single pseudo-reference answer, and (2) **reward derivation**, which converts that pseudo-reference into RL rewards for the current policy.
  - For reference estimation, the paper introduces **synthesis**, a simple rollout-aggregation method, while noting the framework is modular and admits any aggregator.
  - For reward derivation in non-verifiable domains, the paper introduces **self-proposed rubrics**: binary, auditable evaluation criteria automatically generated from the pseudo-reference and scored by an LLM judge — a structured alternative to coarse scalar judge scores that provides more interpretable and hackable-resistant reward signal.
- For verifiable domains, the same framework plugs in programmatic checkers as the reward derivation step, demonstrating "drop-in" versatility across domain types without architectural changes.

---

### Results & Capabilities
CaT trained models on HealthBench match or exceed the quality of inference-time aggregation (running many rollouts at test time) while requiring 9x less test-time compute, converting a compute-at-inference cost into a one-time training cost.
- On HealthBench, CaT yields up to +30% relative improvement over the initial policy, and the learned model competes with models trained on expert physician annotations — despite CaT requiring no human labels.
  - This result is particularly significant because it demonstrates that a non-verifiable, high-stakes domain (healthcare guidance) can be effectively improved via purely self-supervised inference compute.
- On MATH-500, CaT with verifiable rewards matches the best existing test-time RL baselines, confirming the framework does not sacrifice performance in domains where strong alternatives already exist.

---

### Implications
CaT opens a general pathway for RL post-training in any domain where inference compute is affordable, regardless of whether ground truth or expert labels exist, potentially decoupling model improvement from annotation pipelines across the full breadth of LLM applications.
- The compute-to-supervision conversion implies a direct scaling law between inference budget and training signal quality: richer pseudo-references from more rollouts should yield better rewards, linking test-time compute scaling to training-time improvement in a feedback loop.
- Self-proposed rubrics as a reward mechanism offer an interpretable, auditable alternative to opaque scalar LLM judge scores, which has implications for reward hacking mitigation and transparency in RLHF-like pipelines for safety-sensitive domains.
- The result that CaT competes with physician annotation in healthcare suggests that expert-level supervision may be approximable via self-play-style aggregation in specialized domains, with consequences for how AI systems in high-stakes verticals are trained and audited.

---

### Remaining Limitations & Next Steps
The source text (abstract and partial introduction) does not detail ablations, failure modes, or explicit author caveats about limitations; the following are inferred from scope and design.
- The quality of the pseudo-reference answer — and therefore the quality of the reward signal — is bounded by the capability of the current policy, meaning CaT may stall or degrade in domains where the policy is already near its performance ceiling or systematically biased.
  - This is an implicit bootstrapping limitation: if all rollouts are poor, synthesis over poor rollouts produces a poor pseudo-reference and misleading rubrics.
- Self-proposed rubrics are scored by an LLM judge, which inherits the judge's own biases; while binary rubrics mitigate verbosity bias and inconsistency relative to scalar scoring, they do not eliminate judge-induced reward signal distortion.
- Evaluation is demonstrated on HealthBench and MATH-500, which represent one non-verifiable and one verifiable domain respectively; generalization to other qualitative domains (creative writing, freeform dialogue) is claimed but not evidenced in the available text.
- The 9x compute reduction claim is relative to inference-time aggregation at test time, but the absolute training compute cost of CaT (running G rollouts per training step across many steps) is not characterized in the available text, making total compute budget comparisons against annotation pipelines unclear.

## Key Claims

1. Inference compute itself can serve as supervision for RL training, enabling models to learn without human labels
2. CaT enables learning without human labels in non-verifiable domains like healthcare guidance where no programmatic checker exists
3. The CaT framework has two components: reference estimation that aggregates rollouts into a pseudo-reference answer, and reward derivation that converts the pseudo-reference into RL rewards
4. Synthesis is a simple aggregation method used in CaT's reference estimation step, though the framework admits any aggregator
5. Self-proposed rubrics are binary, auditable criteria generated from the pseudo-reference and scored by an LLM judge, used for reward derivation in non-verifiable domains
6. Models trained with CaT match or exceed inference-time aggregation quality on HealthBench while using 9x less test-time compute
7. CaT competes with learning from expert physician annotations on HealthBench, yielding up to +30% relative improvement over the initial policy
8. CaT extends to verifiable domains, matching the best existing baselines on MATH-500 in test-time RL
9. Programmatic checkers for verifiable RL rewards are only applicable in narrow domains like math or code where formal correctness is computable
10. Judge-only LLM feedback for freeform outputs has known issues with inconsistency, verbosity bias, and reward hacking

## Capabilities

- CaT (Compute as Teacher) framework enables RL post-training in non-verifiable domains using parallel inference rollouts as self-generated supervision, eliminating the need for human annotations or programmatic verifiers
- CaT-trained models match or exceed the quality of inference-time aggregation on HealthBench while requiring 9x less test-time compute, effectively amortizing parallel inference cost into training
- Self-proposed rubrics provide binary, auditable RL reward criteria for non-verifiable domains — generated from a pseudo-reference answer and scored by an LLM judge, requiring no external annotation
- CaT training competes with expert physician annotations on HealthBench, yielding up to +30% relative improvement over the initial policy — demonstrating label-free RL can approach human expert supervision quality in medical guidance
- CaT framework transfers to verifiable domains with drop-in compatibility, matching best existing baselines on MATH-500 in test-time RL without domain-specific modifications

## Limitations

- Self-proposed rubrics in CaT rely on LLM judges which carry known failure modes — inconsistency across runs, verbosity bias, and susceptibility to reward hacking — undermining reward reliability in non-verifiable domains
- CaT's pseudo-reference quality is bounded by the policy's own rollout distribution — in domains where the model is systematically wrong, aggregating its own outputs cannot produce correct supervision, creating a self-reference ceiling
- Programmatic correctness verification is structurally restricted to narrow domains (math, code), leaving the vast majority of knowledge work domains without verifiable reward signals for RL training
- In non-verifiable domains like clinical or lifestyle guidance, experts can legitimately disagree — meaning no single pseudo-reference from aggregation can be treated as authoritative, introducing irreducible noise in CaT rewards
- CaT is evaluated only on HealthBench and MATH-500 — generalization to other non-verifiable domains (creative writing, freeform dialogue, legal reasoning) is asserted but not demonstrated
- Human annotation pipelines — the only robust alternative to programmatic verifiers in non-verifiable domains — are hard to scale and expensive, creating a structural bottleneck in post-training for real-world applications
- Self-proposed rubrics are generated from the same pseudo-reference used to derive rewards — creating a circular dependency where the reward signal and the reference it evaluates against share the same origin, amplifying any systematic biases in the initial rollouts

## Bottlenecks

- LLM judge reliability for non-verifiable RL rewards is an unresolved bottleneck: self-proposed rubrics scored by LLM judges inherit the judge's inconsistency, verbosity bias, and reward-hacking vulnerability, limiting the trustworthiness of CaT-derived reward signals in safety-critical domains

## Breakthroughs

- CaT demonstrates that inference-time parallel compute can be converted into training supervision, enabling RL post-training in non-verifiable domains without human labels or programmatic verifiers — breaking the hard boundary between verifiable and non-verifiable RL training

## Themes

- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/healthbench|HealthBench]]
