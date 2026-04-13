---
type: source
title: 'From Bytes to Ideas: Language Modeling with Autoregressive U-Nets'
source_id: 01KJTPVV117TGWN29DZEAS90WA
source_type: paper
authors:
- Mathurin Videau
- Badr Youbi Idrissi
- Alessandro Leite
- Marc Schoenauer
- Olivier Teytaud
- David Lopez-Paz
published_at: '2025-06-17 00:00:00'
theme_ids:
- model_architecture
- pretraining_and_scaling
- pretraining_data
- representation_learning
- scaling_laws
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# From Bytes to Ideas: Language Modeling with Autoregressive U-Nets

This paper proposes AU-Net (Autoregressive U-Net), an architecture that eliminates external tokenization by processing raw bytes through a learned multi-stage hierarchy of contracting and expanding sequence representations. AU-Net matches strong BPE baselines under controlled compute budgets and outperforms them with deeper hierarchies (3–4 stages), while conferring qualitative advantages in multilingual transfer, vocabulary-free operation, and an emergent multi-token prediction mechanism — at the cost of throughput, engineering complexity, and performance gaps on knowledge-intensive tasks at lower compute scales.

**Authors:** Mathurin Videau, Badr Youbi Idrissi, Alessandro Leite, Marc Schoenauer, Olivier Teytaud, David Lopez-Paz
**Published:** 2025-06-17
**Type:** paper

---

## Motivation: What's Wrong With Tokenization

BPE and similar tokenization schemes impose a **fixed granularity** on text that cannot adapt during training or inference. Every token is mapped to an independent vector, so the model must rediscover sub-token structure from scratch — that "strawberry" and "strawberries" share nine characters, for instance — and the vocabulary size acts as the only dial between sequence length and token frequency, with no satisfactory resolution in either direction.

The deeper pathology, as the paper frames it, is that **most issues stem from the embedding operation rather than the splitting act itself**. Isolated token embeddings prevent contextualized representation before pooling, hamper character-level tasks structurally inaccessible to standard LMs, and produce tokenizers that are language-biased by construction — disadvantaging morphologically rich and low-resource languages whose statistics are underrepresented in the merge-rule corpus.

---

## The AU-Net Architecture

AU-Net internalises tokenization entirely. It processes raw bytes through a U-Net-style encoder-decoder:

**Contracting path (pooling):** Stage 1 operates on raw bytes; stage 2 pools at word boundaries (space-delimited); stage 3 at two-word boundaries; stage 4 at four-word boundaries. Pooling is implemented as index selection at split positions followed by a linear projection — the preceding attention layers handle implicit aggregation rather than explicit cross-attention. The hidden dimension grows proportionally to the contraction factor at each stage, enabling richer representations as sequences compress.

**Expanding path (upsampling):** Multi-Linear Upsampling duplicates each coarse vector to match the following segment length, then applies distinct position-specific linear layers shared across segments — varying by intra-segment position. Skip connections pass fine-grained representations from the contracting path back to the expanding path, analogous to image U-Nets.

**Global attention, monolithically applied:** Unlike competing architectures that process words or word groups in isolation with local attention, AU-Net applies full (or sliding-window at byte level) attention monolithically across each stage.

**Key design constraint:** The splitting function must be *stable to rightward insertion* — appending bytes must not alter prior pooling decisions — ensuring consistent autoregressive generation.

This differs from prior work in meaningful ways: MegaByte uses fixed-size blocks; BLT/SpaceByte perform single-stage byte processing; Nawrot et al. (2022) defined a similar structure but used fixed pooling, smaller models, and did not evaluate on generation tasks.

---

## Emergent Multi-Token Prediction

A notable architectural property: **deeper stages inherently function as multi-token predictors**. Stage 4, operating on four-word chunks, must anticipate multiple words ahead to make coherent predictions — but this emerges from the architecture without auxiliary losses, unlike the explicit multi-token prediction heads of Gloeckle et al. (2024). Deeper stages guide shallower stages at the semantic level while shallow stages handle fine phonological/orthographic detail. This provides a natural hierarchy from bytes to ideas without any loss engineering.

At inference, this enables **cascaded conditional activation**: high-level stages activate only at word or word-group boundaries, while the byte-level stage runs at every step. Computationally intensive layers thus fire rarely but still effectively guide predictions.

---

## Scaling Laws for Byte-Level Training

A non-trivial contribution is the establishment of **new hyperparameter scaling formulas** specific to byte-level hierarchical training. Token sequences are on average 4.56× shorter than their byte equivalents on the DCLM corpus (LLaMA 3 tokenizer), which means byte-level batch sizes and learning rates follow substantially different power laws:

- BSZ = 0.66 · C^0.321
- LR = 6.6 × C^{−0.176}

These were derived via quasi-random sweep across 25M–500M parameter models and differ enough from BPE baseline formulas that using BPE scaling heuristics for byte-level training produces suboptimal optimization.

---

## Results

