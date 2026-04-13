---
type: source
title: 'Sleep-time Compute: Beyond Inference Scaling at Test-time'
source_id: 01KJTZ9VS7CEDEQX2QSWQED206
source_type: paper
authors:
- Kevin Lin
- Charlie Snell
- Yu Wang
- Charles Packer
- Sarah Wooders
- Ion Stoica
- Joseph E. Gonzalez
published_at: '2025-04-17 00:00:00'
theme_ids:
- context_engineering
- knowledge_and_memory
- post_training_methods
- reasoning_and_planning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Sleep-time Compute: Beyond Inference Scaling at Test-time

**Authors:** Kevin Lin, Charlie Snell, Yu Wang, Charles Packer, Sarah Wooders, Ion Stoica, Joseph E. Gonzalez
**Published:** 2025-04-17 00:00:00
**Type:** paper

## Analysis

# Sleep-time Compute: Beyond Inference Scaling at Test-time
2025-04-17 · paper · Kevin Lin, Charlie Snell, Yu Wang, Charles Packer, Sarah Wooders et al. (7 total)
https://arxiv.org/pdf/2504.13171

---

### Motivation & Prior Limitations
- Test-time compute scaling has become a dominant strategy for improving LLM performance on hard reasoning tasks, but it imposes severe latency and cost penalties — potentially minutes of wait time and tens of dollars per query for frontier reasoning models like o1-pro.
  - The fundamental inefficiency is that standard test-time scaling treats every query as stateless: context and query arrive together, so the model re-derives the same inferences about a shared context on every independent query, even when that context has been available for some time.
- Many real-world LLM deployments are inherently stateful — document QA, coding assistants operating on a shared repository, multi-turn conversational agents — meaning context exists and is stable long before any user query arrives, yet current paradigms leave the model idle during this window.
  - Both sequential test-time scaling (extended chain-of-thought, budget forcing) and parallel test-time scaling (best-of-N, pass@k) assume context is only available at query time, making them structurally unable to exploit this pre-query idle period.

---

### Proposed Approach
- Sleep-time compute is a new inference dimension that decouples reasoning about context from reasoning about a specific query: during the idle period before a user query arrives, the model processes the raw context `c` to produce a richer re-represented context `c′`, which is then provided at test-time alongside the query, allowing the model to answer with far less additional reasoning.
  - Formally, `S(c) → c′` at sleep-time (where `S` can be any test-time scaling technique applied offline), followed by `T_b(q, c′) → a` at test-time with a much smaller budget `b << B` — the key insight is that the bulk of context-dependent inference is amortized to the pre-query phase.
  - Unlike speculative decoding, which verifies and discards generated tokens, sleep-time compute unconditionally incorporates the pre-computed context `c′` into the test-time prompt regardless of what query eventually arrives, making it a form of natural-language representation learning over tokens rather than a latency trick.
- When multiple queries share the same context, a single sleep-time pass produces `c′` that is reused across all queries, amortizing the sleep-time compute cost across the query workload — directly analogous to pre-fetching and data cubes from systems literature, now applied to LLM inference.
  - To study multi-query amortization, the authors synthetically generate Multi-Query GSM-Symbolic using o3-mini to produce additional question-answer pairs for each existing GSM-Symbolic context.

---

### Results & Capabilities
- Sleep-time compute shifts the Pareto frontier of test-time tokens vs. accuracy, allowing models to reach equivalent accuracy with approximately 5× fewer test-time tokens on both Stateful GSM-Symbolic and Stateful AIME across GPT-4o, GPT-4o-mini, o3-mini, Claude 3.7 Sonnet, and DeepSeek-R1.
  - On Stateful AIME, sleep-time compute yields consistent Pareto improvements for o3-mini, Claude 3.7 Sonnet, and DeepSeek-R1; o1 is the notable exception, showing limited gains, possibly due to its already highly internalized reasoning structure.
- Scaling sleep-time compute itself (via parallel generations for non-reasoning models, or varying reasoning effort for o-series models) further pushes the Pareto curve outward, improving peak accuracy by up to 13% on Stateful GSM-Symbolic and 18% on Stateful AIME at comparable test-time budgets.
  - Gains from parallel sleep-time scaling exhibit diminishing returns: 5 parallel sleep-time generations typically outperforms 10, suggesting a quality saturation point in context re-representation.
- Sleep-time compute consistently Pareto-dominates pass@k parallel test-time scaling at the same test-time token budget across all tasks and models evaluated, demonstrating it is a more compute-efficient strategy than simply sampling more answers at query time.
- Multi-query amortization reduces the average cost per query by up to 2.5× when 10 queries share the same context, modelled under the assumption that test-time tokens are 10× more expensive than sleep-time tokens due to latency-optimized inference pricing.
- Query predictability is a strong predictor of sleep-time compute efficacy: binning Stateful GSM-Symbolic examples by log-probability of the question given context (under Llama2-70B) shows that the accuracy gap between sleep-time and standard test-time compute widens monotonically as questions become more predictable from context.
- In the SWE-Features agentic case study (PRs modifying ≥3 files), sleep-time compute improves F1 by roughly 1.5× at low test-time budgets, but standard test-time compute overtakes it at high budgets — consistent with the pattern seen on mathematical benchmarks.

---

