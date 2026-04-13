---
type: source
title: Arc Institute's Patrick Hsu on Building an App Store for Biology with AI
source_id: 01KJVNVKAH2BZK8Y57QC5CAEFY
source_type: video
authors: []
published_at: '2025-04-15 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- medical_and_biology_ai
- pretraining_and_scaling
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Arc Institute's Patrick Hsu on Building an App Store for Biology with AI

> Patrick Hsu (Arc Institute) argues that evolution is biology's unifying theory and that genomic foundation models — specifically the Evo series — can exploit this by learning directly from evolutionary signal in DNA sequences. The source maps the present capabilities and hard structural limits of AI-driven biology, articulating why drug development timelines remain largely unchanged despite computational advances, why species-translation failure is endemic, and how a fragmented health data ecosystem prevents personalised medicine. Alongside these constraints, Hsu introduces EVO2 as a concrete breakthrough in mutation-effect prediction and CRISPR system design, and sketches an "app store" model in which biological foundation models underpin an ecosystem of domain-specific tools.

**Authors:** Patrick Hsu (Arc Institute)
**Published:** 2025-04-15
**Type:** video

---

## Evolution as Biology's Unifying Theory

Where physics has multiple competing frameworks, biology has one: evolution. This is the foundational premise from which the Evo model series is derived. Evolution propagates the effects of natural selection through generations via DNA mutations, making the relationship between DNA sequences and their functional consequences the master key to biological understanding.

> *"We have this in biology and it's so obvious that we find it, you know, sort of an just an obvious foundation."*

The Evo models operationalise this by treating genome sequences the way large language models treat text — using autoregressive next-base prediction to learn higher-order biological patterns. Just as LLMs learn grammar, syntax, and semantics without being told the rules, Evo learns the molecular logic underlying cell function by predicting the next base or amino acid residue. The 2024 Nobel Prizes for protein structure prediction (Demis Hassabis, John Jumper) and protein design (David Baker) validated the sequence-modelling paradigm for proteins; Evo extends it to the full genome — including RNA, regulatory DNA, and everything else needed to make life.

---

## What EVO2 Does

EVO2 is an autoregressive multi-convolutional hybrid model trained on entire genomes with a long context window, enabling it to reason over all bases and molecules embedded across genomic sequences. Its architecture is designed for efficiency at scale while preserving the long-range dependencies that matter for genomic function.

**Demonstrated capabilities:**

- **Mutation effect prediction at scale.** When a genome is sequenced, most discovered mutations are "variants of unknown significance" (VUS) — neither confirmed pathogenic nor benign. EVO2 was evaluated against ClinVar, the gold-standard database of known disease-causing mutations, using BRCA1 (the breast/ovarian cancer gene) as the benchmark. It achieved state-of-the-art performance in classifying VUS as pathogenic or benign — a task with direct clinical decision-making implications. See [[themes/medical_and_biology_ai|Medical and Biology AI]].

- **CRISPR system design.** EVO2 can design novel CRISPR gene-editing systems at the DNA level, going beyond predicting the effects of existing sequences to generating new functional ones.

- **Full IgG antibody design.** The model can design full immunoglobulin G antibodies by specifying CDR regions predicted to bind targets with high affinity — currently at demonstration maturity.

- **Autonomous data curation agents.** Arc's Virtual Cell Atlas — the world's largest single-cell dataset — was built using autonomous agents that crawl biological databases, process unstructured metadata, and systematically reanalyse data without human intervention. This is a parallel breakthrough: AI as infrastructure for scientific data organisation, not just analysis.

The model is open source, enabling an "app store" ecosystem where third parties build specialised tools on top of the genomic foundation layer — directly analogous to how LLM APIs underpin product ecosystems across software.

---

## The Hard Structural Limits

Hsu is unusually direct about what AI cannot yet do in biology, and this is where the source is most analytically valuable.

### Drug Development Is Not the Bottleneck AI Can Solve

The primary bottleneck in bringing an AI-designed drug to patients is not the design step — it is everything that follows. Even with a perfect computational drug design, candidates must progress through:

1. Animal model testing (mouse, rat, primate)
2. Toxicity and pharmacokinetics studies
3. Phase I/II/III human clinical trials
4. FDA regulatory review

This pipeline takes 5–10 years and cannot be parallelised without predictive power the field does not yet have. The 10% industry probability of success (PoS) is the root cause: regulators scrutinise safety intensely precisely because compounds fail so often. Improving PoS from 10% to 20–30% would meaningfully change regulatory calculus and development economics, but that threshold has not been crossed. See [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]].

### The Species Translation Gap

> *"You can model the mouse in all of its glory to great perfection. It still will not be the human."*

