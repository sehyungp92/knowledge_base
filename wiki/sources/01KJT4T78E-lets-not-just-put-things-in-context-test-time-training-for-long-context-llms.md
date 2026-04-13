---
type: source
title: 'Let''s (not) just put things in Context: Test-Time Training for Long-Context
  LLMs'
source_id: 01KJT4T78EVDXCWB98HK894F38
source_type: paper
authors:
- Rachit Bansal
- Aston Zhang
- Rishabh Tiwari
- Lovish Madaan
- Sai Surya Duvvuri
- Devvrit Khatri
- David Brandfonbrener
- David Alvarez-Melis
- Prajjwal Bhargava
- Mihir Sanjay Kale
- Samy Jelassi
published_at: '2025-12-15 00:00:00'
theme_ids:
- long_context_and_attention
- model_architecture
- post_training_methods
- reasoning_and_planning
- test_time_compute_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Let's (not) just put things in Context: Test-Time Training for Long-Context LLMs

**Authors:** Rachit Bansal, Aston Zhang, Rishabh Tiwari, Lovish Madaan, Sai Surya Duvvuri, Devvrit Khatri, David Brandfonbrener, David Alvarez-Melis, Prajjwal Bhargava, Mihir Sanjay Kale, Samy Jelassi
**Published:** 2025-12-15 00:00:00
**Type:** paper

## Analysis

# Let's (not) just put things in Context: Test-Time Training for Long-Context LLMs
2025-12-15 · paper · Rachit Bansal, Aston Zhang, Rishabh Tiwari, Lovish Madaan, Sai Surya Duvvuri et al. (11 total)
https://arxiv.org/pdf/2512.13898

---

### Motivation & Prior Limitations
- Long-context LLMs have expanded context windows to millions of tokens, but persistent failure modes remain: models miss clauses buried in lengthy documents, overlook function definitions deep in repositories, and fail to retrieve facts from prior turns even when the relevant content is explicitly present in context.
  - The "lost in the middle" effect is well-documented: position sensitivity causes single relevant spans to be overwhelmed by many distractors, and this persists across languages and document structures.
- Inference-time compute scaling strategies — chain-of-thought thinking tokens, best-of-n, self-consistency — were assumed to be a path toward overcoming long-context failures, but this paper demonstrates they are fundamentally insufficient for the retrieval problem.
  - Controlled experiments on two synthetic tasks (bug localization in code repositories and anomaly detection in transaction logs) show that thinking tokens improve performance for short contexts but exhibit clear diminishing returns as context length grows, asymptotically converging toward standard model performance at large T.
- The root cause is formalized as **score dilution**: a phenomenon inherent to static, finite-precision self-attention where distractor tokens inflate the softmax denominator, causing even a uniquely maximal logit to receive vanishingly small attention mass.
  - Formally, if at least m = cT distractors satisfy logits within O(1) of the needle, the needle's attention mass α_{i,j*} → 0 as T → ∞. Avoiding this requires a target–distractor logit margin that scales as Ω(log T) — a requirement that static attention weights cannot reliably meet.
- Thinking tokens are proven incapable of repairing the underlying retrieval failure: the fraction of needle signal any generated token can carry is bounded by its own attention mass on the needle, which is provably tiny under dilution conditions, so attending to thinking tokens cannot materially increase the final answer's effective margin.

---

### Proposed Approach
- The paper introduces **query-only test-time training (qTTT)**: a compute-frugal inference-time adaptation method that performs a single prefill to cache keys and values, then applies a small number of gradient updates exclusively to the query projection matrices W_Q across all attention layers, while holding all other parameters and the KV cache frozen.
  - This contrasts with full-parameter TTT, which is shown to be computationally infeasible for long contexts: a single full-parameter TTT step over a T-token context is FLOP-equivalent to generating approximately 1.2 × T decoding tokens, making it untenable at T ≈ 10^5.
  - The key architectural insight is that score dilution is a property of query-key similarity q_i^T k_j — the evidence (K, V) is fixed and correct, but the queries fail to concentrate attention on it. Updating only W_Q reshapes how queries attend to the already-cached evidence without re-encoding the context or growing the KV cache.
