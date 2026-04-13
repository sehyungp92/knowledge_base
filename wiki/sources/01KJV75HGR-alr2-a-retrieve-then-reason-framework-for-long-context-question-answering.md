---
type: source
title: 'ALR$^2$: A Retrieve-then-Reason Framework for Long-context Question Answering'
source_id: 01KJV75HGRX7X4V2Y5C4QMP3PR
source_type: paper
authors:
- Huayang Li
- Pat Verga
- Priyanka Sen
- Bowen Yang
- Vijay Viswanathan
- Patrick Lewis
- Taro Watanabe
- Yixuan Su
published_at: '2024-10-04 00:00:00'
theme_ids:
- alignment_and_safety
- hallucination_and_reliability
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- retrieval_augmented_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ALR$^2$: A Retrieve-then-Reason Framework for Long-context Question Answering

ALR$^2$ (ALigning LLMs with Retrieval and Reasoning) identifies a fundamental asymmetry in how LLM performance degrades with context length — retrieval capability remains near-stable across 0K–128K tokens while reasoning capability collapses — then addresses it by jointly fine-tuning a single LLM on both retrieval and reasoning objectives. The result is a 35B model that achieves near-flat multi-hop QA performance from 4K to 128K tokens, nearly eliminates retrieval hallucination (61.1% → 0.29%), and outperforms GPT-4 on long-context HotpotQA — demonstrating that training objective design, not architectural scale, is the primary lever for long-context reasoning.

**Authors:** Huayang Li, Pat Verga, Priyanka Sen, Bowen Yang, Vijay Viswanathan, Patrick Lewis, Taro Watanabe, Yixuan Su
**Published:** 2024-10-04
**Type:** paper

---

## Motivation: The Retrieval–Reasoning Asymmetry

The paper begins with a deceptively simple diagnostic. Three passkey tasks test LLMs at context lengths from 0K to 128K: pure retrieval (Task 1), multi-hop retrieval (Task 2), and retrieval-then-reasoning (Task 3). The result is stark: COMMAND-R-PLUS, GPT-4, and CLAUDE-3-HAIKU all maintain high performance on Tasks 1 and 2 across the full range, but Task 3 performance collapses as context grows.

This cleanly separates two problems that benchmarks often conflate:

> "we show that as the input context length grows, LLM reasoning performance degradation is higher than that of retrieval. This decline is more pronounced..."

On HotpotQA, CMD-R with direct answering drops ~17 EM points from 4K to 128K tokens. The bottleneck is not reading long contexts — it is *reasoning over them*.

### Why Prompting Doesn't Fix It

An obvious candidate solution is to prompt the LLM to first retrieve relevant facts, then reason over those facts. This retrieve-then-reason (RR) prompting approach fails for a structural reason: pre-trained LLMs are misaligned with verbatim extraction objectives. When prompted to retrieve, CMD-R hallucinates 61.1% of its "retrieved" sentences on HotpotQA — the majority of returned evidence is fabricated. Recall of golden supporting facts sits at just 34.06%. Downstream reasoning is then grounded in confabulation rather than source text.

This establishes the core claim of the paper: hallucination in long-context retrieval is substantially a **training objective mismatch**, not a fundamental model capacity limitation.

---

## The ALR$^2$ Approach

ALR$^2$ adapts the [[themes/retrieval_augmented_generation|RAG]] formulation to the long-context setting, with one critical difference: the same model performs both retrieval and reasoning, treating the long context itself as the retrieval index rather than relying on external dense retrieval infrastructure (DPR, DSI).

**Stage 1 — Retrieval:** Given question $q$ and long context $c$, the model generates a coherent set of relevant supporting facts $z^*$ (formatted as bulleted sentences).

**Stage 2 — Reasoning:** Given $z^*$, $q$, and $c$, the model generates the answer $y^*$.

Both stages are jointly supervised via:

$$\mathcal{L}_{\text{align}} = \frac{1}{N}\sum_{i=1}^{N}\left[\log p_\theta(z_i^*|q_i, c_i) + \log p_\theta(y^*|z_i^*, q_i, c_i)\right]$$

Golden supporting facts serve as retrieval supervision targets. The joint loss explicitly rewards the model for both finding the right evidence *and* answering correctly from it.

Training data: HotpotQA (5K), SQuAD (25K), and four NIAH variants (1.6K), with context lengths distributed across 4K, 8K, 16K, and 32K. Inference at 64K and 128K is by extrapolation.

---

## Results

### Long-Context QA Performance

| Model | HotpotQA (Overall EM) | SQuAD (Overall EM) |
|---|---|---|
| CMD-R + DA (prompting) | 45.9 | — |
| CMD-R + RR (prompting) | 53.3 | 53.1 |
| GPT-4 + DA | 54.8 | 70.4 |
| CMD-R-FT + DA (fine-tuned) | 68.3 | 64.2 |
| **ALR$^2$** | **76.7** | **72.1** |

