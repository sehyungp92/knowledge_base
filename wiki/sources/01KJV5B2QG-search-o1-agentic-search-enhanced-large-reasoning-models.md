---
type: source
title: 'Search-o1: Agentic Search-Enhanced Large Reasoning Models'
source_id: 01KJV5B2QGE5H6X8PHDC4VKPV5
source_type: paper
authors:
- Xiaoxi Li
- Guanting Dong
- Jiajie Jin
- Yuyao Zhang
- Yujia Zhou
- Yutao Zhu
- Peitian Zhang
- Zhicheng Dou
published_at: '2025-01-09 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- test_time_compute_scaling
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Search-o1: Agentic Search-Enhanced Large Reasoning Models

Search-o1 addresses a fundamental tension in large reasoning models (LRMs): their extended chain-of-thought process creates compounding knowledge gaps that neither direct reasoning nor standard RAG can resolve, and the paper proposes a two-component inference-time framework — agentic mid-chain retrieval plus a dedicated document-refinement module — that enables QwQ-32B to surpass human expert performance on PhD-level science questions without any retraining.

**Authors:** Xiaoxi Li, Guanting Dong, Jiajie Jin, Yuyao Zhang, Yujia Zhou, Yutao Zhu, Peitian Zhang, Zhicheng Dou
**Published:** 2025-01-09
**Type:** paper

---

## Motivation

[[themes/reasoning_and_planning|Reasoning models]] like o1, QwQ, and DeepSeek-R1 achieve strong multi-step performance through large-scale RL, but their extended [[themes/chain_of_thought|chain-of-thought]] creates a structural vulnerability: any single knowledge gap can cascade errors across the entire reasoning trace. The paper quantifies this directly — QwQ-32B-Preview averages over 30 occurrences of "perhaps" per reasoning trace on GPQA diamond questions, indicating frequent guessing rather than knowing.

Two prior approaches both fail:

- **Standard (problem-oriented) RAG** retrieves documents once for the original question. This is misaligned with multi-step reasoning, where each step may require different background knowledge. Empirically, standard RAG sometimes performs no better than direct reasoning on complex tasks.
- **Direct document injection** into the reasoning chain causes coherence breakdown. Web documents are verbose and noisy; inserting them unfiltered disrupts logical flow and introduces irrelevant information — a failure mode compounded by the fact that LRMs have reduced long-context comprehension due to catastrophic forgetting during reasoning-focused fine-tuning.

---

## Proposed Approach

Search-o1 integrates two components into the LRM inference loop without modifying the backbone model:

**Agentic RAG mechanism.** The LRM emits special tokens (`<|begin_search_query|>` / `<|end_search_query|>`) mid-reasoning to trigger retrieval. Unlike ReAct-style agents that insert raw snippets, retrieval fires multiple times per question, conditioned on the evolving reasoning state rather than the original query. In experiments, QwQ-32B-Preview queries Bing Web Search (top-10 documents, US-EN) with full-page fetching via Jina Reader.

**Reason-in-Documents module.** Rather than injecting raw documents, a separate generation pass — using the same base model — receives the current search query, retrieved documents, and accumulated reasoning chain, then produces a concise intermediate analysis and refined summary. Only this summary is injected back into the main chain (between `<|begin_search_result|>` / `<|end_search_result|>` tokens), preserving logical coherence.

The framework supports batch inference by parallelizing token generation and Reason-in-Documents passes, advancing all sequences until EOS or a search trigger, then processing retrieval as a batch before resuming.

---

## Results

### Complex Reasoning Benchmarks

Search-o1 (QwQ-32B) outperforms the next-best 32B retrieval baseline (RAgent-QwQ) by an average of **4.7%** across five datasets:

| Benchmark | Score |
|---|---|
| GPQA Diamond | 63.6% |
| MATH500 | 86.4% |
| AMC2023 | 85.0% |
| AIME2024 | 56.7% |
| LiveCodeBench | 33.0% |

