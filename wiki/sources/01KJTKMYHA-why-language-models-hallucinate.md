---
type: source
title: Why Language Models Hallucinate
source_id: 01KJTKMYHA551GS78K7M808D1V
source_type: paper
authors:
- Adam Tauman Kalai
- Ofir Nachum
- Santosh S. Vempala
- Edwin Zhang
published_at: '2025-09-04 00:00:00'
theme_ids:
- alignment_and_safety
- alignment_methods
- benchmark_design
- evaluation_and_benchmarks
- hallucination_and_reliability
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Why Language Models Hallucinate

**Authors:** Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, Edwin Zhang
**Published:** 2025-09-04 00:00:00
**Type:** paper

## Analysis

# Why Language Models Hallucinate
2025-09-04 00:00:00 · paper · Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, Edwin Zhang
https://arxiv.org/pdf/2509.04664

---

### Motivation & Prior Limitations
- Hallucinations persist in state-of-the-art language models despite extensive mitigation work, and prior explanations have treated them as somewhat mysterious or attributed them to a patchwork of unrelated causes without a unifying statistical account.
  - DeepSeek-V3 (600B parameters) returned three different incorrect birthdates across three attempts, even when explicitly asked to respond only if certain; GPT-4o, DeepSeek, and Llama-4 all fabricated distinct incorrect dissertation titles and years for the same query.
  - Existing hallucination benchmarks have "struggled to gain traction within the AI community" (2025 AI Index Report), indicating the field lacks consensus on how to measure or penalize the problem.
- Binary evaluation metrics — accuracy and pass-rate — dominate leaderboards and systematically reward confident guessing over honest uncertainty, yet prior work has sought to address this by adding new hallucination-specific evaluations rather than modifying the primary evaluations that drive model development.
  - A meta-analysis of ten major benchmarks (GPQA, MMLU-Pro, SWE-bench, HLE, etc.) finds that all use binary grading and none grant any credit for abstention; WildBench partially rewards IDK but its rubric may still score hallucinated "fair" responses above honest abstentions.

---

### Proposed Approach
- The paper provides a formal statistical account of hallucination through a novel reduction from unsupervised learning (pretraining as density estimation) to supervised learning (binary classification), unifying the origin of pretraining errors with decades of misclassification theory.
  - The Is-It-Valid (IIV) binary classification problem is defined: given labeled examples of valid (+) and erroneous (−) outputs, any language model induces an IIV classifier by thresholding its output probability at 1/|E|. Theorem 1 establishes that the generative error rate satisfies `err ≥ 2·erriiv − max_c|Vc|/min_c|Ec| − δ`, where δ measures miscalibration. This means generative hallucination rates are lower-bounded by twice the classification error rate on the IIV problem.
  - The reduction is architecture-agnostic: it does not rely on next-token prediction or Transformer structure, and applies equally to RAG, reasoning, and search-augmented models.
- Three principal statistical drivers of pretraining errors are identified and formalized: (1) arbitrary-fact hallucinations driven by epistemic uncertainty when facts have no learnable pattern; (2) poor-model hallucinations when the model family cannot represent the required concept; and (3) GIGO effects from noisy training corpora.
  - For arbitrary facts, Theorem 2 shows the hallucination rate is lower-bounded by the singleton rate (fraction of training facts appearing exactly once), recovering and extending the Good-Turing missing-mass connection from Kalai & Vempala (2024) while now incorporating prompts and IDK responses.
  - For poor models, Theorem 3 shows that for C-choice multiple-choice with a single valid answer, `err ≥ 2(1 − 1/C) · opt(G)`, where opt(G) is the best achievable misclassification rate in the model family; a trigram model over two prompts differing only in pronoun is proven to have error rate ≥ 1/2.
- For post-training persistence, the paper offers a socio-technical explanation: Observation 1 proves formally that for any distribution over binary graders, the optimal response is never to abstain — meaning binary evaluation structurally selects for overconfident guessing over honest uncertainty.
  - The proposed mitigation is not a new hallucination benchmark but modification of existing primary evaluations to include explicit confidence targets: "Answer only if you are > t confident, since mistakes are penalized t/(1−t) points." This reframes calibration as behavioral calibration — whether a model outputs IDK precisely when its correctness probability falls below t — which is auditable without requiring probabilistic confidence outputs.

---

### Results & Capabilities
- The lower bound `err ≥ 2·erriiv − |V|/|E| − δ` is shown to be relatively tight: for large |E| and small δ, erriiv can approach 1/2 while err ≤ 1, and the constant 2 cannot be substantially improved.
  - For birthday facts, |Ec| = 364 (364 wrong dates for each person), so the |V|/|E| correction term is negligible and the bound directly implies high hallucination rates for singleton-rate facts.
- Calibration (small δ) is shown to be a natural consequence of standard cross-entropy pretraining: if δ ≠ 0, rescaling predicted probabilities by some factor s ≠ 1 would reduce the loss, contradicting local optimality. Empirical GPT-4 calibration histograms (OpenAI 2023) confirm base models are well-calibrated, while post-trained models deviate — consistent with the theory.
  - This yields a corollary: language models that do not hallucinate cannot simultaneously be calibrated under cross-entropy, since avoiding errors requires δ to be large.
- Reasoning models (DeepSeek-R1) correctly count letters in DEEPSEEK by spelling out a 377-step chain-of-thought, while DeepSeek-V3 returns "2" or "3" across ten trials — attributed to poor model capacity rather than missing knowledge, since R1 and V3 share similar training data.
- The meta-evaluation of ten benchmarks finds that all ten use binary grading and none award IDK credit (with WildBench as a partial exception that may still penalize abstention), supporting the claim that primary evaluations constitute an "epidemic" of hallucination reinforcement.

---