### Implications
- Sleep-time compute introduces a new orthogonal axis to the test-time scaling landscape: rather than scaling compute width (parallel sampling) or depth (sequential reasoning), it scales the pre-query reasoning window, and both existing sequential and parallel techniques can be applied within this new axis without modification.
- For stateful LLM applications — coding assistants, document QA, persistent conversational agents — sleep-time compute suggests a practical deployment architecture where models continuously process and enrich persistent context during idle periods, fundamentally changing the latency-cost tradeoff at the application layer.
- The framing of sleep-time compute as natural-language representation learning over tokens connects inference-time scaling to the broader learning dynamics literature: rather than learning representations in parameter space, the model learns context-adapted 

## Key Claims

1. Sleep-time compute reduces the test-time compute needed to achieve the same accuracy by approximately 5× on Stateful GSM-Symbolic and Stateful AIME.
2. Scaling sleep-time compute can increase accuracy by up to 13% on Stateful GSM-Symbolic.
3. Scaling sleep-time compute can increase accuracy by up to 18% on Stateful AIME.
4. Amortizing sleep-time compute across 10 related queries sharing the same context reduces average cost per query by 2.5×.
5. Query predictability from context is well correlated with the efficacy of sleep-time compute.
6. Sleep-time compute consistently outperforms pass@k parallel scaling at the same test-time token budget across all tested tasks and models.
7. At high test-time compute budgets, the standard test-time compute baseline slightly outperforms sleep-time compute, possibly because the standard approach contains only query-relevant content with les
8. The o1 model demonstrates limited gains from sleep-time compute, unlike o3-mini, Claude 3.7 Sonnet, and DeepSeek-R1.
9. Scaling sleep-time compute via parallel generations plateaus and exhibits diminishing returns: 5 parallel generations generally outperforms 10.
10. The largest gains from scaling sleep-time compute appear on more difficult tasks with stronger models, suggesting that more complex contexts benefit more from additional sleep-time compute.

## Capabilities

- Sleep-time compute enables LLMs to pre-process persistent contexts during idle time, generating enriched representations that reduce test-time compute requirements by ~5x for equivalent accuracy on mathematical reasoning benchmarks
- Scaling sleep-time compute via parallel offline generations or higher reasoning effort shifts the test-time compute vs. accuracy pareto frontier outward, improving accuracy by up to 13–18% above the baseline at the same test-time budget
- Amortizing sleep-time compute across multiple queries sharing the same context reduces average inference cost per query by up to 2.5x when 10 queries share a context
- Sleep-time compute consistently outperforms pass@k parallel test-time scaling at equal test-time token budgets across all tested models and tasks, establishing it as a more effective inference scaling strategy for stateful settings
- Sleep-time compute applied to agentic SWE tasks reduces test-time token requirements by ~1.5x at low-to-moderate compute budgets, enabling better codebase exploration before feature implementation queries arrive

## Limitations

- Sleep-time compute is counterproductive at high test-time compute budgets — when ample compute is available at query time, standard test-time-only approaches slightly outperform sleep-time approaches on both reasoning benchmarks and SWE tasks
- Sleep-time compute effectiveness is tightly coupled to query predictability from context — unpredictable or context-unrelated queries gain little to no benefit, requiring runtime classification and fallback to standard test-time compute
- Parallel sleep-time compute scaling has a hard ceiling around 5 parallel generations — 10 parallel generations underperform 5, indicating diminishing and then negative returns from additional offline compute
- Highly capable reasoning models (o1) show limited gains from sleep-time compute, suggesting the technique may not compound with already-strong test-time reasoners — the gap may widen as frontier models improve
- Sleep-time compute for agentic SWE tasks causes lower precision — pre-exploration leads the agent to edit more files than necessary, with the broader context awareness from sleep-time increasing false-positive file edits
- Sleep-time compute is only cost-effective when multiple related queries share the same context — single-query or low-query-per-context deployments absorb full pre-computation overhead with insufficient amortization to justify the cost
- The framework assumes a clean two-phase interaction model (sleep vs. test) that fails to represent real-world LLM applications with continuous context modifications, multiple editing rounds, and variable idle durations between turns
- Evaluation relies entirely on synthetically constructed benchmarks derived from splitting existing datasets — the main experimental evidence comes from artificially imposed context-query separations with no testing on genuine stateful real-world query distributions
- Cost analysis is anchored to an assumed 10x premium for test-time vs. sleep-time tokens, citing a single provisioned-throughput benchmark — this pricing ratio is not validated across general production infrastructure and directly determines when sleep-time compute is economically beneficial
- Multi-query amortization experiments use LLM-generated questions (via o3-mini) as stand-ins for real user queries — no validation of whether synthetic questions capture realistic query diversity, potentially overstating amortization benefits

## Bottlenecks

- Stateless test-time compute paradigm forces redundant re-computation when multiple queries share the same persistent context — all contextual reasoning must restart from scratch at query time, creating unavoidable latency and cost ceilings in stateful LLM applications
- No principled method exists for predicting whether a given context will generate predictable queries — without query predictability estimation, sleep-time compute cannot be selectively allocated where it benefits most, blocking intelligent hybrid inference scheduling

## Breakthroughs

- Sleep-time compute establishes a new orthogonal scaling dimension for LLM inference — applying compute to persistent context before queries arrive, achieving pareto improvements that cannot be reached by scaling test-time compute alone

## Themes

- [[themes/context_engineering|context_engineering]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/budget-forcing|Budget Forcing]]
- [[entities/gsm-symbolic|GSM-Symbolic]]
- [[entities/speculative-decoding|Speculative Decoding]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/parallel-test-time-scaling|parallel test-time scaling]]
- [[entities/passk|pass@k]]
- [[entities/sequential-test-time-scaling|sequential test-time scaling]]
