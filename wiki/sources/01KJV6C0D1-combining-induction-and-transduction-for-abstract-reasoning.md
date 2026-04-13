---
type: source
title: Combining Induction and Transduction for Abstract Reasoning
source_id: 01KJV6C0D1QTS98FMWFF8MZ02H
source_type: paper
authors:
- Wen-Ding Li
- Keya Hu
- Carter Larsen
- Yuqing Wu
- Simon Alford
- Caleb Woo
- Spencer M. Dunn
- Hao Tang
- Michelangelo Naim
- Dat Nguyen
- Wei-Long Zheng
- Zenna Tavares
- Yewen Pu
- Kevin Ellis
published_at: '2024-11-04 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Combining Induction and Transduction for Abstract Reasoning

This paper introduces BARC (Bootstrapped ARC), a system that achieves near-human-average performance on the Abstraction and Reasoning Corpus by training separate neural models for inductive program synthesis and transductive output prediction, then ensembling them. Its central empirical contribution is the surprising discovery that induction and transduction solve strongly complementary problem sets even when trained on identical data with the same architecture — a finding that contradicts prior consensus and reshapes how the field should approach few-shot generalisation systems.

**Authors:** Wen-Ding Li, Keya Hu, Carter Larsen, Yuqing Wu, Simon Alford, Caleb Woo, Spencer M. Dunn, Hao Tang, Michelangelo Naim, Dat Nguyen, Wei-Long Zheng, Zenna Tavares, Yewen Pu, Kevin Ellis
**Published:** 2024-11-04
**Type:** paper
**Source:** https://arxiv.org/pdf/2411.02272

---

## Background and Prior Work

The [[themes/evaluation_and_benchmarks|Abstraction and Reasoning Corpus (ARC)]] is among the most demanding few-shot generalisation benchmarks, covering occlusion, pathfinding, symmetry, gravity, and counting in composite grid-transformation tasks. Prior approaches had bifurcated into two camps:

- **Inductive program search** over domain-specific languages (DSLs), which held against GPT-4 but was ultimately surpassed
- **Transductive neural architectures** with test-time training (Cole et al., 2024), which became the dominant paradigm

Crucially, neither camp left room for genuine complementarity. Seminal work (Devlin et al., 2017) had concluded induction was simply superior to transduction on program synthesis tasks, and the leading ARC team explicitly advocated transduction as the primary approach. BARC challenges both conclusions.

A secondary obstacle was data generation: valid ARC inputs are highly function-specific, and naive LLM hallucination cannot produce the precisely-structured grids the benchmark requires. Prior datasets like ReARC used handwritten DSL programs without natural language annotations, blocking LLM-based augmentation.

---

## The BARC System

### Architecture

BARC trains two models from the same base (Llama3.1-8B-instruct, selected over Mistral-7B and Qwen2-7B in preliminary experiments for its code pretraining):

- **Induction model**: samples a budget of candidate Python programs at test time, filters for consistency with training input-output pairs, predicts using any passing program
- **Transduction model**: uses beam search to directly predict the test output without constructing an intermediate function

The ensemble is sequential and trivial: attempt induction first, fall back to transduction when no consistent program is found.

### Synthetic Data Generation

The [[themes/synthetic_data_generation|data pipeline]] starts from 100–160 manually-written seed programs. Each seed has three components:

1. A natural language description of the ARC task
2. A `transform_grid` Python function implementing the transformation
3. A `generate_input` function that produces valid, precisely-structured inputs

An LLM remixes these seeds via in-context learning (for descriptions) and RAG-based code generation (for programs) to produce up to 400k new problems paired with Python solutions. The key design decision — executing `generate_input` rather than having the LLM hallucinate grids directly — ensures training examples are structurally valid and consistent with their transformations.

### Domain-Specific Libraries, Not Languages

Rather than restricting programs to a DSL, BARC provides a shared Python library of reusable subroutines (sprite generation, symmetry detection, object extraction). The paper explicitly advocates **domain-specific libraries over domain-specific languages**, arguing that general-purpose languages with domain priors give broader coverage without truncating the long tail of diverse tasks. This connects to broader debates in [[themes/mathematical_and_formal_reasoning|formal reasoning]] about the expressive cost of constrained program spaces.

---

## Results and Capabilities

### Near-Human Performance

The ensemble achieves **56.75%** on the ARC public validation set, against average human performance of 60.2%. This surpasses all prior published methods: Claude-3.5 / Greenblatt (42%), CodeIt (15%).

Akyürek et al. (2024) subsequently improved to **61.9%** by applying better [[themes/post_training_methods|test-time training]] to the BARC transduction model while keeping the BARC induction model unchanged. Without BARC's models, their method scores only 47.1% — confirming that program synthesis contributes non-substitutable signal.

### Complementarity

The central empirical finding: induction and transduction solve **largely disjoint problem sets**, statistically significant at p < .004 and stable across random initializations. The division of labour is interpretable:

- **Induction** excels at precise computations and multi-concept composition (counting, symbolic rule chaining)
- **Transduction** excels at fuzzy perceptual judgements (orientation, relative position) that resist clean symbolic description

