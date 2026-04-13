---
type: source
title: 'Google Titans: Learning to Memorize at Test Time'
source_id: 01KJVM8AVMZ6CM9DZQVTYH4B3J
source_type: video
authors: []
published_at: '2025-02-08 00:00:00'
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
# Google Titans: Learning to Memorize at Test Time

Google Research's Titans paper introduces a neural architecture that augments Transformers with a biologically-inspired long-term memory module that updates its weights at inference time. It directly targets the two core structural limitations of Transformers — quadratic attention complexity and stateless inference — by incorporating an RNN-style recurrent hidden state with a surprise-based memory selection mechanism. Results at small scale (340M–760M parameters) show improvements over Mamba and DeltaNet on language modeling and retrieval tasks, though scaling behavior remains untested and the paper's ultimate contribution relative to prior work (state-space models, RWKV) is actively debated.

**Authors:** Google Research
**Published:** 2025-02-08
**Type:** Video / Paper Review

---

## Motivation: What Transformers Can't Do

Standard Transformers have two structural problems that Titans is designed to address:

**Quadratic attention complexity.** Every token is compared to every other token during self-attention, so context window size incurs O(n²) compute and memory cost. This is the primary reason early models like GPT-4 launched with 8K–32K token windows, while reaching Gemini's 1M token window required substantial engineering effort. See [[themes/long_context_and_attention|Long Context and Attention]].

**Stateless inference.** Transformers have no persistent memory across API calls. Every inference starts from scratch — there is no mechanism for a model to carry forward what it learned from previous interactions. This forces all context-dependent reasoning into a single forward pass and makes continuous, test-time adaptation impossible. See [[themes/knowledge_and_memory|Knowledge and Memory]].

---

## Architecture: Three Types of Memory

Titans is explicitly modeled on the structure of human memory, with three distinct components. See [[themes/model_architecture|Model Architecture]] and [[themes/transformer_alternatives|Transformer Alternatives]].

### Short-Term Memory
Implemented as the standard Transformer attention mechanism (queries, keys, values). No architectural modification — this is the familiar quadratic-complexity attention window.

### Long-Term Memory (Neural LTM Module)
The central contribution of the paper. A neural module that:

- Processes tokens sequentially like an RNN, maintaining an internal hidden state that accumulates historical context
- Stores information in **key-value pairs** within the module
- **Updates its own weights during a single inference pass** — unlike standard LLMs whose weights are frozen post-training, Titans adapts its long-term memory module on-the-fly as it processes a sequence
- Uses a **meta-learning framing**: a meta-model is trained to learn how to memorize and forget; memory learning occurs in the inner loop while architecture parameters are trained in the outer loop

This achieves **linear complexity**, directly addressing the quadratic bottleneck of standard attention.

### Persistent Memory
A set of fixed parameters that are always injected into the input sequence, representing hardcoded knowledge or rules. The paper does not explain this component in depth — its initialization, structure, and precise role remain unclear. See [[themes/agent_memory_systems|Agent Memory Systems]].

---

## The Surprise Mechanism

The most distinctive element of the Neural LTM module is its **surprise-based memory selection**, inspired by the human cognitive tendency to remember unexpected events more reliably than predictable ones.

**How it works:**
1. The surprise of an input is measured by the **gradient of the neural network with respect to that input** — a large gradient means the input deviated significantly from the model's expectation
2. Surprising inputs receive preferential treatment and are more likely to be stored in the LTM module
3. A tunable **theta parameter** controls the weight given to surprise in the memory storage decision
4. Memory is stored and retrieved as **key-value associations**, with the loss function optimizing KV mapping at test time
5. A **momentum-based update rule** stabilizes memory across steps; combined with **exponential decay**, older memories gradually fade, allowing the model to discard irrelevant historical context

This mechanism is related to the *Learning to Learn at Test Time* paper, which similarly brings RNN-style hidden states back into Transformer architectures.

---

## Integration Variants

Rather than a single fixed design, Titans proposes three ways to integrate the neural memory into the overall architecture, each with distinct attention masking patterns:

- **Memory-as-Context**: neural memory outputs are prepended as context
- **Memory-as-Layer**: neural memory is inserted as a layer in the processing stack
- **Memory-as-Gate**: neural memory modulates the flow of information via gating

