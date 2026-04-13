---
type: entity
title: Protein Data Bank
entity_type: dataset
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- medical_and_biology_ai
- model_architecture
- multimodal_models
- pretraining_and_scaling
- representation_learning
- scientific_and_medical_ai
- software_engineering_agents
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.00041759314876379453
staleness: 0.0
status: active
tags: []
---
# Protein Data Bank

> The Protein Data Bank (PDB) is the world's primary open-access repository for experimentally determined three-dimensional structures of biological macromolecules, containing approximately 200,000 structures as of recent discussion. It has served as the foundational training and validation corpus for structural AI models — most notably AlphaFold2, whose success in predicting protein structure from sequence alone earned Demis Hassabis and John Jumper the 2024 Nobel Prize in Chemistry — making it one of the most consequential scientific databases in the history of AI-for-biology.

**Type:** dataset
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/multimodal_models|multimodal_models]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/representation_learning|representation_learning]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/unified_multimodal_models|unified_multimodal_models]]

## Overview

The Protein Data Bank is a curated, community-maintained archive of atomic-resolution structures solved primarily via X-ray crystallography, cryo-electron microscopy, and NMR spectroscopy. Each entry records not just coordinates but experimental metadata, resolution quality, and ligand interactions — making it a richly annotated substrate for supervised and self-supervised learning on molecular geometry. Its open-access model has been foundational to the broader open science ethos that characterises the most productive corners of computational biology.

What distinguishes PDB from most biological datasets is the density and precision of its annotation: every structure is a ground-truth spatial map, not an inferred or imputed signal. This made it uniquely suitable as the training target for structure prediction models, culminating in AlphaFold2's near-perfect performance on CASP14 benchmarks. The 2024 Nobel recognition of both protein structure prediction (Hassabis and Jumper) and protein design (David Baker) explicitly cited AI methods, marking a watershed moment for the field and retroactively validating the PDB's decades-long data curation effort.

## Key Findings (claims mentioning this entity)

The sources engaging with PDB do so primarily as a point of contrast — illustrating both what structured biological databases have achieved and where the frontier is moving. The Nobel prizes awarded in 2024 for AI contributions to biology are the most direct signal: structure prediction, built on PDB data, is now considered a solved problem in the same breath as canonical scientific breakthroughs. This framing, noted in discussion of the Arc Institute's work, signals that the field is pivoting from *structure* (where PDB was the bottleneck) to *function and perturbational response* (where datasets like Tahoe 100 are now the frontier).

The contrast with single-cell perturbational data is instructive. Before Tahoe 100, all publicly available perturbational single-cell datasets combined amounted to only 1–2 million data points — a scale problem analogous to the pre-PDB era of structural biology, when structures were too sparse to train generalizable models. Tahoe 100's 100 million single-cell RNA sequencing data points across 60,000 drug–cell line interactions represents an attempt to do for functional genomics what the PDB did for structural biology: create a dataset large enough to train models that genuinely generalise. The parallel is not accidental; Arc Institute researchers explicitly frame large-scale perturbational datasets as the missing precondition for building credible virtual cell models, echoing the role PDB played in enabling AlphaFold.

The EVO2 model — trained on 9.3 trillion nucleotides with no explicit biological supervision — represents a further departure from PDB-style supervised learning. Where AlphaFold required the PDB's experimental ground truth to learn structure, EVO2 learns sequence-level biology purely from DNA statistics. This raises a live question about the relative importance of curated, high-precision datasets (PDB's model) versus massive, lightly annotated sequence data (EVO2's model) as the two paradigms compete for explanatory power across different prediction tasks.

## Limitations and Open Questions

The PDB's ~200,000 structures, while a remarkable scientific achievement, represent a vanishingly small sample of protein sequence space — estimates suggest the space of possible proteins is astronomically larger. This coverage gap is one reason sequence-based models like EVO2 and ESMFold seek to bypass the structural bottleneck by learning functional representations without requiring experimental coordinates.

A deeper limitation is that PDB captures static snapshots: structures solved under idealised, non-physiological conditions that may not reflect the dynamic conformational landscapes proteins occupy in living cells. This gap between crystallographic truth and biological reality is a known source of model failure when structural predictions are applied to drug design or mechanistic interpretation.

The field also lacks accepted benchmarks for evaluating virtual cell models — a striking contrast to structural biology, where CASP competitions provided rigorous, community-agreed evaluation standards that the PDB made possible. The absence of an equivalent benchmark for functional prediction tasks (differentially expressed gene prediction, drug response modelling) means that even the best current models — reportedly achieving only ~10% accuracy on predicting differentially expressed genes — cannot be meaningfully compared or validated at scale. Whether a PDB-equivalent for perturbational biology (potentially Tahoe 100 or its successors) could seed a CASP-like benchmark ecosystem remains an open question.

## Relationships

- No Priors Ep. 103 | With Vevo Therapeutics and the Arc Institute — Tahoe 100 and the data scale problem in functional genomics, implicitly framing PDB's structural success as a model to replicate
- Arc Institute's Patrick Hsu on Building an App Store for Biology with AI — Nobel prize context for protein structure prediction and design; EVO2 open-source release
- AI at the Intersection of Bio | Vijay Pande, Surya Ganguli & Bowen Liu — broader landscape of AI-biology intersection, including structural foundations
- Related entities: AlphaFold2 (primary consumer of PDB as training data), Tahoe 100 (attempted functional analogue), EVO2 (sequence-native alternative paradigm), CASP (benchmark ecosystem enabled by PDB)

## Sources
