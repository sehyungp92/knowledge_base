---
type: source
title: 'Smoothie: Label Free Language Model Routing'
source_id: 01KJV68FPFQGPKRY2YQEF12W1Z
source_type: paper
authors:
- Neel Guha
- Mayee F. Chen
- Trevor Chow
- Ishan S. Khare
- Christopher Ré
published_at: '2024-12-06 00:00:00'
theme_ids:
- adaptive_computation
- alignment_and_safety
- benchmark_design
- evaluation_and_benchmarks
- hallucination_and_reliability
- model_architecture
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Smoothie: Label-Free Language Model Routing

Smoothie introduces a weak supervision approach to LLM routing that eliminates the labeled data requirement blocking practical multi-model deployment. By treating model outputs as noisy voters over a latent true output and solving a closed-form graphical model over SentenceBERT embeddings, Smoothie recovers per-model quality scores without annotation, gradient descent, or auxiliary model training — and matches or exceeds supervised routing baselines on multi-task distributions.

**Authors:** Neel Guha, Mayee F. Chen, Trevor Chow, Ishan S. Khare, Christopher Ré
**Published:** 2024-12-06
**Type:** paper

---

## Expert Analysis

### Motivation & Prior Limitations

[[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]] research in LLM routing has converged on a practical bottleneck: every serious routing method requires labeled data. Engineers either train an auxiliary ranker on human-annotated preference data, or use a labeled validation set to identify the best-performing model on average. Neither path is available in zero-shot or rapidly-shifting deployment contexts — the settings where routing would be most valuable.

The field had also conflated two distinct sub-problems: estimating which LLM is best *globally* (population-level quality) versus identifying the best LLM *per sample* (instance-conditional quality). The latter is more valuable in multi-task deployments but harder to solve without labels. Even nearest-neighbor baselines like LABELED-KNN require 50+ labeled samples from a held-out set.

### Method

Smoothie reframes LLM routing as a weak supervision problem. Model outputs are treated as noisy voters over a latent true output; a latent variable graphical model is defined over SentenceBERT embeddings of those outputs. Each LLM's quality score θᵢ(x) is a canonical parameter controlling the Euclidean distance between its output embedding and an unobserved "true" embedding.

The model corresponds to a multivariate Gaussian with diagonal covariance, enabling a closed-form solution: θᵢ is recovered from pairwise distances between observable LLM embeddings via a triplet identity (Proposition 1). No gradient descent or training is required.

Three operational variants:

- **Smoothie-Global** — pools quality scores over the entire test set, yielding a constant per-LLM score. Useful for identifying the dominant model in an ensemble.
- **Smoothie-Local** — applies kernel smoothing via nearest neighbors in embedding space to produce sample-conditional scores, enabling genuine per-input routing. Uses n₀=1 nearest neighbor in practice.
- **Smoothie-Train** — precomputes quality scores from a fixed training set, eliminating the need to run all m models on each new test input and making runtime independent of test set size.

### Results

**Global routing.** Smoothie-Global's quality scores correlate with ground-truth LLM rankings at Spearman ρ=0.72 averaged across 7 NLG tasks and two ensemble sizes. It correctly identifies the best LLM in 9 of 14 single-task evaluations and 8 of 10 AlpacaEval ensemble trials. On AlpacaEval, it outperforms random selection by an average of 15 win-rate points and up to 27 points across trials — with no labeled data.

**Per-sample routing.** Smoothie-Local outperforms all baselines on multi-task routing, including labeled supervised methods. On DISTR-ACC (accuracy-measured tasks), it scores 58.7 at 3B and 75.0 at 7B, beating supervised PAIRRM (53.9 / 71.8) and LABELED-KNN (51.0 / 71.7) by up to 10 points. Critically, it outperforms BEST-MODEL — the single best fixed LLM — demonstrating genuine per-sample routing value rather than just identifying the dominant model.

**Prompt selection.** The quality-estimation mechanism generalises beyond routing: Smoothie-Global applied to prompt selection enables a 410M-parameter Pythia model to match or exceed a 6.9B-parameter model on E2E, improving over baseline prompt selection by up to 18 points.

**Computation.** Smoothie-Local requires ~2.14 seconds per 1,000 samples on 7B ensembles; Smoothie-Global under 0.03 seconds — both via closed-form arithmetic with no SGD.

---

## Capabilities

**Label-free ensemble routing** — [[themes/adaptive_computation|Adaptive Computation]]
Weak supervision graphical models over output embeddings select the best LLM per input without any labeled data, outperforming supervised baselines by up to 5 points accuracy and unsupervised baselines by up to 10 points. *(maturity: research only)*

**Unsupervised prompt selection**
Embedding-based quality scoring applied to prompt templates enables a 410M parameter model to match or outperform a 6.9B parameter model on generation tasks — a compute-efficient alternative to parameter scaling. *(maturity: research only)*

**Closed-form quality estimation**
Routing weights computed in under 2.14 seconds per 1,000 samples with no gradient-based training or labeled annotations. *(maturity: research only)*

---

## Limitations