- The training objective is standard next-token prediction loss computed over short, randomly sampled contiguous spans x_{t:t+k} where k ≪ T, using the frozen KV cache to avoid repeated full-context passes.
  - This span-sampled approach means each gradient step costs O(k^2) rather than O(T^2), making the per-step compute proportional to span length rather than full context length.
- Theoretical grounding is provided via Proposition 3.1 and Lemma 3.2: a descent step on the query moves q_i toward the needle key k_{j*} and away from the attention-weighted centroid μ_i, provably increasing the target–distractor logit margin at each step, with the improvement largest precisely when attention is most diffuse — i.e., in the long-context regimes where score dilution is most severe.
- FLOP equivalence is established as: T_think ≈ 2 · N_qTTT · k (for long T, span k ≪ T), enabling fair matched-compute comparisons between thinking tokens and qTTT throughout all experiments.

---

### Results & Capabilities
- qTTT yields large, consistent performance improvements across all evaluated models and benchmarks, with average gains of **12.6 percentage points** for Qwen3-4B on LongBench-v2 subsets and **14.1 percentage points** on ZeroScrolls subsets relative to in-context-only baselines.
  - Under FLOP-matched budgets (8K thinking tokens ≈ 32 qTTT steps on spans of k=128), qTTT consistently and substantially outperforms both standard in-context learning and thinking-token baselines across all six LongBench-v2 categories and all ZeroScrolls datasets tested.
- The largest gains occur on retrieval-intensive and multi-hop reasoning tasks, directly validating the score dilution diagnosis.
  - For Qwen3-4B on LongBench-v2: Long Dialogue History improves from 30.8% to 43.6%; Multi-Document QA improves from 40.0% to 46.0%; Code Repositories scales especially strongly with model size, reaching 52.0% for Qwen3-8B.
  - On ZeroScrolls, multi-hop QA and comprehension tasks show gains that strengthen with model size; gains on summarization-style datasets (GovReport, QMSum, SQuALITY) are smaller and comparable to thinking tokens, indicating that when generation quality rather than retrieval is the bottleneck, attention reweighting yields limited returns.
- Improvements are consistent across model sizes (1.7B, 4B, 8B), with gains often scaling favorably with model size, suggesting qTTT is not an artifact of a particular parameter count.
- Attention mass analysis on synthetic tasks confirms the mechanism: qTTT preserves attention mass on target tokens as context length increases, while vanilla attention mass on targets drops sharply — directly empirically validating the margin improvement predicted by Lem

## Key Claims

1. Long-context LLMs can consume far more text than they can reliably use, exhibiting persistent failure modes even when relevant content is present in context.
2. Inference-time compute strategies such as generating thinking tokens show rapidly diminishing returns and fail at long context, asymptotically converging to standard model performance.
3. Score dilution is a fundamental limitation of static self-attention: when a constant fraction of distractor tokens are within O(1) logit of the target (needle), the attention budget cannot concentrate
4. Guaranteeing a fixed target attention mass against worst-case distractors requires a target-distractor logit gap that scales as Ω(log T) — a logarithmic margin requirement that static attention cannot
5. Thinking tokens cannot repair missing access to needle evidence: the fraction of needle signal any generated token can carry is at most its own attention mass on the needle, which is provably tiny und
6. Any successful inference-time strategy for long-context retrieval must change the similarity q⊤k (e.g., by updating queries) rather than sampling more tokens with unchanged parameters.
7. Full-parameter test-time training is computationally infeasible for long-context regimes: a single full-parameter TTT step over a T-token context is FLOP-equivalent to generating approximately 1.2×T d
8. Query-only TTT (qTTT) performs a single prefill to cache all key-value representations, then applies gradient updates exclusively to query projection matrices while reusing the frozen KV cache, keepin
9. qTTT's gradient updates on query projections provably increase the target-distractor logit margin: each gradient step moves the query toward the needle key and away from the attention-weighted mean of
10. qTTT margin improvements are largest precisely in long-context regimes where score dilution is most severe, making it especially well-suited to the failure mode it targets.