Compounds that work in cell lines and mice fail in humans with alarming regularity. Current models — including EVO2 — cannot reliably predict human outcomes from animal data. This is not a gap that scaling alone closes; the fundamental biological complexity of human organisms is not captured by proxy systems, and human experimentation is constrained by regulatory and ethical limits that are unlikely to change substantially.

### The Absence of Predictive Power

The most direct statement of the core limitation:

> *"A model with even a modicum of predictive value would be transformative... which by the way we don't have right now."*

Because predictive power is absent, drug development must proceed sequentially through each validation stage rather than in parallel. If predictive models existed, candidates that will ultimately fail could be eliminated early, and the pipeline could be restructured. The absence of this power is what makes the entire sequential architecture of drug development a rational response to uncertainty rather than bureaucratic inertia.

### The Missing Experimental Record

Scientific literature documents what worked. It almost never documents what didn't — the failed hypotheses, abandoned experimental paths, and negative results that constitute the majority of actual scientific work.

> *"The missing reasoning trace in the scientific literature is you don't know what didn't work."*

This creates a fundamental training data problem for reasoning models trying to learn scientific methodology. Current datasets support extraction of claims but not the full distribution of experimental outcomes needed for end-to-end autonomous scientific reasoning. This bottleneck is classified as 1–2 year horizon precisely because the solution is largely organisational and incentive-based rather than technical.

### Fragmented Health Data

Personalised medicine requires integrating genomics, real-time biomarkers, behavioural data, and clinical outcomes. These datasets exist in incompatible silos across institutions, research groups, and health systems. No integrated platform for genotype-environment-phenotype modelling exists at scale, creating a structural gap between what AI could do with integrated data and what it can do with current fragmented inputs. Horizon: 1–2 years.

### The Bilingual Talent Shortage

There are far more pure ML researchers and far more pure biologists than researchers with genuine depth in both. This "bilingual" expertise — the ability to translate between statistical learning frameworks and biological mechanisms — is the rare resource that powers effective AI-driven biology research. The bottleneck is improving as training pipelines mature, but remains significant.

---

## Evaluation Design as a Hidden Cost

A recurring theme is that when a genuinely new model capability is developed, new evaluations must also be created from scratch. Existing benchmarks may not test the right things, and the field faces a dual problem: benchmarks are expensive to design, and once they exist, models are optimised toward them rather than toward underlying scientific goals. This meta-problem — the cost and validity of biological AI evaluation — is underappreciated relative to the attention paid to model architecture.

---

## The App Store Vision

The central organising metaphor: biological foundation models as platforms on which an ecosystem of domain-specific applications is built. Just as iOS or Android abstract hardware complexity and provide APIs for thousands of apps, EVO2 and successors could abstract genomic complexity and provide APIs for drug discovery tools, diagnostic classifiers, CRISPR designers, personalised health predictors, and agricultural tools.

This vision is partially instantiated already — the open-source model has been adopted and extended by third parties. But the full vision requires closing the gaps above: predictive models that actually work in humans, integrated health data, and evaluation frameworks that reflect real scientific goals rather than benchmark performance.

---

## Landscape Signals

### Capabilities
| Capability | Maturity |
|---|---|
| Genomic mutation effect prediction (VUS interpretation, BRCA1) | Narrow production |
| Novel CRISPR/Cas system design | Narrow production |
| Full IgG antibody design via CDR region specification | Demo |
| Autonomous agents for biological data curation at scale | Narrow production |

### Active Bottlenecks
| Bottleneck | Horizon |
|---|---|
| Drug regulatory and testing pipeline | 5+ years |
| Species translation gap (animal → human) | 5+ years |
| Lack of biological predictive models | 3–5 years |
| Low pharma probability of success (~10%) | 3–5 years |
| Invisible experimental history (negative results undocumented) | 1–2 years |
| Fragmented health and genomic data ecosystem | 1–2 years |
| Scarcity of ML-biology bilingual expertise | 1–2 years |
| Limited human experimental data | Unknown |

### Breakthroughs
- **EVO2**: First DNA-level genomic foundation model predicting mutation effects across all domains of life with state-of-the-art performance on clinically relevant benchmarks (significance: major)
- **Autonomous biological data agents**: Demonstrated deployment of crawlers processing unstructured biological metadata at the scale of the world's largest single-cell dataset (significance: major)

---

## Related Themes

- [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]]
- [[themes/medical_and_biology_ai|Medical and Biology AI]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/scientific_and_medical_ai|Scientific and Medical AI]]

## Key Concepts

- [[entities/alphafold|AlphaFold]]
- [[entities/brca1|BRCA1]]
- [[entities/protein-data-bank|Protein Data Bank]]