These limitations are the most analytically significant part of the paper's contribution — the method's practicality is constrained by several structural assumptions:

**Independence assumption.** The diagonal covariance matrix treats LLM error vectors as independent. This ignores correlated failures when multiple models share pretraining data or architecture — a near-universal condition when routing across models fine-tuned from the same base. Consensus outputs from correlated generators may be systematically overconfident. *(severity: significant, trajectory: improving)*

**No cost-quality tradeoff.** Smoothie optimizes purely for output quality with no awareness of inference cost. It cannot economically route between cheap-but-adequate and expensive-but-better models — the central use case for real production deployments. *(severity: significant, trajectory: unclear)*

**O(n×m) inference requirement.** All m model generations per test sample are needed as input to the algorithm. The overhead of generating from every candidate LLM may negate cost savings from routing to cheaper models, particularly for large ensembles. *(severity: significant, trajectory: unclear)*

**Embedding sensitivity.** Performance varies inconsistently across task-ensemble combinations depending on the embedding model used, with no principled selection criteria. The method's reliance on SentenceBERT means it captures only certain aspects of semantic similarity. *(severity: significant, trajectory: improving)*

**Weak signal on open-ended instructions.** Smoothie-Global achieves only 0.46 Spearman rank correlation on AlpacaEval — near-random signal — compared to 0.94 on MixInstruct. The method's quality estimation degrades sharply for open-ended instruction-following where output diversity is high. *(severity: significant, trajectory: unclear)*

**Brittleness to neighborhood aggregation.** Smoothie-Local performance degrades monotonically as neighborhood size n₀ increases beyond 1 — the sample-conditional quality estimation is maximally local and brittle to any aggregation. *(severity: significant, trajectory: unclear)*

**Coverage gaps.** No validation for factual accuracy, code correctness, safety, or adversarial inputs. Routing correctness at the individual-sample level on abstract reasoning tasks (e.g., GSM8K) is unvalidated — only population-level LLM selection was tested. *(severity: significant, trajectory: unclear)*

**Smoothie-Train accuracy cost.** The inference-efficient variant using precomputed train-set generations underperforms Smoothie-Local across all tested configurations, creating an efficiency/accuracy tradeoff with no principled resolution. *(severity: minor, trajectory: unclear)*

---

## Landscape Contributions

### Bottleneck: Labeled Annotation Requirements for Routing

Smoothie directly addresses the primary practical barrier to deploying LLM ensemble routing in annotation-scarce settings: constructing quality-labeled datasets for each new task and model pool. By reducing this bottleneck via a closed-form unsupervised estimator, it operationalises a form of [[themes/adaptive_computation|adaptive computation]] that was previously inaccessible in zero-shot contexts. The bottleneck is partially resolved at the research level but the O(n×m) generation cost introduces a secondary bottleneck at scale. *(horizon: months)*

### Breakthrough: Unsupervised Routing Matching Supervised Methods

The result that a label-free graphical model over output embeddings matches or exceeds supervised routing methods is notable for the [[themes/evaluation_and_benchmarks|evaluation and benchmarks]] and [[themes/adaptive_computation|adaptive computation]] themes. It demonstrates that aggregate output consensus carries sufficient signal for quality estimation — a non-obvious result given the noise levels typical of LLM generation.

### Cross-Theme Implications

- **[[themes/model_architecture|Model Architecture]] × Adaptive Computation:** The prompt selection result suggests that systematic prompt routing can serve as a compute-efficient substitute for parameter scaling — a structural implication for how capability is allocated across inference budgets.
- **[[themes/hallucination_and_reliability|Hallucination and Reliability]]:** Smoothie's quality estimation is weakest precisely where reliability matters most — open-ended generation on AlpacaEval and factual accuracy tasks. The method's failure modes align with [[themes/hallucination_and_reliability|hallucination]] scenarios where output consensus is a poor proxy for ground truth.
- **[[themes/alignment_and_safety|Alignment and Safety]]:** No safety validation. A routing method that selects models based on output consensus could route toward confidently-generated but incorrect or harmful outputs, particularly given the independence assumption over correlated model failures.

---

## Open Questions

1. Can the diagonal covariance assumption be relaxed to account for correlated model families without losing the closed-form property?
2. Does embedding choice systematically interact with task type — and is there a principled way to select or learn embeddings for quality estimation?
3. Can cost-quality tradeoffs be incorporated into the graphical model's objective without requiring labeled cost annotations?
4. What is the minimum ensemble size at which Smoothie's signal exceeds noise? The triplet identity relies on having enough independent voters — the boundary is unexplored.
5. Does the prompt-selection result generalise to instruction-following tasks, or is it specific to structured generation tasks (E2E, summarization)?

---

## Related Themes

- [[themes/adaptive_computation|Adaptive Computation]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/hallucination_and_reliability|Hallucination and Reliability]]
- [[themes/model_architecture|Model Architecture]]
- [[themes/alignment_and_safety|Alignment and Safety]]
- [[themes/benchmark_design|Benchmark Design]]

## Key Concepts

- [[entities/alpacaeval|AlpacaEval]]
- [[entities/gsm8k|GSM8K]]
