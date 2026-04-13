---
type: source
title: Genome modeling and design
source_id: 01KKT5HWA51XWZR83208KJ8WB9
source_type: paper
authors: []
published_at: '2025-02-19 00:00:00'
theme_ids:
- medical_and_biology_ai
- model_architecture
- pretraining_and_scaling
- pretraining_data
- scientific_and_medical_ai
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Genome Modeling and Design Across All Domains of Life with Evo 2

> Evo 2 is a 40-billion-parameter biological foundation model trained on 9.3 trillion DNA base pairs spanning all three domains of life, introducing the StripedHyena 2 multi-hybrid architecture to achieve 1-million base-pair context at 3x the throughput of Transformer baselines. The paper demonstrates that scaling genomic language models enables, for the first time, zero-shot pathogenicity prediction across all human variant types simultaneously (coding SNVs, noncoding SNVs, indels, splice variants), achieves near-perfect noncoding variant classification (AUROC 0.974 on BRCA1), and shows that inference-time compute scaling via beam search produces predictable improvements in DNA sequence design quality, including programmable chromatin accessibility landscapes verified against computational epigenomic predictors.

**Authors:** Arc Institute (multiple contributors)
**Published:** 2025-02-19
**Type:** paper

---

## What This Source Contributes

Evo 2 addresses three compounding failures of prior genomic language models: their restriction to prokaryotic sequence, their inability to score noncoding or indel variants, and the absence of any inference-time scaling methodology for biological design. The paper introduces both an architectural advance (StripedHyena 2) and a training advance (OpenGenome2, a 9.3T-nucleotide open dataset covering all domains of life), then demonstrates capability across four axes: zero-shot variant effect prediction, whole-genome-scale sequence generation, mechanistic interpretability via sparse autoencoders, and controllable epigenomic design with inference-time scaling.

---

## Architecture: StripedHyena 2

Prior hybrid recurrent/convolutional architectures were insufficient at 40B-parameter scale; standard Transformers impose quadratic attention cost that makes 1M-token context windows computationally prohibitive. StripedHyena 2 resolves this through a "convolutional multi-hybrid" design combining three operator types in a striped block pattern:

- **Short explicit (SE):** inner filter length 7
- **Medium regularized (MR):** filter length 128
- **Long implicit (LI):** Hyena operators for long-range dependencies
- Self-attention layers with rotary positional embeddings are interleaved throughout

The result is up to 1.3x speedup at 16k context and 3x speedup at 1M context versus optimized Transformer baselines, with improved loss scaling on DNA over both Transformers and StripedHyena 1. Generation uses convolution-operator caching analogous to KV-cache, maintaining a constant memory footprint during autoregressive sampling.

Evo 2 is released in three scales: 1B, 7B, and 40B parameters, with instruction-tuned variants for the 7B and 40B sizes.

Themes: [[themes/model_architecture|Model Architecture]], [[themes/transformer_alternatives|Transformer Alternatives]]

---

## Training: OpenGenome2 and Two-Phase Curriculum

OpenGenome2 is a fully open dataset of 9.3 trillion base pairs, assembled as follows:

| Component | Scale |
|---|---|
| Non-redundant eukaryotic genomes (15,032) | 6.98 trillion nucleotides |
| Metagenomes | 854 billion nucleotides |
| Genic windows, promoters, augmented transcripts | Targeted enrichment |

Key training decisions:

- **Repeat element down-weighting:** Cross-entropy loss assigns weight 0.1 to repetitive DNA positions, preventing interspersed repeats from dominating eukaryotic pretraining loss.
- **Genic window upweighting:** Data is weighted toward information-dense functional elements during pretraining at 8,192-token context.
- **Context extension midtraining:** Multi-stage midtraining extends context to 1,048,576 tokens via combined positional interpolation and RoPE base frequency scaling (10x increase per context doubling).
- **Phylogenetic conditioning:** Greengenes-style lineage tags condition sequence generation on taxonomic identity.

Naive long-context training on raw eukaryotic reference genomes degraded model performance, requiring substantial data engineering to upweight genic windows. The OpenGenome2 dataset is publicly available on Hugging Face.

Themes: [[themes/pretraining_data|Pretraining Data]], [[themes/pretraining_and_scaling|Pretraining and Scaling]]

---

## Capability 1: Zero-Shot Variant Effect Prediction

Evo 2 is the first alignment-free model to robustly score all human variant types simultaneously, requiring no task-specific training, no multiple sequence alignments, and no annotation.

### BRCA1/BRCA2 Benchmark Results

| Model | BRCA1 Noncoding SNV AUROC | BRCA1 Combined SNV AUROC |
|---|---|---|
| Evo 2 40B base | **0.974** | 0.901 |
| Evo 2 7B base | 0.959 | **0.904** |
| GPN-MSA | 0.918 | 0.863 |
| CADD | 0.909 | 0.876 |
| PhyloP | 0.898 | 0.811 |
| Evo 1 | 0.212 (below chance) | 0.497 (near random) |