ALR$^2$ outperforms GPT-4 on HotpotQA despite being a 35B model, and exceeds the fine-tuned direct-answering baseline by 8.4 EM on HotpotQA and 7.9 EM on SQuAD — confirming the gain is specific to the two-stage alignment rather than fine-tuning in general.

### Retrieval Quality

| Model | Hallucination Rate ↓ | Recall of Golden Facts ↑ |
|---|---|---|
| CMD-R + RR | 61.1% | 34.06% |
| **ALR$^2$** | **0.29%** | **68.79%** |

The near-elimination of hallucination is the strongest result in the paper. It directly supports the claim that [[themes/hallucination_and_reliability|hallucination]] in this regime is a training objective problem rather than a capacity ceiling.

### Context-Length Stability

On HotpotQA, ALR$^2$ scores range only from 75.2 to 77.5 EM across 4K–128K — effectively flat. CMD-R+DA degrades from 51.6 to 34.29 over the same range. This demonstrates that the [[themes/long_context_and_attention|long-context reasoning bottleneck]] can be substantially resolved through alignment alone, without architectural changes.

### Generalization

On unseen benchmarks (StrategyQA, TriviaQA), ALR$^2$ consistently outperforms the fine-tuned direct-answering baseline: 71.51 vs. 59.74 overall EM on StrategyQA, 74.38 vs. 71.69 on TriviaQA. The retrieve-then-reason structure generalizes across QA task types.

---

## Limitations & Open Questions

Several significant limitations bound the applicability of these results:

**Structural scope.** The retrieve-then-reason framework assumes answers depend on *sparsely distributed, retrievable facts*. It is explicitly inapplicable to summarization tasks where all context is relevant. The approach inherits RAG's fundamental assumption that sparse retrieval is the right abstraction — which excludes synthesis, aggregation, and dense contextual integration tasks.

**Single retrieval granularity.** ALR$^2$ operates at sentence-level granularity only. Tasks requiring phrase-level precision or passage-level context cannot benefit from granularity adaptation. The authors note this as a known limitation without a proposed fix.

**Fine-tuning requirement.** The gains are available only to aligned models. Prompting alone reproduces neither the retrieval quality nor the reasoning stability. This limits deployment to settings where fine-tuning is feasible.

**Extrapolation fragility.** Training covers only 4K–32K tokens; 64K and 128K inference is extrapolation. ALR$^2$'s SQuAD scores across context lengths are notably non-monotonic (89.8 → 63.0 → 78.2 → 71.2), suggesting brittle generalization in the single-hop regime. Multi-hop results are more stable, but the pattern warrants caution.

**Benchmark saturation as a measurement problem.** NIAH tasks are saturated — all methods score ~99.75–99.79 EM. Averaging NIAH with QA scores in composite benchmarks *dilutes* genuine capability differences. The paper argues that evaluation frameworks relying on NIAH as a proxy for long-context capability significantly overstate real-world LLM performance.

---

## Implications

**Scale is not the lever.** A 35B aligned model outperforms GPT-4 and Gemini on multi-hop long-context QA. If training objective design produces larger gains than model scale, the implication is that the field has been targeting the wrong variable for long-context reasoning improvement.

**Hallucination is partially a misalignment problem.** The 61.1% → 0.29% drop in retrieval hallucination after joint alignment supervision suggests that a substantial fraction of [[themes/hallucination_and_reliability|hallucination]] in long-context settings is not a fundamental capacity failure — it is the predictable output of models optimized for generation rather than extraction. This reframes the problem as solvable through [[themes/alignment_and_safety|alignment]] rather than requiring architectural innovation.

**Benchmark reform is implied.** NIAH tasks are saturated and uninformative. The paper's three-task diagnostic framework (separate retrieval and reasoning tasks) provides a cleaner decomposition for evaluating genuine long-context capability. Composite benchmarks that average NIAH with QA scores systematically obscure real capability gaps.

**RAG alignment for [[themes/knowledge_and_memory|knowledge retrieval]].** The finding that generative retrieval from long context can match or exceed specialized dense retrievers — when properly aligned — has implications for [[themes/model_architecture|model architecture]] choices in systems where maintaining separate retrieval infrastructure is costly.

---

## Themes

- [[themes/long_context_and_attention|Long Context & Attention]]
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]
- [[themes/hallucination_and_reliability|Hallucination & Reliability]]
- [[themes/alignment_and_safety|Alignment & Safety]]
- [[themes/knowledge_and_memory|Knowledge & Memory]]
- [[themes/model_architecture|Model Architecture]]

## Key Concepts

- [[entities/exact-match|Exact Match]]
- [[entities/hallucination-rate|Hallucination Rate]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/squad|SQuAD]]
- [[entities/triviaqa|TriviaQA]]
