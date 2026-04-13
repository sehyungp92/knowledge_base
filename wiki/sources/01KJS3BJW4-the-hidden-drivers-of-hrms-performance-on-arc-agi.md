---
type: source
title: The Hidden Drivers of HRM's Performance on ARC-AGI
source_id: 01KJS3BJW4NCGD892MGXKNGCKG
source_type: article
authors: []
published_at: None
theme_ids:
- adaptive_computation
- benchmark_design
- evaluation_and_benchmarks
- model_architecture
- reasoning_and_planning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Hidden Drivers of HRM's Performance on ARC-AGI

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# The Hidden Drivers of HRM's Performance on ARC-AGI
article
https://arcprize.org/blog/hrm-analysis

---

## Briefing

**ARC Prize's independent ablation study of the viral Hierarchical Reasoning Model (HRM) finds that the architecture's headline "brain-inspired hierarchical" design contributes minimally to its ARC-AGI-1 performance — the real drivers are iterative outer-loop refinement during training and task-specific memorization via gradient descent, making HRM fundamentally a test-time training approach rather than a novel reasoning architecture. This matters because it reframes HRM's 32% ARC-AGI-1 semi-private score (impressive for a 27M parameter model) as a validation of test-time compute and program synthesis via weight encoding, not hierarchical cognition — and reveals that the genuine architectural novelty was largely narrative.**

