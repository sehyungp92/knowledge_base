---
type: source
title: 'Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement
  Learning'
source_id: 01KJTMKZPAPXSV9XW07NJW9KTR
source_type: paper
authors:
- Bowen Jin
- Hansi Zeng
- Zhenrui Yue
- Jinsung Yoon
- Sercan Arik
- Dong Wang
- Hamed Zamani
- Jiawei Han
published_at: '2025-03-12 00:00:00'
theme_ids:
- knowledge_and_memory
- policy_optimization
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning

Search-R1 introduces a reinforcement learning framework that trains LLMs to autonomously interleave multi-step reasoning with live search engine calls, using only outcome-based rewards — no labeled retrieval trajectories required. By treating the search engine as part of the RL environment and masking retrieved tokens from the policy gradient, the approach achieves 24% and 20% average relative improvement over RAG baselines for 7B and 3B models respectively across seven QA datasets, while establishing retrieved token masking as a broadly applicable stabilization primitive for RL training with external tool calls.

**Authors:** Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang, Hamed Zamani, Jiawei Han
**Published:** 2025-03-12
**Type:** paper
**Source:** https://arxiv.org/pdf/2503.09516

---

## Motivation

LLMs with strong parametric reasoning (DeepSeek-R1, o1) remain suboptimal at using search engines during inference, because they were never explicitly trained to generate effective queries or integrate retrieved content into multi-step reasoning chains. Three prior paradigms all fall short:

- **Prompting-based** (IRCoT, ReAct): fails to generalize — the LLM has no incentive to develop principled search behaviors, and tasks requiring real-time retrieval may not have appeared during pretraining.
- **Supervised fine-tuning** (Toolformer, Self-RAG): requires large-scale, high-quality annotated reasoning-plus-retrieval trajectories that are expensive and difficult to obtain at scale.
- **Standard RAG**: performs a single retrieval pass before generation; even multi-turn prompted variants are not end-to-end optimized because the non-differentiability of search operations blocks gradient-based training.

The paper identifies three specific unsolved challenges for applying RL to search-augmented reasoning: (1) stable optimization when retrieved tokens are injected mid-trajectory, (2) enabling dynamic multi-turn retrieval decisions, and (3) determining whether simple outcome rewards are sufficient to induce coherent search behavior.

---

## Approach

Search-R1 extends the DeepSeek-R1 Zero RL framework to treat the search engine as part of the RL environment, training the LLM to interleave token generation with live retrieval calls using only answer-correctness rewards.

**Structured token protocol.** Four special token types delimit the trajectory structure:
- `<think>...</think>` — reasoning steps
- `<search>...</search>` — triggers a live retrieval call
- `<information>...</information>` — delimits returned passages
- `<answer>...</answer>` — final output

This enables multi-turn interleaved reasoning and search within a single rollout trajectory, with the model autonomously deciding when and what to search.

**Retrieved token masking.** Gradients are not propagated through retrieved passage tokens. This prevents the RL signal from being corrupted by tokens the model did not generate — the key stabilization technique that makes the framework tractable. Without this, injecting external tokens mid-sequence destabilizes policy optimization.

**Minimal reward design.** The reward function is intentionally simple: outcome correctness of the final answer, with no process reward or search-quality signal. The search engine is a black-box environment component, not a learned module.

**Algorithm-agnostic.** Demonstrated with both PPO and GRPO. GRPO eliminates the need for a critic model by estimating baselines from group scores across sampled trajectories, simplifying implementation. PPO requires multiple rounds of LLM optimization, making it more challenging to deploy at scale.

---

## Results

Under controlled conditions — identical retrieval index, base model, and training data — Search-R1 demonstrates:

| Model | Improvement over RAG baseline |
|---|---|
| Qwen2.5-7B | +24% average (seven QA datasets) |
| Qwen2.5-3B | +20% average (seven QA datasets) |

Key empirical findings from ablations:
- **Outcome rewards suffice**: the model autonomously learns to issue multiple targeted search queries per reasoning trace without any supervision on query quality.
- **Emergent adaptive retrieval**: trained models generate longer reasoning traces with more search calls on harder questions — the retrieval strategy adapts to problem complexity without explicit instruction.
- **Scale generalization**: the RL training signal for search behavior works at both 3B and 7B scales, suggesting it is not exclusive to large models.

---

## Key Contributions

### Retrieved Token Masking as a General Primitive

