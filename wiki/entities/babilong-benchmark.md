---
type: entity
title: BABILong benchmark
entity_type: dataset
theme_ids:
- agent_memory_systems
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 9.457287161821179e-05
staleness: 0.0
status: active
tags: []
---
# BABILong benchmark

> BABILong is a long-context reasoning benchmark that stress-tests models' ability to retrieve and reason over facts scattered across extremely long documents — sometimes reaching millions of tokens. It has become a standard evaluation surface for distinguishing architectures that genuinely handle long-range dependencies from those that merely appear to, exposing fundamental limitations in recurrent memory design that shorter benchmarks mask entirely.

**Type:** dataset
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

BABILong extends the classic bAbI reasoning tasks into the long-context regime by embedding the relevant supporting facts within large volumes of distractor text. A model must locate the needle-facts, reason across them, and produce a correct answer — all while the context stretches to lengths that invalidate the practical assumptions of standard Transformer attention. The benchmark has gained particular importance as a discriminator between recurrent architectures that claim long-context capability and those that can actually deliver it, with evaluation scales reaching 10M tokens in recent work.

## Key Findings

### What BABILong Reveals About Recurrent Architectures

The benchmark's diagnostic value lies in how it exposes the compound failure modes of modern recurrent models. According to ATLAS, these failures trace back to three largely independent design flaws: limited memory capacity bounded by architecture size, the online nature of memory updates, and insufficiently expressive management of fixed-size memory. Each flaw independently degrades BABILong performance, but together they make long-context recall essentially intractable for naive recurrent designs.

The online update problem is particularly pointed: most recurrent models optimise memory with respect to only the current input token, which causes memorisation of individual tokens without any consideration of broader context. This leads to convergence to spurious local minima, where the memory learns poor key-value mappings that happen to minimise the local loss but fail to retain the globally relevant facts BABILong requires. Matrix-valued memory with the standard delta update rule compounds this — it has sub-linear capacity relative to its parameter count, storing at most O(d_k) linearly independent key-value pairs, a hard ceiling that BABILong's distributed-fact structure quickly saturates.

Transformers, meanwhile, solve the recall problem architecturally by computing direct pairwise token dependencies, but their quadratic memory and time complexity makes them impractical at the context lengths BABILong targets at scale — creating the very gap that recurrent alternatives are meant to fill.

### Atlas as a BABILong Milestone

ATLAS reports a +80% accuracy improvement over Titans on BABILong at 10M context length — a result significant enough to serve as Atlas's headline claim. Atlas achieves this by replacing first-order gradient descent memory updates with an approximation of second-order (Newton-step) optimisation via the Omega rule and the Muon optimiser, making it the first parallelisable recurrent architecture to use curvature information for memory updates. The Omega rule also unifies global softmax attention and Sliding Window Attention as special cases, enabling the derivation of DeepTransformers as strict generalisations of the original Transformer architecture.

The polynomial kernel perspective provides theoretical grounding: polynomial feature maps approximate the exponential kernel in Transformers via Taylor series, and the coefficients act as input feature gates — setting a coefficient toward zero excludes the corresponding feature map, while setting it toward one retains it. This gating mechanism gives Atlas more expressive control over what gets written into fixed-size memory, addressing the third failure mode directly.

### Open Questions and Limitations

BABILong's own scope is worth interrogating. It tests recall and multi-hop reasoning across long contexts, but the tasks themselves remain relatively structured — the "needles" are semantically discrete facts rather than diffuse patterns woven through the document. Whether improvements on BABILong transfer to open-ended long-document understanding (where the relevant signal is not cleanly separable from noise) is an open question. The 10M-token regime also remains expensive to evaluate consistently, which limits reproducibility and makes cross-architecture comparisons sensitive to implementation details.

The gap between Titans and Atlas on BABILong also raises a question about what the +80% figure actually measures: whether it reflects a fundamental architectural advantage or a combination of better training, larger effective memory, and the specific structure of bAbI-style tasks. The broader results from Titans + MIRAS suggest the recurrent long-context space is still far from settled.

## Relationships

- **ATLAS** — primary source for BABILong results at 10M tokens; uses it as the key benchmark for validating second-order memory updates
- **Titans** — baseline model against which Atlas's BABILong gains are measured; prior state of the art on test-time memory learning
- **Titans + MIRAS** — broader context for where BABILong fits in the long-term memory evaluation landscape
- **[[themes/long_context_and_attention|Long Context and Attention]]** — BABILong is one of the primary benchmarks driving architectural research in this theme
- **[[themes/transformer_alternatives|Transformer Alternatives]]** — recurrent and linear attention models are evaluated against BABILong precisely because Transformers fail at the required context lengths due to quadratic complexity

## Limitations and Open Questions

## Sources