## Capabilities

- Query-only test-time training (qTTT) achieves 12.6 and 14.1 percentage point improvements for Qwen3-4B on LongBench-v2 and ZeroScrolls benchmarks by adapting only query projection matrices during inference while reusing a frozen KV cache, outperforming thinking-token scaling at matched FLOP budgets
- Test-time gradient updates restricted to query projection matrices provably increase the target–distractor attention margin in static self-attention, directly counteracting score dilution and improving long-context retrieval without modifying pre-training, architecture, or data
- qTTT is FLOP-competitive with thinking tokens for long contexts: updating query projections on short spans (k≪T) with N steps costs approximately 2·N·k equivalent decoding tokens, enabling it to be slotted into existing inference-time compute budgets while delivering superior gains on retrieval task

## Limitations

- Static self-attention suffers from provable score dilution: as context length T grows, a target token's attention probability mass vanishes because the softmax denominator accumulates competing distractor logits, requiring the target–distractor logit gap to scale as Ω(log T) to maintain retrieval — 
- Inference-time scaling via thinking tokens (chain-of-thought, o1-style) provably cannot overcome score dilution in long contexts — generated tokens use the same static attention, so any token that cannot attend to the needle carries at most an ε-fraction of needle signal and cannot amplify retrieval
- Full-parameter test-time training (updating all attention projections including K and V) is computationally infeasible for long-context inputs: one step over T=10^5 tokens is FLOP-equivalent to generating ~120K decoding tokens due to KV cache invalidation requiring fresh full-context forward–backwar
- qTTT gains are substantially smaller and comparable to thinking tokens for summarisation tasks (GovReport, QMSum, SQuALITY), indicating the method's improvements are retrieval-specific and do not generalise to generation-quality bottlenecks
- All qTTT evaluations are confined to Qwen3 models of 1.7B–8B parameters; generalisation to frontier-scale models (70B+), different pre-training recipes, or architectures other than standard dense transformers is entirely unverified
- A single fixed hyperparameter configuration (span length k=128, steps N=32) is evaluated; the optimal allocation across span size and update step count — and whether it varies substantially with context length or task type — is unknown
- qTTT introduces gradient computation overhead at inference time; the paper defers a comprehensive wall-clock latency comparison to an appendix rather than reporting it in the main body, signalling non-trivial latency costs that are not yet production-characterised
- The FLOP-matched compute comparison is limited to thinking tokens; qTTT is not evaluated against self-consistency or best-of-N sampling at matched budgets, leaving its relative efficiency across the full space of inference-time scaling strategies unknown

## Bottlenecks

- Score dilution in static transformer self-attention imposes a provable logarithmic margin requirement (Ω(log T)) that grows with context length, creating a structural barrier to reliable long-context retrieval that cannot be overcome by any decoding-based inference strategy without modifying attenti
- Thinking-token inference scaling is provably bounded by an ε-fraction ceiling on needle signal recovery in long contexts, creating a hard limit on how much decoding-based inference compute can improve retrieval-driven long-context tasks regardless of budget

## Breakthroughs

- Query-only test-time training (qTTT) — updating only query projection matrices with a few gradient steps while keeping a frozen KV cache — provably overcomes score dilution, is FLOP-competitive with thinking tokens, and delivers 12.6–14.1 pp gains on long-context benchmarks, establishing gradient-ba
- Theoretical proof that static self-attention suffers from score dilution with a provable Ω(log T) margin requirement, and that thinking tokens are structurally incapable of recovering buried evidence — establishing a formal theoretical ceiling on decoding-based inference scaling for long-context ret

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/in-context-learning-icl|In-context learning (ICL)]]
- [[entities/kv-cache|KV Cache]]
- [[entities/qwen3|Qwen3]]
