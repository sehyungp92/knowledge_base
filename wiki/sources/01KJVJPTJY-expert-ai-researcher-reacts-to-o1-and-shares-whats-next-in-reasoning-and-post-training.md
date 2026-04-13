---
type: source
title: Expert AI Researcher Reacts to o1 and Shares What's Next in Reasoning and
  Post-Training
source_id: 01KJVJPTJY
source_type: video
authors: []
published_at: '2024-09-18 00:00:00'
theme_ids:
- ai_business_and_economics
- knowledge_and_memory
- reasoning_and_planning
- retrieval_augmented_generation
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 15
tags: []
---
# Expert AI Researcher Reacts to o1 and Shares What's Next in Reasoning and Post-Training

> A founder of [[entities/retrieval-augmented-generation|RAG]] and CEO of Contextual AI analyses the o1 release as confirmation of a systems-over-models thesis, then traces the evolution of post-training from RLHF through DPO, KTO, CLAIR, and APO — arguing that post-training is where practical AI value is created and that alignment methods have fundamental data-quality problems that newer algorithms are only beginning to address.

**Authors:** Douwe Kiela (Contextual AI)
**Published:** 2024-09-18
**Type:** video
**Library:** `library/01KJVJPTJY/`

---

## o1 as Systems Signal

The o1 release is interpreted not primarily as a model advance but as evidence that [[themes/test_time_compute_scaling|test-time compute scaling]] via compressed chain-of-thought works — and that the field is beginning to think in systems terms rather than model terms. From the perspective of someone who co-invented RAG, this directional shift is more significant than the specific capabilities demonstrated.

The key observation: o1 compresses chain-of-thought reasoning into the model weights using RLHF, effectively encoding a system-level behaviour (multi-step deliberation) into a model-level artifact. This was expected — similar ideas had been circulating, and other labs including Contextual had been working on analogous retrieval-side compression. The notable thing is execution: OpenAI demonstrates reliably that compressed deliberative reasoning works at frontier scale.

Two immediate caveats follow. First, **latency is a deployment ceiling**, not a benchmark: reasoning quality at the cost of seconds-to-minutes response time is not viable for most real-time enterprise use cases, regardless of capability. Future models that require hours of wait time for complex long-context reasoning are plausible, but they serve fundamentally different use cases from current interactive deployments. Second, o1-style models are dominant on math and law benchmarks but *weaker* on other tasks compared to prior models — and significantly slower. The capability-latency tradeoff means most production deployments will not follow the o1 architecture.

---

## The Systems-Over-Models Thesis

Contextual AI's founding thesis is that **a model should represent approximately 10–20% of a full enterprise AI system**; the surrounding system — extraction, retrieval, contextualisation, verification, evaluation — is where most of the value is created and where most failures occur.

This is a direct challenge to the standard model-centric framing where capability improvements are assumed to be downstream of model improvements. The argument: enterprises need to acquire a system that works reliably in their specific context, not a model that scores well on generic benchmarks. OpenAI's o1 direction (compressing system behaviours into models) is acknowledged as technically interesting but is read as a continued commitment to model centrism — everything funnelled into the model weights — whereas Contextual's architecture keeps the components explicit and tunable.

The complementary thesis is **specialisation over generalisation**. AGI is framed as a consumer product problem: you need general intelligence when you don't know what the user wants. Enterprises know exactly what they want, and a generalist model that needs to be constrained back down to regulatory compliance and domain specificity is less efficient than a system specialised upfront. For regulated industries (banking, insurance, EU-regulated HR processes), this is not a preference — it is a requirement.

> *"A model is maybe 10–20% of this much bigger system that has to solve the problem."*

The full stack of a production enterprise AI system, as described here:
1. **Extraction** — parsing documents (especially PDFs) into structured, retrievable content. Currently unsolved in open-source; Contextual had to build their own.
2. **Retrieval** — a mixture-of-retrievers approach rather than a single vector database, combining dense, sparse, and structured retrieval mechanisms.
3. **Contextualisation** — grounding the language model response in retrieved content.
4. **Verification and evaluation** — assessing output accuracy and risk before or after delivery to users.

