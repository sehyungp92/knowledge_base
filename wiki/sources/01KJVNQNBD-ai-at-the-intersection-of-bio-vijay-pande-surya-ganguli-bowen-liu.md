---
type: source
title: AI at the Intersection of Bio | Vijay Pande, Surya Ganguli & Bowen Liu
source_id: 01KJVNQNBDEW0S74TBEHBM8K6Z
source_type: video
authors: []
published_at: '2024-10-03 00:00:00'
theme_ids:
- medical_and_biology_ai
- model_architecture
- multimodal_models
- representation_learning
- scientific_and_medical_ai
- unified_multimodal_models
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AI at the Intersection of Bio | Vijay Pande, Surya Ganguli & Bowen Liu

A panel discussion examining how deep learning transformed computational drug discovery — from the historical arc of physics-based and expert-system methods through the self-supervised revolution — with frank assessment of where AI genuinely works, where it fails systematically, and what bottlenecks must be resolved before AI-discovered drugs reach patients at scale.

**Authors:** Vijay Pande, Surya Ganguli, Bowen Liu
**Published:** 2024-10-03
**Type:** video

---

## Historical Arc: From Physics to Deep Learning

Computational chemistry and biology have existed for roughly 40 years, organized around two opposing camps. **Physics-based methods** started from first principles and were highly generalizable, but prohibitively expensive for the molecular scales relevant to drug discovery. **Expert systems** encoded human heuristics and were computationally efficient once built, but failed to generalize beyond their encoded rules.

Early ML methods fell between these extremes — learning from data to generalize better than rules — but still required hand-engineered input features (e.g., how to represent a molecule). Deep learning eliminated this bottleneck by learning representations directly from raw data, letting the algorithm discover what matters for each task.

The deep learning revolution was driven by three converging forces: massive datasets, improved algorithms, and self-supervised learning on unlabeled data. GPT-4's training corpus — ~5 trillion unique token sequences — would take a human 20,000 years to read; it was trained solely to predict the next word, yet the learned representations generalize across tasks.

---

## Scale of Biological Data

The panel offers a revealing data comparison across biological modalities:

| Modality | Scale |
|---|---|
| GPT-4 training | ~5 trillion tokens |
| ESM3 (protein sequences) | ~2.8 billion sequences / ~1 trillion tokens |
| Protein Data Bank (3D structures) | ~200,000 solved structures |
| Single-cell transcriptomes | ~36 million cells |

A striking observation: **evolution produced less protein sequence text than humans left on the internet**. This asymmetry has direct consequences — protein sequence models can be trained at near-language-model scale, but 3D structural data remains sparse, and small molecules lack even an evolutionary generative process to mine.

See [[themes/representation_learning|Representation Learning]] for the broader context of scale effects on learned representations.

---

## Capabilities

### What Is Now Solved

**Protein structure prediction** underwent a phase transition. [[themes/scientific_and_medical_ai|AlphaFold]]/AlphaFold2 and RoseTTAFold converted a 50-year-old fundamental problem into something "arguably pretty much solved for a lot of common protein types." This is paradigm-shifting: structure prediction was previously so hard it warranted its own biennial competition (CASP); it is now a commodity tool.

**AlphaFold 3** extends this to ligand-protein binding prediction (docking), directly enabling small molecule drug design — though its code was not publicly released, limiting independent validation.

**ESMFold and ESM3** transferred the self-supervised language modeling approach to protein sequences. Training on 2.8 billion amino acid sequences without labeled data produces representations that encode meaningful biology and support downstream drug discovery tasks. See [[themes/model_architecture|Model Architecture]] for the self-supervised framing.

**Foundation models for cell biology**, trained on 36 million single-cell gene expression profiles, create interpretable latent spaces of cellular states. These models can embed held-out species coherently and model how drugs shift cells through biological state space — a computational substrate for understanding drug mechanism.

**Generative molecular design** using diffusion models with classifier guidance can produce novel molecules with pre-specified properties, shifting the paradigm from *prediction* (given molecule, predict property) to *inverse design* (given desired property, generate molecule). Some systems achieve 20-30% positive hit rates on generated candidates.

**ChatGPT** is cited as the inflection point that demonstrated qualitatively unexpected capabilities — a reference to the broader shift in what language models can do that now animates the transfer to biology.

---

## Limitations and Open Problems

### Fundamental Generalization Failure

> "The biggest failure mode of ML is that it can't really do out-of-distribution generalization."

This is not a minor caveat — it is the central limiting principle. AlphaFold exemplifies it concretely: for the 50 most common ligands (appearing >100 times in the Protein Data Bank), AlphaFold performs well. For less common ligands, physics-based methods outperform it by 8%. The model has memorized distribution; it has not learned physics.

