---
type: source
title: 'KGARevion: An AI Agent for Knowledge-Intensive Biomedical QA'
source_id: 01KJV8271TDJ2R7E09R133E9V0
source_type: paper
authors:
- Xiaorui Su
- Yibo Wang
- Shanghua Gao
- Xiaolong Liu
- Valentina Giunchiglia
- Djork-Arné Clevert
- Marinka Zitnik
published_at: '2024-10-07 00:00:00'
theme_ids:
- agent_systems
- benchmark_design
- evaluation_and_benchmarks
- knowledge_and_memory
- medical_and_biology_ai
- retrieval_augmented_generation
- scientific_and_medical_ai
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# KGARevion: An AI Agent for Knowledge-Intensive Biomedical QA

KGARevion introduces a neurosymbolic agent pipeline that inverts the standard RAG paradigm — instead of retrieving from knowledge graphs, it prompts LLMs to *generate* candidate knowledge triplets from latent memory, then *verifies* them against structured biomedical KGs using fine-tuned structural embeddings. This generate-verify-revise loop addresses three compounding failure modes in prior work: unverified retrieval, KG incompleteness handling, and LLM positional bias in multiple-choice settings.

**Authors:** Xiaorui Su, Yibo Wang, Shanghua Gao, Xiaolong Liu, Valentina Giunchiglia, Djork-Arné Clevert, Marinka Zitnik
**Published:** 2024-10-07
**Type:** Paper · [arxiv](https://arxiv.org/pdf/2410.04660)

---

## Motivation

The core problem is that neither LLMs nor KG-based retrieval systems alone can handle knowledge-intensive biomedical QA reliably:

- **LLMs** cannot integrate structured codified scientific knowledge with tacit clinical expertise, and degrade sharply on questions requiring multi-concept reasoning (e.g. distinguishing HSPA4 vs. HSPA8 vs. HSPA1B vs. HSPA1A). On newly curated MedDDx-Expert questions, the strongest baseline (LLaMA3.1-8B) achieves only 0.306 accuracy.
- **RAG systems** (Self-RAG, MedRAG, KG-RAG, KG-Rank) retrieve without post-retrieval verification — they cannot assess whether retrieved information is factually accurate or contextually relevant, and are bounded by the quality of underlying biomedical databases, which are systematically incomplete and sometimes incorrect.
- **KG-only models** (QAGNN, JointLK, Dragon) rely solely on direct graph edges and cannot generalize to unseen nodes or implicit relationships — two proteins sharing molecular-level similarity may have no direct KG connection at all.
- **LLMs exhibit severe positional bias**: LLaMA3.1-8B shows average accuracy shifts of 16.0% when answer order changes and 12.9% when answer labels are relabeled ABCD→EFGH, undermining deployment reliability.

See: [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/knowledge_and_memory|Knowledge and Memory]]

---

## Approach: The Generate-Review-Revise-Answer Pipeline

KGARevion executes four actions per query:

### 1. Generate
The LLM is prompted to generate candidate knowledge triplets `(h, r, t)` from its own latent knowledge — not from retrieved graph content. This inverts the RAG paradigm into **generate-then-verify**.

To mitigate positional bias, the pipeline distinguishes:
- **Choice-aware questions** (multi-choice): triplets generated *per answer candidate* separately, preventing the LLM from being anchored by option ordering
- **Non-choice-aware questions** (yes/no): only the question stem is used for generation

### 2. Review
A fine-tuned verifier judges whether each generated triplet is factually consistent with the KG. The key technical contribution here is **bridging the representational gap** between pre-trained graph structural embeddings and LLM token space:

- Pre-trained TransE embeddings `(e_h, e_r, e_t) ∈ R^d` are kept frozen
- A trainable projection `g(·): R^d → R^{dL}` maps them into LLM embedding space via an attention block + two-layer FFN, producing aligned triplet embedding `Z ∈ R^{3×dL}`
- The LLM is fine-tuned with LoRA on a KG completion task (binary True/False next-token prediction), enabling structural + semantic reasoning about triplet correctness

### 3. Revise
Triplets flagged False are iteratively corrected up to `k` rounds. A **soft constraint rule** distinguishes:
- **Factually wrong**: both entities mappable in KG, triplet still False → remove
- **KG-incomplete**: entity not mappable → retain (prevents over-filtering due to KG gaps)

This handles the systematic incompleteness of biomedical KGs without discarding potentially valid LLM-generated knowledge.

### 4. Answer
Verified and revised triplets are used as grounded context for final answer generation.

See: [[themes/agent_systems|Agent Systems]], [[themes/knowledge_and_memory|Knowledge and Memory]]

---

## Results

### Core Benchmarks
KGARevion improves average accuracy over 15 baseline models across seven datasets:

| Setting | Gold-standard benchmarks | MedDDx benchmarks |
|---|---|---|
| Multi-choice | +5.2% average | +10.4% average |
| Open-ended | +8.8% to +18.0% | +14.9% to +18.4% |