Each variant presents different tradeoffs between expressiveness and compute efficiency.

---

## Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| Linear complexity long-context processing (2M+ tokens) | Research only | Outperforms Mamba and DeltaNet at 340M–760M scale |
| Inference-time weight adaptation in LTM module | Research only | Enables continuous compression of new sequence information without retraining |
| Surprise-based memory selection via gradient signal | Research only | Tunable threshold; forgetting via exponential decay |
| Three architectural integration variants | Research only | Memory-as-context, memory-as-layer, memory-as-gate |

---

## Limitations and Open Questions

### Scaling is Completely Untested
The most significant concern. All experiments use 340M–760M parameter models — 2–3 orders of magnitude below frontier production models (GPT-4, Claude Sonnet operate at hundreds of billions of parameters; Llama 7B is already considered "small"). There is direct precedent for skepticism here: with RWKV, improvements observed at 0.5B parameters failed to transfer to 7B+ models. Whether Titans' gains survive scaling is entirely unknown. **Severity: blocking.**

### Minimal Training Data
The paper's experiments use a fraction of the token counts used in modern LLM training (trillions of tokens). Generalization questions from this data regime to standard training scales are unaddressed. **Severity: significant.**

### No Released Code
The paper had no accompanying code at publication. Given the architectural complexity and the precision required to correctly implement the surprise mechanism and memory update rules, this is a substantial reproducibility barrier. **Severity: significant.**

### Ambiguous Diagrams
The 3D architectural diagrams are noted as potentially misleading — it's unclear whether representations refer to single or multiple timesteps, and the memory query/update mechanisms lack precise specification. **Severity: significant.**

### Surprise Mechanism Has a Real-World Failure Mode
The NIAH (needle-in-haystack) benchmark improvement may not generalize. In real documents where a repeated pattern type dominates the context (e.g., an entire Harry Potter book), the surprise metric would never trigger — the model would encounter nothing unexpected. The benchmark improvement may reflect a property of benchmark construction rather than a genuine capability. **Severity: significant.**

### Persistent Memory Design is Unexplained
The paper does not explain how persistent memory is initialized, structured, or contributes to the architecture. This is not the main focus, but the gap is notable. **Severity: minor.**

### Novelty Claim is Disputed
Expert commentary raises concerns about whether Titans represents a genuine breakthrough or an incremental reformulation of prior work in state-space models and RWKV. There is also noted skepticism from practitioners familiar with Google's internal research culture. The paper's relationship to the prior *Learning to Learn at Test Time* (2020) work on self-supervised test-time training is acknowledged but not fully resolved.

---

## Landscape Positioning

Titans is part of a broader wave of research attempting to break the Transformer's two defining constraints. The quadratic attention bottleneck ([[themes/long_context_and_attention|Long Context and Attention]]) has been the target of linear attention variants, state-space models (Mamba), and sliding window approaches. The stateless inference limitation ([[themes/agent_memory_systems|Agent Memory Systems]]) is addressed by retrieval-augmented generation, KV cache compression, and now architectures like Titans that embed persistent state directly in model weights.

What distinguishes Titans from pure retrieval approaches is that memory is **compressed into weight adjustments** rather than stored as raw tokens — more like human episodic compression than a database lookup. Whether this compression is lossy in ways that matter for downstream tasks is one of the key open questions.

The paper's small-scale results are promising. The scaling question is the central unknown. Classification: **promising, requires further testing**.

---

## Related Work

- [[themes/transformer_alternatives|Transformer Alternatives]] — Mamba, DeltaNet, RWKV, state-space models
- [[themes/long_context_and_attention|Long Context and Attention]] — quadratic complexity bottleneck and mitigation strategies
- [[themes/agent_memory_systems|Agent Memory Systems]] — persistent memory across inference calls
- *Learning to Learn at Test Time* (2020) — earlier work on test-time parameter adaptation with RNN hidden states

## Key Concepts

- [[entities/linear-attention|Linear Attention]]
- [[entities/perplexity|Perplexity]]
- [[entities/sliding-window-attention|Sliding Window Attention]]
- [[entities/state-space-model|State Space Model]]
- [[entities/test-time-training|Test-Time Training]]
