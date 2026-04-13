---
type: source
title: AI in Pharmaceutical R&D with Kim Branson
source_id: 01KJVNQMNSTW6KEZ69N6GDMX73
source_type: video
authors: []
published_at: '2024-08-01 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- medical_and_biology_ai
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AI in Pharmaceutical R&D with Kim Branson

Kim Branson (GSK's SVP of AI/ML) provides a practitioner's view of how machine learning is embedded across the full drug discovery pipeline — from target identification using population genomics, through active learning for experimental design, to computational pathology and heavily instrumented clinical trials. The source is notable for its candid treatment of where AI genuinely helps versus where it remains limited, its emphasis on outcome data as the true rate-limiting resource, and its grounding thesis that measurement technology cost drives medical progress.

**Authors:** Kim Branson
**Published:** 2024-08-01
**Type:** video

---

## Expert Analysis

### Target Identification and Genetics

The pipeline begins with selecting what to modulate. GSK draws on large genetic databases pairing sequenced individuals with their medical records, using genome-wide association studies (GWAS) to identify variants statistically associated with disease risk or quantitative traits. ML extends this in two directions: first, generating the quantitative traits themselves — for instance, scoring liver scarring or kidney function from clinical imaging rather than relying on manual radiologist annotation; second, predicting *directionality* of identified variants (does this variant increase expression, decrease it, or alter splicing?). Without directionality prediction, every candidate variant would require bespoke experimental validation — a combinatorial bottleneck that makes unassisted human analysis intractable.

### Active Learning for Experimental Design

Rather than random screening, GSK runs an active learning system that ingests genetics hypotheses, literature signals, and experimental results to recommend which perturbations to test next. This achieves approximately 20% faster discovery than random screening. The system operates in a continuous loop: results filter back in, the model updates, and the next experimental batch is prioritised. The combinatorial argument is stark — a genome-wide exhaustive screen is simply not feasible, so intelligent prioritisation is not an optimisation but a prerequisite.

### Computational Pathology

In clinical trials, ML is used to quantify protein target expression in tissue slides — counting stained pixels and, crucially, attributing expression to specific cell types. This replaces subjective pathologist scoring, which is inherently ordinal and cannot reliably distinguish cell-type-specific signals. Once cell-type-level expression data is paired with trial response outcomes, iterative model refinement can identify which cellular contexts predict treatment response.

### Instrumented Phase 2 Trials and Patient Stratification

GSK ran heavily instrumented Phase 2 trials measuring far more proteomics, imaging, and genomic signals than standard trials. From this data, a subpopulation was identified in which patients are functionally cured when viral surface antigen drops below a specific threshold. This exemplifies the broader strategy: collect more than you think you need, accept that most signals will be uninformative, and use ML to extract the subset that matters. The limitation is patient burden — over-instrumenting trials is ethically and practically constrained.

---

## Key Claims

1. The anti-influenza drug Relenza was the first drug designed using computational methods (the Goodford GRID program for protein surface mapping).
2. GSK uses ML in production to predict directionality of genetic variants — whether they increase or decrease expression or alter splicing.
3. GSK's active learning system for target discovery is **~20% faster** than random screening.
4. ML on clinical imaging generates continuous quantitative traits (liver scarring, kidney function) without manual radiologist scoring.
5. Computational pathology can quantify per-cell-type protein expression from histopathology slides, surpassing human pathologist scoring.
6. A heavily instrumented Phase 2 trial identified a subpopulation functionally cured when viral surface antigen drops below a threshold.
7. Only ~20% of patients respond to immunotherapy (IO), despite remarkable responses in that subset.
8. GSK generates large-scale perturbational genomics datasets intended to serve as both lookup tables and inference systems for in silico prediction.
9. GSK has experienced exponential data growth since Branson joined (~5 years prior to recording).
10. **Data with clinical outcomes is the true rate-limiting step** — biological data is generatable at scale; matched outcomes are not.
11. Pharmaceutical companies hold a unique advantage: they can generate outcome data in humans at scale through clinical trials, ethically and safely.
12. AI became useful in biology primarily because measurement technologies (sequencing, RNA-seq, single-cell) became cheap, generating high-dimensional data requiring ML to interpret.
13. Branson's central hypothesis: medicine advances when new measurement technologies become cheaper.
14. ML has made its largest strides where data collection is cheap (web search, image recognition) — the same dynamic now applies to biology.
15. More data with a simple algorithm is more effective and easier to sell than sophisticated algorithms with less data.

---

## Capabilities

| Capability | Maturity | Notes |
|---|---|---|
| Genetic variant identification and directionality prediction from population genomics | broad_production | Core to GSK's target identification pipeline |
| Automated ML histopathology — per-cell-type protein quantification | broad_production | Replaces manual pathologist scoring |
| Active learning for experimental prioritisation | narrow_production | ~20% speedup vs. random screening |
| Small molecule phenotypic effect prediction from cellular imaging | narrow_production | Similar to Recursion-style high-content screening |
| Multi-omics patient stratification in instrumented clinical trials | narrow_production | Identified functionally-cured subpopulation |
| LLM-based email/report summarisation and Q&A | demo | Branson's personal productivity tooling |
| Multi-document scientific reasoning with language models | demo | Prototype written by Branson himself |

---

## Limitations and Open Questions

### Blocking Limitations

- **High-dimensional data interpretation** — humans cannot make sense of gene expression arrays fluctuating around baseline versus disease; the dimensionality makes unaided interpretation impossible.
- **Genome-wide perturbation tractability** — exhaustive testing of all gene combinations is computationally and experimentally intractable; active learning mitigates but does not solve this.
- **Outcome data scarcity** — unlimited genomics and functional assay data can be generated, but data paired with real clinical outcomes is the rarest and most valuable resource, and cannot be manufactured quickly.

### Significant Limitations

- **Retrospective cohort measurement gaps** — longitudinal cohorts measured only what was affordable and hypothesised at collection time; new questions cannot be answered retroactively.
- **Disease heterogeneity** — why patients respond differently to the same therapy remains poorly understood despite ML advances.
- **ML evaluation culture** — many papers report third-decimal improvements without characterising uncertainty or practical significance thresholds; robustness criteria are under-specified.
- **Distribution shift in deployment** — models trained on specific data distributions fail when deployed across heterogeneous real-world systems.
- **Immune system temporal dynamics** — how immune profiles evolve over time in health and disease remains poorly characterised.
- **MLOps underestimation** — monitoring, retraining, and controlling for model drift in production is poorly standardised and its operational burden is systematically underestimated.
- **Patient burden in trials** — comprehensive multi-modal measurement conflicts with patient welfare constraints; this tension limits how much instrumentation is ethically feasible.

### Open Questions

- When will ML-derived mechanistic insights collide productively with mechanistic modelling of biology (systems medicine)?
- Can perturbational genomics datasets scale to the point where a full experiment is replaceable by inference?
- What does healthy immune system dynamics actually look like over time at single-cell resolution?

---

## Landscape Contributions

### Bottlenecks

**Outcome-paired clinical data** (blocking, 3–5 year horizon) — The most fundamental bottleneck. Perturbational data is generatable at scale; data with matched clinical outcomes is not. Pharmaceutical companies are structurally advantaged here because they can generate this data through trials, but the process is slow, expensive, and ethically constrained.

**Expert annotation for high-dimensional clinical data** (blocking, 1–2 year horizon) — Histopathology and medical imaging require manual expert labels to bootstrap automated systems. Automating label generation itself is the near-term unlock.

**Multi-modal data integration** (blocking, 3–5 year horizon) — Genetics, electronic medical records, proteomics, imaging, and longitudinal follow-up exist in incompatible formats and platforms. Unified disease models require integration standards that do not yet exist at scale.

### Breakthroughs

**Perturbational genomics as inference systems** (major) — The shift from treating CRISPR and morphology profiling datasets as lookup tables to using them as inference systems for predicting phenotypic effects of unseen perturbations represents a qualitative change in what in silico biology can do.

**Quantitative computational pathology** (major) — Replacing subjective ordinal pathologist scoring with automated per-cell-type protein quantification enables downstream analyses (patient stratification, response prediction) that were previously impossible at scale.

---

## Themes

- [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]]
- [[themes/medical_and_biology_ai|Medical and Biology AI]]
- [[themes/scientific_and_medical_ai|Scientific and Medical AI]]

---

## Startup and Strategy Implications

Branson's advice to startups distils to a single principle: **unique data is the moat, not the algorithm**. Common failure modes include using proxy data (data adjacent to, but not actually measuring, the target phenomenon) and lacking the ability to generate more data when public sources are exhausted. The ideal position is being paid to generate data by a partner, then selling the model built on it — arriving at the table with both proprietary and public data.

On algorithms: point estimates are insufficient. Robustness and reliability criteria must be characterised, uncertainty must be quantified, and the threshold for "meaningfully different" must be explicitly defined before deployment.

The five-year prediction: every approved drug will have companion software specifying which patients should use it and under what conditions — a direct consequence of the patient stratification capabilities now entering production.

## Key Concepts

- [[entities/long-context-window|Long Context Window]]
