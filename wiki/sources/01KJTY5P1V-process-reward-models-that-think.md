---
type: source
title: Process Reward Models That Think
source_id: 01KJTY5P1V8G2N1PRSJQPJNCVS
source_type: paper
authors:
- Muhammad Khalifa
- Rishabh Agarwal
- Lajanugen Logeswaran
- Jaekyeom Kim
- Hao Peng
- Moontae Lee
- Honglak Lee
- Lu Wang
published_at: '2025-04-23 00:00:00'
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
# Process Reward Models That Think

**Authors:** Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, Honglak Lee, Lu Wang
**Published:** 2025-04-23 00:00:00
**Type:** paper

## Analysis

# Process Reward Models That Think
2025-04-23 · paper · Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng et al. (8 total)
https://arxiv.org/pdf/2504.16828

---

### Motivation & Prior Limitations
Discriminative process reward models (PRMs) are essential for test-time scaling but require prohibitively expensive step-level supervision to train effectively, limiting their practical deployment.
- Training a reasonably performing discriminative math PRM requires hundreds of thousands of step-level annotations (e.g., the PRM800K dataset contains ~712K step labels), which demands either extensive human annotation, gold step-by-step solutions, or compute-intensive Monte Carlo rollouts.
  - Discriminative PRMs use a classification head rather than the language-modeling head, making them expensive to train, limited in interpretability, and fixed in compute allocation — they cannot dynamically scale verification effort at inference time.

LLM-as-a-judge generative verification is a cheaper alternative but performs poorly as a process verifier due to format failures, overthinking, and infinite looping.
- Off-the-shelf reasoning models used as judges are highly sensitive to prompt wording (F1 shifts of 3–4 points with slight instruction changes), produce unextractable labels in up to 53% of cases for smaller models (e.g., R1-Distill-Qwen-1.5B), and exhibit a distinct spike in CoT length around 7K–8K tokens corresponding to overthinking and repetition loops.
  - These issues prevent LLM-as-a-judge from reliably terminating within a token budget, and prior generative verifiers (e.g., GenRM) rely on short CoTs of only a few hundred tokens, fundamentally capping their scalability.

Prior generative PRMs (e.g., GenRM) were limited to outcome-level verification via short chain-of-thought, preventing effective use of additional inference compute for step-level scoring.

---

### Proposed Approach
THINKPRM repurposes open-weight large reasoning models (LRMs) as verbalized, step-wise process reward models by fine-tuning them on a small set of high-quality synthetic verification chains-of-thought, enabling the verifier to "think" through each step before issuing a judgment.
- Unlike discriminative PRMs that use a classification head and binary cross-entropy on raw step labels, THINKPRM generates a long CoT inside a `<think>` block that individually critiques each solution step and emits a `\boxed{correct}` or `\boxed{incorrect}` label per step, leveraging the model's pre-existing reasoning capabilities rather than training them from scratch.
- The training pipeline uses rejection sampling fine-tuning (no RL or preference learning): QwQ-32B-Preview is prompted to produce verification chains over PRM800K problem-solution pairs, and only chains passing three filters are kept — correct output format, step-level agreement with gold PRM800K labels, and CoT length within a maximum budget to avoid overthinking. This yields ~1K chains (~8K step labels total).
  - Process-based filtering (requiring step-label agreement) is shown to outperform outcome-based filtering (used by GenRM), which retains chains based only on final answer correctness while ignoring intermediate step quality.
  - Fine-tuning is lightweight: QwQ-32B-Preview takes only 4.5 hours on a single A100 80GB GPU, and models as small as R1-Distill-Qwen-1.5B are successfully trained.

THINKPRM supports two orthogonal axes of verification compute scaling: parallel scaling (sampling K independent verification CoTs and averaging scores, denoted @K) and sequential scaling (triggering self-correction with a phrase like "Let's verify again" to elicit longer verification chains), neither of which is available to discriminative PRMs.

---

