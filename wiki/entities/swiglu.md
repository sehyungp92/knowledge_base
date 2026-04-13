---
type: entity
title: SwiGLU
entity_type: method
theme_ids:
- adaptive_computation
- alignment_and_safety
- hallucination_and_reliability
- in_context_and_meta_learning
- latent_reasoning
- long_context_and_attention
- mathematical_and_formal_reasoning
- model_architecture
- post_training_methods
- reasoning_and_planning
- representation_learning
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.00035796756884723987
staleness: 0.0
status: active
tags: []
---
# SwiGLU

> SwiGLU is a gated activation function that combines the Sigmoid Linear Unit (SiLU) with a learned gating projection in the feed-forward sublayer of transformer models. Originally proposed as a drop-in replacement for ReLU-family activations, it has become a standard component in modern transformer architectures and has been identified as a critical source of nonlinear expressivity for complex reasoning tasks — a status reinforced by architectural extensions like ConvSwiGLU that build directly on its gating mechanism.

**Type:** method
**Themes:** [[themes/model_architecture|model_architecture]], [[themes/latent_reasoning|latent_reasoning]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/transformer_alternatives|transformer_alternatives]], [[themes/representation_learning|representation_learning]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

SwiGLU replaces the standard two-matrix MLP block with a three-matrix formulation: two parallel projections (one gating, one value) whose elementwise product passes through SiLU before a final linear output. The gating path gives the network a multiplicative, input-dependent way to suppress or amplify information flowing through each feed-forward unit — a form of conditional computation at the activation level that is cheaper than attention but richer than a static nonlinearity.

Its significance in the context of reasoning-intensive architectures comes from how this local gating interacts with depth and recurrence. In the Universal Reasoning Model (URM), SwiGLU serves as the standard feed-forward activation across a relatively shallow four-layer backbone (hidden size 512, 8 attention heads) that is then iterated through inner and outer recurrent loops. The expressivity budget that would normally require more layers is instead partially carried by SwiGLU's multiplicative nonlinearity, making gating quality more load-bearing as depth is traded for recurrence.

## ConvSwiGLU: Injecting Local Context into Gating

The most architecturally notable development in this space is the **ConvSwiGLU** variant introduced in Universal Reasoning Model. Standard SwiGLU is a pointwise operation — each token's gating signal depends only on that token's own representation. ConvSwiGLU augments the gating projection with a depthwise short convolution of kernel size 2, so the gate for each position sees a local neighbourhood before deciding how much signal to pass. This injects short-range contextual interactions into the feed-forward block without the quadratic cost of attention.

The motivation is directly tied to reasoning: tasks like Sudoku and ARC-AGI require propagating local constraint signals (neighbouring cells, adjacent spatial regions) as part of the iterative solution process. Attention handles long-range dependencies; ConvSwiGLU handles the fine-grained local texture. URM's benchmark results — 77.6% on Sudoku (vs. 66.8% for TRM, 63.9% for HRM), 53.8% pass@1 on ARC-AGI 1 (vs. 40.0% and 34.4%), and 16.0% on ARC-AGI 2 nearly tripling HRM's 5.4% — reflect the combined effect of the recurrent architecture and this activation-level modification, though the isolated contribution of ConvSwiGLU versus other design choices is not reported separately.

## Relationship to Broader Architectural Trends

SwiGLU sits at the intersection of two converging design pressures: the desire to increase per-parameter expressivity without adding depth, and the search for cheap local structure that complements global attention. The [[themes/transformer_alternatives|transformer alternatives]] space is exploring both directions — the Differential Transformer compresses attention itself (achieving comparable language modeling with ~65% the parameters or tokens), while ConvSwiGLU compresses local structure into the feed-forward block.

There is a structural parallel worth noting: the differential attention mechanism in DIFF Transformer uses a learnable scalar λ re-parameterized as a difference of exponentials to control how much noise is cancelled in attention. This is analogous in spirit to SwiGLU's gating — both introduce a learned suppression signal that filters information at a sub-block level. Neither is a global architectural change; both are surgical interventions at the activation or attention-weight level that propagate significant downstream effects.

## Limitations and Open Questions

The primary open question around SwiGLU in reasoning contexts is **attribution**: it is consistently co-deployed with other innovations (recurrence, adaptive computation, differential attention) and its isolated effect on reasoning quality has not been cleanly ablated in published work. URM's gains could be driven by Truncated Backpropagation Through Loops (TBPTL), the ACT outer loop, the inner recurrence, or ConvSwiGLU — or, most likely, their interaction. This makes it difficult to determine whether ConvSwiGLU's local gating is genuinely load-bearing or merely compatible.

A second limitation is scope: ConvSwiGLU's kernel size 2 convolution handles immediately adjacent tokens. Whether extending the kernel or making it adaptive (rather than fixed) would help on tasks with longer local dependency horizons remains unexplored. The design choice of kernel size 2 appears empirically motivated by the structured grid tasks URM targets rather than derived from first principles.

Finally, SwiGLU's three-matrix structure is ~50% wider in parameter count than a two-matrix ReLU MLP for the same output dimension. In recurrent architectures where the same weights are reused across iterations, this overhead is amortized — but it remains a consideration when comparing against architectures that achieve expressivity through other means, such as mixture-of-experts routing.

## Related Entities

- Universal Reasoning Model — primary source introducing ConvSwiGLU and its application to iterative reasoning
- Differential Transformer — parallel architectural intervention at the attention level; shares the design philosophy of learned suppression
- The Free Transformer — orthogonal approach to expressivity via latent variable conditioning rather than activation modification
- [[themes/test_time_compute_scaling|test-time compute scaling]] — the recurrent context in which SwiGLU's per-step expressivity becomes most load-bearing
- [[themes/transformer_alternatives|transformer alternatives]] — the broader landscape of sub-block interventions that SwiGLU and its variants occupy

## Key Findings

## Relationships

## Sources
