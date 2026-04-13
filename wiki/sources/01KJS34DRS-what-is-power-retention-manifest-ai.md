---
type: source
title: What Is Power Retention? - Manifest AI
source_id: 01KJS34DRSXT2FJQK0Y1D6K2G4
source_type: article
authors: []
published_at: None
theme_ids:
- long_context_and_attention
- model_architecture
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 16
tags: []
---
# What Is Power Retention? - Manifest AI

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# What Is Power Retention? - Manifest AI
article
https://manifestai.com/articles/what-is-power-retention/

---

## Briefing

**Manifest introduces Power Retention, a new sequence modeling architecture that replaces Transformer attention with a fixed-size, selective memory mechanism derived from the mathematical concept of the symmetric power — the first retention-based approach claimed to match Transformer scaling properties. The core argument is that Transformers' perfect-recall attention is not a feature but a structural liability: it makes long-context processing computationally intractable, and human-like selective memory is both sufficient and dramatically more efficient.**

### Key Takeaways
1. **Transformers are memorization machines by design** — Attention forces the model to replay the entire past for every prediction; this scales catastrophically with context length and is the root cause of why long-context AI is slow and expensive.
2. **Power retention uses fixed-size memory, not unlimited recall** — By capping memory, the architecture forces selective compression of experience, more closely mirroring how human cognition works.
3. **The "power" is the breakthrough, not retention itself** — Retention has existed since at least 2016 but failed to scale; Manifest's insight is that a retention variant derived from the symmetric power mathematical concept achieves Transformer-class scaling.
4. **Retention unifies attention and recurrence** — It takes hardware-friendliness from attention and memory efficiency from RNNs, synthesizing both paradigms' strengths while avoiding their respective weaknesses.
5. **Custom GPU kernels outperform Flash Attention on GPU utilization** — Manifest open-sourced these kernels, making the speedups immediately accessible to anyone training long-context models.
6. **Long-context AI becomes economically viable at millions of tokens** — The architecture unlocks applications previously prohibitively expensive or impractically slow with Transformers.
7. **RAG becomes architecturally unnecessary** — Instead of heuristic retrieval to fit relevant tokens into a limited context, power retention lets all information be available and lets the model itself decide relevance.
8. **Persistent AI sessions replace ephemeral ones** — Rather than restarting context per interaction, power retention enables continual interaction streams that accumulate understanding of the user over time.
9. **Agentic AI can complete long tasks without context fragmentation** — A single agent can hold an entire complex task in memory rather than requiring orchestrated chunking as context overflows.
10. **PowerCoder-3B is the first public artifact** — An open-source, open-weights 3B-parameter coding model demonstrates the architecture in practice.
11. **Manifest positions power retention as a prerequisite for AGI** — They argue human-level general capability requires human-like selective memory, not perfect recall.

---

### The Structural Flaw in Transformer Attention

- **Transformers remember the past in perfect detail**, and this is framed not as a strength but as an architectural liability that becomes progressively more severe with scale.
  - The analogy used: a doctor who must mentally replay every moment of his life before diagnosing a patient — technically complete, but operationally useless.
  - **The reason current chatbots seem fast is not that the problem is solved — it is that they operate with short, ephemeral contexts.** Fewer tokens to replay means faster response, but the architecture's fundamental cost structure remains unchanged.
  - As context length grows toward millions of tokens, the computational cost of full-fidelity attention becomes prohibitive, both in latency and in dollar cost.

- The core issue is that attention conflates two distinct things: **remembering the past** and **synthesizing the past into predictions**.
  - Transformers solve synthesis by brute-force memorization: store everything, attend to all of it.
  - This sidesteps the harder cognitive problem of deciding what matters — a problem humans solve constantly and which is central to general intelligence.

- **Transformers completely sidestep intelligent memory management in favor of naive memorization**, which means capabilities like ignoring irrelevant details, synthesizing evidence across experiences, and drawing on a rich history are structurally absent.

---

### What Power Retention Is and How It Works

- Retention serves the same architectural role as attention — synthesizing past context into predictions about future tokens — but via a fundamentally different mechanism.
  - Instead of attending to all past tokens with full fidelity, retention **learns to identify which parts of the past are important** and retains only those.
  - The result is a **fixed-size memory state** that is updated continuously, not a growing key-value cache.

