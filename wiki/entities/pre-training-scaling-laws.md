---
type: entity
title: Pre-training Scaling Laws
entity_type: theory
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- compute_and_hardware
- model_architecture
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- scaling_laws
- software_engineering_agents
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000329680440659497
staleness: 0.0
status: active
tags: []
---
# Pre-training Scaling Laws

> Empirical laws governing optimal compute allocation across model size and training data (canonically formalized by Hoffmann et al., 2022 in the Chinchilla paper) that define the dominant paradigm for scaling language models. Their significance lies not only in guiding training runs but in revealing what they omit: residual stream width, inference-time compute, and hardware efficiency constraints fall outside the traditional FLOPs-and-tokens framework, making them active sites of architectural and algorithmic research.

**Type:** theory
**Themes:** [[themes/agent_systems|Agent Systems]], [[themes/ai_market_dynamics|AI Market Dynamics]], [[themes/chain_of_thought|Chain of Thought]], [[themes/compute_and_hardware|Compute and Hardware]], [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/representation_learning|Representation Learning]], [[themes/scaling_laws|Scaling Laws]], [[themes/software_engineering_agents|Software Engineering Agents]], [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Overview

Chinchilla scaling laws established that, for a fixed compute budget, model size and training token count should scale roughly in proportion, overturning prior assumptions that favored larger, undertrained models. This framework became the dominant lens through which the industry plans training runs.

What makes the Chinchilla regime interesting as a research object is precisely where it stops. It governs the FLOPs-and-data surface but says nothing about the geometry of information flow inside the network, the efficiency of hardware access patterns, or how compute can be shifted from training to inference. Recent architectural work treats these blind spots as opportunities. Hyper-Connections (HC) and its successor mHC: Manifold-Constrained Hyper-Connections position residual stream width as a complementary scaling axis: by expanding the width of the residual stream and enhancing connection topology, HC increases representational capacity without altering per-unit FLOPs, effectively decoupling information capacity from layer input dimension. This is a dimension the traditional scaling laws are structurally silent on.

## Residual Stream Width as a New Scaling Axis

The residual connection has been architecturally stable for over a decade. Though the residual function evolved from convolutions to attention and feed-forward networks, the connection itself retained its original form. Early research (He et al., 2016) established that the identity mapping property of the residual connection is what maintains training stability and efficiency at scale, and this property has been treated as inviolable.

HC challenges that conservatism by replacing the identity with a learnable mapping matrix over the residual stream, which widens it without adding FLOPs. The cost is that the identity mapping property is compromised. When HC is stacked across layers, the composite residual mapping deviates from identity, causing signal magnitude to either explode or vanish as depth increases. This instability restricted HC's scalability in practice.

mHC resolves this by treating the residual mapping as a manifold-constrained optimization problem. It uses the Sinkhorn-Knopp algorithm to project the residual mapping matrix onto the Birkhoff polytope, the set of doubly stochastic matrices. A doubly stochastic matrix, having all row and column sums equal to one, makes the residual operation a convex combination of input features, which conserves feature mean and strictly regularizes signal norm. Crucially, doubly stochastic matrices are closed under multiplication, so the conservation property holds through the full depth of the network regardless of how many HC layers are stacked. This is the key structural fix: not just constraining individual layers but guaranteeing compositional stability.

## Hardware Efficiency and Practical Overhead

Widening the residual stream introduces memory access costs that the original HC design left unaddressed, and this gap restricted practical scalability independently of the FLOPs argument. mHC addresses this through kernel fusion and mixed-precision kernels via TileLang, and it overlaps communication within the DualPipe schedule while using selective recomputation to manage memory footprint. The result is that mHC introduces only 6.7% additional time overhead at expansion rate n=4 compared to a baseline without HC, which is low enough to make the scaling axis economically plausible.

## Inference-Time Compute as a Complementary Frontier

The pre-training scaling law framework is fundamentally about training-time compute. OpenAI's work on o1 represents the clearest industrial signal that the scaling frontier has shifted in part toward inference time. O1 is OpenAI's first major foray into general inference-time compute, using search and extended chain-of-thought during generation rather than relying solely on what was baked in during training. This is not a replacement for pre-training scaling laws but a supplementary regime: training-time and inference-time compute interact, and the optimal allocation between them is not captured by Chinchilla's framework.

## Open Questions and Limitations

The mHC line of work establishes theoretical grounding for residual stream width as a scaling dimension, but empirical validation at the scale where pre-training laws are typically evaluated remains an open question. The efficiency claims are demonstrated at particular expansion rates; how overhead scales with larger n or at frontier model sizes is not yet established.

More broadly, pre-training scaling laws describe a surface, not a ceiling. Width, inference compute, and hardware efficiency are three dimensions that sit orthogonal to the FLOPs-and-tokens axes. Whether these yield comparable predictable power laws, or whether they are more irregular and architecture-dependent, is an active open question that spans [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/model_architecture|Model Architecture]], and [[themes/compute_and_hardware|Compute and Hardware]].

## Related Entities

- mHC: Manifold-Constrained Hyper-Connections (primary source for HC/mHC framing)
- OpenAI on o1 and Inference-Time Compute (test-time scaling as complementary frontier)
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]
- [[themes/compute_and_hardware|Compute and Hardware]]

## Key Findings

## Limitations and Open Questions

## Relationships

## Sources