With LLaMA3-8B on specific datasets: +5.2% MMLU-Med, +6.2% MedQA-US, +6.3% BioASQ-Y/N.

### Robustness to Complexity
KGARevion maintains stable accuracy as questions involve 1–6 medical concepts; baselines degrade sharply at 5–6 concepts.

### Positional Bias Reduction
LLM ordering sensitivity reduced from 8.4–16.0% accuracy shift to **1.5–2.5%** — a practically critical improvement for clinical deployment.

### Zero-Shot Generalization
On AfriMed-QA (released *after* training, covering underrepresented African healthcare contexts): +5.2% over LLaMA3.1-8B, +4.6% over GPT-4-Turbo.

### Ablation
- Review action alone: ~9% gain (multi-choice), ~4% (open-ended)
- Revise action adds: +3.3% on MedDDx (multi-choice), +3.0% (open-ended)
- Optimal revision rounds: k=1 for standard multi-choice; additional rounds benefit complex open-ended questions

See: [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]], [[themes/benchmark_design|Benchmark Design]]

---

## Limitations and Open Questions

### Architectural Gaps
- **Codified vs. tacit knowledge**: The fundamental integration gap between structured scientific knowledge and tacit clinical intuition (case-based experience, learned heuristics) remains unsolved. KGARevion reduces the gap but does not close it.
- **KG incompleteness**: Biomedical KGs have systematic structural holes — biologically similar entities may share no direct edges. The soft constraint rule *handles* this case but does not *resolve* it; relationships that should exist simply aren't captured. Horizon: 3–5 years to substantially address.
- **Entity linking gaps**: Not all LLM-generated triplet entities can be mapped to KG entities — a systematic mismatch between LLM latent knowledge and formal graph verification that the current pipeline works around rather than solves.

### Scaling and Deployment Concerns
- **Diminishing returns at scale**: Improvement over GPT-4-Turbo is only +2%, versus +6–7% over smaller LLMs — suggesting KG grounding may matter less as backbone capability increases, which raises questions about the approach's long-term leverage.
- **No clinical evaluation**: All results are on QA benchmarks; there is no evaluation on real clinical decision support scenarios, patient outcomes, clinician workflow integration, or safety-critical failure modes.
- **Non-monotonic revision returns**: k=1 is often optimal; additional revision rounds can *degrade* performance on established datasets, suggesting the Revise action has fragile convergence properties.

### Inherited Limitations
- **LLM knowledge biases**: LLMs generate more detailed information on familiar topics when all candidates are presented simultaneously — distorting choice-aware generation in systematic, hard-to-audit ways.
- **KG-RAG structural blindness**: Prior KG-RAG methods miss implicit multi-hop relationships; KGARevion sidesteps this by verifying LLM-generated triplets rather than traversing the graph, but this means it's bounded by what the LLM can generate, not what the KG structurally implies.

See: [[themes/medical_and_biology_ai|Medical and Biology AI]], [[themes/scientific_and_medical_ai|Scientific and Medical AI]]

---

## Key Bottlenecks Addressed

**Unverified retrieval in medical RAG** — KGARevion is the first demonstrated approach with a post-generation verification loop using grounded KG signal. Prior work retrieved and answered in a single pass with no factual feedback. *(Blocking: reliable clinical decision support; horizon: 1–2 years)*

**Representational mismatch between graph embeddings and LLM token space** — The projection architecture (TransE → attention+FFN → LoRA fine-tuning) is a concrete solution to a previously open problem of feeding structural graph knowledge into LLMs. *(Blocking: neural-symbolic integration for knowledge-intensive reasoning; horizon: 1–2 years)*

**KG incompleteness for biological relationships** — Partially addressed by the soft constraint rule, but the underlying problem of missing KG edges between biologically related entities remains a 3–5 year challenge requiring large-scale graph curation or completion.

---

## Connections

- **Agent systems**: KGARevion is a four-action agentic loop with structured state (generated triplets, verification results, revision history) — an early example of tool-augmented agents for domain-specific factual reasoning. [[themes/agent_systems|Agent Systems]]
- **RAG evolution**: Represents a structural shift from retrieve-then-answer to generate-then-verify — a paradigm inversion that could generalize beyond biomedical domains. [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]]
- **Benchmark design**: The MedDDx benchmarks (Introductory, Intermediate, Expert) are a methodological contribution — curated to test multi-concept differential diagnosis reasoning at graded complexity, filling a gap in existing medical QA evaluation. [[themes/benchmark_design|Benchmark Design]]
- **Neurosymbolic integration**: The TransE alignment architecture is an instance of the broader problem of grounding neural representations in symbolic structures — the approach here (frozen structural embeddings + learned projection + task-specific fine-tuning) is a reusable pattern. [[themes/knowledge_and_memory|Knowledge and Memory]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/lora|LoRA]]