### Key Takeaways
1. **HRM's hierarchical H-L architecture is not the performance driver** — A standard transformer of equal parameter count (~27M) comes within ~5pp of HRM, with the gap narrowing at higher outer loop counts, suggesting the architecture provides marginal benefit over compute alone.
2. **The outer refinement loop is the essential mechanism** — Increasing from 1 to 2 outer loops yields a +13pp jump; going from 1 to 8 loops doubles public evaluation performance, making iterative refinement the single most impactful component.
3. **Training-time refinement matters far more than inference-time refinement** — A model trained with 16 refinement loops but evaluated with only 1 still outperforms a model trained with 1 loop by >15pp, indicating the loops teach the model to refine rather than just applying refinement at test time.
4. **HRM is fundamentally a zero-pretraining test-time training system** — Removing all cross-task transfer data (training set + ConceptARC) and training only on evaluation tasks drops performance from 41% to only 31%, revealing that most performance comes from memorizing specific evaluation task solutions.
5. **The puzzle_id embedding is a major architectural constraint** — The model encodes task identity into a learned embedding rather than few-shot context, meaning it can only operate on tasks seen during training — **a fundamental generalization barrier**.
6. **Data augmentation is critical but subject to diminishing returns** — 300 augmentations achieves near-maximum performance; even 30 augmentations (3% of paper's 1,000) comes within 4pp, showing the paper overstated augmentation requirements.
7. **Training-time augmentation dominates inference-time augmentation** — Models trained with more augmentations suffer much smaller performance drops when inference pool is reduced, confirming that variety during training matters more than majority voting breadth.
8. **HRM scores 32% on ARC-AGI-1 semi-private, 2% on ARC-AGI-2** — The 9pp drop from claimed 41% is on the high end of normal variation but not indicative of overfitting; the 2% on ARC-AGI-2 is non-zero signal but not meaningful progress.
9. **HRM converges with Liao & Gu's "ARC-AGI without pretraining"** — Both use gradient descent on demonstration pairs to implicitly encode task programs into model weights, making HRM a transductive program synthesis substrate rather than a general reasoner.
10. **Adaptive Computational Time (ACT) provides modest benefit** — ACT does reduce actual refinement steps per task during training, but its performance advantage over a fixed 16-loop run is only a few percentage points.
11. **The outer loop mechanism parallels Universal Transformers** — HRM's recurrent outer loop plus ACT-style halting is structurally similar to the Universal Transformer architecture, raising questions about the degree of architectural novelty claimed.
12. **Implicit programs will likely not generalize** — Because HRM is purely transductive and the refinement steps cannot be unrolled into an explicit program, the authors speculate generalization beyond training data is limited.

---

### Verification Methodology and Score Context

- ARC Prize ran HRM against the ARC-AGI-1 and ARC-AGI-2 semi-private evaluation sets, which are hold-out datasets not publicly available for training, providing cleaner generalization signal than public evaluation scores.
  - Eligibility requirements: open-source code, cost under $10K, runtime under 12 hours.
  - ARC-AGI-1 semi-private score: **32%**, runtime 9h 16m, cost $148.50 ($1.48/task).
  - ARC-AGI-2 semi-private score: **2%**, runtime 12h 35m, cost $201 ($1.68/task).
- The 9pp drop from claimed 41% (public evaluation) to 32% (semi-private) is notable but not disqualifying.
  - Public and semi-private ARC-AGI-1 sets are not difficulty-calibrated, so variation is expected.
  - A true overfitting collapse would have produced ~10% or less; the sustained 32% confirms genuine learning signal.
  - **The result confirms something real is happening — but the ablations reveal what that something actually is.**
- ARC-AGI-2 performance of 2% is classified as non-material progress.
  - ARC-AGI-2 public and semi-private sets are difficulty-calibrated, so in-principle scores should align.
  - The near-zero result confirms ARC-AGI-2 remains an unsolved challenge for this class of approach.
- The relatively high dollar cost ($148-$201) reflects that HRM couples training and inference into a single run.
  - Authors indicated they are working to decouple training and inference for the ARC Prize 2025 Kaggle competition.

---

### HRM Architecture: What It Claims vs. What It Does

- HRM is a 27M parameter model marketed as brain-inspired, drawing on the hierarchical and multi-timescale processing of human cognition.
  - Two coupled recurrent modules: **H (slow planner)** and **L (fast worker)**, sharing a hidden state rather than producing separate outputs.
  - The model alternates between high-level planning (H) and detail execution (L) until internal state self-consistency triggers a halt.
- The outer loop is layered around the H-L syst

## Key Claims

1. HRM scored 41% on ARC-AGI-1 with only 1,000 training tasks and a 27M parameter model, as claimed in the original paper.
2. ARC Prize independently verified HRM at 32% on the ARC-AGI-1 Semi-Private evaluation set.
3. HRM scored only 2% on the ARC-AGI-2 Semi-Private evaluation set, which ARC Prize does not consider material progress.
4. The hierarchical dual-module (H-L) architecture of HRM had minimal performance impact compared to a similarly sized standard transformer.
5. The outer loop iterative refinement process was the primary driver of HRM's performance, especially when used at training time.
6. Cross-task transfer learning contributes minimally to HRM's performance; most performance derives from memorizing solutions to evaluation tasks seen at training time.
7. Only 300 augmentations are needed for near-maximum HRM performance, not the 1,000 reported in the paper.
8. A standard transformer of the same parameter count (~27M) comes within approximately 5 percentage points of HRM performance without hyperparameter optimization.
9. Adding a single refinement loop step increases ARC-AGI performance by 13 percentage points; going from 1 to 8 outer refinement loops doubles performance on the Public Evaluation set.
10. Training with refinement loops is more important than using refinement at inference time; training with 16 loops improves single-loop inference performance by more than 15 percentage points.

## Capabilities

- 27M parameter model achieves 32% on ARC-AGI-1 Semi-Private dataset using test-time training and iterative outer-loop refinement, without large-scale pre-training
- Iterative outer-loop refinement enabling a model to repeatedly revise predictions with adaptive halting, achieving substantial performance gains on abstract reasoning tasks
- Zero-pretraining test-time training via gradient descent on task demonstration pairs, encoding task-specific transformations into model weights at evaluation time
- Learned adaptive halting (ACT) controlling per-task compute allocation during iterative refinement, reducing unnecessary refinement steps
- Task augmentation via geometric transformations (rotations, flips, color swaps) combined with majority voting over de-augmented predictions, improving abstract reasoning performance with diminishing returns beyond 300 augmentations

## Limitations

- HRM can only be applied to tasks with puzzle_ids seen during training — the model cannot generalise to entirely new tasks at inference time without retraining
- ARC-AGI-2 performance remains negligible at 2% — approaches effective on ARC-AGI-1 (transduction, test-time memorisation) do not transfer to the harder benchmark
- The claimed bio-inspired hierarchical (H-L) architecture contributes minimally to ARC-AGI performance — a standard transformer of equal parameter count achieves within ~5pp without hyperparameter optimisation
- HRM's performance is primarily driven by memorising solutions to the specific evaluation tasks seen during training, not by cross-task generalisation or transfer learning
- HRM is purely transductive — the underlying transformation program remains implicit and cannot be extracted or verified, likely preventing out-of-distribution generalisation
- Training and inference are coupled in a single run, making HRM expensive to deploy ($148.50 / 9h16m per evaluation) and preventing independent scaling of each phase
- Inference-time task augmentation provides limited additional gains beyond what training-time augmentation already achieves; majority voting pool size is a weak lever
- The H-L hierarchical iteration counts are brittle — deviating from the empirically tuned baseline (L=2, H=2) degrades performance in both directions
- Performance drop from public to semi-private evaluation set (-9pp) is on the high side of normal variation, indicating partial overfitting to the public evaluation distribution
- The puzzle_id embedding approach requires complete retraining to handle any change in task set or augmentation strategy, preventing incremental updates or continual learning
- HRM's few-shot context (seeing other input-output examples of a task) is absent — the model receives only input and puzzle_id, losing the multi-shot signal that benefits larger models on general ARC-like datasets

## Bottlenecks

- ARC-AGI-2 remains essentially unsolved by test-time training and transduction-based approaches, blocking demonstration of genuine fluid abstract reasoning in AI systems
- Transductive reasoning approaches encode implicit programs that cannot be extracted or generalised, blocking verifiable and reusable program synthesis from few-shot abstract reasoning demonstrations
- Test-time training requires gradient updates during inference, coupling training and inference into a single expensive run and blocking practical deployment at scale

## Breakthroughs

- Iterative outer-loop refinement during training — not bio-inspired architecture — is the dominant driver of HRM's ARC-AGI performance, with a standard transformer achieving comparable results when the refinement loop is preserved
- Training with many refinement loops improves single-pass inference performance by >15pp, demonstrating that training-time iterative refinement is more impactful than inference-time compute scaling for abstract reasoning

## Themes

- [[themes/adaptive_computation|adaptive_computation]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/model_architecture|model_architecture]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/arc-agi-1|ARC-AGI-1]]
- [[entities/conceptarc|ConceptARC]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/universal-transformer|Universal Transformer]]