**At 1B scale (370B tokens):**
- AU-Net 3: 72.9 Hellaswag (+2.7 vs. BPE's 70.2), 43.3 ARC-Challenge (+4.8)
- AU-Net 4: 73.7 Hellaswag, 31.7 MMLU (+4.7 vs. BPE's 27.0), 5.3 GSM8K (+0.9)

**At 8B scale (200B tokens):**
- AU-Net 2: 79.1 Hellaswag (+1.9), 80.0 ARC-Easy (+5.5)
- Achieved with 5× less compute than BLT (trained on 1T tokens)

**Multilingual (8B scale, DCLM English-only training):**
- +3.0 avg MMLU gain across Germanic languages, +4.0 across Romance languages
- FLORES-200: avg BLEU 24.6 vs. 20.9 across 23 languages; gains as large as +7.0 (Limburgish), +6.7 (Papiamento)

**Vocabulary overhead:** AU-Net uses a 1M-parameter byte-level embedding versus 525M–1B for BPE baselines — a qualitative architectural advantage for multilingual and code-rich settings.

---

## Capabilities

- **Tokenization-free modeling** from raw bytes, supporting unlimited unique tokens without memory-heavy embedding tables — [[themes/representation_learning|representation learning]] advantage for multilingual and morphologically rich settings. *(maturity: research_only)*
- **Hierarchical multi-scale prediction** emerging architecturally without auxiliary objectives — relevant to debates about [[themes/model_architecture|model architecture]] alternatives to multi-token prediction heads. *(maturity: research_only)*
- **Cross-lingual transfer via morphological shared structure**, particularly for Latin-script language families, from a model trained exclusively on English. *(maturity: research_only)*
- **Principled byte-level [[themes/scaling_laws|scaling laws]]** for batch size and learning rate, enabling prediction of optimal hyperparameters at larger scales. *(maturity: research_only)*

---

## Limitations and Open Questions

**Language coverage:** The space-based splitting function is fundamentally incompatible with non-space-delimited languages (Chinese, Japanese, Thai). AU-Net 2 scores 28.0 vs. BPE's 33.0 on Chinese MMLU — a direct performance regression. Extending to these languages requires learned splitting, which remains future work.

**Hand-engineered splitting:** The splitting function is still predefined, not learned end-to-end. The architecture moves the tokenization decision inside the model but does not eliminate it as a design choice — the locus shifts from corpus preprocessing to architectural specification.

**Knowledge-intensive task deficits:** AU-Net 4 scores 15.5 vs. BPE's 37.2 on TQA at the 60B token scale — a 21.7 point gap. On GSM8K and MMLU, 2–3 stage models remain behind BPE at up to 1e22 FLOPs. The inflection point on these benchmarks appears to shift to higher compute budgets, suggesting deep hierarchies need substantially more training data to converge on tasks requiring memorized knowledge.

**Math and code confounds:** DCLM contains minimal mathematics data, making it impossible to separate architectural underperformance on GSM8K from data confounds. All GSM8K comparisons should be interpreted with this caveat.

**Throughput regression:** AU-Net 4 achieves 155k bytes/sec/GPU versus 210k for a comparable BPE Transformer — a 26% throughput reduction that compounds with the larger parameter count of deeper hierarchies.

**Parallelism ceiling:** FSDP fails to overlap computation and communication at 3–4 stage scale, creating a practical engineering ceiling on scaling deep hierarchical models beyond 8B parameters. Unequal parameter distribution across stages disrupts communication-computation overlap.

**Data starvation for deep hierarchies:** Early signs of diminishing returns beyond 3 stages may reflect data starvation rather than a fundamental architectural ceiling — deeper stages may require substantially more tokens to converge. This conflation cannot be resolved within the paper's compute budget.

**Asymmetric multilingual benefit:** Gains are substantially stronger in the low-resource-to-English direction than English-to-low-resource generation, suggesting byte-level morphological transfer is more useful for understanding than for generation.

**Evaluation scope:** All multilingual evaluations use an English-dominated training corpus, so improvements are attributable solely to morphological transfer — not multilingual training data representation.

---

## Bottlenecks Identified

**Learned splitting for all writing systems** — Current space-based heuristics are fundamentally incompatible with non-space-delimited scripts. Robust tokenization-free multilingual deployment is blocked until splitting can be learned from data rather than hand-specified. *(horizon: 1–2 years)*

**Distributed training infrastructure** — FSDP's inability to overlap computation and communication for unequally-sized hierarchical stages creates a practical ceiling on scaling AU-Net 3/4 beyond 8B parameters. *(horizon: months)*

**Data requirements of deep hierarchies** — Whether 3–4 stage byte-level models are genuinely superior to BPE at equivalent compute cannot be established without much larger training runs. The comparison is currently confounded by data starvation. *(horizon: 1–2 years)*

---

## Significance

AU-Net demonstrates that tokenization can be fully internalised into [[themes/model_architecture|model architecture]] through multi-stage hierarchical pooling from raw bytes — matching and in some configurations exceeding strong BPE baselines — without requiring external vocabulary construction. The implication is that vocabulary design becomes an architectural decision rather than a corpus preprocessing step, dissolving the hard boundary between tokenization and representation learning. Whether this dissolves into a fully learned end-to-end process depends on progress on learned splitting functions.

The emergent multi-scale prediction structure also provides an architectural mechanism for semantic-to-phonological hierarchy without auxiliary objectives, which is a relevant data point for ongoing debates about [[themes/pretraining_and_scaling|pretraining]] efficiency and [[themes/transformer_alternatives|transformer alternatives]].

---

## Related Themes

- [[themes/model_architecture|Model Architecture]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/pretraining_data|Pretraining Data]]
- [[themes/representation_learning|Representation Learning]]
- [[themes/scaling_laws|Scaling Laws]]
- [[themes/transformer_alternatives|Transformer Alternatives]]

## Key Concepts

- [[entities/dclm|DCLM]]
- [[entities/gsm8k|GSM8K]]
- [[entities/hellaswag|HellaSwag]]
- [[entities/mmlu|MMLU]]
- [[entities/multi-token-prediction|Multi-Token Prediction]]