The masking technique that excludes externally injected tokens from policy gradient computation is not specific to search — it applies to any RL setting where tool outputs, environment observations, or other non-generated tokens appear mid-sequence. This is a broadly reusable stabilization primitive for [[themes/policy_optimization|policy optimization]] with external tools.

### Reframing RAG as Policy Optimization

Search-R1 repositions the retrieval-generation interface from a pipeline engineering problem into a [[themes/policy_optimization|policy optimization]] problem. Prior [[themes/retrieval_augmented_generation|RAG]] architectures treated query generation and answer generation as decoupled modules; here they are jointly optimized through the reward signal.

### Lowering the Annotation Barrier

The demonstration that outcome-only RL can induce reliable tool-use behavior without labeled search trajectories significantly reduces the cost of training retrieval-augmented reasoning systems. The "how to search" capability is learnable purely from answer-level feedback.

### Extension of R1-Zero to Open-World Environments

Search-R1 shows that the [[themes/rl_for_llm_reasoning|RL-for-reasoning]] paradigm pioneered by DeepSeek-R1 Zero extends to interactive, open-world environments with minimal architectural changes — multi-step reasoning and multi-turn retrieval are jointly learnable and mutually reinforcing.

---

## Limitations & Open Questions

### Evaluation Scope
- Results are confined to **factoid question-answering benchmarks** — generalizability to long-form generation, multi-document synthesis, agentic tasks, or any setting where correct answers are not machine-verifiable is entirely untested and explicitly acknowledged as uncertain.
- Only **Qwen2.5** model family tested — transferability to LLaMA, Mistral, or GPT-family architectures is not established.
- Only **3B and 7B scales** evaluated — whether RL-based search training provides comparable benefits for frontier-scale models is unknown and potentially diminishing.

### Computational Costs
- **Inference latency** from multi-turn interleaved search calls is not evaluated. Each additional search round adds external network latency plus expanded context token overhead, which could be substantial in production settings.

### Reward Signal Generalization
- Whether simple outcome-based rewards are sufficient for tasks harder than factoid QA — where correct answers are not verifiable strings — is explicitly left as an open question. The reward design that works here may not transfer to open-ended generation tasks.

### Retrieval Quality Sensitivity
- All experiments use a **fixed, high-quality retrieval backend**. How performance degrades with lower-quality retrievers, noisy corpora, or out-of-distribution queries is not evaluated.

### Fundamental Barriers
- The **non-differentiability of external tool calls** remains a fundamental theoretical barrier. RL workarounds are effective but introduce their own stability and sample efficiency challenges that gradient-based optimization avoids in principle. This bottleneck likely constrains the approach for 3–5 years.

---

## Connections

**Themes:**
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] — direct extension of the R1-Zero paradigm to tool-augmented settings
- [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]] — reframes RAG as a policy learning problem rather than pipeline engineering
- [[themes/reinforcement_learning|Reinforcement Learning]] — GRPO and PPO applied to LLM search behavior
- [[themes/policy_optimization|Policy Optimization]] — retrieved token masking as a stabilization technique for non-differentiable environment steps
- [[themes/knowledge_and_memory|Knowledge and Memory]] — dynamic retrieval as an alternative to parametric knowledge for factual grounding

**Related work:**
- DeepSeek-R1 Zero — the RL reasoning framework Search-R1 directly extends
- IRCoT, ReAct — prompting-based baselines that Search-R1 outperforms by training rather than prompting
- Self-RAG, Toolformer — supervised fine-tuning baselines blocked by trajectory annotation costs

---

## Open Questions

1. Can outcome-based RL train effective search behavior on tasks without ground-truth verifiable answers — creative writing, strategic planning, open-ended research?
2. Does the retrieved token masking technique extend cleanly to other tool types (code interpreters, calculators, web browsers) with different output structures and latencies?
3. At what model scale does RL-based search training yield diminishing returns — does a 70B model benefit as much as a 7B model, or does its parametric knowledge make search less necessary?
4. How does performance degrade when the retrieval backend is noisy, domain-shifted, or adversarially corrupted — what is the robustness profile of RL-trained search strategies?
5. Can the approach extend to tasks requiring **sequential dependent sub-queries** — where the answer to one search shapes what must be searched next — at longer horizons than current QA benchmarks probe?

## Key Concepts

- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/ircot|IRCoT]]
- [[entities/outcome-based-reward|Outcome-Based Reward]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/rloo|RLOO]]
- [[entities/react|ReAct]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
