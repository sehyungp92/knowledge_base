---
type: source
title: How a Gemma model helped discover a new potential cancer therapy pathway
source_id: 01KJS27HS4JRR89BBM7EZ80THD
source_type: article
authors: []
published_at: '2025-10-15 00:00:00'
theme_ids:
- ai_for_scientific_discovery
- medical_and_biology_ai
- pretraining_and_scaling
- scaling_laws
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# How a Gemma model helped discover a new potential cancer therapy pathway

**Authors:** 
**Published:** 2025-10-15 00:00:00
**Type:** article

## Analysis

# How a Gemma model helped discover a new potential cancer therapy pathway
2025-10-15 · article
https://blog.google/technology/ai/google-gemma-ai-cancer-therapy-discovery/

---

## Briefing

**Cell2Sentence-Scale 27B (C2S-Scale), a 27B-parameter single-cell foundation model built on Gemma, used a dual-context virtual screen over 4,000 drugs to identify silmitasertib as a novel interferon-conditional amplifier of tumor antigen presentation — a prediction with no prior literature support that was subsequently confirmed in vitro with a ~50% boost in MHC-I expression. This represents a concrete demonstration that scaling biological foundation models past a threshold confers emergent conditional reasoning capabilities that enable genuine hypothesis generation, not just task improvement.**

### Key Takeaways
1. **Scaling laws transfer to biology** — Biological foundation models obey the same scaling laws as language models; larger models perform strictly better, and C2S-Scale 27B extends this to emergent capabilities absent in smaller models.
2. **Conditional reasoning is an emergent capability** — Resolving context-dependent drug effects (boost signal only when interferon is already present) required the 27B scale; smaller models could not handle this task.
3. **70–90% of model-identified drug hits are novel** — Only 10–30% of the virtual screen's hits had prior literature support, confirming the model generates genuinely new hypotheses rather than regurgitating known associations.
4. **Silmitasertib + low-dose interferon is a novel synergistic combination** — Neither drug alone produced meaningful antigen presentation enhancement, but their combination yielded ~50% increase in MHC-I expression.
5. **CK2 inhibition was not previously linked to MHC-I or antigen presentation** — The prediction was novel: although CK2 has known immune roles, its inhibitor's effect on antigen presentation had no prior literature basis.
6. **Validation generalized to an unseen cell type** — Confirmation was performed in human neuroendocrine cell models not present in training data, demonstrating genuine generalization rather than memorization.
7. **The dual-context screen design is a reusable blueprint** — Contrasting immune-context-positive (patient samples) vs. immune-context-neutral (cell lines) is a general methodology for discovering context-conditioned biology.
8. **Cold-to-hot tumor conversion is the immunotherapy goal** — The entire discovery is framed around making immune-invisible ("cold") tumors detectable by forcing upregulation of antigen presentation machinery.
9. **This is an early-stage experimental lead, not a therapy** — The authors explicitly note this is a first step requiring further preclinical and clinical validation before any therapeutic application.
10. **The model is open and publicly available** — C2S-Scale 27B is released on Hugging Face with code on GitHub, enabling community replication and extension.

---

### C2S-Scale Architecture and Context

- C2S-Scale 27B is a single-cell foundation model with 27 billion parameters, developed in collaboration with Yale University.
  - It is built on the **Gemma family of open models**, adapting the language model architecture to interpret single-cell biological data.
  - The model is designed to treat cells as having a "language" — encoding gene expression states as sequences that can be processed and reasoned over.
- This release builds on prior work demonstrating that biological models obey **scaling laws analogous to those in NLP**.
  - The prior finding established that more parameters improve performance on biology benchmarks.
  - C2S-Scale 27B was designed to test whether scale produces qualitative capability jumps, not just quantitative improvements.
- The collaboration with Yale integrates both computational model development and experimental wet-lab validation.
  - Yale teams are continuing to explore the discovered mechanism and test additional AI-generated predictions in other immune contexts.

---

### Scaling Laws and Emergent Capabilities in Biology

- The central scientific claim is that **biological scaling laws produce emergent capabilities** — new reasoning modes absent at smaller scales.
  - The specific capability demonstrated is context-dependent conditional reasoning: predicting that a drug will have an effect only when a specific background condition (low interferon) is present.
  - Smaller C2S models were explicitly tested and **could not resolve this context-dependent effect** — they lacked the capacity to distinguish the two contexts.
- This positions biological AI scaling as qualitatively different from simple benchmark improvement.
  - The authors frame it as the difference between "getting better at existing tasks" vs. "acquiring entirely new capabilities."
  - **The true promise of scaling lies in the creation of new ideas, and the discovery of the unknown** — a direct claim that scale enables genuine scientific novelty.
- The scaling law analogy to natural language is important: it suggests that known insights from LLM scaling (emergent abilities at certain parameter counts, power-law performance curves) may transfer directly to biological foundation models.
  - This has implications for research investment decisions: continued scaling of biological models is likely to yield further emergent capabilities.