Each component has non-trivial engineering depth. The widespread assumption that RAG is a plug-and-play solution masks the difficulty at the extraction and evaluation ends.

---

## The Alignment Frontier: From RLHF to APO

The post-training discussion traces a lineage of alignment algorithms, each motivated by a specific problem with its predecessor.

### RLHF and Its Two Failure Modes

[[themes/reinforcement_learning|RLHF]] was the capability unlock for ChatGPT — specifically, it captured human preferences at the full sequence level rather than the next-token level, which is what instruction-tuning alone cannot do. But RLHF has two structural problems:

1. **Reward model overhead.** Training a reward model that is good enough to propagate useful gradients is expensive, and that model is discarded after training — a large fixed cost for each training run.
2. **Preference data annotation cost.** Generating a useful thumbs-down signal in production requires: noticing the failure, routing it to an annotation team, specifying what the better response would have looked like, and feeding that back. This is slow and expensive at scale, and becomes effectively prohibitive for narrow enterprise domains where few annotators have the necessary expertise.

### DPO and KTO: Eliminating the Reward Model

Direct Preference Optimization (DPO) reformulates RLHF to train directly on preference pairs without a separate reward model, making the process more efficient. KTO (Kahneman-Tversky Optimization) goes further: it breaks the dependency on preference *pairs*, enabling direct optimization from individual user signals (a single thumbs-up or thumbs-down) without requiring annotated comparisons. This is critical for production deployment, where users generate thumbs-down signals but not paired preference annotations.

> *"We have a thumbs up thumbs down mechanism and we can learn from that very directly using our algorithms which you couldn't really do with standard RLHF."*

### CLAIR: Injecting Causal Structure

Standard preference datasets have a deep problem: **they capture rankings without capturing causal reasons.** A preference pair tells the model that response A is better than response B, but not *why* — which specific properties make A better. This under-specification means the model may learn superficial correlates of quality rather than the properties that actually matter.

CLAIR (Contrastive Revisions Alignment) addresses this by constructing preference pairs as contrasted revisions: take response A, identify something wrong with it, fix it to produce response B, and now the preference pair has a tight, causally grounded signal — "this specific change is what makes B better than A." The training signal encodes the improvement mechanism rather than just the outcome ranking.

### APO: Accounting for Model-Data Quality Mismatch

Anchored Preference Optimization (APO) addresses a problem that has become practically relevant as frontier models improve: **the model being trained may be better than the preference data it is learning from.** Standard RLHF and DPO assume the preferred response in the training data is genuinely better than what the model would produce — but if the model has already surpassed the data annotators, this assumption fails and the model learns incorrectly from inferior examples.

APO accounts for the quality relationship between the model being trained and the preference data quality, adjusting learning signals accordingly. This is not a theoretical edge case: as of late 2024, it is "kind of a crazy idea but possible."

---

## Where Enterprise AI Is Actually Stuck

The most direct signal in this source is not about capabilities — it is about where the enterprise AI stack consistently fails in production.

### PDF Extraction

Extracting structured information from PDFs — handling OCR, layout detection, multi-column formats, embedded tables, footnotes, metadata — remains unsolved in open-source tooling. For an enterprise RAG system, this is a prerequisite: if extraction fails, retrieval fails, and model accuracy is irrelevant. Contextual had to build their own extraction pipeline rather than use available tools. This is a significant hidden infrastructure cost that most enterprise AI evaluations do not surface.

### System Evaluation

Enterprise AI system evaluation has no standardised methodology. The current state: most enterprises use ad-hoc spreadsheets with ~50 examples and high variance across evaluators. This is insufficient to confidently assess production safety, accuracy, or regulatory compliance. The problem has two components: (a) enterprises often do not know what success looks like before beginning deployment — defining the evaluation set requires understanding the task, which requires iterating with the customer; and (b) even with a well-defined evaluation set, there is no standard framework for tracking system-level metrics across the full stack.

> *"I'm worried that a lot of people are not taking evaluation seriously enough."*

The recommended approach: engage with customers in a prototype setting to hill-climb toward a shared definition of success, then productionise. This is operationally expensive and does not scale like a standard SaaS product.

