---
type: entity
title: Associative memory
entity_type: theory
theme_ids:
- agent_memory_systems
- continual_learning
- in_context_and_meta_learning
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- pretraining_and_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00012131279972480303
staleness: 0.0
status: active
tags: []
---
# Associative memory

> Associative memory is a theoretical lens — formalized by the MIRAS framework — that reconceives all major sequence models (Transformers, RNNs, SSMs) as systems that compress past tokens into a fixed memory structure and retrieve from it via learned queries. Far from a mere analogy, this unification has generative power: it exposes the structural reasons why current architectures fail on long contexts, motivates principled improvements like second-order memory updates, and extends to reframe gradient-based optimizers themselves as associative compressors of curvature information.

**Type:** theory
**Themes:** [[themes/agent_memory_systems|agent_memory_systems]], [[themes/continual_learning|continual_learning]], [[themes/in_context_and_meta_learning|in_context_and_meta_learning]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/model_architecture|model_architecture]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/test_time_learning|test_time_learning]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

The associative memory framework treats sequence modeling as a problem of *what to store* and *how to retrieve it*. Under this lens, Transformer attention is an associative memory that stores key-value mappings and retrieves them via query-key similarity — but pays at least O(N×d) per token because it operates over direct pairwise dependencies across the full context. Recurrent models (RNNs, SSMs) trade this exact retrieval for a compressed fixed-size memory, incurring bounded cost but introducing irreversible information loss. MIRAS unifies both families under a single objective called the "attentional bias," from which the specific update rules of DeltaNet, Mamba, and other modern recurrent architectures can be derived as special cases.

The unification is not merely taxonomic. It reveals three structurally disjoint failure modes common to modern recurrent models: (1) bounded memory capacity determined by architecture rather than content, (2) online update dynamics that optimize for the current token in isolation, and (3) low-expressivity management of fixed-size memory. The first causes forgetting under load; the second causes convergence to spurious local minima because the memory never sees the full distributional picture; the third limits what patterns can be encoded even within the available capacity.

## Key Findings

The online update problem is particularly sharp. Most recurrent models apply gradient descent with first-order information — each step adjusts memory based on the local gradient of the current token, without awareness of loss landscape curvature. The result is that memory encodes individual token statistics rather than the underlying relational structure of the context. ATLAS addresses this by deriving an update rule (the "Omega rule") from second-order information via an approximation of the Muon optimizer — the first parallelizable recurrent architecture to do so — achieving +80% accuracy over Titans on the BABILong benchmark at 10M context length.

The capacity limitation is also formally precise: matrix-valued memory with the delta update rule (ℓ₂ attentional bias) has *sub-linear* capacity relative to its parameter count, storing at most O(d_k) linearly independent key-value pairs regardless of matrix size. This is not a tuning problem; it is a structural ceiling.

The associative memory view also motivates richer feature maps. Polynomial kernels generalize the Taylor-series approximation of the Softmax exponential kernel, and their coefficients admit a clean interpretation as *input feature gates* — setting a coefficient to zero excludes that feature map, while setting it to one retains it. This provides both theoretical grounding and a modular interface for controlling what the memory encodes.

The framework extends further to connect recurrent memory with attention. The Omega rule formulation subsumes both global and sliding-window (local) Softmax attention as limiting cases, enabling the derivation of *DeepTransformers* — a family of architectures that are strict generalizations of standard Transformers, combining the parallelism of attention with the memory efficiency of recurrence.

Perhaps the most provocative extension is the reframing of gradient-based optimizers (Adam, SGD, SignSGD, Lion, Shampoo, SOAP, and others) as associative memory systems that compress gradient history. Under this view, the standard momentum update uses a Hebbian rule with limited associative capacity — it stores gradient-weighted position but cannot track loss landscape information dynamically. The Delta Momentum optimizer, derived from this perspective, uses gradient-dependent weight decay to adapt to time-varying curvature, converging faster than standard momentum in such settings. This connects test-time memory (context compression) to training-time memory (optimizer state), suggesting the two problems share deeper structure.

## Capabilities

- Diverse gradient-based optimizers (Adam, SGD, SignSGD, NAdam, AMSGrad, RAdam, Lion, Shampoo, SOAP, AdaGrad) can be mathematically reformulated as associative memory systems that compress gradient history — yielding a unified view of optimizer state as learned memory. *(maturity: research_only)*
- Delta Gradient Descent can be extended to an L₂ regression loss objective within the associative memory framework, yielding a closed-form update rule via the Sherman-Morrison identity. *(maturity: research_only)*
- Delta Momentum, derived from this framework, converges faster than standard momentum on time-varying curvature problems by using gradient-dependent weight decay. *(maturity: research_only)*

## Known Limitations

The most immediate limitation is empirical: the optimizer-as-associative-memory reformulation is currently a purely theoretical construction. The MIRAS framing of Adam, Lion, and Shampoo as memory systems provides interpretive unification, but there is no evidence in available sources that this perspective yields practical training improvements beyond the specific Delta Momentum result. The distance between a clean theoretical restatement and a usable training recipe remains uncharted.

Within the recurrent memory setting, standard momentum's Hebbian update rule has limited associative capacity and cannot track loss landscape information — which is precisely why first-order recurrent models converge to spurious local minima. The ATLAS second-order approach improves this, but the trajectory of how far second-order information can scale in parallelizable architectures is still unclear. The capacity ceiling for matrix-valued memory (O(d_k) linearly independent pairs) is a hard constraint that second-order updates mitigate but do not eliminate; truly unlimited memory would require a different structural commitment entirely.

There is also a deeper open question: the associative memory framework unifies existing architectures well, but it is less clear whether it is *generative* — whether it can predict what new architectural forms will work before they are tried empirically, or whether it primarily provides post-hoc coherence to a landscape already discovered by other means.

## Relationships

The associative memory framework is the theoretical backbone underlying the ATLAS architecture, which operationalizes the critique of online first-order updates into a concrete recurrent model. It intersects with Titans + MIRAS work that introduced the unification of transformers, RNNs, and SSMs under this lens, and with Nested Learning which explores how deep learning architectures can be seen as hierarchical associative structures. The connection to optimizers links it to meta-learning and test-time learning research, where the same question — how to compress past experience into reusable structure — recurs at the level of gradient trajectories rather than context tokens.

## Limitations and Open Questions

## Sources
