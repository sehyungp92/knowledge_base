---
type: entity
title: BRCA1
entity_type: entity
theme_ids:
- agent_systems
- ai_for_scientific_discovery
- medical_and_biology_ai
- model_architecture
- pretraining_and_scaling
- pretraining_data
- scientific_and_medical_ai
- software_engineering_agents
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.000671301417237134
staleness: 0.0
status: active
tags: []
---
# BRCA1

> BRCA1 is a well-characterized tumor suppressor gene whose pathogenic variants confer significantly elevated risk of breast and ovarian cancer. It has become a critical benchmark for evaluating AI-based genomic variant effect prediction, serving as the primary test case for Evo 2's ability to classify both coding and noncoding mutations at scale — a capability with direct implications for clinical variant interpretation.

**Type:** entity
**Themes:** [[themes/ai_for_scientific_discovery|AI for Scientific Discovery]], [[themes/medical_and_biology_ai|Medical and Biology AI]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]], [[themes/model_architecture|Model Architecture]], [[themes/pretraining_and_scaling|Pretraining and Scaling]], [[themes/pretraining_data|Pretraining Data]]

## Overview

BRCA1 functions as a benchmark not because it is easy, but because it is hard in precisely the right ways: it has a large noncoding regulatory region, thousands of classified variants in ClinVar, and a well-understood functional assay (saturation genome editing) that provides ground truth for loss-of-function classification. This combination makes it an unusually stringent test for genomic foundation models, exposing weaknesses that simpler gene targets would conceal.

The gene's prominence in the Evo 2 evaluation framework, detailed in Genome modeling and design, reflects a broader ambition: demonstrating that sequence-only foundation models trained without explicit biological supervision can match or exceed task-specific tools on clinically meaningful variant classification.

## Key Findings

The central story around BRCA1 is one of generational progress punctuated by a cautionary failure mode. Evo 1, the predecessor to Evo 2, performs near-randomly on BRCA1 noncoding SNV pathogenicity prediction (AUROC 0.212), revealing that prior genomic foundation models had essentially no signal in the noncoding landscape despite being trained on genomic sequence. This is not a minor gap — it is a near-complete failure on a clinically critical task.

Evo 2 reverses this dramatically. The base 40B model achieves AUROC 0.974 and AUPRC 0.903 on BRCA1 noncoding SNVs in a zero-shot setting — without any task-specific training. On coding variants, it approaches CADD performance (AUROC 0.843–0.899 vs. CADD's 0.889–0.900) without task-specific architectural modifications. When Evo 2 embeddings are used to build a supervised BRCA1 classifier, performance climbs further: AUROC 0.94 on coding SNVs and 0.95 across all SNVs, outperforming AlphaMissense and other specialized tools.

This zero-shot competency emerges from a model trained on 9.3 trillion nucleotides with no explicit biological labels — the model was simply given DNA and asked to predict the next nucleotide, yet internalized enough genomic grammar to distinguish pathogenic from benign variants. As noted in the No Priors Ep. 103 discussion, the Evo 2 team "didn't tell it anything about DNA" — the biological structure was learned implicitly.

## Limitations and Open Questions

The BRCA1 results carry several important caveats that should temper enthusiasm.

The most striking limitation is the fine-tuning collapse. Fine-tuning the Evo 2 40B model catastrophically degrades noncoding performance: the fine-tuned model drops to AUROC 0.467 on BRCA1 noncoding SNVs, compared to 0.974 for the base model. This near-random collapse suggests that the noncoding signal is fragile and may reside in distributed representations that fine-tuning disrupts. The trajectory is listed as unclear — it is unknown whether this is a fundamental instability or a solvable optimization problem.

The generalizability question is entirely open. All evaluations focus on BRCA1 and BRCA2, two of the most extensively studied cancer genes in the genome. Whether the model's variant effect prediction capabilities extend to rare, poorly annotated, or structurally unusual genes remains undemonstrated. The benchmark may be selecting for genes where training data was abundant.

There is also a precision-recall tension: Evo 2's AUPRC on combined BRCA1 variant prediction (0.677 for 40B) is substantially lower than its AUROC (0.901). AUROC is robust to class imbalance; AUPRC is not. In real clinical settings, pathogenic variants are rare, meaning the model's effective precision may be considerably lower than headline numbers suggest.

Finally, the optimal embedding layer for downstream tasks is inconsistent across applications — block 20 for BRCA1 variant prediction, block 26 for exon classification, different blocks for other tasks — with no principled selection rule. This is a practical barrier to deployment and hints at heterogeneous internal representations.

## Connections

BRCA1 sits at the intersection of two converging threads in the current AI landscape. The first is the push toward genomic foundation models capable of universal biological understanding — represented by Evo 2 and the OpenGenome2 dataset. The second is the development of large-scale perturbational datasets like Tahoe 100 (100 million single-cell data points, detailed in No Priors Ep. 103) that enable data-hungry models to learn drug-response and disease mechanisms at scale.

BRCA1 is relevant to the first thread directly, as a benchmark, and to the second indirectly — cancer cell lines carrying BRCA1 mutations are among the targets in perturbational screening platforms like Vivo's Mosaic system. The bottleneck in virtual cell modeling (current best models predict differentially expressed genes with only ~10% accuracy) and the absence of accepted benchmarks for evaluating virtual cell quality both echo the evaluation challenges visible in BRCA1 variant classification itself.

The broader implication is that BRCA1 represents a rare area of genuine measurability in computational biology — where ground truth exists, clinical stakes are high, and model performance can be directly compared. Its status as a benchmark will likely persist precisely because so few genomic targets offer the same combination of scale, annotation quality, and clinical relevance.

## Relationships

## Sources