---

### The Cancer Immunotherapy Target: Cold vs. Hot Tumors

- A core challenge in cancer immunotherapy is that many tumors are **"cold" — they evade immune detection** by failing to display surface signals that the immune system can recognize.
  - The mechanism of detection involves **antigen presentation**: cells displaying protein fragments via MHC-I molecules on their surface that cytotoxic T cells can recognize.
  - Cold tumors suppress or fail to upregulate this display, making them invisible to immune surveillance.
- Making tumors "hot" — boosting their antigen presentation — is a key therapeutic goal 

## Key Claims

1. C2S-Scale 27B is a 27 billion parameter foundation model designed to understand the language of individual cells, built on the Gemma family of open models.
2. C2S-Scale generated a novel hypothesis about cancer cellular behavior that was subsequently confirmed by experimental validation in living cells.
3. Biological foundation models follow clear scaling laws analogous to natural language models — larger models perform better on biology tasks.
4. Scaling biological models can confer entirely new capabilities beyond incremental improvement on existing tasks.
5. Many tumors are 'cold' — invisible to the immune system — and a key strategy to make them 'hot' is forcing them to display immune-triggering signals via antigen presentation.
6. Conditional reasoning to identify drugs that only boost immune signals in specific interferon-present contexts appeared to be an emergent capability of scale — smaller models could not resolve this co
7. The dual-context virtual screen simulated the effect of over 4,000 drugs across immune-context-positive and immune-context-neutral conditions.
8. 10–30% of drug hits identified by the model were already known in prior literature; the remainder were surprising hits with no prior known link to antigen presentation.
9. C2S-Scale predicted that silmitasertib (CX-4945), a CK2 kinase inhibitor, would strongly boost antigen presentation only in the immune-context-positive setting and have little to no effect in the immu
10. Inhibiting CK2 via silmitasertib had not previously been reported in the literature to explicitly enhance MHC-I expression or antigen presentation.

## Capabilities

- High-throughput virtual drug screening across biological contexts using single-cell foundation models, simulating the effect of 4,000+ drug candidates simultaneously to identify context-conditioned synergistic effects
- Context-conditioned hypothesis generation in cancer biology — predicting drug effects that are conditional on specific immune microenvironment states, an emergent capability that only appears at 27B+ parameter scale
- Zero-shot generalization of single-cell predictions to entirely unseen cell types — predictions validated in human neuroendocrine cell models not present in training data
- Biological foundation models follow predictable scaling laws analogous to natural language — larger models achieve qualitatively superior performance on single-cell biology tasks

## Limitations

- Conditional reasoning in single-cell biology is a hard capability cliff — smaller models entirely fail to resolve context-dependent drug effects that 27B scale handles, with no partial success, implying a sharp threshold rather than gradual improvement
- In silico drug predictions require mandatory wet lab validation before any utility claim can be made — the computational output alone has no established reliability threshold
- The false positive rate for novel drug hits is unknown and likely high — 70–90% of predicted hits have no prior literature support, making it impossible to distinguish genuine discoveries from spurious model outputs without exhaustive lab testing
- Experimental validation is limited to in vitro cell models — no preclinical animal models or clinical evidence; the gap between cell-line results and therapeutic efficacy in humans is substantial
- The emergent conditional reasoning capability is confined to a single demonstrated task type (immune-context drug screening) — generalizability to other context-dependent biological questions is undemonstrated
- It is unknown whether the scaling laws observed in biological models generalize across cell types, organisms, or biological modalities beyond single-cell transcriptomics
- Security, data contamination, and reproducibility concerns are entirely absent from the announcement — there is no mention of held-out validation sets, potential training data contamination with drug literature, or independent replication

## Bottlenecks

- Wet lab validation throughput is the hard bottleneck in AI-driven drug discovery pipelines — AI can generate thousands of hypotheses but each requires expensive, slow in vitro and in vivo validation, creating a severe asymmetry between generation and confirmation rates
- Context-conditioned biological reasoning requires very large scale (27B+), making the capability inaccessible to research groups without significant compute resources and blocking democratization of AI-driven hypothesis generation

## Breakthroughs

- First experimentally validated AI-generated novel cancer therapy hypothesis from a biological foundation model: C2S-Scale 27B predicted silmitasertib + low-dose interferon synergistically amplifies tumor antigen presentation in a context-conditional manner, confirmed in vitro in cell types unseen du
- Emergent conditional reasoning demonstrated as a scale-dependent capability in biological foundation models — analogous to emergent reasoning in LLMs but now demonstrated in single-cell biology, with smaller models showing a hard capability cliff

## Themes

- [[themes/ai_for_scientific_discovery|ai_for_scientific_discovery]]
- [[themes/medical_and_biology_ai|medical_and_biology_ai]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/scaling_laws|scaling_laws]]
- [[themes/scientific_and_medical_ai|scientific_and_medical_ai]]
