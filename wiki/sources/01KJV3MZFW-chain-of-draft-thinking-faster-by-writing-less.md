---
type: source
title: 'Chain of Draft: Thinking Faster by Writing Less'
source_id: 01KJV3MZFWPT1XMRZ5BZYQ0DMX
source_type: paper
authors:
- Silei Xu
- Wenhao Xie
- Lingxiao Zhao
- Pengcheng He
published_at: '2025-02-25 00:00:00'
theme_ids:
- chain_of_thought
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Chain of Draft: Thinking Faster by Writing Less

**Authors:** Silei Xu, Wenhao Xie, Lingxiao Zhao, Pengcheng He
**Published:** 2025-02-25 00:00:00
**Type:** paper

## Analysis

# Chain of Draft: Thinking Faster by Writing Less
2025-02-25 · paper · Silei Xu, Wenhao Xie, Lingxiao Zhao, Pengcheng He
https://arxiv.org/pdf/2502.18600

---

### Motivation & Prior Limitations
Chain-of-Thought (CoT) prompting substantially improves reasoning accuracy in LLMs but produces verbose intermediate steps that inflate token counts, increase latency, and raise inference costs — making it impractical for real-time or budget-constrained deployments.
- Standard CoT on GSM8k generates ~200 tokens per response for GPT-4o, producing latencies of 4.2 seconds, while direct prompting yields only 53.3% accuracy — exposing a hard trade-off between accuracy and efficiency that existing methods fail to resolve.
  - Skeleton-of-Thought reduces perceived latency via parallel decoding but does not reduce computational cost and requires parallelizable questions. Token-budget methods (CCoT, TALE) either apply a fixed global budget that models fail to adhere to, or require an additional LLM call to estimate complexity, adding latency.
  - Coconut avoids natural language reasoning entirely by operating in latent space, but suffers accuracy degradation on complex tasks, loses interpretability, and cannot be applied to black-box APIs like GPT or Claude.

The core gap is the absence of a prompting strategy that preserves or improves reasoning accuracy while achieving genuine reductions in both output token count and wall-clock latency, without requiring model retraining or architectural changes.

---

### Proposed Approach
Chain of Draft (CoD) is a few-shot prompting strategy that instructs LLMs to generate minimalistic intermediate reasoning steps — capped at five words per step — rather than the verbose natural-language elaborations produced by standard CoT.
- The method is implemented purely through prompt engineering: the system prompt directs the model to "think step by step, but only keep a minimum draft for each thinking step, with 5 words at most," and few-shot examples demonstrate CoD-style compact reasoning.
  - Unlike global token budgets (CCoT, TALE), CoD applies a per-step word limit while placing no ceiling on the number of reasoning steps, preserving the model's ability to handle problems requiring reflection, self-correction, or extended chains.
  - CoD is model-agnostic, requires no fine-tuning, and is compatible with black-box APIs. It can be composed with orthogonal latency-reduction techniques such as speculative decoding or adaptive parallel reasoning.
- The cognitive motivation is that humans externalise thought through concise notations — equations, keywords, abbreviated transformations — rather than full prose, and CoD aligns LLM intermediate outputs with this pattern.

---

### Results & Capabilities
CoD matches or exceeds CoT accuracy across arithmetic, commonsense, and symbolic reasoning benchmarks while reducing output tokens by 80–92% and cutting latency by up to 76%.
- On GSM8k (arithmetic reasoning), CoD achieves 91.1% (GPT-4o) and 91.4% (Claude 3.5 Sonnet) accuracy versus CoT's 95.4% and 95.8%, using only ~40 tokens per response compared to ~200 for CoT — an 80% token reduction. Latency falls from 4.2s to 1.0s for GPT-4o (76.2% reduction) and from 3.1s to 1.6s for Claude 3.5 Sonnet (48.4% reduction).
- On symbolic reasoning (coin flip), both GPT-4o and Claude 3.5 Sonnet achieve 100% accuracy under CoD (matching CoT), while reducing tokens by 68% and 86% respectively.
- On commonsense reasoning (sports understanding), CoD surpasses CoT: Claude 3.5 Sonnet scores 97.3% vs. CoT's 93.2%, while collapsing average output tokens from 189.4 to 14.3 — a 92.4% reduction. GPT-4o scores 98.3% vs. CoT's 95.9%.
- CoD also reduces input token costs for few-shot prompting because the in-context examples themselves are shorter, providing a compounded cost saving in API-billed deployments.

---

### Implications
CoD challenges the assumption that reasoning depth requires output verbosity, demonstrating that information-dense but syntactically minimal intermediate representations can be as computationally effective as natural-language step-by-step reasoning.
- For inference efficiency and test-time compute, CoD offers a practical, zero-retraining path to 5–13x token reduction in reasoning traces, directly translating to lower API costs and reduced latency — critical for production LLM deployments and real-time applications.
- For reasoning model design and RL-based training (o1, R1 paradigms), the paper raises the question of whether models trained on CoD-style compact reasoning data could internalize efficient intermediate representations, potentially compressing the long thinking traces that characterise current frontier reasoning models.
- CoD is composable with speculative decoding, parallel decoding (Skeleton-of-Thought), and multi-pass validation, suggesting it could serve as a layer in a broader inference optimisation stack rather than a standalone technique.
- The finding that CoD sometimes exceeds CoT accuracy (sports understanding, coin flip) suggests that verbosity in CoT may introduce noise or distraction, and that dense, abstract intermediate representations may be a more reliable reasoning substrate for certain task types.

---