### High-Stakes Decision Automation

High-value use cases — investment decisions, hiring, performance reviews, medical triage — are precisely the ones where AI output cannot be directly exposed to customers or applied without human review. The risk scales with business value. This creates a structural constraint: the most economically attractive AI applications are the ones where current reliability is insufficient for autonomous deployment, and the timeline to sufficient reliability for high-stakes autonomous operation is 3–5 years minimum for regulated domains.

---

## The Transformer Architecture's Hidden Dependency

A structural observation that cuts across the field: **Transformer success is substantially explained by GPU hardware compatibility, not algorithmic superiority.** GPUs are optimised for the specific matrix operations that Transformers require; Transformers became dominant partly because they are optimal for GPUs, and GPUs became the dominant AI hardware because they were already being built for graphics workloads. The architecture-hardware co-evolution is a form of path dependency that may not reflect the most capable architecture on alternative hardware.

This matters for the [[themes/model_architecture|model architecture]] landscape: the dominance of Transformers should not be read as evidence that Transformers are the best possible architecture for cognition, only that they are the best possible architecture for current hardware.

---

## Post-Training as the Primary Value Layer

The overarching argument: post-training is where most practical AI value is created. Pre-training produces a capable base model; post-training determines whether it is useful, safe, aligned to specific objectives, and deployable in a given context. The alignment methods discussion (RLHF → DPO → KTO → CLAIR → APO) is a lineage of successive attempts to make post-training cheaper, more data-efficient, and better specified — and each iteration is motivated by a concrete failure mode of its predecessor.

The reflection on chain-of-thought prompting is instructive: it was initially dismissed by the academic ML community as not a "real" algorithmic contribution, but it turned out to be one of the highest-value engineering insights of the era. This suggests that practical, systems-level contributions may be systematically undervalued during the period when they are developed.

---

## Landscape Connections

This source provides primary evidence for the [[themes/test_time_compute_scaling|test-time compute scaling]] theme's latency constraint — the capability-latency tradeoff is not merely a current limitation but a structural consequence of deliberative computation that will require new deployment paradigms (asynchronous UIs, long-running jobs) rather than engineering workarounds.

The post-training algorithm lineage (RLHF → DPO → KTO → CLAIR → APO) maps directly to the [[themes/alignment_methods|alignment methods]] theme, with CLAIR and APO representing the current research frontier. The under-specification problem in preference data connects to the [[themes/evaluation_and_benchmarks|evaluation and benchmarks]] theme: if training signal is under-specified, benchmark performance may not reflect the specific properties the practitioner cares about.

The systems-over-models thesis and enterprise specialisation argument are central to the [[themes/vertical_ai_and_saas_disruption|vertical AI and SaaS disruption]] theme — the claim that specialised, integrated systems outperform general-purpose models in enterprise settings has direct implications for which companies will capture enterprise AI value.

The mixture-of-retrievers architecture and extraction bottlenecks are primary evidence for the [[themes/retrieval_augmented_generation|retrieval augmented generation]] theme's current limitations. The PDF extraction gap is a concrete, unresolved bottleneck that affects every enterprise RAG deployment.

---

## Key Open Questions

- Can preference data collection be automated with sufficient fidelity to replace manual annotation at scale without inheriting the bias of the automated judge?
- Does CLAIR's causal revision structure generalize to domains other than natural language quality (e.g., code correctness, factual accuracy)?
- What is the practical reliability threshold for autonomous AI deployment in regulated domains — and what evidence standard would be required to establish it?
- Is the 10–20% model / 80–90% system framing stable as models become more capable, or does the optimal system composition shift as model capability increases?
- Can enterprise AI evaluation be standardised without losing the domain specificity that makes bespoke evaluation sets valuable?
- What alternative architectures might be better suited to non-GPU hardware, and how would a shift in hardware substrate affect the Transformer dominance?

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/post-training|Post-training]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/retrieval-augmented-generation|Retrieval-Augmented Generation]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/test-time-compute|Test-time compute]]
- [[entities/multi-agent-systems|multi-agent systems]]