On ConceptARC (single isolated concepts), transduction's advantage grows because induction's compositional strength becomes less relevant. The stability across initializations indicates that problem *type*, not random variation, governs which paradigm succeeds.

### Scaling Behaviour

| Axis | Behaviour |
|---|---|
| Test-time sampling budget (induction) | Near-monotonic improvement up to 20k samples |
| Human seed count | Saturates quickly beyond ~100 seeds |
| Synthetic data volume | Continues improving with scale |
| Data quality (GPT-4 vs GPT-4o-mini descriptions) | Significant effect, especially for induction |

This scaling profile suggests that **compute, not human labelling**, is the primary scaling lever once a seed threshold is crossed — a meaningful signal for [[themes/synthetic_data_generation|synthetic data]] methodology.

---

## Limitations and Open Questions

### Deployment Infeasibility at Scale

The most immediate practical limitation is compute cost. The flagship model requires 20,000 sampled programs for peak performance; at 384 samples (Kaggle budget), accuracy drops from 38% to 4% on the private test set. Neural inductive program synthesis is currently **research-only** — production deployment is blocked by this compute bottleneck.

### No Autonomous Domain Discovery

BARC cannot grow more competent by solving new problems. It bootstraps entirely from manually-encoded seed knowledge and has no mechanism to discover the domain priors it relies upon. The paper acknowledges this directly: a more compelling system would discover for itself what human experts compiled into the seeds. This limits transfer to new domains without specialist labelling effort, creating a human expert bottleneck of ~100–160 seed programs per domain.

### Fundamental Misfit with Human-Easy Problems

Models trained on simple Python programs surpass human performance on the hardest 20% of ARC problems while underperforming humans on the easiest 20%. This inversion reveals a structural mismatch: the core cognitive priors humans deploy effortlessly on simple problems are not easily expressed in Python — they live in a representational gap that program-space priors cannot close.

### Sequential Ensemble Lacks Integration

The ensemble is strictly induction-then-transduction. Human cognition interleaves these modes: fast intuitions are further processed by deliberative symbolic reasoning, and symbolic hypotheses are informed by perceptual shortcuts. BARC has no mechanism to reproduce this iterative fast-intuition/deliberative loop, representing a fundamental architectural limitation relative to human problem-solving.

### Theoretical Anomaly

Theoretically, induction and transduction should converge with sufficient meta-training data to similar solutions — the empirically observed complementarity implies the real-world setting is subject to constraints not captured by idealised theory (finite data, representational bottlenecks, optimisation landscape). This unresolved gap between theory and observation is a live open question for the [[themes/reasoning_and_planning|reasoning]] community.

### Additional Limitations

- ~9% of programs passing training-example filters are false positives (consistent with training inputs but incorrect on test output); majority voting suppresses about half
- Induction is 41% more sensitive to data quality than transduction (GPT-4o-mini → GPT-4 descriptions: 11.08% → 18.78% for induction vs. negligible for transduction)
- Method is only applicable when target generalisations can be expressed in Python — tasks requiring natural language pragmatics, pixel-level aesthetics, or other non-symbolic representations fall outside scope
- System is compute-inefficient even while sample-efficient — 400k synthetic problems generated via LLM inference plus large-model fine-tuning represents substantial upfront cost

---

## Bottlenecks Addressed and Created

**Partially resolved:** The paper demonstrates that near-human-average ARC performance is achievable without hand-engineering a complete DSL, by replacing language constraints with library priors and scaling synthetic data.

**Created / sharpened:**

- **Cost-effective test-time scaling** of neural inductive program synthesis remains blocking for production use (3–5 year horizon)
- **Unified inductive-transductive representations** — current sequential ensembles are a stopgap; closing the remaining gap to best-human performance requires representations that intertwine both modes rather than switching between them (3–5 year horizon)
- **Autonomous domain prior discovery** — blocking self-improving program synthesis and limiting methodology transfer without expert seed curation (3–5 year horizon)

---

## Connections

- [[themes/benchmark_design|Benchmark Design]] — ARC's structure forces explicit engagement with few-shot generalisation in ways that standard benchmarks do not; this paper's results clarify what kinds of reasoning benchmarks stress
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]] — 56.75% vs. 60.2% human average collapses a previously large gap; subsequent work reaching 61.9% pushes past average human, reframing ARC from an unsolved challenge to a calibration tool
- [[themes/post_training_methods|Post-Training Methods]] — test-time training significantly improves transduction (29.1% → 43.0%); BARC's transduction model is the direct substrate for Akyürek et al.'s TTT gains
- [[themes/synthetic_data_generation|Synthetic Data Generation]] — the seed-bootstrapping pipeline with executable input generators is a methodological contribution applicable beyond ARC to any domain with structured input spaces
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]] — the induction/transduction complementarity finding has implications for hybrid neurosymbolic systems targeting formal domains
- [[themes/reasoning_and_planning|Reasoning and Planning]] — the unresolved theoretical gap between expected and observed induction-transduction convergence is a foundational question for meta-learning theory

## Key Concepts

- [[entities/abstraction-and-reasoning-corpus-arc|Abstraction and Reasoning Corpus (ARC)]]
- [[entities/conceptarc|ConceptARC]]
- [[entities/passk|pass@k]]