- **Retention is a unification of attention and recurrence**, combining:
  - From attention: **hardware-friendly design** that maps efficiently to GPU parallelism.
  - From recurrence (RNNs): **fixed-size memory**, avoiding the quadratic cost scaling of attention with sequence length.

- The "power" component — derived from the **symmetric power**, a specific mathematical structure — is what distinguishes Manifest's approach from prior retention work.
  - Retention has been studied since at least 2016 but was largely an academic curiosity because earlier retention models could not be scaled to LLM scale competitively with Transformers.
  - **Manifest's critical insight is that the symmetric power form of retention has scaling properties that rival Transformers**, unlocking practical deployment for the first time.

- Fixed-size memory creates a kind of cognitive pressure: **space is limited, so it becomes precious**, forcing the architecture to develop genuine selectivity rather than defaulting to memorization.

---

### Practical Capabilities Unlocked

- **Mill

## Key Claims

1. Power retention enables AI to handle millions of tokens at a fraction of today's cost compared to Transformer-based architectures.
2. The fatal flaw of Transformers is that their attention mechanism requires remembering the entire past in perfect detail, causing computational cost to scale poorly with context length.
3. Current Transformer-based chatbots avoid prohibitive latency only because they operate with short context windows, not because the architectural scaling problem is solved.
4. Power retention uses a fixed-size memory, forcing selective incorporation of new information rather than naive memorization of all past tokens.
5. Retention models require human-intelligence-like capabilities — ignoring irrelevant details, synthesizing evidence, and reminiscing — that Transformers bypass through brute-force memorization.
6. Power retention enables persistent, continual AI interaction streams rather than requiring new sessions for each interaction.
7. Power retention could eliminate the need for RAG heuristics by making all information available and letting the model itself decide relevance.
8. Retention is a unification of attention (hardware-friendly design) and recurrence (fixed-size memory), combining strengths of both paradigms.
9. Retention as a concept has been studied since at least 2016 but was previously unable to scale as well as Transformers in the LLM era.
10. Manifest's key insight is that a specific form of retention derived from the symmetric power mathematical concept possesses scaling properties comparable to Transformers.

## Capabilities

- Long-context inference over millions of tokens at a fraction of transformer attention cost, via fixed-size selective retention memory
- Custom power retention GPU kernels achieving higher GPU utilization than Flash Attention, now open-sourced
- PowerCoder-3B: open-source, open-weights coding language model built on power retention architecture
- Continuous persistent memory across AI sessions without resets, enabled by fixed-size retention state that accumulates experience over time

## Limitations

- Transformer attention requires perfect recall of all past tokens, causing inference latency to scale with context length and making long-context operation prohibitively slow
- Current transformer-based chatbots are only practically usable because sessions are kept short — the architecture's long-context cost is hidden by short-lived interactions
- Prior retention and recurrent architectures could not scale competitively with transformers, restricting them to academic research despite being studied since at least 2016
- Power retention uses fixed-size memory, meaning context must be compressed and lower-priority information is inevitably lost — not all past tokens are directly retrievable
- No benchmark comparisons or quality metrics are presented in the public announcement; all empirical evidence is deferred to a separate paper
- Only a 3B parameter coding-specialized model has been released; general-purpose or larger-scale power retention capability has not been demonstrated
- The promised practical benefits — continuous sessions, no context rot, no RAG patchwork — are stated as future projections, not present validated outcomes
- RAG pipelines are characterised as unreliable heuristics with no guarantee that the most relevant tokens are retrieved into context

## Bottlenecks

- Quadratic attention cost prevents scalable long-context inference in transformers; power retention proposes a linear-cost alternative but requires re-training from scratch and independent quality validation
- Lack of scalable non-transformer sequence architectures concentrated the LLM design space around a single paradigm, blocking competitive alternatives despite decade-long research on recurrence

## Breakthroughs

- Discovery that retention derived from the symmetric power mathematical formulation achieves transformer-competitive scaling properties, breaking the decade-long barrier that kept recurrent architectures confined to academic research

## Themes

- [[themes/long_context_and_attention|long_context_and_attention]]
- [[themes/model_architecture|model_architecture]]
- [[themes/transformer_alternatives|transformer_alternatives]]

## Key Concepts

- [[entities/flash-attention|Flash Attention]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
