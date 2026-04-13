---
type: source
title: 'ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning'
source_id: 01KJV1PKTAXTF1J4N7Z2EZQSGK
source_type: paper
authors:
- Mingyang Chen
- Linzhuang Sun
- Tianpeng Li
- Haoze Sun
- Yijie Zhou
- Chenzheng Zhu
- Haofen Wang
- Jeff Z. Pan
- Wen Zhang
- Huajun Chen
- Fan Yang
- Zenan Zhou
- Weipeng Chen
published_at: '2025-03-25 00:00:00'
theme_ids:
- chain_of_thought
- knowledge_and_memory
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning

**Authors:** Mingyang Chen, Linzhuang Sun, Tianpeng Li, Haoze Sun, Yijie Zhou, Chenzheng Zhu, Haofen Wang, Jeff Z. Pan, Wen Zhang, Huajun Chen, Fan Yang, Zenan Zhou, Weipeng Chen
**Published:** 2025-03-25 00:00:00
**Type:** paper

## Analysis

# ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning
2025-03-25 · paper · Mingyang Chen, Linzhuang Sun, Tianpeng Li, Haoze Sun, Yijie Zhou et al. (13 total)
https://arxiv.org/pdf/2503.19470

---

### Motivation & Prior Limitations
Multi-step RAG for complex, multi-hop questions remained an open challenge because existing methods relied on hand-crafted prompts or heuristics that are labor-intensive, brittle, and non-scalable.
- Most approaches to multi-step RAG depend on manually designed prompts or heuristics, "which are not only labor-intensive but also lack scalability for more intricate problems."
- Labeling reasoning steps for supervised training in multi-step RAG pipelines is "often impractical due to the associated costs and time constraints," blocking a straightforward SFT solution.
- Despite the success of RL-based reasoning models like DeepSeek-R1, "current approaches primarily focus on enhancing internal reasoning capabilities, with limited exploration of how to effectively combine this reasoning process with external knowledge retrieval."

---

### Proposed Approach
ReSearch integrates search operations directly into the RL-trained reasoning chain, treating retrieval as a first-class action interleaved with text-based thinking rather than a preprocessing step or post-hoc augmentation.
- The reasoning chain consists of three token types: `<think>` blocks for text-based deliberation, `<search>` blocks for issuing retrieval queries, and `<result>` blocks that inject retrieved content — a superset of the DeepSeek-R1 format which only uses `<think>`.
- Crucially, "when and how to perform search will be steered by previous text-based thinking and the search results will influence subsequent text-based thinking," creating a tight bidirectional coupling between reasoning and retrieval.
- GRPO (Group Relative Policy Optimization) is used as the RL algorithm; no supervised labels on reasoning steps or search decisions are provided — only outcome-based reward signals guide training entirely from scratch on Qwen2.5-7B(-Instruct) and Qwen2.5-32B(-Instruct).
- At rollout time the model generates until it emits a `<search>` tag, the query is executed, the result is concatenated, and generation resumes — enabling a dynamic, variable-depth search-and-reason loop.

---

### Results & Capabilities
ReSearch-Qwen-32B-Instruct outperforms all baselines (built on Qwen2.5-32B-Instruct) by large margins on four multi-hop QA benchmarks, with absolute improvements of 8.9%–22.4%.
- On HotpotQA / 2Wiki / MuSiQue / Bamboogle (LLM-as-a-Judge), ReSearch-Qwen-32B-Instruct scores 63.6% / 54.2% / 33.4% / 54.4%, versus the best prior baseline IRCoT at 52.1% / 30.6% / 14.2% / 36.8%, and naive generation at 30.6% / 27.9% / 10.4% / 22.4%.
- Despite training on only one dataset, trained models "demonstrate strong generalizability across various benchmarks," confirming that RL-induced search-reasoning is a transferable capability rather than dataset-specific overfitting.
- Analysis of the training process reveals that ReSearch progressively and autonomously develops reflection and self-correction behaviors — "reasoning abilities such as reflection and self-correction can be incentivized without relying on any pre-defined heuristics."

---

### Implications
ReSearch demonstrates that RL-based training can unify retrieval and reasoning into a single coherent policy, removing the need for the hand-engineered pipelines that have dominated multi-step RAG research.
- The result suggests that outcome-only reward signals are sufficient to elicit not just correct answers but also sophisticated retrieval-planning behaviors (when to search, what to query), which has broad implications for agentic LLM design where external tool use must be tightly coupled with reasoning.
- The emergence of reflection and self-correction as byproducts of RL on search-augmented reasoning extends findings from pure-reasoning RL (DeepSeek-R1) to the RAG domain, suggesting these metacognitive capabilities may generalize across action spaces.
- Training on a single dataset with strong cross-benchmark transfer suggests that RL shapes general reasoning-with-search skills rather than narrow task adaptation, making the approach potentially viable for low-resource domains.

---

