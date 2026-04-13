---
type: source
title: 'Titans + MIRAS: Helping AI have long-term memory'
source_id: 01KJS0KV75ZWXQTNTVFWHKPY8M
source_type: article
authors: []
published_at: None
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Titans + MIRAS: Helping AI have long-term memory

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# Titans + MIRAS: Helping AI have long-term memory
article
https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/

---

## Briefing

**Google Research's Titans architecture and MIRAS theoretical framework solve the fundamental tension between speed and memory capacity in sequence modeling: by replacing fixed-size recurrent states with a deep MLP memory module that updates its own weights in real-time via gradient-based "surprise" signals, they achieve linear inference cost, parallelizable training, and context windows exceeding 2 million tokens — outperforming GPT-4 on long-context recall despite far fewer parameters. MIRAS goes further by reframing all sequence modeling history as variants of a single associative memory problem, opening a principled design space beyond the MSE/dot-product monoculture that has dominated every architecture to date.**

### Key Takeaways
1. **The speed-accuracy tradeoff is resolved** — Titans combines RNN-speed linear scaling with transformer-level accuracy by using a deep MLP as a dynamically updated long-term memory module.
2. **Test-time memorization without retraining** — The model updates its core memory parameters during inference in response to surprising inputs, not during a separate training phase.
3. **Surprise = gradient magnitude** — The "surprise metric" is literally the gradient of the memory loss: high gradient signals novel, context-breaking information that must be stored; low gradient allows safe skipping.
4. **Depth of memory matters more than size** — Ablations show that deeper MLP memory modules (more layers at fixed parameter count) achieve lower perplexity and better length-scaling than shallower ones.
5. **Titans beats GPT-4 on BABILong with far fewer parameters** — On a benchmark requiring reasoning across facts in extremely long documents, Titans outperforms all baselines including much larger models.
6. **2M+ token context windows** — Titans demonstrates effective scaling to context windows larger than 2 million tokens, a regime inaccessible to standard transformers.
7. **All sequence models are associative memory** — MIRAS' core claim: transformers, RNNs, and SSMs are all special cases of the same four-dimensional design space (memory architecture, attentional bias, retention gate, memory algorithm).
8. **The MSE monoculture is a design bottleneck** — Every major existing sequence model uses MSE or dot-product similarity; MIRAS shows this is a narrow slice of a much richer optimization landscape.
9. **Forgetting is regularization** — MIRAS reframes gating/forgetting mechanisms as regularization choices, enabling systematic design of retention behavior rather than ad hoc gating.
10. **Three non-MSE variants all outperform baselines** — YAAD (Huber loss), MONETA (generalized norms), and MEMORA (probability-map constraint) each improve over Transformer++, Mamba-2, and Gated DeltaNet, validating the broader design space.
11. **Domain generality beyond text** — Titans performs effectively on genomic (DNA) modeling and time-series forecasting, not just language tasks.

---

### The Fundamental Problem: Fixed Memory vs. Long Context

- Transformers use attention to look back at all prior inputs and prioritize relevant ones, but **computational cost scales quadratically with sequence length**, making extremely long contexts (full-document understanding, genomic analysis) computationally prohibitive.
  - The core issue is that transformers don't compress: they must hold everything in the context window, paying full cost for every token.
- Linear RNNs and state space models (SSMs) like Mamba-2 address this with **fixed-size compressed states** that update in O(1) per step, achieving linear scaling.
  - But fixed-size compression is a hard capacity ceiling: the richer and longer the sequence, the more information is inevitably lost in the compression.
  - This creates a fundamental tradeoff: speed comes at the cost of memory fidelity.
- The gap this creates is practically significant for applications that require reasoning over very long documents, scientific sequences (DNA), or streaming contexts where new information must be integrated in real time.

---

### Titans Architecture: Deep MLP as Long-Term Memory

- Titans is built on the observation that **effective learning systems need distinct but interconnected memory types**, analogous to human short-term vs. long-term memory.
  - Attention mechanisms are retained for short-term, precise memory — they remain excellent at fine-grained recall within a window.
  - The novel contribution is a **neural long-term memory module** that replaces fixed-size RNN states.
- Unlike traditional RNN states (fixed-size vectors or matrices), the long-term memory module is **a deep multi-layer perceptron** whose weights are updated dynamically during inference.
  - This gives it dramatically higher expressive power than any fixed-size state: the MLP can represent complex, non-linear relationships across the full input history.
  - The model "isn't simply taking notes; it's understanding and synthesizing the entire story" — the MLP learns to compress information meaningfully, not just accumulate it.
