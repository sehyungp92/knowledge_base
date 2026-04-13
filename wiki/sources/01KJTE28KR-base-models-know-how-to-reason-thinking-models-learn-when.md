---
type: source
title: Base Models Know How to Reason, Thinking Models Learn When
source_id: 01KJTE28KR6AJ5Q8T6ZD9TTZ9R
source_type: paper
authors:
- Constantin Venhoff
- Iván Arcuschin
- Philip Torr
- Arthur Conmy
- Neel Nanda
published_at: '2025-10-08 00:00:00'
theme_ids:
- chain_of_thought
- interpretability
- mechanistic_interpretability
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 14
tags: []
---
# Base Models Know How to Reason, Thinking Models Learn When

**Authors:** Constantin Venhoff, Iván Arcuschin, Philip Torr, Arthur Conmy, Neel Nanda
**Published:** 2025-10-08 00:00:00
**Type:** paper

## Analysis

# Base Models Know How to Reason, Thinking Models Learn When
2025-10-08 · paper · Constantin Venhoff, Iván Arcuschin, Philip Torr, Arthur Conmy, Neel Nanda
https://arxiv.org/pdf/2510.07364

---

### Motivation & Prior Limitations
The fundamental question of *why* thinking models outperform base models remains unresolved despite consistent benchmark gains, with competing hypotheses offering contradictory explanations. Prior hypotheses split across four camps: thinking models acquire entirely new capabilities via specialized training (Gandhi et al., 2025); RL teaches better reasoning structure (Marjanović et al., 2025); RL repurposes pre-existing base model representations for new mechanisms (Ward et al., 2025a); or additional inference time simply allows more computation (Zhao et al., 2025; Wang et al., 2025). Existing taxonomies of reasoning behaviors in thinking models relied on manual inspection of reasoning traces, which is inherently subjective and may overlook subtle or distributed reasoning patterns that an automated, assumption-free method would surface.

---

### Proposed Approach
The paper proposes a hybrid model that steers a frozen base model with reasoning-specific activation vectors at precisely the token positions where a thinking model would deploy a corresponding reasoning mechanism — without any weight updates to the base model. At each token position, a "thinking model activation classifier" monitors the parallel rollout of a target thinking model and identifies which reasoning behavior (e.g., backtracking, arithmetic, problem restatement) is about to be executed; the corresponding steering vector is then injected into the base model's activations. To derive the taxonomy of reasoning behaviors needed to build these vectors, the authors develop an unsupervised, bottom-up clustering methodology using Top-K Sparse Autoencoders (SAEs) applied to sentence-level activations, deliberately avoiding manually imposed or LLM-derived category labels so that the taxonomy remains unbiased. This hybrid architecture is evaluated across three base models and four thinking models (including distillation-trained DeepSeek-R1-Distill series and RLVR-trained QwQ-32B) on GSM8K and MATH500.

---

### Results & Capabilities
The hybrid model recovers up to 91% of the performance gap between base and thinking models on GSM8K and MATH500 without any weight updates, intervening on only 12% of token positions. The result holds across models trained by two different paradigms — distillation (DeepSeek-R1-Distill) and direct RLVR (QwQ-32B) — indicating that the mechanism generalizes beyond a single training recipe. The narrow intervention footprint (12% of tokens) demonstrates that the vast majority of reasoning-critical capability is already latent in the base model and requires only targeted, sparse activation rather than wholesale behavioral change. Qualitatively, the steered base model reproduces complete thinking-model reasoning chains, including backtracking and structured arithmetic steps, from a model that was never trained to produce them.

---

### Implications
These results support a reframing of the roles of pre-training and post-training: pre-training is where models acquire the *substance* of reasoning, while RLVR post-training teaches *when* to deploy that substance in an efficient, ordered sequence. If RL primarily instills temporal scheduling of pre-existing skills rather than creating new skills, future training pipelines could potentially separate capability acquisition (pre-training) from deployment scheduling (a lightweight post-training stage), yielding more sample-efficient paths to reasoning models. The work also provides a causal, empirical methodology for mechanistic interpretability of reasoning — directly invoking specific mechanisms via steering vectors and measuring downstream task performance — which offers a more principled alternative to behavioral analysis of reasoning traces. The unsupervised SAE-based taxonomy contributes a reusable, bottom-up framework for characterizing reasoning behaviors across model families without analyst-imposed assumptions.

---