QwQ-32B without retrieval already outperforms Qwen2.5-72B and Llama3.3-70B on GPQA and math, confirming that [[themes/test_time_compute_scaling|test-time compute scaling]] is the dominant performance axis; Search-o1 adds further gains on top.

### Human Expert Comparison (GPQA Extended, 546 questions)

| Domain | Search-o1 | Human Expert |
|---|---|---|
| Physics | **68.7%** | 57.9% |
| Biology | **69.5%** | 68.9% |
| Chemistry | 40.7% | **72.6%** |
| Overall | **57.9%** | — |

The chemistry gap (40.7% vs. 72.6%) is the largest underperformance against any human expert group, suggesting procedural mechanistic chemistry knowledge is not well-served by web retrieval.

### Open-Domain QA

Search-o1 exceeds RAG-QwQ-32B by **29.6% average EM** on multi-hop tasks and RAgent-QwQ-32B by 5.3%, but shows no meaningful advantage over agentic baselines on single-hop tasks — confirming that iterative retrieval benefits are scoped to questions requiring multi-step knowledge assembly.

---

## Capabilities

- **Mid-chain agentic retrieval for LRMs** — QwQ-32B can autonomously issue targeted web searches at the point of knowledge uncertainty within a reasoning trace, triggering multiple retrievals per question. [[themes/agent_systems|`research_only`]]
- **Reason-in-Documents refinement** — a separate LLM pass distills verbose web documents into chain-compatible summaries, resolving the coherence-injection tradeoff without architectural changes. [[themes/retrieval_augmented_generation|`research_only`]]
- **Superhuman PhD-level science QA** — a 32B model + agentic retrieval surpasses aggregate human expert performance in physics and biology on GPQA. [[themes/test_time_compute_scaling|`research_only`]]
- **Single-document advantage** — even one retrieved document processed through Reason-in-Documents surpasses both direct reasoning and standard RAG with 10 documents, indicating retrieval quality trumps quantity. [[themes/knowledge_and_memory|`research_only`]]
- **Multi-hop QA gains** — agentic RAG improves multi-hop open-domain QA by 23.2% average EM over standard RAG for reasoning models. [[themes/retrieval_augmented_generation|`research_only`]]

---

## Limitations & Open Questions

### Fundamental LRM Limitations Exposed

- **Pervasive reasoning uncertainty** — "perhaps" appears 30+ times per GPQA diamond trace, revealing that LRMs frequently guess rather than know during extended reasoning. *(severity: significant, trajectory: improving)*
- **Error cascading in reasoning chains** — a single factual error at step *n* contaminates all subsequent steps through conditioning context, with no self-correction mechanism. *(severity: significant, trajectory: improving)*
- **Catastrophic forgetting of long-context comprehension** — reasoning RL fine-tuning degrades general document-processing ability, preventing direct integration of external knowledge. This bottleneck motivates the entire Reason-in-Documents architecture. *(severity: significant, trajectory: stable)*
- **LRM factual QA weakness** — without retrieval, QwQ-32B achieves *lower* average EM than Qwen2.5-32B (30.7 vs. 31.3) on open-domain QA, showing that reasoning specialisation trades off factual recall. *(severity: significant, trajectory: stable)*

### Search-o1 Specific Limitations