- **The depth of the MLP is critical**, not just its size: ablation studies comparing memory modules of identical parameter counts at different depths consistently show deeper modules achieve lower perplexity and better sequence-length scaling.
  - This suggests the MLP's representational hierarchy — not just raw capacity — is what enables high-quality long-term compression.

---

### The Surprise Metric: Gradient-Based Selective Memorization

- The central mechanism for deciding *what* to store in long-term memory is the **surprise metric**, directly inspired by human memory psychology.
  - Humans rapidly forget routine, expected events but vividly remember surprising, pattern-breaking, or emotionally significant ones.
  - Titans operationalizes this via the **gradient of the memory loss**:

## Key Claims

1. Transformer computational cost increases drastically with sequence length, limiting scalability to extremely long contexts.
2. Linear RNNs and SSMs like Mamba-2 offer fast, linear scaling by compressing context into a fixed size, but cannot adequately capture rich information in very long sequences.
3. Titans and MIRAS combine the speed of RNNs with the accuracy of transformers.
4. Test-time memorization allows an AI model to maintain long-term memory by incorporating surprise metrics while running, without dedicated offline retraining.
5. The MIRAS/Titans architecture actively learns and updates its own parameters as data streams in, rather than compressing information into a static state.
6. Titans uses a deep neural network (specifically a multi-layer perceptron) as its long-term memory module, unlike the fixed-size vector or matrix memory in traditional RNNs.
7. Using an MLP as a memory module provides significantly higher expressive power, allowing the model to summarize large volumes of information without losing important context.
8. The surprise metric in Titans is defined as the model detecting a large difference between what it currently remembers and what the new input is telling it, operationalized via the gradient.
9. When surprise is low (expected input), the gradient is low and the model skips updating its long-term memory state.
10. When surprise is high (anomalous input), the gradient is high, signaling the input is important and must be prioritized for permanent storage in the long-term memory module.

## Capabilities

- Test-time memorization: AI models can update their own parameters (long-term memory module) during inference as data streams in, without offline retraining
- Long-context scaling to over 2 million tokens with linear inference cost
- Long-context reasoning outperforming GPT-4 on BABILong benchmark with significantly fewer parameters
- Deep MLP-based long-term memory module with selective updating via gradient-based surprise metric, enabling efficient and expressive context compression beyond fixed-size RNN states
- Sequence model architecture generalising to genomic (DNA) modeling and time-series forecasting beyond text
- Non-Euclidean (non-MSE) associative memory objectives enabling outlier-robust sequence models, demonstrated by YAAD, MONETA, and MEMORA variants

## Limitations

- Transformer attention computational cost scales quadratically with sequence length, making extremely long contexts prohibitively expensive
- Traditional RNNs and SSMs use fixed-size context compression that cannot adequately capture rich information in very long sequences
- All major existing sequence models rely on MSE or dot-product similarity, making them sensitive to outliers and limiting their expressive power
- Titans' long-term memory module has finite capacity; extremely long sequences require adaptive forgetting (weight decay), meaning older information is discarded rather than retained
- The gradient-based surprise metric may fail to capture slowly-evolving but semantically critical contextual shifts that do not produce high local gradients
- Evaluation is restricted to standard NLP benchmarks (C4, WikiText, HellaSwag, PIQA); no evaluation on instruction-following, RLHF-aligned generation, agentic tasks, or production chat use cases
- Training compute costs and memory overhead of the deep MLP long-term memory module are not disclosed or quantitatively compared against transformer or RNN baselines
- No discussion of security, adversarial robustness, or prompt injection risks — the surprise-metric-driven selective memory could be exploited by adversarially crafted high-gradient inputs to preferentially overwrite memory

## Bottlenecks

- Fixed-size recurrent state capacity prevents RNN/SSM architectures from matching transformer quality on long-context tasks, blocking efficient long-context deployment
- Quadratic attention cost blocks practical transformer deployment for contexts beyond a few hundred thousand tokens at inference scale
- Universal dependence on MSE/dot-product paradigms constrains the sequence model design space, blocking discovery of more expressive or robust architectures

## Breakthroughs

- Titans introduces a deep MLP as a long-term memory module that learns and updates its own weights at inference time (test-time memorization), combining linear RNN efficiency with transformer-level expressivity and outperforming GPT-4 on long-context recall with far fewer parameters
- MIRAS provides a theoretical unification demonstrating that all major sequence models (transformers, RNNs, SSMs, linear attention) are instances of the same associative memory framework, parameterized by four orthogonal design choices, enabling principled exploration beyond the MSE paradigm

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/associative-memory|Associative memory]]
- [[entities/babilong-benchmark|BABILong benchmark]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/perplexity|Perplexity]]
- [[entities/transformer|Transformer++]]