This has deep implications for [[themes/scientific_and_medical_ai|drug discovery]]: novel chemistry, rare protein families, and unprecedented binding modes are precisely the cases where AI fails, while being precisely the cases of greatest scientific interest.

### The Labeled Data Problem

Supervised learning requires thousands to millions of labeled examples; a typical drug discovery project has ~100 labeled actives. Self-supervised pre-training helps but does not fully close this gap — especially for small molecules, which have **no natural self-supervised signal**. Protein sequences carry evolutionary information that can drive pre-training; small molecules do not have an equivalent generative process. This is a structural asymmetry, not merely a data collection problem.

### Validation as the True Bottleneck

Generating molecular candidates is no longer the hard step. Testing them is. Unlike image or text generation (where quality can be assessed immediately), molecular candidates require:

1. Synthesis (expensive, sequential, not parallelizable at scale)
2. Laboratory testing (wet-lab binding assays, cell assays)
3. Multi-objective filtering (potency, selectivity, solubility, non-toxicity, synthesizability must all be satisfied simultaneously)

Current AI systems generate candidates faster than labs can evaluate them. The **20-30% false positive rate** on claimed active compounds means that even in the best current systems, 70-80% of experimental effort is wasted on model errors.

### Biological Understanding as the Phase 2/3 Wall

The most structurally important limitation: **80% of drugs fail Phase 2/3 clinical trials not because of toxicity but because of incorrect target selection**. AI cannot fix this by improving molecular design; it requires better mechanistic understanding of disease biology. This is the bottleneck with the longest resolution horizon and the least tractable path. See [[themes/medical_and_biology_ai|Medical and Biology AI]] for related discussion.

### Clinical Trial Infrastructure

80% of clinical trials fail to meet enrollment targets due to poor patient recruitment and retention — a logistics and health systems failure, not a modeling failure. AI can help (EMR screening, biomarker-based patient matching, heterogeneity reduction), but regulatory interpretability requirements create an additional constraint: FDA regulators require explainable patient selection decisions, and current AI systems lack sufficient interpretability for this use case.

### Access and Reproducibility

AlphaFold 3's closed release is flagged explicitly: the academic community cannot independently stress-test it, assess edge cases, or extend it. This is a recurring tension in [[themes/scientific_and_medical_ai|scientific AI]] — between commercial incentives and the open science norms that validate and accelerate progress.

---

## The Drug Discovery Cost Curve

The economic backdrop makes the stakes clear: **$2.5 billion per approved drug over 10-15 years, with 90% candidate failure rates**. Productivity is falling — drugs approved per billion dollars spent halves every 9 years (Eroom's Law). FDA-approved drugs target only 800 of 20,000-25,000 known human genes; the unexplored therapeutic space is vast.

AI for drug discovery is "no longer a question of *if*, but *how* it gets deployed" — but deployment at scale requires resolving the validation bottleneck, the out-of-distribution generalization failure, and the upstream biological understanding gap simultaneously.

---

## Anticipations and Open Questions

- **Will self-supervised learning analogues emerge for small molecules?** Protein sequences have evolutionary history as a generative signal; finding an equivalent for molecular design would be a foundational advance.
- **Can AI accelerate target identification, not just molecular design?** The 80% Phase 2/3 failure rate suggests this is the higher-leverage intervention.
- **Will automated synthesis and high-throughput screening close the validation bottleneck?** The limiting factor is lab throughput, not computational generation — this points toward robotics and automation as the necessary complement to ML.
- **Can foundation models for cell biology predict clinical outcomes from in vitro data?** Single-cell transcriptomics models that model drug effects on cellular states are a promising path toward reducing the 80% clinical failure rate.

---

## Connections

- [[themes/representation_learning|Representation Learning]] — self-supervised pre-training on biological sequences; transfer learning from language to biology
- [[themes/model_architecture|Model Architecture]] — ESMFold/ESM3 architecture; diffusion models with classifier guidance for inverse design
- [[themes/scientific_and_medical_ai|Scientific and Medical AI]] — protein structure prediction, drug discovery pipeline, clinical trial AI
- [[themes/medical_and_biology_ai|Medical and Biology AI]] — biological foundations; iPSC-based personalized medicine; clinical translation
- [[themes/multimodal_models|Multimodal Models]] — multi-modality of biological data (sequence, structure, expression, clinical)

## Key Concepts

- [[entities/alphafold|AlphaFold]]
- [[entities/chatgpt|ChatGPT]]
- [[entities/diffusion-models|Diffusion Models]]
- [[entities/foundation-model|Foundation Model]]
- [[entities/protein-data-bank|Protein Data Bank]]
- [[entities/self-supervised-learning|Self-Supervised Learning]]
- [[entities/variational-autoencoder|Variational Autoencoder]]