### Remaining Limitations & Next Steps
CoD degrades substantially in zero-shot settings, where no few-shot CoD examples are provided, suggesting that the compressed reasoning style is not yet natively represented in current LLM pretraining distributions.
- On zero-shot GSM8k, Claude 3.5 Sonnet with CoD achieves only 65.5% accuracy — just 3.6 percentage points above direct answering — versus 90.4% for zero-shot CoT. Token savings also shrink significantly, indicating the model reverts to verbose outputs without in-context guidance.
  - The authors hypothesise this stems from the scarcity of CoD-style reasoning patterns in training data, implying the method is effectively a prompting patch over a training data gap.

CoD underperforms CoT on small model

## Key Claims

1. Chain of Draft (CoD) matches or surpasses Chain of Thought (CoT) in accuracy while using as little as 7.6% of the tokens
2. Chain of Thought achieves above 95% accuracy on GSM8K for both GPT-4o (95.4%) and Claude 3.5 Sonnet (95.8%) but requires approximately 200 tokens per response
3. CoD achieves 91.1% accuracy (GPT-4o) and 91.4% accuracy (Claude 3.5 Sonnet) on GSM8K using only ~40 tokens per response, reducing output token count by 80%
4. CoD reduces average inference latency on GSM8K by 76.2% for GPT-4o and 48.4% for Claude 3.5 Sonnet compared to CoT
5. On date understanding (BIG-bench), CoD achieves 88.1% (GPT-4o) and 89.7% (Claude 3.5 Sonnet) accuracy, comparable to CoT at 90.2% and 87.0% respectively, while using fewer tokens
6. On sports understanding (BIG-bench), CoD reduces average output tokens from 189.4 to 14.3 for Claude 3.5 Sonnet — a 92.4% reduction — while improving accuracy from 93.2% (CoT) to 97.3%
7. Zero-shot CoD shows a significant decline in effectiveness; for Claude 3.5 Sonnet on GSM8K, zero-shot CoD improves over direct answering by only 3.6%, compared to much larger gains in the few-shot set
8. The degraded zero-shot CoD performance is hypothesized to result from scarcity of CoD-style reasoning patterns in LLM training data
9. CoD performs significantly worse than CoT on small language models under 3B parameters, with accuracy gaps of 8.3% to 27.2% on GSM8K
10. Fine-tuning small models with CoD-formatted data is anticipated to significantly enhance their reasoning accuracy with CoD

## Capabilities

- Chain-of-Draft (CoD) prompting reduces reasoning token usage by 80–93% while matching or surpassing Chain-of-Thought accuracy across arithmetic, commonsense, and symbolic reasoning tasks on flagship models (GPT-4o, Claude 3.5 Sonnet)
- Per-step word-budget prompting (≤5 words per reasoning step) as a zero-cost inference efficiency technique requiring no model modification, fine-tuning, or additional API calls
- CoD achieves 92.4% token reduction (189.4→14.3 tokens) on sports understanding for Claude 3.5 Sonnet while improving accuracy over CoT (97.3% vs 93.2%), demonstrating that CoT verbosity is not always correlated with reasoning quality

## Limitations

- Chain-of-Draft fails to generalize in zero-shot settings: Claude 3.5 Sonnet's CoD improves accuracy over direct answering by only 3.6% (65.5% vs 61.9%) without few-shot examples, vs CoT's full recovery to 90.4%
- CoD systematically underperforms CoT on models with fewer than 3B parameters: Qwen2.5-1.5B scores 24.2% (CoD) vs 32.5% (CoT); Llama3.2-3B scores 52.5% (CoD) vs 70.7% (CoT) on GSM8K
- CoD exhibits a persistent 4–9% accuracy gap versus CoT on arithmetic reasoning (GSM8K: 91% CoD vs 95%+ CoT), indicating that verbosity reduction trades off against accuracy on the hardest problem instances
- CoD requires manually crafted few-shot examples with CoD-style reasoning for each task domain — human annotation effort creates a scalability barrier for deploying CoD broadly across diverse applications
- CoD's effectiveness has not been validated on hard reasoning benchmarks (MATH, competition math, coding, multi-hop QA) — all evaluations use grade-school arithmetic, simple commonsense, and toy symbolic tasks
- Standard CoT reasoning models systematically overthink simple tasks — lacking task-complexity awareness causes unnecessary token and compute consumption even when problems require minimal reasoning
- Streaming output cannot reduce overall computational cost or total latency for CoT reasoning, and is generally inappropriate for CoT where intermediate steps should not be user-visible
- Continuous latent-space reasoning (Coconut-style) trades interpretability and model accessibility for latency reduction — losing natural language reasoning and compatibility with black-box API models
- Token-budget-aware reasoning approaches require an additional LLM call for complexity estimation, adding latency, and assume models can accurately predict reasoning complexity upfront — a flawed assumption for tasks requiring mid-stream self-correction or external retrieval

## Bottlenecks

- Absence of concise-reasoning training data in LLM pretraining corpora: models cannot generate minimal-yet-informative reasoning drafts without few-shot exemplars, because CoD-style patterns are essentially absent from training distributions
- Verbose CoT reasoning is a primary bottleneck for cost and latency in deployed reasoning systems — the output token volume of step-by-step reasoning makes reasoning-capable LLMs impractical for latency-sensitive and cost-constrained production applications

## Breakthroughs

- Chain-of-Draft demonstrates that LLMs can achieve near-CoT reasoning accuracy with as little as 7.6% of CoT's token budget by constraining intermediate steps to ≤5 words — establishing that verbose reasoning is a learned artifact of training data rather than a computational necessity

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought|Chain of Thought]]
- [[entities/gsm8k|GSM8K]]
- [[entities/overthinking|Overthinking]]
- [[entities/react|ReAct]]