### Results & Capabilities
THINKPRM-14B, trained on only ~8K process labels, outperforms discriminative PRMs trained on ~712K process labels (100× more data) on ProcessBench, and surpasses LLM-as-a-judge using the same base model by a substantial margin.
- On the OlympiadBench and OmniMath subsets of ProcessBench, THINKPRM-14B achieves F1 scores of 87.3/85.7 versus 5.2/45.2 for LLM-as-a-judge (R1-Qwen-1.5B/14B respectively) and exceeds DiscPRM-14B trained on the full PRM800K.
  - The R1-Distill-Qwen-1.5B model shows the most dramatic improvement: fine-tuning raises F1 by over 70 points compared to the LLM-as-a-judge baseline on the same architecture.

On test-time scaling benchmarks, THINKPRM achieves superior best-of-N and guided beam search accuracy across MATH-500 and AIME 2024.
- THINKPRM-1.5B under guided beam search on MATH-500 surpasses RLHFFlow-Deepseek-PRM (a strong off-the-shelf PRM trained on more data and with a larger 8B model) by more than 7% across all beam sizes.
- Parallel scaling with THINKPRM-1.5B@4 boosts guided search accuracy on MATH-500 by more than 5 percentage points over the single-CoT version.

THINKPRM generalizes out-of-domain despite being trained only on math data, outperforming discriminative baselines on scientific reasoning (GPQA-Diamond physics subset) and code generation (LiveCodeBench).
- THINKPRM-14B outperforms DiscPRM-14B by 8% on GPQA-Physics and by 4.5% on LiveCodeBench, while Qwen2.5-7B-Math-PRM (a discriminative PRM trained on large-scale math process labels via Monte Carlo rollouts) struggles substantially on LiveCodeBench under domain shift.
- THINKPRM particularly excels on hard problems: on MATH-500 difficulty levels 3–5 and GPQA difficulty tiers 2–4, THINKPRM's improvement over DiscPRM is disproportionately large, reflecting that deeper reasoning is most valuable when verification is genuinely hard.

Sequential scaling of verifier compute via forced rechecking improves THINKPRM's F1 monotonically up to 32K tokens on ProcessBench, while LLM-as-a-judge's performance degrades after 16K tokens, and THINKPRM outperforms DiscPRM-14B by 15 F1 points at peak compute.