### Remaining Limitations & Next Steps
The source text provided is a partial excerpt ending mid-section (Section 2.1), so the full set of author-stated limitations and ablations cannot be assessed from the available text. The evaluation benchmarks are limited to two mathematical reasoning datasets (GSM8K and MATH500), leaving open whether the findings generalize to other reasoning domains such as code, logic, or multi-hop factual reasoning. The hybrid model requires access to a parallel target thinking model at inference time to run the activation classifier, which doubles the inference cost compared to running either model alone — a practical overhead not discussed in the available text. The approach steers 12% of tokens to recover 91% of the gap, implying a residual ~9% performance difference that the intervention does not close, and the source of that gap is not explained in the excerpt.

## Key Claims

1. Thinking models significantly outperform their base counterparts on challenging reasoning benchmarks.
2. Base models already possess the fundamental reasoning capabilities; thinking models learn when to deploy these capabilities in a structured sequence.
3. A hybrid model that applies steering vectors to a base model at the right token positions recovers up to 91% of the performance gap between base and thinking models without any weight updates.
4. The hybrid approach requires steering only 12% of tokens to achieve near thinking-model-level reasoning performance.
5. Reinforcement learning with verifiable rewards (RLVR) used to train thinking models primarily teaches when to activate pre-existing skills rather than how to execute those skills.
6. Pre-training is when models acquire most of their reasoning mechanisms, and post-training teaches efficient deployment of these mechanisms at the right time.
7. Prior work has relied on manual inspection of reasoning traces to identify mechanisms in thinking models, which is inherently subjective and may overlook subtle or distributed patterns.
8. The paper introduces an unsupervised, bottom-up methodology using Top-K Sparse Autoencoders to discover human-interpretable reasoning mechanisms in thinking models without pre-existing assumptions.
9. Top-K SAEs enforce sparsity by keeping only the K largest magnitude components of the latent representation, creating a more interpretable and computationally efficient decomposition.
10. The steered base model approach is evaluated across diverse architectures and parameter scales, including models trained with distillation and models trained directly with RLVR.

## Capabilities

- Activation steering vectors applied to only 12% of tokens in a base model can recover up to 91% of the performance gap between base and thinking models on math benchmarks, without any weight updates
- Unsupervised sparse autoencoder (Top-K SAE) clustering over sentence-level activations can discover a human-interpretable taxonomy of reasoning mechanisms in thinking models without manual labelling or LLM-derived assumptions
- Per-category steering vectors derived from thinking model activations can reliably trigger specific reasoning behaviours (e.g. backtracking, problem restatement, arithmetic) in base models on demand
- A 'thinking model activation classifier' trained on thinking model rollouts can predict which reasoning mechanism category should be applied at each token position, enabling automated reasoning orchestration

## Limitations

- The hybrid steering approach requires running a full thinking model in parallel at every token position to classify which reasoning mechanism to apply — roughly doubling inference cost versus a standalone thinking model
- All empirical results are confined to mathematical reasoning benchmarks (GSM8K and MATH500) — generalisability to language, coding, science, or open-domain reasoning is entirely undemonstrated
- Up to 9% of the performance gap between base and thinking models cannot be recovered through steering alone, indicating some capabilities or behaviours are genuinely acquired during post-training rather than merely elicited
- The reasoning mechanism taxonomy derived from SAE clustering is constructed only from thinking model chains of thought on math problems — no validation that the taxonomy generalises across task types or model families beyond the tested set
- The finding that post-training teaches deployment timing rather than new capabilities is demonstrated only for models trained with RLVR and distillation — whether this holds for models trained with RLHF, SFT, or constitutional AI is not assessed
- The steering approach is only validated on reasoning steps that match the discovered taxonomy categories — the 88% of tokens that are not steered are implicitly assumed to be handled correctly by the base model without any analysis
- The paper is under review at ICLR 2026 — all claims are preliminary and have not yet undergone peer review

## Bottlenecks

- Mechanistic understanding of what RLVR training actually modifies in model weights is absent — current training recipes cannot be redesigned for efficiency without knowing whether they are teaching deployment timing, new capabilities, or both
- No general method exists to transfer per-task steering vectors across domains — the steering vectors must be derived from thinking model activations on the specific task distribution, blocking domain-agnostic reasoning elicitation from base models

## Breakthroughs

- Causal empirical evidence that base models already possess all fundamental reasoning mechanisms required for thinking-model-level performance — RLVR post-training teaches deployment timing, not new capabilities

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/interpretability|interpretability]]
- [[themes/mechanistic_interpretability|mechanistic_interpretability]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/deepseek-r1-distill|DeepSeek-R1-Distill]]
- [[entities/gsm8k|GSM8K]]
- [[entities/math500|MATH500]]
- [[entities/qwq-32b|QwQ-32B]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