The collapse of Evo 1 performance on noncoding variants (AUROC 0.212, below chance) establishes how fundamentally different the capability is between model generations. AlphaMissense is absent from all noncoding rows, revealing an architectural limitation: it cannot assess noncoding SNV pathogenicity at all.

A supervised classifier built on Evo 2 40B embeddings (lightweight MLP with 128nt window averaging) achieves AUROC 0.95 across all BRCA1 SNVs, outperforming all zero-shot baselines including AlphaMissense, without any human variant data in pretraining.

### Key Limitations of the Variant Evaluation

- **BRCA1/BRCA2 only.** All evaluations are restricted to two highly studied cancer genes; generalization to the broader genome, especially rare or poorly annotated genes, is entirely undemonstrated.
- **8,192 bp scoring window.** Despite 1M bp context, variant scoring in practice uses 8,192 bp windows, missing enhancer-promoter interactions and TAD-level regulatory effects.
- **Class imbalance.** AUPRC on combined BRCA1 variant prediction (0.677 for 40B) is substantially lower than AUROC (0.901), indicating real-world precision may be lower than AUROC implies.
- **Finetuning catastrophically degrades noncoding performance.** The instruction-tuned 40B model scores AUROC 0.467 on BRCA1 noncoding SNVs (near-random), compared to 0.974 for the base model. This blocks clinical use of finetuned variants for noncoding pathogenicity.
- **No population-scale human variation.** Only the reference genome is in OpenGenome2. Noncoding performance relies on multi-species evolutionary conservation as a proxy for functional constraint, limiting rare variant prediction.

Themes: [[themes/medical_and_biology_ai|Medical and Biology AI]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]]

---

## Capability 2: Whole-Genome-Scale Generation

Evo 2 generates novel genomic sequences at three scales:

- **Mitochondrial genomes** (16 kb): 250 unique sequences prompted from 3,000 bp of human mitochondrial genome
- **Minimal prokaryotic genomes** (580 kb): 35 sequences at M. genitalium scale using Evo 2 40B
- **Eukaryotic chromosome segments** (330 kb): 20 artificial yeast chromosome sequences

Generated sequences are validated entirely via computational proxies (ESMFold pLDDT, Pfam homology, DSSP secondary structure, MitoZ annotation, AlphaFold 3 structure prediction). No wet-lab synthesis or functional validation has been performed.

**Critical caveat:** Generated eukaryotic chromosome-scale sequences have lower density of tRNA genes and coding features than native genomes, indicating that unconstrained autoregressive generation does not fully recapitulate eukaryotic genomic organization. Evo 2 also explicitly excludes viruses infecting eukaryotic hosts from training, yielding random performance on human viral protein generation.

---

## Capability 3: Mechanistic Interpretability via Sparse Autoencoders

Evo 2 is the first genomic foundation model analyzed via sparse autoencoders (SAEs). A BatchTopK SAE trained on activations from layer 26 (a Hyena-MR block) of an intermediate 7B checkpoint reveals discrete internal features corresponding to:

- Exon/intron boundaries
- Transcription factor binding motifs
- Protein secondary structures (alpha-helices, beta-sheets) in coding sequences
- Prophage genomic regions (feature f/19746 fires on annotated prophage, CRISPR spacers by phage origin, and unannotated integrase/invertase loci)

The prophage feature is notable: it associates CRISPR spacers with phage origin rather than memorizing sequence, suggesting the model learns biological concepts beyond explicit annotation.

**Limitations of the interpretability analysis:**
- SAE analysis is conducted only at layer 26 based on preliminary analysis; earlier and later layers may capture biological concepts not yet discovered.
- The SAE was trained on an intermediate 7B checkpoint, not the flagship 40B model.
- The generalizability of discovered features to the full 40B model is unknown.

---

## Capability 4: Controllable Epigenomic Design with Inference-Time Scaling

Evo 2 can generate DNA sequences with programmable chromatin accessibility patterns via beam search guided by an ensemble of Enformer and Borzoi epigenomic predictors. The beam search algorithm:

1. Autoregressively samples K candidate 128 bp chunks per step
2. Scores each chunk against desired accessibility patterns using the Enformer+Borzoi ensemble average
3. Selects the top K' chunks to continue

Demonstrated designs include long square waves (alternating 1,664 bp open/closed chromatin) and Morse code encodings (dots and dashes as open chromatin, spaces as closed chromatin). Design quality is evaluated via AUROC comparing model predictions against the desired peak patterns.