Training THINKPRM on long CoTs is critical: switching to compressed short CoTs (generated by 

## Key Claims

1. THINKPRM outperforms discriminative PRMs trained on approximately 100x more process labels on ProcessBench
2. THINKPRM achieves competitive performance using only 1% of the process labels required by discriminative PRMs
3. Training discriminative PRMs requires hundreds of thousands of step-level annotations for reasonably performing math PRMs
4. LLM-as-a-Judge verification quality is highly sensitive to instruction wording, with slight changes affecting F1-score by up to 3-4 points
5. LLM-as-a-Judge verification suffers from invalid judgments, overthinking, infinite looping, and models attempting to solve rather than verify problems
6. Inaccurate LLM-as-a-Judge verification CoTs spike sharply around 7K-8K tokens, while accurate CoTs tend to be shorter, typically under 3K tokens
7. Finetuning on 1K synthetic verification CoTs substantially improves verifier accuracy, with the 1.5B model gaining over 70 F1 points
8. Finetuning QwQ-32B-Preview to obtain THINKPRM takes only 4.5 hours on a single A100 80GB GPU
9. THINKPRM-1.5B surpasses off-the-shelf PRMs including RLHFFlow-Deepseek-PRM by more than 7% across all beam sizes on MATH-500 verifier-guided search
10. THINKPRM outperforms discriminative PRMs trained on full PRM800K by 8% on GPQA-Diamond and 4.5% on LiveCodeBench in out-of-domain evaluation

## Capabilities

- Generative process reward model (THINKPRM) trained with only 8K step labels achieves higher verification F1 than discriminative PRMs trained on 700K+ labels, by leveraging long chain-of-thought reasoning from pre-trained reasoning models
- Verification compute can be scaled both in parallel (averaging over K independent CoTs) and sequentially (extending token budget via self-correction triggers), with both strategies improving PRM accuracy beyond a fixed-compute baseline
- Generative PRM trained exclusively on math data generalizes out-of-domain to scientific reasoning (GPQA-physics) and code generation (LiveCodeBench) without any domain-specific fine-tuning, outperforming discriminative PRMs trained on substantially more data
- High-quality PRM training data can be generated via lightweight rejection sampling from a reasoning model (QwQ-32B-Preview) in ~4.5 hours on a single A100, filtering synthetic verification CoTs against gold step labels from PRM800K
- Generative PRM trained on short solutions with explicit step delimiters generalizes to verifying long-form reasoning traces with backtracking and self-correction (e.g., Qwen3-1.7B thinking-mode outputs) without explicit step boundary annotations
- Monte Carlo rollout-derived silver step labels are a viable substitute for manual process labels when training generative PRMs, yielding comparable verification performance at lower cost

## Limitations

- Generative PRM scores are systematically overconfident — token probabilities for 'yes'/'no' cluster near 0 or 1, making calibrated step-level confidence scores unreliable for downstream selection
- Step label interference: errors in early step judgments causally bias the model toward labelling subsequent steps as incorrect regardless of their actual correctness, propagating verification mistakes through the chain
- Generative PRM inference is significantly more expensive than discriminative PRMs because each step verification requires generating a full chain-of-thought (1K–5K tokens) rather than a forward pass with a classification head
- LLM-as-a-Judge verification quality is highly sensitive to instruction phrasing — small wording changes can shift F1-score by 3–4 points, making it unreliable in deployment without prompt engineering
- Off-the-shelf reasoning models used as LLM-as-a-Judge verifiers frequently produce non-terminating or unparseable outputs — infinite looping, overthinking, or attempting to solve rather than verify — with up to 53% invalid labels on the 1.5B model
- LLM-as-a-Judge verification performance degrades sharply beyond 16K tokens in sequential scaling — performance peaks and then declines, making it unable to benefit from additional sequential compute
- Discriminative PRMs are domain-brittle — they fail to generalize to out-of-domain tasks (e.g., code, science QA) even when trained on substantially more data, showing sharp accuracy drops at higher sampling budgets
- THINKPRM's performance advantage over self-consistency (majority voting) only materialises at high compute budgets — at low sampling budgets it is comparable, meaning the overhead of verification is only justified at scale
- Process-based filtering for synthetic training data requires gold step-level annotations or Monte Carlo rollouts — training with only outcome-based labels (which are cheaper to obtain) yields significantly weaker PRMs despite using more data
- THINKPRM's strong performance is restricted to structured, verifiable domains (math, science QA, code); the paper does not demonstrate applicability to open-ended or creative tasks where gold step labels cannot be obtained
- Parallel verifier scaling with THINKPRM (averaging K independent CoTs) provides only a slight advantage over sequential scaling, and neither mode yields large gains — suggesting verification compute scaling faces diminishing returns even for the best current method
- Training THINKPRM on only 1K short verification chains leaves performance on the table — scaling to 65K chains yields further improvements, indicating the 1K configuration used in main experiments is below the optimal data frontier

## Bottlenecks

- Generative PRM score miscalibration: token-probability-based confidence scores cluster near 0/1 extremes, blocking reliable use of PRM scores for fine-grained solution ranking in best-of-N and beam search
- Step label interference in autoregressive verification blocks accurate per-step scoring in multi-step solutions — early incorrect judgments causally corrupt subsequent step assessments, degrading overall PRM reliability on longer solutions
- Absence of process-level supervision for open-ended tasks blocks training of generalizable PRMs beyond math and code — the rejection-sampling pipeline requires either human step labels or Monte Carlo rollouts, neither of which scale to unverifiable domains

## Breakthroughs

- Generative PRMs fine-tuned with long chain-of-thought reasoning can match or surpass discriminative PRMs trained on two orders of magnitude more process labels, using only 8K step labels (1% of PRM800K)

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/omnimath|OmniMath]]
- [[entities/overthinking|Overthinking]]
- [[entities/prm800k|PRM800K]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