### Implications
- The dominant explanation for why hallucinations survive post-training is misaligned evaluation incentives rather than fundamental model incapacity: any model that correctly signals uncertainty will be outranked on leaderboards by a model th

## Key Claims

1. Language models hallucinate because training and evaluation procedures reward guessing over acknowledging uncertainty.
2. Hallucinations originate as errors in binary classification: if incorrect statements cannot be distinguished from facts, hallucinations in pretrained language models arise through natural statistical 
3. Hallucinations persist in state-of-the-art language models as of 2025.
4. DeepSeek-V3 (600B parameters) returned three different incorrect birthdates when asked for Adam Kalai's birthday despite being told to respond only if certain.
5. The generative error rate of a base model is lower-bounded by approximately twice its IIV (Is-It-Valid) misclassification rate.
6. The hallucination rate after pretraining is at least the fraction of training facts that appear exactly once (the singleton rate).
7. Post-training typically deviates from cross-entropy in favor of reinforcement learning, causing post-trained models to be less calibrated than base models.
8. For any base model trained with the standard cross-entropy objective, the calibration deviation term δ is typically small, implying that calibration and hence errors naturally arise from pretraining.
9. A non-hallucinating model could be constructed that answers only a fixed set of questions and otherwise outputs IDK; hallucinations are inevitable only for base models that generalize.
10. Language models that do not err must not be calibrated (δ must be large), establishing a tension between calibration and error-freedom.

## Capabilities

- Reasoning models (e.g., DeepSeek-R1) reliably solve character-level tasks like letter counting by explicitly spelling out tokens step-by-step in chain-of-thought, overcoming a structural limitation of non-reasoning base models
- Pretrained base language models are well-calibrated as a natural byproduct of cross-entropy loss minimisation — without any explicit calibration training, predicted probabilities align with empirical truth rates
- Internal model activations and output consistency across semantically equivalent queries encode predictive signals about factual accuracy, enabling hallucination detection without external retrieval
- Behavioral calibration — where a model formulates responses only when confidence exceeds an explicit threshold — can be objectively audited by comparing accuracy and abstention rates across stated confidence thresholds

## Limitations

- State-of-the-art LLMs hallucinate arbitrary facts even when explicitly instructed to respond only if they know the answer — instruction-level suppression of guessing is insufficient against the underlying statistical pressure
- Intrinsic hallucinations — contradicting information present in the user's own prompt — persist across all state-of-the-art models including DeepSeek-V3, Meta AI, and Claude 3.7 Sonnet on basic letter-counting tasks
- Hallucination rate in base models has a provable theoretical lower bound equal to the training-data singleton rate — if N% of facts appear exactly once in training data, at least N% of base-model responses about those facts will be wrong
- Post-training (RLHF, RLAIF, DPO) destroys the calibration achieved during pretraining — post-trained models become systematically overconfident relative to base models even as they are intended to become more accurate
- RAG and search augmentation do not resolve the hallucination problem because binary grading still incentivises guessing whenever search fails to return a confident answer — the evaluation regime, not the retrieval gap, is the root cause
- Fine-tuning on novel information causes a temporary decrease in hallucination rates that later reverses — no stable post-training method exists for reducing hallucination on freshly injected facts
- Virtually all primary AI evaluation benchmarks (GPQA, MMLU-Pro, MATH, SWE-bench, HLE, BBH, IFEval, MuSR) use binary grading that awards zero credit to abstentions — creating a mathematical proof that guessing always dominates honest uncertainty expression
- Hallucination benchmarks have systematically failed to gain adoption — the research community cannot operationalise its own diagnostic tools, revealing a collective-action failure that compounds the evaluation misalignment problem
- Under the cross-entropy objective, calibration and hallucination are mathematically inseparable — a model that avoids hallucinating entirely must be miscalibrated; a well-calibrated model must hallucinate on uncertain facts
- LLMs produce inconsistent answers across repeated trials on the same question, revealing latent uncertainty they do not surface — the inconsistency is a diagnostic signal of epistemic uncertainty that models fail to communicate
- No AI system — regardless of capability — can avoid hallucination on computationally hard problems (NP-hard, undecidable); this is a permanent constraint not addressable by scaling or better training
- The proposed fix (adding confidence targets to existing benchmarks) faces an adoption coordination problem — no empirical evidence is provided that labs would adopt it, and the paper acknowledges it requires socio-technical change, not just technical change

## Bottlenecks

- Binary grading dominates all major AI benchmarks (GPQA, MMLU-Pro, MATH, SWE-bench, HLE, etc.), making confident hallucination mathematically optimal and blocking development of AI systems that honestly express uncertainty — changing these requires industry-wide coordination that has not materialised
- Training data singleton rate creates an irreducible theoretical lower bound on base model hallucination — facts that appear exactly once cannot be learned reliably, and this fraction of training data directly translates into a minimum hallucination rate
- Post-training (RLHF/DPO/RLAIF) is evaluated against metrics that reward the exact overconfidence it should suppress — creating a pipeline where every refinement step optimises toward hallucination while appearing to reduce it

## Breakthroughs

- Formal mathematical proof connecting generative hallucination rate to binary classification misclassification — the IIV (Is-It-Valid) reduction shows hallucination rate ≥ 2× IIV misclassification rate, grounding hallucination in four decades of learning theory
- Formal proof that adding hallucination-specific evaluations is insufficient when primary benchmarks reward hallucination — a model that always guesses confidently mathematically dominates a calibrated honest model under binary grading, making evaluation reform of existing benchmarks a prerequisite f

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/alignment_methods|alignment_methods]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]

## Key Concepts

- [[entities/gpqa|GPQA]]
- [[entities/hle-humanitys-last-exam|HLE (Humanity's Last Exam)]]