### Remaining Limitations & Next Steps
The paper evaluates exclusively on multi-hop question answering benchmarks, leaving broader applicability to open-ended generation, long-form tasks, or tool-use beyond search unexplored.
- All experiments use a fixed retrieval backend; the interaction between RL-trained search behavior and different retrieval system qualities (noisy, sparse, or domain-shifted corpora) is not studied.
- The improvement on MuSiQue (33.4% for the strongest model) remains substantially lower than on HotpotQA (63.6%), indicating that the hardest multi-hop reasoning chains still present a significant challenge not fully resolved by the framework.
- The paper does not discuss computational cost of RL training relative to SFT alternatives, nor the inference-time cost of dynamic multi-step retrieval at scale, both of which are practical concerns for deployment.
- Future work is implicitly pointed toward more realistic scenarios, but explicit plans for handling longer contexts, noisier search results, or multi-modal retrieval are not stated.

## Key Claims

1. Integrating reasoning with external search processes is challenging, especially for complex multi-hop questions requiring multiple retrieval steps.
2. Most existing multi-step RAG approaches rely on manually designed prompts or heuristics, which are labor-intensive and lack scalability.
3. Labeling reasoning steps in a multi-step RAG framework is often impractical due to cost and time constraints.
4. ReSearch trains LLMs to reason with search via reinforcement learning without using any supervised data on reasoning steps.
5. In ReSearch, the reasoning chain is composed of text-based thinking, search queries, and retrieval results, treating search as part of the chain-like reasoning process.
6. When and how to perform search in ReSearch is steered by previous text-based thinking, and search results influence subsequent text-based thinking.
7. ReSearch uses GRPO as its reinforcement learning algorithm.
8. ReSearch is trained on Qwen2.5-7B(-Instruct) and Qwen2.5-32B(-Instruct) models.
9. ReSearch trained models show significant absolute improvements ranging from 8.9% to 22.4% over baselines on multi-hop QA benchmarks.
10. ReSearch models, trained on only one dataset, demonstrate strong generalizability across various benchmarks.

## Capabilities

- LLMs trained via GRPO reinforcement learning learn to reason with search — deciding when and how to issue search queries based on intermediate thinking — achieving 8.9–22.4% absolute improvements on multi-hop QA benchmarks without any labeled reasoning steps
- RL training on search-augmented reasoning chains naturally induces reflection and self-correction behaviors without any pre-defined heuristics for those behaviors
- Models trained on a single multi-hop QA training set via ReSearch generalize across multiple held-out benchmarks (HotpotQA, 2Wiki, MuSiQue, Bamboogle), suggesting RL-trained search-reasoning transfers across question distributions

## Limitations

- Designing robust multi-step RAG strategies applicable to complex real-world problems remains an open research challenge — current methods do not reliably handle the chained retrieval-reasoning loops real-world complexity demands
- Existing RL-for-reasoning approaches are almost entirely limited to internal reasoning (chain-of-thought) and have not been extended to integrate external knowledge retrieval as part of the reasoning process
- Conventional multi-step RAG relies on manually designed prompts and heuristics that are labor-intensive to engineer and do not scale to more intricate problem structures
- Annotating reasoning steps for multi-step RAG training is practically infeasible at scale due to cost and time — this blocks supervised learning approaches to the problem
- ReSearch shows a sharp performance cliff on MuSiQue (33.4%) compared to HotpotQA (63.6%) and 2Wiki (54.2%), indicating significant degradation on the hardest multi-hop question structures even after RL training
- ReSearch is evaluated exclusively on multi-hop factoid QA benchmarks — there is no discussion of applicability to open-ended tasks, longer reasoning horizons, tool use beyond search, or non-factual domains
- All ReSearch experiments train on a single specific training dataset — the generalizability claim rests on a narrow inductive basis and has not been validated under distribution shift from truly novel domains
- The paper implicitly depends on a reliable external search API returning useful results at each reasoning step — robustness to noisy, irrelevant, or adversarial retrieval results is not discussed

## Bottlenecks

- Integrating RL-based reasoning training with external search/tool-use is a hard open problem — existing RL frameworks assume self-contained reasoning chains and cannot cleanly handle environment interaction during rollout
- The absence of labeled reasoning-step data for multi-step RAG blocks supervised approaches and forces reliance on expensive human annotation or brittle heuristics

## Breakthroughs

- ReSearch demonstrates that GRPO reinforcement learning, using only final answer correctness as a reward signal, is sufficient to train LLMs to spontaneously learn when and how to issue search queries within a reasoning chain — requiring zero supervised reasoning-step labels

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/retrieval_augmented_generation|retrieval_augmented_generation]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/2wikimultihopqa|2WikiMultihopQA]]
- [[entities/bamboogle|Bamboogle]]
- [[entities/grpo|GRPO]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/ircot|IRCoT]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/musique|MuSiQue]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/chain-of-thought-reasoning|chain-of-thought reasoning]]