- **Silent failure with back-off** — when the agentic mechanism fails to produce a final answer, the system falls back to direct reasoning. The failure rate is not reported, obscuring true reliability. *(severity: significant, trajectory: unclear)*
- **No gains on competitive programming** — Search-o1 matches QwQ-32B at 33.0% on LiveCodeBench overall and *regresses* on easy problems (57.7% vs. 61.5%), revealing a performance ceiling where code generation is not knowledge-retrieval-bottlenecked. *(severity: significant, trajectory: unclear)*
- **Chemistry specialist gap** — 40.7% vs. 72.6% for domain chemists suggests mechanistic procedural knowledge is not well-served by web retrieval, pointing to limits of the knowledge-as-text assumption. *(severity: significant, trajectory: unclear)*
- **Inference compute cost** — every retrieval step requires a full separate LLM generation pass (Reason-in-Documents) in addition to the primary reasoning chain. All experiments used 8× A800-80GB GPUs with no latency analysis reported. *(severity: significant, trajectory: unclear)*
- **Single-backbone evaluation** — all experiments use QwQ-32B-Preview; no ablation across DeepSeek-R1 or o1 variants, making generalisability to other LRM families unknown. *(severity: minor, trajectory: unclear)*
- **No improvement for single-hop QA** — average EM is flat (47.8 vs. 47.6) with or without agentic retrieval on single-hop tasks; the mechanism's utility is tightly scoped to multi-step knowledge assembly. *(severity: minor, trajectory: stable)*

---

## Key Architectural Insight

The Reason-in-Documents pattern — using the model itself as a document-to-reasoning-chain translator in a separate pass — suggests a general principle for grounding any long-chain reasoner in external knowledge without polluting its context with raw retrieval noise. This is directly relevant to [[themes/knowledge_and_memory|memory augmentation]] and long-context reasoning research beyond this specific framework.

The finding that non-reasoning LLMs with agentic RAG show no improvement (or degrade) on complex tasks is equally significant: effective multi-step retrieval requires the underlying [[themes/chain_of_thought|o1-like reasoning capability]] to formulate precise sub-queries conditioned on in-progress reasoning state. Standard instruction-tuned LLMs cannot exploit this mechanism.

---

## Bottlenecks Addressed & Created

**Addressed:** The paper directly tackles the bottleneck of integrating external knowledge into LRM reasoning chains — previously blocked by both the coherence-injection problem and catastrophic forgetting of document comprehension.

**Created/Revealed:** RL fine-tuning for step-wise reasoning causes catastrophic forgetting of long-document comprehension, preventing direct RAG-LRM integration and requiring a separate document-processing component. This architectural dependency is a bottleneck for seamless end-to-end LRM architectures. *(horizon: 1–2 years)*

---

## Implications

1. **Test-time compute scaling and retrieval scaling are orthogonal and complementary** — LRMs are uniquely positioned to exploit agentic search because step-wise reasoning naturally surfaces knowledge gaps as actionable query opportunities. See [[themes/test_time_compute_scaling|test-time compute scaling]].

2. **RAG system design must change for LRM deployments** — query formulation must be conditioned on in-progress reasoning state, not the original question. Problem-oriented RAG is architecturally mismatched with multi-step reasoners.

3. **Inference-time grounding without retraining is viable** — Search-o1 is applied over a frozen backbone, opening a path to combine RL-trained reasoning with retrieval for models where fine-tuning is impractical.

4. **Human expert comparison is domain-sensitive** — aggregate superhuman performance on PhD-level science QA masks a large deficit in chemistry, suggesting that mechanistic procedural knowledge domains require more than retrieval-augmented reasoning.

---

## Themes

- [[themes/agent_systems|Agent Systems]]
- [[themes/chain_of_thought|Chain of Thought]]
- [[themes/knowledge_and_memory|Knowledge & Memory]]
- [[themes/reasoning_and_planning|Reasoning & Planning]]
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/tool_use_and_agent_protocols|Tool Use & Agent Protocols]]

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/bamboogle|Bamboogle]]
- [[entities/catastrophic-forgetting|Catastrophic Forgetting]]
- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/exact-match|Exact Match]]
- [[entities/gpqa|GPQA]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/large-reasoning-models|Large Reasoning Models]]
- [[entities/math500|MATH500]]
- [[entities/musique|MuSiQue]]
- [[entities/pass1|Pass@1]]
- [[entities/qwq-32b-preview|QwQ-32B-Preview]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/triviaqa|TriviaQA]]