**Inference-time scaling:** Increasing tokens sampled per base pair from 1 to 60 (K'=2, K=30) produces a predictable log-linear improvement in design AUROC. This is the first demonstration of inference-time scaling laws in biological language modeling, analogous to LLM chain-of-thought scaling.

### Fundamental Limitations of Epigenomic Design

- **Circular validation.** Chromatin accessibility design quality is evaluated entirely against the same computational predictors (Enformer, Borzoi) used to guide generation. Whether designed sequences produce the intended chromatin state in actual cells is unknown.
- **No experimental validation.** The entire design-evaluate loop runs within computational models. Wet-lab validation (ATAC-seq, ChIP-seq) has not been performed.
- **Scoring oracle boundary.** Borzoi cannot make predictions for 163,840 bp of left and right flanking context, creating a hard boundary on interpretable sequence influence.
- **Compute cost scales linearly.** Sampling 60 tokens per base pair makes design cost scale linearly with sequence length; the 4-replicate Borzoi ensemble plus Enformer must be queried for every chunk evaluation.
- **Design diversity may be constrained.** The Borzoi ensemble lower-confidence-bound scoring penalizes high variance across replicates, implicitly restricting the diversity of high-scoring designs.

---

## Open Bottlenecks

### Blocking (No Clear Near-Term Solution)

**Absent experimental feedback loop.** The entire generative genomics capability is validated computationally. Improving generated functional quality requires wet-lab validation at scale, which is expensive and slow. Supervised finetuning or reinforcement learning with experimental feedback is identified as necessary but has not been demonstrated. This blocks reliable in silico functional design of novel genes, gene circuits, and synthetic organisms.

**Noncoding variant annotation gap.** Evaluations are restricted to BRCA1 and BRCA2 because large-scale functional annotation of noncoding variants exists only for a handful of highly-studied genes. This blocks genome-wide noncoding variant pathogenicity models and their clinical validation.

**Catastrophic forgetting in finetuned models.** Finetuning destroys noncoding representation quality (0.974 AUROC base vs. 0.467 finetuned), with no clear mitigation strategy identified. This blocks deployment of instruction-tuned biological foundation models for clinical variant interpretation.

**Biosafety frameworks are nascent.** Few empirical risk assessment frameworks exist for open biological foundation models. The paper notes that task-specific post-training may circumvent biosafety exclusions (e.g., re-enabling human viral pathogen design capability), but validated evaluation suites to detect this are absent.

### Improving (Active Research Trajectory)

**Compute accessibility.** Training 40B-parameter genomic foundation models requires 4D parallelism (tensor, pipeline, context, data parallel with ZeRO-3 sharding), creating a compute barrier that concentrates capability at well-resourced institutions. This is improving as hardware and training infrastructure mature.

**Long-range regulatory modeling.** Even with 1M bp context, variant scoring uses 8,192 bp windows. Enhancer-promoter interactions and TAD-level regulatory architecture are not captured. The 3-5 year horizon for accurate noncoding variant prediction for enhancer mutations and structural variants is realistic.

**Population-scale training data.** Combining Evo 2 with population-scale human genomic variation is identified as the path to improved pathogenicity prediction for rare and population-specific variants.

---

## Biosafety Considerations

Evo 2 explicitly excludes viruses infecting eukaryotic hosts from training data. The paper notes that task-specific post-training may circumvent this risk mitigation measure and states this "should be approached with caution." The release includes model weights, an interactive Evo Designer interface, and NVIDIA NIM API access, representing broad deployment of a frontier biological generative model.

---

## Connections

- The inference-time scaling methodology (log-linear improvement via beam search width) parallels scaling laws emerging in [[themes/pretraining_and_scaling|Pretraining and Scaling]] for language models, suggesting a domain-general principle.
- The SAE interpretability approach directly mirrors mechanistic interpretability work in language models (e.g., Anthropic's dictionary learning work), extending the method to biological sequences for the first time.
- The finetuning catastrophe (0.974 to 0.467 AUROC) is structurally similar to catastrophic forgetting phenomena observed across foundation model finetuning, but is especially acute here because noncoding representations appear fragile under gradient updates.
- The restriction to BRCA1/BRCA2 for evaluation is a consequence of annotation availability, not model design; this is the same bottleneck limiting most clinical genomics AI benchmarking.

---

## Summary Judgment

Evo 2 represents a genuine step change in genomic foundation model capability, particularly for noncoding variant interpretation. The 0.212 to 0.974 AUROC leap on BRCA1 noncoding SNVs from Evo 1 to Evo 2 40B is not incremental; it changes what the technology can be used for. The inference-time scaling demonstration is conceptually significant, establishing that biological design quality is amenable to compute-quality tradeoffs in the same way as language model reasoning.

However, the paper's central limitation is that none of the generative results touch wet lab reality. Chromatin designs are validated against the same models used to generate them. Synthetic genomes are evaluated by computational proxies. The transition from "computational demonstration" to "biological reality" remains an unresolved bottleneck across the entire field, and Evo 2 does not close it.

## Key Concepts

- [[entities/brca1|BRCA1]]
- [[entities/inference-time-compute-scaling|Inference-Time Compute Scaling]]
