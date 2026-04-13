---
type: entity
title: UMAP
entity_type: method
theme_ids:
- adaptive_computation
- latent_reasoning
- model_architecture
- multimodal_models
- pretraining_and_scaling
- reasoning_and_planning
- representation_learning
- scaling_laws
- transformer_alternatives
- unified_multimodal_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00030008288459644646
staleness: 0.0
status: active
tags: []
---
# UMAP

> Uniform Manifold Approximation and Projection (UMAP) is a dimensionality reduction technique that projects high-dimensional data onto lower-dimensional spaces while preserving topological structure. Within the knowledge sources here, it plays a key role as a diagnostic and visualization lens — most prominently in the analysis of Continuous Thought Machines, where UMAP reveals emergent geometric structure in neural dynamics that would otherwise be invisible.

**Type:** method
**Themes:** [[themes/representation_learning|representation_learning]], [[themes/model_architecture|model_architecture]], [[themes/adaptive_computation|adaptive_computation]], [[themes/latent_reasoning|latent_reasoning]]

## Overview

UMAP operates on a foundational insight shared across the sources here: high-dimensional data is not uniformly distributed through its ambient space, but concentrates on lower-dimensional manifolds. The MNIST example from AI can't cross this line and we don't know why. illustrates this directly — handwritten digit images formally live in 784-dimensional space (28×28 pixels), but the set of *valid* digits occupies a far smaller manifold within that space. UMAP's purpose is to find and flatten that manifold into something human-interpretable.

In the context of the Continuous Thought Machines paper, UMAP serves a more specific and revealing function: it is applied to the CTM's neuron activation trajectories over internal time — the sequence of pre-activation states across ticks — to produce two-dimensional projections of how individual neurons evolve through a forward pass. The result is not random or static: UMAP visualizations of CTM dynamics expose **emergent traveling wave phenomena**, coherent spatial patterns of activation that propagate across the network without being explicitly trained. This is a property of the architecture's temporal depth, not of any hand-crafted inductive bias.

## Role in the CTM Architecture

The CTM assigns each neuron its own privately parameterized neuron-level model (NLM) — a depth-1 MLP that processes that neuron's M-dimensional history of pre-activations. The internal time dimension `t ∈ {1, ..., T}` is decoupled from data dimensions entirely, enabling iterative refinement even over static inputs. This produces activation trajectories: each neuron traces a path through representation space as ticks accumulate.

UMAP makes those paths legible. By projecting the full trajectory space into two dimensions, the visualization reveals that neurons are not behaving independently — they are participating in structured, wave-like dynamics across the network. This is not a designed feature; it is a geometric consequence of the NLM architecture operating over shared internal time. The traveling waves are, in this sense, a form of emergent coordination.

This matters for interpreting the CTM's adaptive computation mechanism. The model's loss function selects two ticks per data point — the tick of minimum loss and the tick of maximum certainty — without restricting which ticks are eligible. UMAP visualizations help ground the intuition that these selected ticks are not arbitrary: they correspond to moments in a structured internal trajectory, not noise.

## Connections to Representation Geometry

The Platonic Representation Hypothesis (referenced in the source list) invokes related ideas at a different scale — the claim that sufficiently capable models trained on different modalities and architectures converge toward similar representations of the world. UMAP and analogous projection methods are the primary tools used to make such convergence claims visible, mapping high-dimensional representation spaces onto geometries that can be compared across models.

Both uses share a common epistemic structure: UMAP is deployed not to *build* representations but to *audit* them — to test whether structure claimed to exist in high-dimensional space is real and geometrically coherent, or an artifact of training noise.

## Limitations and Open Questions

UMAP's role here is purely diagnostic; it contributes no knowledge to the model's representations and introduces its own distortions. Projection from high-dimensional manifolds to two dimensions necessarily loses information, and the traveling waves visible in UMAP plots may not fully represent the geometry of the original trajectory space. Whether the emergent patterns are causally significant — whether they *drive* good performance or merely accompany it — cannot be answered by visualization alone.

The CTM paper is explicit that its experiments are preliminary, favoring breadth over depth, and not intended to establish state-of-the-art results. UMAP evidence of traveling waves is accordingly suggestive rather than conclusive: it motivates further investigation into whether temporal neural dynamics are a useful design axis, but does not resolve whether wave-like coordination is necessary, sufficient, or incidental to the CTM's behavior.

More broadly, the interpretive reliance on UMAP across representation learning research raises a methodological question: claims about representational convergence or emergent structure depend heavily on the choice of projection algorithm, distance metric, and hyperparameters. UMAP results are not ground truth about high-dimensional geometry — they are one view of it, shaped by choices that are rarely the focus of ablation.

## Relationships

UMAP is applied directly in the analysis of the Continuous Thought Machines, where it surfaces traveling wave dynamics in CTM neuron trajectories. The manifold intuition it operationalizes is illustrated concretely in AI can't cross this line and we don't know why. through the MNIST example. The Platonic Representation Hypothesis uses analogous projection methods to argue for cross-model representational convergence, placing UMAP within the broader toolkit of [[themes/representation_learning|representation learning]] auditing. As a visualization method, UMAP connects to the CTM's core themes of [[themes/adaptive_computation|adaptive computation]] and [[themes/latent_reasoning|latent reasoning]] by making the internal temporal dynamics of thinking machines legible.

## Key Findings

## Sources
